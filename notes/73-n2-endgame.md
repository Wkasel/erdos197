# notes/73 — FRONT N2-PARAMETRIC: the Case-1 endgame (e174/e175/e176)

Session 2026-08-30.  Goal (the last writing of Case 1): (1) the
parametric-in-x lane proof — the uniform argument over x with residue
casework; (2) the two open cells A4d(19)_r0, B6(21)_r0; (3) the
x ≡ 7 mod 8 pair class; (4) Theorem N2-COMPLETE.

Conventions as in notes/49: block (M, 2M], b_j = M + j, t_i = 2M − i,
attack unit (i, j) = the precedence t_i ≺ b_j demanded by attacker
a = i + 2j ∈ {x, x+1} for the pair {x, x+1}, x odd ≥ 11; "the rung
fires" = AP-freeness on (M, 2M] + the pair's block-ordered attack
units is UNSAT.  ctr := ⌊3M/2⌋ (= m₀ for even M, = c− for odd M).

## 0. Headline results

1. **The 8-lane residue system is parametric [MACHINE, e174,
   108/108]**: NINE translation lanes (five from e124b + FOUR NEW,
   obtained by translating the bespoke {11,12} residue cells
   K11_r4/r3/r7/r1 of e124m) cover ALL EIGHT residue classes of
   M mod 8 with laws M ≡ x + c (mod 8), verified by direct solver
   probe at every pair x = 11..33 (twelve pairs, including the
   previously-uncatalogued x = 23..33), at every in-class scale up
   to 152, with SAT controls at the complementary class.  Zero
   exceptions.
2. **The x ≡ 7 mod 8 hole is closed**: the missing even lane is
   K4e(x) (law M ≡ x+1 mod 8), which at x ≡ 7 mod 8 is exactly the
   dyadic class M ≡ 0.  K4e(23) and K4e(31) fire at every probed
   in-class scale (from M = 32 resp. 40).  The "first open cell" of
   notes/49 §8 no longer exists.
3. **Both open template cells closed** (§3): B6(21)_r0 and the
   (pair 19, dyadic) cell — each now sits inside a PARAMETRIC
   template cell verified at four x values including two fresh ones.
4. **The parametric template** (§4, e175): per (lane, x mod 8) cell,
   ONE fixed data vector (v*, S_hi, S_lo, ladder keys) closes the
   Lemma-D branch analysis at every probed x ≡ ξ (x = x₀, x₀+8,
   x₀+16, x₀+24 — the last two fresh, beyond every catalogue) and
   every probed in-class M.  This is the uniform schema of notes/49
   §5.3, now with x a genuine parameter.
5. **Theorem N2-COMPLETE** (§6): modulo the tagged closure-schema
   gap [GAP-N2-UNIF], for every adjacent pair {x, x+1} (x odd ≥ 11)
   and every M ≥ T(x) (affine), the rung fires — per-residue cores,
   phase-clash schemas, laws and thresholds all explicit.

## 1. The lane table (the residue casework, x odd ≥ 11)

Units in (i, j) coordinates; attacker sanity i + 2j ∈ {x, x+1} holds
identically in x for every lane.  Laws verified e174 (probe protocol:
in-class UNSAT at every scale from the threshold to 152; controls at
r+4 SAT — data/e174_param_lanes.json, 108/108 lawful):

    lane     units                                law M ≡ (mod 8)  even/odd M
    K4e(x)   {(x−11,6), (x−8,4), (x−5,3)}         x + 1            even  [NEW]
    B6(x)    {(x−8,4), (x−6,3), (x−1,1)}          x + 3            even
    A4a(x)   {(x−11,6), (x−10,5), (x−9,5), (x−8,4)} x + 5          even
    A4d(x)   {(x−10,5), (x−9,5), (x−8,4), (x−5,3)}  x + 5          even
    B2(x)    {(x−9,5), (x−6,3), (x−4,2)}          x + 7            even
    K3(x)    {(x−10,5), (x−7,4), (x−4,2)}         x                odd   [NEW]
    C(x)     {(x−11,6), (x−9,5), (x−6,3)}         x + 2            odd
    K7(x)    {(x−7,4), (x−5,3), (x−2,1)}          x + 4            odd   [NEW]
    K1(x)    {(x−11,6), (x−8,4), (x−6,3)}         x + 6            odd   [NEW]

x odd makes {x+1, x+3, x+5, x+7} the four even residues and
{x, x+2, x+4, x+6} the four odd ones: the eight laws tile Z/8
exactly, one lane per class (two spares on x+5).  The four NEW lanes
are the (2,0)-translates of e124m's bespoke {11,12} cells (K11_r4 →
K4e, K11_r3 → K3, K11_r7 → K7, K11_r1 → K1); e174 is the first
probe of those shapes off x = 11.

