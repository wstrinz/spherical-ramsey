# probes/: the 2-jet probe harness. [PROBE] evidence, not proof

Every 2-jet and curve-probe verdict in this directory is computed **modulo a prime with a random
specialization**. The exact parts (`realness.py`, and the parts of the `c*.py` scripts marked EXACT
below) are labelled as such. A mod-p result never concludes anything: a Ramsey or non-Ramsey statement
supported only by these logs is `[PROBE]` evidence, never a theorem. The probes are the exploration
that pointed at the exact results in `../certificates/` and the statements in `../note/`; the
status of every claim is in the ledger (`../ledger/`).

**Conjecture numbers.** `C-n` in these scripts, their output and this file is entry `SR-Cn` of the
conjecture ledger (`../ledger/LEDGER.md`).

## What the 2-jet test is

Setup (`probe2.py` docstring): a finite set of points on the unit sphere S^{d-1} in R^d, in the
coordinates p_i = (1, a_i), whose coordinates are rational functions (optionally with square roots)
of k algebraically independent transcendental parameters θ_1..θ_k, with derivations D_j = ∂/∂θ_j.
The Euclidean-Ramsey field criterion asks for a matrix solution P(T, U) of an evaluation system.
Taylor-expanding a solution at the diagonal U = T + e, with P_0 = c·S and S = diag(−1, I_d), gives
the **2-jet system** in the unknowns c, P_j (j < k, full (d+1)×(d+1)) and Q_jl (j ≤ l, symmetric):

- order 1: p_iᵀ P_j p_i = 0;
- order 2: −c⟨D_j a_i, D_l a_i⟩ + p_iᵀ P_j D_l p_i + p_iᵀ P_l D_j p_i + p_iᵀ Q_jl p_i = 0.

The test **PASSes** if this linear system is solvable with c = 1 and **FAILs** otherwise.

**Status of the derivation.** The derivation is by hand (`[HAND]`). It has had one cold review, by
an AI model, not by a human. That review re-proved the direction used here, "Ramsey ⇒ the 2-jet
system is solvable with c = 1", via the Taylor ring map B → F[e]/(e)³, checked the order-1 and
order-2 coefficients (signs, the ½, c = 1) by hand and with exact sympy computations, and found only
slips that change no verdict. So:

- a 2-jet FAIL means non-Ramsey **only through that hand derivation** (AI-reviewed, not
  human-reviewed), **and** only if the mod-p FAIL is itself certified (next section), which these
  probes do not do;
- a 2-jet PASS never shows Ramsey. The 2-jet test is a necessary condition. That it is also
  sufficient is conjecture C-1 (open); e4_six's comparison with the full one-parameter criterion is
  [PROBE] evidence for it.

**Curve probe** (`curve_probe`). Restrict to U = T + e·w along a random direction w, compute the
limit kernel with power series truncated at order N = 12, and test whether I_d lies in its spatial
projection. For k = 1 this is the full criterion (the review agrees); for k ≥ 2 it is a further
necessary test. The truncation order is a heuristic, not a certified bound.

`jet2_reduced` is the 2-jet test when many algebraic points are also present (enough to force
Q_jl ~ S and sym(P_j) ~ S); only antisymmetric parts survive, and only the transcendental points are
passed in.

## Arithmetic: mod p with random specialization

- The prime is p = 2³¹ − 1 by default. The environment variable `PROBE_PRIME` overrides it; it is read
  once, when `probe2` is first imported, and must be an odd prime below 2^31.5 (asserted; this keeps
  the int64 products in `rank_mod` exact). For p ≡ 1 (mod 4) square roots use Tonelli–Shanks,
  deterministic in the argument, so mirror pairs stay consistent.
- Each parameter θ_j is specialized to a random residue; first-order jets (`J`) carry D_j, power
  series (`PS`) carry e. Ranks are computed over F_p.
- Specialization never raises a rank. A spurious FAIL is a drop in rank(A) without a drop in
  rank[A|b]; a spurious PASS is rank[A|b] dropping to rank(A). A specialized FAIL becomes rigorous
  only when (1) the specialization is a genuine ring map on all entries (denominators nonzero,
  algebraic generators sent consistently to roots of their minimal polynomials) and (2) the
  specialized rank of A equals a certified upper bound on its generic rank (for example an explicit
  kernel of the complementary dimension), or when an exact symbolic dual certificate is given.
  Exact certificates of that kind are in `../certificates/`, not here.
