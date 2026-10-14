# Reproducing the checks

Three independent kinds of check, each runnable on its own: the Lean ropes (`ropes/`), the exact
certificates (`certificates/`) and the probes (`probes/`). Commands run from the repository root
unless they say otherwise.

## 1. The Lean ropes ([LEAN])

Each of `ropes/av1` … `ropes/av5` is a standalone Lake package pinned to Lean v4.34.1 and Mathlib
`d13f23b7` (OpenAI's pin for openai/math `fd4aeeb2`). Its `README.md` states the theorem verbatim,
and its `REPRODUCE` checks it with stock Comparator in one command.

**Requirements.**
- Linux with Landlock (Comparator's sandbox, landrun), run as a non-root user. `REPRODUCE` checks
  `/sys/kernel/security/lsm` for Landlock. On WSL2 with a recent kernel `/sys/kernel/security/lsm`
  may be absent; the check is then skipped and Comparator still runs.
- elan, Go ≥ 1.24, git and sha256sum on `PATH`. Non-login shells often miss `~/.elan/bin`:

  ```sh
  curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y --default-toolchain none   # if elan is missing
  export PATH="$HOME/.elan/bin:$HOME/go/bin:/usr/local/go/bin:$PATH"
  ```
- About 16 GB of RAM and several GB of disk per rope (Mathlib's prebuilt files). Network access
  for the toolchain, Lake's dependencies, the Mathlib cache and the Comparator sources. The
  Mathlib cache is shared between the ropes (and with other Lean projects on the same pin) in
  `~/.cache/mathlib`, so only the first rope downloads it.

**Run.**

```sh
cd ropes/av1 && bash REPRODUCE; echo "exit $?"
```

Expected, at the end: `all 10 as expected` and `exit 0` (rope AV4: `all 12 as expected`).
`AV1_UPSTREAM=1 bash REPRODUCE` (likewise `AV2_UPSTREAM`, …) also re-fetches openai/math at the
pinned commit and compares the vendored files with it byte for byte.

What `REPRODUCE` does: a preflight (tools present; every file matches `MANIFEST`; the challenge
definitions are OpenAI's verbatim), then it builds pinned Comparator, lean4export and landrun,
fetches the Mathlib cache, builds the rope, prints `#print axioms` for every checked theorem
(each must be `[propext, Classical.choice, Quot.sound]`), runs Comparator on every challenge (each
must print "Your solution is okay") and on every control (each must be refused with its expected
reason). The build prints `declaration uses 'sorry'` warnings for the statement-only challenge
files and the `sorry` control, and benign linter warnings (unused variables or simp arguments) in
the control files; they are expected.

**Times.** About 25–45 min per rope with a warm Mathlib cache, about 30 min on a fresh GitHub
runner; much longer only if other Lean builds are running at the same time (the build of OpenAI's
sources and each Comparator run, which exports and re-checks the whole tree, slow down sharply
under load). `REPRODUCE`'s progress line for the rope build gives that step alone as "20 min to
2.5 h, depending on machine load"; the upper end applies only under such contention.

**Tip.** Run one rope at a time, and no other lake/Comparator jobs concurrently; each needs several
GB of memory.

| Rope | Theorem | Comparator runs | Fresh-runner time | Warm-cache desktop |
|---|---|---|---|---|
| `av1` | Theorem A, `ramsey_of_algebraic` | 5 accepted, 5 refused | 27 min | 32 min |
| `av2` | B(a), `circle_ramsey_of_le_six` | 5 accepted, 5 refused | 30 min | 23 min |
| `av3` | Theorem D, `radian_configuration`, `radian_ramsey_iff` | 5 accepted, 5 refused | 27 min | 45 min |
| `av4` | Theorem C, `ramsey_iff_ramsey_mobius_full`, and corollaries | 7 accepted, 5 refused | 31 min | 27 min |
| `av5` | B(b), `ramsey_alg_plus_three` | 5 accepted, 5 refused | 27 min | 33 min |

The last column is the fresh-agent reproduction of this release (WSL Ubuntu, 8 cores, 15 GB,
warm Mathlib cache, one rope at a time).

**Preflight only** (any platform with bash and sha256sum, including Git Bash on Windows):

```sh
cd ropes/av1 && grep -v '^#' MANIFEST | sha256sum --quiet -c - && echo "MANIFEST OK"
```

CI: `.github/workflows/rope-av<n>.yml` runs `bash REPRODUCE` on a fresh runner.

## 2. The exact certificates ([CERT])

Python 3.10 with numpy 1.26.4 and sympy 1.14.0 (other versions very likely work; these are the
versions the expected output was produced with). mpmath comes with sympy. A virtual environment is
recommended:

```sh
python3 -m venv .venv && . .venv/bin/activate && pip install numpy==1.26.4 sympy==1.14.0
bash certificates/check.sh          # the fast set; one PASS line per script, exit 0
bash certificates/check.sh --all    # every script, including the slow ones
```

`check.sh` runs each script with `python3 -I`, compares its output with
`certificates/expected/<script>.log`, and exits non-zero on any difference. `certificates/README.md`
says, for each script, what it certifies, its tag, its runtime, and which written argument in the
note turns its identity into a theorem. CI: `.github/workflows/certificates.yml`.

## 3. The probes ([PROBE], evidence only)

```sh
bash probes/run_all.sh              # fast suite into probes/out/, about 10-14 min
bash probes/check.sh                # expected: "check: all logs match expected-v2"
bash probes/run_all.sh --slow       # fast suite plus the slow probes: about 20 min more
bash probes/check.sh                # now also checks the slow logs
```

`probes/README.md` describes the 2-jet harness, its hygiene (seeded specialization points,
`NO_VERDICT` never counted as a verdict, `PROBE_PRIME` to change the prime), the realness filter,
and how to compare `probes/out/` with `probes/expected-v2/`. Nothing in `probes/` is a proof.
