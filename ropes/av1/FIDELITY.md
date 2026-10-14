# AV1 fidelity note

This note checks the statements of rope AV1 against the standard list of formalization pitfalls
(pairs, metric, distinctness, embeddings, junk values, vacuity). Each item says how it was checked.
Labels:
- **PROVED**: a Lean theorem accepted by Comparator in this rope;
- **CHECKED**: a script or diff in `REPRODUCE`;
- **INFERRED**: reading the source.

## Sources and vocabulary

- **No formal-conjectures statement exists** for Graham's spherical conjecture, so the vocabulary
  is OpenAI's public Comparator challenge (openai/math `fd4aeeb2`,
  `lean/ComparatorChallenges/EuclideanRamsey.lean` and `EuclideanRamseySpherical.lean`, vendored in
  `vendor/`).
- `AV1Challenge/Main.lean` is `EuclideanRamseySpherical.lean` with only its theorem replaced.
  - Its preamble and its definitions of `Space`, `Congruent` and `Ramsey` are character for
    character the same as both OpenAI challenge files and OpenAI's `Model.lean`. **CHECKED**:
    REPRODUCE's preflight `cmp`. Comparator also refuses any difference in a constant (control
    `ctl-redeframsey`).
  - It adds 0 definitions. The vocabulary is OpenAI's 3 definitions: 7 non-blank lines, or 12
    with the preamble (`import`, `namespace`, `noncomputable section`, `open scoped`).
- `AV1Challenge/Mathlib.lean` uses Mathlib only: `EuclideanSpace ℝ (Fin d)`, `Metric.sphere`,
  Mathlib's `Congruent` (edist) and `IsAlgebraic`. It has 0 definitions.
- **OpenAI's `Congruent` and Mathlib's `Congruent` differ**, in two ways: `dist` versus `edist`,
  and argument order (`dist (b i) (b j) = dist (a i) (a j)` versus
  `edist (a i) (a j) = edist (b i) (b j)`). **PROVED** equal:
  - `SphericalRamsey.oai_congruent_iff`;
  - `SphericalRamsey.oai_ramsey_iff`: OpenAI's `Ramsey a` is equivalent to the Mathlib-vocabulary
    conclusion of `ramsey_of_algebraic_mathlib`.

  Both are in challenge `equiv`, and together they take 15 lines.
- **Comparator also accepts OpenAI's own challenges, byte for byte** against OpenAI's proof:
  - `classification`, Theorem 1.1 of #172;
  - `ramsey_cospherical`.

  So the vendored proof proves exactly OpenAI's public statements at this pin.

## Pitfalls

