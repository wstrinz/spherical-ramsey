"""Re-specialize the three C-31 families whose first specialization (theta = 0) was undecided
(coincident points at theta = 0; for the two circle families also a dual dimension above the generic
lower bound) at theta = theta0 (seeded rational), same family.
Ledger entry SR-C31 (C-31). applies_to: as corank_exact.py.  Run: python -I certificates/c31_respecialize.py"""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corank_exact as X
from fractions import Fraction as Fr
for (d, N, k, seed) in ((3, 13, 2, 1), (2, 7, 2, 1), (2, 7, 3, 0)):
    G = d * (d + 1) // 2
    rng = random.Random(31000 + 100 * d + 10 * N + k + 1000 * seed)
    alpha, B = X.family(rng, d, N, k)
    print(f"family d={d} N={N} k={k} seed={seed}: B = {[[int(x) for x in Bi[0]] for Bi in B]}")
    r2 = random.Random(777)
    for t in range(3):
        th = [Fr(r2.randint(-7, 7), r2.randint(1, 7)) for _ in range(k)]
        al = [[alpha[i][c] + sum(B[i][c][l] * th[l] for l in range(k)) for c in range(d - 1)] for i in range(N)]
        pts, vel = X.family_data(al, B, d, k)
        kap, dim, lower, nz = X.jet_dual(pts, vel, d, k)
        v = "?(coincident points at theta0)" if X.coincident(pts) else X.jet_verdict(kap, dim, lower, nz, k, G)
        print(f"  theta0={[str(x) for x in th]}: kappa={kap} dimDelta={dim} lower={lower} pairing!=0={nz} -> {v}; predicted {X.predict(kap, k, G)}")
