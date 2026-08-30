# 80-pincer — THE SPARSE-CORNER PINCER: MINT-LOC executed, the
# lattice-affordability core, and the L-NOTAIL exterior kill

Session 2026-08-30 (continuation of the notes/79/80 adjudication).
Mandate: execute the champion route (S4 + MINT-LOC, notes/80 §3):
(1) resolve MINT-LOC exactly as pre-registered (machine at m = 32,
64, 128 on the S5 witnesses, then hand); (2) formalize the mod-4
lattice inhabitants' forced payments across the anchor tower,
combine with MINT-LOC's location content, and drive the pincer
(break-the-lattice arm vs preserve-the-lattice arm); (3) verify
every step on the actual witnesses; (4) state what closes and what
resists, honestly tagged.

Machine companion: experiments/e185_mintloc.py →
data/e185_mintloc.json / .log.  Witnesses = data/e179_s5_witness_*
(verified authentic, notes/80 §4.1).  This §0 is committed BEFORE
any e185 run (campaign rule).

## 0. Pre-flight: instrument spec + predictions (pre-registered)

**Desk facts going in (derived tonight, before any run; proofs in
§2–§3):**

- (D1) The γ-rigidity of the one-mint theory: banning all
  adjacent-seam pairs except one allowed inverted pair (u, w) at
  seam s forces the team order into rigid segments
  blk_s∖{u} < w < u < blk_{s+1}∖{w} (given nonempty presence in
  the seam blocks), whence a complete list of forced-monotone AP
  families K1–K5 (§2.1).  Consequence: a one-mint theory is
  satisfiable only if the team's ENTIRE cross-3-block AP family
  passes through the mint pair itself (x = u AND y = w for seam 0;
  y = u AND z = w for seam 1) and the K-auxiliary families are
  empty.
- (D2) Each adjacent-seam pair covers at most ONE cross-3-block AP
  ((x,y) determines z = 2y−x; (y,z) determines x = 2y−z), so any
  valid order carries ≥ |H_T(m)| inverted adjacent-seam pairs
  (this is exactly notes/54 P5's proven price floor
  Inv_T ≥ #H_T), and the displaced set (distinct low members)
  contains a vertex cover of the bipartite projection of H_T —
  by König, |D_T ∩ (m, 4m)| ≥ max-matching(H_T).
- (D3) e184's witness ownership sequences (read from the existing
  census, not new machine): h4096_D2F64 min-team = B, A, A, A, A,
  A, A for t = 5..11; h8192_D2F64 = B then A for t = 6..12;
  h4096_D2F12_lin4 = B at all t = 5..11.  I.e. ALL THREE witnesses
  have eventually-CONSTANT minority ownership above the boot
  block.
- (D4) DEGS77's opening observation (any ω-permutation of Z+
  contains a monotone 3-AP), plus restriction closure (AP-freeness
  passes to induced sub-permutations) plus affine invariance of
  3-APs, yields: **no 3-permutable team contains an infinite
  arithmetic progression** (L-NOTAIL, §3.1).  With (D3): the
  verbatim ω-extensions of all three S5 witnesses have a team
  containing the mod-4 class tail — dead.  The corner's
  ω-inhabitants must ALTERNATE class ownership between teams
  infinitely often; an ownership case-table (§3.2) then classifies
  which team is forced to carry the H-family per anchor.

**Instrument (e185_mintloc.py), parts:**

- partCENSUS: per witness × anchor m ∈ {16, 32, 64, 128, 256} ×
  team: the cross-3-block AP family H_T (x ∈ B0∩T, y ∈ B1∩T,
  z = 2y−x ∈ B2∩T): |H_T|, #distinct x, #distinct y, max-matching
  of the (x,y)-projection (König VC floor), class-pattern
  breakdown of (x mod 4, y mod 4, z mod 4); block ownership +
  minority class per block.  Plus a PURE-LATTICE control coloring
  (A = class 3 mod 4 on [1, 2048], constant ownership).
