# e120: dense-subset cores (FRONT N5) — the density dial

## Question

N5 (notes/43 §3): does a pair rung fire on ANY in-team subset of
density >= 1/2 + eps of a block?  e120 makes the subset ADVERSARIAL
inside the SAT instance: selection variables s_v alongside the order
variables, cardinality |S| >= k, AP clauses and attack units guarded
by selection.  SAT = the adversary can pick a subset of size >= k
(and an order on it) escaping the rung; UNSAT = the rung fires on
EVERY subset of size >= k.  Escape is monotone downward in k (any
subset of an escaping set escapes, constraints only shrink), so each
gadget has a critical
    k_crit(M, F) = max k with an escape,   rho* = k_crit / M,
and "UNSAT over all subset choices" holds exactly for density
> rho*.  Soundness: full transitivity stays unguarded (a total order
on the whole window restricts to a total order on S), so
UNSAT-for-all-subsets needs no extra argument; every SAT verdict is
re-checked by an independent scanner on the decoded subset + order.
Solver: Cadical195, complete encodings (n <= 192 here).
Code: experiments/e120_density_cores.py; data/e120_{A,B,C,D}.json +
e120_results.jsonl (streaming).

## Part A — fixed low pairs are NOT density-robust (d* = O(1))

Fixed pair F, window (M, 2M], scan by binary search on k.

| F | M | k_crit | d* = M - k_crit | rho* | minimal escape drops |
|---|---|--------|-----------------|------|----------------------|
| {15,16} | 64  | 61  | 3 | 0.953 | {66, 68, 69} = {M+2, M+4, M+5} |
| {15,16} | 96  | 93  | 3 | 0.969 | {98, 100, 101} = {M+2, M+4, M+5} |
| {15,16} | 128 | 125 | 3 | 0.977 | {130, 132, 133} = {M+2, M+4, M+5} |
| {11,12} | 64  | 62  | 2 | 0.969 | {66, 68} = {M+2, M+4} |
| {11,12} | 96  | 94  | 2 | 0.979 | {97, 100} / {M+2, M+4} |
| {11,12} | 128 | 126 | 2 | 0.984 | {130, 132} = {M+2, M+4} |

Three findings, all scale-stable across M = 64/96/128:

1. **The adversarial puncture tolerance of the generic-pair rung is
   exactly 2 (for {11,12}) and exactly 3 (for {15,16})** — sharper
   than the Q3 torture rows (which showed specific <= 8-puncture sets
   staying UNSAT on the richer two-block STG form): here ANY 2 (resp.
   1) punctures leave the single-block rung UNSAT, and a specific 3
   (resp. 2) kill it.  This is the exact N3 constant for the
   single-block form.
2. **The minimal escape is always the same bounded set of bottom
   MIDPOINTS {M+2, M+4(, M+5)}** — the receiver values y of the
   attack units (z, y) = (2y - x, y).  The C3 hand proof's flood
   centres live near 3M/2, but its zigzag anchors are exactly these
   bottom midpoints; the machine says the whole certificate hangs on
   2-3 of them.
3. **Consequently rho*(M, fixed pair) = 1 - O(1)/M -> 1**: a fixed
   low pair's attack surface is O(x) values, and the everywhere-split
   adversary evicts a bounded core of it.  Fixed-pair rungs can NEVER
   power N5; the density dial confirms the suspicion structurally,
   not just asymptotically.  (New small datum: {11,12} intact is
   UNSAT already at M = 64 — the M = 128 pair-threshold map's lowest
   pair fires one scale earlier than previously recorded.)

Relation to the truncation warm start (notes/39 CHECK 4): the S2
truncated rungs stayed UNSAT with up to 36% of the block gone because
the attackers there were SHIFTED (x = 2s + 15/16) to keep their
attack surface inside the surviving window.  With attackers FIXED,
2-3 adversarial evictions suffice.  Lesson for N5: the attacker pair
must be chosen inside / adapted to the dense subset — which is what
Parts B and D test.

## Part B — chain-geometry pair (x ~ M/2): d* = Theta(M), rho* = 7/8

Pair F = {M/2+1, M/2+2} (the "pair inside the previous block" of the
chain rungs), window (M, 2M]: Theta(M) attack units.  Singles x and
x+1 alone stay SAT (chain singles behave like low singles).

| M | F | k_crit | d* | rho* | minimal escape |
|---|---|--------|----|------|----------------|
| 64 | {33,34} | 56 | 8 | 0.875 | drop even midpoints {66,68,...,80} |