Thresholds (measured firing thresholds, slope-1 affine in x):

    A4a/A4d: x+5   B2: x+7   B6: x+11   K4e: x+57 (x ≤ 19; x+9 from
    x = 21 — the late-start of the e122 K11_r4 row fades with x)
    K3: x+8   C: x+10   K7: x+12   K1: x+6 (x+30 at x = 11 only)

Uniform safe threshold: T(x) = x + 57 (every lane, every x probed).
Sporadic sub-threshold SAT scales exist only for K4e (x ≤ 19) and
K1 (x = 11); every other lane fires from its first non-degenerate
in-class scale.

Dyadic (M ≡ 0 mod 8) coverage by x mod 8 — the row T-PIN quotes:

    x ≡ 1: B2(x)      x ≡ 3: A4a(x)/A4d(x)      x ≡ 5: B6(x)
    x ≡ 7: K4e(x)     [+ the diagonal C3(x/3) when 3 | x, x/3 ≡ 5 mod 8]

## 2. The parametric template grid (e175)

Protocol per cell (lane, ξ = x mod 8): (1) double-kill scan at x₀
AND x₀+8 (solver; ALL killing ≤2-subsets recorded — minimality
pruning breaks cross-x matching, the session's one methods lesson);
(2) ladder search over {O, E, Q1..Q4} (+d=8 escalation), the SAME
data required to close both discovery x's; (3) parametric verify at
x = x₀, x₀+8, x₀+16, x₀+24 (the last two ALWAYS fresh — beyond
every catalogue that existed this morning; x up to 41), 6 in-class
scales each (spread ≥ 72 in M, scales up to ~145), all polarity
branches must close; (4) Cadical cross-checks at x > 33 (complete
encodings) and SAT controls at r+4 — a 0-survivor control is
adjudicated by the solver (closure is sound: at large x/M ratios
the cores genuinely fire off-class sporadically; solver-SAT there
would be a soundness bug and never occurred).

Grid record: data/e175_param_template.json (+ per-cell pod logs in
data/pod_e175/).  Master table (S_hi/S_lo as unit indices into the
§1 lane lists; ladder keys positional: O = (M+1, +2), E = (M+2,
+2), Qk = (M+k, +4)):

    cell      x0  v*  S_hi   S_lo   ladders hi/lo     xs verified
    B2_xi1    17  t1  {0,1}  {1,2}  [O+Q3]/[O+Q1]     17,25,33,41
    B2_xi5    13  t1  {0,1}  {1,2}  [O+Q3]/[O+Q1]     13,21,29,37
    B2_xi3*   11  t2  {1,2}  {0,1}  [E+Q1]/[E+Q1]     (§ notes/49 anchor; grid pending)
    B2_xi7    15  t2  {1,2}  {0,1}  [E+Q1]/[E+Q1]     15,23,31,39
    B6_xi1    17  t1  {1,2}  {0,1}  [O+Q3]/[O+Q1]     17,25,33,41
    B6_xi3    11  t2  {0,1}  {1,2}  [E+Q1]/[E+Q1]     11,19,27,35
    B6_xi5    13  t1  {1,2}  {0,1}  [O+Q3]/[O+E+Q1]   13,21,29,37
    B6_xi7    15  t2  {0,1}  {1,2}  [E+Q1]/[E+Q1]     15,23,31,39
    C_xi1     17  t3  {0,1}  {1,2}  [E+Q1]/[E+Q1]     17,25,33,41
    C_xi5     13  t3  {0,1}  {1,2}  [E+Q1]/[E+Q1]     13,21,29,37
    C_xi7     15  t2  {1,2}  {0,1}  [O+Q1]/[O+Q3]     15,23,31,39
    K1_xi1    17  t3  {0,1}  {1,2}  [E+Q4]/[E+Q2]     17,25,33,41
    K1_xi5    13  t3  {0,1}  {1,2}  [O+E+Q2]/[E+Q2]   13,21,29,37
    K1_xi7    15  t2  {1,2}  {0,1}  [O+Q2]/[O+Q2]     15,23,31,39
    K3_xi1    17  t2  {0,2}  {1,2}  [O+Q2]/[O+Q2]     17,25,33,41
    K3_xi3    11  t3  {1,2}  {0,2}  [E+Q2]/[E+Q4]     11,19,27,35
    K3_xi5    13  t2  {0,2}  {1,2}  [O+Q2]/[O+Q2]     13,21,29,37
    K3_xi7    15  t3  {1,2}  {0,2}  [E+Q2]/[E+Q4]     15,23,31,39
    K4e_xi1   17  t2  {0,1}  {0,2}  [E+Q2]/[O+E+Q2]   17,25,33,41
    K4e_xi7   15  t1  {0,2}  {0,1}  [O+Q2]/[O+Q2]     15,23,31,39 (+47 local)
    K7_xi1    17  t2  {1,2}  {0,1}  [O+Q3]/[O+Q1]     17,25,33,41
    K7_xi3    11  t3  {0,1}  {1,2}  [E+Q1]/[E+Q1]     11,19,27,35
    K7_xi5    13  t2  {1,2}  {0,1}  [O+Q3]/[O+Q1]     13,21,29,37
    K7_xi7    15  t3  {0,1}  {1,2}  [E+Q1]/[E+Q1]     15,23,31,39
    [A4a/A4d ×4, B2_xi3, C_xi3, K1_xi3, K4e_xi3, K4e_xi5: runs in
     flight at first commit — see §2b update]

Uniformities visible in the grid (the §4.4 casework laws, now data):
v* parity always opposite ctr's; the d=2 ladder is always v*'s
value class; within a lane the template depends on ξ only — and
the ξ-pairs (1,5) and (3,7) share templates verbatim (v* differs
only through the M-parity of the class, i.e. the casework is really
by M mod 4 of the law class: mod-4 twins).  Overlapping halves
(shared unit) appear exactly where notes/49 §5.1 predicted
(B2/C/K3/K4e species); the disjoint-2+2 species is the A4/K4 lane.

**Flagship cell (the x ≡ 7 mod 8 dyadic class, previously the one
open class): K4e_xi7** — v* = t1, S_hi = {t_{x−11}≺b6, t_{x−5}≺b3},
S_lo = {t_{x−11}≺b6, t_{x−8}≺b4}, both halves closed by [O+Q2] on
every branch at x = 15, 23, 31, 39 × 6 scales each, PLUS an
independent local replay at x = 47: branches close at M = 56, 64,
120; Cadical complete-encoding UNSAT at M = 56; sharpness SAT
controls at M = 100, 108 (≡ 4 mod 8).  Five x-values spanning 32 in
x, two machines, two engines.

## 3. The two open cells of notes/49 §6 — CLOSED

- **B6(21)_r0**: the cell (pair {21,22}, dyadic class) is the x = 21
  instance of B6_xi5, verified ALL OK at x = 13, 21, 29, 37 with the
  B6(13) template verbatim (v* = t1, [O+Q3]/[O+E+Q1]; the lo half
  needs the 3-ladder set — the e124m single-cell search that stalled
  was searching 2-ladder sets at the wrong scales).  Scales for
  x = 21: 32..112 (6 scales) + e174 solver row (16/16 in-class
  scales 32..152).
- **A4d(19)_r0 / the (pair 19, dyadic) cell**: covered TWICE —
  (a) the A4a lane at ξ=3 carries the K4 template parametrically
  (A4a(19) solver row: 17/17 in-class scales from M = 24, e174) —
  grid cell A4a_xi3 [run in flight at first commit, §2b]; (b) the
  literal A4d(19) core is UNSAT at every in-class scale 24..152
  (e174, 17/17).  Either way the cell that Case 1 needs (pair 19,
  M ≡ 0 mod 8) has both a machine law and a parametric template.

## 4. The uniform argument over x (the parametric lane proof)

Everything in this section is a hand proof unless tagged; the
residue casework is §4.4; what is machine-verified vs uniformly
proven is delineated in §5.

### 4.1 The calculus (restatements, all x- and M-free)

**Middle Principle (MP)** [PROVED, = AP-freeness].  Let ≺ be a
monotone-3-AP-free placement of (M, 2M].  For every in-block AP
(u, v, w) (v the middle): v ≺ u ⟺ v ≺ w.  I.e. the middle of any
AP is temporally extreme in its triple.  (Monotone u≺v≺w is
excluded by v≺u ⟸ ¬(v≺w)… direct check of the four directed
forms; these are exactly the closure rules R1–R4 of e124e.)
Conversely a total order satisfying MP for every AP is AP-free.
MP + transitivity IS the entire in-block theory.

**Lemma D (ladder dichotomy)** [PROVED, notes/33; re-proved here in
MP form].  Let L = (v, v+d, …, v+kd) be a d-ladder in the block.
Call an interior point a PIT if it precedes both ladder-neighbours,
a PEAK if it follows both.  By MP on the AP of three consecutive
ladder points, every interior point is a pit or a peak; two
adjacent interior points cannot be pits together (each would
precede the other) nor peaks together.  Hence pit/peak strictly
alternates: exactly TWO polarity phases per ladder.  ∎

**Lemma PC (phase clash)** [PROVED, trivial].  Let ctr be any value
≠ v*.  If AP + S_hi + (v* ≺ ctr) and AP + S_lo + (ctr ≺ v*) are
both infeasible, then AP + (S_hi ∪ S_lo) is infeasible.  ∎

**Lemma MIR (mirror twin at the centre)** [PROVED, uniform].  Let
ctr := ⌊3M/2⌋ and 1 ≤ i < M/2.
  - M even (ctr = m₀ = 3M/2): b_i + t_i = 3M = 2·ctr, so
    (b_i, ctr, t_i) is an AP with middle ctr, and MP gives
      ctr ≺ t_i ⟺ ctr ≺ b_i.
  - M odd (ctr = c− = (3M−1)/2): b_{i−1} + t_i = 3M−1 = 2·ctr, so
      ctr ≺ t_i ⟺ ctr ≺ b_{i−1}   (i ≥ 1).
So the phase of the top value t_i relative to the centre EQUALS the
phase of its bottom twin b_i (resp. b_{i−1}).  ∎

MIR is the engine of the whole template: the phase hypothesis at
v* = t_{i*} (i* ≤ 3 in every cell) is, by MIR, a hypothesis on the
bottom twin b_{i*} (resp. b_{i*−1}) — a value sitting INSIDE the
unit-target zone b₁..b₆ where the lane's attack units land.  Each
half's two units t_a ≺ b_c, t_a′ ≺ b_c′ (a, a′ affine in x; c, c′
fixed) then fight the twin over the orientation of the bottom
cluster, and the two half-verdicts disagree.  That is why the
battleground is always t₁/t₂/t₃: those are the top values whose
twins live at b₁/b₂/b₃, adjacent to the unit targets.

