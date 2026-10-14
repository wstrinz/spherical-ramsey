#!/usr/bin/env bash
# Re-run the exact certificate scripts and compare their output with expected/<name>.log.
#
#   bash check.sh            the fast set (each script under ~2 min; about 12 min in total)
#   bash check.sh --all      fast + slow (the slow set alone takes about 3.5 hours, sequentially)
#   bash check.sh --slow     the slow set only
#   bash check.sh NAME...    only the named entries (names as in the tables below)
#
# Needs Python >= 3.10 with sympy (1.14.0 was used for expected/), numpy and mpmath.  The interpreter
# is $PYTHON if set, else python3.  Every script runs as `$PYTHON -I -B script.py ARGS` (isolated mode,
# no bytecode files), from this directory, with stdout and stderr captured together.
#
# Normalization (applied to both the fresh output and expected/<name>.log before diffing):
#   - carriage returns are deleted (Windows);
#   - elapsed-time stamps are deleted: " (123s)" and " [12.3s]";
#   - "(sympy X.Y.Z; 123s)" becomes "(sympy)".
# Nothing else is filtered: every other byte must match.
#
# Exit status: 0 if every selected entry prints PASS, 1 otherwise.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
PY="${PYTHON:-python3}"

# name|script|args...   (args are separated by '|'; expected output is expected/<name>.log)
FAST=(
  "cert_mobius|cert_mobius.py"
  "radian_det|radian_det.py"
  "cert_s2_quat|cert_s2_quat.py"
  "cert_clifford_obs|cert_clifford_obs.py"
  "cert_clifford_seed|cert_clifford_seed.py"
  "cert_clifford_lorentz|cert_clifford_lorentz.py"
  "g4_test|g4_test.py"
  "dual_cert|dual_cert.py"
  "scalar_exact|scalar_exact.py"
  "cert_nontwogroup|cert_nontwogroup.py"
  "exact_circle_cert.quick|exact_circle_cert.py|[Ramsey|[non-Ramsey, det]|not two-group"
  "rankN_check|rankN_check.py"
  "rankN_sweep|rankN_sweep.py"
  "definable_bigball|definable_bigball.py"
  "definable_crosscheck|definable_crosscheck.py"
)
SLOW=(
  "cert_clifford_crosscheck|cert_clifford_crosscheck.py"
  "cert_s2|cert_s2.py"
  "definable_polyphase|definable_polyphase.py"
  "exact_circle_cert.controls|exact_circle_cert.py|control"
  "exact_circle_cert.NEW|exact_circle_cert.py|NEW: 3 rat|NEW: 4 rat|radian 7-gon"
  "cert_nontwogroup.slow|cert_nontwogroup.py|--slow"
  "cert_clifford|cert_clifford.py"
)

normalize() {
  tr -d '\r' | sed -E \
    -e 's/ *\([0-9]+s\)//g' \
    -e 's/ *\[[0-9]+(\.[0-9]+)?s\]//g' \
    -e 's/\(sympy [^;)]*; *[0-9]+s\)/(sympy)/g'
}

sel=()
case "${1:-}" in
  "") sel=("${FAST[@]}") ;;
  --all) sel=("${FAST[@]}" "${SLOW[@]}") ;;
  --slow) sel=("${SLOW[@]}") ;;
  -h|--help) sed -n '2,19p' "${BASH_SOURCE[0]}"; exit 0 ;;
  *)
    for want in "$@"; do
      hit=0
      for e in "${FAST[@]}" "${SLOW[@]}"; do
        if [ "${e%%|*}" = "$want" ]; then sel+=("$e"); hit=1; fi
      done
      if [ "$hit" -eq 0 ]; then echo "unknown entry: $want" >&2; exit 2; fi
    done ;;
esac

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
status=0
echo "python: $("$PY" -c 'import sys, sympy, numpy, mpmath; print(sys.version.split()[0], "sympy", sympy.__version__, "numpy", numpy.__version__, "mpmath", mpmath.__version__)')"
for e in "${sel[@]}"; do
  IFS='|' read -r -a parts <<< "$e"
  name="${parts[0]}"; script="${parts[1]}"; args=("${parts[@]:2}")
  exp="expected/$name.log"; got="$tmp/$name.log"
  t0=$SECONDS
  rc=0
  "$PY" -I -B "$script" ${args[@]+"${args[@]}"} > "$got" 2>&1 || rc=$?
  dt=$((SECONDS - t0))
  if [ ! -f "$exp" ]; then
    printf 'FAIL  %-28s %5ss  (no %s)\n' "$name" "$dt" "$exp"; status=1; continue
  fi
  if diff <(normalize < "$exp") <(normalize < "$got") > "$tmp/$name.diff"; then
    if [ "$rc" -eq 0 ]; then
      printf 'PASS  %-28s %5ss\n' "$name" "$dt"
    else
      printf 'FAIL  %-28s %5ss  (output matches but exit status %s)\n' "$name" "$dt" "$rc"; status=1
    fi
  else
    printf 'FAIL  %-28s %5ss  (exit status %s; first lines of the diff, expected < > got:)\n' "$name" "$dt" "$rc"
    head -n 20 "$tmp/$name.diff"
    status=1
  fi
done
if [ "$status" -eq 0 ]; then echo "check: all PASS"; else echo "check: FAIL"; fi
exit "$status"
