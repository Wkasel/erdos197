# Erdős #197 campaign — STATUS (2026-08-26, post-N2/N5/N6 front merge)

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
   UNSAT [629 s], data/e125_m64.log — stable over 16..64, a 2.7×
   range beyond the discovery scale for the critical constant.  What
   remains on this side is the hand schema (MUS front, notes/48), not
   compute.
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

### Unresolved runs at merge (all processes now stopped)

(2,2,2)@M=64; C3-balanced MUS at M=32 (reached n=118 of 224, still
dropping); e121 chain-pair price curves + M=128 + counterfactual
probes (Part C log empty); e120 chain M=96 near-critical k=87; Part E
M=64 28/32; Part D 48/64; e124 miner never started.

### Decisive next experiments (post-merge ordering, one per front)

1. **N6 (now the program's critical path)**: attack the double
   non-procrastination hypothesis — formalize L-DESC at two seams
   (re-descent = the procrastinator's own exposure; give it a rung
   family) — with the cheap prerequisite of rerunning (2,2,2)/(3,6,12)
   at M = 64 (RunPod) and finishing the balanced-core MUS at M = 32 →
   hand schema for the sumset/range lemma.
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
