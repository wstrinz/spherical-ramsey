"""Sweep for C-24 (filed before this run): full-rank N must never come with a FAIL of the full
one-parameter criterion (curve probe, k = 1, mod p).

applies_to: random one-parameter circle configurations, n = 6, 7, 8: rational points plus
  circ((a t + b)/(c t + d)) or degree-2 rational functions of t; and mirror-symmetric sets
  {0, +-r_1(t), +-r_2(t), +-r_3(t)}.  No square roots (real; no realness filter needed).
EXACT: rank of N at a random rational t0 (a lower bound for the rank over Q(t); full rank at t0 =>
full rank).  [PROBE]: curve probe (full criterion mod p for k = 1), seeded.
usage (from any directory): python3 -I rankN_sweep.py
  imports probe2, validate, c22_controls and c23_count_law (and through them c13_c22_seven) from ../probes
"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "probes"))
sys.path.insert(0, HERE)
from fractions import Fraction
import sympy as sp
from probe2 import *
from validate import retry, tally_line
from c22_controls import make_spec, ev, pt_fn
from c23_count_law import mirror_specs

t = sp.symbols("t")

def sym(spec):
    if spec[0] == "rat":
        q = spec[1]; return sp.Rational(q.numerator, q.denominator)
    if spec[0] == "mob":
        c = spec[2]; return (c[0] * t + c[1]) / (c[2] * t + c[3])
    c = spec[2]
    den = (c[3] * t + c[4]) if (c[3] or c[4]) else 1
    return (c[0] * t * t + c[1] * t + c[2]) / den

def rankN(specs, rng):
    ss = [sp.sympify(sym(s)) for s in specs]
    rows = [[sp.diff(s, t), sp.diff(s, t) * s, sp.diff(s, t) * s ** 2, 1, s, s ** 2, s ** 3, s ** 4] for s in ss]
    M = sp.Matrix(rows)
    for _ in range(20):
        t0 = sp.Rational(rng.randint(-60, 60), rng.randint(1, 60))
        vals = [s.subs(t, t0) for s in ss]
        if any(v.has(sp.zoo) or v.has(sp.nan) for v in vals) or len(set(vals)) < len(ss):
            continue
        try:
            return M.subs(t, t0).rank()
        except Exception:
            continue
    return None

if __name__ == "__main__":
    rng = random.Random(7240); srng = random.Random(7241)
    tally = {}; bad = []
    def gen(n):
        nrat = rng.randint(0, 3)
        return [make_spec(rng, 1, "rat") for _ in range(nrat)] + [make_spec(rng, 1, rng.choice(["mob", "deg2"])) for _ in range(n - nrat)]
    plan = [("random", 6, 30), ("random", 7, 60), ("random", 8, 60), ("mirror", 7, 40)]
    for kind, n, count in plan:
        for _ in range(count):
            specs = mirror_specs(rng) if kind == "mirror" else gen(n)
            rk = rankN(specs, rng)
            if rk is None: continue
            pts = [pt_fn(s) for s in specs]
            c = retry(curve_probe, pts, 1, 2, trials=1, rng=srng)
            full = (rk == len(specs))
            key = (kind, f"n={len(specs)}", "N full rank" if full else f"N rank {rk}", f"curve {c}")
            tally[key] = tally.get(key, 0) + 1
            if full and c != "PASS":
                bad.append((specs, rk, c))
    for k_, v in sorted(tally.items()):
        print("  " + " | ".join(k_) + f": {v}")
    print(f"C-24 violations (full-rank N with a non-PASS full criterion): {len(bad)}")
    for b in bad: print("  VIOLATION", b)
    print(tally_line())
