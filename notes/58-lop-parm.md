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

---

## 1. The cap and threshold laws at M = 112  [MACHINE-CHECKED]

New scale M = 112 (e146 catalogue: 7836 fan patterns, 36 J; e152/e153
single-K probes, CaDiCaL 0.3–4.2 s each):

    L-LOP(112):  K = 59, 60 UNSAT;  K = 61, 62 SAT
                 → cap(112) = 59 (min|Y| form; kmax_unsat = 60).
    DICH(112):   K = 57, 58, 59 SAT (each frontier witness with
                 Φ = 56 = M/2 exactly — ONE hatch defector);
                 K = 60, 61, 62 UNSAT → K*(112) = 60.

**The cap law (5/5 scales).**  In min|Y| form,

    cap(M) = (M+16)/2 − ⌊M/32⌋ − 2
           = 29 / 36 / 44 / 51 / 59   at M = 48 / 64 / 80 / 96 / 112,

increments alternating +7/+8 by M mod 32.  (Equivalently: the least
killing band-major size is S(M) = (M+16)/2 + ⌊M/32⌋ + 3.)  The
task-brief guess "(M+16)/2 + {5,4}" matches the band-major form's
complement: M+16−S(M)... the clean statement is the display above.
[MACHINE-CHECKED at 5 scales; sharp at all 5.]

**The K* law is NOT mod-32-periodic — falsified at 112.**  Offsets
K*(M) − (M+16)/2:

    −6, −5, −6, −5, −4    at M = 48, 64, 80, 96, 112,

so the notes/56 §3.3 reading (−6 on M ≡ 16, −5 on M ≡ 0 (mod 32))
breaks at the fifth scale.  Overlap width cap − K* + 1:
4 / 2 / 3 / 1 / 0.  At M = 112 the two arms are EXACTLY ADJACENT
(L kills min|Y| ≤ 59, P kills ≥ 60 — still exhaustive, zero slack).

Frontier anatomy at 112 (all three SAT probes): Φ = M/2 — a SINGLE
Z-defector against parity-pure U's, confirming the §4 design point
that the boundary zone is a small-defect regime.

### 1.1 M = 128: both O(1)-drift laws stop drifting; exact adjacency
### again  [MACHINE-CHECKED]

    L-LOP(128): K = 66, 67, 68 UNSAT; K = 69, 70 SAT
                → cap(128) = 67 (NOT the ⌊M/32⌋-law's 66 — that law
                dies at its first out-of-sample test).
    DICH(128):  K = 65, 66, 67 SAT (Φ = 192/64/64 = (M/2)·{3,1,1});
                K = 68, 69, 70 UNSAT → K*(128) = 68.

Combined table (min|Y| forms; offsets from balance (M+16)/2):

    M          48   64   80   96   112  128
    cap        29   36   44   51   59   67     offs −3 −4 −4 −5 −5 −5
    K*         26   35   42   51   60   68     offs −6 −5 −6 −5 −4 −4
    width       4    2    3    1    0    0

Both offset sequences have gone FLAT at −5 (cap) and −4 (K*) over
M = 96..128 resp. 112..128, and K* = cap + 1 EXACTLY at 112 and 128:
the two arms are complementary with zero slack — no hole at 128
(the notes/56 §4b projection of a hole "near M = 128" is falsified
in the good direction).  Candidate asymptotic law: cap = (M+16)/2 − 5
and K* = (M+16)/2 − 4 for M ≥ 96/112 — under which the assembly
stays exhaustive at ALL scales and GAP-ASM′ reduces to proving the
two flat offsets.  The M = 160 endgame (§6) tests this directly;
the robust P-ARM (§4) is the insurance either way.

