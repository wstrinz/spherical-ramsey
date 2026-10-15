# Certificates

Exact scripts behind the certified claims of the note, each with its expected output in `expected/`.

**Exact arithmetic only.** Every check that a claim rests on is done in exact arithmetic: Python
`Fraction`s, sympy rationals, polynomial rings and rational function fields over Q, exact
determinants and ranks, and exact rational interval enclosures. Floating point and random
specialization modulo a prime are used in a few places to *propose* candidates or as a
*consistency* check; they **never conclude**. Each paragraph below says which lines of a log are
exact and which are not.

**Status tags.** Every claim carries one tag.
- **[CERT]**: an exact symbolic identity, determinant, rank or certificate, checked by a script
  here, **plus written glue** that turns the checked identity into the theorem. The script
  certifies the identity; the glue is a written argument, and lives in the note. Neither alone is
  the theorem.
- **[HAND]**: a written argument is the conclusion. A script may check ingredients or instances,
  but the theorem is the argument.
- **[PROBE]**: evidence, not proof (floating point, random rational instances of a general
  statement, or mod-p specialization).
- **[SKETCH]**: an outline, not a proof.

**Scope.** Every claim states the type of its coordinates over Q: `ALGEBRAIC`,
`GENERIC_OF(...)` (algebraically independent free coordinates), `TRANSCENDENTAL_PARAM(spec)`,
`MOBIUS_ORBIT_OF(type)` or `ANY`. "Real" is never a scope: the verdict can flip between the
algebraic and the transcendental members of one real family (Theorem D).

**Conjecture numbers.** `C-n` in these scripts, their output and this file is entry `SR-Cn` of the
conjecture ledger (`../ledger/LEDGER.md`).

**Coordinates.** The configurations are written in OpenAI's coordinates (`p_i = (1, a_i)`, points
on the unit sphere, OpenAI's field criterion over `B = F (x)_Q F`), as in the note's
Preliminaries. "The circle dictionary" and "Lemma 0" refer to that section of the note.

## How to run

Requirements: Python >= 3.10 with sympy, numpy and mpmath. The expected logs were produced with
Python 3.10.6, sympy 1.14.0, numpy 1.26.4 and mpmath 1.3.0; another sympy version can print the
same mathematics in a different form.

```
bash check.sh            # the fast set (about 12 minutes in total)
bash check.sh --all      # fast + slow (the slow set adds about 3 hours)
bash check.sh --slow     # the slow set only
bash check.sh dual_cert scalar_exact   # selected entries
```

`check.sh` works from any directory and on Linux (`python3`) and Git Bash on Windows (set
`PYTHON=python` if there is no `python3`). It runs each script as `python3 -I -B script.py ARGS`,
captures stdout and stderr, and diffs the output against `expected/<entry>.log`. It prints one
`PASS` or `FAIL` line per entry with the elapsed seconds, and exits non-zero on any mismatch or
non-zero exit status.

**Filter.** Before diffing, both sides are normalized: carriage returns are deleted; elapsed-time
stamps of the form ` (123s)` and ` [12.3s]` are deleted; and `(sympy X.Y.Z; 123s)` becomes
`(sympy)`. These are the only wall-clock prints in the scripts (in `cert_clifford.py`,
`cert_s2.py`, `cert_s2_quat.py`, `cert_clifford_seed.py` and `exact_circle_cert.py`, which
`cert_nontwogroup.py` calls). The files in `expected/` are stored already normalized. Nothing else
is filtered. All randomness is seeded, so every other byte is deterministic; each script was run
at least twice and gave identical normalized output.

Each script can also be run by hand, from any directory: `python3 -I <script>.py [args]`.
`dual_cert.py` and `rankN_sweep.py` import `probe2.py` and `validate.py` (and `rankN_sweep.py` also `c22_controls.py`, `c23_count_law.py`, `c13_c22_seven.py`) from
the sibling directory `../probes` (the [PROBE] harness); leave `PROBE_PRIME` unset (default prime
2^31 - 1) when comparing with `expected/`.

