# Erdős #197 campaign — STATUS (2026-08-28, post-audit of the night-shift fronts; see the final section for the current state)

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

## FRONT MERGE (2026-08-26, e120–e124): N2 diagonal schema, N5 density
## verdict, N6 first firing Case-2 core

Three parallel fronts ran to completion (N2's final message was lost
in transit; its results are reconstructed here from commits cdc2d8f /
0996051 and the committed data — there is no notes/44, the artifacts
ARE the record).  Full write-ups: notes/45-density-cores.md (N5 + the
C3 coupled gadget), notes/46-ledger.md (N6), data/e12{1,2,3}_n2* /
e123* (N2).

### N2 — the crux moved: C3 is now an INFINITE hand-schema family

- **Step 1, MUS anatomy** (e121_n2_mus_sweep, data/e121_n2_mus.json):
  complete size-≤3 core catalogues over the attack units for pairs
  {11,12}..{21,22} at M = 48..128 (≡ 0 mod 16): counts 0 / 3 / 7 / 9 /
  11–13 / 17–22 respectively (the hand C3 sits inside {15,16}'s 7);
  {11,12} alone has NO size-3 core there (deletion-MUS size 4).
  Catalogues are scale-stable — the same triples verbatim across M.
- **Step 2, all-residue coverage** (e122, data/e122_n2_residue.*): the
  single-block rung is UNSAT for ALL six pairs at EVERY scale
  M = 16..135 — no residue class escapes — with the minimal-core
  catalogue enumerated at each M; from M ≈ 100 the per-pair core
  counts are EXACTLY periodic mod 8 (e.g. M = 106/114/122/130
  identical), so per-residue schemas plausibly exist everywhere.
- **Step 3, THE N2 HEADLINE — the diagonal schema** (e123 + e123b):
  the C3 hand proof (Z / D / E / P toolkit of notes/33) generalizes
  VERBATIM to the core family
      C3(p) = {t_p ≺ b_p,  t_{p−2} ≺ b_{p+1},  t_{p+5} ≺ b_{p−2}}
  for pair {3p, 3p+1}, every odd p ≥ 5, with flip (UNSAT) class
  M/2 ≡ p+3 mod 4 — i.e. M ≡ 0 mod 8 for p ≡ 1 mod 4 and M ≡ 4 mod 8
  for p ≡ 3 mod 4.  Machine-verified for p = 5, 7, 9, 11, 13
  ({15,16}..{39,40}): 104 L1-scales + 52 flip scales + 52 sharpness
  controls each, ZERO failures (data/e123_diagonal_schema.json);
  independent solver cross-validation (e123b, fresh encoder): C3(p)
  UNSAT exactly on the flip class, SAT on the complement class, full
  rung UNSAT on both, at every probe incl. M = 256/260 — 0 mismatches.
  **The mod-8 arithmetic of thm:c3core was never {15,16}-specific: it
  slides along the diagonal lane exactly as the hand proof predicts.**
- Remaining for N2: hand schemas OFF the diagonal (other pair lanes,
  other residue classes — the ≡ 2 mod 4 and odd-M classes have machine
  cores but no schema; {11,12} needs a size-4 analysis).  The affine
  family miner e124_family_miner.py (mines e122's catalogue for
  uniform-in-x core families + the dyadic sub-catalogue) is committed
  but was NOT yet run.
- **UPDATE (N2-OFF session, this date, notes/49): e124 run and the
  off-diagonal program largely EXECUTED.**  (1) THE LANE LAWS: every
  off-diagonal core lane's residue law slides mod 8, affine in the
  pair index x (direct solver probes, all residues, M = 16..160):
  A4b/c/d-lanes fire at M ≡ x+5, B2 at x+7, B6 at x+3 (the three even
  classes ≠ x+1), C at x+2 (odd) — data/e124b_lane_probe.*.  (2) TWO
  NEW HAND SCHEMAS, both verified end-to-end e113-style (Lemma-D
  polarity case analysis + solver-free zigzag closure per branch,
  independent Cadical cross-checks, sharpness controls, 20 scales each
  + adversarial 256..2048): the {11,12} DYADIC size-4 core (M ≡ 0 mod
  8 — the T-PIN class; 2+2 phase clash on t1 = 2M−1 vs m0: attacker
  12's units {t0≺b6,t2≺b5} force m0≺t1, attacker 11's {t1≺b5,t3≺b4}
  force t1≺m0; each half = Lemma D on 2 ladders, 4 branches) and the
  first ≡ 2 mod 4 flip cell (B2(11) = {t2≺b5,t5≺b3,t7≺b2} at
  M ≡ 2 mod 8, parity dual: even t2 vs ODD m0, overlapping halves
  sharing t5≺b3) — e124i/e124l, zero failures.  (3) THE ODD CLASSES
  FELL TOO (e124n/o/p): for odd M the battleground moves to the
  half-integer center's neighbour c− = (3M−1)/2 — C(11) verified at
  19 scales (M ≡ 5 mod 8) with controls at all three other odd
  classes.  (4) THE TEMPLATE SWEEP (e124m): the same mechanism run
  mechanically per cell — **pair {11,12} is CLOSED AT ALL EIGHT
  RESIDUES mod 8** (first pair with complete per-residue hand-schema
  coverage; no residue escape for Case 1 on {11,12} at any M ≥ 68,
  small M machine-covered by e122), plus verified cells across pairs
  {13,14} (r0/r2/r4), {15,16} (r2), {17,18} (r0), {19,20} (r2) —
  every one a 2-unit half-pair phase clash at v* ∈ {t1,t2,t3} with
  two-to-three-ladder Lemma-D closure.  notes/49 §6 table.
  Remaining N2 gaps: finish the last per-pair cells (A4d(19)/B6(21)
  dyadic searches slow), pairs x ≡ 7 mod 8 off the diagonal (x = 23,
  31, ... — outside the e122 catalogue; extend e122), and the true
  endgame: PARAMETRIC (affine-in-x) verification along each lane,
  e123-style, to cover infinitely many pairs at once.

### N5 — resolved as posed: density 1/2 + ε FAILS for single blocks;
### the robust channel needs Θ(M) attack surface (notes/45)

- **Fixed low pairs are not density-robust**: adversarial-subset SAT
  gadget (selection vars, guarded APs/attacks, cardinality, complete
  transitivity; 153 streamed verdicts, every SAT witness independently
  re-verified, 0 failures).  Single block (M, 2M]: {15,16} has
  k_crit = M−3 at M = 64/96/128, {11,12} k_crit = M−2 — i.e. the exact
  adversarial puncture tolerance is 3 resp. 2 (the sharp single-block
  N3 constants), minimal escape ALWAYS the bottom midpoints
  {M+2, M+4(, M+5)}, and ρ* = 1 − O(1)/M → 1.
- **Density-robustness requires Θ(M) attack surface**: chain-geometry
  pair {M/2+1, M/2+2} has ρ* = 7/8 EXACTLY at M = 64 (d* = M/8 grows;
  escape = every other midpoint), bracketed [7/8, 15/16) at M = 96
  (near-critical k = 87 query unresolved); window-edge pair ρ* = 0.781;
  law ρ* ≈ 1 − x/(4M).
- **The T-PIN-compatible headline**: on the two-block STG window
  (M, 4M] with FIXED pair {15,16} (Θ(M) units from a fixed attacker —
  T-PIN applies verbatim, no varying-attacker caveat), the per-block
  density dial at M = 32 resolves to ρ* = 25/32 = 0.781: the rung
  fires on EVERY in-team subset of per-block density ≥ 13/16 [critical
  UNSAT 862 s].  Baselines 29/32 and 61/64 for the blocks alone — the
  two-block coupling buys the drop from ~0.95 to 0.78.  (M = 64
  bracketed SAT@3/4 / UNSAT@1, 28/32 unresolved; Part D existential
  two-scale form SAT at ρ = 1/2, 48/64 unresolved.)
- So N5 as posed is FALSE, the coupled forms reach 0.78 — and the C3
  discovery (below) SUPERSEDES the question: constant ABSOLUTE counts,
  not densities, suffice once two seams couple.

### N6 — the "SAT everywhere" barrier BROKE: first firing Case-2 core
### (notes/45 Part C3 + notes/46)

- **The two-seam coupled core**: B0, B1, B2 = (M,2M], (2M,4M], (4M,8M],
  every value colored A/B, each team its own order, block-order at BOTH
  seams for both teams (double non-procrastination), exact balance:
  UNSAT at M = 16 [1.2 s], 24, 32 [8.2 s], Glucose42-confirmed.  Seam
  controls at M = 16: none / low-only / high-only / outer-only ALL SAT
  — every proper subset of the seam chain escapes; the two-seam
  coupling itself is load-bearing.  ONE seam never kills (2-block
  balanced SAT at M = 16/32/64).  This is the first finite UNSAT ever
  produced in the everywhere-split regime's 2-colored theory.
- **The constant-bound schema (the Case-2 bridge)**: with ABSOLUTE
  per-team-per-block lower bounds, (3,6,12) is UNSAT at every
  M = 24..48; the floor TIGHTENS with scale ((3,3,3) SAT at 16/24,
  UNSAT from 32; (2,4,8) SAT at 32/40, UNSAT at 48); at M = 48 the
  critical constant is EXACTLY 2 — (2,2,2) UNSAT [135 s, +Glucose],
  (1,1,1) SAT — and the surviving (1,1,1)/(0,0,0) escapes leave a
  1-CLEAN block (A-sizes (47,1,100) / (0,95,90)), which is precisely
  Case-1 (N1+N2) territory.  **The dichotomy closes at C = 1.**
- **Escape anatomy (hand-readable)**: the forced structure is the
  cross-triple hypergraph {(u, y, 2y−u)}; every machine escape is a
  sumset dodge — minority pinned at the bound on a mod-4 lattice, or
  range-hidden in B1's bottom quarter; bounds ≥ (3,6,12) kill every
  dodge.  The hand-schema target: "a 3-element minority cannot keep
  2Y − U off itself at two seams".
- **The ledger (e121)**: L1 as drafted REFUTED (iid balanced controls
  are everywhere-split + window-diffuse — but orbit-supercritical, so
  not YES-candidates); repaired L1' (both teams doubling-subcritical ⇒
  some team keeps near-clean ratio-2 windows) consistent with every
  coloring measured — no diffuse+subcritical example exists.  L2
  strong form REFUTED (donation→donation flux ≡ 0, coupling is
  placement-sensitive); per-pair price form SUPPORTED: p(k) = 3, 7, 7,
  11 for k = 1..4 forced pairs at M = 64 (resolves e118's mindon4:
  p(2) = 7), first interior repairs at k = 3 — the notes/36 endpoint
  law breaks for large-x pairs.  Supply lemma: #AA + #BB + #switches
  = M−1, so away from orbit-dead alternation some team has Θ(M) live
  pairs at every scale (measured saturated).  Surviving route: supply
  + (p(k) → ∞, needs an N2-style schema) + T-PIN ⇒ dense teams pay
  unbounded prices ⇒ densities pinned near 1/2 ⇒ contradict L1'.
