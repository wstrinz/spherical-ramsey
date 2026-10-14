"""Sanity checks for C-13 (naive 7-point two-group classification) and C-22 (its refinement
above transcendence degree 1).  The conjectures were stated before this script was run.

applies_to: finite subsets of the unit circle whose stereographic parameters are rational functions
  of one or two real parameters theta, phi (angles a*theta + b*phi, via tan((a th + b ph)/2) built by
  the tangent addition formula from t = tan(th/2), u = tan(ph/2)).  No square roots, so every member
  with real transcendental (t, u) is a real configuration: the realness filter (realness.py) is not needed.

Part A (EXACT, sympy): the 35 four-point cross-ratios of the radian 7-gon {z^k : k <= 6} are
  non-constant rational functions of z, so at transcendental z = e^{i theta} none is algebraic:
  the radian 7-gon is not a two-group set.
Part B ([PROBE], mod p, seeded): radian n-gons, n = 6..9, 2-jet and curve probe (k = 1: the curve
  probe is the full one-parameter criterion mod p).
Part C (C-22): structured two-parameter 7-sets.  EXACT: transcendence degree of the cross-ratio
  field = rank of the Jacobian of the 35 cross-ratios w.r.t. (t, u) at a rational point (rank at a
  point <= generic rank <= 2, so rank 2 at a point is exact); two-group = some 4-subset has a constant
  cross-ratio (constancy: both partial derivatives vanish at 3 random rational points -- non-vanishing
  is exact, vanishing is probabilistic and flagged).  [PROBE]: 2-jet (k = 2) and curve probe.

usage: python -I c13_c22_seven.py
"""
import os, sys, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)   # probe2 and validate live next to this file
import sympy as sp
from fractions import Fraction
from probe2 import *
from validate import retry, tally_line

z = sp.symbols("z")

# ---------------------------------------------------------------- part A
def partA():
    print("== Part A (EXACT): radian 7-gon cross-ratios as functions of z = e^{i theta}")
    nonconst = 0
    for a, b, c, d in itertools.combinations(range(7), 4):
        cr = sp.cancel((z**a - z**c) * (z**b - z**d) / ((z**a - z**d) * (z**b - z**c)))
        if sp.cancel(sp.diff(cr, z)) != 0:
            nonconst += 1
        else:
            print("  CONSTANT cross-ratio on", (a, b, c, d), "=", cr)
    print(f"  non-constant: {nonconst}/35  => radian 7-gon has no algebraic 4-point cross-ratio: {nonconst == 35}")

# ---------------------------------------------------------------- exact dual numbers over Q
class Dual:
    """value + first derivatives w.r.t. (t, u), exact over Q (Fractions)."""
    def __init__(s, v, d=(0, 0)):
        s.v = Fraction(v); s.d = (Fraction(d[0]), Fraction(d[1]))
    def _c(s, o): return o if isinstance(o, Dual) else Dual(o)
    def __add__(s, o): o = s._c(o); return Dual(s.v + o.v, (s.d[0] + o.d[0], s.d[1] + o.d[1]))
    __radd__ = __add__
    def __sub__(s, o): o = s._c(o); return Dual(s.v - o.v, (s.d[0] - o.d[0], s.d[1] - o.d[1]))
    def __rsub__(s, o): return s._c(o) - s
    def __mul__(s, o):
        o = s._c(o); return Dual(s.v * o.v, (s.d[0] * o.v + s.v * o.d[0], s.d[1] * o.v + s.v * o.d[1]))
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = s._c(o)
        if o.v == 0: raise ZeroDivisionError
        q = s.v / o.v
        return Dual(q, ((s.d[0] - q * o.d[0]) / o.v, (s.d[1] - q * o.d[1]) / o.v))

def stereo(a, b, T, U):
    """tan((a th + b ph)/2) from T = tan(th/2), U = tan(ph/2) by the addition formula (exact or mod p)."""
    s = 0
    for _ in range(a):
        s = T if (isinstance(s, int) and s == 0) else (s + T) / (1 - s * T)
    for _ in range(b):
        s = U if (isinstance(s, int) and s == 0) else (s + U) / (1 - s * U)
    return s

