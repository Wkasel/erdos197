# 71 — FRONT J/F-SCHEMA: the uniform hand schema for the telescope's
# residual family (the (v,0) pump cells and the F freshness cells)

Task: write the uniform hand schema behind [GAP-J-schema] /
[GAP-F-schema] (notes/70) — (1) anatomize the (12,0)@8 exact cell,
(2) generalize via the 50-value (16; 6,0) MUS bands, (3) prove for
all M ≡ 0 mod 8 or state the exact residue casework; machine-check
at 8/16/24 (+32).

Machine companion: scratch tools (fmass/interval/zsumset, inlined
below as e174_jf_schema.py) + e158c fixed-coloring pricer + e158b
MUS at (8; 11,0); records data/e174_*, data/e158b_mus_M8_up11_dn0.*.

**Verdict of the front in one line: the (v,0) family has a uniform
two-case hand schema — every balanced coloring is either LOW-PURE
(its bottom two blocks single-parity), in which case Lemma K kills
the low chain outright at EVERY budget for every M ≥ 12 (M ≡ 0 mod
4 — no residue casework needed beyond this), or LOW-IMPURE, in
which case it carries forced sumset mass μ_up + μ_skip ≥ f(M) on
some team, paid unit-for-unit in s2 by L-PREFIX — with f(M) = M/2
measured EXACTLY at M = 8, 12, 16 (f = 4/6/8, min-max both teams);
so (v,0) is UNSAT for every v < M/2, all M ≡ 0 mod 4, M ≥ 12,
modulo one new counting lemma [GAP-FHALF: f(M) ≥ M/2, no orders
involved], and v_min(0)(M) ≥ M/2 → ∞ — [GAP-VMIN0-growth]'s
divergence reduces to the same counting lemma.  M = 8 is the
exceptional scale (its low chain is Lemma K's SAT cell (6,2)):
there the low-pure class survives at finite price — the complete
anatomy of v_min(0)(8) = 12 is §2, and every piece of it
(safe-zone, chain law K(24,8) = 40, the 6+7 witness anatomy) is
the M ≥ 12 schema's mechanism at the one scale where it is
finite.**

## 0. Pod harvest: vmus_cert.log is MIS-INSTRUMENTED — discard

/root/e/data/vmus_cert.log on sprint-C reads
`CERT M=8 (up=11,dn=0): SAT [0s]`, which LOOKS like a refutation of
the local (11,0)@8 UNSAT [40.6 s, e173].  It is not: the pod's
run_vmus.py imports `solve_budget` from e127_seam_budget — the
3-BLOCK per-TEAM-budget instrument — so the cell it solved is the
3-block window (8, 64] with team budgets (vA, vB) = (11, 0), which
is SAT consistently with v*(bal,8) = 0 (notes/62 §2: the standalone
anchor-8 window has a seam-clean escape; budgets don't bind).  The
pod never had e158/e173 pushed to it.  Verdict: harvest DISCARDED
as a certification of the pump cells; the (11,0)@8 UNSAT stands on
the local e173 run (Cadical195, 40.6 s) and the (12,0)@8 SAT
witness is independently audited (e173 audit_chain).  [Proper pod
work relaunched this session: the f(M) counting ladder, §3.]

## 1. The reduction, and what the (v,0) cell IS

Notation as notes/62: values (M/2, 8M], blocks Bm1 = (M/2, M],
B0 = (M, 2M], B1 = (2M, 4M], B2 = (4M, 8M]; exact per-team balance
per block (M ≡ 0 mod 4 so |Bm1| = M/2 is even); budgets vup on
inverted s1 ∪ s2 pairs, vdn on s0 ∪ s1 (s1 shared).

**Lemma R0 (reduction) [PROVED — one line, notes/62 §4c].**  At
vdn = 0 both teams are wholesale block-ordered
[Bm1∩T] ≺ [B0∩T] ≺ [B1∩T], and s1 spending is doubly banned, so
the full budget vup prices s2 alone: the (v,0) cell is, per team,
"weave B2∩T into the forced chain Bm1→B0→B1 with ≤ v inverted
(B1, B2) pairs, monotone-3AP-free."  Payment anatomy: a B2-value w
placed before k values of B1∩T costs k (advancement); a B1-value y
placed after j values of B2∩T costs j (delay); total
n_s2 = Σ_{y∈B1∩T} #{w ∈ B2∩T : w ≺ y}.

**The AP families and their prices** (u < y < z, z = 2y − u, all
in T; family = block pattern):

| pattern | forced edge under R0 | price |
|---|---|---|
| in-P families ((−1,−1,−1)..(0,0,0)) | breakable by within-block order | 0, but ORDER-constrained — this is where Lemma K lives |
| (−1,0,1) = H_dn | u≺y and y≺z both forced | IMPOSSIBLE — μ_dn = 0 or instant UNSAT [L-PREFIX(i)] |
| (0,1,2) = H_up, (−1,1,2) = SKIP | u≺y forced ⟹ z≺y forced | 1 s2 unit each, edges pairwise distinct [L-PREFIX(ii,iii)] |
| (0,1,1), (−1,1,1) | z≺y within B1 | 0, B1-order-constrained |
| (1,1,2) | z≺y (s2) OR y≺u (B1-internal) | 0 or 1 — the mixed engine's currency |
| (1,2,2), (0,2,2), (−1,2,2), (2,2,2) | breakable within B2 | 0, B2-order-constrained |

So the cell splits into a COUNTING layer (μ_dn must vanish;
μ_up + μ_skip is a hard floor on n_s2) and an ORDER layer (the
within-block orders of the chain and of B2 must jointly break the
price-0 families; their interaction with the weave is the mixed
tax).  Everything below is organized by which layer kills.

## 2. The M = 8 exact cell, complete anatomy (v_min(0)(8) = 12)

At M = 8 the instance is 60 values (4/8/16/32 per block), the only
scale where the low chain escapes Lemma K — the schema's mechanisms
all appear at FINITE price, which is exactly why the cell is worth
anatomizing by hand.  All machine facts below are seconds-cheap and
re-runnable (e174; fixed-coloring queries via e158c).

### 2a. The low-chain dichotomy at 8

Call a balanced coloring **low-pure** if each team's low set
L(T) = (Bm1 ∪ B0) ∩ T is single-parity.  Balance forces the count
|L(T)| = 3M/4 = exactly the size of one parity class of (M/2, 2M],
so low-pure means L(A), L(B) = the odd/even classes — the parity
low-schedule, with B1/B2 still free.

- **Low-pure branch.**  The low chain L(T) ≅ the integer interval
  [1, 3M/4] (parity class ↦ interval via v ↦ (v − M/2 + 1)/2, so at
  M = 8 the odds {5,...,15} ↦ [1..6]; APs correspond exactly), with the
  s0-forced prefix condition "Bm1-part (M/4 = 2 values) before
  B0-part (M/2 = 4 values)".  This is Lemma K's cell
  (n, k) = (6, 2) — its SHARP SAT cell (Lemma K kills only from
  n ≥ k + 5).  So at M = 8 (and ONLY at M = 8: M ≥ 12 gives
  n = k+M/2 ≥ k+6) the low-pure class survives the order layer of
  the low blocks, and its price is set higher up.
- **Low-impure branch.**  μ_dn = 0 plus balance plus impurity
  force sumset mass: f(8) = 4 (§3's counting function, measured
  exact) — every low-impure balanced coloring with μ_dn = 0 has a
  team with μ_up + μ_skip ≥ 4.  (At M = 8 this branch is priced
  BELOW the low-pure branch's 12 — the impure escapes at budget
  4..11 are excluded by the mixed engine, not by counting alone;
  the exact-12 statement rides the machine UNSAT at 11.  At the
  schema scales M ≥ 12 the branch comparison reverses: low-pure
  dies at every budget and impure counting is the whole bound.)

### 2b. The safe-zone lemma (where defectors may live)

**Lemma SZ [PROVED — two-line image computation].**  Let T be
low-pure of parity p (M ≡ 0 mod 4, M ≥ 8).  The H_dn images
z = 2y − u over u ∈ Bm1∩T, y ∈ B0∩T are exactly the parity-p
values of (2M, z_max], z_max = 7M/2 − 3 for the odd team and
7M/2 − 2 for the even team (upper end: z ≤ 2·max(B0∩p) −
min(Bm1∩p); fullness: for any target z pick u ≡ 2 − z mod 4, both
odd — resp. even — residues mod 4 exist in Bm1∩p once M/4 ≥ 2, and
y = (z+u)/2 lands in B0∩p).  So μ_dn = 0 ⟺ T's B1 values of parity
p (its "defectors") all lie in the SAFE ZONE (z_max, 4M] — exactly
M/4 + 1 parity-p values for either team.  At M = 8: safe odds
{27, 29, 31}, safe evens {28, 30, 32} (the witness's B-side B1
evens are exactly {28, 30, 32} — measured consistent).  ∎

This is the first band of the schema: **the top quarter-ish of B1
is the only place a low-pure team may host same-parity B1
material.**  (Compare the (16; 6,0) MUS: B1 enters as the LOWER
two-thirds — the support stops where the safe zone starts, the
same law seen from the UNSAT side.)

### 2c. The parity-schedule chain law at 8: price = K(3M, M) = 40

For the exact schedule (1,1,0,0) (zero defectors anywhere) the two
parity chains of each team decouple (cross-parity APs need a
middle in the other chain's range — impossible here; the
SCHED-DEAD decomposition of notes/62 §4d), so the cell price is
EXACTLY the interval-budget invariant:

    K(n, k; v): interval [1..n], low [1..k] wholesale-before,
    ≤ v inverted (low, high) pairs, monotone-3AP-free order.
    K(n, k) := least SAT v  (Lemma K says K(n,k) > 0 for k ≥ 2,
    n ≥ k+5; K becomes the BUDGETED Lemma K).

The even chain of team A ≅ [1..3M] with low [1..M] and the s2
budget counting exactly the (low, high) inversions; the odd chain
is the free (6,2) cell.  Machine (this session, two INDEPENDENT
encoders — e158c on the full gadget with fixed coloring, and a
standalone 24-value interval solver):

    fixed-coloring (1,1,0,0) @ M=8:  UNSAT at v = 39, SAT at 40
    standalone interval:             K(24, 8) = 40 (UNSAT 39/SAT 40)

Exact agreement — the chain decomposition is machine-exact at 8,
and the parity schedule pays 40 ≫ 12: **the pure schedule is
nowhere near optimal at 8; defectors are how the witness gets to
12.**

### 2d. The 12-witness anatomy (the exact cell's SAT side)

The e173 (12,0)@8 witness (independently audited) is a low-pure
defector coloring, B = A + 1 (shift-mirror):

    A = odds of (4,16] ∪ {18,20,22,24,26} ∪ {27,29,31}   [B1]
        ∪ {34,36,38,40,44,46,48,50,52,54,56,58,62} ∪ {41,59,63} [B2]

- B1 defectors = {27,29,31} = the FULL safe zone (Lemma SZ sharp);
  B2 defectors {41, 59, 63}.
- Sumset masses (μ_dn, μ_up, μ_skip) = (0, 2, 1) — floor 3.
- Payment n_s2 = 12 per team, in TWO monolithic moves:
  (i) ONE advanced B2-defector: 41 ≺ {24, 26, 27} is FORCED (41
  completes the mono triples (7,24)→41 [skip], (11,26)→41 [up],
  (13,27)→41 [up] — the entire μ-floor lands on one z-value), and
  the placement drags 41 ≺ {18, 20, 22} as transitive collateral:
  6 units;
  (ii) ONE delayed B1-value: 24 placed after {34, 46, 48, 50, 59,
  63} ∪ {41}: 7 units (−1 shared) — delaying 24 breaks the fan of
  APs (24, b, 2b−24), b ∈ B2∩A ({34, 41}: both broken by delay;
  (24,36,48)/(24,38,52)/(24,40,56) broken inside B2 instead),
  and the deep delay position (after six B2 values) is transitive
  collateral of 34's late slot.
  Total 6 + 7 − 1 = 12 = saturated budget, all on s2 — the shape
  notes/70 recorded as "the lavish export is the forced shape
  under vdn = 0", now resolved into "forced fan + collateral".
- BOTH teams identical (shift-mirror) — the cell's optimum is
  symmetric at 8.

So v_min(0)(8) = 12 decomposes as 3 (sumset floor, L-PREFIX) + 9
(mixed tax: 3 advancement collateral + 6 delay collateral) — the
mixed engine already dominates at the bottom scale.  The UNSAT
side at 11 is machine (40.6 s Cadical, e173); its deletion-MUS is
running (e158b, harvested in §4 below) — the pre-registered band
prediction is committed in §4 BEFORE harvest.

### 2e. What is and is not hand-proved at 8

[PROVED]: R0, SZ, the chain decomposition for the exact schedule,
Lemma K's (6,2) SAT base, the forced-fan reading of the witness
(each of the 12 edges is either a forced L-PREFIX edge, a forced
fan-break, or transitivity collateral of one — checkable by hand
from the order printed above).  [MACHINE]: the exact thresholds
11/12 (full coloring space) and 39/40 (fixed schedule; two
encoders).  A complete hand derivation of "≥ 12 over ALL
colorings" would need the low-pure mixed-tax analysis at 8
(defector calculus over the ≤ 3+3 safe-zone choices — finite but
not written) and the impure interpolation 4..11; NOT attempted —
at 8 this is anatomy, not schema: the M ≥ 12 schema (§3) never
needs the mixed engine.

## 3. The uniform boot schema: Theorem J-BOOT

The dichotomy discovered on the way to the M = 8 anatomy turns out
to be the uniform law for the whole (v,0) family — stated here
with its division of labor against notes/75's Theorem J-DOWN
(which collapses the family into the half-anchor coupled core for
M ≥ 32): **J-BOOT is elementary (Lemma K + one counting lemma —
no CORE′/N6a machinery), uniform over ALL M ≡ 0 mod 4, M ≥ 12,
and is the only uniform law in the boot window M ∈ {12, 16, 20,
24}, exactly where J-DOWN's half-core does not fire.**

**Theorem J-BOOT [PROVED modulo GAP-CMIN].**  Let M ≡ 0 (mod 4),
M ≥ 12, and consider U4(M; bal; v, 0).  Every balanced coloring
falls into exactly one of:

1. **μ_dn > 0**: some mono H_dn triple; both its edges are forced
   by the vdn = 0 block order — infeasible outright [L-PREFIX(i)].
2. **μ_dn = 0, low-pure** (each team's (Bm1 ∪ B0) single-parity):
   balance makes each team's low set the FULL parity class of
   (M/2, 2M] ≅ the interval [1, 3M/4] with prefix M/4 (§2a), the
   prefix wholesale-first by s0 ∪ s1 cleanliness.  Lemma K
   (bases (7,2)/(8,3), k = M/4 ≥ 3, n − k = M/2 ≥ 6) kills the
   chain — infeasible at EVERY budget vup.
3. **μ_dn = 0, low-impure**: some team carries sumset mass
   μ_up + μ_skip ≥ f(M), and L-PREFIX(ii,iii) charges each such
   triple a distinct s2 unit: n_s2 ≥ f(M).  Infeasible for every
   vup < f(M).

Hence (v, 0) is UNSAT for all v < f(M), where

    f(M) := min over balanced μ_dn = 0 LOW-IMPURE colorings of
            max_T (μ_up + μ_skip)(T)

is a pure coloring-layer (counting) function — no order variables.

**Measured: f(M) = M/2 EXACTLY at FIVE scales** (e174 fmass, local
8/12/16 + sprint-C pod 20/24; scan UNSAT at every m < M/2, SAT
witness at M/2):

    f(8) = 4, f(12) = 6, f(16) = 8, f(20) = 10, f(24) = 12.

[GAP-FHALF] f(M) ≥ M/2 for all M ≡ 0 mod 4 — reduced to GAP-CMIN
below.  Corollaries, modulo that one tag:

- **v_min(0)(M) ≥ M/2 for every M ≡ 0 mod 4, M ≥ 12** — in
  particular the whole boot window; combined with Theorem J-DOWN
  (v_min(0)(M) = ∞ for M ≥ 32, notes/75) the (·,0) demand family
  is now covered at EVERY anchor: boot by J-BOOT, large by J-DOWN.
- The pump cells (6,0)@16, (6,0)@24, (5..7,0)@anything in range
  are schema instances, not isolated machine facts.

**Residue casework (task question 3): there is NONE beyond
M ≡ 0 mod 4.**  The instance requires M ≡ 0 (mod 4) (even block
halves and integral M/4); given that, every ingredient (Lemma K
thresholds, the interval isomorphism, L-PREFIX, the f-law) is
uniform in M, and f(M) = M/2 is measured on BOTH residues mod 8
(8/16/24 ≡ 0, 12/20 ≡ 4).  M = 8 is the unique exceptional scale:
case 2's chain is Lemma K's sharp SAT cell (6, 2), which is why
v_min(0)(8) = 12 is finite and its witness is low-pure (§2).  The
task's "M ≡ 0 mod 8" guess was the wrong class — the family is
mod-4 uniform with a single boot anomaly at 8.

**End-to-end machine checks (sprint-B, e173 encoder, fresh scales
AND fresh residues, all this session):**

    ( 5,0)@12 UNSAT [1.1 s]   (schema: v < 6)   — NEW scale, ≡ 4 mod 8
    ( 7,0)@16 UNSAT [2.9 s]   (schema: v < 8)   — first cell beyond the
                                                  measured (6,0); predicted
                                                  by f(16) = 8 before the run
    ( 9,0)@20 UNSAT [8.5 s]   (schema: v < 10)  — NEW scale, ≡ 4 mod 8
    (11,0)@12 UNSAT [7.0 s]   beyond the counting bound — mixed tax
    (19,0)@20 UNSAT [9.5 s]     (consistent with J-DOWN-side behavior;
                                 not claimed by J-BOOT)

Zero mismatches with any prediction; the two beyond-bound cells
show the counting floor is not the whole truth at boot scales
(the mixed engine tops up, as at M = 8).

## 4. The counting lemma: anatomy and proof skeleton [GAP-CMIN]

**Reduction CMIN→FHALF [PROVED — three lines].**  For a coloring
write c_T(z) = #{(u, y) ∈ (low∩T) × (B1∩T) : 2y − u = z} for
z ∈ B2.  Then Mass(T) := μ_up + μ_skip = Σ_{z ∈ B2∩T} c_T(z), so

    Mass(A) + Mass(B) ≥ Σ_{z ∈ B2} min(c_A(z), c_B(z)) =: S(col)

(each z lands in one team and contributes at least the min), and
max_T Mass ≥ ⌈S/2⌉.  The B2 coloring has vanished: S depends only
on the split of low ∪ B1.  Define cmin(M) = min S over balanced
μ_dn = 0 LOW-IMPURE splits of low ∪ B1.  Then f(M) ≥ ⌈cmin(M)/2⌉.

**Measured: cmin(M) = M exactly at 8, 12, 16** (adversarial
side-selection encoding; UNSAT at every m < M, SAT at M) — and the
f-witness at 8 realizes S = 8 = M with the 4/4 split: BOTH
inequalities of the reduction are tight.  [GAP-CMIN]: S ≥ M for
every balanced μ_dn = 0 low-impure split — pure combinatorics of
one seam of colors, THE remaining hand target of the (·,0) family.

**The discontinuity that explains the dichotomy.**  For LOW-PURE
splits S = 0 identically (an odd z has all its low-representatives
u ≡ z odd, and the even team owns no odd low values — one of
c_A, c_B vanishes at every z).  One impurity makes S jump to M:

**Proof skeleton (the two-channel sweep) — the partner conditions
are the open residue.**  Low-impure gives d ∈ low∩A even and
r ∈ low∩B odd (both teams have both parities: if one team's low
were pure, its partner's low would be the complementary full
parity class, pure too).  For y ∈ B1 define the two channels

    z_r(y) = 2y − r  (odd),    z_d(y) = 2y − d  (even).

For every y ∈ B1 with y > 2M + max(r, d)/2, both z's land in B2
with y as a legal representative pair-partner (u = r resp. d).
The sweep interval I = (2M + max(r,d)/2, 4M] has ≥ M values
(max(r,d) ≤ 2M).  Every y ∈ I is colored: y ∈ B gives
c_B(z_r(y)) ≥ 1 via (r, y); y ∈ A gives c_A(z_d(y)) ≥ 1 via
(d, y).  The maps y ↦ z_r(y), y ↦ z_d(y) are injective and the
two channels are parity-disjoint, so DISTINCT y ∈ I contribute at
DISTINCT z: if every such z also has a representative on the
OTHER team (the partner condition), then S ≥ |I| ≥ M.  ∎(skeleton)

The partner condition is where balance and μ_dn = 0 must enter
(each z needs one opposite-team pair (u', y') with y' in an
explicit 3M/4-long window — a dodging team must concentrate its
B1 mass, which feeds the other channel; the extremal witnesses
confirm the tension is real and exactly balanced).  Sharpness
check: the f(8)-witness's impurity sits at d = 16 = 2M — the TOP
of B0 — making |I| = M exactly; the measured cmin = M says the
adversary can achieve the sweep bound but never beat it.

## 5. The F-schema: the same dichotomy prices the freshness family

notes/75 §2.4 leaves F(N; v) [GAP-F-schema] as a family that does
NOT collapse (one-seam theories are SAT; F keeps genuine joint
content at every scale).  The J-BOOT engine transfers — the ONLY
property of vdn = 0 that case 2 used was s0-cleanliness, which F
has by definition:

**Theorem F-BOOT [PROVED modulo GAP-FTOT].**  Let M ≡ 0 (mod 4),
M ≥ 12, and consider F(M; v) (s0 = 0; n_s1 + n_s2 ≤ v per team)
with v < M/2.  Then:

1. **Low-pure colorings are infeasible at EVERY v** — Lemma K on
   the low chain needs only the s0-forced prefix.  (For v ≥ M/2
   nothing is claimed; a B1-value jumped before Bm1 costs ≥ M/2
   s1-inversions, see step 3, so the chain hypothesis holds
   whenever v < M/2.)
2. **Low-impure colorings pay ⌈mass_tot/2⌉:** with v < M/2 every
   B1∩T value sits after every Bm1∩T value (jumping one costs
   ≥ |B0∩T| = M/2 s1-units, over budget), so: each mono H_dn
   triple charges its s1 edge (y, z); each mono H_up triple
   charges its s1 edge (u, y) or its s2 edge (y, z); each mono
   SKIP triple charges its s2 edge.  An s1 pair (b0, b1) serves at
   most 2 triples (one H_dn as (y,z), one H_up as (u,y)); an s2
   pair serves at most 1 (its u = 2y − z is in exactly one block).
   Hence v ≥ n_s1 + n_s2 ≥ (μ_dn + μ_up + μ_skip)/2 ≥ f_F(M)/2,

   f_F(M) := min over balanced LOW-IMPURE colorings (μ_dn free!)
             of max_T (μ_dn + μ_up + μ_skip)(T).

**Measured: f_F(8) = 4, f_F(12) = 6 — EQUAL to f(M) = M/2** (pod
ladder; f_F(16) descending, ≥ 6 at harvest).  Letting μ_dn > 0
does not help the adversary at the measured scales.  [GAP-FTOT]:
f_F(M) ≥ M/2 (implied by GAP-CMIN if the μ_dn-free minimum keeps
matching f; the CMIN reduction applies verbatim to the
μ_up + μ_skip part).

**Corollary F1: F(M; v) UNSAT for every v < ⌈M/4⌉, uniformly in
M ≡ 0 mod 4, M ≥ 12 [modulo GAP-FTOT].**  This is the first
uniform-in-M statement ever produced for the freshness family:
T-FRESH's hypothesis [GAP-F-schema] now has a proved-modulo-one-
counting-lemma instance family at every scale — density-one fresh
minting with v(N) = ⌈N/4⌉ − 1 — rather than a single machine point
(16; 6).  The measured F(16; 6) UNSAT [983.5 s] sits 2 units above
the counting bound (v < 4): the F mixed engine tops up exactly as
the (·,0) one does.  What F1 buys T-TEL′/T-FRESH at ω: branch (b)
freshness holds with any budget curve below M/4, no appeal to the
half-core, no N6a dependency — an INDEPENDENT second engine under
the telescope's disjointness theorem.

## 6. The margin family: the budgeted Lemma K is its low-pure engine

notes/75 §2.4's other residue is the margin family
U4(M; v, w), w ≥ 1.  Case 2 of J-BOOT generalizes verbatim: under
vdn = w, a low-pure team's chain (≅ [1, 3M/4], prefix M/4) may
carry at most w inverted (prefix, rest) pairs — i.e. the LOW-PURE
branch of the (v, w) cell is governed by the BUDGETED Lemma K:

    K(n, k) := least v such that [1..n] with low [1..k] admits a
    monotone-3AP-free order with ≤ v inverted (low, high) pairs.

**Lemma MARGIN-LP [PROVED].**  If w < K(3M/4, M/4) then every
low-pure coloring is infeasible in U4(M; v, w) for every v.
(The chain's (prefix, rest) inversions are s0 pairs ≤ w.)

**Measured K-diagonal (e174 interval, exact — UNSAT at K−1, SAT
at K):**

    K(6,2) = 0    (M = 8:  the boot anomaly)
    K(9,3) = 3    (M = 12)
    K(12,4) = 4   (M = 16)
    K(15,5) = 11  (M = 20)
    K(18,6) = 20  (M = 24)
    K(21,7) = 28  (M = 28)
    K(24,8) = 40  (M = 32; independently = the fixed-parity-
                   schedule price at M = 8 via the §2c chain
                   decomposition — two encoders agree)

No growth law recorded (campaign rule); the raw values suffice
for every margin cell in the boot-and-collapse range: e.g. the
notes/75 margin targets (v, 3)@48 have their low-pure branch dead
by w = 3 < K(9,3)·(scale) — precisely: at M = 48, w < K(36, 12)
(unmeasured, ≥ K(24,8) = 40 by deletion-monotonicity of Lemma K's
step 1... the monotone step gives K non-increasing in n at fixed
k is FALSE in budget form; K(36,12) needs its own run — queued).
The impure branch at w ≥ 1 loses L-PREFIX(i)'s hard μ_dn = 0
(≤ w mono H_dn triples become payable) — the margin analogue of
case 3 needs the mass function at μ_dn ≤ w [GAP-MARGIN-MASS,
scoped, not attempted].

