"""Mod-p cross-check of C-31 / C-32 (ledger SR-C31, SR-C32) with the 2-jet harness (probe2.py jet2).

applies_to: the seed-0 rational-affine families of ../certificates/corank_exact.py c31 (u_i(theta) =
  alpha_i + B_i theta on S^{d-1}, same seeds), specialized at random theta mod p. [PROBE]: mod p never
  concludes; this is an independent PRIMAL check of the exact DUAL computation in corank_exact.py c31.
  The cells (N, k) = (12, 4) and (13, 3) have the (N, k) of SR-C32 but are the c31 families, not the four
  c32 families.
Run: cd probes && python c31_c32_jet2.py     (validate.py controls must pass first; needs python-flint)
"""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe2 import *          # noqa
from validate import retry, tally_line   # noqa
from fractions import Fraction as Fr

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "certificates"))
import corank_exact as X


def mk_point(alpha, Bi, k):
    def f(th):
        u = []
        for c in range(len(alpha)):
            x = R(alpha[c].numerator, alpha[c].denominator)
            for l in range(k):
                b = int(Bi[c][l])
                if b:
                    x = th[l] * b + x
            u.append(x)
        return sph(u)
    return f


def run():
    cases = [(3, 10, 6), (3, 10, 7), (3, 11, 5), (3, 11, 6), (3, 12, 3), (3, 12, 4), (3, 13, 2), (3, 13, 3)]
    srng = random.Random(3131)
    for (d, N, k) in cases:
        G = d * (d + 1) // 2
        rng = random.Random(31000 + 100 * d + 10 * N + k)       # seed 0 of corank_exact.c31
        alpha, B = X.family(rng, d, N, k)
        pts = [mk_point(alpha[i], B[i], k) for i in range(N)]
        kap = N - (d + 1) * (d + 2) // 2 + 1
        v = retry(jet2, pts, k, d, rng=srng)
        print(f"d={d} N={N} k={k} kappa={kap}: jet2 {v:10s} predicted {X.predict(kap, k, G)}")
        sys.stdout.flush()
    print(tally_line())


if __name__ == "__main__":
    run()