- **Dodger shape pinned** (the YES-material, notes/46 §5): a survivor
  must be (i) doubling-subcritical in BOTH teams, (ii) window-diffuse
  at every ratio-2 anchor, (iii) donation material pair-sparse
  (gaps ≥ 3), (iv) P(t) → ∞ arbitrarily slowly.  (i) and (ii) pull in
  opposite directions; no coloring with both is known.

### N-program table (notes/43 §3 numbering, post-merge status)

| # | Lemma | Pre-merge | Now |
|---|-------|-----------|-----|
| N1 | pigeonholes (T-PIN / -STAGE / -BLOCKS) | HAND | HAND (unchanged) |
| N2 | generic-pair core schema | RUNG — THE crux | **infinite hand family on the diagonal** C3(p) + **off-diagonal lane laws slide mod 8** (e124b) + **{11,12} closed at ALL 8 residues by verified schemas** (K4/B2/C(11)/K11_r1-r7/B6 — incl. the odd classes via half-integer center c−) + template-verified cells across pairs 13..19 — notes/49; remaining: last dyadic cells (A4d(19)/B6(21)), x ≡ 7 mod 8 pairs, parametric-in-x lane verification |
| N3 | bounded-dust robustness | RUNG | RUNG + **exact constants**: single-block tolerance d* = 2 ({11,12}) / 3 ({15,16}), scale-stable |
| N4 | dichotomy frame | HAND-trivial | restated **anchor-free** (ratio-2 windows, any anchor — e121 salting lesson); **C = 1 suffices** from M = 48 |
| N5 | dense-subset cores | OPEN | **resolved as posed: FALSE** for single blocks (ρ* → 1); robust variants: chain pair 7/8, two-block fixed pair 0.781 (T-PIN-clean); superseded by C3 constants |
| N6 | coupled-scale accounting | OPEN, no statement | **FIRING**: first finite Case-2 core (2-seam balance, 3 scales) + constant-bound schema (crit. constant = 2 at M = 48) + surviving ledger statements L1', p(k) → ∞ |
| N7 | density ceiling | OPEN, maybe dispensable | **likely dispensable**: the C3 bridge routes around it |

### The closing geometry (Case-2 outlook: CHANGED, materially)

Any partition either (a) gives some team infinitely many 1-clean
blocks — Case 1, dead modulo N2, which is no longer a bare rung but an
infinite hand-schema family with all-residue machine coverage — or
(b) eventually has ≥ 2 per team per block, hence ≥ (2,2,2) in every
window triple (M, 8M], dead modulo the C3 coupled schema.  The windows
compose freely at scales M·8^k (everything outside a window is
unconstrained), so the pigeonhole side is trivial.  Exactly TWO gaps
remain:

1. **Scale-stability of the constant-bound coupled schema**: CLOSED at
   M = 64 (e125 rerun, 2026-08-26): (2,2,2) UNSAT [304 s] and (3,6,12)
   UNSAT [629 s], data/e125_m64.log — and EXTENDED to M = 80
   (e126_deep_stability: (2,2,2) UNSAT [1414 s], data/e126_deep.log;
   M = 96 in flight) — stable over 48..80 for the critical constant,
   a 5× range beyond the balanced discovery scale.  What remains on
   this side is the hand schema (MUS front, notes/48), not compute.