| Set | Entry (`expected/<entry>.log`) | Script and arguments | Runtime here |
|---|---|---|---|
| fast | `cert_mobius` | `cert_mobius.py` | 131 s |
| fast | `radian_det` | `radian_det.py` | 8 s |
| fast | `cert_s2_quat` | `cert_s2_quat.py` | 95 s |
| fast | `cert_clifford_obs` | `cert_clifford_obs.py` | 9 s |
| fast | `cert_clifford_seed` | `cert_clifford_seed.py` | 7 s |
| fast | `cert_clifford_lorentz` | `cert_clifford_lorentz.py` | 6 s |
| fast | `g4_test` | `g4_test.py` | 13 s |
| fast | `dual_cert` | `dual_cert.py` | 130 s |
| fast | `scalar_exact` | `scalar_exact.py` | 58 s |
| fast | `cert_nontwogroup` | `cert_nontwogroup.py` | 36 s |
| fast | `exact_circle_cert.quick` | `exact_circle_cert.py "[Ramsey" "[non-Ramsey, det]" "not two-group"` | 53 s |
| fast | `rankN_check` | `rankN_check.py` | 11 s |
| fast | `rankN_sweep` | `rankN_sweep.py` | 75 s |
| fast | `definable_bigball` | `definable_bigball.py` | 9 s |
| fast | `definable_crosscheck` | `definable_crosscheck.py` | 5 s |
| fast | `corank_exact.c29` | `corank_exact.py c29` | 4 s |
| fast | `corank_exact.c30` | `corank_exact.py c30` | 10 s |
| fast | `corank_exact.c31` | `corank_exact.py c31` | 26 s |
| fast | `corank_exact.c32` | `corank_exact.py c32` | 27 s |
| fast | `c31_respecialize` | `c31_respecialize.py` | 5 s |
| fast | `c34_det16` | `c34_det16.py` | 5 s |
| slow | `cert_clifford_crosscheck` | `cert_clifford_crosscheck.py` | 161-283 s |
| slow | `cert_s2` | `cert_s2.py` | 137 s |
| slow | `definable_polyphase` | `definable_polyphase.py` | 403 s |
| slow | `exact_circle_cert.controls` | `exact_circle_cert.py control` | 705 s (12 min) |
| slow | `exact_circle_cert.NEW` | `exact_circle_cert.py "NEW: 3 rat" "NEW: 4 rat" "radian 7-gon"` | 2,100-2,900 s (35-48 min) |
| slow | `cert_nontwogroup.slow` | `cert_nontwogroup.py --slow` | 2,200-2,800 s (37-47 min) |
| slow | `cert_clifford` | `cert_clifford.py` | 3,200-3,800 s (54-63 min) |

Runtimes are wall-clock seconds on the machine that produced `expected/` (a Windows desktop, with
other jobs running), as printed by `check.sh`; a laptop may be slower. A range means
several runs under different load. The fast set takes about 12 minutes in total and each fast
script well under 3 minutes (most under 2); the slow set takes about 3 hours run one after another.
CI (`.github/workflows/certificates.yml`) runs the fast set on every push; the slow set on
dispatch only.

## The scripts

### The circle, and two Möbius groups (Ramsey side)

**`cert_mobius.py`** — Theorems B(a) and B(b) on the circle. It checks two (2,2)-form
certificates symbolically, as identities in the stereographic parameters: (1) for **any six points**
of a circle, the product `g123 * g456` of the Möbius graph forms of two triples has vanishing
evaluations at all six points, and its diagonal restriction has spatial block `c I` with
`c = -(1/2)(T1-T2)(T1-T3)(T2-T3)(T4-T5)(T4-T6)(T5-T6)`, nonzero for distinct points; (2) for
**rational points plus three arbitrary points**, `(s - s') * g123` does the same at six named
rational points and the three symbolic ones, with `c = (1/2)(T1-T2)(T1-T3)(T2-T3)` (the factor
`s - s'` vanishes at every rational point, so the number of rational points is irrelevant). Glue (in the note): the circle dictionary and Lemma 0 turn each identity
into OpenAI's criterion, so the set is Ramsey; for B(b) with algebraic (not rational) points the
glue adds the separability idempotent of the number field (tested by `g4_test.py`), and the case of
at least seven points uses that four algebraic points fix an algebraic centre and radius. Tag:
**[CERT]** (both theorems are also [LEAN] in the ropes AV2 and AV5). Scope: B(a) `ANY` (six points);
B(b) `ALGEBRAIC` plus three `ANY`. Runtime: 131 s. Log: `expected/cert_mobius.log`.
Dependencies: sympy.

