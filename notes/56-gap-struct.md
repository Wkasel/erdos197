# 56 — GAP-STRUCT: the regime bridge as a coloring-level covering theorem

Companion to notes/55 (the N6a hand-proof skeleton; this note attacks
its §6.2 crux), notes/51 (locked schema), notes/54 (ledger/potential
style), notes/33 (C3 toolkit).  Everything from the proved layer of
notes/55 is used freely: Lemma U, A1–A9, Seesaw/Z′/D′, E2/C, P′, W,
PAR, FG-high, Theorem H, the frontier law (T1/T2 UNSAT at 48/64/80),
Lemma J.

**This note is written incrementally; every section ends with its
verification pointer and a status tag [PROVED] / [MACHINE-CHECKED] /
[GAP].**

**Overall status: `bridge machine-solved at 48/64/80/96 — GAP-STRUCT
reduced to three scoped uniformization gaps`.**  The notes/55 §6.2
crux ("every straddle-free coloring lands in the fan or lattice
regime") is now a three-case theorem (fan / lopsided / parity) with
per-scale machine certificates: the potential Φ (same-parity P0×P2
exposure) vanishes exactly on the PAR-alignment family (Lemma PH,
proved), fan-cleanness at band balance forces Φ = 0 (DICH, thresholds
K* = 26/35/42/51), band imbalance kills through the band-major team's
Th1 alone (L-LOP), and the Φ = 0 family with arbitrary mixed band is
dead wholesale (P-ARM).  See §5 for the updated gap ledger.

---

## 0. The reframing: death patterns and the covering statement

### 0.1 What GAP-STRUCT asks

notes/55 §6.2 leaves open the bridge: every straddle-free bounded
coloring of CORE′(M) must land in the fan regime R1 (some team's
double fan is refutable → R1–R4 closure / FG-high kills) or the
lattice regime R2 (parity/resonant alignment → PAR halving → Theorem
H / GAP-H1) — or admit a potential decreasing toward R2.  The
difficulty is that R1-death and R2-membership are properties of the
*coloring*, while the kills are *order* arguments; the two interact
through the guards (which units fire is decided by the coloring).

### 0.2 Death patterns

Fix M and the core CORE′(M) = P0 ∪ P1 ∪ P2 as in notes/55 §0.  For a
set S ⊆ CORE′(M) and a block index i ∈ {0, 1, 2}, define the
**S-restricted block-i theory** Th_i[S]: order variables on S ∩ P_i;
transitivity; and

* the AP-midpoint constraints (R1–R4 closure equivalent, i.e. the
  clause pair ¬(a≺b ∧ b≺c), ¬(c≺b ∧ b≺a)) for every AP (a, b, c)
  with a, b, c ∈ S ∩ P_i;
* the notes/55 §1.3 unit for every mixed AP whose *entire member set*
  lies in S and whose unit lives in block i — i.e. (0,0,1)-units for
  i = 0, (0,1,1)/(1,1,2)-units for i = 1, (0,2,2)/(1,2,2)-units for
  i = 2, each guarded by all three AP members being in S.

**Definition (death pattern).**  S is a *death pattern at scale M for
block i* iff Th_i[S] is unsatisfiable.

**Lemma DP.**  If S is a death pattern (for any block) and χ is the
coloring of a feasible state of CI(M), then S is not monochromatic
under χ.

*Proof.*  Suppose S ⊆ T for a team T of a feasible state.  By Lemma U
(notes/55 §1.3), Th_i(T) is consistent — some linear order ≺ of
T ∩ P_i satisfies all in-block AP constraints and all fired units of
block i.  Restrict ≺ to S ∩ P_i.  Every constraint of Th_i[S] is a
constraint of Th_i(T): an AP within S ∩ P_i is an AP within T ∩ P_i;
a mixed AP with all members in S ⊆ T has its unit fired in Th_i(T)
(the guard "all members in T" holds).  Transitivity is inherited by
restriction.  So Th_i[S] is consistent — contradiction.  ∎
[PROVED — pure restriction; no solver content.]

The three previously identified kill species are death patterns:

* **FG patterns** (block 2): S = {x₁, x₂} ∪ (P2-support of an R1–R4
  closure refutation of the double fan).  The minimal instance is the
  FG-high gadget: S = {4M−p, 4M−q} ∪ {4M+s, 4M+2p−3q, 4M+3p−4q,
  4M+5p−6q}, s = p−2q, for p ≥ 2q+1, 5p−6q ≤ 2M+15 (notes/55 §5.3b,
  PROVED).  Every one of the 1851 closure-dead pairs at M = 48
  yields such a pattern (its derivation-DAG value support).
* **J patterns** (block 1): S = R ∪ {4M+j : j ∈ F} for each of the
  36 minimal forbidden sets F of Lemma J (notes/55 §3.4): here the
  units used are β-units (1,1,2) with all members in S, and the AP
  constraints are within R ⊆ P1.
* **Crown/α patterns** (blocks 0/1): the finite A1/A2 families feed
  Th_0/Th_1 units; their inconsistent combinations (e.g. the halved
  crown core ThW0 of notes/55 §5.4c, whose support is U-material)
  are death patterns of block 0 resp. 1.

### 0.3 The covering statement (the bridge, reformulated)

**Proposition COV(M) (target).**  There is a finite catalogue 𝔇(M) of
death patterns such that every 2-coloring of CORE′(M) that is
(i) straddle-free for both teams and (ii) meets the (2,2,2) bounds
has a monochromatic member of 𝔇(M).

COV(M) + Lemma DP + the per-pattern certificates ⟹ Theorem N6a at
scale M: a feasible state's coloring would be straddle-free and
bounded (Lemma U), hence make some S ∈ 𝔇(M) monochromatic,
contradicting Lemma DP.  **COV(M) is exactly the GAP-STRUCT bridge in
finite form**: the catalogue's families ARE the regimes (FG patterns
= R1; the lattice-flavoured patterns that kill the fan-escaping
colorings = R2 and whatever third regime exists), and the covering
statement is the "every coloring lands somewhere" step, now a pure
coloring-combinatorics assertion with no order quantifier — the order
theory is quarantined inside the finitely many pattern certificates.

