"""Exact certificates for OpenAI #172 (Thm 1.1) on the unit circle, verified symbolically.

Unit circle points p(t) = (1, (1-t^2)/(1+t^2), 2t/(1+t^2)) = q(t)/(1+t^2), q(t) = C (1,t,t^2).
A (2,2)-form f(s,s') = v(s)^T M v(s') gives P = C^{-T} M C^{-1}, and
    p_i(T)^T P p_i(U) = f(T_i, U_i) / ((1+T_i^2)(1+U_i^2)).
Graph form of the unique Mobius map sending T_a -> U_a (a = 1,2,3):
    g(s,s') = det [[s s', s, s', 1], [T_a U_a, T_a, U_a, 1]_{a=1,2,3}]
which vanishes at (T_a, U_a) and restricts on the diagonal (U = T) to (s - s') * Vandermonde.
"""
import sympy as sp
s, sq = sp.symbols("s sq")
C = sp.Matrix([[1, 0, 1], [1, 0, -1], [0, 2, 0]])
Ci = C.inv()

def g(pairs):
    rows = [[s * sq, s, sq, 1]] + [[T * U, T, U, 1] for T, U in pairs]
    return sp.expand(sp.Matrix(rows).det())

def to_P(f):
    poly = sp.Poly(sp.expand(f), s, sq)
    M = sp.zeros(3, 3)
    for (a, b), c in poly.terms():
        M[a, b] = c
    return sp.expand_func(Ci.T * M * Ci)

def p(t):
    return sp.Matrix([1, (1 - t**2) / (1 + t**2), 2 * t / (1 + t**2)])

def check(name, f, free_pairs, rational_ts):
    P = to_P(f)
    ok = True
    for T, U in free_pairs:
        ok &= sp.simplify((p(T).T * P * p(U))[0]) == 0
    for a in rational_ts:
        ok &= sp.simplify((p(a).T * P * p(a))[0]) == 0
    subs = {U: T for T, U in free_pairs}
    D = sp.simplify(P.subs(subs))
    spatial_ok = sp.simplify(D[1, 2]) == 0 and sp.simplify(D[2, 1]) == 0 and sp.simplify(D[1, 1] - D[2, 2]) == 0
    c = sp.factor(D[1, 1])
    print(f"{name}\n   evaluation identities: {ok};  m(P) spatial block = c*I: {spatial_ok};  c = {c}")

T = sp.symbols("T1:7"); U = sp.symbols("U1:7")
pairs = list(zip(T, U))
# (1) ANY six points on the circle: product of two Mobius graph forms
check("six arbitrary points (two triples, two Mobius graphs)", g(pairs[:3]) * g(pairs[3:6]), pairs[:6], [])
# (2) rational points (any number) + three arbitrary points: diagonal x one Mobius graph
rat = [sp.Rational(0), sp.Rational(1, 2), sp.Rational(-3, 4), sp.Rational(5, 3), sp.Rational(7), sp.Rational(-2, 9)]
check("6 rational points + three arbitrary points (diagonal x Mobius graph)", (s - sq) * g(pairs[:3]), pairs[:3], rat)
