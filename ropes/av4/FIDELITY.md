# AV4 fidelity note

This note checks the statements of rope AV4 against the standard list of formalization pitfalls
(pairs, metric, distinctness, embeddings, junk values, vacuity), plus the items the non-builder
review of rope AV1's note found missing there: Ramsey quantifiers, set vs tuple, edge cases, basis dependence and sphericity. Each
item says how it was checked. Labels:
- **PROVED**: a Lean theorem accepted by Comparator in this rope;
- **CHECKED**: a script or diff in `REPRODUCE`;
- **INFERRED**: reading the source.

## Sources and vocabulary

- **No formal-conjectures statement exists** for Möbius invariance of the Euclidean Ramsey property
  (and none for Euclidean Ramsey sets at all; a code search of its default branch). The vocabulary is OpenAI's
  public Comparator challenge (openai/math `fd4aeeb2`, `lean/ComparatorChallenges/EuclideanRamsey.lean`
  and `EuclideanRamseySpherical.lean`, vendored in `vendor/`), plus three statement definitions.
- The challenge is split by solution module (see "Comparator note" below). `AV4Challenge/Defs.lean`
  is OpenAI's preamble and its definitions of `Space`, `Congruent` and `Ramsey`, character for
  character (**CHECKED**: REPRODUCE's preflight `cmp` against both OpenAI
  challenge files and `Model.lean`), then the three statement definitions (no theorems).
- **Definition count.** OpenAI's vocabulary is 7 non-blank lines (3 definitions; 12 with the
  preamble). AV4 adds **7 lines of statement definitions**:
  - `lorentzForm d` (2 lines): `S = diag(-1, 1, …, 1)`, indexed by `Option (Fin d)` with `none`
    as the extra (time) coordinate, as in OpenAI's `augmented`;
  - `aug x` (3 lines): the augmented vector `(1, x)`;
  - `mobiusMap L x` (2 lines): the spatial part of `L (1, x)` divided by its `none` coordinate.

  They are the solution's own definitions verbatim (**CHECKED**: REPRODUCE's preflight `cmp`
  against `Rope/MobiusDefs.lean`), and Comparator refuses any difference in a constant (control
  `ctl-redefmobius`: `mobiusMap L x := x`). `AV4Challenge/Cor.lean` adds the circle chart
  `circ t = ((1 - t²)/(1 + t²), 2t/(1 + t²))` (2 lines, verbatim from `Rope/MobiusCorCircle.lean`,
  CHECKED), and `AV4Challenge/Sanity.lean` adds `liftO Q = diag(1, Q)` (5 lines, verbatim from
  `Rope/MobiusSanity.lean`, CHECKED). Total non-OpenAI statement definitions: 14 lines. Proof-internal definitions (`Nondeg`, `ι₁`, `ι₂`, `μ`, `τ`, `symmetrize`, and
  the transport helpers) are not in any statement.
- `AV4Challenge/Mathlib.lean` uses Mathlib only: `EuclideanSpace ℝ (Fin d)`, `Metric.sphere`,
  `Matrix.diagonal`, `Option.elim`, `*ᵥ`, `WithLp.toLp` and Mathlib's `Congruent`. It
  has 0 definitions: the Lorentz form and the Möbius image are written out inline.
- **OpenAI's `Congruent` and Mathlib's `Congruent` differ** (`dist` vs `edist`, and argument order).
  **PROVED** equal (`SphericalRamsey.oai_congruent_iff`, `oai_ramsey_iff`, challenge `equiv`; rope AV1's
  bridge, same statements and proofs).
- **Comparator also accepts OpenAI's own challenges**, byte for byte against OpenAI's proof
  (`classification`, `ramsey_cospherical`), so the vendored proof proves OpenAI's public statements.

## The Möbius model (the main fidelity question)

