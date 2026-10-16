# spherical-ramsey

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23366343.svg)](https://doi.org/10.5281/zenodo.23366343)

Archived on Zenodo. Cite all versions with the concept DOI [10.5281/zenodo.23366343](https://doi.org/10.5281/zenodo.23366343); v1.1.0 is [10.5281/zenodo.23396387](https://doi.org/10.5281/zenodo.23396387) and v1.0.0 is [10.5281/zenodo.23366344](https://doi.org/10.5281/zenodo.23366344).

**Version 1.1.1** adds the written proofs of first-order rigidity (SR-C34) and of the finite-type
reformulation (SR-C33(a)–(c)) to the note (section "First-order rigidity"). v1.1.0 labelled them proved
`[HAND]` while publishing only a summary of the argument; the written proofs were then reviewed
independently by a second non-author AI agent, which found every step sound. It also scopes Theorem C's `[LEAN]` level to the
unit sphere and credits Pálvölgyi in two rows below. See [`CHANGELOG.md`](CHANGELOG.md).

**Version 1.1.0** corrects the credit in v1.0.0. OpenAI's quadric-independence criterion (result 172,
Prop. 7.3) and Pálvölgyi's appendix Theorems A.11–A.13 had been overlooked. Several ledger statuses
change (SR-C3, SR-C7, SR-C11, SR-C16), and a v1.0.0 sentence calling a certificate for seven generic
points of S² "the first certified Ramsey set beyond the two-group mechanism" is withdrawn. The release
also adds ledger entries SR-C29 to SR-C35, including first-order rigidity (SR-C34), and a frontier
document, [`FRONTIER.md`](FRONTIER.md). Every change is listed in [`CHANGELOG.md`](CHANGELOG.md).

**Which finite sets of points on a sphere are Euclidean Ramsey?** Lean 4 proofs, exact
certificates, numerical probes, a note and a conjecture ledger, each result labelled with how it
was verified.

A finite set of points in Euclidean space is *Ramsey* if for every number of colours `r ≥ 2`
there is a dimension `D` such that every `r`-colouring of `ℝ^D` contains a monochromatic congruent
copy of the set. OpenAI's result 172 (openai/math, commit `fd4aeeb2`) classified the finite Ramsey
configurations by a tensor condition over their coordinate field, and proved it in Lean. Everything
here builds on that classification and **trusts OpenAI's Lean proof**; the deep work is theirs.

## Contents

| Path | What it is |
|---|---|
| [`note/`](note/) | The note: every claim below, with its proof or its certificate and glue, stated at its verification level |
| [`ropes/av1`](ropes/av1/) … [`ropes/av5`](ropes/av5/) | Five *ropes*: standalone Lean packages (Lean v4.34.1, Mathlib `d13f23b7`, OpenAI's pin), each checked by stock Comparator with one command |
| [`certificates/`](certificates/) | Exact certificate scripts (Python, sympy; exact arithmetic only) with their expected output |
| [`probes/`](probes/) | The 2-jet probe harness (arithmetic mod a prime). **[PROBE] evidence, not proof** |
| [`ledger/`](ledger/) | The public conjecture ledger: open, proved and refuted conjectures, each with a replay command |
| [`FRONTIER.md`](FRONTIER.md) | The ranked open frontier: entry points by audience and a first step for each problem |
| [`CHANGELOG.md`](CHANGELOG.md) | Corrections and additions since v1.0.0 |

## Verification levels

- **[LEAN]**: a Lean theorem, kernel-checked by stock
  [Comparator](https://github.com/leanprover/comparator) against a statement-only challenge file,
  with only the axioms `propext`, `Classical.choice` and `Quot.sound`, and with negative controls
  refused. **Comparator-checked on a fresh runner** means that the rope's one-command `REPRODUCE`
  passed on a fresh GitHub-hosted runner (ubuntu-24.04, cold caches); every rope here has.
  **Lean-checked** means that, in addition, a non-builder fidelity review and a fresh-agent
  reproduction have passed.
- **[CERT]**: an exact symbolic identity, determinant or certificate, checked by a script in
  `certificates/` (rational or polynomial arithmetic; floating point never concludes), plus a
  written argument (the *glue*, in the note) that turns it into the theorem.
- **[HAND]**: a written proof in the note. Reviewed by AI agents only (see `DISCLOSURE.md`).
- **[PROBE]**: random specialization modulo a prime. Evidence, never a theorem.

Each claim also states the type of its coordinates over ℚ: algebraic, generic (algebraically
independent parameters), a transcendental parameter, a Möbius orbit of a type, or any. "Real" is
never a scope: the verdict can flip between algebraic and transcendental members of one real
family.

## Results and their levels

The note is authoritative for wording; this table is a map.

| Claim | Level | Where |
|---|---|---|
| **Theorem A.** A finite spherical set with real algebraic coordinates is Ramsey. Prior work (JD-Jones-ASES, Rogerhu12, atimics); this is a further proof, with no affine-span hypothesis | [LEAN], Lean-checked (fresh-runner Comparator, non-builder fidelity review, fresh-agent reproduction) | `ropes/av1` |
| **B(a).** Any at most six distinct points on a circle are Ramsey. The criterion for six points was first proved in Lean by JD-Jones-ASES, with the Ramsey conclusion conditional on OpenAI's sufficiency; this rope makes it unconditional | [LEAN], Comparator-checked on a fresh runner; [CERT] `cert_mobius.py` | `ropes/av2` |
| With a 7-point non-Ramsey cyclic set (Pálvölgyi's heptagon; also the 3 + 4 set below), 7 is the minimum size of a non-Ramsey cyclic set. The minimality is not in Lean | [LEAN] (≤ 6 points, rope AV2) plus [CERT] (`dual_cert.py`) or Pálvölgyi's theorem for the 7-point set | `ropes/av2`; `certificates/` |
| **Theorem D.** The radian nine-gon `(cos kθ, sin kθ)`, `k = 0, …, 8`, is not Ramsey when `tan(θ/2)` is transcendental, and (distinct points) is Ramsey iff `e^{iθ}` is algebraic | [LEAN], Lean-checked (fresh-runner Comparator, non-builder fidelity review, fresh-agent reproduction); [CERT] `radian_det.py` | `ropes/av3` |
| θ = 1 radian: the nine points at angles 0, …, 8 are not Ramsey | [HAND]: Theorem D plus Lindemann–Weierstrass (not in Mathlib at this pin) | note |
| **Theorem C.** The Ramsey property of a finite spherical set is Möbius invariant (no spanning hypothesis), with corollaries: Möbius images of algebraic spherical sets, and the circle families `circ(k tᵢ)`, `circ(tᵢ + c)`, are Ramsey. **Published** in mobius-ramsey v1.0.0 ([doi:10.5281/zenodo.23339523](https://doi.org/10.5281/zenodo.23339523)) | [LEAN] for the unit sphere (Möbius maps φ_L), Comparator-checked on a fresh runner; other spheres by a similarity, by hand ([HAND]) | `ropes/av4` |
| **B(b).** Algebraic concyclic points plus at most three arbitrary points on the same circle are Ramsey | [LEAN], Lean-checked (fresh-runner Comparator, non-builder fidelity review, fresh-agent reproduction); [CERT] `cert_mobius.py` (rational case) | `ropes/av5` |
| **The two-group theorem (C2).** For every `d ≥ 2`, a union of two Möbius images of finite algebraic subsets of `S^{d-1}` is Ramsey (any sizes, both orientations) | every `d ≥ 2`: [HAND], AI-reviewed. Exact certificates plus glue: `S¹` and `S²` [CERT] (`cert_s2.py`, with `g4_test.py` for algebraic seeds); `S³`, `S⁴` [CERT] (`cert_s2_quat.py`); `S⁵` [CERT] (`cert_clifford*.py`); instance cross-checks through `d = 8` | note; `certificates/` |
| **OpenAI's quadric-independence criterion** (prior work; ledger SR-C29): up to (d+1)(d+2)/2 − 1 generic points of S^{d−1} are Ramsey; on S² this gives non-two-group Ramsey sets | [LEAN] (OpenAI's theorem) + [HAND] genericity step, AI-reviewed; exact ranks `corank_exact.py` | note; ledger |
| **Not only two groups on the circle.** Explicit 7- and 8-point Ramsey sets on a circle that are not unions of two Möbius images of algebraic sets, and the radian 7-gon (on the circle the quadric criterion reaches at most five points) | [CERT] plus glue, reviewed (AI) (`cert_nontwogroup.py`; non-two-group-ness by an exact cross-ratio check) | `certificates/` |
| An exact decision procedure for one-parameter cyclic sets; it reproduces the known exact verdicts | [CERT] per instance (`exact_circle_cert.py`) | `certificates/` |
| **The rank criterion** (ledger SR-C24): a one-parameter cyclic set with `5 ≤ n ≤ 8` is Ramsey if its `n × 8` 2-jet matrix has rank `n` | [HAND], AI-reviewed; exact ranks by `rankN_check.py`, `rankN_sweep.py` | note; ledger |
| **The radian 8-gon** (ledger SR-C10): the points `k = 0, …, 7` are Ramsey for every θ | [HAND] (the rank criterion plus an exact rank 8), AI-reviewed | note; ledger |
| **Rigid-group absorption** (ledger SR-C14) on the circle (regular coordinate fields) | [HAND], AI-reviewed; exact 9 × 9 determinants of instances in `probes/c14_rigid.py` | note; ledger |
| The 2-jet test is a necessary condition for Ramsey | [HAND], AI-reviewed | note |
| **First-order rigidity** (ledger SR-C34): if the dual space of the 2-jet system vanishes, the set is Ramsey; with the finite-type reformulation (SR-C33(a)–(c)) | [HAND]: written proof in the note since v1.1.1, reviewed twice (AI); see `DISCLOSURE.md` | note; ledger |
| 3 rational + 4 algebraically independent circle points are not Ramsey (an instance of Pálvölgyi's Theorem A.3) | [CERT] (`dual_cert.py`) | `certificates/` |
| The circle phase diagram: `m` rational + `j` independent points are non-Ramsey iff `j ≥ 4` and `m + j ≥ 7`. The non-Ramsey half is Pálvölgyi's (Theorems A.3 and A.7 of his appendix, labelled unchecked by its author); the Ramsey half combines prior work with B(b) | [HAND], AI-reviewed | note |
| The minimal 2-jet failure cells on `S²` and `S³` are non-Ramsey. The ten-point `S²` cell with all coordinates independent is the case d = 3 of Pálvölgyi's Theorem A.12 (appendix, labelled unchecked by its author), which is prior; ours there is the exact certificate | [CERT] identities (`scalar_exact.py`) plus glue, AI-reviewed | note; `certificates/` |
| Graham's conjecture holds trivially for colourings definable in an o-minimal structure (big-ball lemma); polynomial-factor colourings contain every bounded-dimension spherical set | [HAND], AI-reviewed; exact interval checks of examples (`definable_*.py`, `exact_intervals.py`) | note; `certificates/` |
| Phase diagrams, thresholds and searches on `S¹` … `S⁴` | [PROBE] only | `probes/` |

Open and refuted conjectures (with the evidence for and against each) are in `ledger/`, as entries
`SR-C1` … `SR-C35`. The scripts' own output and docstrings call these `C-1` … `C-35`; `C-n` there is
ledger entry `SR-Cn`. Since v1.1.0 the ledger also holds results reviewed by AI agents only, such as
first-order rigidity (SR-C34), whose written proof is in the note since v1.1.1 and was reviewed twice; `FRONTIER.md` ranks the
open problems.

## Reproduce

`REPRODUCE.md` has every command and its expected output. In short:

```sh
# a rope (Linux with Landlock; elan, Go >= 1.24, git, sha256sum; about 30 min on a fresh runner,
# about 25-45 min with a warm Mathlib cache; run one rope at a time)
export PATH="$HOME/.elan/bin:$HOME/go/bin:/usr/local/go/bin:$PATH"
cd ropes/av1 && bash REPRODUCE            # exit 0: "all 10 as expected"

# the exact certificates (Python 3.10, numpy 1.26.4, sympy 1.14.0, python-flint 0.9.0)
bash certificates/check.sh                # fast set; every line PASS
bash certificates/check.sh --all          # everything, including the slow scripts

# the probes ([PROBE] only)
bash probes/run_all.sh                    # fast suite into probes/out/, about 10-14 min
bash probes/check.sh                      # expected: "check: all logs match expected-v2"
```

`bash probes/run_all.sh --slow` adds the slow probes (about 20 min more); `bash probes/check.sh`
then checks those logs too.

CI: `.github/workflows/rope-av1.yml` … `rope-av5.yml` run each rope's `REPRODUCE` on a fresh
runner, and `certificates.yml` re-runs the fast certificate scripts and diffs them against
`certificates/expected/`.

## Limitations

- **OpenAI's proof is trusted**, as far as the kernel and Comparator check it. Its mathematics has
  not been reviewed here.
- **Review.** No human expert has reviewed this work. Every review reported here is an AI review,
  except the author's own read of the hand proof of Theorem C (`DISCLOSURE.md`).
- [CERT] results need their glue, which is [HAND]: the script checks the identity, the note's
  argument makes it a theorem.
- [PROBE] results are evidence only: the arithmetic is modulo a prime, and a 2-jet failure means
  non-Ramsey only through the hand-proved (AI-reviewed) necessity of the 2-jet test.
- The identification of the Lorentz-matrix maps with the Möbius group (Theorem C) is classical and
  cited, not formalized.

## Licence and citation

A mixed tree. MIT (`LICENSE`) for this project's files. Apache-2.0 (`LICENSES/Apache-2.0.txt`) for
OpenAI's Lean files vendored unmodified in each rope, and for the few files adapted from them.
`NOTICE` says which file is under which licence. Cite with `CITATION.cff`. Archive: Zenodo,
concept DOI 10.5281/zenodo.23366343 (v1.1.0: 10.5281/zenodo.23396387; v1.0.0: 10.5281/zenodo.23366344).

This repository cites mobius-ramsey v1.0.0 (Will Strinz, 2026; doi:10.5281/zenodo.23339523), the
published home of Theorem C; OpenAI's result 172; Pálvölgyi, *A cyclic non-Ramsey heptagon*
(arXiv:2609.23327, including its appendix); JD-Jones-ASES/six-concyclic-lean (`0703d7d`); Rogerhu12/openai-math-extensions
(`f8a2bb2`); atimics/math2 (`8ab51fa`); and Gibbons–Luo, *Colorings of the n-sphere and inversive
geometry* (arXiv:1307.5351).

## Authorship

Will Strinz is the sole human author. AI agents (Claude Opus 5.5 and Claude Sonnet 5.5, Anthropic)
produced the proofs, the Lean, the certificates, the probes, the checks and the documentation under
his direction. `DISCLOSURE.md` says who did what and which reviews were AI reviews.
