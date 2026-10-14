import sys, random
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry, palv, rats, tally_line
from e3_sphere import indep_sphere
rng = random.Random(29)
srng = random.Random(229)   # specialization RNG, explicit seed (reproducible counts)

def mob_circle(base, o):
    """apply s -> (th[o]*s + th[o+1]) / (s + th[o+2]) (transcendental Mobius) to a circle point given
    by stereographic parameter function base(th) -> s"""
    def f(th):
        s = base(th)
        return circ((th[o] * s + th[o + 1]) / (s + th[o + 2]))
    return f

def rat_s(a, b): return lambda th: R(a, b)
def free_s(i): return lambda th: th[i]
RQ = [(0,1),(1,2),(1,3),(2,3),(3,4),(1,5),(2,5),(3,5),(4,5),(1,7),(3,7),(5,7),(6,7),(2,7)]

def stereo_of(pt_fn):
    # stereographic parameter of a unit-circle point from (-1,0): s = y/(1+x)
    return lambda th: (lambda xy: xy[1] / (1 + xy[0]))(pt_fn(th))

def show(name, pts, k, d=2, expect=""):
    j = retry(jet2, pts, k, d, trials=1, rng=srng)
    c = retry(curve_probe, pts, k, d, trials=1, rng=srng) if len(pts) * (d+1)**2 <= 150 else "-"
    print(f"{name:72s} expect {expect:5s} | 2-jet {j:5s} | curve {c}"); sys.stdout.flush()

if __name__ == "__main__":
    print("== Mobius invariance (circle)")
    show("12 rational pts under one transcendental Mobius (generic 12 => FAIL)",
         [mob_circle(rat_s(*q), 0) for q in RQ[:12]], 3, expect="PASS")
    # (Palvolgyi heptagon under Mobius maps: see e5b.py, which re-projects from (0,1) so that it
    #  avoids the pole of stereo_of above: the heptagon contains (-1,0) itself.)
    print("== two Mobius groups (circle)")
    show("generic triple + Mobius image of 4 rational pts (7 pts)",
         [lambda th, i=i: circ(th[i]) for i in range(3)] + [mob_circle(rat_s(*q), 3) for q in RQ[:4]], 6, expect="PASS")
    show("Mobius-alg 4 (nu1) + Mobius-alg 4 (nu2)  (8 pts)",
         [mob_circle(rat_s(*q), 0) for q in RQ[:4]] + [mob_circle(rat_s(*q), 3) for q in RQ[4:8]], 6, expect="PASS")
    show("Mobius-alg 6 + Mobius-alg 6  (12 pts)",
         [mob_circle(rat_s(*q), 0) for q in RQ[:6]] + [mob_circle(rat_s(*q), 3) for q in RQ[6:12]], 6, expect="PASS")
    show("Mobius-alg 4 + 4 + 4 (three groups, 12 pts)",
         [mob_circle(rat_s(*q), 0) for q in RQ[:4]] + [mob_circle(rat_s(*q), 3) for q in RQ[4:8]] + [mob_circle(rat_s(*q), 6) for q in RQ[8:12]], 9, expect="?")
    show("Mobius-alg 3 + 3 + 3 + rational 3 (12 pts)",
         [mob_circle(rat_s(*q), 0) for q in RQ[:3]] + [mob_circle(rat_s(*q), 3) for q in RQ[3:6]] + [mob_circle(rat_s(*q), 6) for q in RQ[6:9]] + [rat_circ(*q) for q in RQ[9:12]], 9, expect="?")
    show("generic triple + generic 4 (= generic 7)",
         [lambda th, i=i: circ(th[i]) for i in range(7)], 7, expect="FAIL")
    
if __name__ == "__main__": print("== S^2: complex Mobius z -> (z + b)/(c z + d), b,c,d complex transcendental")
def cmul(a, b): return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])
def cdiv(a, b):
    den = b[0]*b[0] + b[1]*b[1]
    return ((a[0]*b[0] + a[1]*b[1]) / den, (a[1]*b[0] - a[0]*b[1]) / den)
def mob_s2(z0, o):
    def f(th):
        z = z0
        b = (th[o], th[o+1]); c = (th[o+2], th[o+3]); d = (1 + th[o+4], th[o+5])
        num = (z[0] + b[0], z[1] + b[1])
        den = cmul(c, z); den = (den[0] + d[0], den[1] + d[1])
        w = cdiv(num, den)
        return sph([w[0], w[1]])
    return f
zs = [(R(rng.randint(-5,5), rng.randint(1,4)), R(rng.randint(-5,5), rng.randint(1,4))) for _ in range(20)]
if __name__ == "__main__": show("S^2: 14 rational pts under one transcendental Mobius (generic 14 => FAIL)", [mob_s2(z, 0) for z in zs[:14]], 6, 3, expect="PASS")
if __name__ == "__main__": show("S^2: Mobius-alg 6 + Mobius-alg 6 (12 pts; generic 12 => FAIL)", [mob_s2(z, 0) for z in zs[:6]] + [mob_s2(z, 6) for z in zs[6:12]], 12, 3, expect="PASS?")
if __name__ == "__main__": show("S^2: Mobius-alg 4 + 4 + 4", [mob_s2(z, 0) for z in zs[:4]] + [mob_s2(z, 6) for z in zs[4:8]] + [mob_s2(z, 12) for z in zs[8:12]], 18, 3, expect="?")
if __name__ == "__main__": print(tally_line())
