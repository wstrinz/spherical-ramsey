# Spherical Ramsey conjecture ledger

The open problems, partial results and refuted guesses that accompany the note *Two Möbius groups
suffice* (`note/` in this release). Every entry has a stable id, a status, the strongest artifact
behind it, and a starting state that a reader can replay. Refuted entries are kept, with the sample
that killed them. The format, status vocabulary and warrant rules are in `README.md`; the YAML
headers are collected in `ledger.yaml`; statement-only Lean stubs for six entries are in
`lean/SphericalRamseyConjectures.lean`; the open threads are in `BACKLOG.md`.

**Count (28 entries).** proved: 6 (SR-C2, SR-C10, SR-C14, SR-C24, SR-C25, SR-C26); refuted: 2
(SR-C13, SR-C22); consistent-on-sample: 5 (SR-C15, SR-C16, SR-C19, SR-C23, SR-C27); open: 15. Four
further refuted or withdrawn guesses with no entry of their own are listed under *Tailings* at the end.

**Reading the warrants.** `[LEAN]`: proved in Lean 4 and checked by Comparator. `[CERT]`: an exact
symbolic identity (sympy, over ℚ or ℚ(T)) plus written glue that is not machine-checked. `[HAND]`: a
complete written argument, not machine-checked. `[SKETCH]`: an outline. `[PROBE]`: computational
evidence, usually random specialization modulo a prime near 2³¹; never a theorem. **Every review
mentioned in this ledger was carried out by an AI agent that did not write what it reviewed; no human
expert has reviewed any entry.**

**Conventions.** "Ramsey" is OpenAI's notion (openai/math `fd4aeeb2`, result #172): for every r there is
D such that every r-colouring of ℝ^D contains a monochromatic congruent copy. Points on a circle are
given by stereographic parameters, `circ(t) = ((1 − t²)/(1 + t²), 2t/(1 + t²))`, after a rational
rotation that moves the pole (−1, 0) off the set. "Two-group" means a union of two Möbius images of
finite sets with algebraic coordinates. The *cross-ratio field* of a cyclic set is the field generated
over ℚ by all its four-point cross-ratios; it is a Möbius invariant. Scope tags name the type of the
coordinates over ℚ: `ALGEBRAIC`, `GENERIC_OF(…)`, `TRANSCENDENTAL_PARAM(…)`, `MOBIUS_ORBIT_OF(…)`,
`ANY`, and, where needed, `REGULAR(F/ℚ)` (ℚ algebraically closed in the coordinate field F). "Real" is
never a scope: the verdict can change between algebraic and transcendental members of one real family.

**Replay.** Paths are relative to the release root. Exact scripts: `python -I certificates/<script>`.
Modulo-p probes import their siblings: `cd probes && python <script>`. Expected outputs are next to the
scripts (`certificates/expected/`, `probes/expected-v2/`); compare ignoring timing lines. Python 3.10,
numpy 1.26, sympy 1.14, mpmath 1.3.

---

## Proved

### SR-C2: the two-group theorem in every dimension

```yaml
id: SR-C2
title: Two Möbius groups suffice, every d >= 2
status: proved
warrant: "CERT + written glue for d <= 6; HAND for every d >= 2; reviewed by AI agents only"
scope: "MOBIUS_ORBIT_OF(ALGEBRAIC) x 2"
difficulty: "engineering (a dimension-uniform Lean proof)"
lean_stub: "lean/SphericalRamseyConjectures.lean#C2_two_group"
fc_category: "research open (until a proof is public and accepted)"
ams: ["05D10", "51B10", "52C10"]
replay: ["certificates/cert_s2.py", "certificates/cert_s2_quat.py", "certificates/g4_test.py", "certificates/cert_clifford.py", "certificates/cert_clifford_seed.py", "certificates/cert_clifford_crosscheck.py"]
note: "Theorem C2"
history: ["2026-10-12 filed as a conjecture", "2026-10-12 proved: CERT for d <= 5, then d = 6, HAND for every d"]
```

- **Statement.** Let d ≥ 2, let A₁′, A₂′ ⊂ S^{d−1} be finite sets with real algebraic coordinates,
  and let ν₁, ν₂ be Möbius transformations of S^{d−1} (orientation-reversing ones allowed). Then
  ν₁(A₁′) ∪ ν₂(A₂′) is Ramsey. There is no bound on |A₁′| or |A₂′|. ("Two groups" means two Möbius
  maps; this is unrelated to Kříž's results on soluble symmetry groups acting with at most two orbits,
  see Behague, arXiv:2510.15677.)
- **Status and evidence.** For d ≤ 6 every identity the proof needs is checked as an exact polynomial
  identity: complex graph forms for S¹ and S², quaternionic for S³ and S⁴, a Clifford-algebra (Vahlen
  normal form, Lipschitz group) certificate in Cl₀,₄ for S⁵; algebraic seeds by a separability
  idempotent. For every d the argument is written out (pairing lemma, Lipschitz lemma, Vahlen
  identities, vanishing, coverage of every Möbius map via Cartan–Dieudonné); its identity families are
  cross-checked on exact random instances through d = 8. Adversarial AI reviews found the glue and the
  all-d argument correct, with wording fixes applied.
- **Falsifier.** A two-group configuration that fails the second-order test (SR-C1's necessary half,
  which is reviewed), confirmed exactly; or a failing exact identity in the cross-check for some d ≤ 8.
- **Starting state.** `python -I certificates/cert_s2.py` (about 2.3 min), `cert_s2_quat.py` (1–2 min),
  `g4_test.py`, `cert_clifford.py` (54–63 min), `cert_clifford_crosscheck.py`.
- **Difficulty.** Done at HAND level. Open: a single Lean statement uniform in d over Mathlib's
  `CliffordAlgebra` (the even-n orientation step must be done inside the family), and three groups
  (SR-C15).
- **Lean.** `C2_two_group` (statement only).
- **Links.** Theorem C (Möbius invariance), published: mobius-ramsey v1.0.0,
  doi:10.5281/zenodo.23339523. Related: SR-C4, SR-C13, SR-C15, SR-C23.

### SR-C10: the radian 8-gon

```yaml
id: SR-C10
title: Eight consecutive multiples of any angle form a Ramsey set
status: proved
warrant: "HAND (via SR-C24) + exact rank computation; reviewed by one AI agent only"
scope: ANY
difficulty: "attackable (an explicit certificate would upgrade it to CERT)"
lean_stub: "lean/SphericalRamseyConjectures.lean#C10_radian_eight"
fc_category: "research open (until a proof is public and accepted)"
ams: ["05D10", "52C10"]
replay: ["certificates/rankN_check.py"]
note: "Corollary (the radian 8-gon)"
history: ["2026-10-12 filed (probe evidence)", "2026-10-13 proved via SR-C24 and an exact rank"]
```

- **Statement.** For every θ such that the eight points are distinct, {(cos kθ, sin kθ) : 0 ≤ k ≤ 7} is
  Ramsey.
