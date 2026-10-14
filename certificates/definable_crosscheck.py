"""Independent cross-check of `definable_polyphase.py` Part B certificates.

applies_to: the output log of `definable_polyphase.py` only. It re-parses each certified copy (P, r,
centre c, Cayley parameters a, colour j) and recomputes everything without `exact_intervals`:
- Q via sympy rationals, with Q^T Q = I checked exactly;
- the copy's pairwise distances against E_1's, |x_i - x_j|^2 = 2 - 2 cos(i - j), at 60 digits;
- P(x_k) at 60 digits (mpmath), and that frac(P(x_k)) lies in [j/r, (j+1)/r) with margin > 1e-40.
This is a consistency check of the exact certificate, not a replacement for it.

Run (from any directory):  python3 -I definable_crosscheck.py [LOG]
LOG defaults to expected/definable_polyphase.log next to this script (the shipped output of definable_polyphase.py).
"""
from __future__ import annotations

import ast
import os
import re
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 60


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                             "expected", "definable_polyphase.log")
    lines = open(path, encoding="utf-8").read().splitlines()
    n_ok = 0
    for i, ln in enumerate(lines):
        m = re.match(r"r=(\d) seed#\s*(\d+)\s+P = (.*)$", ln)
        if not m:
            continue
        r = int(m.group(1))
        terms = m.group(3).split(" + ")
        cert = lines[i + 1]
        mm = re.search(r"colour (\d+): c = (\[.*?\]), Cayley a = (\[.*?\])", cert)
        assert mm, cert
        j = int(mm.group(1))
        c = [sp.Rational(t) for t in ast.literal_eval(mm.group(2))]
        a = [sp.Rational(t) for t in ast.literal_eval(mm.group(3))]
        S = sp.Matrix([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
        Q = (sp.eye(3) - S) * (sp.eye(3) + S).inv()
        assert Q.T * Q == sp.eye(3)
        tau = mp.tan(mp.mpf(1) / 2)
        poly = []
        for t in terms:
            tm = re.match(r"(-?\d+)(\*tan\(1/2\))?\*x\^(\(.*\))", t)
            coef = int(tm.group(1)) * (tau if tm.group(2) else 1)
            poly.append((coef, ast.literal_eval(tm.group(3))))
        pts = []
        for k in range(9):
            v = [mp.mpf(sp.Rational(c[q]).p) / sp.Rational(c[q]).q
                 + mp.mpf(Q[q, 0].p) / Q[q, 0].q * mp.cos(k) + mp.mpf(Q[q, 1].p) / Q[q, 1].q * mp.sin(k)
                 for q in range(3)]
            pts.append(v)
        for p in range(9):
            for q in range(p + 1, 9):
                d2 = sum((pts[p][t] - pts[q][t]) ** 2 for t in range(3))
                assert abs(d2 - (2 - 2 * mp.cos(p - q))) < mp.mpf(10) ** -50
        for v in pts:
            val = sum(co * v[0] ** e[0] * v[1] ** e[1] * v[2] ** e[2] for co, e in poly)
            fr = val - mp.floor(val)
            assert mp.mpf(j) / r + mp.mpf(10) ** -40 < fr < mp.mpf(j + 1) / r - mp.mpf(10) ** -40
        n_ok += 1
    print(f"crosscheck: {n_ok} certified copies re-verified independently (60-digit mpmath, exact Q)")
    assert n_ok == 30


if __name__ == "__main__":
    main()