2. **The double non-procrastination hypothesis** — both teams
   block-ordered at two consecutive seams, infinitely often.  The seam
   controls prove this hypothesis cannot be thinned; converting it
   into a theorem (or killing its negation: a team fails it only by
   re-descending below a previous block infinitely often — L-DESC
   well-founded-descent territory, notes/39) is now THE gap of the
   entire NO program.  **Second-wave verdict (e127 + notes/47, below):
   NOT a theorem — false single-team at every anchor, irreducibly
   two-sided, and correctly read FORWARD as forced procrastination
   (T-FORCE); the budget dial v*(M) is the new quantitative front.**

### Unresolved runs at merge — superseded (2026-08-26 late)

All merge-time stragglers either landed or were relaunched crash-safe:
(2,2,2)@M=64 LANDED (UNSAT, e125); the balanced MUS was rewritten
resumable (e126) and the M=32 target is DONE (see the MUS landing
section below), M=48 still descending (n = 155 of 336 at last check,
snapshot data/e126_mus_M48_b222.resume.json); e124 miner run (notes/49).
Still in flight: e126_deep (2,2,2)@M=96; e126 M=48 MUS; e124m searches
A4d(19)/B6(21)/A4d(13); e127 near-critical v* queries ((3,6,12)@24
v ≥ 2, bal@16 SAT-side bisection, (2,2,2)@48 scans — memory-heavy,
RunPod-sized).  Older N5/N6 stragglers (e121 price curves M=128, e120
chain M=96 k=87, Part E M=64 28/32, Part D 48/64) remain unrun.

### Decisive next experiments (post-merge ordering, one per front)

1. **N6 (now the program's critical path)**: ~~attack the double
   non-procrastination hypothesis~~ SUPERSEDED by the second wave
   (notes/47: DNP false as stated; the live target is T-FORCE
   affordability + v*(M) growth) — the prerequisites landed: M = 64
   AND M = 80 UNSAT (e125/e126_deep), M=32 MUS final (n = 116, all
   necessary).  NEXT: finish the M=48 support, run the
   anchor-coordinate comparison, write the dichotomy schema
   (notes/48), and measure the v*(M) trend (bal@16 exact, bal@24,
   (3,6,12)@24 — RunPod-sized).
2. **N2**: ~~run e124 + hand-verify ONE off-diagonal lane~~ DONE ×2
   (notes/49: {11,12} dyadic K4 AND ≡ 2 mod 4 B2 both verified
   end-to-end; lane laws uniform).  NEXT: the odd-class phase center
   ((3M±1)/2 pair for odd m0·2 — lane C at M ≡ x+2 mod 8 is the
   target), and extend e122 to x = 23..29 to close the x ≡ 7 mod 8
   off-diagonal pairs.
3. **N5**: lock scale-stability of the Θ(M)-surface law ρ* = 1 − x/4M
   (chain M = 96/128, two-block M = 64) — the density dial the C3
   bridge quotes when P(t) diverges slowly.

### FRONT G2 second wave (2026-08-26, e127 + notes/47): the seam
### hypothesis dissected — false single-team, irreducibly two-sided,
### and priced

Full write-up notes/47-seam-hypothesis.md; machine
experiments/e127_seam_budget.py (+ e127b_cover_check.py), records
data/e127_*.json/.log + e127_seam_budget.jsonl.

- **Formalization (§0)**: seam-clean at the anchor-free window
  W(N) = (N, 8N]; violation = adjacent-seam inversion pair (u, w),
  w placed before u; skip inversions cost ≥ |B1 ∩ T| adjacent ones
  (transitivity trichotomy).  Exact anchor-covering law: an inversion
  pair poisons ≤ 2 anchor intervals inside [u/4, u) (formulas
  machine-audited, e127b, 500 random pairs + exhaustive anchors).
  ¬DNP ⇔ the two teams' inversion pairs jointly cover cofinitely many
  anchors — inversions must recur in every octave.
- **Normalization verdict (§1)**: lem:normal TRANSPORTS — N-GEN: every
  permutable team admits running-max chunking with finite fibers,
  s(v) ≥ blk(v), (A)∧(B); the proof is team-blind — so "block-monotone
  up to finite fibers with δ ≥ 0" is WLOG for every team.  But DNP
  does NOT follow, and is FALSE single-team: X-INTERLEAVE (pairwise-
  swapped powers of two — an AP-free SET, so every arrangement is
  valid) re-descends at EVERY anchor (coverage machine-checked) with
  depth-1 descents, no infinite descending position chain, all
  displacements ≤ 1.  **The attack-plan question "does infinite
  re-descent force infinite position descent, or can positions
  interleave?" is answered: positions interleave.**  X-INTERLEAVE-v
  (greedy Behrend octave-interleave) pushes the violation budget to
  N^{1−o(1)} at every anchor — no DNP(v) weakening is single-team
  true either (Roth caps this free-team family at o(N²)).
- **The supply barrier (§2)**: disjoint windows have fresh inversion
  supply — no per-window budget hypothesis can be closed by counting/
  well-foundedness across scales.  What fresh supply cannot buy is
  exemption from the window's own AP theory (a late value's attack
  units are live on the material after it): the affordability of
  forced inversions for a DENSE team is the entire open content.
- **The budget schema (e127)**: seam units replaced by per-team
  inversion budgets ≤ v (indicators + cardinality; complete
  encodings; SAT witnesses independently audited incl. the §3
  edge-audit).  v = 0 reproduces the e120 cores.  Verdicts so far
  (near-critical UNSAT times explode; jsonl is the running record):
  balanced M = 16 UNSAT at v = 0/1/2 [2 s/24 s/244 s], SAT at
  v = 160/320/480 — v* ∈ (2, 160]; (3,6,12) M = 24 UNSAT at v = 0/1
  [8 s/190 s]; (3,6,12) M = 32 UNSAT at v = 0 [43 s]; scans for the
  first SAT points and (2,2,2) M = 48 in flight.  **Procrastination
  is not free: the cores tolerate genuine violation budgets.**
- **Irreducibly two-sided (the decisive structural find)**: BOTH
  one-sided weakenings are SAT already at v = 0 — asym (one team
  budget-free): free majority reverses its low blocks wholesale (2090
  inversions, 520 broken H-triples) while the pinned minority stays
  clean; majb (budget on the MAJORITY, minority free): SAT again,
  clean mono-free majority by range-hiding + free minority.  So no
  "only the dense team behaves" hypothesis has a finite core; the
  hypothesis DNP is two-sided or nothing.  Caveat that keeps this
  honest at ω: these are FINITE-only escapes — a 3-block window
  cannot charge the free team's prefix cohort or attacks from below
  the window; extending downward reaches notes/36's SAT-everywhere
  theory, so the ω-accounting is exactly N6, not a bigger finite core.
