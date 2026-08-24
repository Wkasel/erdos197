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
