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
| SR-C3 / SR-C4 → SR-C17 phase diagram | passing side j ≥ 4 below N(d) (first case SR-C16); S³ cells with j ≥ 6 at m + j = 14, 15; an exact S⁴ (17,4) cell (drop one more identically dependent row) | `cd probes && python e1_s2.py`; `python e3_sphere.py threshold 3,4,5`; `python -I certificates/scalar_exact.py` | A | 1–2 |
| SR-C5 measurable Graham | a Euclidean density theorem for one affinely dependent non-product spherical set (for example an isosceles trapezoid) | note, Conjecture M1 and the remarks after it; stub `C5_measurable_graham` | M | n/a |
| SR-C6 rigidity, n ≥ 9 | rational families via SR-C23(ii); families without a rigid five-point group | `cd probes && python c14_rigid.py`; `python c23_count_law.py` | A | 1 |
| SR-C7 specialization closure | off the circle: certify SR-C16(a); on the circle: degenerations of two-group families with the exact k = 1 procedure | `cd probes && python c15_c16.py`; `python -I certificates/exact_circle_cert.py control` | A | 1 |
| SR-C8 / SR-C18 pseudo-Euclidean and hyperbolic | decide the horocyclic triple; write out the Rado step of the linear-necessity sketch; literature sweep | `LEDGER.md` SR-C18 (all arguments inline) | M (test case), A (write-ups) | 1 |
| SR-C9 transcendence-hard instances | final literature check of the status of e^{ie}; with SR-C19, state "explicit instances are as hard as their relation ideal" | `python -I certificates/radian_det.py` | A | 0.5 |
| SR-C10 radian 8-gon (proved, HAND) | optional upgrade to CERT: an explicit certificate (the direct search was stopped after 40 min; try kernel interpolation or z = e^{iθ} coordinates) | `python -I certificates/exact_circle_cert.py "radian 8"` (long); `python -I certificates/rankN_check.py` | A | 0.5 |
| SR-C11 / SR-C12 scalar sufficiency | bilinear (λ, c) search on failing configurations with shared parameters (three Möbius groups; 6 + 6 + 6 on S³) | `cd probes && python scalar_cert.py`; `python -I certificates/scalar_exact.py` | A | 1 |
| SR-C14 rigid absorption (proved, HAND) | extension to algebraic seeds (idempotent transport) | `cd probes && python c14_rigid.py` (about 30 s) | A | 0.5 |
| SR-C15 three generic groups | exact Fredholm duals for (4,4,1) and (4,4,4) | `cd probes && python c15_c16.py`; `certificates/dual_cert.py` | A | 1 |
| SR-C16 specialization fails on S² | an exact Ramsey certificate for 7 generic points (or 3 rational + 4 free) on S² | `cd probes && python c15_c16.py` | A | 2 |
| SR-C19 decidability | a general-k implementation (Singular or Macaulay2 syzygies over ℚ[T, U]) | `python -I certificates/exact_circle_cert.py control` (5/5 exact controls) | A | 2 |
| SR-C20 effective Ramsey dimension | write out part 1 (existential theory of the reals) | `LEDGER.md` SR-C20 | M | n/a |
| SR-C21 colour number | bookkeeping of the colour counts of the Lemma A.1 route for the circle heptagons, the radian 9-gon and the S²/S³ cells | note, Lemma A.1 and Theorem NR-S23 | A (upper), M (lower) | 1 |
| SR-C23 expected-dimension law | k = 1: "nine non-two-group points ⇒ nonzero determinant" and "rational families have full-rank N"; k ≥ 2 needs SR-C1 | `cd probes && python c23_count_law.py`; `python -I certificates/cert_nontwogroup.py` | A (k = 1), M | 2 |
| SR-C24 rank criterion (proved, HAND) | drop the regularity hypothesis (reviewer's inference); a k = 2 analogue that explains the mirror family; one-parameter families on S² | `python -I certificates/rankN_check.py`; `python -I certificates/rankN_sweep.py` | A | 1 |
| SR-C27 polynomial phases in ℝ³ | an exact avoidance attempt for an instance where the search fails (none so far) | `python -I certificates/definable_polyphase.py`; `definable_crosscheck.py` | A | 0.5 |
| SR-C28 locally semialgebraic Graham | SAT over ℤ^D-periodic grid colourings at small (D, N, r), constrained by exactly certified robust copies | `LEDGER.md` SR-C28 | M | n/a |

Closed: SR-C13 (refuted, CERT) and SR-C22 (refuted, PROBE; superseded by SR-C23). Both are kept.
SR-C25 and SR-C26 are proved and need no next step; an effective bound in SR-C26 needs new mathematics.

## Other open threads

| Thread | Starting state | Diff. |
|---|---|---|
| Non-builder fidelity reviews of ropes AV2 and AV4 (both already reproduced by a fresh agent; AV4's published v4.35 port passed both checks). AV1, AV3 and AV5 are Lean-checked | `ropes/av2`, `ropes/av4` READMEs and `FIDELITY.md` | E |
| Done 2026-10-13: a separate (non-builder AI) review of the circle glue for the non-two-group certificates (SR-C13), with independent sympy/python-flint re-checks; sound, wording fixes applied | note, Theorem NTG; `certificates/cert_nontwogroup.py` | E |
| The radian 9-gon at θ = 1 radian in Lean: needs Lindemann–Weierstrass in Mathlib | rope AV3 | E (upstream) |
| `scalar_exact.py`: fold in the check that every point with a non-identically-zero weight has a nonzero weight at the specialization | `certificates/scalar_exact.py` | E |
| Closed Poncelet polygons (chains are refuted; closure needs an elliptic-curve torsion parametrization) | `probes/e6_wild.py` | A |