**L-LOP frontier anatomy at 128 (K = 69 witness)** — the escape is a
PARITY-LATTICE coloring: Y_A = the full even band class + 4 odd
E1-region values (depths 133/137/139/141 = y ∈ {3M−13, 3M−11, 3M−9,
3M−5}); U_B ⊇ the odd α-window, Z_B ⊇ the even completion zone.
I.e. the coloring is (up to swap) a HATCH coloring with band split
by parity and 4 odd-E1 defectors to A — Th1(B)'s α system on the
punctured odd class escapes precisely because half its 8 odd
E1-midpoints are gone.  Read: at the cap the L arm hands off exactly
the P-arm family (compare notes/56 §2.3's balanced cluster), and the
L-LOP cap is set by how many E1-midpoint defectors the α/crown
system tolerates — the quantitative bridge between GAP-LLOP-α and
(H-RW0).

[MACHINE-CHECK: data/e152_llop_probes.log, data/e153_dich_probes.log,
data/e146_catalogue.log (M=112/128 blocks).]

---

## 2. L-LOP anatomy I: the defuse dichotomy and the punch-descent
## lemma  [PROVED core + scoped remainder]

Fix M ≡ 0 (mod 16), M ≥ 48 (all inequalities below need only M ≥ 32
and M even; noted where finer).  Notation (notes/55 §2):

    A_α := [2M−30, 2M]        the α attacker window (B0's top-31; A2)
    C   := [4M+1, 5M+15]      the completion zone (A3: every in-band
                              high-pair completion lands here)
    C′  := [5M+16, 6M+15]     the upper zone (M values; band
                              completions never reach it)
    y₀  := (7M+16)/2          the punch threshold (integer, M even)
    MID := [3M−14, (7M+14)/2] the middle band zone (M/2 + 22 values)

### 2.1 Why Th1(B) alone cannot kill: the AP-free order lemma

**Lemma AO.**  Every finite S ⊆ ℤ admits a linear order with no
monotone 3-AP.  *Proof.*  Order the evens of S (recursively, via
x ↦ x/2, which preserves APs) before the odds of S (recursively, via
x ↦ (x−1)/2).  A mono AP (a, b, c) has a ≡ c (mod 2); if a, c are
even and b odd then b follows both in the order, so the AP is not
monotone unless it lies in one parity class; recurse.  Induction on
diameter terminates.  ∎  [PROVED — classical argument.]

**Consequence.**  Th1(B) restricted to its in-band AP constraints
alone is ALWAYS consistent.  An L-LOP kill therefore requires fired
α-units (attacker in U_B ∩ A_α, by A2) or fired β-units (completion
in Z_B ∩ C, by A3).  Call the team *defused* if

    (defuse-α)  U_B ∩ A_α = ∅       and
    (defuse-β)  Z_B ∩ C  = ∅.

If B can be defused, Th1(B) is consistent and L-LOP(M) would be SAT
at every K ≥ 3.  The machine caps say it is not.  §2.2 is the reason.

### 2.2 Lemma D3 (defuse incompatibility — the punch-descent)
### [PROVED]

**Lemma D3.**  Let χ be a 2-coloring of CORE′(M) that is
straddle-free for both teams and has |Y_A| ≥ 2, |U_B| ≥ 1.  Then

    U_B ∩ A_α ≠ ∅    or    Z_B ∩ C ≠ ∅.

(Equivalently: a team with ≥ 2 opposing band values and ≥ 1 own
P0 value cannot be defused.  Note the hypothesis uses only the
bounds; no fan-cleanness, no band-major assumption, and Th1 itself
never appears — this is a pure coloring lemma.)

*Proof.*  Suppose both intersections are empty, so A_α ⊆ U_A and
C ⊆ Z_A.

**Step 1 (position: Y_A avoids MID).**  For y ∈ Y_A the *punch
window* PW(y) := 2y − A_α = [2y−2M, 2y−2M+30] consists of 31
consecutive integers.  For every u ∈ A_α ⊆ U_A, straddle-freeness of
A forbids (u, y, 2y−u) mono, i.e. 2y−u ∉ Z_A whenever
2y−u ∈ P2.  Since C ⊆ Z_A this gives PW(y) ∩ C = ∅.  But
PW(y) ∩ C ≠ ∅ exactly for y ∈ MID = [3M−14, (7M+14)/2].  Hence

    Y_A ⊆ {3M−15} ∪ [y₀, 4M].

**Step 2 (a high value exists).**  |Y_A| ≥ 2 and only one band value
lies at 3M−15, so Y_A ∩ [y₀, 4M] ≠ ∅.  Let ŷ := min(Y_A ∩ [y₀, 4M]).

**Step 3 (punch).**  Every z ∈ PW(ŷ) ∩ P2 satisfies z = 2ŷ − u with
u ∈ A_α ⊆ U_A, so z ∉ Z_A (straddle-freeness of A), i.e.
PW(ŷ) ∩ P2 ⊆ Z_B.  Moreover PW(ŷ) ⊆ C′ ∪ (6M+15, ∞): its bottom is
2ŷ−2M ≥ 5M+16 and 2ŷ−2M ≤ 6M (ŷ ≤ 4M), so in particular
z₀ := 2ŷ−2M + j ∈ Z_B ∩ C′ for j ∈ {0, 1} of either parity choice.

**Step 4 (exclusion and descent).**  Pick any u ∈ U_B and the
j ∈ {0, 1} with z₀ := 2ŷ−2M+j ≡ u (mod 2).  Then
y′ := (u+z₀)/2 is an integer with

    3M+8 ≤ ŷ − M + (u+j)/2 = y′ ≤ ŷ − 15         (u ≤ 2M−31),

so y′ ∈ P1, and (u, y′, z₀) is an AP with u ∈ U_B, z₀ ∈ Z_B.
Straddle-freeness of B forces y′ ∉ Y_B, i.e. y′ ∈ Y_A.  But
3M−15 < 3M+8 ≤ y′ < ŷ, so y′ contradicts Step 1 (if y′ < y₀) or the
minimality of ŷ (if y′ ≥ y₀).  ∎

(All range inequalities were symbol-checked and brute-verified at
M = 48: the MID characterization and the descent-step ranges have
zero exceptions over all (ŷ, u) — see the §2 audit block in the
session transcript; they are linear in M and need only M ≥ 32, M
even for y₀ ∈ ℤ.  For u ∈ [M+1, 2M−31] both endpoints of the
descent inequality are tight at u = 2M−31.)

**Remark (the u-range).**  Step 4 needs u ≤ 2M−31, which is exactly
u ∈ P0 ∖ A_α — guaranteed by defuse-α: U_B ⊆ [M+1, 2M−31].  The
lemma's two hypotheses feed precisely the two straddle applications:
defuse-α powers the punch (Step 3), defuse-β powers the position
constraint (Step 1).

[MACHINE-CHECK of Lemma D3: e156 — the pure coloring instance
(straddles + (2,2,2) + both defuses, no order theory) is UNSAT at
M = 48, 64, 96 in < 0.1 s, and all three controls behave as the
lemma predicts: defuse-α alone SAT, defuse-β alone SAT (each arm
individually defusable — the dichotomy is genuinely two-armed), and
dropping the |U_B| ≥ 1 hypothesis restores SAT (the hypothesis is
necessary).  data/e156_d3_check.log.]

### 2.3 The armed dichotomy and the two remaining arms

By Lemma D3 applied to each team (bounds give |Y_T| ≥ 2, |U_T| ≥ 1
for both), every straddle-free bounded coloring has BOTH teams
armed.  For the band-major team B of L-LOP this gives the case
split of the uniform proof:

* **Arm α (α-supply)**: U_B ∩ A_α ≠ ∅.  Fired units are the A2
  family: z ≺ y with y ∈ E1 ∩ Y_B, z ∈ top-31 ∩ Y_B, guarded by an
  attacker x ∈ U_B ∩ A_α with x = 2y − z.  The kill species is the
  ThW1′/α-lattice family (notes/56 §2.2, §4.2): a band-major Y_B
  contains most of one arithmetic class, and the α-units on that
  class halve (classwise Lemma H) to the H1-ThW1′ core.  [GAP-LLOP-α
  — the robust/punctured uniformization of the ThW1′ kill; the
  species of GAP-H1.]
* **Arm β (β-supply)**: Z_B ∩ C ≠ ∅.  Fired units are the A3/A4
  family: b ≺ a for high pairs a < b ⊆ Y_B with 2b − a ∈ Z_B ∩ C;
  when Y_B ⊇ most of the top run R, Lemma J turns S3-memberships
  into the 30+6 forbidden systems, and deeper completion-zone
  memberships give the generalized-J β patterns of E(M).
  [GAP-LLOP-β — the robust Lemma-J argument on co-bounded band
  subsets.]

The adversary can be armed in only one arm, so the uniform L-LOP
proof must kill each arm separately under band-majority.  Both arms
are QUANTITATIVE (one attacker or one completion is not enough —
the machine cap is sharp at min|Y| = cap+1); the cap law of §1 is
the arms' supply-demand balance point.  Status of the arms:
[GAP — scoped; species named; not attempted tonight beyond the MUS
anatomy below.]

**What Lemma D3 already buys the assembly.**  The notes/56 §4b
composition needs L-LOP as a wholesale machine lemma; D3 is its
first uniform (all even M ≥ 32) hand component, and it is exactly
the piece that makes the arms exhaustive.  It also explains a
frontier-law asymmetry from notes/55 §5.2: the (·,0,·) escapes have
|Y_T| ≤ 1 and dodge Step 2 — consistent with D3's |Y_A| ≥ 2
hypothesis being genuinely necessary.

[Status: Lemma AO, Lemma D3 PROVED; arms GAP-LLOP-α/β scoped.]

---

## 3. P-ARM: the classwise halving proof (conditional on two named
## finite schemas)

Throughout: the hatch is orientation 1 (U_A = odds of P0,
U_B = evens, Z_A = evens of P2, Z_B = odds; Lemma PH + team swap
give WLOG), m := M/2, and the band split is arbitrary.  Write

    A_e := Y_A ∩ 2ℤ,  A_o := Y_A ∖ 2ℤ,  B_e, B_o likewise,

so A_e ⊔ B_e = evens of P1, A_o ⊔ B_o = odds of P1.

### 3.1 Lemma PARM-HALVE (guard bookkeeping + halving)  [PROVED]

Under the hatch:

(a) Straddles are vacuous (a straddle has u ≡ z (mod 2), hence u, z
    in opposite teams).  [notes/55 §5.4 verbatim.]
(b) **Th2(A)** = the even-halved fan theory: its (0,2,2) units are
    empty (completion parity = attacker parity = odd ∉ Z_A); its
    (1,2,2) units need y, z ∈ Z_A (even) and then x = 2y − z is
    even, so exactly the attackers x ∈ A_e fire, with NO other
    guard; its in-block APs on Z_A = evens halve under v ↦ v/2.
    Image: AP-freeness on W2e := [4m+1, 6m+7] plus the FULL double
    fans of the attacker set h(A_e) ⊆ W1 := [3m−7, 4m]
    (h = halving).  Consequently: if h(A_e) contains ANY attacker
    set with an R1–R4+transitivity refutation of its fans in W2e,
    Th2(A) is inconsistent outright — under the hatch the entire
    refutation support is automatically in Z_A (all even), so there
    is no support-monochromaticity caveat.  Same for **Th2(B)** with
    h = v ↦ (v+1)/2, window W2o := [4m+1, 6m+8], attackers h(B_o).
(c) **Th0(A)** = ThW0(m) with guarded crown: order theory on
    h(U_A) = [m+1, 2m]; in-block APs halve; the (0,0,1) units have
    completions c = 2b − a odd, c ∈ E1 ∩ P1's bottom [3M−15, 3M−1]
    (Lemma A1), and fire iff c ∈ A_o.  Halved: the notes/55 §5.4c
    crown-unit system {2m−k ≺ m+j : k ≤ 3, 1 ≤ j ≤ 7−2k} (16
    units), whose unit (k, j) has completion c′ = 3m − (2k+j), so
    the completion window is c′ ∈ CW := [3m−7, 3m−1] — SEVEN
    values, unit multiplicities (1, 1, 2, 2, 3, 3, 4) for
    i = 2k+j = 1..7 — each guarded by the corresponding full-scale
    odd c = 2c′ − 1 ∈ A_o.  (The eighth halved value 3m is
    unreachable: it would need a′ = m ∉ [m+1, 2m]; arithmetic
    verified by script, session transcript.)  **Th0(B)** halves
    (via v ↦ v/2 on evens) to the IDENTICAL guarded theory with
    guards "c ∈ B_e" — both parities produce the same halved crown
    core ThW0(m) with completion window CW.
(d) **Th1(T)** contains its class restrictions (a restriction of a
    consistent theory is consistent, as in Lemma DP): Th1(A)[A_o] =
    the α-theory image on h(A_o) (α-units z ≺ y fire for A whenever
    y, z ∈ A_o with 2y − z ∈ [2M−30, 2M] — the attacker is odd,
    hence in U_A for free), and Th1(A)[A_e] = the β-theory image on
    h(A_e) (completions of even high pairs are even, hence in Z_A
    for free).  Mirror statements for B.  [Not needed for the §3.3
    kill; recorded because they make the aligned special cases
    literal sub-instances: A_o = all odds reproduces H1's ThW1′,
    A_e = all evens reproduces H(m)'s W1-side.]

*Proof.*  Parity bookkeeping identical to Lemma PAR's (notes/55
§5.4), classwise instead of globally; halving preserves/reflects
APs (notes/33 Lemma H).  The one new observation is (b)'s "no
support caveat": every value the closure refutation touches lies in
the attacker's parity class of P2, which the hatch assigns wholly
to the attacking team.  ∎

### 3.2 The two finite schema hypotheses

**(H-FG6)(m)**  In the fan theory on W2e (resp. W2o) with attacker
window W1: every attacker pair at distance ≤ 6 is refuted by plain
R1–R4 + transitivity closure of its double fan.
[Machine-true at all audited full scales for the analogous window
(notes/55 §5.3b: every escape pair has gap ≥ 16); to be re-audited
tonight on the HALVED windows W2e/W2o at m = 24..80 (e155) since
their upper ends 6m+7/6m+8 differ from the full-scale 6M+15.
Uniformization = GAP-FG-schema, already on the ledger.]

**(H-RW0)(m)**  ThW0(m) remains UNSAT after deleting the unit group
of any ONE completion value c′ ∈ CW.  (7 variants + the full
theory.)  [Finite per scale, solver-trivial; to be checked tonight
at m = 24, 28, 32, 40, 48, 56, 64, 80 (e155).  Uniformization =
GAP-H1's species, now in punctured form: GAP-RW0 ⊆ GAP-H1 ∪ {7
finite variants}.]

### 3.3 Theorem P-ARM′ (conditional)  [PROVED modulo H-FG6, H-RW0]

**Theorem.**  Assume (H-FG6)(m) and (H-RW0)(m).  Then P-ARM(M)
holds at M = 2m: under the hatch, for EVERY band split, some block
theory of some team is inconsistent.

*Proof.*  Case F: h(A_e) or h(B_o) contains an attacker pair at
distance ≤ 6.  By (H-FG6) and Lemma PARM-HALVE(b), the owning
team's Th2 is inconsistent.  Done.

Case S (separated): both h(A_e) and h(B_o) are 7-separated subsets
of W1.  The crown completion window CW = [3m−7, 3m−1] has width 6,
so |h(B_o) ∩ CW| ≤ 1: at most ONE of the 7 odd crown completions of
A lies in B_o; the other ≥ 6 lie in A_o (band partition), so the
guard groups of ≥ 6 of the 7 completions fire in Th0(A).  By
(H-RW0), Th0(A) is inconsistent.  ∎

(The kill is doubly redundant: |h(A_e) ∩ CW| ≤ 1 likewise fires
Th0(B) through the identical halved crown.  Neither the band bounds
nor Th1 are needed in the argument — matching the e150 machine fact
that blocks {0, 1} alone are SAT while adding block 2 kills: the
fan layer's role is exactly to force the separation that makes the
crown guards immune to defusal.)

### 3.4 The residue condition, made exact

The only residue-sensitive ingredient is (H-RW0): ThW0(m) is the
notes/55 §5.4c halved crown core, machine-dead on the line
m ≡ 0 (mod 8) — that is M ≡ 0 (mod 16) — with a SAT sharpness point
at m = 14 (M = 28) and scattered off-line UNSAT (m = 10, 12, 20).
So the task-brief expectation is realized precisely: **the mod-16
line inside GAP-H1 becomes P-ARM's residue condition through
(H-RW0)**; everything else in §3 is residue-free (H-FG8 needs
nothing; PARM-HALVE needs M even).  Off the target class
(M ≡ 8 (mod 16), i.e. m ≡ 4 (mod 8)) the theorem stands or falls
with ThW0's punctured variants at that m — probed tonight at M = 56
(m = 28) both wholesale (e150 part A) and at the ThW0 level (e155).

[Status at first writing: conditional on H-FG6 + H-RW0.  BOTH
falsified as stated by e155 — see §3.5 for the corrected case
analysis; PARM-HALVE (§3.1) is unaffected and remains the frame.]

### 3.5 Revision after e155/e155b: the lattice law, the droppable
### completions, and the corrected theorem  [MACHINE-CHECKED inputs]

e155 (m = 24, 28, 32, 40; both halved windows W2e/W2o) + e155b (SAT
adjudication of every closure-alive pair) corrected both §3.2
hypotheses:

**(a) H-FG6 is FALSE, and its truth is a LATTICE law.**  Closure
stalls on the deep cluster (attacker pairs inside/near the CW zone) —
the known GAP-FG-deep phenomenon — and SAT adjudication shows the
TRUE escape set is:

    H-LAT(m): every SAT-alive attacker pair has gap ≡ 0 (mod 8)
              at m = 28, 32, 40   (mod 4 at m = 24),

in BOTH windows.  Contrapositive, the usable kill: any attacker
pair with gap ∉ 8ℤ is fan-dead, so a fan-safe attacker set is
contained in a SINGLE residue class mod 8 (mod 4 at m = 24).
Counts: closure-alive 66/63/77/75/71/61/82/79 → SAT-alive
46/44/48/48/36/32/48/48 at (m, window) over the grid; closure
misses only deep pairs, and SAT kills those with gap ∉ 4ℤ resp.
8ℤ.  This refines the full-scale "escapes have gap ≥ 16" of
notes/55 §5.3b into an exact congruence at half scale, and is
consistent with the full-scale escape data (all recorded full-scale
escape pairs — including the law-breaking g = M+8 = 56 at M = 48 —
have gap ≡ 0 mod 8 with attackers in one mod-8 class).  NEW input
for GAP-FG-schema: the object to classify is the mod-8 sublattice
recursion, not a distance threshold.

**(b) H-RW0 is FALSE exactly at completions {4, 6}.**  ThW0(m) is
UNSAT, and stays UNSAT after dropping any ONE completion group
EXCEPT i = 4 or i = 6 (m = 24, 32, 40, i.e. the m ≡ 0 (8) line); at
m = 28 (off-line) only i = 6 is droppable.  Two-drop SAT pairs
concentrate on {4, 6} accordingly.  In full-scale terms the fragile
guards are the odd completions c = 3M−9, 3M−13 (team A) and the
even c = 3M−8, 3M−12 (team B) — EXACTLY the values the L-LOP
frontier witness at M = 128 defects (§1.1: depths 133–141 ⊇
{3M−9, 3M−13}).  The machine's lopsided-arm escapes and the
crown's non-robust points are the same finite set of values.

**(c) Corrected case analysis for P-ARM.**  Under the hatch, for an
arbitrary band split:

  * **Case F** — some team's same-parity attacker share (A_e or
    B_o) contains a fan-dead pair: Th2 of that team dies
    (PARM-HALVE(b); no support caveat).  By H-LAT this covers every
    configuration where the share is NOT inside one mod-8 class.
    [Certificates: closure DAGs off the deep cluster; phase-split /
    SAT certificates on it (GAP-FG-deep).]
  * **Case S** — both shares mod-8-aligned (halved).  CW is 7
    consecutive values, so each share defects ≤ 1 crown completion
    per team; ≥ 6 of 7 crown guard groups fire in Th0 of BOTH
    teams.
      - **S1**: for some team the defected completion is ∉ {4, 6}
        (or no completion is defected): that team's Th0 dies by the
        punctured-ThW0 checks.  [machine, 4 half-scales]
      - **S2 (the corner — the honest residual gap)**: both teams'
        defected completions land in the droppable set — B_o's CW
        value ∈ {3M−9, 3M−13}, A_e's ∈ {3M−8, 3M−12} — and both
        shares are mod-8-aligned.  The crowns escape; the kill must
        come from the joint block theories.  P-ARM's machine UNSAT
        at 48/64/80/96 covers this corner per scale; its structure
        (a mod-8 lattice family with two marked defectors) is the
        quartet/quarter-scale-recursion species of E(M) (notes/56
        §4.2).  **GAP-PARM-CORNER** := uniformize this kill.

