# 72 — FRONT VMIN0-GROWTH: the diverging demand series — growth
# theorem attempt + the composed T-TEL′ keystone

Task: (1) prove v_min(0)(M) ≥ c·M from the band-exhaustion mechanism
(notes/68) by layer counting; (2) write the composed statement
T-LEDGER + T-FRESH + v_min(0) → ∞ ⟹ demand side of L-AFFORD for the
linear regime, with every link's status.  This is the keystone
document for the Case-2 ledger chain.

Verdict in one line (WRITTEN MID-SESSION, then overtaken and merged
— see §5): **the demand calculus of the (v,0) cell is a proved
three-channel theorem (T-CHAN) with new proved extremal lemmas
(L-MID, L-SEESAW, L-RANGE — direct progress on notes/71's
[GAP-FHALF]); the sumset floor's zero set is STRICTLY BIGGER than
the parity schedules (e174: composite parity-core + range-top zeros
at every scale, all LOW-PURE, hence all Lemma-K-dead) — and the
growth question itself was resolved during this session by the
convergence of three fronts: notes/75's Theorem J-DOWN collapses
the pump into the anchor-m coupled core, giving v_min(0)(M) = ∞ for
every M ≥ 32 (machine at 32; modulo GAP-N6a beyond), notes/71's
two-case schema gives v_min(0)(M) ≥ M/2 for all M ≥ 12 modulo the
orders-free counting lemma [GAP-FHALF], and this front's harvest
pins the finite regime to exactly M ∈ {8, 16, 24} (12 exact;
(6,384]; (65,1440]).  [GAP-VMIN0-growth] is DISCHARGED.  The
composed keystone statement (T-LEDGER + T-FRESH + collapse ⟹
demand side of L-AFFORD, linear regime) is §6, every link
statused.  Fleet incident: the pods were mis-launched on the wrong
cell — caught, quarantined, redeployed (§2).**

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
| 16 | 6 (2.1s ×2 encoders); **12 (12.3s), 24 (36.6s), 48 (706.2s)** [sprint-B, correct encoder, landed in-session] | 384 (17.2s); TIMEOUT@3600s at 96, 192 | ∈ **(48, 384]** |
| 24 | 65 (46.0s) | — | > 65 |
| 32 | 100 (62.6s), 256 (137.2s), **512 (98.6s)** | — | **> 512** |
| 40 | **(none,0) UNSAT [12.6s]** [sprint-D wave 2, in-session] | — | **= ∞ MACHINE — and m = 20 is a FRESH scale for the coupled-core family itself** (e120 tested 16/24/32) |
| 48 | **64 (67.7s), 128 (164.4s), 256 (246.6s), then (none,0) UNSAT [22.0s]** [sprint-D, in-session]; 512 TIMEOUT @43200s (main pod) | — | **= ∞ MACHINE** (the (none,0) cell settles what the deep-budget cells could only suggest) |

const mode (bounds (2, 3, 6, 12) — NO balance):

| M | verdict | reading |
|---|---------|---------|
| 24 | (6,0) UNSAT [106.0s]; **(65,0) UNSAT [14797.6s]** | **the const-bounds ladder has a second point: v_min^const(0)(24) > 65** — the pump demand at 24 is not a balance artifact at any measured budget |
| 32 | (100,0) TIMEOUT @43200s | open |

Freshness refinement F(M; v) (s0 = 0 only, s1 freed below,
x_{s1} + x_{s2} ≤ v):

| cell | verdict |
|------|---------|
| F(16; 6) | UNSAT — THREE TIMES independently (983.5s local, 1350.2s main pod, 802.0s sprint-C in-session) |
| F(24; 65) | TIMEOUT @43200s (relaunched on sprint-C at 86400s) |

Key facts: v_min(0)(8) = 12 = 1.5M; v_min(0)(24) > 65 ≈ 2.7M;
v_min(0)(32) > 512 = 16M.  Every point sits far above the balanced
v*₃ bracket at its scale (v*(bal,8) = 0; v*(bal,32) witness
368 < 512) — zeroing an anchor costs qualitatively more than paying
the floor, at every measured scale.  Deep-UNSAT stays cheap through
v = 512 at M = 32 (98.6s); the wall is scale (M = 48), not budget
depth.  READING CORRECTED BY THE MERGE (§5): the 32-row is not a
large finite lower bound but the shadow of v_min(0)(32) = ∞
(notes/75 J-DOWN: (none,0)@32 UNSAT [7.4s] — the anchor-16 coupled
core fires under vdn = 0 regardless of vup); the finite regime is
exactly M ∈ {8, 16, 24} with v_min(0)(24) ∈ (65, 1440] (notes/75
C2@24 (none,0) SAT).  The 48-timeout row is moot (predicted UNSAT
at every v by J-DOWN + the bal core at 24).

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
At bal: |W| = M/4, |U| = M/2, |Y| = M, |X| = 2M.  Sumset masses
(campaign convention, notes/62): μ_dn = #AP triples in W×U×Y,
μ_up = # in U×Y×X, μ_skip = # in W×Y×X (an AP triple (a, b, 2b−a)
with the three members in the three listed blocks respectively).

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

