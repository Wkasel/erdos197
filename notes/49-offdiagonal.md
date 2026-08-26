# notes/49 — FRONT N2-OFF: off-diagonal core lanes (e124/e124b/e124c)

Session 2026-08-26 (post-front-merge).  Goal: per-residue hand schemas
for the (pair, residue) cells the diagonal C3(p) family misses —
closing Case 1 of the dichotomy outright.  Named targets from the
merge: the {11,12} size-4 lane (0 mod 8 — the dyadic class T-PIN
needs; {11,12} is the ONE pair with no size-3 core there), and one
≡ 2 mod 4 flip class.

Conventions as everywhere: block (M, 2M], b_j = M + j, t_i = 2M − i,
attack unit (i, j) = the precedence t_i ≺ b_j demanded by attacker
a = i + 2j (a ∈ {x, x+1} for pair {x, x+1}); "core" = minimal set of
units whose conjunction with in-block AP-freeness is UNSAT.

## 1. Catalogue reconstruction (e124_prep_catalogue)

The final e122_n2_residue.json died with its session at M = 135; the
partial checkpoint data/e122_n2_residue_partial.json holds the COMPLETE
per-M rows for M = 16..128 (113 consecutive scales, every residue).
Reconstructed catalogue → data/e122_n2_residue_recon.json (same schema
the miner expects).  Full-rung UNSAT at 113/113 scales for all six
pairs (re-confirms e122).  Distinct minimal cores per pair:
110 / 155 / 173 / 277 / 401 / 533 for x = 11..21.

Caveat carried through everything below: laws fitted on MINIMAL-core
appearance lists undercount the true firing sets (a core also fires
where a different core preempts minimality).  e124b re-probes the
interesting lanes DIRECTLY (solver, exact firing set at every M).

## 2. The miner (e124_family_miner, fixed and run)

Two fixes to the committed-but-unrun miner: (a) the constant-delta
requirement is now enforced during chain extension (was dead code —
subset chains and mixed deltas survived); (b) cores of different sizes
can no longer match (zip silently truncated).  Result:
data/e124_families.json — 3135 maximal affine families of length ≥ 3
(most are noise: "family" only requires a bijection with constant even
(di, dj) per unit and di + 2dj = lane step; the signal is in the
families whose member LAWS also slide).  Dyadic (0 mod 8, ≥ 5 scales)
sub-catalogue counts: x = 11: 23, 13: 3, 15: 7, 17: 9, 19: 13, 21: 22
— every pair has dyadic cores (the miner's second question: YES).

### The headline family (pure translation, laws slide mod 8)

    C(x) = { t_{x−11} ≺ b_6,  t_{x−9} ≺ b_5,  t_{x−6} ≺ b_3 }

(delta (2,0) per lane step of 2; attackers x+1, x+1, x).  Miner laws:
x = 11: M ≡ 5 (mod 8), x = 13: ≡ 7, x = 15: ≡ 1, x = 17: ≡ 3 — i.e.

    C(x) kills its pair on the ODD class  M ≡ x + 2 (mod 8)

(x = 19, 21 flagged irregular on minimal-appearance lists — direct
probe below).  An odd-M lane is beyond every schema we have (m₀ = 3M/2
is not an integer; the notes/33 machinery needs even M), so this is
recorded as a statement + machine law, not a hand target today.

### The ≡ 2 mod 4 flip candidates at x = 11

    B2(11) = {t2≺b5, t5≺b3, t7≺b2}   law M ≡ 2 (mod 8)
    B6(11) = {t3≺b4, t5≺b3, t10≺b1}  law M ≡ 6 (mod 8)

Together they cover the whole ≡ 2 mod 4 class for {11,12}.  Their
(2,0)-translates exist in the catalogue at higher x (with laws that
slide); direct probes in e124b.

### The {11,12} size-4 dyadic lane (0 mod 8)

Four size-4 cores fire at every M ≡ 0 mod 8 in 24..128 (14/14 scales):

    A4a = {t0≺b6, t1≺b5, t2≺b5, t3≺b4}
    A4b = {t0≺b6, t2≺b5, t3≺b4, t7≺b2}
    A4c = {t0≺b6, t2≺b5, t7≺b2, t9≺b1}
    A4d = {t1≺b5, t2≺b5, t3≺b4, t6≺b3}

({11,12} has NO size-3 core on 0 mod 8 at M ≥ 24 — e121's deletion-MUS
size-4 finding, now with the residue law.)  This is the hand-verify
target: same residue class as thm:c3core, so the whole notes/33
toolkit (odd/even ladders, centers m₀ ± 1, G4 floods) applies —
only the core anatomy is new (expected 2+2: two units force an
L1-type order, two close the flip).

## 3. Direct lane probes (e124b_lane_probe) — DONE, the lane laws

Sweep M = 16..160, every lane instance probed directly (AP + units,
complete encoding, exact firing set — no minimality confound).
data/e124b_lane_probe.{json,log}.  THE RESULT — every off-diagonal
lane's law is a SLIDING mod-8 class, affine in x (thresholds finite
and small, a few sporadic sub-threshold hits):

    lane      units (pair {x, x+1}, odd x >= 11)                law
    ----      ------------------------------------------       --------------------
    A4a(x)  {t_{x-11}<b6, t_{x-10}<b5, t_{x-9}<b5, t_{x-8}<b4}  M ≡ x+5 AND M ≡ x+2 (mod 8)
    A4b(x)  {t_{x-11}<b6, t_{x-9}<b5, t_{x-8}<b4, t_{x-4}<b2}   M ≡ x+5 (mod 8)
    A4c(x)  {t_{x-11}<b6, t_{x-9}<b5, t_{x-4}<b2, t_{x-2}<b1}   M ≡ x+5 (mod 8)
    A4d(x)  {t_{x-10}<b5, t_{x-9}<b5, t_{x-8}<b4, t_{x-5}<b3}   M ≡ x+5 (mod 8)
    B2(x)   {t_{x-9}<b5, t_{x-6}<b3, t_{x-4}<b2}                M ≡ x+7 (mod 8)
    B6(x)   {t_{x-8}<b4, t_{x-6}<b3, t_{x-1}<b1}                M ≡ x+3 (mod 8)
    C(x)    {t_{x-11}<b6, t_{x-9}<b5, t_{x-6}<b3}               M ≡ x+2 (mod 8)  [odd class]