- partMINTLOC (the notes/80 §3.3 pre-registration, verbatim):
  anchors m = 32, 64, 128, all three witnesses, both teams:
  budget-0 control (double block order on the fixed coloring,
  per-team theory — teams decouple since the coloring is fixed),
  then enumeration of ALL candidate mints (u, w) at both seams:
  K1–K5 structural filter, exact rigid-γ SAT solve on any
  survivor.  Output: the SAT region, and for each SAT candidate
  the location of the displaced value u (distance to nearest other
  minority material of its block, residue mod 4).
- partNU (extension, labeled as such — NOT part of the notes/80
  pre-registration): minimum-payment scan: per-team theory with
  ALL adjacent-seam pairs allowed but counted, totalizer budget
  b ∈ {0, 1, 2, 4, 8, 12}; witnesses at m = 32 (both teams) and
  m = 64 where the team encoding stays ≤ ~250 values; control
  lattice at m = 16, 32 scanned to b = 24 to look for the SAT
  frontier against |H_T|.

**Predictions (committed before any run):**

- P-a. partCENSUS: at every anchor whose 3 blocks are pure-lattice
  with constant ownership (AAA/BBB vectors), BOTH teams have
  |H_T| = Θ(m²) (minority via in-class APs; majority via in-class
  and mixed-class APs) and matching = Θ(m).  At the F64 witnesses'
  m = 32 anchor (vector B,A,A): |H_A| = 0 — the e184 §4.3 anomaly
  is the (B,A,A) row of the case-table, A = the team owning the
  class in the two UPPER blocks; |H_B| > 0.  Lin4 boot blocks
  (t = 5, 6 mixed) may blur m = 32/64 rows for that witness only.
