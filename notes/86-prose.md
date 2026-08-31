# 86 — FRONT PROSE + ASSEMBLY-PREP: the C3(p) referee pass, the
# definitive gap ledger, and the paper-2 skeleton
# (2026-08-30, assembly-prep session; sources: notes/78 Part I read
# line-by-line against notes/33; notes/50-82 swept for tags;
# paper/main.tex conventions)

Three deliverables: (1) the C3(p) prose rider — notes/82's SOLE
condition on Lemma Q / Theorem ALT-DEAD — discharged by a careful
referee pass of the affine write-up (notes/78 Part I) against the
p = 5 toolkit (notes/33); (2) the reconciled tag graph for notes
50–82 and the DEFINITIVE gap list; (3) paper2/main.tex, the skeleton
of "The Erdős–Graham two-set problem, II: the general case" — no new
mathematics anywhere in this note.

---

## 1. The C3(p) prose rider: referee pass of notes/78 Part I
## [DISCHARGED — one cosmetic arithmetic slip found, conservative
## direction, zero mathematical effect; write-up is publication-grade]

Mandate (notes/82 §2.2 dependency audit): "ALT-DEAD inherits exactly
one rider: the C3(p) prose pass at paper time."  The pass below
re-derives, by hand, every displayed identity, congruence, index,
mirror membership, and window bound of notes/78 §§I.0–I.5, and
checks each lemma statement against its p = 5 instance in notes/33.
Method: statement-by-statement; nothing was taken from the machine
record (the e123/e180 layers are corroboration here, not evidence).

### 1.1 Statement layer (I.0) — CLEAN

- Unit convention: attacker a's j-th unit is (t_{a−2j} ≺ b_j).
  A1(p) = (a=3p, j=p): t_{3p−2p} = t_p ≺ b_p ✓.  A2(p) = (a=3p,
  j=p+1): t_{p−2} ≺ b_{p+1} ✓.  A3(p) = (a=3p+1, j=p−2):
  t_{3p+1−2(p−2)} = t_{p+5} ≺ b_{p−2} ✓.
- p = 5 specialization: {t₅≺b₅, t₃≺b₆, t₁₀≺b₃} = C3 of notes/33
  verbatim, and the stated bound M ≥ 2p+6 = 16 matches thm:c3core ✓.
- Flip-class arithmetic: p odd ⟹ 2p+6 ≡ 0 (mod 4), so
  M ≡ 2p+6 (mod 8) ⟹ M ≡ 0 (mod 4); and M/2 ≡ p+3 (mod 4) is an
  exact restatement ✓.  For p ≡ 1 (mod 4): 2p+6 ≡ 8 ≡ 0 (mod 8) —
  the class consumed by Theorem B1 at C₀ = 0 (every 2^m, m ≥ 3, is
  in it; for fixed p the rung claim applies at the cofinitely many
  m with 2^m ≥ 2p+6, which is how B1 consumes it) ✓.  For
  p ≡ 3 (mod 4): class M ≡ 4 (mod 8) ✓.

### 1.2 Affine constant table (I.1) — CLEAN, all eight identities
### re-derived

p odd gives 2p+2 ≡ 0 (mod 4), hence −p ≡ p+2 and 2−p ≡ p (mod 4);
with M ≡ 0 (mod 4), ω(v) ≡ v (mod 4).  Checked: t_p = 2M−p ≡ p+2;
t_{p−2} ≡ p; b_p ≡ p; b_{p−2} ≡ p+2; t_{p+5}, b_{p+1} even ✓ (p
odd).  m₀ = 3M/2 even; m₀±1 odd and cover both odd classes mod 4 ✓.
POLAR mirror 2m₀ − t_p = 3M − (2M−p) = M+p = b_p, p-free ✓.  Flip
mirrors b_{p−2} + t_p = 3M−2 = 2(m₀−1) and b_p + t_{p−2} = 3M+2 =
2(m₀+1), p-free ✓.  G4-center condition (c ≡ class+2 mod 4) as in
notes/33 §3 ✓: center ≡ p floods class p+2 ∋ {b_{p−2}, t_p}, center
≡ p+2 floods class p ∋ {b_p, t_{p−2}} ✓.

### 1.3 Toolkit import + Lemma E(p) (I.2) — CLEAN

