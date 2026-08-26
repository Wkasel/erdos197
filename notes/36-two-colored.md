# 36 — The 2-colored order gadget and coupled rungs (task H3)

Session goal: abstract the impossibility machinery from the fixed dyadic
partition to ARBITRARY 2-colorings, per team, coupled only through the
coloring. Two machine probes: (a) the joint 2-colored order gadget on
(M, 2M] + attackers {15, 16}; (b) the coupled chunk/rung system (paper
thm:chunk conditions (A)+(B) per team) with displacement caps.

## Formalization

Fix M and a 2-coloring c of (M, 2M] ∪ {15, 16}. Team T's induced gadget
takes only its own material:

- **triples**: every in-block AP triple (x, y, z=2y−x) with
  c(x)=c(y)=c(z)=T must be non-monotone in T's order;
- **attacks**: for attacker x ∈ {15, 16} with c(x)=T and j ∈ [1, ⌊x/2⌋],
  y = M+j, z = 2M+2j−x ∈ (M, 2M]: if c(y)=c(z)=T then z ≺_T y (residue of
  x's finite position: x precedes cofinitely many block values, so the
  increasing AP x < y < z forces z before y).

A completion crossing teams is FREE for the completing team — but the
crossing value now lives in, and is constrained by, the other team. The
coupling is purely through c. This is the per-team specialization of the
chunk reduction, which holds verbatim for any team (thm:chunk never uses
the dyadic structure; normalization lem:normal ports to any team with base
g(v) = ⌈log₄ v⌉, since the running-max argument only needs finite level
sets of g on the team).

Code: `experiments/e118_two_color_og.py` (gadget, modes allA / free /
split / mindon / nosliver / minsliver), `experiments/e119_two_color_rung.py`
(coupled rung, modes dyadicAonly / dyadic / same / split / free / richD).
Both: color variables + two order matrices, constraints gated by colors,
lazy transitivity per team (UNSAT verdicts are conclusive at any point since
clauses are only added; SAT verdicts are reported only on
transitivity-clean models). e119 encodes stage-forced order by unary
thresholds: for each pair (p,q), team T, threshold t:
(s(q) ≥ t) ∧ (s(p) < t) → p ≺_T q — exactly (A)+(B) of thm:chunk at finite
horizon, ~24 clauses/pair/team instead of e83's (cap+1)² combos.

## (a) Joint gadget: always SAT; the price and shape of feasibility

Baselines (encoder validation): forcing every color = A reproduces OG(M)
UNSAT at M = 64, 128, 256 (data/e118_{64,128,256}_allA.json).

**Free coloring is SAT at M = 64, 128, 256** — the joint system is never
universally infeasible, as expected. First witnesses found by the solver:

- M=64: c15=A, c16=B (crown SPLIT);
- M=128: c15=B, c16=A (crown split);
- M=256: c15=c16=B with team B a scattered 55-element minority (crown
  together but its team BLOCK-POOR).

