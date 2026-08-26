# The portable crown theorem (hand sketch, session 10)

## Claim (to verify carefully)
The dyadic proof's two pillars are portable to ANY team T ⊆ ℤ⁺:

**Theorem (portable crown, candidate).** If 15 ∈ T, 16 ∈ T, and T ⊇ (M, 2M]
for infinitely many M ≡ 0 (mod 8), then T is not 3-permutable.

*Why it should be free:* (1) thm:c3core is a statement about ANY AP-free
order of the interval (M, 2M] with the three precedences — no reference to
S_A. Extra in-team values beyond the block only ADD constraints (more
in-team completions), preserving infeasibility of the embedded C3 system —
CHECK: the attack precedences derive, in the scheme/position setting, from
15, 16 sitting at finite positions while the block's guards/bottoms recur;
this is thm:ogred's overflow argument, which used only positions of 15, 16
and per-scale C3 infeasibility. Re-derive with T arbitrary; the odd-block
escape property of S_A was used ONLY to make finite horizons exact for the
machine — the infinite argument should not need it. VERIFY this point
hard: in S_A, completions of block pairs leaving the block were out-of-team
(free); for general T they may be in-team ABOVE the block — additional
constraints on the order (harmless for UNSAT-transfer) but ALSO the
gadget's "b_j guarded" derivation needs pairs (15, y) with y in the block:
completion z = 2y−15 ∈ block ✓ in-team ✓ same. OK.

## Consequences if true
- Any YES-partition: the team containing both 15 and 16 contains only
  finitely many full blocks (M, 2M], M ≡ 0 mod 8. Since one team must
  contain infinitely many full blocks of ANY partition into "few long
  intervals"... no — partitions need not contain full blocks at all
  (alternating colorings). The theorem constrains interval-rich partitions.
- Geneson-complements: contain giant stage-gap intervals ⊇ many full
  blocks; if they also contain 15, 16 (or a portable analogue pair — see
  below) → dead. This likely closes H1 negatively.

## The attacker-pair generalization (machine question)
Does every pair {2^j − 1, 2^j} (j ≥ 4) generate a working C3-analogue on
blocks at suitable residues (mod 2^{j/2}-ish)? Our coalition analysis at
j = 4 found {15,16} minimal-and-sufficient. If yes ∀j: any team containing
SOME crown pair + infinitely many full blocks at matching residues is dead
⟹ every YES-partition must SPLIT every crown pair {2^j−1, 2^j} between
teams, OR keep the crown-owning team block-free at the matching residues —
a severe structural constraint pushing toward either a canonical YES shape
(alternating crown ownership + sliver swaps) or a full NO via exhaustion of
the remaining shapes.
