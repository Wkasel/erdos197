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
