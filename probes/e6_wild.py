import sys
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from probe2 import *
from validate import retry
from e5_mobius import show
from validate import tally_line

# (A) points at angles 0, th, 2th, ..., (n-1)th  (th transcendental, e.g. 1 radian)
def angle_prog(n, o=0, start_free=False):
    pts = []
    for k in range(n):
        def f(th, k=k):
            t = th[o]                      # tan(th/2)
            tk = 0
            for _ in range(k):            # tan((j+1)x) = (tan jx + tan x)/(1 - tan jx tan x)
                tk = (tk + t) / (1 - tk * t)
            return circ(tk)
        pts.append(f)
    return pts

# (B) Poncelet chain: unit circle C, inner circle D centered (a,0) radius rho with chord t0-t1 tangent to D.
#     Poncelet correspondence: (a(1-tu) - (1+tu))^2 = rho^2 (1+t^2)(1+u^2); next vertex by Vieta.
def poncelet_chain(n):
    def make(k):
        def f(th):
            a, t0, t1 = th[0], th[1], th[2]
            rho2 = (a * (1 - t0 * t1) - (1 + t0 * t1)) ** 2 if False else None
            num = (a * (1 - t0 * t1) - (1 + t0 * t1))
            rho2 = num * num / ((1 + t0 * t0) * (1 + t1 * t1))
            ts = [t0, t1]
            while len(ts) <= k:
                t = ts[-1]
                S = 2 * (a * a - 1) * t / ((a + 1) * (a + 1) * t * t - rho2 * (1 + t * t))
                ts.append(S - ts[-2])
            return circ(ts[k])
        return f
    return [make(k) for k in range(n)]

def generic3(n):
    import random
    rng = random.Random(n)
    pts = []
    for i in range(n):
        c = [rng.randint(-3, 3) for _ in range(6)]
        pts.append(lambda th, c=c: circ((c[0]*th[0] + c[1]*th[1] + th[2] + c[2]) / (c[3]*th[0] + c[4]*th[2] + 1 + c[5]*th[1])))
    return pts

print("== (A) arithmetic progressions of angles (one transcendental parameter)")
for n in range(6, 14):
    show(f"angles 0, th, ..., {n-1}th", angle_prog(n), 1, expect="?")
print("== (B) Poncelet chains, circle D (3 transcendental params: a, t0, t1)")
for n in range(6, 15):
    show(f"Poncelet chain, {n} vertices", poncelet_chain(n), 3, expect="?")
print("== control: random 3-parameter families of the same sizes")
for n in (7, 9, 11, 13):
    show(f"random 3-param family, {n} pts", generic3(n), 3, expect="FAIL?")
print(tally_line())
