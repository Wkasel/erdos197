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
- **Adversarial audit (e115, parallel session; partly still running at
  integration time):** from-scratch closure engine (independent data
  structures) closes every case-tree branch at fresh scales L1 = {204,
  244, 404, 520, 1000}, FLIP = {208, 328, 520, 1000}, with 4-mod-8
  controls correctly NOT closing (engine sanity); e113 schema re-run at
  adversarial scales incl. M = 2048, 4096 — all pass; independent SAT
  encoder confirms L1/C3 UNSAT at M = 404, 408, 520 (larger scales in
  flight).  The one audit failure so far is a KeyError bug in the audit
  script's own Lemma-H bookkeeping check (appendix/halving material,
  not on the Target chain).
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
2. Erdős #197 in general — whether any 2-partition works.  The attack
   calculus (overload of block-bottom slivers by small values) is the
   candidate abstraction; see notes/27 "arc beyond dyadic".

## Key files

- paper/main.tex — full write-up incl. thm:main, thm:c3core (§ The C3
  core theorem and the main theorem).
- notes/33-og-proof.md — the hand proof, machine-check pointers.
- notes/27-dichotomy-ladder.md — the running status ledger (session 10
  = gap closed + audit record).
- experiments/e113_c3_hand_proof.py, e113b_closure_crossval.py,
  e114_theorem_spotcheck.py — verification suite; data/e113*, e114*.
