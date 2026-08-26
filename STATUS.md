# Erdős #197 campaign — STATUS (2026-08-26, post-G4)

## Bottom line

**THEOREM (proven, hand proof, machine-audited).  S_A = ∪_{k even}
(2^{k−1}, 2^k] is not 3-permutable: it admits no permutation free of
monotone 3-term APs.  The canonical dyadic partition Z⁺ = S_A ⊔ S_B
therefore does NOT resolve Erdős #197.**

Erdős #197 itself (does *some* 2-set partition work?) remains open; this
theorem eliminates the canonical candidate and the natural YES route.

## The proof chain (paper/main.tex)

1. **Order-gadget reduction** (thm:ogred, unconditional): if
   OG(2^{2t−1}) is infeasible for infinitely many t ≥ 4, then S_A is
   not 3-permutable.  OG(M) = order the block (M, 2M] AP-freely with
   15 guard-precedence attacks from the values 15, 16.  [Hand proof,
   argued directly on a hypothetical permutation; boundary arithmetic +
   case table audited by e96_reduction_check.]  NOTE: thm:ogred does
   NOT depend on the chunk reduction (thm:chunk, exact, now proved in
   the paper); the chunk calculus was the discovery coordinate system
   and gives an alternative route (paper rem:ogchunk), but the main
   chain is just thm:ogred + thm:c3core.
2. **C3 core theorem** (thm:c3core, hand): for every M ≡ 0 (mod 8),
   M ≥ 16, AP-freeness on (M, 2M] is inconsistent with the 3-axiom core
   C3 = {t₅≺b₅, t₃≺b₆, t₁₀≺b₃} ⊂ OG(M)'s attacks (b_j = M+j,
   t_i = 2M−i).  Proof toolkit (notes/33 v2 = paper §"C3 core"):
   - Lemma Z (zigzag propagation on d-ladders), Lemma D (phase
     dichotomy), Lemma E (transfer lock: b₅≺b₃ ⟺ t₃≺t₅ at M ≡ 0 mod 4),
     Lemma P (mirror-flood induction at a center c over a g-class;
     phase-blind).
   - Theorem L1: A2+A3 force b₅≺b₃ and t₃≺t₅ (M ≡ 0 mod 4, M ≥ 12).
   - Theorem FLIP: given those, A1 is contradictory (M ≡ 0 mod 8).
   - The mod-8 arithmetic enters exactly once: m₀±1 (m₀ = 3M/2) are
     G4-flood centers iff M ≡ 0 (mod 8) — matching machine sharpness
     (C3 satisfiable at all other residues mod 8).
3. Every dyadic scale 2^{2t−1} (t ≥ 4) is ≡ 0 mod 8 and ≥ 128, so 1 + 2
   give the main theorem (thm:main).

## What is machine vs hand

- **Hand (with step-by-step machine audit of each schema instance):**
  everything in the chain above.  e113_c3_hand_proof.py executes every
  lemma application with strict assertions at 100 scales (L1, 12..400 +
  512 + 1024) / 51 scales (FLIP, 16..400 + 512 + 1024); zero failures,
  re-run fresh 2026-08-25.
- **Independent cross-checks:** e113b (closure engine, no schema
  knowledge, refutes all case-tree branches; 51 + 27 scales, re-run
  fresh); e114 (NEW, integration session): direct SAT tests of the
  theorem statements at scales untouched by discovery — L1-forcing
  UNSAT at M = 148, 212, 264; C3 UNSAT at M = 264, 328; ≡4 mod 8
  sharpness SAT at M = 268, 332.
- **Adversarial audit (e115, parallel session; completed 2026-08-25):**
  from-scratch closure engine (independent data structures) closes every
  case-tree branch at fresh scales L1 = {204, 244, 404, 520, 1000},
  FLIP = {208, 328, 520, 1000}, with 4-mod-8 controls correctly NOT
  closing (engine sanity); e113 schema re-run at adversarial scales
  incl. M = 2048, 4096 — all pass; independent SAT encoder
  (e115_audit_sat.py, record data/e115_audit_sat.json): all 11 checks
  pass — L1-forcing UNSAT at M = 404, 520; C3 UNSAT at M = 408, 520;
  sharpness SAT at M = 412 (≡4 mod 8) and M = 413 (odd) with models
  independently re-validated; L0 forced at M = 302; Lemma-E lock at
  M = 46, 52.  The one audit failure found was a KeyError bug in the
  audit script's own Lemma-H bookkeeping check (appendix/halving
  material, not on the target chain).