- **Status and evidence.** If e^{iθ} is algebraic, by the algebraic-coordinates theorem (prior work,
  Lean-checked). Otherwise t = tan(θ/2) is transcendental and the 8 × 8 matrix N of SR-C24 has rank 8,
  computed exactly at t = 2/7 and t = −5/11 (specialization does not raise rank). The reviewer
  re-verified the rank at a third point (t = 3/13) and, by an independent π-adic computation at
  T = 2/7, found a kernel element whose reduction is proportional to (s − s′)². This proves that a
  certificate exists; it does not exhibit one.
- **Dependence.** SR-C24 (`[HAND]`, AI-reviewed) and rank N = 8 at one rational value of t (two were
  computed).
- **Contrast.** Nine consecutive multiples are Ramsey iff e^{iθ} is algebraic (Theorem D, `[LEAN]`,
  Lean-checked, rope AV3). With the radian 7-gon (SR-C13), this shows Theorem D is sharp: for transcendental e^{iθ}
  the progression is Ramsey with seven and eight points and not with nine.
- **Falsifier.** A gap in SR-C24. Independently: the direct exact certificate search
  (`python -I certificates/exact_circle_cert.py "radian 8"`) returning NON-RAMSEY.
- **Starting state.** `python -I certificates/rankN_check.py` (seconds).
- **Difficulty.** Attackable: an explicit certificate. The direct search was stopped after more than
  40 minutes (the radian 7-gon took 25); try kernel interpolation or z = e^{iθ} coordinates.
- **Lean.** `C10_radian_eight` (statement only).

### SR-C14: rigid-group absorption on the circle

```yaml
id: SR-C14
title: One rigid five-point group forces the two-group structure
status: proved
warrant: "HAND for regular coordinate fields; reviewed by one AI agent only; CERT instances"
scope: "REGULAR(F/Q)"
difficulty: "attackable (extension to algebraic seeds)"
lean_stub: "lean/SphericalRamseyConjectures.lean#C14_rigid_absorption"
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["probes/c14_rigid.py"]
note: "Theorem (rigid-group absorption)"
history: ["2026-10-13 filed with a proof sketch", "2026-10-13 proved after review (fixes applied)"]
```

- **Statement.** Let A be a finite subset of the unit circle centred at 0 whose coordinate field F is
  regular over ℚ, and suppose some five points of A have all their cross-ratios rational. Then A is
  Ramsey iff A = G ∪ H with all cross-ratios within G and all within H rational, that is, iff A is a
  union of two Möbius images of rational sets.
- **One-parameter form.** Five rational points plus circ(r₁(t)), …, circ(r_j(t)), with t transcendental
  and rᵢ ∈ ℚ(t), are Ramsey iff among the non-constant rᵢ there are at most three, or all their
  cross-ratios are constant in t.
- **Status and evidence.** Proof: a Ramsey certificate is a (2,2)-form f over F ⊗ F; the Möbius graph
  g_G of the rigid group divides f (degree count), the other factor vanishes on the remaining points,
  and is itself a Möbius graph once three or more points remain. Reviewed (AI) as correct, with two
  fixes applied. Sample: 139 seeded one-parameter sets with five rational points; the 119 that are not
  two-group have an exactly nonzero 9 × 9 evaluation determinant (hence non-Ramsey, `[CERT]` per
  instance), the other 20 are two-group (Ramsey); 0 mismatches.
- **Falsifier.** A gap in the proof; or a non-two-group instance that passes the full one-parameter
  criterion.
- **Starting state.** `cd probes && python c14_rigid.py` (about 30 s).
- **Difficulty.** Attackable: the same statement with "algebraic" in place of "rational" for arbitrary F
  (should need the idempotent transport used for algebraic seeds in SR-C2).
- **Lean.** `C14_rigid_absorption` (statement only).

### SR-C24: the rank criterion for one-parameter cyclic sets

```yaml
id: SR-C24
title: Rank criterion for one-parameter cyclic sets of at most eight points
status: proved
warrant: "HAND; reviewed by one AI agent only"
scope: "transcendence degree 1, F regular over Q"
difficulty: "attackable (generalizations)"
lean_stub: none
fc_category: "research open"
ams: ["05D10", "52C10", "12F20"]
replay: ["certificates/rankN_check.py", "certificates/rankN_sweep.py"]
note: "Theorem (rank criterion)"
history: ["2026-10-13 filed with a sketch, before its falsifier ran", "2026-10-13 proved after review (fixes applied)"]
```

- **Statement.** Let A ⊂ S¹ with 5 ≤ n = |A| ≤ 8 have coordinate field F of transcendence degree 1,
  regular over ℚ. Fix t ∈ F transcendental, δ = d/dt, let sᵢ be the stereographic parameters and
  δᵢ = δ(sᵢ), and let N be the n × 8 matrix over F with rows (δᵢ, δᵢsᵢ, δᵢsᵢ², 1, sᵢ, sᵢ², sᵢ³, sᵢ⁴). If
  rank N = n, then A is Ramsey.
- **Status and evidence.** Proof via the limit criterion at the diagonal discrete valuation ring of
  F ⊗ F: the reduction of the lattice of vanishing (2,2)-forms has dimension ≥ 9 − n, its forms vanish on
  the diagonal, and the order-one expansion maps the non-(s − s′)² part into the projection of ker N.
  Reviewed (AI) as correct; the reviewer supplied the simplification used in the note. Falsifier run
  before the review: Pálvölgyi's non-Ramsey heptagon has rank N ≤ 6 exactly for every value of its
  parameter (every point satisfies δ = −s(1 + s²)/(2r), which gives two explicit kernel vectors);
  185 seeded one-parameter rational sets (n = 6, 7, 8; 40 of them mirror-symmetric) all have exact full
  rank and all pass the full criterion `[PROBE]`.
- **Falsifier.** An exact non-Ramsey instance with n ≤ 8 and rank N = n.
- **Starting state.** `python -I certificates/rankN_check.py` (seconds); `python -I
  certificates/rankN_sweep.py` (about 1 min).
- **Difficulty.** Attackable: the reviewer inferred that regularity can be dropped (the local ring at
  the diagonal is a DVR for any finitely generated F of transcendence degree 1); a k = 2 analogue must
  explain the mirror family of SR-C23; one-parameter families on S².
- **Lean.** None.

### SR-C25: Graham's conjecture for o-minimal colourings is trivial

```yaml
id: SR-C25
title: Big-ball lemma for definable colourings (o-minimal folklore)
status: proved
warrant: "HAND (two derivations); reviewed by one AI agent only"
scope: ANY
difficulty: done
lean_stub: none
fc_category: "n/a"
ams: ["05D10", "03C64"]
replay: ["certificates/definable_bigball.py"]
note: "Remark (definable and polynomial-factor colourings), item (a)"
history: ["2026-10-13 proved"]
```

- **Nature.** An observation from o-minimal tameness (van den Dries, *Tame Topology and O-minimal
  Structures*, Ch. 4), not a new result; it is recorded because it scopes SR-C5.
