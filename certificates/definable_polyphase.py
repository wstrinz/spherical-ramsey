"""Polynomial-phase colourings and the radian 9-gon E_1.

applies_to: Part A, any quartic that is diagonal on a 5-dim coordinate block (exact sympy identity);
Part B, polynomial-phase colourings chi(x) = floor(r * frac(P(x))) of R^3 with deg P <= 3 and
coefficients in Z[tan(1/2)] (exact Fraction-interval certificates, `exact_intervals`).

Part A (an instance of C-26, polynomial-factor Graham): on V = span(u, v) in R^5 with
(u_i, v_i) = sqrt(2/5) (cos 2 pi i/5, sin 2 pi i/5), u and v are orthonormal and
sum x_i^4 restricted to the unit circle of V is the constant 3/10 (a 5-point circle 4-design).
So P = sum_{i<=5} x_i^4 + tan(1/2) (x_6^3 + x_1 x_6 x_7) + e x_8 is constant on that circle, and
any colouring f(P) is constant on the copy {u cos k + v sin k} of E_1.

Part B (C-27, a working hypothesis filed before this probe): for seeded random P,
search over copies x_k = c + Q (cos k, sin k, 0) with c in (1/100) Z^3 and Q a rational
orthogonal matrix (Cayley transform of a rational skew matrix), screen in floating point, then
CERTIFY exactly: every P(x_k) lies strictly inside one window [j/r, (j+1)/r) + Z, using rational
enclosures of cos k, sin k, tan(1/2). Floating point only proposes; only the exact check counts.

Run (from any directory):  python3 -I definable_polyphase.py   (prints the log; expected/definable_polyphase.log,
which definable_crosscheck.py re-verifies)
"""
from __future__ import annotations

import itertools
import math
import os
import random
from fractions import Fraction as Fr

import numpy as np
import sympy as sp
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # sibling imports under python -I

from exact_intervals import TAN_HALF, I, cayley, cos_q, poly_eval, sin_q


def part_a(say):
    t = sp.symbols("t", real=True)
    C, S = sp.symbols("C S")
    rho = sp.sqrt(sp.Rational(2, 5))
    u = [rho * sp.cos(2 * sp.pi * i / 5) for i in range(5)]
    v = [rho * sp.sin(2 * sp.pi * i / 5) for i in range(5)]
    uu = sp.nsimplify(sp.simplify(sum(a * a for a in u)))
    vv = sp.nsimplify(sp.simplify(sum(b * b for b in v)))
    uv = sp.simplify(sum(a * b for a, b in zip(u, v)))
    q = sp.expand(sum((a * C + b * S) ** 4 for a, b in zip(u, v)) - sp.Rational(3, 10) * (C**2 + S**2) ** 2)
    coeffs = sp.Poly(q, C, S).coeffs()
    zero = all(sp.simplify(sp.radsimp(sp.expand(c.rewrite(sp.sqrt)))) == 0 for c in coeffs)
    say(f"Part A: |u|^2 = {uu}, |v|^2 = {vv}, u.v = {uv}; "
        f"sum (u_i C + v_i S)^4 - 3/10 (C^2+S^2)^2 == 0 coefficientwise: {zero}")
    assert uu == 1 and vv == 1 and uv == 0 and zero
    say("Part A: P = sum_{i<=5} x_i^4 + tan(1/2)(x_6^3 + x_1 x_6 x_7) + e x_8 equals 3/10 on the "
        "unit circle of V = span(u, v) (the extra terms vanish on V, which lies in span(e_1..e_5)); "
        "every colouring f(P) is constant on the E_1 copy {u cos k + v sin k : k = 0..8}. CHECKED")


MONS3 = [m for m in itertools.product(range(4), repeat=3) if sum(m) <= 3]


def rand_P(rng):
    mons = rng.sample(MONS3, rng.choice([4, 6, 8]))
    if not any(sum(m) == 3 for m in mons):
        mons.append(rng.choice([m for m in MONS3 if sum(m) == 3]))
    poly, desc, used_tau = {}, [], False
    for i, m in enumerate(sorted(mons)):
        c = rng.choice([-3, -2, -1, 1, 2, 3])
        tau = rng.random() < 0.5 or (i == len(mons) - 1 and not used_tau)
        used_tau |= tau
        poly[m] = (TAN_HALF if tau else I(1)) * c
        desc.append(f"{c}{'*tan(1/2)' if tau else ''}*x^{m}")
    fpoly = {m: float(c.lo) for m, c in poly.items()}
    return poly, fpoly, " + ".join(desc)


