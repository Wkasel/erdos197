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
