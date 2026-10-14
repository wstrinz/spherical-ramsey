import sys, random, time
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry
rng = random.Random(5)
srng = random.Random(205)   # specialization RNG, explicit seed (reproducible counts)
def indep_sphere(j, d):
    return [(lambda i: (lambda th: sph(th[i*(d-1):(i+1)*(d-1)])))(i) for i in range(j)]
def rat_sphere(m, d):
    return [rand_rat_sphere(d, rng) for _ in range(m)]
mode = sys.argv[1] if __name__ == "__main__" else None
if mode == "threshold":
    # many rational points (kill all quadrics) + j independent points on S^{d-1}
    for d in [int(x) for x in sys.argv[2].split(',')]:
        m = (d+1)*(d+2)//2 + 1
        out = []
        for j in range(1, 6):
            t0 = time.time()
            v = retry(jet2, rat_sphere(m, d) + indep_sphere(j, d), j*(d-1), d, trials=1, rng=srng)
            out.append(f"j={j}:{v}({time.time()-t0:.0f}s)")
            print(f"S^{d-1} in R^{d}, {m} rational pts + j generic:", " ".join(out)); sys.stdout.flush()
            if v == "FAIL": break
elif mode == "generic":
    d = int(sys.argv[2])
    for n in range(int(sys.argv[3]), int(sys.argv[4])+1):
        t0 = time.time()
        v = retry(jet2, indep_sphere(n, d), n*(d-1), d, trials=1, rng=srng)
        print(f"S^{d-1}: {n} generic points: {v} ({time.time()-t0:.0f}s)"); sys.stdout.flush()
        if v == "FAIL": break
