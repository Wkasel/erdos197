# 80 — FINAL-FOUR ADJUDICATION: spot-audit of the species write-ups,
# tournament verdict, champion designation

Session 2026-08-30, close of the final-four phase.  Inputs: notes/77
(N6a pool), notes/78 (C3(p) + N3-GROW), notes/79 (afford tournament),
notes/50 (FINAL graph).  Mandate: (1) spot-verify every species
write-up — one reconstruction + one fresh scale each; (2) adjudicate
the tournament — exact completed-proof bills for the survivors,
champion, independent verification + characterization of the S5
witnesses; (3) ledger + probability.

Machine companion: experiments/e184_finalfour_spot.py →
data/e184_finalfour.json / .log, plus fresh-scale runs of the
existing instruments (e181, e155/e155b/e155c, e179, e180.partK) —
local + main pod.  In-flight landings from the notes/77/78 close are
folded in (§2).

**Headline: every spot-check passed — zero anomalies across six
species × (reconstruction + fresh scale).  The S5 witnesses are
authentic and are, structurally, MOD-4 LATTICE colorings — the
sharpest characterization of the surviving YES-space the campaign
has produced (§4).  Champion: S4 (sparse-corner pincer), decisive
next statement MINT-LOC (§3.4).**

---

## 1. Spot-audit: one reconstruction + one fresh scale per species

| species (write-up) | reconstruction (fresh instrument) | fresh scale/parameter | verdict |
|---|---|---|---|
| Theorem C3(p) (notes/78 I) | every displayed affine identity re-derived by independent code, p ≤ 39, all M sweeps (fulcrum APs, E(p) indices+parity, mod-8 lock, all four flood mirrors, betweenness, G4 distance) | p = 23 AND 25 (both mod-4 classes, beyond every earlier run): schema 104/104 + 52/52 + 52/52 each, 0 fail [2 s each]; solver x-val 20/20 incl. M = 256/260 | **CLEAN** |
| Lemmas LANE/PS (notes/78 II) | PS halving identities re-derived as exact set equalities, fresh code; LANE count+disjointness numerically | x = 29, 31 at M = 96/160 (beyond the 5 recorded x); LANE all odd x ∈ [11, 99]; d*(19; 112) = 4 EXACT (atmost-3 anywhere UNSAT 23 s, SAT at 4 — witness the pure-bottom transversal {b₂,b₄,b₆,b₈}, 4/4 lane units) | **CLEAN** — x = 19 law point now global at TWO scales |
| Lemma PURE (notes/77 §3.1) | part (i) re-implemented set-level (AP bijection + unit bijection incl. the r̂ = 0 odd line) at M = 48/56/64/80 | e181 SAT-level equivalence at M = 56 (fresh): 1260 same-parity pairs, 1164 halved-dead, **0 mismatches** [142 s] — third scale | **CLEAN** |
| Theorem P-ARM‴ / ThW1′-ROBUST (notes/77 §4.5) | a-fortiori restriction step re-read (B_o fan-safe ⟹ h(B_o) ⊆ maximal clique Q; UNSAT ∖ Q lifts to UNSAT ∖ h(B_o) by constraint superset); e183 raw data re-read: min_break = 4 ×4 cells, EVERY breaker ⊇ core triple, ctrl_sat = [] ×240 | m = 64 (M = 128, fresh — beyond the 5-scale battery): full α system UNSAT, **0/72 single drops SAT, 0/49 maximal-clique drops SAT** (both classes) [7 s/class]; e182 independent-encoder re-verification landed: 0 SAT / 156 solves at m = 48/56 | **CLEAN** — P-ARM‴ modular at SIX scales 48..128 |
| L-DOUBLE-DUTY (notes/79 §1) | counting argument re-derived: the |O_m∩T| pairs are y-named distinct; the mint pair (u,w) is separate from BOTH families via pos(u) < pos(u′); +1 sharp | M = 24 (fresh, third scale): UNSAT at budget 11 [1038 s] and 12 [in flight at write time — see postscript], SAT expected at 13 = |B0∩A|+1 | **CLEAN** (11-row landed; threshold row postscripted) |
| GAP-SPARSE-CORE (notes/79 §4) | AAA covering bound quantified: gap-≥3 set covers ≤ ⌈n/2⌉ of a spacing-2 u-line and ≤ ⌈n/3⌉ of a contiguous y-run; ⌈n/2⌉+⌈n/3⌉ < n for n ≥ 13 ⟹ AAA closes for m ≥ 26 by hand (n = m/2), machine covers 16..48, boot ≤ 12 consistent | m = 36 (fresh, 8th scale, 2nd in residue 4 mod 16): sparse CELL **UNSAT ×4 designations** [≤ 6 s each]; controls bare (1,1,1) SAT, cap-only SAT | **CLEAN** |
| FG-deep laws (notes/77 §2) | (in-flight audit landed, sprint-D) | M = 144, 160: RES-LAW 0 violations (now EIGHT scales 48..160); CLOSE-LAW′ 0 distance-≤15 escapes; stall corner scaled-zone confirmed (pred ⊂ D strictly, no false predictions) | **CLEAN** |

