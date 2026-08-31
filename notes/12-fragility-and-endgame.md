> **ARCHIVAL / SUPERSEDED. Contains statements later shown false. Do not use as a dependency. See paper/main.tex and STATUS.md for the current formulation.**
>
> **SUPERSEDED — THE FRAGILITY INTERPRETATION IS WITHDRAWN
> (KNOWN OVERCLAIMED AS STATED).**  notes/14: radius-1 robustness
> fails generically in 3-AP-arrangement systems (including
> settings with known infinite constructions), so item 3's
> "fragility theorem" consequences — "all
> pumping-by-approximation is dead", "rules out Lipschitz-like
> rules" — are NOT valid inferences about #197.  Even the weaker
> Lipschitz statement was later demoted to a recorded observation
> (paper fix, commit 59655a9).  The SAT/UNSAT rows themselves
> (selfsim-1024 SAT, witness-fixed 4096 UNSAT) stand as data.
> (Review remediation notes/88 item 4.)

# Fragility and the 4096 endgame (2026-08-24 late night)

## Established this stretch
1. **selfsim-1024 SAT, audited clean** (0 AP-violations, 0 invariance-violations;
   pysat 28 min after CP-SAT UNKNOWN at 2h). Eventual-selfsim variant also SAT.
2. **Witness-fixed selfsim-4096: UNSAT** (676s, genuine): the audited 1024
   witness is a dead branch even at the self-similar level.
3. **Fragility theorem (empirical, machine-certified at 256):** robust variants
   — requiring completions' ±1/±2 in-block S-neighbors to also precede — are
   UNSAT even at radius 1, even without invariance. Valid arrangements are
   knife-edge exact. Consequences:
   - All pumping-by-approximation (anchor descent with rounding drift) is dead:
     drift ≥ 1 cannot be absorbed. Any pumping proof must be drift-free/exact.
   - Rules out Lipschitz-like construction rules (positions can't vary slowly
     in value).
4. Macro-property "top quarter before bottom quarter" is FALSE in witnesses
   (half the pairs inverted) while exact Z(y)-conditions hold — fine braiding
   is essential, not an artifact.

## The decisive computations now running
- pure-complete-4096 (n=2730): UNSAT would kill the dyadic partition outright
  (then: perturbation harness e40 + ray-piercing rigidity → general-NO bridge).
- free selfsim-4096: UNSAT would cap exact self-similarity at 1024 (no uniform
  pumping); SAT would revive the transition-repetition program with new witness
  pairs.

## Honest posture
YES-paths remaining: non-uniform towers (König guarantees existence of viable
branches if pure-X stays SAT forever — but navigating/证明 them requires ideas
beyond finite SAT); exact drift-free pumping (needs algebraic miracle).
NO-paths remaining: pure-X UNSAT at some scale (decidable, running); or a new
infinite-descent argument exploiting fragility (every valid arrangement
separates adjacent values across pivots — quantify accumulation?).
The problem is fighting back exactly as a 47-year-old problem should.

## Fragility universality (machine-certified, all families)
ratio 2/3/4/8 alternating-interval partitions: plain pure systems all SAT
(n up to 819), radius-1 robust versions ALL UNSAT. Fragility is intrinsic to
the two-set problem. Consequences: no partition offers a drift-tolerant
pumpable tower; exact self-similar towers are the only uniform YES-route
(dented by witness-fixed-4096 UNSAT); fragility-accumulation is the most
promising uncharted NO-route (each scale forces tight separations (z ≺ y ≺ z+1);
do separations compose into an infinite descent? — tomorrow's question).
