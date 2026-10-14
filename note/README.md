# Note

`spherical-ramsey.tex` is the note: *Two Möbius groups suffice: Euclidean Ramsey sets on spheres of every dimension, after the tensor
classification*, version 1.0.0 (2026-10-14).
It states every result of this repository with its verification level (`[LEAN]`, `[CERT]`,
`[HAND]`, `[PROBE]`), gives the hand proofs and the written glue for the certificates, and cites
the scripts in `../certificates/` and `../probes/`, the ropes in `../ropes/`, and the conjecture
ledger in `../ledger/` by path. Theorem C (Möbius invariance) is published separately in
mobius-ramsey v1.0.0 (doi:10.5281/zenodo.23339523) and is cited, not re-proved.

**Build.** Plain ASCII LaTeX (`amsart`, with `geometry`, `amsmath`, `amssymb`, `amsthm`, `mathrsfs`,
`mathtools`, `booktabs`, `xcolor`, `hyperref`). It needs a full TeX Live, or these packages (Ubuntu,
the set that CI installs):

```sh
sudo apt-get install -y --no-install-recommends latexmk texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-science
```

CI (`.github/workflows/note.yml`) builds it with `latexmk`, which runs pdflatex as often as the
cross-references need:

```sh
cd note
latexmk -pdf -interaction=nonstopmode -halt-on-error spherical-ramsey.tex
```