Existence of SOME catalogue is trivial at each scale (for every
straddle-free bounded χ, e135 + Lemma U give an inconsistent
Th_i(T); its value-support is a monochromatic death pattern; take
all of them).  The content is:

1. a SMALL catalogue, generated by named mechanisms (fan closure,
   Lemma J, crown), machine-verified pattern-by-pattern;
2. ADV(M) := SAT instance [coloring vars; straddle clauses; bounds;
   for each S ∈ 𝔇(M) and each team the clause "S not ⊆ T"] is
   UNSAT — this is the machine form of COV(M);
3. schema-stability of 𝔇(M) across M = 48, 64, 80 (offset-anchored
   families, like the notes/51 schema itself), so a uniform hand
   proof of COV(M) has a fixed finite shape to aim at.

The attack is CEGAR: seed 𝔇 with the known families; while ADV(M) is
SAT, take the escaping coloring χ, find an inconsistent block theory
Th_i(T) under χ (one exists, by the e135 lock + Lemma U), extract a
minimal unsatisfiable core, add its value-support as a new pattern.
Termination is guaranteed (each new pattern kills at least the
current witness; finitely many colorings); the question is whether
the discovered patterns organize into finitely many schematic
families — that answer, whatever it is, is the honest content of
GAP-STRUCT.

Status of this section: Lemma DP [PROVED]; COV(M) [GAP — the rest of
this note].

---

## 1. The seed catalogue 𝔇₀(48)  [MACHINE-CHECKED]

experiments/e146_dp_catalogue.py builds and validates the two known
families at M = 48:

* **FG patterns** — the full (q, p) grid 0 ≤ q < p ≤ M+15 (2016
  pairs): 1851 closure-dead (exactly the e142o count), 165 alive
  (the resonance region).  For each dead pair the derivation-DAG
  value support is extracted, independently re-validated by a direct
  SAT solve of Th₂[S] (order vars on S ∩ P2 + APs inside S + fan
  units of the in-S attackers), then greedily deletion-minimized —
  every deletion step re-validated.  Result: 1851 distinct minimized
  patterns, sizes 6–40 (median ≈ 12; 308 pairs reduce to exactly the
  six-value FG-high gadget {4M−p, 4M−q} ∪ 4M+{s, 2p−3q, 3p−4q,
  5p−6q}).
* **J patterns** — S = R ∪ {4M+j : j ∈ F} for the 36 minimal
  forbidden sets of Lemma J (e138 partB), each re-validated against
  Th₁[S] (APs inside R + β-units with completion in S): 36 patterns
  of sizes 18–19.

𝔇₀(48): 1887 validated death patterns.  Every validation is a
from-scratch SAT check of the notes/56 §0.2 definition — the closure
engine is only a generator, never trusted.

[MACHINE-CHECK: experiments/e146_dp_catalogue.py →
data/e146_catalogue_M48.json, data/e146_catalogue.log; 32 s.]

---

## 2. COV(48) HOLDS  [MACHINE-CHECKED] — and the third regime is now
## characterized

### 2.1 The CEGAR run

experiments/e147_adv_cegar.py: ADV(48) with the seed catalogue,
(2,2,2) bounds, WLOG χ(M+1) = A.  Loop: solve; on SAT evaluate all
six block theories of the witness (Lemma U form; assumption-selector
encoding), extract a deletion-minimized core from every UNSAT theory,
validate its value support against the §0.2 restricted-theory
definition (independent SAT check — asserted every time), add it as a
new pattern.

