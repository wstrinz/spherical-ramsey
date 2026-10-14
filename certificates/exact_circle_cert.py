"""Exact one-parameter circle decision procedure (C-19's algorithm, case k = 1, circle),
written as C-19's falsifier (the record was filed before this script).

applies_to: finite subsets of the unit circle given by stereographic parameters r_i(t) in Q(t)
  (rational points = constants), t transcendental.  Coordinate field F inside Q(t), so
  B = F (x) F embeds in Q(T, U); everything below is exact sympy arithmetic over Q(T)[U].

Criterion (the note's circle form of OpenAI's field criterion, |A| >= 3, pole avoided): A is Ramsey iff there is a (2,2)-form
f(s, s') = sum_{a,b<=2} f_ab s^a s'^b with coefficients in B such that f(r_i(T), r_i(U)) = 0 for all i
and m(f) := f|_{U=T} = kappa (s - s')^2 with kappa in F^x.

Procedure:
  1. V = kernel over K = Q(T, U) of the n x 9 evaluation matrix (rows x_i^a y_i^b, x = r_i(T),
     y = r_i(U)); clear denominators so each basis vector lies in Q[T, U]^9 (inside B).
  2. Saturate at the prime (U - T) of Q(T)[U]: while the reductions b_j(T, T) are Q(T)-dependent,
     replace one b_j by (sum_j c_j b_j)/(U - T), with c in Q(T)^r (exact division in Q(T)[U]).
     Entries stay in Q(T)[U], which lies in B (functions of T alone are in F (x) 1).
  3. RAMSEY certificate: if (s - s')^2 lies in the Q(T)-span of the reductions, output
     g = sum alpha_j b_j (alpha in Q(T)) and VERIFY it independently: g(r_i(T), r_i(U)) == 0 for all i
     (sympy cancel) and g(T, T) = kappa (s - s')^2 with kappa != 0.  This verification alone is the
     [CERT] (the glue is the note's circle dictionary plus Lemma 0, as for Theorem B(a)).
  4. Otherwise NON-RAMSEY, by the k = 1 DVR criterion (the local ring at the diagonal is a DVR; a
     written argument, reviewed (AI), not part of this script's check): the reductions of the saturated lattice span exactly the limit space.
     (For n = 9 with a 0-dimensional kernel this is just Theorem D's determinant argument.)
usage (from any directory): python3 -I exact_circle_cert.py [names...]
  each name selects the cases whose label contains it (no names = every case, including the radian
  8-gon, which did not finish in 40 min); see README.md for the selections used by check.sh.
"""
import sys, time
import sympy as sp
from sympy.polys.matrices import DomainMatrix

T, U, S, S2 = sp.symbols("T U s sp")
QTU = sp.QQ.frac_field(T, U)
MONO = [(a, b) for a in range(3) for b in range(3)]
TARGET = {(2, 0): 1, (1, 1): -2, (0, 2): 1}           # (s - s')^2

def eval_rows(rs):
    rows = []
    for r in rs:
        x, y = r, r.subs(T, U)
        rows.append([sp.together(x ** a * y ** b) for a, b in MONO])
    return rows

def kernel(rs):
    M = sp.Matrix(eval_rows(rs))
    dM = DomainMatrix.from_Matrix(M).convert_to(QTU)
    ns = dM.nullspace().to_Matrix()
    vecs = []
    for i in range(ns.rows):
        v = [sp.together(ns[i, j]) for j in range(ns.cols)]
        den = sp.Integer(1)
        for e in v:
            den = sp.lcm(den, sp.denom(e))
        v = [sp.expand(sp.cancel(e * den)) for e in v]
        g = sp.Integer(0)
        for e in v:
            g = sp.gcd(g, e)
        vecs.append([sp.expand(sp.cancel(e / g)) for e in v] if g not in (0, 1) else v)
    return vecs

def red(v):
    return [sp.cancel(e.subs(U, T)) for e in v]

def saturate(vecs, log):
    it = 0
    while vecs:
        R = sp.Matrix([red(v) for v in vecs])          # r x 9 over Q(T)
        dR = DomainMatrix.from_Matrix(R.T).convert_to(sp.QQ.frac_field(T))
        rel = dR.nullspace().to_Matrix()                # relations among the r reductions
        if rel.rows == 0:
            return vecs
        c = [sp.cancel(rel[0, j]) for j in range(rel.cols)]
        den = sp.Integer(1)
        for e in c: den = sp.lcm(den, sp.denom(e))
        c = [sp.cancel(e * den) for e in c]
        j0 = next(j for j in range(len(c)) if c[j] != 0)
        comb = [sp.expand(sum(c[j] * vecs[j][k] for j in range(len(vecs)))) for k in range(9)]
        new = []
        for e in comb:
            q, rmd = sp.div(sp.Poly(e, U, domain=sp.QQ.frac_field(T)), sp.Poly(U - T, U, domain=sp.QQ.frac_field(T)))
            assert rmd.is_zero, "saturation: combination not divisible by (U - T)"
            new.append(sp.cancel(q.as_expr()))
        vecs[j0] = new
        it += 1
        if it > 60:
            raise RuntimeError("saturation did not terminate")
    return vecs