- **Machine-only (corroboration, no longer load-bearing):** AP+C3 UNSAT
  sweeps (e104 part 3: all M ≡ 0 mod 8 in 16..256, and 512), OG(M)
  UNSAT for 16 ≤ M ≤ 200 and M = 512 (e89, e96 P5 — note these check
  the full 15-attack gadget, a weaker UNSAT statement than AP+C3), the
  S1 forcing sweep (e101), the v1 closure trees (e112).
- **Supporting theorems in the paper (hand):** orbit obstruction,
  balance law, Lemma R, vdC absorption, no-contiguous-runs, tower
  characterization, chunk reduction + normalization, block-granular
  death, ×4 restriction, crown-ladder rungs (machine), ray piercing.

## The single remaining gap

**None for the main theorem.**  Open beyond it:
1. Full OG conjecture (OG(M) infeasible for every M ≥ 16, all residues)
   — not needed; would require per-residue analogues of L1/FLIP (C3 is
   satisfiable off the 0 mod 8 class; other attack subsets take over).
2. Erdős #197 in general — whether any 2-partition works.  See the
   "General case" section below (hunt synthesis, notes/34–37).

## General case (beyond S_A): hunt synthesis H1–H3 (2026-08-25)

Three parallel hunts (notes/34 complement, notes/35 sliver-swap,
notes/36 two-colored theory, notes/37 portable crown) mapped the space
of candidate partitions.  Net result: **every concrete candidate tested
is dead — several at theorem level — but the finite 2-colored theory is
SAT everywhere, with a sharp trichotomy of escape shapes.  One YES-shape
survives untested; one NO-program has a machine-verified first rung.**

### What is now proven or machine-certified

- **Geneson's own partition is a NO** (Theorem H1, notes/34, commit
  b7a839f): the complement C of Geneson's exact density-2/3 witness
  contains the infinite doubling orbit u_s = 2^s + 3 (s ≥ 5, reflector
  3 ∈ C), killed by lem:orbit; verified to 2^200 by exact interval
  arithmetic.  So the natural "use the best known permutable set as one
  side" route fails unconditionally.
- **Orbit dichotomy law** (10/10 parameter points machine-certified):
  C(λ, r) contains an infinite orbit iff r and 2λ are both powers of
  two.  λ = 3 keeps W at upper density 2/3 yet makes C orbit-free —
  there is NO universal complement-death theorem via orbits.  But every
  tuned complement stays CROWN+SLIVER flagged and would need to permute
  at upper density ≥ 5/6, far above the 2/3 record.  Plausibility: low.
- **All fixed-depth sliver-swap partitions are dead** (notes/35, commit
  4b80f0a; 14 candidates, dyadic and quad families, bottom/top swaps at
  depths 8/12/16).  Dyadic bottom-swaps die at theorem level: donation
  creates period-2 infinite orbits on BOTH teams simultaneously
  (explicit certificates, e.g. s=8 team A offsets (14,8) reflectors
  {20,2}, walked to 2^60) — lem:orbit kills.  Quads (block ratio > 2)
  are self-attacking: reflections are trapped in-block, sliver policy
  irrelevant.  **Structural lesson: in an octave-periodic partition the
  attack surface is conserved — keep your bottom slivers → crown death;
  donate them → orbit death.  Geneson escapes only because his removed
  slivers fall into silent zones owned by nobody, which cannot exist in
  a partition.**
