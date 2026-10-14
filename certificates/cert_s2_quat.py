"""Exact two-group certificates via quaternions: S^4 in R^5 (d = 5), specialising to S^3, S^2 and S^1.

applies_to: finite subsets of S^4 (pole (0,0,0,0,1) avoided) that are a union of two Mobius images of
  {3 arbitrary points} -- i.e. ANY 6 points of S^4 -- and of {finitely many rational points} under generic
  quaternionic Mobius maps; by restriction (zero coordinates) the same identities cover S^3, S^2, S^1.
  The identities are ring identities over Q, so they hold for any values of the symbols in any commutative
  Q-algebra B (B = F (x)_Q F, or R (x)_Q R via OAI Prop 2.1). Exact; no mod-p step.

Coordinates: x in H = R^4 (stereographic chart of S^4 from N = e_5),
    a(x) = (2x, |x|^2 - 1)/(1 + |x|^2),  p = (1, a) = q/(1+|x|^2),  q = (1+|x|^2, 2x, |x|^2-1) = C b,
    b(x) = (1, x0, x1, x2, x3, |x|^2),   q(x)^T S q(y) = -2|x - y|^2,  S = diag(-1, I_5).
Construction: for a Mobius correspondence y = (a x + b)(c x + d)^{-1} write the AFFINE-AFFINE
quaternionic graph form h(x, y) = y C x + y D + A x + B  (C = c, D = d, A = -a, B = -b), and put
    f(x, y) = Re( h_1(x, y) * conj(h_2(x, y)) ).
Because x is rightmost in every term of h and Re is cyclic, f only sees x through (1, x_alpha, |x|^2) and y
through (1, y_beta, |y|^2): f = b(x)^T M b(y) with M bilinear in the coefficients (checked in part I).
On the diagonal h_k = kappa_k (y - x), kappa_k in F, so m(f) = kappa_1 kappa_2 |x - y|^2 and
m(P) = -(kappa_1 kappa_2 / 2) S (part III).
Three-point graph form (part II): phi_x(t) = (t - x1)(t - x3)^{-1} k_x sends x1, x2, x3 to 0, 1, inf; the
relation phi_x(x) = phi_y(y) rearranges (no inverse of a non-pure element) to
    sigma rho h = (y - y3) conj(y3 - y1) [sigma (x - x1) - E (x - x3)] - rho E (x - x3),
    rho = |y3 - y1|^2,  sigma = |y2 - y1|^2 |x2 - x3|^2,  E = (y2 - y3) conj(y2 - y1) (x2 - x1) conj(x2 - x3).
rho, sigma are pure tensors (units of B); all inverses are of pure-tensor quaternions with unit norms.
Run (from any directory):  python3 -I cert_s2_quat.py
"""
import random
import sys
import time

import sympy as sp
from sympy import QQ
from sympy.polys.rings import ring

T0 = time.time()


def log(*a):
    print(*a)
    sys.stdout.flush()


class Qn:
    """quaternion w + x i + y j + z k over a commutative ring"""
    __slots__ = ("c",)

    def __init__(self, c):
        self.c = tuple(c)

    def __add__(a, b):
        return Qn(p + q for p, q in zip(a.c, b.c))

    def __sub__(a, b):
        return Qn(p - q for p, q in zip(a.c, b.c))

    def __neg__(a):
        return Qn(-p for p in a.c)

    def __mul__(a, b):
        if not isinstance(b, Qn):              # central scalar
            return Qn(p * b for p in a.c)
        a0, a1, a2, a3 = a.c
        b0, b1, b2, b3 = b.c
        return Qn((a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
                   a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
                   a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
                   a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0))

    def conj(a):
        return Qn((a.c[0], -a.c[1], -a.c[2], -a.c[3]))

    def norm(a):
        return a.c[0] ** 2 + a.c[1] ** 2 + a.c[2] ** 2 + a.c[3] ** 2

    def re(a):
        return a.c[0]

    def is_zero(a):
        return all(p == 0 for p in a.c)


def h_eval(co, x, y):
    C, D, A, B = co
    return y * C * x + y * D + A * x + B


