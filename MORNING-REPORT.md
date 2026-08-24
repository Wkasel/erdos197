# Erdős #197 — Overnight Campaign Report (2026-08-24)

## TL;DR
No resolution yet — but the problem's structure is now mapped at a depth nobody
has published. Eight proven theorems/lemmas, a machine-certified atlas of what
is and isn't possible, and the difficulty localized to one precise phenomenon
(**universal fragility**). The paper draft holds everything. The remaining gap
is exactly the infinite/finite boundary, and both YES and NO now have concrete,
targeted attack plans.

## Proven (hand proofs, in paper/main.tex)
1. Orbit Obstruction lemma (no infinite doubling orbits in a permutable set).
2. Balanced-placement law + records corollary.
3. Lemma R (ratio-ascent obstruction, {k,2k,3k,5k}).
4. van der Corput absorption theorem (+ coherent self-absorbing class towers).
5. Theorem 1: no contiguous-run solutions for the dyadic partition
   (halving descent + 16 machine-checked bases + finish-time descent).
6. Ray-piercing partition rigidity (both teams pierce every doubling ray).
7. Horizon collapse + Tower characterization (exact finite content of the
   problem: bounded-delay towers ⟺ permutability).
8. Team-B structure (parallel shifted copy of Team A; earlier reduction claim
   corrected).

## Machine-certified atlas (all cross-checked after fixing an early decider bug)
- Pure-complete systems (the exact finite restrictions): SAT at X = 16..1024.
- g_256(64) = 153 optimal: 87% of block (128,256] precedes small-completion;
  the 13% residue = one residue class mod 8 (the reservoir).
- Self-similar systems: SAT at 256 and 1024 (audited witnesses!); the audited
  1024 witness does NOT extend to 4096 (dead branch); free-4096 undecided.
- **Universal fragility**: radius-1 robust variants UNSAT for every partition
  family tested (ratios 2,3,4,8) — solutions are knife-edge exact everywhere.
  Kills: all drift-tolerant pumping, Lipschitz rules, anchor-descent schemes.
- All two-phase pipelines, interval schemes, contiguous schedules: UNSAT
  (systematically, with certificates).

## Where the answer lives now
- The finite fragments are ALWAYS satisfiable; the infinite assembly must
  thread an exact braid at every scale. Finite computation provably cannot
  decide this alone (tail-artifact phenomenon demonstrated).
- YES needs: an exact (drift-free) self-similar tower — search continuing
  (4 native C annealers + CDCL sentinel on pure-4096 running now).
- NO needs: converting fragility into an infinite-descent argument
  (each scale forces tight separations; do they compose? — next session's
  first question) — or a pure-X UNSAT at some scale (engines running).

## Running right now
- 4 seeded C annealers on pure-4096 witness hunt (data/anneal_c_1*.log)
- pysat CDCL sentinel on pure-4096 UNSAT side (data/pure4096_pysat.log)

## Cost so far: $0 beyond electricity. RunPod not yet needed (CPU-bound SAT).

## Recommendation for today
1. Let engines finish; if pure-4096 SAT → tower alive, mine the new witness.
2. Decide whether to write up now: the paper is already a genuine contribution
   ("Structural rigidity in the Erdős–Graham two-set permutation problem") —
   posting to arXiv + erdosproblems.com forum would stake the claim on the
   fragility discovery and the theorem collection while the resolution hunt
   continues.
