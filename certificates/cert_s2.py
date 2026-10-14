"""Exact certificates for OpenAI #172 (Thm 1.1) on the unit sphere S^2 in R^3 (d = 3): two Mobius groups.

applies_to: finite subsets of S^2 (pole (0,0,1) avoided) that are a union of two orientation-preserving
  Mobius images of {3 arbitrary points} or of {finitely many rational points}; the identities are ring
  identities, so they hold for ANY values of the symbols in any commutative Q-algebra B (here B = F (x)_Q F,
  or R (x)_Q R via OAI Prop 2.1). Exact sympy only; no mod-p step anywhere.

Coordinates (same convention as probe2.sph): z = u + i v, inverse stereographic projection from the pole
N = (0,0,1):  a(z) = (2u, 2v, |z|^2 - 1) / (1 + |z|^2),  p(z) = (1, a(z)) = q(z) / (1 + |z|^2),
q(z) = (1+|z|^2, 2u, 2v, |z|^2-1) = C b(z),  b(z) = (1, u, v, |z|^2).
A bilinear form f(z, w) = b(z)^T M b(w) gives P = C^{-T} M C^{-1}, and
    p(X)^T P p(Y) = f(X, Y) / ((1+|X|^2)(1+|Y|^2)),    q(z)^T S q(w) = -2|z - w|^2,  S = diag(-1,1,1,1).
Tensor convention (mirrors cert_mobius.py): U_a, V_a stand for u_a (x) 1, v_a (x) 1 (left factor) and
Up_a, Vp_a for 1 (x) u_a, 1 (x) v_a (right factor); the multiplication map m is Up -> U, Vp -> V.
The imaginary unit is formal: every quantity is stored as a pair (real part, imaginary part) of
polynomials over Q, so all checked entries of P are in Q[U, V, Up, Vp], i.e. in B.

Two-group certificate: with g_k the C-bilinear graph form of the Mobius correspondence of group k,
    H = g_1 * conj(g_2),   f_r = Re H,   f_i = Im H.
Both are Hermitian-bilinear in (z, w), hence lie in span{1,u,v,|z|^2} (x) span{1,u',v',|w|^2}.
Run (from any directory):  python3 -I cert_s2.py   (reads cert_mobius.py from its own directory)
"""
import ast
import os
import sys
import time

import sympy as sp
from sympy import QQ
from sympy.polys.rings import ring

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()


def log(*a):
    print(*a)
    sys.stdout.flush()


class Cx:
    """formal complex number re + i*im over a polynomial ring (i is NOT in B; it is cancelled)"""
    __slots__ = ("r", "i")

    def __init__(self, r, i):
        self.r, self.i = r, i

    def __add__(a, b):
        return Cx(a.r + b.r, a.i + b.i)

    def __sub__(a, b):
        return Cx(a.r - b.r, a.i - b.i)

    def __neg__(a):
        return Cx(-a.r, -a.i)

    def __mul__(a, b):
        return Cx(a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r)

    def conj(a):
        return Cx(a.r, -a.i)

    def scale(a, q):
        return Cx(a.r * q, a.i * q)

    def is_zero(a):
        return a.r == 0 and a.i == 0


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


# ---------------------------------------------------------------- fixed linear algebra (sympy, exact)
Cm = sp.Matrix([[1, 0, 0, 1], [0, 2, 0, 0], [0, 0, 2, 0], [-1, 0, 0, 1]])  # q = Cm b
Ci = Cm.inv()
S = sp.diag(-1, 1, 1, 1)
# e(z) = (1, z, zbar, z zbar) = K b(z)
K = [[Cx(1, 0), Cx(0, 0), Cx(0, 0), Cx(0, 0)],
     [Cx(0, 0), Cx(1, 0), Cx(0, 1), Cx(0, 0)],
     [Cx(0, 0), Cx(1, 0), Cx(0, -1), Cx(0, 0)],
     [Cx(0, 0), Cx(0, 0), Cx(0, 0), Cx(1, 0)]]


