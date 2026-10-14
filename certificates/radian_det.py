"""Exact proof (OpenAI Prop 7.6 method) that the 9 points at angles 0, th, ..., 8th are non-Ramsey
whenever t = tan(th/2) is transcendental: the 9x9 tensor evaluation matrix has nonzero determinant
in Q(T,U) (checked at rational specializations), so its kernel over Frac(B) is 0."""
from fractions import Fraction as Fr
import sympy as sp
def tank(t, k):
    r = Fr(0)
    for _ in range(k): r = (r + t) / (1 - r * t)
    return r
def circ(s): return (1 - s*s)/(1 + s*s), 2*s/(1 + s*s)
def row(pT, pU):
    a = [Fr(1), *pT]; b = [Fr(1), *pU]
    return [a[i]*b[j] for i in range(3) for j in range(3)]
for (T, U) in [(Fr(1,3), Fr(2,7)), (Fr(-5,11), Fr(3,13))]:
    M = sp.Matrix([row(circ(tank(T, k)), circ(tank(U, k))) for k in range(9)])
    print(f"T={T}, U={U}: det = {M.det()}")