**Theorem P-ARM″ (corrected conditional form).**  H-LAT(m) +
(punctured-ThW0 off {4,6}) + a kill for the S2 corner ⟹ P-ARM(M).
The first two are machine-true at all tested scales with exact
finite statements; S2 is the scoped remainder, strictly smaller
than GAP-PARM (it fixes the coloring up to a mod-8 lattice family
with 2 marked values), and its species is shared with GAP-LLOP-α's
frontier (§1.1) — one corner, two arms.

**(d) Clique refinement — fan-safe shares have ≤ 4 members.**  A
fan-safe attacker share of size ≥ 2 must be a CLIQUE in the
SAT-alive pair graph (every pair inside it must escape).  Computed
max cliques of the e155b graphs:

    m=24: {65,69,77,93} (both windows)      m=28: {77,85,93,109}
    m=32: {96,104,112,128} (W2e) / {89,105,121} (W2o)
    m=40: {113,121,153} (both)

— size ≤ 4 at every tested (m, window), each an explicit mod-8
(mod-4 at 24) aligned family, with ≤ 1 member in the CW zone at
m ≥ 28.  So in Case S: |A_e|, |B_o| ≤ 4 (or ≤ 1), hence A_o resp.
B_e miss at most FOUR values of their class — the punctured-H1
robustness the corner needs is ≤ 4 spread punctures, not Θ(m/8),
and the corner colorings form an explicitly-listable finite family
per scale.  (Pairwise-clique is necessary, not sufficient — joint
triple fans can still kill inside a clique, which only shrinks the
corner further.  Compare notes/57 §0.2's α_c(M), the shallow-zone
version of the same quantity.)