**Result: UNSAT after 170 iterations, 198 discovered patterns, 10 s
total.**  COV(48) holds with |𝔇(48)| = 2085.  Per-iteration
invariant confirmed 169/169 times: every straddle-free bounded
coloring the adversary produced had an UNSAT block theory (the e135
lock seen through Lemma U — the loop's assertion never fired).

Kill-block histogram over the 169 witnesses: block 1: 176, block 2:
14, block 0: 8.  The bridge's live content is overwhelmingly
**Th1 — the band theory** (α + β unit systems), not the fan theory:
the seed already saturates the fan regime, and the adversary's
escapes are band-placement games.

### 2.2 The essential catalogue E(48)

experiments/e148_essential.py: soften every pattern (one selector per
pattern guarding both monochromaticity clauses; straddle + bounds +
symmetry hard), assumption-core + deletion-minimization over the
2085 patterns.

**Result: E(48) has 191 patterns** (first core 802; minimized in
2 s / 384 solves):

| block | # | sources | anatomy |
|-------|---|---------|---------|
| 2 (fan) | 160 | all fg | 22 six-value FG-high gadgets + small closures ≤ 16; heavily parity-pure (fans surviving on one parity class) |
| 1 (band) | 28 | 3 J + 25 cegar | see below |
| 0 (crown) | 3 | cegar | ≈ one full parity class of P0 + 2–4 same-parity E1 values: the halved crown core ThW0 (H1-species) in situ |

Of Lemma J's 36 minimal forbidden sets only THREE are load-bearing:
J({1,2}), J({1,3}), J({2,4}).  The 25 cegar band patterns split into
two species:

* **α-lattice species**: {2–5 values of P0's top run} ∪ {a mod-2 or
  mod-4 class of the band} — pure α-unit kills, exactly the ThW1′
  (A2 α-geometry) family of notes/55 §5.4c, including MOD-4 class
  versions (offsets ≡ 0 mod 4: the quarter-scale recursion
  predicted by Lemma PAR's "higher lattice alignments halve once
  more");
* **αβ-mixed species**: {E1/band-bottom values, single parity} ∪
  {a few S3 values} — Lemma-J-flavoured β conflicts glued to α
  units, killing the band-heavy teams.

### 2.3 The third regime, seen in the witness stream

The 169 witnesses cluster by min-team band size:

* **Lopsided cluster** (min|Y| ≤ 18: 131 witnesses, incl. 57 at the
  (2, 62) extreme): one team band-dominant, the other band-starved
  but P0/P2-rich.  Killed by Th1 of the band-dominant team.
* **Balanced cluster** (min|Y| ≥ 28: 38 witnesses): **exactly the
  parity family of Lemma PAR with a mixed band** — U(A) = all odds
  of P0, U(B) = all evens, Z(A) = evens of P2, Z(B) = odds
  (pointwise, every single witness inspected), band split near
  parity with 1–4 defectors per team.  Killed by Th1 α+β patterns
  (and twice by Th0 crown patterns).

So the R3 interpolation of notes/55 §6.2 is EMPTY at the coloring
level at M = 48 in a precise sense: straddle pressure (Lemma W both
teams simultaneously) plus the fan catalogue leave only (i) lopsided
band splits and (ii) the P0/P2-parity-aligned family with band
mixing — and both die by finite Th1/Th0 patterns of the α/β/crown
species, i.e. by the SAME mechanism families that kill the exact
lattice alignments (the H1 block theories of notes/55 §5.4c).  The
"mixed ⟹ at least as dead" step that notes/55 §5.4 flagged as
missing is exactly what the 25 cegar band patterns certify at this
scale.

[MACHINE-CHECK: data/e147_cegar_M48.json/.log,
data/e148_essential_M48.json/.log.]

---

## 3. The potential and the dichotomy

### 3.1 The potential  [definition + PROVED structure lemma]

For a 2-coloring χ define

    Φ(χ)  :=  Σ_T  #{ (u, z) ∈ U_T × Z_T : u ≡ z (mod 2) }

— the *same-parity P0×P2 exposure mass*.  Φ is a pure coloring
quantity (no order, no arithmetic beyond parity); Lemma W(d)'s
parity hatch is exactly Φ = 0.  On the 169 CEGAR witnesses at
M = 48 the potential separates the two clusters PERFECTLY:

    balanced cluster (38 witnesses):   Φ = 0        (all of them)
    lopsided cluster (131 witnesses):  Φ ≥ 288      (all of them)

— no witness in (0, 288), and no witness with min|Y| in (18, 28).

**Lemma PH (parity-hatch structure).**  Let χ be a 2-coloring of
CORE′(M) with |U_T| ≥ 1 for both teams.  Then Φ(χ) = 0 if and only
if, up to team swap,

    U_A = odds of P0,  U_B = evens of P0,
    Z_A = evens of P2,  Z_B = odds of P2,

i.e. χ restricted to P0 ∪ P2 is EXACTLY the complementary parity
family of Lemma PAR (band unconstrained).

*Proof.*  (⇐) A same-parity pair (u, z) in one team would pair an
odd with an odd or an even with an even inside a team; by
construction every team's U and Z have opposite parities.  (⇒) Fix a
parity c.  P2 ∩ c ≠ ∅ (it has ≥ M values).  If u, u′ ∈ P0 ∩ c lay
in different teams, any z ∈ P2 ∩ c would share a team with one of
them — a same-parity in-team pair, so Φ ≥ 1.  Hence P0 ∩ c is
monochromatic, say ⊆ T_c; and any z ∈ P2 ∩ c in T_c would give
Φ ≥ 1 (P0 ∩ c ≠ ∅), so P2 ∩ c ⊆ T_c′.  If T_odd = T_even, the other
team's U would be empty, against the bounds; so T_odd ≠ T_even,
which is the displayed structure up to swap.  ∎  [PROVED]

### 3.2 The dichotomy, stated

**Proposition DICH(M) (machine form; the CLAIM-B bridge).**  Let χ
be straddle-free, meet the (2,2,2) bounds, and contain no
monochromatic block-2 (fan) pattern of 𝔇(M) ["fan-clean"].  Then

    min_T |Y_T|  ≥  K*(M)   ⟹   Φ(χ) = 0,

for a threshold K*(M); by Lemma PH the conclusion says χ|_{P0∪P2}
is the PAR alignment.  Equivalently: ADV_fan(M) ∧ (min|Y| ≥ K*) ∧
(Φ ≥ 1) is UNSAT.  [experiments/e149_dichotomy.py sweeps K and
certifies the threshold; results in §3.3.]

With DICH, the covering theorem COV(M) organizes into the case
analysis the notes/55 §6.2 bridge asked for:

* **Case F (fan regime = R1).**  Some team monochromatizes a fan
  pattern: dead by the FG-high gadget / closure certificates.
* **Case L (lopsided regime).**  Fan-clean and min|Y| ≤ K*(M) − 1:
  one team's band holds ≥ |P1| − K* + 1 values; dead by the
  lopsided-band Th1 patterns (α/β species on the band-major team).
* **Case P (parity regime = R2).**  Fan-clean and min|Y| ≥ K*(M):
  Φ = 0 by DICH, so χ|_{P0∪P2} is the PAR alignment with a mixed
  band; dead by the class-local Th1/Th0 patterns (α-lattice, β/J,
  crown — the H1 species), which contain Lemma PAR + Theorem H as
  the fully-aligned special case.

The task-prompt's "potential low → fan kill / potential high →
lattice forced" is realized with Φ inverted: Φ > 0 (exposure) can
only be sustained by fan-vulnerable or lopsided colorings; at band
balance the fan catalogue plus straddle-freeness EXTINGUISH the
exposure entirely, collapsing the coloring onto the lattice arm.

Status: Lemma PH [PROVED]; DICH(M) [MACHINE-CHECKED at the scales
of §3.3]; the uniform hand proof of DICH is part of GAP-COV (§5).

### 3.3 The threshold K*(M)  [MACHINE-CHECKED]

experiments/e149_dichotomy.py encodes Φ ≥ 1 (one selector per
same-parity P0×P2 pair, forced to imply same-team, plus their
disjunction) over the fan-clean base and sweeps K in min|Y| ≥ K.

    M = 48:  SAT at every K ≤ 25 (frontier witness at K = 25:
             Φ = 48, sizes A = [24, 25, 57], B = [24, 39, 54]);
             UNSAT at K = 26 — and at the balance cap K = 32.
             K*(48) = 26.
    M = 64:  SAT at every K ≤ 34 (frontier Φ = 64); UNSAT at 35
             and at the cap 40.   K*(64) = 35.
    M = 80:  SAT at every K ≤ 41 (frontier Φ = 120); UNSAT at 42
             and at the cap 48.   K*(80) = 42.
    M = 96:  SAT at every K ≤ 50 (frontier Φ = 48); UNSAT at 51
             and at the cap 56.   K*(96) = 51.

K* tracks the balance point (M+16)/2 at a bounded, mod-32-periodic
offset:

    K*(M) − (M+16)/2 = −6, −5, −6, −5   at M = 48, 64, 80, 96,

i.e. −6 on M ≡ 16 (mod 32) and −5 on M ≡ 0 (mod 32) over the data.
Below K* the frontier witnesses' Φ decays toward the threshold
(Φ = 48, 32–64, 80–120, 48 near the frontier) — the exposure mass is
squeezed out, then vanishes.

Sharpness: the K = 25 frontier witness keeps both U's parity-pure
(24 odd vs 24 even) and leaks its Φ = 48 through a handful of
same-parity P2 values — the hatch fails only marginally below the
threshold.  (Bug record, for honesty: a first version of e149 reused
one `top_id` for the two cardinality encoders, colliding their
auxiliary variables and yielding a spurious K* = 2; the contradiction
with the CEGAR witness stream — fan-clean witnesses with Φ ≥ 288 at
min|Y| = 3 — exposed it.  The witness stream is the regression test.)

---

## 4. Scale stability: COV holds at 48, 64, 80 and the essential
## catalogue is one fixed family system

### 4.1 The runs

| M | seed 𝔇₀ | CEGAR iterations | discovered | verdict | E(M) |
|---|---------|------------------|------------|---------|------|
| 48 | 1887 (1851 fg + 36 J) | 170 | 198 | **UNSAT** | 191 |
| 64 | 3018 (2982 fg + 36 J) | 800 + 89 (resumed) | 929 | **UNSAT** | 219 |
| 80 | 4596 (4560 fg + 36 J) | interrupted (3290 + 756 + 764 over three runs) | 5888 (archived in e147_cegar_M80.json for resume) | interrupted — superseded by §4b (COV-W(80) holds) | — |

Every discovered pattern was validated on the spot against the §0.2
restricted-theory definition (assertion in the loop, never fired);
the witness-must-die invariant (some block theory UNSAT — the e135
lock through Lemma U) held at every single iteration at every scale.

At M = 80 the per-pattern loop entered a slow grind inside ONE
witness family (the lopsided cluster: band split ≈ 8/88, the
adversary permuting which ≈ 10 band + ≈ 50 P2 values the band-major
team sheds; thousands of minimal patterns).  That grind is what
motivated the WHOLESALE reformulation of §4b, which kills each arm
with a single hybrid instance instead of a pattern stream; the M = 80
pattern run is kept alive in the background purely as the exhaustive
record (its verdict is subsumed by §4b).

### 4.2 The essential catalogue's family system (48 vs 64)

E(M) splits into FIVE schematic families, stable across scales:

| family | block | E(48) | E(64) | shape |
|--------|-------|-------|-------|-------|
| **F** (fan) | 2 | 160 | 191 | attacker pair + closure support; 159/160 resp. 190/191 parity-pure; 6-value FG-high gadgets + closures ≤ 30 (a handful of deep-pair supports 52–77) |
| **J** (top-run) | 1 | 3 | 3 | THE SAME three: J({1,2}), J({1,3}), J({2,4}) at both scales |
| **α** (band lattice) | 1 | 19 | 15 | 2–7 P0-top attackers (values 2M−k, k ≤ 29) + most of one band parity class; ALL parity-pure |
| — incl. the **mod-4 quartet** | 1 | 4 | 4 | exactly four patterns, one per mod-4 class of the band: 3 P0-top attackers + a mod-4 band class (the quarter-scale crown, see below) |
| **β** (generalized J) | 1 | 6 | 6 | single-parity band material + 2–8 S3 completions, no P0 guards; ALL parity-pure |
| **crown** | 0 | 3 | 4 | ≈ one parity class of P0 + 2–7 same-parity E1 values (the ThW0 halved-crown core in situ); ALL parity-pure |

Parity-purity is near-total across the whole of E(M): the essential
death of the coloring space is CLASS-LOCAL, matching the halving
recursion of Lemma PAR — each pattern lives on one arithmetic
lattice, and the covering statement gathers the lattices.

**The mod-4 quartet, halved by hand (example of the species).**  At
M = 64 the four patterns are, in offsets from 4M,
{−139,−135,−131} ∪ {−79, −75, …, −3} and its three mod-4 shifts.
Take the ≡ 0 (mod 4) member; every value is divisible by 4, and the
quarter-scale map v ↦ v/4 (twice the notes/33 Lemma H halving)
carries its restricted theory Th₁[S] to: an AP-free order of a
16-interval + the α-units of three attackers at distance
{2m′−k} below it — a crown/ThW1′ core at quarter scale, the
notes/55 §5.4c species on the line m′ = M/4.  The quartet is the
machine's rediscovery, inside the essential catalogue, of the
"higher lattice alignments halve once more" prediction of Lemma
PAR — now with the exact finite instances named.

[MACHINE-CHECK: data/e148_essential_M48.json, _M64.json; every
pattern's restricted theory independently SAT-validated.]

---

## 4b. The wholesale form: two hybrid lemmas close the two non-fan
## arms at ALL THREE SCALES  [MACHINE-CHECKED]

The pattern catalogue finitizes the order theory one MUS at a time;
the better cut (e150) kills each arm with ONE hybrid
coloring-plus-order instance.

**Lemma L-LOP(M) (lopsided arm).**  The instance

    coloring vars on CORE′(M);  straddle-freeness (both teams);
    (2,2,2) bounds;  no monochromatic fan pattern;
    |Y_A| ≤ K − 1        [so |Y_B| ≥ M + 17 − K: B is band-major];
    Th1(B) as a guarded order theory (order vars on P1;
        in-band APs, α-units, β-units, each guarded by the
        B-membership of its member set; transitivity)

is UNSAT — the band-major team's band theory alone is inconsistent —
for every K up to:

    M = 48: K ≤ 30  (band-major size ≥ 35 of 64 kills)    0.2–0.4 s
    M = 64: K ≤ 37  (band-major size ≥ 44 of 80 kills)    0.4–0.9 s
    M = 80: K ≤ 45  (band-major size ≥ 52 of 96 kills)    1.0–2.4 s
    M = 96: K ≤ 52  (band-major size ≥ 61 of 112 kills)   1.7–3.2 s

with SAT one step above each cap (sharp).  By team-swap symmetry the
lemma reads: min|Y| ≤ K − 1 ⟹ the band-major team's Th1 is
inconsistent ⟹ the coloring is infeasible (Lemma U).

**Lemma P-ARM(M) (parity arm).**  Under the parity hatch — P0/P2
pinned to the Lemma-PH alignment (U_A = odds of P0, U_B = evens,
Z_A = evens of P2, Z_B = odds; WLOG by swap), band coloring FREE
(≥ 2 per team) — the six guarded block theories (blocks 0, 1, 2 ×
both teams; straddles are vacuous under the hatch, §5.4 of notes/55)
are jointly inconsistent:

    M = 48: UNSAT 0.1 s    M = 64: UNSAT ~1 s
    M = 80: UNSAT ~2 s     M = 96: UNSAT 0.9 s (1.7M clauses)

Moreover blocks {0, 1} alone are SAT at all four scales: the
block-2 (fan/A6) layer is genuinely load-bearing in the parity arm —
matching the anatomy of the aligned special cases (alignment (i)
dies through Th2's even FG-gadget, alignment (ii) through
Th0/Th1 = H1's two theories).  P-ARM is exactly the notes/55 §5.4
"mixed band ⟹ at least as dead" statement, now a single machine
lemma per scale instead of a conjecture.

**Theorem COV-W(M), M ∈ {48, 64, 80, 96}  [MACHINE-CHECKED].**  Every
straddle-free 2-coloring of CORE′(M) meeting the (2,2,2) bounds is
order-infeasible, by the three-case analysis:

    F  (fan):      some team monochromatizes a fan pattern
                   → Th2 dies (FG-high [PROVED] / closure DAGs);
    L  (lopsided): fan-clean, min|Y| ≤ K*(M) − 1
                   → Th1(band-major) dies            [L-LOP(M)];
    P  (parity):   fan-clean, min|Y| ≥ K*(M)
                   → Φ = 0                            [DICH(M), e149]
                   → P0/P2 = the PAR alignment        [Lemma PH]
                   → the six theories die             [P-ARM(M)].

The case split is exhaustive because K*(M) − 1 ≤ L-LOP's cap at all
four scales, with overlap width 4 / 2 / 3 / 1 (48 / 64 / 80 / 96):
26–29, 35–36, 42–44, {51} are covered by BOTH arms.

**GAP-ASM′ warning (the honest trend).**  The L-LOP cap drifts
against balance (−3, −4, −4, −5) while K* holds at −6/−5: the
overlap narrows by ≈ 1 per 32 in M and would hit width 0 near
M = 128 (still exhaustive) and could go NEGATIVE near M = 160,
opening a middle zone covered by neither wholesale arm.  Two levers
were probed at M = 96 and do NOT move the thresholds: (i) adding the
36 J patterns to the DICH hypothesis leaves K* = 51 (still SAT at
K = 50); (ii) adding the band-minor team's Th1 to L-LOP leaves the
cap at 52 (still SAT at K = 53).  So the boundary-zone kills
genuinely need the block-0/2 layers, and the natural fix for large
M is a ROBUST P-ARM: replace Φ = 0 by Φ ≤ φ₀ (a bounded number of
hatch defectors, quantified in the instance) so the parity arm
absorbs the boundary zone.  This is the concrete content of
GAP-ASM′ going forward; at the four verified scales the present
split suffices.  With Lemma U and Lemma DP this is
Theorem N6a at each scale, re-proved through the structured bridge —
i.e. GAP-STRUCT's bridge exists and is machine-certified at
48/64/80.

*Soundness of the composition.*  (F) A monochromatic fan pattern
makes Th₂(T) inconsistent by Lemma DP's restriction argument.
(L) L-LOP's instance existentially quantifies the coloring and the
band-major team's Th1 order; its UNSAT says no such coloring has
Th1(band-major) consistent; a fan-clean bounded straddle-free χ with
min|Y| ≤ K − 1 is (after the WLOG swap) inside the instance space,
so ITS Th1(band-major) is inconsistent.  (P) DICH's UNSAT says every
fan-clean bounded straddle-free coloring with min|Y| ≥ K* has
Φ = 0; Lemma PH pins χ|_{P0∪P2} up to swap; P-ARM's instance
quantifies over ALL band splits above the pinned P0/P2, so its
UNSAT covers χ's own split: some block theory of χ is inconsistent.
In each case Lemma U converts the inconsistent block theory into
infeasibility of any state over χ.  The two pinnings of Lemma PH
are exchanged by the team swap, under which every constraint family
of every instance here is invariant.

[MACHINE-CHECK: experiments/e150_wholesale.py →
data/e150_wholesale_M{48,64,80}.json/.log; experiments/
e149_dichotomy.py → data/e149_dichotomy_M{48,64,80}.json/.log.
Independent cross-checks: a real M = 64 lopsided CEGAR witness's
band-major Th1 re-verified UNSAT through the e147 theory evaluator
(different encoding path than e150); random hatch-band colorings die
in multiple block theories at once through the same evaluator.]

---

## 5. Status, the new gap decomposition, and what remains

### 5.1 What this note establishes

1. **Lemma DP** [PROVED]: monochromatic death patterns are forbidden
   for feasible-state colorings (restriction of Lemma U).
2. **COV(48), COV(64)** [MACHINE-CHECKED, pattern form]: the CEGAR
   loop terminates UNSAT; essential catalogues E(48) = 191,
   E(64) = 219 patterns in five schematic families (fan, J, α, β,
   crown), near-totally parity-pure, with the SAME three J patterns
   and the SAME mod-4 quartet structure at both scales.
3. **Lemma PH** [PROVED]: Φ = 0 ⟺ χ|_{P0∪P2} is the PAR alignment.
4. **DICH(M)** [MACHINE-CHECKED at 48/64/80/96]: fan-clean ∧
   min|Y| ≥ K*(M) ⟹ Φ = 0; K* = 26/35/42/51 = (M+16)/2 − 6
   resp. − 5 by M mod 32, sharp.
5. **L-LOP(M)** [MACHINE-CHECKED at 48/64/80/96]: fan-clean ∧
   min|Y| ≤ 29/36/44/51 ⟹ the band-major team's Th1 alone is
   inconsistent; sharp one step above.
6. **P-ARM(M)** [MACHINE-CHECKED at 48/64/80/96]: the parity hatch with
   FREE band is dead through the six guarded block theories — the
   notes/55 "mixed ⟹ at least as dead" statement.
7. **Theorem COV-W(M)** [MACHINE-CHECKED at 48/64/80/96]: 4 + 5 +
   6 + the fan certificates cover every straddle-free (2,2,2)-
   bounded coloring, with overlap widths 4/2/3/1 between the L and
   P arms.
   Via Lemma U this re-proves Theorem N6a at each scale THROUGH THE
   STRUCTURED BRIDGE — the e135 monolithic lock is no longer the
   only route.

### 5.2 GAP-STRUCT: the replacement ledger

The notes/55 §7 row

    GAP-STRUCT | R3 → R1∪R2 bridge ... | genuinely open | HIGH

is replaced by the scoped decomposition (jointly: **GAP-COV**):

| gap | statement to uniformize (machine-true at 48/64/80/96) | species | risk |
|-----|-----------------------------------------------------|---------|------|
| GAP-DICH | fan-clean ∧ min\|Y\| ≥ K*(M) ⟹ Φ = 0, with K*(M) = (M+16)/2 − 6/−5 by M mod 32 | counting: Lemma-W windows + fan geometry vs exposure mass; the frontier witnesses' Φ decays linearly to 0 | medium |
| GAP-LLOP | band-major (≥ (M+16) − K* + 1 band values) ⟹ Th1 inconsistent | α/β/J order geometry on a co-bounded band subset; H1-ThW1′ + Lemma-J species with phase machinery | medium |
| GAP-PARM | parity hatch + any band mixing ⟹ some block theory inconsistent | halving recursion with a mixed band; CONTAINS GAP-H1 (alignment (ii) is its band-aligned special case) | medium (≥ GAP-H1) |
| GAP-ASM′ | the three thresholds overlap for all M ≡ 0 (16), M ≥ 48 | arithmetic of K*(M) and the L-LOP cap (both track (M+16)/2 with O(1), mod-32-periodic offsets); the overlap NARROWS ≈ 1 per 32 in M (4/2/3/1 at 48–96) — for large M the robust-P-ARM (Φ ≤ φ₀) strengthening is the designated fix (§4b warning) | medium-low (upgraded from low after the M = 96 trend) |

Honest accounting: GAP-PARM subsumes GAP-H1, so the total gap count
of the program does not decrease by this note alone — but the crux
changes character completely.  Before: "we do not know WHY general
colorings fall into the regimes" (no statement to prove).  After:
three concrete, scoped, machine-true-at-three-scales statements with
sharp thresholds and named species, each with exact finite
certificates to mine (the e149/e150 instances are small; their MUSes
are the natural seeds for the uniform schemas).  The pattern-level
COV runs additionally supply the exhaustive kill catalogue (E(M))
whose family structure the uniform proof must reproduce.

### 5.3 Next steps (ranked)

1. **GAP-ASM′ data**: DONE at M = 96 (K* = 51, cap 52→51, P-ARM
   UNSAT; overlap width 1).  Next: M = 112/128 to confirm the
   mod-32 offset laws and the narrowing trend, and prototype the
   robust P-ARM (Φ ≤ φ₀) that removes the trend's risk.
2. **GAP-DICH schema**: MUS-mine the e149 UNSAT at K* (which fan
   patterns + straddle windows are load-bearing?); candidate hand
   shape — the FORCED-INTERVAL mechanism.  The frontier witnesses
   are already U-hatched (both U's parity-pure); the last exposure
   is a Z-defector z ∈ Z_T of U_T's parity.  Straddle-freeness then
   forces the midpoint set Mid(U_T, z) = {(u+z)/2 : u ∈ U_T} into
   Y_T′, and because U_T is a full parity class (an arithmetic
   progression of step 2), Mid(U_T, z) ∩ P1 is an arithmetic
   progression of STEP 1 — an interval.  For a high defector
   (z ≥ 5M−31) the interval has length |U_T| = M/2: the other team
   is forced to own a length-M/2 CONTIGUOUS band interval, which
   saturates the close-pair fan geometry (every pair at distance
   ≤ 15 is closure-dead, notes/55 §5.3b) and collides with
   |Y_T| ≥ K* — a Lemma-W + FG-high counting argument whose
   threshold arithmetic should reproduce K*(M) ≈ (M+16)/2 − 6.
   Low defectors (z < 5M−31) force shorter intervals but sit inside
   the FG-gadget support zone of T's own fans; U-defectors are the
   mirror case.
   MUS DATA (e151 at M = 48, K = K* = 26; deterministic deletion
   minimization, 1157 of 4395 soft constraints): the load-bearing
   fans are 305 pairs, EVERY ONE with a same-parity attacker pair
   (parities (0,0): 142, (1,1): 163 — all gaps even, decaying from
   gap 2), i.e. exactly the class-local fans; the load-bearing
   straddles are 852 triples concentrated on low attackers
   (u ≤ M+32: 590), band-edge midpoints (y ∈ E1: 392) and
   bottom-of-P2 completions (z ≤ 4M+32: 510) — the Lemma-A7(d)
   family.  So the uniform GAP-DICH proof should live INSIDE one
   parity class at half scale: same-class fans + E1→S3 straddle
   exclusions vs the exposure mass.  data/e151_dich_mus_M48.log.
3. **GAP-PARM schema**: the band-mixing recursion — notes/33 Lemma H
   halving applied classwise with the band split as the new
   coloring; its aligned boundary cases are Theorem H (proved) and
   GAP-H1 (open); the machine says the interpolation is dead at
   three scales.
4. **GAP-LLOP schema**: robust Lemma-J/α-family argument on
   co-bounded band subsets (the co-boundedness K* − 1 ≈ M/2 − 5 is
   large, so this is a genuinely robust version of the J/ThW1′
   kills).
5. The M = 80 exhaustive pattern run (archived at 5888 patterns;
   resume optional via e147's resume support) and E(80) — the
   catalogue record only; COV(80) already holds via §4b.

### 5.4 Relation to the notes/54 ledger style

The task brief suggested a notes/54-style potential/ledger argument;
Φ is exactly such a ledger quantity, but the discovered structure is
a THRESHOLD dichotomy, not a descent: no pass-the-parcel decreasing
sequence was needed, because at balance the exposure doesn't shrink
step by step — it is EXTINGUISHED outright by fan-cleanness
(K* sharp, frontier Φ linear in the last few K).  The notes/54
"strictly-decreasing potential step toward R2" is thus realized in
degenerate form: one step, from Φ ≥ 1 to Φ = 0.

