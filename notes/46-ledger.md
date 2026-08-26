# 46 — The N6 ledger: candidate infinite-accounting statements, drafted to be broken

FRONT N6 (notes/43 §3): the everywhere-split regime (Case 2) is the whole
remaining YES-space, its finite theory is SAT everywhere, so a NO must come
from an *infinite accounting* argument.  This note writes the candidate
ledger down precisely — two statements, L1 (sum-type) and L2 (per-scale
coupling) — and then machine-attacks both by MEASURING actual price
sequences and their coupling on the orbit-free everywhere-split colorings
we have, at horizons 2^10..2^14.  Either a statement survives measurement
(candidate theorem) or the measurements show how everywhere-split
partitions dodge (YES-material: what dodgers look like).

Experiment: `experiments/e121_ledger.py`; records `data/e121_*.json/.log`.

## 0. Setup and the price vocabulary

Partition Z+ = A ⊔ B.  Dyadic block B(t) = (2^t, 2^(t+1)], M = 2^t.
n_T(t) = |B(t) ∩ T|, densities δ_T(t) = n_T(t)/M.  Case 2
(everywhere-split): P(t) := min(n_A(t), n_B(t)) → ∞ (notes/43 §2).

From the finite 2-colored theory (notes/36) the price vocabulary:

- **donation**: a value inside a block-range that carries the *other*
  team's color — from the block-majority's viewpoint, material it ceded;
  from the partner's viewpoint, a value it must ABSORB into its own
  permutation while it sits inside foreign territory (landing-pad
  material — exactly the received-sliver surface that killed every
  sliver-swap candidate, notes/38-40).
- **endpoint zones** of B(t): bottom (M, M+w] and top [2M−w, 2M)
  (w = 16 here).  The e118 theorems: an attacked full block demands
  exactly 3 donations, and *every* optimal donation set lives on the
  attack endpoints (bottom M+{1,2,4,5,6} or top 2M−{3,5,7,11,13});
  multi-crown demands strictly more (mindon4 ≥ 5, unfinished).
- **against-type count**: P_T(t) = n_T(t) if T is the block-minority at
  scale t, else 0.  P(t) = P_A(t) + P_B(t) is the block's total price
  paid in the crudest currency (any minority value counts).

**Attacker-pair supply.**  For adjacent positions (v, v+1) in B(t):
#AA-pairs + #BB-pairs + #switches = M − 1.  So both teams can be
gap-1-pair-free only under near-perfect alternation (≥ M − O(1)
switches), which is local odd/even structure — and global odd/even dies
instantly by lem:orbit.  Away from alternation, SOME team owns Θ(M)
adjacent pairs at every scale: attacker supply is structurally
unavoidable.  (Supply lemma — trivial, but it is the pump of the ledger.)

**Attack geometry** (chain form, g4b §4b): a pair {x, x+1} ⊆ T with
x in (M/2, M] attacks B(t): for j ∈ [1, x/2], y = M + j,
z = 2M + 2j − x; if y, z ∈ T the completion forces z ≺_T y under
recurrence (T-PIN / T-PIN-STAGE pigeonhole).  Note the sharing: ALL
pairs attack the SAME bottom values y = M + j through different sources
z.  A bottom donation at M+j kills coordinate j of EVERY pair at once; a
source donation kills one (x, j) combination.  Whether prices grow with
the number of live pairs is therefore a genuine machine question, not an
additivity triviality.  This is measured below (Part B).

## 1. Statement L1 (sum-type / feedback into Case 1)

> **L1.** In every everywhere-split partition there exist a team T, a
> constant C, and infinitely many anchors a with |(a, 2a] \ T| ≤ C.

I.e., cumulative absorbed donations must CONCENTRATE: the price flow
recreates boundedly-punctured ratio-2 *windows* (not necessarily
dyadic-anchored) in some team.  If L1 holds, Case 2 feeds back into a
window-version of Case 1: the interval-form order gadgets (e89 interval
mode, machine-UNSAT at every tested (M, 2M] regardless of anchor) + the
T-PIN pigeonhole kill T modulo the window version of N2, and the NO
closes as N1 + N2 + N4 + L1.

