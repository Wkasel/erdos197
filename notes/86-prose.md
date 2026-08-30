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
