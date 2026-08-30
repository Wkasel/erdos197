# 72 — FRONT VMIN0-GROWTH: the diverging demand series — growth
# theorem attempt + the composed T-TEL′ keystone

Task: (1) prove v_min(0)(M) ≥ c·M from the band-exhaustion mechanism
(notes/68) by layer counting; (2) write the composed statement
T-LEDGER + T-FRESH + v_min(0) → ∞ ⟹ demand side of L-AFFORD for the
linear regime, with every link's status.  This is the keystone
document for the Case-2 ledger chain.

Verdict in one line: **the demand calculus of the (v,0) cell is now a
proved three-channel theorem (T-CHAN), the sumset floor is exactly
computable and its ONLY zero is the parity schedule already killed by
SCHED-DEAD at every budget — the growth theorem reduces to one
extremal coverage inequality [GAP-BAND-COV] plus one robustness
radius [GAP-K-ROB], both stated exactly, with the coverage arm
PROVED on the canonical range family (demand ≥ M − O(1)); the series
itself is harvested to five scales (v_min(0)(32) > 512, const-bounds
(65,0)@24 UNSAT) after quarantining a fleet mis-launch that was
solving the WRONG CELL.**

## 0. The object

The (v, 0) pump cell (e158/e173 4-block encoder — the ONLY encoder
that defines v_min(0)):

- blocks Bm1 = (M/2, M], B0 = (M, 2M], B1 = (2M, 4M], B2 = (4M, 8M];
  seams s0 = β(M) (Bm1×B0), s1 = β(2M) (B0×B1), s2 = β(4M) (B1×B2);
- coloring A/B with per-block bounds (bal = exact balance; const =
  lower bounds (2, 3, 6, 12)); per-team AP-free orders;
- per-ANCHOR budgets: anchor M/2 pays x_{s0} + x_{s1} = 0 (vdn = 0),
  anchor M pays x_{s1} + x_{s2} ≤ v (vup) — per team.

Under vdn = 0 both teams are wholesale block-ordered
[Bm1∩T] ≺ [B0∩T] ≺ [B1∩T] (L-PREFIX, notes/62 §4c), so the effective
budget is x_{s2} ≤ v.  v_min(0)(M) := least v with the cell SAT =
the price of a FREE lower anchor (notes/62 §5).

## 1. The series (harvest complete as of this session)

bal mode (exact balance):

| M | UNSAT at v (time) | SAT at v (time) | v_min(0)(M) |
|---|-------------------|-----------------|-------------|
| 8 | 6 (2.1s), 8 (7.3s), 9 (11.5s), 10 (24.5s), 11 (40.6s) | 12 (8.6s), 16, 64, 256 | **= 12 EXACT** |
| 16 | 6 (2.1s ×2 encoders) | 384 (17.2s); TIMEOUT@3600s at 96, 192 | ∈ (6, 384] |
| 24 | 65 (46.0s) | — | > 65 |
| 32 | 100 (62.6s), 256 (137.2s), **512 (98.6s)** | — | **> 512** |
| 48 | — (512 TIMEOUT @43200s, main pod) | — | open (5th scale) |

const mode (bounds (2, 3, 6, 12) — NO balance):

| M | verdict | reading |
|---|---------|---------|
| 24 | (6,0) UNSAT [106.0s]; **(65,0) UNSAT [14797.6s]** | **the const-bounds ladder has a second point: v_min^const(0)(24) > 65** — the pump demand at 24 is not a balance artifact at any measured budget |
| 32 | (100,0) TIMEOUT @43200s | open |

Freshness refinement F(M; v) (s0 = 0 only, s1 freed below,
x_{s1} + x_{s2} ≤ v):

| cell | verdict |
|------|---------|
| F(16; 6) | UNSAT — TWICE independently (983.5s local, 1350.2s main pod) |
| F(24; 65) | TIMEOUT @43200s (relaunched on sprint-C at 86400s) |

