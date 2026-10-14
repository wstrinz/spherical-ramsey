# Rope AV2: any at most six distinct points on a circle are Euclidean Ramsey

A *rope* is a standalone Lean package that anyone can check with stock
[Comparator](https://github.com/leanprover/comparator), without trusting the rest of this
repository.

**Status: [LEAN], Comparator-checked on a fresh runner.** There are no hypotheses. The
rope's `REPRODUCE` passed on a fresh GitHub-hosted runner (ubuntu-24.04, cold caches): exit 0,
all 10 Comparator runs as expected, in 30 minutes.

**Names.** That run, and the builder's own run, checked
this rope before the namespace of its own declarations was renamed to `SphericalRamsey` (names
and doc comments only; statements and proofs unchanged). For this version, fresh-runner CI on
this repository (`.github/workflows/rope-av2.yml`) is the check of record.

## Main theorem (verbatim; vocabulary is OpenAI's challenge text, `AV2Challenge/Main.lean`)

```lean
theorem circle_ramsey_of_le_six {s : ℕ} (a : Fin s → EuclideanSpace ℝ (Fin 2))
    (hs : s ≤ 6) (ha : Function.Injective a)
    (hsph : ∃ c : EuclideanSpace ℝ (Fin 2), ∃ r : ℝ, ∀ i, a i ∈ Metric.sphere c r) :
    Ramsey a
```

`Ramsey a`: for every `r ≥ 2` there is `D ≥ 1` such that every `r`-colouring of
`EuclideanSpace ℝ (Fin D)` has a monochromatic `Congruent` copy of `a`. No condition on the
coordinates. Also checked:
- `SphericalRamsey.circle_ramsey_of_le_six_mathlib`, the same in Mathlib vocabulary (Mathlib's
  `Congruent`);
- `SphericalRamsey.oai_congruent_iff` and `oai_ramsey_iff` (rope AV1's bridge), which show OpenAI's notions
  equal Mathlib's;
- `SphericalRamsey.circle_ramsey_of_le_six_nonvacuous`: six distinct points on a circle exist.

## Check

- Pinned to Lean v4.34.1 and Mathlib `d13f23b7`, OpenAI's own pin for this release.
- Stock Comparator accepts 5 challenges:
  - OpenAI's own `at_most_five_circle_points_ramsey` (which AV2 extends) and `ramsey_cospherical`,
    byte for byte;
  - `main`, `equiv` and `mathlib` against `Rope`.
- It refuses 5 controls, each with its expected reason: `sorry`, a custom axiom, an extra
  hypothesis, a redefined `Ramsey`, and a proved weaker Mathlib statement.
- All seven theorems use only `propext`, `Classical.choice` and `Quot.sound`; no `sorry`,
  `native_decide` or `ofReduceBool` in `OAI/` or `Rope/`.
- The builder's run (WSL, Landlock) is recorded in a record kept with the development sources, not in this release (pre-rename names); that record was
  written while some of its runs were still going. The fresh-runner run completed all 10.
  Statement fidelity, item by item: `FIDELITY.md`.

## Reproduce

```sh
export PATH="$HOME/.elan/bin:$HOME/go/bin:/usr/local/go/bin:$PATH"   # elan and Go must be on PATH
bash REPRODUCE
```

Needs Linux with Landlock, a non-root user, elan, Go ≥ 1.24, git, sha256sum. Non-login shells
often miss `~/.elan/bin`; without it `REPRODUCE` stops at the tool check with exit 2.
On WSL2 with a recent kernel `/sys/kernel/security/lsm` may be absent; the Landlock check is then skipped and Comparator still runs.

Preflight checks `MANIFEST`, that the challenge definitions are OpenAI's verbatim, and that the
one adapted OpenAI lemma differs only by 5 → 6. It then builds Comparator and lean4export (tag
v4.34.0, rebuilt with v4.34.1) and landrun, fetches the Mathlib cache and builds the rope. Exit 0
means all 10 runs behaved as expected.

`AV2_UPSTREAM=1` also re-checks the vendored files against openai/math on GitHub.

**Expected warnings.** The build prints `declaration uses 'sorry'` warnings for the challenge files
(`AV2Challenge/*.lean`, whose theorems are statement-only placeholders) and for the control
`AV2Control/SorryMain.lean`, and benign linter warnings (unused variables or simp arguments)
in the control files (`AV2Control/*.lean`). They are not errors. `REPRODUCE` fails if a `sorry` appears in `OAI/`
or `Rope/`.

**Time and memory.** About 25–45 min per rope with a warm Mathlib cache (23 min for this rope
in the fresh-agent reproduction), about 30 min on a fresh GitHub runner (30 min); much longer
only if other Lean builds are running at the same time: the build of OpenAI's sources and each
Comparator run (which exports and re-checks the whole tree) slow down sharply under load.
Run one rope at a time, and no other lake/Comparator jobs concurrently; each needs several GB
of memory. The Mathlib cache is shared between the ropes (and with other Lean projects on the
same pin) in `~/.cache/mathlib`, so only the first rope downloads it. Plan on about 16 GB of RAM.

## Independence

This rope **trusts OpenAI's Lean proof of #172**, checked by stock Comparator against OpenAI's public
challenge statement. Shared with OpenAI: the sufficiency direction (`fieldCriterion_ramsey`), the
circle lemmas (`CircleGeometry`, `CircleExtension`), vendored unmodified, and the definitions. What
is added:
- a certificate that six distinct unit-circle points satisfy OpenAI's `FieldCriterion` (a product
  of two Möbius graph forms), and the rotation and scaling that reduce any circle to that case;
- `extend_to_six` (OpenAI's `extend_to_five`, 5 → 6), the Mathlib restatement, and a kernel check
  through stock Comparator.

"Independent verification" covers only that kernel check.

## Prior art (no novelty claimed for the criterion)

- **JD-Jones-ASES/six-concyclic-lean** (MIT; root commit `0703d7d`, 2026-10-07, Lean
  v4.35.0-rc2) was first to prove in Lean that six concyclic points satisfy the criterion, with the
  same two-triple certificate idea. Its Ramsey conclusions assume a hypothesis `hsuff`, the
  sufficiency half of OpenAI's classification.
- **OpenAI** proved the case of at most five points (`at_most_five_circle_points_ramsey`).

AV2 adds an **unconditional** Ramsey conclusion for six points, discharging `hsuff` with OpenAI's
sorry-free proof. AV2's Lean was written independently of JD-Jones; no code was copied
(`FIDELITY.md`).

## Provenance and review

`OAI/` is OpenAI's code (openai/math `fd4aeeb2`, Apache-2.0; see `NOTICE`). Everything else, apart
from the adaptations of OpenAI lemmas that `NOTICE` lists, was written by AI agents (Claude Opus
5.5, Anthropic, in Claude Code) under the direction of the author, Will Strinz.

- `FIDELITY.md` is the assembling agent's self-assessment; it has had no non-builder review.
- A fresh AI agent (Claude Sonnet 5.5) reproduced the rope from this README and the release's
  `REPRODUCE.md` alone (exit 0, all 10 as expected); the friction it reported (linter warnings,
  times, memory, the Landlock check on WSL2) is fixed above. Because the fidelity note is only
  self-assessed, the rope stays Comparator-checked, not Lean-checked.
- **No human expert has reviewed any of it.**

## Not checked

- OpenAI's proof beyond what the kernel and Comparator check.
- Faithfulness of `Ramsey` to the literature: see `FIDELITY.md`.
- Sharpness of 6 (some 7-point circle sets are not Ramsey): cited only.
- The Mathlib-cache oleans are trusted, as Comparator's README allows.