def cayley_np(a):
    a1, a2, a3 = a[..., 0], a[..., 1], a[..., 2]
    n = a.shape[0]
    Sm = np.zeros((n, 3, 3))
    Sm[:, 0, 1], Sm[:, 0, 2], Sm[:, 1, 0] = -a3, a2, a3
    Sm[:, 1, 2], Sm[:, 2, 0], Sm[:, 2, 1] = -a1, -a2, a1
    Id = np.broadcast_to(np.eye(3), (n, 3, 3))
    return (Id - Sm) @ np.linalg.inv(Id + Sm)


def screen(fpoly, r, nprng, n=200000):
    num = nprng.integers(-20, 21, size=(n, 3))
    den = nprng.integers(1, 11, size=(n, 3))
    a = num / den
    cn = nprng.integers(-300, 301, size=(n, 3))
    c = cn / 100.0
    Q = cayley_np(a)
    k = np.arange(9)
    circ = np.stack([np.cos(k), np.sin(k), np.zeros(9)], axis=0)  # 3 x 9
    X = c[:, :, None] + Q @ circ  # n x 3 x 9
    val = np.zeros((n, 9))
    for m, co in fpoly.items():
        val += co * X[:, 0, :] ** m[0] * X[:, 1, :] ** m[1] * X[:, 2, :] ** m[2]
    fr = val - np.floor(val)
    win = np.floor(fr * r)
    same = (win == win[:, :1]).all(axis=1)
    lo = win[:, :1] / r
    margin = np.minimum(fr - lo, lo + 1.0 / r - fr).min(axis=1)
    margin[~same] = -1
    order = np.argsort(-margin)[:20]
    return [(margin[i], [Fr(int(num[i, j]), int(den[i, j])) for j in range(3)],
             [Fr(int(cn[i, j]), 100) for j in range(3)]) for i in order if margin[i] > 0]


def certify(poly, r, a, c):
    Q = cayley(a)
    pts = []
    for k in range(9):
        ck, sk = cos_q(k), sin_q(k)
        pts.append([I(c[i]) + Q[i][0] * ck + Q[i][1] * sk for i in range(3)])
    js = set()
    for x in pts:
        v = poly_eval(poly, x)
        n = math.floor(v.lo)
        if math.floor(v.hi) != n:
            return None
        lo, hi = v.lo - n, v.hi - n
        j = math.floor(lo * r)
        # strictly inside the half-open window [j/r, (j+1)/r)
        if not (Fr(j, r) < lo and hi < Fr(j + 1, r)):
            return None
        js.add(j)
    return js.pop() if len(js) == 1 else None


def part_b(say):
    rng = random.Random(20261013)
    nprng = np.random.default_rng(20261013)
    tally = {}
    for r in (2, 3):
        for s in range(15):
            poly, fpoly, desc = rand_P(rng)
            cands = screen(fpoly, r, nprng)
            res = None
            for margin, a, c in cands:
                j = certify(poly, r, a, c)
                if j is not None:
                    res = (margin, a, c, j)
                    break
            tally[(r, res is not None)] = tally.get((r, res is not None), 0) + 1
            say(f"r={r} seed#{s:2d}  P = {desc}")
            if res:
                margin, a, c, j = res
                say(f"    CERTIFIED monochromatic E_1 copy, colour {j}: c = {[str(t) for t in c]}, "
                    f"Cayley a = {[str(t) for t in a]} (float margin {margin:.3g}); "
                    f"{len(cands)} screened candidates")
            else:
                say(f"    no certified copy ({len(cands)} screened candidates)")
    for r in (2, 3):
        say(f"SUMMARY r={r}: certified {tally.get((r, True), 0)}/15, "
            f"uncertified {tally.get((r, False), 0)}/15")


def main():
    out = []
    say = out.append
    part_a(say)
    part_b(say)
    text = "\n".join(out) + "\n"
    print(text, end="")


if __name__ == "__main__":
    main()
