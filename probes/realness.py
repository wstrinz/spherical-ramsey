"""Exact realness test (scope filter) for e4_six's configurations, and the exact structure of the 15
configurations that get NO_VERDICT from e4_six at p = 2^31-1.  No mod-p arithmetic: everything is
exact over Q (fractions.Fraction); a float grid is used only as an independent cross-check.

applies_to: any configuration of e4_six's spec families (rational circle points, circ(Mobius(t)) points,
  and sqrt points (x, sg*sqrt(1-x^2)) with x = (a t + b)/(c t + d), t one of k real parameters).
  The square-class algebra (F2 linear algebra on Q(t)^*/Q(t)^*2, constants included) and the
  interval sign analysis apply to any finite set of radicands that are products of linear forms.

Replays e4_six's configuration stream (rng = Random(23), identical consumption to e4_six), and for
every configuration, EXACTLY over Q:
  (1) realness: for each parameter t_v, is there an open real interval on which every sqrt radicand
      1 - x_i(t)^2 attached to t_v is > 0 (or is identically 0)?  A transcendental real parameter must
      lie in such an interval, so if none exists the configuration has no real member with t
      transcendental (only isolated algebraic t, a different configuration): NONREAL, out of scope.
  (2) square-class dependencies: subsets S of the sqrt points with prod_{i in S} (1 - x_i^2) a square
      in Q(t) up to a rational constant C_S (Gaussian elimination over F2 on factor parities, with the
      constant tracked exactly).  C_S < 0 forces NONREAL (the product of those radicands is <= 0
      everywhere).  C_S a positive non-square: the relation involves sqrt(C_S); C_S a rational square:
      a genuine sign relation prod y_i = +-g(t) between distinct radicands (the probe's sqrtmod picks
      that sign at random per tau).
  (3) the Legendre symbol of every obstruction constant at p1 = 2^31-1 and p2 = 2147483629.
Default output: one block per NO_VERDICT configuration and a census over all 1,557 configurations
(expected-v2/realness.log).

Scope filter: `realness(specs, k)` is the function to use.  `python -I realness.py --tsv` prints one
line per e4_six test, in e4_six's order (seq 0..1556, section a first), with REAL / NONREAL, so that
any e4_six count can be restricted to real configurations.
usage: python -I realness.py [--tsv]
"""
import random
import sys
from fractions import Fraction
from itertools import combinations

P1, P2 = 2147483647, 2147483629   # default probe prime (3 mod 4); a second prime (1 mod 4)

rng = random.Random(23)

def rand_family(n, k):
    specs = []
    for _ in range(n):
        kind = rng.random(); var = rng.randrange(k)
        a, b, c, d = [rng.randint(-4, 4) for _ in range(4)]
        if a * d - b * c == 0: a, d = 1, 1
        if kind < 0.15: specs.append(("rat", rng.randint(-7, 7), rng.randint(1, 7)))
        elif kind < 0.55: specs.append(("mob", var, a, b, c, d, 0))
        else: specs.append(("sqrt", var, a, b, c, d, rng.choice((1, -1))))
    return specs

def mirror_family(npairs, k, extra):
    specs = []
    for _ in range(npairs):
        var = rng.randrange(k); a, b, c, d = [rng.randint(-4, 4) for _ in range(4)]
        if a * d - b * c == 0: a, d = 1, 1
        specs += [("sqrt", var, a, b, c, d, 1), ("sqrt", var, a, b, c, d, -1)]
    specs += [("rat",) + tuple(e) for e in extra]
    return specs

