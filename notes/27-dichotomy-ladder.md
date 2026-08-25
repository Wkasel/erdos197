# The dichotomy ladder (session 6)

## The NO-theorem template (rigorous modulo the ladder)
Let L(m) := min over all stage schemes at horizon 4^m (any displacements
δ(v) = s(v) − block(v)/2 ≥ 0) of max_{v ≤ 16} δ(v).

**If L(m) → ∞ then S_A is not 3-permutable.** Proof: an infinite scheme
assigns each of the ten values v ≤ 16 a FIXED finite displacement; its
restriction to horizon 4^m is a valid finite scheme whose low-value
displacements are those constants — contradicting L(m) ≥ m−2 for large m.
(Chunk reduction is exact, so non-existence of schemes = non-permutability.)

## Machine rungs so far
- L(3) ≤ 1 (witness, e75: δ(15)=0 feasible at 64; window-1 opt at 64).
- **L(4) ≥ 2** (e77: capping δ ≤ 1 on all v ≤ 16, rest free ≤ 8:
  INFEASIBLE at 256, 252s CP-SAT). pysat cross-check running (e82).
- L(5) ≥ 3? — e78 running on fleet5 (cap ≤ 2 at 1024, rest free).
- Minimal coalition at m=4 being extracted (e81): which low values'
  caps drive infeasibility (deletion loop).