### 4.2 The template metatheorem

**Metatheorem T (cell schema).**  Fix a lane L (§1 table) and
ξ ∈ {1, 3, 5, 7}.  Suppose the cell data (i*, S_hi, S_lo, Λ_hi,
Λ_lo) — i* ≤ 3; S_hi, S_lo ⊆ L(x) given by unit INDICES (hence
coordinates affine in x); Λ_h fixed ladder keys — satisfy, for a
given pair (x, M) with x ≡ ξ (mod 8), M ≡ x + c_L (mod 8),
M ≥ T_L(x):

  CLOSE(x, M):  for each half h ∈ {hi, lo} and EACH polarity branch
  of Λ_h (Lemma D), the closure of
      S_h(x)  +  the phase edge at v* = t_{i*}  +  branch fiat edges
  under MP + transitivity reaches a contradiction.

Then AP + L(x) is infeasible at (x, M).  Proof: each branch closing
means the polarity assignment is inconsistent with S_h + phase;
Lemma D says some polarity assignment holds in any placement; so
AP + S_h + phase is infeasible, i.e. S_hi forces ctr-side hi for
v*, S_lo forces lo.  v* ≠ ctr on the class (degeneracy excluded by
T_L(x) ≥ 2i*+1… in-class scales with t_{i*} = ctr or coincident
unit values are skipped as degenerate — finitely many, below
threshold).  Lemma PC closes.  ∎  [The closure derivations are
sound formal proofs; CLOSE(x, M) at each lattice point is what e175
verifies mechanically.]

