"""Sanity checks of C-15 (generic Mobius-group unions on S^1) and C-16 (specialization closure
fails on S^2), run after both conjectures were stated.

applies_to:
  C-15: unions of Mobius images nu_k(R_k) of rational circle sets, nu_k(s) = (a s + b)/(s + c) with
    independent transcendental a, b, c (e5_mobius.mob_circle), plus free circle points; by Theorem C
    the first group is taken rational (nu_1 = id).  No square roots: real configurations.
  C-16: points of S^2 with independent stereographic coordinates (e3_sphere.indep_sphere), circle
    points embedded in the great circle z = 0 of S^2, and rational points on that great circle.
[PROBE] only: 2-jet (necessary; full test under C-1) and curve probe (necessary for k >= 2), seeded.
usage: python -I c15_c16.py
"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = HERE   # probe2, validate, e3_sphere, e5_mobius live next to this file
sys.path.insert(0, PROBES)
from probe2 import *
from validate import retry, tally_line, indep_circle
from e3_sphere import indep_sphere
from e5_mobius import mob_circle, rat_s, RQ

def show(name, pts, k, d, expect, srng, curve=True):
    j = retry(jet2, pts, k, d, trials=1, rng=srng)
    c = retry(curve_probe, pts, k, d, trials=1, rng=srng) if curve and len(pts) * (d + 1) ** 2 <= 200 else "-"
    flag = "" if (expect == "?" or j == expect) else "   <== differs from C-15/C-16 prediction"
    print(f"  {name:66s} predict {expect:5s} | 2-jet {j:10s} | curve {c}{flag}")
    sys.stdout.flush()

def free_circle(i):
    return lambda th: circ(th[i])

def lift3(f):
    """a circle point placed on the great circle z = 0 of S^2."""
    return lambda th: f(th) + [0]

if __name__ == "__main__":
    srng = random.Random(7150)
    rats = [rat_circ(*q) for q in RQ]
    print("== C-15: generic Mobius-group unions on S^1 (group 1 rational; nu_2, nu_3 generic; singletons free)")
    G1 = rats[:4]
    G2 = lambda o: [mob_circle(rat_s(*q), o) for q in RQ[4:8]]
    G3 = lambda o, m: [mob_circle(rat_s(*q), o) for q in RQ[8:8 + m]]
    show("(4,4)        two rigid groups", G1 + G2(0), 3, 2, "PASS", srng)
    show("(4) + 3 free  one rigid + 3", G1 + [free_circle(i) for i in range(3)], 3, 2, "PASS", srng)
    show("(4) + 4 free  = PD (4,4)", G1 + [free_circle(i) for i in range(4)], 4, 2, "FAIL", srng)
    show("(4,4,1)", G1 + G2(0) + [free_circle(3)], 4, 2, "FAIL", srng)
    show("(4,4,2)", G1 + G2(0) + [free_circle(3), free_circle(4)], 5, 2, "FAIL", srng)
    show("(4,4,3)", G1 + G2(0) + [free_circle(3 + i) for i in range(3)], 6, 2, "FAIL", srng)
    show("(4,4,4)", G1 + G2(0) + G3(3, 4), 6, 2, "FAIL", srng)
    show("(4,4,4) with group 1 also generic", [mob_circle(rat_s(*q), 0) for q in RQ[:4]] + G2(3) + G3(6, 4), 9, 2, "FAIL", srng)
    show("(5,4,1)      (C-14 covers)", rats[:5] + G2(0) + [free_circle(3)], 4, 2, "FAIL", srng)
    show("(4,3,3) = rigid 4 + 6 generic points (via groups of 3)", G1 + G3(0, 3) + [mob_circle(rat_s(*q), 3) for q in RQ[11:14]], 6, 2, "FAIL", srng)
    show("(3,3) + 0 = two non-rigid groups (6 pts)", [mob_circle(rat_s(*q), 0) for q in RQ[:3]] + [mob_circle(rat_s(*q), 3) for q in RQ[3:6]], 6, 2, "PASS", srng)

    print("== C-16: S^2, seven points")
    show("7 generic points on S^2 (k = 14)", indep_sphere(7, 3), 14, 3, "PASS", srng)
    show("7 independent points on a great circle of S^2 (k = 7)", [lift3(free_circle(i)) for i in range(7)], 7, 3, "FAIL", srng)
    show("3 rational on the great circle + 4 free on S^2 (k = 8)", [lift3(r) for r in rats[:3]] + [(lambda i: (lambda th: sph(th[2*i:2*i+2])))(i) for i in range(4)], 8, 3, "PASS", srng)
    show("3 rational + 4 independent, all on the great circle (k = 4)", [lift3(r) for r in rats[:3]] + [lift3(free_circle(i)) for i in range(4)], 4, 3, "FAIL", srng)
    show("8 generic points on S^2 (k = 16)", indep_sphere(8, 3), 16, 3, "PASS", srng, curve=False)
    show("9 generic points on S^2 (k = 18)", indep_sphere(9, 3), 18, 3, "PASS", srng, curve=False)
    print(tally_line())
