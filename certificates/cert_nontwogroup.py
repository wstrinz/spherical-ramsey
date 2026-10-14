"""Exact Ramsey certificates for cyclic sets that are NOT unions of two Mobius images of
algebraic sets (the note's Theorem NTG: W7, W8 and the radian 7-gon; the exact refutation of C-13;
evidence for C-23(i)).

applies_to: the one-parameter circle configurations listed below (stereographic parameters
  r_i(t) in Q(t), t transcendental real; F = Q(t); B = Q(t) (x) Q(t) inside Q(T, U)).

For each configuration:
  (1) EXACT non-two-group check: list the 4-point cross-ratios of the r_i that are constant in t
      (sympy); a non-constant rational function of t is transcendental at transcendental t.  A part
      of a two-group partition is a Mobius image of an algebraic set iff it has <= 3 points or all
      its 4-point cross-ratios are algebraic (= constant here); test all 2-part partitions.
  (2) EXACT certificate: a (2,2)-form g with coefficients in Q(T)[U] (inside B), printed in full,
      with g(r_i(T), r_i(U)) = 0 identically and g(T, T) = kappa (s - s')^2, kappa != 0 (re-verified
      here by exact_circle_cert.verify).  Glue: the note's circle dictionary (P := C^{-T} M_g C^{-1}) plus
      Lemma 0, exactly as for Theorem B(a) / cert_mobius.py.
usage (from any directory): python3 -I cert_nontwogroup.py          (expected/cert_nontwogroup.log)
       slow (radian 7-gon):  python3 -I cert_nontwogroup.py --slow   (expected/cert_nontwogroup.slow.log)
"""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
from exact_circle_cert import T, U, MONO, decide, verify, R5, tan_mult

H4 = [T, T + 1, 2 * T, 1 / T]
CONFIGS = {
    "W7: rational 0, 1/2, 1/3 + circ(t), circ(t+1), circ(2t), circ(1/t)": R5[:3] + H4,
    "W8: rational 0, 1/2, 1/3, 2/3 + circ(t), circ(t+1), circ(2t), circ(1/t)": R5[:4] + H4,
}
SLOW = {
    "radian 7-gon {k theta : k <= 6}, t = tan(theta/2)  (slow: 25-40 min)": [tan_mult(k) for k in range(7)],
}
if "--slow" in sys.argv:
    CONFIGS = SLOW

def constant_crs(rs):
    bad = []
    for q in itertools.combinations(range(len(rs)), 4):
        a, b, c, d = [rs[i] for i in q]
        cr = sp.cancel((a - c) * (b - d) / ((a - d) * (b - c)))
        if sp.cancel(sp.diff(cr, T)) == 0:
            bad.append((q, cr))
    return bad

if __name__ == "__main__":
    for name, rs in CONFIGS.items():
        print("=" * 100)
        print(name)
        print("stereographic parameters r_i(t):", [str(r) for r in rs])
        bad = constant_crs(rs)
        n4 = len(list(itertools.combinations(range(len(rs)), 4)))
        const = {q for q, _ in bad}
        print(f"(1) constant 4-point cross-ratios: {len(bad)} of {n4}")
        for q, cr in bad: print("    constant:", q, cr)
        def is_group(part):
            return len(part) <= 3 or all(q in const for q in itertools.combinations(sorted(part), 4))
        n = len(rs)
        two = any(is_group([i for i in range(n) if m >> i & 1]) and is_group([i for i in range(n) if not m >> i & 1])
                  for m in range(1 << (n - 1)))
        print(f"    exact partition test (a part is a group iff <= 3 points or all its 4-point cross-ratios constant): two-group = {two}")
        verdict, g = decide(name[:52], rs)
        if g is not None:
            print("(2) certificate g(s, s') = sum g_ab s^a s'^b, coefficients in Q(T)[U]:")
            for k, (a, b) in enumerate(MONO):
                print(f"    g_{a}{b} = {sp.factor(g[k])}")
            gT = [sp.cancel(e.subs(U, T)) for e in g]
            print("    kappa = g_20(T, T) =", sp.factor(gT[MONO.index((2, 0))]))
            print("    independent re-verification:", verify(rs, g))
        print("VERDICT:", verdict)
