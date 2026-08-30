# 79 — FRONT AFFORD-TOURNAMENT: five strategies vs GAP-AFFORD′

Task: GAP-AFFORD′ is the program's terminal open problem (notes/50
§2d): for every valid Case-2 pair, the donation supply (single-use
colored values, P3-accounted) cannot fund the T-TEL″ forced mint
system (≥ 1 displaced value per two octaves, disjoint, forever).
Refuted routes, NOT retried here: pair-counting (X-INTERLEAVE / P1
freshness), budget rectangles (NG4), descent 2-path counting
(GAP-COMP, parity orientation), naive cross-anchor disjointness
(maximal overlap measured, notes/70 §2), single-team accounting
(NG1/P7).  This front generates FIVE genuinely distinct strategies,
pre-registers each as an exact statement with a machine attack, runs
the attacks in-session, and records survival.

Machine companion: experiments/e179_afford_tournament.py →
data/e179_*.json / .log.  All predictions in §0 committed BEFORE any
run (campaign rule).

## 0. The five strategies (pre-registered)

**S1 RECURSION (home-conflict).**  Displaced values have home
anchors with their own mint demands.  Statement to prove
(L-DOUBLE-DUTY): a value u ∈ O_m cannot be simultaneously the low
member of an inverted pair at β_m (mint-low for anchor chain above)
and the high member of an inverted pair at β_{m−1} (mint-high for
the anchor below) unless the team pays ≥ |O_m ∩ T| adjacent
inversions at anchor 2^{m−1} — i.e. mint material at consecutive
boundaries is VALUE-disjoint below presence-scale budgets.  Hand
proof expected (pure transitivity, P4's argument specialized);
machine check: 4-block gadget with a forced double-duty value,
budget scan around |B0 ∩ T|.  Prediction: lemma true, UNSAT below
presence, SAT at/above; upgrades T-FRESH's pair-disjointness to
value-disjointness; does NOT by itself close AFFORD′ (still
demand-side bookkeeping — NG4 delimits).

**S2 BAND-WEIGHT.**  Mints consume values from specific bands (the
P3-displaced low members live in Bm1 = the paying window's prefix
block); the band theorems (L-MID/L-SEESAW, notes/72 §4) constrain
them.  Question: is the mint low member forced into a THIN band of
its octave (e.g. the top-of-Bm1 boundary zone), so that a band-depth
weighting makes supply converge while T-TEL″ demand diverges?
Machine: band-relaxed (v,0) cells at M = 8 (v = 11 = v_min(0)−1):
allow s0-inversions only when the low member lies in band B ⊆ Bm1,
scan singleton and top-k/bottom-k bands, map where the mint can
live.  Prediction (honest): the mint can live in MANY bands (any
single value suffices), because every value is colored and some team
always has band material — in which case S2 as stated dies by the
same supply-freshness that killed pair-counting; recorded value =
the band map itself (finite shadow of AFFORD′'s eventual currency).

**S3 DENSITY-TRANSFER.**  Each mint displaces a value against type;
claim: infinitely many against-type displacements force one team's
density in some window family to drift, contradicting a
concentration bound (window concentration L1′-style, or ROT4's
sup-density 5/6, notes/76).  Pre-registered obstacles: (a) density
is a coloring fact — order displacement does not move it; the only
displacement→density channel is donation flux, measured ≡ 0 (e121,
L2-strong refuted); (b) the payer is not single-team (e127 asym
rows SAT at v = 0; irreducibly two-sided) and ROT4's per-scale
coupled failures already ALTERNATE teams (B at 16, both at 32, A at
64 — e131); (c) L1′ is REFUTED (ROT4) and 5/6 is not universal
(ROT2 sup = 1).  Machine: fresh-scale payer-identity runs (ROT4
coupled at m = 48, 80) to test whether the failing team is
eventually constant.  Prediction: alternation persists ⇒ S3 REFUTED
at the formalization level.

**S4 HYBRID-CASE (dodger-axis split).**  Split Case 2 by dodger
axis (iii) (pair-sparse donation material, notes/46 §5, notes/74
§II.4).  If (iii) fails, donations hand the partner gap ≤ 2
attacker pairs — the G3 landing-pad geometry / p(k) pump (arm open
in general; supported).  If (iii) holds, every block-minority is
gap ≥ 3, hence ≤ |blk|/3 per block and lattice-structured.  Machine
(the load-bearing test): the two-seam coupled core CI(m) with the
per-block MINORITY constrained pair-sparse (all 8
minority-designation vectors per cell), at cells where the general
core is SAT: (1,1,1) @ m = 16, 24, 32, 48; (2,2,2) @ m = 16, 24,
32, 40.  Prediction (from the spacing-2 sumset argument, §4 below):
sparse-minority cores go UNSAT strictly BELOW the general
thresholds — i.e. axis (iii) buys the dodger nothing at the core
and costs it the lattice escapes; if confirmed at ≥ 3 scales this
pincers the corner: (iii)-dodgers meet a STRONGER core family,
¬(iii)-dodgers feed the pair pump.  Exhaustion of the corner =
this + arm-B closure (NOT expected to complete in-session).

**S5 YES-CONSTRUCTION (the honest dodger build).**  CP-SAT build of
a 2-coloring of [1, 2^12] with all three dodger axes encoded:
(i) subcriticality proxied by censored chain depth (no in-team
doubling chain of depth ≥ D with reflectors ≤ F, D ∈ {2, 4},
F = 12 — ROT4-style; NOTE the proxy is STRONGER than true
subcriticality, so UNSAT certifies only the bounded-depth
sub-corner); (ii) window-diffuse: min-team count ≥ g(a) in every
ratio-2 window (a, 2a], 32 ≤ a ≤ 2^11, g slowly growing;
(iii) every dyadic-block minority pair-sparse (gaps ≥ 3).
Everywhere-split floor: minority ≥ f(t) per dyadic block, f slow.
SAT ⇒ audit the witness (orbit depth, window stats, live pairs) —
first inhabitant of the corner under proxy, YES-material.  UNSAT ⇒
finite certificate that the BOUNDED-DEPTH corner is empty at 2^12;
bisect the horizon.  Prediction: genuinely uncertain — the (i)/(iii)
tension (lattice minorities carry their own reflector classes) vs
the freedom of depth-D-censored chains; this is the strategy most
likely to produce a surprise in either direction.

Survival protocol: each §1–§5 records statement → machine verdict →
survival status ∈ {PROVED-TOOL, SURVIVES (escalate), WOUNDED,
REFUTED}.  §6 is the tournament verdict + ledger movement.

---

## 1. S1 RECURSION — Lemma L-DOUBLE-DUTY [PROVED, machine-exact ×2]

**Lemma L-DOUBLE-DUTY.**  Let T be a team of a valid pair, u ∈ O_m,
and suppose u serves double duty: u is the HIGH member of an
inverted pair (u′, u) at β_{m−1} (u′ ∈ O_{m−1}, pos(u) < pos(u′))
AND the LOW member of an inverted pair (u, w) at β_m (w ∈ O_{m+1},
pos(w) < pos(u)).  Then

    Inv_T(2^{m−1})  =  x_{m−1}(T) + x_m(T)  ≥  |O_m ∩ T| + 1.

*Proof.*  pos(w) < pos(u) < pos(u′) gives pos(w) < pos(u′): the
skip pair (u′, w) is inverted across O_m.  For every y ∈ O_m ∩ T:
if pos(y) < pos(u′) then (u′, y) is an inverted β_{m−1} pair; else
pos(y) ≥ pos(u′) > pos(w), so (y, w) is an inverted β_m pair.  The
|O_m ∩ T| pairs so produced are distinct (each names y), and the
mint pair (u, w) itself is an inverted β_m pair distinct from all
of them except the y = u case — count again: y = u produces
(u′, u) at β_{m−1}, and (u, w) is separate.  Total ≥ |O_m ∩ T| + 1.
Both pairs are eligible seam pairs of anchor 2^{m−1} (L-2PRICE:
β_{m−1} = its s1, β_m = its s2).  ∎

**Machine (e179 s1lemma, 4-block gadget, balance, double duty
forced on a mid value u ∈ B0, budget on the payer's s0+s1 total):**
M = 8: UNSAT at 3, 4, SAT at 5 = |B0∩A| + 1 exactly.  M = 16
(BLIND after the M = 8 correction): UNSAT at 8, SAT at 9 = 8 + 1
exactly.  The lemma is sharp — the machine found the +1 the first
draft missed (the mint pair itself), then confirmed it blind at the
next scale.

**Reading (the home-conflict formalized).**  T-FRESH mints are
pair-disjoint across boundaries (L-HOME); L-DOUBLE-DUTY upgrades
this to VALUE-disjointness at consecutive boundaries for any team
whose anchor price is below its own presence: if
Inv_T(2^{m−1}) ≤ |O_m ∩ T| (true forever for Θ-dense teams under
any sub-presence payment regime), then the O_m-values used by the
mint at β_{m−1} (as highs) and by the mint at β_m (as lows) are
DISTINCT.  Per octave, the everywhere-mint branch of T-TEL′
consumes ≥ 2 distinct values of paying teams.  What it does NOT
give: any upper bound on supply — the two values are fresh per
octave (P1) and the payer may alternate (notes/47).  S1 is a
bookkeeping theorem, not a route to the cap.

**Survival: PROVED-TOOL** — enters the ledger chain next to
L-HOME/L-2PRICE; escalation value = combines with any future
band-localization (S2) to charge SPECIFIC values twice.

---

## 2. S2 BAND-WEIGHT — REFUTED as stated (full band map measured)

**Machine (e179 s2band, M = 8, v = 11 = v_min(0)(8) − 1).**  The
(11, 0) cell (s0 = s1 = 0, s2 ≤ 11) is UNSAT [38.1 s, fresh
encoder — third independent replication of the point].  Relaxation:
allow s0 (= β(8)) inversions ONLY when the pair's low member lies
in band B ⊆ Bm1 = {5, 6, 7, 8}, s1 still 0, s2 ≤ 11.  Result:
**SAT for EVERY singleton** B = {5}, {6}, {7}, {8} (5.2 / 6.3 /
94.4 / 20.7 s) and for both halves and the full band.  The mint
can be minted on ANY single low-member value; the forced-band map
is FULL, not thin.

**Why this kills the strategy (a-priori half, now with the machine
half confirming).**  A band-depth weighting w(·) proves a supply
cap only if per-octave forced-demand weight exceeds per-octave
supply weight infinitely often.  T-TEL″ demand is O(1) mints per
octave, each consuming O(1) values (L-DOUBLE-DUTY: 2 per octave);
supply per octave is EVERY colored value of the octave (P1
freshness), and the band map says no sub-band is forced — the mint
chooses its band freely, so any weighting that makes demand
diverge makes supply diverge at least as fast, at every octave,
for every monotone band weighting.  The only escape would have
been a FORCED thin band with vanishing team presence — but values
partition: some team always has band material, and the map shows
even singletons suffice.  (Caveat recorded: measured at the
(·,0)-form of the mint at the boot scale M = 8; the F-form and the
scales 16/24 are the same shape and are the only other finite
scales — v_min(0) = ∞ from 32 on, J-DOWN.)

**Survival: REFUTED** (as a route to AFFORD′).  Salvage kept: the
band map itself — mint-location freedom is now measured, which any
future supply argument must respect (it must charge mints
independently of WHERE in the octave they are minted).

---

## 3. S3 DENSITY-TRANSFER — REFUTED (payer identity alternates)

Formalization attempted: "infinitely many against-type mint
displacements force one team's density in some window family to
drift, contradicting a concentration bound."  Three independent
kills, one new machine layer:

1. **No channel.**  Window density is a COLORING fact; a mint is an
   ORDER fact.  The only known order→coloring channel is donation
   flux, and donation→donation completion flux is identically 0 on
   every coloring ever measured (e121; L2-strong REFUTED).  A drift
   argument would need a new channel; none is on the table.
2. **No fixed payer.**  Both one-sided budget weakenings of the
   coupled core are SAT at v = 0 (notes/47 asym/majb) — nothing
   forces the SAME team to pay twice, let alone forever.
3. **Machine (e179 s3rot, fresh scales): the payer identity of the
   only known (i)+(ii) realizer alternates.**  ROT4-colored double
   block order, per team: m = 16: B fails; 32: both; 48: both
   (NEW); 64: A fails, B survives; 80: both (NEW).  The failing
   team follows the 4-phase rotation — no eventually-constant
   payer, hence no single-team drift, on the exact witness class a
   density-transfer argument would have to bite.  (Also
   cross-validates e131's 16/32/64 rows verbatim.)
4. The quoted concentration bounds cannot serve anyway: L1′ is
   REFUTED (ROT4), and the 5/6 sup-density law is a ROT4-specific
   theorem (ROT2 has sup 1) — there is no universal window
   concentration to contradict.

**Survival: REFUTED.**  Nothing here is salvageable as a supply
route; the alternation map is kept as a constraint on future
strategies (any ledger must allow the payer to rotate).

---

## 4. S4 HYBRID-CASE — the SPARSE CORE fires: axis (iii) buys the
## dodger a STRICTLY STRONGER core [MACHINE, 7 scales + controls]

**The instrument** (e179 s4core): CI-geometry at anchor m — blocks
(m, 2m], (2m, 4m], (4m, 8m], both teams block-ordered at both
seams, per-team per-block lower bound k = 1 ONLY (no balance, no
(2,2,2)) — plus the dodger's axis (iii): in each block, the
designated minority team (card ≤ half) is pair-sparse (no two of
its values at distance ≤ 2, i.e. all gaps ≥ 3, the notes/46 §5
constraint verbatim).  All 4 designation vectors mod global team
swap; cell = UNSAT iff every designation is UNSAT.

**Machine map (all cells this session; sprint fleet + local):**

| m | bare (1,1,1) | cap-only | sparse gap≥3 | sparse1 gap≥2 |
|---|--------------|----------|--------------|---------------|
| 8  | SAT | — | SAT (ABA escape) | — |
| 12 | SAT | — | SAT (ABA escape) | — |
| 16 | SAT | SAT (ABA/ABB) | **UNSAT ×4** | SAT (ABA escape) |
| 20 | SAT | — | **UNSAT ×4** | — |
| 24 | SAT | — | **UNSAT ×4** | SAT (ABA escape) |
| 28 | SAT | — | **UNSAT ×4** | — |
| 32 | SAT | SAT (ABA/ABB) | **UNSAT ×4** | — |
| 40 | SAT | — | **UNSAT ×4** | — |
| 48 | SAT | — | **UNSAT ×4** (≤ 222 s) | — |

Readings, in order of weight:

1. **The sparse core fires from m = 16 at bounds (1,1,1)** — seven
   consecutive scales, all four residues mod 16 represented, boot
   window m ≤ 12 (exactly the bal core's boot window).  The general
   Case-2 core needs (2,2,2) + m ≥ 48; under axis (iii) the SAME
   double-block-order death appears at minority size 1 and scale
   16.  Pair-sparseness SUBSTITUTES for balance in the coupled-core
   engine.
2. **Attribution is complete.**  Bare (1,1,1): SAT at every scale
   (the known hide-a-block escapes).  Cap-only (minority ≤ half,
   no sparseness): SAT.  Gap ≥ 2 only: SAT — and the surviving
   designation is exactly ABA, the parity-lattice escape (minority
   on a spacing-2 class).  Gap ≥ 3 — precisely the (iii)
   constraint — is what outlaws the parity lattice, and with it
   every escape.  The dodger corner's own defining constraint is
   the killing clause.
3. **Hand-schema skeleton (the spacing-2 covering argument), AAA
   designation.**  If one team A is sparse-minority in all three
   blocks, the majority B must void its straddle family
   (u, y, 2y−u) ∈ (B∩B0)×(B∩B1)×(B∩B2) (each mono triple forces a
   banned seam edge — L-PREFIX/T-CHAN verbatim).  Fix z ∈ B∩B2 in
   the reachable midband: its representation line
   ℓ_z = {(u, y) : u = 2y − z} has u-values spaced 2 (one parity
   class) and y-values CONTIGUOUS.  Voiding z needs every rep hit
   by A: but a gap-≥3 set covers ≤ every other point of a
   spacing-2 u-line and ≤ 1/3 of a contiguous y-interval —
   jointly < 1 once ℓ_z is long enough, so z must leave B: B
   vacates a contiguous Θ(m) midband of B2, i.e. A ⊇ a contiguous
   band — contradicting A's own sparseness.  Mixed designations
   are catalogue cases (the machine closes all of them); the
   uniformization residue is the same N6a species as the rest of
   the pool.  [Write-up gap tagged GAP-SPARSE-CORE.]
4. **What this does to the dodger corner (the honest reading).**
   The corner (i)+(ii)+(iii) was the entire known YES-space, with
   (iii) the unexcluded axis.  Now: a Case-2 pair satisfying (iii)
   meets the sparse core at EVERY anchor with presence ≥ 1 — its
   T-TEL″ demand fires immediately (no (2,2,2) threshold, no boot
   beyond m = 12), and the ¬(iii) branch hands the partner
   attacker pairs (the p(k) pump, measured growing 3/7/7/11).
   Axis (iii) is a pincer, not an escape: it minimizes the
   partner's attack supply at the price of a strictly stronger
   forced-demand core.  NOT claimed: corner emptiness — both arms
   end in demand statements, and the supply cap (AFFORD′ proper)
   is untouched; arm B's general form (p(k) → ∞ + T-PIN at
   varying x) remains open.

**Survival: SURVIVES — escalate.**  Concrete escalation targets:
(a) GAP-SPARSE-CORE uniformization (the covering argument is
close to a complete hand proof for AAA; catalogue the mixed
designations); (b) test whether the sparse core, like CORE′,
collapses the 4-block pump at (·, 0) for sparse colorings
(J-DOWN transfers verbatim — restriction argument is
coloring-agnostic); (c) the sharp question the pincer isolates:
can the MINT SYSTEM ITSELF be paid while keeping (iii) — i.e. is
the displaced value of each mint forced to sit at distance ≤ 2
from other minority material?  If yes, paying mints EVENTUALLY
BREAKS (iii) and the corner self-destructs — that is a NEW
statement of exactly AFFORD′'s shape, now with a finite handle.