# ---------------------------------------------------------------- fixed linear algebra (sympy)
NQ = 6
Cm = sp.zeros(NQ, NQ)
Cm[0, 0] = 1; Cm[0, 5] = 1
for al in range(4):
    Cm[al + 1, al + 1] = 2
Cm[5, 0] = -1; Cm[5, 5] = 1
Ci = Cm.inv()
S = sp.diag(-1, *([1] * 5))


def coordinate_checks():
    x = sp.symbols("x0:4", real=True)
    y = sp.symbols("y0:4", real=True)
    nx, ny = sum(t**2 for t in x), sum(t**2 for t in y)
    q = sp.Matrix([1 + nx] + [2 * t for t in x] + [nx - 1])
    qy = sp.Matrix([1 + ny] + [2 * t for t in y] + [ny - 1])
    a = q[1:, 0] / q[0]
    on_sphere = sp.simplify((a.T * a)[0] - 1) == 0
    b = sp.Matrix([1] + list(x) + [nx])
    by = sp.Matrix([1] + list(y) + [ny])
    q_is_Cb = sp.expand(q - Cm * b) == sp.zeros(NQ, 1)
    s_ident = sp.expand((q.T * S * qy)[0] + 2 * sum((s - t)**2 for s, t in zip(x, y))) == 0
    Ms = sp.Matrix(NQ, NQ, sp.symbols(f"M0:{NQ * NQ}"))
    conv = sp.expand((q.T * Ci.T * Ms * Ci * qy)[0] - (b.T * Ms * by)[0]) == 0
    log(f"[0] S^4 coordinates: |a(x)| = 1: {on_sphere} | q = C b: {q_is_Cb} | q^T S q' = -2|x-y|^2: {s_ident}"
        f" | q^T (C^-T M C^-1) q' = b^T M b' (symbolic M): {conv}")
    return on_sphere and q_is_Cb and s_ident and conv


# ---------------------------------------------------------------- Part I: universal identity
def part_universal():
    cn = [f"{L}{k}_{t}" for k in (1, 2) for L in "CDAB" for t in range(4)]
    names = cn + [f"x{t}" for t in range(4)] + [f"y{t}" for t in range(4)] + ["k1", "k2"]
    R, *g = ring(",".join(names), QQ)
    co = {}
    for k in (1, 2):
        for L in "CDAB":
            co[(k, L)] = Qn([g[names.index(f"{L}{k}_{t}")] for t in range(4)])
    xs = [g[names.index(f"x{t}")] for t in range(4)]
    ys = [g[names.index(f"y{t}")] for t in range(4)]
    x, y = Qn(xs), Qn(ys)
    k1, k2 = g[names.index("k1")], g[names.index("k2")]
    co1 = [co[(1, L)] for L in "CDAB"]
    co2 = [co[(2, L)] for L in "CDAB"]
    f = (h_eval(co1, x, y) * h_eval(co2, x, y).conj()).re()
    ix = [names.index(f"x{t}") for t in range(4)]
    iy = [names.index(f"y{t}") for t in range(4)]

    def slot(exps, idxs):
        e = [exps[i] for i in idxs]
        if sum(e) == 0:
            return 0
        if sum(e) == 1:
            return 1 + e.index(1)
        if e == [2, 0, 0, 0]:
            return 5               # read |x|^2 off the x0^2 coefficient; reconstruction checks the rest
        return None

    M = [[R.zero] * NQ for _ in range(NQ)]
    for mono, cf in f.terms():
        j, k = slot(mono, ix), slot(mono, iy)
        if j is None or k is None:
            continue
        rest = list(mono)
        for i in ix + iy:
            rest[i] = 0
        M[j][k] += R({tuple(rest): cf})
    bx = [R.one] + xs + [sum(t * t for t in xs)]
    by = [R.one] + ys + [sum(t * t for t in ys)]
    recon = R.zero
    for j in range(NQ):
        for k in range(NQ):
            recon += bx[j] * M[j][k] * by[k]
    span_ok = (recon - f) == 0
    # M only involves coefficient symbols (no x, y)
    no_xy = all(all(mono[i] == 0 for i in ix + iy for mono in M[j][k].monoms()) for j in range(NQ) for k in range(NQ)
                if M[j][k] != 0)
    # III: on the diagonal C = B = 0, D = kappa, A = -kappa
    sub = []
    for k, kk in ((1, k1), (2, k2)):
        for L, val in (("C", [0, 0, 0, 0]), ("B", [0, 0, 0, 0]), ("D", [kk, 0, 0, 0]), ("A", [-kk, 0, 0, 0])):
            for t in range(4):
                sub.append((g[names.index(f"{L}{k}_{t}")], val[t] if val[t] != 0 else R.zero))
    Md = [[M[j][k].compose(sub) for k in range(NQ)] for j in range(NQ)]
    Pd = [[sum((Md[r][s] * QQ(int(sp.numer(Ci[r, al] * Ci[s, be])), int(sp.denom(Ci[r, al] * Ci[s, be])))
                for r in range(NQ) for s in range(NQ) if Ci[r, al] * Ci[s, be] != 0), R.zero)
           for be in range(NQ)] for al in range(NQ)]
    target = -QQ(1, 2) * k1 * k2
    mS_ok = all((Pd[al][be] - (target * int(S[al, be]))) == 0 for al in range(NQ) for be in range(NQ))
    log(f"[I] universal: Re(h1 conj h2) = b(x)^T M b(y) with M bilinear in the 32 coefficient symbols, no x,y: "
        f"{span_ok and no_xy}  (f has {len(f)} terms)")
    log(f"[III] at C=B=0, D=kappa, A=-kappa (both forms): P = C^-T M C^-1 = -(kappa1 kappa2 / 2) S: {mS_ok}"
        f"  ({time.time() - T0:.0f}s)")
    return span_ok and no_xy and mS_ok, (R, names, M)


