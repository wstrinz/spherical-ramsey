# Changelog

## v1.1.1 (2026-10-15)

A correction release. Every review named here was done by an AI agent that did not write what it
reviewed; no human expert has reviewed any of it.

- **Written proofs of first-order rigidity and the finite-type reformulation.** v1.1.0 labelled SR-C34
  and SR-C33(a)–(c) as proved `[HAND]` in the note, the ledger, the README and the archive metadata, but
  the note printed only a summary of the argument; the complete proof existed only in the reviewer's
  report. The note now has a section "First-order rigidity" with the full proofs: the local ring of
  F ⊗ F at the diagonal (Noetherian, the Taylor isomorphism modulo 𝔪³, a discrete valuation ring for one
  parameter), the obstruction bᵢ = −½ Σⱼ (aᵢⱼ ⊗ 1 − 1 ⊗ aᵢⱼ)², the finite-type reformulation with a
  deciding jet order (SR-C33(a), by the Krull intersection theorem, not effective), a Smith form over the
  local ring, the duality between the 2-jet system and its dual space Δ(A), first-order rigidity
  (SR-C34, by Nakayama's lemma), and the corank-one membership criterion (SR-C33(b), (c)). Status:
  `[HAND]`: written proof in §First-order rigidity (added in v1.1.1), independently reviewed twice by
  non-author AI agents (the first review reconstructed the argument; a second, independent review found
  every step sound).
  - Verdict of the independent second review of the written proofs: every step sound; `[HAND]` kept
    for SR-C34, SR-C33(a), SR-C33(b),(c) and SR-C31(a). Its two small fixes are applied: in the
    corank-one proposition the condition for I = 0 is β_J = 0 *in O* (B → O need not be injective
    when B is not a domain), and the local-ring lemma now states that B/𝔪ⁿ ≅ O/𝔪ⁿO carries 𝔪ʳ/𝔪ⁿ onto
    𝔪ʳO/𝔪ⁿO. Its exact search for counterexamples (about fifteen families of configurations) found no
    non-Ramsey set with Δ(A) = 0.
  - Ledger: the "only if" directions of SR-C31(a), SR-C33(a) and SR-C33(b) now say that they need a
    set that affinely spans (the "if" directions need no span); SR-C33's setting calls O a Noetherian
    local ring (it is regular, but that is not used). Each of SR-C31, SR-C33 and SR-C34 has a one-line
    status; SR-C33 stays open only because (d) is open, and SR-C31 stays consistent-on-sample because
    of (b).
  - By-products, proved there: the "symmetric part" conditions of the 2-jet dual are automatic, so the
    dual form of the 2-jet test holds at every quadric rank (SR-C31(a)); at quadric corank one the 2-jet
    test fails exactly when a Lemma A.1 derivation exists; the rank criterion SR-C24 holds without its
    regularity hypothesis and without 5 ≤ n.
  - Not proved, and stated so: the one-parameter (d+1)² threshold law and "not two-group" for the S²
    sample (consistent on sample only); first-order rigidity is not a characterization, and it is silent
    when κ ≥ 1 and a derivation acts on the points as one matrix (for example transcendental rotations of
    rational sets).
- **Theorem C's Lean scope.** README, `CITATION.cff`, `.zenodo.json` and the note's summary table said
  `[LEAN]` for Möbius invariance of finite spherical sets. The Lean covers the unit sphere and the maps
  φ_L; other spheres follow by a similarity, by hand. Now stated so (the note's Theorem C status line
  already said it).
- **Credit in two README rows.** The circle phase diagram (its non-Ramsey half is Pálvölgyi's Theorems
  A.3 and A.7) and the minimal non-Ramsey cells (the ten-point S² cell is the case d = 3 of Pálvölgyi's
  Theorem A.12) now carry the credit the note gives them.
- **Novelty sweep for SR-C34.** Done on 2026-10-15 (novel as far as found; already stated in v1.1.0's
  ledger and changelog); the stale "posting-day literature sweep" next steps in `FRONTIER.md` and
  `ledger/BACKLOG.md` are marked done.
- Versions: `CITATION.cff` and `.zenodo.json` 1.1.1; the note is version 1.1.1. No script, certificate,
  probe or rope changed.

## v1.1.0 (2026-10-15)

Corrections first, then additions. Every review named here was done by an AI agent that did not write
what it reviewed; no human expert has reviewed any of it.

### Corrections and credit

- **OpenAI's quadric-independence criterion was overlooked.** Result 172, Proposition 7.3 (Lean
  `spherical_quadraticIndependent_ramsey_all`, Comparator challenge `EuclideanRamseyQuadratic`; vendored
  unmodified in every rope here) says that a spherical set is Ramsey if the vectors vec(pᵢpᵢᵀ) are linearly
  independent over its coordinate field. v1.0.0 cited only its circle case (Cor. 7.4). Its corollaries
  (with a genericity step, reviewed once) are now credited as prior work: up to (d+1)(d+2)/2 − 1 generic
  points of S^{d−1} are Ramsey (new entry SR-C29).
  - Note: credit paragraph, new Remark (quadric independence), abstract and introduction; the
    non-two-group theorem (NTG) is now stated as a result about the circle, where the criterion reaches
    at most five points. Non-two-group Ramsey sets off the circle (for example seven generic points of
    S²) follow from OpenAI's criterion.
  - Ledger SR-C16: (a) is proved, as a corollary of Proposition 7.3. **Withdrawn:** the v1.0.0 sentence
    that an exact certificate for seven generic points on S² "would be the first certified Ramsey set
    beyond the two-group mechanism on a sphere of dimension ≥ 2". It was wrong: OpenAI's criterion
    already gives one.
  - Ledger SR-C7 (specialization closure): refuted for every d ≥ 3 (seven generic points of S^{d−1} are
    Ramsey and specialize to seven independent points on a great circle, which are not; Pálvölgyi's A.13
    gives another counterexample). Its circle form is open, as a successor question (`FRONTIER.md` F13).
  - Ledger SR-C3 (generic thresholds): proved, mostly by prior work (Theorem B(a) and the circle phase
    diagram on the circle; OpenAI's Prop. 7.3 and Pálvölgyi's A.12 for d ≥ 3). Bookkeeping, not a new
    result.
  - Ledger SR-C17: the passing side is proved (SR-C2 for j ≤ 3, OpenAI's Prop. 7.3 below the threshold).
- **Pálvölgyi's appendix Theorems A.11, A.12 and A.13 (arXiv:2609.23327; labelled unchecked by its
  author) were not cited.** A.11: no nonzero fixed weighted derivation-energy identity on at most 2d + 2
  points. A.12: for d ≥ 3, (d+1)(d+2)/2 points of S^{d−1} with algebraically independent stereographic
  parameters are not Ramsey; this is the non-Ramsey half of SR-C3 and contains the note's ten-point S²
  cell (Theorem NR-S23), which is now credited. A.13: explicit non-Ramsey sets of 2d + 3 points in every
  affine dimension d ≥ 2. Credited in the note and in SR-C3, SR-C17, SR-C30.