- **The reframing that replaces G2 (T-FORCE, notes/47 §2b)**: read
  the schema forward — its UNSAT at budget v proves every valid
  Case-2 pair is FORCED to exceed v inversions at EVERY large anchor
  (validity restricted to a window must sit in the SAT region).  The
  gap is no longer "prove DNP" (unprovable) but "prove a dense team
  cannot afford v*(N) forced inversions at every anchor forever" —
  with the covering law pinning inversions to every octave and the μ
  lower bound (each broken cross-triple needs its own inversion edge;
  μ can be 0 at balance via the parity dodge, so the cores tax the
  mixed in-block theory too).  This is an N6-ledger statement with a
  measured finite pump, no longer a bare order hypothesis.

### FRONT MUS landing (2026-08-26, later the same day): the M=32
### coupled-core support is FINAL — and it confirms the reduction

Background: notes/48 (Result 0, e126c) had already shown the Case-2
coupled core is NOT a pure sumset statement — the cross-triple
hypergraph alone is 2-colorable at both targets via exactly the two
known dodges (range-hide past the 7M−1 reachability cap /
parity-lattice-hide), and each dodge visibly recreates generic-pair
rung geometry one seam up.  Predicted support shape: seam anchors in
B0/B1 (bottom-offset coordinates) + a both-parity midband B2 run below
7M (proportional coordinates).

**The (3,3,3)@M=32 deletion-minimal support is now FINAL**
(data/e126_mus_M32_b333.json, log e126_mus_M32.log): n = 116 of 224,
Glucose42 re-verified UNSAT [2.8 s], criticality certificate **116
necessary / 0 redundant / 0 cardinality-locked** — a fully minimal
support, every value load-bearing.  Anatomy (block sizes 15/47/54):

- B0 = (32,64]: 15 values {33,34, 41,42, 45, 47,48, 57..64} — bottom
  pairs at offsets 1-2/9-10/15-16 (the C3-style bottom-midpoint anchor
  family) + the intact top run 57..64;
- B1 = (64,128]: the 47-value near-run [81,119] ∪ [121,128] — the top
  three-quarters of the sandwiched block, contiguous but for the
  single puncture 120;
- B2 = (128,256]: 54 values [129,168] ∪ [177,188] ∪ {191,192} —
  ENTIRELY within (4M, 6M], i.e. the reachable bottom of B2, far below
  the unreachable top eighth (> 7M = 224); every mod-4 class present
  in every block (no lattice escape hatch left).

This is the notes/48 prediction verbatim: (i) B0/B1 seam-anchor
material in bottom-offset coordinates, (ii) a long both-parity B2
midband run positioned so that every range/lattice hide recreates a
generic-pair rung.  **At machine level and at this scale, the Case-2
crux is confirmed to be the N2 rung geometry wrapped in one layer of
sumset forcing — one schema family for both cases.**  Pending to make
this scale-stable: the (2,2,2)@M=48 support (still descending,
crash-safe) and the formal anchor-coordinate comparison
(e126b_anatomy_compare.py 32 333 48 222).  Side landing, same session:
G1's compute range extended to M = 80 (above).

### What remains for a complete NO proof (the honest ledger,
### end of 2026-08-26)

The dependency graph lives in notes/50-assembly.md.  If every tag
below clears, Erdős #197 = NO.  None has cleared yet; every one is an
unproven link, listed with its current shape:

1. **GAP-G2 (THE gap, now reframed — notes/47).**  The double
   non-procrastination hypothesis is NOT a theorem and cannot be one:
   FALSE single-team (X-INTERLEAVE re-descends at every anchor;
   positions interleave), false for every budget weakening DNP(v) up
   to v = N^{1−o(1)}, irreducibly two-sided (both one-sided budget
   variants SAT at v = 0), and immune to counting across scales
   (fresh supply in disjoint windows).  The surviving statement is
   T-FORCE/affordability: *two Θ(M)-dense teams cannot both afford
   their forced > v*(M) inversions at every anchor forever* — an
   N6-ledger statement with a measured finite pump (v*(bal,16) ∈
   (2,160], v*((3,6,12),24) ≥ 2, one-sided escapes priced at ~2000
   inversions).  Sub-linear minorities are NOT a seam problem
   (majority density → 1; N5 ρ*-rungs + T-PIN), EXCEPT the
   alternating-majority sub-case (block-majority alternating every
   octave with growing dust), which needs a NECK/d_t extension to
   unbounded dust or the coupled core — that caveat is its own
   sub-gap.  Nothing here is proven at ω.
2. **GAP-N6a (coupled-schema hand proof).**  The constant-bound core
   is compute-true over M = 16..80 ((2,2,2) critical from 48) but has
   no all-M hand schema.  The M=32 MUS landing above pins the target
   anatomy and the reduction-to-N2 shape; needs the M=48 support +
   anchor-coordinate stability + the actual schema write-up (the
   dichotomy of notes/48: mono cross triple, or hide ⇒ rescaled
   generic-pair rung).
   UPDATE (notes/55 + notes/56): the schema is locked
   (CORE′(M), five-scale UNSAT), the skeleton is proved (Lemma U,
   A1–A9, E2/C, P′, W, PAR, FG-high, Theorem H), and the former
   crux GAP-STRUCT — why every straddle-free coloring falls into a
   killable regime — is now a machine-certified three-case theorem
   at M = 48/64/80 (fan / lopsided / parity, via the exposure
   potential Φ and the wholesale lemmas DICH, L-LOP, P-ARM;
   notes/56 §4b).  Remaining: uniformization gaps GAP-DICH,
   GAP-LLOP, GAP-PARM (⊇ GAP-H1), GAP-ASM′, plus the pre-existing
   GAP-FG-schema and GAP-J-pencil (notes/56 §5.2).
   UPDATE (notes/57, night 2026-08-27): GAP-DICH is now a proved
   case tree (forced-interval calculus: Lemmas T/FI/ANCHOR/COLL/MID
   + Theorem H-DICH + Lemma SP) over five finite fan-catalogue
   facts, with the corrected mechanistic threshold law K* = M/2 + 9
   + max(α − f) — exact at six scales including BLIND predictions
   at 112/128 that matched notes/58's direct measurements.  What
   remains of GAP-DICH are catalogue-schema sub-gaps of the same
   species as GAP-FG (notes/57 §7).
3. **GAP-N2 endgame (Case 1).**  Closed per-cell far beyond the
   original crux ({11,12} at ALL 8 residues by verified hand schemas;
   lane laws slide mod 8; template cells across pairs 13..19; C3(p)
   diagonal family p = 5..13), but a complete Case-1 kill needs:
   (a) PARAMETRIC-in-x lane verification (infinitely many pairs at
   once — currently every closed cell is a finite verification),
   (b) the last dyadic cells A4d(19), B6(21) (searches running),
   (c) pairs x ≡ 7 mod 8 (x = 23, 31, ... — outside the e122
   catalogue).