Lemmas Z, D, P are quoted UNCHANGED from notes/33 §§2–3; verified
that their statements and proofs are p-free (they mention only a
ladder, a center, a seed, a target — no core offsets).  Lemma E(p):
- ladder indices: b_{p−2} = w_{(p−3)/2}, b_p = w_{(p−1)/2},
  t_p = w_{(M−p−1)/2}, t_{p−2} = w_{(M−p+1)/2} — two adjacent pairs ✓
  (w_i = M+1+2i).
- collision scales: b_p = t_{p−2} and b_{p−2} = t_p at M = 2p−2;
  b_{p−2} = t_{p−2} at 2p−4; b_p = t_p at 2p — all < 2p+2, so the
  stated bound M ≥ 2p+2 gives four distinct values ✓.
- index gap (M−p+1)/2 − (p−1)/2 = M/2 − p + 1 ≡ M/2 (mod 2, p odd):
  even iff M ≡ 0 (mod 4) ✓; the two displayed lock directions follow
  from Lemma Z exactly as in notes/33, and at p = 5 the
  M ≡ 0 (mod 4) case reads b₅≺b₃ ⟺ t₃≺t₅ = notes/33 Lemma E
  verbatim ✓.

### 1.4 Theorem L1(p) (I.3) — CLEAN; the affine formulation
### SUBSUMES notes/33's per-residue center definition

- Seed: S = b_{p−2} ≺ b_p at adjacent indices makes the ODD2 leaders
  the offsets ≡ 1 + (p−3) ≡ p+2 (mod 4) ✓ (matches notes/33's
  "≡ 3 (mod 4)" at p = 5).
- Centers: c* ≡ p is a G4-center for class p+2 ∋ b_{p−2} and an ODD2
  trailer; c** ≡ p+2 is a G4-center for class p ∋ t_{p−2} and an
  ODD2 leader ✓.  Note the improvement over notes/33 §4, which
  defined c*/c** by cases on M mod 8; the affine form "the element
  of {m₀−1, m₀+1} with c* ≡ p (mod 4)" needs no case split and
  specializes correctly (checked at p = 5 against both notes/33
  branches) ✓.
- Case I floods: G4-inward mirror 2c* − b_{p−2} = 2M−p+2±2 ∈
  {t_{p−4}, t_p}, offsets p−4 ≥ 1 (p ≥ 5) and p ≤ M−1 ✓; pair
  distance ≡ p−(p+2) ≡ 2 (mod 4) ✓; P2-outward mirror 2c* − t_{p+5}
  = M+p+5±2 ∈ {b_{p+3}, b_{p+7}}, offsets ≤ p+7 ≤ M ✓ (this is
  where M ≥ p+7 is sharp); t_{p+5} in block ⟺ M ≥ p+6 ✓; 3-cycle
  with A3 ✓.
- Case II floods: mirrors {b_{p−4}, b_p} and {t_{p−1}, t_{p+3}} —
  offsets p−4 ≥ 1, p+3 ≤ M−1 ✓; 3-cycle with A2 ✓.
- Cross-parity split (t_p, m₀) legitimate (odd vs even, distinct) ✓;
  case anatomy (I consumes only A3, II only A2) matches p = 5 ✓.
- Transfer half below M = 2p+2: within M ≡ 0 (mod 4) the only
  E-collision scale is 2p−2 (p odd ⟹ 2p−2 ≡ 0, 2p−4 ≡ 2p ≡ 2
  (mod 4)) ✓, and there b_p = t_{p−2}, b_{p−2} = t_p make the
  transfer conclusion literally identical to the already-forced
  b_p ≺ b_{p−2} ✓.  Coincidence-tolerance remark (I.5) covers
  interior collisions of core values with flood targets at
  p+7 ≤ M < 2p+6; the machine boundary scan (e180 partMINM: L1
  passes at EVERY 4 | M ≥ p+7, fails below) independently confirms
  the window is exact ✓.

### 1.5 Theorem FLIP(p) (I.4) — CLEAN except ONE cosmetic slip

- Seed b_p ≺ b_{p−2} makes ODD2 leaders ≡ p (mod 4) ✓.  Center
  offsets: M/2−1 ≡ p+2, M/2+1 ≡ p (mod 4) from M/2 ≡ p+3 ✓; cI
  trailer with leader neighbors m₀−3, m₀+1 (offsets ≡ p) ✓; cII
  leader ✓.  This is the p-shifted mod-8 lock; at p = 5 it
  reproduces notes/33 §5's center/leader table exactly ✓.
