"""Exact checks for ledger entries SR-C29, SR-C30, SR-C31, SR-C32 (C-29 ... C-32 below; each entry was
filed before this script ran).

applies_to: finite subsets of the unit sphere S^{d-1} given by rational stereographic coordinates
  (projection from (0,...,0,1)), with first-order derivation data D_l a_i given as rational tangent
  vectors (a rational-affine parametrization u_i(theta) = alpha_i + B_i theta specialized at a rational
  point). Everything is exact over Q (python-flint fmpq_mat, sympy for Groebner bases).

Exactness / specialization logic (see the records):
  * quadric rank at a rational point <= generic rank, so rank N at tau certifies kappa = 0 generically;
  * 2-jet dual space Delta = {(C^rho) symmetric : sum_rho Pi_rho C^rho = 0}: dim at tau >= generic dim, so
    dim 0 at tau => generic 2-jet PASS; if dim at tau equals the universal lower bound
    kappa*k(k+1)/2 - k*G, kernels specialize and a nonzero trace pairing at tau => generic FAIL;
  * scalar locus {lambda : rank Pi_lambda < k}: empty at tau => empty generically (closed condition).

Requirements: Python >= 3.10, sympy (1.14.0 used for expected/) and python-flint (0.9.0 used).
Usage:  python -I certificates/corank_exact.py [c29|c30|c31|c32|all]     (seeded; deterministic)

C-31 verdicts marked "?" are undecided at this specialization (coincident points there, dual
dimension above the generic bound, or pairing zero); they are neither agreements nor mismatches.
c31_respecialize.py decides the three such families at other rational points. Every family is checked
to be injective (its generic member has pairwise distinct points), and every fixed rational
configuration (c29, c30) to have pairwise distinct points.
"""
import sys, random, itertools
from fractions import Fraction as Fr
import flint
import sympy as sp


# ------------------------------------------------------------------ geometry
def sph(u):
    s = sum(x * x for x in u)
    return [2 * x / (1 + s) for x in u] + [(s - 1) / (1 + s)]


def jac(u):
    """d x (d-1) Jacobian of sph at u (columns = d a / d u_k)."""
    s = sum(x * x for x in u)
    n = len(u)
    cols = []
    for k in range(n):
        col = [(2 * (1 if i == k else 0)) / (1 + s) - 4 * u[i] * u[k] / (1 + s) ** 2 for i in range(n)]
        col.append(4 * u[k] / (1 + s) ** 2)
        cols.append(col)
    return cols  # list of tangent vectors


def coincident(pts):
    keys = [tuple(p) for p in pts]
    return len(set(keys)) < len(keys)


def assert_family_injective(alpha, B):
    """The generic member of the family u_i(theta) = alpha_i + B_i theta is injective iff the pairs
    (alpha_i, B_i) are pairwise distinct (stereographic projection is injective)."""
    keys = [tuple(a) + tuple(tuple(r) for r in b) for a, b in zip(alpha, B)]
    assert len(set(keys)) == len(keys), "family is not injective"


def assert_distinct(pts):
    """Injectivity: the configurations must consist of pairwise distinct points (OpenAI's criterion
    is for injective families). A collision would be a sampler bug, not a verdict."""
    keys = [tuple(p) for p in pts]
    assert len(set(keys)) == len(keys), "sampled configuration has coincident points"


def quad_row(a):
    p = [Fr(1)] + list(a)
    return [p[i] * p[j] for i in range(len(p)) for j in range(i, len(p))]


def mat(rows):
    return flint.fmpq_mat([[flint.fmpq(x.numerator, x.denominator) if isinstance(x, Fr) else flint.fmpq(x) for x in r] for r in rows])


def rank(rows):
    if not rows:
        return 0
    return mat(rows).rank()


def nullspace_left(rows):
    """basis of {lam : sum_i lam_i rows[i] = 0} (exact)."""
    M = sp.Matrix(rows).T
    return [list(v) for v in M.nullspace()]


