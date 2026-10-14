"""Scalar (single-derivation) 2-jet certificates, mod p: the test for conjectures SR-C11 / SR-C12.

applies_to: the 2-jet system (probe2.jet2, c = 1; the note's second-order section) for any finite
  spherical configuration given as probe2 point functions of k parameters.
  Method R (random c) applies to every such configuration.  Method A (all c at once) needs the
  parameter sets of the non-constant points to be pairwise disjoint (e.g. rational points plus
  independent generic points, indep_circle / indep_sphere); it is asserted.

Background (the corrected dual form of the 2-jet system, as in the note).  A dual certificate of the
2-jet system is (Lambda_i, mu_ij) with, for each j, sum_i sum_l (Lambda_i)_jl p_i (D_l p_i)^T in
span{p_i p_i^T} (full matrices), sum_i (Lambda_i)_jl p_i p_i^T = 0, and sum_i tr(Lambda_i G_i) != 0.
A SCALAR certificate is Lambda_i = lambda_i c c^T (one derivation D = sum_j c_j D_j, c in F^k; order-1
multipliers mu_ij free).  Substituting, the conditions become
    (Q)  sum_i lambda_i p_i p_i^T = 0,
    (P)  sum_i lambda_i p_i (D p_i)^T in span{p_i p_i^T}   (full (d+1)x(d+1) matrices),
    (E)  sum_i lambda_i |D a_i|^2 != 0,
which is exactly the Fredholm dual of the 2-jet system for the ONE derivation D (k = 1, rows
p^T P p = 0 and 2 p^T P Dp + p^T Q p = |Da|^2).  So:
  Method R: fix c (random mod p), run probe2.jet2 on the configuration seen through D alone.
            FAIL  <=>  (mod p) a scalar certificate with this c exists.
  Method A: with w_i = lambda_i D a_i (tangent at a_i), (Q) and (P) are LINEAR and decouple:
            lambda in L = {sum lambda_i p_i p_i^T = 0},  w in W = {sum p_i (0, w_i)^T in span p_i p_i^T},
            w_i = 0 where lambda_i vanishes on L; and (E) reads  E = sum_i |w_i|^2 / lambda_i.
            A scalar certificate exists for SOME D iff E is not identically 0 on L x W (generic
            point test).  When E != 0 the derivation is recovered (v_i = w_i / lambda_i -> c) and
            re-checked by Method R with that c (it must FAIL).
Everything is mod p and [PROBE]; NO_VERDICT if every attempt raised (nonresidue), never PASS/FAIL.

As a script: the scan of rational points + independent generic points (pairwise disjoint parameter
sets) on S^1..S^4: three circle controls, the S^2 cells of e1_s2.py next to and beyond the threshold
(rational points regenerated exactly as there, Random(11)), the S^3 threshold cells of e1_s3.py
(Random(13)), the S^4 threshold of e1_s4.py (Random(17)), and 9 / 10 generic points on S^2.  Per cell:
the 2-jet verdict, method A (3 independent draws; SCALAR_FOUND is re-checked by method R with the
recovered c, which must FAIL), and method R over C11_NC random c (default 12; a random c is NOT a
valid test for the absence of a scalar certificate, it is printed for contrast).  All specialization
streams are seeded (Random(1111)).  Every verdict is [PROBE].  Log: expected-v2/scalar_cert.log.
usage: python3 -I scalar_cert.py      (about 2 min; C11_S3=0 / C11_S4=0 skip the S^3 / S^4 parts)
"""
import os, sys, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
import probe2


def jets_at(points, k, tau):
    """p_i = (1, a_i) and D_j p_i (j < k) at theta = tau, mod p."""
    th = [J(tau[j], [1 if i == j else 0 for i in range(k)]) for j in range(k)]
    ps, Dps = [], []
    for f in points:
        a = [x if isinstance(x, J) else J(x, [0] * k) for x in f(th)]
        ps.append([1] + [x.v for x in a])
        Dps.append([[0] + [x.d[j] for x in a] for j in range(k)])
    return ps, Dps


def single_derivation(points, k, tau, c):
    """The configuration seen through the one derivation D = sum c_j d/dtheta_j at tau: point
    functions of a dummy 1-parameter theta, returning first-order jets with d = [D x]."""
    th = [J(tau[j], [c[j]]) for j in range(k)]
    vals = [[x if isinstance(x, J) else J(x, [0]) for x in f(th)] for f in points]
    return [(lambda v: (lambda _th: v))(v) for v in vals]