[MACHINE-CHECK: data/e155_parm_hyp.log/.json (e155 + e155b);
crown-window arithmetic scripts in transcript.]

### 3.6 The residue probe at M = 56  [MACHINE-CHECKED]

e150 part A at M = 56 (m = 28 ≡ 4 mod 8, OFF the target line):
blocks {0,1} SAT, all six blocks **UNSAT** (0.1 s).  So P-ARM's
machine truth does NOT require M ≡ 0 (mod 16) — at 56 the parity
arm dies anyway, consistent with e155's finding that ThW0(28) is
UNSAT with only ONE droppable completion (i = 6, vs {4, 6} on the
line).  Exact residue statement: the mod-16 condition is a property
of the UNIFORM ThW0 proof line (m ≡ 0 (8), where the known
schema-search targets live and where the sharpness point m = 14
sits below threshold), not of the finite P-ARM verdicts; the
notes/55 residue ledger stands but the risk that P-ARM FAILS off-
line is reduced by this probe.

---

## 4.4 The robust chain verified at M = 128  [MACHINE-CHECKED]

With K_P = 68 = cap(128) + 1 and d₀ = 4:

    L-LOP(128):        min|Y| ≤ 67 dead                  (§1.1)
    DICH-U(128, 68):   UNSAT  0.9 s   (U forced pure)
    DICH-Z(128, 68, 4): UNSAT 0.2 s   (≤ 4 defectors forced)
    RP-ARM(128, 4):    UNSAT 10.0 s   (15.4M clauses; hatch + ≤ 4
                       free Z-defectors + free band + six theories)
    RP-ARM(48, d₀):    UNSAT for d₀ = 0, 2, 4, 8 (0.4–1.5 s);
                       d₀ = 0 audit reproduces e150 exactly
                       (blocks {0,1} SAT / full UNSAT).