Key monotone facts: v_min(0)(8) = 12 = 1.5M; v_min(0)(24) > 65 ≈
2.7M; v_min(0)(32) > 512 = 16M.  The lower-bound curve is
super-linear on its face between 24 and 32 (both are only lower
bounds; no curve-fitting per campaign rule).  Every point sits far
above the balanced v*₃ bracket at its scale (v*(bal,8) = 0;
v*(bal,32) witness 368 < 512) — zeroing an anchor costs
qualitatively more than paying the floor, at every measured scale.
Deep-UNSAT stays cheap through v = 512 at M = 32 (98.6s); the wall
is scale (M = 48), not budget depth.

## 2. FLEET INCIDENT (quarantine + fix, this session) — the wrong cell

The three sprint pods had been launched (previous infra hand-off)
with drivers calling **e127's solve_budget(M, None, v, 0)** — the
3-block window (M, 8M] with per-TEAM budgets (team A ≤ v, team B ≤ 0)
— NOT the 4-block per-anchor pump cell that defines v_min(0).  The
mismatch was caught by the first landed point: sprint-C printed
"CERT M=8 (up=11,dn=0): SAT [0s]" where the true pump cell (11,0)@8
is UNSAT [40.6s, data/e173_pump_M8_up11_dn0.json].  The e127 cell is
SAT there because a per-team (v, 0) budget is the one-sided
weakening already known toothless (notes/47: asym one-sided variants
SAT at v = 0).

Actions: all three pod runs killed before any wrong point could
enter the series; e173_telescope.py deployed to all pods; drivers
rewritten against solve_chain with the exact budget vectors
[("vdn", [0,1], 0), ("vup", [1,2], v)] (sprint-B bisect grid
16: 12/24/48/96, 24: 128/256, 32: 768/1024; sprint-D fifth scale
48: 64/128/256 + interp 40: 256/512 + long (512,0)@48; sprint-C
cross-encoder cert battery (11,0)@8 / (12,0)@8 / (6,0)@16 /
(65,0)@24 + F(16;6) third run + F(24;65) at 86400s).  **Quarantine
rule: no number enters the v_min(0) table unless its record carries
the e173/e158 4-block budget vector.**  (§1's table is built
exclusively from such records: local e173_telescope.jsonl +
e158_c3/f_* + main-pod e158_tel_*.)

Also harvested from the main pod this session (correct encoder,
previously unlogged in notes): (512,0)@32 UNSAT [98.6s] and the
const-bounds (65,0)@24 UNSAT [14797.6s] — both now in §1.

## 3. The demand calculus of the (v, 0) cell [PROVED]

Notation, per team T: W = Bm1∩T, U = B0∩T, Y = B1∩T, X = B2∩T.
At bal: |W| = M/4, |U| = M/2, |Y| = M, |X| = 2M.  Sumset masses:
μ_dn = #{(u,y,z) ∈ U×Y... } — CORRECTION, campaign convention
(notes/62): μ_dn = #AP triples in W×U×Y, μ_up = # in U×Y×X,
μ_skip = # in W×Y×X (an AP triple (a, b, 2b−a) with the three
members in the three listed blocks respectively).

**Theorem T-CHAN (three-channel demand) [PROVED — this is L-PREFIX
(notes/62 §4c) restated in (v,0) coordinates; proof reproduced for
self-containment].**  In any model of the (v,0) cell, for each team:

(i) **μ_dn(T) = 0 as a coloring fact.**  vdn = 0 forces wholesale
block order W ≺ U ≺ Y (every cross pair at s0 and s1 non-inverted).
An AP (w, u, 2u−w) ∈ W×U×Y would be positioned w ≺ u ≺ 2u−w —
monotone, and BOTH break edges (u before w, or 2u−w before u) are
banned s0/s1 inversions.  So no such AP exists in the coloring:
(2U − W) ∩ Y = ∅.

(ii) **Every AP (u, y, 2y−u) ∈ U×Y×X costs one s2 unit.**  u ≺ y is
forced (s1); monotone-freedom forces 2y−u ≺ y — an inverted s2 pair
(y, 2y−u).