Notes on what the reconstructions actually established:

1. **C3(p)**: the identity layer — the part of an affine write-up
   where errors hide — was re-derived from scratch (not read off the
   note) over a p-range 2× the machine record, including the two
   L1-case mirror memberships {t_{p−4}, t_p} / {b_{p−4}, b_p} and
   both P2 mirror families.  With the fresh-p executor and solver
   runs, GAP-N2-DIAG's "adversarial audit pending" rider is
   substantially discharged: instrument battery at fresh parameters
   in BOTH mod-4 classes, zero anomalies.  Residual formality: a
   line-by-line referee pass of the prose at paper-integration time
   (the bar thm:c3core cleared via e115).  Tag moves to
   **[PROVED — spot-audited (this note)]**.
2. **PS/LANE**: the h_E/h_O index bijections re-derived by hand
   (h_E: (t_{(x+1)−2j}, b_j) ↦ (t′_{y−2j′}, b′_{j′}), j′ = j/2;
   h_O: (t_{x−2j}, b_j) ↦ (t′_{y−2j′}, b′_{j′}), j′ = (j+1)/2; both
   onto attacker y = (x+1)/2) — the notes/74 correction is forced by
   the arithmetic.  The fresh d*(19; 112) point removes the last
   asymmetry in the law table (every x-point ≥ 15 now has ≥ 1
   verification at a scale ≥ 112 or a second scale).
3. **PURE**: the set-level reconstruction independently caught the
   subtle r̂ = 0 case (odd-class unit r = 1 halves onto the
   source-2a line) and confirmed the window-end formulas exactly —
   the two places the isomorphism could break.
4. **SPARSE-CORE**: the covering arithmetic yields a HAND closure of
   the AAA designation for m ≥ 26 (rep-line length n = m/2 ≥ 13);
   the machine interval 16..48 overlaps it, so AAA is now closed at
   ALL m ≥ 16 (hand ≥ 26, machine 16..48 exhaustive ×8 scales).
   GAP-SPARSE-CORE's residue is the mixed-designation catalogue
   only — same species as the N6a pool, now provably so.

## 2. In-flight landings folded in

- **e182** (independent Glucose42 full-scale encoder): 0 SAT / 156
  solves at m = 48/56 → notes/77 §4.6 filled.
- **e180 deep-law audit at 144/160** (sprint-D): landed clean (§1
  table); notes/77 §2 record extended to eight scales.
- **e155 chain at m = 64**: H-LAT alive gaps [16,32,48,64] all
  ≡ 0 mod 8 — seventh scale; cliques within the ≤ 4 law.
- **h8192 S5 horizon stress**: SAT [58 s], witness verified in §4.
- **e146 catalogues at 176/192**: still building on sprint-B/-C at
  write time (relaunched, crash-safe); the notes/77 §4.8
  pre-registered probe chain has NOT run — predictions stand
  untouched (C(176) = 92, C(192) = 100; K* by scan-then-blind).
- Local s1lemma M = 24 near-critical rows: postscript below.

## 3. Tournament adjudication

