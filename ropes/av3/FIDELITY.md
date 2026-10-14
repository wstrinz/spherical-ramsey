# AV3 fidelity note

This note checks the statements of rope AV3 against the standard list of formalization pitfalls
(pairs, metric, distinctness, embeddings, junk values, vacuity), plus the items the non-builder
review of rope AV1's note found missing there: Ramsey quantifiers, set vs tuple, edge cases, basis dependence and sphericity. Each
item says how it was checked. Labels:
- **PROVED**: a Lean theorem accepted by Comparator in this rope;
- **CHECKED**: a script or diff in `REPRODUCE`;
- **INFERRED**: reading the source.

## Sources and vocabulary

- **No formal-conjectures statement exists** for Euclidean Ramsey sets (a code search of its default branch), so the
  vocabulary is OpenAI's public Comparator challenge (openai/math `fd4aeeb2`, vendored in `vendor/`).
- `AV3Challenge/Main.lean` is OpenAI's preamble and its definitions of `Space`, `Congruent` and
  `Ramsey`, character for character (**CHECKED**: REPRODUCE's preflight `cmp` against both OpenAI
  challenge files and `Model.lean`; Comparator refuses a redefined `Ramsey`, control
  `ctl-redeframsey`), then `radianConfig` and the four theorems.
- **Definition count.** OpenAI's vocabulary is 7 non-blank lines (3 definitions; 12 with the
  preamble). AV3 adds **2 lines of statement definitions**, `radianConfig`, the solution's own
  definition verbatim (**CHECKED**: REPRODUCE's preflight `cmp` against `Rope/Radian.lean`).
  Proof-internal definitions (52 lines in `Rope/Radian*.lean`, including the 12-line integer
  certificate `Lcert`) are in no statement.
- `AV3Challenge/Mathlib.lean` uses Mathlib only; it has 0 definitions. The nine points are written
  out with a `let`, and they are `radianConfig θ` by definition (`rfl`); "on the unit circle" is
  `Metric.sphere 0 1`; the Ramsey property is unfolded through `oai_ramsey_iff` (Mathlib's
  `Congruent`).
- **OpenAI's `Congruent` and Mathlib's `Congruent` differ** (`dist` vs `edist`, and argument order).
  **PROVED** equal (`SphericalRamsey.oai_congruent_iff`, `oai_ramsey_iff`, challenge `equiv`; rope AV1's
  bridge, same statements and proofs).
- **Comparator also accepts OpenAI's own challenges**, byte for byte against OpenAI's proof
  (`classification`, `ramsey_cospherical`).

## Hypotheses and the junk value of `tan`

| Hypothesis | Role | Check |
|---|---|---|
| `ht : Transcendental ℚ (Real.tan (θ / 2))` | the non-Ramsey direction | Mathlib's `Real.tan x = sin x / cos x` with `x / 0 = 0`, so at `cos (θ/2) = 0` (θ ≡ π mod 2π) `tan (θ/2) = 0`, which is algebraic. So `ht` excludes θ ≡ π (`cos_half_ne`), where the points are `±1` and Ramsey. The junk value makes the statement *more* restrictive there, never wrong. INFERRED from the definitions; the exclusion is PROVED inside the proof |
| `hinj : Function.Injective (radianConfig θ)` | the two iff theorems only | needed for the ⇐ direction (rope AV1 requires distinct points). For the ⇒ direction (non-Ramsey) distinctness is a **conclusion** (`radian_configuration`), not a hypothesis |

- The iffs need no condition on θ besides `hinj`. At θ ≡ π, the only place where `tan` takes its
  junk value, the nine points alternate between (1,0) and (−1,0), so `hinj` fails and the iffs say
  nothing. INFERRED; the iffs are PROVED for every θ.
- No other hypothesis is used, and OpenAI's `Ramsey` is not modified.

## Pitfalls

| Pitfall | How it was checked |
|---|---|
| Ramsey quantifiers | `Ramsey a`: ∀ `r ≥ 2`, ∃ `D ≥ 1`, ∀ colourings `c : Space D → Fin r`, ∃ `b` with `Congruent a b` and `c ∘ b` constant. `D` depends on `r` only, and one `D` works for all colourings; colourings are arbitrary functions; congruence is at scale 1. "∃ D" is equivalent to "∀ D ≥ D₀". **¬ Ramsey** therefore says: for some `r ≥ 2`, every `D ≥ 1` has an `r`-colouring of `Space D` with no monochromatic congruent copy. Same quantifier order as EGMRSS 1973 (checked against #172 §1 by the non-builder review of rope AV1). INFERRED; the definition is OpenAI's verbatim (CHECKED). |
| Ordered vs unordered pairs | `Congruent` quantifies over all ordered pairs; symmetric, diagonal `0 = 0`. INFERRED; PROVED for the OpenAI/Mathlib match. |
| Set vs tuple | `radianConfig θ` is a 9-tuple. When it is injective, `Ramsey` is a property of its range (invariant under permuting indices). When it is not injective (θ a rational multiple of π with small denominator), the iffs do not apply (`hinj`), and the non-Ramsey theorem cannot apply either, since it proves injectivity. INFERRED. |
| Metric | `Space 2 = EuclideanSpace ℝ (Fin 2)`, the ℓ² metric; `dist (radianConfig θ k) 0 = 1` is the unit circle in that metric. INFERRED. |
| Injectivity / distinctness | See the hypotheses table. PROVED (conclusion) / hypothesis. |
| Faithful vs non-faithful embeddings | `Congruent` preserves every pairwise distance; a finite congruence extends to an isometric embedding of the affine hull into `Space D`. INFERRED. |
| `sSup` junk values | None. The only junk value is `tan` at odd multiples of π/2 (above). INFERRED. |
| ℕ subtraction and division | None in the statements. `(k : ℕ) * θ` casts the index to ℕ then ℝ; `k` ranges over `0, …, 8`. INFERRED. |
| Edge cases | θ ≡ 0 mod 2π: all nine points equal `(1, 0)`; not injective, so only the junk-free part matters: `tan 0 = 0` is algebraic, so `ht` fails and the theorem is silent. θ ≡ π: covered above. θ a rational multiple of π: `tan (θ/2)` is algebraic (INFERRED), so the non-Ramsey theorem is silent, as it must be (the points are then algebraic and Ramsey by AV1 when distinct). |
| Vacuous or contradictory hypotheses | `ht` holds for all but countably many θ (INFERRED: the algebraic reals are countable and `θ ↦ tan (θ/2)` is injective on `(-π, π)`). **Not exhibited in Lean.** θ = 1 needs Lindemann–Weierstrass, which is not in Mathlib at this pin. An explicit witness is available in principle (θ = 2·arctan L with L a Liouville number, via Mathlib's `Liouville.transcendental`), but it is not done. The iffs need only `hinj`, which holds for example at θ = 1 (INFERRED). |
| Vacuous conclusion | `Ramsey` is not trivially true (**PROVED**, OpenAI's `ramsey_cospherical`), and `¬ Ramsey` of these points is a real obstruction (OpenAI's linear obstruction with a nonzero determinant). Both sides of each iff occur: algebraic θ-points are Ramsey (AV1), transcendental ones are not. INFERRED. |

## Scope remarks (not pitfalls, but easy to misread)

- **Basis dependence.** The points are given in the standard frame, on the unit circle about `0`,
  starting at `(1, 0)`. `Ramsey` is invariant under congruence, so the theorems cover every
  congruent copy (any centre, any starting angle `θ₀`: the points `θ₀ + kθ` on any unit circle).
  INFERRED; the rope states only the normalized form.
- **Sphericity.** The points lie on the unit circle (`radian_configuration`, second conjunct).
- **Scope.** Non-Ramsey: `TRANSCENDENTAL_PARAM(tan(θ/2))`. The iff: `ANY` real θ with distinct
  points (see the note, Theorem D).
- **Not "real".** The verdict flips between algebraic and transcendental θ, as the iff shows.

## Prior art consulted

None found (the prior-work searches for this release and for mobius-ramsey). OpenAI's Proposition 7.6 is the generic nine-parameter case; its
Lean proof (`EuclideanRamseyNine`) is the template this proof mirrors (see `NOTICE`).

## Review

This note was self-assessed by the agent that assembled the rope. It had a non-builder AI review
(Claude Opus 5.5, read-only): faithful, fixes to this note only (applied). A fresh AI agent
(Claude Sonnet 5.5) then reproduced the rope from its README alone (exit 0, all 10 as expected),
so the rope is Lean-checked: fresh-runner Comparator, non-builder fidelity review, fresh-agent
reproduction. There has been no human review.