# ---------------------------------------------------------------- Part II: instance identities (3-point form)
def three_point_coeffs(X, Y):
    """X, Y: the three left / right points (quaternions). Returns (C, D, A, B) of sigma*rho*h."""
    x1, x2, x3 = X
    y1, y2, y3 = Y
    G = (y3 - y1).conj()
    rho = (y3 - y1).norm()
    sigma = (y2 - y1).norm() * (x2 - x3).norm()
    E = (y2 - y3) * (y2 - y1).conj() * (x2 - x1) * (x2 - x3).conj()
    sig = Qn([sigma, 0 * sigma, 0 * sigma, 0 * sigma])
    rh = Qn([rho, 0 * rho, 0 * rho, 0 * rho])
    Cc = G * (sig - E)
    Dc = G * (E * x3 - x1 * sigma)
    Ac = -(y3 * G * (sig - E)) - E * rho
    Bc = -(y3 * G * (E * x3 - x1 * sigma)) + E * x3 * rho
    return Cc, Dc, Ac, Bc


def part_instance():
    names = [f"X{a}_{t}" for a in range(1, 4) for t in range(4)] + [f"Y{a}_{t}" for a in range(1, 4) for t in range(4)]
    R, *g = ring(",".join(names), QQ)
    X = [Qn(g[4 * a:4 * a + 4]) for a in range(3)]
    Y = [Qn(g[12 + 4 * a:12 + 4 * a + 4]) for a in range(3)]
    co = three_point_coeffs(X, Y)
    van = [h_eval(co, X[a], Y[a]).is_zero() for a in range(3)]
    mp = [(g[12 + i], g[i]) for i in range(12)]
    mco = [Qn([c.compose(mp) for c in q.c]) for q in co]
    kappa = (X[2] - X[0]).norm() * (X[1] - X[0]).norm() * (X[1] - X[2]).norm()
    Kq = Qn([kappa, R.zero, R.zero, R.zero])
    diag_ok = mco[0].is_zero() and (mco[1] - Kq).is_zero() and (mco[2] + Kq).is_zero() and mco[3].is_zero()
    sizes = [sum(len(c) for c in q.c) for q in co]
    log(f"[II] three-point quaternionic graph form (generic x1,x2,x3 / y1,y2,y3 in H, 24 symbols; term counts {sizes}):")
    log(f"     h(x_a, y_a) = 0 for a = 1, 2, 3: {van};  m(C) = m(B) = 0, m(D) = -m(A) = "
        f"|x3-x1|^2 |x2-x1|^2 |x2-x3|^2: {diag_ok}  ({time.time() - T0:.0f}s)")
    return all(van) and diag_ok