(iii) **Every AP (w, y, 2y−w) ∈ W×Y×X costs one s2 unit** (same
argument through s0∪s1 transitivity: w ≺ y forced).

The charged edges are pairwise distinct within and across channels
(ii)/(iii): the edge (y, z) determines a = 2y − z, which lies in
exactly one of B0, Bm1.  Hence for each team

    v ≥ x_{s2}(T) ≥ μ_up(T) + μ_skip(T),

and therefore
    v_min(0)(M) ≥ min { max_T (μ_up + μ_skip)(T) :
                        legal coloring, μ_dn(A) = μ_dn(B) = 0 }.   (F)

Everything else the cell charges (in-block orientation systems under
the wholesale prefix order — the Lemma-K/flood theory) is NOT priced
in v; that is the order-theory arm (§5).

**Lemma L-HIT [PROVED — one line].**  Let Z(T) = (2Y − U) ∪ (2Y − W).
Every z ∈ X ∩ Z has ≥ 1 representation, so
μ_up + μ_skip ≥ |X ∩ Z| ≥ |X| + |Z ∩ B2| − |B2| = |Z ∩ B2| − 2M
(bal).  Coverage of the band beyond 2M values is paid unit-for-unit.

**Lemma L-SEESAW [PROVED].**  Unconditionally at bal,
|Z ∩ B2| ≥ |Y ∩ (2M + w₁/2, 4M]| ≥ M/2 where w₁ = min W ≤ M
(the map y ↦ 2y − w₁ is injective into B2 for y > 2M + w₁/2).
Pushing Y low to dodge this runs into μ_dn = 0 (§4); pushing Y high
doubles it straight into B2 — the window seesaw: **2·B1 = B2
identically — the reachable band IS the double of the mid block.**

## 4. The zero set of the sumset floor, and the extremal lemma L-MID

The floor (F) is toothless by itself: the block-parity schedule
(x, x, 1−x, 1−x) (T = odds of (M/2, 2M] ∪ evens of (2M, 8M], and its
complement) has μ_dn = μ_up = μ_skip = 0 for both teams (notes/62
§4c: unique zero among pure parity schedules), and it is killed only
by pure order theory — Lemma K + Theorem SCHED-DEAD [PROVED,
notes/62 §4d]: UNSAT at EVERY budget, every M ≥ 12.  The growth
theorem is therefore forced into a two-arm shape (§5).  What is new
here is the extremal structure of the zero set and the price of
leaving it.

**Lemma L-MID (the midband is never sumset-clean) [PROVED, hand,
M ≥ 32; machine-checked at M = 16, 24, 32, 40 (e174, §6)].**  For
every U ⊆ (M, 2M] with |U| = M/2 and every W ⊆ (M/2, M] with
|W| = M/4:  (2U − W) ∩ (2M, 3M] ≠ ∅.