- **Statement.** Let 𝓡 be an o-minimal expansion of the real field (semialgebraic sets with arbitrary
  real parameters, ℝ_exp, ℝ_an, …), D ≥ 2, and ℝ^D = C₁ ⊔ … ⊔ C_r with every C_j definable in 𝓡. Then
  a single class C_j contains balls of every radius, hence a congruent copy of every bounded subset of
  ℝ^D, spherical or not.
- **Status and evidence.** Proof: the union of the boundaries has dimension ≤ D − 1; after compressing
  ℝ^D into the open unit ball, its closure meets the unit sphere in dimension ≤ D − 2, so some truncated
  cone misses every boundary; the cone is connected (D ≥ 2), so it lies in one class, and it contains
  balls of every radius. For semialgebraic classes an elementary leading-form variant gives the same.
  Reviewed (AI): verified, with the single-class (uniformity) wording fixed as above. The script gives
  exact big-ball certificates for random semialgebraic colourings with parameters tan ½, e, cos 1, and
  for one ℝ_exp colouring (a sanity check, not part of the proof).
- **Consequence.** For definable colourings the Ramsey property holds trivially for every bounded
  configuration, and this class cannot
  tell spherical sets from non-spherical ones; it is not a route to SR-C5.
- **Falsifier.** A definable finite colouring of some ℝ^D with no monochromatic ball of radius 1.
- **Starting state.** `python -I certificates/definable_bigball.py`.
- **Lean.** None (Mathlib has no semialgebraic sets at the pinned commit).

### SR-C26: polynomial-factor colourings

```yaml
id: SR-C26
title: Colourings through boundedly many polynomials contain every low-dimensional spherical set
status: proved
warrant: "HAND modulo two cited theorems (Dol'nikov-Karasev, Theorems 1 and 5, read at statement level); reviewed by one AI agent only"
scope: ANY
difficulty: "needs new math (an effective bound)"
lean_stub: none
fc_category: "n/a"
ams: ["05D10", "52A21"]
replay: ["certificates/definable_polyphase.py"]
note: "Remark (definable and polynomial-factor colourings), item (b)"
history: ["2026-10-13 proved"]
```

- **Statement.** For all d, m, k there is N(d, m, k) such that for D ≥ N any P₁, …, P_m ∈ ℝ[x₁, …, x_D]
  of degree ≤ d are simultaneously radial (functions of |x|) on some k-dimensional linear subspace V.
  Hence every colouring f ∘ (P₁, …, P_m), with f : ℝ^m → [r] arbitrary (not even measurable) and any r,
  is constant on every sphere of V centred at 0, and contains a monochromatic congruent copy of every
  finite spherical set of affine dimension ≤ k. The same holds, with a bound N(d, s, m, k), for m
  bracket-polynomial expressions with at most s gates (+, ×, ⌊·⌋) over polynomial leaves of degree ≤ d.
- **Status and evidence.** Apply Dol'nikov–Karasev's Theorem 1 (an even-degree form is proportional to
  |x|^{deg} on a subspace of prescribed dimension) and their Theorem 5 (an odd polynomial map to ℝ^m
  vanishes on such a subspace) to the homogeneous components one at a time, in a decreasing chain of
  subspaces. N is not effective (the cited proofs use topological methods). Reviewed (AI): verified,
  with the dependence N(d, s, m, k) and the effectivity caveat added.
- **Credit.** The ingredients are Dol'nikov–Karasev (arXiv:1009.0392). Bukh–Karasev (*Suborbits in
  Knaster's problem*, arXiv:1212.5351, §2) already link Dvoretzky/Knaster-type theorems to Euclidean
  Ramsey problems, and Gromov's "Hilbert symmetrization" and "Ramsey–Dvoretzky" discussion (*Number of
  questions*, 2014, §1.12) is prior art for the radialisation idea. The only new content is that this
  disposes of the class of candidate colourings. The script checks one explicit exact instance (Σxᵢ⁴ on ℝ⁵).
- **Not covered.** Families whose number of brackets grows with D, for example
  Σ_{i,j} a_{ij} x_i ⌊b_{ij} x_j⌋.
- **Falsifier.** A system (d, m) and D at or above the bound with no such V (it would contradict a
  published theorem).
- **Difficulty.** An effective N needs new math.
- **Lean.** None.

---

## Refuted (kept)

### SR-C13: seven cyclic points are Ramsey iff two-group

```yaml
id: SR-C13
title: Naive seven-point classification by two groups
status: refuted
warrant: "CERT (exact certificates, independently re-checked; the circle glue is that of the six-point theorem, reviewed for these instances by one AI agent)"
scope: "TRANSCENDENTAL_PARAM(t)"
difficulty: done
lean_stub: "lean/SphericalRamseyConjectures.lean#C13_refuted"
fc_category: "research solved (answer False) once public"
ams: ["05D10", "52C10"]
replay: ["certificates/cert_nontwogroup.py", "certificates/exact_circle_cert.py"]
note: "Theorem (non-two-group Ramsey sets)"
history: ["2026-10-13 filed as the naive working hypothesis, before any check", "2026-10-13 refuted at probe level, then exactly"]
```

- **Statement (refuted).** A 7-point subset of a circle is Ramsey iff it is a union of two Möbius images
  of finite algebraic sets (equivalently, iff some four of its points have an algebraic cross-ratio).
- **Counterexamples.** With t transcendental, W₇ = {0, ½, ⅓, t, t + 1, 2t, 1/t} (stereographic
  parameters) and the radian 7-gon {kθ : 0 ≤ k ≤ 6} with e^{iθ} transcendental. For each, an explicit
  (2,2)-form g with coefficients in ℚ(T)[U] vanishes identically at all seven pairs, with g|_{U=T} =
  (s − s′)², re-verified by an independent routine; and none of the 35 four-point cross-ratios is constant
  in the parameter (exact), so the set is not two-group. The 8-point set W₈ = W₇ ∪ {⅔} is a further
  non-two-group Ramsey set.
