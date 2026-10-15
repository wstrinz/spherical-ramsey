# Public conjecture ledger

This directory holds the open problems, partial results and refuted guesses that accompany the note
*Two Möbius groups suffice* (`note/` in this release). It is meant to be a landing surface: every open
thread is left in a state that someone else can pick up and replay.

| File | Contents |
|---|---|
| `LEDGER.md` | One entry per problem (35), with a YAML header and prose fields; refuted entries are kept |
| `ledger.yaml` | The YAML headers of `LEDGER.md`, collected; generated, not edited by hand |
| `BACKLOG.md` | The next step and starting state for every open or consistent-on-sample entry, plus open threads that are not conjectures |
| `lean/SphericalRamseyConjectures.lean` | Statement-only Lean 4 stubs for six entries (SR-C2, SR-C5, SR-C10, SR-C13, SR-C14, SR-C16) |
| `../FRONTIER.md` | The ranked open frontier (since v1.1.0): entry points by audience and a first step for each problem |
| `../CHANGELOG.md` | Every correction and addition since v1.0.0 |

## Ids

Entries are `SR-C1` to `SR-C35` (SR-C29 to SR-C35 added in v1.1.0). Ids are stable and never reused, including for refuted or merged
entries. The note cites entries by these ids.

## Entry format

Each entry is a Markdown section with a YAML header:

| Field | Meaning |
|---|---|
| `id`, `title` | Stable id and a short title |
| `status` | `open` · `consistent-on-sample` · `refuted` · `proved` (see below) |
| `warrant` | The strongest artifact behind the status, with its tag; reviews are named as AI reviews |
| `scope` | Type of the coordinates over ℚ (`ALGEBRAIC`, `GENERIC_OF(…)`, `TRANSCENDENTAL_PARAM(…)`, `MOBIUS_ORBIT_OF(…)`, `ANY`, `REGULAR(F/Q)`); "real" is never a scope |
| `difficulty` | Attackable with the tooling of this release, engineering, or needs new mathematics |
| `lean_stub` | `lean/SphericalRamseyConjectures.lean#<name>`, or `none` |
| `fc_category` | The google-deepmind/formal-conjectures category the entry would carry |
| `ams` | MSC 2020 codes |
| `replay` | Scripts of this release (`certificates/…`, `probes/…`) that reproduce the evidence |
| `note` | Where the note states or discusses it, if it does |
| `history` | Dated status changes |
| `amended`, `merged_into` | Present when an entry was amended or merged |

The prose fields follow in this order: statement (quantifiers explicit, field-type scope, OpenAI's
"Ramsey"); status and evidence (modulo-p evidence labelled `[PROBE]`); falsifier (concrete, and cheaper
than a research campaign); starting state (commands); difficulty; Lean; links.

## Status vocabulary

| Status | Meaning | formal-conjectures |
|---|---|---|
| open | no evidence either way, or heuristic only | `research open` |
| consistent-on-sample | survives a stated, replayable falsifier run | `research open` |
| refuted | a stated counterexample, at the stated warrant (`[PROBE]` refutations say so) | `research solved` with the negation, once the warrant is `[CERT]` or better and public |
| proved | a written proof (`[HAND]`) or certificate (`[CERT]`); not machine-checked unless it says `[LEAN]` | `research solved` only once a proof is public and accepted |

## Warrant rules

- No entry states a claim above its recorded warrant.
- `[PROBE]` (random specialization modulo a stated prime near 2³¹) is evidence, never a verdict.
- `[SKETCH]` is an outline; it is not upgraded until a non-author review passes.
- Every review named in the ledger was carried out by an AI agent that did not write what it reviewed.
  **No human expert has reviewed any entry.**
- Statements proved in Lean are not ledger entries; they are the ropes of this release
  (`ropes/av1`–`ropes/av5`) and the published Möbius-invariance package (mobius-ramsey v1.0.0,
  doi:10.5281/zenodo.23339523; registered on the Palomar registry as PALOMAR-2026-10-14-000008 v1).

## Replaying

- Python 3.10 with numpy 1.26, sympy 1.14 and mpmath 1.3; python-flint 0.9 for the scripts of SR-C29 to
  SR-C34.
- Exact scripts: `python -I certificates/<script>`; compare with `certificates/expected/`.
- Modulo-p probes import their siblings: `cd probes && python <script>`; compare with
  `probes/expected-v2/`, ignoring timing lines. The `validate.py` controls must pass before any probe
  output is cited. Probes are seeded; a "no verdict" outcome is never counted as a pass, a fail or an
  agreement.
- Lean stubs: from any Lake project pinned to Lean v4.34.1 and Mathlib `d13f23b7` (for example a rope
  directory of this release after its setup), `lake env lean <path>/lean/SphericalRamseyConjectures.lean`.
  Expected output: six `declaration uses 'sorry'` warnings and nothing else (Mathlib import: several
  minutes).
- `ledger.yaml` is regenerated from `LEDGER.md` by collecting its YAML blocks in order.

## Credit

Human author: Will Strinz. The entries were found, tested and written by Claude agents (Anthropic;
Claude Opus 5.5 and Claude Sonnet 5.5) directed by the author; see `DISCLOSURE.md` of this release.
Upstream: OpenAI's classification of finite Euclidean Ramsey configurations (openai/math `fd4aeeb2`,
result #172), including its quadric-independence criterion (Prop. 7.3), and Pálvölgyi, *A cyclic
non-Ramsey heptagon*, arXiv:2609.23327, including its appendix (labelled unchecked by its author).
