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

## Part C3 — THE HEADLINE: the two-seam coupled core (N6 fires)

Extend Part C to THREE blocks B0 = (M, 2M], B1 = (2M, 4M],
B2 = (4M, 8M] and TWO seams: coloring c_v in {A, B}; each team its own
order; guarded APs; block-order units at BOTH seams for BOTH teams
(double non-procrastination); balance: each team >= ceil(frac |blk|)
of EACH block.  (solve_coupled3 in e120_density_cores.py; data/e120_C3.*)

**Exact balance (frac = 1/2) is UNSAT at every scale tested:**

| M | window | verdict | time |
|---|--------|---------|------|
| 16 | (16, 128], n = 112 | UNSAT | 1.2 s |
| 24 | (24, 192], n = 168 | UNSAT | 3.8 s |
| 32 | (32, 256], n = 224 | UNSAT | 8.2 s |

while ONE seam never kills (controls at M = 16 balanced, all SAT:
seams=none 0.4 s, seams=low-only 2.2 s, seams=high-only 0.8 s; plus
Part C's 2-block M = 16/32/64 SAT).  **The two seams are jointly
load-bearing: this is the first firing N6 ledger core.**  One scale
coupling cannot kill; two can.  Also SAT: seams=outer only (B0 < B2,
middle free) at M = 16 [0.6 s] and M = 24 [7.3 s] — every proper
subset of the seam chain escapes; the full chain B0 < B1 < B2 (the
middle block SANDWICHED) is exactly what fires.  The hypothesis is
honestly double non-procrastination and cannot be thinned.

**The balance dial — the UNSAT region WIDENS with scale, in both
fractional and ABSOLUTE terms:**

| M | UNSAT down to frac (bounds) | SAT at frac (bounds) | escape A-sizes |
|---|------------------------------|----------------------|----------------|
| 16 | 5/16 (5, 10, 20) | 1/4 (4, 8, 16) | [5, 24, 31] |
| 24 | 1/8 (3, 6, 12) | 1/16 (2, 3, 6) | [22, 3, 54] |

The M = 24 SAT escape at frac 1/16 nearly VACATES the middle block
(A owns 22/24, 3/48, 54/96) — i.e. the only escapes left at low
balance are block-granular / Case-1-like shapes, which N1+N2 already
handle.  The M = 16 frac-1/4 escape is the same shape one scale up
(minority 5 in the LOW block).

**Escape anatomy — the sumset dodge (hand-readable).**  Under the full
seam chain the FORCED monotone structure is exactly the cross-triple
hypergraph H = {(u, y, 2y-u) : u in B0, y in B1, 2y-u in B2}: such a
triple monochromatic in T is position-forced increasing => T dies.
(All other AP shapes have two members in one block and can be
order-dodged — which is why every proper seam subset is SAT.)  So each
color class C with U = C ∩ B0, Y = C ∩ B1 must satisfy
(2Y - U) ∩ B2 ∩ C = emptyset — a SUMSET avoidance condition, plus the
in-block order theory.  The machine escapes are exactly sumset dodges:
- M = 32, bounds (2,4,8), SAT: A ∩ B0 = {56, 60} (both ≡ 0 mod 4) =>
  2Y_A - U_A is all even => A keeps the whole ODD half of B2; while
  B ∩ B1 = {68, 72, 76, 80} sits in the BOTTOM quarter of B1, where
  2y - u <= 128 never reaches B2 at all — B has zero forced triples.
- M = 24, frac 1/16, SAT: same shape (A ∩ B1 = {52, 56, 60}, 4-spaced
  lattice, bottom of the block).
Raising the bounds to (3, 6, 12) kills every such dodge at
M = 24..40+: minorities of size >= 3 per block can no longer stay
simultaneously lattice-aligned, range-hidden, and consistent with the
in-block order theory.  The hand-schema target for N6 is precisely a
sumset/range lemma formalizing this ("a 3-element minority cannot keep
2Y - U off itself at two seams"), with the in-block rung theory
supplying the rest — the natural MUS target (e88/e90 path applied to
the balanced M = 16 core).

**The constant-bound schema (the Case-2 bridge datum).**  Fix ABSOLUTE
lower bounds (c0, c1, c2): each team owns >= c_i of block i (window
values only — the rest of Z+ unconstrained).  Machine verdicts:

| bounds | M=16 | M=24 | M=32 | M=40 | M=48 |
|--------|------|------|------|------|------|
| (3, 6, 12) | SAT | **UNSAT** | **UNSAT** (+Glucose) | **UNSAT** | **UNSAT** [187 s] |
| (3, 3, 3)  | SAT [12,3,37] | SAT [3,45,43] | **UNSAT** (+Glucose) | see log | — |
| (2, 4, 8)  | —   | —   | SAT [2,60,56] | SAT [2,76,78] | — |
| (2, 6, 12) | —   | —   | **UNSAT** | — | — |
| (3, 4, 8) / (3, 6, 6) | — | — | **UNSAT** | — | — |

Two headline facts.  (i) **(3,6,12) is UNSAT at every scale from
M = 24 to 48** — a scale-stable constant-bound rung over a 2x range,
cross-checked under Glucose42 at 24/32.  (ii) **the floor TIGHTENS
with scale**: even the minimal triple (3,3,3) fires from M = 32 on,
while every bound-2 escape that survives is the same sumset dodge
(minority pinned at the bound, mod-4 lattice, range-hidden).

Continued at M = 48: **(2,2,2) is UNSAT [135 s] and (1,1,1) is SAT**
[43 s, escape A-sizes (47, 1, 100)] — the critical constant at M = 48
is EXACTLY 2, and the (1,1,1) escape survives by leaving a 1-CLEAN
block (A has a single value in B1).  So at M = 48 the C3 gadget kills
every coloring EXCEPT those with a 1-clean block — and infinitely
many 1-clean blocks is precisely Case 1, where N1+N2 rungs already
fire.  **If the constant-2 schema is scale-stable (M = 64 probe in
flight) the dichotomy closes at C = 1**: any partition either gives
some team infinitely many 1-clean blocks (Case 1, dead modulo N2) or
eventually has >= 2 per team per block, hence >= (2,2,2) in every
window triple (M, 8M] (dead modulo the C3 schema + double
non-procrastination).
Everywhere-split partitions eventually have >= 3 per team per block,
so a proof that (3,6,12) (or (3,3,3)) stays UNSAT for ALL large M —
the coupled schema hunt, now with deletion-minimal supports as input —
kills Case 2 modulo the double non-procrastination hypothesis at two
consecutive seams (the L-DESC/T-REGRESS caveat of notes/39, now needed
at two seams: N7 may be dispensable after all).

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

RESOLVED at M = 32, F = {15,16}: last escape at per-block density
rho = 25/32 = 0.781; **UNSAT for ALL subsets with per-block density
>= 26/32 = 0.8125** [862 s at the critical point].  A FIXED low pair
is density-robust at ~0.78 on the two-block window — the same ~0.78
floor as the B2 edge pair, now from a fixed attacker with T-PIN
applying verbatim.  Edge dials (data/e120_E2_edges.log): with block1
intact, HALF-density in block2 already fires (k2 = M UNSAT); with
block2 intact, k1 = 1 fires.  Baselines: block1-alone k_crit = 29/32,
block2-alone 61/64 — the two-block coupling buys the drop from ~0.95
to 0.78.  (M = 64 refinement bracketed SAT at 24/32, UNSAT at 32/32;
the 28/32 near-critical query still running at session end.)

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
- Part C3 imposes it at TWO consecutive seams for both teams (double
  non-procrastination), and the seam controls show every proper subset
  of that hypothesis is escapable — so the C3 cores are exactly as
  strong as the hypothesis.  Converting "both teams block-ordered at
  two consecutive seams, infinitely often" from an assumption into a
  theorem (or excluding its failure by a separate rung family — the
  procrastinator teams have their own exposure: a team is
  non-block-ordered only if it re-descends below a previous block
  infinitely often, which is the L-DESC well-founded-descent
  territory) is now THE gap between the C3 schema and a Case-2 death.
  Note the C3 window values are only (M, 8M] — everything below M and
  between windows is UNCONSTRAINED, so the schema composes freely
  across disjoint window instances at scales M·8^k: the pigeonhole
  side is trivial; only the seam hypothesis is real.