- **SR-C11 / SR-C12 re-scoped.** The `[PROBE]` "evidence against" a 2-jet failure without a scalar
  certificate was automatic: every tested cell has quadric corank one or contains a failing corank-one
  cell, and at corank one the 2-jet test equals the scalar test (SR-C31(a)). Re-scoped in the note (the
  section on the second-order test) and the ledger. SR-C11 is
  now answered (SR-C32).
- **Searches.** The note's red `\TODO` in the credit section (visible in the v1.0.0 PDF) is replaced by the
  coverage of the two sweeps of 2026-10-13 and 2026-10-14, with their limits; the special case of the
  rigid-group theorem that follows from Pálvölgyi's A.3 is stated. The stale "posting-day sweep still
  required" remark under Theorem C2 is removed.
- **Name collision.** Pálvölgyi's "two-orbit problem" (arXiv:2608.10865, appendix) is added to the
  caveat on "two groups".
- **References.** Elstrodt–Grunewald–Mennicke (Math. Z. 196, 1987, doi:10.1007/BF01200359) and Waterman
  (Adv. Math. 101, 1993, doi:10.1006/aima.1993.1043) are cited with Vahlen and Ahlfors.
- **Stale status lines.** Theorem C is registered on the Palomar registry as PALOMAR-2026-10-14-000008
  (version 1, 2026-10-14) (note, `ledger/README.md`). SR-C9: the e^{ie} literature re-check was done on
  2026-10-14. SR-C13: the "pre-posting gate" line is replaced by the review record (the glue was reviewed
  on 2026-10-13). `ledger/BACKLOG.md`: the `scalar_exact.py` fold-in row is marked done (it was in
  v1.0.0). The note's header comment no longer mentions `\TODO` markers.
- **Tailings.** "Matrix weights are strictly stronger than scalar ones": still withdrawn for its original
  witness; true for certificates (SR-C32), not known for colourings (SR-C35).

### Additions

- **First-order rigidity** (SR-C34, `[HAND]`, reviewed by one non-author AI agent): if the 2-jet dual
  space vanishes, the set is Ramsey. It contains OpenAI's quadric-independence criterion and the rank
  criterion SR-C24 (without its regularity hypothesis). Novel as far as found (literature sweep of
  2026-10-15); its algebraic-coordinate and small-point-count cases are prior (OpenAI Prop. 7.3; JD-Jones-ASES). Summarized in the note's "Changes in version 1.1".
- **Failures without a scalar certificate** (SR-C32, proved for four seeded families on S², reviewed by
  one non-author AI agent): 2-jet failures with no scalar Lemma A.1 certificate, even over ℂ.
- New ledger entries SR-C29 (OpenAI's criterion, corollaries), SR-C30 (phase diagram, failing side, every
  d), SR-C31 (corank law; (a) proved), SR-C33 (finite-type reformulation; (a)–(c) proved), SR-C35
  (matrix-weighted Lemma A.1, a sketch). 35 entries in all.
- `FRONTIER.md`: the ranked open frontier, with entry points by audience.
- Scripts (they need python-flint 0.9.0 in addition to sympy): `certificates/corank_exact.py` (c29–c32),
  `certificates/c31_respecialize.py`, `certificates/c34_det16.py` (fast set of `certificates/check.sh`;
  CI installs python-flint), and the probes `probes/c31_c32_jet2.py`, `probes/c34_test.py`
  (`probes/run_all.sh`, `probes/check.sh`), each with an expected log.
- Versions: `CITATION.cff` and `.zenodo.json` 1.1.0; the note is version 1.1.0.

## v1.0.0 (2026-10-14)

First release (doi:10.5281/zenodo.23366344).