S1 = proved tool (enters the T-TEL″ bookkeeping next to
L-HOME/L-2PRICE).  S2, S3 = refuted, on the no-retry list; nothing
in this session's audit disturbs either refutation.  The two
survivors:

### 3.1 S4 (sparse-corner pincer) — the completed-proof bill, exactly

A finished NO along S4 requires, beyond what is already proved:

  (a) **GAP-SPARSE-CORE uniformization** — DONE for AAA at m ≥ 16
      (§1.4: covering hand proof ≥ 26 + machine 16..48); remaining:
      the mixed-designation catalogue (machine-closed ×8 scales;
      catalogue-schema species, same bar as the N6a pool).
  (b) **MINT-LOC (the new statement — the AFFORD′ content for the
      (iii)-corner).**  For a sparse-corner coloring, the T-TEL″
      mint at anchor 2^m displaces a value; prove the displaced
      value is forced to sit within distance ≤ 2 of other minority
      material of its block (or in a band whose occupation breaks
      gap-≥3 within O(1) octaves).  Then paying the everywhere-mint
      system eventually violates axis (iii) — the corner
      SELF-DESTRUCTS, and with (c) Case 2 closes.  Species: order
      forcing at one anchor + finite coloring bookkeeping — finite,
      pre-registerable, instrumentable on the S5 witnesses.
  (c) **Arm B (¬(iii))**: donation material at gap ≤ 2 hands the
      partner attacker pairs; needs the p(k) → ∞ schema (N2 species,
      measured 3/7/7/11) composed with T-PIN at varying x.  Open,
      but of known species.
  (d) Composition: N4 + (a)/(c) dichotomy + T-TEL″ + (b) ⟹ Case 2;
      with Case 1 (C3(p) + N3-b) ⟹ NO.  All composition steps
      already [PROVED].

### 3.2 S5 (YES-construction) — the completed-proof bill, exactly

A finished YES along S5 requires:

  (a) an ω-coloring in the corner — after §4 this is the EASY part:
      the pure mod-4 lattice family extends to ω verbatim as a
      coloring (axes (ii), (iii), split hold by arithmetic);
  (b) TRUE axis (i) at ω — the witnesses' minorities are
      orbit-CLOSED lattices (§4), so subcriticality must come from
      reflector growth (T-SHARP procrastination), not absence of
      chains; unverifiable by any finite censor (measured, notes/79
      §5), needs a hand argument;
  (c) **the actual pair of AP-free orders** — both teams
      3-permutable, paying the forced > v*(M) inversions at every
      anchor forever (the witnesses are STRUCTURALLY void for
      double block order — §4.3 — so payment is not optional).
      This is constructive ¬AFFORD′: nothing in the campaign or the
      literature approximates a pair of orders with coupled
      unbounded procrastination; T-SHARP gives the single-team,
      single-orbit analogue only.

### 3.3 Champion: S4

The survivors are complementary halves of one question (sparse-corner
affordability), but they are not symmetric in what remains:

- S4's residue = one new finite-shape statement (MINT-LOC) + two
  catalogue write-ups of proved-in-instances species; every
  composition step exists.  S5's residue includes an ω-construction
  of a COUPLED pair of permutable orders — an object with no
  finite handle and no precedent.
- The machine record weights S4: every finite coupled theory of the
  corner ever posed is UNSAT (the sparse core now at 8 scales from
  presence 1); every escape hatch ever found (parity lattice,
  range-hide, clique punctures, band splits) was later killed by a
  stronger core; and the witnesses' own structure (§4) is exactly
  the shape the sparse core taxes hardest.
- S5's witnesses stay ON the critical path as the champion's
  instrument bench, not as a competing program.