def nullspace(rows, ncols):
    M = sp.Matrix(rows) if rows else sp.zeros(0, ncols)
    return [list(v) for v in M.nullspace()]


def rand_q(rng, lo=-9, hi=9):
    return Fr(rng.randint(lo, hi), rng.randint(1, 9))


def rand_u(rng, n):
    return [rand_q(rng) for _ in range(n)]


def antisym_vec(lam_i, p, w):
    """upper entries (a<b) of lam*(p w^T - w p^T)"""
    n = len(p)
    return [lam_i * (p[a] * w[b] - p[b] * w[a]) for a in range(n) for b in range(a + 1, n)]


def Pi_matrix(lam, pts, vel):
    """G x k matrix: column l = antisym part of sum_i lam_i p_i (0, D_l a_i)^T.
    vel[i][l] = tangent vector D_l a_i (list length d) or None for zero."""
    k = len(vel[0])
    d = len(pts[0])
    G = d * (d + 1) // 2
    cols = []
    for l in range(k):
        col = [Fr(0)] * G
        for i, a in enumerate(pts):
            v = vel[i][l]
            if v is None or lam[i] == 0:
                continue
            p = [Fr(1)] + list(a)
            w = [Fr(0)] + list(v)
            col = [x + y for x, y in zip(col, antisym_vec(Fr(lam[i]), p, w))]
        cols.append(col)
    return [[cols[l][g] for l in range(k)] for g in range(G)]


def to_fr(x):
    x = sp.Rational(x)
    return Fr(int(x.p), int(x.q))


# ------------------------------------------------------------------ C-29
def c29():
    print("== C-29: quadric rank of D_d seeded rational points on S^{d-1} (expect D_d), d = 3..8")
    ok = True
    for d in range(3, 9):
        D = (d + 1) * (d + 2) // 2 - 1
        rng = random.Random(2900 + d)
        pts = [sph(rand_u(rng, d - 1)) for _ in range(D)]
        assert_distinct(pts)
        r = rank([quad_row(a) for a in pts])
        print(f"  d={d}: N={D} rank={r} {'OK' if r == D else 'DEFICIT'}")
        ok &= (r == D)
    rng = random.Random(2916)
    pts = [sph(rand_u(rng, 2)) for _ in range(7)]
    assert_distinct(pts)
    r = rank([quad_row(a) for a in pts])
    print(f"  C-16 instance, 7 seeded rational points on S^2: rank={r} (expect 7)")
    ok &= (r == 7)
    R2 = [(Fr(5, 9), Fr(5, 8)), (Fr(7, 4), Fr(-4, 9)), (Fr(2), Fr(-3, 4)), (Fr(0), Fr(-7, 9)), (Fr(-8, 7), Fr(5, 3)), (Fr(-1), Fr(-7))]
    pts = [sph(list(u)) for u in R2] + [sph(rand_u(rng, 2)) for _ in range(3)]
    assert_distinct(pts)
    r = rank([quad_row(a) for a in pts])
    print(f"  NR-S23 R_2 + 3 seeded rational points (cell (6,3)/(9,0) shape): rank={r} (expect 9)")
    ok &= (r == 9)
    print("  C-29 check:", "PASS" if ok else "FAIL")
    return ok


# ------------------------------------------------------------------ C-30
R2 = [(Fr(5, 9), Fr(5, 8)), (Fr(7, 4), Fr(-4, 9)), (Fr(2), Fr(-3, 4)), (Fr(0), Fr(-7, 9)), (Fr(-8, 7), Fr(5, 3)), (Fr(-1), Fr(-7))]


