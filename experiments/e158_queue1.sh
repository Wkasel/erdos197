#!/bin/zsh
# e158 queue 1 (sequential, one solver at a time), 2026-08-28.
# Order: M=24 pump cells (scale-stability of the headline), schedule
# mixedtax curves 16/24/32, then the (16;6,0) value-MUS.
cd "$(dirname "$0")/.."
PY=.venv/bin/python

echo "== Q1: bal@12 standalone baseline (3-block, e127)"
$PY experiments/e127_seam_budget.py bal --M 12 --vmax 64 \
    --budget 1200 --tag e158_bal12_base \
    > data/e158_bal12_base.log 2>&1

echo "== Q2: C2@24 (none, 0)"
$PY experiments/e158_joint4.py bal --M 24 --vup none --vdn 0 \
    --budget 3600 --tag c2_M24_dn0 > data/e158_c2_M24_dn0.log 2>&1

echo "== Q3: headline C3@24 (65, 0)"
$PY experiments/e158_joint4.py bal --M 24 --vup 65 --vdn 0 \
    --budget 10800 --tag c3_M24_up65_dn0 \
    > data/e158_c3_M24_up65_dn0.log 2>&1

VUPS=0,1,2,3,4,6,8,12,16,24,32,48,64,96,128,192,256,384,512
echo "== Q4: sched(1100) mixedtax @16"
$PY experiments/e158c_sched_price.py --M 16 --sched 1100 --vdn 0 \
    --vups $VUPS --budget 900 > data/e158c_s1100_M16.log 2>&1

echo "== Q5: sched(1100) mixedtax @24"
$PY experiments/e158c_sched_price.py --M 24 --sched 1100 --vdn 0 \
    --vups $VUPS --budget 900 > data/e158c_s1100_M24.log 2>&1

echo "== Q6: sched(1100) mixedtax @32"
$PY experiments/e158c_sched_price.py --M 32 --sched 1100 --vdn 0 \
    --vups $VUPS --budget 1200 > data/e158c_s1100_M32.log 2>&1

echo "== Q7: value-MUS of (16; 6, 0)"
$PY experiments/e158b_joint_mus.py --M 16 --vup 6 --vdn 0 \
    --budget 300 --chunk 16 > data/e158b_mus_M16.log 2>&1

echo "== QUEUE1 COMPLETE"
