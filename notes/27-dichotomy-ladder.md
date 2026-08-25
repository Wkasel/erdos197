# The dichotomy ladder (session 6)

## The NO-theorem template (rigorous modulo the ladder)
Let L(m) := min over all stage schemes at horizon 4^m (any displacements
δ(v) = s(v) − block(v)/2 ≥ 0) of max_{v ≤ 16} δ(v).

**If L(m) → ∞ then S_A is not 3-permutable.** Proof: an infinite scheme
assigns each of the ten values v ≤ 16 a FIXED finite displacement; its
restriction to horizon 4^m is a valid finite scheme whose low-value
displacements are those constants — contradicting L(m) ≥ m−2 for large m.
(Chunk reduction is exact, so non-existence of schemes = non-permutability.)

## Machine rungs so far
- L(3) ≤ 1 (witness, e75: δ(15)=0 feasible at 64; window-1 opt at 64).
- **L(4) ≥ 2** (e77: capping δ ≤ 1 on all v ≤ 16, rest free ≤ 8:
  INFEASIBLE at 256, 252s CP-SAT). pysat cross-check running (e82).
- L(5) ≥ 3? — e78 running on fleet5 (cap ≤ 2 at 1024, rest free).
- Minimal coalition at m=4 being extracted (e81): which low values'
  caps drive infeasibility (deletion loop).