4. **GAP-BRIDGE1 (Case-1 assembly bridge).**  DISCHARGED
   (2026-08-27, notes/52): Theorem B1 — Case-1 teams are not
   permutable, with NO partner hypothesis and NO descent.  The
   diagonal usable pairs {3p, 3p+1}, p ≡ 1 mod 4, fire on exactly the
   dyadic class (e123 flip law) with density 1/12 per block, so a
   clean block above 12C₀+25 always contains a fully-owned pair
   (ownership branch unconditional); "every pair split" punctures
   every block linearly, contradicting cleanliness (split branch
   vacuous); the planned landing-pad well-ordering provably does not
   exist (notes/52 §4.3: splitter fixed point for any finite usable
   family — density is necessary).  Machine: e152_bridge1 (3
   colorings × 2 scales, incl. core-targeted C = 3 punctures, all
   pass).  Residual dependencies (pre-existing tags, sharpened):
   GAP-N2-DIAG (parametric diagonal schema — now THE Case-1 rung
   target) + GAP-N3.  Bonus: Cor B1.2 recovers "ℤ⁺ itself is not
   3-permutable" unconditionally from thm:c3core.
5. **GAP-N3 (dust robustness).**  Exact machine constants (d* = 2/3,
   scale-stable, C = 1 suffices from M = 48) but the one-paragraph
   hand extension of C3 to punctured blocks is unwritten.
6. **GAP-L1' (concentration lemma).**  "Both teams doubling-subcritical
   ⇒ some team keeps near-clean ratio-2 windows" — measured true
   everywhere, no proof; it patrols the dodger corner (subcritical +
   diffuse), the only YES-shape not excluded by known machinery.
7. **Rung finiteness caveat (global).**  Every machine-true rung
   family in the program (STG, chain, seam, coupled) is verified at
   finitely many scales; each use at ω rides on its (b)-style schema
   or on T-PIN with a FIXED finite core — the parametric/hand forms in
   2-3 are what discharge this, and nothing else does.

What broke toward YES this session: nothing new — but the DEATH of
DNP-as-stated (link 1) removed the simplest closing route and is the
honest reason the estimate stays capped: the load-bearing open
statement is now a genuinely new ledger-type claim, not an instance
count.  The only known YES-shape remains the notes/46 dodger
(subcritical + diffuse + pair-sparse + slow P(t)); its requirements
(i)/(ii) pull against each other and no instance is known to exist,
but it is not excluded.

### Honest assessment (updated 2026-08-26, post-merge)