So **Theorem COV-W′(128) holds**: every straddle-free (2,2,2)-
bounded coloring of CORE′(128) dies through fan / L-LOP / robust-P
— the first scale where the bridge is verified WITHOUT relying on
the exact-adjacency accident (K* = cap + 1), and the direct
confirmation that the notes/56 §4b designated fix works as designed.
The robust arm has real margin: 4 defectors at 128, ≥ 8 at 48.

[MACHINE-CHECK: data/e154_rparm.log/.json, data/e153_dich_probes.log,
data/e150_wholesale_M56.log.]

---

## 4. The robust parity arm: Lemma PH+ and the RP-ARM assembly

### 4.1 Lemma PH+ (quantitative parity hatch)  [PROVED]

For a 2-coloring χ call z ∈ P2 a *defector* (relative to a pure-U
orientation) if χ(z) equals the team owning z's parity class of P0.

**Lemma PH+.**  Let χ have |U_T| ≥ 1 for both teams and
Φ(χ) ≤ φ₀ < M + 7.  Then each parity class of P0 is monochromatic
with the two classes in opposite teams (the pure-U alignment, up to
swap), and the defector count is exactly D = 2Φ/M ≤ ⌊2φ₀/M⌋.

*Proof.*  (1) If P0 ∩ c meets both teams for a parity c, every
z ∈ P2 ∩ c shares a team with some u ∈ P0 ∩ c, contributing ≥ 1 to
Φ; |P2 ∩ even| = M+7, |P2 ∩ odd| = M+8, so Φ ≥ M+7 > φ₀ —
contradiction.  So each class is monochromatic.  (2) Same team for
both classes empties the other team's U — excluded.  (3) Under the
pure alignment, a value z ∈ P2 contributes |U_{χ(z)} ∩ (z mod 2)|
to Φ, which is M/2 if z defects and 0 otherwise; each P0 class has
exactly M/2 values.  Hence Φ = (M/2)·D.  ∎

