# AV5 fidelity note

This note checks the statements of rope AV5 against the standard list of formalization pitfalls
(pairs, metric, distinctness, embeddings, junk values, vacuity), plus the items the non-builder
review of rope AV1's note found missing there: Ramsey quantifiers, set vs tuple, edge cases, basis dependence and sphericity. Each
item says how it was checked. Labels:
- **PROVED**: a Lean theorem accepted by Comparator in this rope;
- **CHECKED**: a script or diff in `REPRODUCE`;
- **INFERRED**: reading the source.

## Sources and vocabulary

- **No formal-conjectures statement exists** for Euclidean Ramsey sets (a code search of its default branch), so the
  vocabulary is OpenAI's public Comparator challenge (openai/math `fd4aeeb2`, vendored in `vendor/`).
- `AV5Challenge/Main.lean` is OpenAI's preamble and its definitions of `Space`, `Congruent` and
  `Ramsey`, character for character (**CHECKED**: REPRODUCE's preflight `cmp` against both OpenAI
  challenge files and `Model.lean`; Comparator also refuses a redefined `Ramsey`, control
  `ctl-redeframsey`), then the theorem.
- **Definition count.** OpenAI's vocabulary is 7 non-blank lines (3 definitions; 12 with the
  preamble). AV5 adds **0 statement definitions**: the hypotheses use only Mathlib
  (`EuclideanSpace ℝ (Fin 2)`, `Metric.sphere`, `Finset.card`, `IsAlgebraic`). Proof-internal
  definitions (`hd`, `Alg`, `tp`, `j₁`, `j₂`, `jm`; and AV2's `tpar`, `ι₁`, `ι₂`, `μ`,
  `stereographic`, the certificate algebra) are in no statement.
