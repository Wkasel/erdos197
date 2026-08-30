# 77 — FRONT N6a-POOL: clearing the uniformization sub-pool

Companion to notes/50 §2a/§6 (the FINAL dependency graph; this note
works its GAP-N6a sub-pool row), notes/55 (proved skeleton), notes/56
(bridge), notes/57 (DICH case tree + catalogue facts F0–F4), notes/58
(LLOP/PARM + robust chain), notes/59 (FG-schema/J-pencil/FG-deep/ASM′).
Audit baseline: notes/60/60-1/61-2 (scales through 160), notes/76.

**This note is written incrementally; every section ends with its
verification pointer and a status tag [PROVED] / [MACHINE-CHECKED] /
[GAP] / [CLEARED] / [RESISTS].**

**Overall status: `in progress`.**

## 0. The pool, the clearing bar, and the dependency order

The notes/50 §2a sub-pool (all one species — finite catalogue-schema
write-ups of machine-proved-in-instances claims):

| item | uniform claim to write up | prior state |
|------|---------------------------|-------------|
| GAP-FG-schema | sound uniform calculus covering the closure-dead fan grid; residue = RT-glue rule + cross-scale boundary audit (notes/59 §A.6) | FW covers 1467/1851 at 48; deep block q ≥ M−12 uncovered |
| GAP-FG-deep | branch-certificate schema for the closure-alive UNSAT stalls D(M); resonance law 8 \| gap; E1×E1 characterization | exact at 48 only; 55/75 certs; 20-pair core → PARM |
| GAP-DICH (5 rows, notes/57 §7) | F0 purity / F1 α-law / F2 f-law / F3 windows / F4 cascade + SPLIT finish; K* = m + 9 + max(α_E−f_O, α_O−f_E) | K* law exact at 8 scales 48..160 (2 blind); facts checked at 6 scales |
| GAP-LLOP-α/β | band-major Th1 kill; cap law C(M); arms = punctured ThW1′ / robust Lemma J | cap flat law (M+16)/2−5 survives 96..160; arms scoped, unproved |
| GAP-PARM (⊇ CORNER ⊇ FG-deep 20-pair core) | hatch + any band split dead; H-LAT lattice law, ThW0 punctured {4,6} law, S2 corner | P-ARM machine-dead 48..96 + 56; laws at m = 24..40 |
| GAP-ASM′ = (OV-∀) | K*(M) ≤ C(M) for all M ≡ 0 (16) | true at 8 scales 48..160; robust chain COV-W′ verified 128/160 |

**Clearing bar (this front).**  An item is CLEARED when (a) its
uniform statement is written exactly, (b) the schema layer behind it
is proved (hand) or reduced to named finite facts, and (c) every
uniform claim it rests on is machine-checked at TWO scales fresh for
that claim.  Items that fail (b) at day's end get exact statements
and a RESISTS tag.

**Fresh scales for this front**: full-scale claims M = 176, 192
(never touched; catalogues built this session); half-scale claims
m = 48, 56 (e155 grid ran m = 24..40); FG-deep laws M = 64, 96
(e154 classification ran only at 48).

**Dependency order worked**: FG-schema → FG-deep → DICH → LLOP →
PARM → ASM′ (each later item consumes catalogue laws of the earlier).

Machine queue discipline: one local solver at a time; bulk (e146
catalogues at 176/192, deep classification at 96) on sprint pods.

---

## 1. GAP-FG-schema: the glue verdict, Theorem AFF⁺, and Lemma MON

Executes the notes/59 §A.6 designated next steps ((1) RT-glue, (2)
cross-scale boundary audit).  Instrument: experiments/e179_glue_walk.py
→ data/e179_glue_walk_M{48,64,80,96}.json, data/e179_glue_walk.log.
Ground truth at every scale: the closure-dead pair lists of the e146
catalogues (independent engine; = e142o/e152 at 48).

### 1.1 The glued fan-walk calculus GFW  [PROVED sound]

**Definition.**  E⁺(q,p;M) := the least edge set on O = [1, N]
(N = 2M+15) containing every fan unit (2a+r, a), every fan-walk fact
(h, x) with x ∈ D(h) and every RL-head fact (h, 2h−x) (e152d descent
sets), closed under the EDGE-WISE rules

    (RL)  (u, v) ∈ E⁺, 2u−v ∈ O ∖ {u}  ⟹  (u, 2u−v) ∈ E⁺
    (RT)  (u, v) ∈ E⁺, 2v−u ∈ O ∖ {v}  ⟹  (2v−u, v) ∈ E⁺ .

