import sys, random, time
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry, tally_line
from e3_sphere import indep_sphere
rng = random.Random(17)
srng = random.Random(217)   # specialization RNG, explicit seed (reproducible counts)
d = 5
rats = [rand_rat_sphere(d, rng) for _ in range(24)]
for n in range(18, 24):
    t0 = time.time()
    v = retry(jet2, rats[:n-4] + indep_sphere(4, d), 16, d, trials=1, rng=srng)
    print(f"S^4, 4 free + {n-4} rational (n={n}): {v} ({time.time()-t0:.0f}s)"); sys.stdout.flush()
    if v == "FAIL": break
print(tally_line())
