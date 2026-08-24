# The subset-escape algebra (2026-08-24)

Task: test and explain the conjecture that removing the defect class
D = {v ∈ B : v ≡ 2 mod 2^{k/2}} (k = log2(2M)) from B = (M, 2M] restores
feasibility of the fatal-zone system (a)+(b) with zone Z = (M/4, M/2].
Scripts: `experiments/e52_subset_escape.py` (parts 1, 2, era systems),
`experiments/e52c_suffix.py` (suffix/nested/append systems),
`experiments/e52b_floats.py` (float minimization; superseded, see §3),
scratch `e51_noextras.py`, `e51_res.py`, `e51_res_d3.py` (ladder variants).
All SAT results are exact (CaDiCaL, lazy-transitivity OrderSAT of e3);
every SAT witness re-verified by the independent checker.

## 0. Headline (honest): the hypothesis as posed is FALSE — and what is true

1. **B ∖ D with pre-placed zone is UNSAT for M = 32, 64, 128** (both the
   single-level zone Z = (M/4,M/2] and the full team zone Z_M). Only M = 16
   escapes — and at M = 16 *almost everything* escapes (14 of the 16
   single-value removals — all except {20} and {30} —, every tested class,
   10/10 random 4-subsets). The empirical basis of the "removal
   restores feasibility" reading was the marginal M = 16 case; it does not
   scale.
2. No thin-class removal works at M ≥ 32: classes ≡2 mod 4/8/16/32,
   ≡1 mod m, ≡6 mod m, and 0/10 random |D|-subsets — all UNSAT.
3. The minimal fatal-zone repair at M = 32 (zone Z_M) has size **3**, and is
   **unique**: {34, 36, 61} (exhaustive over all C(32,1), C(32,2), C(32,3)).
   Moreover **D plus any single extra value never works** (all 28 extensions
   UNSAT). The defect class is not even close to a repair set of the
   zone-preplaced system.
4. The verified defect-law ladders (e50/e51) escape by a *different*
   mechanism: **interleaving/reservoirs**. No-extras variants of the law
   ladder (P_i = exactly [1, comp_i] ∖ D_i) are UNSAT at every tested (X, d)
   — (4,2), (16,2), (4,3). The SAT witnesses place essentially the whole
   next block (minus *its* defect) **before** the level boundary: at X=4,
   d=2 the level-0 state (comp 16) already contains all of (32,64] except
   D_64 = {34,42,50,58}; the boundary-respecting tail is just D_16 = {10,14}.
5. What *is* true — the corrected subset-escape law (verified M = 32…128):
   the defect class is a **deferrable suffix of the complete state**. With
   V = team ∩ [1, 2M]:
   - `[bulk | D_{M/2} | D_{2M}]` is SAT for M = 32, 64, 128
     (bulk = V minus both defects); the reversed stacking
     `[bulk | D_{2M} | D_{M/2}]` is **UNSAT** at all three — defects must be
     released in scale order.
   - **Any** residue class of B mod m works as a suffix (≡2, ≡6, ≡1 mod m;
     ≡2 and ≡m+2 mod 2m — all SAT); **no** random |D|-subset works
     (0/10 at every M), and random subsets *of 2·odd values* degrade with
     scale (10/10 at M=16, 3/10 at 32, 0/10 at 64, 128). The escape is
     **class coherence**, not the specific residue.
   - The residue 2 is not forced by chain depth ≤ 3: law ladders re-pinned
     with defect residue 1, 6, 4, 0, or class ≡2 mod 2m are all SAT at
     (X,d) = (4,2), (16,2), and residues 1, 6 also at (4,3). "≡2 mod
     2^{k/2}" is an emergent preference of unpinned witnesses, not (yet) a
     uniqueness.
6. D-release is witness-dependent: given a *random* AP-free arrangement of
   V ∖ D, the defect can be appended in **0/5** trials (M = 16, 32, 64);
   with a *suitably chosen* bulk arrangement it always can (item 5). The
   bulk must be arranged with foresight — it must anti-orient every pair
   completing into D (see §2).

## 1. Part 1 data (fatal-zone semantics, zone pre-placed)

decide(B∖C, Z) for B = (M,2M]; "law D" = ≡2 mod 2^{⌊k/2⌋}, k = log2(2M).
Identical results for Z = (M/4,M/2] and Z = full team zone.

| M   | full B | ∖ law D | ∖ ≡2 mod 4 | ∖ ≡2 mod 16 | ∖ ≡1 mod m | ∖ ≡6 mod m | random ×10 |
|-----|--------|---------|-----------|------------|-----------|-----------|------------|
| 16  | UNSAT  | SAT     | (=law)    | SAT        | SAT       | —         | 10/10 SAT  |
| 32  | UNSAT  | UNSAT   | UNSAT     | UNSAT      | UNSAT     | UNSAT     | 0/10       |
| 64  | UNSAT  | UNSAT   | UNSAT     | UNSAT      | UNSAT     | UNSAT     | 0/10       |
| 128 | UNSAT  | UNSAT   | UNSAT     | UNSAT      | UNSAT     | UNSAT     | 0/10       |

