# 62 — GAP-AFFORD: the 4-block downward gadget (GAP-JOINT first)

Task: L-AFFORD (notes/54 §4.3) — for every valid ε-linear pair,
liminf_N max_T Inv_T(N)/v*(N) < 1.  Attack per the measured gap
ordering (e130 check 3: the operative escape channel at small M is
DONATION plus a below-window exposure surface ~2× the in-window
mass): build the downward-extended gadget and measure what paying the
price at anchor N forces at anchor N/2.

Machine companion: experiments/e158_joint4.py →
data/e158_joint4.jsonl + data/e158_*.json/.log.

## 1. The instrument

Values (M/2, 8M], blocks Bm1 = (M/2, M], B0 = (M, 2M],
B1 = (2M, 4M], B2 = (4M, 8M].  Two overlapping 3-block windows:

    upper  W(M)   = (M, 8M]    seams s1 = B0→B1, s2 = B1→B2
    lower  W(M/2) = (M/2, 4M]  seams s0 = Bm1→B0, s1 = B0→B1

Per-team budgets vup on Inv(M) = #inverted s1 ∪ s2 pairs and vdn on
Inv(M/2) = #inverted s0 ∪ s1 pairs (s1 shared, counts in both).
Bounds: `bal` = exact balance in all four blocks (even sizes;
M ≡ 0 mod 4); `const` = 4-vector per-team lower bounds.  Complete
encoding (full transitivity per team; guarded APs both directions
over the WHOLE range (M/2, 8M] — this is what exposes the attack
surfaces of B0-donations from below; one-way indicators; seqcounter
cards).  Every SAT witness independently re-audited (bounds, per-team
monotone-AP freedom, per-seam recounts at both anchors, mono
cross-triple/inversion-edge cross-audit for BOTH windows'
H-families).  v = 'none' ⇒ that anchor unpriced (no indicators).

**Lemma T-FORCE-4 [PROVED — verbatim restriction, notes/54 Lemma
T-FORCE].**  A valid pair meeting the four block bounds at anchor M
with Inv_T(M) ≤ vup and Inv_T(M/2) ≤ vdn for both teams induces a
model.  Hence UNSAT(M; vup, vdn) ⟹ every valid pair meeting the
bounds has some team exceeding a budget at one of the two anchors.

**Lemma L-PROJ [PROVED — projection].**  Deleting all clauses that
mention Bm1-values from the 4-block instance yields exactly the
3-block e127 instance at anchor M (inversion indicators on s1, s2
unchanged; bounds on B0..B2 unchanged).  A 4-block model restricted
to (M, 8M] is therefore a 3-block model at the same vup.  So
SAT_4(vup, ·) ⟹ SAT_3(vup):  **v*_up-in-4-block ≥ v*_3(M)**, and
every 3-block UNSAT verdict transfers upward to the 4-block for
free.  Symmetrically, restricting to (M/2, 4M] shows
v*_dn-in-4-block ≥ v*_3(M/2).

## 2. Cell map and baselines

| cell | (vup, vdn) | question |
|------|-----------|----------|
| C0 | (none, none) | encoding sanity — finite theory SAT (notes/36) |
| C1 | (v, none) | does the dense block BELOW raise the anchor-M price past v*_3(M)? |
| C2 | (none, w) | anchor-M/2 price with B2-material present, upper unpriced (baseline) |
| C3 | (v, w) | THE PUMP — does paying at anchor M force > baseline at anchor M/2? |

Baselines measured this session:

- **v*(bal,8) = 0** [MACHINE-CHECKED, data/e158_bal8_base.log]: the
  standalone 3-block window at anchor 8 (blocks 8/16/32) is SAT at
  v = 0 — a seam-clean balanced escape exists, audit-passed.  The
  two-seam core does not yet fire at M = 8.  Consequence: at M = 16
  ANY forced vdn > 0 in the joint gadget is pure downward coupling —
  the standalone lower-anchor price is zero.
- 3-block v*(bal,16): UNSAT at v ≤ 2 (e127), pin-variant UNSAT at 4
  (pod3, data/fleet_2026-08-28/), SAT at 6 (e132 CP-SAT) ⟹
  v*(bal,16) ∈ {5,6}; Cadical SAT-side at v = 8/32 times out
  (17000/14400 s) — near-critical SAT hunting is the hard direction
  on this instance family.
- **C0 (M=16) SAT [0.3 s]**, audit clean; unpriced witness pays
  n_up = 528/358, n_dn = 44/92 (A/B) — lavish procrastination when
  free, exactly the §4 e127 asym phenomenology.

## 3. Verdicts (updated as cells land)

- **C2 (none, 0) @ M=16: SAT [0.8 s]** [MACHINE-CHECKED,
  data/e158_c2_M16_dn0.log].  With the upper anchor unpriced, BOTH
  teams are perfectly clean at the lower anchor — n_s0 = n_s1 = 0 for
  both — by dumping the entire procrastination mass onto seam s2
  (n_s2 = 392/442, far beyond any upper budget).  **The material of
  B2 alone forces nothing at anchor M/2; the baseline lower price in
  the 4-block geometry is 0.**  Every forced vdn > 0 in a priced cell
  is therefore attributable to the upper anchor's BUDGET, not to the
  presence of material — the attribution control the strong-L2
  refutation lacked.
- **C3 (vup=6, vdn=0) @ M=16: UNSAT [2.1 s]** [MACHINE-CHECKED,
  data/e158_c3_M16_up6_dn0.log].  THE HEADLINE CELL: with both
  anchors priced at values their standalone 3-block theories ALLOW
  (3-block bal@16 is SAT at v = 6, e132; standalone anchor-8 price is
  0, §2), the joint 4-block system is INFEASIBLE — and the UNSAT is
  three orders of magnitude faster than the near-critical 3-block
  queries (2 s vs hours), i.e. heavily overconstrained: the true
  joint frontier is far from the componentwise prices.  By
  T-FORCE-4: every valid balanced pair has, at anchor 16 vs 8, some
  team with Inv(16) > 6 or Inv(8) > 0.
- C1 attribution cell (vup=6, vdn=none) in flight.