Pre-merge the estimate was NO ≈ 85 % with the cap justified by "Case 2
is untouched and needs new ideas": the finite 2-colored theory had
been SAT at every horizon ever tested, and no candidate infinite
statement existed.  Both halves of that cap broke this session.
Case 2's finite theory now has a firing core whose UNSAT region
WIDENS with scale (critical constant 2 at M = 48, escapes forced into
Case-1 shapes), plus two candidate ledger statements (L1', p(k) → ∞)
that survived adversarial measurement; and the Case-1 crux upgraded
from "machine rung that never fails" to "infinite hand-schema family
with the residue arithmetic predicted and verified".  The whole NO
now hangs on two named, well-shaped gaps (constant-schema scale
stability — compute; the two-seam order hypothesis — mathematics)
rather than on an unexplored regime.  Against: the seam hypothesis
quantifies over arbitrary partitions' order behavior — exactly the
kind of statement that has resisted every compactness-style attempt
this campaign — and a YES could still live in the dodger corner
(subcritical + diffuse), though no such coloring is known to exist.
Current estimate: **NO ≈ 90 %, YES ≈ 10 %** (up from 85: Case 2 went
from untouched to two-gaps-remaining; capped because the remaining
gap is a genuinely new statement, not an instance count).

**Post-second-wave addendum (2026-08-26, late — synthesis session).**
Held at **NO ≈ 90 %**, but the composition changed materially in both
directions.  FOR: G1 is compute-closed and extended (M ≤ 80, critical
constant stable over a 5× range); the M=32 MUS landed fully-minimal
and CONFIRMED the one-schema reduction (Case 2's crux = N2's rung
geometry + one sumset layer), so the program now has ONE schema family
to prove rather than two unrelated cruxes; Case 1 gained its first
all-residue pair.  AGAINST (and why not > 90): the seam hypothesis —
one of the two named gaps — turned out to be FALSE as stated, not
merely unproven; what replaced it (T-FORCE affordability, link 1 of
the ledger above) is better shaped, quantitative, and machine-priced,
but no proof strategy for it has survived contact yet (single-team,
counting, and well-foundedness attacks are all dead ends by
construction), and v*(M)'s growth — the pump the ledger needs — is
measured only as v*(bal,16) ∈ (2,160].  A YES would now have to live
in the dodger corner AND evade the coupled cores at every scale; a NO
still needs every link 1-7 above.  Neither side moved enough to shift
the number.

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
- notes/45-density-cores.md + experiments/e120_density_cores.py,
  e120c3_mus.py — N5 density dials, the C3 two-seam coupled core and
  constant-bound schema; data/e120_*.
- notes/46-ledger.md + experiments/e121_ledger.py — N6 ledger
  statements L1'/L2, price curves p(k), dodger shape; data/e121_A.json,
  e121_B.log.
- N2 (no notes file — reconstructed in the FRONT MERGE section above):
  experiments/e121_n2_mus_sweep.py, e122_n2_residue.py,
  e123_diagonal_schema.py, e123b_diagonal_solver_xval.py,
  e124_family_miner.py (unrun); data/e121_n2_mus.json,
  e122_n2_residue_partial.json (M ≤ 135), e123_diagonal_schema.json,
  e123b_diagonal_xval.json.
- notes/49-offdiagonal.md — N2-OFF: catalogue reconstruction, the
  sliding lane laws, and the two new verified hand schemas ({11,12}
  dyadic K4 + ≡ 2 mod 8 B2), plus the two-ladder template; tools
  experiments/e124_prep_catalogue.py, e124_family_miner.py (fixed +
  run), e124b_lane_probe.py, e124c..e124h (anatomy/discovery chain),
  e124i_k4_schema_verify.py + e124l_b2_schema_verify.py (the
  end-to-end verifiers), e124m_template.py; data/e124*.

### FRONT BRIDGE1 (2026-08-27, night shift): the Case-1 assembly
### bridge is written — notes/52, GAP-BRIDGE1 discharged

Third attempt on this front; no prior partial existed in git.  Full
write-up notes/52-bridge1.md; machine record
experiments/e152_bridge1_check.py + data/e152_bridge1.{json,log}.

- **Theorem B1** [PROVED modulo (H1)]: any team with infinitely many
  C₀-clean dyadic blocks (any constant C₀) is not 3-permutable.  No
  hypothesis on the partner; no dichotomy case survives to need one.
  (H1) = RUNG-DIAG-PUNCT: the diagonal rung R(3p, 3p+1; 2^m, D),
  |D| ≤ C, is UNSAT above a threshold — exactly the union of two
  pre-existing tags (GAP-N2-DIAG: parametric C3(p) write-up, p ≡ 1
  mod 4, dyadic scales only; GAP-N3: dust robustness), with hand
  anchor p = 5, C = 0 (thm:c3core) and machine anchors p = 9, 13 +
  core-targeted C = 3 punctures (e152, M = 128/256).
- **Why the expected hard branch vanished**: the usable supply is
  dense — DIAG-DENSE gives ≥ (2^m−13)/12 disjoint usable pairs per
  block (spacing 12), so bounded dust can never puncture them all
  (ownership always holds), and "every usable pair split" implies
  linear T′-mass in every block, contradicting cleanliness in one
  step (SPLIT-QUANT + B2-VAC).  The task-predicted partner
  inheritance (one value of each crown pair {2^j−1, 2^j} — even-j
  crowns are exactly the p ≡ 5 mod 8 diagonal members, CROWN-2ADIC)
  is real but is used against the hypothesis, not the partner.
- **The descent obstruction** (§4.3, recorded so it is never
  re-attempted): for any FINITE usable family the splitter adversary
  has a fixed point (split the pairs + crowns, donate every
  landing-pad completion — machine coloring χ3), and the landing-pad
  inheritance moves strictly UP in scale — there is no well-ordering
  to found the planned descent on.  An infinite usable family with
  unbounded per-block counts is NECESSARY, and the diagonal family is
  the one with the strongest existing evidence.  Landing pads survive
  as donation-forcing (every dodge makes the clean team cleaner), not
  as kills.
- **Ledger movement**: GAP-BRIDGE1 row CLOSED (notes/50 updated);
  GAP-N2-DIAG promoted to THE Case-1 rung target, ahead of the
  off-diagonal cells (those now matter only for the anchor-free
  variant BRIDGE1-AF, mapped and tagged in notes/52 §5, and for
  catalogue completeness).  Bonus sanity anchor: Cor B1.2 — ℤ⁺ is
  not 3-permutable — falls out UNCONDITIONALLY (p = 5 instance),
  recovering the classical fact through the program's own machinery.
- Numbering note: this session's experiment file is
  e152_bridge1_check.py; a parallel notes/58 session independently
  used e152_dich_probe for an unrelated N6a probe — filenames are
  distinct, only the ordinal collides.

### FRONT LLOP+PARM (2026-08-27, night shift, notes/58): cap/K* laws
### corrected at 112/128, Lemma D3, P-ARM anatomy, robust chain
### verified at 128

Machine (e146/e152/e153/e154/e155/e156, notes/58 §§1, 3.5–3.6, 4.4):

- **Threshold laws at 112/128**: cap(112) = 59, cap(128) = 67 (both
  L-LOP sharp); K*(112) = 60, K*(128) = 68.  BOTH prior laws die:
  the mod-32 K* offsets (notes/56 §3.3) break at 112, the
  ⌊M/32⌋-cap fit breaks at 128.  What replaces them on present
  data: both offsets FLAT ((C−1) − balance = −5, K* − balance = −4
  over 96–128) and K* = cap + 1 EXACTLY at 112 and 128 — the L and
  P arms stay complementary with zero slack; NO GAP-ASM′ hole
  opened at 128 (falsifying the notes/56 §4b projection, in the
  good direction).
- **Lemma D3 (punch-descent, notes/58 §2) [PROVED + machine-audited
  e156]**: straddle-freeness + bounds alone forbid jointly defusing
  the band-major team's α-window AND completion zone — an infinite-
  descent coloring lemma, uniform in all even M ≥ 32.  Th1's kill
  supply is therefore forced; the L-LOP remainder is scoped as
  GAP-LLOP-α/β (H1/J species).
- **P-ARM anatomy (notes/58 §3, e155/e155b/e155c pending)**: under
  the hatch everything reduces classwise at half scale m = M/2:
  Th2 = halved fan theories with NO support caveat; Th0 = one
  ThW0(m) per team with a 7-value guard window CW = [3m−7, 3m−1].
  e155 falsified both first-draft hypotheses and found the real
  structure: (i) the half-scale fan-escape law is a LATTICE law
  (every SAT-alive attacker pair has gap ≡ 0 mod 8 at m = 28–40 —
  fan-safe shares lie in ONE mod-8 class), (ii) ThW0 minus one
  guard group stays UNSAT EXCEPT at completions {4, 6} — exactly
  the values the L-LOP frontier witness defects, (iii) fan-safe
  shares of size ≥ 2 are cliques of the SAT-alive graph: max size
  3–4, explicit families.  P-ARM″ = three-layer conditional proof
  (fan pair / crown / punctured-ThW1′-on-clique-punctures) with
  the single scoped residue GAP-PARM-CORNER; P-ARM machine-holds
  OFF the mod-16 line too (M = 56 UNSAT probe).
- **Robust P-ARM implemented and VERIFIED at 128 (the notes/56 §4b
  designated fix)**: Lemma PH+ [PROVED] (Φ < M+7 forces the pure-U
  alignment and Φ = (M/2)·#defectors exactly); machine chain at
  K_P = 68, d₀ = 4: DICH-U UNSAT (0.9 s), DICH-Z UNSAT (0.2 s),
  RP-ARM(128, 4) UNSAT (10 s, 15.4M clauses; straddles + (0,2,2)
  units live for defectors).  RP-ARM(48, d₀ ≤ 8) all UNSAT.
  ⟹ **Theorem COV-W′(128)**: N6a at 128 through the structured
  bridge WITHOUT the adjacency accident.  M = 160 endgame running
  (catalogue + L-LOP/K* brackets + robust chain).

Ledger deltas: GAP-ASM′ risk DOWN (no hole at 112/128 + verified
robust fix at 128 + notes/59 §D's (OV-∀) reduction); GAP-PARM
reduced to lattice-law + finite punctured-family checks +
GAP-PARM-CORNER; GAP-LLOP gains Lemma D3 (proved base case) and the
frontier witness anatomy tying its α-arm to the same corner as
P-ARM's.  New machine-true finite laws to uniformize: H-LAT (mod-8
lattice law), the {4,6}-droppable-crown table, the ≤ 4 clique bound.

### FRONT AUDIT (2026-08-28, three referee passes: notes/60, notes/60-audit-1, notes/61-audit-2) — ALL FOUR NIGHT-SHIFT FRONTS SOUND

Adversarial referee audits of notes/52 (BRIDGE1), 57 (DICH), 58
(LLOP/PARM), 59 (lowgaps): hand reconstructions of every proof,
independent reimplementations (closure engine for the J-pencil;
alpha/f scanner; fresh DICH probe instrument anchored at M = 96),
fresh adversarial colorings for BRIDGE1, and blind measurements at
scales no session ever touched.  **Verdict: SOUND across the board;
zero broken theorems; two wording fixes (52-G1/52-G2, applied);
one dead extrapolation (notes/58's flat K* law).**  Key movements:

- **The mechanistic K* law won its discriminating test.**  Blind
  protocol at M = 144 and 160: predictions committed before any
  probe; at 160 the notes/57 catalogue law (alpha drops to 2 ⟹
  K* = 83) DISAGREED with both flat-law pre-registrations (84).
  Measured: K*(144) = 76, K*(160) = 83 — the mechanistic law is
  exact at all 8 scales 48..160 with 4 blind hits; the flat-offset
  and mod-32 K* laws are dead.  (Correction to notes/57 prose:
  alpha is NOT monotone in M.)
- **The cap law stayed flat and the feared ASM′ hole never
  materialized** (61-audit-2): cap(144) = 75, cap(160) = 83 (both
  = (M+16)/2 − 5, first out-of-sample wins for the flat cap law);
  adjacency K* = cap+1 is dead as a law (W = 1 at 160) but the
  overlap condition (OV) K* ≤ C now holds at ALL EIGHT measured
  scales — at 160, the predicted hole scale, with margin.
- **Robust chain COV-W′ verified at 160** (on top of the reproduced
  128 chain): L-LOP(160) K = 84 UNSAT + DICH-upure(160,84) +
  DICH-zdef(160,84,4) + RP-ARM(160,4) all UNSAT (29M clauses, 25 s,
  SAT controls passed).  Full bridge chains now at SIX scales
  (48/64/80/96 exact + 128/160 robust); N6a's per-scale machine
  layer is closed everywhere it has been asked.
- **BRIDGE1 cleared**: line-by-line + fresh adversarial batteries
  (greedy-puncture coloring pushing extraction to fresh p = 21 —
  kills at both dyadic scales + dust-on-core robustness = new (H1)
  evidence outside the verified p-layer; hi-half splitter mirror).
  The §4.3 descent post-mortem is honest (fixed point confirmed);
  its two overbroad sentences fixed in place.
- **Lemma J's PROVED status independently re-established** (fresh
  closure engine reproduces all 36 pencil derivations); JP/JP′/Γ
  algebra re-solved by hand (two presentational nits recorded in
  61-audit-2 §5).
- FG-deep cross-scale at 64 RUN (61-audit-2 §5.3): the resonance
  law (8 | gap necessary for escape) CONFIRMED at the second scale —
  but the E1×E1/non-resonant characterization of the deep stalls is
  48-specific (at 64, twelve stalls spill one shoulder below E1 and
  include resonant gaps 8/24); GAP-FG-deep's uniformization target
  restated accordingly.
- Still-unrun carryovers: e155c (ThW1′ puncture tolerance = the
  cap-law mechanism), e156 D3 at 80/112/128, P-arm instances at
  112/144.

**Honest assessment (updated 2026-08-28): NO ≈ 92 %, YES ≈ 8 %**
(up from 90).  Movement FOR: an adversarial audit cycle attacked
every load-bearing night-shift claim and broke nothing structural;
the N6a bridge survived its predicted failure point (160) twice
over; the threshold laws are now mechanistic rather than curve-fit;
Case 1's (H1) gained fresh-p evidence.  Held below higher: the two
genuinely new statements are untouched by all of this — GAP-G2's
T-FORCE ledger (v* brackets still uselessly wide: (4,65] at bal24,
(2,368] at bal32) and the parametric uniformizations (GAP-N2-DIAG,
GAP-DICH/LLOP/PARM species) remain finite-scale records, and the
notes/46 dodger corner is still not excluded.  The audit shrank
risk in the verified layer; it did not shorten the list of unproven
links (still: N2-DIAG, N3, N6a-uniformization pool, G2-ledger,
L1', rung-finiteness).

### FRONT GAP-AFFORD (2026-08-28 afternoon, e158 + notes/62): the
### 4-block downward gadget — GAP-JOINT measured YES at two scales;
### GAP-COMP refuted as counting; first proved arm of the (·,0) schema

Full write-up notes/62-afford.md; machine experiments/e158_joint4.py
(+ e158b MUS, e158c fixed-coloring prober, queue scripts), records
data/e158*.

- **The instrument**: values (M/2, 8M], blocks Bm1/B0/B1/B2, TWO
  overlapping 3-block windows sharing seam s1; per-team budgets vup
  (anchor M: s1+s2) and vdn (anchor M/2: s0+s1).  T-FORCE-4
  (restriction) and L-PROJ (projection to the 3-block instances)
  proved — every UNSAT cell is a joint demand statement for valid
  pairs.
- **GAP-JOINT answered YES — the pump is real, at 2 scales.**
  Baselines: v*(bal,8) = v*(bal,12) = 0 (standalone half-anchors are
  FREE, seam-clean witnesses).  M = 16 triangle: (none,0) SAT [0.8s]
  (clean below by dumping ~400 inversions on s2), (6,none) SAT
  [364s, audited], **(6,0) UNSAT [2.1s]**.  M = 24: (none,0) SAT
  [20.6s], **(65,0) UNSAT [46s]** with 65 = the pod's 3-block SAT
  point.  So paying the upper anchor at 3-block-legal prices forces
  payment at the half-anchor where the standalone price is ZERO —
  the joint demand curve is strictly above the componentwise floors
  [GAP-J-schema, machine-true at 16 and 24].  Attribution clean:
  material alone forces nothing (C2), the upper BUDGET does (C3).
- **Mechanism measured** (C1 witness anatomy): to pay 6 up, the
  coloring voids the entire upper H-family by donation (n_H_up = 0,
  82/78 z-defections) — and the donation pattern seeds 8 mono
  H-triples in the LOWER window, broken by wholesale s0 reversal
  (32 inversions) — donations received in the window have their own
  attack surfaces one block down, exactly the e130/notes/54
  prediction.  Payment: 38 below when below is free.
- **Negative results that shape L-AFFORD** (notes/62 §4): NG4 — no
  family of finite budget cells (forbidden rectangles) can prove
  L-AFFORD (overpay-everywhere dodge); budget gadgets are DEMAND
  instruments only.  GAP-COMP refuted as posed: no sub-vacuous
  compliant-descent threshold exists (parity-oriented descent
  digraphs have zero AP 2-paths at any density; the C1 witness
  realizes it, 334/352 edges, 0 two-paths).  The supply side of the
  ledger must be denominated in DONATIONS (single-use colored
  values), not inversions [GAP-AFFORD′].
- **The (·,0) family by hand** (notes/62 §4c-d): L-PREFIX proved
  (under vdn = 0 the prefix cohort Bm1 taxes the window: μ_dn = 0
  forced; n_s2 ≥ μ_up + μ_skip, edge-disjoint charging; the SKIP
  family (Bm1×B1×B2) is new — no 3-block window ever charged it;
  the H-voiding schedule carries exactly 13M²/64 + M/8 skip mass).
  **Lemma K proved** (an integer interval with its bottom k ≥ 3
  values forced first has no monotone-AP-free order once n ≥ k+6;
  two exhaustive bases + two monotone steps) — giving **Theorem
  SCHED-DEAD**: the unique zero-sumset parity coloring (1,1,0,0) is
  dead under vdn = 0 at EVERY budget and EVERY M ≥ 12 (its low
  parity chain is Lemma K's pattern; machine-confirmed at
  M = 16/24/32 through vup = 512, seconds per query).  First fully
  proved arm of the three-arm (·,0) schema (flood / sumset-mass /
  robustness).
- **MUS**: (16; 6,0) deletion-minimal support n = 50 of 120, 50/50
  necessary; Bm1 and B0 enter COMPLETE, B1 as lower two-thirds
  (3 punctures), B2 collapses to the six-value stub (4M, 4M+6]
  (balance bound 0) — blind prediction (notes/62 §3c) 4/4, with the
  B2 collapse much sharper than predicted.  The (·,0) core is a
  lower-window object with a thin upper boundary family — a small
  hand target.
- **Frontier state**: v_min(0)(16) ∈ (6, 442] (bisection running:
  96/192/384), v_min(0)(24) > 65; forced(x) is DECREASING (C2 kills
  naive multiplicative cascades — notes/62 §5); the growth of
  v_min(0)(M) is the decisive remaining measurement, and
  GAP-AFFORD′ (overpayment ledger) the decisive remaining statement.

### FRONT TELESCOPE (2026-08-29, e173 + notes/70): the boundary
### ledger — GAP-V*-growth made unnecessary, disjointness settled

Full write-up notes/70-telescope.md; machine
experiments/e173_telescope.py, data/e173_* + pod data/tel_*.

- **The right tower**: boundary currency.  On the 2-adic chain
  N_j = N₀·2^j, Inv_T(N_j) = x_{j+1} + x_{j+2} where x_m = inverted
  adjacent-octave pairs at boundary β_m.  L-HOME (each pair at
  exactly one boundary; skip pairs at none — P4 amplifies them),
  L-2PRICE (each boundary priced by exactly the two anchors
  N_{m-1}, N_{m-2}; machine-exact on 10/10 witness records incl. the
  odd-base q=3 chain at 24), **T-LEDGER** (4-adic subchains partition
  the boundary currency EXACTLY — payments there pairwise disjoint;
  full chain double-counts exactly ×2), L-SQUEEZE (no parking:
  Inv(N_j) ≤ Inv(N_{j-1}) + Inv(N_{j+1})), L-ECHO (a zero anchor
  forces the giant v_min(0) payment to echo at TWO consecutive
  anchors above, same team).
- **Naive T-TEL refuted honestly**: consecutive-anchor disjointness
  is FALSE — the C1@16 witness's ENTIRE upper payment (6 pairs, all
  on the shared seam) is simultaneously lower-anchor payment
  (maximal overlap, measured); and P1/NG4 kill any
  divergence-as-contradiction reading (X-INTERLEAVE pays every
  boundary legally).
- **The corrected disjointness (T-FRESH) — machine-true at 16**:
  F(16; 6) (pump cell with the shared seam FREED below, only
  new-boundary currency banned) is **UNSAT [983.5 s]** — cheap upper
  anchors mint fresh β(N)-currency that cannot ride the doubly-priced
  shared seam; mints at distinct anchors sit at distinct boundaries,
  hence pairwise disjoint at EVERY anchor (density 1/octave, no
  factor 2), each with a P3-displaced low member.  Corollary: the
  2-step chain cell U5(16) (6,·,0) UNSAT a fortiori — no parking.
- **T-TEL′ dichotomy [proved modulo GAP-J/F-schema +
  GAP-VMIN0-growth]**: every valid regime-(I) pair either (a) has
  limsup Inv = ∞ (with L-ECHO booking each giant payment twice), or
  (b) pays ≥ 1 with fresh disjoint currency at every large anchor —
  the notes/47 §5.4 covering statement DERIVED.  Either way
  cumulative fresh demand diverges: **GAP-V*-growth is demoted; the
  demand curve is now v_min(0)(M), measurable by cheap deep-UNSAT
  queries** (the near-critical wall does not apply: vdn = 0
  collapses the lower order theory).
- **New measurements**: v_min(0) monotone at FOUR scales —
  **= 12 EXACTLY (@8, bisected: UNSAT ≤ 11, SAT at 12 — the
  program's first exact v_min(0) point)**, > 6/≤ 384 (@16), > 65
  (@24), **> 256 (@32, pod, 137 s)**; and the **const-bounds pump fires**: (6,0)@24 at bounds
  (2,3,6,12) UNSAT [106 s] ⟹ by D1+D2 the pump demand applies at
  EVERY large Case-2 anchor — not a balance artifact.  In flight:
  (512,0)@32, const ladder (65,0)@24 + (100,0)@32, F(24;65), pod
  F(16;6) cross-check.
- **What remains THE gap**: GAP-AFFORD′ unchanged — the supply cap
  must charge, in donation currency, either branch (a)'s echoing
  giant payments or branch (b)'s one-displaced-value-per-octave
  system.  The telescope closes the demand bookkeeping; it cannot
  (NG4) close supply.

### FRONT PUMP-SCHEMA (2026-08-30, e175 + notes/75): the 4-block
### gadget's uniform law — the pump COLLAPSES into the CORE′ engine
### one window down; GAP-VMIN0-growth discharged

Full write-up notes/75-pump-schema.md; machine
experiments/e175_pump_schema.py, data/e175_* (all parts 0 failures).

- **NEST correspondence [PROVED]**: the lower window (M/2, 4M] of
  the 4-block gadget IS the two-seam coupled-core window at anchor
  m = M/2, block for block ((Bm1,B0,B1) = (B0′,B1′,B2′)), and
  vdn = 0 is exactly its block-order hypothesis (transitivity gives
  the outer seam).  Dictionary (notes/75 §2.1): H_dn = the straddle
  family of CI(m); L-PREFIX(i) = Lemma U(m)'s condition (S); the
  parity dodge = A7(a) one level down; vup is charged on the
  S3 = 2×S2 seam-2 wall of CORE′(M) — the (16;6,0)-MUS B2 stub is
  the bottom 6 of S3(16) machine-exactly.
- **Theorem J-DOWN [PROVED — three-line restriction]**: U4(M; v, w)
  UNSAT for EVERY vup whenever the anchor-m 3-block core fires at
  budget w.  Machine: (none,0)@32-bal UNSAT [7.4 s] (THE collapse
  cell), proj@32/48/64 reproduce the e120 half-cores through the
  4-block encoder, and CORE′(48)@96 (bounds (2,2,2,0), vdn = 0)
  UNSAT [39.2 s] — the locked CI(48) engine reached through the
  pump, independent xval of e135.  **GAP-J's (·,0) family at large
  anchors is GAP-N6a verbatim — one schema engine.**
- **Corollary VMIN0**: v_min(0)(M) = ∞ for every M ≥ 32 (bal
  32/48/64 machine; const (2,2,2) 96/128/160 via e125/e126; uniform
  for m ≡ 0 mod 16, m ≥ 48 modulo GAP-N6a + the proved balance→band
  pigeonhole 16/15).  The finite regime is the boot window M ≤ 24:
  v_min(0)(8) = 12 (re-verified fresh: (11,0) UNSAT / (12,0) SAT),
  (6, 384] at 16, (65, 1440] at 24.  [GAP-VMIN0-growth] is
  DISCHARGED BY COLLAPSE — the notes/70 demand curve reverts to the
  budgeted half-core frontier v*₃(m; bounds) [GAP-V*] + the margin
  family.  The queued (512,0)@32 / (512,0)@48 pod cells are MOOT.
- **Parametric geometry [PROVED + machine at 6 scales]**: 4-block
  pattern catalogue (exactly 4 empty patterns), family laws
  |H_up| = 5M²/4, |H_dn| = 5M²/16, |SKIP| = 13M²/16, and Lemma
  LEAK — the C1 witness's '8' is Σ_{z∈leak} c(z) (leak
  {36,40,44,48}, 2 parents each), verified on 5 recorded witnesses.
- **Honest residue**: the margin family U4(2m; v, v*₃(m)+b) (all
  measured pump content lives there; (368,6)@32 still unresolved)
  and the freshness family F(N; v) [GAP-F-schema], which does NOT
  project (one-seam 3-block theories are SAT).  NG4/supply
  [GAP-AFFORD′] untouched.
