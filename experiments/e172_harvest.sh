#!/bin/bash
# e172 harvest: pull pod jsonl + per-tag jsons, commit snapshot.
cd "$(dirname "$0")/.."
scp -q -o StrictHostKeyChecking=no -P 13289 root@64.119.209.250:/root/e/data/e172_maxsat_lb.jsonl data/e172_maxsat_lb.pod.jsonl 2>/dev/null
for t in bal_M16p bal_M16g4 bal_M24 bal_M24g4 bal_M32 bal_M40 const3_6_12_M24 const3_6_12_M32; do
  scp -q -o StrictHostKeyChecking=no -P 13289 root@64.119.209.250:/root/e/data/e172_${t}.json data/e172_${t}.pod.json 2>/dev/null
done
python3 experiments/e172_summary.py data/e172_maxsat_lb.jsonl data/e172_maxsat_lb.pod.jsonl 2>/dev/null
