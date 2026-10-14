# Rope AV5: algebraic concyclic points plus at most three arbitrary points are Euclidean Ramsey

A *rope* is a standalone Lean package that anyone can check with stock
[Comparator](https://github.com/leanprover/comparator), without trusting the rest of this
repository.

**Status: [LEAN], Lean-checked** (Comparator-checked on a fresh runner, a non-builder AI fidelity
review, and a fresh-agent AI reproduction; see *Provenance and review*). There are no hypotheses beyond the theorem's own. The
rope's `REPRODUCE` passed on a fresh GitHub-hosted runner (ubuntu-24.04, cold caches): exit 0,
all 10 Comparator runs as expected, in 27 minutes.

**Names.** That run, and the builder's own run, checked
this rope before the namespace of its own declarations was renamed to `SphericalRamsey` (names
and doc comments only; statements and proofs unchanged). For this version, fresh-runner CI on
this repository (`.github/workflows/rope-av5.yml`) is the check of record.

## Main theorem (verbatim; vocabulary is OpenAI's challenge text, `AV5Challenge/Main.lean`)

```lean
theorem ramsey_alg_plus_three {s : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin 2))
    (ha : Function.Injective a)
    (hsph : ∃ c : EuclideanSpace ℝ (Fin 2), ∃ r : ℝ, ∀ i, a i ∈ Metric.sphere c r)
    (T : Finset (Fin s)) (hT : T.card ≤ 3) (halg : ∀ i ∉ T, ∀ j, IsAlgebraic ℚ (a i j)) :
    Ramsey a
```

This is `OAI.EuclideanRamsey.ramsey_alg_plus_three` (claim B(b) of the note). Finitely many
distinct points on one circle in the plane, all of whose coordinates are algebraic except for the
points with indices in a set `T` of at most three, form a Euclidean Ramsey configuration. Neither
the centre nor the radius is assumed algebraic, and `s` is unbounded. `Ramsey` is OpenAI's
definition: for every `r ≥ 2` there is `D ≥ 1` such that every `r`-colouring of
`EuclideanSpace ℝ (Fin D)` has a monochromatic congruent copy.

Also checked:
- `SphericalRamsey.ramsey_alg_plus_three_mathlib`, the same in Mathlib vocabulary (Mathlib's `Congruent`);
- `SphericalRamsey.oai_congruent_iff` and `oai_ramsey_iff` (rope AV1's bridge): OpenAI's notions equal
  Mathlib's;
- `SphericalRamsey.ramsey_alg_plus_three_nonvacuous`: the hypotheses can be met with `T` nonempty.

## Check

- Pinned to Lean v4.34.1 and Mathlib `d13f23b7`, OpenAI's own pin for this release.
- REPRODUCE runs 5 challenges, each of which must be accepted by stock Comparator:
  - OpenAI's own `classification` and `ramsey_cospherical` challenges, byte for byte;
  - `main`, `equiv` and `mathlib` against `Rope`.
- And 5 controls, each of which must be refused with its expected reason: a `sorry` proof, a custom axiom, a weaker
  statement (an extra hypothesis), a redefined `Ramsey`, and a weaker Mathlib statement that was
  actually proved.
- All 7 theorems use only `propext`, `Classical.choice` and `Quot.sound`. There is no `sorry`,
  `native_decide` or `ofReduceBool` in `OAI/` or `Rope/`.
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
- Preflight checks `MANIFEST`, and checks that the challenge definitions are OpenAI's verbatim.
- It builds Comparator and lean4export (tag v4.34.0, rebuilt with v4.34.1) and landrun.
- It fetches the Mathlib cache and builds the rope.
- Exit 0 means all 10 runs behaved as expected.

`AV5_UPSTREAM=1` also re-checks the vendored files against openai/math on GitHub.

**Expected warnings.** The build prints `declaration uses 'sorry'` warnings for the challenge files
(`AV5Challenge/*.lean`, whose theorems are statement-only placeholders) and for the control
`AV5Control/SorryMain.lean`, and benign linter warnings (unused variables or simp arguments)
in the control files (`AV5Control/*.lean`). They are not errors. `REPRODUCE` fails if a `sorry` appears in `OAI/`
or `Rope/`.

**Time and memory.** About 25–45 min per rope with a warm Mathlib cache (33 min for this rope
in the fresh-agent reproduction), about 30 min on a fresh GitHub runner (27 min); much longer
only if other Lean builds are running at the same time: the build of OpenAI's sources and each
Comparator run (which exports and re-checks the whole tree) slow down sharply under load.
Run one rope at a time, and no other lake/Comparator jobs concurrently; each needs several GB
of memory. The Mathlib cache is shared between the ropes (and with other Lean projects on the
same pin) in `~/.cache/mathlib`, so only the first rope downloads it. Plan on about 16 GB of RAM.

## Independence

This rope **trusts OpenAI's Lean proof of #172**, checked by stock Comparator against OpenAI's public
challenge statement. Shared with OpenAI, vendored unmodified and imported (none copied): the
definitions (`Ramsey`, `Congruent`, `FieldCriterion`, `coordinate`, `augmented`, `multiply`) and the sufficiency direction
`fieldCriterion_ramsey`. What is added:
- the case `s ≤ 6` (rope AV2, six concyclic points: `Rope/SixPoint*.lean`, 531 lines);
- for `s ≥ 7` (`Rope/AlgPlusThree*.lean`, 473 lines): the centre and radius are algebraic (three
  algebraic points fix the circle), a rational rotation moves the pole off the configuration, and
  an explicit `FieldCriterion` certificate `P = e · g_w · (s − s')` is built, with `e` the
  separability idempotent of the number field of the algebraic points;
- the Mathlib restatement and a kernel check through stock Comparator.

All of the rope's own Lean was produced by AI agents (Claude Opus 5.5, Anthropic). "Independent verification" covers only that
kernel check.

## Prior art (no novelty claim is made here; none found)

- No prior statement of this result was found (the prior-work searches for this release).
- Pálvölgyi's A.10 says only that his *certificates* fail for this class; it is not a statement
  about the Ramsey property.
- Rope AV1 (algebraic coordinates) is the case `T = ∅`, restricted to the plane.

## Provenance and review

`OAI/` is OpenAI's code (openai/math `fd4aeeb2`, Apache-2.0; see `NOTICE`). Everything else, apart
from the adaptations of OpenAI lemmas that `NOTICE` lists, was written by AI agents (Claude Opus
5.5, Anthropic, in Claude Code) under the direction of the author, Will Strinz.
`Rope/SixPoint*.lean` (as in rope AV2) and `Rope/AlgPlusThree*.lean` are the development's proof
files, copied unchanged apart from doc comments (references to unpublished notes replaced by
references to the note).

- `FIDELITY.md` is the assembling agent's self-assessment. It had a non-builder AI review (Claude
  Opus 5.5, read-only): faithful, fixes to this note only (applied).
- A fresh AI agent (Claude Sonnet 5.5) reproduced the rope from this README and the release's
  `REPRODUCE.md` alone (exit 0, all 10 as expected); the friction it reported (linter warnings,
  times, memory, the Landlock check on WSL2) is fixed above.
- **No human expert has reviewed any of it.**

## Not checked

- OpenAI's proof is trusted only as far as the kernel and Comparator check it. Its mathematics has
  not been reviewed here.
- Faithfulness of OpenAI's `Ramsey` to the literature's definition: see `FIDELITY.md` and rope AV1.
- The Mathlib-cache oleans are trusted, as Comparator's README allows.
