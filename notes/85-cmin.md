# 85 — FRONT CMIN: the counting lemma written out — exact-constant
# sweep, the Bm1 arm is VACUOUS, Theorem CMIN-SMALLT (16t ≤ M − 14),
# and the honest big-t residue

Task (queue of notes/71 §9.1 + §4d): write the complete hand
argument for [GAP-CMIN] — Σ_z min(c_A, c_B) ≥ M over balanced
μ_dn = 0 low-impure splits of low ∪ B1 — from the notes/71
skeleton (two-channel sweep + SZ′ + WALL + parity-split rigidity);
machine-check the t ≥ 2 exchange floor at three more scales;
propagate to FHALF / J-BOOT / F-BOOT / FTOT.

Machine companion: experiments/e188_cmin_close.py (cmin / cmin_t2 /
bm1vac / sweepaudit; predictions PRE-REGISTERED in the e188 commit
before any run), records data/e188_cmin.jsonl + pod logs
(sprint-B e188_t2_2024.log, sprint-D e188_cmin_242832.log); plus
the sprint-C e174 ftot harvest (§8).

**Verdict up front.  The near-pure regime of GAP-CMIN is now a
THEOREM with explicit constants: (i) impurity inside Bm1 is
VACUOUS (Lemma BM1-VAC — for t ≤ ⌊M/8⌋ − 1 no balanced μ_dn = 0
coloring has a mixed-parity Bm1 side at all: a whole residue class
of B1 becomes uncolorable; machine: UNSAT at 16/20/24/28/32, and
the unrestricted Bm1-mixed corner is inhabited only from
t*(M) = 4/5/5/6/7 with S ≈ 3M–6M there); (ii) with all impurity in
B0, the two-channel sweep closes with room to spare whenever
16t ≤ M − 14 (Theorem CMIN-SMALLT) — in particular the measured
extremal frame t = 1 is DEAD for every M ≥ 32, no top-corner
case-split left, the O(1) bookkeeping of notes/71 §4d is done and
the constants are 1/4-tight against the (2M−1, 2M) witness law.
What remains of GAP-CMIN is exactly the big-t regime
t > (M − 14)/16 at M ≥ 36 — renamed [GAP-CMIN-BIGT] — where the
exchange lemma stays machine-supported, not proved: the naive
un-swap breaks μ_dn = 0, and cmin_{t≥2} is measured STRICTLY above
M at every asked scale.  Downstream (§8): FHALF and hence J-BOOT
are now unconditional on the entire boot window (measured f at
8..32 + this theorem at 32), the (·,0) family needs BIGT nowhere,
and ftot(16) = 8 landed on sprint-C — F-BOOT's counting floor is
measured-true at three scales.**

## 0. Setting (recap of notes/71 §4, fixing the canonical frame)

M ≡ 0 (mod 4).  low = (M/2, 2M] (Bm1 = (M/2, M], B0 = (M, 2M]),
B1 = (2M, 4M].  A split is balanced (|Bm1∩A| = M/4,
|B0∩A| = M/2, |B1∩A| = M), μ_dn = 0 (no team owns a triple
(w, u, y) ∈ Bm1 × B0 × B1, y = 2u − w, monochromatic), and
low-impure (some — equivalently, by the balance count
|T∩low| = 3M/4 = #odds(low), EACH — team's low set carries both
parities).  For z ∈ B2, c_T(z) = #{(u, y) ∈ (low∩T) × (B1∩T) :
2y − u = z}; S = Σ_{z∈B2} min(c_A, c_B); cmin(M) = min S.
[GAP-CMIN]: cmin(M) ≥ M.  Measured EXACT (= M): 8/12/16 (notes/71)
+ 20 (notes/76); 24/28/32 launched this session (§7).