- Case I: P2 mirror 2cI − t_{p+5} = b_{p+3} ✓ in block; R4 on
  (b_{p−2}, cI, t_p) rides b_{p−2} + t_p = 3M−2 = 2cI ✓; G4 mirror
  2cI − b_p = t_{p+2} ✓; pair distance |M/2−1−p| ≡ |p+3−1−p| ≡ 2
  (mod 4) ✓; the 4/5 2-cycle consumes A1 + A3 ✓.
- Case II: mirrors t_{p−1} (offset ≥ 4 at p ≥ 5) and b_{p+2} ✓; R3
  on (b_p, cII, t_{p−2}) rides b_p + t_{p−2} = 3M+2 = 2cII ✓;
  distance ≡ 2 (mod 4) ✓; consumes A1 + A2 ✓.
- **The slip (cosmetic, conservative).**  Case I step 3 displays the
  betweenness condition "p−2 < M/2−1 < M−p, i.e. M > 2p+2".  Both
  displayed inequalities are equivalent to p−1 < M/2, i.e.
  **M > 2p−2**, not M > 2p+2.  The stated sufficient condition
  M > 2p+2 is strictly stronger than what is needed, and the theorem
  hypothesis M ≥ 2p+6 implies both, so nothing is wrong — but the
  "i.e." is inaccurate as an equivalence.  PAPER FIX: replace by
  "i.e. M > 2p−2, amply covered in class by M ≥ 2p+6" (and the
  parallel Case II step 3 "betweenness again from M ≥ 2p+6" is fine
  as stated).  No other display in Part I has this issue.
- In-class boundary: the one in-class scale below 2p+6 is 2p−2,
  where t_p = b_{p−2} degenerates the hypothesis set — matches the
  I.5 boundary paragraph and the machine scan ✓.

### 1.6 Assembly, sharpness, residue casework (I.5) — COMPLETE

- Assembly: M ≡ 2p+6 (mod 8) ⟹ M ≡ 0 (mod 4), and 2p+6 ≥ p+7 ⟺
  p ≥ 1 ✓, so L1(p) + FLIP(p) compose with no extra hypothesis ✓.
  FLIP consumes only the b-pair half of L1's conclusion, so Lemma
  E(p)'s M ≥ 2p+2 never binds the assembly ✓.
- Sharpness: on M/2 ≡ p+1 (mod 4) the center offsets become
  M/2−1 ≡ p, M/2+1 ≡ p+2 — each center lands in the SAME class it
  would need to flood (violating c ≡ class+2), and the ODD2
  leader/trailer statuses invert, so neither case's seed set exists
  ✓ — the prose reason is complete and matches notes/33 Remark (b)
  at p = 5; machine SAT on the complementary class at every tested
  p corroborates ✓.
- Residue casework completeness: the write-up never splits on
  p mod 4 — all congruences are carried symbolically in {p, p+2}
  (mod 4), and both flip classes (0 and 4 mod 8) are instances of
  the single statement M ≡ 2p+6 (mod 8) ✓.  Both mod-4 classes of p
  are machine-instantiated (p = 5..25 schema; solver x-val at 9
  p-values; identities re-derived to p = 39 — notes/80 §1.1) ✓.
- No [M40-ONLY]-style leftovers anywhere in Part I: the only
  bracketed scope tags in notes/78 are in Part II ((N3-b) [GAP],
  GAP-SA-HALF), which is NOT on the ALT-DEAD chain ✓.  Constants:
  every window bound displayed in Part I (p+7, 2p+2, 2p+6, 2p−2,
  in-block offset bounds) is affine in p ✓.

### 1.7 The consumption interface to Lemma Q — CHECKED

Two facts notes/82 §2.1(iii) uses about C3(p), verified affine:
(a) the three C3(p) units are among the fired units of the full rung
R(3p, 3p+1; M, ∅): j-values p, p+1, p−2 ≥ 1 and t-offsets
p, p−2, p+5 ∈ [0, M−1] whenever M ≥ p+6 ✓ (so C3(p)-inconsistency
kills R a fortiori — machine 6/6 in e186 partQVERIFY); (b) DIAG-DENSE
supplies pairs {3p, 3p+1} with p ≡ 1 (mod 4), p ≥ 5, whose flip
class is 0 mod 8 ∋ every dyadic scale ≥ 2p+6 ✓; (c) B1's Step-1
threshold 3p ≥ x₀(0) = 6 is automatic at p ≥ 5 ✓.

### 1.8 VERDICT