**`g4_test.py`** — the algebraic-seed glue (transport of a certificate from rational to algebraic
seeds by a separability idempotent), checked exactly on one example: the circle, two Möbius
groups with seeds in Q(√2) and Q(√3), and the idempotent `e = e_2 e_3` of the compositum, computed
in `K (x) K` presented as a quotient of a polynomial ring over Q. It checks `e * f(x_i, y_i) = 0`
at all seven algebraic seeds, the control that `f(x_i, y_i) != 0` without `e` at the irrational
seeds, and `m(f) = det N1 det N2 (s' - s)^2`. Tag: **[CERT]** for this example; the general
statement (the note's "Algebraic seeds" subsection) is a written argument, reviewed (AI). Scope:
`MOBIUS_ORBIT_OF(ALGEBRAIC)` x2 on the circle, for the seeds listed. Runtime: 13 s. Log:
`expected/g4_test.log`. Dependencies: sympy.

**`cert_s2.py`** — Theorem C2 for d = 3 (S²), complex form; by specialization to real maps it also
covers the circle. The chart is C, and `H = g_1 * conj(g_2)` for the C-bilinear graph forms `g_k` of
two Möbius correspondences gives two real certificates `P_r = Re H`, `P_i = Im H`. It checks, as
polynomial identities over Q (the imaginary unit is formal): [0] the coordinate identities;
[1] any 6 points of S² split 3 + 3 (vanishing evaluations, and `m(P_r) + i m(P_i)` a complex
multiple of `S`); [2] the great-circle restriction reproduces `cert_mobius.py`'s certificate;
[3] the primary statement: two Möbius images `nu_1(A_1) u nu_2(A_2)` with generic parameters
(independent symbols in the two tensor factors) have vanishing evaluations identically in a
symbolic seed point, an explicit 6 + 6 = 12-point rational instance, and `m(P) = c S`; and a
three-group control (nonzero). Glue (in the note, proof of Theorem C2 and "Exact certificates for
d <= 6"): one of `Re H`, `Im H` (or a unit multiple of `H`) has `m = c S` with `c != 0`, Lemma 0,
rotation off the pole, coverage of every Möbius map of S² by PSL₂(C) and conjugation, and the
idempotent transport to algebraic seeds. Tag: **[CERT]** plus glue, reviewed (AI). Scope:
`MOBIUS_ORBIT_OF(ALGEBRAIC)` x2 on S² (rational seeds directly; algebraic seeds via the glue).
Runtime: 137 s (slow set). Log: `expected/cert_s2.log`. Dependencies: sympy; reads
`cert_mobius.py` from its own directory (for check [2]).

**`cert_s2_quat.py`** — Theorem C2 for d = 4, 5 (S³, S⁴), quaternionic form, restricting to S², S¹.
With `h(x, y) = y C x + y D + A x + B` the affine-affine quaternionic graph form of a Möbius
correspondence and `f = Re(h_1 conj h_2)`, it checks: [0] coordinates; [I] the pairing identity
`f = b(x)^T M b(y)` with M free of x, y (32 coefficient symbols); [III] the diagonal
`m(P) = -(kappa_1 kappa_2 / 2) S`; [II] the three-point graph form; [II'] the graph form of a
generic quaternionic Möbius map vanishes identically in a symbolic seed point; [V] a general leading
coefficient; and [IV], [IV'] end-to-end evaluations at exact rationals on S⁴, S³, S², S¹. Glue (in
the note): as for `cert_s2.py`; coverage of every Möbius map of S⁴ by PSL₂(H) (a cited fact), S³ as
a great 3-sphere of S⁴, or the Clifford route below. Tag: **[CERT]** plus glue, reviewed (AI).
Scope: `MOBIUS_ORBIT_OF(ALGEBRAIC)` x2 on S⁴ and S³. Runtime: 95 s. Log:
`expected/cert_s2_quat.log`. Dependencies: sympy.

**`cert_clifford.py`** — Theorem C2 for d = 6 (S⁵), Clifford form in `Cl_{0,4}`, with the
every-dimension lemmas checked for small n. It checks: the algebra axioms of `Cl_{0,k}` for
k = 1..6; the coordinate identities; the pairing lemma `f = Re(h_1 conj h_2) = b(x)^T M b(y)` with
128 free coefficient symbols and its diagonal ([I], [III]); the one-step Lipschitz lemma [L] for
n = 1..7; the Vahlen normal-form identities [II'] symbolically (36 symbols); an end-to-end test at
exact rationals with independent parameters on the two sides, five seeds per group, in OpenAI's
coordinates, with a third group as a control; and [I] + [III] for n = 2, 3, 4, 6, 7 and [II'] for
n = 2, 3, 4. Glue (in the note: the Clifford conventions, the Pairing, Lipschitz, Vahlen and
Vanishing lemmas, the coverage lemma, the proof of Theorem C2 and "Algebraic seeds"): every Möbius
map with `nu(inf) != inf` has the normal form up to rational changes of seeds (cited: the
inversion-similarity decomposition and Cartan–Dieudonné), Lemma 0, and the idempotent transport.
Tag: **[CERT]** plus glue for d = 6, reviewed (AI); for every d the conclusion is **[HAND]**,
with these identity families as machine checks. Scope: `MOBIUS_ORBIT_OF(ALGEBRAIC)` x2 on S⁵.
Runtime: 3,200-3,800 s (54-63 min) (slow set; it prints elapsed seconds, which `check.sh` filters). Log:
`expected/cert_clifford.log`. Dependencies: sympy. The next three scripts import its `Cl` class
and helpers.

**`cert_clifford_crosscheck.py`** — an independent cross-check of `cert_clifford.py`, written by a
reviewer with its own blade-sign table, exact Fractions, and inverses by linear solving. For
n = 2..7 (d = 3..8) it checks (V0), (V0'), (V1)–(V3), an instance of the vanishing lemma and an
instance of the pairing identity [I], at seeded random exact rationals; then a floating-point
coverage test: the normal-form family recovers every sampled Möbius map with `nu(inf) != inf`
(both orientations for odd n, exactly the orientation-preserving ones for even n, which is why the
log shows `False` entries for n = 2, 4, 6). Tag: corroboration only. The exact checks are exact
but are random instances, not identities; the coverage test is floating point, **[PROBE]**. The
every-d statement is [HAND]. Scope: as for `cert_clifford.py`, d = 3..8. Runtime:
161-283 s. Log: `expected/cert_clifford_crosscheck.log`. Dependencies: numpy
(standalone; it does not import `cert_clifford.py`).

**`cert_clifford_obs.py`** — why the quaternionic generic-entry recipe does not transfer to
`Cl_{0,4}`: exact computations on explicit elements show that `1 + e1e2e3e4` is a zero divisor,
that the invertible non-Lipschitz element `2 + e1e2e3` sends the paravector 1 off the chart under
`t -> t (2 + e1e2e3)^{-1}`, and that used as `w` it breaks the normal-form identities, while a
product of four rational paravectors does not. Tag: **[CERT]** (explicit counterexamples; the
note's "The naive route fails" paragraph). Scope: the algebra `Cl_{0,4}`; not a configuration
claim. Runtime: 9 s. Log: `expected/cert_clifford_obs.log`. Dependencies:
`cert_clifford.py`.

**`cert_clifford_seed.py`** — the input to the algebraic-seed glue on S⁵, on three seeded
instances: with exact rational parameters chosen independently in the two tensor factors and a
symbolic seed point `t` in R⁵, `n_L n_R h(nu_L t, nu_R t) = 0` identically in `t`, and, with
independent seeds `t_L != t_R`, the same expression is a nonzero polynomial vanishing on
`t_L = t_R`. Tag: **[CERT]** for these three instances; it is a test of a glue step, not a proof
step (the proof is `cert_clifford.py`'s (V1)–(V3) plus the written glue). Scope: S⁵,
rational instances. Runtime: 7 s. Log: `expected/cert_clifford_seed.log`.
Dependencies: `cert_clifford.py`.

**`cert_clifford_lorentz.py`** — a structural reading of the two-group certificate (the note's
remark "Why two"): `f` is bilinear and symmetric in the two Vahlen matrices, so it is the polar
form of `mu -> f(mu, mu)`, and for one Vahlen matrix `S Q(mu)^T` is, up to scale, the Lorentz
matrix of `mu` in O(1, 6). Checked exactly on three rational instances on S⁵. Tag: the instance
checks are exact; the reading itself is **[SKETCH]** and is **not** evidence that three groups
fail. Scope: S⁵, rational instances. Runtime: 6 s. Log:
`expected/cert_clifford_lorentz.log`. Dependencies: `cert_clifford.py`.

### Radian progressions and non-two-group cyclic sets

**`radian_det.py`** — Theorem D, non-Ramsey direction. For the nine points at angles
`0, theta, ..., 8 theta`, the 9 x 9 tensor evaluation matrix (entries in `Q(T, U)`, `T = tan(theta/2)
(x) 1`, `U = 1 (x) tan(theta/2)`) has a nonzero exact determinant at the rational points
`(T, U) = (1/3, 2/7)` and `(-5/11, 3/13)`, so its determinant is nonzero in `Q(T, U)`. Rope AV3
certifies the same determinant, denominator-cleared, at `(T, U) = (2, 3)` in the Lean kernel. Glue
(in the note, proof sketch of Theorem D, OpenAI's Prop. 7.6 method): if `tan(theta/2)` is transcendental,
`B` embeds in `Q(T, U)`, so condition (1) forces `P = 0`, contradicting (2). Tag: **[CERT]** for
the determinant (Theorem D itself is [LEAN], rope AV3). Scope:
`TRANSCENDENTAL_PARAM(tan(theta/2))`. Runtime: 8 s. Log: `expected/radian_det.log`.
Dependencies: sympy.

**`exact_circle_cert.py`** — an exact decision procedure for one-parameter cyclic sets
(stereographic parameters in `Q(t)`, `t` transcendental). It computes the kernel `V` of the
evaluation matrix over `Q(T, U)`, saturates it at the prime `U - T` inside `Q(T)[U]`, and tests
whether `(s - s')^2` lies in the span of the reductions. A Ramsey verdict comes with a (2,2)-form
certificate that is **independently re-verified** (vanishing at every `(r_i(T), r_i(U))` and
`g(T, T) = kappa (s - s')^2`, `kappa != 0`); with the circle dictionary and Lemma 0 this is a
**[CERT]**. A non-Ramsey verdict with `dim V = 0` is Theorem D's determinant argument, **[CERT]**;
a non-Ramsey verdict with `dim V > 0` rests on the k = 1 DVR criterion (the local ring at the
diagonal is a DVR), a **[HAND]** argument reviewed (AI). Selections (each argument selects the
cases whose label contains it): `quick` = the four fast controls (B(b), multiples `circ(kt)`, the
9-point determinant example, a two-group set) and the 7- and 8-point non-two-group sets;
`controls` = all five controls, including the radian 9-gon (Theorem D); `NEW` = the 7- and
8-point non-two-group sets and the radian 7-gon. The case "radian 8-gon" (C-10) is **not** run by
`check.sh`: its kernel computation did not finish in 40 minutes. Scope:
`TRANSCENDENTAL_PARAM(t)`. Runtimes: 53 s (quick),
705 s (12 min) (controls, slow), 2,100-2,900 s (35-48 min) (NEW, slow). Logs:
`expected/exact_circle_cert.quick.log`, `.controls.log`, `.NEW.log`. Dependencies: sympy.

**`cert_nontwogroup.py`** — Theorem NTG: two Möbius groups are not the only mechanism. For W7 =
{0, 1/2, 1/3} u {circ(t), circ(t+1), circ(2t), circ(1/t)} and W8 = W7 u {2/3} (stereographic
parameters, `t` transcendental), and with `--slow` the radian 7-gon `{k theta : k <= 6}`, it
(1) checks exactly that the set is **not** a union of two Möbius images of algebraic sets (every
2-part partition has a part with at least four points and a non-constant, hence transcendental,
4-point cross-ratio), and (2) prints an explicit (2,2)-form certificate with coefficients in
`Q(T)[U]` (inside `B`), re-verified independently by `exact_circle_cert.verify`. Glue (in the note):
the circle dictionary and Lemma 0, exactly as for Theorem B(a). Tag: **[CERT]** plus glue, reviewed
(AI) (this refutes C-13).
Scope: `TRANSCENDENTAL_PARAM(t)` (W7, W8: `t` transcendental; radian 7-gon: `tan(theta/2)`
transcendental; for algebraic values Theorem A applies). Runtimes: 36 s (fast),
2,200-2,800 s (37-47 min) (`--slow`). Logs: `expected/cert_nontwogroup.log`,
`expected/cert_nontwogroup.slow.log`. Dependencies: `exact_circle_cert.py`.

**`rankN_check.py`** — the rank criterion C-24 and the radian 8-gon C-10. C-24: a one-parameter
cyclic set with `5 <= n <= 8` points is Ramsey if the `n x 8` matrix `N` with rows
`(delta_i, delta_i s_i, delta_i s_i^2, 1, s_i, s_i^2, s_i^3, s_i^4)` has rank `n` over the coordinate
field. The script (1) runs the criterion's falsifier on Pálvölgyi's heptagon (non-Ramsey):
numerical singular values at four values of `r` (mpmath, 50 digits; **[PROBE]**), then (1b) the
exact identity `delta_i = -s_i (1 + s_i^2) / (2r)` for every heptagon point, which gives two
explicit kernel vectors, so `rank N <= 6` for every `r` (exact); and (2) exact ranks of `N` at
two rational points (full rank at a point implies full generic rank): rank 7 for the radian
7-gon, **rank 8 for the radian 8-gon**, rank 7 and 8 for W7 and W8, and controls. Tag: the
ranks are exact; C-24 is **[HAND]** (proof reviewed (AI), in the note), and C-10 (the radian 8-gon
is Ramsey for every `theta`) is **[HAND]**, from C-24 plus the exact rank 8 here (for algebraic
`tan(theta/2)`, Theorem A). Scope: C-24 `TRANSCENDENTAL_PARAM` (k = 1); C-10 `ANY`. Runtime:
11 s. Log: `expected/rankN_check.log`. Dependencies: sympy, mpmath.

**`rankN_sweep.py`** — a sweep for C-24: 185 random one-parameter cyclic sets (n = 6, 7, 8, and
mirror-symmetric 7-sets), each with the exact rank of `N` at a random rational point and the full
one-parameter criterion evaluated modulo `p = 2^31 - 1` (the curve probe of `../probes/probe2.py`,
seeded). Result: every set has full rank and passes; no violation. Tag: **[PROBE]** (mod p never
concludes; the exact full ranks make these sets Ramsey only through the [HAND] C-24). Scope:
`TRANSCENDENTAL_PARAM(t)`. Runtime: 75 s. Log: `expected/rankN_sweep.log`. Dependencies:
`../probes/probe2.py`, `../probes/validate.py`, `../probes/c22_controls.py` and
`../probes/c23_count_law.py` (which import `../probes/c13_c22_seven.py`); these [PROBE] modules
live in the sibling `probes/` directory, not here, and the expected log was produced against them.

### The non-Ramsey side

**`dual_cert.py`** — J2-F7: three rational points (`t = 0, 1/2, 1/3`) plus four points with
algebraically independent stereographic parameters `T1..T4` on a circle are not Ramsey. All in the
field `Q(T1, ..., T4)` (sympy fraction field): [1] the configuration; [2] the 2-jet linear system,
built exactly; [3] CERT-M, a matrix-weight dual vector with `y^T A = 0` and
`y^T b = 1/((T1-T2)(T1-T3)(T1-T4)) != 0`; [4] CERT-S, Pálvölgyi's scalar weights with the
derivation `D = sum_m g(T_m) d/dT_m`, `g(t) = t (t - 1/2)(t - 1/3)`: the hypotheses of Lemma A.1
hold exactly with energy `E = 4`, and the same data is a 2-jet dual vector; [6] a control
(3 rational + 3 independent: the system is consistent, no dual certificate); [7] CERT-S with the three
rational parameters replaced by symbols R1, R2, R3; [8] the generic-rank route. Check [5] compares with the mod-p matrix of
`probe2.jet2` at seeded points; it is a consistency check, **[PROBE]**, and not part of any proof.
Glue (in the note): Lemma A.1 (re-derived, reviewed (AI)) with EGMRSS I, Lemma 15, turns CERT-S into
non-Ramsey with no further input; CERT-M needs Proposition J2 as well. The statement is an
instance of Pálvölgyi's Theorem A.3. Tag: **[CERT]**. Scope: `GENERIC_OF(3 rational + 4
independent)`; a concrete member is `(T_m) = (e^√2, e^√3, e^√5, e^√7)` (Lindemann–Weierstrass).
Runtime: 130 s. Log: `expected/dual_cert.log`. Dependencies: sympy;
`../probes/probe2.py` and `../probes/validate.py` (for [5] only).

**`scalar_exact.py`** — Theorem NR-S23: on S², `m` named rational points plus `j` points with
algebraically independent stereographic coordinates are not Ramsey for
`(m, j) = (6,4), (5,5), (4,6), (3,7)`, nor are ten points with all coordinates independent; on S³,
`(m, j) = (11,4), (10,5)`. With homogeneous lifts, the weights `lambda~(u)` and the derivation
`z(u)` are cofactor vectors of polynomial matrices `M_L(u)`, `M_W(u)`, so they solve the
certificate conditions **identically** in the free coordinates (Laplace). At one rational point
`u = tau` the script checks exactly that both matrices have full rank, that `lambda~_i(tau) != 0`
for every generic point, and that the energy `E(tau)` is a nonzero rational; it then checks
Pálvölgyi's three conditions and `E` in the inhomogeneous coordinates at `tau`, and the same data
as a dual vector of `probe2.jet2`'s exact layout. Glue (in the note, and in the script's
docstring): full rank at `tau` makes the cofactor vectors nonzero there; `E(tau) != 0` with all
`lambda~_i(tau) != 0` gives `E != 0` in the coordinate field `F`; then Lemma A.1 with EGMRSS I,
Lemma 15 (no J2 needed), or alternatively the 2-jet dual and Proposition J2, gives non-Ramsey in
every dimension. Supersets of these cells are non-Ramsey too. Tag: **[CERT]** identities plus glue,
reviewed (AI). Scope: `GENERIC_OF(independent free coordinates)`, with the rational points named in
the script (they replay `../probes/e1_s2.py`'s and `e1_s3.py`'s seeded rational points exactly).
The **S⁴ threshold cell (17, 4) is not certified**: the (P) system there has a second, identically
vanishing row relation, so the script reports "no exact certificate of this shape in 50 attempts
(inconclusive)" for it, and the last line is `all certified: False` with exactly that entry
`False`; this is expected (the S⁴ cell is [PROBE] only). **Fixes applied to this copy, as asked by
the review of its glue:** (a) the code check now requires `lambda~_i(tau) != 0` for **all** generic
points, not only those with `w_i(tau) != 0` (`if any(lam[i] == 0 for i in gen): continue`, was
`... for i in active`), and the printed line now reports it ("lambda~_i(tau) != 0 for all j
generic points"); every cell is certified at the same `tau` as before and all checks hold; (b) the
docstring now says that the code computes an RREF kernel vector at `tau`, which equals the cofactor
vector up to a factor `kappa` in `Q^x`, so that `E(tau)` scales by `kappa'^2 / kappa` and its
nonvanishing is unaffected (it previously spoke of the cofactor vectors as if computed); (c) the
second route is cited as Pálvölgyi's Lemma A.1 with EGMRSS I, Lemma 15 (it was cited as "Thm
A.3"). Runtime: 58 s. Log: `expected/scalar_exact.log`. Dependencies: none beyond the
standard library.

### Definable colourings

These scripts concern the dual question: which **colourings** of R^D avoid a monochromatic copy of
a given set. They give exact certificates that specific colourings do **not** avoid the radian
9-gon `E_1 = {(cos k, sin k) : 0 <= k <= 8}` (which is not Ramsey by Theorem D and
Lindemann–Weierstrass). The general statements, C-25 (Graham holds trivially for colourings
definable in an o-minimal structure, by the big-ball lemma) and C-26 (polynomial-factor colourings,
via Dol'nikov–Karasev, non-effective), are **[HAND]**, reviewed (AI), and are stated in the note as
a remark; the scripts are exact sanity checks of them on samples, and C-27 is a working hypothesis
tested on a sample.

**`definable_bigball.py`** — 32 colourings of R^D (D = 2..4) given by sign vectors of random
polynomials with coefficients in `Q[tan(1/2), e, cos 1]`, plus one colouring defined with `exp`. For
each, it picks an integer direction `w` where every leading form is nonzero and certifies, by exact
rational interval arithmetic (`exact_intervals.py`), that every polynomial has constant sign on the box
`R w + [-1, 1]^D`; so the box contains a monochromatic unit ball and the explicit monochromatic copy
`x_k = R w + (cos k, sin k, 0, ...)` of `E_1`. Result: 32/32 certified. Tag: **[CERT]** for each
printed instance (the interval bounds are proven enclosures); for C-25 it is a sample check of the
derivation, and the theorem is [HAND]. Scope of the instances: the listed colourings (their
parameters are transcendental constants; the configuration `E_1` is
`TRANSCENDENTAL_PARAM(tan(1/2))`). Runtime: 9 s. Log: `expected/definable_bigball.log`.
Dependencies: `exact_intervals.py`.

**`definable_polyphase.py`** — Part A: an exact sympy identity, the quartic `sum_{i<=5} x_i^4` is
constant (3/10) on a 5-point circle 4-design, so every colouring `f(P)` with the listed `P` is
constant on an explicit copy of `E_1` (an instance of C-26; **[CERT]** for the identity). Part B:
30 seeded polynomial-phase colourings `chi(x) = floor(r * frac(P(x)))` of R³ (r = 2, 3; deg P <= 3;
coefficients in `Z[tan(1/2)]`); for each, floating point proposes a copy `c + Q (cos k, sin k, 0)`
(Q a rational orthogonal matrix from a Cayley transform, c in (1/100) Z³), and exact rational
interval arithmetic certifies that every `P(x_k)` lies strictly inside one colour window. Result:
30/30 certified. Tag: **[CERT]** for each printed instance (floating point only proposes); as
evidence for the hypothesis C-27 it is a sample, **[PROBE]**. Runtime: 403 s (slow
set). Log: `expected/definable_polyphase.log`. Dependencies: numpy, sympy, `exact_intervals.py`. (The
working copy also wrote its log to a side file; this copy only prints it.)

**`definable_crosscheck.py`** — re-parses the 30 certified copies from `definable_polyphase.py`'s log
(by default `expected/definable_polyphase.log`, or a path given as the first argument) and
re-verifies them without `exact_intervals.py`: the orthogonal frame exactly (sympy rationals), and the
pairwise distances and the colour windows at 60 digits (mpmath, margin `> 1e-40`). Tag: a
consistency check of the exact certificates, **[PROBE]** (it does not replace them). Runtime:
5 s. Log: `expected/definable_crosscheck.log`. Dependencies: sympy, mpmath.

### Quadric corank and the 2-jet dual (ledger SR-C29 to SR-C34; added in v1.1.0)

These scripts need python-flint (0.9.0 was used) in addition to sympy. Their ledger entries were
filed before the scripts ran. Every configuration is given by rational stereographic coordinates
(projection from (0, ..., 0, 1)); first-order derivation data are rational tangent vectors.

**`corank_exact.py`** — exact computations over Q (python-flint `fmpq_mat`, sympy for null spaces and
Gröbner bases), one subcommand per entry. `c29`: the quadric evaluation matrix (rows `vec(p_i p_iᵀ)`)
has full rank at `D_d = (d+1)(d+2)/2 − 1` seeded rational points of S^{d−1} for d = 3..8, at 7 seeded
rational points of S² and at the rational points `R_2` of Theorem NR-S23 plus 3 more; since
specialization does not raise rank, the generic member of each family has quadric corank 0, and
OpenAI's quadratic criterion (Prop. 7.3 of result 172, Lean `spherical_quadraticIndependent_ramsey_all`)
applies (SR-C29; the genericity glue is in the ledger entry, reviewed once by an AI agent). `c30`: the
minimal cell (N(d) − 4, 4) of the phase diagram for d = 3..7 (an embedded S² cell and seeded
general-position instances): quadric corank 1, nonzero weights at the four free points, rank of the
conformal-Killing pairing matrix `4d − 6`, a two-dimensional kernel and a nonzero energy form on it
(the Lemma A.1 data), plus two three-free-point controls with no certificate (SR-C30). `c31`: the exact
2-jet dual dimension and trace pairing at θ = 0 for 19 (d, N, k) rational-affine families × 2 seeds on
S¹, S², S³, compared with the corank law (SR-C31); a verdict marked `?` is undecided at that
specialization (coincident points there, dual dimension above the generic bound, or pairing zero) and
is not counted as agreement or mismatch: three families, (d, N, k) = (3, 13, 2) seed 1, (2, 7, 2) seed 1
and (2, 7, 3) seed 0, have coincident points at θ = 0 and decide as predicted at other rational points
(`c31_respecialize.py`; (2, 7, 2) seed 1 at 2 of 3, the third again having coincident points). Every
family is checked to be injective (its generic member has distinct points), and every fixed rational
configuration to have distinct points. **Checked
condition:** every test point of `c31`, `c32` and `../probes/c34_test.py` has maximal quadric rank there
(κ = N − D_d; the printed κ shows it), which the specialization arguments need. `c32`: two (κ, k) = (3, 4) and two (4, 3)
families on S² whose 2-jet dual is nonzero with nonzero pairing at the generic lower bound (2-jet FAIL)
and whose scalar (Lemma A.1) locus is empty: the maximal minors of the pairing matrix in the relation
coordinates generate a zero-dimensional homogeneous ideal over Q (SR-C32). Tag: **[CERT]** per
instance (exact ranks, dimensions and Gröbner bases at one rational specialization) plus written
specialization glue (in the ledger entries; reviewed by one non-author AI agent for SR-C32 and the dual formulation of SR-C31; and, once each, for SR-C29 and SR-C30). Scope: `GENERIC_OF` the seeded rational
families. Runtimes: 4, 10, 26, 27 s. Logs: `expected/corank_exact.c29.log` … `.c32.log`.

**`c31_respecialize.py`** — the three families of `corank_exact.py c31` that were undecided at θ = 0
(coincident points there), re-specialized at three seeded rational points each: all decide as predicted. Tag: **[CERT]**
per instance, as above. Runtime: 5 s. Log: `expected/c31_respecialize.log`.

**`c34_det16.py`** — the non-Ramsey side of the one-parameter threshold 16 on S² (SR-C34), by Theorem
D's method: for the two N = 16 one-parameter families of `../probes/c34_test.py`, the 16 × 16
evaluation matrix `[p_ia(T) p_ib(U)]` has nonzero determinant at two rational points (T, U), hence in
Q(T, U), so condition (1) forces P = 0. Tag: **[CERT]** per instance (glue: the argument of Theorem D).
Scope: `TRANSCENDENTAL_PARAM(T)` for those two families. Runtime: 5 s. Log: `expected/c34_det16.log`.

### Helper module (no expected log of its own)

**`exact_intervals.py`** — exact interval arithmetic over Fractions: rational enclosures of `cos q`,
`sin q`, `exp q` (q rational) and `tan(1/2)`, with Lagrange remainder bounds, so that "0 is not in
I" and "I lies inside a window" are exact certificates. Used by `definable_bigball.py` and
`definable_polyphase.py`; it has no `__main__`.

## Changes from the working copies

Only comments, docstrings, printed labels, file paths and the one `scalar_exact.py` check above
were changed; no computed value changed. Every script was re-run here and its output compared with
the working copy's log; the only differences are the relabellings below and the `scalar_exact.py`
line above.
- Printed labels: the non-two-group sets are labelled `W7`, `W8` and `radian 7-gon`, as in the note's
  Theorem NTG; one control of
  `exact_circle_cert.py` is labelled `[Ramsey, B(b)]`; the slow radian 7-gon label says
  "slow: 25-40 min" (the measured time of `cert_nontwogroup.py --slow` is 37-47 min; see the table); a heading of `rankN_check.py` says "from the cold review".
- Imports: scripts that import a sibling insert their own directory on `sys.path` (needed under
  `python -I`); `dual_cert.py` and `rankN_sweep.py` also insert `../probes`.
- `definable_bigball.py` and `definable_polyphase.py` no longer write a side copy of their log;
  `definable_crosscheck.py` reads the log from `expected/` or from its first argument.
- `cert_clifford_crosscheck.py`: its docstring and header were rewritten (it was a reviewer's
  scratch script); the code is unchanged.