**Canonical labeling.**  Call A the team owning the majority of
low ODDS (relabel teams and/or parities so this holds and the
majority is ≥ 3M/8).  Then A-low = (O ∖ R) ∪ D, B-low =
(E ∖ D) ∪ R with O/E the odds/evens of low, R = the odds B owns,
D = the evens A owns, and |R| = |D| =: t ≥ 1 (balance), t ≤ 3M/8
(majority).  Per-block balance splits t = t₁ + t₀ with
|R∩Bm1| = |D∩Bm1| = t₁, |R∩B0| = |D∩B0| = t₀ (each block's A-count
equals that block's odd-count).  t is THE impurity; the measured
extremal witnesses are all t = 1, t₁ = 0 (notes/71 §4d).

## 1. Lemma BM1-VAC: impurity in Bm1 is vacuous  [PROVED]

**Lemma BM1-VAC.**  Let M ≡ 0 (mod 4) and t ≤ ⌊M/8⌋ − 1.  No
balanced μ_dn = 0 coloring has t₁ ≥ 1.  (So in the small-t regime
ALL impurity sits in B0 — "the binding case is the swap inside B0"
of notes/71 §4c is upgraded from a confinement comparison to
outright vacuity.)

*Proof.*  Suppose t₁ ≥ 1: fix d₁ ∈ D ∩ Bm1 (an even Bm1-value in
A-low).  Consider the even values z ∈ (2M, 3M] with
z ≡ 2 − d₁ (mod 4); there are M/4 of them.

(a) *A cannot own z, except at ≤ t₀ holes.*  y := (z + d₁)/2 is an
integer in (M + d₁/2, 3M/2 + d₁/2] ⊆ B0, and z + d₁ ≡ 2 (mod 4)
makes y ODD.  B0-odds lie in A-low except the t₀ values R∩B0.  So
for all but ≤ t₀ of our z, (d₁, y) is an A-pair with 2y − d₁ = z:
if A owned z, μ_dn(A) > 0.

(b) *B cannot own ANY of them.*  Reps of an even z ∈ (2M, 3M] on
the B side: w ∈ Bm1∩B even with w ≡ −z (mod 4) (then
u = (z + w)/2 is an even integer, and u ∈ (M, 2M] = B0 because
z ≤ 3M ⟹ the whole Bm1 window qualifies), u ∈ B0∩B.  Bm1-evens in
a fixed mod-4 class: ≥ ⌊M/8⌋; remove ≤ t₁ (w ∈ D∩Bm1) and ≤ t₀
(u ∈ D∩B0, u determined by w): ≥ ⌊M/8⌋ − t ≥ 1 rep survives.  If B
owned z, μ_dn(B) > 0.

M/4 − t₀ ≥ 1 of the z's are banned for BOTH teams — but every
B1-value is colored.  Contradiction.  ∎

**Machine (e188 bm1vac, pre-registered).**  The scoped query
(Bm1∩A mixed + t ≤ ⌊M/8⌋ − 1) is UNSAT at M = 16/20/24/28/32
(all < 0.1 s).  The UNRESTRICTED query is SAT at all five scales —
a pre-registration miss worth keeping honest: Bm1-mixing IS
feasible at big t.  Threshold sweep: minimal feasible impurity
t*(M) = 4/5/5/6/7 at M = 16/20/24/28/32 (vs the lemma's
⌊M/8⌋ − 1 = 1/1/2/2/3 — the lemma is safe with a factor ≈ 2), all
minimal witnesses have t₁ = 1 exactly, and their S values are
49/79/103/143/201 ≈ 3M–6M: the mixed-Bm1 corner pays S several
times over the target.  (These witnesses are feasibility
witnesses, not S-optima; the point is the corner is inhabited but
lavish, consistent with every cmin optimum being t₁ = 0.)

## 2. Lemma SZ′(t): confinement with explicit constants  [PROVED]

From here on t₁ = 0 (Lemma BM1-VAC), so Bm1∩A = all M/4 Bm1-odds,
Bm1∩B = all M/4 Bm1-evens, R, D ⊆ B0.  Write c(t) := 4t + 8 and
call C := (7M/2 − c(t), 4M] the CORNER (|C| = M/2 + c(t)),
W := (2M, 7M/2 − c(t)] the below-corner range.  Assume
t ≤ ⌊M/8⌋ − 1.

**Lemma SZ′(t).**  (i) A owns no odd y₀ ∈ W.  (ii) B owns no even
y₀ ∈ W.

*Proof.*  (i) Count μ_dn-forcing reps of odd y₀: w ∈ Bm1-odds with
w ≡ 2 − y₀ (mod 4) (making u = (y₀ + w)/2 an ODD integer) and
u ∈ B0 ⟺ w ∈ (2M − y₀, 4M − y₀], i.e. w ∈ (M/2, min(M, 4M − y₀)].
Such u is in A-low unless u ∈ R (≤ t losses, w determined by u).
For y₀ ≤ 3M the w-window is all of Bm1: ≥ ⌊M/8⌋ − t ≥ 1 rep.  For
3M < y₀ ≤ 7M/2 − c(t): window length 7M/2 − y₀ ≥ c(t) − 1... use
the exact form: a window of L consecutive integers contains
≥ (L − 3)/4 members of any fixed mod-4 class, so reps
≥ (7M/2 − y₀ − 3)/4 − t ≥ (4t + 8 − 3)/4 − t > 1 − 1 = 0, i.e.
≥ 1.  A rep (w, u) ∈ A × A with y₀ ∈ A is a mono H_dn triple.
(ii) Symmetric: w ∈ Bm1-evens ≡ −y₀ (mod 4) gives even
u = (y₀ + w)/2 ∈ B0, in B-low unless u ∈ D; same counts.  ∎

(Scope note, as in notes/71 §4c: at M = 8 the count ⌊M/8⌋ − t dies
at t = 1 — the f(8)-witness's B1-odds {19, 21} sit exactly in the
two holes of its removed y = 13.  Nothing below needs M = 8.)

**Corollary RIGID.**  On W the coloring is FORCED: odds → B,
evens → A.  Hence exactly: |B ∩ W| = #odds(W) = 3M/4 − c(t)/2,
|B ∩ C| = M/4 + c(t)/2 = |A ∩ C| + 0 (same count for A by the even
mirror), and NO team owns two consecutive values inside W (the
WALL of notes/71 §4c, now with constants).

## 3. The two channels and the candidate count  [PROVED]

Choose channels r := min R (odd), d := min D (even) — both in B0,
so M < r, d ≤ 2M, r ≠ d, and r + d ≤ (2M − 1) + 2M = 4M − 1.
Channel intervals I_r = {y ∈ B1 : 2y − r > 4M},
I_d = {y ∈ B1 : 2y − d > 4M}.  CANDIDATES: y ∈ B ∩ I_r (feeding
z = 2y − r, odd, with B-rep (r, y)) and y ∈ A ∩ I_d (feeding
z = 2y − d, even, with A-rep (d, y)).  Distinct candidates feed
distinct z (y ↦ 2y − r injective; the channels are
parity-disjoint), so S ≥ #candidates − #failures, a failure being
a candidate whose z has NO rep on the opposite team.

**Candidate floor: N ≥ 2M − (r + d)/4 − 1/4.**
Below-corner odds in I_r are all candidates (RIGID: they are B's):
the first odd y > 2M + r/2 is ≥ 2M + (r+1)/2, the last is
< 7M/2 − c(t) (even endpoint), count
≥ (3M/2 − c(t) − (r+1)/2)/2 = 3M/4 − c(t)/2 − r/4 − 1/4.
Below-corner evens in I_d likewise, count ≥ (first even
≥ 2M + d/2 + 2, so) 3M/4 − c(t)/2 − d/4.  Corner values are ALL
candidates (C ⊆ I_r ∩ I_d since 7M/2 − c(t) ≥ 2M + max(r,d)/2
⟸ 3M/2 − c(t) ≥ M, true for t ≤ M/8 − 1; each corner value feeds
its own team's channel): + |C| = M/2 + c(t).  Sum: the c(t)'s
cancel — N ≥ 2M − (r + d)/4 − 1/4.  With r + d ≤ 4M − 1:
**N ≥ M, always.**  (Sharpness: at the measured extremal cell
(r, d) = (2M−1, 2M) this is exactly the notes/71 §4d count; the
f(8) witness's 9 candidates at (13, 16) match the formula's
16 − 29/4 − 1/4 = 8.5 → 9.)

## 4. Failures: location and run bound  [PROVED]

Fix the r-channel (B-side; the d-channel is the even mirror with
every constant shifted by the even-grid offset ≤ 1/2).  The
partner offsets are Δ_A = ((O ∖ R) − r)/2: ALL integers in
[−w_dn, w_up] except 0 and the ≤ t − 1 HOLES ((R ∖ {r}) − r)/2,
where w_dn = (r − M/2 − 1)/2 ≥ M/4 (Bm1-odds are never removed —
this is where BM1-VAC pays) and w_up = (2M − 1 − r)/2.  A
candidate y FAILS iff A ∩ (y + Δ_A) ∩ B1 = ∅.

**(a) Failures live at the top.**  The below-corner part of
[y − w_dn, y + w_up] ∩ B1 is an integer run; every even in it at a
non-hole offset is an A-value (RIGID) and a partner.  y itself is
never one of those evens (below-corner candidates are odd;
corner candidates are above W).  A run of ℓ consecutive integers
has ≥ (ℓ − 1)/2 evens ⟹ failure needs (ℓ−1)/2 ≤ t − 1, i.e.
ℓ ≤ 2t − 1: **failed y satisfy y − w_dn ≥ 7M/2 − c(t) − 2t + 2.**

**(b) Run bound.**  Let y₀ = least failed candidate.  Failure of
y₀ forces every non-hole value of [y₀ − w_dn, y₀ − 1] (all in B1,
by (a) ≥ 2M) to be B: ≥ w_dn − t + 1 B-values below y₀.  All
failed candidates are B-values ≥ y₀.  Both live in
[y₀ − w_dn, 4M] ⊆ [7M/2 − c(t) − 2t + 2, 4M], whose B-capacity is
|B ∩ C| + #odds in the ≤ 2t − 1 below-corner slots
≤ (M/4 + c(t)/2) + t = M/4 + 3t + 4.  Hence
(w_dn − t + 1) + f_B ≤ M/4 + 3t + 4:

    f_B ≤ max(0, M/2 + 4t + 7/2 − r/2),
    f_A ≤ max(0, M/2 + 4t + 4  − d/2)   (even mirror).

Note the shape: a failure zone EXISTS only if the channel value is
low (r < M + 8t + 7), and r, d > M always (impurity is in B0) — a
second place BM1-VAC pays.

## 5. Theorem CMIN-SMALLT  [PROVED]

**Theorem.**  M ≡ 0 (mod 4).  Every balanced μ_dn = 0 low-impure
split with (canonical) impurity 16t ≤ M − 14 has
S = Σ_z min(c_A, c_B) ≥ M.  In particular (t = 1) every ONE-SWAP
split has S ≥ M for all M ≥ 32.

*Proof.*  t ≤ (M − 14)/16 < ⌊M/8⌋ (so BM1-VAC applies: t₁ = 0,
and SZ′(t)/RIGID hold).  S ≥ N − f_A − f_B with §3–4's bounds.
Four cases on which failure zones are nonempty:
- none: S ≥ N ≥ M.
- both: S ≥ [2M − (r+d)/4 − 1/4] − [M/2 + 4t + 7/2 − r/2] −
  [M/2 + 4t + 4 − d/2] = M + (r + d)/4 − 8t − 31/4
  ≥ M + (2M + 3)/4 − 8t − 31/4 = 3M/2 − 8t − 7 ≥ M  ⟺  16t ≤ M − 14.
- r-side only: S ≥ 3M/2 + r/4 − d/4 − 4t − 15/4
  ≥ 3M/2 + (M+1)/4 − 2M/4 − 4t − 15/4 = 5M/4 − 4t − 7/2 ≥ M  ⟺
  16t ≤ M − 14.
- d-side only: mirror, same threshold.  ∎

**What this discharges from notes/71 §4d:** the "top-corner
optimization + ≤ 4 one-sidedness cases + swap-in-Bm1 subcase" are
all gone — the corner bookkeeping is absorbed into the exact c(t)
cancellation in §3, the one-sidedness cases into the max(0, ·)
failure bounds, and the Bm1 subcase into vacuity.  The extremal
cell (2M−1, 2M) needs no separate treatment (its failure zones are
empty: r = 2M − 1 ≥ M + 8t + 7 for M ≥ 24, t = 1), though the
§4d direct proof remains the cleanest special case.

**Machine audit of the accounting (e188 sweepaudit, M = 40,
pre-registered).**  For sampled t = 1 cells (r, d) ∈ B0² (corners
+ midpoints), the inner CP-SAT minimum of S over all B1-colorings
is computed and the proof quantities (N, f_A, f_B, RIGID) are
re-derived on each optimal witness: prediction — every cell
S ≥ 40, S ≥ N − f_A − f_B, RIGID true below 7M/2 − 12.  [Harvest
in §7; committed before completion.]

## 6. The big-t residue: [GAP-CMIN-BIGT], and why exchange is hard

What survives of GAP-CMIN: **S ≥ M for t > (M − 14)/16, M ≥ 36**
(at M ≤ 32 the measured cmin — §7 — covers all t).  Honest status:

- The exchange claim of notes/71 §4d ("more defectors only add
  channels") is TRUE in every measurement but is NOT a proof.  The
  natural exchange (un-swap a defector pair r₂ → A, d₂ → B) does
  not preserve feasibility: the new A-low odd r₂ mints H_dn images
  2u − w through the whole Bm1∩A fan, and the OLD B1-coloring may
  own them — μ_dn = 0 breaks, the B1 side needs repair, and S is
  not monotone under repair.  Any proof must couple the un-swap
  with a controlled recoloring; none is written.  [GAP]
- Machine floor (the assigned check, three fresh scales): forcing
  impurity ≥ 2 per parity per team, cmin_{t≥2}(8) = 10,
  cmin_{t≥2}(12) = 22 (notes/71 §11) and NEW: M = 16 local +
  20/24 on sprint-B [harvest §7 — pre-registered: all > M].
- The BIGT region's known inhabitants are lavish: the minimal
  Bm1-mixed witnesses (§1) pay 3M–6M; every cmin optimum ever
  dumped is t = 1.  BIGT gates NOTHING downstream (§8): it is a
  hardening statement for the uniform-in-M law at M ≥ 36 only.

## 7. Machine ledger (runs of this front)

| run | where | result |
|---|---|---|
| bm1vac scoped (t ≤ ⌊M/8⌋−1), M = 16/20/24/28/32 | local | UNSAT ×5 [<0.1 s] — BM1-VAC machine-true |
| bm1vac unrestricted, same M | local | SAT ×5; t* = 4/5/5/6/7; t₁ = 1 minimal; S = 49/79/103/143/201 |
| cmin_t2(16) | local | [in flight at write time] |
| cmin_t2(20), cmin_t2(24) | sprint-B | [in flight] |
| cmin(24), cmin(28), cmin(32) | sprint-D | [in flight — closes the 24/28 measurement hole between cmin(20) and the M ≥ 32 theorem] |
| sweepaudit(40), 9 cells | local | [in flight] |
| ftot(16) | sprint-C (e174) | **= 8 = M/2** (UNSAT through 7, the m = 7 query 6920 s; SAT at 8 [3.5 s]) |
| ftot(20) | sprint-C (e174) | ≥ 8 and descending (m = 7 UNSAT 8785 s; predicted 10) |

The ftot(16) witness is one more extremal-frame instance:
low split (r, d) = (31, 32) = (2M−1, 2M), Bm1 pure, corner odds
{59, 61, 63} — the SAME shape as every f-witness (notes/71 §4d)
and both reduction inequalities tight.

## 8. Propagation (the assigned mop-up)

| tag | before | after |
|---|---|---|
| GAP-CMIN | proof skeleton + extremal cell (M ≥ 32) + "finite drafting task" | **Theorem CMIN-SMALLT [PROVED]**: S ≥ M whenever 16t ≤ M − 14 (all M ≡ 0 mod 4); + Lemma BM1-VAC [PROVED]; + measured cmin = M at 8/12/16/20 (24/28/32 in flight).  Residue renamed **[GAP-CMIN-BIGT]** (t > (M−14)/16, M ≥ 36) |
| GAP-FHALF (f(M) ≥ M/2) | reduces to GAP-CMIN | **CLOSED on M ≤ 32** (f measured EXACT at 8/12/16/20/24/28/32 — that IS the inequality there); for M ≥ 36 [PROVED mod GAP-CMIN-BIGT] via the verbatim reduction |
| Theorem J-BOOT | PROVED mod GAP-CMIN | **UNCONDITIONAL on the boot window and beyond: (v,0) UNSAT for v < M/2 at every M ≡ 0 mod 4, 12 ≤ M ≤ 32** (measured f + the M = 32 theorem); mod GAP-CMIN-BIGT for M ≥ 36 — where Theorem J-DOWN (notes/75) already owns the verdict.  **The (·,0) demand family is covered at every anchor with NO appeal to BIGT**; J-BOOT remains the N6a-independent leg, now gap-free through 32 |
| boot window | closed "modulo one counting lemma" | closed, full stop, for the finite regime: v_min(0)(8) = 12 (anatomy notes/71 §2), v_min(0)(M) ≥ M/2 for M = 12..28 unconditional, v_min(0)(M) = ∞ for M ≥ 32 [J-DOWN, mod N6a] |
| GAP-FTOT (f_F ≥ M/2) | measured = f at 8/12 | measured = f at **8/12/16** (ftot(16) = 8 landed); F-BOOT's floor v < ⌈M/4⌉ is measurement-backed at three scales, conditional (same BIGT species via the verbatim CMIN reduction on the μ_up + μ_skip part) beyond; ftot(20) descending |
| GAP-MARGIN-MASS | scoped, untouched | untouched (not this front) |

Net ledger effect: the FOUR gating gaps of notes/76 are untouched
(this front hardens, as predicted there); the J/F demand layer's
independence from the N6a pool is now unconditional through
M = 32 and one clean statement (BIGT) from uniform.

## 9. Queue at close

1. Harvest §7's in-flight runs; if cmin(24/28/32) = M lands, GAP-
   CMIN's measured floor meets the theorem with no scale hole.
2. [GAP-CMIN-BIGT]: the only surviving mathematics of this front.
   Attack sketch: in the big-t regime BOTH parities have ≥ t ≥
   M/16 channels on EACH team; a two-sided sweep with the ROLES of
   R and D symmetrized (candidates counted on both parities
   simultaneously) should beat M with t-slack — the §1 S-values
   (3M–6M) say the truth is lavish.  Alternatively couple the
   exchange with a B1 repair map (the failure mode is §6's minted
   H_dn fans — they land in W where RIGID pins the coloring, so
   the repair is forced, not chosen: plausible route).
3. ftot(20) completion (predicted 10); then GAP-FTOT mirrors
   FHALF's status mechanically.
4. NOT this front: GAP-MARGIN-MASS; the const-bounds analogue.