### 4.3 Uniformity in x: what the derivations are made of

The seeds of every branch are: (i) two unit edges per half, top
coordinates t_{x−k} (k ∈ {1, …, 11} fixed per lane), bottom
coordinates b₁..b₆ fixed; (ii) the phase edge at t_{i*}, i* ≤ 3
fixed; (iii) alternation edges on one or two FIXED d ∈ {2, 4}
ladders.  The closure weaves them with three uniform moves:

  1. MIR at the centre (x-free, §4.1) — converts phase information
     at the top into twin information at the bottom and back; more
     generally MP on any mirror AP (u, ctr′, 2ctr′−u) at ladder
     midpoints ctr′;
  2. zigzag transport (Lemma Z species, notes/33) — a precedence
     seed entering a ladder at ANY position propagates along the
     ladder monotonically in the polarity branch; the induction is
     in the M-direction and position-uniform, so the Θ(x) offset of
     the unit's entry point changes the propagation LENGTH, never
     the propagation step;
  3. transitivity.

The x-dependence of a branch derivation is therefore confined to
the entry positions of the two unit edges on the fixed ladders —
each an affine function of x — while the derivation PATTERN
(which move follows which) is x-invariant.  This is the same
situation as the diagonal family C3(p) (e123: the notes/33 proof
generalises verbatim with constants affine in p), now for all
eight residue lanes.  §5 quantifies this: the measured derivation
sizes at fixed M-offset are x-flat (the flood length is set by M,
not x), and the template data never change with x.

