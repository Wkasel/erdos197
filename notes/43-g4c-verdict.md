# G4c: adversarial re-verification, shape-coverage audit, and the NO program

## Question (TASK G4c)

Independently re-verify the G4b death certificates (fresh oracle, exact
walks, different solver); if survivors: escalate; if all dead: assess
whether Lemma NECK + T-PIN-STAGE + the seam law cover ALL partition
shapes, enumerate honestly what a complete NO proof still needs, and
write the NO program as a numbered lemma list.

Context: the parallel G4a screen session left no artifacts (no notes/41,
no g4a data files); G4b (notes/42) is the only G4 input.  G4c therefore
re-verified the ENTIRE G4b certificate set from scratch and, since the
fresh methods turned out strictly stronger than the originals
(complete encodings, no CEGAR), escalated scale on its own.

**Verdict: every G4b death certificate re-verifies — 24/24 catalogue
rows, 75+ solver verdicts, exact walks, instance identity, zero
mismatches anywhere — and the rungs extend to M = 1024 (windows to
4096).  No survivors.  The stage-alternating family stays dead; all
block-granular geometry is dead modulo the generic-pair rung schema;
the NO program below has exactly three open lemmas.**

## 1. What was re-verified and how (experiments/g4c_verify.py)

Independence discipline: membership oracle and channel classifier
REWRITTEN from the notes/42 definitions (no shared code with
g4b_seam_law.py); SAT instances rebuilt from the mathematical
definitions; solver = Glucose42 (campaign used Cadical195); for every
n <= 300 the encoding is COMPLETE — AP clauses + units + full
2*C(n,3) transitivity, no CEGAR loop, so UNSAT needs no soundness
argument at all; larger instances use a freshly written lazy loop
(numpy triangle detection, batch clause addition — UNSAT-sound since
only order-axiom consequences are ever added); every SAT verdict is
re-checked on an explicit witness by an independent O(n^2) scanner.

- **PART A — seam law, fresh oracle (24/24 rows OK).**  All nine
  stage-alternating variants rebuilt from scratch; brute enumeration of
  in-team triples (x <= 24) at every recorded seam (m = 32..4096)
  reproduces every recorded per-channel count EXACTLY (incl. the
  seam-1 spillover keys C2@1, SLIVIN@1, the halfBT zero-DUST row, and
  the tri_none C0-only rows).  Exact big-int walks: X2 stays closed and
  the stage neck 2*lo - hi diverges to -infinity for ALL k <= 300 on
  both tri and quad schedules (values ~2^45000), and the FAN completion
  arithmetic holds at seam 2^20102 for x up to 10^6.  The seam law is
  not a small-scale artifact.
- **PART B — small battery, complete encoding (44/44 OK).**  C3
  puncture robustness (M = 64/128, all four puncture states UNSAT,
  4-mod-8 control SAT); OG_5 {31,32} UNSAT (M = 64/128); single-block
  pairs incl. the full M = 128 threshold map ({7,8}, {9,13} SAT;
  {11,12}, {13,14}, {15,17}, {17,18}, {41,42} UNSAT); STG M = 64 —
  singles SAT, ALL seven pairs UNSAT, all five puncture patterns
  UNSAT; chain M = 128 {65,66} UNSAT; 3-block singles SAT.
- **PART C — heavy battery, complete encoding at n = 254..256 (7/7
  OK).**  B/D/1-block/chain rows at M = 256, all UNSAT as recorded.
  Notable: the complete encoding decides in ~2.5 s instances where
  G4b's CEGAR took 70-245 s and G4b's own CP-SAT cross-check timed
  out — the transitivity-complete formulation is simply the right one,
  which is what made the escalation in E affordable.
