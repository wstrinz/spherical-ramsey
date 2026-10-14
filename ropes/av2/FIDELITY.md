# AV2 fidelity note

This note checks the statements of rope AV2 against the standard list of formalization pitfalls
(pairs, metric, distinctness, embeddings, junk values, vacuity). Each item says how it was checked. Labels:
- **PROVED**: a Lean theorem accepted by Comparator in this rope;
- **CHECKED**: a script or diff in `REPRODUCE`;
- **INFERRED**: reading the source.

## Sources and vocabulary

- **No formal-conjectures statement exists** for "every set of at most six concyclic points is
  Ramsey", so the vocabulary is OpenAI's public Comparator challenge (openai/math `fd4aeeb2`,
  `lean/ComparatorChallenges/EuclideanRamseyCircle.lean` and `EuclideanRamseySpherical.lean`,
  vendored in `vendor/`).
- `AV2Challenge/Main.lean` is `EuclideanRamseySpherical.lean` with only its theorem replaced.
  - Its preamble and its definitions of `Space`, `Congruent` and `Ramsey` are character for
    character the same as OpenAI's spherical challenge and OpenAI's `Model.lean`, and the three
    definitions are the same as in OpenAI's circle challenge. **CHECKED**: REPRODUCE's preflight
    `cmp`. Comparator also refuses any difference in a constant (control `ctl-redeframsey`).
  - It adds 0 definitions. The vocabulary is OpenAI's 3 definitions: 7 non-blank lines, or 12
    with the preamble.
- The statement writes the plane as `EuclideanSpace ℝ (Fin 2)` (which `Space 2` abbreviates) and
  "on a circle" as Mathlib's `Metric.sphere c r`, as the development's theorem does. OpenAI's
  five-point challenge writes `∃ c r, ∀ i, dist (a i) c = r`; `Metric.mem_sphere` is that equation
  by definition.
- `AV2Challenge/Mathlib.lean` uses Mathlib only: `EuclideanSpace ℝ (Fin 2)`, `Metric.sphere` and
  Mathlib's `Congruent` (edist). It has 0 definitions.
- **OpenAI's `Congruent` and Mathlib's `Congruent` differ**, in two ways: `dist` versus `edist`,
  and argument order. **PROVED** equal by rope AV1's bridge, reused here with the same statements
  and proofs: `SphericalRamsey.oai_congruent_iff` and `SphericalRamsey.oai_ramsey_iff` (challenge `equiv`, which is
  AV1's `Equiv.lean` byte for byte).
- **Comparator also accepts OpenAI's own challenges, byte for byte**, against OpenAI's proof:
  - `at_most_five_circle_points_ramsey`: every nonempty set of at most five distinct concyclic
    points is Ramsey. AV2 strictly extends it (six points; `s = 0` allowed).
  - `ramsey_cospherical`.

## Pitfalls

| Pitfall | How it was checked |
|---|---|
| Ordered vs unordered pairs | `Congruent` quantifies over all ordered pairs `(i, j)`, in both the OpenAI and Mathlib forms. The relation is symmetric and the diagonal is `0 = 0`, so ordered and unordered agree. INFERRED from the definitions; PROVED for the OpenAI/Mathlib match (`oai_congruent_iff`). |
| Metric | The configuration lives in `EuclideanSpace ℝ (Fin 2)`, the ℓ² plane, never `Fin 2 → ℝ` (sup metric) or `ℝ × ℝ`. The colourings live on `Space D = EuclideanSpace ℝ (Fin D)`. The proof computes distances with `EuclideanSpace.dist_eq` (`dist_sq_two` in `Rope/SixPoint.lean`). INFERRED from the source; Comparator fixes the constants. |
| Injectivity / distinctness | `ha : Function.Injective a`, so the `s` points are distinct. Without it the theorem would be about multisets, and a repeated point is harmless anyway. `b` is not required injective, but `Congruent a b` with injective `a` makes it so. INFERRED. |
| Faithful vs non-faithful embeddings | A copy must preserve **every** pairwise distance (`Congruent`), not just some. In Euclidean space such a finite map extends to an isometry: the standard "congruent copy". INFERRED. |
| `sSup` junk values | None: there is no `sSup`, `iSup`, `⨆` or `Nat.find` in any statement. INFERRED. |
| ℕ subtraction and division | None: the ℕ facts are `s ≤ 6`, `2 ≤ r` and `1 ≤ D`, with no subtraction or division. `s` may be 0 or 1; those cases are true and harmless. INFERRED. |
| Vacuous or contradictory hypotheses | **PROVED** satisfiable at the full size `s = 6`: `circle_ramsey_of_le_six_nonvacuous` gives six distinct points `(±1, 0)`, `(0, ±1)`, `±(3/5, 4/5)` on the unit circle. A negative radius makes `hsph` false for `s ≥ 1` (an empty sphere); radius 0 forces `s ≤ 1`. These are false or degenerate instances, not a weakened theorem. |
| Vacuous conclusion | `Ramsey` is not trivially true: **PROVED** (`ramsey_cospherical`, OpenAI's challenge) every injective Ramsey configuration is cospherical, so three collinear points are not `Ramsey`. |

## Scope remarks (not pitfalls, but easy to misread)

- **No condition on the coordinates.** Unlike AV1, the points may have transcendental coordinates.
  Scope: `ANY`. The proof rotates and scales the circle to the unit circle off the pole
  `(-1, 0)`; the normalized configuration has its own coordinate field, and `Ramsey` transfers back
  along the similarity (`ramsey_of_scaled`).
- **Six is the limit of this statement.** Some 7-point subsets of a circle are not Ramsey
  (Pálvölgyi, arXiv:2609.23327, Thm A.3; cited, not checked in this rope; see also the note and
  the ledger). So `s ≤ 6` cannot be raised to 7 without a further hypothesis.
- **The plane only.** The theorem is stated for circles of `EuclideanSpace ℝ (Fin 2)`. A circle in
  a higher-dimensional space is congruent to a planar one, and `Ramsey` is congruence-invariant, but
  the rope does not state or prove that transfer.
- **No affine-span hypothesis.** OpenAI's `classification` assumes `affineSpan ℝ (Set.range a) = ⊤`;
  AV2 does not, and its proof uses `fieldCriterion_ramsey`, which needs none.

## Independence from the prior Lean proof of the criterion

- JD-Jones-ASES/six-concyclic-lean (root `0703d7d`) proves first, in Lean, that six concyclic points
  satisfy the criterion; its Ramsey conclusion assumes `hsuff`.
- AV2's Lean was written by an AI agent whose certificate draft existed before it read that
  repository, which it did afterwards, at the coordinating agent's request, for a line-count
  comparison. Changes after that reading were
  compile-error fixes only. No code was ported or adapted, so no MIT attribution is needed. The
  shared helper name `det3` is a standard name.
- This rope was assembled without consulting that repository.
- The only borrowed code is OpenAI's: vendored unmodified, plus `extend_to_six` (Apache-2.0, see
  `NOTICE`; **CHECKED** by REPRODUCE to be `extend_to_five` with 5 replaced by 6).

## Review

This note was self-assessed by the agent that assembled the rope. It has had no non-builder
review. There has been no human review.
