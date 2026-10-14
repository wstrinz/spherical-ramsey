"""Falsification test of the 'rank-N' sketch for C-23(i), k = 1 (filed as C-24 before the radian /
random runs below were cited; the heptagon test is the sketch's own falsifier).

Sketch (C-24): A on the unit circle, coordinate field F of transcendence degree 1 with derivation
delta = d/dt, stereographic parameters s_i in F, velocities delta_i = delta(s_i).  Let N be the n x 8
matrix with rows (delta_i, delta_i s_i, delta_i s_i^2, 1, s_i, s_i^2, s_i^3, s_i^4).  If n <= 8 and
rank_F N = n, then A is Ramsey.

applies_to: one-parameter circle configurations (rational functions of t, or Palvolgyi's heptagon with
  its square roots, evaluated numerically).

Tests:
  (1) FALSIFIER: Palvolgyi's heptagon (non-Ramsey, arXiv:2609.23327; 2-jet FAIL in validate.py).  The
      sketch predicts rank N < 7.  Numerical (mpmath, 50 digits) singular values at several r.
      rank N = 7 here would REFUTE the sketch.
  (2) EXACT ranks (sympy, one rational t; full rank at a point => full generic rank): radian 7- and
      8-gons; W7, W8 (cert_nontwogroup.py); and controls.
usage (from any directory): python3 -I rankN_check.py
"""
import sympy as sp
import mpmath as mp

t = sp.symbols("t")

def N_rows(ss):
    rows = []
    for s in ss:
        d = sp.diff(s, t)
        rows.append([d, d * s, d * s ** 2, 1, s, s ** 2, s ** 3, s ** 4])
    return sp.Matrix(rows)

def exact_rank_at(ss, t0):
    M = N_rows(ss).subs(t, t0)
    return M.rank()

def tan_mult(k):
    s = sp.Integer(0)
    for _ in range(k):
        s = sp.cancel((s + t) / (1 - s * t))
    return s

def heptagon_params():
    """Palvolgyi's heptagon (validate.palv): (-1, 0) and ((j - r)/r, +-sqrt(j(2r - j))/r), j = 1, 3, 4.
    Stereographic projection from (1, 0) (a rational rotation of the standard pole): s = y / (1 - x)."""
    r = t
    ss = [sp.Integer(0)]          # (-1, 0) -> s = 0
    for j in (1, 3, 4):
        x = (j - r) / r
        for sg in (1, -1):
            y = sg * sp.sqrt(j * (2 * r - j)) / r
            ss.append(sp.simplify(y / (1 - x)))
    return ss

if __name__ == "__main__":
    mp.mp.dps = 50
    print("== (1) FALSIFIER: Palvolgyi heptagon (known non-Ramsey).  Sketch predicts rank N < 7.")
    ss = heptagon_params()
    print("   stereographic parameters:", [str(s) for s in ss])
    Nsym = N_rows(ss)
    for r0 in (sp.Rational(7, 2) + sp.Rational(1, 3), sp.Integer(5), sp.Rational(23, 3), sp.Integer(11)):
        M = mp.matrix([[mp.mpf(sp.N(e.subs(t, r0), 60)) for e in row] for row in Nsym.tolist()])
        sv = mp.svd_r(M, compute_uv=False)
        svs = sorted([float(x) for x in sv], reverse=True)
        print(f"   r = {r0}: singular values {['%.3e' % x for x in svs]}  (numerical rank {sum(1 for x in svs if x > 1e-30 * svs[0])})")
    print("== (1b) EXACT (from the cold review): every heptagon point satisfies delta_i = -s_i (1 + s_i^2) / (2r),")
    print("        so (1,0,0,0,-c,0,-c,0) and (0,1,0,0,0,-c,0,-c), c = -1/(2r), lie in ker N: rank N <= 6 for every r.")
    ident = [sp.simplify(sp.diff(s_, t) + s_ * (1 + s_ ** 2) / (2 * t)) for s_ in ss]
    print("   identity residuals:", ident, "=> all zero:", all(e == 0 for e in ident))
    c = -1 / (2 * t)
    k1 = sp.Matrix([1, 0, 0, 0, -c, 0, -c, 0]); k2 = sp.Matrix([0, 1, 0, 0, 0, -c, 0, -c])
    print("   N k1 == 0:", all(sp.simplify(e) == 0 for e in Nsym * k1), "; N k2 == 0:", all(sp.simplify(e) == 0 for e in Nsym * k2))
    print("== (2) exact ranks at a rational point (full rank there => full rank over Q(t))")
    cases = {
        "radian 7-gon": [tan_mult(k) for k in range(7)],
        "radian 8-gon (C-10)": [tan_mult(k) for k in range(8)],
        "radian 9-gon (control: n = 9 > 8, sketch silent)": [tan_mult(k) for k in range(9)],
        "W7 (exact Ramsey cert exists)": [0, sp.Rational(1, 2), sp.Rational(1, 3), t, t + 1, 2 * t, 1 / t],
        "W8 (exact Ramsey cert exists)": [0, sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3), t, t + 1, 2 * t, 1 / t],
        "control: 4 rat + t, t+1, t+2, t+3 (two-group)": [0, sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3), t, t + 1, t + 2, t + 3],
        "control: 3 rat + 4 'independent' (n/a: k = 4)": None,
    }
    for name, ss in cases.items():
        if ss is None:
            print(f"   {name}"); continue
        ss = [sp.sympify(s) for s in ss]
        ranks = [exact_rank_at(ss, t0) for t0 in (sp.Rational(2, 7), sp.Rational(-5, 11))]
        print(f"   {name:50s} n = {len(ss)}  exact rank N at t = 2/7, -5/11: {ranks}")