- **PART D — big battery, fresh lazy loop (19/19 rows OK, each run
  under BOTH backends).**  STG M = 128 pairs intact/punct + Q1 pairs +
  Q3 puncture torture + STG M = 256 {15,16}/{21,22} intact+punct: all
  UNSAT under Glucose42 (20-30 s at n = 768) AND again under
  Cadical195 in the same fresh loop (12-17 s) — vs 70-245 s for the
  campaign's own CEGAR.  The S2 straggler: **RUNG-X gm/B t = 9 rebuilt
  from scratch from the Geneson-matched schedule definition** (fresh
  stage table L_k = 4 M_{k-1}, M_k = 2 L_k 4^k; fresh team oracle) —
  the derived instance matches the recorded one EXACTLY (n = 1280,
  units = 137, the 20-attacker cohort, I_9 = (289, 544],
  I_11 = (1057, 2080], neck 32) — and is **UNSAT** on the rebuilt
  instance [1308 s, 246 rounds — the identical round count as the
  original record, the loop being deterministic].  Caveat kept honest:
  this verdict ran through the campaign's CEGAR loop applied to the
  G4c-rebuilt instance (so the CONSTRUCTION is independently verified,
  the loop is not); the G4c fresh-loop runs of this one instance were
  killed by the session harness at ~1 h wall under both backends
  before finishing (an infrastructure limit, not a solver verdict —
  see g4c_hedge_gm.log).  All 19 other big rows carry fresh-loop
  verdicts under two backends.
- **PART E — scale escalation (5/5 OK, all UNSAT).**  Beyond every
  scale G4b touched: 1-block {21,22} at M = 512 [54 s] AND M = 1024
  [1996 s]; chain rungs with the pair inside the preceding block —
  {513,514} on (1024, 2048] [153 s] and {1025,1026} on (2048, 4096]
  [2325 s, n = 2048]; STG two-block {15,16} at M = 512 [n = 1536,
  279 s].  The generic-pair core is now machine-true across a 16x
  scale range (M = 64..1024, windows to 4096) with three distinct
  proof engines.

S2 streaming postscript: the lin/B t = 9 RUNG-X seam solver (the
sparse-seam family predicted "plausibly SAT forever" in notes/39/42)
ended in TIMEOUT after 5784 s (n = 1282, 11 units, no verdict) —
consistent with the prediction, no death claim there; log committed
(data/s2_rungx_linB.log).  The frac/B solver died without output.

Records: data/g4c_verify_{A,B,C,D,E}.{json,log} (+ the Glucose partial
log g4c_verify_D_glucose_partial.log and data/g4c_hedge_gm.*).  Totals:
24 catalogue rows, 44 + 7 + 19x2 + 1 + 5 = 94 solver verdicts, exact
walks, instance identity — zero discrepancies with the G4b/S2 records
(and a key-level cross-tab of all 51 overlapping (n, units) instances
against the recorded G4b JSONs: 0 disagreements).

## 2. Shape coverage: what NECK + T-PIN-STAGE + the seam law now kill

Write B(m) = (2^m, 2^{m+1}] for the dyadic blocks.  For a partition
Z+ = T_A u T_B and a constant C, say a block is C-CLEAN for team T if
|B(m) \ T| <= C.  Exhaustive dichotomy (no shape hypothesis):

**Case 1 — some team T has, for some constant C, infinitely many
C-clean blocks.**  Then T is dead MODULO the generic-pair rung schema
(open lemma N2 below): pick an adjacent pair {x, x+1} inside T's
lowest C-clean block (any block minus C values still contains adjacent
in-team pairs), thin the remaining C-clean blocks to a disjoint family
above it, and run the T-PIN pigeonhole (hand-proven) against the
single-block rungs, which are machine-UNSAT for every pair tested from
{11,12} up, at M = 64..1024, under <= 8 arbitrary punctures, chains
included — with attacker pairs both below the block, inside the
previous block, and inside the block family.  This case CONTAINS, as
special cases, every shape the campaign killed piecewise:
  - the canonical dyadic partition (proven dead by hand, thm:main);
  - octave-alternating with ANY donation schedule (notes/35, 38-40:
    the d_t law / Lemma NECK is the sharper hand route; rungs
    machine-true wherever the neck is bounded);
  - stage-alternating ownership (notes/42: seam law closes the
    schedule dials, T-PIN-STAGE + puncture-robust C3 force splitting,
    STG rungs kill both teams through consecutive blocks);
  - irregular block-granular ownership, mixed run lengths, and every
    finite modification of any of these (all the machinery quantifies
    only over "infinitely many scales"; finite modifications cannot
    rescue, and attacker pairs are drawn from high blocks, so moving
    any fixed finite set of values changes nothing).
  For j = 4 crown content ({15,16} + infinitely many INTACT in-team
  blocks) this case is dead UNCONDITIONALLY (thm:ogred + thm:c3core,
  hand); the C-clean generalization is what needs lemma N2.

