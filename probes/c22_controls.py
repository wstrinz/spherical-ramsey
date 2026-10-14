"""Controls for C-13 / C-22 after c13_c22_seven.py found every structured 2-parameter
lattice 7-set PASSing.  Question: do low-parameter 7-sets FAIL at all without square roots?

applies_to: 7-point subsets of the unit circle whose stereographic parameters are rational
  functions (degree 1 or 2, small integer coefficients) of k = 1, 2, 3, 4 real parameters, mixed with
  rational points.  No square roots: real for real parameters, no realness filter needed.
  EXACT two-group test as in c13_c22_seven.py (dual numbers over Q; non-constancy exact).

[PROBE] 2-jet and curve probe (full criterion for k = 1, necessary for k >= 2), seeded.
usage: python -I c22_controls.py
"""
import os, sys, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)   # probe2, validate and the sibling scripts live next to this file
from fractions import Fraction
import sympy as sp
from probe2 import *
from validate import retry, tally_line
from c13_c22_seven import Dual, cr

def make_spec(rng, k, kind):
    """kind: 'rat' | 'mob' (degree 1 in one variable) | 'mix' (degree 1 in all variables) | 'deg2'."""
    if kind == "rat":
        return ("rat", Fraction(rng.randint(-7, 7), rng.randint(1, 7)))
    v = rng.randrange(k)
    c = [rng.randint(-4, 4) for _ in range(6)]
    if kind == "mob":
        if c[0] * c[3] - c[1] * c[2] == 0: c[0], c[3] = 1, 1
        return ("mob", v, c)
    if kind == "mix":
        return ("mix", c, [rng.randint(-3, 3) for _ in range(2 * k + 2)])
    return ("deg2", v, c)

def ev(spec, X, one=1):
    """evaluate a spec's stereographic parameter at the variable list X (Dual, J or PS)."""
    if spec[0] == "rat":
        return spec[1]
    if spec[0] == "mob":
        _, v, c = spec; t = X[v]
        return (c[0] * t + c[1]) / (c[2] * t + c[3])
    if spec[0] == "mix":
        _, c, w = spec; n = len(X)
        num = w[2 * n] + sum(w[i] * X[i] for i in range(n)) + 0 * X[0]
        den = 1 + sum(w[n + i] * X[i] for i in range(n)) + 0 * X[0]
        return num / den
    _, v, c = spec; t = X[v]
    return (c[0] * t * t + c[1] * t + c[2]) / (c[3] * t + c[4] + 0 * t if c[3] or c[4] else 1 + 0 * t)

def two_group(specs, k, rng):
    """EXACT non-constancy; returns (two_group?, trdeg of CR field)."""
    for _ in range(50):
        X0 = [Fraction(rng.randint(-50, 50), rng.randint(1, 50)) for _ in range(k)]
        try:
            X = []
            for i in range(k):
                d = [0] * k; d[i] = 1
                X.append(DualK(X0[i], d))
            S = []
            for sp_ in specs:
                s = ev(sp_, X)
                S.append(s if isinstance(s, DualK) else DualK(Fraction(s), [0] * k))
            if len({s.v for s in S}) < 7: continue
            C = [cr(*[S[i] for i in q]) for q in itertools.combinations(range(7), 4)]
            const = any(all(x == 0 for x in c.d) for c in C)
            trd = sp.Matrix([list(c.d) for c in C]).rank()
            return const, trd
        except ZeroDivisionError:
            continue
    return None, None

class DualK:
    def __init__(s, v, d):
        s.v = Fraction(v); s.d = [Fraction(x) for x in d]
    def _c(s, o): return o if isinstance(o, DualK) else DualK(o, [0] * len(s.d))
    def __add__(s, o): o = s._c(o); return DualK(s.v + o.v, [a + b for a, b in zip(s.d, o.d)])
    __radd__ = __add__
    def __sub__(s, o): o = s._c(o); return DualK(s.v - o.v, [a - b for a, b in zip(s.d, o.d)])
    def __rsub__(s, o): return s._c(o) - s
    def __mul__(s, o): o = s._c(o); return DualK(s.v * o.v, [a * o.v + s.v * b for a, b in zip(s.d, o.d)])
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = s._c(o)
        if o.v == 0: raise ZeroDivisionError
        q = s.v / o.v
        return DualK(q, [(a - q * b) / o.v for a, b in zip(s.d, o.d)])
    def __rtruediv__(s, o): return s._c(o) / s

def pt_fn(spec):
    if spec[0] == "rat":
        q = spec[1]
        return rat_circ(q.numerator, q.denominator)
    return lambda th: circ(ev(spec, th))

if __name__ == "__main__":
    rng = random.Random(7099)
    srng = random.Random(7098)
    plan = [(1, "mob", 60), (1, "deg2", 40), (2, "mob", 60), (2, "mix", 40), (3, "mob", 40), (4, "mob", 30)]
    for k, kind, count in plan:
        tally = {}
        for _ in range(count):
            nrat = rng.randint(0, 3)
            specs = [make_spec(rng, k, "rat") for _ in range(nrat)] + [make_spec(rng, k, kind) for _ in range(7 - nrat)]
            tg, trd = two_group(specs, k, rng)
            if tg is None:
                continue
            pts = [pt_fn(s) for s in specs]
            j = retry(jet2, pts, k, 2, trials=1, rng=srng)
            c = retry(curve_probe, pts, k, 2, trials=1, rng=srng)
            key = (f"trdeg={trd}", "two-group" if tg else "not-two-group", f"2jet={j}", f"curve={c}")
            tally[key] = tally.get(key, 0) + 1
            if (not tg) and j == "FAIL" and c == "PASS":
                print("   note: 2-jet FAIL but curve PASS:", specs)
        print(f"k={k} kind={kind}: " + "; ".join(f"{'/'.join(key)}: {n}" for key, n in sorted(tally.items())))
        sys.stdout.flush()
    print(tally_line())