**The C3(p) prose rider is DISCHARGED.**  Theorem C3(p)'s write-up
(notes/78 Part I) is publication-grade as it stands, modulo one
one-word paper fix (§1.5: "M > 2p+2" → "M > 2p−2", conservative
direction, zero effect on any claim).  Every lemma statement is
affine in p, every residue/parity/window check is done once
parametrically and is complete, the p = 5 specialization reproduces
notes/33 verbatim (statements, constants, centers, case anatomy),
and the interfaces consumed by Lemma Q / Theorem ALT-DEAD (notes/82)
are exactly as claimed there.  With this pass, **Lemma Q, Theorem
ALT-DEAD, and Cor. HSPLIT carry no rider at all**: their input chain
(PIN + DIAG-DENSE + C3(p) + restriction/affine transport) is
[PROVED] end to end.  Tag move for notes/50 §6 row (H1′) part 1:
"residual = referee prose pass at paper time" → **NONE (prose pass
done, notes/86 §1)**.

---

## 2. Tag-graph reconciliation (notes 50–82) and THE DEFINITIVE
## GAP LIST

Method: every bracketed [GAP…] tag and every named GAP-* mention in
notes 50–82 was grepped, read in context, and traced to its latest
disposition (authorities: notes/50 final graph, notes/77 §7 pool
inventory, notes/80-pincer §3.4, notes/82 §5, plus §1 above).  The
drift is real: 14 stale tags dangle in notes that later notes closed,
superseded, or renamed.  §2.1 is the reconciliation; §2.2 is the
single authoritative list.

### 2.1 Reconciliation table (dangling tag → disposition)

| dangling tag (where it dangles) | disposition (closer) |
|---|---|
| GAP-N2-DIAG (notes/52 §; 50 §6 row) | **DISCHARGED**: Theorem C3(p) [PROVED — notes/78 Part I; spot-audited notes/80 §1.1; prose pass DONE notes/86 §1].  Residual: NONE |
| GAP-N3 uniform-C (notes/52) | REFUTED as posed (transversal escapes); reshaped → GAP-N3-GROW (notes/74); only (N3-b) open |
| GAP-RHO (notes/54 IIa) | SUPERSEDED (route retired): the notes/54 regime-(II) ledger route was replaced by the N4 frame + coupled-core + T-TEL″ chain (notes/43/46/70/72), which needs no density-regime split; no successor tag; nothing cites it after notes/54 |
| GAP-ALT (notes/54 IIb — OLD tag, ≠ GAP-AFFORD″-ALT) | SUPERSEDED with the same route; the ω-alternation question was reborn as GAP-AFFORD″-ALT (notes/80-pincer) and KILLED by Theorem ALT-DEAD (notes/82).  Name collision noted for the record |
| GAP-AFFORD (notes/54 §4) | superseded by the sharper **GAP-AFFORD′** (notes/62 §5) — still THE terminal gap |
| GAP-COMP (notes/54) | REFUTED (notes/62 §4b: descent digraphs carry zero AP 2-paths; counting form dead; no-retry) |
| GAP-JOINT (notes/54) | RESOLVED as measurement (notes/62 §§3–4: downward coupling real, priced, demand-side only — NG4); surviving content absorbed into GAP-AFFORD′ + L-CASCADE |
| GAP-V*-growth (notes/54, 68, 70) | DEMOTED (notes/75: demand existence rides J-DOWN collapse, not the curve); GAP-V* survives for RATE sharpening only |
| COV(M) [GAP] = GAP-STRUCT (notes/56) | ABSORBED: the DP/CEGAR catalogue became the N6a machine layer (COV-W ×6 scales, COV-W′ robust); the uniform residue is the pool's GAP-ASM′ = (OV-∀) + GAP-RES (notes/59 ASM′; notes/77 §7) |
| GAP-PARM residual (notes/55 §7, 58) | reduces to GAP-RES + ThW1′-ROBUST (notes/77 §4.7); GAP-PARM-CORNER itself CLEARED (Theorem P-ARM‴) |
| FW-boundary cross-scale [GAP — cheap compute] (notes/59 §1) | CLOSED by notes/77 §1.2: the q = M−12 deep-block edge is 48-SPECIFIC (machine, 4 scales) — recharacterized into GAP-RES's scaled zone |
| GAP-J-schema (notes/62, 70) | ABSORBED: large-M = GAP-N6a verbatim via J-DOWN (notes/75); boot window = Theorem J-BOOT [PROVED mod GAP-CMIN]; residue = GAP-J-margin + GAP-F-schema |
| GAP-VMIN0-growth (notes/70, 71) | DISCHARGED (notes/72: collapse J-DOWN + floor J-BOOT; confirmed notes/75) |
| SPAN-4 / ODD-KILL clustered [GAP] (notes/66) | CONSOLIDATED into GAP-RES as its DICH-ALPHA arm via Cor. PURE-2 (notes/77 §7); current front material |
| GAP-DICH-F0 (notes/57) | CLEARED (Lemma PURE [PROVED] + SAT-level bijection ×3 scales; notes/77 §3.1) |
| GAP-FG-schema fixed-pair half (notes/59) | CLEARED (Theorem AFF⁺ + Lemma MON; notes/77 §1.3); glue half → GAP-RES |
| GAP-FHALF / GAP-FTOT (notes/71, 72) | REDUCED to GAP-CMIN (verbatim reduction, notes/71); not independent tags anymore |
| GAP-BRIDGE1, GAP-G2/DNP, GAP-L1′, GAP-N2's 3 remainders | as notes/50 §3: discharged / refuted-reframed / REFUTED (ROT4) / discharged |
| MINT-LOC (notes/80 §3) | RETIRED resolved-strong-form (notes/80-pincer §2: literal mechanism wrong, stronger theorem AFFORD-DEMAND [PROVED]) |
| GAP-AFFORD″-ALT (notes/80-pincer §3.4) | RETIRED (notes/82: Lemma Q + ALT-DEAD kill the whole arithmetic corner); residue renamed **GAP-AFFORD‴-SPLIT** |
| L-NOTAIL (notes/80-pincer §3) | not a gap — [PROVED], now a COROLLARY of Lemma Q on the lattice family (notes/82 §5); kept for classical self-audit |
| C3(p) prose rider (notes/82 §2.2; 50 §6; STATUS) | DISCHARGED this note (§1).  Lemma Q / ALT-DEAD / HSPLIT are rider-free |

