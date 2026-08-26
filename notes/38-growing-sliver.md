# G3: growing-sliver swap — the last surviving shape (TASK S1)

## Question
After H1-H3 the only untested YES-shape was the growing-sliver swap
(STATUS.md "General case"): ratio-2 blocks (2^{t-1}, 2^t] alternate teams
(A even t, B odd t, 1 -> B); each team donates the bottom s_t values of
each of its own blocks to the partner, with s_t -> infinity. Growth
provably defeats the two mechanisms that killed the fixed-depth family
(notes/35): fixed-attacker crowns lose their kept-bottom attacks, and the
period-2 orbit reflectors outgrow every finite set, voiding lem:orbit.
The untested death routes were (a) slowly-growing reflector sets and
(b) scale-adapted attacker families. TASK S1: build the family, screen
schedules {s_t = t, 2^{floor(t/2)}, floor(2^t/t), Geneson-stage-matched}
x {natural crowns, forced-alternating/split crowns} on both teams at
horizons 2^12 / 2^15 / 2^18.

**Answer: no survivors. The portable-crown (fixed-attacker) death
signature fires on at least one team of every candidate, and a two-line
conservation law — the d_t law below — shows this is forced for EVERY
schedule in this geometry, not just the four tested. Growth is a
zero-sum dial: the same quantity d_t = 2 s_t − s_{t+1} that starves the
owner's fixed attackers arms the receiver's.**

## The d_t law (the theory result of this session)

Write d_t := 2 s_t − s_{t+1}. Fix an attacker x (any in-team value; an
attack at octave t is a triple x < 2^{t-1} < y with y, z = 2y − x in the
same team as x). For large t the only channels by which a FIXED x can
attack are sliver-mediated, and they are governed by d_t:

- **Kept-bottom channel** (hurts the block OWNER X at its own-parity t):
  y = 2^{t-1} + o with o just above s_t, completion z = 2^t + (2o − x)
  lands in X's *received* sliver of octave t+1 iff 1 ≤ 2o − x ≤ s_{t+1}.
  Minimising over o > s_t: **x attacks iff x ≥ d_t + 2** (±1 parity).
- **Sliver-top channel** (hurts the RECEIVER Y at partner-parity t):
  y = 2^{t-1} + o with o ≤ s_t in Y's received sliver, completion
  z = 2^t + (2o − x) lands in Y's *kept body* of octave t+1 iff
  2o − x ≥ s_{t+1} + 1. Maximising over o ≤ s_t: **x attacks iff
  x ≤ d_t − 1**.

(All other completions from these surfaces land out-of-team or require
x growing with t; the adaptive scan below verifies the two inequalities
are exact, up to a scale-adapted boundary family x ≈ 2^{t-1} − s_t
attacking within the sliver — bounded description, not fixed-x.)

**Law.** On each octave-parity class, the owner escapes fixed
kept-bottom attackers iff d_t → ∞ along the class; the receiver escapes
fixed sliver-top attackers iff d_t ≤ x_0 eventually (x_0 = its smallest
attacker, ≤ 3 for any team containing a value ≤ 3). Both conditions
cannot hold on the same class. **Hence in every growing-sliver swap
partition, at least one team has a fixed attacker whose attacks recur at
infinitely many scales — the portable-crown death pattern (notes/37,
thm:ogred pigeonhole) that killed S_A.** Crown-pair OWNERSHIP is
irrelevant to these killers: they are generic small in-team values, so
splitting or alternating the pairs {2^j−1, 2^j} (trichotomy escape (1))
cannot rescue anyone — and the screen shows splitting is in fact
actively harmful (planted halves are landing pads; see the results
section).

The tested schedules realise the three corners of the law:
- s_t = t: d_t = t − 1 → ∞ on BOTH classes — both receivers die
  (x = 1, 2, 3, 5 … attack every partner-parity octave; e.g. team B's
  x = 1 attacks (1, 12, 23), (1, 37, 73), … at every even octave).
- s_t = 2^{floor(t/2)}: d_t = 2^{t/2} → ∞ on even t, d_t ≡ 0 on odd t —
  the extreme split. Team A (owner of even, receiver of odd) is protected
  on BOTH surfaces and (in the natural-crown variant) comes out **fully
  clean — the first structurally clean team of an exact partition in the
  whole campaign** (upper density
  2/3 at even horizons, matching Geneson's record; its received slivers
  are one-way: max landing 2 s_t − 1 = s_{t+1} − 1 falls exactly 2 short
  of its kept bodies). But the same two choices doubly kill team B: every
  fixed x_B ≥ 1 attacks B's received slivers (even t) AND every
  x_B ≥ 2 its kept bottoms (odd t, d = 0). One team can be saved, never
  both.
