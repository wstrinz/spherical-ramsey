import sys, random, time
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry, tally_line
rng = random.Random(41)
srng = random.Random(241)   # specialization RNG, explicit seed (reproducible counts)
def mob_sphere(u0, o, d):
    """Mobius map of S^{d-1} in stereographic coords: u -> lam*(u-c)/|u-c|^2 + b, params lam,c,b"""
    m = d - 1
    def f(th):
        lam = th[o]; c = th[o+1:o+1+m]; b = th[o+1+m:o+1+2*m]
        w = [u0[i] - c[i] for i in range(m)]
        n2 = 0
        for x in w: n2 = n2 + x * x
        v = [lam * w[i] / n2 + b[i] for i in range(m)]
        return sph(v)
    return f
def rat_u(m): return [R(rng.randint(-6, 6), rng.randint(1, 5)) for _ in range(m)]
for d, sizes in [(3, (6, 6)), (4, (8, 8)), (3, (4, 4, 4)), (4, (6, 6, 6)), (5, (11, 11))]:
    np_ = 2 * d - 1
    pts = []
    for g, sz in enumerate(sizes):
        pts += [mob_sphere(rat_u(d - 1), g * np_, d) for _ in range(sz)]
    t0 = time.time()
    v = retry(jet2, pts, np_ * len(sizes), d, trials=1, rng=srng)
    print(f"S^{d-1}: Mobius-algebraic groups {sizes} (n={sum(sizes)}): 2-jet {v}  ({time.time()-t0:.0f}s)"); sys.stdout.flush()
print(tally_line())