def coordinate_checks():
    """obligation 2: q, p, a are OAI's coordinates of points of the unit sphere; the S-identity."""
    u, v, u2, v2 = sp.symbols("u v u2 v2", real=True)
    n = u**2 + v**2
    q = sp.Matrix([1 + n, 2 * u, 2 * v, n - 1])
    a = q[1:, 0] / q[0]
    on_sphere = sp.simplify((a.T * a)[0] - 1) == 0
    p_is_q_over = sp.simplify(sp.Matrix([1] + list(a)) - q / q[0]) == sp.zeros(4, 1)
    b = sp.Matrix([1, u, v, n])
    q_is_Cb = sp.expand(q - Cm * b) == sp.zeros(4, 1)
    n2 = u2**2 + v2**2
    q2 = sp.Matrix([1 + n2, 2 * u2, 2 * v2, n2 - 1])
    s_ident = sp.expand((q.T * S * q2)[0] + 2 * ((u - u2)**2 + (v - v2)**2)) == 0
    # generic symbolic M: q^T (C^-T M C^-1) q' = b^T M b'
    Ms = sp.Matrix(4, 4, sp.symbols("M0:16"))
    b2 = sp.Matrix([1, u2, v2, n2])
    conv = sp.expand((q.T * Ci.T * Ms * Ci * q2)[0] - (b.T * Ms * b2)[0]) == 0
    # e = K b : (1, z, zbar, |z|^2) with z = u + i v
    e = sp.Matrix([1, u + sp.I * v, u - sp.I * v, n])
    Kmat = sp.Matrix([[1, 0, 0, 0], [0, 1, sp.I, 0], [0, 1, -sp.I, 0], [0, 0, 0, 1]])
    k_ok = sp.expand(e - Kmat * b) == sp.zeros(4, 1)
    log("[0] coordinates: |a(z)| = 1:", on_sphere, "| p = q/q0 = (1, a):", p_is_q_over, "| q = C b:", q_is_Cb,
        "| e = K b:", k_ok)
    log("    q(z)^T S q(w) = -2|z-w|^2:", s_ident, "| q^T (C^-T M C^-1) q' = b^T M b' for symbolic M:", conv)
    return all([on_sphere, p_is_q_over, q_is_Cb, s_ident, conv, k_ok])


def form_to_P(G1, G2):
    """H(z,w) = g1(z,w) * conj(g2)(zbar,wbar) with g_k = sum G_k[a][c] z^a w^c.
    Returns (P_r, P_i): 4x4 lists over the ring, H = b(z)^T (M_r + i M_i) b(w), P = C^-T M C^-1."""
    idx = [(0, 0), (1, 0), (0, 1), (1, 1)]          # e-basis index j <-> z^a zbar^b
    N = [[G1[a][c] * G2[bb][d].conj() for (c, d) in idx] for (a, bb) in idx]
    # M = K^T N K
    M = [[None] * 4 for _ in range(4)]
    for r in range(4):
        for s_ in range(4):
            acc = Cx(0, 0)
            for j in range(4):
                if K[j][r].is_zero():
                    continue
                for k in range(4):
                    if K[k][s_].is_zero():
                        continue
                    acc = acc + K[j][r] * N[j][k] * K[k][s_]
            M[r][s_] = acc
    out = []
    for part in ("r", "i"):
        Mp = [[getattr(M[r][s_], part) for s_ in range(4)] for r in range(4)]
        P = [[0] * 4 for _ in range(4)]
        for al in range(4):
            for be in range(4):
                acc = 0
                for r in range(4):
                    if Ci[r, al] == 0:
                        continue
                    for s_ in range(4):
                        if Ci[s_, be] == 0:
                            continue
                        acc = acc + Mp[r][s_] * QQ(int(sp.numer(Ci[r, al] * Ci[s_, be])),
                                                   int(sp.denom(Ci[r, al] * Ci[s_, be])))
                P[al][be] = acc
        out.append(P)
    return out


def bil(qL, P, qR):
    acc = 0
    for al in range(4):
        if qL[al] == 0:
            continue
        for be in range(4):
            if P[al][be] == 0 or qR[be] == 0:
                continue
            acc = acc + qL[al] * P[al][be] * qR[be]
    return acc


def qvec(Z, one):
    n = Z.r * Z.r + Z.i * Z.i
    return [one + n, 2 * Z.r, 2 * Z.i, n - one]


def qvec_frac(num, den):
    """|den|^2 q(num/den), a polynomial vector (|den|^2 is a pure-tensor unit)"""
    nn = num.r * num.r + num.i * num.i
    dd = den.r * den.r + den.i * den.i
    nd = num * den.conj()
    return [dd + nn, 2 * nd.r, 2 * nd.i, nn - dd]


def apply_m(P, mp):
    return [[x.compose(mp) if x != 0 else x for x in row] for row in P]


