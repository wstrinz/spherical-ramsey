import sys, random
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry, tally_line
from e3_sphere import indep_sphere
rng = random.Random(11)
srng = random.Random(211)   # specialization RNG, explicit seed (reproducible counts)
rats = [rand_rat_sphere(3, rng) for _ in range(14)]
print("S^2: rows m = #rational points, cols j = #independent generic points (2-jet)")
print("      j=" + " ".join(f"{j:2d}" for j in range(1, 8)))
for m in range(0, 12):
    row = []
    for j in range(1, 8):
        n = m + j
        if n < 4 or n > 13: row.append(" ."); continue
        v = retry(jet2, rats[:m] + indep_sphere(j, 3), 2*j, 3, trials=1, rng=srng)
        row.append(" P" if v == "PASS" else (" F" if v == "FAIL" else (" N" if v == "NO_VERDICT" else " ?")))
    print(f"m={m:2d}   " + " ".join(row)); sys.stdout.flush()
print(tally_line())