def stream():
    """e4_six's configuration stream, in order: (label, index, specs, k)."""
    out = [("a heptagon minus point", i, None, 1) for i in range(7)]   # consumes no rng
    def run(label, gen, count, k):
        for i in range(count): out.append((label, i, gen(), k))
    run("b rand 1-param 6pt", lambda: rand_family(6, 1), 400, 1)
    run("c1 3 mirror pairs k=1", lambda: mirror_family(3, 1, []), 150, 1)
    run("c2 3 mirror pairs k=3", lambda: mirror_family(3, 3, []), 100, 3)
    run("c3 2 mirror pairs + 2 axis, k=1", lambda: mirror_family(2, 1, [(0, 1)]) + [("axis",)], 150, 1)
    run("d1 rand 2-param 6pt", lambda: rand_family(6, 2), 200, 2)
    run("d2 rand 3-param 6pt", lambda: rand_family(6, 3), 100, 3)
    for n in (7, 8, 9):
        for i in range(150):
            specs = rand_family(n, 1) if rng.random() < 0.6 else mirror_family(n // 2, 1, [(0, 1)] * (n % 2))
            out.append((f"e {n}pt k=1", i, specs, 1))
    return out

# ------------------------------------------------------------ exact radicand algebra
def lin_factors(s):
    """1 - x^2 = L1*L2/(ct+d)^2 with L1 = (c-a)t + (d-b), L2 = (c+a)t + (d+b)."""
    _, var, a, b, c, d, sg = s
    return ((c - a, d - b), (c + a, d + b))

def factor_prime(n):
    n = abs(n); f = {}; q = 2
    while q * q <= n:
        while n % q == 0: f[q] = f.get(q, 0) + 1; n //= q
        q += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def sqclass(s):
    """Class of 1-x^2 in Q(t)^*/Q(t)^*2 as a frozenset of generators ('t+r' monic roots, primes,
    '-1'), plus the exact numerator content: returns (gens, zero) where zero means 1-x^2 == 0."""
    L1, L2 = lin_factors(s)
    if L1 == (0, 0) or L2 == (0, 0): return None, True
    gens = {}
    const = Fraction(1)
    for (u, v) in (L1, L2):
        if u == 0: const *= v
        else:
            const *= u
            key = ("root", Fraction(v, u))      # monic factor t + v/u
            gens[key] = gens.get(key, 0) ^ 1
    if const < 0: gens[("sign",)] = 1
    for q, e in factor_prime(const.numerator).items():
        if e % 2: gens[("p", q)] = gens.get(("p", q), 0) ^ 1
    for q, e in factor_prime(const.denominator).items():
        if e % 2: gens[("p", q)] = gens.get(("p", q), 0) ^ 1
    return frozenset(g for g, x in gens.items() if x), False

def numerator_value(s, t):
    L1, L2 = lin_factors(s)
    return (L1[0] * t + L1[1]) * (L2[0] * t + L2[1])

def realness(specs, k):
    """For each var: an open interval (as a rational test point) with all radicand numerators > 0,
    ignoring identically-zero radicands.  Returns (real?, {var: witness t or None})."""
    wit = {}
    for v in range(k):
        sq = [s for s in specs if s[0] == "sqrt" and s[1] == v and not sqclass(s)[1]]
        if not sq: wit[v] = "free"; continue
        roots = set()
        for s in sq + [s for s in specs if s[0] in ("sqrt", "mob") and s[1] == v]:
            for (u, w) in lin_factors(s):
                if u: roots.add(Fraction(-w, u))
            if s[4]: roots.add(Fraction(-s[5], s[4]))       # pole of x
        rs = sorted(roots)
        tests = ([rs[0] - 1] + [(x + y) / 2 for x, y in zip(rs, rs[1:])] + [rs[-1] + 1]) if rs else [Fraction(0)]
        good = [t for t in tests if all(numerator_value(s, t) > 0 for s in sq)]
        wit[v] = good[0] if good else None
    return all(w is not None for w in wit.values()), wit

def dependencies(specs):
    """Minimal-ish F2 dependencies among the distinct sqrt radicand classes.  Returns a list of
    (subset of spec indices, constant class gens) where the polynomial part is trivial.  Identical
    radicand functions (mirror pairs) are reported separately (they are consistent by construction)."""
    idx = [i for i, s in enumerate(specs) if s[0] == "sqrt" and not sqclass(s)[1]]
    funcs = {}
    for i in idx:
        funcs.setdefault(radicand_key(specs[i]), []).append(i)
    reps = [v[0] for v in funcs.values()]
    deps = []
    # brute force over subsets of distinct radicands (at most 9 points): trivial polynomial class
    for r in range(1, len(reps) + 1):
        for S in combinations(reps, r):
            cls = {}
            for i in S:
                for g in sqclass(specs[i])[0]:
                    gg = (specs[i][1],) + g if g[0] == "root" else g
                    cls[gg] = cls.get(gg, 0) ^ 1
            live = {g for g, x in cls.items() if x}
            if not any(len(g) == 3 for g in live):   # no (var, "root", r) generator left
                # minimality: skip if a proper subset is already a dependency
                if any(set(T) < set(S) for T, _ in deps): continue
                deps.append((S, frozenset(live)))
    return deps, funcs

def radicand_key(s):
    """1 - x^2 as an exact rational function of t (var-tagged): x = (at+b)/(ct+d) normalised."""
    _, var, a, b, c, d, sg = s
    # x up to sign determines 1-x^2; normalise (a,b,c,d) by scaling and the sign of x
    import math
    g = math.gcd(math.gcd(a, b), math.gcd(c, d)) or 1
    a, b, c, d = a // g, b // g, c // g, d // g
    if (c, d) < (0, 0) or (c == 0 and d < 0): a, b, c, d = -a, -b, -c, -d
    x1 = (a, b, c, d); x2 = (-a, -b, c, d)
    return (var, min(x1, x2))

def float_real(specs, k):
    """Independent float cross-check of realness: grid t in [-60, 60] (step 1/997) plus +-1e6."""
    import numpy as np
    ts = np.concatenate([np.arange(-60, 60, 1 / 997.0), [-1e6, 1e6]])
    for v in range(k):
        sq = [s for s in specs if s[0] == "sqrt" and s[1] == v and not sqclass(s)[1]]
        ok = np.ones_like(ts, dtype=bool)
        for s in sq:
            (u1, w1), (u2, w2) = lin_factors(s)
            ok &= (u1 * ts + w1) * (u2 * ts + w2) > 0
        if not ok.any(): return False
    return True

def const_value(gens):
    """The rational constant class as a squarefree integer."""
    v = 1
    for g in gens:
        if g == ("sign",): v = -v
        elif g[0] == "p": v *= g[1]
    return v

def legendre(v, p):
    v %= p
    return 1 if pow(v, (p - 1) // 2, p) == 1 else -1

if __name__ == "__main__" and "--tsv" in sys.argv[1:]:
    print("seq	section	index	k	n	scope")
    for seq, (label, i, specs, k) in enumerate(stream()):
        if specs is None:   # section a: heptagon minus a point, real by hand (r >= 2), see below
            print(f"{seq}	{label}	{i}	1	6	REAL"); continue
        print(f"{seq}	{label}	{i}	{k}	{len(specs)}	{'REAL' if realness(specs, k)[0] else 'NONREAL'}")
elif __name__ == "__main__":
    NV = {("b rand 1-param 6pt", 184), ("c2 3 mirror pairs k=3", 50), ("d2 rand 3-param 6pt", 56),
          ("e 7pt k=1", 62), ("e 7pt k=1", 127), ("e 8pt k=1", 80), ("e 8pt k=1", 104),
          ("e 8pt k=1", 113), ("e 8pt k=1", 131), ("e 8pt k=1", 133), ("e 9pt k=1", 2),
          ("e 9pt k=1", 7), ("e 9pt k=1", 65), ("e 9pt k=1", 68), ("e 9pt k=1", 91)}
    # ^ the 15 e4_six configurations with 2-jet NO_VERDICT at p = 2^31-1 (located by a separate
    #   residue-feasibility replay of e4_six's stream, not shipped; the count 15 is in e4_six.log)
    census = dict(configs=0, with_sqrt=0, nonreal=0, signdep=0, negconst=0, float_mismatch=0)
    bysec = {}
    for label, i, specs, k in stream():
        if specs is None: continue
        census["configs"] += 1
        if any(s[0] == "sqrt" for s in specs): census["with_sqrt"] += 1
        real, wit = realness(specs, k)
        if real != float_real(specs, k): census["float_mismatch"] += 1
        sec = bysec.setdefault(label, [0, 0]); sec[0] += 1; sec[1] += not real
        deps, funcs = dependencies(specs)
        consts = [const_value(c) for S, c in deps]
        if not real: census["nonreal"] += 1
        if any(c < 0 for c in consts): census["negconst"] += 1
        if any(c == 1 for c in consts): census["signdep"] += 1
        if (label, i) in NV:
            print(f"== {label} #{i}  (k={k}, n={len(specs)})")
            for j, s in enumerate(specs):
                if s[0] == "sqrt":
                    _, var, a, b, c, d, sg = s
                    L1, L2 = lin_factors(s)
                    print(f"   p{j}: sqrt t{var} x=({a}t+{b})/({c}t+{d}) sg={sg:+d}  1-x^2 ~ ({L1[0]}t+{L1[1]})({L2[0]}t+{L2[1]})")
                elif s[0] == "mob": print(f"   p{j}: circ(({s[2]}t{s[1]}+{s[3]})/({s[4]}t{s[1]}+{s[5]}))")
                else: print(f"   p{j}: {s}")
            print(f"   distinct radicand functions: {len(funcs)}; dependencies (subset: constant class):",
                  [(list(S), c) for (S, _), c in zip(deps, consts)])
            print(f"   Legendre of constants at p1=2^31-1: {[legendre(c, P1) for c in consts]}; at p2={P2}: {[legendre(c, P2) for c in consts]}")
            print(f"   REAL: {real}; witness test points per var: {wit}")
    print("census over all e4_six configurations (sections b-e):", census)
    print("NONREAL per section (tested, nonreal):", bysec)
    print("section a (heptagon minus a point, 7 configs): REAL by hand (x = (j-r)/r, y^2 = j(2r-j)/r^2 >= 0 for r >= 2)")