| Pitfall | How it was checked |
|---|---|
| Ordered vs unordered pairs | `Congruent` quantifies over all ordered pairs `(i, j)`, in both the OpenAI and Mathlib forms. The relation is symmetric and the diagonal is `0 = 0`, so ordered and unordered agree. INFERRED from the definitions; PROVED for the OpenAI/Mathlib match (`oai_congruent_iff`). |
| Metric | `Space d` is `abbrev` for `EuclideanSpace ℝ (Fin d)`, the ℓ² metric, never `Fin d → ℝ` (sup metric). The colourings live on `Space D`, the same metric. The proof unfolds `dist` with `EuclideanSpace.dist_eq` (√Σ (Δ)², `sphere_equation_descends`). INFERRED from the source; Comparator fixes the constants. |
| Injectivity / distinctness | `ha : Function.Injective a`, so the `s` points are distinct, as in the literature's "finite set". `b` is not required injective, but `Congruent a b` with injective `a` makes it so, since distances `> 0` are preserved. INFERRED. |
| Faithful vs non-faithful embeddings | A copy must preserve **every** pairwise distance (`Congruent`), not just some. In Euclidean space such a finite map extends to an isometric embedding of the affine hull of `range a` into `Space D` (`D` may be smaller than `d`), which is the standard "congruent copy" (Erdős et al. 1973). Reflections are allowed, as in the literature. INFERRED. |
| Ramsey quantifiers | `Ramsey a`: ∀ `r ≥ 2`, ∃ `D ≥ 1`, ∀ colourings `c : Space D → Fin r`, ∃ `b` with `Congruent a b` and `c ∘ b` constant. So `D` depends on `r` only, and one `D` works for all colourings; the colourings are arbitrary (no measurability); congruence is at scale 1. This is the quantifier order of Erdős et al. 1973 and of #172 §1. Omitting `r ∈ {0, 1}` is harmless (they are trivially true or vacuous), and so is requiring `D ≥ 1`. "∃ `D`" is equivalent to "∀ `D ≥ D₀`", since `Space D` embeds isometrically in `Space D'` for `D ≤ D'` and a colouring of `Space D'` restricts. INFERRED. |
| Set vs tuple | The configuration is an injective enumeration `a : Fin s → Space d` of a finite set. `Ramsey` is invariant under permuting the indices (permute `b` the same way), so it is a property of `range a`, as in the literature. INFERRED. |
| Edge cases | `hs : 2 ≤ s` excludes only `s ≤ 1`, where the statement is trivially true (a point is Ramsey). `hd : 1 ≤ d` is redundant given `s ≥ 2` and injectivity (`Space 0` has one point). INFERRED. |
| Sphericity | `hsph` (all points at one distance `ρ` from a centre `c`) is exactly `Cospherical (Set.range a)`, which is the necessity conclusion of OpenAI's `ramsey_cospherical` (challenge `oai-spherical`). INFERRED. |
| `sSup` junk values | None: there is no `sSup`, `iSup`, `⨆` or `Nat.find` in any statement. INFERRED. |
| ℕ subtraction and division | None: the ℕ facts are `2 ≤ s`, `1 ≤ d`, `2 ≤ r` and `1 ≤ D`, with no subtraction or division. `r ≥ 2` excludes only the trivial one-colour case. INFERRED. |
| Vacuous or contradictory hypotheses | **PROVED** satisfiable: `ramsey_of_algebraic_nonvacuous` gives `±e₀` in `EuclideanSpace ℝ (Fin 1)`, which is injective, has algebraic coordinates and lies on the unit sphere. `ρ < 0` or `ρ = 0` with `s ≥ 2` makes `hsph` false; that is a false instance, not a weakened theorem. |
| Vacuous conclusion | `Ramsey` is not trivially true: **PROVED** (`ramsey_cospherical`, OpenAI's challenge) every injective Ramsey configuration is cospherical. So, for example, three collinear points are not `Ramsey`. |

## Scope remarks (not pitfalls, but easy to misread)

- **Coordinate dependence.** "Algebraic coordinates" depends on the frame: the statement is about
  coordinates in the standard frame of `Space d`. `Ramsey` depends only on the distance matrix
  (it is invariant under congruence, since congruence composes). So the theorem covers every set
  congruent to one with algebraic coordinates. Equivalently, up to congruence, it covers every
  finite spherical set whose squared distances are real algebraic numbers: such a Gram matrix has
  a Cholesky factor over the real algebraic numbers. Both are INFERRED, not proved in the rope,
  which states only the coordinate form. Scope: `ALGEBRAIC`.
- **Not "real".** The conclusion fails for some spherical sets with transcendental coordinates, so
  `halg` cannot be weakened to "real". Examples: OpenAI's 9-point example, and OpenAI's separate
  formal challenge `GrahamSpherical` (openai/math `fd4aeeb2`,
  `lean/ComparatorChallenges/GrahamSpherical.lean`; not vendored here), a 12-point subset of the
  unit circle built from a Liouville-type parameter `∑ 10^{-(m+1)!}` and stated to be not
  Euclidean Ramsey. Pálvölgyi's heptagon with a transcendental parameter is cited for the same
  point; that case is not checked here (OPEN in this rope).
- **No affine-span hypothesis.** OpenAI's `classification` assumes `affineSpan ℝ (Set.range a) = ⊤`.
  AV1 does not, so it is stronger in that respect. The proof uses `fieldCriterion_ramsey`, which
  needs no span hypothesis.
- **"Spherical" means on a sphere of the ambient `Space d`.** A set on a sphere inside an affine
  subspace also lies on a sphere of the ambient space, with the same centre, so nothing is lost.

## Prior art consulted

Neither prior statement of Theorem A was consulted:
- JD-Jones-ASES/six-concyclic-lean;
- Rogerhu12/openai-math-extensions.

This rope's statements and code were written from OpenAI's challenge text and the development's own
proof of `ramsey_of_algebraic` (`Rope/AlgebraicRamsey.lean`, copied byte for byte).

## Review

Version 1.0 of this note was self-assessed by the assembling agent. A non-builder AI review
(Claude Opus 5.5, read-only, an agent that did not build the rope) found every statement faithful
and asked for fixes to this note only: the definition count, the embedding wording, and the rows
on Ramsey quantifiers, set vs tuple, edge cases, sphericity, frame dependence and the
`GrahamSpherical` example. They are applied in version 1.1. Optional extras it suggested and that
are **not** done: a non-vacuity witness with `s ≥ 3`; controls that redefine `Congruent` or
`Space`; Lean proofs of congruence invariance, of `Ramsey a ↔ Cospherical (range a)` under the
hypotheses, and of a bridge to `GrahamSpherical.EuclideanRamsey` (set and isometry form).

There has been no human review.
