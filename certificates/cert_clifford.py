"""Exact two-group certificates via Clifford paravectors and Vahlen matrices: S^5 in R^6 (d = 6), Cl_{0,4}.

applies_to: finite subsets of S^n (pole e_{n+1} avoided) that are a union of two Mobius images nu_1(A'_1) u
  nu_2(A'_2) of finite rational point sets, for every Mobius map nu of the chart R^n u {inf} with
  nu(inf) != inf, written in the Vahlen normal form nu(t) = q + lam w (t + p)^{-1} w^^{-1} (w a product of
  paravectors).  Full certificate run: n = 5 (S^5, d = 6, Cl_{0,4}).  The universal identity [I]/[III] and the
  one-step Lipschitz lemma [L] are also run for n = 2..7 (S^2..S^7).  The identities are ring identities over
  Q, so they hold for ANY values of the symbols in any commutative Q-algebra B (B = F (x)_Q F, or R (x)_Q R via
  OAI Prop 2.1).  Exact sympy only; no mod-p step anywhere.

Algebra: Cl_{0,k}, k = n - 1, generators e_1..e_k with e_i^2 = -1 (dimension 2^k).  Paravectors
x = x_0 + x_1 e_1 + ... + x_k e_k form the chart R^n of S^n.  Involutions: reversion a*, grade involution a^,
Clifford conjugation abar = (a^)*.  For paravectors x xbar = |x|^2, and Re(a bbar) = sum_I a_I b_I.
Coordinates (as cert_s2_quat.py): a(x) = (2x, |x|^2 - 1)/(1 + |x|^2), p = (1, a) = q/(1+|x|^2),
    q = (1+|x|^2, 2x, |x|^2-1) = C b,  b(x) = (1, x_0..x_k, |x|^2),  q(x)^T S q(y) = -2|x - y|^2,  S = diag(-1, I_{n+1}).
Construction (the quaternionic one of cert_s2_quat.py, carried to Cl): for a Vahlen matrix mu = [[a, b], [c, d]] put h(x, y) = y c x + y d - a x - b,
    f(x, y) = Re(h_1(x, y) conj(h_2(x, y)))   = b(x)^T M b(y)   (part I, M free of x, y).
Normal form (part II'): N = T(q) D(lam w, w^) J T(p) = [[q w^, lam w + q w^ p], [w^, w^ p]], acting as
    nu(t) = (N11 t + N12)(N21 t + N22)^{-1} = q + lam w (t + p)^{-1} (w^)^{-1}.
mu = nu^(2) o (nu^(1))^{-1} has matrix N^(2) adj(N^(1)), adj([[a,b],[c,d]]) = [[d*, -b*], [-c*, a*]].
Non-division issue: generic (beta, gamma, delta) in Cl_4 do NOT give a Mobius map; the normal form is used
instead, and every inverse taken is of a paravector or of w^ (norms are pure-tensor scalars, units of B).
Run (from any directory):  python3 -I cert_clifford.py   (about 40 min; prints elapsed seconds)
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


def el():
    return f"({time.time() - T0:.0f}s)"


# ---------------------------------------------------------------- Clifford algebra Cl_{0,k}
class Cl:
    """Cl_{0,k} over a commutative ring; elements are lists of 2^k coefficients indexed by blade bitmask."""

    def __init__(self, k, zero):
        self.k, self.dim, self.zero = k, 1 << k, zero
        self.tab = [[self._blade_mul(A, B) for B in range(self.dim)] for A in range(self.dim)]
        g = [bin(A).count("1") for A in range(self.dim)]
        self.rev_s = [(-1) ** (r * (r - 1) // 2) for r in g]
        self.inv_s = [(-1) ** r for r in g]
        self.con_s = [a * b for a, b in zip(self.rev_s, self.inv_s)]
        self.para_idx = [0] + [1 << i for i in range(k)]

    @staticmethod
    def _blade_mul(A, B):
        s, a = 0, A >> 1
        while a:                                   # reordering sign
            s += bin(a & B).count("1")
            a >>= 1
        s += bin(A & B).count("1")                 # e_i^2 = -1
        return (-1 if s % 2 else 1), A ^ B

    def mul(self, a, b):
        if hasattr(self.zero, "ring"):
            return self._mul_poly(a, b)
        out = [self.zero] * self.dim
        nb = [(B, y) for B, y in enumerate(b) if y]
        for A, x in enumerate(a):
            if not x:
                continue
            row = self.tab[A]
            for B, y in nb:
                s, C = row[B]
                if s > 0:
                    out[C] = out[C] + x * y
                else:
                    out[C] = out[C] - x * y
        return out

    def _mul_poly(self, a, b):
        """same product over a sympy PolyRing; per-blade dict accumulation (no repeated copying of partial sums)"""
        R = self.zero.ring
        acc = [dict() for _ in range(self.dim)]
        nb = [(B, y) for B, y in enumerate(b) if y]
        for A, x in enumerate(a):
            if not x:
                continue
            row = self.tab[A]
            for B, y in nb:
                s, C = row[B]
                d = acc[C]
                for m, c in (x * y).items():
                    v = d.get(m)
                    if s > 0:
                        d[m] = c if v is None else v + c
                    else:
                        d[m] = -c if v is None else v - c
        return [R.from_dict({m: c for m, c in d.items() if c}) for d in acc]

    def re_mul(self, a, b):
        """scalar part of the product a b, read off the same multiplication table (only B = A contributes)"""
        out = self.zero
        for A, (x, y) in enumerate(zip(a, b)):
            if x and y:
                out = out + x * y if self.tab[A][A][0] > 0 else out - x * y
        return out

    def add(self, a, b):
        return [x + y for x, y in zip(a, b)]

    def sub(self, a, b):
        return [x - y for x, y in zip(a, b)]

    def neg(self, a):
        return [-x for x in a]

    def smul(self, s, a):                          # central scalar
        return [s * x for x in a]

    def rev(self, a):
        return [s * x for s, x in zip(self.rev_s, a)]

    def hat(self, a):
        return [s * x for s, x in zip(self.inv_s, a)]

    def conj(self, a):
        return [s * x for s, x in zip(self.con_s, a)]

    def scalar(self, s):
        return [s] + [self.zero] * (self.dim - 1)

    def para(self, comps):
        out = [self.zero] * self.dim
        for i, c in zip(self.para_idx, comps):
            out[i] = c
        return out

    def is_zero(self, a):
        return all(x == 0 for x in a)

    def is_scalar(self, a):
        return all(x == 0 for x in a[1:])

    def is_para(self, a):
        return all(x == 0 for i, x in enumerate(a) if i not in self.para_idx)

    def pcomps(self, a):
        return [a[i] for i in self.para_idx]

    def mulall(self, *xs):
        r = xs[0]
        for x in xs[1:]:
            r = self.mul(r, x)
        return r


# ---------------------------------------------------------------- [0] algebra axioms and coordinates
def part_algebra(k):
    dim = 1 << k
    names = [f"a{I}" for I in range(dim)] + [f"b{I}" for I in range(dim)] + [f"c{I}" for I in range(dim)]
    names += [f"x{i}" for i in range(k + 1)] + [f"y{i}" for i in range(k + 1)]
    R, *g = ring(",".join(names), QQ)
    A = Cl(k, R.zero)
    a, b, c = g[:dim], g[dim:2 * dim], g[2 * dim:3 * dim]
    x = A.para(g[3 * dim:3 * dim + k + 1])
    y = A.para(g[3 * dim + k + 1:])
    one = R.one
    e = [A.para([R.zero] * (i + 1) + [one] + [R.zero] * (k - 1 - i)) for i in range(k)]
    gens_ok = all(A.mul(e[i], e[i]) == A.scalar(-one) for i in range(k)) and all(
        A.add(A.mul(e[i], e[j]), A.mul(e[j], e[i])) == A.scalar(R.zero) for i in range(k) for j in range(i + 1, k))
    assoc = A.is_zero(A.sub(A.mul(A.mul(a, b), c), A.mul(a, A.mul(b, c))))
    ab = A.mul(a, b)
    anti = (A.conj(ab) == A.mul(A.conj(b), A.conj(a)) and A.rev(ab) == A.mul(A.rev(b), A.rev(a))
            and A.hat(ab) == A.mul(A.hat(a), A.hat(b)) and A.conj(a) == A.rev(A.hat(a)))
    cyc = ab[0] == A.mul(b, a)[0] and A.re_mul(a, b) == ab[0]
    dot = A.mul(a, A.conj(b))[0] == sum((s * t for s, t in zip(a, b)), R.zero)
    nx = sum((t * t for t in A.pcomps(x)), R.zero)
    xx = A.mul(x, A.conj(x)) == A.scalar(nx) and A.mul(A.conj(x), x) == A.scalar(nx)
    pinv = A.hat(x) == A.conj(x) and A.rev(x) == x
    ok = gens_ok and assoc and anti and cyc and dot and xx and pinv
    log(f"[0] Cl_(0,{k}) (dim {dim}): e_i^2 = -1, e_i e_j = -e_j e_i: {gens_ok} | associative (3 generic elements): "
        f"{assoc} | (ab)bar = bbar abar, (ab)* = b* a*, (ab)^ = a^ b^, abar = (a^)*: {anti} | Re(ab) = Re(ba) (= table scalar part): {cyc}"
        f" | Re(a bbar) = sum a_I b_I: {dot} | paravector x xbar = xbar x = |x|^2, x^ = xbar, x* = x: {xx and pinv}  {el()}")
    return ok


def coord_mats(n):
    NQ = n + 2
    Cm = sp.zeros(NQ, NQ)
    Cm[0, 0] = 1; Cm[0, NQ - 1] = 1
    for al in range(n):
        Cm[al + 1, al + 1] = 2
    Cm[NQ - 1, 0] = -1; Cm[NQ - 1, NQ - 1] = 1
    return Cm, Cm.inv(), sp.diag(-1, *([1] * (n + 1)))


def coordinate_checks(n):
    NQ = n + 2
    Cm, Ci, S = coord_mats(n)
    x = sp.symbols(f"x0:{n}", real=True)
    y = sp.symbols(f"y0:{n}", real=True)
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
    log(f"[0] S^{n} coordinates: |a(x)| = 1: {on_sphere} | q = C b: {q_is_Cb} | q^T S q' = -2|x-y|^2: {s_ident}"
        f" | q^T (C^-T M C^-1) q' = b^T M b' (symbolic M): {conv}")
    return on_sphere and q_is_Cb and s_ident and conv


def to_P(M, Ci, NQ):
    """P = C^-T M C^-1 over a polynomial ring (M a list of lists)."""
    out = []
    for al in range(NQ):
        row = []
        for be in range(NQ):
            acc = None
            for r in range(NQ):
                for s in range(NQ):
                    cf = Ci[r, al] * Ci[s, be]
                    if cf != 0:
                        t = M[r][s] * QQ(int(sp.numer(cf)), int(sp.denom(cf)))
                        acc = t if acc is None else acc + t
            row.append(acc)
        out.append(row)
    return out


# ---------------------------------------------------------------- [I] + [III] universal identity
def part_universal(n, verbose=True):
    k = n - 1
    dim = 1 << k
    NQ = n + 2
    cn = [f"{L}{j}_{I}" for j in (1, 2) for L in "CDAB" for I in range(dim)]
    names = cn + [f"x{t}" for t in range(n)] + [f"y{t}" for t in range(n)] + ["k1", "k2"]
    R, *g = ring(",".join(names), QQ)
    A = Cl(k, R.zero)
    pos = {nm: i for i, nm in enumerate(names)}
    co = {(j, L): [g[pos[f"{L}{j}_{I}"]] for I in range(dim)] for j in (1, 2) for L in "CDAB"}
    xs = [g[pos[f"x{t}"]] for t in range(n)]
    ys = [g[pos[f"y{t}"]] for t in range(n)]
    x, y = A.para(xs), A.para(ys)
    k1, k2 = g[pos["k1"]], g[pos["k2"]]

    def h(j):
        C, D, Aa, B = (co[(j, L)] for L in "CDAB")
        return A.add(A.add(A.mul(A.mul(y, C), x), A.mul(y, D)), A.add(A.mul(Aa, x), B))

    h1, h2 = h(1), h(2)
    f = A.re_mul(h1, A.conj(h2))
    ix = [pos[f"x{t}"] for t in range(n)]
    iy = [pos[f"y{t}"] for t in range(n)]

    def slot(exps, idxs):
        e = [exps[i] for i in idxs]
        if sum(e) == 0:
            return 0
        if sum(e) == 1:
            return 1 + e.index(1)
        if e[0] == 2 and sum(e) == 2:
            return NQ - 1          # read |x|^2 off the x0^2 coefficient; the reconstruction checks the rest
        return None

    M = [[R.zero] * NQ for _ in range(NQ)]
    for mono, cf in f.terms():
        j, kk = slot(mono, ix), slot(mono, iy)
        if j is None or kk is None:
            continue
        rest = list(mono)
        for i in ix + iy:
            rest[i] = 0
        M[j][kk] += R({tuple(rest): cf})
    bx = [R.one] + xs + [sum(t * t for t in xs)]
    by = [R.one] + ys + [sum(t * t for t in ys)]
    recon = R.zero
    for j in range(NQ):
        for kk in range(NQ):
            recon += bx[j] * M[j][kk] * by[kk]
    span_ok = (recon - f) == 0
    no_xy = all(all(mono[i] == 0 for i in ix + iy for mono in M[j][kk].monoms())
                for j in range(NQ) for kk in range(NQ) if M[j][kk] != 0)
    # III: C = B = 0, D = kappa, A = -kappa (scalar kappa) in both forms
    sub = []
    for j, kk in ((1, k1), (2, k2)):
        for L, s0 in (("C", R.zero), ("B", R.zero), ("D", kk), ("A", -kk)):
            for I in range(dim):
                sub.append((g[pos[f"{L}{j}_{I}"]], s0 if I == 0 else R.zero))
    Md = [[M[r][s].compose(sub) for s in range(NQ)] for r in range(NQ)]
    _, Ci, S = coord_mats(n)
    Pd = to_P(Md, Ci, NQ)
    target = -QQ(1, 2) * k1 * k2
    mS_ok = all((Pd[al][be] - target * int(S[al, be])) == 0 for al in range(NQ) for be in range(NQ))
    if verbose:
        log(f"[I] S^{n} (Cl_(0,{k})): Re(h1 conj h2) = b(x)^T M b(y), M bilinear in the {len(cn)} coefficient symbols, "
            f"free of x, y: {span_ok and no_xy}  (f has {len(f)} terms)")
        log(f"[III] S^{n}: at C = B = 0, D = kappa, A = -kappa: P = C^-T M C^-1 = -(kappa1 kappa2 / 2) S_{n + 1}: {mS_ok}  {el()}")
    return span_ok and no_xy and mS_ok, (R, names, M)


# ---------------------------------------------------------------- [L] one-step Lipschitz lemma
def part_lipschitz_step(n):
    """For paravectors p, s: p pbar = pbar p = |p|^2, and p s p = 2<p, sbar> p - |p|^2 sbar (a paravector).
    By induction, for w = p_1...p_m:  w wbar = wbar w = w^ w* = w* w^ = |w|^2 (scalar) and w s w* is a paravector."""
    k = n - 1
    R, *g = ring(",".join([f"p{i}" for i in range(n)] + [f"s{i}" for i in range(n)]), QQ)
    A = Cl(k, R.zero)
    p, s = A.para(g[:n]), A.para(g[n:])
    sb = A.conj(s)
    np_ = sum((t * t for t in g[:n]), R.zero)
    ip = sum((u * v for u, v in zip(A.pcomps(p), A.pcomps(sb))), R.zero)
    lhs = A.mulall(p, s, p)
    rhs = A.sub(A.smul(2 * ip, p), A.smul(np_, sb))
    ok = lhs == rhs and A.mul(p, A.conj(p)) == A.scalar(np_) and A.mul(A.conj(p), p) == A.scalar(np_)
    return ok


# ---------------------------------------------------------------- [II'] Vahlen normal form, one tensor factor
def vahlen_N(A, w, lam, p, q):
    wh = A.hat(w)
    a = A.mul(q, wh)
    b = A.add(A.smul(lam, w), A.mul(a, p))
    c = wh
    d = A.mul(wh, p)
    return a, b, c, d


def adj(A, N):
    a, b, c, d = N
    return A.rev(d), A.neg(A.rev(b)), A.neg(A.rev(c)), A.rev(a)


def mat_mul(A, N1, N2):
    a, b, c, d = N1
    e, f, g, h = N2
    return (A.add(A.mul(a, e), A.mul(b, g)), A.add(A.mul(a, f), A.mul(b, h)),
            A.add(A.mul(c, e), A.mul(d, g)), A.add(A.mul(c, f), A.mul(d, h)))


def part_vahlen(n, nfac):
    """Symbolic, one tensor factor.  w = p_1 ... p_nfac (generic paravectors), lam scalar, p, q, t paravectors.
    t enters only through s = t + p (t := s - p is a change of polynomial variables)."""
    k = n - 1
    names = [f"w{j}_{i}" for j in range(nfac) for i in range(n)] + ["lam"]
    names += [f"p{i}" for i in range(n)] + [f"q{i}" for i in range(n)] + [f"s{i}" for i in range(n)]
    R, *g = ring(",".join(names), QQ)
    A = Cl(k, R.zero)
    pos = {nm: i for i, nm in enumerate(names)}
    ps = [A.para([g[pos[f"w{j}_{i}"]] for i in range(n)]) for j in range(nfac)]
    lam = g[pos["lam"]]
    p = A.para([g[pos[f"p{i}"]] for i in range(n)])
    q = A.para([g[pos[f"q{i}"]] for i in range(n)])
    s = A.para([g[pos[f"s{i}"]] for i in range(n)])
    t = A.sub(s, p)
    w = A.mulall(*ps)
    wh, ws, wb = A.hat(w), A.rev(w), A.conj(w)
    nw = R.one
    for pp in ps:
        nw *= sum((u * u for u in A.pcomps(pp)), R.zero)
    ns = sum((u * u for u in A.pcomps(s)), R.zero)
    # (V0) Lipschitz norms
    v0 = all(A.mul(*pr) == A.scalar(nw) for pr in ((w, wb), (wb, w), (wh, ws), (ws, wh)))
    # (V0') rotation part maps paravectors to paravectors
    v0b = A.is_para(A.mulall(w, s, ws))
    N = vahlen_N(A, w, lam, p, q)
    a, b, c, d = N
    u = A.add(A.mul(c, t), d)                       # = w^ s
    ub = A.conj(u)
    nn = A.mul(u, ub)
    v1 = A.is_scalar(nn) and A.mul(ub, u) == nn and nn[0] == ns * nw and u == A.mul(wh, s)
    at_b = A.add(A.mul(a, t), b)                     # = q u + lam w
    v2a = at_b == A.add(A.mul(q, u), A.smul(lam, w))
    log(f"[II'] S^{n}, w = product of {nfac} generic paravectors ({len(names)} symbols, one tensor factor):")
    log(f"      (V0) w wbar = wbar w = w^ w* = w* w^ = |w|^2 (scalar): {v0} | w s w* is a paravector: {v0b}  {el()}")
    log(f"      (V1) u = N21 t + N22 = w^ (t+p);  n = u ubar = ubar u = |t+p|^2 |w|^2 (scalar): {v1}  {el()}")
    Xt = A.mul(at_b, ub)                             # X~ = (N11 t + N12) ubar ;  nu(t) = X~ / n
    v2 = v2a and A.is_para(Xt)
    log(f"      (V2) X~ = (N11 t + N12) ubar is a paravector (so nu(t) = X~/n lies in the chart R^{n}): {v2}"
        f"  (terms {sum(len(z) for z in Xt)})  {el()}")
    Delta = -lam * nw
    AN = mat_mul(A, adj(A, N), N)
    NA = mat_mul(A, N, adj(A, N))
    sc = A.scalar(Delta)
    zz = A.scalar(R.zero)
    v3 = AN == (sc, zz, zz, sc) and NA == (sc, zz, zz, sc)
    log(f"      (V3) adj(N) N = N adj(N) = Delta I, Delta = -lam |w|^2 (pure-tensor scalar): {v3}  {el()}")
    return v0 and v0b and v1 and v2 and v3


# ---------------------------------------------------------------- [IV'] end-to-end at exact rationals
def rat(v):
    return sp.Rational(int(v.numerator), int(v.denominator))


def part_end_to_end(n, univ, seed, nfac, nseed=5):
    """Two Mobius maps per side (left/right parameters chosen independently: B = F (x) F simulated by independent
    rationals), nseed rational seeds per group.  Points are computed INDEPENDENTLY of the Vahlen matrix, as
    nu(t) = q + lam w (t+p)^{-1} (w^)^{-1} with honest inverses.  OAI evaluations (1,a)^T P (1,a') must vanish;
    on the diagonal (right = left) P = c S, c != 0.  Control: a third group's points give nonzero evaluations."""
    R, names, M = univ
    k = n - 1
    NQ = n + 2
    A = Cl(k, QQ(0))
    rng = random.Random(seed)
    rnd = lambda: QQ(rng.randint(-9, 9), rng.randint(1, 7))
    rpara = lambda: A.para([rnd() for _ in range(n)])

    def par():
        lam = QQ(0)
        while lam == 0:
            lam = rnd()
        return [rpara() for _ in range(nfac)], lam, rpara(), rpara()

    def pinv(x):
        nx = sum((t * t for t in A.pcomps(x)), QQ(0))
        return A.smul(QQ(1) / nx, A.conj(x))

    def nu(pr, t):
        ws, lam, p, q = pr
        w = A.mulall(*ws)
        nw = A.mul(w, A.conj(w))[0]
        whinv = A.smul(QQ(1) / nw, A.rev(w))
        assert A.mul(A.hat(w), whinv) == A.scalar(QQ(1))
        X = A.add(q, A.smul(lam, A.mulall(w, pinv(A.add(t, p)), whinv)))
        assert A.is_para(X)
        return A.pcomps(X)

    def nmat(pr):
        ws, lam, p, q = pr
        return vahlen_N(A, A.mulall(*ws), lam, p, q)

    seeds = [[rpara() for _ in range(nseed)] for _ in range(3)]
    PL = [par(), par(), par()]
    PR = [par(), par(), par()]
    _, Ci, S = coord_mats(n)
    pos = {nm: i for i, nm in enumerate(names)}

    def p_of(v):
        v = [rat(t) for t in v]
        nv = sum(t**2 for t in v)
        return sp.Matrix([1] + [2 * t / (1 + nv) for t in v] + [(nv - 1) / (1 + nv)])

    res = []
    conformal = True
    for diag in (False, True):
        PRk = PL if diag else PR
        sub = {}
        for j in (0, 1):
            mu = mat_mul(A, nmat(PRk[j]), adj(A, nmat(PL[j])))
            a, b, c, d = mu
            for L, qq in zip("CDAB", (c, d, A.neg(a), A.neg(b))):
                for I in range(A.dim):
                    sub[pos[f"{L}{j + 1}_{I}"]] = qq[I]
        Mn = sp.zeros(NQ, NQ)
        for r in range(NQ):
            for s_ in range(NQ):
                val = QQ(0)
                for mono, cf in M[r][s_].terms():
                    term = cf
                    for i, e in enumerate(mono):
                        if e:
                            term *= sub[i] ** e
                    val += term
                Mn[r, s_] = rat(val)
        P = Ci.T * Mn * Ci
        if diag:
            c0 = P[1, 1]
            res.append(c0 != 0 and P == c0 * S)
            continue
        evs, ctrl = [], []
        for j in (0, 1, 2):
            for t in seeds[j]:
                X, Y = nu(PL[j], t), nu(PR[j], t)
                val = (p_of(X).T * P * p_of(Y))[0]
                (evs if j < 2 else ctrl).append(val == 0)
        res.append(all(evs))
        res.append(not any(ctrl))
        # conformality of the normal form (test of the hand lemma): |nu x - nu y|^2 = lam^2 |x-y|^2 / (|x+p|^2 |y+p|^2)
        for pr in PL[:2]:
            ws, lam, p, q = pr
            for t1, t2 in ((seeds[0][0], seeds[0][1]), (seeds[1][2], seeds[1][3])):
                X1, X2 = nu(pr, t1), nu(pr, t2)
                n12 = sum(((u - v) ** 2 for u, v in zip(X1, X2)), QQ(0))
                d12 = sum(((u - v) ** 2 for u, v in zip(A.pcomps(t1), A.pcomps(t2))), QQ(0))
                np1 = sum((u * u for u in A.pcomps(A.add(t1, p))), QQ(0))
                np2 = sum((u * u for u in A.pcomps(A.add(t2, p))), QQ(0))
                conformal = conformal and n12 == lam * lam * d12 / (np1 * np2)
    log(f"[IV'] end-to-end at exact rationals, S^{n}: two normal-form Mobius maps x {nseed} rational seeds, left != right: "
        f"all {2 * nseed} OAI evaluations (1,a)^T P (1,a') = 0: {res[0]};  diagonal P = c S_{n + 1}, c != 0: {res[2]}")
    log(f"      control: third group, all {nseed} evaluations nonzero: {res[1]};  normal form is conformal with the"
        f" inversion distortion (4 pairs): {conformal}  {el()}")
    return res[0] and res[2] and conformal, res[1]


if __name__ == "__main__":
    N = 5
    NFAC = 2 * (N // 2)                     # Cartan-Dieudonne: SO(n) = products of <= 2 floor(n/2) reflections
    r_alg = all([part_algebra(k) for k in range(1, 7)])      # Cl_(0,1) .. Cl_(0,6): charts R^2 .. R^7
    r_coord = coordinate_checks(N)
    r_univ, univ = part_universal(N)
    r_lip = all(part_lipschitz_step(n) for n in range(1, 8))
    log(f"[L] one-step Lipschitz lemma, n = 1..7: p pbar = pbar p = |p|^2 and p s p = 2<p, sbar> p - |p|^2 sbar: {r_lip}  {el()}")
    r_v = part_vahlen(N, NFAC)
    r_e2e, r_ctrl = part_end_to_end(N, univ, 6, NFAC)
    r_e2e = part_end_to_end(N, univ, 66, NFAC)[0] and r_e2e
    # every dimension: the universal identity [I] + [III] and the normal-form identities, smaller n
    other = []
    for n in (2, 3, 4, 6, 7):
        ok, _ = part_universal(n, verbose=False)
        other.append((n, ok))
    log(f"[I]+[III] universal identity, S^n for n = 2, 3, 4, 6, 7 (Cl_(0,n-1)): {other}  {el()}")
    vs = []
    for n in (2, 3, 4):
        vs.append((n, part_vahlen(n, 2 * (n // 2))))
    log(f"[II'] normal-form Vahlen identities for n = 2, 3, 4: {vs}  {el()}")
    r_other = all(o for _, o in other) and all(o for _, o in vs)
    allok = r_alg and r_coord and r_univ and r_lip and r_v and r_e2e and r_ctrl and r_other
    log(f"ALL CHECKS PASS: {allok}  (sympy {sp.__version__}; {time.time() - T0:.0f}s)")