Minimal repairs at M = 32 (Z_M): size 1, 2 — none (exhaustive); size 3 —
exactly one: {34, 36, 61}; size-4 examples {34,36,38,55}, {33,34,36,38};
removing the whole bottom quarter (33..40) works, removing all 2·odd, all
odds, all evens, or the top even half does not. D ∪ {v} fails for all v.

## 2. Part 2: why D-removal cannot fix the zone-preplaced system

Census at M = 32 (Z = (8,16], D = {34,42,50,58}): 48 (b)-forced pairs, only
12 touch D (as z: (16,33,50),(10,34,58),(12,35,58),(14,36,58),(16,37,58);
as y: the eight (x,34,68−x)); 240 3-AP triples in B, 82 touch D. Eight
distinct minimal UNSAT value-cores (sizes 18–23) were extracted with
different shrink orders: |core ∩ D| ranges over 1..4, and since B ∖ D is
itself UNSAT there are cores disjoint from D. D is not a hitting set of the
core family — no single thin class is, which is the combinatorial face of
the robustness in §1.

**The algebraic mechanism.** Work mod m (m = 2^{⌊k/2⌋}); write completions
of an increasing pair (x, y) as z = 2y − x.

- *Class closure*: if x ≡ y ≡ r (mod m) then z ≡ r. Residue classes are
  completion-closed; a class's internal threats stay internal.
- *Sink structure of one root*: fix a target class r and ask which placed
  pairs threaten to complete into class r: x ≡ 2b − r where b is the class
  of the middle. At class level this is the doubling map φ_r(b) = 2b − r on
  Z/m, whose iterates 2^j(b − r) + r converge to the unique fixed point r
  (2^j ≡ 0 mod m eventually): **the functional graph of φ_r is a tree
  rooted at r**. Hence there exists a linear order of the classes (any
  topological order of the tree, root last) in which every completion into
  class r is anti-oriented, and class r itself can sit at the end. This is
  why *every* residue class is a deferrable suffix (§0 item 5) and why the
  suffix escape needs class coherence — a random subset meets many classes
  and inherits conflicting orientation demands (0/10 SAT).
- *Why the zone kills it*: a pre-placed zone interval (M/4, M/2] contains
  attackers x of **every** residue mod m. Each attacker residue a imposes
  the demands of *its own* tree φ_a — the (b)-constraints "z before y" are
  unconditional because x is already placed. Simultaneously satisfying the
  root-last demands for all roots a ∈ Z/m is impossible; the demands close
  into cycles, which is exactly what the minimal cores exhibit. Deleting
  one class removes one tree's root but leaves the other m−1 root demands
  intact — hence the robustness of the fatal zone under any thin-class
  deletion (§1). (This is the class-level reading of the machine result,
  not yet a hand proof; the cores confirm the cyclic structure but a
  uniform-in-M hand argument is open. Lemma R is the depth-1 instance.)
- *Parity/ν₂ stratification*: z = 2y − x ≡ x (mod 2): the outer terms of an
  AP share parity, so completions of odd-rooted pairs are odd; even values
  2w reproduce the whole problem at half scale (halving descent), so the
  2-adic phases ν₂ = 0, 1, 2, … form nested copies. The defect class
  ≡ 2 mod m is 2·(≡ 1 mod m/2) — an *odd-class problem one level down*.