## 5. The growth theorem — resolved by three-front convergence
## (MERGE section: notes/71 + notes/75 + this front, same day)

This front was tasked with proving v_min(0)(M) ≥ c·M.  Mid-session,
two sibling fronts landed results that resolve the growth question
from both sides; this section is the merged statement, with this
front's contributions folded in where they now belong.

**Theorem V0 (growth/collapse of the free-lower-anchor price).**
Let M ≡ 0 mod 4.  bal mode:

(a) **Collapse route [notes/75 Theorem J-DOWN, PROVED; 3-line
restriction].**  If the balanced 2-seam coupled core at anchor
m = M/2 is infeasible, then the (v,0) cell at M is infeasible for
EVERY v: v_min(0)(M) = ∞.  The core is machine-true at
m = 16, 24, 32, 48, 64, 80 — **plus m = 20, NEW this session:
(none,0)@40 UNSAT [12.6s] via the 4-block encoder, a fresh core
scale** — ⟹ **v_min(0)(M) = ∞ at M = 32, 40, 48 by DIRECT
(none,0) cells (7.4s / 12.6s / 22.0s) and at 64, 96, 128, 160 via
the tested m's**; all-m is GAP-N6a (the near-closed N6a schema).  The
finite regime is exactly M ∈ {8, 16, 24}: 12 exact; (6, 384];
(65, 1440] ((none,0)@24 SAT — the m = 12 core does not fire).

(b) **Two-case route [notes/71 schema; unconditional on (a)].**
Every balanced coloring is either LOW-PURE (its Bm1∪B0 part
single-parity per team) — dead at EVERY budget by Lemma K on the
low chain (M ≥ 12; the kill is intrinsic to the chain: any AP-free
team order restricts to an AP-free prefix-order of the parity
chain, so it covers ALL low-pure colorings, including the
composite zeros found by e174 below) — or LOW-IMPURE, in which
case it pays μ_up + μ_skip ≥ f(M) in s2 by T-CHAN (§3).  Hence
v_min(0)(M) ≥ f(M), and [GAP-FHALF: f(M) ≥ M/2] gives the linear
bound this front was tasked with — as an orders-free counting
lemma.

(c) **[GAP-VMIN0-growth] is DISCHARGED**: divergence holds by
route (a) modulo GAP-N6a (machine-true along the tested ladder to
M = 160), and independently v_min(0)(M) ≥ M/2 → ∞ modulo the
single counting lemma GAP-FHALF.  const mode: the collapse
threshold is m = 48 via the (2,2,2) cores (J-DOWN + D1/D2), so
const-(v,0)@M = ∞ for M ≥ 96 modulo GAP-N6a; the measured const
points at 24 ((6,0), (65,0) UNSAT) are finite-regime demand.

**This front's standing contributions (the GAP-FHALF layer):**

1. **The zero set of the sumset floor is bigger than the parity
   schedules** (e174 zeroset, M = 16, 24, 32, 40): balanced
   colorings with μ_dn = μ_up = μ_skip = 0 for BOTH teams exist at
   Hamming distance 6..26 from the nearest (x,x,1−x,1−x) schedule —
   anatomy: parity core + full-range blocks at the TOPS of B1/B2
   (e.g. M = 32: A = evens(16,64] ∪ odds(64,109] ∪ [120,128] ∪
   odds(128,221] ∪ {233,237} ∪ [242,256]).  Every zero found is
   LOW-PURE, hence Lemma-K-dead — machine confirmation that the
   two-case split of route (b) is exhaustive-in-practice: **the
   floor's entire zero variety lives inside the order-dead class.**
2. **f(M) measured by a second instrument** (e174 fhalf, CP-SAT
   min-max over teams, exact): f(8) = 4, f(12) = 6, f(16) = 8 —
   agreeing with notes/71's pod ladder value M/2 at all three
   scales — and EXTENDED: **f(24) = 12 = M/2, optimal certificate
   [84.8s]** — the fourth exact scale, first beyond notes/71's
   ladder; M = 32, 40 running at close.