- A configuration whose square-root radicands are not jointly residues at p cannot be specialized at
  p at all; see `NO_VERDICT` below.

## Hygiene (read before citing any count)

- **Seeded.** Every driver passes an explicitly seeded `random.Random` as `rng=` to the tests, separate
  from the stream that builds configurations, so every count in `expected-v2/` reproduces exactly.
- **`NO_VERDICT` is never PASS, never FAIL and never agreement.** `validate.retry` retries a test while
  it raises `ValueError` (a square root of a nonresidue mod p). If every attempt raises it returns
  `NO_VERDICT`; `MIXED{True, False}` is reserved for a genuine split between trials. The attempt cap
  scales with the number of square-root points (points tagged `f.is_sqrt = True`):
  min(max(200, 20·2^m), 20000). Every driver prints a `# retry tally:` line with PASS / FAIL /
  NO_VERDICT / MIXED counts per test function, and `e4_six` counts decided pairs separately.
  `retry` catches every `ValueError`, including numpy's `AxisError` when k = 0: the j = 0 cells of
  the `e1_phase` table are `N` for that reason, not a residue reason.
- **The 15 `NO_VERDICT`s of e4_six are deterministic at p = 2³¹ − 1.** Each contains square-root
  points whose radicands multiply to a rational constant times a square, with the constant a
  nonresidue mod p; no number of attempts helps. A prime at which the constants are residues
  (`PROBE_PRIME`) decides them.
- **Use `probe2.div`, never `/`, on plain integers.** Integer `/` silently produces floats.
- **Rotate away from the stereographic pole (−1, 0).** A point at the pole makes the stereographic
  parameter undefined (`e5b.py` re-projects from (0, 1) for this reason).
- The first two traps once produced false PASSes. A new probe should reproduce `validate.py`'s
  controls before its output is cited.

## The realness filter (`realness.py`)

e4_six's sampler draws an independent Möbius x(t) for every square-root point (x, ±√(1 − x²)). With
several such points on one parameter, the intervals where |x| ≤ 1 often do not intersect, and the
configuration then has **no real member with t transcendental**: it is out of scope for any
statement about real point sets, even though the mod-p tests still return a verdict for it.

`realness(specs, k)` decides this **exactly over ℚ**: a configuration is real iff, for each parameter,
some open interval has every radicand positive (identically-zero radicands excepted). It tests a
rational point in each interval between consecutive rational roots. A float grid is an independent
cross-check (0 mismatches over the 1,550 generated configurations). The module also does the
square-class algebra (F₂ elimination on ℚ(t)*/ℚ(t)*², constants included) behind the 15 deterministic
`NO_VERDICT`s.

Wiring:
- `python -I realness.py` replays e4_six's configuration stream (`Random(23)`, identical consumption)
  and prints the 15 `NO_VERDICT` configurations with their obstructions, then a census: **507 of the
  1,557 e4_six configurations are not real**, by section. 3 of the 15 `NO_VERDICT` configurations
  are real; 12 are not.
- `python -I realness.py --tsv` prints one line per e4_six test, in e4_six's order, with `REAL` or
  `NONREAL`.
- `python -I e4_six.py --real-scope` runs e4_six unchanged and appends one `REAL-SCOPED` line with every
  count restricted to real configurations (log: `expected-v2/e4_six_real.log`).

Any C-1 count taken from e4_six should be the real-scoped one. Every other probe family in this
directory is real by construction (stereographic `circ` / `sph`, rational points, and `palv` with
r ≥ 2).

## Files