(This is the exact quantization seen in every frontier witness:
Φ ∈ {48, 64, 120, 48, 56} = (M/2)·{2, 2, 3, 1, 1} at
M = 48..112.  Lemma PH is the case φ₀ = 0.)

### 4.2 The robust assembly, designed

Replace notes/56 §4b's P arm by the three machine lemmas (each per
scale, each a single instance; e153/e154):

    DICH-U(M, K):      fan-clean ∧ bounds ∧ straddle-free ∧
                       min|Y| ≥ K ∧ (U not purely aligned in either
                       orientation)                        — UNSAT?
    DICH-Z(M, K, d₀):  same, U pinned to orientation 1,
                       ≥ d₀ + 1 defectors                  — UNSAT?
    RP-ARM(M, d₀):     orientation-1 hatch with ≤ d₀ FREE defectors,
                       band free (≥ 2 each), straddles, all six
                       guarded block theories               — UNSAT?

**Theorem COV-W′(M) (schema).**  If L-LOP(M) holds at K_P − 1 ≤
cap(M), and DICH-U(M, K_P), DICH-Z(M, K_P, d₀), RP-ARM(M, d₀) are
all UNSAT, then every straddle-free (2,2,2)-bounded coloring of
CORE′(M) is order-infeasible: fan-monochromatic ones die by Lemma
DP; fan-clean ones with min|Y| ≤ K_P − 1 die by L-LOP; fan-clean
ones with min|Y| ≥ K_P have pure U (DICH-U; up to swap), ≤ d₀
defectors (DICH-Z), and then some block theory dies (RP-ARM, whose
instance space contains every such coloring after the swap
normalization — swap-invariance of every constraint family as in
notes/56 §4b).  [PROVED as a composition; the per-scale inputs are
machine lemmas.]