def is_cS(P, c):
    ok = True
    for al in range(4):
        for be in range(4):
            target = (-c if al == 0 else c) if al == be else 0
            ok &= (P[al][be] - target) == 0
    return ok


def nterms(P):
    return sum(len(x) for row in P for x in row if x != 0)


# ---------------------------------------------------------------- Part 1: any 3 + 3 points (two-group certificate)
def part1():
    names = ([f"U{a}" for a in range(1, 7)] + [f"V{a}" for a in range(1, 7)]
             + [f"Up{a}" for a in range(1, 7)] + [f"Vp{a}" for a in range(1, 7)])
    Rg, *gens = ring(",".join(names), QQ)
    U, V, Up, Vp = gens[0:6], gens[6:12], gens[12:18], gens[18:24]
    one = Rg(1)
    X = [Cx(U[a], V[a]) for a in range(6)]       # z_a (x) 1
    Y = [Cx(Up[a], Vp[a]) for a in range(6)]     # 1 (x) z_a
    ONE = Cx(one, Rg(0))

    def graph(ids):
        """g(z,w) = det [[z w, z, w, 1], [X_a Y_a, X_a, Y_a, 1]_{a in ids}] = sum G[a][c] z^a w^c"""
        rows = [[X[a] * Y[a], X[a], Y[a], ONE] for a in ids]
        minor = lambda cols: det3([[r[c] for c in cols] for r in rows])
        G = [[None, None], [None, None]]
        G[1][1] = minor([1, 2, 3])
        G[1][0] = -minor([0, 2, 3])
        G[0][1] = minor([0, 1, 3])
        G[0][0] = -minor([0, 1, 2])
        return G

    G1, G2 = graph([0, 1, 2]), graph([3, 4, 5])
    Pr, Pi = form_to_P(G1, G2)
    log(f"[1] any 6 points on S^2, split 3+3; H = g123 * conj(g456).  terms: P_r {nterms(Pr)}, P_i {nterms(Pi)}"
        f"  ({time.time() - T0:.0f}s)")
    # entries of P live in Q[U,V,Up,Vp] (no imaginary unit, no form variables): structural, by construction
    ev_ok = True
    for a in range(6):
        qL, qR = qvec(X[a], one), qvec(Y[a], one)
        er, ei = bil(qL, Pr, qR), bil(qL, Pi, qR)
        ev_ok &= (er == 0 and ei == 0)
        log(f"    point {a + 1}: (1+|x|^2)(1+|y|^2) p(x)^T P_r p(y) = 0: {er == 0};  same for P_i: {ei == 0}")
    mp = [(Up[a], U[a]) for a in range(6)] + [(Vp[a], V[a]) for a in range(6)]
    mPr, mPi = apply_m(Pr, mp), apply_m(Pi, mp)
    cr, ci = mPr[1][1], mPi[1][1]
    s_ok = is_cS(mPr, cr) and is_cS(mPi, ci)
    # predicted scalar: c = -(1/2) W1 conj(W2), W = Vandermonde (z2-z1)(z3-z1)(z3-z2) of each triple (up to sign)
    Z = [Cx(U[a], V[a]) for a in range(6)]
    W1 = (Z[1] - Z[0]) * (Z[2] - Z[0]) * (Z[2] - Z[1])
    W2 = (Z[4] - Z[3]) * (Z[5] - Z[3]) * (Z[5] - Z[4])
    pred = (W1 * W2.conj()).scale(QQ(-1, 2))
    c_ok = (cr - pred.r) == 0 and (ci - pred.i) == 0
    log(f"    m(P_r) = c_r S and m(P_i) = c_i S: {s_ok};  c_r + i c_i = -(1/2) W123 conj(W456)"
        f" (W = Vandermonde of the triple's complex coordinates): {c_ok}")
    # uniform normaliser lambda = conj(W1) W2 (x) 1 in B[i]:  P_lam = lam_r P_r - lam_i P_i,  m(P_lam) = -(1/2)|W1|^2|W2|^2 S
    lam = W1.conj() * W2
    mlam = Cx(lam.r.compose(mp), lam.i.compose(mp))  # lam already lives in the left factor: m is the identity on it
    cl = mlam.r * cr - mlam.i * ci
    nW1 = W1.r * W1.r + W1.i * W1.i
    nW2 = W2.r * W2.r + W2.i * W2.i
    lam_ok = (cl - QQ(-1, 2) * nW1 * nW2) == 0
    log(f"    lambda = conj(W123) W456 (x) 1:  m(lam_r P_r - lam_i P_i) = -(1/2)|W123|^2|W456|^2 S: {lam_ok}"
        f"  ({time.time() - T0:.0f}s)")
    return ev_ok and s_ok and c_ok and lam_ok, (Rg, U, V, Up, Vp, Pr, Pi)