Notes whose bracketed [GAP]s are NOT stale (verified current):
notes/71 (CMIN/FTOT/MARGIN-MASS), notes/72 (ZERO, V*, F-schema,
J-margin), notes/73 (N2-UNIF), notes/74/78 ((N3-b)), notes/59 §5
((OV-∀)), notes/58 (LLOP-α/β), notes/77 §7 (the pool residue),
notes/80-pincer/82 (AFFORD‴-SPLIT).

### 2.2 THE DEFINITIVE GAP LIST (2026-08-30, post notes/82 + §1)

**GATING (the assembly theorem's hypotheses, notes/50 §5 — now
THREE, was four):**

1. **GAP-AFFORD′** — the terminal supply cap: no valid Case-2 pair
   can fund the T-TEL″ mint system (≥ 1 displaced value per 2
   octaves, single-use colored values) forever.  Sharpest surviving
   form after the chart kill: **GAP-AFFORD‴-SPLIT** — the cap for
   gap-≥3, 2-adically split minorities [NOT "hence aperiodic" —
   corrected, notes/88 item 2: mod-3 periodic minorities are
   HSPLIT-compatible]; no known inhabitant of the full corner
   axes; plus arm B's p(k) → ∞ pump.
   Species: genuinely new ledger mathematics; zero completed
   strategies; professor-certified no elegant kill (notes/82 §5).
2. **GAP-N6a sub-pool** — CI(m)/CORE′ fires for all m; owed
   write-ups per notes/77 §7: **GAP-RES** (consolidated crux:
   classify SAT-alive fan pairs uniformly in window length; carries
   FG-scaled-zone, FG-deep taxonomy, DICH-ALPHA/SPAN-4, H-LAT) +
   ThW1′-ROBUST/-TOL + GAP-DICH-F2/CASC + SPLIT staircase +
   GAP-LLOP-α/β + GAP-ASM′ = (OV-∀).  Species: uniformization/
   classification, discharged instances exist for every item.
3. **GAP-N3-GROW (N3-b)** — every puncture set D, |D| < ⌊(x−1)/4⌋,
   leaves R(x; M) UNSAT, uniformly in odd x ≥ 11 and D.  Skeleton
   LANE + SEV + (N3-b′) stated (notes/78 §II.3); machine-exact at
   x = 11/15/19/23/27.  Species: uniformization + robustness.

**HARDENING (open, NOT gating the assembly):**

4. GAP-CMIN — Σ_z min(c_A, c_B) ≥ M (extremal cell PROVED M ≥ 32;
   near-pure = O(1) bookkeeping + 2 scoped subcases); carries
   GAP-FHALF and GAP-FTOT verbatim, hence J-BOOT/F-BOOT
   unconditional.