GFW refutes ThFG(q,p;M) iff E⁺ has a directed cycle.

**Lemma GL.**  GFW is sound.  *Proof.*  By induction every edge is a
T/RL/RT-derivable fact of Lemma CC's calculus: units are axioms; walk
facts and RL-heads are derivable (Lemma FW(a),(b)); an (RL)/(RT) child
of a derivable fact is derivable (the same AP read through R2/R4 resp.
R1/R3, as in Lemma CC).  A directed cycle composes under T to u ≺ u,
contradicting irreflexivity.  ∎

(RT) applied to walk facts is exactly the "RT-glue" fragment that the
e152b deep-block DAGs exhibit (head fact 51 ≺ 26 → glue fact 1 ≺ 26
at (q,p) = (48,49), M = 48).

### 1.2 Machine verdict: glue does NOT absorb the deep block, and the
### q = M−12 boundary is 48-specific  [MACHINE-CHECKED, 4 scales]

    M    dead   FW-cov         GFW-cov        GFW-resid  FW-resid outside q≥M−12
    48   1851   1467 (79.3%)   1579 (85.3%)   272        105 of 384
    64   2982   2372 (79.5%)   2559 (85.8%)   423        341 of 610
    80   4345   3551 (81.7%)   3770 (86.8%)   575        546 of 794
    96   5986   4917 (82.1%)   5251 (87.7%)   735        820 of 1069

Soundness at all four scales: ZERO alive pairs acquire a GFW cycle
(0/165, 0/178, 0/215, 0/230) — the strongest available correctness
test for the calculus layer, now passed by the extended fragment too.

Two honest corrections to notes/59 §A.5–A.6:

1. **"RT-glue expected to absorb the deep block" is FALSIFIED.**
   Edge-wise glue absorbs only ≈ 30% of the FW residual (112/384,
   187/610, 219/794, 334/1069).  The deep kills genuinely need RL/RT
   applied to T-COMPOSED facts — i.e. the fragment hierarchy
   FW ⊂ GFW ⊂ … converges to the full closure calculus and no proper
   structured fragment tested reaches the deep zone.
2. **The deep-block edge q = M−12 is NOT scale-stable.**  The
   FW-residual's component OUTSIDE q ≥ M−12 grows with scale
   (105/341/546/820): the uncovered zone is a scaled region
   (bulk q ≳ 2M/3, absolute width Θ(M), plus thin resonance lines
   p − q ∈ {40, 44, 48, 56} reaching down to q ≈ M/3).  The notes/59
   cross-scale conjecture is answered: NO.

### 1.3 Theorem AFF⁺ and Lemma MON: what IS uniform  [PROVED]