# ---------------------------------------------------------------- Part 2: great-circle control vs cert_mobius.py
def load_cert_mobius():
    """exec ONLY the definitions C, g, to_P (and s, sq) from cert_mobius.py, without running its checks"""
    src = open(os.path.join(HERE, "cert_mobius.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    keep = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            keep.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in ("g", "to_P"):
            keep.append(node)
        elif isinstance(node, ast.Assign):
            tgt = {n.id for n in ast.walk(node.targets[0]) if isinstance(n, ast.Name)}
            if tgt & {"s", "sq", "C", "Ci"}:
                keep.append(node)
    ns = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), "cert_mobius.py[defs]", "exec"), ns)
    return ns


def part2(ctx):
    Rg, U, V, Up, Vp, Pr, Pi = ctx
    # restrict every point to the great circle a_2 = 0 (v = 0 on both factors)
    zero = [(V[a], Rg.zero) for a in range(6)] + [(Vp[a], Rg.zero) for a in range(6)]
    Pr0, Pi0 = apply_m(Pr, zero), apply_m(Pi, zero)
    pi_zero = all(Pi0[i][j] == 0 for i in (0, 1, 3) for j in (0, 1, 3))  # P_i restricted to the circle's plane
    cm = load_cert_mobius()
    T = sp.symbols("T1:7")
    Uc = sp.symbols("U1:7")
    pairs = list(zip(T, Uc))
    Pc = cm["to_P"](cm["g"](pairs[:3]) * cm["g"](pairs[3:6]))
    L = sp.Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])  # (1, x_c, y_c) = L (1, a1, a3); same pole
    target = sp.expand(L.T * Pc * L)
    # our ring symbols U_a -> T_a (left), Up_a -> U_a (right) of cert_mobius
    sub = {sp.Symbol(f"U{a}"): T[a - 1] for a in range(1, 7)}
    sub.update({sp.Symbol(f"Up{a}"): Uc[a - 1] for a in range(1, 7)})
    ex = lambda x: x.as_expr() if hasattr(x, 'as_expr') else sp.Integer(x)
    ours = sp.Matrix(3, 3, lambda i, j: sp.expand(ex(Pr0[[0, 1, 3][i]][[0, 1, 3][j]]).xreplace(sub)))
    eq = sp.expand(ours - target) == sp.zeros(3, 3)
    log(f"[2] great-circle control (all v = 0): the (1, a1, a3) block of P_i vanishes: {pi_zero};  the (1, a1, a3) block of P_r equals"
        f" L^T P_circle L from cert_mobius.py's g123*g456: {eq}  ({time.time() - T0:.0f}s)")
    return pi_zero and eq