- **The 2-colored trichotomy** (notes/36, e118/e119, commits 8031204 +
  8756098): over ARBITRARY colorings of (M, 2M] + attackers, the joint
  order-gadget and coupled chunk-rung systems are SAT at every horizon
  tested, and every feasible coloring uses one of exactly three escapes:
  (1) **crown split** — 15 and 16 in different teams (0 cost);
  (2) **block-poor crown team** — the crown's team a scattered minority
  in every long block; (3) **endpoint donations** — exactly 3 values
  per attacked full block, supported ONLY on the attack endpoints
  (bottom sliver M+{1,2,4,5,6} or its mirror, top sources
  2M−{3,5,7,11,13}); busiest repairs M+4 and 2M−7, scale- and
  residue-stable.  Conversely the block-rich class (rich0) inherits the
  dyadic crown-displacement ladder rung-for-rung (min CAP 1 at m=3,
  exactly 2 at m=4) — the finite shadow of the portable-crown theorem,
  machine-checked over the whole coloring class.
- **Multi-crown price is strictly higher** (e118 mindon4, partial run,
  log in data/): with all four attackers 15,16,31,32 forced into one
  team, donation budgets ≤ 4 are UNSAT at M=64 (vs exactly 3 for the
  single pair) — handling several crown pairs in one team costs
  strictly more per block.  (M=256 single-crown min donation ≥ 2,
  budgets 0–1 UNSAT, run interrupted.)

### Growing-sliver swap: DEAD (G3, notes/38, 2026-08-25)

The candidate below was built and screened (experiments/
g3_growing_sliver.py; schedules s_t ∈ {t, 2^{floor(t/2)}, floor(2^t/t),
Geneson-stage-matched} × {natural, split-alternating crowns}, both teams,
horizons 2^12/2^15/2^18): **no survivors — 8/8 candidates carry the
portable-crown death signature on at least one team, and the d_t law
(notes/38) shows this is forced for EVERY donation schedule in this
geometry.**  With d_t := 2 s_t − s_{t+1}: a fixed attacker x hits the
block owner's kept bottom iff x ≥ d_t + 2 and the receiver's sliver top
iff x ≤ d_t − 1, so on each octave-parity class "owner safe" needs
d_t → ∞ while "receiver safe" needs d_t eventually ≤ its smallest
attacker — never both.  Growth is a zero-sum dial; the attack surface is
conserved, only re-aimed.  Crown splitting (escape (1)) never helps and
is actively harmful: the planted half 2^j−1 atop the partner's block is
a portable landing pad — it alone kills the otherwise-clean geo/A via
(x, 2^j−1, 2^{j+1}−2−x), machine examples (2,31,60), (2,127,252).  Two
by-products: (i) **geo_nat/A** (s_t = 2^{t/2}, team A) is the
first fully clean partition team of the campaign (no fixed attacker, no
ray, density 2/3 at peaks) — but its partner is doubly dead and the law
says no partner inside this geometry can be clean; (ii) the RAY-GROW
instrument (censored ratio-2 rays with reflectors ≤ 4 s_t + 64, verified
witnesses) shows all dead teams also sit exactly in lem:orbit's
finite-F gap — a **lem:orbit-grow** (f_m ≤ C s_t) would kill the family
a second, unconditional way.  Remaining YES-shapes must break octave
alternation itself (stage-alternating ownership à la Geneson).

### Growing-death theory: which G3 signatures are theorems (S2, notes/39, 2026-08-26)

G3's verdicts rested on the portable-crown SIGNATURE (fixed attacker
recurring at infinitely many scales); S2 built the theory layer that
says which signatures convert to death theorems.  Everything below is
machine-checked on the S1 partitions at ≥ 3 scales
(experiments/s2_growing_death.py, data/s2_*).

- **The orbit mechanism does NOT extend — lem:orbit is exactly sharp at
  |F| < ∞ (T-SHARP).**  For every unbounded growth bound g there is a
  permutable set containing an infinite orbit with distinct reflectors
  f_k ≤ g(k) + C (f_k = Θ(log u_k) achievable) — greedy constructions
  built at K = 20/40/60 steps, AP-exhaustively verified.  So the
  **lem:orbit-grow hoped for in the G3 notes does not exist**: no size
  or growth hypothesis on reflectors can replace finiteness.  What
  survives is the placement dichotomy (L-STEP/L-DESC): infinite orbits
  force infinitely many DISTINCT late reflectors, each procrastinated
  past an exponentially larger value — death must come from forcing
  reflectors EARLY (per-scale finite cores), never from growth alone.
  SLIVER-ORBIT gives the exact schedule criterion s_{t+2} ≤ 2s_{t+1}−2:
  lin/frac carry certified slow orbits on both teams (exact-int walks
  to octave ~413), geo/A and gm are orbit-clean — either way, by
  T-SHARP these orbits prove nothing alone.
