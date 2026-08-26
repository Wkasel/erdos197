# V: tuned per-parity schedules + adversarial re-verification — the growing-sliver verdict

## Question
S1/G3 (notes/38) found the first clean partition team ever — geo_nat/A
under s_t = 2^{floor(t/2)} — clean precisely because d_t = 2 s_t − s_{t+1}
splits by parity: d_even → ∞ (A's kept bottoms recede) and d_odd ≡ 0
(A's received slivers are one-way).  Its partner B died on both surfaces.
TASK V: (1) tune — can a PER-PARITY donation schedule hand BOTH teams
what A got (donated depth growing on every block, kept bottoms receding
on all blocks of both teams)?  (2) verify — re-derive every S1 death
certificate with fresh code; then deliver the family verdict.

**Answers: (1) No.  Six tuned per-parity schedules, all six dead, every
per-team verdict exactly as the d_t law predicts (12/12).  The law is
parity-pointwise, so per-parity tuning has no room: on each octave-parity
class the class owner is safe iff d_t → ∞ there while the class receiver
is safe iff d_t stays below its smallest member — one dial, two hands.
(2) All S1 certificates verified by independent code; the one WIP failure
(geo/B ray extension) was a search-budget artifact, now fixed — the ray
is real to octave 80.  VERDICT: the growing-sliver swap — the last
surviving shape — is dead at every schedule, uniform or per-parity.
The octave-alternating sliver-swap program is closed.**

## 1. The tuned screen (experiments/v2_tuned_screen.py)

Six schedules, natural crowns only (S1 already showed splitting is never
free), both teams, horizons 2^12/2^15/2^18, full g3 instrument suite +
pure-complete SAT (all SAT, ABJ-verified, CDCL cross-check at 2^12):

| tune | d_even, d_odd | team A at 2^18 | team B at 2^18 | law match |
|---|---|---|---|---|
| geomix  s = 2^{t/2+1} ev, 3·2^{(t-1)/2} od | 2^{t/2}, 2^{(t+1)/2} | DEAD CROWNP (recv) | DEAD CROWNP (recv) | 2/2 |
| geomirror  s = 2^{floor((t-1)/2)} | 0, 2^{(t-1)/2} | DEAD CROWNP+ORBIT | **CLEAN** | 2/2 |
| geo3  s = 2^{floor(t/3)} | 0 at t≡2 (3), else 2^{t/3} | DEAD CROWNP | DEAD CROWN+CROWNP | 2/2 |
| addgeo  s = 2^{floor(t/2)} + t | ~2^{t/2}, t−1 | DEAD CROWNP | DEAD CROWN+CROWNP | 2/2 |
| linmix  s = 3t ev, 2t od | 4t−2, t−3 | DEAD CROWNP+ORBIT | DEAD CROWN+CROWNP+ORBIT | 2/2 |
| neck2  s = floor(7·2^t/128)+2 | 2, 2 | DEAD CROWNP (kept) | DEAD CROWN+CROWNP+ORBIT | 2/2 |

Both-teams-clean survivors: **NONE** (so the 2^20 + coupled-displacement
escalation clause never triggered).

Reading of the table:
- **geomix / addgeo / linmix** are the task's target tune — d_t → ∞ on
  BOTH classes, i.e. both teams' kept bottoms recede on all their blocks.
  Exactly as the law forces, the SAME growth arms every fixed attacker
  against both received-sliver surfaces: both teams die as receivers
  (CROWNP at ~100 % of partner-parity octaves).  Growth given to every
  owner is growth given against every receiver.
- **geomirror** is the parity mirror of geo and produces the SECOND clean
  partition team of the campaign — team B this time (no orbit, no ray, no
  crown; only the benign ADAPT-kept-bottom bounded-description family,
  same as geo/A).  Cleanliness is symmetric and cheap for ONE team;
  the partner is doubly dead both times.  One dial, two hands.
- **geo3** shows a mod-3 stall pattern cannot dodge the mod-2 team
  assignment: the d = 0 stalls at t ≡ 2 (mod 3) alternate parity, giving
  BOTH teams infinitely many open kept bottoms AND infinitely many hot
  received slivers.
- **neck2** (constant neck d ≡ 2) is the bounded-neck corner: every
  in-team x ≥ 4 pierces every own-parity interval — the RUNG-IN/T-PIN
  regime of notes/39, where death is theorem-modulo-machine-true-rungs.
  Fine agreement detail: neck2/A's receiver surface stays UNflagged —
  the only attacker the law permits there is x ≤ d−1 = 1, and 1 ∈ B.
  The instruments see exactly what the law sees, including its edges.

## 2. Adversarial re-verification of S1 (experiments/v1_growing_verify.py)

Fresh membership oracle (pure ints, any scale; CHECK 0: equals
g3.build_labels on [1, 2^16] for all 8 candidates).  All checks PASS:

- CHECK 1 — d_t law as an exact iff (both directions), t ∈ [8, 40],
  x ≤ 8, all 4 schedules: 543 predicted attacks + 513 predicted blanks,
  zero mismatches.
- CHECK 2 — crown recurrences at exact high octaves (big ints, t ≤ 60):
  every claimed fixed attacker of every S1 team attacks every claimed
  octave, e.g. lin/B x=1 at all even t ≤ 60, geo/B x=1 (even) + x=3
  (odd), genstage kept-bottom attacks exactly at the computed stage
  jumps {12, 32, 60} (A) / {21, 45} (B); geo_alt/A's crown-plant family
  (2, 2^j−1, 2^{j+1}−4) verified at every odd j ∈ [9, 59]; all concrete
  triples from notes/38 re-verified.
- CHECK 3 — channel-agnostic brute-force attack scan at 2^16: attacked
  octave sets EQUAL to d_t predictions for every in-team x ≤ 64 on all
  nat variants (alt variants: predictions plus plant extras only);
  geo_nat/A clean — no in-team x ≤ 64 attacks any octave ≥ 12.
- CHECK 4 — ray re-walks: both stored RAY-GROW witnesses re-verified
  step-by-step, then DFS-extended from stored node 65793/65554 (octave
  17) to octave 80 under the growing cap 4 s_t + 64: lin/B max new
  reflector 266, geo/B max new reflector ~2^40 ≈ 4 s_40 (reflectors
  Θ(sqrt u) — the growing-reflector regime lem:orbit cannot see, and by
  T-SHARP no growth-hypothesis lemma ever will).  Censoring at 2^18 was
  not a horizon artifact.
  The earlier WIP failure here was a bug in the verifier's own search
  (linear reflector scan capped at 4096 — but at octave 47 the nearest
  in-team reflector sits past a full donated sliver, a run of ~4100
  partner values).  Fixed by enumerating reflectors over the analytic
  team-run intervals; no scan budget.
- CHECK 5 — independent bit-reversal order rebuilt from scratch: 0
  monotone 3-APs on [1, 4096] full and restricted to geo/A and lin/B.

## 3. The verdict

**The growing-sliver swap family is DEAD — and with it the entire
sliver-swap idea, fixed or growing, uniform or per-parity tuned, natural
or split crowns.**  Status of the evidence, by strength:

1. Machine-exact and independently reproduced: the d_t law is an exact
   iff on every candidate tested (CHECK 1/3, v2 12/12 predictions).
2. Theorem (notes/39): Lemma NECK — EVERY schedule leaves some team
   fixed-pair-attacked at infinitely many of its scales (machine-exact
   at 480 points); T-PIN converts machine-UNSAT rungs into death, and
   the rungs are UNSAT everywhere tested for bounded/negative necks
   (geo dead modulo its RUNG-IN family at 3 scales).
3. No counter-tune exists: 14 candidate partitions screened across S1+V
   (8 + 6), every per-team death matching the law; the only clean teams
   (geo/A, geomirror/B) are parity mirrors whose partners are doubly
   dead, and the law forbids a both-clean schedule.

What survives of the YES side inside this geometry: two clean TEAMS at
density 2/3 (peaks) — proof that single-team death machinery does not
bite everything; the failure is always the PAIRING.  Conservation of
attack surface (bottom slivers are a hot potato) is the reason, and it
is now backed at law/lemma level, not just screens.

## 4. Where the program goes (the only door left)

Remaining YES-shapes must break octave alternation itself:
**stage-alternating ownership** — teams own super-blocks
(2^{a_k}, 2^{a_{k+1}}] with a_{k+1} − a_k → ∞ (à la Geneson), donated
slivers only at stage seams.  There the d_t parity dichotomy does not
apply (a team owns consecutive octaves inside a stage).  But note what
already awaits it: stage interiors contain full dyadic blocks (every
scale M = 2^{t-1} ≡ 0 mod 8 for t ≥ 4), so thm:ogred + thm:c3core kill
any team containing the pair {15, 16} — the shape is forced into
splitting EVERY crown pair {2^j−1, 2^j} across teams (trichotomy escape
(1)), and G3 showed planted halves are landing pads in exact partitions.
The G4 experiment: build the stage-alternating family (stage growth ×
seam-sliver schedule × split-crown placement), screen with the g2/g3
kit, and derive the seam analogue of the d_t law.  That is the single
next experiment; a NO there would close the last natural YES-shape, a
survivor would be the strongest YES-candidate since the campaign began.

RUNG-X postscript: the two seam solvers lost at the S2 session close
were relaunched (gm/B t=9 plateau seam — the one OG-density seam family;
lin/B t=9 sparse seam, expected SAT); results stream to
data/s2_rungx_{gmB,linB}.log and s2_sg_rungs.jsonl.

## Reproduce
    .venv/bin/python experiments/v2_tuned_screen.py    # ~2 min
    .venv/bin/python experiments/v1_growing_verify.py  # ~1 min
Artifacts: data/v2_run.log, data/v2_summary.json, data/v2_<tune>.json,
data/v1_verify.log, data/v1_verify.json.