5. GAP-F-schema — F(N; v) freshness family; only sharpens demand
   density 1/2 → 1 per octave.
6. GAP-J-margin / GAP-MARGIN-MASS — the U4 margin family's impure
   arm (low-pure arm PROVED, MARGIN-LP + K-diagonal).
7. GAP-N2-UNIF ∖ N2-DIAG — the remaining 35 template cells; feeds
   BRIDGE1-AF only, and (with N3-GROW at C = 2) Cor. Q-ODD [stated].
8. GAP-SA-HALF — SA(y; m) always SAT (single-attacker rungs never
   kill); gates only the SHARPNESS side (N3-a) of the growth law.
9. GAP-V* — v*₃ growth/rate sharpening only (+ the GAP-V*-schema
   seed of notes/68).
10. GAP-ZERO — classify the sumset floor's zero variety (all zeros
    measured low-pure/order-dead; N3-species).
11. GAP-SPARSE-CORE residue — mixed-designation catalogue only (AAA
    arm HAND-CLOSED m ≥ 26 + machine 16..48; strengthens the
    (iii)-corner demand, arms but does not gate).

**Standing no-gos respected by all of the above:** NG1–NG4 (supply
caps not provable by demand instruments), T-SHARP (no orbit-growth
shortcut), the notes/47 DNP refutation, L1′ refuted (ROT4), N5
ρ* → 1 (density never fires rungs), notes/81 §1 (majority-side
class-punctured rungs provably SAT — the minority chart is the only
route).

**Count check:** gating gaps 3 (was 4 — GAP-N2-DIAG cleared with
zero residual); the entire arithmetic YES-corner dead at ω with the
last rider now discharged; the YES requires a 2-adically generic
gap-≥3 coloring (never constructed) AND ¬AFFORD on it.

---

## 3. Paper-2 skeleton: paper2/main.tex

Drafted and compiled (tectonic, clean): **"The Erdős–Graham two-set
problem, II: the general case"** — paper/main.tex conventions
(11pt article, amsthm envs, same author/thanks block).  Contents,
NO new mathematics:

- Theorem A (unconditional headline): the hereditary-splitness
  package — Lemma Q, Theorem ALT-DEAD, Cor. HSPLIT, Cor. L-NOTAIL —
  stated verbatim from notes/82/80-pincer, tagged [PROVED],
  rider-free per §1.
- Theorem B (conditional assembly, notes/50 §5) modulo exactly
  three numbered Hypotheses = the gating gaps of §2.2: N3-GROW
  (N3-b), N6a closure (sub-pool per notes/77 §7), AFFORD′ (with the
  SPLIT-residue sharpening stated inside the hypothesis).
- Full statements transcribed for: C3(p)/L1(p)/FLIP(p)/E(p)
  (notes/78 Part I), PIN/DIAG-DENSE/(H1)/B1 + the unconditional
  C₀ = 0 corollary (notes/52), N4 (notes/43/46), T-TEL″ (notes/72
  §6), Q-ODD [stated only].
- Dependency graph (verbatim block, [P]/[M]/[GAP] legend) mirroring
  notes/50; section-to-notes assembly checklist table; the
  recommended truncation cut (a): §§2–5 = "structure + Theorem A"
  is publication-complete NOW; cut (b) = full paper when a
  hypothesis moves.

Every section of the skeleton names the notes that already contain
its finished mathematics; the only [GAP]-tagged objects in the file
are the three Hypotheses.  File: paper2/main.tex (compiles to
main.pdf, 113 KB).

## 4. Session summary

| deliverable | state |
|---|---|
| C3(p) referee prose pass (notes/82's sole ALT-DEAD rider) | DISCHARGED (§1); one cosmetic paper fix recorded; Lemma Q / ALT-DEAD / HSPLIT rider-free |
| tag-graph reconciliation notes 50–82 | §2.1 table, 14+ stale tags traced to closers; notes/50 rider lines updated |
| DEFINITIVE gap list | §2.2 — gating: GAP-AFFORD′ (residue AFFORD‴-SPLIT), GAP-N6a sub-pool, GAP-N3-GROW (N3-b); hardening: CMIN, F-schema, J-margin/MARGIN-MASS, N2-UNIF, SA-HALF, V*, ZERO, SPARSE-CORE catalogue |
| paper-2 skeleton | paper2/main.tex, compiles; Theorem A unconditional cut identified |
