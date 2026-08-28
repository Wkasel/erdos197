#!/bin/zsh
# e158 queue 2 (sequential), 2026-08-28 afternoon.
cd "$(dirname "$0")/.."
PY=.venv/bin/python

echo "== Q8: v_min(0)(16) bisection — (96,0), (192,0), (384,0)"
for v in 96 192 384; do
  $PY experiments/e158_joint4.py bal --M 16 --vup $v --vdn 0 \
      --budget 3600 --tag f_M16_up${v}_dn0 \
      > data/e158_f_M16_up${v}_dn0.log 2>&1
done

echo "== Q9: sched(1100) any-budget certification (vup none)"
$PY experiments/e158c_sched_price.py --M 16 --sched 1100 --vdn 0 \
    --vups none --budget 1200 > data/e158c_s1100_M16_none.log 2>&1
$PY experiments/e158c_sched_price.py --M 24 --sched 1100 --vdn 0 \
    --vups none --budget 1200 > data/e158c_s1100_M24_none.log 2>&1
$PY experiments/e158c_sched_price.py --M 32 --sched 1100 --vdn 0 \
    --vups none --budget 1800 > data/e158c_s1100_M32_none.log 2>&1

echo "== Q10: attribution at 24 — (65, none)"
$PY experiments/e158_joint4.py bal --M 24 --vup 65 --vdn none \
    --budget 10800 --tag c1_M24_up65 > data/e158_c1_M24_up65.log 2>&1

echo "== Q11: third scale — (368, 6) @ 32 (both componentwise payable)"
$PY experiments/e158_joint4.py bal --M 32 --vup 368 --vdn 6 \
    --budget 10800 --tag c3_M32_up368_dn6 \
    > data/e158_c3_M32_up368_dn6.log 2>&1

echo "== QUEUE2 COMPLETE"
