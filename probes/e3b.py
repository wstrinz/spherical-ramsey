import sys, time, random
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry, tally_line
srng = random.Random(203)   # specialization RNG, explicit seed (reproducible counts)
def indep_sphere(j, d):
    return [(lambda i: (lambda th: sph(th[i*(d-1):(i+1)*(d-1)])))(i) for i in range(j)]
for d in range(2, 10):
    out = []
    for j in range(1, 8):
        t0 = time.time()
        v = retry(jet2_reduced, indep_sphere(j, d), j*(d-1), d, trials=1, rng=srng)
        out.append(f"{j}:{v[0]}")
        if v == "FAIL": break
    pred = d*(d+1)//(2*(d-1))
    print(f"d={d} (S^{d-1}): " + " ".join(out) + f"   naive count (REFUTED) predicted = {pred}"); sys.stdout.flush()
print(tally_line())
