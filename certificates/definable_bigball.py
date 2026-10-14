"""Exact monochromatic-big-ball certificates for definable colourings.

applies_to: colourings of R^D that are any function of the sign vector (sgn g_1, ..., sgn g_s) of
finitely many real polynomials (coefficients in Q[tan(1/2), e, cos 1]), plus one R_exp instance;
D = 2..4. The certificate is exact (Fraction interval arithmetic, `exact_intervals`), not numeric.

Tests C-25 (definable Graham; filed before this probe): in every o-minimal colouring
some class contains a ball of every radius. The leading-form derivation (ii) is exercised directly:
pick an integer direction w with g_i,top(w) != 0 for all i (certified), then for R large the box
R*w + [-1, 1]^D (which contains the unit disc centred at R*w, hence the explicit copy
x_k = R*w + (cos k, sin k, 0, ...) of E_1) has every g_i bounded away from 0 (certified).

Run (from any directory):  python3 -I definable_bigball.py   (prints the log; expected/definable_bigball.log)
"""
from __future__ import annotations

import itertools
import os
import random
from fractions import Fraction as Fr
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # sibling imports under python -I

from exact_intervals import COS1, E, TAN_HALF, I, cos_q, exp_i, poly_eval, sin_q

PARAMS = {"1": I(1), "tan(1/2)": TAN_HALF, "e": E, "cos 1": COS1}


def rand_poly(rng, D, deg, nterms):
    mons = [m for m in itertools.product(range(deg + 1), repeat=D) if sum(m) <= deg]
    top = [m for m in mons if sum(m) == deg]
    chosen = set(rng.sample(mons, min(nterms, len(mons)))) | {rng.choice(top)}
    poly, desc = {}, []
    for m in sorted(chosen):
        c = rng.choice([x for x in range(-5, 6) if x])
        pname = rng.choice(list(PARAMS))
        poly[m] = PARAMS[pname] * c
        desc.append(f"{c}*{pname}*x^{m}")
    return poly, " + ".join(desc)


def top_form(poly):
    d = max(sum(m) for m in poly)
    return {m: c for m, c in poly.items() if sum(m) == d}


def directions(D, B=3):
    vs = [v for v in itertools.product(range(-B, B + 1), repeat=D) if any(v)]
    vs.sort(key=lambda v: (sum(t * t for t in v), v))
    return vs


def certify_semialgebraic(polys, D):
    tops = [top_form(p) for p in polys]
    for w in directions(D):
        wi = [I(t) for t in w]
        if any(poly_eval(t, wi).contains0() for t in tops):
            continue
        for m in range(1, 40):
            R = 2 ** m
            box = [I(R * t - 1, R * t + 1) for t in w]
            vals = [poly_eval(p, box) for p in polys]
            if not any(v.contains0() for v in vals):
                return w, R, vals
        return w, None, None
    return None, None, None


def copy_points(w, R, D):
    pts = []
    for k in range(9):
        x = [I(R * t) for t in w]
        x[0] = x[0] + cos_q(k)
        x[1] = x[1] + sin_q(k)
        pts.append(x)
    return pts


def main():
    out = []
    say = out.append
    rng = random.Random(20261013)
    ok = 0
    cases = []
    for D in (2, 3, 4):
        for _ in range(10):
            s = rng.choice([1, 2, 3])
            cases.append((D, [rand_poly(rng, D, rng.choice([1, 2, 3, 4]), rng.choice([2, 4, 6]))
                              for _ in range(s)]))
    # hand-picked: top forms with many zero directions
    x2 = {(1, 0): I(1), (0, 1): -TAN_HALF}            # x - tan(1/2) y
    lines = {(0, 0): I(0)}
    import sympy as sp
    X, Y = sp.symbols("x y")
    expr = sp.expand(sp.prod([(X - k * Y) for k in range(-3, 4)]) - 1)
    lines = {m: I(Fr(int(c))) for m, c in sp.Poly(expr, X, Y).terms()}
    cases.append((2, [(x2, "x - tan(1/2)*y"), (lines, "prod_{k=-3..3}(x - k y) - 1")]))
    for idx, (D, polys) in enumerate(cases):
        w, R, vals = certify_semialgebraic([p for p, _ in polys], D)
        say(f"case {idx:2d}  D={D}  s={len(polys)}")
        for _, d in polys:
            say(f"    g = {d}")
        if R is None:
            say(f"    NO CERTIFICATE (direction {w})")
            continue
        pts = copy_points(w, R, D)
        signs = []
        for p, _ in polys:
            sv = set()
            for x in pts:
                v = poly_eval(p, x)
                assert not v.contains0()
                sv.add(1 if v.lo > 0 else -1)
            assert len(sv) == 1
            signs.append(sv.pop())
        box_signs = [1 if v.lo > 0 else -1 for v in vals]
        assert box_signs == signs
        ok += 1
        say(f"    CERTIFIED: box {R}*{w} + [-1,1]^{D} has constant signs {signs}; "
            f"E_1 copy x_k = {R}*{w} + (cos k, sin k, 0..) monochromatic")
    # R_exp instance (derivation (i) existence; certificate still exact)
    say("R_exp case: g1 = exp(x) - tan(1/2)*y^3 + 2xy - e ;  g2 = exp(y) - cos(1)*x^2")

    def g1(x, y):
        return exp_i(x) - TAN_HALF * y ** 3 + 2 * x * y - E

    def g2(x, y):
        return exp_i(y) - COS1 * x ** 2

    found = None
    for w in directions(2):
        for m in range(1, 8):
            R = 2 ** m
            bx, by = I(R * w[0] - 1, R * w[0] + 1), I(R * w[1] - 1, R * w[1] + 1)
            v1, v2 = g1(bx, by), g2(bx, by)
            if not v1.contains0() and not v2.contains0():
                found = (w, R, v1, v2)
                break
        if found:
            break
    if found:
        w, R, v1, v2 = found
        say(f"    CERTIFIED: box {R}*{w} + [-1,1]^2: g1 in {v1}, g2 in {v2} (constant signs)")
        ok += 1
    else:
        say("    NO CERTIFICATE")
    say(f"SUMMARY: {ok}/{len(cases) + 1} colourings certified to contain a monochromatic radius-1 "
        f"ball and an explicit monochromatic copy of E_1")
    text = "\n".join(out) + "\n"
    print(text, end="")


if __name__ == "__main__":
    main()