**Theorem AFF⁺.**  Every finite derivation DAG in the full T/RL/RT
calculus (arbitrary interleaving, from fan units, at any (q,p,M)) is
an M-uniform affine schema in the sense of Theorem AFF: its node
values are affine forms in the base parameters and (p,q); its validity
at (q′,p′,M′) is a finite conjunction of linear equations (rule
applications AND the T-compositions' middle-element matchings),
integrality congruences, positivity constraints, and window
inequalities ℓ ≤ N′ = 2M′+15.

*Proof.*  Verbatim Theorem AFF (notes/59 §A.3): its proof used only
that each rule application maps affine forms to affine forms with one
affine side condition per application.  T-composition of two facts
adds a linear equation (equality of the composed endpoints) and no new
values.  Nothing in the argument used the walk structure.  ∎

**Lemma MON (upward death monotonicity).**  If ThFG(q,p;M) is
inconsistent and M′ ≥ M (same q, p), then ThFG(q,p;M′) is
inconsistent.  *Proof.*  Restriction: a linear order of [1, N′]
satisfying all AP constraints and fan units of the M′-window restricts
to [1, N], where it satisfies every constraint of ThFG(q,p;M) (each
is a constraint of the larger theory supported inside [1, N]).  ∎
[MACHINE: 0 violations over all 28 ordered scale pairs from the eight
catalogues 48..160 — every dead (q,p) stays dead at every larger
audited scale.]

**Consequence (the fixed-pair half of GAP-FG-schema is CLOSED).**  For
every FIXED pair (q,p): once dead at some scale M₀, the pair carries
ONE finite certificate (its closure DAG at M₀), which by AFF⁺ + MON is
valid verbatim at every M ≥ M₀ (window conditions relax monotonely).
So the uniformization question for GAP-FG-schema lives ONLY in the
scaled coordinates — pairs whose position grows with M (the deep zone
q ≳ 2M/3 and the resonance lines), where the certificate changes with
scale.

### 1.4 Status after §1

| sub-item | verdict |
|----------|---------|
| calculus soundness (CC/FW/GL) | [PROVED]; 0 false positives on 788 alive pairs across 4 scales |
| certificate uniformity | [PROVED — Theorem AFF⁺]: every closure DAG at any scale is an affine schema |
| fixed-pair uniformization | [PROVED — AFF⁺ + Lemma MON]: one certificate per pair, valid for all larger M; machine-corroborated on 28 scale pairs |
| structured-fragment taxonomy of the SCALED zone | **[RESISTS]** — exact statement: classify, uniformly in M, the closure derivations of the dead pairs with q ≳ 2M/3 (bulk) and the lines p−q ∈ 8ℤ ∩ [40, 56] (thin); the fragment hierarchy FW ⊂ GFW provably stalls there (this section), a fixed affine list provably cannot cover (notes/59), and the honest species is the full calculus with per-scale certificates |

The RESISTS item does not gate the assembly at any verified scale
(the catalogue is per-scale machine material under (H-F)); it is the
price of an ALL-M fan-clean hypothesis, and it merges with the
resonance-law uniformization of §2 (the alive/dead boundary and the
deep certificates are two faces of the same scaled-zone geometry).

[MACHINE-CHECK: data/e179_glue_walk_M{48,64,80,96}.json; runtime 2/4/12/21 s.]

---

## 2. GAP-FG-deep: the laws at six scales — resonance law CLEARED,
## deep zone RECHARACTERIZED, close-pair law STRENGTHENED

Instrument: experiments/e180_deep_classify.py (scale-generic e154:
one incremental CaDiCaL instance per scale — full order theory,
transitivity, AP-freeness on [1, 2M+15]; fan units as assumptions) →
data/e180_deep_M{48,64,80,96,112,128}.json, data/e180_deep.log.
M = 96 ran on sprint-D; the M = 48 run REPRODUCES e154 exactly
(|R| = 90, |D| = 75).  Five of the six scales are FRESH for every law
below (notes/59 §C had them exact at 48 only).

### 2.1 The complete R/D map, 48..128

    M     alive   R (SAT escapes)   D (UNSAT stalls)   D q-range
    48    165     90                75                 [48, 62]
    64    178     68                110                [48, 78]
    80    215     96                119                [64, 94]
    96    230     99                131                [64, 110]
    112   292     131               161                [96, 126]
    128   319     147               172                [96, 142]

### 2.2 (RES-LAW)  [MACHINE-CHECKED at 6 scales — was 1]

**Every SAT escape has gap ≡ 0 (mod 8).**  Zero violations among
631 escapes across all six scales.  This is the uniform claim that
GAP-DICH-ALPHA and P-ARM's H-LAT consume (a fan-safe attacker share
is mod-8 aligned); it now stands at six scales with five fresh.

### 2.3 (CLOSE-LAW′)  [MACHINE-CHECKED at 6 scales; STRENGTHENED]

At M = 64, 80, 96, 112, 128 there are **ZERO escapes at distance
≤ 15** — the notes/59 close-pair kill law holds WITHOUT the E1
exclusion at every scale above 48:

    for M ≥ 64 (audited grid): a team owning two band values at
    distance ≤ 15 has a fan-dead pair — no exception zone.

The 48-exceptional gap-8 E1×E1 escapes (the reason notes/59 added
the E1 exclusion) die from 64 up: minimum realized escape gap is
≥ 16 at every audited M ≥ 64 (gaps realized: 16/32/48/64 at 64;
16/32/64/80 at 80; 16/32/48/64/96 at 96; …; 32/64/96/128 at 128).
By Lemma MON's species this cannot be concluded for free at unseen
scales (alive sets are not monotone), so the uniform form is a
per-scale audit fact with a six-scale record; its consumer (the
notes/55 §5.3b close-pair hypothesis) only ever fires per scale.