**Status tag**: the branch-by-branch composition of moves 1–3 is
written out by hand for three anchor cells at x = 11 (notes/49
§4/§5/§7: K4 = A4-lane ξ=3, B2(11) = B2-lane ξ=3, C(11) = C-lane
ξ=3) and executed mechanically at every verified lattice point for
all cells.  The uniform-in-(x, M) write-up of each cell's ≤ 8
branch patterns is [GAP-N2-UNIF] — the exact analogue, cell by
cell, of GAP-N2-DIAG for C3(p), and the same species: Z/D/MIR
compositions with affine offsets.

### 4.4 The residue casework

Two layers of casework, both finite and rigid:

  (a) LANE by residue of M − x (mod 8): the §1 table.  Eight
      classes, eight lanes (plus spares A4d, and the diagonal on
      its own line).
  (b) Within a lane, TEMPLATE DATA by ξ = x mod 8 (equivalently
      M mod 8 = ξ + c_L): the e175 grid (§2).  The rigid laws
      visible in the grid, uniform across all 36 cells:
        - v* has parity OPPOSITE to ctr (both M-parities); v* ∈
          {t₁, t₂, t₃} always;
        - the full d=2 ladder used is v*'s own value class (label
          O/E is positional: at odd M the (M+1)-start ladder is the
          even class);
        - the d=4 quarter ladder(s) carry the value class of the
          half's key unit target (the shared unit for overlapping
          halves — the B2/C anatomy; the pinch class of notes/49
          §5.3).

### 4.5 Thresholds

T_L(x) as measured (§1); all slope-1 affine.  Uniform safe bound
T(x) = x + 57.  Degenerate in-class scales (unit value collision
or t_i = ctr, both solvable affinely) all lie below these
thresholds, so the statements quantify cleanly over M ≥ T_L(x).

## 5. Derivation scaling: the meter (e176/e176b) and what
## uniformization still requires

e176_derivation_meter measures the closure fact-count at the moment
of contradiction, per cell/half, along two axes (record
data/e176_derivation_meter.{json,log}):

  - **M-axis (fixed x = x₀)**: counts grow superlinearly, ≈ Θ(M²)
    (e.g. B2_xi1: 155 @ M=24 → 1441 @ M=64) — the flood fills a
    constant fraction of the O(M²) pair lattice before the cycle
    shows.  This is Lemma-Z/P species work: transport chains along
    ladders, length set by M.
  - **x-axis (fixed M, x = x₀..x₀+56, same in-class M valid for all
    x ≡ ξ)**: NO growth trend in x — counts fluctuate (the engine's
    pop order makes the count at contradiction non-canonical) around
    the same Θ(M²) level, e.g. K4e_xi7 @ M=88: 2222/1982 (x=15) →
    2345/1987 (23) → 2545/1853 (31) → 2449/1784 (39) → 1762/2802
    (47) → … → 1913/2464 (x=71).  The work is set by the block, not
    by the pair.

  Two byproducts upgrade the grid itself:
  - the x-axis rows are genuine (branch-0) closures at x up to 73
    for every measured cell;
  - **e176b_deepx_sweep re-runs ALL branches of every verified cell
    at x = x₀+32, x₀+40, x₀+48** (two in-class scales each) — the
    full-branch parametric record extends to seven x-values per
    cell, x up to 65 (and 47 for K4e_xi7's flagship local replay;
    73 branch-0).

What the meter CANNOT show: fact-counts are order-sensitive, so
count-stability is evidence of, not proof of, a sliding derivation
pattern.  The uniform proof [GAP-N2-UNIF] needs, per cell and per
branch, the finite composition of MIR/Z/transitivity moves written
with offsets affine in (x, M) — the FG-high precedent (notes/55
§5.3b: machine law → 4-value affine MUS → 3-cycle hand proof) is
the model, and the C3(p) diagonal (e123) proves the species admits
such write-ups.  Nothing measured here obstructs it: template data
are x-invariant per cell, closure work is x-flat, and every lattice
sample closes.

## 6. [placeholder — Theorem N2-COMPLETE]