- s_t = floor(2^t/t): d_t ≈ 2^{t+1}/t² → ∞ on both classes — both
  receivers die, as in lin.
- Geneson-stage-matched (s = M_{k-1}: 1, 32, 4096 on octaves 1-5, 6-12,
  13-21): plateaus give constant d = M_{k-1} (receiver dies while the
  plateau lasts), stage jumps give d < 0 (owner's kept bottom open to ALL
  x); both teams flagged. Geneson's real construction survives because
  its removed slivers are silent zones owned by NOBODY — in a partition
  the receiver must hold them, and holding them is what kills it.

## Why growth really does void the OLD death theorems (both arms checked)
- lem:orbit (finite F): the infinite rays that exist here need reflectors
  f ≈ d_t → ∞, outside every finite reflector set. The finite-F ORBIT
  flag at 2^18 is a horizon artifact for lin (reflectors d_t = t − 1
  ≤ 64 suffice up to 2^18 but not asymptotically); on geo, nearfull and
  genstage the finite-F instrument is already quiet at 2^18. The new
  RAY-GROW instrument (exact FFT octave-reachability with cap
  4 s_t + 64) shows censored rays spanning 14-16 octaves with
  machine-verified witness
  chains, e.g. lin/B: 8 → 12 → 23 → 38 → 72 → 135 → 266 → … reflectors
  {4, 1, 8, 4, 9, …} growing ~ d_t. So the growing-sliver family sits
  exactly in the lem:orbit gap (slowly-growing F) — a YES-proof for any
  such team would need to refute these concrete growing-reflector rays,
  and a NO-program gets a target: **lem:orbit-grow, allowing f_m = o(u_m)
  or f_m ≤ C s_{oct(u_m)}, would convert the RAY-GROW signal into a
  second unconditional death for all four schedules.**
- Fixed-attacker crowns: kept-bottom attacks by fixed x indeed die out
  whenever d_t → ∞ (verified: adaptive scan shows x_min = d_t + 2
  exactly at every kept-bottom octave). The direction in the task memo
  ("x ≤ 2 s_t") resolves as: the kept bottom is protected, but the
  attack surface is CONSERVED, not destroyed — it reappears as the
  partner's sliver-top exposure x ≤ d_t − 1.

## Screens (experiments/g3_growing_sliver.py)
Per team at H = 2^12, 2^15, 2^18:
1. **Pure-complete SAT**: ABJ bit-reversal witness, independently
   verified (fully at 2^12/2^15; 2046 sampled gaps at 2^18) + Cadical195
   lazy-transitivity cross-check at 2^12 with ABJ phase hint. All 48
   team-horizons SAT, as the ABJ soundness ceiling demands — death
   evidence is structural, never finite-window UNSAT.
2. **ORBIT** (finite F, lem:orbit proper): g2 orbit scan, fmax 64.
3. **RAY-GROW** (new): exact reachability of rays u → 2u − f, f in-team,
   f ≤ 4 s_t + 64 (growing cap), per start octave, by boolean sumset
   convolution; witness chains reconstructed and re-verified. Calibrated:
   S_A span 0; Z+ full-span censored (flag); h2 bottom8/A rediscovers the
   proven infinite orbit (flag).
4. **CROWN** scans: g2 recurrence-ratio (x ≤ 64); h2 persistence scan at
   top_gap 1 AND 2 (donation pushes completions one octave up, so a
   receiving surface's last attackable y-octave is top−2; calibration
   preserved: S_A flagged, Geneson clean at both gaps); NEW adaptive
   surface scan: exact attacker sets against the kept-bottom and
   sliver-top windows per octave, checked against the d_t predictions,
   ADAPT flag if a surface is attackable at ≥ 80% of large octaves.
5. **SLIVER** load (g2, width 8): structurally blind here (received
   slivers fall below the 0.25 occupancy threshold at large t) — kept
   for continuity, clean everywhere as expected.

Partition property (disjoint + covering) machine-verified at N and at
every horizon; generator calibrated: s ≡ 0 reproduces S_A | S_B exactly,
s ≡ 8 reproduces h2's dyadic_bottom8 exactly.

## Results (flags at the top horizon 2^18; full per-horizon data in
data/g3_<name>.json, verdicts in data/g3_summary.json)

