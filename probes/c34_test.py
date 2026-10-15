"""C-34 test (filed before running): one-parameter (k = 1) rational-affine families on S^2 (d = 3).
Prediction: Delta = 0 (Ramsey, by C-34) for N <= 15, 2-jet FAIL (non-Ramsey by J2) for N >= 16.
Exact: dim Delta at theta = 0 over Q (corank_exact.jet_dual). Probe: curve_probe (the truncated pi-adic test
of order 12, mod p) and jet2, seeded, via validate.retry.  [PROBE] parts never conclude.
Ledger entry SR-C34. applies_to: as ../certificates/corank_exact.py.  Run: cd probes && python c34_test.py"""
import os, sys, random
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.path.insert(0, os.path.join(here, "..", "certificates"))
from probe2 import *            # noqa
from validate import retry, tally_line
import corank_exact as X
from c31_c32_jet2 import mk_point

srng = random.Random(3434)
d, k, G = 3, 1, 6
for N in (13, 14, 15, 16, 17):
    for seed in (0, 1):
        rng = random.Random(34000 + 10 * N + seed)
        alpha, B = X.family(rng, d, N, k)
        pts_e, vel = X.family_data(alpha, B, d, k)
        kap, dim, lower, nz = X.jet_dual(pts_e, vel, d, k)
        pts = [mk_point(alpha[i], B[i], k) for i in range(N)]
        cv = retry(curve_probe, pts, k, d, rng=srng)
        jv = retry(jet2, pts, k, d, rng=srng)
        pred = "Ramsey" if N <= 15 else "non-Ramsey"
        print(f"N={N} seed={seed}: kappa={kap} dimDelta={dim} pairing!=0={nz} | curve(pi-adic, ord 12) {cv:5s} jet2 {jv:5s} | predicted {pred}")
        sys.stdout.flush()
print(tally_line())