def decide(name, rs, verbose=True):
    t0 = time.time()
    vecs = kernel(rs)
    dimV = len(vecs)
    if dimV == 0:
        print(f"{name:52s} n={len(rs)} dim V = 0  => NON-RAMSEY (exact: Theorem D argument)  [{time.time()-t0:.1f}s]")
        return "NON-RAMSEY", None
    vecs = saturate(vecs, None)
    R = [red(v) for v in vecs]
    tgt = sp.Matrix([TARGET.get(m, 0) for m in MONO])
    A = sp.Matrix(R).T                                   # 9 x r over Q(T)
    dA = DomainMatrix.from_Matrix(A.row_join(tgt)).convert_to(sp.QQ.frac_field(T))
    rA = DomainMatrix.from_Matrix(A).convert_to(sp.QQ.frac_field(T)).rank()
    if dA.rank() != rA:
        print(f"{name:52s} n={len(rs)} dim V = {dimV}  (s-s')^2 not in limit space => NON-RAMSEY (k=1 DVR criterion)  [{time.time()-t0:.1f}s]")
        return "NON-RAMSEY", None
    # solve A alpha = tgt over Q(T)
    sol = sp.Matrix(A).gauss_jordan_solve(tgt)[0]
    sol = sol.subs({s: 0 for s in sol.free_symbols - {T}})
    alpha = [sp.cancel(a) for a in sol]
    g = [sp.cancel(sum(alpha[j] * vecs[j][k] for j in range(len(vecs)))) for k in range(9)]
    ok = verify(rs, g)
    print(f"{name:52s} n={len(rs)} dim V = {dimV}  RAMSEY certificate found; independent verification: {ok}  [{time.time()-t0:.1f}s]")
    return ("RAMSEY" if ok else "CERT-VERIFY-FAILED"), g

def verify(rs, g):
    """independent check: g has denominators in T only, vanishes at every (r_i(T), r_i(U)),
    and g(T, T) = kappa (s - s')^2 with kappa != 0."""
    for e in g:
        if sp.denom(sp.together(e)).has(U):
            return False
    for r in rs:
        x, y = r, r.subs(T, U)
        val = sp.cancel(sum(g[k] * x ** a * y ** b for k, (a, b) in enumerate(MONO)))
        if val != 0:
            return False
    gT = [sp.cancel(e.subs(U, T)) for e in g]
    kappa = gT[MONO.index((2, 0))]
    if kappa == 0:
        return False
    return all(sp.cancel(gT[k] - kappa * TARGET.get(m, 0)) == 0 for k, m in enumerate(MONO))

def tan_mult(k):
    s = sp.Integer(0)
    for _ in range(k):
        s = sp.cancel((s + T) / (1 - s * T))
    return s

R5 = [sp.Integer(0), sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(3, 4)]
R6 = R5 + [sp.Rational(-2, 5)]
H4 = [T, T + 1, 2 * T, 1 / T]

CASES = {
    # controls with known verdicts (C-19 falsifier: must reproduce these)
    "control: 6 rational + circ(t)  [Ramsey, B(b)]": R6 + [T],
    "control: circ(kt), k=1..7  [Ramsey, C-cor]": [k * T for k in range(1, 8)],
    "control: 5 rat + t, t+1, 2t, 1/t  [non-Ramsey, det]": R5 + H4,
    "control: 3 rat + t, t+1, t+2, t+3  [Ramsey, two-group]": R5[:3] + [T, T + 1, T + 2, T + 3],
    "control: radian 9-gon  [non-Ramsey, Theorem D]": [tan_mult(k) for k in range(9)],
    # new: non-two-group configurations predicted Ramsey by C-23(i)
    "NEW: 3 rat + t, t+1, 2t, 1/t  (7 pts, not two-group)": R5[:3] + H4,
    "NEW: 4 rat + t, t+1, 2t, 1/t  (8 pts, not two-group)": R5[:4] + H4,
    "NEW: radian 7-gon": [tan_mult(k) for k in range(7)],
    "NEW: radian 8-gon  (C-10)": [tan_mult(k) for k in range(8)],
}

if __name__ == "__main__":
    want = sys.argv[1:]
    for name, rs in CASES.items():
        if want and not any(w in name for w in want):
            continue
        try:
            decide(name, rs)
        except Exception as ex:
            print(f"{name:52s} ERROR {type(ex).__name__}: {ex}")
        sys.stdout.flush()