**Case 2 — otherwise.**  For every C, cofinitely many blocks are
C-dirty for BOTH teams: the intruder count of each team in B(m) tends
to infinity.  Call this the EVERYWHERE-SPLIT regime — both teams have
unboundedly growing presence in every sufficiently large dyadic block.
This regime is NOT covered by any current death mechanism, EXCEPT that
lem:orbit still bites inside it wherever a team carries an infinite
finite-reflector orbit (e.g. the odd/even partition dies instantly:
odds contain 3, 5, 9, 17, ... with reflector 1, evens contain 4, 6,
10, 18, ... with reflector 2).  The 2-colored trichotomy (notes/36)
lives entirely in this regime and is SAT at every finite horizon —
there is no finite certificate against it today.

So the honest answer to "do NECK + T-PIN-STAGE + the seam law cover
all shapes": **they cover all of Case 1 modulo one rung schema — which
is every partition in which either team ever concentrates a whole
block up to bounded dust, i.e. every 'geometric' shape proposed in
five months of hunting — and none of Case 2.**  The YES-space is
squeezed into everywhere-split partitions: both teams must
simultaneously permute at upper density about 1/2..2/3 per side while
paying the e118/e119 per-block coordination prices, with no clean
teams available (notes/42 SS5) and lem:orbit patrolling the orbits.
No explicit candidate partition in this regime has ever survived
construction attempts (H1-H3), but the regime itself is not refuted.

## 3. The NO program (numbered, with current status)

A complete NO proof = N1 + N2 + N3 + N4 (N5-N7 are the Case-2 attack,
where N4 is the frame).  Status legend: [HAND] proven by hand +
machine-audited; [RUNG] true at all machine-tested instances, hand
schema missing; [OPEN] no proof route yet demonstrated.

- **N1 [HAND] — pigeonhole reductions.**  T-PIN / T-PIN-STAGE /
  T-PIN-BLOCKS: a fixed finite attacker set in team T + infinitely
  many disjoint windows whose per-scale gadgets are UNSAT ==> T not
  permutable.  Proven (thm:ogred verbatim; notes/39 SS4, notes/42
  SS3).  Also here: lem:orbit + its exact sharpness T-SHARP, the d_t
  law, Lemma NECK, the seam law (now re-verified to seam ~2^20000).
- **N2 [RUNG — THE crux, "next-C3"] — the generic-pair core schema.**
  Claim: for every adjacent (or gap-2) pair {x, x+1} with x >= 11,
  the single-block rung OG_{x,x+1}(M) is UNSAT for all sufficiently
  large M (uniformly: all M >= 4x, say).  Machine: true at every
  instance ever tested — M = 64..1024, 15+ pair configs, chains,
  truncations to 36%, <= 8 punctures, two-block STG forms, interval
  and seam forms; three independent solver routes (CEGAR/Cadical,
  complete/Glucose, CP-SAT).  C3 is one member of an evidently large
  family; no hand schema yet.  Program: MUS anatomy across
  {11,12}..{21,22} x scales (the e88/e90 path that found C3).
  N1 + N2 kill all of Case 1.
- **N3 [RUNG, partially machine] — bounded-dust robustness.**  For
  each fixed C, the N2 rungs stay UNSAT under any <= C punctures at
  cofinitely many scales.  Machine-true at C <= 8 (Q3 torture,
  re-verified); the C3-specific instance (top-pair puncture) is
  flagged in notes/42 as a one-paragraph hand extension (the
  flood/zigzag lemmas never touch the top two values).  Expected to
  fall out of whatever schema proves N2.
- **N4 [HAND, frame] — the Case dichotomy.**  Exactly as in SS2:
  either a team has infinitely many C-clean blocks for some C (Case
  1), or both intruder counts diverge (Case 2).  Trivial, but worth
  stating: it is what makes the enumeration of "remaining shapes"
  EXHAUSTIVE rather than a list of guesses.