**Minimum donation (mindon: c15=c16=A, minimize #block values colored B):**

| M | min donation | # optimal sets | support of all optimal sets |
|---|---|---|---|
| 64 | 3 | 28 | {66,68,69,70} ∪ {117,121,123,125} |
| 68 (≡4 mod 8 control) | 3 | 24 | {69,70,72,74} ∪ {123,125,129,133} |
| 128 | 3 | 26 | {129,130,132,133,134} ∪ {243,245,249,251,253} |
| 256 | (see data/e118_256_mindon.json) | | |

In block coordinates the support is IDENTICAL across scales and residues:
bottom-sliver b-values M+{1,2,4,5,6} and top t-values 2M−{3,5,7,11,13} —
precisely the attack endpoints (b_j = attacked bottoms, t_i = attack
sources z = 2M+2j−x). Nothing outside the two slivers ever appears in an
optimal repair. Min donation 3 is stable in M (64→128, and 68 shows it is
not a mod-8 artifact: the full attack system, not just the C3 core, drives
the price).

**Sliver donation is NOT forced.** With the bottom sliver pinned to A
(nosliver), min donation is still 3, with exactly 3 pure-top optimal sets
at both M=64 and M=128: {2M−11, 2M−7, 2M−5, 2M−3} minus one element, every
set containing 2M−7. And minsliver = 0: a coloring can donate 0 sliver
values. So the gadget's minimum repairs form exactly TWO families:
bottom-sliver swaps (the Geneson/H2 shape) and TOP-sliver swaps (its mirror
at the attack sources). H2-unification is thus partial-but-sharp: Geneson's
bottom-sliver removal is one of exactly two minimum repair families, and
both live on the attack endpoints.

Splitting the crown (split mode) needs 0 donations at M=64.

**Multi-crown (free4: attackers 15, 16, 31, 32 all colored):** still SAT
at M = 64 and 128. The witnesses do NOT split every pair: at M=64 the
solver keeps {31,32} together in the minority team B (24 scattered values)
while splitting {15,16}; at M=128 it keeps {15,16} together in minority B
and splits {31,32}. So at a single block the escapes compose: split SOME
pair, park the others in the block-poor team. A pair kept together in the
MAJORITY team is what costs donations (mindon4 measures that price).

## (b) Coupled rungs: no universal divergence; a coloring trichotomy

Model: colors for all v ∈ [2, 4^m]; per value a stage s(v) = g(v) + δ(v),
g = ⌈log₄·⌉, δ ∈ [0, cap]; per team, order respects stages and every
same-team AP triple is non-monotone (= (A)+(B) of thm:chunk). Crown-cap
metric (as in the crown ladder): δ(15), δ(16) ≤ CAP, all else free ≤ 8.

Validation: dyadicAonly (dyadic coloring, team-A constraints only)
reproduces the crown ladder: m=3 min CAP = 1; m=4 CAP=1 UNSAT (11 s) ⇒
min CAP = 2 at N=256 — the machine-certified crown rung. With team B's
constraints added (dyadic, both teams) the values are unchanged (m=4:
CAP=1 UNSAT, CAP=2 SAT) — the odd-block team is schedulable alongside.

Coupled results over coloring classes:

| mode | m=3 (N=64) | m=4 (N=256) |
|---|---|---|
| dyadic (fixed coloring) | min CAP = 1 | min CAP = 2 |
| rich0 (c15=c16=A, even blocks ≥ 6 fully A, rest free) | min CAP = 1 | min CAP = 2 (CAP=1 UNSAT 23 s; CAP=2 SAT, δ15=δ16=2) |
| same (c15=c16=A, ALL else free) | CAP = 0 SAT | CAP = 0 SAT |
| split (c15=A, c16=B, rest free) | CAP = 0 SAT | CAP = 0 SAT |
| free | CAP = 0 SAT | (subsumed by split/same) |

**The divergence shadow does NOT extend to all colorings**: at both
horizons there are colorings with zero crown displacement even with the
crown forced together (same mode). The witness shape is the point: the
crown-owning team is a strict MINORITY inside every long dyadic block
(m=4 same-witness block profile (nA,nB): block 5: 2/14, block 6: 11/21,
block 7: 11/53, block 8: 34/94), with a handful of off-majority sliver
values. The solver, given full freedom, lands exactly on the escape route
predicted by the portable-crown analysis (notes/37): keep the crown team
block-poor.

**But the ladder is coloring-UNIFORM on the block-rich class**: rich0
(crown together + even blocks intact in the crown team, everything else —
including all odd blocks and small values — free) has min CAP = 1 at m=3
and ≥ 2 at m=4, matching the dyadic ladder rung-for-rung. The dyadic crown
rung is thus not about the dyadic coloring at all: EVERY coloring whose
crown team keeps the even blocks intact pays the same growing displacement.
This is the finite shadow of the portable crown theorem, now
machine-checked over the whole class rather than one partition.

**Donation-displacement tradeoff (richD: ≤ D donations per even block ≥ 6):**
D=3 at CAP=1, m=4: see data/e119_4_1_rich3 — compares the coupled price
with the order-only price 3 from (a).

## Shape of the feasible region (the emerging trichotomy)

Every coloring the machine found feasible at these horizons uses one of:

1. **Crown split**: 15 and 16 in different teams (kills both attack
   families at once; 0 donations, 0 displacement);
2. **Block-poor crown team**: the crown's team is a minority in every long
   block (no full-block gadget ever forms);
3. **Endpoint donations**: ≥ 3 values per attacked full block, drawn
   exclusively from the two attack slivers — bottom M+{1,2,4,5,6}
   (Geneson/H2 sliver-swap shape) or top 2M−{3,5,7,11,13}.

Conversely, colorings outside these escapes (rich0) inherit the full
dyadic displacement ladder uniformly. For a general NO one would now have
to kill the three escapes at ω: (1) is a single Boolean choice per crown
pair {2^j−1, 2^j} (the portable-crown attacker-pair program — if every
crown pair must be split, and crown pairs interact, a global parity
obstruction becomes conceivable); (2) forces upper density ≤ 1/2 on blocks
for the crown team, i.e., a Geneson-complement-like structure for the
OTHER team, which then contains near-full blocks and needs ITS crown pairs
handled; (3) is exactly the sliver-swap geometry of H2. The 2-colored
machinery here (e118/e119) is the diagnostic for all three.

## Open / next

- rich-D bisection at m=4 CAP=1 (donation price under coupling) — partial.
- m=5 (N=1024) same-mode CAP=0: does the block-poor escape survive another
  octave pair, or does minority-team pressure (its OWN crown pairs, e.g.
  {31,32}, {63,64}) start biting? Needs RunPod-scale encoding (~25M gated
  clauses with the threshold encoding; stream DIMACS rather than pysat
  lists). Not launched locally. Multi-attacker gadgets ({2^j−1, 2^j} for several j
  simultaneously, each colored) are the natural e118 extension: escape (1)
  splits ONE pair, but every pair must be handled; a joint gadget with
  attackers 15,16,31,32,63,64 would test whether splits can be chosen
  consistently. Not yet coded.
- Mid-block donations never appear in optimal repairs — worth a hand proof
  ("repairs live on attack endpoints"): plausibly an exchange argument on
  the hitting-set of inconsistent cores.
