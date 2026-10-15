# Authorship, AI use and review

## Human author

**Will Strinz** is the sole human author and the person responsible for this repository. He
directed the work, made the decisions recorded here (scope, licence, what to release), read the
hand proof of Theorem C, and is accountable for the release. He is not an expert in Euclidean
Ramsey theory.

## AI contributions, by name

| Contributor | What it did |
|---|---|
| Claude Opus 5.5 (Anthropic), in claude.ai | The exploratory conversation in which most of the claims here, and the first versions of several certificate scripts, first appeared; the task description that started the project |
| **Claude Opus 5.5** (Anthropic), in Claude Code | Coordination of the work; the Lean proofs and the five rope packages (`ropes/`); the exact certificate scripts (`certificates/`) and the probe harness (`probes/`); the reviews listed below as AI reviews; the note, the ledger and this repository's documentation; the assembly of this package |
| **Claude Sonnet 5.5** (Anthropic), in Claude Code | The prior-work and novelty searches; the hygiene audit of the probe harness (the no-verdict counting fix); a fresh reproduction of rope AV1 from its README alone (reproduced); a fresh reproduction of this whole release (all five ropes, the certificates and the probes) from its README and REPRODUCE alone (reproduced); a literature scout on definable colourings |

Every machine check reported in this repository was run by these agents; the author did not
re-run them.

## Foundation

**OpenAI's result 172**, *A classification of finite Euclidean Ramsey configurations*, and its
complete Lean proof (github.com/openai/math, commit `fd4aeeb2`), is the foundation of this work.
Every rope builds on OpenAI's Lean proof, whose files are included unmodified in each rope
(Apache-2.0; see `NOTICE`), and trusts it.

## Review: who checked what

| Check | By | Kind |
|---|---|---|
| The ropes' Lean proofs: kernel checking, axioms, statement match against the challenge files, refusal of negative controls | stock Comparator (Lean kernel, in its Landlock sandbox), on the builder's machine and on a fresh GitHub runner for each rope | machine |
| The exact certificate scripts (`certificates/`) | the scripts themselves, re-run for this package against `certificates/expected/` | machine; the written glue that turns each identity into a theorem is reviewed as below |
| Fidelity of rope AV1's statements (`ropes/av1/FIDELITY.md`), by an agent that did not build it | Claude Opus 5.5 | AI review: faithful, fixes to the fidelity note only, all applied |
| Fresh reproduction of rope AV1 from its README alone | Claude Sonnet 5.5 | AI reproduction: reproduced; its friction notes are fixed in the README |
| Fidelity of ropes AV3 and AV5 (`FIDELITY.md` in each), by an agent that did not build them | Claude Opus 5.5, read-only | AI review: faithful, documentation fixes applied; fresh-agent reproduction done (next row): both are Lean-checked |
| Fresh reproduction of all five ropes, the certificates (fast and slow) and probes, from README/REPRODUCE alone | Claude Sonnet 5.5 | AI reproduction: reproduced, friction fixed in the docs |
| Fidelity of ropes AV2 and AV4 (`FIDELITY.md` in each) | the agents that assembled them | AI self-assessment only (for AV4, see the next row); both ropes reproduced (row above), so they stay Comparator-checked |
| Theorem C and its corollaries | for the published mobius-ramsey v1.0.0 (the same statements ported to Lean v4.35): a non-builder AI fidelity review and a fresh AI reproduction of that package; rope AV4 here (Lean v4.34.1) has only its assembling agent's self-assessment | AI review |
| The 2-jet necessary test (the basis of the `probes/` verdicts), cold | Claude Opus 5.5 | AI review: necessity proved by the reviewer, with text corrections |
| The written glue for the two-group theorem (circle, S², S³, S⁴), the circle phase diagram and the dual certificates | Claude Opus 5.5, adversarial | AI review: supported, with wording fixes |
| The two-group theorem for every dimension (Clifford/Vahlen route) | Claude Opus 5.5 | AI review: supported |
| The non-Ramsey cells on S² and S³ (glue) | Claude Opus 5.5 | AI review: supported, with fixes (applied in `certificates/scalar_exact.py` and the note) |
| The rank criterion (SR-C24), rigid-group absorption (SR-C14) and the radian 8-gon (SR-C10) | Claude Opus 5.5, cold | AI review: supported, with fixes |
| The definable-colouring results (big-ball lemma, polynomial-factor colourings) | Claude Opus 5.5 | AI review: supported, with wording fixes |
| The glue for the non-two-group Ramsey sets (Theorem NTG), with an independent re-check of its certificates (sympy, python-flint), and the check of the hypotheses of Pálvölgyi's Theorems A.3 and A.7 used in the circle phase diagram (exact Jacobian rank) | Claude Opus 5.5, non-builder | AI review: glue sound, wording fixes applied; every cell covered |
| This package: the statements of ropes AV3 and AV5 against the note, the certificate READMEs against the code, the note and ledger statuses, private residue | Claude Opus 5.5, non-builder, read-only | AI review: no blocking finding; fixes applied |
| v1.1.0: the corrections (the corollaries of OpenAI's quadric-independence criterion, SR-C29 with its genericity step, SR-C3, SR-C7, SR-C16, and the phase-diagram sketch SR-C30) | a Claude agent that did not write it | AI review: sound with fixes (a spanning fix, wording and credit), applied |
| v1.1.0: first-order rigidity (SR-C34), the 2-jet dual (SR-C31(a)) and the finite-type reformulation (SR-C33(a)–(c)) | a Claude agent that did not write it | AI review: proved, with the scope and wording now in the ledger |
| v1.1.0: failures without a scalar certificate (SR-C32), with independent exact checks | a Claude agent that did not write it | AI review: proved for the four seeded families; the reviewer derived the matrix-weighted Lemma A.1 (SR-C35, not itself reviewed) |
| Novelty of the new claims | Claude Sonnet 5.5 (arXiv, GitHub, MathOverflow, OpenAlex searches) | AI search; not a literature review by an expert |
| Hand proof of Theorem C, line by line | Will Strinz | owner's read: an author's sign-off by a non-expert, **not** expert review |
| The note and the ledger | Claude agents; the author reviewed both before release (not line by line) | AI review; owner's review, not expert review |

**Every review listed here is an AI review, except the author's own read. No human expert has
reviewed this work.** Probe results (`probes/`, `[PROBE]`) are evidence, not proof, and are never
stated as theorems.
