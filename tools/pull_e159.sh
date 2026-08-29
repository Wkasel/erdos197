#!/bin/bash
# Pull e159 artifacts from pod3 and merge jsonl (dedup by tag+cell, pod wins on rerun).
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
POD="-o StrictHostKeyChecking=no -P 13289"
scp $POD "root@64.119.209.250:/root/e/data/e159_*" "$REPO/data/pod_e159/" 2>/dev/null || true
python3 - <<'EOF'
import json, os, glob
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if '__file__' in dir() else '.'
repo = os.path.expanduser('~/Dev/personal/tasks/math/erdos197')
main = os.path.join(repo, 'data', 'e159_seam_split.jsonl')
pod = os.path.join(repo, 'data', 'pod_e159', 'e159_seam_split.jsonl')
rows, seen = [], {}
for path in (main, pod):
    if not os.path.exists(path):
        continue
    for line in open(path):
        r = json.loads(line)
        seen[(r['tag'], r['cell'])] = r          # later file wins
for k in seen:
    rows.append(seen[k])
rows.sort(key=lambda r: (r['M'], r['tag'], str(r['cell'])))
with open(main, 'w') as f:
    for r in rows:
        f.write(json.dumps(r) + '\n')
print(f'merged {len(rows)} unique (tag, cell) rows')
EOF
