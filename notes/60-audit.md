# 60 — Night-2 audit: adversarial verification of notes/52, 57, 58, 59 + assembly

Referee shift (2026-08-28).  Mandate: reconstruct the four night-shift
fronts' arguments independently, machine-check at scales the authors
did NOT use, complete the lost M = 160 endgame (the e146(160) build
was in flight at handoff and never landed — data/ has no
e146_catalogue_M160.json; the queued e152/e153/e154(160) probes and
e155c never ran), then update the ledgers.  A gap clears here only if
I would defend it as referee.

Written incrementally; every section ends with a verdict tag
[CONFIRMED] / [CONFIRMED WITH CORRECTION] / [REFUTED] / [NOT CHECKED].
Audit instruments live in audit/a7_night2/; new solver data in data/
with the e157+ prefix to avoid ordinal collisions.

## 0. Scope and inputs

Audited artifacts: notes/52 (BRIDGE1), notes/57 (GAP-DICH), notes/58
(GAP-LLOP/PARM + robust P-ARM), notes/59 (low gaps + Theorem ASM′),
against the proved layer of notes/55/56.  All night-shift logs in
data/ re-read and cross-checked against the notes' claims (e152_llop,
e153_dich_lemmas + _112_128, e153_dich_probes, e154_rparm,
e154_dich_split, e156_d3, e152_bridge1, e152_mc_schema, e153_j_pencil,
e154_deep_classify, e154b, e155_parm_hyp): NO discrepancy between any
note claim and its cited log found.  [CONFIRMED at the
bookkeeping level; substantive checks below.]

Planned checks (status filled in as sections land):

1. §1 Hand reconstruction, DICH front: Lemma T / FI / ANCHOR / COLL /
   H-DICH counting; K* formula arithmetic at all six measured scales.
2. §2 Hand reconstruction, LLOP/PARM front: Lemma AO / D3 (full range
   audit at fresh scales) / PH+ / PARM-HALVE bookkeeping / COV-W′
   composition.
3. §3 Hand reconstruction, LOWGAPS front: Lemma CC soundness, Γ₂′
   algebra, S6/JP/JP′ enumeration vs Lemma J's minimal sets,
   ASM′ composition logic.
4. §4 Hand reconstruction, BRIDGE1: PIN / DIAG-DENSE / CROWN-2ADIC /
   B1 counting / descent obstruction.
5. §5 NEW-SCALE machine tests: M = 144 (a scale NO session ever
   touched — blind test of the notes/57 mechanistic K* law AND the
   notes/58 flat-offset cap law, which DISAGREE with the dead mod-32
   law there), M = 160 (the pre-registered endgame: C = 84, K* = 84
   predicted), e156 D3 at 80/112, e155c (pre-registered ThW1′
   puncture-tolerance prediction), deep-classify resonance law at 64.
6. §6 Ledger updates + final inventory.