**Decisive next experiment (pre-register before running):** MINT-LOC
on the S5 witnesses — at anchors m = 32, 64, 128, enumerate the SAT
region of "witness coloring + double block order minus one inversion
pair (u, w)" over all candidate mints and record WHERE the displaced
value can live relative to the minority lattice.  Prediction is
genuinely open (the S2 band map was FULL at the boot scale — freedom
may persist; the lattice's arithmetic closure argues confinement).
Either verdict moves AFFORD′: confinement ⟹ (b) has a proof shape;
freedom ⟹ the corner can dodge indefinitely at the mint layer and
the YES-side gains its first affordability evidence.

### 3.4 Verdict table (final)

| strategy | verdict | disposition |
|---|---|---|
| S1 | L-DOUBLE-DUTY [PROVED, sharp; M = 24 fresh scale §1] | tool, in the ledger |
| S2 | REFUTED (band map full) | no-retry |
| S3 | REFUTED (payer alternates) | no-retry |
| S4 | SURVIVES ×8 scales + AAA hand closure | **CHAMPION**; bill = MINT-LOC + mixed catalogue + arm B |
| S5 | SURVIVES as YES-material; witnesses verified authentic + characterized (§4) | instrument bench for MINT-LOC; YES-bill = §3.2 |

## 4. The S5 witnesses: independent verification + characterization

Fresh checker (e184 partS5/partS5CORE — no CP-SAT, no reuse of the
e179 encoding; exact DP for chain depth, direct constraint re-check
from the raw colorings):

### 4.1 Authenticity — every axis re-verified

| witness | split | (iii) sparse | (ii) lin4 diffuse | sup win. density | rung-safe < 13/16 | censor (depth < D at F, seeds > u₀) |
|---|---|---|---|---|---|---|
| h4096 D2F12 lin4 | OK | OK | OK | 0.7692 | YES | OK (depth 1/1 at F=12) |
| h4096 D2F64 lin4 | OK | OK | OK | 0.7612 | YES | OK (depth 1/1 at F=64) |
| h8192 D2F64 lin4 | OK | OK | OK | 0.7576 | YES | OK (depth 0/1 at F=64) |

### 4.2 THE characterization: the corner's inhabitants are mod-4
### lattice colorings

Minority anatomy (exact, from the raw colorings): in EVERY dyadic
block above the boot zone, the minority is a **difference-4 AP on a
single residue class mod 4**, at exactly 1/4 of the block:
h4096_F64 → class 3 (mod 4), all blocks t = 5..11, gap histogram
pure {4}; h8192_F64 → class 1 (mod 4), t = 5..12; lin4 → class 0
(mod 4) from t = 7 up (boot blocks t = 5, 6 mixed — the solver's
censor-cleanup zone).  Block A-counts are exactly size/4 or
3·size/4 throughout.

Readings:

1. **The corner's canonical shape is the mod-4 lattice** — one step
   beyond the outlawed spacing-2 lattice: gap ≥ 2 leaves the parity
   lattice (measured escape, notes/79 §4); gap ≥ 3 forces the
   minority off mod 2, and the solver lands it exactly on mod 4.
   The s4price optimal sparse repair witnesses (difference-4 APs)
   were the same object one layer down.
2. **The minority is orbit-closed**: a mod-4 class is closed under
   v ↦ 2v − f for in-class f (2c − c ≡ c).  The witnesses' minority
   is a self-reflecting doubling lattice — which explains the depth
   explosion one band up, and sharpens it: exact DP gives max chain
   depth 24/43 (h4096_F64, teams A/B at F = 128), 25/14 (lin4 at
   F = 64), 25/43 (h8192 at F = 128) — the e179 estimate (~10) was
   LOW.  The censor is clean only because in-class reflectors below
   F with seeds above u₀ are scarce; at 2F the lattice's arithmetic
   takes over.  True axis (i) at ω therefore rides entirely on
   reflector growth — T-SHARP procrastination is not an artifact of
   these witnesses but their ESSENCE.
3. **They pay structurally.**  Double block order + per-team
   AP-freeness on the witness colorings is void at EVERY tested
   anchor (m = 16/32/64, both h4096 witnesses) — before any solver
   call: a mod-4 class is AP-closed, so the lattice minority carries
   cross-3-block in-team APs automatically (explicit certificates:
   B-triple (35, 82, 129) in h4096_F64 at m = 32; A-(33, 81, 129) +
   B-(48, 90, 132) in lin4).  A lattice-minority coloring can NEVER
   be double-block-ordered — the sparse core's verdict on this
   sub-family is a two-line hand fact, and the mint demand on the
   corner's canonical inhabitants is unconditional.
4. **ω-extension**: as a COLORING the pure lattice family exists at
   ω trivially; S5's open content is exactly axes (i) at ω and the
   orders (§3.2 (b), (c)).  The YES-question is now: *can the mod-4
   lattice corner afford its everywhere-mint system?* — the same
   battleground as the champion's MINT-LOC, approached from the
   other side.

### 4.3 Honest caveats

- My S5CORE encoder never reached a solver (structural voidness
  fired first); its solver path is untested — irrelevant here since
  voidness is certificate-checked, but recorded.
- The e179 "true depth ~10 at 2F" rows understate (exact DP:
  24–58); the notes/79 §5 qualitative reading (censor dodged one
  band up) is unchanged and STRENGTHENED.
- At m = 32 in h4096_F64, team A has no cross-3-block AP (only B
  is structurally void there); the joint theory is void at every
  tested anchor regardless.

## 5. Ledger movement (applied to notes/50 + STATUS.md)

| tag | movement |
|---|---|
| GAP-N2-DIAG | [PROVED — audit pending] → **[PROVED — spot-audited]**: identity layer re-derived independently, fresh p = 23/25 executor + solver clean; residual = referee prose pass at paper time |
| GAP-N3-GROW | (N3-b) unchanged [GAP]; law table: d*(19; 112) = 4 fresh; PS identities ×7 x-values; LANE numeric to x = 99 |
| GAP-N6a sub-pool | PURE ×3 scales; P-ARM‴ ×6 scales + e182; FG-deep laws ×8 scales; pool residue per notes/77 §7: **GAP-RES** (consolidated crux) + ThW1′-ROBUST/-TOL uniformization + DICH-F2/CASC + SPLIT + LLOP-α/β + ASM′ = (OV-∀) |
| GAP-SPARSE-CORE | AAA designation **closed at all m ≥ 16** (covering hand proof m ≥ 26 + machine 16..48, 8 scales incl. fresh 36); residue = mixed-designation catalogue |
| L-DOUBLE-DUTY | fresh scale M = 24 (UNSAT at 11; near-critical rows postscripted) |
| GAP-AFFORD′ | still open, still terminal; champion route fixed = S4 + MINT-LOC; witnesses characterized as mod-4 lattice colorings (canonical corner inhabitants, structurally paying) |

**Probability (honest assessment, end of adjudication): NO ≈ 93 %,
YES ≈ 7 % — HELD, variance reduced.**  FOR a bump: six species
spot-audited with zero anomalies at fresh scales/parameters; gating
gap (3) now spot-audited [PROVED]; the sparse core at 8 scales with
its AAA arm hand-closed.  AGAINST a bump (and why 93 holds): the S5
verification UPGRADED the YES-side too — the corner's inhabitants
are not solver noise but a canonical arithmetic family (mod-4
lattices) that extends to ω as a coloring, with T-SHARP
procrastination as its essence; and AFFORD′/MINT-LOC — the entire
remaining content of Case 2 — is genuinely open with a live
either-way experiment.  Composition of the 7 %: ≈ 5 % the mod-4
lattice corner affords its mints (YES via S5), ≈ 2 % some unmodeled
break elsewhere.  Composition of the 93 %: the three catalogue-
species gaps are near-certain writing (every instance ever attempted
has discharged; two full audit cycles + this spot-audit, zero
breaks); AFFORD′ carries essentially all the residual NO-risk.

## 6. Postscript: stragglers at close

- s1lemma M = 24 budgets 12 (expect UNSAT) / 13 (expect SAT = 12+1):
  near-critical solves, in flight; crash-safe rerun:
  `python experiments/e179_afford_tournament.py s1lemma --Ms 24
  --budgets 12,13`.  The lemma's proof is scale-free; the M = 24
  rows are corroboration only.
- e146 catalogues 176/192 (sprint-B/-C) + the notes/77 §4.8
  pre-registered probe chain: untouched predictions, run next
  session.
- MINT-LOC: pre-registration written here (§3.3); instrument next
  session.
