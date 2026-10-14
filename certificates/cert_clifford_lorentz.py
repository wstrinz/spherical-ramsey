"""Structure test: the two-group certificate is the polar form of the Vahlen -> Lorentz quadratic map (S^5).

applies_to: S^5 (n = 5, Cl_{0,4}); exact rational Vahlen matrices in the normal form of cert_clifford.py.
  Let P(mu_1, mu_2) be the 7x7 matrix that cert_clifford.py [I] builds from f = Re(h_1 conj h_2).  f is bilinear
  in (mu_1, mu_2) and symmetric (Re a = Re abar), so P(mu_1, mu_2) is the polar form of Q(mu) := P(mu, mu).
  Tested here, at exact rationals:
    (a) for a Vahlen mu, L := S Q(mu)^T satisfies L^T S L = c^2 S, c != 0, i.e. Q(mu) is (up to scale and S) a
        Lorentz matrix in O(1, 6): the single-group form |h|^2 is the Minkowski pairing q(y)^T S L q(x);
    (b) L maps the light-cone vector q(x) to a multiple of q(mu x)  (so L is THE Lorentz matrix of mu);
    (c) polarization: P(mu1, mu2) + P(mu2, mu1) = Q(mu1 + mu2) - Q(mu1) - Q(mu2) and P(mu1, mu2) = P(mu2, mu1).
  A test of a structural reading (for the next sharp question), not part of the S^5 proof.
Run (from any directory):  python3 -I cert_clifford_lorentz.py
"""
import random
import sys
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # sibling imports under python -I

import sympy as sp
from sympy import QQ

from cert_clifford import Cl, adj, coord_mats, mat_mul, part_universal, rat, vahlen_N

n = 5
NQ = n + 2
_, univ = part_universal(n, verbose=False)
R, names, M = univ
pos = {nm: i for i, nm in enumerate(names)}
A = Cl(n - 1, QQ(0))
_, Ci, S = coord_mats(n)
rng = random.Random(2026)
rnd = lambda: QQ(rng.randint(-9, 9), rng.randint(1, 7))
rpara = lambda: A.para([rnd() for _ in range(n)])


def log(*a):
    print(*a)
    sys.stdout.flush()


def vahlen():
    lam = QQ(0)
    while lam == 0:
        lam = rnd()
    return vahlen_N(A, A.mulall(*[rpara() for _ in range(4)]), lam, rpara(), rpara())


def Pof(mu1, mu2):
    sub = {}
    for j, mu in ((1, mu1), (2, mu2)):
        a, b, c, d = mu
        for L, qq in zip("CDAB", (c, d, A.neg(a), A.neg(b))):
            for I in range(A.dim):
                sub[pos[f"{L}{j}_{I}"]] = qq[I]
    Mn = sp.zeros(NQ, NQ)
    for r in range(NQ):
        for s in range(NQ):
            val = QQ(0)
            for mono, cf in M[r][s].terms():
                term = cf
                for i, e in enumerate(mono):
                    if e:
                        term *= sub[i] ** e
                val += term
            Mn[r, s] = rat(val)
    return Ci.T * Mn * Ci


def madd(m1, m2):
    return tuple(A.add(x, y) for x, y in zip(m1, m2))


def q_of(v):
    v = [rat(t) for t in v]
    nv = sum(t**2 for t in v)
    return sp.Matrix([1 + nv] + [2 * t for t in v] + [nv - 1])


def apply(mu, x):
    a, b, c, d = mu
    den = A.add(A.mul(c, x), d)
    nd = A.mul(den, A.conj(den))
    assert A.is_scalar(nd)
    y = A.smul(QQ(1) / nd[0], A.mul(A.add(A.mul(a, x), b), A.conj(den)))
    assert A.is_para(y)
    return A.pcomps(y)


oka, okb, okc = [], [], []
for trial in range(3):
    N1, N2, N3, N4 = vahlen(), vahlen(), vahlen(), vahlen()
    mu1 = mat_mul(A, N2, adj(A, N1))                 # Vahlen matrices of Mobius maps (compositions)
    mu2 = mat_mul(A, N4, adj(A, N3))
    Q1 = Pof(mu1, mu1)
    Lm = S * Q1.T
    G = Lm.T * S * Lm
    c2 = G[1, 1]
    oka.append(c2 != 0 and G == c2 * S)
    good = True
    for _ in range(3):
        x = rpara()
        v1, v2 = Lm * q_of(A.pcomps(x)), q_of(apply(mu1, x))
        good = good and v1.T * S * v1 == sp.Matrix([[0]]) and sp.Matrix.hstack(v1, v2).rank() == 1
    okb.append(good)
    P12, P21 = Pof(mu1, mu2), Pof(mu2, mu1)
    okc.append(P12 == P21 and P12 + P21 == Pof(madd(mu1, mu2), madd(mu1, mu2)) - Q1 - Pof(mu2, mu2))
log(f"[LOR-a] Vahlen mu (3 rational instances): L = S Q(mu)^T has L^T S L = c^2 S, c != 0 (Lorentz up to scale): {oka}")
log(f"[LOR-b] L q(x) is a light-cone multiple of q(mu x) (3 points each): {okb}")
log(f"[LOR-c] P(mu1, mu2) = P(mu2, mu1) and 2 P(mu1, mu2) = Q(mu1 + mu2) - Q(mu1) - Q(mu2): {okc}")
log(f"LORENTZ STRUCTURE CHECKS PASS: {all(oka) and all(okb) and all(okc)}")
