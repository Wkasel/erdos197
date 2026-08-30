# Master assembly: the complete NO (skeleton, session 11)

Target: **Theorem (conditional assembly).** No partition of ℤ⁺ into two
sets has both parts 3-permutable — i.e. Erdős #197 = NO — modulo the
explicitly-tagged gaps below. This document is the dependency graph; each
node cites its proof or its gap tag.

## The dichotomy (N4, proven frame)
Fix a partition (A, B). For C ∈ {A, B} and window W_t = (M·8^t, M·8^{t+1}]
(disjoint tiling), classify:
- **Case 1** (some team, infinitely many 1-clean blocks): ∃ team T and
  infinitely many dyadic blocks where T's complement-within-block has size
  ≤ C₀ (bounded dust). [Anchor-free form per e121: ratio-2 windows, any
  anchor.]
- **Case 2** (everywhere-split): both teams' within-block presence → ∞.
Every partition is in exactly one case (frame: notes/43; anchor-free
restatement: notes/46 §4A).

## Case 1 kill chain
1. **C3(p) infinite hand family** [N2, notes from e122 session; status:
   diagonal lane machine-complete M=16..135 all residues, hand schema for
   5 pairs, 0 failures; GAP-N2: off-diagonal lanes (e124) + uniform hand
   proof of the family].
2. **Bounded-dust robustness** [N3 — RESHAPED (notes/74): the
   uniform-in-C form at fixed p is REFUTED (8 offset-stable
   transversal 3-escapes for {15,16} at every dyadic scale tested);
   the load-bearing form is N3-GROW: tolerance d*(x) grows along the
   diagonal (measured 2 / 3 / ≥ 4 at x = 11 / 15 / 27, exhaustive),
   and B1's extracted pair has p > 2^{m₀}/3 so a one-line patch to
   B1 Step 1 (choose m₀ with 2^{m₀} ≥ 3x₀(C₀)) restores the chain
   under (H1′) = N3-GROW + N2-DIAG.  GAP-N3-GROW: hand schema open;
   severed-ladder derivation closes odd/top punctures, open at
   even/b1/center (e130c part2)].
3. **T-PIN pigeonhole** [N1, proven]: fixed attacker pair at finite
   positions + infinitely many disjoint UNSAT windows ⟹ not permutable.
4. Assembly: **DONE (notes/52, Theorem B1) — AUDIT-CLEARED (60-audit
   §4, 60-audit-1 §1/§3; wording fixes 52-G1/52-G2 applied).**  The diagonal usable
   pairs {3p, 3p+1}, p ≡ 1 mod 4, fire on exactly the dyadic class and
   appear with density 1/12 in every block, so a C₀-clean block above
   scale 12C₀+25 always contains a fully-owned pair — the ownership
   branch holds unconditionally, the split branch is vacuous
   (SPLIT-QUANT: splitting punctures every block linearly, contradicting
   cleanliness), and the planned landing-pad descent provably has no
   well-ordering (notes/52 §4.3 — finite usable families admit a
   splitter fixed point; density is necessary).  Case-1 chain is now
   N1 + B1(patched, notes/74 §I.4) + (GAP-N2-DIAG, GAP-N3-GROW);
   GAP-BRIDGE1 discharged.

## Case 2 kill chain
1. **The coupled 2-seam core** [N6]: balanced 3-block gadget UNSAT at
   M=16/24/32; absolute-bound schema: (2,2,2) UNSAT at M=48, 64
   (e125: 304s), M=80/96 running (e126). [GAP-N6a: all-M schema (hand,
   from the MUS anatomy — notes/48 in progress).]
2. **Window composition** [trivial, verified]: windows (M·8^t, M·8^{t+1}]
   tile; constraints are window-local; T-PIN-style pigeonhole applies to
   the window family.
3. **Everywhere-split ⟹ (2,2,2) eventually**: by definition of Case 2,
   both teams eventually have ≥ 2 in every block of every window. ✓
   definitionally.
4. **Double non-procrastination** [GAP-G2 — THE gap]: the core's
   hypothesis that both teams are block-ordered at both seams, at
   infinitely many window scales. Candidate routes: (i) generalize
   lem:normal (running-max chunking) — any permutable team WLOG
   block-monotone up to finite fibers; (ii) v*(M) violation-budget +
   L-PROC procrastination accounting. notes/47 in progress.

