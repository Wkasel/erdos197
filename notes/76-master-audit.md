# 76 — MASTER ASSEMBLY AUDIT (2026-08-30, end of day): adversarial
# spot-verification of notes/71-75 + final pod harvest

Task: (1) spot-verify each same-day front document — one load-bearing
lemma per doc reconstructed independently, one machine check at a
FRESH scale, encoders written from scratch (experiments/
e178_audit_spot.py, record data/e178_audit_spot.jsonl); (2) harvest
the in-flight pod ladders; (3) rewrite notes/50 as the final
dependency graph; (4) update STATUS + probability.  This file is
(1)+(2); the graph is notes/50; the bottom line is STATUS.

## 1. Spot-verification: 8/8 checks PASS, zero broken claims

All expectations pre-registered in the e178 docstring before any run.

| doc | reconstructed lemma (hand) | fresh machine check | verdict |
|-----|----------------------------|---------------------|---------|
| notes/71 (J/F-schema) | **Lemma K** re-proved by exhaustive search: [1..n] with prefix [1..k] wholesale-first admits a monotone-3AP-free order iff n ≤ k+4, for k = 2, 3, 4 (15 cells, sharp at both bases (7,2)/(8,3) — exactly the notes/62/71 statement incl. the (6,2) boot anomaly) | **cmin(20) = 20 = M, CP-SAT OPTIMAL [25.7s]** — a FOURTH exact scale for GAP-CMIN's basis (was 8/12/16); fresh instrument (independent min-encoding, adversarial side-selection via big-M switch) | PASS |
| notes/71 §6 (margin) | budgeted-K encoder rebuilt from scratch (order vars + MP clauses + inversion cardinality) | K(9,3) = 3 and K(12,4) = 4 reproduced; **NEW diagonal point K(27,9) = 51** (the k = 9 hole; monotone inside (40, 69]); **K(36,12) = 111 CONFIRMED** (UNSAT 110 [0.5s] / SAT 111 [0.4s]) — see §2 provenance note | PASS |
| notes/72 (vmin0) | **L-MID** case analysis re-derived (V(u) window computation checked case by case; the (3M/2, 7M/4] all-of-Bm1 window and the |U| ≤ M/4 safe prefix both re-verified) | L-MID UNSAT at **FRESH M = 48** (SAT-encoder, |U| = M/2, |W| = M/4, midband-clean forbidden) with the |U| = M/4 control SAT; independent brute force at M = 16 (0 clean pairs over all C(16,8)×C(8,4)) | PASS |
| notes/73 (N2-parametric) | **Lemma MIR** arithmetic re-derived (b_i + t_i = 3M = 2·ctr, even M; b_{i−1} + t_i = 3M−1, odd M — the twin law is one line of algebra, checked) | **K4e(23) fires at FRESH M = 160** (beyond the probed 152; complete-encoding from-scratch solver, UNSAT [~1s]) with SAT control at M = 164 (≡ 4 mod 8) — the x ≡ 7 mod 8 dyadic lane law extends | PASS |
| notes/74 (N3+L1′) | **ROT4 phase identity** re-derived by hand: u = 2^m + 1 + p ⟹ p_w = 2p_u + 1 − f ⟹ φ(2u−f) = φ(u) − 4(f−1)/2^{m+1} exactly (checked; the two-branch r-drop analysis follows) | window law max_a(6·|T∩(a,2a]| − 5a) = **0 for BOTH teams to FRESH horizon 2^17** (sup 5/6 attained, never exceeded); chains from FRESH seed octave (2^12, 2^13], adversarial f ≤ 64, horizon 2^23: **max depth 1** | PASS |
| notes/75 (pump-schema) | **Theorem J-DOWN** restriction argument re-walked (a feasible U4(M; b; v, 0) state restricts to a feasible anchor-M/2 3-block state at budget 0 — every AP clause/bound/indicator of the small instance is a constraint of the big one; sound) + Lemma P-CAT emptiness re-derived (the four range computations) | P-CAT family laws at **FRESH M = 200**: same 4 empty patterns, |H_up| = 50000 = 5M²/4, |H_dn| = 12500, |SKIP| = 32500 — exact; **balanced two-seam coupled core UNSAT at FRESH anchor m = 28 [3.2s]** — from-scratch encoder (global-order + conditioned MP + 2.5M clauses), a NEW core scale between the tested 24 and 32 ⟹ with J-DOWN: v_min(0)(56) = ∞, a fresh instance | PASS |

Audit incidentals (both in my own audit code, both fixed in place —
the fronts' claims were right and my first instruments wrong):
octave-top misassignment in the ROT4 membership function
(v.bit_length on v = 2^{m+1}; the −6 excess it produced was the
audit's bug, not the notes'); no others.

## 2. One provenance finding (value CONFIRMED, citation imprecise)

notes/71 §11 reports "K(36,12) = 111 (sprint-D, UNSAT 110 / SAT
111)".  The sprint-D log (data/e174_K36.log, 224 bytes) contains
only the coarse grid 60..130 step 10: UNSAT through 110, SAT from
120 — the fine step is in no pod or local record.  Adjudicated this
session with the independent e178 encoder: **UNSAT at 110, SAT at
111 — K(36,12) = 111 exactly** as claimed.  The number stands; the
cited provenance was incomplete.  (Margin conclusion unaffected
either way: the (v,3)@48 low-pure branch is dead with margin 108.)

## 3. Final pod harvest (all in-flight rows, end of day)

- **(none,0)@64 UNSAT [56.0s]** (sprint-D fresh_fix2) — NEW: fourth
  direct collapse cell; v_min(0) = ∞ now machine-DIRECT at
  M = 32/40/48/64 (m = 16/20/24/32 cores through the pump encoder);
  @96 still running (37 GB RSS — left to run).
- fmass(32) = 16 = M/2 landed in the sprint-C log (already §10-11 of
  notes/71); **fmass(40) ≥ 18** (UNSAT through m = 17, descending
  toward the predicted 20); fmass(36) descending on the same driver.
- ftot(16) ≥ 7 (m = 6 UNSAT [1187s]; heading to the predicted 8).
- v_min(0)(16): UNSAT through 48 [706.2s] (sprint-B), 96-query
  running; bracket stands at (48, 384].
- F(24;65)@86400 and margin (368,6)@32@86400: still running.
- Local (8; 11,0) deletion-MUS: crash-safe at n = 58, not harvested
  this session (the §7 pre-registration stands for the next).

## 4. Audit verdict

The five same-day fronts are SOUND at every point probed: every
reconstructed lemma re-derives, every fresh-scale machine check
lands on the predicted verdict, and the one imprecise provenance
resolves in the fronts' favor.  Combined with the 2026-08-28 referee
passes (notes/60/60-audit-1/61-audit-2) the verified layer of the
program has now survived two full adversarial cycles with zero
structural breaks.  The gap inventory is NOT empty — see notes/50
(final graph) and STATUS (bottom line): the NO-proof is NOT complete;
what remains is exactly the tagged pool there, dominated by
GAP-AFFORD′ (terminal, no proof strategy yet) + the N6a/N2
uniformization species + GAP-CMIN.
