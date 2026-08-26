# S2: death-mechanism theory for growing reflector sets

## Question
The growing-sliver swap (S1 family) survives every existing death
mechanism because both hypotheses break under growth: lem:orbit needs a
FINITE reflector set, thm:ogred needs FIXED attackers (15, 16) at
finitely many positions.  Does either mechanism extend to growing
reflectors / scale-adapted attackers, and exactly under what condition?

**Answers.**
1. The orbit mechanism does NOT extend on any size/growth hypothesis:
   lem:orbit's finiteness is sharp (T-SHARP below, machine-certified).
   What survives is a *relative-position* dichotomy (L-STEP/L-DESC):
   an infinite orbit forces the permutation to procrastinate infinitely
   many DISTINCT reflector values past exponentially larger orbit
   elements.  Growth alone can never be a death certificate; forced
   *early placement* can.
2. The crown/order-gadget mechanism DOES extend — but in FIXED-PAIR
   form, not the expected scale-adapted form.  Teams are interval
   unions with necks n_r = 2 s_r − s_{r+1}; the NECK lemma (§4) shows
   every schedule leaves some team attacked by a fixed pair of its own
   values at infinitely many scales (bounded necks: in-interval;
   unbounded: across the seams), and T-PIN (thm:ogred's pigeonhole
   verbatim) reduces death to per-scale finite UNSAT rungs.  The
   scale-adapted route (x_t = 2 s_t + c with a position-regress
   overflow, T-REGRESS §4b) is closed by machine: single-attacker
   rungs are SAT everywhere, only PAIRS force, and pair conclusions
   admit a per-scale sacrifice.  Machine rungs (§5): pair rungs UNSAT
   at 4 schedules × 3 scales; RUNG-IN geo/B UNSAT at 3 scales — geo is
   dead modulo its rung family; C3's own core dies under truncation,
   so the rungs ride a new, unknown core (the next-C3 crux).

Everything below is machine-checked by experiments/s2_growing_death.py
(data/s2_*.json); the checks are cited inline.

## 1. The step lemma, and what lem:orbit's proof really uses

Setup: S ⊆ Z+ permutable via π; write pos(v) for the position of v.
An *orbit* is u_0 < u_1 < ... in S with u_{k+1} = 2 u_k − f_k, f_k ∈ S
(so f_k < u_k, and (f_k, u_k, u_{k+1}) is a 3-AP inside S).

**Lemma L-STEP.**  In any monotone-3-AP-free arrangement,
pos(u_{k+1}) < pos(u_k)  ⇔  pos(f_k) < pos(u_k), and
pos(u_{k+1}) > pos(u_k)  ⇔  pos(f_k) > pos(u_k).
*Proof.*  The AP (f_k, u_k, u_{k+1}) must not be placed increasingly
(f_k, u_k, u_{k+1} in position order) nor decreasingly.  If the
reflector is early (pos(f_k) < pos(u_k)) the decreasing pattern is
impossible and the increasing one forbidden, so pos(u_{k+1}) <
pos(u_k): the orbit *descends*.  If the reflector is late the mirrored
argument forces ascent.  ∎

So along an orbit, position descends exactly at early-reflector steps
and ascends exactly at late-reflector steps.  lem:orbit is the special
case where finiteness of F forces every sufficiently late step to be an
early-reflector step (all of F sits below the fixed position
q = max pos(F), while pos(u_k) → ∞): eventually all steps descend —
infinite strictly decreasing positions, contradiction.

**Lemma L-DESC (descent bound / sharp dichotomy).**  If S is permutable
and contains an infinite orbit, then the ascent set
K↑ = {k : pos(f_k) > pos(u_k)} is infinite.
*Proof.*  Otherwise all steps beyond max K↑ descend (L-STEP).  ∎

