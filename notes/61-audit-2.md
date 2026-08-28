# 61-audit-2 — Referee audit of notes/58 (LLOP/PARM) and notes/59 (lowgaps), post-K*(160)

Third referee pass (2026-08-28), scoped to notes/58-lop-parm.md and
notes/59-lowgaps.md, taking as INPUT the notes/60-audit-1 verdicts
(notes/52 SOUND + 2 wording fixes; notes/57 SOUND; blind measurements
K*(144) = 76, K*(160) = 83 — the notes/58 flat-offset K* law FALSIFIED
at 160 in favor of the notes/57 mechanistic law).  Mandate: reconcile
notes/58's cap-law claims with the corrected law; determine which of
its L-LOP / P-ARM results survive; verify the robust-chain-at-128
claim; spot-check one L-LOP cap and one P-ARM instance at scales the
author never ran; referee notes/59's FG-schema, J-pencil, and ASM′ as
logic.  Solver runs are appended to the authors' own logs
(data/e152_llop_probes.log, e154_rparm.log, e153_dich_probes.log);
one solver at a time throughout.

Division of labor with the two prior audits (no duplication): notes/60
(night-2) already hand-reconstructed D3/AO/PH+/PARM-HALVE/COV-W′
(§2) and CC/FW/AFF/JP/JP′/ASM′ (§3) with an independent closure
engine reproducing the full J-pencil catalogue; notes/60-audit-1
measured K* at 144/160 blind.  This pass adds: the cap measurements
at 144/160 (never run by anyone), the RP-ARM reproduction + fresh
scale, the COV-W′(160) chain, my own line-level re-derivations of the
notes/59 §A/§B algebra, and the reconciliation verdict.

---

## 1. Reconciliation: what K*(160) = 83 does and does not kill in notes/58

notes/58 §1.1 proposed TWO flat-offset extrapolations from the
96..128 data: cap(M) = (M+16)/2 − 5 and K*(M) = (M+16)/2 − 4, plus
the observation K* = cap + 1 ("exact adjacency") at 112/128, and §6
pre-registered C(160) = 84 (cap 83), K*(160) = 84.

* The K* half is DEAD (audit-1): K*(160) = 83 = the notes/57
  mechanistic prediction (α drops to 2 at 160).  notes/58's
  §6 pre-registration loses.
* The cap half was UNMEASURED.  §2 below measures it: cap(160) = 83
  — the flat cap law's prediction is CORRECT at 160 (and at 144).
* Consequently the ADJACENCY reading (K* = cap + 1 always) is also
  dead: at 144 it holds (76 = 75+1); at 160 it FAILS in the good
  direction (K* = 83 = cap, overlap width W = C − K* = 84 − 83 = 1).
  The two laws are now seen to be different animals: the cap follows
  a flat offset (a Th1-side supply constant — consistent with the
  §1.1/§5.1 reading that the cap is the ThW1′ E1-midpoint puncture
  tolerance, which has no α in it), while K* follows the catalogue
  quantities α, f and is NOT monotone (α: 2,3,2,2,3,3,3,2 at
  48..160).  A side casualty in notes/57 §0.2: the phrase "both
  monotone-in-M trends" is falsified by α(160) = 2 — the resonance
  lattice does not widen monotonically.  Harmless to every theorem
  (the formula never assumed monotonicity), but the extrapolation
  prose should not be trusted; only the per-scale scans matter.
* What this means for (OV-∀) = GAP-ASM′ (notes/59 §D): measured
  W(M) = C − K* = 4, 2, 3, 1, 0, 0, 0, 1 at M = 48..160.  (OV) has
  now held at EIGHT consecutive scales, and the first genuinely
  adversarial scale (α-drop at 160) moved the margin AWAY from the
  hole.  The danger direction for (OV) is α GROWING while the cap
  stays flat; no measured scale shows W < 0.  (OV-∀) remains open
  as arithmetic, but with the robust chain (§4) verified at 128 AND
  160 the assembly no longer rides on it.

**Survival table for notes/58's claims** (referee verdict per item):

