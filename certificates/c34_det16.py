"""Exact non-Ramsey side of the one-parameter threshold (d+1)^2 = 16 on S^2 (Theorem D's method):
for the N = 16 one-parameter families of c34_test.py, the 16 x 16 evaluation matrix
[p_ia(T) p_ib(U)] (rows i, columns (a,b)) has nonzero determinant in Q(T,U) iff nonzero at some rational
(T,U); then condition (1) forces P = 0 and A is not Ramsey (F = Q(T), B embeds in Q(T,U)). [CERT per instance]
applies_to: one-parameter rational-affine families u_i(T) = alpha_i + beta_i T on S^2.
Ledger entry SR-C34 (C-34). Run: python -I certificates/c34_det16.py"""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corank_exact as X
from fractions import Fraction as Fr
import flint
d, k = 3, 1
for seed in (0, 1):
    rng = random.Random(34000 + 10 * 16 + seed)
    alpha, B = X.family(rng, d, 16, k)
    for (T, U) in ((Fr(1, 3), Fr(2, 7)), (Fr(-5, 11), Fr(3, 13))):
        rows = []
        for i in range(16):
            uT = [alpha[i][c] + B[i][c][0] * T for c in range(2)]
            uU = [alpha[i][c] + B[i][c][0] * U for c in range(2)]
            pT = [Fr(1)] + X.sph(uT)
            pU = [Fr(1)] + X.sph(uU)
            rows.append([pT[a] * pU[b] for a in range(4) for b in range(4)])
        det = X.mat(rows).det()
        print(f"N=16 seed={seed} (T,U)=({T},{U}): det = {'nonzero' if det != 0 else 'ZERO'}")
    print(f"  distinct points / F = Q(T): beta nonzero somewhere = {any(B[i][c][0] != 0 for i in range(16) for c in range(2))}")