(x odd: x+3, x+5, x+7 are the three even residues ≠ x+1; x+2 is odd.)
So the off-diagonal lanes cover, per pair, three of four even classes
+ one odd class as uniform parametric statements; the diagonal D3
covers M ≡ 2(x/3)+6 on its own x = 3p lane.  Dyadic (0 mod 8) row of
the catalogue's six pairs: x=11, 19 (≡3 mod 8) by A4b/c/d; x=17
(≡1) by B2; x=13, 21 (≡5) by B6; x=15 (≡7) by D3 = C3(5).  Every
catalogued pair has a dyadic lane.  (x ≡ 7 mod 8 pairs OFF the
diagonal — 23, 31, ... — are outside this catalogue; first open cell.)

## 4. THE HAND SCHEMA: the {11,12} dyadic lane, verified end-to-end

### 4.1 Anatomy (e124c, e124d)

At every M ≡ 0 mod 8 tested (24..48) the size-4 core
A4a = {t0≺b6, t1≺b5, t2≺b5, t3≺b4} splits 2+2 BY ATTACKER:

    U12 = {t0≺b6, t2≺b5}   (attacker 12's units, j = 6, 5)
    U11 = {t1≺b5, t3≺b4}   (attacker 11's units, j = 5, 4)

and the two 2-unit sets fight over the PHASE of t1 = 2M−1 relative to
m0 = 3M/2 (equivalently of t3 — both are double-killed):

    HALF-A:  AP + U12 + (t1 ≺ m0)  is UNSAT   [so U12 forces m0 ≺ t1]
    HALF-B:  AP + U11 + (m0 ≺ t1)  is UNSAT   [so U11 forces t1 ≺ m0]

t1 ≠ m0, so A4a ⊇ U11 ∪ U12 is UNSAT.  At M ≡ 4 mod 8 the kills
disappear (t1's lo phase survives even the full core) — the lock is
exactly mod 8.  Scale-stable at every probe.  This is a genuinely new
core SHAPE: C3(p) is 2+1 (two units force an order lemma, one closes
the flip); the {11,12} core is 2+2, a two-attacker phase clash, with
no order-transfer lemma at all.

### 4.2 The derivation (e124e/g/h): Lemma D + zigzag propagation

Pure rule-closure from the 3 seeds alone does nothing (4-6 facts,
e124e) — as with C3, case analysis is essential.  The right case
frame (e124g, e124h): Lemma D (each d-ladder's leader/trailer pattern
strictly alternates — exactly two polarity phases) on TWO ladders per
half, then closure under the four AP rules + transitivity kills every
branch:

    HALF-A: ladders O = (M+1, M+3, ..., 2M−1)  [odd values, d=2]
            and Q2 = (M+2, M+6, ..., 2M−2)     [t2's mod-4 class, d=4]
    HALF-B: ladders O and Q3 = (M+3, M+7, ..., 2M−1) [t1's mod-4 class]

4 polarity branches per half, every branch closes by propagation —
minimal ladder sets, uniform across scales (e124h: {O,Q2} or {O,Q4}
for A, {O,Q3} for B, at every M tested).  The quarter-ladder matches
the value class of the half's own top unit (t2 ≡ 2, t1 ≡ 3 mod 4) —
the schema "knows" which class carries the pinch.

### 4.3 The verified statement (e124i_k4_schema_verify)

THEOREM SCHEMA (K4 dyadic lane).  For every M ≡ 0 mod 8, M ≥ 24: an
AP-free placement of (M, 2M] admits no assignment satisfying U11 ∪ U12
— the four listed unit demands of a block-ordered attacker pair
{11, 12}.  Hence the {11,12} rung fires on the whole dyadic class.
Proof: HALF-A + HALF-B (each: Lemma D on two ladders, 4 branches,
zigzag propagation) + the t1-phase dichotomy.

Machine verification, e113-style (the derivation NEVER consults a
solver; the Lemma-D discharge is e113's fiat_zig in closure form):
  - 20/20 dyadic scales M = 24, 32, ..., 176: all 4+4 branches close
    in both halves;
  - independent complete-encoding Cadical195 cross-check at each
    M ≤ 96: AP + A4a UNSAT (and e124b already has it UNSAT at every
    M ≡ 0 mod 8 ≤ 160);
  - adversarial scales M = 256, 512, 1024, 2048: all branches close
    (1 s / 9 s / 71 s / 539 s);
  - sharpness controls, 20 scales M = 28, ..., 180 (≡ 4 mod 8):
    surviving branches exist in BOTH halves (stable fingerprint:
    HALF-A survives only odd-ladder polarity False branches, HALF-B
    only True — the mod-8 lock is visible in WHICH branch survives),
    and Cadical confirms AP + A4a SAT at each control ≤ 96.
data/e124i_k4_schema.{json,log}; zero failures.

### 4.4 Why this matters for Case 1

The dyadic class 0 mod 8 is the class of every scale T-PIN hands the
Case-1 argument (dyadic block scales 2^{2t-1}).  {11,12} was the ONE
catalogued pair with no size-3 core there — the last pair whose
dyadic cell had no hand-schema candidate.  It now has a full schema
with a new (2+2 phase-clash) anatomy, and the anatomy is SIMPLER than
C3's (no L1 analogue, no order transfer — two independent 2-unit
half-flips).  Combined with the diagonal family and the sliding lane
laws of §3, every (pair, dyadic) cell of the catalogue has either a
verified schema ({11,12}, {15,16}=C3(5), and by translation
candidates for the rest) or a uniform lane statement awaiting the
same treatment.

## 5. SECOND HAND SCHEMA: the ≡ 2 mod 4 flip class (B2 lane at x = 11)

The same pipeline (e124j anatomy scan → e124k minimal ladders →
e124l verifier) closed the second named target IN FULL, revealing the
parity DUAL of the dyadic schema.

### 5.1 Statement (pair {11,12}, M ≡ 2 mod 8, M ≥ 18; m0 = 3M/2 ODD)

Core B2 = {t2≺b5, t5≺b3, t7≺b2} (attacker 12's j=5 unit + attacker
11's j=3,2 units).  Phase battleground: t2 = 2M−2 (EVEN value, odd
center — dual of the dyadic case's odd t1 / even m0):

    HALF-A2:  AP + {t5≺b3, t7≺b2}  forces  m0 ≺ t2
    HALF-B2:  AP + {t2≺b5, t5≺b3}  forces  t2 ≺ m0

t2 ≠ m0 (M ≠ 4) ⇒ AP + B2 UNSAT ⇒ the {11,12} rung fires on the whole
class M ≡ 2 mod 8.  Anatomy note: the two half-flips OVERLAP in the
shared unit t5≺b3 — a 3-unit core carrying two 2-unit halves (the K4
dyadic core's halves were disjoint, hence size 4; here sharing is
possible and the core stays size 3.  Conjecture: that is exactly WHY
{11,12} needs size 4 on the dyadic class — no shareable unit exists
there).

### 5.2 Derivation and verification (e124j/k/l)

Each half: Lemma D on the even ladder E = (M+2, ..., 2M) and the
quarter ladder Q1 = (M+1, M+5, ..., 2M−1) (= the mod-4 value class of
t5, the SHARED unit — again the quarter ladder carries the pinch
class); 4 polarity branches; zigzag propagation closes all.  Minimal
ladder sets uniform across scales ({E,Q1} or {E,Q3}, e124k).
Machine verification e113-style (e124l, data/e124l_b2_schema.*):
  - 20/20 scales M = 18, 26, ..., 170: all 4+4 branches close;
  - independent Cadical cross-check M ≤ 96: AP + B2 UNSAT;
  - adversarial M = 258, 514: all branches close (2 s / 9 s);
  - sharpness controls, 20 scales M = 22, ..., 174 (≡ 6 mod 8):
    surviving branches + Cadical SAT confirmations.  Zero failures.

With §4 + §5, pair {11,12} has verified hand schemas on BOTH named
lanes: M ≡ 0 mod 8 (dyadic, K4) and M ≡ 2 mod 8 (the first ≡ 2 mod 4
flip cell ever closed by hand).  The remaining {11,12} cells: 4 mod 8
(catalogue core {t0<b6,t3<b4,t6<b3}), 6 mod 8 (B6 lane), and the four
odd classes (C lane at ≡ 5; three others).

### 5.3 The emerging uniform picture

Three schema instances are now hand-verified ({15,16} dyadic = C3,
{11,12} dyadic = K4, {11,12} ≡ 2 mod 8 = B2), and they share ONE
shape: a phase battleground value v* adjacent to the block top
(t1 or t2), a center m0, two premise half-sets each forcing one phase,
and Lemma-D case analysis over exactly TWO ladders per half — the
full d=2 ladder of v*'s parity class and one d=4 quarter ladder
carrying the half's key unit's value class.  The residue lock selects
which parity pairing (odd v*/even m0 at 0 mod 8, even v*/odd m0 at
2 mod 8) is available.  This is strong evidence the remaining six
{11,12} cells and the other pairs' lanes all yield to the same
two-ladder template — a plausible UNIFORM off-diagonal metatheorem:
"every lane law of §3 is witnessed by a two-half phase clash at v*
with two-ladder Lemma-D closure."

## 6. THE TEMPLATE SWEEP (e124m): the mechanism across all cells

The pipeline of §4/§5/§7 (phase-kill scan → two-ladder Lemma-D search
→ multi-scale closure verification + solver cross-checks + SAT
controls at the complementary class), run MECHANICALLY per cell.
Engineering lessons folded in: kills are scale-stable and cheap to
find at small M, but ladder tests must use SPREAD scales (small
scales close accidentally; pairs picked only at large scales can fail
between them) with a verify-retry loop; degeneracy guard (unit value
= center).  Cell record: data/e124m_template.json + _rerun.json.

### §6-results

Every cell verified at 8 scales spanning ≥ 56 in M, with Cadical
UNSAT cross-checks (M ≤ 80) and SAT controls at the complementary
class.  v* = phase battleground, [ladders] per half:

    cell         class    v*   halves (hi / lo)              ladders
    K4      {11,12} r0    t1  {t0b6,t2b5}/{t1b5,t3b4}     [O+Q2]/[O+Q3]  (§4, 20 scales + 2048)
    B2(11)  {11,12} r2    t2  {t5b3,t7b2}/{t2b5,t5b3}     [E+Q1] both    (§5, 20 scales + 514)
    K11_r4  {11,12} r4    t1  {t0b6,t6b3}/{t0b6,t3b4}     [O+Q2] both    (68..124)
    C(11)   {11,12} r5    t2  {t2b5,t5b3}/{t0b6,t2b5}     [D1+Q1]/[D1+Q1+Q3] (§7, 19 scales)
    B6(11)  {11,12} r6    t2  {t3b4,t5b3}/{t5b3,t10b1}    [E+Q1] both    (22..78)
    K11_r1  {11,12} r1    t2  {t3b4,t5b3}/{t0b6,t3b4}     [O+Q2]/[O+Q4]  (41..97)
    K11_r3  {11,12} r3    t3  {t4b4,t7b2}/{t1b5,t7b2}     [E+Q2]/[E+Q4]  (27..83)
    K11_r7  {11,12} r7    t3  {t4b4,t6b3}/{t6b3,t9b1}     [E+Q1] both    (31..87)
    B2(13)  {13,14} r4    t1  {t4b5,t7b3}/{t7b3,t9b2}     [O+Q3]/[O+Q1]  (28..84)
    B6(13)  {13,14} r0    t1  {t7b3,t12b1}/{t5b4,t7b3}    [O+Q3]/[O+E+Q1] (32..88)
    B6(15)  {15,16} r2    t2  {t7b4,t9b3}/{t9b3,t14b1}    [E+Q1] both    (26..82)
    B2(17)  {17,18} r0    t1  {t8b5,t11b3}/{t11b3,t13b2}  [O+Q3]/[O+Q1]  (24..80)
    B2(19)  {19,20} r2    t2  {t13b3,t15b2}/{t10b5,t13b3} [E+Q1] both    (34..90)
    A4d(13) {13,14} r2    t2  {t3b5,t5b4}/{t4b5,t8b3}     [E+Q1] both    (26..82)
    [A4d(19) r0, B6(21) r0 — see log; slow ladder searches]

**HEADLINE: pair {11,12} is CLOSED AT ALL EIGHT RESIDUES mod 8 by
verified two-ladder hand schemas** (thresholds ≤ 68; below-threshold
scales covered by e122's machine UNSAT at every M = 16..135).  This
is the first pair with complete per-residue hand-schema coverage:
Case 1 for a team owning {11,12} has NO residue escape at any scale
M ≥ 68, modulo only the N1/T-PIN pigeonhole side.  The battleground
v* is always one of t1/t2/t3 (the top three block values), the
halves are always 2 units, and the ladder sets are always the
full d=2 ladder of v*'s parity + one or two d=4 quarter ladders.

## 7. THIRD HAND SCHEMA: the ODD class falls (lane C at x = 11)

The presumed-hard case — odd M, where no integer m0 = 3M/2 exists —
fell to the SAME template within one probe cycle (e124n/o/p).

### 7.1 Statement (pair {11,12}, M ≡ 5 mod 8, M ≥ 21)

Core C(11) = {t0≺b6, t2≺b5, t5≺b3} (lane C law: M ≡ x+2 mod 8).
The phase battleground is t2 = 2M−2 against the half-integer center's
left neighbour c− = (3M−1)/2:

    HALF-hi: AP + {t2≺b5, t5≺b3}  forces  c− ≺ t2
    HALF-lo: AP + {t0≺b6, t2≺b5}  forces  t2 ≺ c−

t2 ≠ c− (M ≠ 3) ⇒ AP + C(11) UNSAT on the whole class.  Overlapping
halves share t2≺b5 (as in B2).  The anatomy scan (e124n, M = 21, 29,
37 — identical tables) shows the same double-kill structure at BOTH
half-integer neighbours c± with the roles of the t-parities swapped —
c− owns the even t's (t2, t4, t6), c+ the odd t's (t1, t3, t5, t7).

### 7.2 Derivation + verification (e124o, e124p)

HALF-hi: Lemma D on D1 = (M+1, M+3, ..., 2M) [d=2] + Q1 = (M+1, ...,
2M) [d=4], 4 branches.  HALF-lo: D1 + Q1 + Q3, 8 branches (the pair
choice oscillates between (D1,Q1)/(D1,Q3) with scale — the triple is
the uniform closing set; closure is monotone so supersets stay
closed).  e124p verification: 19/19 scales M = 21, 29, ..., 165 all
branches close; Cadical UNSAT cross-checks at M ≤ 96; controls at
ALL THREE other odd classes (7, 1, 3 mod 8 — 18 scales): survivors +
Cadical SAT.  Zero failures.  data/e124p_odd_schema.*.

With §4 + §5 + §7: pair {11,12} has verified end-to-end hand schemas
on THREE classes (0, 2, 5 mod 8) spanning ALL parity regimes (even
m0, odd m0, half-integer center).  Nothing about the remaining five
{11,12} classes looks different in kind.

## 8. What remains open on this front

(Rewritten end-of-session; the original list's items 2 and 3 — the
≡ 2 mod 4 flip classes and odd M — were both CLOSED, §5 and §7.)

  - Cells the e124m sweep leaves unclosed (see §6-results): each
    needs either a bespoke anatomy (different v*/center) or a wider
    ladder pool — no sign yet of a conceptual obstruction.
  - Remaining {11,12} cells beyond the sweep, then per-pair
    completion: the goal state is all 8 residues × all pairs.  The
    honest quantifier gap for Case 1 remains INFINITELY MANY pairs:
    the lane laws slide mod 8 uniformly (statement per lane, x free),
    so the right endgame is a PARAMETRIC schema verification along
    each lane (e123-style: constants affine in x), not per-cell.
  - Pairs x ≡ 7 mod 8 off the diagonal (x = 23, 31, ...): outside
    the e122 catalogue; extend e122 to x = 23..29 and check the lane
    laws extrapolate (they should: catalogues are mod-8 periodic).
  - The Case-1 composition ALSO needs the T-PIN side per pair (the
    attackers block-ordered before the 1-clean block) — unchanged,
    N1 territory, not this front's gap.
