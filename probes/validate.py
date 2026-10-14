import random, sys, collections
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *

DECIDED = ("PASS", "FAIL")
TALLY = collections.Counter()   # (fn name, verdict class) -> number of retry() calls

def attempt_cap(pts, attempts=None):
    """Attempts per trial. Each independent sqrt point is a QR mod p with probability 1/2, so a
    configuration with m of them needs ~2^m attempts. Cap = 20*2^m (failure prob ~e^-20), floor 200,
    ceiling 20000. m = number of points tagged `is_sqrt` (a conservative upper bound: mirror pairs
    share one radicand)."""
    if attempts is not None: return attempts
    m = sum(1 for p in pts if getattr(p, "is_sqrt", False))
    return min(max(200, 20 * 2 ** m), 20000)

def retry(fn, pts, k, d, trials=2, rng=None, attempts=None):
    """PASS / FAIL / MIXED{True, False} (both outcomes seen) / NO_VERDICT (every attempt raised
    ValueError: no information; never PASS, never FAIL, never agreement).
    rng: a seeded random.Random for the mod-p specialization (default: probe2's global `random`)."""
    cap = attempt_cap(pts, attempts)
    kw = {} if rng is None else {"rng": rng}
    out = set()
    for _ in range(trials):
        for _ in range(cap):
            try:
                out.add(fn(pts, k, d, **kw)); break
            except ValueError:
                continue
    if not out: res = "NO_VERDICT"
    elif out == {True}: res = "PASS"
    elif out == {False}: res = "FAIL"
    else: res = f"MIXED{out}"
    TALLY[(fn.__name__, res if res in DECIDED or res == "NO_VERDICT" else "MIXED")] += 1
    return res

def tally_line():
    """One summary line of every retry() verdict class, per test function."""
    names = sorted({n for n, _ in TALLY})
    parts = [n + " " + " ".join(f"{c}={TALLY[(n, c)]}" for c in ("PASS", "FAIL", "NO_VERDICT", "MIXED")) for n in names]
    return "# retry tally: " + "; ".join(parts)

def indep_circle(j, offset=0):
    return [(lambda jj: (lambda th: circ(th[jj])))(offset + i) for i in range(j)]

rats = [rat_circ(a, b) for a, b in [(0,1),(1,2),(1,3),(2,3),(3,4),(1,5),(2,5),(3,5),(4,5),(1,7),(3,7),(5,7)]]
Q0 = [(1,0),(P-1,0),(0,1),(0,P-1)]
def sq(sign):
    def mk(q):
        def f(th):
            t = th[0]; u, v = circ(t)
            x, y = q
            return [u*x - v*y, v*x + u*y] if sign > 0 else [u*x + v*y, -v*x + u*y]
        return f
    return [mk(q) for q in Q0]
three_squares = sq(1) + sq(-1) + [const_point(list(q)) for q in Q0]

def palv():
    pts = [const_point([P-1, 0])]
    for j in (1, 3, 4):
        for sg in (1, -1):
            def f(th, j=j, sg=sg):
                r = th[0]
                return [(j - r) / r, sg * sqrt(j * (2 * r - j)) / r]
            f.is_sqrt = True
            pts.append(f)
    return pts

mob = lambda g: (lambda th: circ(g(th[0])))
if __name__ == "__main__":
    cases = [
      ("5 independent circle pts (<=5 => Ramsey)", indep_circle(5), 5, 2, "PASS"),
      ("OAI 12-pt three squares (non-Ramsey)", three_squares, 1, 2, "FAIL"),
      ("9 independent circle pts (OAI 7.6, non-Ramsey)", indep_circle(9), 9, 2, "FAIL"),
      ("Palvolgyi heptagon, r transcendental (non-Ramsey)", palv(), 1, 2, "FAIL"),
      ("5 rat + circ(t),circ(t+1),circ(2t),circ(1/t) (det!=0)", rats[:5] + [mob(lambda t:t), mob(lambda t:t+1), mob(lambda t:2*t), mob(lambda t:1/t)], 1, 2, "FAIL"),
      ("5 rat + circ(kt), k=1..4 (expected Ramsey)", rats[:5] + [mob(lambda t,c=c: c*t) for c in (1,2,3,4)], 1, 2, "PASS?"),
      ("circ(kt) k=1..7 (certificate found)", [mob(lambda t,c=c: c*t) for c in range(1,8)], 1, 2, "PASS"),
      ("6 rat + circ(t) (certificate found)", rats[:6] + [mob(lambda t: t)], 1, 2, "PASS"),
    ]
    srng = random.Random(101)   # specialization RNG (explicit seed; reproducible counts)
    for name, pts, k, d, exp in cases:
        j = retry(jet2, pts, k, d, rng=srng)
        c = retry(curve_probe, pts, k, d, rng=srng) if (len(pts) <= 12 and k <= 9) else "-"
        print(f"{name:55s} expect {exp:6s} | 2-jet {j:5s} | curve {c}"); sys.stdout.flush()
    print(tally_line())
