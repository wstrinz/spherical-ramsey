#!/usr/bin/env bash
# Regenerate the 2-jet probe logs. [PROBE] evidence, not proof: every verdict is mod-p.
# Fast suite ~14 min; --slow adds e1_s4 (~30 s), e4_six --real-scope (~6 min) and e7_hopf (~14 min).
# Needs Python >= 3.10 with numpy and sympy (and python-flint for c31_c32_jet2, c34_test). Logs go to $PROBE_OUT (default out/), LF line endings;
# compare them with expected-v2/ by running check.sh.
#   PYTHON=python bash run_all.sh                  # if your interpreter is not called python3
#   PROBE_OUT=expected-v2 bash run_all.sh --slow   # regenerate the reference logs
#   PROBE_PRIME=2147483629 bash run_all.sh         # another prime (logs will differ from expected-v2)
set -uo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
OUT="${PROBE_OUT:-out}"
mkdir -p "$OUT"
# runas LOGNAME SCRIPT [ARGS...]: python -I (isolated), -B (no __pycache__), CRs stripped
runas() {
  local name="$1"; shift
  echo "== $name"
  ( time ( "$PY" -I -B "$@" 2>&1 | tr -d '\r' ) ) > "$OUT/$name.log" 2>&1
  tail -n 3 "$OUT/$name.log"
}
run() { runas "${1%.py}" "$@"; }
run validate.py      # controls: 8 configurations with known verdicts, 2-jet and curve probe
run e1_phase.py      # circle phase diagram (m rational points + j independent points)
run e1_s2.py         # S^2 phase diagram
run e1_s3.py         # S^3 threshold
run e3b.py           # 'many algebraic + j free points' threshold, d = 2..9
run e5_mobius.py     # Mobius invariance / two- and three-group checks on S^1 and S^2
run e5b.py           # Palvolgyi heptagon under Mobius maps
run e6_wild.py       # radian progressions, Poncelet chains, random 3-parameter controls
run e4_six.py        # 6-point hunt + 2-jet vs full one-parameter criterion (C-1) on up to 9 points
run realness.py      # EXACT: which e4_six configurations are real (scope filter); no mod-p
run scalar_cert.py   # scalar single-derivation certificates on the S^1..S^4 cells (SR-C11 / SR-C12)
run c13_c22_seven.py # seven-point circle sets: two-group test (exact part A), radian n-gons, lattice 7-sets
run c22_controls.py  # low-parameter 7-sets mixed with rational points (controls for c13_c22_seven)
run c23_count_law.py # the expected-dimension count law on the circle (SR-C23)
run c14_rigid.py     # rigid-group absorption (SR-C14); exact 9x9 determinants at rational points
run c15_c16.py       # generic Mobius-group unions on S^1, seven points on S^2
run c31_c32_jet2.py  # corank law (SR-C31) and SR-C32 cells: primal jet2 cross-check (needs python-flint)
run c34_test.py      # first-order rigidity (SR-C34): exact dim Delta, curve probe and jet2, one parameter on S^2
if [ "${1:-}" = "--slow" ]; then
  run e1_s4.py                                 # S^4 threshold
  runas e4_six_real e4_six.py --real-scope     # e4_six counts restricted to real configurations
  run e7_hopf.py                               # Mobius-algebraic groups on S^2, S^3, S^4 (~14 min)
fi
