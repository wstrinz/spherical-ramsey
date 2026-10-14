import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))   # siblings importable under python -I
from e5_mobius import *
from validate import tally_line
def mob_circle2(pt_fn, o, rot=0):
    def f(th):
        x, y = pt_fn(th)
        s = div(x, 1 - y)                       # stereographic from (0,1)
        m = (th[o] * s + th[o + 1]) / (s + th[o + 2])
        return sph([m])
    return f
hp = palv()
show("Palvolgyi heptagon, identity re-projection (sanity)", [ (lambda f: (lambda th: sph([ (lambda xy: div(xy[0], 1-xy[1]))(f(th)) ])))(f) for f in hp], 1, expect="FAIL")
show("Palvolgyi heptagon under transcendental Mobius (3 new params)", [mob_circle2(f, 1) for f in hp], 4, expect="FAIL")
show("Palvolgyi heptagon under RATIONAL Mobius s->(2s+1)/(s+3)", [ (lambda f: (lambda th: sph([ (lambda xy: div(2*div(xy[0], 1-xy[1]) + 1, div(xy[0], 1-xy[1]) + 3))(f(th)) ])))(f) for f in hp], 1, expect="FAIL")
print(tally_line())
