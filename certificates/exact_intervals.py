"""Exact interval arithmetic over Fractions, for the definable-colouring certificates.

applies_to: any real-polynomial or exp expression in finitely many variables whose transcendental
constants are cos q, sin q, exp q (q rational) or tan(1/2); every bound is a rational interval and
is a proven enclosure (Taylor with Lagrange remainder), so a verdict "0 not in I" or "I inside a
window" is an exact certificate, not a numeric estimate.

Soundness notes:
- Interval ops return supersets of the true range (standard interval arithmetic, exact Fractions:
  no rounding at all).
- cos/sin at rational x: partial Taylor sum S_N plus |remainder| <= |x|^(N+1)/(N+1)! (Lagrange;
  all derivatives bounded by 1).
- exp at rational x >= 0: S_N <= e^x <= S_N + x^(N+1)/(N+1)! * 3^ceil(x) (e < 3); x < 0 by reciprocal.
"""
from __future__ import annotations

from fractions import Fraction as Fr
from math import ceil, factorial


class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        lo = Fr(lo)
        hi = lo if hi is None else Fr(hi)
        if lo > hi:
            raise ValueError("empty interval")
        self.lo, self.hi = lo, hi

    @staticmethod
    def of(v):
        return v if isinstance(v, I) else I(v)

    def __add__(self, o):
        o = I.of(o)
        return I(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-I.of(o))

    def __rsub__(self, o):
        return I.of(o) - self

    def __mul__(self, o):
        o = I.of(o)
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return I(min(p), max(p))

    __rmul__ = __mul__

    def recip(self):
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains 0")
        return I(1 / self.hi, 1 / self.lo)

    def __truediv__(self, o):
        return self * I.of(o).recip()

    def __pow__(self, n: int):
        if n == 0:
            return I(1)
        if n % 2 == 1 or self.lo >= 0:  # odd powers are increasing; even powers too on [0, inf)
            return I(self.lo ** n, self.hi ** n)
        if self.hi <= 0:
            return I(self.hi ** n, self.lo ** n)
        return I(0, max(self.lo ** n, self.hi ** n))

    def contains0(self):
        return self.lo <= 0 <= self.hi

    def width(self):
        return self.hi - self.lo

    def __repr__(self):
        return f"[{float(self.lo):.6g}, {float(self.hi):.6g}]"


def _taylor(x: Fr, start: int, N: int) -> Fr:
    """sum_{j >= 0, start + 2j <= N} (-1)^j x^(start+2j) / (start+2j)!"""
    s, j = Fr(0), 0
    while start + 2 * j <= N:
        n = start + 2 * j
        s += (-1) ** j * x ** n / factorial(n)
        j += 1
    return s


def cos_q(x, N: int = 60) -> I:
    x = Fr(x)
    s = _taylor(x, 0, N)
    r = abs(x) ** (N + 1) / factorial(N + 1)
    return I(s - r, s + r)


def sin_q(x, N: int = 60) -> I:
    x = Fr(x)
    s = _taylor(x, 1, N)
    r = abs(x) ** (N + 1) / factorial(N + 1)
    return I(s - r, s + r)


def exp_q(x, N: int = 60) -> I:
    x = Fr(x)
    if x < 0:
        return exp_q(-x, N).recip()
    s = sum(x ** j / factorial(j) for j in range(N + 1))
    r = x ** (N + 1) / factorial(N + 1) * 3 ** ceil(x)
    return I(s, s + r)


def exp_i(v: I, N: int = 60) -> I:
    """exp is increasing: enclose exp on an interval by its endpoints."""
    return I(exp_q(v.lo, N).lo, exp_q(v.hi, N).hi)


TAN_HALF = sin_q(Fr(1, 2)) / cos_q(Fr(1, 2))  # tan(1/2) = 0.5463024898...
E = exp_q(1)
COS1 = cos_q(1)


def cayley(a):
    """Rational orthogonal 3x3 matrix Q = (I - S)(I + S)^{-1}, S skew from a = (a1, a2, a3).
    Exact over Fractions; Q^T Q = I is re-checked by the caller."""
    import sympy as sp
    a1, a2, a3 = (sp.Rational(Fr(t).numerator, Fr(t).denominator) for t in a)
    S = sp.Matrix([[0, -a3, a2], [a3, 0, -a1], [-a2, a1, 0]])
    Q = (sp.eye(3) - S) * (sp.eye(3) + S).inv()
    assert sp.simplify(Q.T * Q - sp.eye(3)) == sp.zeros(3, 3)
    return [[Fr(int(sp.fraction(Q[i, j])[0]), int(sp.fraction(Q[i, j])[1])) for j in range(3)]
            for i in range(3)]


def poly_eval(poly, xs):
    """poly: dict {exponent tuple: coefficient (I or rational)}; xs: list of I."""
    tot = I(0)
    for mon, c in poly.items():
        term = I.of(c)
        for xj, e in zip(xs, mon):
            if e:
                term = term * (xj ** e)
        tot = tot + term
    return tot
