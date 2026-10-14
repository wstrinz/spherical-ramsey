import sys, random
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry, indep_circle, rats, tally_line
srng = random.Random(201)   # specialization RNG, explicit seed (reproducible counts)
print("circle: rows m = #rational points, cols j = #independent transcendental points")
print("2-jet verdict (F = 2-jet FAIL, mod-p evidence of non-Ramsey; P = passes; N = NO_VERDICT; ? = mixed)")
print("      j=" + " ".join(f"{j:2d}" for j in range(0, 8)))
for m in range(0, 9):
    row = []
    for j in range(0, 8):
        n = m + j
        if n < 3 or n > 13:
            row.append(" ."); continue
        v = retry(jet2, rats[:m] + indep_circle(j), j, 2, rng=srng)
        row.append(" P" if v == "PASS" else (" F" if v == "FAIL" else (" N" if v == "NO_VERDICT" else " ?")))
    print(f"m={m:2d}   " + " ".join(row)); sys.stdout.flush()
print(tally_line())