def method_R(points, k, d, rng, tau=None, c=None):
    """True = consistent (no scalar certificate for this c), False = scalar certificate exists."""
    tau = tau or [rng.randrange(2, P - 2) for _ in range(k)]
    c = c or [rng.randrange(1, P - 1) for _ in range(k)]
    return jet2(single_derivation(points, k, tau, c), 1, d, tau=[2])


def _rand_comb(basis, n, rng):
    v = [0] * n
    for b in basis:
        r = rng.randrange(1, P - 1)
        v = [(x + r * y) % P for x, y in zip(v, b)]
    return v


def method_A(points, k, d, rng, varsets, draws=4):
    """varsets[i] = list of parameter indices of point i ([] for constant points), pairwise disjoint.
    Returns (verdict, info): verdict 'SCALAR_FOUND' / 'SCALAR_NONE' (E == 0 at every draw);
    raises ValueError (nonresidue) like probe2."""
    used = [j for vs in varsets for j in vs]
    assert len(used) == len(set(used)), "method A needs disjoint parameter sets"
    tau = [rng.randrange(2, P - 2) for _ in range(k)]
    ps, Dps = jets_at(points, k, tau)
    n, D1 = len(ps), d + 1
    sym = [(a, b) for a in range(D1) for b in range(a, D1)]
    # L: sum lambda_i p_i p_i^T = 0
    Lb = nullspace_mod([[ps[i][a] * ps[i][b] % P for i in range(n)] for (a, b) in sym], n)
    supp = [any(v[i] for v in Lb) for i in range(n)]
    # W: unknowns alpha_{i,j} (w_i = sum_j alpha_ij D_j a_i, j in varsets[i]) then mu_i
    cols = [(i, j) for i in range(n) for j in varsets[i]]
    nv = len(cols) + n
    eqs = []
    for a in range(D1):
        for b in range(D1):
            row = [0] * nv
            for t, (i, j) in enumerate(cols):
                row[t] = ps[i][a] * Dps[i][j][b] % P
            for i in range(n):
                row[len(cols) + i] = ps[i][a] * ps[i][b] % P
            eqs.append(row)
    for t, (i, j) in enumerate(cols):          # w_i = 0 where lambda_i vanishes identically on L
        if not supp[i]:
            row = [0] * nv; row[t] = 1; eqs.append(row)
    Wb = nullspace_mod(eqs, nv)
    info = dict(dimL=len(Lb), dimW=len(Wb), n=n)
    if not Lb:
        return "SCALAR_NONE", info
    for _ in range(draws):
        lam = _rand_comb(Lb, n, rng)
        z = _rand_comb(Wb, nv, rng) if Wb else [0] * nv
        if any(supp[i] and lam[i] == 0 for i in range(n)):
            continue
        w = {}
        for t, (i, j) in enumerate(cols):
            w.setdefault(i, [0] * D1)
            w[i] = [(x + z[t] * y) % P for x, y in zip(w[i], Dps[i][j])]
        E = sum(sum(x * x for x in wi[1:]) % P * inv(lam[i]) for i, wi in w.items() if supp[i]) % P
        if E:
            # recover c: v_i = w_i / lambda_i = sum_j c_j D_j a_i  =>  c_j = alpha_ij / lambda_i
            c = [0] * k
            for t, (i, j) in enumerate(cols):
                c[j] = z[t] * inv(lam[i]) % P if supp[i] else 0
            recheck = jet2(single_derivation(points, k, tau, c), 1, d, tau=[2])
            info.update(E=E, recheck_R_with_recovered_c=("FAIL" if recheck is False else "PASS"))
            return "SCALAR_FOUND", info
    return "SCALAR_NONE", info


def retry_A(points, k, d, rng, varsets, attempts=200):
    for _ in range(attempts):
        try:
            return method_A(points, k, d, rng, varsets)
        except ValueError:
            continue
    return "NO_VERDICT", {}


def retry_R(points, k, d, rng, nc, attempts=200):
    """Method R over nc random c (fresh tau each): counts (found, none, no_verdict)."""
    found = none = nv = 0
    for _ in range(nc):
        for _ in range(attempts):
            try:
                if method_R(points, k, d, rng): none += 1
                else: found += 1
                break
            except ValueError:
                continue
        else:
            nv += 1
    return found, none, nv