# ---------------------------------------------------------------- Part II': Mobius images of rational sets in H
def mu_coeffs(bL, gL, dL, bR, gR, dR, ONE):
    """right-fraction matrix [[a, b], [c, d]] of mu = nu^(2) o (nu^(1))^{-1}, scaled by |s|^2 (s = delta - gamma beta):
    N2 * adj(N1), adj(N1) = |s|^2 N1^{-1} = [[|s|^2 + beta sbar gamma, -beta sbar], [-sbar gamma, sbar]]."""
    s = dL - gL * bL
    sb = s.conj()
    ns = s.norm()
    i11 = ONE * ns + bL * sb * gL
    i12 = -(bL * sb)
    i21 = -(sb * gL)
    i22 = sb
    a = i11 + bR * i21
    b = i12 + bR * i22
    c = gR * i11 + dR * i21
    d = gR * i12 + dR * i22
    return (c, d, a, b), ns


def part_mobius_rational():
    """nu_k(t) = (t + beta_k)(gamma_k t + delta_k)^{-1}, beta, gamma, delta generic quaternions (12 params per map,
    delta = 1 + ...). mu = nu^(2) o (nu^(1))^{-1} with matrix N2 adj(N1), adj(N1) = |s|^2 N1^{-1} via the Schur
    complement s = delta - gamma beta (pure tensor). h = y c x + y d - a x - b."""
    names = [f"L{j}" for j in range(12)] + [f"R{j}" for j in range(12)] + [f"t{j}" for j in range(4)]
    R, *g = ring(",".join(names), QQ)
    one, zer = R.one, R.zero
    tq = Qn(g[24:28])   # ONE generic seed point t in H, the same symbol in both tensor factors

    def params(th):
        beta = Qn(th[0:4])
        gamma = Qn(th[4:8])
        delta = Qn([one + th[8]] + list(th[9:12]))
        return beta, gamma, delta

    bL, gL, dL = params(g[:12])
    bR, gR, dR = params(g[12:])
    ONE = Qn([one, zer, zer, zer])
    (c, d, a, b), ns = mu_coeffs(bL, gL, dL, bR, gR, dR, ONE)
    co = (c, d, -a, -b)
    ok = []
    for rr in [tq]:
        # X = (r + beta)(gamma r + delta)^{-1} = Xt / |gamma r + delta|^2, Xt = (r + beta) conj(gamma r + delta)
        Xt = (rr + bL) * (gL * rr + dL).conj()
        nx = (gL * rr + dL).norm()
        Yt = (rr + bR) * (gR * rr + dR).conj()
        ny = (gR * rr + dR).norm()
        ht = Yt * c * Xt + Yt * d * nx - a * Xt * ny - b * (nx * ny)
        ok.append(ht.is_zero())
    mp = [(g[12 + j], g[j]) for j in range(12)]
    mco = [Qn([t.compose(mp) for t in q.c]) for q in co]
    Kq = Qn([ns, zer, zer, zer])
    diag_ok = mco[0].is_zero() and (mco[1] - Kq).is_zero() and (mco[2] + Kq).is_zero() and mco[3].is_zero()
    log(f"[II'] one generic quaternionic Mobius map nu (12 params per factor), generic seed point t in H:"
        f" h(nu^(1) t, nu^(2) t) = 0 identically in t: {ok};")
    log(f"      m(C) = m(B) = 0, m(D) = -m(A) = |delta - gamma beta|^2: {diag_ok}  ({time.time() - T0:.0f}s)")
    return all(ok) and diag_ok


