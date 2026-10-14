import sys, random
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry, tally_line
from e3_sphere import indep_sphere
rng = random.Random(13)
srng = random.Random(213)   # specialization RNG, explicit seed (reproducible counts)
for d in (4,):
    rats = [rand_rat_sphere(d, rng) for _ in range(20)]
    for j in (4, 5):
        out = []
        for m in range(6, 14):
            v = retry(jet2, rats[:m] + indep_sphere(j, d), (d-1)*j, d, trials=1, rng=srng)
            out.append(f"n={m+j}:{v[0]}")
            print(f"S^{d-1}, j={j} free + m rational:", " ".join(out)); sys.stdout.flush()
            if v == "FAIL": break
print(tally_line())
