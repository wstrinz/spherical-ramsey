"""Hunt for a 6-point non-Ramsey cyclic set (2-jet FAIL), plus C1 test: 2-jet vs full criterion.

--real-scope (optional): also restrict every count to the configurations that realness.py decides
are real (exact test; about a third of this sampler's configurations are not real and are out of
scope).  The default output is unchanged; the flag only appends one REAL-SCOPED line.
"""
import sys, random
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry, palv, rats, tally_line, DECIDED
rng = random.Random(23)       # configuration stream
srng = random.Random(223)     # specialization stream: explicit seed (reproducible counts), independent of rng
fails, disagree, tested = [], [], 0
# NO_VERDICT is counted separately and is never agreement.
# pairs = (2-jet, full-criterion) comparisons; decided = both verdicts in {PASS, FAIL}.
stats = dict(pairs=0, decided=0, agree=0, nv_jet=0, nv_curve=0, nv_jet_all=0)
REAL_SCOPE = "--real-scope" in sys.argv[1:]
if REAL_SCOPE:   # realness.py replays this file's configuration stream with its own Random(23)
    from realness import stream as _stream, realness as _realness
    _SCOPE = [True if specs is None else _realness(specs, k)[0] for _l, _i, specs, k in _stream()]
    rstats = dict(tested=0, fail=0, nv_jet=0, pairs=0, decided=0, agree=0, pp=0, ff=0)

def rnd_q(): return R(rng.randint(-6, 6), rng.randint(1, 5))

def mob_pt(var, a, b, c, d):
    def f(th):
        t = th[var]; m = (a * t + b) / (c * t + d)
        return circ(m)
    return f

def sqrt_pt(var, a, b, c, d, sg):
    # x = Mobius(t) in (-1,1)-ish, y = sg*sqrt(1-x^2): algebraic extension of Q(t)
    def f(th):
        t = th[var]; x = (a * t + b) / (c * t + d)
        return [x, sg * sqrt(1 - x * x)]
    f.is_sqrt = True     # lets validate.retry scale its attempt cap
    return f

def rand_family(n, k):
    pts = []
    for _ in range(n):
        kind = rng.random()
        var = rng.randrange(k)
        a, b, c, d = [rng.randint(-4, 4) for _ in range(4)]
        if a * d - b * c == 0: a, d = 1, 1
        if kind < 0.15:
            pts.append(rat_circ(rng.randint(-7, 7), rng.randint(1, 7)))
        elif kind < 0.55:
            pts.append(mob_pt(var, a, b, c, d))
        else:
            pts.append(sqrt_pt(var, a, b, c, d, rng.choice((1, -1))))
    return pts

def mirror_family(npairs, k, extra):
    pts = []
    for i in range(npairs):
        var = rng.randrange(k); a, b, c, d = [rng.randint(-4, 4) for _ in range(4)]
        if a * d - b * c == 0: a, d = 1, 1
        pts += [sqrt_pt(var, a, b, c, d, 1), sqrt_pt(var, a, b, c, d, -1)]
    pts += [rat_circ(*e) for e in extra]
    return pts

def test(name, pts, k):
    global tested
    tested += 1
    real = REAL_SCOPE and _SCOPE[tested - 1]
    j = retry(jet2, pts, k, 2, trials=1, rng=srng)
    if real:
        rstats["tested"] += 1; rstats["fail"] += j == "FAIL"; rstats["nv_jet"] += j == "NO_VERDICT"
    if j == "NO_VERDICT": stats["nv_jet_all"] += 1
    if j == "FAIL":
        fails.append(name); print("  2-jet FAIL:", name); sys.stdout.flush()
    if k == 1 and len(pts) <= 10:   # full criterion available
        c = retry(curve_probe, pts, k, 2, trials=1, rng=srng)
        stats["pairs"] += 1
        stats["nv_jet"] += j == "NO_VERDICT"; stats["nv_curve"] += c == "NO_VERDICT"
        if real: rstats["pairs"] += 1
        if j in DECIDED and c in DECIDED:
            stats["decided"] += 1
            if real:
                rstats["decided"] += 1; rstats["agree"] += j == c
                rstats["pp"] += j == c == "PASS"; rstats["ff"] += j == c == "FAIL"
            if j == c: stats["agree"] += 1
            else:
                disagree.append((name, j, c)); print("  DISAGREE:", name, j, c); sys.stdout.flush()
        else:
            print("  NO_VERDICT:", name, j, c); sys.stdout.flush()
    return j