# ---------------------------------------------------------------- Part IV: end-to-end test at exact rational values
def part_end_to_end(univ, dim, seed):
    """Specialise ALL symbols (left and right independently) to exact rationals, build P from the universal M,
    and evaluate OAI's (1,a)^T P (1,a') at the 6 points; then the diagonal test. A test of the glue (code and
    composition), not a proof by itself: the proof is I + II + III."""
    R, names, M = univ
    rng = random.Random(seed)
    rnd = lambda: QQ(rng.randint(-9, 9), rng.randint(1, 7))
    ncomp = {4: 4, 3: 3, 2: 2, 1: 1}[dim]        # S^4: x in H; S^3: span{1,i,j}; S^2: C; S^1: R

    def pt():
        return [rnd() for _ in range(ncomp)] + [QQ(0)] * (4 - ncomp)

    QQring = lambda v: Qn([QQ(t) for t in v])
    left = [pt() for _ in range(6)]
    right = [pt() for _ in range(6)]
    res = []
    for diag in (False, True):
        Rp = left if diag else right
        X = [QQring(v) for v in left]
        Y = [QQring(v) for v in Rp]
        c1 = three_point_coeffs(X[:3], Y[:3])
        c2 = three_point_coeffs(X[3:], Y[3:])
        sub = {}
        for k, cc in ((1, c1), (2, c2)):
            for L, qq in zip("CDAB", cc):
                for t in range(4):
                    sub[names.index(f"{L}{k}_{t}")] = qq.c[t]
        Mn = sp.zeros(NQ, NQ)
        for j in range(NQ):
            for k in range(NQ):
                val = QQ(0)
                for mono, cf in M[j][k].terms():
                    term = cf
                    for i, e in enumerate(mono):
                        if e:
                            term *= sub[i] ** e
                    val += term
                Mn[j, k] = sp.Rational(int(val.numerator), int(val.denominator))
        P = Ci.T * Mn * Ci
        keep = list(range(1 + ncomp)) + [5]           # drop the q-coordinates that are identically 0
        Pk = P.extract(keep, keep)
        if not diag:
            evs = []
            for i in range(6):
                def p_of(v):
                    n = sum(sp.Rational(int(t.numerator), int(t.denominator))**2 for t in v)
                    a = [2 * sp.Rational(int(t.numerator), int(t.denominator)) / (1 + n) for t in v[:ncomp]]
                    return sp.Matrix([1] + a + [(n - 1) / (1 + n)])
                evs.append((p_of(left[i]).T * Pk * p_of(right[i]))[0] == 0)
            res.append(all(evs))
        else:
            c = Pk[1, 1]
            Sk = sp.diag(-1, *([1] * (len(keep) - 1)))
            res.append(c != 0 and Pk == c * Sk)
    log(f"[IV] end-to-end at exact rationals, S^{dim}: (1,a_i)^T P (1,a_i') = 0 for all 6 (left != right): {res[0]};"
        f"  on the diagonal P = c S_{dim + 1}, c != 0: {res[1]}")
    return all(res)


