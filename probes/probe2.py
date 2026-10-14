"""Second-order ("2-jet") necessary test and full-order curve probe for the OpenAI #172
Euclidean-Ramsey criterion, for finite subsets of the unit sphere S^{d-1} in R^d.

Setup: coordinates are rational functions (optionally with square roots) of k transcendental
parameters theta_1..theta_k (algebraically independent).  Specialize theta to random values
mod a prime (default 2^31-1; env PROBE_PRIME overrides); derivations D_j = d/dtheta_j are carried by first-order jets.

2-jet test (derived by Taylor-expanding a criterion solution P(T,U) at the diagonal U = T + e,
with P_0 = c*S, S = diag(-1, I_d)):
  unknowns c, P_j (j<k, (d+1)x(d+1)), Q_jl (j<=l, symmetric)
  order 1:  p_i^T P_j p_i = 0
  order 2:  -c <D_j a_i, D_l a_i> + p_i^T P_j D_l p_i + p_i^T P_l D_j p_i + p_i^T Q_jl p_i = 0
  NECESSARY for Ramsey: solvable with c = 1.

Curve probe: restrict to U = T + e*w (random direction w); compute lim_{e->0} ker D(T, T+ew)
via truncated power series; NECESSARY: I_d in the spatial span of that limit space.
(For k = 1 this is the full criterion.)
"""
import os
import random
import numpy as np

# Default 2^31 - 1 (= 3 mod 4).  The environment variable PROBE_PRIME, read once at import, selects
# another prime (e.g. one = 1 mod 4, where -1 is a residue).  It must be set before the first
# `import probe2` so that every `from probe2 import *` sees the same P.  P < 2^31.5 keeps the int64
# products in rank_mod exact.  Unset = the default prime.
P = int(os.environ.get("PROBE_PRIME", "2147483647"))
assert 2 < P < 3037000499 and pow(2, P - 1, P) == 1, "PROBE_PRIME must be an odd prime below 2^31.5"


def inv(a):
    return pow(int(a) % P, P - 2, P)