- **The crown mechanism DOES extend, in fixed-pair form (NECK + T-PIN).**
  Teams are interval unions I_t = (2^{t−1}+s_t, 2^t+s_{t+1}] with neck
  n_r = 2s_r − s_{r+1}; a fixed x attacks in-interval iff x ≥ n_t + 2
  and across the seam iff x ≤ n_{t+1} − 1.  **Lemma NECK: on every
  schedule some team carries a fixed pair of its own values attacking
  at infinitely many of its scales** (bounded necks ⇒ pierced
  in-interval; unbounded ⇒ every fixed pair seam-attacks).  T-PIN
  (thm:ogred's pigeonhole verbatim) reduces death to an infinite family
  of finite UNSAT rungs with FIXED attackers.  Scale-ADAPTED attackers
  (x_t = 2s_t + c) fire only in pair form and cannot overflow: single
  rungs are SAT everywhere (c ≤ 200 scanned), the pair's second member
  can be sacrificed per scale (depth (64, 96] of 247 at lin t=9, cohort
  = C3's g-classes: all odds, then ≡ 6 mod 8), and T-SHARP's
  procrastination makes distinct per-scale sacrifices legal — T-REGRESS
  (the varying-attacker overflow) is closed.
- **Machine rungs**: pair rungs SG(t, {15,16}) UNSAT at 4 schedules × 3
  scales (t = 9/10/11, deepest truncation 36 % of the block); the
  C3-shifted core is SAT under truncation (already at s = 9 of 256) —
  the C3 certificate does NOT transfer, the pair UNSAT rides an unknown
  new core (THE open crux); **RUNG-IN geo/B (neck-0 intervals, fixed
  pair {21,22}) UNSAT at r = 7/9/11** with scale-independent unit count
  — geo is dead conditional on this rung family, the same epistemic
  shape as thm:ogred+thm:c3core before the C3 hand proof; gm stage-jump
  rung (r = 8, neck −30, pair {4,5}) also UNSAT; RUNG-X seam rungs
  (lin/gm/frac t = 9) in flight at close — unit-density arithmetic:
  gm's plateau seams are the only OG-density seam family (fixed
  ~M_{k−1}-attacker cohort, Θ(s) units), lin/frac seams are
  Θ(log)-sparse and plausibly SAT forever.
- Net: for bounded/zero-neck schedules the growing-sliver death is now
  **theorem-modulo-rungs with the rungs machine-true at 3 scales**; for
  growing-neck schedules (lin, frac) the fixed pairs sit on sparse
  seams and the per-scale core there is the open front.  The single
  crux for the whole family: a hand schema (next-C3) for truncated/
  interval cores.

### Growing-sliver verdict (TASK V, notes/40, 2026-08-26): ALL DEAD — the family is closed

Final adversarial pass over the last surviving shape.  Two campaigns:

- **Tuned per-parity schedules (v2_tuned_screen.py): 6/6 dead, no
  both-clean variant exists.**  The S1 finding (geo/A = first clean
  partition team, clean because d_even → ∞ and d_odd ≡ 0) raised the
  tuning question: can a per-parity donation schedule give BOTH teams
  receding kept bottoms?  Six tunes screened (geomix / geomirror / geo3 /
  addgeo / linmix / neck2 — exponential, mirrored, mod-3, additive,
  per-parity-linear, constant-neck; natural crowns; 2^12/2^15/2^18; all
  SAT): every per-team verdict matches the d_t law exactly (12/12,
  including the edge case neck2/A whose receiver surface stays clean
  because its only lawful attacker x = 1 lives in B).  Making both
  teams' kept bottoms recede (geomix/addgeo/linmix) arms every fixed
  attacker against both received slivers — both teams die as receivers.
  The mirror tune produces the SECOND clean team (geomirror/B, parity
  mirror of geo/A) with a doubly-dead partner: cleanliness is cheap for
  one team, impossible for two — one dial, two hands.
- **Independent re-verification of every S1 death certificate
  (v1_growing_verify.py, all checks PASS):** fresh membership oracle ==
  g3 generator; d_t law exact iff (543 attacks + 513 blanks, 0
  mismatches, t ≤ 40); crown recurrences re-derived at exact high
  octaves (big ints, t ≤ 60, incl. genstage stage-jump lists and the
  geo_alt crown-plant family at all odd j ≤ 59); brute-force attack
  scan at 2^16 EQUAL to d_t predictions (nat) for all x ≤ 64; both
  RAY-GROW witnesses re-walked and DFS-extended to octave 80 (geo/B
  reflectors grow to ~2^40 ≈ 4 s_t — censoring at 2^18 was real, and
  the earlier CHECK4 failure was a verifier scan-budget bug, fixed);
  independent bit-reversal SAT sanity at 2^12.

**Verdict: the sliver-swap program (notes/35 fixed + notes/38 growing +
notes/40 tuned) is closed — every octave-alternating block partition
with ANY donation schedule carries the portable-crown death pattern on
at least one team, by the d_t law / Lemma NECK, with T-PIN reducing
bounded-neck cases to machine-true rungs.  What survives: two clean
single teams (geo/A, geomirror/B, density 2/3 at peaks) proving the
pairing, not single-team permutability, is the obstruction.  The only
untested YES-shape left is stage-alternating ownership (à la Geneson,
teams owning growing runs of consecutive octaves, slivers only at stage
seams) — which must already split every crown pair {2^j−1, 2^j} to
survive thm:ogred + thm:c3core on its full interior blocks (every
interior scale is ≡ 0 mod 8), and G3 showed planted halves are landing
pads.  That G4 screen is the single next experiment.**

### G4b (notes/42, 2026-08-26): THE LAST SHAPE IS DEAD — and the death
### argument generalized past every geometry

Stage-alternating ownership (the one YES-shape left after TASK V) was
attacked by theory + machine (experiments/g4b_seam_law.py + probes):

- **The stage-seam law** (7-channel exact catalogue, machine-exact on
  9 variants × 26 seams × 24 attackers): the d_t dial does not exist in
  stage geometry — the cross-stage channel X2 is CLOSED, bottom slivers
  are pure poison (every fixed receiver attacker fires, no threshold),
  donation protects nobody, and a NEW dense channel opens: a fixed x
  attacks EVERY value of a non-top in-stage block with completions in
  the next in-team block — Θ(M) units per block pair (the STG rung).
- **T-PIN-STAGE** (hand, thm:ogred verbatim): pair + infinitely many
  intact blocks counted in TOTAL across stages ⇒ death; j = 4 pair is
  unconditional (thm:c3core); the C3 core SURVIVES top-pair punctures
  (machine, 3 scales × 3 puncture states + mod-8 control), so forced
  splitting of all but O(1) pairs per stage has NO orientation
  loophole.  Every seam-pair split hands the new owner a fixed-cohort
  FAN — no stage-alternating team is clean (the two clean teams of the
  octave world have no analogue here).
- **STG rungs**: every fixed pair tested kills two consecutive blocks
  (7 pairs × 3 scales × 5 puncture patterns, all UNSAT; singles always
  SAT, even on three blocks).  **The single-block collapse (§4b): the
  pair phenomenon is NOT crown-specific** — {21,22} kills a single
  intact block at M = 64..256; threshold at M = 128: everything from
  ≈{11,12} up is UNSAT; chain form: a pair INSIDE block (64,128] kills
  (128,256]..(512,1024].  {15,16} was never magic, only conveniently
  located.  **T-PIN-BLOCKS**: modulo this generic-pair rung family,
  ANY team of ANY partition containing infinitely many full (or
  boundedly-punctured) dyadic blocks is dead.
- RUNG-X postscript: gm/B t=9 plateau seam rung (the one OG-density
  seam family) came home UNSAT [667 s, n=1280, 137 units]; every
  parity class of every S1 schedule now has a machine-true rung family
  or a proven-sparse seam.

### G4c (notes/43, 2026-08-26): adversarial re-verification — all
### certificates CONFIRMED, rungs extended to M = 1024

Fresh oracle, fresh classifier, fresh instance builders, different
solver (Glucose42 vs Cadical195), COMPLETE encodings (full
transitivity, no CEGAR) for n ≤ 300, fresh lazy loop above that,
independent witness checking (experiments/g4c_verify.py, data/
g4c_verify_*).  Every G4b death certificate re-verifies: the 24-row
seam-law catalogue reproduces exactly; exact big-int walks confirm X2
closure and neck divergence to seam ~2^20000 and FAN arithmetic at
2^20102; all SAT/UNSAT verdicts match across ~76 instances including
the rebuilt gm/B RUNG-X (instance identity re-derived from the Geneson
construction); scale escalation: 1-block {21,22} UNSAT at M = 512 and
1024, chain rungs UNSAT with the pair inside (512,1024] and
(1024,2048], STG {15,16} UNSAT at M = 512.  Zero mismatches anywhere.
The generic-pair core is machine-true across a 16× scale range under
three independent proof engines.

**Shape coverage after G4 (the honest dichotomy — notes/43 §2):** call
a block C-clean for team T if T owns all but ≤ C of it.  Case 1: some
team has infinitely many C-clean blocks for some constant C — dead
modulo the generic-pair rung schema (this contains every shape ever
proposed: canonical, octave-alternating any schedule, stage-
alternating, irregular block-granular, all finite modifications).
Case 2: both teams' intruder counts diverge in every block — the
EVERYWHERE-SPLIT regime, the entire remaining YES-space; not refuted
(its finite theory is SAT everywhere), patrolled only by lem:orbit.
The NO program is now a numbered 7-lemma list (notes/43 §3): N1
pigeonholes [HAND], N2 generic-pair core schema [RUNG — THE crux],
N3 bounded-dust robustness [RUNG], N4 dichotomy frame [HAND-trivial],
N5 dense-subset cores [OPEN], N6 coupled-scale accounting [OPEN],
N7 density ceiling [OPEN, maybe dispensable].  N1+N2 close Case 1;
N5-N7 are the Case-2 attack.

### Best surviving YES-candidate (pre-G3 text, kept for the record)

**Growing-sliver swap with alternating crown ownership**: ratio-2 block
partition in which each team donates the bottom s_t values of its
blocks with s_t → ∞ (e.g. s_t matched to Geneson's stage widths
M_{k−1}), and crown pairs {2^j−1, 2^j} are split or alternated between
teams.  This is the ONLY member of the sliver-swap idea left standing:
growing depth breaks both fixed-attacker crowns (attacks need kept
offsets ≤ s_t + x/2, failing eventually for every fixed x) and
finite-reflector orbits (reflectors 2o₁−o₂ > s_t outgrow every finite
set, voiding lem:orbit's hypothesis), and it composes escapes (1)+(3)
of the trichotomy.  Verification campaign: (i) generator + g2 death
screens (orbit/crown/crown-persistence/sliver) on both teams at
2^16–2^20 across growth schedules; (ii) survivors → chunk-stage
(thm:chunk) SAT verification at m = 4, 5 (RunPod for m=5); (iii) hand
analogue of Geneson Lemma 3.1 per team: reflections from kept block
bodies must exit into partner-owned territory (out-of-team = free);
the risk concentrates on the sliver-receiving side, whose received
intervals are exactly the H2 landing pads, now with growing width —
whether growth defeats a *growing-reflector* orbit analogue is the
open mathematical crux (lem:orbit needs finite F; no theorem yet for
slowly-growing F).

### Best NO-theorem target

**Multi-scale crown-pair consistency**: (a) portable-crown theorem
(notes/37) — any team containing a crown pair {2^j−1, 2^j} together
with infinitely many full blocks at matching residues is dead; proven
machinery exists for j = 4 (thm:c3core + thm:ogred); (b) per-j
C3-analogues for all j ≥ 4; (c) the endgame: in any partition, at each
block one team is the majority (both teams cannot be block-poor at the
same scale), so escape (2) merely transfers the burden — if every
majority team must handle its own crown pairs and the multi-crown price
grows with the number of pairs owned (first rung machine-proven: ≥ 5
vs 3 at M=64), a global consistency/parity obstruction over all pairs
and scales becomes a NO.  Hardest steps: per-j attack cores (the mod-8
arithmetic of C3 entered exactly once and is j-specific — each j needs
its own residue class and core), and killing the block-poor escape at
ω (the transfer argument needs "majority ⇒ effectively block-rich",
i.e. a robust version of the crown ladder for dense-but-not-full
blocks — currently the ladder is only proven for intact blocks).

### Decisive next experiments (post-G4 ordering, by leverage)

1. **N2 schema hunt (THE crux)**: MUS anatomy of the generic-pair core
   across {11,12}..{21,22} × M = 64..1024 (the e88/e90 path that found
   C3) — a scale-stable hand schema converts ALL of Case 1 into a
   two-lemma theorem and retires every per-shape argument at once.
2. **NO route in Case 2 (e120, now THE experimental front)**:
   dense-subset / coupled two-scale split-block gadgets — does a pair
   rung fire on an in-team subset of density ≥ 1/2 + ε of a block (N5)?
   Plus the coupled donation-price ledger at adjacent scales (N6);
   finish mindon4 (budget 5+) and the m=5 same-mode CAP=0 run.
3. **RunPod bulk**: generic-pair rungs at M = 2048/4096 + systematic
   pair-threshold maps at several scales (is the {11,12} threshold
   scale-stable?) — cheap now that the complete encoding is known to
   decide these instances in seconds-to-minutes.

### Honest assessment (updated 2026-08-26, post-G4c)

Every named partition shape is now dead: the canonical partition at
full theorem level; octave-alternating (any donation schedule) by the
d_t law / NECK + machine-true rungs; stage-alternating by the seam law
+ T-PIN-STAGE + STG rungs; and all block-granular geometry at once by
T-PIN-BLOCKS modulo the generic-pair rung schema — whose instances
have never once failed (three independent solver engines, M = 64 to
1024, ~90 UNSAT certificates, adversarially re-verified with complete
encodings and a fresh oracle in G4c).  The YES-space has been squeezed
into a single regime with a clean definition — everywhere-split
partitions, both teams' per-block presence unbounded — which no
concrete candidate has ever inhabited successfully, but which no
current mechanism refutes (its finite theory is SAT at every horizon;
only lem:orbit patrols it).  Against NO: the everywhere-split regime
is large, structurally unlike anything killed so far, its death needs
genuinely new mathematics (N5–N7: dense-subset cores, coupled-scale
accounting, density ceilings — all OPEN), and the campaign's history
of "SAT everywhere" for the finite 2-colored theory is a real warning
that finite certificates may simply not exist there.  Current
estimate: **NO ≈ 85 %, YES ≈ 15 %** (up from 75–80 pre-G4: the last
proposed shape died and the death mechanism went generic; capped
because Case 2 is untouched and needs new ideas, not new compute).

## Key files

- paper/main.tex — full write-up incl. thm:main, thm:c3core (§ The C3
  core theorem and the main theorem).
- notes/33-og-proof.md — the hand proof, machine-check pointers.
- notes/27-dichotomy-ladder.md — the running status ledger (session 10
  = gap closed + audit record).
- experiments/e113_c3_hand_proof.py, e113b_closure_crossval.py,
  e114_theorem_spotcheck.py — verification suite; data/e113*, e114*.
- notes/42-seam-law.md + experiments/g4b_seam_law.py, g4b_stg_probes.py
  — the stage-seam law, T-PIN-STAGE, STG rungs, the generic-pair
  single-block collapse (T-PIN-BLOCKS); data/g4b_*.
- notes/43-g4c-verdict.md + experiments/g4c_verify.py — adversarial
  re-verification (fresh oracle, complete encodings, Glucose42),
  scale escalation to M = 1024, the Case-1/Case-2 dichotomy and the
  numbered NO program N1–N7; data/g4c_verify_*.