def part_end_to_end_mobius(univ, seed):
    """two quaternionic Mobius maps with independent exact rational parameters on the two sides, 5 rational seeds
    per group: OAI evaluations (1,a)^T P (1,a') = 0 on S^4 for all 10 points, and P = c S on the diagonal.
    A test of code + composition (II' + V not used: alpha = 1); the proof is I + II' + III."""
    R, names, M = univ
    rng = random.Random(seed)
    rnd = lambda: QQ(rng.randint(-9, 9), rng.randint(1, 7))
    ONE = Qn([QQ(1), QQ(0), QQ(0), QQ(0)])
    par = lambda: (Qn([rnd() for _ in range(4)]), Qn([rnd() for _ in range(4)]), Qn([rnd() for _ in range(4)]))
    seeds = [[Qn([rnd() for _ in range(4)]) for _ in range(5)] for _ in range(2)]
    PL = [par(), par()]
    PR = [par(), par()]
    res = []
    for diag in (False, True):
        PRk = PL if diag else PR
        sub = {}
        for k in (0, 1):
            (c, d, a, b), _ = mu_coeffs(*PL[k], *PRk[k], ONE)
            for L, qq in zip("CDAB", (c, d, -a, -b)):
                for t in range(4):
                    sub[names.index(f"{L}{k + 1}_{t}")] = qq.c[t]
        Mn = sp.zeros(NQ, NQ)
        for j in range(NQ):
            for k in range(NQ):
                val = QQ(0)
                for mono, cf in M[j][k].terms():
                    term = cf
                    for i, e in enumerate(mono):
                        if e:
                            term *= sub[i] ** e
                    val += term
                Mn[j, k] = sp.Rational(int(val.numerator), int(val.denominator))
        P = Ci.T * Mn * Ci
        if diag:
            res.append(P[1, 1] != 0 and P == P[1, 1] * S)
            continue
        evs = []
        for k in (0, 1):
            for r in seeds[k]:
                def img(pr):
                    be, ga, de = pr
                    den = ga * r + de
                    X = (r + be) * den.conj() * (QQ(1) / den.norm())
                    return [sp.Rational(int(t.numerator), int(t.denominator)) for t in X.c]
                def p_of(v):
                    n = sum(t**2 for t in v)
                    return sp.Matrix([1] + [2 * t / (1 + n) for t in v] + [(n - 1) / (1 + n)])
                evs.append((p_of(img(PL[k])).T * P * p_of(img(PR[k])))[0] == 0)
        res.append(all(evs))
    log(f"[IV'] end-to-end at exact rationals, S^4, two Mobius maps x 5 rational seeds (left != right): all 10 "
        f"evaluations 0: {res[0]};  diagonal P = c S_5, c != 0: {res[1]}")
    return all(res)


# ---------------------------------------------------------------- Part V: general leading coefficient
def part_left_factor():
    """nu = L_alpha o nu0 (x -> alpha nu0(x)) covers (alpha t + beta)(gamma t + delta)^{-1} with alpha != 0.
    If h0 = y C0 x + y D0 + A0 x + B0 is the graph form of mu0 = nu0^(2) o (nu0^(1))^{-1}, then
    C = C0 abar, D = n D0, A = alpha' A0 abar, B = n alpha' B0  (n = |alpha|^2 left, alpha' right factor) satisfy
    n' (y C x + y D + A x + B) = alpha' * [n n' h0(abar x / n, abar' y / n')]   (polynomial identity checked here),
    so h vanishes on the graph of mu = L_alpha' o mu0 o L_alpha^{-1}; on the diagonal kappa -> n kappa."""
    names = ([f"{L}{t}" for L in ("C0", "D0", "A0", "B0", "al", "ar") for t in range(4)]
             + [f"x{t}" for t in range(4)] + [f"y{t}" for t in range(4)])
    R, *g = ring(",".join(names), QQ)
    Qs = [Qn(g[4 * i:4 * i + 4]) for i in range(8)]
    C0, D0, A0, B0, al, ar, x, y = Qs
    n, n2 = al.norm(), ar.norm()
    C, D, A, B = C0 * al.conj(), D0 * n, ar * A0 * al.conj(), ar * B0 * n
    lhs = h_eval((C, D, A, B), x, y) * n2
    xs, ys = al.conj() * x, ar.conj() * y          # n x', n' y'
    rhs = ar * (ys * C0 * xs + ys * D0 * n + A0 * xs * n2 + B0 * (n * n2))
    ok = (lhs - rhs).is_zero()
    log(f"[V] general leading coefficient alpha: n'(yCx + yD + Ax + B) = alpha' [n n' h0(alpha^-1 x, alpha'^-1 y)]: {ok}")
    return ok


if __name__ == "__main__":
    r0 = coordinate_checks()
    r1, univ = part_universal()
    r2 = part_instance()
    r2b = part_mobius_rational()
    r5 = part_left_factor()
    r4 = all(part_end_to_end(univ, dim, 100 + dim) for dim in (4, 3, 2, 1))
    r4 = part_end_to_end_mobius(univ, 7) and r4
    log(f"ALL CHECKS PASS: {r0 and r1 and r2 and r2b and r4 and r5}  (sympy {sp.__version__}; {time.time() - T0:.0f}s)")