- P-b. partMINTLOC: the single-mint SAT region is EMPTY at every
  (witness, anchor, team) with |H_T| ≥ 2 (by D1: two H-triples
  cannot both pass through one mint pair; plus K-aux).  Every
  structurally-void team at m = 32/64/128 has empty region.  For
  h4096_F64/h8192_F64 team A at m = 32: |H_A| = 0 and predicted
  budget-0 SAT (the mint question is moot there — A pays 0 at
  that anchor; B pays and B's region is empty).  Consequence
  drawn if confirmed: MINT-LOC's literal location claim
  ("displaced value within distance ≤ 2 of minority material,
  breaking (iii) in O(1) octaves") is REFUTED-VACUOUS — the true
  resolution is STRONGER: no single mint (nor any o(presence)
  mint system, by D2 + census counts) pays any structurally-void
  anchor; and displaced values sit ON the minority lattice (gap
  exactly 4) or on majority values — order payment never breaks
  (iii), the corner does NOT self-destruct at the coloring level.
- P-c. partNU: UNSAT through b = 12 at every pure anchor for both
  teams (|H_T| ≫ 12 there); control lattice at m = 16: SAT
  frontier at b ≥ |H_minority| (exact value recorded as a
  measurement — the K-cascade may push it above |H|; genuinely
  uncertain within [|H|, |H| + O(m)]).
- P-d. No machine for L-NOTAIL (classical: DEGS77 + two lines).

Survival protocol: §1 machine harvest; §2 MINT-LOC resolution
(hand); §3 the lattice-affordability core + the pincer; §4 ledger.

---

## 1. Machine harvest (e185; census + mintloc landed, nu appended
## below)

### 1.1 partCENSUS — the H-family census [P-a CONFIRMED, and
### sharper]

Selected rows (full table data/e185_mintloc.json):

| coloring | m | H_A | match_A | H_B | match_B | pres A / B (B0) |
|---|---|---|---|---|---|---|
| pureL3 (control) | 32 | 80 | 8 | 552 | 24 | 8 / 24 |
| pureL3 | 64 | 320 | 16 | 2224 | 48 | 16 / 48 |
| pureL3 | 128 | 1280 | 32 | 8928 | 96 | 32 / 96 |
| pureL3 | 256 | 5120 | 64 | 35776 | 192 | 64 / 192 |
| h4096_F64 | 32 | **0** | 0 | 164 | 8 | 24 / 8 |
| h4096_F64 | 64 | 296 | 15 | 2201 | 48 | 16 / 48 |
| h4096_F64 | 128 | 1280 | 32 | 8928 | 96 | 32 / 96 |
| h4096_lin4 | 32 | 562 | 24 | 26 | 3 | 24 / 8 |
| h4096_lin4 | 128 | 8960 | 96 | 1280 | 32 | 96 / 32 |
| h8192_F64 | 32 | **0** | 0 | 164 | 8 | 24 / 8 |
| h8192_F64 | 128 | 1280 | 32 | 8960 | 96 | 32 / 96 |

Readings:

1. **The pure-lattice minority H-count is the closed form
   |H| = 5m²/64 EXACTLY** (80/320/1280/5120 at m = 32..256) — the
   desk formula of §3.3 lands to the integer.  The majority count
   is ≈ 7× that (mixed-class families).
2. **max-matching = |T ∩ B0| — the König displaced-value floor
   saturates at FULL anchor-block presence at every measured
   cell** (8 = |B∩B0| at m=32; 96 = |B∩B0| at m=128; both teams,
   all colorings, zero exceptions).  Sharper than predicted (only
   Θ(m) was pre-registered).
3. The ownership case-table is machine-exact: H_A = 0 precisely at
   the (B,A,A)-vector anchor m = 32 of both F64 witnesses (the
   e184 §4.3 anomaly, now DERIVED and postdicted); everywhere else
   both teams carry Θ(m²).
4. Above the boot zone the witnesses' counts converge to the pure
   lattice verbatim (35776 = pureL3's own m=256 majority count on
   h4096_F64) — the witnesses ARE the canonical family plus boot
   noise, as characterized in notes/80 §4.2.

### 1.2 partMINTLOC — the pre-registered enumeration [P-b
### CONFIRMED, and strengthened]

All three witnesses, m = 32/64/128, both teams, both seams, ALL
candidate mints (896–92160 per cell), fast filter cross-validated
against the exact γ-filter on 150-cand samples + all survivors
(**xval failures: 0 across all cells**):

- **The one-mint SAT region is EMPTY at every cell** (22/22,
  including the pure-lattice control at 32/64).
- Every team with H ≠ 0 is budget-0 UNSAT-STRUCTURAL with ZERO
  K-survivors: no candidate even reaches a solver.
- **The silent-row teams (H = 0: team A at m = 32, both F64
  witnesses) are budget-0 UNSAT at the SOLVER level too** — the
  within-block + 2-block AP system kills them without any
  H-triple; and their K-survivors (29 resp. 144 candidates) are
  ALL solver-UNSAT.  Prediction P-b had budget-0 SAT here — wrong
  in the direction that STRENGTHENS the demand side: at every
  witness anchor tested, both teams pay ≥ 1, and no single mint
  is ever sufficient (pay ≥ 2 even in the silent rows).

MINT-LOC as pre-registered is therefore resolved by the machine in
the STRONG (empty-region) form; the hand argument is §2.

### 1.3 partNU — the budget frontier [P-c CONFIRMED, and the
### silent rows pay too]

Minimum-payment scans (adjacent-seam inversion indicators,
totalizer; per-team theory on the fixed coloring):

- **Witnesses, m = 32 (all 3, both teams) and m = 64 (the ≤ 260
  side): UNSAT through budget 12, every cell** — including
  h4096_F64/h8192_F64 team A at m = 32, the H = 0 silent rows
  (n = 72): their payment is > 12 from the within-block +
  2-block AP system alone (A's blocks there are 3/4-dense
  near-intervals — Varnavides-species demand, no H needed).
- **Pure lattice control, m = 16, minority: UNSAT through
  b = 24 > |H| = 20** (n = 28, instant solves): the true frontier
  ν EXCEEDS the H-cover floor — the K-cascade families (§2.1)
  charge above |H|.  Majority at m = 16 and both teams at m = 32:
  UNSAT through 24.

Net: on the corner's canonical inhabitants, per-anchor per-team
payment is > 12 at every cell measured, > 24 where scanned, with
the proven floor |H_T| = Θ(m²) (P5) wherever H ≠ 0 — against
T-TEL″'s previous unconditional floor of ONE pair per two octaves.

**Encoder positive control + exact frontiers (post-scan
addendum):** the same encoder's SAT side is reachable — pure
lattice minority: **ν(8) = 9 (|H| = 5), ν(12) = 31 (|H| = 11),
ν(16) = 58 (|H| = 20)**, each pinned by consecutive
UNSAT/SAT rows in one totalizer.  ν ≈ 2.8–2.9 × |H| ≈ 0.23 m²:
quadratic per-anchor payment measured EXACTLY at three scales,
with the hand floor 5m²/64 below it and the cascade factor on
top.

---

## 2. MINT-LOC resolved (the hand argument)

Throughout: one team T, window (m, 8m], blocks B0, B1, B2, block
order = all adjacent-seam pairs (a, b) ∈ (B_i × B_{i+1}) ∩ T²
placed pos(a) < pos(b); H_T = the cross-3-block AP family
{(x, y, 2y−x) ∈ (B0×B1×B2) ∩ T³}.  Teams decouple (the coloring is
fixed), so all statements are per-team; joint verdicts are
conjunctions.

### 2.1 Lemma γ-RIGID + the K-catalogue [PROVED; machine-exact]

**Lemma γ-RIGID.**  In the one-mint theory (block order minus the
single pair (u, w) at seam s, the mint forced inverted), if
T ∩ B_{s+1} ∖ {w} ≠ ∅ the team order decomposes into rigid
segments

    seam 0:  B0∖{u}  <  w  <  u  <  B1∖{w}  <  B2
    seam 1:  B0  <  B1∖{u}  <  w  <  u  <  B2∖{w}

(only within-segment order is free).  *Proof.*  Every non-mint
seam pair is oriented by its ban; w after B_s∖{u} (their pairs
with w are banned), w before u (the mint), u before
B_{s+1}∖{w} (banned pairs), the rest by transitivity through any
value of the middle block.  ∎

**K-catalogue.**  Writing γ for the segment index, an in-team AP
(x, y, z) with strictly increasing γ is forced monotone-increasing
— fatal.  Enumerating the γ-patterns (§0 D1, verified against the
exact filter with 0 mismatches on every cell):

- seam 0 fatal families: any H-triple with (x, y) ≠ (u, w); APs
  (x, w, z) x ∈ B0∖{u}; (x, u, z) with z ≠ w; (w, y, z) into
  B1×B2; (u, y, z) with y ≠ w.
- seam 1 fatal families: any H-triple with (y, z) ≠ (u, w); APs
  (x, y, w) y ≠ u; (x, y, u) y ∈ B1∖{u}; (x, w, z); (x, u, z)
  z ≠ w; (y, w, z) y ≠ u; (y, u, z) z ≠ w.

**Lemma MINT-1 (one-mint characterization).**  The one-mint theory
at (u, w) is satisfiable only if EVERY H-triple passes through the
mint pair itself (x = u ∧ y = w at seam 0; y = u ∧ z = w at
seam 1) — hence only if |H_T| ≤ 1 (the mint pair determines its
third point) — AND the listed auxiliary families are empty, AND
the residual within-block system is satisfiable.  *Proof.*  The
K-catalogue plus γ-RIGID.  ∎

Machine realization (§1.2): on the witnesses |H_T| ≥ 26 at every
carrier cell — region empty by the first clause; at the two
|H| = 0 cells the auxiliary + within-block layers finish it
(solver).  22/22 empty.

### 2.2 The floors that survive any budget [PROVED]

**Lemma H-COVER.**  In ANY valid order of T (no block-order
hypothesis): each H-triple (x, y, z) forces pos(y) < pos(x) or
pos(z) < pos(y) (P5, notes/54 — else monotone), i.e. an inverted
adjacent-seam pair; and distinct H-triples force DISTINCT pairs
((x, y) determines z, (y, z) determines x).  Hence
Inv_T(m) ≥ |H_T(m)|.  [This is notes/47 §3 / notes/54 P5's proven
price floor, now with |H_T| computed on the corner: Θ(m²).]

**Lemma D-FLOOR (the König displaced floor).**  Let G_T(m) be the
bipartite graph on (T∩B0) ⊔ (T∩B1) with an edge (x, y) for each
H-triple.  The displaced set D_T(m) (distinct low members of
inverted adjacent-seam pairs) contains a vertex cover of G_T(m),
so |D_T(m) ∩ (m, 4m)| ≥ max-matching(G_T(m)).  *Proof.*  Each
H-triple puts x ∈ D (left seam) or y ∈ D (right seam); König.  ∎

**Lemma D-SAT (matching saturates presence, pure lattice).**  For
the class-c minority on pure-lattice blocks, N(x) = {y ≡ c :
y > 2m + x/2} has |N(x)| ≥ m/4 = |T ∩ B0| for every x, so Hall
gives a matching saturating T ∩ B0: **|D_T(m) ∩ (m, 4m)| ≥
|T ∩ B0(m)| — the anchor block's ENTIRE presence is displaced.**
Machine (§1.1): max-matching = |T ∩ B0| exactly at every measured
cell, BOTH teams, witnesses included — the majority-side
saturation is machine-fact (same staircase shape; not needed by
hand below).

### 2.3 The resolution

**MINT-LOC [RESOLVED — literal form REFUTED-VACUOUS, strong form
PROVED].**  The pre-registered literal statement ("the displaced
value is forced within distance ≤ 2 of other minority material,
so paying breaks axis (iii) within O(1) octaves") is the WRONG
mechanism: order payment never recolors, and on the corner's
canonical family the displaced values sit ON the minority lattice
(mutual distance exactly 4) or on majority values — axis (iii) is
never broken by paying.  What is TRUE is stronger and carries the
same arrow:

> **T-MINT-LOC (location/mass form).**  For any blockwise mod-4
> lattice coloring, at every anchor m above boot and any valid
> pair of orders: the one-mint theory is void for both teams
> (Lemma MINT-1 + |H| ≥ 2 resp. the measured aux layer), and any
> valid order pays Inv_T(m) ≥ |H_T(m)| = Θ(m²) for every
> H-carrier team, with displaced values confined to (m, 4m) in
> at least full-anchor-block-presence numbers
> (|D_T ∩ (m, 4m)| ≥ |T ∩ B0(m)|, Lemmas D-FLOOR + D-SAT).

What it pins: not a 2-neighborhood of minority material but the
FULL presence mass of the paying block, lattice-structured,
window-confined — the input the pincer (§3) needs.

---

## 3. The lattice-affordability core and the pincer

### 3.1 Lemma L-NOTAIL [PROVED — classical import, two lines]

**Lemma L-NOTAIL.**  No 3-permutable team contains an infinite
arithmetic progression.

*Proof.*  Suppose T ⊇ L = {a + id : i ≥ 0}.  The restriction of
π_T to L is an ω-permutation of L; the affine bijection
i ↦ a + id identifies 3-APs of ℤ⁺ with 3-APs of L in both
directions.  By DEGS77's opening observation (any ω-permutation of
ℤ⁺ contains an INCREASING 3-AP: first term a₁, least k with
a_k > a₁, then 2a_k − a₁ is right of both), π_T|_L contains a
monotone in-team 3-AP; monotone-AP-freeness is closed under
restriction.  ∎

**Corollary C-LATDEAD (the preserve-the-lattice arm CLOSES).**  A
blockwise mod-4 lattice coloring whose class-ownership sequence
τ(t) is eventually constant has a team containing the class tail
{v ≡ c (4), v > 2^{t₀}} — an infinite AP.  It is not a valid
pair.  **In particular the verbatim ω-extensions of ALL THREE S5
witnesses (ownership constant above t = 6, §0 D3) are dead** —
the notes/80 §3.2(a) "easy part" of the YES-bill produces only
dead colorings from the realized witnesses.  The corner's
ω-YES-space shrinks to lattices whose ownership ALTERNATES
between the teams infinitely often.  (More generally: any
gap-≥3-corner coloring whose minority material contains an
infinite AP owned by one team from some point on is dead — the
lattice does not need to be mod-4 for L-NOTAIL to bite.)

### 3.2 The ownership case-table [hand; machine-exact]

For pure blockwise lattices, at the anchor on blocks
(t, t+1, t+2) with ownership vector (τ_t, τ_{t+1}, τ_{t+2}), the
H-carrier status is forced by residue arithmetic (x + z = 2y,
classes mod 4; the minority side of a block is exactly class c,
the majority side exactly the other three classes):

| vector | H-silent team | carrier channels |
|---|---|---|
| (X,X,X) | none | X: in-class (c,c,c); Y: (b,b,b) b ≠ c and mixed |
| (X,X,Y) | X (z ≡ c lands in Y) | Y: (c+2, c±1, c) |
| (Y,X,X) | X (x ≡ c lands in Y) | Y: (c, c±1, c+2) — TWO channels |
| (X,Y,X) | none | X: (c, c+2, c) via i+k odd; Y: (b, c, 2c−b) |

Every anchor has ≥ 1 carrier; at most one team is H-silent, and
only at run boundaries (patterns XXY / YXX).  Each carrier channel
is a fixed-residue staircase, so |H_carrier| ≥ 5m²/64 − O(m)
(§1.1's closed form; the two-channel row measures 164 ≈ 2×80 at
m = 32 — machine-exact).  Machine: §1.1 confirms every row,
including H_A = 0 exactly at the F64 witnesses' (B,A,A) anchor.
NOTE (measured, §1.2/§1.3): H-silence is NOT payment-silence — the
silent team's 3/4-dense near-interval blocks carry Varnavides-
species demand: budget-0 UNSAT and ν > 12 at both silent cells.
The hand floor below uses carriers only; the silent-row payments
are machine-fact on the witnesses.

### 3.3 Theorem AFFORD-DEMAND [PROVED; the demand half of
### L-AFFORD on the lattice corner, unconditional]

**Theorem AFFORD-DEMAND.**  Let (A, B) be a valid pair whose
coloring is a blockwise mod-4 lattice above scale 2^{t₀}
(ownership sequence τ, any).  Then, with no further hypotheses
(no N6a, no budget, no machine):

1. τ alternates infinitely (L-NOTAIL).
2. At every anchor m = 2^t, t > t₀: for every H-carrier team T
   (≥ 1 exists, §3.2):  Inv_T(m) ≥ |H_T(m)| ≥ 5m²/64 − O(m)
   (Lemma H-COVER = P5 + the census closed form).
3. |D_T(m) ∩ (m, 4m)| ≥ matching(G_T(m)) ≥ m/4 − O(1)
   (Lemmas D-FLOOR + D-SAT applied to a carrier channel; measured
   saturation is the FULL block presence |T ∩ B0|).
4. Along either 4-adic subchain the windows (m_j, 4m_j) are
   disjoint, so the displaced sets of item 3 are disjoint sets of
   values: for every horizon N, at least (1/3)·max m_j ≥ N/12 −
   O(log N) DISTINCT values below 4N are displaced (each the low
   member of an inverted adjacent-seam pair, P3).

Reading: T-TEL″'s unconditional ledger floor on general Case-2
pairs was one displaced value per two octaves — Θ(log N)
cumulative.  On the corner's canonical family the floor is a
POSITIVE FRACTION of all values: Θ(N) cumulative, Θ(m²) pair
demand per anchor, measured exactly (ν(8), ν(12), ν(16) = 9, 31,
58 ≈ 0.23 m² on the pure minority — 2.9× the hand floor).

### 3.4 The pincer, assembled — and where it stops

- **Arm 1 (preserve the lattice as a team-object): CLOSED.**
  Eventually-constant ownership dies by L-NOTAIL — including
  every realized S5 witness's canonical extension.  The exterior
  machinery required was classical (DEGS77), not the campaign's.
- **Arm 2 (alternate): DEMAND QUANTIFIED, SUPPLY STILL OPEN.**
  Alternating lattices must pay Θ(m²) inversions per anchor with
  presence-scale displaced sets forever (AFFORD-DEMAND) — and at
  switch-dense regimes BOTH teams carry (§3.2 row 4), while
  switch-sparse regimes approach the L-NOTAIL wall (long constant
  runs make the class-material of a run an ever-longer finite AP
  owned by one team — no finite kill, but the runs' interiors
  admit no donation escape in the L-CASCADE outflow trichotomy:
  within a run, u ≡ c displaced has its Top-band pairs
  (a, b) = (2b−u, b) in-class, hence in-team — outflows 2/3
  (donate a or b) are unavailable; only comply (cascade
  inversions 1–5 octaves down) or order-dodge remain).
  The strictly-decreasing-slack recursion the pincer aimed at
  does NOT close from these floors alone: per 4-adic window,
  demand ≥ (window presence)/1 but supply of colored values in
  the same window is 3× that; no counting contradiction — this
  is NG1–NG4 territory, as pre-registered in notes/79.

**What remains, exactly (the sharpened terminal gap):**

> **GAP-AFFORD″-ALT.**  No blockwise mod-4 lattice coloring with
> infinitely-alternating ownership admits a pair of ω-orders
> paying Θ(m²) adjacent-seam inversions at every anchor subject
> to: L-COMP (forced descents never compose along an AP),
> L-DOUBLE-DUTY (consecutive-boundary value-disjointness below
> presence prices), the d-zigzag law (along every AP line of a
> team, positions strictly alternate), and the L-CASCADE outflow
> trichotomy with in-run donation channels VOID (above).  Plus
> its sibling for non-lattice gap-≥3 corners (unchanged: the
> SPARSE-CORE mixed catalogue + arm B).

### 3.5 Pre-registration: S5-ALT (the alternating family's finite
### theory — run next, predictions first)

The alternating family is now the ENTIRE lattice-corner ω-YES-
space, and NO witness realizes it (all three are constant-
ownership).  Experiment (e185 partS5ALT = e179 s5dodger + forced
designation alternation mA_t ≠ mA_{t+1} for t ≥ 6): hor = 4096,
(i)-censor D = 2 with F = 12 and F = 64 (u₀ = 32/64), (ii) lin4,
(iii) sparse, split floor as in e179.  Predictions (committed
before the run): genuinely uncertain; lean SAT ≈ 60 % at F = 12
(the constraints are local; the solver was simply never asked to
alternate), less at F = 64 (alternation moves class material
across teams every block — reflector traffic between teams may
create censored chains).  If SAT: first alternating inhabitant;
audit its per-anchor H (both teams should carry at switch
anchors — its payment obligation is then WORSE than the constant
witnesses').  If UNSAT at both censors: the corner's finite
theory REJECTS alternation under orbit censors while ω demands
it (L-NOTAIL) — the pincer closes at the (i)-proxy level, with
only the proxy-vs-true-(i) caveat (T-SHARP) between the corner
and emptiness.