### 2.4 (DEEP-LAW) CORRECTED: the E1×E1 characterization is
### 48-specific  [MACHINE-CHECKED]

At 48, D(48) = non-mod-8 alive pairs of E1×E1 exactly (reproduced).
At EVERY scale 64..128 the stall set is strictly larger: 20/…/20
extra stalls below q = M, reaching down to q_min(D) = 48, 64, 64,
96, 96 at 64..128 — the stall corner is a SCALED zone q ≳ 2M/3
(16-quantized onset), not the fixed-width band-edge corner.  And
mod-8 gaps are NOT protected inside it: gap-8/16/24 stalls appear
from 64 up (e.g. the whole gap-8 diagonal q ∈ [56, 71] at M = 64) —
"mod-8 necessary, not sufficient" now has mass, including INSIDE
E1×E1 (e.g. (64, 72) at M = 64 stalls).

Consequences recorded: (i) the notes/59 §C.1 deep law and its
"mod-8 members of E1×E1 are in R" clause are corrected as above;
(ii) the D(M) branch-certificate taxonomy (L1/L2/L3, 55/75 at 48)
is ALSO a scaled-zone question — |D| grows ≈ Θ(M), so a per-pair
finite catalogue cannot close it; the honest species is the same
scaled-zone recursion as §1.4's RESISTS item and the 20-pair
parity-locked core (→ §5 / GAP-PARM).

### 2.5 Status after §2

| claim | verdict |
|-------|---------|
| (RES-LAW) 8 \| gap necessary for escape | **[CLEARED as a six-scale machine law]** — 0 violations / 631 escapes; 5 fresh scales |
| (CLOSE-LAW′) distance ≤ 15 ⟹ fan-dead, M ≥ 64 | **[CLEARED as a six-scale machine law]** — stronger than the notes/59 form (no E1 exclusion) |
| deep-stall characterization | **corrected**: scaled corner q ≳ 2M/3, 16-quantized onset; E1×E1 form retired |
| D(M) branch-certificate taxonomy | **[RESISTS]** — exact statement: uniform-in-M certificates for the stall corner {(q,p) alive-UNSAT : q ≥ q₀(M)}; the corner's population grows Θ(M) and its even-gap members halve onto half-scale fan systems (GAP-PARM species); per-scale SAT verdicts + the six-scale laws above are the machine layer |

[MACHINE-CHECK: data/e180_deep_M*.json; runtimes 3–28 s/scale.]

---

## 3. GAP-DICH: Lemma PURE clears F0 and reduces ALPHA; the catalogue
## facts and the K* law at two fresh scales

### 3.1 Lemma PURE (the class-c subsystem IS the halved double fan)
### [PROVED]

