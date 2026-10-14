# Rope AV3: the radian nine-gon is Euclidean Ramsey iff e^{iθ} is algebraic (Theorem D)

A *rope* is a standalone Lean package that anyone can check with stock
[Comparator](https://github.com/leanprover/comparator), without trusting the rest of this
repository.

**Status: [LEAN], Lean-checked** (Comparator-checked on a fresh runner, a non-builder AI fidelity
review, and a fresh-agent AI reproduction; see *Provenance and review*). There are no hypotheses beyond the theorems' own. The
rope's `REPRODUCE` passed on a fresh GitHub-hosted runner (ubuntu-24.04, cold caches): exit 0,
all 10 Comparator runs as expected, in 27 minutes.

**Names.** That run, and the builder's own run, checked
this rope before the namespace of its own declarations was renamed to `SphericalRamsey` (names
and doc comments only; statements and proofs unchanged). For this version, fresh-runner CI on
this repository (`.github/workflows/rope-av3.yml`) is the check of record.

## Main theorems (verbatim; vocabulary is OpenAI's challenge text plus 2 lines, `AV3Challenge/Main.lean`)

```lean
def radianConfig (θ : ℝ) (k : Fin 9) : Space 2 :=
  WithLp.toLp 2 ![Real.cos ((k : ℕ) * θ), Real.sin ((k : ℕ) * θ)]

theorem radian_configuration (θ : ℝ) (ht : Transcendental ℚ (Real.tan (θ / 2))) :
    Function.Injective (radianConfig θ) ∧ (∀ k, dist (radianConfig θ k) 0 = 1) ∧
      ¬ Ramsey (radianConfig θ)

theorem radian_ramsey_iff (θ : ℝ) (hinj : Function.Injective (radianConfig θ)) :
    Ramsey (radianConfig θ) ↔ IsAlgebraic ℚ (Real.cos θ) ∧ IsAlgebraic ℚ (Real.sin θ)

theorem radian_ramsey_iff_tan (θ : ℝ) (hinj : Function.Injective (radianConfig θ)) :
    Ramsey (radianConfig θ) ↔ IsAlgebraic ℚ (Real.tan (θ / 2))
```

These are in `OAI.EuclideanRamsey.Radian` (with `radian_not_ramsey`, the third conjunct alone).
The nine points `(cos kθ, sin kθ)`, `k = 0, …, 8`, on the unit circle: if `tan (θ/2)` is
transcendental they are distinct and **not** Euclidean Ramsey; and whenever they are distinct, they
are Ramsey iff `cos θ` and `sin θ` are algebraic (that is, iff `e^{iθ}` is algebraic), iff
`tan (θ/2)` is algebraic. `Space 2` is `EuclideanSpace ℝ (Fin 2)`, and `Ramsey` is OpenAI's
definition: for every `r ≥ 2` there is `D ≥ 1` such that every `r`-colouring of `Space D` has a
monochromatic congruent copy.

Also checked:
- `SphericalRamsey.radian_configuration_mathlib`, `radian_ramsey_iff_mathlib`,
  `radian_ramsey_iff_tan_mathlib`: the same with no definitions beyond Mathlib (the nine points
  written out, `Metric.sphere`, Mathlib's `Congruent`);
- `SphericalRamsey.oai_congruent_iff` and `oai_ramsey_iff` (rope AV1's bridge): OpenAI's notions equal
  Mathlib's.

The hypotheses are satisfiable: `ht` holds for every θ outside a countable set (the preimage of the
countably many algebraic numbers under the injective map `θ ↦ tan (θ/2)` on `(-π, π)`; INFERRED,
not in Lean). The concrete case θ = 1 needs Lindemann–Weierstrass, which is not in Mathlib at this
pin. An explicit witness is available in principle (θ = 2·arctan L with L a Liouville number, via
Mathlib's `Liouville.transcendental`), but it is not done.

## Check

- Pinned to Lean v4.34.1 and Mathlib `d13f23b7`, OpenAI's own pin for this release.
- REPRODUCE runs 5 challenges, each of which must be accepted by stock Comparator:
  - OpenAI's own `classification` and `ramsey_cospherical` challenges, byte for byte;
  - `main`, `equiv` and `mathlib` against `Rope`.
- And 5 controls, each of which must be refused with its expected reason: a `sorry` proof, a custom axiom, a weaker
  statement (an extra hypothesis), a redefined `Ramsey` (`False`), and a weaker Mathlib statement
  that was actually proved.
- All 11 theorems use only `propext`, `Classical.choice` and `Quot.sound`. There is no `sorry`,
  `native_decide` or `ofReduceBool` in `OAI/` or `Rope/`. The 9×9 determinant certificate is checked
  by `decide +kernel` over ℤ (kernel reduction; no extra axiom).
- The builder's run (WSL, Landlock): the rope's own challenges accepted and the 5 controls
  refused as expected; OpenAI's two challenges were run once outside REPRODUCE in the same work
  directory (both accepted). Results: a record kept with the development sources, not in this release (pre-rename names). Statement fidelity, item by
  item: `FIDELITY.md`.

## Reproduce

```sh
export PATH="$HOME/.elan/bin:$HOME/go/bin:/usr/local/go/bin:$PATH"   # elan and Go must be on PATH
bash REPRODUCE
```

Prerequisites: Linux with Landlock, a non-root user, and elan, Go ≥ 1.24, git and sha256sum on
`PATH`. Non-login shells often miss `~/.elan/bin`; without it `REPRODUCE` stops at the tool check
with exit 2. On WSL2 with a recent kernel `/sys/kernel/security/lsm` may be absent; the Landlock check is then skipped and Comparator still runs.

What it does:
- Preflight checks `MANIFEST`, checks that the challenge definitions are OpenAI's verbatim, and that
  `radianConfig` (2 lines) is the solution's verbatim.
- It builds Comparator and lean4export (tag v4.34.0, rebuilt with v4.34.1) and landrun.
- It fetches the Mathlib cache and builds the rope.
- Exit 0 means all 10 runs behaved as expected.

`AV3_UPSTREAM=1` also re-checks the vendored files against openai/math on GitHub.

**Expected warnings.** The build prints `declaration uses 'sorry'` warnings for the challenge files
(`AV3Challenge/*.lean`, whose theorems are statement-only placeholders) and for the control
`AV3Control/SorryMain.lean`, and benign linter warnings (unused variables or simp arguments)
in the control files (`AV3Control/*.lean`). They are not errors. `REPRODUCE` fails if a `sorry` appears in `OAI/`
or `Rope/`.

**Time and memory.** About 25–45 min per rope with a warm Mathlib cache (45 min for this rope
in the fresh-agent reproduction), about 30 min on a fresh GitHub runner (27 min); much longer
only if other Lean builds are running at the same time: the build of OpenAI's sources and each
Comparator run (which exports and re-checks the whole tree) slow down sharply under load.
Run one rope at a time, and no other lake/Comparator jobs concurrently; each needs several GB
of memory. The Mathlib cache is shared between the ropes (and with other Lean projects on the
same pin) in `~/.cache/mathlib`, so only the first rope downloads it. Plan on about 16 GB of RAM.

## Independence

This rope **trusts OpenAI's Lean proof of #172**, checked by stock Comparator against OpenAI's public
challenge statement. Shared with OpenAI, vendored unmodified and imported: the definitions, the
linear obstruction `NineLinearObstruction.not_ramsey_of_det_ne_zero` (through OpenAI's necessity
direction), `IndependentTensor` (`ℚ(t) ⊗ ℚ(t) ↪ ℚ(T, U)`), `CircleConsequence.circle_five_affineSpan`,
and, for the converse, `fieldCriterion_ramsey` through rope AV1's `ramsey_of_algebraic`. Adapted with
attribution (see `NOTICE`): 6 lines of local instances and one proof pattern from OpenAI's
`NineField.lean`. What is added (589 lines, `Rope/Radian*.lean`):
- half-angle trigonometry: the coordinate field is `ℚ(tan (θ/2))`;
- a one-parameter determinant: the denominator-cleared 9×9 evaluation matrix is nonsingular,
  certified at `(T, U) = (2, 3)` by an explicit integer triangular factorization (`decide +kernel`),
  replacing OpenAI's nine-parameter Kronecker argument;
- the converse via rope AV1, the Mathlib restatement, and a kernel check through stock Comparator.

All of the rope's own Lean was produced by AI agents (Claude Opus 5.5, Anthropic). "Independent verification" covers only that
kernel check.

## Prior art (none found)

- No prior statement of Theorem D was found (the prior-work searches for this release).
- OpenAI's Proposition 7.6 (#172) is the generic nine-parameter case: nine points on a circle with
  algebraically independent parameters are not Ramsey. It does not apply directly to Theorem D,
  whose nine angles `kθ` all depend on one parameter.

## Provenance and review

`OAI/` is OpenAI's code (openai/math `fd4aeeb2`, Apache-2.0; see `NOTICE`). Everything else, apart
from the adaptations of OpenAI lemmas that `NOTICE` lists, was written by AI agents (Claude Opus
5.5, Anthropic, in Claude Code) under the direction of the author, Will Strinz.
`Rope/Radian*.lean` and `Rope/AlgebraicRamsey.lean` (rope AV1) are the development's proof files,
copied unchanged apart from doc comments (references to unpublished notes replaced by references
to the note).

- `FIDELITY.md` is the assembling agent's self-assessment. It had a non-builder AI review (Claude
  Opus 5.5, read-only): faithful, fixes to this note only (applied).
- A fresh AI agent (Claude Sonnet 5.5) reproduced the rope from this README and the release's
  `REPRODUCE.md` alone (exit 0, all 10 as expected); the friction it reported (linter warnings,
  times, memory, the Landlock check on WSL2) is fixed above.
- **No human expert has reviewed any of it.**

## Not checked

- Any explicit θ (for example θ = 1) satisfying `ht`.
- The `ℂ` form `IsAlgebraic ℚ (Complex.exp (θ * I))` of the iff (not stated).
- OpenAI's proof is trusted only as far as the kernel and Comparator check it.
- Faithfulness of OpenAI's `Ramsey` to the literature's definition: see `FIDELITY.md` and rope AV1.
- The Mathlib-cache oleans are trusted, as Comparator's README allows.