| File | Role |
|---|---|
| `probe2.py` | Core: jets `J` and power series `PS` mod p; `rank_mod`, `nullspace_mod`; point constructors (`circ`, `sph`, `rat_circ`, `rand_rat_sphere`, `div`); `jet2` (2-jet test, any dimension), `jet2_reduced`, `curve_probe`. Also imported by `../certificates/` |
| `validate.py` | `retry`, `NO_VERDICT`, `tally_line`, shared point sets (`rats`, `palv`, `indep_circle`); as a script, 8 controls (7 with known verdicts, 1 marked `PASS?`) |
| `e1_phase.py` | Circle: phase diagram over m rational + j independent points |
| `e1_s2.py` | S²: phase diagram over m rational + j independent points |
| `e1_s3.py` | S³: threshold for j = 4, 5 independent points plus m rational |
| `e1_s4.py` | S⁴: threshold for 4 independent points plus m rational (`--slow`) |
| `e3_sphere.py` | Helpers `indep_sphere`, `rat_sphere`; standalone modes `threshold d,..` and `generic d n0 n1` (not in the suite) |
| `e3b.py` | Free-point threshold with `jet2_reduced`, d = 2..9 |
| `e4_six.py` | 6-point hunt (1,107 sets, 1-3 parameters), and the C-1 comparison of the 2-jet test with the full one-parameter criterion, including 450 sets of 7-9 points; `--real-scope` |
| `e5_mobius.py` | Möbius invariance; two and three Möbius groups on S¹ and S² |
| `e5b.py` | Pálvölgyi heptagon under rational and transcendental Möbius maps |
| `e6_wild.py` | Angle progressions 0, θ, 2θ, ... (radian progressions); Poncelet chains; random 3-parameter controls |
| `e7_hopf.py` | Möbius-algebraic groups on S², S³, S⁴ (`--slow`, ~14 min) |
| `realness.py` | **Exact** realness test and square-class algebra for e4_six's configurations (no mod p) |
| `scalar_cert.py` | Scalar (single-derivation) 2-jet certificates, mod p (SR-C11, SR-C12): method R (one fixed derivation) and method A (all derivations at once, for disjoint parameter sets). As a script, the scan of the S¹ controls, the S² cells beyond the threshold, the S³ and S⁴ threshold cells and 9 / 10 generic points on S²; `[PROBE]` only. The exact certificates of the minimal cells are `../certificates/scalar_exact.py` |
| `c13_c22_seven.py` | C-13 / C-22 (seven-point circle sets). Part A **EXACT** (sympy): the 35 cross-ratios of the radian 7-gon are non-constant, so it is not two-group. Part B `[PROBE]`: radian n-gons, n = 6..9. Part C: two-parameter lattice 7-sets; transcendence degree of the cross-ratio field **EXACT** (Jacobian rank 2 at a rational point), two-group test exact for non-constancy and probabilistic for constancy; verdicts `[PROBE]` (the `COUNTER-CANDIDATE` flags are probe-level) |
| `c22_controls.py` | Controls for C-13 / C-22: low-parameter 7-sets (k = 1..4) mixed with rational points; two-group test and transcendence degree as above; verdicts `[PROBE]`. Also a library (`make_spec`, `ev`, `pt_fn`, `DualK`) used by the next two scripts and by `../certificates/` |
| `c23_count_law.py` | C-23 (expected-dimension law on the circle): per configuration, k and the two-group test as above, prediction PASS iff two-group or (n − 5)(k + 1) ≤ 6, compared with the 2-jet test (and the curve probe for k = 1); verdicts `[PROBE]`. `classify` and `mirror_specs` are also used elsewhere |
| `c14_rigid.py` | C-14 (rigid-group absorption) and C-23(ii) at n = 9, k = 1. The 9×9 (2,2)-form determinant at a rational point is an **EXACT** computation; det ≠ 0 there implies non-Ramsey through the circle reduction to (2,2)-forms (a hand-proved argument, see the note), so those lines are exact checks resting on that reduction, not mod-p evidence. The two-group classification is exact for non-constancy; the 2-jet and curve verdicts are `[PROBE]` |
| `c15_c16.py` | C-15 (generic Möbius-group unions on S¹) and C-16 (seven points on S²); `[PROBE]` only |
| `run_all.sh` | Runs the suite into `out/` (or `$PROBE_OUT`) with LF logs; `--slow` adds the slow runs |
| `check.sh` | Diffs `out/` against `expected-v2/`, ignoring timing; non-zero exit on mismatch |
| `expected-v2/` | Reference logs |

