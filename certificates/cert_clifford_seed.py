"""Two-factor vanishing identically in a symbolic seed point t (instances), S^5 / Cl_{0,4}.

applies_to: S^5 (n = 5), the Vahlen normal form nu(t) = q + lam w (t+p)^{-1} (w^)^{-1} of cert_clifford.py,
  with EXACT RATIONAL parameters chosen independently on the left and right tensor factor (3 seeded instances)
  and the seed point t a SYMBOLIC paravector (5 symbols).  Checks, as polynomial identities in t:
    n_L(t) n_R(t) h(X(t), Y(t)) = 0, where h is the graph form of mu = N_R adj(N_L), X = X~_L / n_L, Y = X~_R / n_R;
  and the control: with independent seeds t_L != t_R the same expression is a nonzero polynomial that vanishes
  on t_L = t_R (so it lies in the ideal of the components of t_L - t_R: the input of the idempotent glue G4).
  This is a TEST of the 2x2 associativity glue (the proof is cert_clifford.py (V1)-(V3) + glue), not a proof.
Run (from any directory):  python3 -I cert_clifford_seed.py
"""
import random
import sys
import time
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # sibling imports under python -I

from sympy import QQ
from sympy.polys.rings import ring

from cert_clifford import Cl, adj, mat_mul, vahlen_N

T0 = time.time()
n = 5
R, *g = ring(",".join([f"t{i}" for i in range(n)] + [f"r{i}" for i in range(n)]), QQ)
A = Cl(n - 1, R.zero)
tL = A.para(g[:n])
tR = A.para(g[n:])


def log(*a):
    print(*a)
    sys.stdout.flush()


def instance(seed):
    rng = random.Random(seed)
    rnd = lambda: R(QQ(rng.randint(-9, 9), rng.randint(1, 7)))
    rpara = lambda: A.para([rnd() for _ in range(n)])

    def par():
        lam = R.zero
        while lam == 0:
            lam = rnd()
        return A.mulall(*[rpara() for _ in range(4)]), lam, rpara(), rpara()

    PL, PR = par(), par()
    NL, NR = vahlen_N(A, *PL), vahlen_N(A, *PR)
    a, b, c, d = mat_mul(A, NR, adj(A, NL))

    def scaled_point(N, t):
        a_, b_, c_, d_ = N
        u = A.add(A.mul(c_, t), d_)
        ub = A.conj(u)
        nn = A.mul(u, ub)
        assert A.is_scalar(nn)
        Xt = A.mul(A.add(A.mul(a_, t), b_), ub)
        assert A.is_para(Xt)
        return Xt, nn[0]

    out = []
    for tr in (tL, tR):
        Xt, nL = scaled_point(NL, tL)
        Yt, nR = scaled_point(NR, tr)
        # n_L n_R h(X, Y) = Y~ c X~ + Y~ d n_L - a X~ n_R - b n_L n_R
        val = A.sub(A.add(A.mulall(Yt, c, Xt), A.smul(nL, A.mul(Yt, d))),
                    A.add(A.smul(nR, A.mul(a, Xt)), A.smul(nL * nR, b)))
        out.append(val)
    same = A.is_zero(out[0])
    indep = out[1]
    nonzero = not A.is_zero(indep)
    back = [z.compose([(g[n + i], g[i]) for i in range(n)]) for z in indep]
    on_diag = all(z == 0 for z in back)
    return same, nonzero and on_diag


res = [instance(s) for s in (11, 12, 13)]
log(f"[SEED] S^5, 3 instances (rational left != right parameters, w = product of 4 paravectors), symbolic seed t in R^5:")
log(f"       n_L n_R h(nu_L t, nu_R t) = 0 identically in t: {[r[0] for r in res]}")
log(f"       control t_L != t_R: nonzero polynomial, vanishing on t_L = t_R: {[r[1] for r in res]}  ({time.time() - T0:.0f}s)")
log(f"SEED CHECKS PASS: {all(r[0] and r[1] for r in res)}")
