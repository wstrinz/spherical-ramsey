# Rope AV1: spherical configurations with algebraic coordinates are Euclidean Ramsey

A *rope* is a standalone Lean package that anyone can check with stock
[Comparator](https://github.com/leanprover/comparator), without trusting the rest of this
repository. This one is version 1.1 (documentation fixes) with the namespace of the rope's own
declarations renamed to `SphericalRamsey`; statements and proofs are unchanged since 1.0.

**Status: [LEAN], Lean-checked** (Comparator-checked on a fresh runner, a non-builder AI fidelity
review, and a fresh-agent AI reproduction; see *Provenance and review*). There are no hypotheses beyond the
theorem's own. The rope's `REPRODUCE` passed on a fresh GitHub-hosted runner (ubuntu-24.04, cold
caches, upstream re-check on): exit 0, all 10 Comparator runs as expected, in 27 minutes.

**Names.** That run, and the builder's own run, checked
this rope before the namespace of its own declarations was renamed to `SphericalRamsey` (names
and doc comments only; statements and proofs unchanged). For this version, fresh-runner CI on
this repository (`.github/workflows/rope-av1.yml`) is the check of record.

## Main theorem (verbatim; vocabulary is OpenAI's challenge text, `AV1Challenge/Main.lean`)

```lean
theorem ramsey_of_algebraic {s d : ℕ} (a : Fin s → Space d)
    (hs : 2 ≤ s) (hd : 1 ≤ d) (ha : Function.Injective a)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j))
    (hsph : ∃ c : Space d, ∃ ρ : ℝ, ∀ i, dist (a i) c = ρ) :
    Ramsey a
```

This is `OAI.EuclideanRamsey.ramsey_of_algebraic`. `Space d` is `EuclideanSpace ℝ (Fin d)`.
`Ramsey a`: for every `r ≥ 2` there is `D ≥ 1` such that every `r`-colouring of `Space D` has a
monochromatic `Congruent` copy of `a`. Also checked:
- `SphericalRamsey.ramsey_of_algebraic_mathlib`, the same in Mathlib vocabulary (`Metric.sphere`,
  Mathlib's `Congruent`);
- `SphericalRamsey.oai_congruent_iff` and `oai_ramsey_iff`, which show OpenAI's notions equal Mathlib's;
- `SphericalRamsey.ramsey_of_algebraic_nonvacuous`, which shows the hypotheses can be met.

## Check

- Pinned to Lean v4.34.1 and Mathlib `d13f23b7`, OpenAI's own pin for this release.
- Stock Comparator accepts 5 challenges:
  - OpenAI's own `classification` and `ramsey_cospherical` challenges, byte for byte;
  - `main`, `equiv` and `mathlib` against `Rope`.
- It refuses 5 controls, each with its expected reason: a `sorry` proof, a custom axiom, a weaker
  statement (an extra hypothesis), a redefined `Ramsey`, and a weaker Mathlib statement that was
  actually proved.
- All seven theorems use only `propext`, `Classical.choice` and `Quot.sound`. There is no `sorry`,
  `native_decide` or `ofReduceBool` in `OAI/` or `Rope/`.
- Results of the builder's run (WSL Ubuntu, Landlock): a record kept with the development sources, not in this release (pre-rename names). Statement
  fidelity, item by item: `FIDELITY.md`.

## Reproduce

```sh
export PATH="$HOME/.elan/bin:$HOME/go/bin:/usr/local/go/bin:$PATH"   # elan and Go must be on PATH
bash REPRODUCE
```

Prerequisites: Linux with Landlock, a non-root user, and elan, Go ≥ 1.24, git and sha256sum on
`PATH`. Non-login shells (for example `wsl --exec bash -c …`) often miss `~/.elan/bin`; without it
`REPRODUCE` stops at the tool check with exit 2. Install elan with
`curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y --default-toolchain none`.
On WSL2 with a recent kernel `/sys/kernel/security/lsm` may be absent; the Landlock check is then skipped and Comparator still runs.

What it does:
- Preflight checks `MANIFEST`, and checks that the challenge definitions are OpenAI's verbatim.
- It builds Comparator and lean4export (tag v4.34.0, rebuilt with v4.34.1) and landrun.
- It fetches the Mathlib cache and builds the rope.
- Exit 0 means all 10 runs behaved as expected.

`AV1_UPSTREAM=1` also re-checks the vendored files against openai/math on GitHub.

**Expected warnings.** The build prints `declaration uses 'sorry'` warnings for the challenge files
(`AV1Challenge/*.lean`, whose theorems are statement-only placeholders) and for the control
`AV1Control/SorryMain.lean`, and benign linter warnings (unused variables or simp arguments)
in the control files (`AV1Control/*.lean`). They are not errors. `REPRODUCE` fails if a `sorry` appears in `OAI/`
or `Rope/`, the code that is checked.

**Time and memory.** Plan on about **16 GB of RAM** (8 parallel jobs) and several GB of disk for
the Mathlib cache. Each Comparator run exports and re-checks the whole OpenAI tree, so it takes
minutes, not seconds.

| Machine | Wall clock for `bash REPRODUCE` |
|---|---|
| Fresh GitHub runner, cold caches | 27 min |
| Desktop (WSL, 8 threads), idle | about 1.5 h (rope build 20 min; 10 Comparator runs 35 to 60 min) |
| Same desktop, heavily loaded, warm caches | 5 h 50 min (rope build 2 h 28 min; Comparator runs 13 to 51 min each) |
| Desktop (WSL, 8 cores), warm Mathlib cache, one rope at a time (fresh-agent reproduction) | 32 min |

Expect about 25–45 min per rope with a warm Mathlib cache, about 30 min on a fresh GitHub runner;
much longer only if other Lean builds are running at the same time (the rows above with hours).
Run one rope at a time, and no other lake/Comparator jobs concurrently; each needs several GB
of memory. The Mathlib cache is shared between the ropes (and with other Lean projects on the
same pin) in `~/.cache/mathlib`, so only the first rope downloads it.

## Independence

This rope **trusts OpenAI's Lean proof of #172**, checked by stock Comparator against OpenAI's public
challenge statement. Shared with OpenAI: the whole sufficiency direction (`fieldCriterion_ramsey`),
vendored unmodified, and the definitions. What is added:
- the ~105-line step `fieldCriterion_of_algebraic` (algebraic coordinates ⇒ OpenAI's field
  criterion, via a separability idempotent);
- the Mathlib restatement;
- a kernel check through stock Comparator.

All of the rope's own Lean was produced by AI agents (Claude Opus 5.5, Anthropic). "Independent
verification" covers only that kernel check.

## Prior art (no novelty is claimed for the theorem)

Theorem A was stated before this rope:
- **JD-Jones-ASES/six-concyclic-lean** (MIT; root commit `0703d7d`, 2026-10-07, Lean
  v4.35.0-rc2) proves in Lean, unconditionally, that a spherical set with algebraic coordinates
  satisfies the criterion. Its Ramsey conclusions assume a hypothesis `hsuff`, the sufficiency
  half of OpenAI's classification.
- **Rogerhu12/openai-math-extensions** (`f8a2bb2`, 2026-10-07/08) states Theorem A in TeX, with the
  same idempotent proof.
- **atimics/math2** (`8ab51fa`, 2026-10-08) proves it in Lean, end to end and unconditionally, for
  algebraic configurations with full affine span.

What AV1 adds is a further unconditional Lean proof with no affine-span hypothesis. It builds on
OpenAI's complete, sorry-free proof. This rope's code was written without consulting these
repositories.

## Provenance and review

`OAI/` is OpenAI's code (openai/math `fd4aeeb2`, Apache-2.0; see `NOTICE`). Everything else was
written by AI agents (Claude Opus 5.5, Anthropic, in Claude Code) under the direction of the
author, Will Strinz.

- `FIDELITY.md` had a non-builder AI review (Claude Opus 5.5): faithful, with fixes to the note
  only; the fixes are applied in this version.
- A fresh AI agent (Claude Sonnet 5.5) reproduced the rope from this README alone (exit 0, all 10
  as expected); the friction it reported (PATH, times, expected warnings) is fixed above. A second
  fresh-agent reproduction, of this release's renamed version, passed too (exit 0, all 10 as
  expected, 32 min); its friction notes (linter warnings, times, memory) are also fixed above.
- **No human expert has reviewed any of it.**

## Not checked

- OpenAI's proof is trusted only as far as the kernel and Comparator check it. Its mathematics has
  not been reviewed here.
- Faithfulness of OpenAI's `Ramsey` to the literature's definition: see `FIDELITY.md`.
- The Mathlib-cache oleans are trusted, as Comparator's README allows.