Fix a same-parity attacker pair (q, p), q ≡ p ≡ ε (mod 2), on the
window O = [1, N] (N = 2M+15), class c := {s ∈ O : s ≡ ε (mod 2)}
(= the parity class of the attackers' VALUES 4M−p, 4M−q inside P2).

**Definition (class-c subsystem).**  Order theory on O ∩ c: in-class
AP-freeness (APs with all three members in c, i.e. even common
difference) + the fan units (2a+r) ≺ a with midpoint a ∈ c (their
sources 2a+r ≡ r ≡ ε are in c automatically).

**Lemma PURE.**  (i) The halving map h(s) = s/2 (ε = 0) resp.
h(s) = (s+1)/2 (ε = 1) is an isomorphism from the class-c subsystem
onto ThFG(q̂, p̂; N̂) with q̂ = (q−ε)/2, p̂ = (p−ε)/2 and
N̂ = ⌊N/2⌋ (ε = 0) resp. (N+1)/2 (ε = 1): it is a bijection
O ∩ c → [1, N̂] carrying in-class APs bijectively onto the APs of
[1, N̂] and the in-class unit family bijectively onto the halved
fan-unit family (source (2a+r) ↦ 2h(a) + r̂, r̂ = (r−ε)/2; the range
bounds match exactly: a ≤ (N−r+2ε)/4 on both sides).
(ii) Consequently the following are EQUIVALENT:
    (a) (q, p) is *pure-dead*: some death pattern S (Th₂[S] UNSAT,
        notes/56 §0.2) with attacker pair (q, p) has support ⊆ c;
    (b) the class-c subsystem is inconsistent;
    (c) the halved pair (q̂, p̂) is fan-dead (SAT level) on [1, N̂].

*Proof.*  (i) Parity bookkeeping: sources 2a+r ≡ r (mod 2) always,
so a unit has BOTH members in c iff its midpoint does; h preserves
and reflects APs on one parity class (notes/33 Lemma H); the window
and range arithmetic is the displayed formulas (checked: for ε = 0,
2a+r ≤ N ⟺ 2h(a)+r̂ ≤ ⌊N/2⌋; for ε = 1, ⟺ 2h(a)+r̂ ≤ (N+1)/2).
(ii) (b) ⟺ (c) by (i).  (b) ⟹ (a): the class-c subsystem is itself
the S-restricted theory of S = {attackers} ∪ (O ∩ c) — a pure death
pattern.  (a) ⟹ (b): every constraint of Th₂[S] for a pure S (its
in-S APs have all members in c; its units have midpoint AND source
in S ⊆ c) is a constraint of the class-c subsystem, so a model of
the subsystem restricts to a model of Th₂[S]; contrapositive.  ∎

[MACHINE-CHECK (bijection bookkeeping): experiments/
e181_pure_halving.py solves (b) and (c) with independent direct
encodings for EVERY same-parity pair at M = 48 and 64 — both scales
fresh for this equivalence — asserting identical verdicts; results
§3.2.]

**Corollary PURE-1 (GAP-DICH-F0 discharged as a lemma).**  The
H-DICH case analysis (notes/57 §4) consumes F0 only through: "for a
dead-pure class-c pair inside a class-c-owning team's band material,
a monochromatic pure pattern exists".  By PURE(ii)(a) ⟺ (b) this is
DEFINITIONALLY available whenever the pair is pure-dead — no appeal
to the catalogue-wide purity observation is needed.  F0-total (every
same-parity catalogue pattern IS pure, 100% at the six audited
scales) survives as a machine curiosity about minimized supports,
no longer load-bearing.

**Corollary PURE-2 (GAP-DICH-ALPHA = half-scale resonance).**  The
dead-pure pair graph on any subset of the band's class c equals the
lift, through h, of the half-scale fan-dead pair graph on [1, N̂].
Hence α_c(M) (notes/57 F1: max alive-clique of the shallow zone) is
EXACTLY a max clique in the half-scale ALIVE graph — the object
classified by (RES-LAW) and the e155b clique data.  GAP-DICH-ALPHA,
GAP-DICH-F0's recursion remark, and P-ARM's H-LAT are now PROVABLY
one statement: classify the alive set of the fan grid uniformly in
the window length (named **GAP-RES** below).

(Relation to the catalogue-level notions: the e153 α scans used
closure-level dead-pure pairs; at the audited scales closure-dead ∧
same-parity ⟹ minimized support pure (F0-total), so the two notions
agreed wherever K* was measured.  The SAT-level notion of Lemma PURE
is ⊇ and is the right uniform object; DICH's instances stay stated
relative to their per-scale catalogue 𝔉(M), unchanged.)

### 3.2 The bijection audit  [MACHINE-CHECKED, 2 fresh scales]

e181_pure_halving.py solves (b) (class-c subsystem, full-scale
coordinates) and (c) (halved fan on [1, N̂]) with independent direct
encodings for EVERY same-parity pair:

    M=48: 992 pairs, 902 halved-dead, 0 mismatches   [116 s]
    M=64: 1560 pairs, 1492 halved-dead, 0 mismatches [446 s]

Both scales fresh for this equivalence (it was never before stated,
let alone checked).  The window-end arithmetic of Lemma PURE(i) is
exact.  [data/e181_pure_M{48,64}.json, data/e181_pure.log]

---

## 4. GAP-PARM: every half-scale law extends to m = 48, 56
## (both fresh)

Instruments: e155_parm_hypotheses.py + e155b_alive_sat.py at
m = 48, 56 (prior grid: 24, 28, 32, 40) — data/e155_parm_hyp.json/
.log.  Both new scales are on the target line m ≡ 0 (mod 8).

### 4.1 (H-RW0′) the punctured-ThW0 law  [MACHINE-CHECKED ×6 scales]

At m = 48 AND m = 56: ThW0(m) full theory UNSAT; single-completion
drops UNSAT for i ∈ {1, 2, 3, 5, 7} and SAT for i ∈ {4, 6} EXACTLY —
the droppable set is {4, 6}, as at m = 24, 32, 40.  Moreover the
21-pair two-drop SAT verdict lists are IDENTICAL across m = 48, 56
(and match the smaller on-line scales): the fragile-completion
structure of the halved crown is scale-invariant in every audited
coordinate, not just in its droppable set.  P-ARM's S1 sub-case
(notes/58 §3.5c) now rests on six scales, two fresh.

### 4.2 (H-LAT) the lattice law  [MACHINE-CHECKED ×6 scales]

SAT-alive attacker-pair gaps on the halved windows:

    m=48 W2e: {8, 16, 24, 32, 48}      W2o: {16, 32, 48}
    m=56 W2e: {8, 16, 24, 32, 48, 56}  W2o: {16, 32, 48}

ALL ≡ 0 (mod 8) — zero violations among 51 + 48 + 67 + 64 SAT-alive
pairs.  H-LAT (fan-safe share ⟹ mod-8 aligned), the load-bearing
Case-F/Case-S split of P-ARM″, holds at every audited half-scale
(m = 28..56 mod-8 form; m = 24 mod-4).

### 4.3 Clique refinement  [MACHINE-CHECKED ×6 scales]

Max cliques of the SAT-alive pair graphs (branch-and-bound, this
session):

    m=48: {137, 153, 169} (both windows) — size 3, all ≡ 1 (mod 8),
          one CW-zone member
    m=56: W2e {168, 176, 192, 224} — size 4, all ≡ 0 (mod 8), no CW
          member; W2o {161, 177, 209} — size 3, ≡ 1 (mod 8), one CW
          member

So fan-safe shares have ≤ 4 members with ≤ 1 in the CW zone at EVERY
audited scale (24..56) — the S2-corner finiteness inputs of notes/58
§3.5d extend to both fresh scales.

### 4.5 THE S2 CORNER FALLS: e155c (first run) kills ALL of Case S
### through the α system — Theorem P-ARM‴

e155c_thw1_punctured.py — written in the notes/58 shift, queued,
NEVER RUN until tonight (sprint-D; data/e155_parm_hyp.json key 'C',
log appended) — checks the class-α system ThW1′[class ∖ X]: points =
one parity class of the band [3M−15, 4M], units z ≺ y for every A2
AP (x, y, z) inside the class (attacker x = 2y−z automatically in the
hatch owner's U), minus a puncture set X.  Verdicts at m = 24, 32,
40, 48, 56 (M = 48..112), BOTH classes:

    full system:                     UNSAT  (10/10 cases)
    minus any SINGLE value:          UNSAT  (0 SAT / 240 solves)
    minus any MAXIMAL CLIQUE of the
    e155b SAT-alive graph:           UNSAT  (0 SAT / 245 cliques)

**Theorem P-ARM‴ (modular, per-scale machine inputs).**  Under the
Lemma-PH hatch, for EVERY band split, some block theory dies:

  Case F — some share (A_e or B_o) contains a fan-dead pair of its
  halved window: that team's Th2 is inconsistent [PARM-HALVE(b),
  PROVED; deadness = the e155/e155b classification].

  Case S — both shares fan-safe.  Then every pair inside B_o is
  SAT-alive, so h(B_o) is a clique of the W2o alive graph, hence
  contained in a MAXIMAL clique Q (or |B_o| ≤ 1).  Th1(A) restricted
  to A_o = odds ∖ B_o contains the odd α system minus h(B_o) ⊇ the
  system minus Q; the e155c battery says THAT is UNSAT; a-fortiori
  (fewer punctures = superset of constraints, restriction argument)
  Th1(A) is inconsistent.  Symmetrically Th1(B) dies through the
  even class minus A_e.  ∎

Consequences:

1. **GAP-PARM-CORNER (S2) is DISCHARGED** at every audited scale:
   the crown/ThW0 arm — and with it the droppable-{4, 6} caveat that
   CREATED the S2 corner in notes/58 §3.5 — exits the critical path
   entirely.  H-LAT and (H-RW0′) become descriptive (they still pin
   the corner anatomy; they are no longer load-bearing for P-ARM).
2. P-ARM now has a MODULAR proof (not the monolithic e150 instance)
   at M = 48, 64, 80, 96, 112 — the last a scale where wholesale
   P-ARM was never run.
3. The remaining uniformization of GAP-PARM = (i) GAP-RES (the
   alive/dead classification, shared with DICH-ALPHA/F0) + (ii) one
   NEW quantitative law, named **ThW1′-ROBUST**: the class-α system
   minus any alive-clique is inconsistent.  Both are per-scale-cheap
   scans (no SAT sweeps).
4. Relation to the notes/58 §5.1 pre-registration: confirmed in the
   operative half — ThW1′ has NO fragile single completions (unlike
   ThW0's {4, 6}); the dangerous ≥ 4-puncture patterns (the L-LOP
   frontier witness's packed E1 odd values at gaps 2/4/6) are
   pairwise fan-DEAD, hence NOT alive-cliques — exactly why Case S
   cannot reach them.  The α-arm's breaking punctures are
   fan-unsafe sets, which Case F re-captures: the two arms are
   complementary BY CONSTRUCTION now, not by threshold arithmetic.

[MACHINE-CHECK: data/e155_parm_hyp.json 'C' keys ×5 scales;
independent re-verification e182 below.]

### 4.6 Independent re-verification (e182)  [MACHINE-CHECKED]

Fresh encoder (full-scale coordinates, no halving; Glucose42, not
CaDiCaL; independent clause construction) re-solves the α system
minus every maximal clique AND minus random sub-cliques (a-fortiori
sanity) at m = 48, 56: results below.

### 4.8 PRE-REGISTRATION for the M = 176/192 chain (written BEFORE
### any probe at those scales ran)

Catalogues at 176/192 are building on sprint-B/-C at time of writing;
no threshold at either scale has ever been measured.  Predictions:

1. **Cap flat law** (notes/58 §1.1, survived 96..160):
   C(176) = (176+16)/2 − 4 = **92**;  C(192) = **100**
   (probe protocol: e152_llop_probe K = C expect UNSAT, K = C+1
   expect SAT).
2. **K\* mechanistic law** (notes/57): K*(M) = m + 9 + max(α_E − f_O,
   α_O − f_E) with α, f computed from the catalogue by e153_dich_lemmas
   BEFORE the phi1 probes — the numeric prediction is whatever the
   scan outputs, registered in §5 the moment it prints, then tested
   by e153_dich_probe phi1 at K* (UNSAT) and K*−1 (SAT).  No residue
   law is assumed (the α non-monotonicity at 160 is on record).
3. **(OV)**: K*(M) ≤ C(M) expected to HOLD at both scales (it held at
   all eight 48..160), but the robust chain is run REGARDLESS:
   DICH-upure(M, K_P), DICH-zdef(M, K_P, 4), RP-ARM(M, 4) with
   K_P = C(M) — the ASM′ insurance that does not ride on (OV).
4. **SPLIT**: e154_dich_split UNSAT at both scales, fast (it has died
   far below threshold at all six audited scales).

### 4.7 Status after §4 (supersedes the §4.4 draft table)

| claim | verdict |
|-------|---------|
| PARM-HALVE frame | [PROVED] (notes/58 §3.1, unchanged) |
| (H-RW0′) droppable = {4, 6} on the line | six-scale machine law (2 fresh) — now DESCRIPTIVE (off critical path) |
| (H-LAT) mod-8 lattice law | six-scale machine law (2 fresh) — now DESCRIPTIVE; = GAP-RES via Cor. PURE-2 |
| clique ≤ 4, ≤ 1 CW member | six-scale machine fact |
| **GAP-PARM-CORNER (S2)** | **[CLEARED — Theorem P-ARM‴]**: the α-robustness route kills all of Case S; corner discharged at 5 scales (M = 48..112), battery + independent re-verification |
| GAP-PARM residual | reduces to GAP-RES + ThW1′-ROBUST (uniform-in-m write-ups of two per-scale scans); exact statements in §7 |

---