def _tonelli(a):
    """sqrt of a QR a mod P for P = 1 mod 4 (Tonelli-Shanks); deterministic in a."""
    q, s = P - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (P - 1) // 2, P) != P - 1:
        z += 1
    m, c, t, r = s, pow(z, q, P), pow(a, q, P), pow(a, (q + 1) // 2, P)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % P
            i += 1
        b = pow(c, 1 << (m - i - 1), P)
        m, c, t, r = i, b * b % P, t * b * b % P, r * b % P
    return r


def sqrtmod(a):
    a %= P
    if P % 4 == 3:
        r = pow(a, (P + 1) // 4, P)
    elif a == 0 or pow(a, (P - 1) // 2, P) != 1:
        r = 0 if a == 0 else None
    else:
        r = _tonelli(a)
    if r is None or r * r % P != a:
        raise ValueError("nonresidue")
    return r


def R(a, b=1):
    return a % P * inv(b) % P


# ---------------------------------------------------------------- first-order jets
class J:
    __slots__ = ("v", "d")

    def __init__(s, v, d):
        s.v = v % P
        s.d = [x % P for x in d]

    def _l(s, o):
        return o if isinstance(o, J) else J(o, [0] * len(s.d))

    def __add__(s, o):
        o = s._l(o)
        return J(s.v + o.v, [a + b for a, b in zip(s.d, o.d)])
    __radd__ = __add__

    def __neg__(s):
        return J(-s.v, [-a for a in s.d])

    def __sub__(s, o):
        return s + (-s._l(o))

    def __rsub__(s, o):
        return s._l(o) + (-s)

    def __mul__(s, o):
        o = s._l(o)
        return J(s.v * o.v, [s.v * b + o.v * a for a, b in zip(s.d, o.d)])
    __rmul__ = __mul__

    def inverse(s):
        iv = inv(s.v)
        return J(iv, [-a * iv % P * iv for a in s.d])

    def __truediv__(s, o):
        return s * s._l(o).inverse()

    def __rtruediv__(s, o):
        return s._l(o) * s.inverse()

    def sqrt(s):
        r = sqrtmod(s.v)
        i2 = inv(2 * r)
        return J(r, [a * i2 for a in s.d])


# ---------------------------------------------------------------- power series in e
class PS:
    N = 12
    __slots__ = ("c",)

    def __init__(s, c):
        c = [x % P for x in c][:PS.N]
        s.c = c + [0] * (PS.N - len(c))

    def _l(s, o):
        return o if isinstance(o, PS) else PS([o])

    def __add__(s, o):
        o = s._l(o)
        return PS([a + b for a, b in zip(s.c, o.c)])
    __radd__ = __add__

    def __neg__(s):
        return PS([-a for a in s.c])

    def __sub__(s, o):
        return s + (-s._l(o))

    def __rsub__(s, o):
        return s._l(o) + (-s)

    def __mul__(s, o):
        o = s._l(o)
        n = PS.N
        r = [0] * n
        for i, a in enumerate(s.c):
            if a:
                for j in range(n - i):
                    r[i + j] += a * o.c[j]
        return PS(r)
    __rmul__ = __mul__

    def inverse(s):
        a0 = s.c[0]
        assert a0
        n = PS.N
        r = [0] * n
        r[0] = inv(a0)
        for k in range(1, n):
            acc = sum(s.c[j] * r[k - j] for j in range(1, k + 1)) % P
            r[k] = (-acc * r[0]) % P
        return PS(r)

    def __truediv__(s, o):
        return s * s._l(o).inverse()

    def __rtruediv__(s, o):
        return s._l(o) * s.inverse()

    def sqrt(s):
        n = PS.N
        r = [0] * n
        r[0] = sqrtmod(s.c[0])
        i2 = inv(2 * r[0])
        for k in range(1, n):
            acc = sum(r[i] * r[k - i] for i in range(1, k)) % P
            r[k] = (s.c[k] - acc) * i2 % P
        return PS(r)


def sqrt(x):
    return x.sqrt() if hasattr(x, "sqrt") else sqrtmod(x)


# ---------------------------------------------------------------- linear algebra mod P
def rank_mod(M):
    M = np.array(M, dtype=np.int64) % P
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        if r == rows:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        piv = r + nz[0]
        if piv != r:
            M[[r, piv]] = M[[piv, r]]
        M[r] = M[r] * inv(M[r, c]) % P
        below = M[r + 1:, c].copy()
        nzb = np.nonzero(below)[0]
        if len(nzb):
            idx = r + 1 + nzb
            M[idx] = (M[idx] - np.outer(below[nzb], M[r]) % P) % P
        r += 1
    return r


def nullspace_mod(A, n):
    """basis of {x : A x = 0} over F_P (python ints; A list of rows)"""
    A = [list(map(lambda x: x % P, row)) for row in A]
    piv = []
    r = 0
    for c in range(n):
        pr = next((i for i in range(r, len(A)) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = inv(A[r][c])
        A[r] = [x * iv % P for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % P for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == len(A):
            break
    free = [c for c in range(n) if c not in piv]
    out = []
    for fc in free:
        v = [0] * n
        v[fc] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-A[i][fc]) % P
        out.append(v)
    return out


# ---------------------------------------------------------------- point constructors
def div(a, b):
    if isinstance(a, (J, PS)) or isinstance(b, (J, PS)):
        return a / b
    return a % P * inv(b) % P


def circ(s):
    """unit circle via stereographic parameter s"""
    d = 1 + s * s
    return [div(1 - s * s, d), div(2 * s, d)]


def sph(us):
    """unit sphere S^{len(us)} via inverse stereographic projection"""
    n2 = 0
    for u in us:
        n2 = n2 + u * u
    d = 1 + n2
    return [div(2 * u, d) for u in us] + [div(n2 - 1, d)]


def const_point(coords):
    return lambda th: list(coords)


def rat_circ(a, b=1):
    s = R(a, b)
    d = (1 + s * s) % P
    return const_point([(1 - s * s) * inv(d) % P, 2 * s * inv(d) % P])


def rand_rat_sphere(dim, rng):
    us = [R(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(dim - 1)]
    pts = sph(us)
    return const_point([x % P for x in pts])


# ---------------------------------------------------------------- 2-jet test
def jet2(points, k, d, tau=None, rng=random):
    tau = tau or [rng.randrange(2, P - 2) for _ in range(k)]
    th = [J(tau[j], [1 if i == j else 0 for i in range(k)]) for j in range(k)]
    A_pts, Dp = [], []
    for f in points:
        a = [x if isinstance(x, J) else J(x, [0] * k) for x in f(th)]
        A_pts.append([1] + [x.v for x in a])
        Dp.append([[0] + [x.d[j] for x in a] for j in range(k)])
    D1 = d + 1
    nP = D1 * D1
    pairs = [(j, l) for j in range(k) for l in range(j, k)]
    sym = [(a, b) for a in range(D1) for b in range(a, D1)]
    nQ = len(sym)
    nun = k * nP + len(pairs) * nQ
    rows, rhs = [], []
    for i, p in enumerate(A_pts):
        pp = [p[a] * p[b] % P for a in range(D1) for b in range(D1)]
        for j in range(k):  # order 1
            row = [0] * nun
            row[j * nP:(j + 1) * nP] = pp
            rows.append(row)
            rhs.append(0)
        for q, (j, l) in enumerate(pairs):  # order 2
            row = [0] * nun
            dl, dj = Dp[i][l], Dp[i][j]
            for a in range(D1):
                for b in range(D1):
                    row[j * nP + a * D1 + b] = (row[j * nP + a * D1 + b] + p[a] * dl[b]) % P
                    row[l * nP + a * D1 + b] = (row[l * nP + a * D1 + b] + p[a] * dj[b]) % P
            base = k * nP + q * nQ
            for t, (a, b) in enumerate(sym):
                row[base + t] = p[a] * p[b] % P
            rows.append(row)
            rhs.append(sum(dj[b] * dl[b] for b in range(1, D1)) % P)  # <D_j a, D_l a>
    A = np.array(rows, dtype=np.int64)
    Ab = np.concatenate([A, np.array(rhs, dtype=np.int64)[:, None]], axis=1)
    return rank_mod(A) == rank_mod(Ab)


# ---------------------------------------------------------------- full-order curve probe
def curve_probe(points, k, d, N=12, rng=random):
    PS.N = N
    tau = [rng.randrange(2, P - 2) for _ in range(k)]
    w = [rng.randrange(1, P - 1) for _ in range(k)]
    thT = [PS([tau[j]]) for j in range(k)]
    thU = [PS([tau[j], w[j]]) for j in range(k)]
    D1 = d + 1
    nu = D1 * D1
    rowsPS = []
    for f in points:
        aT = [x if isinstance(x, PS) else PS([x]) for x in f(thT)]
        aU = [x if isinstance(x, PS) else PS([x]) for x in f(thU)]
        pT = [PS([1])] + aT
        pU = [PS([1])] + aU
        rowsPS.append([pT[a] * pU[b] for a in range(D1) for b in range(D1)])
    nvar = nu * N
    eqs = []
    for r in rowsPS:
        for n in range(N):
            eq = [0] * nvar
            for kk in range(n + 1):
                for j in range(nu):
                    eq[nu * kk + j] = (eq[nu * kk + j] + r[j].c[n - kk]) % P
            eqs.append(eq)
    ns = nullspace_mod(eqs, nvar)
    L = [v[:nu] for v in ns]
    spat = [(a, b) for a in range(1, D1) for b in range(1, D1)]
    S = [[v[a * D1 + b] for (a, b) in spat] for v in L]
    target = [1 if a == b else 0 for (a, b) in spat]
    if not S:
        return False
    return rank_mod(S) == rank_mod(S + [target])


def verdict(fn, points, k, d, trials=2, **kw):
    vs = {fn(points, k, d, **kw) for _ in range(trials)}
    return "PASS" if vs == {True} else ("FAIL" if vs == {False} else "MIXED")


def jet2_reduced(points, k, d, rng=random):
    """2-jet test when MANY algebraic points are also present (enough to force Q_jl ~ S and
    sym(P_j) ~ S): only antisymmetric A_j survive.  `points` = the transcendental points only."""
    tau = [rng.randrange(2, P - 2) for _ in range(k)]
    th = [J(tau[j], [1 if i == j else 0 for i in range(k)]) for j in range(k)]
    D1 = d + 1
    asym = [(a, b) for a in range(D1) for b in range(a + 1, D1)]
    nA = len(asym)
    rows, rhs = [], []
    for f in points:
        a = [x if isinstance(x, J) else J(x, [0] * k) for x in f(th)]
        p = [1] + [x.v for x in a]
        Dp = [[0] + [x.d[j] for x in a] for j in range(k)]
        for j in range(k):
            for l in range(j, k):
                row = [0] * (k * nA)
                for t, (al, be) in enumerate(asym):  # p^T A v = sum_{a<b} A_ab (p_a v_b - p_b v_a)
                    row[j * nA + t] = (row[j * nA + t] + p[al] * Dp[l][be] - p[be] * Dp[l][al]) % P
                    row[l * nA + t] = (row[l * nA + t] + p[al] * Dp[j][be] - p[be] * Dp[j][al]) % P
                rows.append(row)
                rhs.append(sum(Dp[j][b] * Dp[l][b] for b in range(1, D1)) % P)
    A = np.array(rows, dtype=np.int64)
    Ab = np.concatenate([A, np.array(rhs, dtype=np.int64)[:, None]], axis=1)
    return rank_mod(A) == rank_mod(Ab)
