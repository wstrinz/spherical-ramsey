# Spherical Ramsey conjecture ledger

The open problems, partial results and refuted guesses that accompany the note *Two Möbius groups
suffice* (`note/` in this release). Every entry has a stable id, a status, the strongest artifact
behind it, and a starting state that a reader can replay. Refuted entries are kept, with the sample
that killed them. The format, status vocabulary and warrant rules are in `README.md`; the YAML
headers are collected in `ledger.yaml`; statement-only Lean stubs for six entries are in
`lean/SphericalRamseyConjectures.lean`; the open threads are in `BACKLOG.md`. The ranked open
frontier is `FRONTIER.md` at the release root.

**Version 1.1.0.** This version corrects the credit and status of several entries (SR-C3, SR-C7,
SR-C11, SR-C12, SR-C13, SR-C16, SR-C17; the full list is `CHANGELOG.md` at the release root): OpenAI's
quadric-independence criterion (result 172, Prop. 7.3) and Pálvölgyi's appendix Theorems A.11–A.13 were
overlooked in v1.0.0. It adds SR-C29 to SR-C35. Each entry names the reviews behind its status.

**Count (35 entries).** proved: 12 (SR-C2, SR-C3, SR-C10, SR-C11, SR-C14, SR-C16, SR-C24, SR-C25,
SR-C26, SR-C29, SR-C32, SR-C34); refuted: 3 (SR-C7, SR-C13, SR-C22); consistent-on-sample: 6 (SR-C15,
SR-C19, SR-C23, SR-C27, SR-C30, SR-C31); open: 14. Four further refuted or withdrawn guesses
with no entry of their own are listed under *Tailings* at the end.

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
numpy 1.26, sympy 1.14, mpmath 1.3; python-flint 0.9 for `corank_exact.py`, `c31_respecialize.py`,
`c34_det16.py`, `probes/c31_c32_jet2.py` and `probes/c34_test.py`.

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

### SR-C3: generic thresholds

```yaml
id: SR-C3
title: Generic n-subsets of S^{d-1} are non-Ramsey iff n >= N(d)
status: proved
merged_into: SR-C17
warrant: "bookkeeping of prior work: d = 2: Theorem B(a) (LEAN) + the circle phase diagram (HAND, AI-reviewed); d >= 3, Ramsey half: OpenAI's Prop. 7.3 (LEAN, theirs) + HAND genericity glue (reviewed once by an AI agent); non-Ramsey half: Palvolgyi's Theorem A.12 (appendix labelled unchecked by its author; its proof read by an AI reviewer) and independently SR-C30 with m = 0 (SKETCH, reviewed once)"
scope: "GENERIC_OF(configuration space)"
difficulty: done
lean_stub: none
fc_category: "research solved (by prior work) once public"
ams: ["05D10", "52C10"]
replay: ["certificates/corank_exact.py", "probes/e1_phase.py", "probes/e1_s2.py", "probes/e1_s3.py", "probes/e1_s4.py"]
note: "Conjecture C3"
history: ["2026-10-12 filed", "2026-10-13 merged into SR-C17", "2026-10-14 proved, mostly by prior work (v1.1.0)"]
```

- **Statement.** A generic n-subset of S^{d−1} is non-Ramsey iff n ≥ N(d), with N(2) = 7 and
  N(d) = (d + 1)(d + 2)/2 for d ≥ 3.