## Free-space structure findings
- δ(15) ≥ 2 is NOT forced in free space (e75/e76: feasible with 15 at
  natural stage — window-2's {15}-MUS was window-specific). The burden
  moves (δ(4)=3 in the m=4 free optimum): it's a COALITION property, not
  a single-value property. Hence L uses max over the low set.
- Free-space minimal skeleton (kept-at-natural): K_s = {v ≡ 2^s−1 mod 2^s}
  ∩ escape zone = {3} ≺ {11,15} ≺ {47,55,63} — the trailing-ones classes.
  Class-closed; K-attackers' completions land in K (self-protecting).
- K-scheme with lag-2 dump: fiber-4 UNSAT via the half-class traitors
  (sub-escape ≡ −1 mod 2^{s−1} values reflecting K_s pairs from a later
  stage: cycle 191<239<207<191, hand-verified). Full-class version breaks
  (A) at (55,143,231): reflections drop to the parent class ≡ −1 mod 2^{s−1}
  — the class tower needs R-comparator-style ORDER-side protection, which
  rigid stages cannot express. Every closed-form rescue so far dies one
  level up: consistent with L(m) growth being genuine.

## If the ladder holds — the arc beyond dyadic
Dyadic NO kills the natural candidate + the LV-refutation route. The attack
calculus (small values attack every block's bottom sliver; overload forces
displacement growth) may abstract to arbitrary teams: (1) finish dyadic NO;
(2) abstract attack-overload lemma; (3) every 2-partition has a side meeting
overload at all scales ⟹ Erdős #197 = NO. Step 3 is where DEGS/HS ray
methods would combine with density pigeonholing (why 3 teams escape: block
rotation breaks attack chains).

## Coalition extraction (e81, in progress)
Deletion order 3,4,9,10,11,12,13,14 — ALL droppable (UNSAT persists with
caps only on the remainder). Interim: the free-space divergence coalition at
N=256 is ⊆ {15, 16} — the top of block 4. Consistent with (i) the top-half
non-deferrability characterization, (ii) the window-2 MUS {15}, (iii) the
2024-era prediction that block tops (16, 64, 256) are the divergence locus.
Awaiting final drop-15 / drop-16 tests.

## FINAL COALITION (e81 complete): {15, 16} EXACTLY
Jointly UNSAT capped at δ≤1 (rest free ≤8) at N=256; either alone droppable
(SAT). So: **every scheme at 256 has δ(15) ≥ 2 or δ(16) ≥ 2.**
15 = 1111₂ = crown of the ≡−1 (K/odd) tower; 16 = 10000₂ = block top =
crown of the ≡0 (C/even) tower. The two defense skeletons are mutually
limiting: a scheme protects the block hierarchy with one crown early only by
diving the other. Refined divergence conjecture:
    max(δ(15), δ(16)) ≥ m − 2  at horizon 4^m  (⟹ S_A not permutable).
Crown rung at m=5 (cap {15,16} ≤ 2, rest free): e84 launched.
Cross-refs: window-2 MUS {15} (window space); e76 (cap 15 → δ(16)=2 dive);
prediction "block tops = divergence locus" (notes/09, session 2).

## CROWN THEOREM (two rungs, machine-certified)
- N=256: cap δ(15),δ(16) ≤ 1, rest free ≤ 8: INFEASIBLE ⟹ max(δ15,δ16) ≥ 2.
- N=1024: cap ≤ 2, rest free ≤ 8: UNSAT (pysat 5181s, 69 rounds)
  ⟹ **max(δ(15), δ(16)) ≥ 3.**
Reframed: the crowns must reach the top block's stage-region at every
horizon (δ ≥ m−2 ⟺ stage ≥ m). If this holds ∀m: S_A not permutable
(two fixed values, finite displacements, restriction contradiction).
Robustness run: DMAX=14 rerun at 1024 (exclude ceiling artifacts) — running.
Crown rung 3 (N=4096, cap ≤ 3): launched fleet5.

## The cascade mechanism (hand, toward the induction)
Deferring block-6 crowns (60, 64) to stage σ forces, per witness pair
(x ∈ block 4, midpoint (x+60)/2 ∈ {35..38} ⊂ block-6 bottom): either the
midpoint defers to ≥ σ too, or the block-4 attacker x rises above the
midpoint's stage. So high crowns drag either (i) a block-4 value upward
(→ its own crown pressure) or (ii) growing bottom-mass of block 6 up to σ,
which re-attacks block 6's top sliver and recurses. Target formal lemma:
deferred mass at stage σ in block 2t forces (crown of block 2t−2 at ≥ σ−c)
or (positive-fraction of block 2t−2 at ≥ σ−1) — mass exhaustion over m
scales then yields the crown divergence. Bookkeeping in progress.

## THE ORDER GADGET (session 7 — the breakthrough)
Family-MUS of crown-cap infeasibility at 256 = {atk15:8, atk16:8, blk:8}:
single-block! And within one block the stage machinery collapses (stages +
fiber orders ⟺ one total order of the block; the case table degenerates to
plain non-monotonicity + attack precedences). Hence:

**Crown theorem at horizon 4^m ⟸ OG_{2m} infeasible** (this direction is
what the NO route uses and it is unconditional; the converse — rebuilding a
full capped scheme from an OG witness — is justified only by the e86
family-MUS at 256 being single-block and is UNPROVEN at other scales; do
not state it as an equivalence), where OG_K is the
pure order problem: order block (M, 2M] (M = 2^{K−1}) with (i) all in-block
AP triples non-monotone, (ii) attack precedences t_{15−2j} ≺ b_j and
t_{16−2j} ≺ b_j (b_j = M+j, t_i = 2M−i): each of the bottom-eight values
guarded by an adjacent top PAIR {t_{15−2j}, t_{16−2j}} (b_8 by t_0 alone).

Machine: OG_8 UNSAT (2s); drop either attack family → SAT (both crowns
essential ✓ matches coalition); **OG_10 UNSAT (108s)**; OG_12 running.

**If OG_K is UNSAT for infinitely many even K ≥ 8, then S_A IS NOT
PERMUTABLE.**  CORRECTED ARGUMENT (the old phrasing "some crown has stage
≥ t for every t" tacitly assumed δ ≥ 0, which arbitrary chunkings do not
give; use the finite-fiber overflow directly — repair verified in
e96_reduction_check and written up in paper/main.tex, section "The order
gadget and the main theorem"): in any valid scheme, for each block B_{2t}
with OG(2^{2t−1}) UNSAT, NOT all eight bottom values b_1..b_8 can have
stage > max(s(15), s(16)) — otherwise the induced block order satisfies
all of OG (in-block APs non-monotone unconditionally; each attack
t_{x−2j} ≺ b_j forced whenever s(x) < s(b_j) via (A) + the
s(x)<s(y)=s(z) ⟹ z≺y row of (B)) — so some bottom-eight value has stage
≤ max(s(15), s(16)); infinitely many such blocks put infinitely many
distinct values into the finitely many finite fibers below that stage.
Contradiction, with NO normalization needed.  (Note the per-block
condition consumed is "some bottom-eight value dives", weaker than
"crown below the whole block"; and "infinitely many K" suffices — the
hypothesis need not cover all K.)  Even simpler, the whole argument runs
directly on the permutation with singleton chunks: P = max(pos(15),
pos(16)); if every bottom-eight of a block sits after position P, the
position order restricted to the block satisfies OG.  The remaining
mathematics is ONE scale-uniform statement about interval orders.
Triple-level MUS of OG_8
extracting now (e88) — target: a scale-invariant finite pattern + hand proof.
Note: guard pairs' downward completions 2b_j − t = 16 leave the block —
the gadget is genuinely self-contained (crowns appear only as the numbers
15, 16 in the offsets).

## Late fleet verdicts (batch)
- LADDER X=256 d=2 (free extras): SAT (42559s) — weak necessary condition
  passes, as expected.
- LAW X=64 d=3 (law-pinned): UNSAT (48064s) — the ≡2 mod 2^{k/2} defect law
  is definitively wrong/too rigid at (64, d3); the law frame is closed.
  (Chunk/OG frame superseded it; this is consistency, not news.)

## STATUS LEDGER (session 8 — post-verification integration)

PROVEN UNCONDITIONALLY (hand proofs, machine-audited; written up in
paper/main.tex "The order gadget and the main theorem"):
- Reduction theorem: if OG(2^{2t−1}) is infeasible for infinitely many
  t ≥ 4, then S_A is not 3-permutable.  Proof = per-block dichotomy +
  finite-fiber overflow (corrected pigeonhole above; no δ ≥ 0
  normalization needed).  Component checks: e96_reduction_check (boundary
  arithmetic, chunk case table exhaustive, attack forcing, normalization),
  plus verifier reconstruction of thm:chunk row by row.
- Normalization lemma (running-max chunking ⟹ WLOG δ ≥ 0, finite
  fibers) — needed by thm:divergence's restriction step, now stated and
  proved in the paper (chunk section); the OG route does NOT need it.

MACHINE-VERIFIED (Cadical195; lazy transitivity cross-validated against
eager encodings):
- OG(M) UNSAT at EVERY tested scale: all of M = 16..200, plus M = 128
  (eager re-check e96, 1s) and M = 512 (re-run 75s).  Gadget degenerates
  below M = 16.  M = 2048 unresolved (og_12: 200+ rounds, no verdict).
- Of the dyadic family {128, 512, 2048, 8192, ...} needed by the
  reduction: only 128 and 512 are verified.  No finite sweep can
  discharge the hypothesis (supports grow with M — notes/30 G1).
- Crown ladder rungs: L(4) = 2, L(5) = 3; crown coalition {15,16} exact
  at 256; max(δ15, δ16) ≥ 3 at 1024.

THE ONE REMAINING MATHEMATICAL GAP (NO route):
- [CLOSED — session 10, see below] Scale-uniform OG infeasibility
  (sharpest target: the C3 core {t₅≺b₅, t₃≺b₆, t₁₀≺b₃} on M ≡ 0 mod 8
  — notes/30 S8).  Historical parametric status: notes/30.

SUPERSEDED / CLOSED FRAMES: defect law (above); note-28 M=40 kernel
66<53 does not lift (notes/30 G4); j = 7 final-attack identity not
universal (notes/30 G5); lemma layer O1–O8 is M ≡ 0 (mod 4) only
(notes/30 G6 — reverse-forced elsewhere).

## STATUS LEDGER (session 10 — THE GAP IS CLOSED; MAIN THEOREM PROVEN)

notes/33 v2 contains the complete hand proof of the C3 core: for every
M ≡ 0 (mod 8), M ≥ 16, AP-freeness + C3 is contradictory.  Toolkit:
Lemma Z (zigzag), Lemma D (phase dichotomy), Lemma E (transfer lock),
Lemma P (mirror flood; the mod-8 lock is the center-class condition on
m₀ ± 1).  Theorem L1 (A2+A3 force b₅≺b₃, t₃≺t₅ at M ≡ 0 mod 4, M ≥ 12)
+ Theorem FLIP (then A1 is contradictory at M ≡ 0 mod 8, M ≥ 16).

AUDIT (integration session, 2026-08-25): e113 strict schema checker
re-run fresh — layer1 100/100 scales (12..400 + 512, 1024), flip 51/51
(16..400 + 512, 1024), sharpness 35/35, zero failures.  e113b closure
cross-validation re-run fresh — 51/51 + 27/27, zero failures.  NEW
e114_theorem_spotcheck: independent end-to-end SAT checks of the theorem
STATEMENTS at scales never touched by any discovery loop — L1 forcing
UNSAT at M = 148, 212, 264; C3 UNSAT at M = 264, 328; sharpness SAT at
M = 268, 332.  Hand-trace of Z/D/E/P residue arithmetic, mirror APs
(b₃+t₅ = 2(m₀−1), b₅+t₃ = 2(m₀+1), mirrors t₁/t₅/t₇/b₇/M+8/2M−4
in-block), and case-detachment logic: no gaps found.  VERDICT: SOUND.
Parallel adversarial audit (e115, separate session, interim at
integration time): independent closure engine closes all branches at
fresh scales up to M = 1000 with sane 4-mod-8 controls; e113 schema
passes at adversarial M = 2048, 4096; independent SAT encoder concurs
at M = 404, 408, 520 (bigger scales still running).

CONSEQUENCE (now unconditional, in paper/main.tex thm:main):
    S_A IS NOT 3-PERMUTABLE — the canonical dyadic partition does not
    resolve Erdős #197.
Chain: C3 core (thm:c3core, hand) ⟹ OG(M) infeasible ∀ M ≡ 0 mod 8,
M ≥ 16 (C3 ⊂ attack list, (i) = AP-freeness) ⟹ [thm:ogred,
unconditional reduction, audited e96] S_A not 3-permutable.  Every
dyadic scale 2^{2t−1}, t ≥ 4 is ≡ 0 mod 8 and ≥ 128.

STILL OPEN (not needed for the main theorem): full OG infeasibility at
residues ≢ 0 mod 8 (C3 satisfiable there; other attack subsets take
over); Erdős #197 itself (other 2-partitions undecided).  The crown
ladder / displacement-divergence program (this note's original frame) is
SUBSUMED: the OG route delivered the theorem without needing L(m) → ∞.