def scalar_cert_data(rat_u, free_u, d):
    """returns (quad rank, kappa, lam, rank Pi, kernel dim, E Gram on kernel) for rational points rat_u
    plus free points free_u (each carrying d-1 derivations along its chart coordinates)."""
    n = d - 1
    pts = [sph(u) for u in rat_u] + [sph(u) for u in free_u]
    assert_distinct(pts)
    Q = [quad_row(a) for a in pts]
    r = rank(Q)
    rel = nullspace_left(Q)
    out = {"N": len(pts), "rank": r, "kappa": len(rel)}
    if len(rel) != 1:
        return out
    lam = [to_fr(x) for x in rel[0]]
    nr = len(rat_u)
    out["lam_free_nonzero"] = all(lam[nr + i] != 0 for i in range(len(free_u)))
    # velocities: one derivation per (free point, chart coordinate)
    k = len(free_u) * n
    vel = []
    for i in range(len(pts)):
        row = [None] * k
        if i >= nr:
            fi = i - nr
            J = jac(free_u[fi])
            for c in range(n):
                row[fi * n + c] = J[c]
        vel.append(row)
    Pi = Pi_matrix(lam, pts, vel)
    rP = rank(Pi)
    ker = nullspace(Pi, k)
    out["rankPi"] = rP
    out["kerdim"] = len(ker)

    def Ev(c1, c2):
        tot = Fr(0)
        for i in range(len(pts)):
            v1 = [Fr(0)] * d
            v2 = [Fr(0)] * d
            for l in range(k):
                if vel[i][l] is not None:
                    v1 = [x + to_fr(c1[l]) * y for x, y in zip(v1, vel[i][l])]
                    v2 = [x + to_fr(c2[l]) * y for x, y in zip(v2, vel[i][l])]
            tot += lam[i] * sum(x * y for x, y in zip(v1, v2))
        return tot
    out["Egram"] = [[Ev(a, b) for b in ker] for a in ker]
    out["E_nonzero"] = any(x != 0 for row in out["Egram"] for x in row)
    return out


def c30():
    print("== C-30: PD_d minimal cell (N(d)-4, 4): special (embedded S^2 cell) and general position")
    ok = True
    for d in range(3, 8):
        N = (d + 1) * (d + 2) // 2
        n = d - 1
        rng = random.Random(3000 + d)
        emb = lambda u2: [u2[0], u2[1]] + [Fr(0)] * (n - 2)
        if d >= 4:
            rat = [emb(u) for u in R2] + [rand_u(rng, n) for _ in range(N - 10)]
            free = [emb(rand_u(rng, 2)) for _ in range(4)]
            o = scalar_cert_data(rat, free, d)
            exp = 4 * d - 6
            good = o.get("kappa") == 1 and o.get("lam_free_nonzero") and o.get("rankPi") == exp and o.get("E_nonzero")
            print(f"  d={d} special : N={o['N']} quadrank={o['rank']} kappa={o['kappa']} lam_free!=0={o.get('lam_free_nonzero')} rankPi={o.get('rankPi')} (expect {exp}) kerdim={o.get('kerdim')} E!=0={o.get('E_nonzero')} -> {'OK' if good else 'BAD'}")
            ok &= bool(good)
        for trial in range(2):
            rat = [rand_u(rng, n) for _ in range(N - 4)]
            free = [rand_u(rng, n) for _ in range(4)]
            o = scalar_cert_data(rat, free, d)
            exp = 4 * d - 6 if d >= 3 else None
            good = o.get("kappa") == 1 and o.get("lam_free_nonzero") and o.get("rankPi") == exp and o.get("E_nonzero")
            print(f"  d={d} general#{trial}: N={o['N']} quadrank={o['rank']} kappa={o['kappa']} lam_free!=0={o.get('lam_free_nonzero')} rankPi={o.get('rankPi')} (expect {exp}) kerdim={o.get('kerdim')} E!=0={o.get('E_nonzero')} -> {'OK' if good else 'BAD'}")
            ok &= bool(good)
    # control: three free points must give no certificate (rank Pi = 3(d-1), kernel 0) -- C-2 says Ramsey
    for d in (4, 5):
        N = (d + 1) * (d + 2) // 2
        n = d - 1
        rng = random.Random(3100 + d)
        o = scalar_cert_data([rand_u(rng, n) for _ in range(N - 3)], [rand_u(rng, n) for _ in range(3)], d)
        good = o.get("kerdim") == 0
        print(f"  control d={d} (N(d)-3, 3): kappa={o['kappa']} rankPi={o.get('rankPi')} kerdim={o.get('kerdim')} (expect 0) -> {'OK' if good else 'BAD'}")
        ok &= bool(good)
    print("  C-30 check:", "PASS" if ok else "FAIL")
    return ok