| claim | status |
|---|---|
| measured caps 29/36/44/51/59/67 at 48..128 (§1, §1.1) | SURVIVE (measurements; logs re-read, §2 extends the series) |
| measured K* 60/68 at 112/128 (§1, §1.1) | SURVIVE (confirmed independently by notes/57 blind formula + audit-1's instrument at 96 anchor) |
| ⌊M/32⌋ cap law (§1) | already declared dead at 128 by the note itself |
| flat cap law cap = (M+16)/2 − 5, M ≥ 96 (§1.1 candidate) | SURVIVES its first two out-of-sample tests (75@144, 83@160 — §2) |
| flat K* law (M+16)/2 − 4 (§1.1 candidate) | DEAD at 160 (audit-1; mechanistic law wins) |
| exact adjacency K* = cap+1 (§1.1) | DEAD as a law (fails at 160, W = 1); survives as per-scale fact at 112/128/144 |
| §6 pre-registration C(160) = 84 | CORRECT (§2) |
| §6 pre-registration K*(160) = 84 | WRONG (audit-1: 83) |
| Lemma AO, Lemma D3 (§2) | SOUND — re-derived line-by-line here; already brute-audited at 48/144 by notes/60 §2; e156 controls behave |
| PARM-HALVE / P-ARM″ / lattice law / {4,6}-droppable / clique ≤ 4 (§3) | SURVIVE as tagged (machine facts + conditional theorem; notes/60 §2 re-derived the bookkeeping; not re-audited here beyond log cross-reads) |
| Lemma PH+ / COV-W′ composition (§4.1–4.2) | SOUND (notes/60 §2 re-derivation; composition logic re-checked here — see §4) |
| robust chain at 128 (§4.4) | REPRODUCED (§3) |

## 2. The cap measurements at 144 and 160  [MACHINE — fresh scales]

e152_llop_probe (author's instrument, author's catalogue files; the
144/160 catalogues were built by audit-1's recovery run,
data/e157_audit_catalogue_144_160.log):

    L-LOP(144): K = 76 UNSAT [9.4 s];  K = 77 SAT
                → cap(144) = 75, C(144) = 76
    L-LOP(160): K = 84 UNSAT [17.7 s]; K = 85 SAT
                → cap(160) = 83, C(160) = 84

Both flat-cap predictions hit.  Combined table (min|Y| forms,
offsets from balance (M+16)/2):

    M      48   64   80   96   112  128  144  160
    cap    29   36   44   51   59   67   75   83     offs −3 −4 −4 −5 −5 −5 −5 −5
    K*     26   35   42   51   60   68   76   83     offs −6 −5 −6 −5 −4 −4 −4 −5
    W       4    2    3    1    0    0    0    1

Frontier anatomy: the K = 85 witness at 160 is the SAME species as
the 128 one — Y_A = one full parity class of the band (odd, 80
values) + FOUR opposite-parity defectors in the E1 region (depths
164/168/170/172); U_B ⊇ the α-window, Z_B ⊇ the completion zone.
The cap's "+4 = E1-midpoint puncture tolerance" reading (§1.1/§5.1)
survives at the new scale; the pre-registered e155c experiment that
would pin it (ThW1′ puncture tolerance) has still never been run —
carried as an open item.

[MACHINE-CHECK: data/e152_llop_probes.log (M=144/160 blocks appended
this audit).]

## 3. The robust P-ARM chain at 128: claim verified

* Log cross-read: data/e154_rparm.log and e153_dich_probes.log match
  notes/58 §4.4 verbatim (RP-ARM(128,4) UNSAT 10.0 s, 15.4M clauses;
  DICH-upure(128,68) UNSAT 0.9 s; DICH-zdef(128,68,4) UNSAT 0.2 s;
  RP-ARM(48, d₀ = 0/2/4/8) all UNSAT with the d₀ = 0 e150 audit).
* Encoding read against the §4.2 spec: the e154_robust_parm.py build
  implements exactly the declared instance (U pinned by parity; P2
  free with ≤ d₀ defector budget; band free ≥ 2 per team; straddles
  both teams; six guarded block theories incl. the (0,2,2) units that
  are vacuous at d₀ = 0 but live for defectors).  The --audit mode's
  blocks-{0,1} SAT control is the right guard against a
  trivially-UNSAT encoding bug.
* RE-RUN, fresh process: RP-ARM(128, 4) --audit → blocks (0,1) SAT
  [1.5 s], full UNSAT [9.0 s].  Claim REPRODUCED.

## 4. COV-W′ at a scale the author never ran: the 160 chain closes

Fresh-scale P-ARM spot-check + the full robust assembly at 160, with
K_P = cap(160) + 1 = 84, d₀ = 4:

    L-LOP(160):          min|Y| ≤ 83 dead        (§2, K = 84 UNSAT)
    DICH-upure(160, 84): UNSAT  0.6 s            (U forced pure)
    DICH-zdef(160, 84, 4): UNSAT  0.2 s          (≤ 4 defectors forced)
    RP-ARM(160, 4):      UNSAT 25.0 s  (29.0M clauses; blocks {0,1}
                         SAT control passed)

⟹ **Theorem COV-W′(160) holds**: every straddle-free
(2,2,2)-bounded coloring of CORE′(160) dies through fan / L-LOP /
robust-P.  This is the second scale (after 128) where the bridge is
verified WITHOUT the adjacency accident, and it is exactly the scale
where notes/56 §4b predicted the hole ({min|Y| = 82} was the feared
gap value; in fact 82 is L-dead and 84 is P-dead with W = 1 slack,
covered twice over).  The notes/58 §4 designated fix is confirmed
working at the scale it was designed for.  Full bridge chains are
now verified at SIX scales (48/64/80/96 exact COV-W + 128/160
robust COV-W′); 112 and 144 have both thresholds measured but no
P-arm instance run — cheap to close if wanted, not load-bearing.

Composition logic re-checked while at it (COV-W′ and ASM′ share it):
the three machine instances quantify over supersets of the
swap-normalized coloring; every constraint family is swap-invariant;
PH+ needs |U_T| ≥ 1 both teams (bounds) and φ₀ = (M/2)·d₀ < M+7
fails for d₀ ≥ 2 — NOTE the correct reading (already implicit in
§4.2 but worth pinning): DICH-Z's UNSAT at (K_P, d₀) is what bounds
the defector count by d₀, and Lemma PH+ is invoked with the DICH-U
verdict to pin U-purity; the chain does not need Φ ≤ φ₀ < M+7 as a
hypothesis anywhere.  Sound.

[MACHINE-CHECK: data/e154_rparm.log, e153_dich_probes.log (160
blocks appended this audit).]

## 5. notes/59 refereed

### 5.1 §A FG-schema (Lemma CC / FW / Theorem AFF / Γ families)  [SOUND]

Line-level re-derivations, independent of the notes/60 §3 pass:

* Lemma CC: RL/RT are exactly the R2/R4 resp. R1/R3 midpoint rules
  applied to the integer APs (v, u, 2u−v) / (u, v, 2v−u); window and
  ≠-guards present; T is order transitivity.  Sound.
* Lemma FW: rules (i)–(iii) re-derived as unit+RL+T compositions.
  One presentational nit (not an error): rule (i)'s guard "2h−x ≤ N"
  suffices because 2h−x = 2y+r ≥ 2 gives the lower window bound for
  free, but the RL side-condition 2h−x ≠ h needs x ≠ h, which holds
  since h is removed from D(h) — worth one clause in a final
  write-up.
* Theorem AFF: each rule is affine with one integrality/positivity/
  window side-condition; cycle closure is linear; M enters only via
  N.  Sound as stated.
* Γ₁: m₁ = 2p−3q, m₂ = 3p−4q, m₃ = 5p−6q from s = p−2q re-computed;
  RL steps 2m₁−s = m₂, 2m₂−s = m₃ check; closing p-unit
  m₃ = 2m₁+p checks.  Γ₂′: the whole chain re-computed symbolically
  (m₁ = 2(2a+q)+q, m₂ = 2m₁−a = 2a+p, m₃ = 2m₂−a = 2m₁+p) — exact;
  window 13a+12q ≤ N is the only size condition; at q = 0 it is
  e142n.  Γ₃: the D-unit derivation and the linear solution
  (a = −2r₁+3r₁′+2r₂−4r₂′, a′ = (4a+2r₁−2r₂+r₂′)/3) re-solved by
  hand — both match.  All SOUND.
* The honest corrections in §A.6 (fixed affine lists provably
  insufficient; deep block needs an RT-glue rule family) are
  well-supported by the coverage data and correctly re-scope
  GAP-FG-schema.  The 0/165 false-positive control is the right
  soundness discipline and passed at every level.

### 5.2 §B J-pencil (S6 / JP / JP′ / the 36 derivations)  [SOUND — closure upgrade defended]

* S6 re-derived: RT(A) gives b ≺ a, RT(B) gives c ≺ b, unit C with
  t_C = a gives a ≺ c, T gives the (b, c) 2-cycle.  The linear
  solution t_A = 2j_C − 2j_A − j_B re-solved by hand from the three
  constraints — matches; of the eight residue patterns exactly
  (j, j′, j′) and (j, j, j′) admit t_A ≥ 0 (all six others are
  forced negative for 1 ≤ j < j′) — the note says "16 patterns";
  the space is {j, j′}³ = 8 (t_C is determined, not free).  NIT
  only; the two surviving patterns and their windows are correct.
* JP re-computed: t = j′−2j, a = j+2t, b = 3j′−4j = 2a−t,
  c = 5j′−6j = 2b−t; window 5j′−6j ≤ 15 → exactly
  {(1,2),(1,3),(1,4),(2,4),(2,5),(3,6)}.  JP′ re-computed:
  t_A = 2j′−3j, t_B = 3j′−4j, a = 4j′−5j, b = 6j′−7j, c = 9j′−10j;
  window 9j′−10j ≤ 15 → {(1,2),(2,3),(3,5),(4,6)}.  Union = the
  nine 6-fact pairs, matching e153_j_pencil.log and the notes/60 §3
  independent-engine reproduction.  The RT windows (b ≤ c ≤ 15)
  close because b ≥ t_B forces b ≤ c.  Sound.
* Lemma J's upgrade [MACHINE-CHECKED → PROVED] is defended: validity
  is by reflection (every printed step a Lemma-CC rule application),
  the split search is exhaustive, and an independent engine
  (notes/60 §3) reproduced the full 29+7 catalogue.  The three
  assembly-load-bearing sets (J({1,2}), J({1,3}), J({2,4})) are in
  the hand-checkable JP family.

### 5.3 §C FG-deep  [SOUND as tagged; still 48-only]

The exact maps R(48)/D(48), the resonance law (8 | gap necessary),
the E1×E1 deep characterization, and the 55/75 branch certificates
are honest machine facts with the right speciation (the 20-pair
parity-locked core correctly merged into GAP-PARM).  The §C.1
"close-pair law" correction to notes/55 §5.3b (E1 exclusion needed)
is real.  Caveat the note itself carries: everything is at M = 48;
the cross-scale audit (planned at 64 with the precomputed alive grid
data/e157_audit_alive_M64.json) has not run — GAP-FG-deep's risk
rating (medium for the halving core) is appropriate, and the
resonance law should not be cited as multi-scale until that runs.

### 5.4 §D ASM′  [SOUND; composition assessed]

Theorem ASM′'s proof re-read case by case (F/L/P): Lemma-U
integration correct; Case L's swap normalization discharged by the
listed invariances; Case P correctly derives Φ = 0 from (H-D) UNSAT
and applies PH + (H-P); coverage of m exhaustive given (OV).  Two
referee remarks, neither a flaw:

* (61-A1) The (H-L)/(H-D) instances must use the SAME catalogue
  𝔉(M) — stated in the hypotheses; the fielded instruments satisfy
  it (both load e146_catalogue_M{M}.json).  Worth keeping explicit
  in any final write-up because the catalogue is regenerable.
* (61-A2) ASM′ as displayed uses the EXACT hatch (Φ = 0) P arm; at
  160 that would still work only because W = 1 ≥ 0, but the robust
  COV-W′ replacement (notes/58 §4.2) is verified at 128 AND now 160
  (§4) and does not consume (OV).  The §D.4 status line ("(OV-∀)
  remains") is correct for ASM′ but the assembly's actual reliance
  on (OV-∀) is now: none at verified scales, insurance-only beyond.

With §2's data the D.3 bookkeeping extends: W(M) ≥ 0 at eight
scales; the (OV-∀) gap is unchanged in status but weakened in
load (61-A2).

## 6. Verdicts

**notes/58 (LLOP/PARM): SOUND WITH ONE DEAD EXTRAPOLATION** — every
measured claim reproduced or log-verified; Lemma AO/D3/PH+ and the
COV-W′ composition defended (here + notes/60 §2); the robust chain
at 128 reproduced and EXTENDED to 160 (COV-W′(160), §4).  The §1.1
flat K* law and the adjacency reading are dead (audit-1's
K*(160) = 83); the §6 K* pre-registration was wrong; the flat cap
law and the C(160) = 84 pre-registration were right (§2).  The
note's own machine-fact layer survives intact — only the
extrapolation prose loses, exactly as audit-1's ledger note
anticipated.

**notes/59 (lowgaps): SOUND** — §A/§B algebra re-derived at line
level with two presentational nits (FW rule-(i) guard bookkeeping;
"16 residue sign patterns" should be 8); Lemma J's PROVED upgrade
defended; §C honest and correctly scoped (cross-scale audit still
outstanding); Theorem ASM′ sound with the two §5.4 remarks.  No
overclaim found.

Ledger deltas applied to notes/50 + STATUS.md this session:
BRIDGE1 CLEARED (audit-1; 52-G1/52-G2 wording fixes applied to
notes/52); DICH sound under the mechanistic law; GAP-ASM′ = (OV-∀)
now 8-scale-true with robust-chain insurance verified at 2 scales;
N6a machine record 48..160 complete (seven scales).
