# applies_to: Vahlen normal-form identities (V0)-(V3), G2' vanishing and the [I] interpolation in Cl_{0,n} for any n, with an independent blade-sign table, exact Fractions, and inverses by linear solve; plus a float coverage test of the normal form. Author: an independent AI reviewer (Claude Opus). Cross-check for cert_clifford.py.
"""Independent spot checks of cert_clifford.py (own Clifford implementation; exact Fractions + numpy coverage test).
The exact checks are check_dim(n); coverage_test(n) is a floating-point test of the normal form (evidence only).
Run (from any directory):  python3 -I cert_clifford_crosscheck.py"""
import itertools
import random
import sys
from fractions import Fraction as Fr

import numpy as np
DBG=False


class Cl:
    """Cl_{0,k}: blades as bitmasks; e_i^2 = -1."""

    def __init__(self, k):
        self.k, self.dim = k, 1 << k
        self.tab = {}
        for A in range(self.dim):
            for B in range(self.dim):
                # sign: count swaps moving each bit of B past higher bits of A, then squares
                s = 0
                for i in range(k):
                    if B >> i & 1:
                        s += bin(A >> (i + 1)).count("1")
                s += bin(A & B).count("1")  # e_i e_i = -1
                self.tab[A, B] = (-1 if s % 2 else 1, A ^ B)
        g = [bin(A).count("1") for A in range(self.dim)]
        self.rev = [(-1) ** (r * (r - 1) // 2) for r in g]
        self.hat = [(-1) ** r for r in g]
        self.pidx = [0] + [1 << i for i in range(k)]

    def mul(self, a, b):
        out = [Fr(0)] * self.dim
        for A, x in enumerate(a):
            if x == 0:
                continue
            for B, y in enumerate(b):
                if y == 0:
                    continue
                s, C = self.tab[A, B]
                out[C] += s * x * y
        return out

    def mm(self, *xs):
        r = xs[0]
        for x in xs[1:]:
            r = self.mul(r, x)
        return r

    def R(self, a): return [s * x for s, x in zip(self.rev, a)]
    def H(self, a): return [s * x for s, x in zip(self.hat, a)]
    def C(self, a): return self.R(self.H(a))
    def add(self, a, b): return [x + y for x, y in zip(a, b)]
    def sub(self, a, b): return [x - y for x, y in zip(a, b)]
    def sm(self, c, a): return [c * x for x in a]
    def sc(self, c): return [Fr(c)] + [Fr(0)] * (self.dim - 1)

    def para(self, v):
        o = [Fr(0)] * self.dim
        for i, c in zip(self.pidx, v):
            o[i] = Fr(c)
        return o

    def ispara(self, a): return all(x == 0 for i, x in enumerate(a) if i not in self.pidx)
    def isscal(self, a): return all(x == 0 for x in a[1:])
    def pc(self, a): return [a[i] for i in self.pidx]

    def inv_honest(self, a):
        """inverse by solving the left-multiplication linear system (no norm formula used)"""
        import sympy as sp
        M = sp.zeros(self.dim, self.dim)
        for B in range(self.dim):
            eB = [Fr(0)] * self.dim
            eB[B] = Fr(1)
            col = self.mul(a, eB)
            for i in range(self.dim):
                M[i, B] = sp.Rational(col[i].numerator, col[i].denominator)
        rhs = sp.zeros(self.dim, 1)
        rhs[0] = 1
        sol = M.LUsolve(rhs)
        return [Fr(int(sp.numer(z)), int(sp.denom(z))) for z in sol]


rng = random.Random(4242)
rq = lambda: Fr(rng.randint(-9, 9), rng.randint(1, 5))


def rpara(n):
    v = [rq() for _ in range(n)]
    while all(x == 0 for x in v):
        v = [rq() for _ in range(n)]
    return v


def normal_form(A, n, m):
    ps = [A.para(rpara(n)) for _ in range(m)]
    w = A.mm(*ps) if m else A.sc(1)
    lam = Fr(0)
    while lam == 0:
        lam = rq()
    p, q = A.para(rpara(n)), A.para(rpara(n))
    wh = A.H(w)
    N = (A.mul(q, wh), A.add(A.sm(lam, w), A.mm(q, wh, p)), wh, A.mul(wh, p))
    return dict(ps=ps, w=w, lam=lam, p=p, q=q, N=N)


def adj(A, N):
    a, b, c, d = N
    return (A.R(d), A.sm(-1, A.R(b)), A.sm(-1, A.R(c)), A.R(a))


def matmul(A, X, Y):
    a, b, c, d = X
    e, f, g, h = Y
    return (A.add(A.mul(a, e), A.mul(b, g)), A.add(A.mul(a, f), A.mul(b, h)),
            A.add(A.mul(c, e), A.mul(d, g)), A.add(A.mul(c, f), A.mul(d, h)))


def nu_honest(A, nf, t):
    w, lam, p, q = nf["w"], nf["lam"], nf["p"], nf["q"]
    X = A.add(q, A.sm(lam, A.mm(w, A.inv_honest(A.add(t, p)), A.inv_honest(A.H(w)))))
    return X


def check_dim(n):
    k = n - 1
    A = Cl(k)
    m = 2 * (n // 2)
    out = {}
    nf = normal_form(A, n, m)
    w, lam, N = nf["w"], nf["lam"], nf["N"]
    nw = A.mul(w, A.C(w))
    out["V0"] = A.isscal(nw) and all(A.mul(*pr) == nw for pr in ((A.C(w), w), (A.H(w), A.R(w)), (A.R(w), A.H(w))))
    s = A.para(rpara(n))
    out["V0'"] = A.ispara(A.mm(w, s, A.R(w)))
    t = A.sub(s, nf["p"])
    a, b, c, d = N
    u = A.add(A.mul(c, t), d)
    nn = A.mul(u, A.C(u))
    out["V1"] = A.isscal(nn) and A.mul(A.C(u), u) == nn
    Xt = A.mul(A.add(A.mul(a, t), b), A.C(u))
    out["V2"] = A.ispara(Xt) and A.sm(1 / nn[0], Xt) == nu_honest(A, nf, t)
    D = -lam * nw[0]
    I2 = (A.sc(D), A.sc(0), A.sc(0), A.sc(D))
    out["V3"] = matmul(A, adj(A, N), N) == I2 and matmul(A, N, adj(A, N)) == I2
    # G2' instance: mu = N_R adj(N_L), points by honest inverses, h(X, Y) = Y c X + Y d - a X - b = 0
    nfR = normal_form(A, n, m)
    mu = matmul(A, nfR["N"], adj(A, N))
    ok = True
    for _ in range(3):
        tt = A.para(rpara(n))
        X, Y = nu_honest(A, nf, tt), nu_honest(A, nfR, tt)
        ma, mb, mc, md = mu
        h = A.sub(A.add(A.mm(Y, mc, X), A.mul(Y, md)), A.add(A.mul(ma, X), mb))
        ok = ok and A.ispara(X) and A.ispara(Y) and all(z == 0 for z in h)
    out["G2'-inst"] = ok
    # [I] at this instance: f(x,y) = Re(h1 conj h2) is in span b(x) (x) b(y): interpolate M, test on fresh points
    nfL2, nfR2 = normal_form(A, n, m), normal_form(A, n, m)
    mu2 = matmul(A, nfR2["N"], adj(A, nfL2["N"]))

    def hf(mu_, x, y):
        a_, b_, c_, d_ = mu_
        return A.sub(A.add(A.mm(y, c_, x), A.mul(y, d_)), A.add(A.mul(a_, x), b_))

    def f(x, y):
        return A.mul(hf(mu, x, y), A.C(hf(mu2, x, y)))[0]

    def bvec(v):
        return [Fr(1)] + list(v) + [sum(z * z for z in v)]

    import sympy as sp
    NQ = n + 2
    while True:
        xs = [rpara(n) for _ in range(NQ)]
        Bx = sp.Matrix([[sp.Rational(z.numerator, z.denominator) for z in bvec(v)] for v in xs])
        if Bx.det() != 0:
            break
    while True:
        ys = [rpara(n) for _ in range(NQ)]
        By = sp.Matrix([[sp.Rational(z.numerator, z.denominator) for z in bvec(v)] for v in ys])
        if By.det() != 0:
            break
    Fm = sp.Matrix(NQ, NQ, lambda i, j: (lambda z: sp.Rational(z.numerator, z.denominator))(
        f(A.para(xs[i]), A.para(ys[j]))))
    M = Bx.inv() * Fm * By.T.inv()
    good = True
    for _ in range(4):
        x, y = rpara(n), rpara(n)
        bx = sp.Matrix([sp.Rational(z.numerator, z.denominator) for z in bvec(x)])
        by = sp.Matrix([sp.Rational(z.numerator, z.denominator) for z in bvec(y)])
        fv = f(A.para(x), A.para(y))
        good = good and (bx.T * M * by)[0] == sp.Rational(fv.numerator, fv.denominator)
    out["[I]-inst"] = good
    return out


def coverage_test(n, trials=20, seed=1):
    """float test: a random Mobius map (composition of random inversions/reflections/similarities) with
    nu(inf) != inf equals q + lam R_w kappa sigma(x + p) for some w in the paravector product family,
    lam real, iff orientation allows (n odd: always; n even: only orientation-preserving nu)."""
    r = np.random.default_rng(seed)
    kappa = np.diag([1.0] + [-1.0] * (n - 1))

    def inv_sphere(c, rad):
        def f(x):
            if x is None:
                return c.copy()
            dx = x - c
            if np.dot(dx, dx) == 0:
                return None
            return c + rad ** 2 * dx / np.dot(dx, dx)
        return f

    def refl(v, off):
        v = v / np.linalg.norm(v)
        return lambda x: None if x is None else x - 2 * (np.dot(x, v) - off) * v

    def householder(v):
        v = v / np.linalg.norm(v)
        return np.eye(n) - 2 * np.outer(v, v)

    results = []
    for _ in range(trials):
        maps, orient = [], 1
        for _j in range(r.integers(1, 5)):
            if r.random() < 0.5:
                maps.append(inv_sphere(r.normal(size=n), abs(r.normal()) + .5)); orient *= -1
            else:
                maps.append(refl(r.normal(size=n), r.normal())); orient *= -1
        if r.random() < 0.5:
            maps.append(refl(r.normal(size=n), r.normal())); orient *= -1

        def nu(x):
            for f in maps:
                x = f(x)
            return x
        # nu(inf) via a far point; c = nu^{-1}(inf): invert composition numerically
        # inverses: inversions and reflections are involutions
        def nuinv(x):
            for f in reversed(maps):
                x = f(x)
            return x
        # c = nu^{-1}(inf): limit of nuinv at large |x|
        c = nuinv(None)
        q = nu(None)
        if c is None or q is None:
            results.append((orient, None, 'fixes inf', None)); continue
        # psi(x) = nu(c + sigma(x)) - q is linear L x
        sig = lambda x: x / np.dot(x, x)
        L = np.column_stack([(nu(c + sig(1e-0 * e)) - q) for e in np.eye(n)])
        # check similarity: L^T L = s^2 I
        s2 = (L.T @ L)[0, 0]
        sim_ok = np.allclose(L.T @ L, s2 * np.eye(n), atol=1e-4 * s2)
        detsign = np.sign(np.linalg.det(L))
        # target: L = lam R kappa, R in SO(n)
        lam = np.sqrt(s2)
        found = False
        for sgn in (1, -1):
            Rm = (L / (sgn * lam)) @ kappa
            if DBG: print('det Rm', sgn, np.linalg.det(Rm))
            if np.linalg.det(Rm) > 0:
                # decompose Rm into 2*floor(n/2) reflections (Householder), padding
                vs, Mx = [], Rm.copy()
                for i in range(n):
                    e = np.eye(n)[i]
                    col = Mx[:, i]
                    if np.linalg.norm(col - e) > 1e-7:
                        v = col - e
                        H = householder(v)
                        Mx = H @ Mx
                        vs.append(v)
                # now Rm = H_1 ... H_r ; r even since det > 0 (and r <= n so r <= 2 floor(n/2))
                # pad
                while len(vs) < 2 * (n // 2):
                    z = r.normal(size=n); vs += [z, z]
                if DBG: print('nvs', len(vs))
                if len(vs) > 2 * (n // 2):
                    break
                # Clifford: R_w = rho_{p1} rho_{pbar2} rho_{p3} ... ;  p_{odd} = v, p_{even} = conj(v) = kappa v
                ps = [vs[i] if i % 2 == 0 else kappa @ vs[i] for i in range(len(vs))]
                # build R_w as a matrix via the product formula R_p = -rho_p kappa
                Af = Cl(n - 1)
                def fpara(v):
                    o = [0.0] * Af.dim
                    for i, cc in zip(Af.pidx, v):
                        o[i] = float(cc)
                    return o
                wf = fpara([1.0] + [0.0] * (n - 1))
                for pv in ps:
                    wf = Af.mul(wf, fpara(pv))
                nwf = Af.mul(wf, Af.C(wf))[0]
                whinv = [z / nwf for z in Af.R(wf)]
                cols = []
                for e in np.eye(n):
                    img = Af.mm(wf, fpara(e), whinv)
                    assert max((abs(img[i]) for i in range(Af.dim) if i not in Af.pidx), default=0.0) < 1e-8
                    cols.append(Af.pc(img))
                Rw = np.array(cols, dtype=float).T   # R_w(s) = w s w^{-hat}, computed in Cl directly
                cand = lambda x: q + sgn * lam * Rw @ kappa @ sig(x - c)
                pts = [r.normal(size=n) for _ in range(5)]
                found = all(np.allclose(cand(x), nu(x), rtol=1e-5, atol=1e-5) for x in pts)
                if not found and DBG: print('DBG n',n,'sgn',sgn,'|Rw-Rm|',np.abs(Rw-Rm).max(),'|L-sgn lam Rm k|',np.abs(L-sgn*lam*Rm@kappa).max(), 'cand-nu', max(np.abs(cand(x)-nu(x)).max() for x in pts), 'nvs', len(vs))
                if found:
                    break
        results.append((orient, round(detsign), sim_ok, found))
    return results


if __name__ == "__main__":
    for n in (2, 3, 4, 5, 6, 7):
        print(f"n={n} (Cl_(0,{n - 1}), m={2 * (n // 2)} paravectors):", check_dim(n)); sys.stdout.flush()
    for n in (2, 3, 4, 5, 6, 7):
        res = coverage_test(n)
        print(f"coverage n={n}: (orientation, det L sign, similarity ok, found in family)")
        print("   ", res)
        sys.stdout.flush()
