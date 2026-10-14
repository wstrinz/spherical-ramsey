"""Exact dual certificates for the 2-jet FAIL of "3 rational + 4 independent" circle points.

applies_to: the 2-jet linear system of the note's second-order section (= probe2.jet2, c = 1) for a
  circle configuration whose points are rational or circ(T_m) with T_m independent
  indeterminates (field Q(T_1..T_k)); here m = 3 rational points (t = 0, 1/2, 1/3) and k = 4.
  The certificate machinery (exact field arithmetic, Fredholm alternative) applies to any
  linear system over a rational function field; Lemma A.1 checks apply to any finite planar set
  with a derivation given on its coordinate field.

Configuration (OAI coordinates, unit circle, p_i = (1, a_i)):
  a_i = circ(t_i), circ(t) = ((1-t^2)/(1+t^2), 2t/(1+t^2)),
  t = 0, 1/2, 1/3, T1, T2, T3, T4      (jet2 point order: rats[:3] + indep_circle(4)).

What is checked (all EXACT, in the field K = QQ(T1,T2,T3,T4), sympy FracField):
  [1] the configuration: |a_i|^2 = 1, distinct, 3 rational points non-collinear.
  [2] the 2-jet system A x = b is built exactly with probe2.jet2's row/column layout.
  [3] certificate CERT-M ("matrix weights", Lambda_i NOT of the form lambda_i*C):
        y^T A = 0 identically and y^T b = 1/((T1-T2)(T1-T3)(T1-T4)) != 0.
  [4] certificate CERT-S (Palvolgyi arXiv:2609.23327 Thm A.3, scalar weights, single
        derivation D = sum_m g(T_m) d/dT_m, g(t) = t(t-1/2)(t-1/3)):
        (a) Lemma A.1 hypotheses hold exactly, energy E = 4;
        (b) the same data, Lambda_i = lambda_i * c c^T, is also a 2-jet dual vector: y^T A = 0,
            y^T b = 4.
  [5] consistency with the 2-jet probe: probe2.jet2's own mod-p matrix (captured) equals
        A evaluated mod p at seeded random points, and both certificates annihilate it mod p.
  [6] control: 3 rational + 3 independent (a PASS cell): exact rank(A) = rank([A|b]) over
        QQ(T1,T2,T3), i.e. NO dual certificate exists (exact Gaussian elimination in the field).

Run (from any directory):  python3 -I dual_cert.py      (expected output: expected/dual_cert.log)
Imports probe2 and validate from the sibling directory ../probes (the [PROBE] harness); they are used
only in the mod-p consistency check [5], which assumes the default prime 2^31 - 1 (env PROBE_PRIME unset).
"""
import random
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "probes"))   # probe2.py, validate.py (sibling directory)
sys.path.insert(0, HERE)

from sympy import QQ, Rational
from sympy.polys.fields import field

import probe2
import validate