## Support layer (proven)
- lem:orbit + T-SHARP sharpness (kills doubling-supercritical teams
  directly — iid-like colorings die here).  The L1' concentration lemma
  that was slated for the subcritical remainder is REFUTED (notes/74:
  ROT4 — rotating quarters — is balanced, subcritical in both teams for
  every finite reflector family [PROVED], and window-diffuse with sharp
  sup density 5/6); the subcritical remainder is handled by the ordinary
  Case-1/Case-2 dichotomy, which never needed L1'.
- d_t law, Lemma NECK, seam 7-channel law (octave/stage-alternating
  shapes — subsumed by Case 1 once GAP-BRIDGE1 lands, kept as independent
  confirmation).
- Price ledger: supply lemma + p(k) → ∞ [GAP-p(k): needs N2-style schema;
  possibly dispensable if Case 2 closes via the seam core alone].

## Current gap inventory (updated 2026-08-28, post-audit: notes/60
## night-2 referee + notes/60-audit-1 blind tests + notes/61-audit-2
## measurements folded in)
| Tag | Statement | Type | Status |
|-----|-----------|------|--------|
| GAP-N2 | off-diagonal lanes + uniform family proof | hand+machine | largely EXECUTED (notes/49: {11,12} all 8 residues, lane laws, template cells 13..19); remains: PARAMETRIC-in-x lane proof, cells A4d(19)/B6(21), pairs x ≡ 7 mod 8.  PRIORITY UPDATE (notes/52): the Case-1 critical path needs ONLY the diagonal parametric sub-piece **GAP-N2-DIAG** (C3(p) write-up, p ≡ 1 mod 4, dyadic scales — e123's verbatim-schema claim; fresh-p machine evidence now at p = 21 both dyadic scales + robustness, 60-audit-1 §3); off-diagonal parametrics matter only for BRIDGE1-AF |
| GAP-N3 | ~~dust-robust C3 (uniform in C at fixed p)~~ RESHAPED → **GAP-N3-GROW**: d*(x) → ∞ along the diagonal | hand + machine | uniform-C form REFUTED at p = 5 (notes/74 §I.2: the 8 transversal 3-escapes of {t11≺b2, t7≺b4, t3≺b6}, offset-stable at M = 80/96/128/144 — no m*(5, C ≥ 3) exists); growth form measured: d* = 2 / 3 / ≥ 4 at x = 11 / 15 / 27 with the p = 9 census EXHAUSTIVE (all ≤ 3-subsets of the 41-value support at M = 80, all 2-subsets at 112/144); B1 patched (notes/74 §I.4, one line — extracted p > 2^{m₀}/3 makes x₀(C₀) free); hand schema open — severed-ladder Lemma-D extension closes odd/top punctures at 3 scales, open at even/b1/center (e130c part2) |
| GAP-BRIDGE1 | ~~pair-ownership/split dichotomy in Case 1~~ **DISCHARGED + AUDIT-CLEARED** (notes/52 Theorem B1; refereed SOUND by 60-audit §4 and 60-audit-1 §1/§3 — line-by-line re-derivation + fresh adversarial colorings χA/χA′/χB incl. H1 robustness at fresh p = 21; the two §4.3 wording fixes 52-G1/52-G2 APPLIED to notes/52) — residual dependencies: GAP-N2-DIAG + GAP-N3-GROW (Step 1 patched per notes/74 §I.4 — the literal (H1) is refuted at small p, the extracted pair's p > 2^{m₀}/3 restores it as (H1′)); BRIDGE1-AF still open | hand | CLOSED modulo N2-DIAG/N3-GROW; audited |
| GAP-N6a | all-M coupled schema | hand (from MUS) | DECOMPOSED (notes/55 skeleton + notes/56 bridge + notes/59 low-gap closures; notes/57 DICH + notes/58 LLOP/PARM both refereed SOUND — 60-audit, 60-audit-1, 61-audit-2).  Proved layer: Lemma U, A1–A9, Seesaw/Z′/D′, E2/C, P′, W, PAR, FG-high, Theorem H, Cor. PAR-i, Lemma J (PROVED, independently re-established), fan-walk calculus + affine families, Lemma AO/D3, Lemma PH+, Theorem ASM′ + COV-W′ compositions, DICH case tree (H-DICH over F0–F4).  **Machine record**: DICH/L-LOP thresholds measured at all EIGHT scales 48..160 (step 16); mechanistic K* law exact at all 8 incl. 4 blind hits (K*(144) = 76, K*(160) = 83); flat cap law C(M) = (M+16)/2 − 4 exact at 96..160 (caps 51/59/67/75/83); (OV) W(M) = C − K* ≥ 0 at ALL EIGHT scales (W = 1 at 160 — the feared hole never materialized); full bridge chains verified at SIX scales (48/64/80/96 exact COV-W + **robust COV-W′ at 128 AND 160**, 61-audit-2 §4; 112/144 have thresholds but no P-arm run).  Sub-gaps remaining (unchanged in kind, shrunk in load): GAP-DICH (5 catalogue-schema rows, notes/57 §7), GAP-LLOP-α/β, GAP-PARM (⊇ GAP-PARM-CORNER ⊇ FG-deep 20-pair halving core), GAP-ASM′ = (OV-∀) only — now 8-scale-true with robust-chain insurance, GAP-FG-schema (RT-glue + deep block), GAP-FG-deep (L1/L2/L3 write-ups; cross-scale audit at 64 RUN, 61-audit-2 §5.3: resonance law CONFIRMED two-scale, but the E1×E1/non-resonant characterization of the stall set is 48-specific — at 64 twelve stalls spill to the E1 shoulder q ∈ [M−16, M−1] incl. resonant gaps 8/24, so the uniformization target must not bake in the 48 shape) |
| GAP-G2 | ~~double non-procrastination~~ REFRAMED: T-FORCE affordability — two Θ(M)-dense teams cannot both afford forced > v*(M) inversions at every anchor forever | hand (THE gap, ledger-type) | DNP as stated is FALSE (single-team, all budgets to N^{1−o(1)}, irreducibly two-sided — notes/47); FORMAL LEDGER THEOREM drafted (notes/54: demand side PROVEN modulo GAP-V*-schema/growth; supply side = GAP-AFFORD with proven mechanism lemmas; X-INTERLEAVE survives the accounting — e130 all-pass); pump brackets still wide: v*(bal,16) ∈ [3,6] (CP-SAT witness at 6), v*(bal,24) ∈ (4,65], v*(bal,32) ∈ (2,368], v*(pin,16) > 4 (fleet verdicts, 60-audit §5.0c) — too wide to confirm or refute growth.  **GAP-AFFORD session (2026-08-28, e158 + notes/62): GAP-JOINT measured YES — the 4-block downward gadget fires: (vup,vdn) = (6,0)@16 and (65,0)@24 UNSAT at componentwise-payable budgets (v*(bal,8) = v*(bal,12) = 0 measured; pure pump, attribution controls C1/C2 SAT); joint demand curve strictly above per-anchor floors at 2 scales [GAP-J-schema].  GAP-COMP refuted as counting (parity orientation, witness-realized); NG4 proved (budget rectangles are demand-only — L-AFFORD needs the donation currency); L-PREFIX proved (prefix-cohort tax; skip family Θ(M²), exact law 13M²/64+M/8); Lemma K + Theorem SCHED-DEAD proved (zero-sumset parity class dead at every budget, every M ≥ 12 — first complete arm of the (·,0) schema); (16;6,0)-MUS n = 50 FULLY critical (B2 = six-value stub).  Live sub-gaps: GAP-J-schema (2-scale staircase, machine-true 16/24), GAP-VMIN0 (v_min(0)(24) > 65; growth law open), GAP-AFFORD′ (overpayment ledger in donations — THE residual) |
| GAP-L1' | ~~concentration lemma~~ | — | **REFUTED, tag retired** (notes/74 Part II): ROT4 is everywhere-split + doubling-subcritical both teams for EVERY finite reflector family (hand proof, chains die at depth ≤ 2; machine max depth 1 with adversarial f ≤ 64 to 2^22) yet window-diffuse (every ratio-2 window misses ≥ a/16 − O(1) of each team by hand, sharp a/6 machine-exact to 2^16).  The notes/46 dodger corner (i)+(ii) is REALIZED; (iii) fails for ROT4 (Θ(M) gap-1 pairs — rotation is intervals); ROT4 itself dies at the coupled core (e131: ≥ 1 team UNSAT at each of M = 16/32/64, both at 32).  The ledger route's final step must point at the coupled core / T-FORCE instead |

Note the STRUCTURAL simplification bought by the MUS landing: if the
M=48 support confirms the anchor-coordinate match, GAP-N6a's schema is
the N2 schema family (GAP-N2) applied one seam up plus one layer of
sumset forcing — the program then has ONE schema engine (Z/D/E/P
ladders + rung geometry) and ONE genuinely new statement (GAP-G2's
ledger) left, with everything else short hand write-ups.

When every tag clears: Erdős #197 = NO. Any tag that BREAKS instead
re-opens a YES-shape with exact specifications.  One tag DID break
this session — GAP-G2's original DNP form (X-INTERLEAVE refutes it) —
and the re-opened specification is exactly the notes/46 dodger corner;
the reframed tag above is what must now clear instead.

### Night-shift delta (2026-08-27, notes/59)

Inside GAP-N6a, closed or reshaped this shift: GAP-J-pencil CLOSED
(Lemma J now fully PROVED — 36 pencil derivations, uniform 6-fact
schemas JP/JP′ = the FG-high geometry at run scale); GAP-FG-schema
recast as the PROVED fan-walk calculus (Lemma CC/FW + Theorem AFF;
new families Γ₂′, Γ₃; 1467/1851 of the dead fan grid covered at 48,
residual exactly the deep E1×E1 block + 105 mid pairs); GAP-FG-deep
mapped exactly at 48 (R(48): 90 escapes, resonance law 8 | gap
necessary; D(48): 75 deep kills, 55 with branch certificates, 20-pair
parity-locked core merges into GAP-PARM); GAP-ASM′ reduced to the
single inequality (OV-∀): K*(M) ≤ C(M) by Theorem ASM′ (notes/59 §D
— the F/L/P composition-soundness theorem, PROVED).  Corrected en
route: the notes/55 close-pair fan-kill hypothesis (distance ≤ 15)
needs the E1 exclusion — gap-8 escapes exist inside E1×E1.

### Audit delta (2026-08-28, notes/60 + notes/60-audit-1 + notes/61-audit-2)

Three referee passes over the four night-shift fronts (52/57/58/59);
**all four SOUND, zero broken theorems**.  Specifics folded into the
inventory above:

* BRIDGE1 (notes/52): cleared — line-by-line + fresh adversarial
  machine battery (greedy-puncture χA pushing extraction onto fresh
  p = 21 with kills at both dyadic scales + dust-on-core robustness;
  hi-half splitter χB); two §4.3 wording fixes (52-G1 cohort scoping,
  52-G2 fan-completion corner case) found and APPLIED.
* DICH (notes/57): cleared — the mechanistic K* law
  K* = m + 9 + max(α_E−f_O, α_O−f_E) is now exact at EIGHT scales
  with FOUR blind hits; the blind test at 160 was adversarial (law
  predicted 83 AGAINST both flat-law pre-registrations of 84) and the
  measurement sided with the mechanism.  The flat-offset K* law and
  the mod-32 law are both dead.  One prose correction: α is NOT
  monotone in M (α(160) = 2 < α(144) = 3).
* LLOP/PARM (notes/58): cleared minus its extrapolation prose — all
  measurements reproduce; caps measured at the two fresh scales
  (cap(144) = 75, cap(160) = 83, both = (M+16)/2 − 5, flat law's
  first out-of-sample wins); adjacency K* = cap+1 is dead as a law
  (W = 1 at 160) but (OV) holds at all 8 scales; robust chain
  REPRODUCED at 128 and EXTENDED to 160 — **Theorem COV-W′(160)**,
  the scale where the hole was predicted, now closed twice over.
* LOWGAPS (notes/59): cleared — J-pencil catalogue independently
  re-established (fresh closure engine); JP/JP′/Γ algebra re-solved
  by hand (two nits: FW rule-(i) guard bookkeeping; "16 residue
  patterns" should read 8); ASM′ composition sound.
* FG-deep cross-scale audit at 64 RUN (61-audit-2 §5.3): resonance
  law CONFIRMED (all escapes 8-divisible, gaps 16/32/48/64); zero
  close escapes; but the E1×E1/non-resonant stall characterization
  is 48-specific (12 E1-shoulder stalls at 64 incl. resonant gaps
  8/24) — audit-1's descriptive pre-registration refuted, notes/59's
  own tagging unharmed.
* Still-unrun items carried forward: e155c (ThW1′ puncture
  tolerance — the cap-law mechanism probe), e156 D3 at 80/112/128,
  P-arm instances at 112/144.

### Law-consistency delta (2026-08-28, notes/64 + e167)

Formula-only stress of every exact law against every other at
M = 2^k (k ≤ 40) and spots to 2^1000: **mutually consistent, zero
residue clashes in the M·8^t tiling to t = 1000** (all constraints
affine, thresholds ≤ 48, preserved by ×8; only t = 0 needs
M ≡ 0 mod 16, M ≥ 48).  Sharpened (OV-∀): for M ≥ 96 the laws give
W(M) = 3 − α_max(M) exactly — (OV-∀) ⇔ α_max ≤ 3 forever; W already
0 at 112/128/144, margin ONE alive value, and the half-scale cousin
of α already reaches 4 (e155b) — recommended target: α_max ≤ 4 via
H-LAT (caps the hole at width 1 = the d₀ = 4 robust chain's size),
α_max ≤ 3 restores (OV-∀).  Skip-mass law re-derived independently
+ extended (fresh scales 192/256; new B-form 13M²/64 − M/8); the v*
witness curve 6/65/368 fits ≈ 3M^6/2^23 (exponent 5.9–6.0) — NOT
the skip law's Θ(M²), curves cross at M ≈ 28, and flat lower
brackets (5/5/3) leave v*-growth undecided [GAP-V*].  Two prose
fixes: CORE′ P1 is CLOSED [3M−15, 4M] (notes/51's "(3M−15," is
off-by-one; |CORE′| = 4M+31 arbitrates); notes/57 §0.1 P2 parity
counts should read M+8/M+7, not m+8/m+7.

### Telescope delta (2026-08-29, notes/70 + e173)

Ledger-graph changes from FRONT TELESCOPE:

* **[GAP-V*-growth] DEMOTED from load-bearing** (Theorem D's demand
  no longer needs it): T-TEL′ + T-FRESH (notes/70 §4) run the
  regime-(I) demand side on the pump curve v_min(0)(M) instead —
  divergence of cumulative fresh demand follows from
  [GAP-J/F-schema] + [GAP-VMIN0-growth] alone, whether or not v*
  grows.  [GAP-V*] survives only as constant-sharpening.
* **New tags**: [GAP-F-schema] (freshness family F(N; v): pump with
  shared seam freed below, new-boundary currency banned; UNSAT at
  (16; 6), 983.5 s — refines GAP-J-schema); [GAP-VMIN0-growth]
  promoted to THE demand curve (measured: = 12 exactly at 8; > 6 /
  ≤ 384 at 16; > 65 at 24; > 256 at 32 — all deep-UNSAT-cheap).
* **Const-bounds pump machine-true**: (6,0)@24 at (2,3,6,12) UNSAT
  [106 s] — via D1+D2 the pump demand holds at every large Case-2
  anchor; GAP-J-schema should be proved at const bounds.
* **Proven infrastructure** (no tags): L-HOME, L-2PRICE, T-LEDGER
  (exact 4-adic disjoint bookkeeping; ×2 exact overlap on the full
  2-adic chain), L-SQUEEZE (no parking), L-ECHO (zero anchors book
  the forced giant payment at two anchors, same team),
  L-FRESH-DECOMP.  Naive consecutive-anchor disjointness REFUTED
  (maximal overlap measured on C1@16; overlap ≡ shared seam on
  10/10 records).
* **Unchanged terminal gap**: [GAP-AFFORD′] — supply cap in donation
  currency; the telescope proves it cannot be closed in pair
  currency (NG4 confirmed at chain level) and pins its two targets:
  echoing giant payments (branch a) or one-displaced-value-per-
  octave forever (branch b).

### Pump-schema delta (2026-08-30, notes/75 + e175)

The 4-block gadget's uniform law landed; ledger-graph changes:

* **[GAP-VMIN0-growth] DISCHARGED BY COLLAPSE** (Theorem J-DOWN,
  notes/75 §2.2–2.3): the lower window of U4(M) IS the coupled-core
  window at m = M/2 and vdn = 0 is its block-order hypothesis, so
  U4(M; v, w) is UNSAT for EVERY v whenever the anchor-m core fires
  at budget w (three-line L-PROJ restriction).  Hence
  **v_min(0)(M) = ∞ for all M ≥ 32** (bal machine at M = 32/48/64
  via e120 half-cores — new direct cell (none,0)@32 UNSAT 7.4 s;
  const (2,2,2) at M = 96/128/160 via e125/e126; uniform for
  M = 2m, m ≡ 0 mod 16, m ≥ 48 modulo GAP-N6a with the balance→
  band pigeonhole 16/15 proved).  The demand curve reverts to the
  budgeted half-core frontier v*₃(m; bounds) [GAP-V*, const form]
  plus the margin family below.  Queued pod cells (512,0)@32 and
  (512,0)@48 are MOOT.
* **[GAP-J-schema] RESCOPED**: the (·,0) family at large anchors is
  GAP-N6a verbatim (one schema engine — the intended collapse);
  the surviving content is the MARGIN family
  U4(2m; v, v*₃(m)+b) (all measured pump cells (6,0)@16 /
  (65,0)@24 are margin instances with v*₃(m) = 0; (368,6)@32
  unresolved) and the boot window M ≤ 24 (calibration only;
  v_min(0)(24) ∈ (65, 1440], finite).  The notes/62 §4c–4d
  three-arm (·,0) hand schema is demoted from load-bearing to
  boot-window documentation.
* **[GAP-F-schema] UNTOUCHED** (does not project: one-seam 3-block
  theories are SAT) — T-FRESH keeps genuine joint content; it is
  now the pump instrument's only load-bearing residual besides the
  margin family.
* **Proven infrastructure** (no tags): Lemma P-CAT (4-block pattern
  catalogue, 4 empty patterns; family laws |H_up| = 5M²/4,
  |H_dn| = 5M²/16, |SKIP| = 13M²/16), Lemma LEAK (the parametric
  '8': μ_dn = Σ_{z∈leak} c(z), verified on 5 witnesses), NEST
  correspondence + dictionary (notes/75 §2.1: H_dn = straddles(m),
  L-PREFIX(i) = Lemma-U(m) condition (S), vup charged on the
  S3 = 2×S2 wall — MUS stub ⊂ S3(16) machine-exact), band
  pigeonhole.  Independent cross-validation: CORE′(48) reproduced
  UNSAT through the 4-block encoder (C5, 39.2 s).

### Keystone delta (2026-08-30, notes/72 + notes/71 + notes/75)

Three same-day fronts merged; notes/72 §6 now holds THE composed
ledger statement (Theorem T-TEL″) with the complete link-status
table.  Tag movements:

* **[GAP-VMIN0-growth] DISCHARGED** — two independent routes:
  (a) notes/75 Theorem J-DOWN collapse: v_min(0)(M) = ∞ for M ≥ 32
  modulo GAP-N6a (machine to 160); (b) notes/71 two-case schema:
  ≥ M/2 for M ≥ 12 modulo [GAP-FHALF].  Finite regime exactly
  M ∈ {8, 16, 24} (12 exact / (6,384] / (65,1440]).
* **[GAP-J-schema] absorbed at large M**: the (·,0) family IS
  GAP-N6a via J-DOWN; residual tags [GAP-J-margin] (the
  (v, w ≥ v*₃(m)) rectangle — all measured pump content) and
  [GAP-F-schema] (freshness family; does not project; (16;6)
  UNSAT ×2 pods).
* **New [GAP-FHALF]** (from notes/71, instrumented in notes/72):
  f(M) ≥ M/2, orders-free counting; = M/2 exact at 8/12/16 by two
  independent instruments; proved pieces L-MID / L-SEESAW / L-HIT /
  L-RANGE (notes/72 §3-4); needed only for the finite-scale linear
  law independent of N6a — NOT on the critical path.
* **[GAP-G2/T-FORCE] demand half now a theorem modulo N6a closure**
  (T-TEL″): no zero anchors + ≥ 1 disjoint fresh pair per two
  octaves forever, no budget hypothesis; rate statements re-point
  at [GAP-V*].  **Critical path for Case 2 is now: N6a sub-gap
  closure + [GAP-AFFORD′]** (terminal, unchanged).
* e174 zero-variety: the sumset floor's zeros extend beyond the
  parity schedules (range-top composites) but all fall in the
  LOW-PURE order-dead arm — the two-case split is machine-exhaustive
  at 16..40.