Against notes/56 §4b this differs ONLY in the P arm: Φ = 0 / exact
hatch is upgraded to ≤ d₀ defectors, absorbing the boundary zone
that the narrowing L/P overlap (§1) no longer covers.  RP-ARM keeps
straddle clauses and the (0,2,2) units — both vacuous at d₀ = 0 but
live for defectors (a defector's parity matches its team's U).

### 4.3 What the hand proof of RP-ARM will look like (design note)

The §3 proof survives d₀ defectors with two modifications: (i) a
defector z ∈ Z_A ∖ 2ℤ re-opens straddle constraints through odd
attackers u ∈ U_A — MORE constraints on the coloring, harmless for
the kill; (ii) the halved fan/crown theories lose the defected
values: Th2(A)'s halved window W2e gets ≤ d₀ punctures, and the
crown guard budget rises from 1 to at most 1 + d₀ compromised
completions ONLY IF defectors sit on crown-relevant values — but
crown guards are BAND values, which defectors are not; the actual
degradation is: (a) the fan closure refutations must survive ≤ d₀
punctures of W2e/W2o (robust H-FG6; the notes/55 §5.3 robustness
data: the top double fan survives 14 deletions), and (b) ThW0 is
untouched (its order block is P0, pinned; its guards are band
values).  So the conditional theorem of §3 should extend verbatim
with H-FG6 replaced by its d₀-punctured form — the reason to expect
RP-ARM to be no harder than P-ARM for small d₀.  [Design note; the
machine instances below are the authority.]

[Status: Lemma PH+ PROVED; COV-W′ composition PROVED given the
per-scale machine inputs; instances in flight.]

---

## 5. Machine queue (running log; sequential, one solver at a time)

1. e146 catalogue M=128 [running] → e152 L-LOP(128) K=66/67/68
   (predict UNSAT/UNSAT/SAT; cap 66) + witness anatomy at the SAT
   frontier;
2. e153 phi1(128) K=67, 68, ... → K*(128); hole iff K* > 68;
3. e156 D3 cross-checks (M=48, 64): lemma UNSAT + 3 controls;
4. e155 H-RW0 + H-FG6 at m = 24, 28, 32, 40, 48, 56, 64, 80;
5. e150 part A at M=56: the P-ARM residue probe (m = 28);
6. e153 upure/zdef(128, 67, d₀) → minimal d₀; e154 RP-ARM(48, 2)
   audit, then RP-ARM(128, d₀);
7. M=160 endgame: e146(160), e152(160) K=81/82/83, e153
   upure/zdef(160, K_P, d₀), e154 RP-ARM(160, d₀) — the possibly-
   hours queries; fallback = overlap-width law + conditional fix.