- **"Möbius" means `PO(1,d)` via the classical identification.** A Möbius transformation of
  `S^{d-1}` is modelled as `φ_L = mobiusMap L` for a real `(1+d) × (1+d)` matrix `L` with
  `Lᵀ S L = S` (`L ∈ O(1,d)`). `L` permutes the null lines of `S`; the null line through `(1, x)`,
  `x ∈ S^{d-1}`, goes to the null line through `(1, φ_L x)`. That the maps `φ_L` are exactly the
  conformal (Möbius) transformations of `S^{d-1}`, `Möb(S^{d-1}) ≅ PO(1,d)`, is **classical and
  cited, not proved here** (the note cites it; so does mobius-ramsey's note).
- **What is proved about the model** (**PROVED**, challenge `sanity`):
  - `mobiusMap_bijOn`: every `φ_L`, `L ∈ O(1,d)`, is a bijection of the unit sphere onto itself;
  - `liftO_lorentz`, `mobiusMap_liftO`: every orthogonal `Q` gives `L = diag(1, Q) ∈ O(1,d)` with
    `φ_L x = Q x`. So all isometries of the sphere (rotations and reflections) are in the model.
- **Non-isometric maps are in the model** (**PROVED**, challenge `cor`): `exists_mobius_circ_mul`
  and `exists_mobius_circ_add` give explicit `L ∈ O(1,2)` (a boost and a parabolic element) acting
  on the circle chart as `t ↦ k t` (`k ≠ 0`) and `t ↦ t + c`. For `k ∉ {±1}` or `c ≠ 0` these do
  not preserve distances (INFERRED: they move three chart points `0, 1, -1` to points with
  different pairwise distances), so the model is not just the isometry group.
- **Signs.** `L` and `-L` give the same `φ_L` (the quotient by `±1` is why the group is `PO(1,d)`).
  No time-orientation condition is imposed, so the model includes both components; INFERRED from
  the definition.
- **Off the sphere `mobiusMap` is junk** (Lean's `x / 0 = 0`). The theorem only evaluates it at the
  points `a i`, which lie on the sphere, where the divisor is nonzero (`time_ne_zero`, in the proof).

## Comparator note: one challenge file per solution module

A first local run used a single challenge file with Theorem C, the corollaries and the model checks.
Comparator refused it: `Const does not match between challenge and target
'OAI.EuclideanRamsey.Mobius.circ'`. Cause (CHECKED with `set_option pp.all true`): Lean abstracts
the proof of `Nat.AtLeastTwo 2` inside the numeral `2` into an auxiliary lemma, shared within a
module. In the single challenge file `circ`'s body pointed at `mobiusMap._proof_1` (from the
earlier `mobiusMap`); in the solution, `circ` lives in its own module and points at
`circ._proof_1`. The statements were identical as text. Fix: `Defs.lean` holds the vocabulary,
and `Main.lean`, `Cor.lean`, `Sanity.lean` each import it and mirror one solution module, so every
auxiliary name agrees. Comparator's README trusts the challenge's import closure, so the split adds
nothing to trust; REPRODUCE checks that each of the three imports only `AV4Challenge.Defs`.

## Hypotheses

| Hypothesis | Role | Check |
|---|---|---|
| `hL : Lᵀ * lorentzForm d * L = lorentzForm d` | `L ∈ O(1,d)`: the Möbius map | the model above |
| `ha : Function.Injective a` | distinct points (a set of `s` points) | INFERRED |
| `hsph : ∀ i, a i ∈ Metric.sphere 0 1` | the points lie on the **unit** sphere centred at `0` | INFERRED; a general sphere reduces to it by a similarity, which is not formalized here |

- **No spanning hypothesis.** The points need not affinely span `ℝ^d` (they may lie on a smaller
  subsphere). This matches Theorem C as stated in the note. An earlier Lean form
  (`ramsey_iff_ramsey_mobius'`) carried `hspan` on `a`; it was removed at the criterion level
  (`realCriterion_of_ramsey`, `realCriterion_mobius_full`). The `hspan` form is not in this rope.
- No `2 ≤ s` and no `1 ≤ d`: for `s ≤ 1` both sides are Ramsey (`ramsey_of_lt_two`; the empty
  family is Ramsey under OpenAI's definition, vacuously).
- No other hypothesis is used, and OpenAI's `Ramsey` is not modified. The weaker-statement control
  (`ctl-weakermain`) re-adds `hspan` and an assumption of the conclusion; Comparator refuses it.

## Pitfalls

| Pitfall | How it was checked |
|---|---|
| Ramsey quantifiers | `Ramsey a`: ∀ `r ≥ 2`, ∃ `D ≥ 1`, ∀ colourings `c : Space D → Fin r`, ∃ `b` with `Congruent a b` and `c ∘ b` constant. `D` depends on `r` only, and one `D` works for all colourings; colourings are arbitrary functions (no measurability); congruence is at scale 1. Omitting `r ∈ {0, 1}` is harmless (those cases are trivial or vacuous), and so is requiring `D ≥ 1`. "∃ D" is equivalent to "∀ D ≥ D₀", since a copy in `Space D` embeds in `Space D'`, `D' ≥ D`. Same quantifier order as EGMRSS 1973 (checked against #172 §1 by the non-builder review of rope AV1). INFERRED; the definition is OpenAI's verbatim (CHECKED). |
| Ordered vs unordered pairs | `Congruent` quantifies over all ordered pairs; it is symmetric and the diagonal is `0 = 0`. INFERRED; PROVED for the OpenAI/Mathlib match (`oai_congruent_iff`). |
| Set vs tuple | `a` is an injective enumeration of an `s`-point set. `Ramsey` is invariant under permuting the indices (permute `b` the same way), so `Ramsey a` is a property of `Set.range a`; and `φ_L ∘ a` enumerates `φ_L (range a)` injectively (PROVED inside the proof: `mobiusMap_injOn`). INFERRED. |
| Metric | `Space d` is `EuclideanSpace ℝ (Fin d)`, the ℓ² metric; the unit sphere is `Metric.sphere 0 1` in that metric. INFERRED; Comparator fixes the constants. |
| Injectivity / distinctness | `ha`. The image is injective, proved. INFERRED. |
| Faithful vs non-faithful embeddings | `Congruent` preserves every pairwise distance; a finite congruence extends to an isometric embedding of the affine hull of `range a` into `Space D` (`D` may be smaller than `d`). INFERRED (wording from the non-builder review of rope AV1). |
| `sSup` junk values | None in any statement. The only junk value is division by `0` in `mobiusMap` off the sphere (see the model section). INFERRED. |
| ℕ subtraction and division | None: the ℕ facts are `2 ≤ r`, `1 ≤ D`. INFERRED. |
| Edge cases | `s = 0`: both sides are Ramsey (vacuous copies). `s = 1`: both sides are Ramsey (one point). `d = 0`: the unit sphere is empty, so `s = 0`. Points on a lower-dimensional subsphere (not spanning): covered. All PROVED inside the theorem; INFERRED for the case analysis. |
| Vacuous or contradictory hypotheses | **PROVED** satisfiable: `ramsey_iff_ramsey_mobius_nonvacuous` gives `±e₀` in `EuclideanSpace ℝ (Fin 1)`, `L = 1`; and the corollaries apply the theorem to non-isometric `L` (`ramsey_circ_mul`, `ramsey_circ_add`). |
| Vacuous conclusion | `Ramsey` is not trivially true (**PROVED**, OpenAI's `ramsey_cospherical`: every injective Ramsey configuration is cospherical), and it is not trivially false (rope AV1). An iff could be vacuous only if both sides were constant on the class, which they are not: on the circle there are Ramsey and non-Ramsey sets (AV1; rope AV3). INFERRED. |
| Mathlib restatement | `ramsey_iff_ramsey_mobius_mathlib` writes `lorentzForm d` as `Matrix.diagonal (fun α => Option.elim α (-1) fun _ => 1)` (definitionally equal) and `aug x` as `fun α => Option.elim α 1 fun k => x k` (equal by cases, proved in the rope); its conclusion is `oai_ramsey_iff` applied to both sides. PROVED. |

## Scope remarks (not pitfalls, but easy to misread)

- **Basis dependence.** None: the theorem has no algebraicity hypothesis. Both sides are properties
  of the configuration up to congruence, and the unit sphere about `0` is a normalization (any
  sphere is similar to it, and `Ramsey` is invariant under similarity: congruence composes, and a
  scaled copy of a Ramsey set is Ramsey since `Space D` is scale-invariant; INFERRED).
- **Sphericity.** `hsph` puts the points on the unit sphere. A non-spherical set is never Ramsey
  (OpenAI's `ramsey_cospherical`), so Theorem C loses nothing by assuming it. Scope: `ANY` (the
  coordinates of `a` and the entries of `L` are arbitrary reals).
- **Corollaries.** `ramsey_mobius_of_algebraic`: scope `MOBIUS_ORBIT_OF(ALGEBRAIC)` (the
  pre-image has algebraic coordinates in the standard frame; `L` is arbitrary real). `circ` is the
  stereographic chart from the pole `(-1, 0)` (`circ t → (-1, 0)` as `t → ±∞`, never reached), so
  `{circ (k tᵢ)}` and `{circ (tᵢ + c)}` are honest point sets on the unit circle; the `_rat` forms
  need distinct rational `tᵢ` (`ht`), and `k ≠ 0` (for `k = 0` all points collapse to `(1, 0)`).
  INFERRED from the statements.
- **Consequence not formalized.** On the circle, Theorem C makes Ramsey-ness depend only on
  cross-ratios (by hand, in the note and in mobius-ramsey's note). No such corollary is stated in this rope.

## Prior art consulted

None found (the prior-work searches for this release and for mobius-ramsey). Pálvölgyi's Lemma A.5 is certificate-level, with an explicit
disclaimer; it was not used.

## Review

This note was self-assessed by the agent that assembled the rope. It has had no non-builder review
of its own. The same four statements (Theorem C and the three corollaries, same definitions) are
the published package mobius-ramsey v1.0.0 (DOI 10.5281/zenodo.23339523), whose fidelity table
(`docs/FIDELITY.md` there) had a non-builder AI review (Claude Opus 5.5) on a Lean v4.35 port of
this proof. There has been no human review of the Lean; the author's read of the hand proof of
Theorem C is an owner's read by a non-expert, not expert review and not a review of this rope.
