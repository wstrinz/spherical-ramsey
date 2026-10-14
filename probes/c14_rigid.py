"""Sanity check of C-14 (rigid-group absorption), run after the conjecture was stated;
part B also gives exact certificates for C-23(ii) at n = 9, k = 1.

applies_to: one-parameter circle configurations: rational points plus points circ(r_i(t)) with
  r_i in Q(t) (t transcendental, coordinate field inside Q(t): B = F (x) F embeds in Q(T, U), a
  domain).  No square roots: real, no realness filter.

EXACT non-Ramsey test (the (2,2)-form determinant argument at n = 9; see the note): rows = the nine
(2,2)-monomials x^a y^b (a, b <= 2) at (x_i, y_i) = (r_i(T), r_i(U)) (rational points: (c, c)).
If det != 0 at one rational (T0, U0) with all denominators nonzero and the 9 points distinct there,
det != 0 in Q(T, U), so the only (2,2)-form over B through the 9 pairs is 0, and the circle
criterion (in its (2,2)-form reduction) fails: NON-RAMSEY (exact, given the reviewed circle reduction).
Cross-ratio constancy: EXACT for non-constancy (derivative nonzero at a rational point).
[PROBE]: 2-jet and curve probe (k = 1: full criterion mod p).
usage: python -I c14_rigid.py
"""
import os, sys, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)   # probe2, validate and the sibling scripts live next to this file
from fractions import Fraction
import sympy as sp
from probe2 import *
from validate import retry, tally_line
from c22_controls import make_spec, ev, DualK, pt_fn
from c23_count_law import classify

RATS = [Fraction(0), Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(3, 4), Fraction(-2, 5), Fraction(5, 2)]

def exact_det(specs, rng, tries=40):
    """det of the 9x9 (2,2)-evaluation matrix at a random rational (T0, U0); None if no valid point."""
    assert len(specs) == 9
    for _ in range(tries):
        T0 = Fraction(rng.randint(-60, 60), rng.randint(1, 60)); U0 = Fraction(rng.randint(-60, 60), rng.randint(1, 60))
        try:
            xs = [Fraction(ev(s, [T0])) for s in specs]
            ys = [Fraction(ev(s, [U0])) for s in specs]
        except ZeroDivisionError:
            continue
        if len(set(xs)) < 9 or len(set(ys)) < 9:
            continue
        M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) ** a * sp.Rational(y.numerator, y.denominator) ** b
                        for a in range(3) for b in range(3)] for x, y in zip(xs, ys)])
        return M.det()
    return None

def cr_const(Hspecs, rng):
    """EXACT non-constancy of the cross-ratio of 4 one-parameter points (dual numbers over Q)."""
    for _ in range(3):
        for _ in range(60):
            T0 = Fraction(rng.randint(-50, 50), rng.randint(1, 50))
            try:
                X = [DualK(T0, [1])]
                S = [ev(s, X) for s in Hspecs]
                S = [v if isinstance(v, DualK) else DualK(Fraction(v), [0]) for v in S]
                c = (S[0] - S[2]) * (S[1] - S[3]) / ((S[0] - S[3]) * (S[1] - S[2]))
                break
            except ZeroDivisionError:
                continue
        if c.d[0] != 0:
            return False
    return True

def mob_image_specs(rng):
    """four points nu_t(q_i), nu_t(s) = (t s + 1)/(s + t): a t-dependent Mobius image of rationals.
    With q = a/b: (a t + b)/(b t + a), integer 'mob' coefficients [a, b, b, a]."""
    qs = rng.sample([(a, b) for a in range(-6, 7) for b in range(1, 5) if a != 0 and abs(a) != b], 4)
    return [("mob", 0, [a, b, b, a, 0, 0]) for a, b in qs]

if __name__ == "__main__":
    rng = random.Random(7140)
    srng = random.Random(7141)
    print("== Part A (C-14): 5 rational points + 4 one-parameter points")
    tally = {}; mismatches = []
    cases = [("random", lambda: [make_spec(rng, 1, rng.choice(["mob", "deg2"])) for _ in range(4)])] * 120 + \
            [("Mobius image of rationals (CR constant)", lambda: mob_image_specs(rng))] * 20
    for label, gen in cases:
        H = gen()
        specs = [("rat", q) for q in RATS[:5]] + H
        # C-14's prediction uses the MAXIMAL rational-cross-ratio group G (a constant r_i(t) joins G),
        # i.e. the exact two-group partition test; the naive 4-point CR of H is printed alongside.
        # (Using the naive CR as the prediction instead gives 2 spurious 'mismatches': configurations
        #  with a constant r_i, which are two-group.)
        cl = classify(specs, 1, rng)
        if cl is None:
            continue
        const = cl[1]
        naive = cr_const(H, rng)
        d = exact_det(specs, rng)
        if d is None:
            continue
        pts = [pt_fn(s) for s in specs]
        j = retry(jet2, pts, 1, 2, trials=1, rng=srng)
        c = retry(curve_probe, pts, 1, 2, trials=1, rng=srng)
        pred = "PASS" if const else "FAIL"
        exact = "det!=0 (EXACT NON-RAMSEY)" if d != 0 else "det=0 at point"
        key = (label, "two-group" if const else "not two-group", "naive H-CR const" if naive else "naive H-CR non-const", exact, f"2-jet {j}", f"curve {c}")
        tally[key] = tally.get(key, 0) + 1
        if (const and (j != "PASS" or c != "PASS")) or ((not const) and (c == "PASS" or j == "PASS")):
            mismatches.append((H, const, d, j, c))
    for k_, v in sorted(tally.items(), key=str):
        print("  " + " | ".join(k_) + f": {v}")
    print(f"  C-14 mismatches (not two-group with a PASS, or two-group with a FAIL): {len(mismatches)}")
    for m in mismatches: print("   MISMATCH", m)
    sys.stdout.flush()

    print("== Part B (C-23(ii), n = 9, k = 1): exact determinants on fresh random one-parameter 9-sets")
    tally = {}
    for _ in range(60):
        nrat = rng.randint(0, 3)
        specs = [make_spec(rng, 1, "rat") for _ in range(nrat)] + [make_spec(rng, 1, rng.choice(["mob", "deg2"])) for _ in range(9 - nrat)]
        cl = classify(specs, 1, rng)
        if cl is None: continue
        trd, two = cl
        d = exact_det(specs, rng)
        if d is None: continue
        key = (f"k={trd}", "two-group" if two else "not two-group", "det!=0 EXACT NON-RAMSEY" if d != 0 else "det=0 at point")
        tally[key] = tally.get(key, 0) + 1
    for k_, v in sorted(tally.items(), key=str):
        print("  " + " | ".join(k_) + f": {v}")
    print("  radian 9-gon control: see ../certificates/radian_det.py (det != 0)")
    print(tally_line())