# (a) Palvolgyi heptagon minus one point
hp = palv()
for i in range(7):
    test(f"heptagon minus point {i}", hp[:i] + hp[i+1:], 1)
# (b) random one-parameter 6-point sets (mixed Mobius / sqrt / rational)
for _ in range(400): test("rand 1-param 6pt", rand_family(6, 1), 1)
# (c) mirror-symmetric 6-sets: 3 mirror pairs, one parameter / three parameters; 2 pairs + 2 axis pts
for _ in range(150): test("3 mirror pairs, k=1", mirror_family(3, 1, []), 1)
for _ in range(100): test("3 mirror pairs, k=3", mirror_family(3, 3, []), 3)
for _ in range(150): test("2 mirror pairs + (1,0),(-1,0), k=1", mirror_family(2, 1, [(0, 1)]) + [const_point([P - 1, 0])], 1)
# (d) random two/three-parameter 6-point sets
for _ in range(200): test("rand 2-param 6pt", rand_family(6, 2), 2)
for _ in range(100): test("rand 3-param 6pt", rand_family(6, 3), 3)
print(f"6-point sets tested: {tested}; 2-jet FAILs: {len(fails)}; 2-jet/full disagreements: {len(disagree)}")
sec_ab = dict(stats)
print(f"  6-point sets: 2-jet NO_VERDICT {stats['nv_jet_all']}; full-criterion comparisons {stats['pairs']}, "
      f"decided {stats['decided']}, agreements {stats['agree']}, NO_VERDICT (2-jet/curve) {stats['nv_jet']}/{stats['nv_curve']}")
# (e) C1 stress test on 7..9 point one-parameter sets (where failures do occur)
f7 = 0; t7 = 0
for n in (7, 8, 9):
    for _ in range(150):
        pts = rand_family(n, 1) if rng.random() < 0.6 else mirror_family(n // 2, 1, [(0, 1)] * (n % 2))
        t7 += 1
        if test(f"rand 1-param {n}pt", pts, 1) == "FAIL": f7 += 1
print(f"7-9 point one-parameter sets: {t7}, 2-jet FAIL {f7}; total disagreements with full criterion: {len(disagree)}")
print(f"  7-9 point sets: full-criterion comparisons {stats['pairs'] - sec_ab['pairs']}, "
      f"decided {stats['decided'] - sec_ab['decided']}, agreements {stats['agree'] - sec_ab['agree']}, "
      f"NO_VERDICT (2-jet/curve) {stats['nv_jet'] - sec_ab['nv_jet']}/{stats['nv_curve'] - sec_ab['nv_curve']}")
print(f"TOTAL: full-criterion comparisons {stats['pairs']}, decided {stats['decided']}, agreements {stats['agree']}, "
      f"disagreements {len(disagree)}, undecided {stats['pairs'] - stats['decided']}; 2-jet NO_VERDICT over all {tested} tests: {stats['nv_jet_all']}")
print(tally_line())
if REAL_SCOPE:
    assert tested == len(_SCOPE)
    print(f"REAL-SCOPED (realness.py, exact): real configurations {rstats['tested']} of {tested}; "
          f"2-jet FAIL {rstats['fail']}, 2-jet NO_VERDICT {rstats['nv_jet']}; full-criterion comparisons "
          f"{rstats['pairs']}, decided {rstats['decided']} (PASS/PASS {rstats['pp']}, FAIL/FAIL {rstats['ff']}), "
          f"disagreements {rstats['decided'] - rstats['agree']}")