def point_fn(a, b):
    def f(th):
        s = stereo(a, b, th[0], th[1] if len(th) > 1 else None)
        if isinstance(s, int):
            return [1, 0]          # angle 0: the point (1, 0), stereographic parameter 0
        return circ(s)
    return f

def cr(s1, s2, s3, s4):
    return (s1 - s3) * (s2 - s4) / ((s1 - s4) * (s2 - s3))

def analyse(lattice, rng):
    """EXACT transcendence degree of the cross-ratio field (Jacobian rank at a rational point) and
    two-group status (some 4-subset with both partials zero at 3 random rational points).
    Returns (trdeg, two_group)."""
    jac_rows, const = None, None
    for trial in range(3):
        while True:
            T0 = Fraction(rng.randint(-40, 40), rng.randint(1, 40)); U0 = Fraction(rng.randint(-40, 40), rng.randint(1, 40))
            try:
                S = [stereo(a, b, Dual(T0, (1, 0)), Dual(U0, (0, 1))) for a, b in lattice]
                S = [x if isinstance(x, Dual) else Dual(0) for x in S]
                if len({x.v for x in S}) < 7: continue
                C = [cr(*[S[i] for i in q]) for q in itertools.combinations(range(7), 4)]
                break
            except ZeroDivisionError:
                continue
        flags = [c.d == (0, 0) for c in C]
        const = flags if const is None else [x and y for x, y in zip(const, flags)]
        if jac_rows is None:
            jac_rows = [[c.d[0], c.d[1]] for c in C]
    trdeg = sp.Matrix(jac_rows).rank()
    return trdeg, any(const)

def partB(srng):
    print("== Part B ([PROBE]): radian n-gons, k = 1 (curve probe = full criterion mod p)")
    for n in range(6, 10):
        pts = [point_fn(k, 0) for k in range(n)]
        j = retry(jet2, pts, 1, 2, rng=srng)
        c = retry(curve_probe, pts, 1, 2, rng=srng)
        print(f"  radian {n}-gon: 2-jet {j:10s} curve {c}")

FAMILIES = {
    "L1 {0,th,2th,ph,th+ph,2th+ph,2ph}": [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2)],
    "L2 {0..3}th u ph+{0..2}th": [(0,0),(1,0),(2,0),(3,0),(1,1),(2,1),(0,1)],
    "L3 radian 6-gon + ph": [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(0,1)],
    "L4 {0..3}th u {1..3}ph": [(0,0),(1,0),(2,0),(3,0),(0,1),(0,2),(0,3)],
    "L5 radian 5-gon + {ph, ph+th}": [(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(1,1)],
    "L6 {0,th,ph,th+ph,2th,2ph,2th+2ph}": [(0,0),(1,0),(0,1),(1,1),(2,0),(0,2),(2,2)],
}

def partC(srng, arng):
    print("== Part C (C-22): two-parameter 7-sets: trdeg(CR field) EXACT, two-group, 2-jet / curve [PROBE]")
    fams = dict(FAMILIES)
    grid = [(a, b) for a in range(4) for b in range(4)]
    for i in range(40):
        fams[f"R{i:02d} random 7-subset of {{a th + b ph : a,b <= 3}}"] = sorted(arng.sample(grid, 7))
    counts = {}
    for name, lat in fams.items():
        trd, two = analyse(lat, arng)
        pts = [point_fn(a, b) for a, b in lat]
        j = retry(jet2, pts, 2, 2, rng=srng)
        c = retry(curve_probe, pts, 2, 2, rng=srng)
        tag = ""
        if trd >= 2 and not two and j == "PASS":
            tag = "  <== C-22 COUNTER-CANDIDATE"
        if two and j == "FAIL":
            tag = "  <== two-group FAIL (contradicts B(c)! check)"
        key = (trd, two, j)
        counts[key] = counts.get(key, 0) + 1
        print(f"  {name:48s} lattice={lat} trdeg={trd} two-group={two} | 2-jet {j:10s} curve {c}{tag}")
        sys.stdout.flush()
    print("  summary (trdeg, two-group, 2-jet) -> count:", dict(sorted(counts.items(), key=str)))

if __name__ == "__main__":
    srng = random.Random(7013)   # specialization RNG (explicit seed; reproducible counts)
    arng = random.Random(7022)   # family sampling / exact evaluation points
    partA()
    partB(srng)
    partC(srng, arng)
    print(tally_line())
