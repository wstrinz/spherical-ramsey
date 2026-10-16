# Backlog

Every `open` or `consistent-on-sample` entry of `LEDGER.md` appears here with a next step and a
replayable starting state. Paths are relative to the release root (`README.md` explains how to run
them). Difficulty: **A** attackable with this release's tooling, **M** needs new mathematics, **E**
engineering or review. Sizes are rough, in person-days of focused work.

## Ledger entries

| Entry | Next step | Starting state | Diff. | Size |
|---|---|---|---|---|
| SR-C1 second-order completeness | k = 1: prove that the limit condition at the diagonal reduces to the second-order one; sweep the second-order test against the exact k = 1 procedure on real one-parameter configurations | `cd probes && python e4_six.py`; `python realness.py`; `python -I certificates/exact_circle_cert.py control` | A (k = 1), M | 2 |
| SR-C2 two-group theorem (proved, HAND) | a Lean proof uniform in d over Mathlib's `CliffordAlgebra` (the even-n orientation step inside the family) | stub `C2_two_group`; `certificates/cert_clifford*.py` | E | 5+ |
| SR-C4 → SR-C17 phase diagram (SR-C3 is proved, mostly by prior work) | passing side: done (SR-C2; OpenAI's Prop. 7.3 via SR-C29); failing side: a written proof of SR-C30's step-2 rank lemma (`FRONTIER.md` F6); a check of Pálvölgyi's A.12 for the all-free cell | `python -I certificates/corank_exact.py c29`; `python -I certificates/corank_exact.py c30`; `python -I certificates/scalar_exact.py` | E | 1 |
| SR-C5 measurable Graham | a Euclidean density theorem for one affinely dependent non-product spherical set (for example an isosceles trapezoid) | note, Conjecture M1 and the remarks after it; stub `C5_measurable_graham` | M | n/a |
| SR-C6 rigidity, n ≥ 9 | rational families via SR-C23(ii); families without a rigid five-point group | `cd probes && python c14_rigid.py`; `python c23_count_law.py` | A | 1 |
| Successor to SR-C7 (refuted): specialization closure for cyclic configurations | open on the circle; no entry yet. Degenerations of two-group families with the exact k = 1 procedure (`FRONTIER.md` F13) | `python -I certificates/corank_exact.py c29`; `python -I certificates/exact_circle_cert.py control` | E, A | 1 |
| SR-C8 / SR-C18 pseudo-Euclidean and hyperbolic | decide the horocyclic triple; write out the Rado step of the linear-necessity sketch; literature sweep | `LEDGER.md` SR-C18 (all arguments inline) | M (test case), A (write-ups) | 1 |
| SR-C9 transcendence-hard instances | literature check of the status of e^{ie} (re-checked 2026-10-14: still open as far as we know; `FRONTIER.md` F12); with SR-C19, state "explicit instances are as hard as their relation ideal" | `python -I certificates/radian_det.py` | A | 0.5 |
| SR-C10 radian 8-gon (proved, HAND) | optional upgrade to CERT: an explicit certificate (the direct search was stopped after 40 min; try kernel interpolation or z = e^{iθ} coordinates) | `python -I certificates/exact_circle_cert.py "radian 8"` (long); `python -I certificates/rankN_check.py` | A | 0.5 |
| SR-C12 scalar sufficiency (SR-C11 is answered by SR-C32) | disjoint-parameter failures that contain no failing corank-one subset (the earlier evidence was automatic) | `cd probes && python scalar_cert.py`; `python -I certificates/scalar_exact.py` | A | 1 |
| SR-C14 rigid absorption (proved, HAND) | extension to algebraic seeds (idempotent transport) | `cd probes && python c14_rigid.py` (about 30 s) | A | 0.5 |
| SR-C15 three generic groups | exact Fredholm duals for (4,4,1) and (4,4,4) | `cd probes && python c15_c16.py`; `certificates/dual_cert.py` | A | 1 |
| SR-C16 (proved, a corollary of OpenAI's Prop. 7.3) | a Lean corollary: an explicit rank-7 rational instance plus a generic-rank lemma (`FRONTIER.md` F8) | `python -I certificates/corank_exact.py c29` | E | 1 |
| SR-C19 decidability | a general-k implementation (Singular or Macaulay2 syzygies over ℚ[T, U]) | `python -I certificates/exact_circle_cert.py control` (5/5 exact controls) | A | 2 |
| SR-C20 effective Ramsey dimension | write out part 1 (existential theory of the reals) | `LEDGER.md` SR-C20 | M | n/a |
| SR-C21 colour number | bookkeeping of the colour counts of the Lemma A.1 route for the circle heptagons, the radian 9-gon and the S²/S³ cells | note, Lemma A.1 and Theorem NR-S23 | A (upper), M (lower) | 1 |
| SR-C23 expected-dimension law | k = 1: "nine non-two-group points ⇒ nonzero determinant" and "rational families have full-rank N"; k ≥ 2 needs SR-C1 | `cd probes && python c23_count_law.py`; `python -I certificates/cert_nontwogroup.py` | A (k = 1), M | 2 |
| SR-C24 rank criterion (proved, HAND) | (done in v1.1.1: the regularity hypothesis is dropped, as a case of SR-C34); a k = 2 analogue that explains the mirror family; one-parameter families on S² | `python -I certificates/rankN_check.py`; `python -I certificates/rankN_sweep.py` | A | 1 |
| SR-C27 polynomial phases in ℝ³ | an exact avoidance attempt for an instance where the search fails (none so far) | `python -I certificates/definable_polyphase.py`; `definable_crosscheck.py` | A | 0.5 |
| SR-C29 quadric corank zero (proved) | a Lean corollary for seven generic points of S² (`FRONTIER.md` F8) | `python -I certificates/corank_exact.py c29` | E | 0.5 |
| SR-C30 phase diagram, failing side | a written proof of the step-2 rank lemma (stabilizer so(W^⊥)) (`FRONTIER.md` F6) | `python -I certificates/corank_exact.py c30` | E | 1 |
| SR-C31 corank law | (b): generic non-vanishing of the pairing; general position of geometric families (no Möbius-null derivation) (`FRONTIER.md` F1) | `python -I certificates/corank_exact.py c31`; `python -I certificates/c31_respecialize.py`; `cd probes && python c31_c32_jet2.py` | A | 2 |
| SR-C32 failures with no scalar certificate (proved for four families) | colour counts for the SR-C35 colouring (`FRONTIER.md` F3, F10) | `python -I certificates/corank_exact.py c32` | A | 1 |
| SR-C33 finite type | doubly degenerate corank-one families: exact π-adic orders of the minor ideal and the obstruction (`FRONTIER.md` F2) | `certificates/exact_circle_cert.py` machinery | A | 2 |
| SR-C34 first-order rigidity (proved, HAND; written proof in the note since v1.1.1, reviewed twice, AI) | (done 2026-10-15: literature sweep, novel as far as found); the (d+1)² threshold law as a theorem (generic-rank lemma); a Lean proof over OpenAI's `FieldCriterion` (`FRONTIER.md` F1, F8) | `cd probes && python c34_test.py`; `python -I certificates/c34_det16.py` | A, E | 2 |
| SR-C35 matrix-weighted Lemma A.1 | a review of the identity and the colouring step; colour counts (SR-C21) | `LEDGER.md` SR-C35 | E | 1 |
| SR-C28 locally semialgebraic Graham | SAT over ℤ^D-periodic grid colourings at small (D, N, r), constrained by exactly certified robust copies | `LEDGER.md` SR-C28 | M | n/a |

Closed: SR-C13 (refuted, CERT), SR-C22 (refuted, PROBE; superseded by SR-C23), SR-C7 (refuted for every
d ≥ 3; its circle form is the successor row above), SR-C3 (proved, mostly prior work) and SR-C11
(answered yes by SR-C32). All are kept. SR-C25 and SR-C26 are proved and need no next step; an effective bound in
SR-C26 needs new mathematics.

## Other open threads

| Thread | Starting state | Diff. |
|---|---|---|
| Non-builder fidelity reviews of ropes AV2 and AV4 (both already reproduced by a fresh agent; AV4's published v4.35 port passed both checks). AV1, AV3 and AV5 are Lean-checked | `ropes/av2`, `ropes/av4` READMEs and `FIDELITY.md` | E |
| Done 2026-10-13: a separate (non-builder AI) review of the circle glue for the non-two-group certificates (SR-C13), with independent sympy/python-flint re-checks; sound, wording fixes applied | note, Theorem NTG; `certificates/cert_nontwogroup.py` | E |
| The radian 9-gon at θ = 1 radian in Lean: needs Lindemann–Weierstrass in Mathlib | rope AV3 | E (upstream) |
| Done in v1.0.0: `scalar_exact.py` checks that every point with a non-identically-zero weight has a nonzero weight at the specialization | `certificates/scalar_exact.py` | E |
| Closed Poncelet polygons (chains are refuted; closure needs an elliptic-curve torsion parametrization) | `probes/e6_wild.py` | A |
