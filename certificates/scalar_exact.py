"""Exact scalar (Palvolgyi-type, single-derivation) 2-jet certificates for rational + generic sphere points.

applies_to: m rational points plus j generic points on the unit sphere S^{d-1} in R^d, the generic
  points with pairwise disjoint, algebraically independent stereographic parameters
  (field F = Q(u_{i,1..d-1} : i < j), type GENERIC / TRANSCENDENTAL_PARAM).  Here: the minimal FAIL
  cells of e1_s2.py on S^2 (rational points of Random(11)) and e1_s3.py on S^3 (Random(13)), with
  m + j = n_min (dim L = 1); also e1_s4.py's S^4 threshold (Random(17), 17 rational + 4 free) and
  e3_sphere.py's 10 generic points on S^2.  The cofactor/Laplace argument applies to any polynomial matrices.

Certificate shape: the corrected dual form of the 2-jet system (the note's second-order section).
Homogeneous lifts p~_i = h_i p_i = (1+|u|^2, 2u, |u|^2-1) (polynomial; p~^T S p~ = 0, S = diag(-1, I)).
With lambda~_i = lambda_i / h_i^2 and w_i = lambda~_i D p~_i the scalar certificate conditions are
    (Q) sum lambda~_i p~_i p~_i^T = 0
    (P) sum_i p~_i w_i^T + sum_i mu_i p~_i p~_i^T = 0              (full d+1 square matrices)
    (E) E = sum_{i generic} w_i^T S w_i / lambda~_i != 0
and D = sum_i sum_r (alpha_ir / lambda~_i) d/du_ir, where w_i = sum_r alpha_ir d p~_i/du_ir.
(The h-rescaling only adds multiples of p~_i p~_i^T to (P), using p~^T S p~ = 0 = p~^T S D p~.)
Generic construction, no symbolic algebra needed:
  * (Q): drop the (0,0) row (it equals rows (1,1)+...+(d,d) identically, since p~^T S p~ = 0); the
    remaining N-1 rows x n matrix M_L(u) is polynomial; lambda~(u) := its cofactor vector satisfies
    M_L lambda~ = 0 IDENTICALLY (Laplace).  n = N = d(d+3)/2 + 1 here, so M_L is (n-1) x n.
  * (P): drop the (0,0) row (S-trace of (P) vanishes identically); fix a set Z of unknowns to 0 so the
    remaining matrix M_W(u) is (R) x (R+1); z(u) := its cofactor vector solves (P) IDENTICALLY.
  * At one rational point u = tau (a ring map Q[u] -> Q): if rank M_L(tau) and rank M_W(tau) are full
    then the cofactor vectors at tau are nonzero and span the (1-dim) exact kernels.  The code does not
    form the cofactor vectors: it computes an RREF kernel vector at tau, which equals the cofactor
    vector at tau up to a factor kappa in Q^x (kappa' for M_W).  So lambda~(tau) scales by kappa, w(tau)
    by kappa' and E(tau) by kappa'^2 / kappa, and the nonvanishing of each lambda~_i(tau) and of E(tau)
    is the same for the RREF vectors as for the cofactor vectors.
  * E over F is sum over the generic i with w_i not identically 0 of w_i^T S w_i / lambda~_i.  So the
    code requires lambda~_i(tau) != 0 for EVERY generic i (the rational points carry no w_i), not only
    for the i with w_i(tau) != 0; then specialization at tau is defined on E, and E(tau) != 0 shows
    E != 0 in F.
  So an exact scalar certificate exists over F, hence (Fredholm, trivial direction) the 2-jet system
  is inconsistent over F, and by J2 (the note's Proposition J2: Ramsey => 2-jet solvable) the set is
  non-Ramsey.  Equivalently, and without J2: Palvolgyi's Lemma A.1 hypotheses (arXiv:2609.23327,
  Lemma A.1) hold with energy E != 0, and with EGMRSS I, Lemma 15, the set is non-Ramsey.
Consistency checks at tau (not needed for the argument, run anyway): Palvolgyi's three conditions
  sum lambda_i p_i p_i^T = 0, sum lambda_i D a_i = 0, sum lambda_i D(a_i) a_i^T symmetric, in the
  inhomogeneous coordinates, and E recomputed as sum lambda_i |D a_i|^2.
usage (from any directory): python3 -I scalar_exact.py
The S^4 threshold cell is expected to report 'no exact certificate of this shape' (a second, identically
vanishing row relation of (P) needs one more dropped row; not implemented here), so the last line reads
'all certified: False' with exactly that entry False.
"""
import random
from fractions import Fraction as Fr