| schedule | crowns | team A (death / signals) | team B (death / signals) | SAT | verdict |
|---|---|---|---|---|---|
| s_t = t | natural | **CROWN CROWNP ORBIT** / ADAPT-kb ADAPT-rt RAY-GROW | **CROWN CROWNP ORBIT** / ADAPT-kb ADAPT-rt RAY-GROW | all SAT | DEAD |
| s_t = t | alt-split | **CROWN CROWNP ORBIT** / ADAPT-kb ADAPT-rt RAY-GROW | **CROWN CROWNP ORBIT** / ADAPT-kb ADAPT-rt RAY-GROW | all SAT | DEAD |
| s_t = 2^{floor(t/2)} | natural | **clean** / ADAPT-kb | **CROWN CROWNP** / ADAPT-kb ADAPT-rt RAY-GROW | all SAT | DEAD (via B) |
| s_t = 2^{floor(t/2)} | alt-split | **CROWNP** / ADAPT-kb ADAPT-rt | **CROWN CROWNP** / ADAPT-kb ADAPT-rt RAY-GROW | all SAT | DEAD |
| s_t = floor(2^t/t) | natural | **CROWNP** / ADAPT-kb ADAPT-rt RAY-GROW | **CROWNP** / ADAPT-kb ADAPT-rt RAY-GROW | all SAT | DEAD |
| s_t = floor(2^t/t) | alt-split | **CROWNP** / ADAPT-kb ADAPT-rt RAY-GROW | **CROWN CROWNP** / ADAPT-kb ADAPT-rt RAY-GROW | all SAT | DEAD |
| Geneson-stage | natural | **CROWNP** / ADAPT-kb ADAPT-rt RAY-GROW | **CROWNP** / ADAPT-kb ADAPT-rt | all SAT | DEAD |
| Geneson-stage | alt-split | **CROWNP** / ADAPT-kb ADAPT-rt RAY-GROW | **CROWN CROWNP** / ADAPT-kb ADAPT-rt | all SAT | DEAD |

(kb = kept-bottom, rt = recv-top; flags at 2^18.  CROWNP fires on 15 of
the 16 teams — the single exception is geo_nat/A, fully clean.  ORBIT
(finite-F) fires only on lin, whose reflectors d_t = t − 1 still fit
under fmax = 64 at 2^18 — a horizon artifact, resolved by RAY-GROW; on
geo/nearfull/genstage the finite-F instrument is already quiet at 2^18
while the growing-cap ray persists, e.g. geo/B: fixed-cap ray dies at
octave 17, cap-4s_t ray censored at 18 with verified reflectors up to
513 ≈ 2 s_t.  genstage/B's ray dies at the t = 12 stage jump, where
d_12 = −4032 < 2 closes the recv→kept hop — the plateau structure
breaks rays but hands every plateau to the receiver's fixed attackers
instead, d_t law again.)

### Crown splitting is not free — it is actively harmful
lin: nat and alt flags identical (the d_t killers never mention crown
pairs).  geo: the alt variant KILLS the otherwise-clean team A.  The
planted half 2^j−1 (moved into A because 2^j sits atop B's block at odd
j) is a portable landing pad at the top of the partner's octave:
geo_alt/A dies of exactly the family (x, 2^j−1, 2^{j+1}−2−x) — machine
examples (2, 31, 60), (2, 127, 252), (2, 511, 1020) — and the planted
values also serve as *completions*, e.g. (3, 17, 31), (5, 66, 127).
So trichotomy escape (1), free in the finite coloring theory, has a
strictly positive price in an exact partition: the moved value must
live somewhere, and where it lives it is attackable.

## Where this leaves the program
1. **The sliver-swap idea is now exhausted at ALL depths, fixed or
   growing**: notes/35 closed fixed depths; the d_t law closes growing
   ones. Conservation of attack surface holds across the whole family:
   bottom slivers are a hot potato — whoever holds them at scale t is
   attackable at scale t+1, and growth only chooses the victim.
2. **The geo_nat/A team is the new object of interest**: a partition team,
   density-2/3-at-peaks, no fixed attacker, no ray, clean at 2^18. Its
   partner is unfixable INSIDE this geometry — the natural H5 question
   is whether ANY set can partner it (its complement is forced to hold
   every donated sliver plus the odd kept bodies), or whether the
   portable-crown + d_t argument extends to every complement of a clean
   team. If yes-shape partitions exist at all, they now must break
   octave alternation itself (non-periodic ownership, e.g.
   stage-alternating à la Geneson with growing stages — where the d_t
   law's parity classes no longer alternate teams).
3. **NO-program targets sharpened**: (a) lem:orbit-grow (reflectors
   f ≤ C s_t) — would make RAY-GROW a certificate and kill this family
   twice over; (b) formalise the d_t law + portable crown per attacker
   into "no octave-alternating block partition with ANY donation
   schedule is a YES" — the first infinite CLASS death beyond S_A.

## Reproduce
    .venv/bin/python experiments/g3_growing_sliver.py          # ~40 min
    .venv/bin/python experiments/g3_growing_sliver.py --quick  # no CDCL
Artifacts: data/g3_run.log, data/g3_summary.json,
data/g3_{lin,geo,nearfull,genstage}_{nat,alt}.json.