- **N5 [OPEN] — dense-subset cores (majority transfer).**  In every
  block one team owns >= half.  Needed: a rung that fires not on
  full-or-nearly-full blocks but on ANY in-team subset of density
  >= 1/2 + eps in a block (or in two consecutive blocks) — the robust
  crown ladder for dense-but-not-full blocks.  Evidence: S2's
  truncated pair rungs stay UNSAT with 36% of the block removed;
  e119's rich-D machinery is scale-stable.  This is the front where
  Case 2 must be attacked (experiment e120: coupled two-scale
  split-block gadgets with per-team density dials).
- **N6 [OPEN] — the coupled-scale accounting.**  The e118/e119 finite
  theory shows every feasible finite coloring pays a strictly
  positive, scale-stable price (exactly 3 endpoint donations per
  attacked full block; multi-crown strictly more; min CAP 1..2 on the
  displacement ladder).  Needed: a conservation/consistency argument
  that in an everywhere-split partition the two teams cannot BOTH pay
  their prices at all scales simultaneously — the infinite-ledger
  version of the trichotomy.  No candidate statement is currently
  written down; this is the least-developed piece of the program.
- **N7 [OPEN, may be dispensable] — a density ceiling for permutable
  sets.**  Any upper-density bound < 1 for 3-permutable sets would
  kill all sufficiently skewed everywhere-split shapes and reduce
  Case 2 to near-balanced splits, where N5/N6 have the most traction.
  Currently NO such theorem exists (the 2/3 record is a lower-bound
  construction; nothing forbids density-1 permutable sets except
  lem:orbit-style obstructions applied ad hoc — e.g. any set
  containing a full tail of Z+ dies via the doubling orbit
  u_{s+1} = 2 u_s - r off any of its own elements r, so cofinite
  sets are out; quantitative versions unknown).

Route note: N2 is where the leverage is — it converts five months of
per-shape verdicts into a single two-lemma theorem (N1 + N2) covering
all of Case 1, and its proof machinery (whatever replaces C3's
zigzag/flood at generic pairs) is the natural seed for N5.

## 4. Probability and the honest state

- All named geometric shape families: DEAD (Case 1), at epistemic
  level "hand theorem modulo a rung schema whose instances are
  machine-true under three independent engines at 16x scale range,
  with zero exceptions ever observed".
- The single proven-unconditional island: crown pair + intact blocks
  (thm:main machinery), now known NOT to be magic — {15,16} is just
  the crown instance of the generic-pair core (G4b SS4b, re-verified).
- Remaining YES-space: everywhere-split partitions only.  Nothing
  survives IN it as a concrete candidate; nothing refutes it as a
  regime.  Its finite theory is SAT everywhere (notes/36), so a NO
  must come from infinite accounting (N5-N7), not finite certificates.
- The G4a screen never ran; G4c's PART A (fresh-oracle catalogue at
  all recorded seams + exact walks to 2^20000) and PART E (scale
  escalation) are strictly stronger evidence on the same questions,
  so nothing is owed there.

**Estimate: NO ~ 85-88% (up from 75-80% pre-G4b; the G4b jump to ~85%
survives adversarial re-verification intact, and the complete-encoding
+ 16x-scale confirmations shave the residual doubt about the rung
family being a solver artifact or small-scale accident).  YES ~
12-15%, all of it living in the everywhere-split regime.**  Decisive
next steps, in order of leverage: (1) MUS anatomy of the generic-pair
core (N2 schema hunt); (2) e120 dense-subset/coupled-scale gadgets
(N5); (3) writing down any candidate N6 ledger statement, even a wrong
one, to give the machine something to break.

## Reproduce

    PY=.venv/bin/python
    $PY experiments/g4c_verify.py --part A     # seam law + walks, ~1 min
    $PY experiments/g4c_verify.py --part B     # small battery, ~1 min
    $PY experiments/g4c_verify.py --part C     # n~256 complete, ~1 min
    G4C_SOLVER=Cadical195 $PY experiments/g4c_verify.py --part D  # ~40 min
    G4C_SOLVER=Cadical195 $PY experiments/g4c_verify.py --part E  # ~1.5 h

Backend note: parts D/E default to Glucose42; the n >= 1024 instances
took > 1 h wall under Glucose and the session harness killed the
processes, so their verdicts on record are Cadical195 under the same
fresh loop (both backends agree on all 19 D rows).  Artifacts:
data/g4c_verify_{A,B,C,D,E}.{json,log}, g4c_hedge_gm.json.