## Reference runtimes

Wall-clock times of the `expected-v2/` run (Python 3.10.6, numpy 1.26.4, one core of a desktop PC;
the `real` line of each log):

| Log | Set | Wall clock | Content in one line |
|---|---|---|---|
| `validate.log` | fast | 7 s | 8 controls, all as expected, 2-jet and curve; no `NO_VERDICT` |
| `e1_phase.log` | fast | 5 s | circle grid; 6 `N` cells at j = 0 (k = 0, see Hygiene) |
| `e1_s2.log` | fast | 28 s | S² grid: 47 P, 16 F |
| `e1_s3.log` | fast | 17 s | S³: first FAIL at n = 15 for j = 4 and j = 5 |
| `e3b.log` | fast | 7 s | PASS for j ≤ 3, FAIL at j = 4, every d = 2..9 |
| `e5_mobius.log` | fast | 69 s | Möbius invariance and group checks |
| `e5b.log` | fast | 4 s | heptagon FAILs under all three maps |
| `e6_wild.log` | fast | 11 s | angle progressions PASS up to 8 points, FAIL from 9; Poncelet chains |
| `e4_six.log` | fast | 5 min 6 s | 1,557 configurations; 0 six-point FAILs; 1,144 decided comparisons, 0 disagreements; 15 `NO_VERDICT` |
| `realness.log` | fast | 21 s | exact: 507 of 1,557 configurations not real |
| `e1_s4.log` | slow | 29 s | S⁴: first FAIL at n = 21 |
| `e4_six_real.log` | slow | 5 min 37 s | real-scoped: 702 comparisons, 701 decided (634 PASS/PASS, 67 FAIL/FAIL), 0 disagreements |
| `e7_hopf.log` | slow | 13 min 38 s | two groups PASS on S², S³, S⁴; three groups FAIL on S², S³ |
| `c13_c22_seven.log` | fast | 36 s | radian 7-gon not two-group (exact); radian 6-8-gons PASS, 9-gon FAIL; all 46 lattice 7-sets: trdeg 2, not two-group, 2-jet PASS |
| `c22_controls.log` | fast | 1 min 32 s | low-parameter 7-sets; 2-jet FAIL only at transcendence degree ≥ 3 (44 sets), curve probe PASS throughout (necessary-only for k ≥ 2) |
| `c23_count_law.log` | fast | 1 min 8 s | 0 mismatches with the C-23 prediction over 8 families |
| `c14_rigid.log` | fast | 50 s | 0 C-14 mismatches; 119 + 57 exact det ≠ 0 non-Ramsey instances |
| `c15_c16.log` | fast | 13 s | every C-15 / C-16 prediction matched by the 2-jet test |
| `scalar_cert.log` | fast | 1 min 18 s | a scalar certificate (method A) at every failing cell, none at the passing cells; random fixed derivations miss them (method R), as expected |

Fast suite about 10–14 min in total; `--slow` adds about 20 min. All verdicts are mod-p `[PROBE]`
results; `realness.log` and the lines marked EXACT in the `c*` logs are exact computations.

## Reproduce

```
cd probes
bash run_all.sh            # fast suite into out/, about 10-14 min
bash check.sh              # expected: "check: all logs match expected-v2"; exit 1 on any difference
bash run_all.sh --slow     # fast suite + e1_s4, e4_six --real-scope, e7_hopf: about 34 min
bash check.sh              # now also checks the slow logs
```

Needs Python ≥ 3.10, numpy, and sympy (for the `c*.py` scripts). Scripts run as `python3 -I` (set `PYTHON=python` if your interpreter
has another name); each driver puts its own directory on `sys.path`, so `-I` is safe. Logs are
written with LF line endings. `check.sh` ignores the `real/user/sys` lines, the per-line `(Ns)`
timings of `e1_s4` and `e7_hopf`, and carriage returns; everything else, including every count and
every `NO_VERDICT`, must match. `PROBE_PRIME=<p> bash run_all.sh` runs the suite at another prime;
its logs are not expected to match `expected-v2/` line for line (the specialization points change,
and so do the `NO_VERDICT` counts).