# ---------------------------------------------------------------- Part 3: two Mobius images of rational sets (+ 3-group control)
def part3():
    ng = 3
    names = [f"L{j}" for j in range(6 * ng)] + [f"R{j}" for j in range(6 * ng)] + ["t0", "t1"]
    Rg, *gens = ring(",".join(names), QQ)
    Lp, Rp = gens[:6 * ng], gens[6 * ng:12 * ng]
    tsym = Cx(gens[12 * ng], gens[12 * ng + 1])   # ONE generic point t = t0 + i t1 of the (rational) seed set,
    # the SAME symbol in both tensor factors: an identity in t covers every rational seed point at once, and
    # (times the separability idempotent e_K) every algebraic one.
    one, zer = Rg(1), Rg(0)

    def mob(th, k):
        """nu_k(t) = (t + b)/(c t + d), b = th0 + i th1, c = th2 + i th3, d = 1 + th4 + i th5 (as e5_mobius.mob_s2)"""
        o = 6 * k
        return Cx(th[o], th[o + 1]), Cx(th[o + 2], th[o + 3]), Cx(one + th[o + 4], th[o + 5])

    def graph_nu(k):
        """(adj N^(1) zhat) ^ (adj N^(2) what), N = [[1, b], [c, d]]:  coefficients of 1, z, w, zw"""
        b, c, d = mob(Lp, k)
        b2, c2, d2 = mob(Rp, k)
        G = [[None, None], [None, None]]
        G[0][0] = b2 - b
        G[1][0] = d - c * b2
        G[0][1] = b * c2 - d2
        G[1][1] = c * d2 - d * c2
        return G

    def point(r, k, th):
        b, c, d = mob(th, k)
        rr = r if isinstance(r, Cx) else Cx(Rg(r[0]), Rg(r[1]))
        return rr + b, c * rr + d     # numerator, denominator

    rq = [(QQ(1, 2), QQ(0)), (QQ(-1, 3), QQ(2)), (QQ(3), QQ(-1, 4)), (QQ(0), QQ(-5, 2)), (QQ(2, 7), QQ(1, 3)),
          (QQ(-4), QQ(-1)), (QQ(5, 3), QQ(3, 2)), (QQ(-1, 5), QQ(-2, 3)), (QQ(1), QQ(1)), (QQ(-3, 2), QQ(4, 5)),
          (QQ(0), QQ(1, 6)), (QQ(7, 4), QQ(-3))]
    G1, G2 = graph_nu(0), graph_nu(1)
    Pr, Pi = form_to_P(G1, G2)
    def ev(r, k):
        nL, dL = point(r, k, Lp)
        nR, dR = point(r, k, Rp)
        qL, qR = qvec_frac(nL, dL), qvec_frac(nR, dR)
        return bil(qL, Pr, qR), bil(qL, Pi, qR)

    gen_ok = all(e == 0 for k in (0, 1) for e in ev(tsym, k))
    ok = True
    for k, pts in [(0, rq[:6]), (1, rq[6:12])]:
        for r in pts:
            ok &= all(e == 0 for e in ev(r, k))
    mp = [(Rp[j], Lp[j]) for j in range(6 * ng)]
    mPr, mPi = apply_m(Pr, mp), apply_m(Pi, mp)
    cr, ci = mPr[1][1], mPi[1][1]
    s_ok = is_cS(mPr, cr) and is_cS(mPi, ci)
    b1, c1, d1 = mob(Lp, 0)
    b2_, c2_, d2_ = mob(Lp, 1)
    D1, D2 = d1 - c1 * b1, d2_ - c2_ * b2_   # det N_k
    pred = (D1 * D2.conj()).scale(QQ(-1, 2))
    c_ok = (cr - pred.r) == 0 and (ci - pred.i) == 0
    log(f"[3] PRIMARY: two Mobius images nu_1(A1) u nu_2(A2), nu_k(t) = (t+b_k)/(c_k t+d_k) generic (6 real params per map"
        f" per factor, symbols for th (x) 1 and 1 (x) th in R (x) R):")
    log(f"    generic seed point t (symbolic, same in both factors), groups 1 and 2, P_r and P_i: "
        f"(q~ . P . q~') = 0 identically in t: {gen_ok}")
    log(f"    explicit 6+6 = 12-point instance (rational seeds), 24 evaluation identities: {ok};  m(P_r), m(P_i) = c S: {s_ok};"
        f"  c_r + i c_i = -(1/2) det N1 conj(det N2): {c_ok}  ({time.time() - T0:.0f}s)")
    # control (three groups): the same two-group form does not vanish on a third Mobius-rational group
    third = []
    for r in rq[:4]:
        nL, dL = point(r, 2, Lp)
        nR, dR = point(r, 2, Rp)
        qL, qR = qvec_frac(nL, dL), qvec_frac(nR, dR)
        third.append(bil(qL, Pr, qR) != 0 or bil(qL, Pi, qR) != 0)
    # control: a product of three graph forms has a z^2 (or zbar^2) term, so it is not of the form q^T P q
    G3 = graph_nu(2)
    z2 = G1[1][0] * G2[1][0]            # coefficient of z^2 in g1*g2 (any third factor's constant term multiplies it)
    z2_nonzero = not z2.is_zero() and not G3[0][0].is_zero()
    log(f"    3-group control: H = Re/Im(g1 conj g2) is nonzero at all 4 points of a third group nu_3(A3): {all(third)};"
        f"  a triple product g1 g2 conj(g3) has a nonzero z^2-coefficient (not bilinear in p): {z2_nonzero}")
    return gen_ok and ok and s_ok and c_ok and all(third) and z2_nonzero


if __name__ == "__main__":
    r0 = coordinate_checks()
    r1, ctx = part1()
    r2 = part2(ctx)
    r3 = part3()
    log(f"ALL CHECKS PASS: {r0 and r1 and r2 and r3}  (sympy {sp.__version__}; {time.time() - T0:.0f}s)")