**Corollary L-PROC (procrastination principle).**  In the situation of
L-DESC: the reflectors {f_k : k ∈ K↑} take infinitely many DISTINCT
values, and their positions are unbounded; each such f_k is placed
later than u_k ≥ 2^{k−k_0} u_{k_0} — a value exponentially larger than
itself.  In particular lem:orbit follows (finite F ⇒ finitely many
distinct reflector values).
*Proof.*  pos is injective and pos(u_k) → ∞ in the "all but finitely
many exceed any bound" sense; for k ∈ K↑, pos(f_k) > pos(u_k).  A fixed
value has a fixed position, so a value can serve as a late reflector at
only finitely many k.  ∎

Machine (CHECK 2, data/s2_shadow.json): on explicit orbit prefixes of
the S1 teams (lin/A t0=12 L=6, lin/A t0=14 L=8, lin/B t0=13 L=10),
the constraint set {every reflector early} + {u_0 before u_L} is UNSAT,
while {every reflector early} + {u_L before u_0} is SAT — the finite
shadow of forced descent, on the actual partitions, at 3 scales.

## 2. T-SHARP: growth alone can never kill

**Theorem T-SHARP.**  For every unbounded nondecreasing g: Z+ → Z+
there is a permutable S containing an infinite orbit whose reflectors
are distinct with f_k ≤ g(k) + C — in particular f_k = o(u_k) with
f_k = Θ(log u_k) achievable.  Hence there is NO theorem of the form
"S contains an infinite orbit with f_k = o(u_k) (or any growth bound on
reflector sizes alone) ⇒ S not permutable".

*Construction.*  Greedily pick u_0 and distinct reflectors f_0 < f_1 <
... as small as possible subject to: the only 3-APs wholly inside
S = {u_k} ∪ {f_k} are the orbit APs (each new f_k, u_{k+1} rules out
finitely many values, so the greedy choice stays within f_k = Θ(k)).
Arrange S as  u_0, u_1, f_0, u_2, f_1, u_3, f_2, ...  Every AP in S is
some (f_k, u_k, u_{k+1}); its position pattern is (last, first, middle)
— neither monotone direction.  So the arrangement is monotone-3-AP-free
while every reflector is LATE and every step ascends (L-STEP sign rule
in vivo).  ∎

Machine (CHECK 1, data/s2_sharp.json): built at K = 20/40/60 steps,
u_0 = 101; exhaustive AP enumeration confirms only-orbit-APs; the
interleaved order verified monotone-AP-free; reflectors distinct,
f: 3..581 vs u_K ~ 2^67 (max f/u ≈ 3·10⁻²  at k=0, decreasing);
step-lemma sign audit passes at every step.  All PASS.

Interpretation: the moment reflectors may be pairwise distinct, an
adversary can pay for every descent with one fresh procrastinated
reflector.  Death must therefore come from *forcing reflectors early* —
a placement statement, not a size statement.  That is exactly what
per-scale finite cores (OG/C3 style) provide, and nothing else in the
current toolkit does.

## 3. The ray form, and which S1 teams even have slow orbits

Writing the orbit as a ray: u_m = 2^m(u_0 − Σ_{j<m} f_j 2^{−j−1}), so
u_m = 2^m α + ρ_m with α = u_0 − Σ f_j 2^{−j−1} and drift
ρ_m = Σ_{j≥m} f_j 2^{m−j−1}.  For f_j ≤ B(j) slowly growing,
ρ_m = O(B(m)): a ratio-2 ray staying within O(B(scale)) of the exact
ray 2^m α — the task's "2^m A + t_m" shape, with t_{m+1} = 2 t_m + f_m.
In the growing-sliver partition the in-team corridor at scale t has
width s_t (kept bottom above s_t, received sliver below s_{t+1}), so
slow orbits ⇔ rays threading the sliver corridors:

**Lemma SLIVER-ORBIT.**  In the S1 partition with schedule s, team P
(owner parity p), the sliver route kept(t) → received(t+1) → kept(t+2)
is realizable at scale t (any reflector sizes) iff
        s_{t+2} ≤ 2 s_{t+1} − 2 ,