# ---------------------------------------------------------------- exact linear algebra over K
def rref_rank(rows, ncols, K):
    """Exact rank of a matrix (list of lists of K-elements) by Gaussian elimination."""
    M = [list(r) for r in rows]
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = 1 / M[r][c]
        M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def solve_unique(Arows, rhs, K):
    """Solve a square nonsingular system exactly (raises if singular)."""
    n = len(Arows)
    M = [list(Arows[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] != 0), None)
        if piv is None:
            raise ValueError("singular")
        M[c], M[piv] = M[piv], M[c]
        iv = 1 / M[c][c]
        M[c] = [x * iv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return [M[i][n] for i in range(n)]


def solve_any(Arows, rhs, ncols, K):
    """A particular solution of a consistent (possibly rank-deficient) system; free vars = 0."""
    M = [list(Arows[i]) + [rhs[i]] for i in range(len(Arows))]
    piv_cols, r = [], 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = 1 / M[r][c]
        M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv_cols.append(c)
        r += 1
    for i in range(r, len(M)):
        if M[i][ncols] != 0:
            raise ValueError("inconsistent")
    x = [K.zero] * ncols
    for i, c in enumerate(piv_cols):
        x[c] = M[i][ncols]
    return x


# ---------------------------------------------------------------- configuration
def circ(t):
    d = 1 + t * t
    return [(1 - t * t) / d, (2 * t) / d]


def dcirc(t):
    """d/dt of circ(t)"""
    d = 1 + t * t
    return [-4 * t / d ** 2, 2 * (1 - t * t) / d ** 2]


def build(K, Ts, rat_ts):
    """Points as (p, [D_j p for j<k]) with p = (1, a), exactly in K; jet2 order."""
    k = len(Ts)
    pts = []
    for t in rat_ts:
        tt = QQ.convert(t) if K is QQ else K(t)
        a = circ(tt)
        pts.append(([K.one] + a, [[K.zero] * 3 for _ in range(k)]))
    for m, T in enumerate(Ts):
        a = circ(T)
        da = dcirc(T)
        D = [[K.zero] * 3 for _ in range(k)]
        D[m] = [K.zero] + da
        pts.append(([K.one] + a, D))
    return pts


def jet2_system(pts, k, K, d=2):
    """Exact copy of probe2.jet2's layout. Returns rows (list of lists), rhs, labels."""
    D1 = d + 1
    nP = D1 * D1
    pairs = [(j, l) for j in range(k) for l in range(j, k)]
    sym = [(a, b) for a in range(D1) for b in range(a, D1)]
    nQ = len(sym)
    nun = k * nP + len(pairs) * nQ
    rows, rhs, labels = [], [], []
    for i, (p, Dp) in enumerate(pts):
        pp = [p[a] * p[b] for a in range(D1) for b in range(D1)]
        for j in range(k):
            row = [K.zero] * nun
            row[j * nP:(j + 1) * nP] = pp
            rows.append(row)
            rhs.append(K.zero)
            labels.append((i, "o1", j))
        for q, (j, l) in enumerate(pairs):
            row = [K.zero] * nun
            dl, dj = Dp[l], Dp[j]
            for a in range(D1):
                for b in range(D1):
                    row[j * nP + a * D1 + b] += p[a] * dl[b]
                    row[l * nP + a * D1 + b] += p[a] * dj[b]
            base = k * nP + q * nQ
            for t, (a, b) in enumerate(sym):
                row[base + t] = p[a] * p[b]
            rows.append(row)
            rhs.append(sum((dj[b] * dl[b] for b in range(1, D1)), K.zero))
            labels.append((i, "o2", (j, l)))
    return rows, rhs, labels, nun, pairs


def check_cert(y, rows, rhs, nun, K):
    yA = [sum((y[r] * rows[r][c] for r in range(len(rows)) if y[r] != 0 and rows[r][c] != 0),
              K.zero) for c in range(nun)]
    nz = [c for c in range(nun) if yA[c] != 0]
    yb = sum((y[r] * rhs[r] for r in range(len(rows))), K.zero)
    return nz, yb


def sym_outer(u, v):
    return [[u[a] * v[b] for b in range(3)] for a in range(3)]


def flat(M):
    return [M[a][b] for a in range(3) for b in range(3)]


def quad_relation(pts_p, idx, fixed, K):
    """Vector lam over idx with sum lam_i p_i p_i^T = 0, given fixed {i: value}; the free
    indices (idx minus fixed) must be exactly 5 so the solution is unique."""
    free = [i for i in idx if i not in fixed]
    assert len(free) == 5
    # equations: 6 sym entries (a<=b); rank 5 (all p p^T are S-traceless); use 5 of them
    sym = [(0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]  # (0,0) entry dependent: -00 + 11 + 22 = 0
    A = [[pts_p[i][a] * pts_p[i][b] for i in free] for (a, b) in sym]
    rhs = [-sum((v * pts_p[i][a] * pts_p[i][b] for i, v in fixed.items()), K.zero)
           for (a, b) in sym]
    sol = solve_unique(A, rhs, K)
    lam = dict(fixed)
    lam.update(dict(zip(free, sol)))
    # verify all 6 entries (incl. the dependent one)
    for a in range(3):
        for b in range(3):
            assert sum((v * pts_p[i][a] * pts_p[i][b] for i, v in lam.items()), K.zero) == 0
    return lam


def main():
    K, T1, T2, T3, T4 = field("T1,T2,T3,T4", QQ)
    Ts = [T1, T2, T3, T4]
    rat_ts = [Rational(0), Rational(1, 2), Rational(1, 3)]
    k = 4
    pts = build(K, Ts, rat_ts)
    P = [p for p, _ in pts]
    n = len(pts)

    # [1] configuration
    print("[1] configuration: t = 0, 1/2, 1/3, T1..T4 ; a_i = circ(t_i) on the unit circle")
    for p, _ in pts:
        assert p[1] ** 2 + p[2] ** 2 == 1
    print("    rational points:", [(str(p[1]), str(p[2])) for p in P[:3]])
    # non-collinear rational points: det of (1,x,y) rows != 0
    def det3(u, v, w):
        return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0])
                + u[2] * (v[0] * w[1] - v[1] * w[0]))
    print("    det(p_1,p_2,p_3) =", det3(P[0], P[1], P[2]), "(nonzero => affine span R^2)")
    print("    |a_i|^2 = 1 for all 7 points: OK (exact)")

    # [2] the system
    rows, rhs, labels, nun, pairs = jet2_system(pts, k, K)
    print(f"[2] 2-jet system: {len(rows)} rows x {nun} unknowns over QQ(T1..T4)")
    rowidx = {lab: r for r, lab in enumerate(labels)}

    # [3] CERT-M
    # tangent velocities v_m = D_m p at transcendental point 3+m
    tr = list(range(3, 7))
    V = {i: pts[i][1][i - 3] for i in tr}
    # omega: sum_m omega_m (p v^T - v p^T) = 0 ; closed form, then verified
    def prod_others(m):
        out = K.one
        for kk in range(4):
            if kk != m:
                out *= (Ts[m] - Ts[kk])
        return out
    omega = {3 + m: (1 + Ts[m] ** 2) ** 2 / (2 * prod_others(m)) for m in range(4)}
    for a in range(3):
        for b in range(3):
            s = sum((omega[i] * (P[i][a] * V[i][b] - V[i][a] * P[i][b]) for i in tr), K.zero)
            assert s == 0
    print("[3] CERT-M: omega_m = (1+T_m^2)^2 / (2 prod_{k!=m}(T_m-T_k)); "
          "sum omega_m (p v^T - v p^T) = 0 : OK")
    y = [K.zero] * len(rows)
    # P_0 coefficients: w_{0m} = omega_m
    y[rowidx[(3, "o2", (0, 0))]] = omega[3] / 2
    for m in (1, 2, 3):
        y[rowidx[(3 + m, "o2", (0, m))]] = omega[3 + m]
    # mu_{i,0}: sum_i mu_i p_i p_i^T = - sum_m omega_m p_m v_m^T  (9 equations, 7 unknowns)
    target = [[-sum((omega[i] * P[i][a] * V[i][b] for i in tr), K.zero) for b in range(3)]
              for a in range(3)]
    Amu = [[P[i][a] * P[i][b] for i in range(n)] for a in range(3) for b in range(3)]
    mu = solve_any(Amu, flat(target), n, K)
    for i in range(n):
        y[rowidx[(i, "o1", 0)]] = mu[i]
    # Q pair (0,0): relation over points except index 6, prescribed at point 3
    lam00 = quad_relation(P, [0, 1, 2, 3, 4, 5], {3: omega[3] / 2}, K)
    for i, v in lam00.items():
        if i != 3:
            y[rowidx[(i, "o2", (0, 0))]] = v
    # Q pairs (0,m): relation over points except index 3 (value 0 there), prescribed at 3+m
    lam0m = {}
    for m in (1, 2, 3):
        lam = quad_relation(P, [0, 1, 2, 4, 5, 6], {3 + m: omega[3 + m]}, K)
        lam0m[m] = lam
        for i, v in lam.items():
            if i != 3 + m:
                y[rowidx[(i, "o2", (0, m))]] = v
    nz, yb = check_cert(y, rows, rhs, nun, K)
    print(f"    y^T A: {nun - len(nz)}/{nun} entries are exactly 0 ; nonzero columns: {nz}")
    print("    y^T b =", yb)
    expect = 1 / prod_others(0)
    assert not nz and yb == expect and yb != 0
    print("    == 1/((T1-T2)(T1-T3)(T1-T4)) : OK.  CERT-M VERIFIED (exact).")
    # report Lambda_i as symmetric 4x4 (Lambda_{uv} with y_(u,v) = 2 Lambda_uv for u<v,
    # y_(u,u) = Lambda_uu, so that y^T b = sum_i tr(Lambda_i G_i))
    def Lam_of(y, i):
        L = [[K.zero] * k for _ in range(k)]
        for (u, v) in pairs:
            val = y[rowidx[(i, "o2", (u, v))]]
            if u == v:
                L[u][u] = val
            else:
                L[u][v] = L[v][u] = val / 2
        return L
    print("    nonzero Lambda_i entries (u,v) [0-based derivation index]:")
    for i in range(n):
        L = Lam_of(y, i)
        ents = [(u, v) for u in range(k) for v in range(u, k) if L[u][v] != 0]
        print(f"      point {i}: {ents}")
    # Lambda_i proportional to a common C?  Check rank of the stacked flattened Lambda_i.
    stack = [[Lam_of(y, i)[u][v] for u in range(k) for v in range(u, k)] for i in range(n)]
    rk = rref_rank(stack, len(stack[0]), K)
    print(f"    rank of span{{Lambda_i}} = {rk}  (1 would mean Lambda_i = lambda_i * C)")
    print("    mu_{i,0} =", [str(x) for x in mu])

    # [4] CERT-S (Palvolgyi Thm A.3)
    ts_all = [K(t) for t in rat_ts] + Ts
    def g(t):
        return t * (t - K(Rational(1, 2))) * (t - K(Rational(1, 3)))
    def Hp(i):
        out = K.one
        for kk in range(n):
            if kk != i:
                out *= (ts_all[i] - ts_all[kk])
        return out
    lam = [(1 + ts_all[i] ** 2) ** 2 / Hp(i) for i in range(n)]
    c = [g(T) for T in Ts]
    # derivation D = sum_m c_m d/dT_m : D a_i = g(t_i) dcirc(t_i) (=0 at rational points)
    Da = [[K.zero, K.zero] if i < 3 else [c[i - 3] * x for x in dcirc(Ts[i - 3])]
          for i in range(n)]
    a2 = [P[i][1:] for i in range(n)]
    ok = True
    ok &= sum(lam, K.zero) == 0
    ok &= all(sum((lam[i] * a2[i][u] for i in range(n)), K.zero) == 0 for u in range(2))
    ok &= all(sum((lam[i] * a2[i][u] * a2[i][v] for i in range(n)), K.zero) == 0
              for u in range(2) for v in range(2))
    ok &= all(sum((lam[i] * Da[i][u] for i in range(n)), K.zero) == 0 for u in range(2))
    M = [[sum((lam[i] * Da[i][u] * a2[i][v] for i in range(n)), K.zero) for v in range(2)]
         for u in range(2)]
    ok &= M[0][1] == M[1][0]
    E = sum((lam[i] * (Da[i][0] ** 2 + Da[i][1] ** 2) for i in range(n)), K.zero)
    print("[4] CERT-S (Palvolgyi Thm A.3): lambda_i = (1+t_i^2)^2/H'(t_i), D = sum g(T_m) d/dT_m")
    print("    Lemma A.1 hypotheses (sum l=0, sum l a=0, sum l a a^T=0, sum l Da=0, M sym):",
          "OK" if ok else "FAIL")
    print("    energy E = sum lambda_i |D a_i|^2 =", E)
    assert ok and E == 4
    # as a 2-jet dual vector: Lambda_i = lambda_i c c^T
    y2 = [K.zero] * len(rows)
    for i in range(n):
        for (u, v) in pairs:
            val = lam[i] * c[u] * c[v]
            y2[rowidx[(i, "o2", (u, v))]] = val if u == v else 2 * val
    # P_j equations: sum_i mu_ij p p^T + 2 c_j sum_i lam_i p_i (D p_i)^T = 0 ; mu_ij = c_j nu_i
    Dp = [[K.zero] + Da[i] for i in range(n)]
    tgt = [[-2 * sum((lam[i] * P[i][a] * Dp[i][b] for i in range(n)), K.zero) for b in range(3)]
           for a in range(3)]
    nu = solve_any(Amu, flat(tgt), n, K)
    for i in range(n):
        for j in range(k):
            y2[rowidx[(i, "o1", j)]] = c[j] * nu[i]
    nz2, yb2 = check_cert(y2, rows, rhs, nun, K)
    print(f"    as 2-jet dual (Lambda_i = lambda_i c c^T): y^T A nonzero columns: {nz2};"
          f" y^T b = {yb2}")
    assert not nz2 and yb2 == 4
    print("    CERT-S VERIFIED (exact), both as Lemma A.1 data and as a 2-jet dual vector.")

    # [5] cross-check against probe2.jet2's own matrix, mod p, seeded
    rng = random.Random(20261012)
    Pp = probe2.P
    def q_modp(q):
        q = QQ.convert(q)
        return int(q.numerator) % Pp * pow(int(q.denominator) % Pp, -1, Pp) % Pp

    def modp(x, tau):
        """exact evaluation of a K-element at integer tau, reduced mod p"""
        return q_modp(x.numer(*tau)) * pow(q_modp(x.denom(*tau)), -1, Pp) % Pp
    captured = []
    orig = probe2.rank_mod
    def cap(Mx):
        captured.append(Mx)
        return orig(Mx)
    pts_probe = validate.rats[:3] + validate.indep_circle(4)
    for trial in range(3):
        tau = [rng.randrange(2, Pp - 2) for _ in range(k)]
        captured.clear()
        probe2.rank_mod = cap
        try:
            verdict = probe2.jet2(pts_probe, k, 2, tau=tau)
        finally:
            probe2.rank_mod = orig
        Ab = captured[1]
        same = all(int(Ab[r][cc]) % Pp == modp(rows[r][cc], tau)
                   for r in range(len(rows)) for cc in range(nun)) and \
            all(int(Ab[r][nun]) % Pp == modp(rhs[r], tau) for r in range(len(rows)))
        res = []
        for yy in (y, y2):
            yv = [modp(x, tau) for x in yy]
            yA = [sum(yv[r] * int(Ab[r][cc]) for r in range(len(rows))) % Pp for cc in range(nun)]
            ybv = sum(yv[r] * int(Ab[r][nun]) for r in range(len(rows))) % Pp
            res.append((all(v == 0 for v in yA), ybv != 0))
        print(f"[5] tau seed-trial {trial}: jet2 -> {'PASS' if verdict else 'FAIL'}; "
              f"exact A,b == jet2 matrix mod p: {same}; CERT-M (yA=0, yb!=0): {res[0]}; "
              f"CERT-S: {res[1]}")
        assert same and not verdict and res[0] == (True, True) and res[1] == (True, True)

    # [6] control: 3 rational + 3 independent
    K3, S1, S2, S3 = field("S1,S2,S3", QQ)
    pts3 = build(K3, [S1, S2, S3], rat_ts)
    rows3, rhs3, _, nun3, _ = jet2_system(pts3, 3, K3)
    rA = rref_rank(rows3, nun3, K3)
    rAb = rref_rank([r + [b] for r, b in zip(rows3, rhs3)], nun3 + 1, K3)
    print(f"[6] control 3 rat + 3 indep: {len(rows3)} x {nun3}; exact rank A = {rA}, "
          f"rank [A|b] = {rAb} -> {'consistent: NO dual certificate exists' if rA == rAb else 'INCONSISTENT'}")
    assert rA == rAb
    # and the exact 7-point FAIL system: rank A < rank [A|b]
    rA7 = rref_rank(rows, nun, K)
    rAb7 = rref_rank([r + [b] for r, b in zip(rows, rhs)], nun + 1, K)
    print(f"    for comparison, 3 rat + 4 indep: exact rank A = {rA7}, rank [A|b] = {rAb7}")
    assert rAb7 == rA7 + 1

    # [7] CERT-S for an ARBITRARY rational (indeed any) triple: Lemma A.1 data over
    #     QQ(R1,R2,R3,T1..T4), R_i treated as constants (D R_i = 0).
    K7, R1, R2, R3, U1, U2, U3, U4 = field("R1,R2,R3,U1,U2,U3,U4", QQ)
    tv = [R1, R2, R3, U1, U2, U3, U4]
    def Hp7(i):
        out = K7.one
        for kk in range(7):
            if kk != i:
                out *= (tv[i] - tv[kk])
        return out
    lam7 = [(1 + tv[i] ** 2) ** 2 / Hp7(i) for i in range(7)]
    g7 = lambda t: (t - R1) * (t - R2) * (t - R3)
    a7 = [circ(t) for t in tv]
    Da7 = [[K7.zero, K7.zero] if i < 3 else [g7(tv[i]) * x for x in dcirc(tv[i])]
           for i in range(7)]
    ok7 = sum(lam7, K7.zero) == 0
    ok7 &= all(sum((lam7[i] * a7[i][u] for i in range(7)), K7.zero) == 0 for u in range(2))
    ok7 &= all(sum((lam7[i] * a7[i][u] * a7[i][v] for i in range(7)), K7.zero) == 0
               for u in range(2) for v in range(2))
    ok7 &= all(sum((lam7[i] * Da7[i][u] for i in range(7)), K7.zero) == 0 for u in range(2))
    M7 = [[sum((lam7[i] * Da7[i][u] * a7[i][v] for i in range(7)), K7.zero) for v in range(2)]
          for u in range(2)]
    ok7 &= M7[0][1] == M7[1][0]
    E7 = sum((lam7[i] * (Da7[i][0] ** 2 + Da7[i][1] ** 2) for i in range(7)), K7.zero)
    print(f"[7] CERT-S with symbolic triple R1,R2,R3: Lemma A.1 hypotheses {'OK' if ok7 else 'FAIL'};"
          f" E = {E7}  (denominators: prod (t_i - t_j) only)")
    assert ok7 and E7 == 4

    # [8] reviewer's rank route, reproduced: 14 explicit kernel vectors of A (exact, generic),
    #     then exact ranks at rational specializations (a ring map: the only denominators of
    #     A, b are powers of 1 + T_m^2, nonzero at rational T_m).
    D1 = 3
    sym = [(a, b) for a in range(D1) for b in range(a, D1)]
    Ssym = [(-1 if a == 0 else 1) if a == b else 0 for (a, b) in sym]
    Sfull = [(-1 if a == 0 else 1) if a == b else 0 for a in range(3) for b in range(3)]
    kern = []
    for j in range(k):
        x = [K.zero] * nun
        x[j * 9:(j + 1) * 9] = [K(v) for v in Sfull]
        kern.append(x)
    for q in range(len(pairs)):
        x = [K.zero] * nun
        x[k * 9 + q * 6: k * 9 + (q + 1) * 6] = [K(v) for v in Ssym]
        kern.append(x)
    okk = all(sum((rows[r][cc] * x[cc] for cc in range(nun) if x[cc] != 0), K.zero) == 0
              for x in kern for r in range(len(rows)))
    print(f"[8] {len(kern)} kernel vectors (P_j = S, j<4; Q_jl = S, 10 pairs), disjoint supports, "
          f"A x = 0 exactly: {okk}  => generic rank A <= {nun - len(kern)}")
    assert okk
    rng8 = random.Random(172)
    for trial in range(3):
        while True:
            tri = sorted({Rational(rng8.randint(-9, 9), rng8.randint(1, 9)) for _ in range(3)})
            th = [Rational(rng8.randint(-30, 30), rng8.randint(1, 30)) for _ in range(4)]
            allt = tri + th
            if len(tri) == 3 and len(set(allt)) == 7:
                break
        ptsq = build(QQ, [QQ.convert(t) for t in th], tri)
        rq, bq, _, nq, _ = jet2_system(ptsq, 4, QQ)
        ra = rref_rank(rq, nq, QQ)
        rab = rref_rank([r + [b] for r, b in zip(rq, bq)], nq + 1, QQ)
        print(f"    triple {[str(t) for t in tri]}, theta -> {[str(t) for t in th]}: "
              f"rank A = {ra}, rank [A|b] = {rab}")
        assert rab == 83
        # CERT-S for this triple specializes: Lemma A.1 data at R = triple stays valid
        # for T generic (denominators prod(t_i - t_j) nonzero since triple distinct).
    print("    => generic rank [A|b] >= 83 > 82 >= generic rank A: 2-jet system inconsistent")
    print("       over QQ(T1..T4) for each listed triple (independent of the dual certificates).")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