# ---------------------------------------------------------------------------------------------------
# The scan (script mode).

def _varsets_sphere(m, j, d):
    return [[] for _ in range(m)] + [list(range(i * (d - 1), (i + 1) * (d - 1))) for i in range(j)]


def _cell(name, pts, k, d, vs, srng, nc, na=3):
    from validate import retry
    t0 = time.time()
    v = retry(jet2, pts, k, d, trials=1, rng=srng)
    A = [retry_A(pts, k, d, srng, vs) for _ in range(na)]
    Av = sorted({a for a, _ in A})
    info = A[0][1]
    R = retry_R(pts, k, d, srng, nc)
    print(f"{name:34s} 2-jet {v:10s} | A: {'/'.join(Av):24s} dimL={info.get('dimL')} dimW={info.get('dimW')}"
          f" recheck={[i.get('recheck_R_with_recovered_c', '-') for _, i in A]} | R(random c, {nc}): found {R[0]} none {R[1]} nv {R[2]}"
          f"  ({time.time() - t0:.0f}s)")
    sys.stdout.flush()
    return v, Av, R


if __name__ == "__main__":
    from validate import rats as circ_rats, indep_circle, tally_line
    from e3_sphere import indep_sphere
    NC = int(os.environ.get("C11_NC", "12"))      # random c per cell for method R
    print(f"# prime P = {P}")
    srng = random.Random(1111)                     # specialization RNG (explicit seed)
    print("== controls (circle, k = #free points)")
    _cell("S1: 3 rat + 4 free (CERT-S known)", circ_rats[:3] + indep_circle(4), 4, 2, [[]] * 3 + [[i] for i in range(4)], srng, NC)
    _cell("S1: 3 rat + 3 free (PASS cell)", circ_rats[:3] + indep_circle(3), 3, 2, [[]] * 3 + [[i] for i in range(3)], srng, NC)
    _cell("S1: 0 rat + 9 free (OAI 7.6)", indep_circle(9), 9, 2, [[i] for i in range(9)], srng, NC)

    print("== S^2 (e1_s2 rational points, Random(11))")
    rng = random.Random(11)
    rats2 = [rand_rat_sphere(3, rng) for _ in range(14)]
    fails = [(m, j) for j in range(4, 8) for m in range(0, 12) if m + j >= 10 and m + j <= 13]
    passes = [(9, 3), (5, 4), (4, 5), (3, 6), (2, 7)]           # PASS cells next to the boundary
    for m, j in passes + fails:
        tag = "FAIL cell" if (m, j) in fails else "PASS cell"
        _cell(f"S2: m={m} j={j} n={m + j} ({tag})", rats2[:m] + indep_sphere(j, 3), 2 * j, 3, _varsets_sphere(m, j, 3), srng, NC)

    if os.environ.get("C11_S3", "1") == "1":
        print("== S^3 (e1_s3 rational points, Random(13))")
        rng = random.Random(13)
        rats3 = [rand_rat_sphere(4, rng) for _ in range(20)]
        for m, j in [(10, 4), (11, 4), (9, 5), (10, 5)]:
            tag = "FAIL cell" if m + j == 15 else "PASS cell"
            _cell(f"S3: m={m} j={j} n={m + j} ({tag})", rats3[:m] + indep_sphere(j, 4), 3 * j, 4, _varsets_sphere(m, j, 4), srng, NC)

    if os.environ.get("C11_S4", "1") == "1":
        print("== S^4 threshold (e1_s4 rational points, Random(17)) and S^2 generic (e3_sphere)")
        rng = random.Random(17)
        rats4 = [rand_rat_sphere(5, rng) for _ in range(24)]
        for m in (16, 17):
            tag = "FAIL cell" if m == 17 else "PASS cell"
            _cell(f"S4: m={m} j=4 n={m + 4} ({tag})", rats4[:m] + indep_sphere(4, 5), 16, 5, _varsets_sphere(m, 4, 5), srng, NC)
        for j in (9, 10):
            tag = "FAIL cell" if j == 10 else "PASS cell"
            _cell(f"S2: generic j={j} ({tag})", indep_sphere(j, 3), 2 * j, 3, _varsets_sphere(0, j, 3), srng, NC)
    print(tally_line())