**d* = x/4 = M/8 GROWS with scale**: the chain-geometry rung is
density-robust with critical density rho* = 7/8 (the escape needs a
positive FRACTION of the block — every other midpoint — not a bounded
dust).  First rung in the campaign whose subset-tolerance is Theta(M).
(M = 96/128 in flight to confirm 7/8 is exact and scale-stable.)

## Part B2 — pushing the attacker to the window edge: rho* ~ 0.78

Law test rho* = 1 - x/(4M) with the pair just below the window,
F = {M-2, M-1}:

| M | F | k_crit | d* | rho* | law prediction |
|---|---|--------|----|------|----------------|
| 64 | {62,63} | 50 | 14 | 0.781 | 0.766 |

Close to the law but slightly above (the minimal escape is no longer
pure midpoint-parity — it mixes low midpoints with scattered high
receivers).  Higher x buys a lower critical density; extrapolated
floor of the single-pair mechanism ~ 3/4.

## Part D — existential-attacker two-scale gadget

The faithful N5 form: adversary keeps S0 (>= rho |B0|) of
B0 = (M/2, M] AND S1 (>= rho |B1|) of B1 = (M, 2M]; ALL kept B0
values precede all kept B1 values (non-procrastination); guarded APs
everywhere (cross-block APs = chain attacks from EVERY kept low
value).  Intact (rho = 1): UNSAT.  rho = 1/2: SAT escape at M = 64.
Binary search on the 1/64 grid in flight.

## Part C — coupled complementary coloring (N6 probe): SAT at balance

B0 = (M, 2M], B1 = (2M, 4M]; every value colored A or B; each team
must own >= kb/M fraction of EACH block (everywhere-split), each team
carries its own order with ITS block-order hypothesis (both teams
non-procrastinating at the seam).

- M = 32, exact balance (kb = 16): **SAT** [0.6 s].
- M = 64, exact balance (kb = 32): **SAT** [61 s].

Neither side inherits a firing core from ONE seam: the finite coupled
theory is SAT at exact balance.  Escape structure at M = 64: exactly
32/64 per block per team, hybrid coloring — complementary interval
RUNS in the lower parts (both teams hold many adjacent pairs — the
pairs do not fire because each team denies the partner the matching
receiver cohort upstairs) and a clean odd/even PARITY split near the
top of B1 (225..243 odd -> A, even -> B).  This is notes/36's "SAT
everywhere" surviving even under the strongest two-scale coupling +
double block-order hypothesis: a single seam cannot kill; any N6
ledger must couple >= 3 scales or add cross-seam conservation.

## Part E — fixed pair, STG TWO-block window, per-block density dial

The channel that changes everything for N5: over the two-block window
(M, 4M], a FIXED low pair x attacks with y in block1's upper part and
z = 2y - x in block2 — Theta(M) units from a fixed attacker, so
density-robustness no longer requires attackers scaling with the
window (no varying-attacker/procrastination caveat: T-PIN applies
verbatim to infinitely many disjoint two-block windows).
Per-block cardinalities k1 >= rho M, k2 >= rho 2M.  Results stream
into data/e120_E.{log,json}.

## Mechanism notes (chain escape anatomy, M = 64)

- The minimal chain escape (drop even midpoints) leaves 17 units in
  which consecutive receiver pairs are spaced 4 apart instead of
  overlapping — the coupling between consecutive attack triples is
  what the adversary must destroy, and destroying it costs every
  other midpoint = x/4 = M/8 values.  The escape is CONSTRUCTIVE at
  every scale tested: parity-thinned instances are SAT at
  M = 96/128/192/256 (k ~ 0.87 M, data/e120_B3_thinned.log).
- The naive hand schema "two consecutive kept midpoints + full rest
  of the block => fire" is FALSE: keeping any single consecutive
  midpoint pair (all other midpoints dropped) is SAT at M = 64, for
  every pair position (data/e120_B4_schema.log).  The core needs a
  LONGER midpoint zigzag; its exact anatomy is the natural next MUS
  target (e88/e90 path applied to the k = k_crit + 1 instances).

## Caveats

- Parts B/D treat the lower-scale attackers as placed before the
  upper window.  For a FIXED finite attacker set this is T-PIN
  (any fixed finite F in T has only finitely many T-values at
  positions below max-position(F), so cofinitely many blocks are
  clean); for the two-scale form with attackers varying per scale it
  is the non-procrastination hypothesis — the L-DESC/T-REGRESS
  well-foundedness machinery of notes/39 is the intended hand
  companion, NOT yet a theorem at this geometry.  e120 measures the
  finite side only.
- Part C additionally imposes block-order for BOTH teams at the same
  seam (both teams non-procrastinating) — the strongest hypothesis;
  its UNSAT would be a finite N6 ledger core under that hypothesis.
