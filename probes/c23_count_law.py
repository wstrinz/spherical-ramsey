"""Fresh test of C-23 (expected-dimension law on the circle), run after the conjecture was
stated.  Prediction per configuration: two-group => PASS (B(c), proved); otherwise
PASS iff (n - 5)(k + 1) <= 6, k = transcendence degree of the cross-ratio field.

applies_to: n-point subsets of the unit circle (n = 6..9) whose stereographic parameters are rational
  functions (Mobius in one variable, or angle sums a th + b ph + c ps via the tangent addition
  formula) of up to 4 real parameters, plus rational points.  No square roots: real configurations,
  no realness filter needed.  Purely transcendental coordinate field by construction.

EXACT: k (Jacobian rank of all 4-point cross-ratios at a rational point, exact dual numbers) and the
two-group test (all 2-part partitions; a part is a group if <= 3 points or every 4-subset has a
cross-ratio with zero gradient at 3 random rational points: non-zero is exact, zero is probabilistic).
[PROBE]: 2-jet (necessary; with C-1 the full test) and curve probe (full criterion only for k = 1).
usage: python -I c23_count_law.py
"""
import os, sys, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)   # probe2, validate and the sibling scripts live next to this file
from fractions import Fraction
import sympy as sp
from probe2 import *
from validate import retry, tally_line
from c22_controls import make_spec, ev, DualK, pt_fn
from c13_c22_seven import cr

def lattice_spec(coeffs):
    return ("lat", tuple(coeffs))

def ev2(spec, X):
    if spec[0] != "lat":
        return ev(spec, X)
    s = 0
    for v, c in enumerate(spec[1]):
        for _ in range(c):
            s = X[v] if (isinstance(s, int) and s == 0) else (s + X[v]) / (1 - s * X[v])
    return s

def pt_fn2(spec):
    if spec[0] != "lat":
        return pt_fn(spec)
    def f(th):
        s = ev2(spec, th)
        return [1, 0] if isinstance(s, int) else circ(s)
    return f

def mirror_specs(rng):
    """{0, +-r1(t), +-r2(t), +-r3(t)} with r_i Mobius in t: reflection s -> -s is y -> -y."""
    out = [("rat", Fraction(0))]
    for _ in range(3):
        c = [rng.randint(-4, 4) for _ in range(4)]
        if c[0] * c[3] - c[1] * c[2] == 0: c[0], c[3] = 1, 1
        out.append(("mob", 0, c + [0, 0]))
        out.append(("mob", 0, [-c[0], -c[1], c[2], c[3], 0, 0]))
    return out

def classify(specs, k, rng):
    n = len(specs)
    quads = list(itertools.combinations(range(n), 4))
    flags = None; jac = None
    for trial in range(3):
        for _ in range(60):
            X0 = [Fraction(rng.randint(-50, 50), rng.randint(1, 50)) for _ in range(k)]
            try:
                X = [DualK(X0[i], [1 if j == i else 0 for j in range(k)]) for i in range(k)]
                S = []
                for s_ in specs:
                    v = ev2(s_, X)
                    S.append(v if isinstance(v, DualK) else DualK(Fraction(v), [0] * k))
                if len({s.v for s in S}) < n: continue
                C = [cr(*[S[i] for i in q]) for q in quads]
                break
            except ZeroDivisionError:
                continue
        else:
            return None
        f = [all(x == 0 for x in c.d) for c in C]
        flags = f if flags is None else [a and b for a, b in zip(flags, f)]
        if jac is None:
            jac = [list(c.d) for c in C]
    trd = sp.Matrix(jac).rank()
    const = dict(zip(quads, flags))
    def is_group(part):
        return len(part) <= 3 or all(const[q] for q in itertools.combinations(sorted(part), 4))
    two = False
    for mask in range(1 << (n - 1)):
        G = [i for i in range(n) if mask >> i & 1]
        H = [i for i in range(n) if not mask >> i & 1]
        if is_group(G) and is_group(H):
            two = True; break
    return trd, two

def run(name, gen, count, k, rng, srng):
    tally = {}; bad = []
    for _ in range(count):
        specs = gen()
        c = classify(specs, k, rng)
        if c is None: continue
        trd, two = c
        n = len(specs)
        pred = "PASS" if (two or (n - 5) * (trd + 1) <= 6) else "FAIL"
        pts = [pt_fn2(s) for s in specs]
        j = retry(jet2, pts, k, 2, trials=1, rng=srng)
        cv = retry(curve_probe, pts, k, 2, trials=1, rng=srng) if k == 1 else "-"
        obs = j if k > 1 else (j if j == cv else f"2jet {j}/curve {cv}")
        ok = (obs == pred)
        key = (f"n={n}", f"k={trd}", "two" if two else "not-two", f"pred={pred}", f"obs={obs}")
        tally[key] = tally.get(key, 0) + 1
        if not ok: bad.append((specs, trd, two, pred, obs))
    print(f"== {name}")
    for key, v in sorted(tally.items()):
        print("   " + " ".join(key) + f": {v}")
    for b in bad:
        print("   MISMATCH:", b)
    sys.stdout.flush()
    return len(bad)

if __name__ == "__main__":
    rng = random.Random(7230)
    srng = random.Random(7231)
    def rand_family(n, k, kind="mob", maxrat=3):
        def g():
            nrat = rng.randint(0, maxrat)
            return [make_spec(rng, k, "rat") for _ in range(nrat)] + [make_spec(rng, k, kind) for _ in range(n - nrat)]
        return g
    def lattice(n, k, top=3):
        grid = list(itertools.product(range(top + 1), repeat=k))
        return lambda: [lattice_spec(c) for c in rng.sample(grid, n)]
    bad = 0
    bad += run("n=8, one parameter (pred PASS)", rand_family(8, 1), 40, 1, rng, srng)
    bad += run("n=9, one parameter (pred FAIL unless two-group)", rand_family(9, 1), 40, 1, rng, srng)
    bad += run("n=8, two parameters (pred FAIL unless two-group or k<=1)", rand_family(8, 2), 40, 2, rng, srng)
    bad += run("n=8, lattice {a th + b ph} (pred FAIL unless k<=1/two-group)", lattice(8, 2), 25, 2, rng, srng)
    bad += run("n=7, lattice {a th + b ph + c ps} (pred FAIL if k=3)", lattice(7, 3, 2), 25, 3, rng, srng)
    bad += run("n=7, mirror-symmetric {0, +-r_i(t)} (pred PASS)", lambda: mirror_specs(rng), 30, 1, rng, srng)
    bad += run("n=6, three parameters (control, B(a): PASS)", rand_family(6, 3), 20, 3, rng, srng)
    bad += run("n=9, lattice one parameter {a th}, a<=12 (pred FAIL unless two-group)", lattice(9, 1, 12), 20, 1, rng, srng)
    print(f"TOTAL MISMATCHES vs C-23 prediction: {bad}")
    print(tally_line())
