"""Why the quaternionic [II'] recipe does not transfer verbatim to Cl_{0,4} (S^5), and why the normal form repairs it.

applies_to: the algebra Cl_{0,4} only (16-dim, e_i^2 = -1); exact rational arithmetic, a handful of explicit
  elements.  These are counterexamples to the NAIVE route (generic entries beta, gamma, delta, as in
  cert_s2_quat.py [II']), not to the certificate: cert_clifford.py restricts to the Lipschitz group, where every
  norm is a scalar.  Run (from any directory):  python3 -I cert_clifford_obs.py
"""
import sys
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # sibling imports under python -I

from sympy import QQ

from cert_clifford import Cl


def log(*a):
    print(*a)
    sys.stdout.flush()


A = Cl(4, QQ(0))
E123, E1234 = 0b0111, 0b1111


def blade(I, c=1):
    v = [QQ(0)] * A.dim
    v[I] = QQ(c)
    return v


one = A.scalar(QQ(1))
para = lambda *c: A.para([QQ(x) for x in c])

# (a) Cl_4 has zero divisors: the Schur-complement inverse of cert_s2_quat [II'] (adj N = |s|^2 N^{-1}) needs s sbar scalar
s = A.add(one, blade(E1234))
sm = A.sub(one, blade(E1234))
zd = A.is_zero(A.mul(s, sm)) and not A.is_zero(s) and not A.is_zero(sm)
nrm = A.mul(s, A.conj(s))
a_ok = zd and not A.is_scalar(nrm)
log(f"[OBS-a] s = 1 + e1e2e3e4: s (1 - e1e2e3e4) = 0 with both factors nonzero: {zd};  s sbar = {nrm[0]} + {nrm[E1234]} e1234"
    f" is not a scalar: {not A.is_scalar(nrm)}")

# (b) an invertible non-Lipschitz delta: t -> t delta^{-1} leaves the paravector chart R^5
d = A.add(A.scalar(QQ(2)), blade(E123))
dinv = A.smul(QQ(1, 3), A.sub(A.scalar(QQ(2)), blade(E123)))
inv_ok = A.mul(d, dinv) == one and A.mul(dinv, d) == one
img = A.mul(para(1, 0, 0, 0, 0), dinv)
b_ok = inv_ok and not A.is_para(img) and not A.is_scalar(A.mul(d, A.conj(d)))
log(f"[OBS-b] delta = 2 + e1e2e3 is invertible (delta^-1 = (2 - e1e2e3)/3): {inv_ok};  1 * delta^-1 is not a paravector:"
    f" {not A.is_para(img)};  delta deltabar not scalar: {not A.is_scalar(A.mul(d, A.conj(d)))}")

# (c) the same element used as w in the normal form breaks (V0)-(V2); a Lipschitz w (product of paravectors) does not
def normal_form_checks(w):
    wh, ws = A.hat(w), A.rev(w)
    s_ = para(1, 2, -1, 3, 1)                    # s = t + p, a rational paravector
    u = A.mul(wh, s_)
    nn = A.mul(u, A.conj(u))
    Xt_rot = A.mulall(w, A.conj(s_), ws)         # the rotation part of X~ (X~ = q n + lam w sbar w*)
    return A.is_scalar(A.mul(wh, ws)), A.is_scalar(nn), A.is_para(Xt_rot)


bad = normal_form_checks(d)
good = normal_form_checks(A.mulall(para(1, 2, 0, -1, 1), para(0, 1, 1, 2, -3), para(2, 0, -1, 1, 1), para(1, -1, 3, 0, 2)))
c_ok = (not any(bad)) and all(good)
log(f"[OBS-c] normal form with w = 2 + e1e2e3 (invertible, not Lipschitz): w^ w* scalar, u ubar scalar, w sbar w* paravector"
    f" = {list(bad)} (all False);  with w = product of 4 rational paravectors: {list(good)} (all True)")
log(f"OBSTRUCTION-TO-NAIVE-ROUTE CHECKS PASS: {a_ok and b_ok and c_ok}")