# ------------------------------------------------------------------ C-31 / C-32 (generic-structure families)
def family(rng, d, N, k):
    """N points on S^{d-1}, u_i(theta) = alpha_i + B_i theta; returns (alpha list, B list) with rational entries."""
    n = d - 1
    alpha = [rand_u(rng, n) for _ in range(N)]
    B = [[[Fr(rng.randint(-5, 5)) for _ in range(k)] for _ in range(n)] for _ in range(N)]
    return alpha, B


def family_data(alpha, B, d, k):
    assert_family_injective(alpha, B)
    pts = [sph(u) for u in alpha]
    vel = []
    for i, u in enumerate(alpha):
        J = jac(u)
        row = []
        for l in range(k):
            v = [Fr(0)] * d
            for c in range(d - 1):
                v = [x + B[i][c][l] * y for x, y in zip(v, J[c])]
            row.append(v)
        vel.append(row)
    return pts, vel


def jet_dual(pts, vel, d, k):
    """exact 2-jet dual at the specialization: returns (kappa, dim Delta, lower bound, pairing nonzero?)."""
    Q = [quad_row(a) for a in pts]
    rel = [[to_fr(x) for x in v] for v in nullspace_left(Q)]
    kap = len(rel)
    G = d * (d + 1) // 2
    if kap == 0:
        return kap, 0, 0, False
    Pis = [Pi_matrix(lam, pts, vel) for lam in rel]
    sym = [(j, l) for j in range(k) for l in range(j, k)]
    # unknown x[rho, (j,l)] = C^rho_{jl}; equation for (g, j): sum_rho sum_l Pi_rho[g][l] C^rho[l][j] = 0
    ncol = kap * len(sym)
    idx = {(r, s): r * len(sym) + t for r in range(kap) for t, s in enumerate(sym)}
    rows = []
    for g in range(G):
        for j in range(k):
            row = [Fr(0)] * ncol
            for r in range(kap):
                for l in range(k):
                    key = (min(l, j), max(l, j))
                    row[idx[(r, key)]] += Pis[r][g][l]
            rows.append(row)
    ker = nullspace(rows, ncol)
    lower = kap * k * (k + 1) // 2 - k * G
    # trace pairing: sum_rho tr(C^rho M_rho), M_rho = sum_i lam^rho_i Gram_i
    Ms = []
    for lam in rel:
        M = [[sum(lam[i] * sum(x * y for x, y in zip(vel[i][j], vel[i][l])) for i in range(len(pts))) for l in range(k)] for j in range(k)]
        Ms.append(M)
    nz = False
    for v in ker:
        tot = Fr(0)
        for r in range(kap):
            for (j, l) in sym:
                c = to_fr(v[idx[(r, (j, l))]])
                tot += c * Ms[r][j][l] * (1 if j == l else 2)
        if tot != 0:
            nz = True
            break
    return kap, len(ker), lower, nz


def jet_verdict(kap, dim, lower, nz, k, G):
    """dim at tau >= generic dim >= universal lower bound; equality => kernels specialize."""
    if kap == 1:
        w = max(k - G, 0)          # kappa = 1: Delta = Sym^2(ker Pi), ker Pi has dim >= k - G everywhere
        lower = w * (w + 1) // 2
    lower = max(lower, 0)
    if dim == 0:
        return "PASS(exact)"
    if not nz:
        return "PASS?(pairing 0 on dual at tau)" if dim > lower else "PASS(exact: pairing 0 on specialized dual)"
    if dim == lower:
        return "FAIL(exact)"
    return "FAIL?(dual dim above lower bound at tau)"


def predict(kap, k, G):
    if kap == 0:
        return "PASS"
    if kap == 1:
        return "FAIL" if k > G else "PASS"
    return "FAIL" if kap * (k + 1) > 2 * G else "PASS"


