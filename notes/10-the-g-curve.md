# The g-curve: the problem's decisive quantity (2026-08-24 night)

g_X(L) := min over pure-complete-X arrangements of (max position among values ≤ L).
Soundness: a global solution bounds g_X(L) ≤ pos_π(last small) for all X, so
**divergence of g_X(L) in X (fixed L) proves S_A not permutable**, and with ray-piercing rigidity, is the route to #197 = NO.

Data:
- g_64(64) = 41 (floor: all 42 values ≤ 64).
- g_256(64) = 153 OPTIMAL (95s, CP-SAT). 112 of the 128 block-(128,256] values must precede small-completion (87%).
- g_1024(64): computing (682 values; timeout 3h).

Mechanism (why bigs precede smalls): if small values are placed early they become
zone-x's for every future block; full zones are fatal (Lemma F / tolerance O(1)),
so future blocks must be nearly complete BEFORE the smalls arrive. This repeats
at every scale — each new block pushes small-completion later. Predicted:
g_1024(64) ≈ 0.9·682 ≈ 600+. If instead g plateaus (~153), bounded-delay towers
exist and the YES-program (bounded-displacement extensions) reopens.

Proof skeleton for NO (if growth confirms):
1. Tolerance lemma (generalized): any sub-arrangement of block K placed after ≥ T
   zone-elements are placed can cover at most c·|K| of the block (c < 1) — the
   quantitative fatal zone. [Machine-assisted; needs sub-SET version.]
2. Hence in any pure-4X arrangement, ≥ (1−c)|new block| of the new values precede
   the moment when the zone (≈ old smalls) completes.
3. Iterate: g_{4X} ≥ g_X + (1−c)·|new block| − C → divergence at geometric rate.
4. Conclude S_A not permutable; ray-piercing extends the argument toward general
   partitions (to be developed).

Parallel probe: insertion cost of extending a FIXED pure-256 arrangement to 1024
(min #new values before the old part's end) — running.