3. **Proved extremal steps toward GAP-FHALF** (§3–4): L-MID (the
   midband (2M, 3M] is never sumset-clean: every balanced (U, W)
   mints (2U−W)-mass there — hand proof M ≥ 32, machine 16..40),
   L-SEESAW (2·B1 = B2: coverage ≥ M/2 unconditionally), L-HIT
   (coverage beyond 2M paid unit-for-unit), L-RANGE (the
   up-interval dodge family pays ≥ M/2 − O(1) — the f-target
   achieved on that family).  What remains of GAP-FHALF: the
   general low-impure case analysis (lattice/range composites, N3
   species) — the same residue-casework species as the campaign's
   other uniformization gaps.

## 6. THE KEYSTONE: the composed ledger statement, every link
## statused

**Theorem T-TEL″ (demand side of L-AFFORD, linear regime;
composition of T-LEDGER + T-FRESH + the V0 collapse).**
Assume:

- [N6a] the coupled core fires at every anchor m ≥ 16 (bal) /
  m ≥ 48 (const (2,2,2)) — machine-true m = 16..80, hand schema
  near-closed (sub-gaps: GAP-DICH catalogue rows, GAP-LLOP-α/β,
  GAP-PARM, GAP-ASM′ = (OV-∀), GAP-FG — notes/50 inventory);
- [D1+D2, PROVED] cell transfer: a const-bounds cell applies at
  every anchor whose per-block presence meets its bounds —
  cofinitely many anchors of every Case-2 pair.

Then for every valid Case-2 pair and every 2-adic chain {N_j}:

1. **No zero anchors** (J-DOWN reading): for all large j, some team
   has Inv_T(N_j) ≥ 1 — the everywhere-payment branch of notes/70's
   T-TEL′ dichotomy holds UNCONDITIONALLY on that dichotomy; the
   zero-anchor/echo branch (a) is empty above the collapse
   threshold.  (L-ECHO stays live only at the three finite scales.)
2. **Disjoint ledger** [T-LEDGER, PROVED]: along each 4-adic
   subchain the forced payments are pairwise-disjoint inversion-pair
   families — an infinite disjoint system, ≥ 1 fresh pair per two
   octaves, forever.
3. **Fresh mints at every anchor** [T-FRESH, PROVED modulo
   GAP-F-schema]: if both teams pay ≤ v(N_j) at anchor N_j, some
   team owns an inverted pair AT β_j itself; by L-HOME these are
   disjoint at EVERY anchor — density one per octave — and each
   mint's low member is a displaced value (P3), feeding the
   donation ledger.
4. **Per-anchor demand size**: with v_min(0) collapsed to ∞, the
   quantitative per-anchor floor reverts to the budgeted half-core
   frontier v*₃(m; bounds) [GAP-V*, now constant-sharpening for the
   ledger but load-bearing for RATE statements — notes/75 §segment].

