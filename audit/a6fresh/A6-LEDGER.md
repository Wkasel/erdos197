# AUDIT A6 — independent re-proof ledger

Protocol: derivations + encoders written from paper/main.tex definitions only
(def:og, sec:c3 statements); notes/33 proof bodies read only afterwards.
Code: a6_encoder.py (SAT, Cadical195; eager O(n^3) transitivity at M<=200,
lazy refinement at M=1000 — sound for UNSAT), a6_engine.py (no SAT solver:
parity union-find over AP xor constraints + bitset transitive closure +
hand-proof-guided DPLL splits), a6_flipsteps.py (step-granular FLIP audit).

## Independent hand derivation (before reading notes/33 proofs)

Lemma E: odd d=2 ladder w_i = M+1+2i; consecutive-rung orientation is an
alternating xor chain (midpoint rule on (w_i,w_{i+1},w_{i+2})); with
b3=w_1, b5=w_2, t5=w_{M/2-3}, t3=w_{M/2-2}, parity of the chain distance
M/2-4 == M/2 (mod 2) gives, at M == 0 mod 4: b5<b3 <=> t3<t5.
A2/A3 unused; no transitivity needed. Confirmed: both mismatched
orientations are refuted by unit xor propagation alone (1 lazy round /
0.0s parity propagation, every scale tested incl. M=1000).

FLIP at M=48 skeleton independently reconstructed (case split on (72,91);
chains 71<86<51, AP(51,71,91), 69/73<71 class-A flood -> 53<71 vs 71<53;
mirror case with 54<73, AP(53,73,93), 73<91 class-B flood). Verified.

## Machine results (all AGREE, zero disagreements)

SAT eager (Cadical195): M = 16, 24, 32, 40, 48, 56, 104, 200:
  E1 (AP + b5<b3 + t5<t3)            UNSAT  \  Lemma E, strong form
  E2 (AP + b3<b5 + t3<t5)            UNSAT  /  (no A2/A3 hypotheses)
  E1h/E2h (with A2+A3, task form)    UNSAT (M=48,56,104,200)
  F  (AP + A2 + A3 + b5<b3 + A1)     UNSAT      FLIP
  Fs (AP + A2 + A3 + b5<b3, no A1)   SAT        FLIP non-vacuous
  C3 (AP + A1 + A2 + A3)             UNSAT      thm:c3core instance
  T0 (AP alone)                      SAT        encoder sanity
Controls: M=52 (== 4 mod 8): C3 SAT (sharpness, matches prop:cores).
  M=46,54 (== 2 mod 4): shifted lock b5<b3 <=> t5<t3 confirmed
  (both mismatches UNSAT, matched orientation SAT).
Sanity: odd-before-even recursive order verified AP-clause-free at 48,56.

Engine (no SAT): M = 48, 56, 104, 200: E1, E2, F, C3 all UNSAT (AGREE).
M = 1000: E1, E2 UNSAT instantly; F/C3 see out_engine_M1000.log.

Lazy SAT M = 1000: E1, E2 UNSAT in 1 round (xor units only);
F/C3 see out_sat_M1000.log.

FLIP step-granular audit (M = 48, 104): 15/15 AGREE — each numbered
step of notes/33 sec.5 Case I/II individually forced from exactly the
hypotheses the proof cites (POLAR floods, P2 floods I.1/II.1, midpoint
steps I.3/II.3, G4 floods I.5/II.5), and both case ambients SAT.

## Line-by-line verdicts: notes/33 Lemma E and FLIP — see audit report.
No errors found. Two cosmetic notes:
(1) Lemma E is stated for all even M but the four listed rungs collide
    for M <= 10 (e.g. t5 = b3 at M = 8); all uses are at M >= 12 where
    they are distinct — suggest adding "M >= 12" to the statement.
(2) Lemma Z's induction step tacitly handles ladder-boundary rungs
    ("leads both" = leads existing neighbors); harmless as used.