and an infinite slow orbit (f ≤ 6·max local s) exists iff this holds at
all large owner-parity t together with in-team availability of
reflectors in the induced windows (which are intervals of width ~s and
always contained team values in every case tested).
*Proof of the inequality.*  From a received offset o' ≤ s_{t+1}, a kept
landing needs offset 2o' − f' > s_{t+2} with f' ≥ 1, i.e.
s_{t+2} + 2 ≤ 2o' ≤ 2 s_{t+1}.  Conversely take o' = s_{t+1},
o'' = s_{t+2} + 1.  The kept → received step imposes no inequality
(f = 2o − o' ranges over an interval of width s_{t+1}).  ∎

Machine (CHECK 3, data/s2_orbit.json), predictions vs certified walks
(exact big ints, every step asserted in-team, orbit relation, cap):

| schedule            | team A       | team B       |
|---------------------|--------------|--------------|
| lin  s_t = t        | EXISTS (walk to octave 412, f ≤ 2^10) | EXISTS (oct 413) |
| geo  s_t = 2^⌊t/2⌋  | **BLOCKED** (s_{t+2} = 2 s_{t+1})     | EXISTS (oct 413) |
| frac s_t = ⌊2^t/t⌋  | EXISTS (oct 412, f huge but o(u))     | EXISTS (oct 413) |
| gm   Geneson-matched| **BLOCKED** (stage jumps)             | **BLOCKED**      |

Notes.  (i) geo is asymmetric: the doubling schedule blocks team A's
route by the pure inequality (independent of reflectors), while team B
(where s_{t+2} = s_{t+1}) has orbits.  (ii) gm is blocked on BOTH teams
at every stage boundary (s jumps by the unbounded factor 8·4^k) — the
growing-sliver partition matched to Geneson's stage widths inherits
exactly the mechanism by which Geneson's own W stays orbit-clean:
continuing through a stage jump needs Θ(u) reflectors.  (iii) For lin
the walk's reflectors grow like Θ(t) = Θ(log u) — the slowest possible
growth beyond finiteness (cf. T-SHARP), so lem:orbit misses these teams
by exactly one hypothesis.  By T-SHARP, the EXISTS entries are NOT
death certificates; they mark where the orbit pressure sits.

## 4. The interval view, the neck lemma, and the return of the
## fixed-attacker pigeonhole

**Interval view.**  In every growing-sliver partition, team P (owner
parity p) is — apart from finitely many small values — a union of
INTERVALS: kept body and received sliver are adjacent, so
    I_t = (2^{t−1} + s_t, 2^t + s_{t+1}],   t ≡ p,
with Q's interval I_{t+1} filling the gap.  Define the *neck* sequence
    n_r := 2 s_r − s_{r+1}   (any sign).

**Attack thresholds (exact).**  For a fixed in-team x below I_t:
- in-interval attacks (x, y, 2y−x), y and 2y−x ∈ I_t:  exist iff
  x ≥ n_t + 2, about (x − n_t)/2 of them, attacking y from lo(I_t)+1
  upward with completions at the top of I_t (OG shape, bottom shifted);
- cross-interval attacks, y ∈ I_t, 2y−x ∈ I_{t+2}:  exist iff
  x ≤ n_{t+1} − 1, about (n_{t+1} − x)/2 of them, attacking the TOP of
  I_t with completions at the BOTTOM of I_{t+2} (the "seam": these are
  single steps of the sliver-route orbit of §3 — margin m_t = n_{t+1}).
Growth kills fixed in-interval attackers iff n_t → ∞; it kills fixed
cross-attackers iff n_{t+1} is bounded.  These two conditions PULL IN
OPPOSITE DIRECTIONS on the same sequence — hence:

**Lemma NECK (conservation of attack surface, exact form).**  For every
schedule, some team carries a FIXED pair {a, a+1} of its own values
attacking (in- or cross-interval) at infinitely many of its scales:
if sup_{r ≡ q, r large} n_r < ∞ then any fixed pair of Q-values above
that sup + 2 pierces every large I_r (r ≡ q) in-interval; otherwise
limsup_{r ≡ q} n_r = ∞ and every fixed pair of P-values cross-attacks
I_t → I_{t+2} at the infinitely many t ≡ p with n_{t+1} large.  (Same
with p, q swapped; often both teams are attacked.)  ∎

Schedule map: lin (n_r = r − 1 → ∞ both parities) and frac and gm
(within stages): both teams cross-attacked by every fixed pair; geo:
n_r = 0 on odd r — team B pierced in-interval by any fixed pair (its
intervals have neck 0) while team A escapes all fixed attacks (necks
→ ∞ on its parity, 0 on the other); one attacked team suffices, since
a partition needs both teams permutable.  gm's stage jumps have
n_r < 0 (r = 8: −30; r = 15: −4032): there EVERY in-team value attacks
the jump interval in-interval.

Machine (CHECK 8, data/s2_neck.json): on the real team sets of all
four schedules, r = 8..13, every in-team x ≤ 40: brute-force attack
enumeration matches the two channel predictions EXACTLY — existence
iffs, exact counts ((x − n_r)/2-style formulas), and channel
completeness (no completion 2y − x, y ∈ I_r, lands in-team outside
I_r ∪ I_{r+2}).  480 (r, x) points, 0 mismatches.

**Theorem T-PIN (pigeonhole, thm:ogred's argument verbatim).**  If team
T contains a fixed pair {a, a+1} attacking at infinitely many scales,
and the per-scale gadget — AP-free order of the attacked window (I_t,
or I_t ∪ I_{t+2} for cross) with both attackers' forced precedences
z ≺ y as units — is UNSAT at infinitely many of those scales, then T is
not permutable.  *Proof.*  pos(a), pos(a+1) are fixed; at most
max(pos(a), pos(a+1)) window elements sit before both; the attacked
windows (thinned to a disjoint subfamily) are infinitely many and
pairwise disjoint, so some window lies entirely after both attackers;
its restriction realizes the gadget — contradiction.  ∎

The pigeonhole survives BECAUSE the attackers are fixed: the
"sacrifice" escape of §4b below (procrastinate one attacker per scale)
is unavailable — one value cannot be sacrificed at infinitely many
scales.  Thus the growing-sliver family is reduced, for EVERY schedule,
to two families of finite UNSAT questions ("rungs"):
- RUNG-IN(t):  interval + fixed-pair attacks (bounded-neck teams, e.g.
  geo/B);  structurally OG(M) with both interval endpoints shifted;
- RUNG-X(t):  seam window I_t ∪ I_{t+2} (or its R ∪ W core) +
  fixed-pair cross-attacks (unbounded-neck case: lin, frac, gm — all
  teams; the attack count at usable scales grows like n_{t+1}/2).
Machine results in §5.

## 4b. T-REGRESS: why varying attackers were NOT enough

Before the neck lemma, the natural repair of thm:ogred was
scale-adapted attackers x_t = 2 s_t + c (which always attack the kept
bottom).  Define SG(t, c): AP-free order of the kept window
(2^{t−1} + s_t, 2^t] with x = 2 s_t + c preceding all of it (units
z ≺ y).  A regress overflow (T-REGRESS) would run: every large in-team
value v is an attacker of some scale; if v cannot precede its window,
some window element w ≺ v; w is again an attacker of a (much larger)
scale; iterate — infinite position descent.  The machine kills this
route in a precise way (§5):
- single-attacker SG(t, (c,)) is SAT at every offset tested (c ≤ 200,
  including the untruncated s = 0 classic OG) — per-VALUE forcing
  fails; the C3 core always needed BOTH attackers 15 and 16;
- pair SG(t, (15, 16)) is UNSAT at every schedule/scale/shift tested —
  but a pair conclusion only forces "some window element precedes ONE
  member", and a per-scale adversary may sacrifice a different member
  at every scale (distinct values ⇒ unbounded positions permitted —
  exactly the T-SHARP procrastination escape).  Quantitatively the
  sacrifice is expensive (with x₁ early, the sacrificed x₂ must follow
  > 64 of the 247 window elements at t = 9: UNSAT for sacrifice bound
  k ≤ 64, SAT at k = 96, so the forced depth lies in (64, 96]; the
  k = 96 witness cohort preceding x₂ is 96 window values, ALL odd, and
  at k = 128 it is all 123 odd values plus two ≡ 6 (mod 8) — the C3
  g-class hierarchy in vivo) but never impossible.
So varying attackers fire per scale only in pair form, and pair
conclusions do not overflow.  The neck lemma makes this moot: fixed
pairs never stopped existing — they just moved to the seams.

The scale-adapted crown.  In team P's kept block t (M = 2^{t−1}),
in-block attacks (x, y, 2y − x) with y = M + s_t + j need
x = 2 s_t + c, c ≥ 2j + (2M − (2y−x)) offsets; concretely the attacker
x = 2 s_t + c attacks y = M + s_t + j with completion
z = 2M − (c − 2j) for 1 ≤ j ≤ c/2 — the SAME (j, i = c − 2j) incidence
as OG's attacker c on a full block, with completions at the SAME top
values 2M − i, only the attacked bottom shifted by s_t.  A fixed x
attacks only scales with 2 s_t < x: growth defeats every fixed
attacker, but at every scale the attacker slot is refilled by
x_t = 2 s_t + c — an in-team value ~2 s_t.

**Definition SG(t, c).**  The finite system: a linear order of the
integer interval W_t = (M + s_t, 2M] with (a) no monotone 3-AP among
in-window triples, (b) the attacker x = 2 s_t + c preceding all of W_t,
i.e. units z ≺ y for every y ∈ W_t with z = 2y − x ∈ W_t.  (For s_t = 0
this is the OG(M) single/pair-attacker system.)

**Theorem T-REGRESS (conditional on rungs).**  Fix the S1 partition
with schedule s and team P with owner parity p.  Suppose there are T_0
and offset sets C_t such that
  (i)  [rungs]  SG(t, c) is UNSAT for every owner-parity t ≥ T_0 and
       c ∈ C_t;
  (ii) [coverage]  every sufficiently large integer v is 2 s_t + c for
       some owner-parity t ≥ T_0, c ∈ C_t.
Then P is not permutable.
*Proof.*  Let π arrange P monotone-3-AP-freely and let v_0 ∈ P be large.
By (ii) pick its scale t_0.  W_{t_0} ⊆ P (the kept interval), and the
restriction of π to {v_0} ∪ W_{t_0} is monotone-3-AP-free (all triples
are in P).  If v_0 preceded all of W_{t_0}, this restriction would
satisfy SG(t_0, c_0) — impossible by (i).  So some w_1 ∈ W_{t_0} has
pos(w_1) < pos(v_0).  Now w_1 ∈ P and w_1 > 2^{t_0−1} ≫ v_0, so (ii)
applies to w_1; iterate.  This yields pos(v_0) > pos(w_1) > pos(w_2) >
... , an infinite strictly decreasing sequence of positive integers.  ∎

Three structural remarks.
- **The overflow is new.**  thm:ogred pinned the attackers 15, 16 at
  finitely many positions and pigeonholed blocks past them.  Here no
  position is pinned: the contradiction is an infinite position regress
  along a chain of values that EXPLODES upward (w_{k+1} ~ 2^{s^{-1}
  (w_k/2)}), each preceded by the next.  Procrastination (the escape
  that voids the orbit route, §2) is exactly what the regress consumes:
  every scale's attacker may be procrastinated, but each procrastination
  event names a larger in-team value placed even earlier, and positions
  are well-founded.
- **Coverage is the schedule-dependent part.**  A value v can attack
  ANY owner-parity scale t with 2 s_t + 14 < v ≤ M + s_t, so coverage
  needs rungs for offsets c up to ~2(s_{t+2} − s_t):
  bounded increments (lin: c ∈ {15,...,18} suffices, all residues
  covered by t ↦ (v−c)/2 parity choice); bounded ratio (geo: c up to
  ~2 s_t; frac: c up to ~6 s_t); gm has genuine coverage HOLES at stage
  boundaries (values in (2^{t−2} + 2 s_t, 2 s_{t+2}) attack no
  owner-parity scale) — T-REGRESS as stated does not close gm.
- **Which team dies is per-parity.**  The rungs are team-blind (SG
  depends only on (t, s_t, c)); owner parity only selects which t serve
  which team.  If rungs hold at all large t of both parities, BOTH
  teams die — the partition dies.

**Relation to C3.**  The pair {x_1, x_2} = {2s_t+15, 2s_t+16} forces
exactly the C3-shifted core {2M−5 ≺ M+s+5, 2M−3 ≺ M+s+6,
2M−10 ≺ M+s+3} among its attacks (completions are s-independent), so
"thm:c3core survives truncation of the bottom s_t values" would have
implied the pair rungs for free.  The machine KILLS the transfer
(§5, CHECK 4b): the C3-shifted core is SAT at lin t = 9, 10, 11 while
the full pair system stays UNSAT — under truncation the UNSAT
certificate migrates to a different, currently unknown core.  The
single-attacker rungs (c = 15 alone, etc.) would have been the cleaner
currency for T-REGRESS since a value v is ONE attacker, not a pair
(and its neighbor v±1 may belong to the partner) — but they are SAT
everywhere tested (§5).

## 5. Machine rungs (CHECK 4–7)

Every instance is a finite linear-order system built by
experiments/s2_growing_death.py and solved with Cadical195 under lazy
transitivity (UNSAT-sound: the CEGAR loop only ever ADDS clauses; every
SAT row carries an explicitly re-verified witness order).  All rows
stream to data/s2_sg_rungs.jsonl.

**Controls (s = 0: the untruncated OG window (M, 2M]).**  Pair
{15, 16}: UNSAT at M = 256 (7 s) and M = 512 (163 s) — thm:ogred's
finite core reproduced by this code path.  Singles c = 3, and c = 15
and c = 16 ALONE: SAT with verified witnesses — the pair phenomenon
is intrinsic already in the classic window (OG's "dropping either
guard family → SAT", reproduced).

**CHECK 4 — pair rungs SG(t, {15, 16}), attackers x = 2 s_t + 15/16:
UNSAT at 4 schedules × 3 scales, no exception.**

| schedule (s_9/s_10/s_11) | t = 9 | t = 10 | t = 11 |
|---|---|---|---|
| lin  (9/10/11)    | UNSAT n=247, x=33,34 [18 s]   | UNSAT n=502, x=35,36 [216 s]   | UNSAT n=1013, x=37,38 [742 s] |
| geo  (16/32/32)   | UNSAT n=240, x=47,48 [13 s]   | UNSAT n=480, x=79,80 [150 s]   | UNSAT n=992, x=79,80 [582 s]  |
| frac (56/102/186) | UNSAT n=200, x=127,128 [5 s]  | UNSAT n=410, x=219,220 [73 s]  | UNSAT n=838, x=387,388 [191 s]|
| gm   (32/32/32)   | UNSAT n=224, x=79,80 [5 s]    | UNSAT n=480, x=79,80 [150 s]   | UNSAT n=992, x=79,80 [585 s]  |

Truncation never rescues the pair gadget — not even frac's
s_t = 2M/t (22 % of the block gone at t = 9, attackers pushed to
x ≈ M/2).

**CHECK 4 — single rungs SG(t, (c)): SAT everywhere tested.**
c ∈ {15, 16, 17, 18} at t = 9, 10 for all four schedules; c = 15 at
lin t = 11; wide probes c ∈ {63, 64} (geo, gm); offset scan at lin
t = 9 up to c = 200 (c = 32, 64, 96, 110, 128, 160, 200 — attacker x
up to 218 against window bottom 266): SAT with verified witnesses,
every one (data/s2_single_cscan_t9.json, s2_single_t11.json).
Per-VALUE forcing fails: hypothesis (i) of T-REGRESS is false at every
point tested, for every schedule — the regress route is closed by
machine, not saved by it.

**CHECK 4b — the C3 core does NOT survive truncation.**  Control s = 0
(= thm:c3core, M = 512): UNSAT [67 s].  The C3-shifted 3-precedence
core at lin t = 9/10/11 (s = 9/10/11): SAT with verified witnesses
[1.5 / 164 / 38 s].  Truncating merely 9 of 256 bottom values already
revives the C3 core, while the full pair system above stays UNSAT: the
UNSAT certificate migrates to a different, currently unknown core.

**CHECK 7 — sacrifice depth (how pair-only the forcing is).**  lin
t = 9, x₁ = 33 early, x₂ = 34 allowed at most k window predecessors:
UNSAT for k ∈ {0, 1, 2, 4, 8, 16, 32, 64}, SAT at k = 96 — the forced
sacrifice depth lies in (64, 96] of a 247-element window (classic
s = 0 control: same shape, UNSAT k ≤ 32 tested).  The k = 96 witness
cohort preceding x₂ is 96 values, ALL odd (mod-8 residues {1,3,5,7});
at k = 128 it is all 123 odd values plus two ≡ 6 (mod 8) — C3's
g-class hierarchy (odd leaves first, then 6 mod 8) appearing in an
adversarial witness nobody asked to be structured.
(data/s2_sacrifice_t9.json, s2_sac_t9_hi.json)

**CHECK 5 — RUNG-IN (fixed-pair in-interval rungs): UNSAT at every
bounded/negative-neck point tested.**
- geo/B, fixed pair {21, 22} ⊂ B, neck-0 intervals I_r =
  (2^{r-1} + s_r, 2^r + s_{r+1}], 21 units each:
  r = 7 UNSAT [0.1 s, n=72], r = 9 UNSAT [6 s, n=272], r = 11 UNSAT
  [337 s, n=1056].  The unit count is SCALE-INDEPENDENT (≈ x/2 per
  attacker) while the window doubles — a bounded core on a growing
  interval, exactly the shape thm:c3core conquered for full blocks.
  If the rungs hold at all large odd r, T-PIN kills geo/B and hence
  the geo schedule.
- gm/A at the stage-jump octave r = 8 (neck −30 < 0: EVERY in-team
  value attacks in-interval), pair {4, 5} ⊂ A: UNSAT [1.2 s, n=159,
  34 units] (data/s2_rungin_gmA_jump8.json).  Whether jump rungs kill
  gm hinges on which parity the sparse jump octaves recur at — stage
  arithmetic, not order theory.

**CHECK 6 — RUNG-X (fixed-set seam rungs, growing-neck parities).**
Instances launched: lin/B t = 9 (seam I_9 ∪ I_11, n = 1282, fixed set
{1, 3, 4, 8}, 11 units), gm/B t = 9 (plateau neck 32, fixed 20-attacker
set x ≤ 31, 137 units, n = 1280), frac/B t = 9 (n = 1481, 52 units).
Solvers still IN FLIGHT at session close (budget 5400 s each; results
land in data/s2_rungx_{linB,gmB,fracB}.json + .log and
s2_sg_rungs.jsonl when done).  The unit-density arithmetic already
separates the cases: lin/frac seam units grow like n_{t+1}/2 = Θ(t)
against windows of size Θ(2^t) — vanishing density, so small-scale SAT
(inconclusive) is the expected verdict, and death for lin/frac would
have to couple consecutive seams (that composite IS the §3 sliver
orbit, closed by T-SHARP) or find a richer core; gm's plateau seams
carry a FIXED cohort of ~M_{k−1} attackers with Θ(s) units — the one
seam family with OG-like density, and the best UNSAT candidate.

**Verdict of the rungs.**  The fixed-attacker pigeonhole is alive and
scale-robust exactly where the NECK lemma predicts: pair cores survive
arbitrary truncation (CHECK 4), bounded-neck interval rungs fire at
every scale tested (CHECK 5), and the escapes that would void a
varying-attacker argument (single-SAT, sacrifice, C3-migration) are
all machine-real (CHECK 4/4b/7) — death must ride FIXED pairs, and
does, wherever the per-scale core is rich enough.

## 6. What is provable now — the honest map

- **Provable, unconditional:**  L-STEP, L-DESC, L-PROC (one-paragraph
  proofs above; finite shadows machine-checked).  T-SHARP: the orbit
  mechanism cannot be extended by any growth hypothesis — lem:orbit is
  exactly sharp at |F| < ∞.  SLIVER-ORBIT: the exact schedule
  inequality; geo/A and gm are orbit-free, lin and frac carry slow
  orbits on both teams (which by T-SHARP proves nothing by itself).
  Lemma NECK: every schedule leaves some team fixed-pair-attacked at
  infinitely many scales — the attack surface conserved in exact form.
  T-PIN: fixed-pair rungs at infinitely many scales ⇒ death (the
  thm:ogred pigeonhole, verbatim).
- **Provable conditionally (rungs → death):**  via T-PIN — geo is dead
  modulo the RUNG-IN family (machine-UNSAT at r = 7/9/11, fixed pair
  {21, 22}, bounded core on growing windows): the same epistemic shape
  as thm:ogred + thm:c3core before the C3 hand proof.  T-REGRESS
  (varying attackers, position-regress overflow) is also a complete
  conditional proof, but its premise — single-attacker rungs — is
  machine-FALSE at every point tested: the theorem stands, its
  hypothesis does not occur in this family.
- **Not provable (dead ends, certified):**  any "growing orbit ⇒ dead"
  theorem (T-SHARP); any fixed-attacker KEPT-BOTTOM crown argument
  against growing slivers (the attack window empties once 2 s_t ≥ x —
  but the NECK lemma re-aims the same pair at intervals or seams, so
  this closes a proof route, not the mechanism); per-value regress
  T-REGRESS on these schedules (single rungs SAT); transferring
  thm:c3core to truncated windows verbatim (CHECK 4b: its core is SAT
  already at s = 9).
- **Open crux (the next C3):**  a hand schema proving the per-scale
  cores UNSAT at all large scales in their family — RUNG-IN(geo-like
  bounded-neck intervals; machine-true at 3 scales, scale-independent
  unit count) and the pair rungs SG(t, {15, 16}) (machine-true at 12
  schedule-scale points, core unknown since C3 dies under truncation).
  For the growing-neck parities the seam cores (RUNG-X; solvers in
  flight) are the analogous family — their unit density separates gm
  (OG-like, Θ(s) units, plausible rungs) from lin/frac (Θ(log t)-sparse
  seams, plausibly SAT forever: for those two schedules the fixed-pair
  route needs a genuinely richer per-scale core, or a new mechanism).

## Reproduce
    PY=.venv/bin/python; S=experiments/s2_growing_death.py
    $PY $S sharp    # ~1 min   (T-SHARP constructions, CHECK 1)
    $PY $S shadow   # ~1 min   (L-STEP finite shadows, CHECK 2)
    $PY $S orbit    # ~1 min   (SLIVER-ORBIT walks/blocks, CHECK 3)
    $PY $S sg  --sg-sched lin --sg-scales 9,10,11 --budget 3000   # hours
    $PY $S c3  --sg-sched lin --sg-scales 9,10,11                 # ~6 min
    $PY $S rungin --sg-sched geo --team B --pair 21,22 \
        --sg-scales 7,9,11 --budget 5400                          # ~6 min
    $PY $S rungx  --sg-sched gm  --team B --sg-scales 9 \
        --budget 5400                                  # seam gadgets
    $PY $S sac --sg-sched lin --sac-t 9 --sac-ks 64,96,128        # ~1 min
Artifacts: data/s2_sharp.json, s2_orbit.json (with full re-verifiable
walk certificates), s2_shadow.json, s2_sg_rungs.jsonl (every
control/rung row, streaming), s2_sacrifice_t9.json + s2_sac_t9_hi.json,
s2_single_cscan_t9.json, s2_single_t11.json, s2_rungin_geoB.json,
s2_rungin_gmA_jump8.json, s2_rungx_{linB,gmB,fracB}.json, logs
data/s2_*.log.