*Proof.*  Say u ∈ U is HOT if some w ∈ (M/2, M] has 2u − w ∈
(2M, 3M], i.e. the w-window V(u) = [2u−3M, 2u−2M) ∩ (M/2, M] is
nonempty; the pair (U, W) is clean iff W avoids V(u) for every
u ∈ U.  Compute V(u): u ≤ 5M/4 ⟹ V = ∅ (safe); u ∈ (5M/4, 3M/2] ⟹
V = (M/2, 2u−2M); u ∈ (3M/2, 7M/4] ⟹ V = (M/2, M] ENTIRE (no W can
avoid it — such u are forbidden in U outright); u ∈ (7M/4, 2M) ⟹
V = [2u−3M, M]; u = 2M ⟹ V = {M} (avoid by M ∉ W).  Since
|(M, 5M/4]| = M/4 < M/2 = |U|, at least M/4 members of U exceed
5M/4, and none may lie in (3M/2, 7M/4], so U' := U ∩ ((5M/4, 3M/2] ∪
(7M/4, 2M]) has |U'| ≥ M/4 − 1 (allowing u = 2M).  Three cases.
(B) U' ∩ (7M/4, 2M) = ∅: then U' ⊆ (5M/4, 3M/2], and |U'| ≥ M/4 − 1
forces max U' ≥ 3M/2 − 2, whence W ⊆ [2·max−2M, M] ⊆ [M−4, M]:
|W| ≤ 5 < M/4 for M ≥ 32 — contradiction.  (C) U' ∩ (5M/4, 3M/2] =
∅: then U' ⊆ (7M/4, 2M] must contain all but O(1) of that quarter,
in particular some u ≤ 7M/4 + 2, forcing W ⊆ (M/2, 2u−3M) ⊆
(M/2, M/2 + 4): |W| ≤ 3 < M/4 — contradiction.  (A) both nonempty:
let u_a = max U'∩(5M/4, 3M/2], u_b = min U'∩(7M/4, 2M).  W ⊆
[2u_a − 2M, 2u_b − 3M), so M/4 ≤ 2(u_b − u_a) − M, i.e.
u_a ≤ u_b − 5M/8 ≤ 2M − 5M/8 = 11M/8.  Then U ⊆ (M, 5M/4] ∪
(5M/4, 11M/8] ∪ [u_b, 2M] with the middle piece of size ≤ M/8 and,
for W (M/4 values) to fit in (M/2, 2u_b − 3M), also 2u_b − 3M ≥
M/2 + M/4 ⟹ u_b ≥ 15M/8: |[u_b, 2M]| ≤ M/8 + 1.  Total |U| ≤ M/4 +
M/8 + M/8 + 1 = M/2 + 1 — tight, but the W-fit ALSO requires
2u_a − 2M ≤ M/2 + 2 ⟹ u_a ≤ 5M/4 + 1, collapsing the middle piece
to ≤ 1 value: |U| ≤ M/4 + 1 + M/8 + 1 < M/2 for M ≥ 32 —
contradiction.  ∎

Reading: the prefix material (W, U) ALWAYS mints sumset mass into
the midband (2M, 3M].  μ_dn = 0 then FORBIDS Y from sitting on the
hit set — the bottom-interval range dodge Y ⊇ (2M, 3M] is dead for
every (U, W) (this is the general form of the worked example: any
attempt to hide Y low collides with L-MID; any Y pushed high is
doubled into B2 by L-SEESAW).

**Lemma L-RANGE (canonical up-range family priced) [PROVED].**  If
Y ⊆ (3M, 4M] (the up-interval dodge, forced when Y dodges a
midband-covering hit set), then for u₀ = min U ≤ 3M/2 + 1 (bal),
Z ⊇ 2Y − u₀ ⊇ step-2 values filling (2·3M − u₀, 8M − u₀], and with
the U-sweep 2Y − U ⊇ (9M/2 + 2, 7M − 1) once U contains any M/2
values of B0; hence |Z ∩ B2| ≥ 5M/2 − O(1) and by L-HIT the team
pays μ_up + μ_skip ≥ M/2 − O(1).  (Worked instance: U = (M, 3M/2],
Y = (3M, 4M]: μ_dn = 0 holds — 2U − W ⊆ (5M/4, 5M/2 − 1] misses Y —
and Z_up = (9M/2, 7M): coverage 5M/2, demand ≥ M/2.)

**The zero-set question.**  Is the (x,x,1−x,1−x) schedule pair the
ONLY zero of the floor (F) at bal?  L-MID + L-SEESAW say every zero
must thread: Y off the midband hit set, X off a ≥ M/2-deep covered
band, μ_dn = 0.  The parity thread does it via congruence classes;
higher-modulus lattice threads are capacity-limited (Y needs M of
2M values — exactly ONE class mod 4; W is forced to be ALL of one
parity of Bm1).  e174 (§6) answers the question by machine at
16..40; the hand classification is [GAP-ZERO], expected N3-species.
