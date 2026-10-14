#!/usr/bin/env bash
# Compare the logs in out/ (or $1, or $PROBE_OUT) with expected-v2/, ignoring timing:
# the `real/user/sys` lines of bash's `time` and the per-line "(Ns)" timings of e1_s4, e7_hopf and scalar_cert.
# Carriage returns are ignored too. Exit status 1 on any difference or on a missing fast-suite log;
# missing slow logs (e1_s4, e4_six_real, e7_hopf: run_all.sh --slow) are reported as skipped.
set -uo pipefail
cd "$(dirname "$0")"
OUT="${1:-${PROBE_OUT:-out}}"
FAST="validate e1_phase e1_s2 e1_s3 e3b e5_mobius e5b e6_wild e4_six realness scalar_cert c13_c22_seven c22_controls c23_count_law c14_rigid c15_c16"
SLOW="e1_s4 e4_six_real e7_hopf"
norm() { tr -d '\r' < "$1" | grep -v -E '^(real|user|sys)[[:space:]]' | sed -E 's/ *\([0-9]+s\)//g'; }
status=0
for name in $FAST $SLOW; do
  exp="expected-v2/$name.log"; got="$OUT/$name.log"
  if [ ! -f "$got" ]; then
    case " $SLOW " in
      *" $name "*) echo "SKIP     $name (slow; not in $OUT/)" ;;
      *) echo "MISSING  $name"; status=1 ;;
    esac
    continue
  fi
  if diff <(norm "$exp") <(norm "$got") > /dev/null; then
    echo "OK       $name"
  else
    echo "DIFFER   $name"; diff <(norm "$exp") <(norm "$got") | head -n 20; status=1
  fi
done
[ "$status" -eq 0 ] && echo "check: all logs match expected-v2" || echo "check: MISMATCH"
exit "$status"
