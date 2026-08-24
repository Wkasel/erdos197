# The dyadic reduction (candidate YES-construction)

**Setup.** Partition ℤ⁺ into dyadic blocks J_k = (2^{k−1}, 2^k], k ≥ 1, plus {1}. Team A owns {1} and blocks with k even, Team B owns k odd (or some variant). Each team plays its blocks in increasing order, each block internally arranged by a permutation to be chosen. Cumulative max after block k is 2^k — exactly doubling.

**Claim (checked case analysis).** For a team's infinite sequence, every potential monotone 3-AP is excluded automatically by the doubling geometry EXCEPT triples confined as follows. Writing J = (M, 2M] for a team block (M = 2^{k−1}), past = team's earlier blocks (all values ≤ M/2 — the other team owns (M/2, M]):

1. All three terms in J → need internal arrangement with no monotone 3-AP. **(a)**
2. x in team past, y and z = 2y−x both in J (increasing AP x…y…z threat): must place z before y. Danger x-values: team territory below M, i.e. zones Z_M = (M/4, M/2] ∪ (M/16, M/8] ∪ … (same-parity dyadic blocks; plus {1} for team A). **(b)**
3. Everything else is impossible:
   - Two past + one in J: completion 2y−x ≤ 2·(M/2) − 1 < M < min J. ✗
   - Pairs in J completing upward: 2y−x < 3M < 4M < min of team's next block → completions always land in the OTHER team's block (2M, 4M]. ✗ (the "dump completions on the other team" mechanism — this is exactly the leverage that defeats the DEGS argument)
   - Decreasing APs across blocks: impossible since later blocks have strictly larger values.
   - Cross-team: irrelevant; APs live within one team's sequence.
   - Forbidden-future set F_T is permanently empty: completions from values ≤ 2M are < 4M, and the team's future starts after 4M. **No global bookkeeping survives — the problem is purely block-local.**

**Reduced problem (finite, per block!).** For each M = 2^{k−1}: does there exist a permutation π of (M, 2M] with:
- (a) no monotone 3-term AP;
- (b) for every pair y < z in (M, 2M] with 2y − z ∈ Z_M: z precedes y in π.

If YES for all k (with an inductive/uniform rule), then **Erdős #197 is TRUE** — and LeSaulnier–Vijay's tightness conjecture (α(3) = 1/2) is FALSE, since each team has limsup density 2/3 (> 1/2) and liminf 1/3, α+β = 1 exactly marginal. Knife-edge again — consistent with everything else about this problem.

**Structural analysis of (b).** All top-zone (b)-pairs have y ∈ (M, 5M/4), z ∈ (3M/2, 2M] — i.e. y in the bottom quarter-ish, z in the top half. Playing the top half H = (3M/2, 2M] before the bottom half L = (M, 3M/2] satisfies ALL (b)-pairs at every zone depth (deeper zones give y in a bottom sliver, z in a top sliver). Cross-half increasing APs are geometrically impossible; the surviving conditions are:
- L must avoid decreasing-placed pairs (y first, u later, y > u) with 2y − u ∈ H;
- H must avoid decreasing-placed pairs (w first, y later, w > y) with 2y − w ∈ L;
- plus (a) within each half.
These cascade recursively with alternating forced-increasing / forced-decreasing flavors. Whether the cascade closes consistently at all depths = finite computational question per block size. If a uniform self-similar rule emerges from computation, the induction should be clean.

**Plan.** exp1: exact backtracking search for (a)+(b) permutations of (M, 2M], M = 2, 4, …, 512, both parities of zone structure. exp2: assemble full team sequences from found blocks and brute-force verify no monotone 3-AP up to 2^k. Then extract pattern → prove → write up. If blocks start failing: the failure certificates are the seed of an impossibility argument (and we pivot to non-dyadic partitions first).