- **Proof (bookkeeping, not a new result).** d = 2: generic sets of at most six points are Ramsey
  (Theorem B(a), prior work: JD-Jones-ASES), and the phase-diagram cell (0, 7) is non-Ramsey (Pálvölgyi's
  Theorems A.3/A.7), hence so is every superset. d ≥ 3: generic n-sets with n ≤ D_d = N(d) − 1 are Ramsey,
  a corollary of OpenAI's Proposition 7.3 (result 172; Lean `spherical_quadraticIndependent_ramsey_all`)
  with the genericity glue of SR-C29 (reviewed once by an AI agent; the same genericity remark is in the
  proof of Pálvölgyi's A.12); generic n-sets with n ≥ N(d) are non-Ramsey by Pálvölgyi's Theorem A.12
  (arXiv:2609.23327, appendix labelled unchecked by its author; its proof was read by our AI reviewer)
  and, independently, by SR-C30 with m = 0 (`[SKETCH]`, reviewed once). The S² ten-point cell certified
  in the note (Theorem NR-S23) is the case d = 3.
- **Earlier evidence `[PROBE]`.** Circle 6 pass / 7 fail; S² 9 / 10; first failures at 15 (S³) and 21 (S⁴).
- **Starting state.** `python -I certificates/corank_exact.py c29`; `cd probes && python e1_s2.py`;
  `python e1_s3.py`.

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

### SR-C11: a second-order failure without a scalar certificate

```yaml
id: SR-C11
title: Is there a 2-jet failure with no scalar single-derivation certificate?
status: proved
warrant: "answered yes by SR-C32 (CERT + HAND glue, reviewed by one non-author AI agent; non-Ramsey via the 2-jet necessity); the earlier PROBE evidence against was automatic (quadric corank one)"
scope: ANY
difficulty: done
lean_stub: none
fc_category: "research solved (answer yes) once public"
ams: ["05D10"]
replay: ["probes/scalar_cert.py", "certificates/scalar_exact.py"]
note: "Section (second-order necessary test), scalar certificates"
history: ["2026-10-12 filed (replacing a withdrawn witness)", "2026-10-12 evidence against on all tested cells", "2026-10-14 evidence re-scoped (automatic at corank one)", "2026-10-14 answered yes by SR-C32"]
```

- **Statement (question).** Is there a finite spherical set whose second-order system is inconsistent
  but which has no scalar certificate (weights Λᵢ = λᵢC with a single derivation of the coordinate
  field), even with order-one multipliers allowed?
- **Answer: yes** (SR-C32). Four seeded families of 12 and 13 points on S² with shared parameters
  (quadric corank 3 and 4) fail the 2-jet test and have no scalar certificate, even over ℂ; proved for
  those families, with the glue reviewed by one non-author AI agent. A matrix-weighted Lemma A.1 (SR-C35,
  a sketch) would still colour them: matrix weights are strictly stronger for certificates, not
  (as far as is known) for colourings.
- **Earlier evidence, re-scoped (v1.1.0).** A scalar certificate exists in all sixteen failing S² cells,
  both S³ threshold cells, the S⁴ threshold and ten generic points on S² `[PROBE]`, seven of them exact.
  This was recorded as evidence against; it is automatic. Every one of these cells has quadric corank one
  or contains a failing cell of corank one, and at corank one the 2-jet test equals the scalar test
  (SR-C31(a), `[HAND]`, reviewed by one non-author AI agent). An earlier claimed witness (three rational
  plus four independent circle points) is withdrawn: it has a scalar certificate (exact, J2-F7).
- **Starting state.** `python -I certificates/corank_exact.py c32`; `cd probes && python scalar_cert.py`.

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

### SR-C16: Ramsey-ness is not closed under specialization off the circle

```yaml
id: SR-C16
title: Seven generic points on S^2 are Ramsey
status: proved
warrant: "(a): LEAN (OpenAI's Prop. 7.3; theirs) + HAND genericity glue (reviewed once by an AI agent) + exact rank; holds for up to nine generic points on S^2. (b): HAND, reviewed by AI"
scope: "GENERIC_OF((S^2)^7)"
difficulty: "done; engineering (a Lean corollary)"
lean_stub: "lean/SphericalRamseyConjectures.lean#C16_generic_seven_S2"
fc_category: "research solved (a corollary of prior work) once public"
ams: ["05D10", "52C10"]
replay: ["certificates/corank_exact.py", "probes/c15_c16.py", "probes/e1_s2.py"]
history: ["2026-10-13 filed", "2026-10-13 consistent on sample; part (c) withdrawn after its prediction failed", "2026-10-14 (a) proved: a corollary of OpenAI's Prop. 7.3, overlooked in v1.0.0"]
```

- **Statement.** (a) Seven points of S² whose fourteen stereographic coordinates are algebraically
  independent over ℚ are Ramsey. (b) Seven points on a great circle of S² with algebraically independent
  parameters are not Ramsey. Hence the irreducible family of 7-point configurations on S² has a Ramsey
  generic member and a non-Ramsey specialization, and SR-C7 fails for d ≥ 3.
- **Status and evidence.** (a) `[LEAN]` (OpenAI's Proposition 7.3, Lean
  `spherical_quadraticIndependent_ramsey_all`; theirs) + `[HAND]` genericity glue (SR-C29, reviewed once by an
  AI agent) + an exact rank (seven seeded rational points of S² have quadric rank 7,
  `corank_exact.py c29`); it holds for up to nine generic points on S². This is a corollary of prior work;
  ours is only the bookkeeping. (b) `[HAND]`, AI-reviewed (the circle phase diagram). Earlier `[PROBE]`
  evidence: generic 7, 8 and 9 points on S² pass the second-order test; controls on a great circle fail.
- **Correction (v1.1.0).** An earlier version said that a certificate for (a) would be the first certified
  Ramsey set beyond the two-group mechanism on S². That was wrong: OpenAI's criterion already gives one
  (seven generic points of S² are not two-group: four points of a Möbius image of an algebraic set have an
  algebraic complex cross-ratio, and four generic points do not). The note's non-two-group Ramsey sets
  (SR-C13) are on the circle, where the criterion reaches at most five points.
- **Corollary of (a)** (by Möbius 3-transitivity): three rational plus four free points on S² are Ramsey.
- **Withdrawn part (c).** The prediction that the generic mirror-symmetric cyclic family {0, ±a, ±b, ±c}
  is Ramsey (which would have refuted SR-C7 on the circle too) failed: it fails the second-order test at
  3 of 3 seeds `[PROBE]`.
- **Falsifier.** A gap in SR-C29's genericity step.
- **Starting state.** `python -I certificates/corank_exact.py c29`; `cd probes && python c15_c16.py`;
  `python e1_s2.py`.
- **Lean.** `C16_generic_seven_S2` (statement of (a) only). It follows from OpenAI's Lean theorem plus an
  explicit rank-7 rational instance and a generic-rank lemma (`FRONTIER.md`, F8); not done here, so (a) is
  not "Lean-checked".

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

### SR-C29: generic points up to the quadric dimension are Ramsey (OpenAI's quadric-independence criterion)

```yaml
id: SR-C29
title: Generic points of S^{d-1}, up to the dimension of quadrics on the sphere, are Ramsey (corollaries of OpenAI's Prop. 7.3)
status: proved
warrant: "LEAN (OpenAI's spherical_quadraticIndependent_ramsey_all; theirs, prior work) + HAND genericity glue (reviewed once by an AI agent) + exact quadric ranks (d = 3..8)"
scope: "GENERIC_OF((S^{d-1})^N), N <= (d+1)(d+2)/2 - 1"
difficulty: "done; engineering (a Lean corollary)"
lean_stub: none
fc_category: "research solved (corollaries of prior work) once public"
ams: ["05D10", "52C10"]
replay: ["certificates/corank_exact.py"]
history: ["2026-10-14 filed before its exact rank checks", "2026-10-14 proved; genericity glue reviewed once (AI), with a spanning fix"]
```

- **Prior result (OpenAI).** Result 172, Proposition 7.3: a finite spherical set A ⊂ ℝ^d with
  coordinate field F that affinely spans ℝ^d is Ramsey if the vectors vec(pᵢpᵢᵀ), pᵢ = (1, aᵢ), are
  linearly independent over F, that is, if the points impose independent conditions on quadratic
  polynomials. Lean: `spherical_quadraticIndependent_ramsey_all` (Comparator challenge
  `EuclideanRamseyQuadratic`), in `Quadratic.lean`, which every rope of this release vendors unmodified
  (we never ran Comparator on that challenge; the `[LEAN]` tag is OpenAI's). Its circle case (Cor. 7.4, at
  most five circle points) was cited in v1.0.0; the general criterion was overlooked until 2026-10-14. Call
  κ(A) = N − rank_F{vec(pᵢpᵢᵀ)} the *quadric corank*; the criterion says κ = 0 ⇒ Ramsey.
- **Statement (corollaries of OpenAI's Proposition 7.3).** Let D_d = (d + 1)(d + 2)/2 − 1, the dimension
  of the space of quadratic polynomials restricted to S^{d−1}, and N(d) = D_d + 1.
  - (Q1) For every d ≥ 2 and N ≤ D_d, N points of S^{d−1} whose stereographic coordinates are
    algebraically independent over ℚ are Ramsey.
  - (Q2) SR-C16(a): seven (indeed up to nine) such points of S² are Ramsey, and they are not two-group.
    With SR-C16(b) this refutes SR-C7 for every d ≥ 3.
  - (Q3) SR-C17, passing side: m rational points of S^{d−1}, outside a proper Zariski-closed set of
    rational m-tuples, plus j points with algebraically independent stereographic coordinates are
    Ramsey whenever m + j ≤ D_d, for every j.
  - (Q4) SR-C3, Ramsey half: for d ≥ 3, generic n-subsets of S^{d−1} with n < N(d) are Ramsey.
- **Genericity glue `[HAND]`** (reviewed once by an AI agent, which required the spanning fix below).
  D_d generic points of S^{d−1} affinely span ℝ^d and impose independent conditions on quadrics:
  quadratic polynomials restrict to linearly independent functions on S^{d−1}, so a D_d × D_d evaluation
  minor is a nonzero polynomial in the stereographic coordinates (the F-rank is at least the rank at any
  rational specialization; exact rational instances of full rank for d = 3, …, 8 below); the same
  genericity remark is in the proof of Pálvölgyi's Theorem A.12. So a generic spanning D_d-set is Ramsey by OpenAI's theorem. Subsets of Ramsey sets are
  Ramsey, and a generic N-set (N ≤ D_d), or m rational points in general position plus j generic points
  with m + j ≤ D_d, is a subset of such a generic spanning D_d-set (for (Q3), full rank at generic free
  points is the nonvanishing of a minor, a polynomial condition on the rational points). This matters
  already for seven points when d ≥ 7, where seven points do not span. Not two-group: four points of a
  Möbius image of an algebraic set have an algebraic complex cross-ratio and four generic points do not,
  so each group of a two-group set of generic points has at most three points, and seven or more generic
  points are not two-group.
- **Exact checks.** `corank_exact.py c29` (seeded): D_d rational points on S^{d−1} have quadric rank D_d
  for d = 3, …, 8 (9, 14, 20, 27, 35, 44); seven rational points on S² have rank 7; the rational points R₂
  of the note's Theorem NR-S23 plus three more have rank 9. The script asserts that every configuration
  has distinct points.
- **Credit.** The criterion and its mechanism (a right inverse over F lifted through the section
  F → F ⊗ F; OpenAI's `lift_kernel`) are OpenAI's. The consequences are corollaries; our contribution is
  noticing them and the bookkeeping.
- **Falsifier.** A gap in the genericity glue (the criterion itself is OpenAI's Lean theorem).
- **Starting state.** `python -I certificates/corank_exact.py c29` (seconds).
- **Lean.** None here. (Q2) as a Lean corollary needs one explicit rank-7 rational instance and a
  generic-rank lemma (`FRONTIER.md`, F8); until then nothing in this entry is "Lean-checked" beyond
  OpenAI's own theorem.

### SR-C32: second-order failures with no scalar certificate

```yaml
id: SR-C32
title: Twelve and thirteen points on S^2 (quadric corank 3 and 4) fail the 2-jet test and have no scalar certificate
status: proved
warrant: "proved for the four seeded families: (i) 2-jet FAIL by CERT (dual rank at a rational specialization, plus an independent primal rank pair) + HAND specialization glue, reviewed by one non-author AI agent; non-Ramsey via the 2-jet necessity (HAND, reviewed by AI); (ii) no scalar certificate, even over C: CERT (the ideal of k x k minors is exactly (y)^k) + glue, reviewed by AI"
scope: "GENERIC_OF(F_{N,k,s}): the four seeded rational-affine families of certificates/corank_exact.py c32, with theta algebraically independent over Q"
difficulty: "done for these families; attackable (colour counts via SR-C35)"
lean_stub: none
fc_category: "research solved once public"
ams: ["05D10", "13N15"]
replay: ["certificates/corank_exact.py"]
history: ["2026-10-14 filed as a prediction before any computation", "2026-10-14 consistent on sample (4/4 exact)", "2026-10-14 proved for the four seeded families after a non-author AI review"]
```

- **Statement.** For (N, k) = (12, 4) and (13, 3) and seeds s = 0, 1, let F_{N,k,s} be the family of N
  points of S² whose stereographic coordinates are the rational-affine functions αᵢ + Bᵢθ of
  `corank_exact.py c32` (seeded rational coefficients), with θ = (θ₁, …, θ_k) algebraically independent
  over ℚ (quadric corank 3, respectively 4). Then (i) the 2-jet test fails, so the set is not Ramsey; and
  (ii) no relation λ ≠ 0, even complex, and derivation satisfy the linear conditions of Lemma A.1 (or its
  matrix reduction, Pálvölgyi's A.4), so the set has no scalar (single-relation) derivation certificate.
  These are the first non-Ramsey sets known to us with no such certificate. A matrix-weighted
  (vector-energy) version of Lemma A.1 still colours them (SR-C35): "matrix weights are strictly
  stronger" is true for certificates, not for colourings.
- **Why (SR-C31's counts).** The 2-jet dual has dimension at least κk(k + 1)/2 − kG = 30 − 24 = 6 > 0,
  while the scalar locus {λ : rank Π_λ ≤ k − 1} has expected codimension G − k + 1 = 3 > κ − 1 = 2, so it
  is empty. On the circle the two thresholds coincide for every κ; on S² they first separate at
  (κ, k) = (3, 4) and (4, 3).
- **Evidence and proof.** (i) `corank_exact.py c32`: at θ = 0 the dual has dimension 6, equal to the
  generic lower bound, with a nonzero pairing (2-jet FAIL, exact). The reviewer confirmed it with an
  independent exact primal rank pair (N = 12: rank 150 against 151 for the augmented system; N = 13: 99
  against 100; computed in the review, not shipped here). The specialization glue was reviewed (one
  non-author AI review); non-Ramsey follows from the 2-jet necessity (Proposition J2, `[HAND]`,
  AI-reviewed). (ii) The maximal (k × k) minors of Π_y (y the relation coordinates) generate a
  zero-dimensional homogeneous ideal over ℚ (`corank_exact.py c32`); the reviewer showed that this ideal
  is exactly (y)^k (the minors have full rank on the degree-k monomials, 15/15 and 20/20; one nonzero
  rational determinant certifies it), so its only zero is y = 0, even over ℂ, and emptiness at the
  specialization gives emptiness for the generic member (a closed condition). 4/4.
- **Note on the probe.** `probes/c31_c32_jet2.py` runs the primal 2-jet test modulo p on SR-C31's seed-0
  families with the same (N, k), not on these four families; the exact primal check above covers the
  SR-C32 families themselves.
- **Falsifier.** A gap in the reviewed glue.
- **Starting state.** `python -I certificates/corank_exact.py c32` (about 20 s).

### SR-C34: first-order rigidity

```yaml
id: SR-C34
title: If the 2-jet dual space vanishes, the set is Ramsey
status: proved
warrant: "HAND, reviewed by one non-author AI agent (Smith form over the local ring at the diagonal, J2 duality, Nakayama); the (d+1)^2 threshold law and 'not two-group' consistent on sample (10/10 PROBE with exact dual dimensions); the non-Ramsey side at 16 points CERT per instance"
scope: ANY
difficulty: "done (HAND); engineering (a Lean proof over OpenAI's FieldCriterion)"
lean_stub: none
fc_category: "research open (until a proof is public and accepted)"
ams: ["05D10", "13N15"]
replay: ["probes/c34_test.py", "certificates/c34_det16.py", "certificates/corank_exact.py"]
history: ["2026-10-14 filed with a sketch, before its probe test", "2026-10-14 consistent on sample (10/10)", "2026-10-14 proved after a non-author AI review"]
```

- **Statement.** Let A be a finite subset of the unit sphere S^{d−1} centred at 0 (other spheres by a
  similarity), with coordinate field F, let D₁, …, D_k be a basis of Der_ℚ(F) (or of the derivations of
  any finitely generated real field containing the coordinates), and let Δ(A) be the 2-jet dual space
  (SR-C31(a)), without the trace-pairing condition. If Δ(A) = 0, then A is Ramsey. Scope `ANY`.
- **Proof** (`[HAND]`, reviewed by one non-author AI agent). Over O = (F ⊗ F)_𝔪 take a Smith form of the
  evaluation map Φ; the obstruction b has entries bᵢ = −½ Σ_j (a_ij ⊗ 1 − 1 ⊗ a_ij)², so it lies in
  𝔪²O^N; by the duality behind Proposition J2 the annihilator of the order-two image is Δ(A) (Δ ≅ W^⊥);
  so Δ = 0 gives 𝔪²O^κ ⊆ 𝔪·Im Ψ + 𝔪³O^κ, and Nakayama's lemma puts the obstruction in 𝔪·Im Ψ, which by
  SR-C33(a) is Ramsey.
- **Special cases.** κ = 0 is OpenAI's quadric-independence criterion (SR-C29). On the circle with one
  parameter it contains SR-C24, now without the regularity hypothesis on F. It is silent when κ ≥ 1 and
  some derivation is Möbius-null (for example transcendental rotations of rational sets).
- **Instances.** A Ramsey verdict where Δ = 0 at a specialization with maximal quadric rank is a theorem:
  for example the exact 2-jet passes with Δ = 0 in SR-C31's sample and in `probes/c34_test.py` (N ≤ 15 on
  S², one parameter).
- **Consistent on sample (not proved).** For one-parameter configurations in general position on
  S^{d−1}, the threshold is (d + 1)² points (9 on the circle, Theorem D's count; 16 on S²), and the Ramsey
  sets with quadric corank 1 to 4 that this gives on S² are not two-group. Evidence: `probes/c34_test.py`,
  N = 13, …, 17 on S², two seeds each: exact dim Δ at θ = 0 is 0 for N ≤ 15 and 1, 2 (nonzero pairing) for
  N = 16, 17; the curve probe (the truncated π-adic test, order 12, modulo p) and the 2-jet test pass for
  every N ≤ 15 and fail for N = 16, 17 `[PROBE]`, 10/10 as predicted. The non-Ramsey side at N = 16 is
  exact without the 2-jet test: the 16 × 16 evaluation determinant is nonzero at two rational points for
  both seeds (`certificates/c34_det16.py`, Theorem D's method, `[CERT]` per instance).
- **Novelty.** Novel as far as found: a literature sweep on 2026-10-15 (OpenAI's paper and Lean tree, Pálvölgyi's appendix, arXiv, OpenAlex, zbMATH, GitHub including OpenAI's forks, the Palomar registry, MathOverflow) found no prior statement. Its order-zero case is OpenAI's Proposition 7.3; its cases with algebraic coordinates (k = 0) or at most m + 4 points in affine dimension m are prior (JD-Jones-ASES/six-concyclic-lean, and the algebraic-coordinates prior work credited for Theorem A). The new content is positive transcendence degree together with quadric relations (κ ≥ 1).
- **Falsifier.** A gap in the reviewed argument; a configuration with exact Δ = 0 (maximal quadric rank,
  a basis of derivations) that is not Ramsey.
- **Starting state.** `cd probes && python c34_test.py` (about 30 s); `python -I certificates/c34_det16.py`.
- **Difficulty.** Done at `[HAND]`; a Lean proof is pure commutative algebra over OpenAI's `FieldCriterion`
  (`FRONTIER.md`, F8).

---

## Refuted (kept)

### SR-C7: specialization closure (R2)

```yaml
id: SR-C7
title: If the generic member of an irreducible family is Ramsey, every member is
status: refuted
warrant: "refuted as stated, for every d >= 3: SR-C16(a) (OpenAI's Prop. 7.3, LEAN, theirs + HAND genericity glue, reviewed once by an AI agent + exact ranks) and SR-C16(b) (HAND, reviewed by AI); the review of the refutation: one AI agent"
scope: "GENERIC_OF(V)"
difficulty: done
lean_stub: none
fc_category: "research solved (answer False) once public"
ams: ["05D10", "14Q99"]
replay: ["certificates/corank_exact.py", "probes/c15_c16.py"]
history: ["2026-10-12 filed", "2026-10-13 probe-level counter-instance off the circle (SR-C16)", "2026-10-14 refuted for every d >= 3 via OpenAI's Prop. 7.3 (reviewed once, AI)"]
```

- **Statement (refuted).** If the generic member of an irreducible family of finite spherical
  configurations is Ramsey, every member is.
- **Counterexample.** For each d ≥ 3, the family (S^{d−1})⁷ of seven-point configurations has a Ramsey
  generic member (SR-C16(a): a corollary of OpenAI's Proposition 7.3 with the genericity step) and a
  non-Ramsey member: seven points on a great circle with algebraically independent parameters (the circle
  phase diagram; Pálvölgyi's Theorems A.3 and A.7). Pálvölgyi's Theorem A.13 gives another: its explicit
  nine-point non-Ramsey set on S² is a member of (S²)⁹, whose generic member is Ramsey (SR-C29). The
  refutation was reviewed once by an AI agent. (In v1.0.0: "refuted at PROBE level if SR-C16(a) holds".)
- **Successor question (open).** The circle restriction: for irreducible families of *cyclic*
  configurations, is the Ramsey locus closed under specialization? The mirror-family attempt (SR-C16(c))
  did not refute it. It is `FRONTIER.md` F13 and a `BACKLOG.md` row; it has no entry of its own yet.
- **Starting state.** `python -I certificates/corank_exact.py c29`. For the circle question: degenerations
  of two-group families with the exact k = 1 procedure (SR-C19).

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
- **Review.** The circle glue for these instances was reviewed on 2026-10-13 by a separate (non-builder)
  AI agent, with independent sympy and python-flint re-checks; sound, wording fixes applied.
- **Scope of the novelty.** These are non-two-group Ramsey sets on the circle. Off the circle,
  non-two-group Ramsey sets already follow from OpenAI's quadric-independence criterion (SR-C29), which
  on the circle reaches at most five points.

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

### SR-C30: the phase diagram in every dimension, failing side

```yaml
id: SR-C30
title: Rational plus at least four independent points at or above N(d) are non-Ramsey, every d >= 3 (embedded S^2 cell)
status: consistent-on-sample
warrant: "SKETCH for every d, reviewed once by an AI agent (sound; the step-2 rank lemma needs a written proof); CERT per instance (exact ranks and energy forms at rational points) + HAND specialization glue for d = 3..7, 16/16"
scope: "GENERIC_OF(m rational in general position + j independent), d >= 3"
difficulty: "engineering (a non-author review of the sketch)"
lean_stub: none
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["certificates/corank_exact.py"]
history: ["2026-10-14 filed with a sketch, before its exact checks", "2026-10-14 consistent on sample (16/16 exact, d = 3..7)"]
```

- **Statement.** For every d ≥ 3, j ≥ 4 and m with m + j ≥ N(d) = (d + 1)(d + 2)/2: m points of S^{d−1}
  with rational coordinates, outside a proper Zariski-closed subset of rational m-tuples, together with
  j points whose stereographic coordinates are algebraically independent over ℚ, form a non-Ramsey set.
  With SR-C29 (Q3) and SR-C4's first half this would give SR-C17 in full.
- **Sketch `[SKETCH]`, reviewed once by an AI agent (sound)** (Lemma A.1 route). (1) Non-Ramsey passes to supersets, and extra
  free points can be specialized to rational ones, so it suffices to treat the cell (N(d) − 4, 4).
  (2) At quadric corank one a Lemma A.1 certificate is a derivation ∂ on the free coordinates with
  Σᵢ λᵢ⟨V(aᵢ), ∂aᵢ⟩ = 0 for every conformal Killing field V of S^{d−1} and E = Σᵢ λᵢ|∂aᵢ|² ≠ 0. For four
  free points the fields fixing the 2-sphere through them give vanishing conditions, so the rank of this
  system Π is at most 4d − 6 against 4(d − 1) unknowns, so its kernel has dimension at least 2. (This
  rank lemma, via the stabilizer so(W^⊥) of the 2-sphere, needs a written proof. That the kernel
  dimension matches the j(j − 3)/2 = 2 Möbius moduli of four points, and that this is why the free-point
  threshold is 3 in every dimension, is a heuristic.) (3) Special member: the S² cell (6,4) of Theorem NR-S23 on a great
  2-sphere plus N(d) − 10 rational points in general position; a block decomposition of so(1, d) gives
  rank Π = 4d − 6 with the S² kernel, on which E ≢ 0. (4) Specialization back to generic free points keeps
  corank 1, rank Π = 4d − 6 and E ≢ 0. (5) These are polynomial nonvanishing conditions on the rational
  points, so they hold outside a proper Zariski-closed set.
- **Evidence (exact).** `corank_exact.py c30`: the special member for d = 4, …, 7 and two seeded
  general-position instances for each d = 3, …, 7 have quadric corank 1, nonzero weights at the four free
  points, rank Π = 4d − 6, a two-dimensional kernel and E ≢ 0 on it; the controls with three free points
  (d = 4, 5) have kernel 0. 16/16 as predicted. Each general-position instance certifies the cell
  (N(d) − 4, 4) for those rational points directly (exact identities plus the specialization glue of
  Theorem NR-S23).
- **Prior work.** Pálvölgyi's Theorem A.12 (arXiv:2609.23327, appendix, labelled unchecked by its
  author) is the all-free cell and, by its isotropy argument, covers the cells with j(d − 1) > d(d + 1).
  The cells with 4 ≤ j and j(d − 1) ≤ d(d + 1), where the kernel is too small for the isotropy argument,
  are new.
- **Falsifier.** A rank of Π above 4d − 6 anywhere (refutes step 2); a rank below it at every seed, or
  E ≡ 0 on the kernel (breaks steps 3–4).
- **Starting state.** `python -I certificates/corank_exact.py c30` (about 10 s).
- **Difficulty.** A written proof of the step-2 rank lemma; then the entry can be promoted.

### SR-C31: the corank law for the 2-jet test on every sphere

```yaml
id: SR-C31
title: The 2-jet test fails iff (kappa = 1 and k > G_d) or (kappa >= 2 and kappa(k+1) > 2 G_d), for families in general position
status: consistent-on-sample
warrant: "(a): HAND, reviewed by one non-author AI agent; (b): exact 2-jet dual dimensions and pairings at rational specializations, 38/38 decided as predicted (three after re-specializing), plus 8/8 PROBE with the primal 2-jet"
scope: "(a): ANY; (b): GENERIC_OF(rational-affine families u_i(theta) = alpha_i + B_i theta with seeded rational coefficients)"
difficulty: "attackable (generic non-vanishing of the pairing; general position of geometric families)"
lean_stub: none
fc_category: "research open"
ams: ["05D10", "13N15"]
replay: ["certificates/corank_exact.py", "certificates/c31_respecialize.py", "probes/c31_c32_jet2.py"]
history: ["2026-10-14 filed before its probe and exact checks", "2026-10-14 consistent on sample", "2026-10-14 (a) proved after a non-author AI review"]
```

- **Setting.** A ⊂ S^{d−1}, |A| = N, with derivations D₁, …, D_k (k the Möbius-reduced transcendence
  degree), quadric corank κ (SR-C29) and quadric rank D_d, and G_d = d(d + 1)/2 = dim so(1, d). For a
  relation λ (Σᵢ λᵢpᵢpᵢᵀ = 0), Π_λ is the G_d × k matrix whose column l is the antisymmetric part of
  Σᵢ λᵢ pᵢ(D_l pᵢ)ᵀ.
- **Statement.**
  - (a) **Proved** (`[HAND]`, reviewed by one non-author AI agent), for any quadric rank and the full
    derivation module Der(F). The dual space of the 2-jet system is
    Δ(A) = {(C^ρ)_{ρ ≤ κ}, C^ρ ∈ Sym²(F^k) : Σ_ρ Π_{λ^ρ} C^ρ = 0} for a basis λ¹, …, λ^κ of relations, and
    the test fails iff some element of Δ(A) has a nonzero trace pairing with the Gram data. At corank one
    Δ = Sym²(ker Π_λ), so the 2-jet test equals the scalar test of Lemma A.1 (Pálvölgyi's method), and a
    failure that contains a corank-one failing subset has a scalar certificate (extend λ by 0).
  - (b) (conjecture; consistent on sample) For families in general position the 2-jet test fails iff
    κ = 1 and k > G_d, or κ ≥ 2 and κ(k + 1) > 2G_d. On the circle (G = 3, κ = n − 5) this is SR-C23's
    count. The dimension count holds for Π in general position (checked modulo p by the reviewer); open
    are the generic non-vanishing of the pairing and the general position of geometric families, whose
    genericity should include "no Möbius-null derivation" (no derivation moving every point by one
    conformal Killing field). Configurations with disjoint parameters (phase-diagram cells) and two-group
    sets are not in general position.
- **Evidence.** Exact (`corank_exact.py c31`): 19 cells (d, N, k) × 2 seeds on S¹ (N = 7, 8), S²
  (N = 9, …, 13) and S³ (N = 15); 35 decided at θ = 0 exactly as predicted, and 3 families had
  coincident points at θ = 0 (a degenerate specialization; the families themselves are injective) and
  decided as predicted at other rational points (`c31_respecialize.py`). Thresholds where predicted: on S², κ = 1: k = 6 pass, 7 fail; κ = 2: 5, 6;
  κ = 3: 3, 4; κ = 4: 2, 3; on S³, κ = 1: 10, 11. Every test point has maximal quadric rank
  (κ = N − D_d). The undecided family (d, N, k) = (2, 7, 2), seed 1, re-specializes to an exact pass at 2
  of 3 points (the third again has coincident points); it is not a decided mismatch. `[PROBE]` (`probes/c31_c32_jet2.py`): the primal 2-jet test of
  the probe harness agrees on the 8 S² threshold cells, with no `NO_VERDICT`. Where Δ = 0, a 2-jet pass
  is a Ramsey verdict by SR-C34.
- **Falsifier.** A decided exact verdict against (b) for a family in general position.
- **Starting state.** `python -I certificates/corank_exact.py c31` (about 20 s);
  `python -I certificates/c31_respecialize.py`; `cd probes && python c31_c32_jet2.py`.
- **Difficulty.** (b): the generic non-vanishing of the pairing, and the general position of geometric
  families.

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
  Since v1.1.0: exact per-instance certificates of the cell (N(d) − 4, 4) for seeded rational points,
  d = 3, …, 7 (SR-C30; reviewed once by an AI agent).
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
  That it is open is our inference (re-checked on the posting day, 2026-10-14).
- **A decided family** (`[HAND]`, unreviewed): for θ = πβ with β real algebraic, the radian 9-gon is
  Ramsey iff β ∈ ℚ (Gelfond–Schneider: (−1)^β is transcendental for irrational algebraic β).
- **Falsifier.** A proof in the literature that e^{ie} is transcendental (it would kill the example, not
  the framing).

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
- **Evidence, re-scoped (v1.1.0).** The `[PROBE]` evidence recorded under SR-C11 is automatic here: the
  minimal failing cells of rational plus independent points have quadric corank one, every failing cell
  contains one, and at corank one the 2-jet test equals the scalar test (SR-C31(a)). So the hypothesis has
  content only for failing configurations that contain no failing corank-one subset. SR-C32's witnesses
  have shared parameters and do not bear on it.
- **Falsifier.** A disjoint-parameter configuration that fails the 2-jet test, contains no failing
  corank-one subset, and has no scalar certificate.

### SR-C17: the phase diagram in every dimension

```yaml
id: SR-C17
title: Rational plus independent points on S^{d-1}, d >= 3
status: open
warrant: "passing side proved: SR-C2 for j <= 3; OpenAI's Prop. 7.3 + HAND genericity glue (SR-C29, reviewed once, AI) for m + j <= D_d. Failing side: CERT + glue for specific rational points, d = 3..7 (and S^2, S^3 cells in the note); every d at SKETCH, reviewed once (AI), via SR-C30; the all-free cell is Palvolgyi A.12 (unchecked appendix)"
scope: "GENERIC_OF(m rational in general position + j independent)"
difficulty: attackable
lean_stub: none
fc_category: "research open"
ams: ["05D10", "52C10"]
replay: ["probes/e1_s2.py", "probes/e3_sphere.py", "certificates/scalar_exact.py", "certificates/corank_exact.py"]
note: "Conjecture C3 (merged form); Theorem NR-S23"
history: ["2026-10-13 filed, merging SR-C3 and SR-C4", "2026-10-14 passing side proved via OpenAI's Prop. 7.3; failing side via Palvolgyi A.12 and SR-C30"]
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
  only. Passing side (proved): j ≤ 3 is SR-C4's first half (SR-C2); m + j ≤ D_d is a corollary of
  OpenAI's Proposition 7.3 (SR-C29 (Q3); genericity glue reviewed once by an AI agent).
- **Since v1.1.0.** The all-free cell (0, N(d)) is Pálvölgyi's Theorem A.12 (arXiv:2609.23327, appendix,
  labelled unchecked by its author), and its isotropy argument covers the cells with j(d − 1) > d(d + 1).
  The failing side has exact certificates (plus glue) for specific rational points for d = 3, …, 7, and
  an argument in every dimension (SR-C30, `[SKETCH]`, reviewed once by an AI agent: sound, with one rank
  lemma still to be written out). The entry stays open until that lemma is written and checked.
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

### SR-C33: finite-type reformulation; a corank-one membership test

```yaml
id: SR-C33
title: Ramsey iff b lies in Phi(m O^M) over the local ring at the diagonal; corank one reduces to one ideal membership
status: open
warrant: "(a)-(c): HAND, reviewed by one non-author AI agent; (d): conjecture"
scope: ANY
difficulty: "attackable (doubly degenerate corank-one families)"
lean_stub: none
fc_category: "research open"
ams: ["05D10", "13N15", "13D02"]
replay: []
history: ["2026-10-14 filed with sketches; no computation run", "2026-10-14 (a)-(c) proved after a non-author AI review; (d) open"]
```

- **Setting.** B = F ⊗_ℚ F, 𝔪 = ker(multiplication), O = B_𝔪 (a regular local ring with residue field F;
  for one parameter a discrete valuation ring), Φ : O^{(d+1)²} → O^N the evaluation map
  P ↦ ((pᵢ ⊗ 1)ᵀP(1 ⊗ pᵢ))ᵢ, and b = Φ(S ⊗ 1) ∈ 𝔪O^N.
- **Statement.**
  - (a) **Proved** (`[HAND]`, one non-author AI review). A is Ramsey iff b ∈ Φ(𝔪O^{(d+1)²}), membership
    taken in O. Hence for each A there is an order N(A) such that A is Ramsey iff the field criterion is
    solvable over B/𝔪^{N(A)} (by the Krull intersection theorem; N(A) is not effective). The 2-jet test is
    N = 3, and SR-C1 is the uniform statement N(A) ≤ 3.
  - (b) **Proved** (same review). κ(A) = 0 gives OpenAI's quadric-independence criterion (SR-C29) in local
    form. If κ(A) = 1, A is Ramsey iff β ∈ 𝔪·I, where I is the ideal of maximal minors of Φ and β a minor
    of [Φ_J | b]; I = 0 is allowed, and then A is Ramsey iff β = 0. For one parameter (uniformizer π):
    Ramsey iff ord_π β > ord_π I.
  - (c) **Proved** (same review). In (b) with one parameter, ord β = 2 exactly when E ≠ 0, and ord I ≥ 2
    exactly when the derivation satisfies Lemma A.1's linear conditions; the only undecided case is the
    doubly degenerate one (linear conditions hold and E = 0).
  - (d) **Open** (conjecture). At quadric corank one, A is non-Ramsey iff it has a Lemma A.1 certificate.
- **Falsifier of (d).** A doubly degenerate corank-one configuration with I ⊂ 𝔪³ and ord β ≤ ord I.
- **Starting state.** One-parameter families of 10 points on S² with a Lemma A.1 derivation and E ≡ 0;
  compute ord I and ord β exactly over ℚ(T)[U] localized at U = T (the machinery of
  `certificates/exact_circle_cert.py` generalizes).
- **Difficulty.** Attackable: construct the doubly degenerate families.

### SR-C35: a matrix-weighted Lemma A.1

```yaml
id: SR-C35
title: A nonzero pairing on the 2-jet dual space gives an explicit colouring (matrix-weighted Lemma A.1)
status: open
warrant: "SKETCH (derived by a non-author AI reviewer; not itself reviewed); the identity was exact-tested on the four SR-C32 families under random isometric embeddings into R^5, with a failing control (reviewer's check, not shipped)"
scope: ANY
difficulty: "engineering (a review); attackable (colour counts)"
lean_stub: none
fc_category: "research open"
ams: ["05D10", "13N15"]
replay: []
history: ["2026-10-14 filed (found by a non-author reviewer of SR-C32)"]
```

- **Statement `[SKETCH]`.** Let (C^ρ) ∈ Δ(A) with E = Σ_ρ tr(C^ρ M_ρ) ≠ 0 (M_ρ = Σᵢ λ^ρ_i Gramᵢ). For
  derivations ∂_l of ℝ extending the D_l, put g_ρ(x) = Σ_{j,l} C^ρ_{jl}⟨∂_j x, ∂_l x⟩. Then
  Σᵢ Σ_ρ λ^ρ_i g_ρ(a′ᵢ) = E for every congruent copy a′ = v + Qa of A. With an additive χ : ℝ → ℝ/ℤ with
  χ(E) = ½, colouring x by the 1/M-cells of (χ(φᵢ(g(x))))ᵢ, M > 2N, uses M^N colours and has no
  monochromatic copy, so A is not Ramsey.
- **Consequences, if it survives review.** The SR-C32 sets are non-Ramsey without the 2-jet necessity
  (Proposition J2), by an explicit colouring; the first step of `FRONTIER.md` F3 is essentially done.
- **Prior work.** The colouring principle is OpenAI's Proposition 2.4 (the necessity half of their criterion,
  after EGMRSS I, Lemma 15), which colours from any ℚ-linear functional on the tensor space; SR-C35 is an
  explicit derivation-energy form of such a functional, so its non-Ramsey conclusion also follows from
  OpenAI's Theorem 1.1 together with Proposition J2. Pálvölgyi's Theorem A.4 is the scalar-weight analogue
  (one weight vector with a matrix C, which reduces to a single derivation); SR-C35 lets the weight vectors
  λ^ρ vary with ρ. Literature sweep 2026-10-15: no vector-valued form of the EGMRSS Lemma 15 argument found
  (EGMRSS II and III and older surveys not read in full).
- **Credit.** Found by a non-author AI reviewer of SR-C32.
- **Falsifier.** A gap in the identity or in the colouring step.
- **Difficulty.** A review; then colour counts (SR-C21).

---

## Tailings (refuted or withdrawn, no entry of their own)

| Guess | Killed by | Warrant |
|---|---|---|
| Matrix weights in the dual of the second-order test are strictly stronger than Pálvölgyi's scalar identities | its only witness (three rational plus four independent circle points) has a scalar certificate with E = 4 (`certificates/dual_cert.py`) | `[CERT]`; withdrawn (a new witness for certificates, not colourings: SR-C32, SR-C35) |
| Poncelet chains are special (Ramsey beyond the generic threshold) | they fail at seven points like random three-parameter families (`probes/e6_wild.py`) | `[PROBE]` |
| Two Möbius groups work only on Hopf spheres | S³ two-group certificates, then SR-C2 in every dimension | `[CERT]` / `[HAND]` |
| The free-point threshold grows with d | it is 3 for d = 2, …, 9 (`probes/e3b.py`) | `[PROBE]` |