def c31():
    print("== C-31: corank law, exact 2-jet dual at one seeded rational specialization")
    cases = [(3, 9, 10), (3, 10, 5), (3, 10, 6), (3, 10, 7), (3, 10, 8), (3, 11, 5), (3, 11, 6), (3, 11, 7),
             (3, 12, 3), (3, 12, 4), (3, 12, 5), (3, 13, 2), (3, 13, 3), (2, 7, 2), (2, 7, 3), (2, 8, 1), (2, 8, 2),
             (4, 15, 10), (4, 15, 11)]
    mism = 0
    und = 0
    for (d, N, k) in cases:
        G = d * (d + 1) // 2
        for seed in (0, 1):
            rng = random.Random(31000 + 100 * d + 10 * N + k + 1000 * seed)
            alpha, B = family(rng, d, N, k)
            pts, vel = family_data(alpha, B, d, k)
            kap, dim, lower, nz = jet_dual(pts, vel, d, k)
            v = jet_verdict(kap, dim, lower, nz, k, G)
            if coincident(pts):
                v = "?(coincident points at tau)"
            pr = predict(kap, k, G)
            undecided = "?" in v
            agree = (not undecided) and v.startswith(pr)
            mism += (not undecided) and (not agree)
            und += undecided
            tag = "undecided here (re-specialize)" if undecided else ("ok" if agree else "MISMATCH")
            print(f"  d={d} N={N} k={k} seed={seed}: kappa={kap} dimDelta={dim} lower={lower} pairing!=0={nz} -> {v:28s} predicted {pr} {tag}")
            sys.stdout.flush()
    print(f"  C-31 check: {mism} mismatches, {und} undecided at this specialization (see c31_respecialize.py)")
    return mism == 0


def scalar_locus_empty(pts, vel, d, k):
    Q = [quad_row(a) for a in pts]
    rel = [[to_fr(x) for x in v] for v in nullspace_left(Q)]
    kap = len(rel)
    ys = sp.symbols(f"y0:{kap}")
    Pis = [Pi_matrix(lam, pts, vel) for lam in rel]
    G = len(Pis[0])
    Py = sp.Matrix(G, k, lambda g, l: sum(ys[r] * sp.Rational(Pis[r][g][l].numerator, Pis[r][g][l].denominator) for r in range(kap)))
    minors = []
    for rows in itertools.combinations(range(G), k):
        m = sp.expand(Py.extract(list(rows), list(range(k))).det(method="berkowitz"))
        if m != 0:
            minors.append(m)
    GB = sp.groebner(minors, *ys, order="grevlex", domain=sp.QQ)
    return kap, GB.is_zero_dimensional, len(minors)


def c32():
    print("== C-32: S^2, (kappa,k) = (3,4) and (4,3): exact 2-jet dual and scalar (Lemma A.1) locus")
    ok = True
    for (N, k) in ((12, 4), (13, 3)):
        for seed in (0, 1):
            d = 3
            G = 6
            rng = random.Random(32000 + 10 * N + k + 1000 * seed)
            alpha, B = family(rng, d, N, k)
            pts, vel = family_data(alpha, B, d, k)
            kap, dim, lower, nz = jet_dual(pts, vel, d, k)
            fail_exact = nz and dim == lower
            kap2, zd, nm = scalar_locus_empty(pts, vel, d, k)
            print(f"  N={N} k={k} seed={seed}: kappa={kap} dimDelta={dim} lower={lower} pairing!=0={nz} -> 2-jet {'FAIL(exact)' if fail_exact else 'not certified'};"
                  f" scalar locus: {nm} minors, homogeneous ideal zero-dimensional (only y=0) = {zd}")
            sys.stdout.flush()
            ok &= bool(fail_exact and zd)
    print("  C-32 check:", "PASS (prediction holds at every seed)" if ok else "not confirmed at every seed")
    return ok


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, fn in (("c29", c29), ("c30", c30), ("c31", c31), ("c32", c32)):
        if which in (name, "all"):
            fn()
