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

## Part B — chain-geometry pair (x ~ M/2): d* grows with M

(results pending — see data/e120_B.log)

## Part D — existential-attacker two-scale gadget

(results pending — see data/e120_D.log)

## Part C — coupled complementary coloring (N6 probe)

(results pending)

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
