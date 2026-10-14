# applies_to: any seed-independent graph-form certificate P whose evaluation identity holds on the diagonal t_L = t_R; transport to algebraic seeds via the separability idempotent of a number field K in R (here K = Q(sqrt2, sqrt3), circle case). Author: an independent AI reviewer (Claude Opus).
"""Adversarial test of glue G4 (idempotent transport to algebraic seeds), circle case.
K (x) K for K = Q(sqrt2, sqrt3) modelled as Q[a2,b2,a3,b3]/(a2^2-2, b2^2-2, a3^2-3, b3^2-3), a = left, b = right.
Mobius params: independent symbols L (left factor) and R (right factor). Group-1 seeds in Q(sqrt2),
group-2 seeds in Q(sqrt3); e = e_2 e_3 (compositum idempotent). Check e*f(x_i,y_i) = 0, control f != 0."""
from sympy import QQ
from sympy.polys.rings import ring
names = ["a2", "b2", "a3", "b3"] + [f"L{j}" for j in range(6)] + [f"R{j}" for j in range(6)]
Rg, *G = ring(",".join(names), QQ)
a2, b2, a3, b3 = G[:4]; L = G[4:10]; R = G[10:16]
SQ = {0: 2, 1: 2, 2: 3, 3: 3}
def red(p):
    out = Rg.zero
    for mono, c in p.terms():
        m = list(mono); cc = c
        for i, q in SQ.items():
            cc *= QQ(q) ** (m[i] // 2); m[i] %= 2
        out += Rg({tuple(m): cc})
    return out
e = QQ(1, 4) * (1 + a2 * b2 * QQ(1, 2)) * (1 + a3 * b3 * QQ(1, 3))
assert red(e * (a2 - b2)) == 0 and red(e * (a3 - b3)) == 0
me = red(e.compose([(b2, a2), (b3, a3)]))
assert me == 1, me
def params(th, k):
    return th[3 * k], th[3 * k + 1], 1 + th[3 * k + 2]       # nu(t) = (t + beta)/(gamma t + delta)
def gco(k):   # mu = nu^(2) o (nu^(1))^{-1}: matrix N2 adj(N1); graph g = C s s' + D s' - A s - B
    bL, gL, dL = params(L, k); bR, gR, dR = params(R, k)
    A = dL - bR * gL; B = -bL + bR
    C = gR * dL - dR * gL; D = -gR * bL + dR
    return A, B, C, D, dL - gL * bL
def g_hom(co, xn, xd, yn, yd):   # xd*yd*g(xn/xd, yn/yd)
    A, B, C, D, _ = co
    return C * xn * yn + D * yn * xd - A * xn * yd - B * xd * yd
co = [gco(0), gco(1)]
def ev(k, tl, tr):
    bL, gL, dL = params(L, k); bR, gR, dR = params(R, k)
    xn, xd = tl + bL, gL * tl + dL
    yn, yd = tr + bR, gR * tr + dR
    return g_hom(co[0], xn, xd, yn, yd) * g_hom(co[1], xn, xd, yn, yd)
seeds1 = [(1 + a2, 1 + b2), (QQ(1, 3) - 2 * a2, QQ(1, 3) - 2 * b2), (a2 * QQ(1, 5), b2 * QQ(1, 5)), (Rg(QQ(2, 7)), Rg(QQ(2, 7)))]
seeds2 = [(a3 - 1, b3 - 1), (3 * a3 + QQ(1, 2), 3 * b3 + QQ(1, 2)), (-a3, -b3)]
ok = True; ctrl = True
for k, seeds in ((0, seeds1), (1, seeds2)):
    for tl, tr in seeds:
        v = red(ev(k, tl, tr))
        ok &= red(e * v) == 0
        if tl != tr:
            ctrl &= v != 0
# m(g_k) on the diagonal: g_k(s, s) with R -> L equals det N_k (s' - s)
mp = [(R[j], L[j]) for j in range(6)]
mco_ok = True
for k in (0, 1):
    A, B, C, D, kap = co[k]
    mco_ok &= C.compose(mp) == 0 and B.compose(mp) == 0 and D.compose(mp) == kap and A.compose(mp) == kap
print("e*f(x_i, y_i) = 0 at all 7 algebraic seeds (Q(sqrt2) and Q(sqrt3) groups, compositum idempotent):", ok)
print("control: f(x_i, y_i) != 0 WITHOUT e at the 6 irrational seeds:", ctrl)
print("m(C)=m(B)=0, m(D)=m(A)=det N_k  => m(f) = det N1 det N2 (s'-s)^2:", mco_ok)
