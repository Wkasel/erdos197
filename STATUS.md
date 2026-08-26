# Erdős #197 campaign — STATUS (2026-08-25)

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

### Best surviving YES-candidate

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

### Decisive next experiments

1. **YES route (H4)**: growing-sliver swap generator + full g2 screen
   suite at 2^16–2^20, schedules s_t ∈ {t, 2^{t/2}, Geneson-matched};
   any clean survivor goes to chunk-stage SAT at m=4 locally, m=5 on
   RunPod (~25M clauses, streaming DIMACS).
2. **NO route (e120)**: joint multi-pair consistency gadget — attackers
   {2^j−1, 2^j} for j = 4, 5, 6 all colored, blocks at two adjacent
   scales simultaneously, asking whether split/park choices can be made
   consistently and at what total donation price; plus finish mindon4
   (budget 5+) and the m=5 same-mode CAP=0 run (does the block-poor
   escape survive when the minority team's own crown pairs bite?).

### Honest assessment

Every natural candidate partition is now dead, several unconditionally;
the conserved-attack-surface principle and the strictly-rising
multi-crown price point toward NO.  Against that: the finite theory is
SAT everywhere with composable escapes, the growing-sliver shape is
genuinely untested, and lem:orbit's finite-reflector hypothesis is a
real gap in the death machinery.  Current estimate: **NO ≈ 65–70 %,
YES ≈ 30–35 %**, with the growing-sliver screen (H4) the cheapest
experiment most likely to move the estimate in either direction.

## Key files

- paper/main.tex — full write-up incl. thm:main, thm:c3core (§ The C3
  core theorem and the main theorem).
- notes/33-og-proof.md — the hand proof, machine-check pointers.
- notes/27-dichotomy-ladder.md — the running status ledger (session 10
  = gap closed + audit record).
- experiments/e113_c3_hand_proof.py, e113b_closure_crossval.py,
  e114_theorem_spotcheck.py — verification suite; data/e113*, e114*.