- **Not claimed.** Only "not two-group". Ramsey sets that are not subtransitive are already known
  (OpenAI #172, Cor. 7.5: Leader–Russell–Walters kites with transcendental parameter), and whether these
  sets are subsoluble is open (Behague, arXiv:2510.15677, Question 6.1).
- **Starting state.** `python -I certificates/cert_nontwogroup.py` (about 36 s for W₇ and W₈; add
  `--slow` for the radian 7-gon, 37–47 min).
- **Lean.** `C13_refuted` states the negation (statement only).
- **Pre-posting gate.** The note states these sets as a `[CERT]` theorem; a review of the glue for these
  instances is still to be done.

### SR-C22: seven points, cross-ratio transcendence degree at least 2

```yaml
id: SR-C22
title: Seven cyclic points with cross-ratio field of transcendence degree >= 2 are Ramsey iff two-group
status: refuted
warrant: "PROBE (the 2-jet pass is a necessary test only at k = 2)"
scope: "GENERIC_OF(two-parameter rational families)"
difficulty: "attackable (an exact refutation)"
lean_stub: none
fc_category: "n/a"
ams: ["05D10"]
replay: ["probes/c13_c22_seven.py", "probes/c22_controls.py"]
history: ["2026-10-13 filed as the refinement of SR-C13", "2026-10-13 refuted at probe level; superseded by SR-C23"]
```

- **Statement (refuted at probe level).** A 7-point cyclic set whose cross-ratio field has transcendence
  degree ≥ 2 is Ramsey iff it is two-group.
- **Killing sample `[PROBE]`.** Every tested non-two-group 7-set with cross-ratio transcendence degree
  exactly 2 passes the second-order test: 46 structured lattice sets {aθ + bφ} and 118 random
  rational-function sets. Every tested set with degree ≥ 3 fails (44 sets). The threshold is at 3, not 2;
  see SR-C23. The pass is evidence of Ramsey-ness only through SR-C1, so this refutation is not exact.
- **Starting state.** `cd probes && python c13_c22_seven.py`; `python c22_controls.py`.
- **Difficulty.** An exact refutation needs a certificate for a non-two-group 7-set with k = 2.

---

## Consistent on sample

### SR-C15: three generic Möbius groups on the circle

```yaml
id: SR-C15
title: Generic unions of Möbius images of rational sets are Ramsey iff two-groupable
status: consistent-on-sample
warrant: PROBE
scope: "GENERIC_OF(product of Möbius groups)"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10"]
replay: ["probes/c15_c16.py", "probes/e5_mobius.py"]
history: ["2026-10-13 filed", "2026-10-13 consistent on sample"]
```

- **Statement.** Let A = ν₁(R₁) ∪ … ∪ ν_g(R_g) ⊂ S¹ (distinct points), with Rₖ finite rational sets and
  the 3g parameters of the Möbius maps νₖ algebraically independent. Then A is Ramsey iff it is a union
  of at most two Möbius images of rational sets. With "rigid" meaning |Rₖ| ≥ 4 and f the number of
  points in non-rigid groups: Ramsey iff (2 rigid groups, f = 0) or (1 rigid group, f ≤ 3) or (no rigid
  group, f ≤ 6). In particular three rigid generic groups are never Ramsey.
- **Status and evidence.** The "if" direction is SR-C2. Cases with a group of ≥ 5 points follow from
  SR-C14 (the field is purely transcendental, hence regular). `[PROBE]`: the second-order test fails, as
  predicted, on (4,4,1), (4,4,2), (4,4,3), (4,4,4), (5,4,1), (4,3,3) and passes on (4,4), 4 + 3 free and
  (3,3). Open core: every rigid group has exactly four points.
- **Falsifier.** Exact Fredholm duals (`certificates/dual_cert.py` machinery) for (4,4,1) and (4,4,4); a
  pass on any non-two-group cell.
- **Starting state.** `cd probes && python c15_c16.py`.
- **Higher dimensions.** False as stated on S² (five rational plus four free points pass but are not
  two-group); a higher-dimensional analogue must be count-aware (SR-C17).

### SR-C16: Ramsey-ness is not closed under specialization off the circle

```yaml
id: SR-C16
title: Seven generic points on S^2 are Ramsey
status: consistent-on-sample
warrant: "PROBE for (a); HAND, reviewed by AI, for (b)"
scope: "GENERIC_OF((S^2)^7)"
difficulty: attackable
lean_stub: "lean/SphericalRamseyConjectures.lean#C16_generic_seven_S2"
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["probes/c15_c16.py", "probes/e1_s2.py"]
history: ["2026-10-13 filed", "2026-10-13 consistent on sample; part (c) withdrawn after its prediction failed"]
```

- **Statement.** (a) Seven points of S² whose fourteen stereographic coordinates are algebraically
  independent over ℚ are Ramsey. (b) Seven points on a great circle of S² with algebraically independent
  parameters are not Ramsey (the circle phase diagram, `[HAND]`, reviewed). Hence the irreducible family
  of 7-point configurations on S² has a Ramsey generic member and a non-Ramsey specialization, and
  SR-C7 fails for d ≥ 3.
- **Corollary of (a)** (by Möbius 3-transitivity): three rational plus four free points on S² are Ramsey.
- **Status and evidence.** `[PROBE]` generic 7, 8 and 9 points on S² pass the second-order test (which
  is only necessary at this transcendence degree); controls on a great circle fail.
- **Withdrawn part (c).** The prediction that the generic mirror-symmetric cyclic family {0, ±a, ±b, ±c}
  is Ramsey (which would have refuted SR-C7 on the circle too) failed: it fails the second-order test at
  3 of 3 seeds `[PROBE]`.
- **Falsifier.** An exact second-order failure for 7 generic points on S². Promotion needs an exact
  Ramsey certificate for 7 generic points on S²; that would be the first certified Ramsey set beyond the
  two-group mechanism on a sphere of dimension ≥ 2.
- **Starting state.** `cd probes && python c15_c16.py`; `python e1_s2.py`.
- **Lean.** `C16_generic_seven_S2` (statement of (a) only).

### SR-C19: decidability over presented fields

```yaml
id: SR-C19
title: Ramsey-ness is decidable over an explicitly presented finitely generated field
status: consistent-on-sample
warrant: "SKETCH (general); the one-parameter circle case is implemented, with 5/5 exact controls"
scope: "any finitely generated coordinate field, given by a presentation"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10", "13P10", "03B25"]
replay: ["certificates/exact_circle_cert.py"]
history: ["2026-10-13 filed with a sketch", "2026-10-13 consistent on sample (k = 1 circle case)"]
```

- **Statement.** There is an algorithm that, given a prime ideal I ⊂ ℚ[x₁, …, x_k] and the coordinates of
  a finite spherical set as elements of F = Frac(ℚ[x]/I), decides whether the set is Ramsey. So the
  Ramsey-ness of an explicit configuration is exactly as hard as finding the algebraic relations among its
  coordinates (compare SR-C9).
- **Sketch `[SKETCH]`.** Condition (1) of OpenAI's Theorem 1.1 is linear over B = F ⊗ F, a localization
  of R = ℚ[x, x′]/(I(x) + I(x′)); compute the solution module over R by syzygies, apply multiplication,
  and check one linear condition over F.
- **Evidence.** The k = 1 circle case (kernel over ℚ(T, U), saturation at the diagonal, membership test for
  (s − s′)²) reproduces five exact known verdicts, including the non-Ramsey radian 9-gon (228 s). Every
  RAMSEY output carries an independently verified certificate; NON-RAMSEY outputs rely on the k = 1
  limit criterion (reviewed by AI).
- **Falsifier.** A mismatch on an exactly known case.
- **Starting state.** `python -I certificates/exact_circle_cert.py control` (the five exact controls; minutes).
- **Difficulty.** Attackable: a general-k implementation (Singular or Macaulay2 syzygies).

### SR-C23: the expected-dimension law on the circle

```yaml
id: SR-C23
title: Ramsey iff two-group above the expected dimension, for rational families
status: consistent-on-sample
amended: "the first form of (i), without a non-degeneracy hypothesis, is refuted at PROBE level at k = 2"
warrant: "PROBE + CERT instances; the k = 1 case of (i') is SR-C24 (HAND)"
scope: "GENERIC_OF(rational family)"
difficulty: "attackable (k = 1); needs new math (k >= 2)"
lean_stub: none
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["probes/c23_count_law.py", "probes/c14_rigid.py", "certificates/cert_nontwogroup.py", "certificates/exact_circle_cert.py"]
note: "Conjecture (expected-dimension law on the circle)"
history: ["2026-10-13 filed, fitted on earlier data; fresh test filed before it ran", "2026-10-13 fresh test 0 mismatches; (i) amended after a filed prediction failed"]
```

- **Statement.** Let A ⊂ S¹, |A| = n, have a purely transcendental coordinate field, and let k be the
  transcendence degree of its cross-ratio field.
  - (i′) If (n − 5)(k + 1) ≤ 6 and A is non-degenerate, A is Ramsey. For k = 1, non-degenerate means
    rank N = n (SR-C24, which proves this case); for k = 2 it means that the second-order system is
    solvable, and (i′) is then an instance of SR-C1.
  - (ii) If (n − 5)(k + 1) > 6, A is Ramsey iff it is two-group.

  For n = 7: Ramsey iff two-group or (k ≤ 2 and non-degenerate).
- **Status and evidence.** The count is that of the reduced second-order system (n·k(k+1)/2 equations
  against 3k + 5·k(k+1)/2 unknowns); for k = 1 it is derived, not fitted. Fresh seeded test: 0 mismatches
  over 263 configurations `[PROBE]`. Exact: 176 one-parameter non-two-group 9-point sets have a nonzero
  9 × 9 evaluation determinant, hence are not Ramsey (`[CERT]` per instance); W₇ and W₈ (SR-C13) are exact
  non-two-group Ramsey instances of (i′).
- **Amendment.** The mirror-symmetric rational family {0, ±a, ±b, ±c} has k = 2 and fails the
  second-order test `[PROBE]`, refuting (i) without the non-degeneracy hypothesis. Square-root fields are
  excluded: Pálvölgyi's heptagon has n = 7, k = 1 and is not Ramsey.
- **Falsifier.** Any configuration contradicting the prediction, confirmed exactly; for k = 1 the exact
  procedure of SR-C19 decides it in seconds to minutes.
- **Starting state.** `cd probes && python c23_count_law.py`; `python c14_rigid.py`;
  `python -I certificates/cert_nontwogroup.py`.
- **Difficulty.** k = 1: prove "nine non-two-group points ⇒ nonzero determinant" and "rational families
  have full-rank N". k ≥ 2: needs SR-C1-type sufficiency.

### SR-C27: polynomial phases in ℝ³ (working hypothesis)

```yaml
id: SR-C27
title: Low-degree polynomial-phase colourings of R^3 contain the radian 9-gon
status: consistent-on-sample
warrant: "30/30 seeded instances, each with an exactly certified copy"
scope: "colourings floor(r * frac(P)), P in Q(tan 1/2)[x, y, z], deg P <= 3, r in {2, 3}"
difficulty: attackable
lean_stub: none
fc_category: "n/a"
ams: ["05D10"]
replay: ["certificates/definable_polyphase.py", "certificates/definable_crosscheck.py"]
history: ["2026-10-13 filed before its probe", "2026-10-13 30/30"]
```

- **Statement.** For r ∈ {2, 3} and P ∈ ℚ(tan ½)[x, y, z] of degree ≤ 3, the colouring
  χ(x) = ⌊r·{P(x)}⌋ of ℝ³ has a monochromatic congruent copy of E₁ = {(cos k, sin k) : 0 ≤ k ≤ 8}.
- **Evidence.** 30 of 30 seeded instances (15 at r = 2, 15 at r = 3, every P using tan ½) have an exactly
  certified monochromatic copy (rational centre, rational orthogonal frame via the Cayley transform,
  rational interval enclosures of cos k, sin k, tan ½), each re-verified independently. Caveat: the
  success rate matches r^{−8} per random copy, so the sample shows equidistribution of the phases; it
  does not probe any obstruction.
- **Falsifier.** A seeded instance with no certified copy within the full search budget (not itself a
  refutation; the cue to attempt an exact avoidance certificate).

---

## Open

### SR-C1: second-order completeness

```yaml
id: SR-C1
title: The second-order (2-jet) test decides Ramsey-ness
status: open
warrant: "PROBE (sufficiency); necessity is HAND, reviewed by AI"
scope: ANY
difficulty: "attackable (one parameter); needs new math (general)"
lean_stub: none
fc_category: "research open"
ams: ["05D10", "13N15"]
replay: ["probes/e4_six.py", "probes/realness.py", "certificates/exact_circle_cert.py"]
note: "Conjecture C1; Proposition J2"
history: ["2026-10-12 filed", "2026-10-12 evidence restricted to real configurations"]
```

- **Statement.** A finite spherical set is Ramsey iff its second-order system (the field criterion over
  B/𝔪³, 𝔪 = ker(multiplication), in the note's coordinates) is solvable with c = 1.
- **Status and evidence.** Necessity is proved (`[HAND]`; the Taylor map B → F[e]/(e)³ is a ring map
  compatible with multiplication), reviewed by AI. Sufficiency `[PROBE]`: on 702 real one-parameter
  configurations where both tests gave a verdict (635 pass/pass, 67 fail/fail), the second-order test and
  the full one-parameter criterion agree in every case, at two primes near 2³¹. "Real" means an open
  parameter interval on which every radicand is positive, decided exactly; an earlier sample that
  included non-real configurations is not counted.
- **Falsifier.** A one-parameter configuration that passes the second-order test and fails the full
  criterion, confirmed exactly; the exact k = 1 procedure (SR-C19) makes this a sweep.
- **Starting state.** `cd probes && python e4_six.py` (seeded); `python realness.py` (realness filter);
  `python -I certificates/exact_circle_cert.py control` (controls; name a case to run it).
- **Difficulty.** k = 1: attackable (prove that the limit condition at the diagonal reduces to the
  second-order one). General k: needs new math.
- **Lean.** None: the second-order system needs about 60 lines of definitions.

### SR-C3: generic thresholds

```yaml
id: SR-C3
title: Generic n-subsets of S^{d-1} are non-Ramsey iff n >= N(d)
status: open
merged_into: SR-C17
warrant: "PROBE; failing-side boundary cells: S^2 CERT, circle HAND (AI-reviewed)"
scope: "GENERIC_OF(configuration space)"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["probes/e1_phase.py", "probes/e1_s2.py", "probes/e1_s3.py", "probes/e1_s4.py"]
note: "Conjecture C3"
history: ["2026-10-12 filed", "2026-10-13 merged into SR-C17"]
```

- **Statement.** A generic n-subset of S^{d−1} is non-Ramsey iff n ≥ N(d), with N(2) = 7 and
  N(d) = (d + 1)(d + 2)/2 for d ≥ 3.
- **Evidence `[PROBE]`.** Circle 6 pass / 7 fail; S² 9 / 10; first failures at 15 (S³) and 21 (S⁴), with
  four or five free points. On the failing side, the S² boundary cells are certified non-Ramsey (`[CERT]`, the note's
  minimal non-Ramsey theorem) and the circle cell is proved by hand (`[HAND]`, AI-reviewed; the circle
  phase diagram).
- **Falsifier.** An all-generic run on S³ (n = 14, 15) or S⁵ (n = 27, 28), exactly specialized at the
  boundary.
- **Starting state.** `cd probes && python e1_s2.py`; `python e1_s3.py`.

### SR-C4: free-point threshold three

```yaml
id: SR-C4
title: Algebraic points plus at most three arbitrary points are Ramsey on every sphere; four can fail
status: open
merged_into: SR-C17
warrant: "first half: HAND via SR-C2 (CERT + glue for d <= 6); second half: CERT on S^1, S^2, S^3, PROBE for d = 5..9"
scope: "ALGEBRAIC + 3 ANY"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["probes/e3b.py", "certificates/scalar_exact.py", "certificates/dual_cert.py"]
note: "Conjecture C3 (related C4); Remark (three free points in every dimension)"
history: ["2026-10-12 filed", "2026-10-13 merged into SR-C17"]
```

- **Statement.** On every sphere S^{d−1}, finitely many points with algebraic coordinates plus at most
  three arbitrary points form a Ramsey set, and four arbitrary points can fail.
- **Status.** The first half follows from SR-C2 (the algebraic points are one group; any three points are
  a Möbius image of a rational triple), at SR-C2's level: `[CERT]` + glue for d ≤ 6, `[HAND]` for all d;
  on the circle it is `[LEAN]`, Lean-checked (rope AV5). The derivation has had no separate review. Four free points fail
  on S¹ (circle phase diagram), S² and S³ (the cells (6,4) and (11,4), `[CERT]`); `[PROBE]` for 5 ≤ d ≤ 9.
- **Falsifier.** A 3-free-point failure at some d, exactly specialized; or a d where no 4-free-point
  failure exists.
- **Starting state.** `cd probes && python e3b.py`; `python -I certificates/scalar_exact.py`.

### SR-C5: measurable Graham (M1)

```yaml
id: SR-C5
title: Every finite spherical set is Ramsey for measurable colourings
status: open
warrant: none
scope: ANY
difficulty: needs-new-math
lean_stub: "lean/SphericalRamseyConjectures.lean#C5_measurable_graham"
fc_category: "research open"
ams: ["05D10", "28A05", "03E15"]
replay: []
note: "Conjecture M1; Remarks (three lemmas around M1), (definable and polynomial-factor colourings)"
history: ["2026-10-12 filed", "2026-10-12 restated in the forms M1, M1w, M1cat"]
```

- **Statement.** Let A be a finite spherical set.
  - (M1) For every r there is D such that every Lebesgue-measurable r-colouring of ℝ^D is constant on some
    congruent copy of A.
  - (M1w) Moreover the monochromatic copies have positive measure in ℝ^D × O(D) (Lebesgue × Haar).
  - (M1cat) For every r there is D such that whenever U₁, …, U_r are disjoint open subsets of ℝ^D with
    dense union, some U_j contains a congruent copy of A.
- **Status and evidence.** Open; heuristic only. `[SKETCH]` (unreviewed): M1w reduces to Borel
  colourings and is Π¹₂, so a ZFC proof would give Graham's conjecture in Solovay's model, although the
  conjecture fails in ZFC (Pálvölgyi). `[HAND]`: a Lebesgue-measurable ℚ-derivation of ℝ is 0, so the
  separating data in OpenAI's necessity argument cannot be measurable for a spherical set; "robust Graham"
  holds in ZFC (spherical sets with algebraic coordinates are dense); bounded finite witnesses for nearby
  Ramsey sets have unbounded size (compactness). Graham's conjecture holds for o-minimal colourings
  (SR-C25, trivially) and for colourings through boundedly many polynomials (SR-C26).
- **Falsifier.** Some r and, for every D, a Borel r-colouring of ℝ^D whose monochromatic copies of the
  radian 9-gon E₁ form a null set.
- **Difficulty.** Needs new math: a Euclidean density theorem for an affinely dependent, non-product
  spherical set (no such exact theorem is known even for a cyclic quadrilateral).
- **Literature.** No statement of M1 was found in our searches. Zapletal, *Coloring equilateral
  triangles* (arXiv:2503.18295), studies countable chromatic numbers of triangle hypergraphs in
  choiceless models and says nothing about finite colourings, Graham's conjecture or M1.
- **Lean.** `C5_measurable_graham` (the literal form M1).

### SR-C6: rigidity for nine or more cyclic points (R1)

```yaml
id: SR-C6
title: Positive-dimensional Ramsey families of n >= 9 cyclic points are two-group
status: open
warrant: "partial: SR-C14 (HAND) for regular families containing a rigid five-point group"
scope: "GENERIC_OF(positive-dimensional families)"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["probes/c14_rigid.py", "probes/c23_count_law.py"]
note: "Conjecture R1"
history: ["2026-10-12 filed"]
```

- **Statement.** For n ≥ 9 points on a circle, every positive-dimensional family of Ramsey configurations
  lies in a two-Möbius family.
- **Status.** SR-C14 proves it for families with regular coordinate field containing a five-point group
  with rational cross-ratios; SR-C23(ii) predicts it for rational families. The bound n ≥ 9 is needed:
  SR-C13's sets and the radian 8-gon (SR-C10) are non-two-group Ramsey families with 7 and 8 points.
- **Falsifier.** One one-parameter 9-point family that passes the full criterion and is not two-group.
- **Starting state.** `cd probes && python c23_count_law.py` (59 exact-determinant non-Ramsey 9-point
  sets in its sample).

### SR-C7: specialization closure (R2)

```yaml
id: SR-C7
title: If the generic member of an irreducible family is Ramsey, every member is
status: open
warrant: "off the circle: refuted at PROBE level if SR-C16(a) holds; on the circle: no evidence either way"
scope: "GENERIC_OF(V)"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10", "14Q99"]
replay: ["probes/c15_c16.py"]
history: ["2026-10-12 filed", "2026-10-13 probe-level counter-instance off the circle (SR-C16)"]
```

- **Statement.** If the generic member of an irreducible family of finite spherical configurations is
  Ramsey, every member is.
- **Status.** For d ≥ 3 it fails if SR-C16(a) holds (seven generic points on S² `[PROBE]` Ramsey,
  specializing to seven independent cocircular points, non-Ramsey). On the circle it is open; the
  mirror-family attempt (SR-C16(c)) did not refute it.
- **Falsifier.** On the circle: a family with Ramsey generic member and an exact non-Ramsey
  specialization; try degenerations of two-group families with the exact k = 1 procedure (SR-C19).

### SR-C8: pseudo-Euclidean Ramsey theory (L1)

```yaml
id: SR-C8
title: The tensor criterion with an indefinite form gives a well-posed O(p,q)-invariant Ramsey theory
status: open
warrant: "framing only; concrete hyperbolic form in SR-C18"
scope: ANY
difficulty: needs-new-math
lean_stub: none
fc_category: "n/a"
ams: ["05D10", "51F25"]
replay: []
history: ["2026-10-12 filed"]
```

- **Statement.** The tensor criterion with an indefinite form on ℝ^{p,q} gives a well-posed
  pseudo-Euclidean Ramsey theory invariant under O(p, q).
- **Falsifier.** Show that the natural statement is false or ill-posed for ℝ^{1,1} with a small example.
- **See** SR-C18 for the concrete hyperbolic form.

### SR-C9: transcendence-hard instances (T1)

```yaml
id: SR-C9
title: Ramsey-ness of explicit configurations can be equivalent to open transcendence problems
status: open
warrant: "framing; the example rests on Theorem D (LEAN)"
scope: "TRANSCENDENTAL_PARAM"
difficulty: "attackable (literature)"
lean_stub: none
fc_category: "n/a"
ams: ["05D10", "11J81"]
replay: ["certificates/radian_det.py"]
note: "Conjecture T1; Corollary (radian progressions), item 2"
history: ["2026-10-12 filed"]
```

- **Statement.** Ramsey-ness of explicit configurations can be equivalent to open transcendence problems;
  conversely, Schanuel's conjecture would make Ramsey-ness decidable for exponential-algebraic
  configurations (compare SR-C19).
- **Example.** The nine points at 0, e, …, 8e radians are Ramsey iff e^{ie} is algebraic (Theorem D,
  `[LEAN]`, Lean-checked, rope AV3). Schanuel's conjecture implies that e^{ie} is transcendental (Waldschmidt, *Open
  Diophantine problems*, arXiv:math/0312440, §3.1); we know no proof and found none in the literature.
  That it is open is our inference (a final re-check is pending before posting).
- **A decided family** (`[HAND]`, unreviewed): for θ = πβ with β real algebraic, the radian 9-gon is
  Ramsey iff β ∈ ℚ (Gelfond–Schneider: (−1)^β is transcendental for irrational algebraic β).
- **Falsifier.** A proof in the literature that e^{ie} is transcendental (it would kill the example, not
  the framing).

### SR-C11: a second-order failure without a scalar certificate

```yaml
id: SR-C11
title: Is there a 2-jet failure with no scalar single-derivation certificate?
status: open
warrant: "PROBE evidence against, on every tested cell"
scope: ANY
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10"]
replay: ["probes/scalar_cert.py", "certificates/scalar_exact.py"]
note: "Section (second-order necessary test), scalar certificates"
history: ["2026-10-12 filed (replacing a withdrawn witness)", "2026-10-12 evidence against on all tested cells"]
```

- **Statement (question).** Is there a finite spherical set whose second-order system is inconsistent
  but which has no scalar certificate (weights Λᵢ = λᵢC with a single derivation of the coordinate
  field), even with order-one multipliers allowed?
- **Evidence against `[PROBE]`.** A scalar certificate exists in all sixteen failing S² cells, both S³
  threshold cells, the S⁴ threshold and ten generic points on S², at two primes; seven of them are exact
  (the note's minimal non-Ramsey theorem). An earlier claimed witness (three rational plus four
  independent circle points) is withdrawn: it has a scalar certificate (exact, J2-F7). For k = 1 every
  certificate is scalar, so no witness exists there.
- **Falsifier / search.** A random fixed direction is not a test (it misses certificates that exist).
  Search over all directions: method A of `scalar_cert.py` for disjoint parameter sets, otherwise a
  bilinear search in (λ, c). Remaining candidates: k ≥ 2 failures with shared parameters (three Möbius
  groups, 6 + 6 + 6 on S³).
- **Starting state.** `cd probes && python scalar_cert.py`; `python -I certificates/scalar_exact.py`.

### SR-C12: scalar sufficiency on disjoint-parameter configurations

```yaml
id: SR-C12
title: Pálvölgyi's scalar method suffices for rational plus independent points
status: open
warrant: "PROBE (working hypothesis)"
scope: "GENERIC_OF(rational + independent points)"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10"]
replay: ["probes/scalar_cert.py", "certificates/scalar_exact.py"]
history: ["2026-10-12 filed as a working hypothesis"]
```

- **Statement.** On configurations of rational points plus points with pairwise disjoint independent
  parameters, on any S^{d−1}, every failure of the second-order test has a scalar single-derivation
  certificate.
- **Evidence `[PROBE]`.** As SR-C11.
- **Falsifier.** A method-A "no scalar certificate" at a failing cell, for example at the free-point
  thresholds for d = 2, …, 9 (`probes/e3b.py`).

### SR-C17: the phase diagram in every dimension

```yaml
id: SR-C17
title: Rational plus independent points on S^{d-1}, d >= 3
status: open
warrant: "PROBE; the minimal failing cells on S^2 and S^3 are CERT; the passing side with j <= 3 follows from SR-C2"
scope: "GENERIC_OF(m rational in general position + j independent)"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["probes/e1_s2.py", "probes/e3_sphere.py", "certificates/scalar_exact.py"]
note: "Conjecture C3 (merged form); Theorem NR-S23"
history: ["2026-10-13 filed, merging SR-C3 and SR-C4"]
```

- **Statement.** For d ≥ 3 let N(d) = (d + 1)(d + 2)/2. Take m points of S^{d−1} with rational
  coordinates, outside a proper Zariski-closed subset of rational m-tuples, and j points with
  algebraically independent stereographic coordinates. The union is non-Ramsey iff j ≥ 4 and
  m + j ≥ N(d). (On the circle the threshold is 7, not 6, because of two-group certificates.)
- **Status and evidence.** `[PROBE]`: on S² exactly "fail iff j ≥ 4 and m + j ≥ 10"; S³ first failure at
  n = 15; S⁴ at n = 21; free-point threshold 3 for d = 2, …, 9. Failing side: supersets of non-Ramsey sets
  are non-Ramsey, so it reduces to the minimal cells m + j = N(d), and by Möbius 3-transitivity the cells
  with m ≤ 3 are generic N(d)-sets. On S² the minimal cells (6,4), (5,5), (4,6), (3,7) and generic 10, and
  on S³ the cells (11,4), (10,5), are certified non-Ramsey (`[CERT]` identities plus reviewed glue) for
  the specific rational points listed in the note. The S⁴ cell (17,4) has a scalar certificate modulo p
  only. Passing side: j ≤ 3 is SR-C4's first half; j ≥ 4 below N(d) is open (first case: SR-C16).
- **Falsifier.** An S³ cell with j ≥ 6 at m + j = 14 that fails, or one at m + j = 15 that passes; on S²,
  rational points in general position for which (4,6) passes. The S³ j ≥ 6 cells are a large linear
  system (about 4,000 unknowns modulo p): hours, not a campaign.
- **Starting state.** `cd probes && python e1_s2.py`; `python e3_sphere.py threshold 3,4,5`;
  `python -I certificates/scalar_exact.py`.

### SR-C18: hyperbolic Ramsey sets

```yaml
id: SR-C18
title: Hyperbolic-Ramsey sets are the hyperbolic models of Euclidean-Ramsey sets
status: open
warrant: "HAND for one direction (unreviewed); SKETCH for linear necessity"
scope: ANY
difficulty: "needs new math (the test case); attackable (write-ups)"
lean_stub: none
fc_category: "research open"
ams: ["05D10", "51M10"]
replay: []
history: ["2026-10-13 filed"]
```

- **Setting.** ℍ^m is the hyperboloid model, cosh d(x, y) = −⟨x, y⟩. A finite A ⊂ ℍ^m is
  hyperbolic-Ramsey if for every r there is N such that every r-colouring of ℍ^N contains a monochromatic
  isometric copy of A. The hyperbolic model A_B of a finite Euclidean set B is the set with
  cosh d(aᵢ, aⱼ) = 1 + |bᵢ − bⱼ|²/2 (it exists: put B on a horosphere).
- **Statement.** A is hyperbolic-Ramsey iff A = A_B for some Euclidean-Ramsey B.
- **Parts.** (⇐) `[HAND]`, elementary, unreviewed: a horosphere of ℍ^N is ℝ^{N−1} with
  cosh d = 1 + |Δ|²/2, so colourings restrict. Linear necessity `[SKETCH]`: a linear relation
  Σλᵢaᵢ = 0 with no vanishing subsum excludes hyperbolic-Ramsey (colour by a Rado-type colouring of
  cosh d(o, x)); so three points on a geodesic are not hyperbolic-Ramsey.
- **Test case.** The horocyclic image of the collinear triple {0, 1, 2}: its hyperboloid vectors are
  linearly independent (Gram determinant −1) and it lies on no hyperbolic sphere. This conjecture predicts
  not hyperbolic-Ramsey; "every hyperbolic simplex is hyperbolic-Ramsey" predicts Ramsey.
- **Literature.** Two web searches (snippet level) found no hyperbolic Euclidean-Ramsey paper; this is
  not a novelty claim.
- **Falsifier.** A colouring of ℍ^N (fixed r, every N) avoiding the horocyclic triple settles the test case
  in this conjecture's favour; exhibiting the triple inside a hyperbolic-Ramsey structure refutes it.
- **Lean.** None (Mathlib has no hyperbolic space).

### SR-C20: effective Ramsey dimension

```yaml
id: SR-C20
title: Computable and primitive recursive bounds on the Ramsey dimension
status: open
warrant: "SKETCH for part 1; parts 2 and 3 conjectural"
scope: ALGEBRAIC
difficulty: needs-new-math
lean_stub: none
fc_category: "research open"
ams: ["05D10", "03D20"]
replay: []
history: ["2026-10-13 filed"]
```

- **Statement.** Let D_min(A, r) be the least D such that every r-colouring of ℝ^D has a monochromatic
  congruent copy of A.
  1. `[SKETCH]` For finite spherical A with real algebraic coordinates an upper bound for D_min(A, r) is
     computable (enumerate finite witnesses and decide each in the existential theory of the reals; the
     search terminates by the algebraic-coordinates theorem and de Bruijn–Erdős compactness).
  2. D_min(A, r) is primitive recursive in r, |A|, d and the degree and height of the coordinate field.
  3. For algebraic θ_n → 1, D_min(E_{θ_n}, 2) → ∞, where E_θ is the radian 9-gon.
- **Evidence.** Only the finite-witness bound of the note's Remark (three lemmas around M1, item L4),
  which is consistent with part 3 but does not imply it.
- **Falsifier.** (2): an algebraic family of bounded size and degree with D_min growing faster than any
  primitive recursive function. (3): a uniform D along an algebraic sequence θ_n → 1.

### SR-C21: colour number of non-Ramsey spherical sets

```yaml
id: SR-C21
title: Is the colour number of a non-Ramsey spherical set bounded in terms of its size?
status: open
warrant: none
scope: ANY
difficulty: "attackable (upper bounds); needs new math (lower bounds)"
lean_stub: none
fc_category: "research open"
ams: ["05D10"]
replay: []
history: ["2026-10-13 filed"]
```

- **Statement (question).** For a non-Ramsey finite spherical A let r(A) be the least r such that, for
  every D, some r-colouring of ℝ^D has no monochromatic congruent copy of A. Is r(A) bounded by a function
  of |A|? For example, is r bounded on 7-point non-Ramsey cyclic sets?
- **Evidence.** One data point: Pálvölgyi's heptagon is avoided with 8 colours (his appendix). The
  colourings of the note's Lemma A.1 route have colour counts that depend on the derivation data.
- **Falsifier.** Bookkeeping of the colour counts from Lemma A.1 and EGMRSS I, Lemma 15, for the circle
  phase-diagram heptagons, the radian 9-gon and the S²/S³ cells; a family of 7-point non-Ramsey sets with
  r → ∞ answers "no".

### SR-C28: Graham for locally semialgebraic colourings

```yaml
id: SR-C28
title: Locally semialgebraic colourings contain every finite spherical set
status: open
warrant: "partial results HAND (SR-C26, cube lemma); reviewed by AI"
scope: ANY
difficulty: needs-new-math
lean_stub: none
fc_category: "research open"
ams: ["05D10", "14P10"]
replay: []
note: "Remark (definable and polynomial-factor colourings), items (c), (d)"
history: ["2026-10-13 filed"]
```

- **Statement.** For every finite spherical A and every r there is D such that every r-colouring of ℝ^D
  whose classes meet every ball in a semialgebraic set (arbitrary real parameters) has a monochromatic
  congruent copy of A.
- **Why this class.** It contains the colourings ⌊c|x|²⌋ mod r of EGMRSS, which defeat every non-spherical
  set, so unlike the o-minimal class (SR-C25) it sees sphericity. SR-C5 implies it. `[SKETCH]`: in density
  form it is equivalent to the density form of M1 for Borel colourings.
- **Partial results.** Bounded-complexity polynomial factors (SR-C26). Cube lemma `[HAND]`, reviewed (AI):
  for D ≥ 3 a unit circle fits in a closed cube of side 2√(2/D), so a colouring with a class containing
  such a cube has a monochromatic copy of every finite subset of a unit circle, and a colouring constant on
  the cells of a cubical grid of side h is defeated once D > 8/h². A counterexample family therefore needs
  factor complexity growing with D and cells finer than D^{−1/2}.
- **Falsifier.** For one r, an explicit family of locally semialgebraic r-colourings avoiding E₁ in ℝ^D
  for every D, with an exact avoidance certificate. A cheap first probe: SAT over ℤ^D-periodic grid
  colourings at small (D, N, r), constrained by exactly certified robust copies.

---

## Tailings (refuted or withdrawn, no entry of their own)

| Guess | Killed by | Warrant |
|---|---|---|
| Matrix weights in the dual of the second-order test are strictly stronger than Pálvölgyi's scalar identities | its only witness (three rational plus four independent circle points) has a scalar certificate with E = 4 (`certificates/dual_cert.py`) | `[CERT]`; withdrawn |
| Poncelet chains are special (Ramsey beyond the generic threshold) | they fail at seven points like random three-parameter families (`probes/e6_wild.py`) | `[PROBE]` |
| Two Möbius groups work only on Hopf spheres | S³ two-group certificates, then SR-C2 in every dimension | `[CERT]` / `[HAND]` |
| The free-point threshold grows with d | it is 3 for d = 2, …, 9 (`probes/e3b.py`) | `[PROBE]` |