- *An obstruction worth recording*: within the pure class calculus one
  cannot put an odd class c strictly last among odds: the map
  ψ(b) = 2b − c is a bijection on odd classes whose non-fixed orbits are
  cycles, and "completion after middle forbidden" around a cycle is
  contradictory. The SAT witnesses evade this only via range truncation
  (completions beyond 2M land in the other team's blocks and are free),
  which is why witness anatomies always show a few out-of-phase stragglers
  (e.g. value 2 placed among the odds, 5 and 7 placed late, at M = 64).
  Any hand proof of the suffix lemma must use truncation; a pure
  residue-calculus proof cannot exist.

## 3. The corrected escape: state-suffix law (and reservoir necessity)

Era semantics without extras fails: with P0 = (team ∩ [1, M/2]) ∖ D_Z
pre-placed and era1 = D_Z ∪ (B ∖ D_B), the system is UNSAT for M = 32, 64,
128 in *all* five variants (zone complete or minus D_Z; block minus D_B or
full; D_Z released or absent). Cross-validated in the ladder's own
encoding: no-extras law ladders UNSAT at (4,2), (16,2), (4,3). So the
defect law cannot be stated as a per-block/per-era subset condition with
history fully placed — **reservoir extras are necessary**, and the verified
witnesses use them maximally (whole next block minus its defect placed
before the boundary; the fully-interleaved single state with *free* history
order is SAT even with no defects at all, so at a single boundary the
defect is about *what may be deferred*, not about what must be deleted).

**State-suffix form (machine-verified, M = 32, 64, 128).** Let
V = team ∩ [1, 2M], D_Z = defect of (M/4, M/2], D_B = defect of (M, 2M].
There is an AP-free arrangement of V of the form

    [ bulk = V ∖ (D_Z ∪ D_B)  |  D_Z  |  D_B ]

and none with the defects stacked in reversed scale order. This matches the
verified ladder anatomy exactly (in the (X,d) = (16,2) witness the placed
order ends …, 10, 14 (=D_16), …2·odd stragglers…, 50, 58, 34, 42 (=D_64)).

**Witness anatomy** (nested witnesses, values annotated with ν₂):

    M=32:  all odds (both scales, mixed) · ν₂≥2 values · 2·odd values
           ending 10 14 | 50 58 34 42
    M=64:  same template with stragglers (2 early; 5, 7 late)

**Proof sketch for the suffix lemma (partial).** Phase-order the state:
group g0 = odds, g1 = {ν₂ ≥ 2}, g2 = 2·odd values, with D_Z, D_B as the
tail of g2. Closure checks (all elementary):
- pairs inside g0 complete in g0 — handled by a vdC self-absorbing class
  order (notes/07 theorem);
- (g0 before g1), (g0 before g2): completion is odd, hence in g0, already
  placed — safe;
- pairs inside g1: a = 4a′, b = 4b′ ⇒ z = 4(2b′ − a′) ∈ g1 — internal,
  handled recursively (it is the whole problem two levels down, at quarter
  scale, where the block is short and truncation is generous);
- (g1 before g2): b = 2w (w odd), a ≡ 0 mod 4 ⇒ z = 2b − a ≡ 2 mod 4… lands
  in g1 ∪ earlier (ν₂(z) ≥ 2 since z = 4(w − a/4 + …)); checked: z ≡ 0 mod 4
  — safe (already placed);
- pairs inside g2: a = 2u, b = 2w ⇒ z = 2(2w − u) ∈ g2 — the halved odd
  problem; here the defect classes 2·(≡1 mod m/2) must go last, which the
  pure class calculus forbids (ψ-cycle obstruction, §2) but truncation
  permits: this is the **remaining gap**. The gap is real, not an artifact:
  it is exactly where the witnesses place their stragglers.
So the suffix lemma for general M reduces to a truncation-aware statement
about the 2·odd phase (equivalently: odd values at half scale with the
class ≡1 mod m/2 last). Left open here; the φ_r-tree gives the right order
skeleton and the finite verifications give M ≤ 128 (state size 170).

## 4. Part 4: releasing D

Naive append is obstructed in zone-preplaced semantics: pairs y ∈ B ∖ D,
z ∈ D with 2y − z ∈ Z (e.g. (x,y,z) = (16, 33, 50) at M = 32) force z
before y, so no arrangement of B ∖ D with the zone first admits *any*
suffix placement of D — independent of the earlier UNSAT. In state
semantics the results are:
- **Append after an arbitrary valid bulk arrangement: fails.** Random
  AP-free arrangements of V ∖ D admit a D-suffix in 0/5 trials at each of
  M = 16, 32, 64. Appendability is a property the bulk must be built for:
  every placed increasing pair completing into D must be anti-oriented
  (decreasing), cf. the φ_r tree.
- **Append after a suitably built bulk: always possible at tested scales**
  (the [bulk | D_Z | D_B] witnesses of §3, M = 32…128, and the ladder
  witnesses at comp 64/256/1024).
- **Release order is forced**: D_Z before D_B (reversed stacking UNSAT at
  M = 32, 64, 128, each in < 0.1 s — the refutation is shallow: a released
  small-scale defect value d_z sitting after block values turns all pairs
  (y, 2y − d_z) into forced ascents, a Lemma-R configuration).

## 5. Consequences for the program

- The defect law must be restated. Not: "B ∖ D is arrangeable under the
  zone" (false for M ≥ 32). But: "the complete state admits an AP-free
  arrangement with its top-block defect class as a suffix, defects stacked
  in scale order, and the next block (minus its own defect) available as a
  reservoir across the boundary." All three clauses are machine-verified
  at M = 32…128 / (X,d) ≤ (4,3); all three are necessary (each ablation is
  UNSAT).
- The per-block contiguous reduction of notes/02 cannot carry the
  YES-construction on its own: its (b)-hypothesis (zone fully placed
  before the block) is precisely what the construction must violate. The
  induction has to live at state level, with the boundary crossed by
  reservoirs — consistent with the "non-scale-monotone placements"
  conclusion of notes/05.
- The proof target for the extension lemma becomes concrete: an explicit
  phase-ordered arrangement rule (odds/vdC → ν₂ ≥ 2 → 2·odd → D_Z → D_B)
  whose only unproven component is the truncation-aware ordering of the
  2·odd phase with the class 2·(1 mod m/2) last. The φ_r-tree calculus
  (§2) supplies the order skeleton; the ψ-cycle obstruction shows where
  truncation must be invoked.
- Class-coherence, not residue identity, is the operative invariant at
  tested depths: any residue class defers. If deeper chains (d ≥ 4) or the
  rolling construction do force residue 2, that is additional structure
  still to be located; e51-style pins with residues 1 and 6 are SAT through
  d = 3, so nothing at these depths distinguishes them.