Conclusion: **the demand side of L-AFFORD holds in regime (I)** —
diverging cumulative forced fresh demand with exact disjoint
bookkeeping, at density ≥ 1 pair per two octaves (unconditional
modulo [N6a]) and 1 per octave (modulo [GAP-F-schema]).  What the
composition does NOT give — unchanged, and provably not obtainable
in this currency (NG1–NG4; X-INTERLEAVE realizes branch-2 demand
with a valid free team): the supply cap.  **L-AFFORD = demand
(above) ∧ [GAP-AFFORD′]** (overpayment capacity in donations,
single-use colored values — the program's terminal gap).

### Link-status table (complete, as of this session)

| link | statement | status |
|------|-----------|--------|
| L-HOME | each adjacent-octave pair lives at exactly one boundary | PROVED (notes/70 §1) |
| L-2PRICE | each boundary priced by exactly 2 chain anchors | PROVED (notes/70; 10/10 witness audit) |
| T-LEDGER | 4-adic subchain payments = perfect disjoint partition | PROVED (notes/70 §1) |
| L-SQUEEZE | per-anchor price subadditivity (no parking) | PROVED (notes/70 §1) |
| L-ECHO | zero anchor books its giant payment at 2 anchors, same team | PROVED; subsumed above collapse threshold (no zero anchors); live at M ∈ {8,16,24} |
| T-CHAN / L-PREFIX | (v,0) three-channel demand calculus | PROVED (notes/62 §4c = notes/72 §3) |
| Lemma K + SCHED-DEAD + low-pure arm | low-pure colorings dead at every budget, M ≥ 12 | PROVED (notes/62 §4d; notes/71 §1) |
| Theorem J-DOWN | anchor-m core fires ⟹ (·,0)@2m UNSAT ∀vup | PROVED (notes/75 §2.2) |
| coupled core, all m | bal m ≥ 16; const (2,2,2) m ≥ 48 | machine m = 16..80; hand = GAP-N6a (near-closed, sub-gaps in notes/50) |
| GAP-FHALF | f(M) ≥ M/2 (orders-free counting) | OPEN; = M/2 exact at 8/12/16 (two independent instruments); 24/32/40 in flight; proved pieces L-MID/L-SEESAW/L-HIT/L-RANGE (notes/72 §3–4) |
| GAP-VMIN0-growth | v_min(0)(M) → ∞ | **DISCHARGED** (route (a) modulo GAP-N6a; route (b) modulo GAP-FHALF) |
| GAP-J-schema | (v,0) all-M family | large M = GAP-N6a verbatim (J-DOWN); finite scales machine-done; residual: margin family (v, w ≥ v*₃(m)) [GAP-J-margin, open] |
| GAP-F-schema | freshness family F(N; v) UNSAT | OPEN; machine (16;6) UNSAT ×2 pods; does NOT project under J-DOWN (notes/75) — genuinely new content; F(24;65) in flight (sprint-C, 86400s) |
| T-FRESH | disjoint fresh mints, density 1/octave | PROVED modulo GAP-F-schema (notes/70 §4) |
| D1 + D2 | transfer of const cells to Case-2 anchors | PROVED (notes/62, notes/54) |
| GAP-V* | v*₃(m; bounds) growth | open; demoted for demand EXISTENCE, load-bearing for demand RATE |
| GAP-AFFORD′ | supply cap in donation currency | **OPEN — the terminal gap**; unchanged; targets: charge the everywhere-fresh mint system (1 displaced value per octave forever) |

Net for the ledger chain: with GAP-VMIN0-growth discharged, the
Case-2 kill = [N6a closure] + [GAP-AFFORD′] (+ GAP-F-schema for the
density-1 sharpening; + GAP-FHALF only if one wants the finite-scale
linear law independent of N6a).  The demand half of GAP-G2's
reframed T-FORCE statement is now a THEOREM modulo N6a — the first
time the everywhere-payment conclusion holds without any budget
hypothesis.

## 7. Machine record + fleet state (this session)

| item | verdict | provenance |
|------|---------|------------|
| harvest (512,0)@32 bal | UNSAT [98.6s] | main pod e158_tel_M32_up512_dn0.json |
| harvest (65,0)@24 const (2,3,6,12) | UNSAT [14797.6s] | main pod e158_tel_M24_const_up65_dn0.json |
| harvest (100,0)@32 const | TIMEOUT [43200s] | main pod |
| harvest (512,0)@48 bal | TIMEOUT [43200s] — moot post-J-DOWN | main pod |
| harvest F(16;6) pod re-run | UNSAT [1350.2s] — 2nd independent | main pod e173_fresh_M16_v6.json |
| harvest F(24;65) | TIMEOUT [43200.4s] | main pod; relaunched sprint-C 86400s |
| e174 midcheck (L-MID) | UNSAT (= lemma holds) ×4, M = 16/24/32/40 | data/e174_band_floor.jsonl |
| e174 zeroset | SAT ×4 — non-schedule zeros exist, all LOW-PURE | data/e174_band_floor.jsonl (witnesses inline) |
| e174 fhalf | f = 4/6/8 at M = 8/12/16 = M/2 exact (OPT); 24/32/40 running | data/e174_band_floor.jsonl |
| fleet incident | wrong cell (e127 per-team) on all 3 sprint pods; killed + quarantined; nothing entered the series | §2 |
| sprint-B (relaunched, correct encoder) | pump grid 16: 12/24/48/96; 24: 128/256; 32: 768/1024 (last four = J-DOWN blind tests) | data/vmin0_series.log on pod |
| sprint-C cert battery (LANDED in-session) | pump (11,0)@8 **UNSAT [24.9s]** — the same pod that printed SAT under the wrong encoder now confirms the true verdict, closing the incident loop; (12,0)@8 **SAT [5.6s]** (v_min(0)(8) = 12 re-verified cross-pod); (6,0)@16 UNSAT [3.2s]; (65,0)@24 UNSAT [71.9s]; **F(16;6) UNSAT [802.0s] — THIRD independent run**; F(24;65)@86400 in flight | data/vmus_cert.log on pod |
| sprint-D wave 1 (correct encoder) | (64,0)@48 UNSAT [67.7s], (128,0)@48 UNSAT [164.4s], (256,0)@48 UNSAT [246.6s] — fifth-scale deep-UNSAT cheap, J-DOWN-consistent | data/fresh_series.log on pod |
| sprint-D wave 2 (re-task) | **(none,0)@40 UNSAT [12.6s] — m = 20, FRESH core scale; (none,0)@48 UNSAT [22.0s]**; @64 / @96 + margin (368,6)@32 [86400s] running at close | /root/e/run_fresh2.py → data/fresh_fix2.log |

Open rows to harvest next session: sprint logs (above), e174 fhalf
24/32/40, F(24;65).  Decisive next mathematics: GAP-AFFORD′ (the
terminal), GAP-FHALF general case, GAP-J-margin, N6a sub-gaps.
