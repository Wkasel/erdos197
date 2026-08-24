"""When selfsim1024.json exists: test whether the witness's placement of new
values (non-multiples-of-4) is FUNCTIONAL in scale-free data:
  slot(v) = f(v mod 4, relative position of parent v//4, ...?)
Extract candidate rule tables and report consistency. If functional, pump to
4096 and doom-check."""
import json, sys
from collections import defaultdict

def block(v):
    k = (v-1).bit_length()
    if 2**k < v: k += 1
    return k

def sa(N):
    return [v for v in range(2, N+1) if block(v) % 2 == 0]

W = json.load(open('data/selfsim1024.json'))
pos = {v: i for i, v in enumerate(W)}
Wset = set(W)
X = 1024

# skeleton = multiples of 4 with parent in W
skel = sorted([v for v in W if v % 4 == 0 and v // 4 in Wset], key=lambda v: pos[v])
skelset = set(skel)
new = [v for v in W if v not in skelset]
print(f"n={len(W)} skeleton={len(skel)} new={len(new)}")

# for each new v: find its position between consecutive skeleton elements:
# (index of last skeleton element before v) — express relative to parent:
skel_positions = [pos[s] for s in skel]
import bisect
def slot(v):
    i = bisect.bisect_left(skel_positions, pos[v])
    return i  # v sits before skel[i]

# feature: (v mod 4, parent-place p = position of 4*(v//4)?? parent chain)
# parent value u = v // 4 (may or may not be in S_A); use skeleton anchor:
# anchor(v) = the skeleton element 4*(v//4) if present.
table = defaultdict(set)
noanchor = 0
for v in new:
    u4 = 4 * (v // 4)
    if u4 in skelset:
        rel = slot(v) - slot(u4) if u4 in skelset else None
        anchor_idx = bisect.bisect_left(skel_positions, pos[u4])
        rel = slot(v) - anchor_idx
        table[(v % 4, v % 32 // 4)].add(rel)
    else:
        noanchor += 1
print(f"no-anchor new values: {noanchor}")
print("rule table (residue features -> set of relative slots):")
for k in sorted(table):
    s = table[k]
    print(f"  {k}: {sorted(s)[:12]}{'...' if len(s) > 12 else ''}  ({len(s)} distinct)")
functional = all(len(s) == 1 for s in table.values())
print("FUNCTIONAL:", functional)