Rationale for believing it: donations are forced onto endpoint zones
(e118: all optimal repairs are endpoint repairs), endpoint zones are
2-adically placed slivers, and accumulating partner material into
2-adically aligned slivers is exactly the received-sliver geometry that
died in H2/S1/V (the d_t law's receiver surface).  Measurement target:
window-cleanness statistics max_a density_T(a, 2a] and the count of
C-clean windows, per team, per horizon — do surviving colorings keep ALL
window densities bounded away from 1?

## 2. Statement L2 (per-scale coupling)

Donated value d ∈ B(t) ∩ P (P = absorbing team).  Completion geometry:
- with y ∈ P ∩ B(t), y > d: z = 2y − d ∈ (2M-ish, 4M) — the in-partner
  pairs created at scale t complete into B(t+1);
- with d' = d ± 1 or ± 2 also in P ∩ B(t): the pair {d, d'} is itself an
  attacker pair bearing on P's material in B(t+1) (chain geometry above).

> **L2.** There is α > 0 such that in every everywhere-split partition,
> for all large t:  P(t+1) ≥ α · L(t), where L(t) = number of LIVE
> attacker pairs at scale t (in-team gap ≤ 2 pairs in B(t) whose attack
> system into B(t+1) retains ≥ u₀ in-team completions).

Combined with the supply lemma, L2 pins everywhere-split partitions into
an ε-balanced corridor at all large scales (whichever team is
pair-rich at t forces Θ(M) price at t+1 unless its attack systems are
all broken — and breaking them costs the OTHER team donations too), and
iterating the coupling is the intended engine for L1's concentration.

The load-bearing quantitative question inside L2: **does the donation
price grow with the number of forced attacker pairs, or do shared
endpoints let one bounded repair kill all pairs at once?**  Finite probe
(Part B): p(k) = min donations for the block gadget with k pairs forced
in-team, crown pairs and chain pairs separately.  e118 knew p_crown(1)=3
and p_crown(2) ≥ 5 (unfinished).  p_chain(·) was never measured — the
chain rung {65,66} on (128, 256] is UNSAT but its repair price is
unknown.  If p(k) → ∞ the ledger has a pump; if p(k) saturates, L2 as
stated dies and the dodge is "shared-endpoint bulk repair".

## 3. Measurement design (e121)

Colorings (all at horizon 2^14, orbit status checked by closure scan):
- `gc3` — Geneson-complement λ=3, r=4 partition (W(3,4), C): the
  "we have" baseline.  NOT literally everywhere-split (chasm windows are
  C-clean — under the G4 dichotomy this partition is actually Case 1
  material for team C); kept as the family anchor.
- `gc3e` / `gc3i` — two-sided salted variants: minimum per-team presence
  f(t) = max(3, t − 6) enforced in every block by flipping values to the
  deficient team, placed on endpoint zones (`gc3e`) vs spread through
  block interiors (`gc3i`).  These are genuinely everywhere-split with
  slowly diverging prices — the cheapest conceivable Case-2 members.
- `rnd1`, `rnd2` — iid balanced colorings (controls; everywhere-split
  with P(t) ~ M/2, the most expensive members).
- `dyadic` — canonical dyadic partition (Case-1 control).

Part A (counting): per block t = 4..13 and team: n_T, δ_T, minority,
P(t); endpoint occupancy of minority material; adjacent-pair supply
(gap 1, gap 2); cross-scale flux: # in-team triples (x, y, 2y−x) with
x ∈ B(t), y, 2y−x ∈ B(t+1) [chain-attack mass], its against-type-sourced
part, and the D(t) → D(t+1) part (donation-to-donation flux — L2's
"forced donation recurrence" channel, measured directly); window
cleanness curves for L1.

Part B (price curves, the ledger quantifier): min-donation p(k) at
M = 64 and 128, complete transitivity, both teams encoded (e118
faithful), for (i) crown-pair sets {15,16}, {31,32}, ... k = 1..4;
(ii) chain-pair sets {x, x+1} ⊆ (M/2, M], k = 1..6; (iii) mixed.
Record optimal-set supports (endpoint vs interior anatomy).

Part C (counterfactual rung probes on actual traces): majority-team
trace S ⊆ B(t) of each everywhere-split coloring at t = 10, 11: order
gadget on S with attack units from ALL its own live chain pairs in
B(t−1) — SAT means the coloring has already paid this scale's price;
UNSAT means the trace pattern cannot recur infinitely often (T-PIN
pressure on Case 2).  Plus the N5 bridge: random sub-block density sweep
d ∈ {0.5..1.0} at M = 1024 under the same probe — where is the density
threshold below which rungs stop firing?

Honesty note: all Part B/C prices are *finite-gadget* prices; their sums
over scales only become death via the T-PIN pigeonhole under pattern
recurrence.  The ledger statements are the infinite quantifiers; the
measurements test their finite shadows.

## 4. Results

(measurements running — filled in below as data lands)