## Free-space structure findings
- δ(15) ≥ 2 is NOT forced in free space (e75/e76: feasible with 15 at
  natural stage — window-2's {15}-MUS was window-specific). The burden
  moves (δ(4)=3 in the m=4 free optimum): it's a COALITION property, not
  a single-value property. Hence L uses max over the low set.
- Free-space minimal skeleton (kept-at-natural): K_s = {v ≡ 2^s−1 mod 2^s}
  ∩ escape zone = {3} ≺ {11,15} ≺ {47,55,63} — the trailing-ones classes.
  Class-closed; K-attackers' completions land in K (self-protecting).
- K-scheme with lag-2 dump: fiber-4 UNSAT via the half-class traitors
  (sub-escape ≡ −1 mod 2^{s−1} values reflecting K_s pairs from a later
  stage: cycle 191<239<207<191, hand-verified). Full-class version breaks
  (A) at (55,143,231): reflections drop to the parent class ≡ −1 mod 2^{s−1}
  — the class tower needs R-comparator-style ORDER-side protection, which
  rigid stages cannot express. Every closed-form rescue so far dies one
  level up: consistent with L(m) growth being genuine.

## If the ladder holds — the arc beyond dyadic
Dyadic NO kills the natural candidate + the LV-refutation route. The attack
calculus (small values attack every block's bottom sliver; overload forces
displacement growth) may abstract to arbitrary teams: (1) finish dyadic NO;
(2) abstract attack-overload lemma; (3) every 2-partition has a side meeting
overload at all scales ⟹ Erdős #197 = NO. Step 3 is where DEGS/HS ray
methods would combine with density pigeonholing (why 3 teams escape: block
rotation breaks attack chains).

## Coalition extraction (e81, in progress)
Deletion order 3,4,9,10,11,12,13,14 — ALL droppable (UNSAT persists with
caps only on the remainder). Interim: the free-space divergence coalition at
N=256 is ⊆ {15, 16} — the top of block 4. Consistent with (i) the top-half
non-deferrability characterization, (ii) the window-2 MUS {15}, (iii) the
2024-era prediction that block tops (16, 64, 256) are the divergence locus.
Awaiting final drop-15 / drop-16 tests.

## FINAL COALITION (e81 complete): {15, 16} EXACTLY
Jointly UNSAT capped at δ≤1 (rest free ≤8) at N=256; either alone droppable
(SAT). So: **every scheme at 256 has δ(15) ≥ 2 or δ(16) ≥ 2.**
15 = 1111₂ = crown of the ≡−1 (K/odd) tower; 16 = 10000₂ = block top =
crown of the ≡0 (C/even) tower. The two defense skeletons are mutually
limiting: a scheme protects the block hierarchy with one crown early only by
diving the other. Refined divergence conjecture:
    max(δ(15), δ(16)) ≥ m − 2  at horizon 4^m  (⟹ S_A not permutable).
Crown rung at m=5 (cap {15,16} ≤ 2, rest free): e84 launched.
Cross-refs: window-2 MUS {15} (window space); e76 (cap 15 → δ(16)=2 dive);
prediction "block tops = divergence locus" (notes/09, session 2).

## CROWN THEOREM (two rungs, machine-certified)
- N=256: cap δ(15),δ(16) ≤ 1, rest free ≤ 8: INFEASIBLE ⟹ max(δ15,δ16) ≥ 2.
- N=1024: cap ≤ 2, rest free ≤ 8: UNSAT (pysat 5181s, 69 rounds)
  ⟹ **max(δ(15), δ(16)) ≥ 3.**
Reframed: the crowns must reach the top block's stage-region at every
horizon (δ ≥ m−2 ⟺ stage ≥ m). If this holds ∀m: S_A not permutable
(two fixed values, finite displacements, restriction contradiction).
Robustness run: DMAX=14 rerun at 1024 (exclude ceiling artifacts) — running.
Crown rung 3 (N=4096, cap ≤ 3): launched fleet5.

## The cascade mechanism (hand, toward the induction)
Deferring block-6 crowns (60, 64) to stage σ forces, per witness pair
(x ∈ block 4, midpoint (x+60)/2 ∈ {35..38} ⊂ block-6 bottom): either the
midpoint defers to ≥ σ too, or the block-4 attacker x rises above the
midpoint's stage. So high crowns drag either (i) a block-4 value upward
(→ its own crown pressure) or (ii) growing bottom-mass of block 6 up to σ,
which re-attacks block 6's top sliver and recurses. Target formal lemma:
deferred mass at stage σ in block 2t forces (crown of block 2t−2 at ≥ σ−c)
or (positive-fraction of block 2t−2 at ≥ σ−1) — mass exhaustion over m
scales then yields the crown divergence. Bookkeeping in progress.

## THE ORDER GADGET (session 7 — the breakthrough)
Family-MUS of crown-cap infeasibility at 256 = {atk15:8, atk16:8, blk:8}:
single-block! And within one block the stage machinery collapses (stages +
fiber orders ⟺ one total order of the block; the case table degenerates to
plain non-monotonicity + attack precedences). Hence:

**Crown theorem at horizon 4^m ⟺ OG_{2m} infeasible**, where OG_K is the
pure order problem: order block (M, 2M] (M = 2^{K−1}) with (i) all in-block
AP triples non-monotone, (ii) attack precedences t_{15−2j} ≺ b_j and
t_{16−2j} ≺ b_j (b_j = M+j, t_i = 2M−i): each of the bottom-eight values
guarded by an adjacent top PAIR {t_{15−2j}, t_{16−2j}} (b_8 by t_0 alone).

Machine: OG_8 UNSAT (2s); drop either attack family → SAT (both crowns
essential ✓ matches coalition); **OG_10 UNSAT (108s)**; OG_12 running.

**If OG_K is UNSAT for all even K ≥ 8, then in any valid scheme both crowns
cannot lie strictly below any block ⟹ some crown has stage ≥ t for every
t ⟹ contradiction ⟹ S_A IS NOT PERMUTABLE.** (Pigeonhole over the two
crowns; chunk reduction exactness.) The remaining mathematics is ONE
scale-uniform statement about interval orders. Triple-level MUS of OG_8
extracting now (e88) — target: a scale-invariant finite pattern + hand proof.
Note: guard pairs' downward completions 2b_j − t = 16 leave the block —
the gadget is genuinely self-contained (crowns appear only as the numbers
15, 16 in the offsets).

## Late fleet verdicts (batch)
- LADDER X=256 d=2 (free extras): SAT (42559s) — weak necessary condition
  passes, as expected.
- LAW X=64 d=3 (law-pinned): UNSAT (48064s) — the ≡2 mod 2^{k/2} defect law
  is definitively wrong/too rigid at (64, d3); the law frame is closed.
  (Chunk/OG frame superseded it; this is consistency, not news.)
