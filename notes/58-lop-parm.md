# 58 — GAP-LLOP + GAP-PARM: cap laws, hand-proof skeletons, and the robust P-ARM fix

Companion to notes/56 (the three-case bridge; §4b defines L-LOP and
P-ARM, §5.2 scopes the gaps, §5.3 ranks the attack) and notes/55 (the
proved layer: Lemma U, A1–A9, Seesaw/Z′/D′, E2/C, P′, W, PAR, FG-high,
Theorem H, Lemma J).  Everything tagged [PROVED] there is used freely.

**This note is written incrementally; every section ends with its
verification pointer and a status tag [PROVED] / [MACHINE-CHECKED] /
[GAP].**

**Overall status: `in progress`.**

## 0. Targets and plan of attack (2026-08-27 night shift)

The two single-instance hybrid lemmas of notes/56 §4b, machine-true at
M = 48/64/80/96, each need a uniform hand proof:

* **L-LOP(M)**: fan-clean + straddle-free + (2,2,2) bounds +
  min|Y| ≤ K − 1 ⟹ the band-major team's Th1 alone is inconsistent.
  Sharp caps (largest dead min|Y|): 29/36/44/51 at 48/64/80/96.
* **P-ARM(M)**: the Lemma-PH parity hatch (U_A = odds of P0,
  U_B = evens, Z_A = evens of P2, Z_B = odds) with FREE band (≥ 2 per
  team) ⟹ the six guarded block theories are jointly inconsistent.
  Machine fact: blocks {0,1} alone are SAT — Th2 is load-bearing.

Plan, in order (single solver query at a time; commit per section):

1. §1 [machine]: the exact L-LOP cap law.  Four data points suggest
       cap(M) = (M+16)/2 − ⌊M/32⌋ − 2   (min|Y| form),
   equivalently band-major kill size S(M) = (M+16)/2 + ⌊M/32⌋ + 3
   (note S = M+16 − cap).  Predictions: cap(112) = 59, cap(128) = 66,
   cap(160) = 81.  Probe at 112/128 (catalogue via e146, then single-K
   probes), accept/refute the law, and likewise pin K*(M) (predicted
   58/67 by the mod-32 law (M+16)/2 − 6/−5).
2. §2 [hand]: L-LOP mechanism decomposition — the defuse dichotomy
   (α-window / completion-zone / full-defuse) and the straddle-punch
   cascade that kills the full-defuse corner; identify which arms are
   H1-species (GAP-H1-hard) and which are new-provable.
3. §3 [hand]: P-ARM via classwise PAR halving: Th2(A)/Th2(B) halve to
   the H(m) fan theories on W2 with attacker sets = the halved
   same-parity band shares; the Theorem-H/FG-high dichotomy vs the
   near-aligned robust-H1 arm; make the residue condition exact
   (probe M = 56 ≡ 8 mod 16).
4. §4 [machine]: the robust P-ARM fix for the narrowing L/P overlap
   (notes/56 GAP-ASM′ warning: width 4/2/3/1 at 48..96, predicted
   hole {min|Y| = 82} at M = 160).  Design: replace Φ = 0 by
   "alignment up to ≤ d₀ Z-defectors" — justified by a quantitative
   Lemma PH (proved below: Φ < M+7 forces U-purity, and then
   Φ = (M/2)·#defectors exactly), so the machine pieces are
   DICH-U (U must be pure), DICH-Z (≤ d₀ defectors at min|Y| ≥ K_P),
   RP-ARM(M, d₀) (hatch with ≤ d₀ Z-defectors, free band ⟹ dead).
   Verify at M = 128 and 160 directly; fallback = overlap-width law +
   conditional fix.

Machine-facts bank from prior sessions used for the law fits:
L-LOP kmax_unsat(K-form) = 30/37/45/52, K* = 26/35/42/51 at
M = 48/64/80/96; DICH frontier Φ quantizes as (M/2)·(1..4) near K*
(e149 logs), e.g. Φ = 48·{1,3,4} at M = 96.

[Status: plan — commits follow per section.]
