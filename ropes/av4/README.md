# Rope AV4: the Ramsey property of a spherical set is Möbius invariant (Theorem C)

A *rope* is a standalone Lean package that anyone can check with stock
[Comparator](https://github.com/leanprover/comparator), without trusting the rest of this
repository.

**Status: [LEAN], Comparator-checked on a fresh runner.** There are no hypotheses beyond the theorem's own. The
rope's `REPRODUCE` passed on a fresh GitHub-hosted runner (ubuntu-24.04, cold caches): exit 0,
all 12 Comparator runs as expected, in 31 minutes.

**Names.** That run, and the builder's own run, checked
this rope before the namespace of its own declarations was renamed to `SphericalRamsey` (names
and doc comments only; statements and proofs unchanged). For this version, fresh-runner CI on
this repository (`.github/workflows/rope-av4.yml`) is the check of record.

## Main theorem (verbatim; `AV4Challenge/Main.lean`, vocabulary in `AV4Challenge/Defs.lean`: OpenAI's challenge text plus 7 lines)

```lean
def lorentzForm (d : ℕ) : Matrix (Option (Fin d)) (Option (Fin d)) ℝ :=
  Matrix.diagonal fun α => Option.elim α (-1) fun _ => 1

def aug (x : Space d) : Option (Fin d) → ℝ
  | none => 1
  | some j => x j

def mobiusMap (L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ) (x : Space d) : Space d :=
  WithLp.toLp 2 fun j => (L *ᵥ aug x) (some j) / (L *ᵥ aug x) none

theorem ramsey_iff_ramsey_mobius_full {s d : ℕ} (a : Fin s → Space d)
    (L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ)
    (hL : Lᵀ * lorentzForm d * L = lorentzForm d) (ha : Function.Injective a)
    (hsph : ∀ i, a i ∈ Metric.sphere (0 : Space d) 1) :
    Ramsey a ↔ Ramsey (mobiusMap L ∘ a)
```

This is `OAI.EuclideanRamsey.Mobius.ramsey_iff_ramsey_mobius_full`: for every finite set of
distinct points on the unit sphere of `ℝ^d` (no spanning hypothesis, any `s`, any `d`) and every
`L ∈ O(1,d)`, the set is Euclidean Ramsey iff its Möbius image is. `Space d` is
`EuclideanSpace ℝ (Fin d)`, and `Ramsey` is OpenAI's definition: for every `r ≥ 2` there is
`D ≥ 1` such that every `r`-colouring of `Space D` has a monochromatic congruent copy.

**What "Möbius" means here.** A Möbius transformation of the unit sphere `S^{d-1}` is modelled as
`mobiusMap L` for a real matrix `L` with `Lᵀ S L = S`, `S = diag(-1, 1, …, 1)`: that is, `L ∈ O(1,d)`
acting on the null lines of `S`, and `mobiusMap L x` is the point where the line of `L (1, x)` meets
the chart `{first coordinate = 1}`. That these maps are exactly the Möbius group of `S^{d-1}`
(`Möb(S^{d-1}) ≅ PO(1,d)`) is the **classical identification; it is cited, not proved** in this
rope. What is proved about the model: every such map is a bijection of the unit sphere, every
orthogonal map `x ↦ Qx` is one of them, and the non-isometric maps `t ↦ kt`
and `t ↦ t + c` of the circle chart are given by explicit `L ∈ O(1,2)`.

## Corollaries (`AV4Challenge/Cor.lean`, with the 2-line chart `circ`)

```lean
def circ (t : ℝ) : Space 2 :=
  WithLp.toLp 2 ![(1 - t ^ 2) / (1 + t ^ 2), 2 * t / (1 + t ^ 2)]

theorem ramsey_mobius_of_algebraic {s d : ℕ} (a : Fin s → Space d)
    (L : Matrix (Option (Fin d)) (Option (Fin d)) ℝ)
    (hL : Lᵀ * lorentzForm d * L = lorentzForm d) (ha : Function.Injective a)
    (hsph : ∀ i, a i ∈ Metric.sphere (0 : Space d) 1)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j)) :
    Ramsey (mobiusMap L ∘ a)

theorem ramsey_circ_mul_rat {s : ℕ} (t : Fin s → ℚ) (ht : Function.Injective t) (k : ℝ)
    (hk : k ≠ 0) : Ramsey (fun i => circ (k * (t i : ℝ)))

theorem ramsey_circ_add_rat {s : ℕ} (t : Fin s → ℚ) (ht : Function.Injective t) (c : ℝ) :
    Ramsey (fun i => circ ((t i : ℝ) + c))
```

So Möbius images of algebraic spherical sets are Ramsey; and for distinct rational parameters
`tᵢ` and any real `k ≠ 0` and `c` (transcendental allowed), `{circ (k tᵢ)}` and `{circ (tᵢ + c)}`
are Ramsey. The challenge also has `ramsey_circ_mul` and `ramsey_circ_add` (algebraic parameters)
and `exists_mobius_circ_mul`, `exists_mobius_circ_add` (the explicit maps).

Also checked:
- `mobiusMap_bijOn`, `liftO_lorentz`, `mobiusMap_liftO` (fidelity of the model; 5 more definition
  lines, `liftO Q = diag(1, Q)`);
- `SphericalRamsey.ramsey_iff_ramsey_mobius_mathlib`, the main theorem with no definitions beyond Mathlib
  (`Metric.sphere`, Mathlib's `Congruent`, the Lorentz form and the Möbius image written out);
- `SphericalRamsey.oai_congruent_iff` and `oai_ramsey_iff` (rope AV1's bridge): OpenAI's notions equal
  Mathlib's;
- `SphericalRamsey.ramsey_iff_ramsey_mobius_nonvacuous`: the hypotheses can be met.

## Check

- Pinned to Lean v4.34.1 and Mathlib `d13f23b7`, OpenAI's own pin for this release.
- REPRODUCE runs 7 challenges, each of which must be accepted by stock Comparator:
  - OpenAI's own `classification` and `ramsey_cospherical` challenges, byte for byte;
  - `main` (Theorem C), `cor` (the 7 corollaries), `sanity` (the 3 model checks), `equiv` and
    `mathlib`, against `Rope`. `main`, `cor` and `sanity` share the vocabulary file
    `AV4Challenge/Defs.lean` (OpenAI's definitions and the 7 Lorentz-model lines), which they
    import.
- And 5 controls, each of which must be refused with its expected reason: a `sorry` proof, a custom axiom, a weaker
  statement (extra hypotheses), a redefined `mobiusMap` (the identity), and a weaker Mathlib
  statement that was actually proved.
- All 17 theorems use only `propext`, `Classical.choice` and `Quot.sound`. There is no `sorry`,
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
- Preflight checks `MANIFEST`, checks that the challenge definitions are OpenAI's verbatim, and that
  the 7 statement-definition lines (and `circ`, `liftO`) are the solution's verbatim.
- It builds Comparator and lean4export (tag v4.34.0, rebuilt with v4.34.1) and landrun.
- It fetches the Mathlib cache and builds the rope.
- Exit 0 means all 12 runs behaved as expected.

`AV4_UPSTREAM=1` also re-checks the vendored files against openai/math on GitHub.

**Expected warnings.** The build prints `declaration uses 'sorry'` warnings for the challenge files
(`AV4Challenge/*.lean`, whose theorems are statement-only placeholders) and for the control
`AV4Control/SorryMain.lean`, and benign linter warnings (unused variables or simp arguments)
in the control files (`AV4Control/*.lean`). They are not errors. `REPRODUCE` fails if a `sorry` appears in `OAI/`
or `Rope/`.

**Time and memory.** About 25–45 min per rope with a warm Mathlib cache (27 min for this rope
in the fresh-agent reproduction), about 30 min on a fresh GitHub runner (31 min); much longer
only if other Lean builds are running at the same time: the build of OpenAI's sources and each
Comparator run (which exports and re-checks the whole tree) slow down sharply under load.
Run one rope at a time, and no other lake/Comparator jobs concurrently; each needs several GB
of memory. The Mathlib cache is shared between the ropes (and with other Lean projects on the
same pin) in `~/.cache/mathlib`, so only the first rope downloads it. Plan on about 16 GB of RAM.

## Independence

This rope **trusts OpenAI's Lean proof of #172**, checked by stock Comparator against OpenAI's public
challenge statement. Shared with OpenAI, vendored unmodified and imported (none copied): the
definitions; the necessity direction to the real criterion (`ramsey_realCriterion`); the
congruence lemmas (`full_affine_representative`, `congruent_linearIsometry`,
`ramsey_congruent_iff`, `singleton_ramsey`); the descent `realCriterion_fieldCriterion`; and the
sufficiency `fieldCriterion_ramsey`. The corollaries also use rope AV1's `ramsey_of_algebraic`.
What is added (`Rope/Mobius*.lean`, about 1,050 lines):
- the Lorentz-model algebra: `L⁻¹ = S Lᵀ S`, `L (1, x) = μ (1, φ_L x)` with `μ ≠ 0` on the sphere,
  injectivity;
- the transport of OpenAI's real criterion along `L` with no spanning hypothesis
  (`realCriterion_mobius_full`), and its transfer along affine isometric embeddings
  (`realCriterion_of_isometry`), which removes the span hypothesis from OpenAI's necessity
  direction (`realCriterion_of_ramsey`);
- the corollaries, the Mathlib restatement and a kernel check through stock Comparator.

All of the rope's own Lean was produced by AI agents (Claude Opus 5.5, Anthropic). "Independent verification" covers only that
kernel check.

## Published home of Theorem C

Theorem C and these corollaries are published in **mobius-ramsey v1.0.0** (Will Strinz, 2026;
Zenodo DOI [10.5281/zenodo.23339523](https://doi.org/10.5281/zenodo.23339523), concept DOI
10.5281/zenodo.23339522; https://github.com/wstrinz/mobius-ramsey). That package is the citable
home of Theorem C: the same statements and the same proof, ported to Lean v4.35 and the module
system, checked by the toolchain's `lake comparator` with three kernels, with a note giving the
hand proof. This rope is the original Lean v4.34.1 development on OpenAI's own pin, kept here so
that the other ropes and the note can refer to one toolchain.

## Prior art (no prior statement found)

- No prior statement of Theorem C was found (the prior-work searches for mobius-ramsey; its
  `docs/PRIOR-WORK-SEARCH.md`).
- Pálvölgyi's Lemma A.5 is certificate-level (about his certificates, not the Ramsey property), with
  an explicit disclaimer.

## Provenance and review

`OAI/` is OpenAI's code (openai/math `fd4aeeb2`, Apache-2.0; see `NOTICE`). Everything else was
written by AI agents (Claude Opus 5.5, Anthropic, in Claude Code) under the direction of the
author, Will Strinz.
The `Rope/Mobius*.lean` files and `Rope/AlgebraicRamsey.lean` (rope AV1) are the development's
proof files, copied unchanged apart from doc comments (references to unpublished notes replaced by
references to the note).

- `FIDELITY.md` is the assembling agent's self-assessment; it has had no non-builder review of its
  own. The same four statements, ported to Lean v4.35, are the published package
  mobius-ramsey v1.0.0, whose fidelity table had a non-builder AI review and whose README was
  reproduced by a fresh AI agent.
- A fresh AI agent (Claude Sonnet 5.5) reproduced this rope from this README and the release's
  `REPRODUCE.md` alone (exit 0, all 12 as expected); the friction it reported (linter warnings,
  times, memory, the Landlock check on WSL2) is fixed above. Because this rope's fidelity note is
  only self-assessed, the rope stays Comparator-checked, not Lean-checked.
- The author read the hand proof of Theorem C: an owner's read by a non-expert, not expert review.
- **No human expert has reviewed any of it.**

## Not checked

- The identification `Möb(S^{d-1}) ≅ PO(1,d)` (classical; cited).
- The circle consequence "Ramsey-ness depends only on cross-ratios" (not stated as a theorem).
- OpenAI's proof is trusted only as far as the kernel and Comparator check it.
- Faithfulness of OpenAI's `Ramsey` to the literature's definition: see `FIDELITY.md` and rope AV1.
- The Mathlib-cache oleans are trusted, as Comparator's README allows.