def rat_sphere_exact(dim, rng):
    """Exact replay of probe2.rand_rat_sphere (same rng consumption): stereographic u, rational."""
    return [Fr(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(dim - 1)]


def lift(us):
    n2 = sum(u * u for u in us)
    return [1 + n2] + [2 * u for u in us] + [n2 - 1]


def dlift(us, r):
    """d p~ / d u_r"""
    return [2 * us[r]] + [2 if s == r else 0 for s in range(len(us))] + [2 * us[r]]


def rref(M, ncols):
    M = [list(r) for r in M]
    piv, r = [], 0
    for c in range(ncols):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        iv = 1 / M[r][c]
        M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    return M[:r], piv


def kernel(M, ncols):
    R, piv = rref(M, ncols)
    free = [c for c in range(ncols) if c not in piv]
    out = []
    for fc in free:
        v = [Fr(0)] * ncols; v[fc] = Fr(1)
        for i, pc in enumerate(piv): v[pc] = -R[i][fc]
        out.append(v)
    return out, len(piv)


def jet2_dual_check(p, Dp, lam, c, nu, k, d):
    """Build probe2.jet2's system exactly (same layout) from p_i, D_v p_i and form the dual vector
    y[(i,o1,j)] = -2 c_j nu_i, y[(i,o2,(j,l))] = lam_i c_j c_l * (1 if j == l else 2).
    Returns (y^T A == 0, y^T b)."""
    D1 = d + 1; nP = D1 * D1
    pairs = [(a, b) for a in range(k) for b in range(a, k)]
    sym = [(a, b) for a in range(D1) for b in range(a, D1)]
    nQ = len(sym); nun = k * nP + len(pairs) * nQ
    yA = [Fr(0)] * nun; yb = Fr(0)
    for i in range(len(p)):
        pi = p[i]
        for jj in range(k):                                   # order-1 rows
            y = -2 * c[jj] * nu[i]
            if y:
                for a in range(D1):
                    for b in range(D1):
                        yA[jj * nP + a * D1 + b] += y * pi[a] * pi[b]
        for q, (jj, ll) in enumerate(pairs):                  # order-2 rows
            y = lam[i] * c[jj] * c[ll] * (1 if jj == ll else 2)
            if not y: continue
            dl, dj = Dp[i][ll], Dp[i][jj]
            for a in range(D1):
                for b in range(D1):
                    yA[jj * nP + a * D1 + b] += y * pi[a] * dl[b]
                    yA[ll * nP + a * D1 + b] += y * pi[a] * dj[b]
            base = k * nP + q * nQ
            for t, (a, b) in enumerate(sym):
                yA[base + t] += y * pi[a] * pi[b]
            yb += y * sum(dj[b] * dl[b] for b in range(1, D1))
    return all(x == 0 for x in yA), yb


def certify(name, rat_us, m, j, d, seed):
    rng = random.Random(seed)
    D1 = d + 1
    last = "no attempt reached the W step"
    for attempt in range(50):
        free_us = [[Fr(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(d - 1)] for _ in range(j)]
        us = rat_us[:m] + free_us
        P = [lift(u) for u in us]
        n = len(P)
        gen = list(range(m, n))
        # (Q): rows (a,b), a <= b, minus (0,0)
        symr = [(a, b) for a in range(D1) for b in range(a, D1) if (a, b) != (0, 0)]
        ML = [[P[i][a] * P[i][b] for i in range(n)] for (a, b) in symr]
        KL, rL = kernel(ML, n)
        if not (rL == len(symr) and len(KL) == 1): continue        # need full row rank, n = rows + 1
        lam = KL[0]
        # (P): unknowns alpha_{i,r} (i generic, r < d-1), then mu_i
        cols = [(i, r) for i in gen for r in range(d - 1)]
        nv = len(cols) + n
        dP = {(i, r): dlift(us[i], r) for (i, r) in cols}
        fullr = [(a, b) for a in range(D1) for b in range(D1) if (a, b) != (0, 0)]
        MW = []
        for (a, b) in fullr:
            MW.append([P[i][a] * dP[(i, r)][b] for (i, r) in cols] + [P[i][a] * P[i][b] for i in range(n)])
        R = len(fullr)
        Z = sorted(rng.sample(range(nv), nv - (R + 1)))           # unknowns fixed to 0
        keep = [c for c in range(nv) if c not in Z]
        KW, rW = kernel([[row[c] for c in keep] for row in MW], len(keep))
        last = f"rank M_L = {rL} of {len(symr)}; rank M_W(kept columns) = {rW} of R = {R} rows, full M_W rank {kernel([list(x) for x in zip(*MW)], R)[1]}"
        if not (rW == R and len(KW) == 1): continue
        z = [Fr(0)] * nv
        for c, v in zip(keep, KW[0]): z[c] = v
        w = {i: [sum(z[t] * dP[(ii, r)][b] for t, (ii, r) in enumerate(cols) if ii == i) for b in range(D1)] for i in gen}
        active = [i for i in gen if any(w[i])]
        # lambda~_i(tau) != 0 for ALL generic i (every i whose w_i may be nonzero as a polynomial), not only
        # for the active ones (w_i(tau) != 0): each term of E over F divides by lambda~_i.
        if any(lam[i] == 0 for i in gen): continue
        S = [-1] + [1] * d
        E = sum(sum(S[b] * w[i][b] ** 2 for b in range(D1)) / lam[i] for i in active)
        if E == 0: continue
        # ---- consistency checks in inhomogeneous coordinates (exact, at tau)
        h = [p[0] for p in P]
        lam_in = [lam[i] * h[i] ** 2 for i in range(n)]
        p_in = [[x / h[i] for x in P[i]] for i in range(n)]
        # D p_i = (D p~_i)/h - p~_i (D h)/h^2 with D p~_i = w_i / lam~_i
        Dp = []
        for i in range(n):
            if i in active:
                Dpt = [x / lam[i] for x in w[i]]
                Dp.append([Dpt[b] / h[i] - P[i][b] * Dpt[0] / h[i] ** 2 for b in range(D1)])
            else:
                Dp.append([Fr(0)] * D1)
        c1 = all(sum(lam_in[i] * p_in[i][a] * p_in[i][b] for i in range(n)) == 0 for a in range(D1) for b in range(D1))
        c2 = all(sum(lam_in[i] * Dp[i][b] for i in range(n)) == 0 for b in range(1, D1))
        Ma = [[sum(lam_in[i] * Dp[i][a] * p_in[i][b] for i in range(n)) for b in range(1, D1)] for a in range(1, D1)]
        c3 = all(Ma[a][b] == Ma[b][a] for a in range(d) for b in range(d))
        E2 = sum(lam_in[i] * sum(Dp[i][b] ** 2 for b in range(1, D1)) for i in range(n))
        c0 = all(Dp[i][0] == 0 for i in range(n))
        print(f"{name}: m={m} j={j} n={n} d={d}  tau-attempt {attempt}: rank M_L = {rL} (of {len(symr)} rows, n = {n}), "
              f"rank M_W = {rW} (of {R} rows, {nv} unknowns, {len(Z)} fixed to 0)")
        print(f"   generic points carrying the derivation at tau: {len(active)} of {j}; "
              f"lambda~_i(tau) != 0 for all {j} generic points: {all(lam[i] != 0 for i in gen)}")
        print(f"   E(tau) = {float(E):.6e} (exact rational; numerator {len(str(abs(E.numerator)))} digits, "
              f"denominator {len(str(E.denominator))} digits); nonzero => scalar certificate over F")
        print(f"   checks at tau: Dp_0 = 0 {c0}; sum lam p p^T = 0 {c1}; sum lam D a = 0 {c2}; "
              f"sum lam D(a) a^T symmetric {c3}; sum lam |Da|^2 = E {E2 == E}")
        print(f"   tau (free points' stereographic u): {[[str(x) for x in u] for u in free_us]}")
        # ---- the same certificate as a dual vector of probe2.jet2's exact row/column layout, at tau
        k = j * (d - 1)
        c = [Fr(0)] * k
        Dfull = [[[Fr(0)] * D1 for _ in range(k)] for _ in range(n)]     # D_v p_i, inhomogeneous
        for t, (i, r) in enumerate(cols):
            v = (i - m) * (d - 1) + r                                    # indep_sphere's parameter index
            c[v] = z[t] / lam[i] if i in active else Fr(0)
            dpt = dP[(i, r)]
            Dfull[i][v] = [dpt[b] / h[i] - P[i][b] * dpt[0] / h[i] ** 2 for b in range(D1)]
        mu_t = z[len(cols):]
        # sum lam_i p_i (D p_i)^T = sum nu_i p_i p_i^T  with  nu_i = -(mu~_i + lam~_i D h_i / h_i) h_i^2
        nu = [-(mu_t[i] + (w[i][0] / h[i] if i in active else 0)) * h[i] ** 2 for i in range(n)]
        y_ok, yb = jet2_dual_check(p_in, Dfull, lam_in, c, nu, k, d)
        print(f"   as a jet2 dual vector at tau: y^T A = 0 {y_ok}; y^T b = E {yb == E}")
        return E != 0 and c0 and c1 and c2 and c3 and E2 == E and y_ok and yb == E
    print(f"{name}: m={m} j={j}: no exact certificate of this shape in 50 attempts (inconclusive, not NONE); "
          f"last attempt: {last}.  If full M_W rank < R the cofactor construction needs a second certified row relation.")
    return False


if __name__ == "__main__":
    rng = random.Random(11)
    rats2 = [rat_sphere_exact(3, rng) for _ in range(14)]     # e1_s2.py's rational points, exactly
    rng = random.Random(13)
    rats3 = [rat_sphere_exact(4, rng) for _ in range(20)]     # e1_s3.py's rational points, exactly
    ok = []
    for m, j in [(6, 4), (5, 5), (4, 6), (3, 7)]:
        ok.append(certify("S^2 cell", rats2, m, j, 3, seed=100 + m))
    for m, j in [(11, 4), (10, 5)]:
        ok.append(certify("S^3 cell", rats3, m, j, 4, seed=200 + m))
    rng = random.Random(17)
    rats4 = [rat_sphere_exact(5, rng) for _ in range(24)]     # e1_s4.py's rational points, exactly
    ok.append(certify("S^4 threshold", rats4, 17, 4, 5, seed=317))
    ok.append(certify("S^2 generic (e3_sphere generic 3)", [], 0, 10, 3, seed=410))
    print("all certified:", all(ok), ok)