- `AV5Challenge/Mathlib.lean` uses Mathlib only; it has 0 definitions. Its hypotheses are the
  OpenAI statement's, verbatim except that the radius is named `ρ`; its conclusion is OpenAI's
  `Ramsey a` unfolded through `oai_ramsey_iff` (Mathlib's `Congruent`).
- **OpenAI's `Congruent` and Mathlib's `Congruent` differ** (`dist` vs `edist`, and argument order).
  **PROVED** equal (`SphericalRamsey.oai_congruent_iff`, `oai_ramsey_iff`, challenge `equiv`; rope AV1's
  bridge, same statements and proofs).
- **Comparator also accepts OpenAI's own challenges**, byte for byte against OpenAI's proof
  (`classification`, `ramsey_cospherical`).

## Hypotheses

| Hypothesis | Role | Check |
|---|---|---|
| `ha : Function.Injective a` | distinct points | INFERRED |
| `hsph : ∃ c r, ∀ i, a i ∈ Metric.sphere c r` | concyclic; centre and radius arbitrary reals (not assumed algebraic) | INFERRED. For `s ≥ 7` the proof derives that `c` and `r` are algebraic from three algebraic points (`circum_C0`, `circum_C1`, `alg_of_sq`) |
| `T : Finset (Fin s)`, `hT : T.card ≤ 3` | the exceptional indices | INFERRED |
| `halg : ∀ i ∉ T, ∀ j, IsAlgebraic ℚ (a i j)` | every coordinate of every point outside `T` is algebraic over `ℚ` | INFERRED; no condition at all on the points of `T` |

No other hypothesis is used, and OpenAI's `Ramsey` is not modified.

## Pitfalls

| Pitfall | How it was checked |
|---|---|
| Ramsey quantifiers | `Ramsey a`: ∀ `r ≥ 2`, ∃ `D ≥ 1`, ∀ colourings `c : Space D → Fin r`, ∃ `b` with `Congruent a b` and `c ∘ b` constant. `D` depends on `r` only, and one `D` works for all colourings; colourings are arbitrary functions; congruence is at scale 1. Omitting `r ∈ {0, 1}` is harmless, and so is requiring `D ≥ 1`. "∃ D" is equivalent to "∀ D ≥ D₀", since a copy in `Space D` embeds in `Space D'`, `D' ≥ D`. Same quantifier order as EGMRSS 1973 (checked against #172 §1 by the non-builder review of rope AV1). INFERRED; the definition is OpenAI's verbatim (CHECKED). |
| Ordered vs unordered pairs | `Congruent` quantifies over all ordered pairs; symmetric, diagonal `0 = 0`. INFERRED; PROVED for the OpenAI/Mathlib match. |
| Set vs tuple | `a` is an injective enumeration of an `s`-point set. `Ramsey` is invariant under permuting indices, and the hypotheses are too (permute `T` with them), so the theorem is about the set `range a` with at most three exceptional points. INFERRED. |
| Metric | `EuclideanSpace ℝ (Fin 2)`, the ℓ² metric; the circle is `Metric.sphere c r` in that metric. INFERRED. |
| Injectivity / distinctness | `ha`. INFERRED. |
| Faithful vs non-faithful embeddings | `Congruent` preserves every pairwise distance; a finite congruence extends to an isometric embedding of the affine hull of `range a` into `Space D`. INFERRED. |
| `sSup` junk values | None in any statement. INFERRED. |
| ℕ subtraction and division | None: the ℕ facts are `T.card ≤ 3`, `2 ≤ r`, `1 ≤ D`. INFERRED. |
| Edge cases | `s ≤ 1`: Ramsey trivially (one point, or none). `s ≤ 6`: covered by AV2 (`circle_ramsey_of_le_six`) whatever `T` is; every case with at most two algebraic points has `s ≤ 5`. `r < 0` in `hsph`: no point, so `s = 0`. `r = 0`: all points equal the centre, so `s ≤ 1` (`zero_radius_ramsey`). `T` may contain algebraic points; `T = ∅` is the plane case of rope AV1. INFERRED for the case analysis; each case is PROVED inside the theorem. |
| Vacuous or contradictory hypotheses | **PROVED** satisfiable with `T` nonempty: `ramsey_alg_plus_three_nonvacuous` gives `±e₀` on the unit circle, `T = {0, 1}`. That witness is small; the theorem's content beyond AV1 and AV2 is `s ≥ 7` with non-algebraic points in `T`, which is not exhibited in Lean (a witness is possible in principle, for example circ(L) = ((1 − L²)/(1 + L²), 2L/(1 + L²)) with L a Liouville number via Mathlib's `Liouville.transcendental`, plus six rational circle points; not done). |
| Vacuous conclusion | `Ramsey` is not trivially true: **PROVED** (OpenAI's `ramsey_cospherical`) every injective Ramsey configuration is cospherical. It is also not true of all concyclic sets: OpenAI's nine-point example and rope AV3 give non-Ramsey concyclic sets, which have at least four non-algebraic points. INFERRED. |

## Scope remarks (not pitfalls, but easy to misread)

- **Basis dependence.** "Algebraic coordinates" depends on the frame. `Ramsey` is invariant under
  congruence, so the theorem covers every set congruent to one satisfying the hypotheses. INFERRED,
  not proved in the rope. Scope: `ALGEBRAIC ∪ 3·ANY` (see the note, Theorem B(b)).
- **Sphericity.** The points lie on a circle in the plane. A non-cospherical set is never Ramsey
  (OpenAI's `ramsey_cospherical`), so concyclicity is necessary in the plane, not a convenience.
- **Sharpness of "three".** The circle phase diagram (the note, Proposition PD, `[HAND]`) says four
  independent transcendental points with three rational ones can already fail; that is not checked
  in this rope.
- **Dimension.** The theorem is for the plane (`Fin 2`). Concyclic points in a plane of `ℝ^d` are
  congruent to planar ones, so it covers them up to congruence (INFERRED).

## Prior art consulted

None found (the prior-work searches for this release and for mobius-ramsey). Pálvölgyi's A.10 says only that his certificates fail for this
class; it was not used.

## Review

This note was self-assessed by the agent that assembled the rope. It had a non-builder AI review
(Claude Opus 5.5, read-only): faithful, fixes to this note only (applied). A fresh AI agent
(Claude Sonnet 5.5) then reproduced the rope from its README alone (exit 0, all 10 as expected),
so the rope is Lean-checked: fresh-runner Comparator, non-builder fidelity review, fresh-agent
reproduction. There has been no human review.
