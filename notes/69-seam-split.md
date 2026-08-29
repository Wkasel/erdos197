# 69 — FRONT SEAM-SPLIT: decomposing the budget demand per seam

Successor instrument to e127 (notes/47 §4, notes/54 §1) on the v* wall:
near-critical JOINT decision queries are hopeless (bal@16 v=8: 17000 s
TIMEOUT; bal@24 v=16: >22 h TIMEOUT), so v* growth cannot be measured
head-on.  This front splits the budget per seam and maps the tradeoff
staircase; the payoff is both a NEW demand statement (per-seam
concentration laws via corner cells) and — the practical crux — a
DECOMPOSITION of the joint decision into per-cell decisions that sit
far from the joint criticality wall and are individually cheap.

Machine companion: experiments/e159_seam_split.py →
data/e159_seam_split.jsonl (streaming) + data/e159_{tag}.json/.log
(local + pod3).  Every SAT verdict independently re-audited (bounds,
per-team monotone-AP freedom, per-seam recounts, mono-H/inversion-edge
cross-audit).

## 1. The instrument and the transfer lemmas

The e127 3-block window (M, 8M], blocks B0/B1/B2, per-team block lower
bounds (`bal` = exact balance), with the single per-team budget v on
total adjacent-seam inversions REPLACED by a per-seam pair:

    seam-1 pairs (u, w) ∈ B0 × B1,  budget a1 per team,
    seam-2 pairs (y, z) ∈ B1 × B2,  budget a2 per team,

'n' (none) = seam unpriced (no indicators).  Cell (a1, a2) = "is there
an escape with ≤ a1 seam-1 AND ≤ a2 seam-2 inversions per team?".
Per-team asymmetric budgets (vA1, vA2, vB1, vB2) are supported by the
encoding; the mapped family here is symmetric (both teams same pair).

**Lemma T-FORCE-SPLIT [PROVED — verbatim notes/54 Lemma T-FORCE,
whose proof never uses the shape of the priced pair family: indicators
are set honestly to the induced order's truth values, and the per-seam
counts are exactly Inv1_T, Inv2_T].**  A valid pair meeting the block
bounds at anchor N with Inv1_T(N) ≤ a1 and Inv2_T(N) ≤ a2 for both
teams induces a model.  Hence

    UNSAT(N; a1, a2)  ⟹  every valid pair meeting the bounds has a
    team T with Inv1_T(N) > a1  OR  Inv2_T(N) > a2.

Unpriced seams impose nothing, so UNSAT(N; a1, n) is an UNCONDITIONAL
per-seam floor: max_T Inv1_T(N) > a1 regardless of seam-2 spending —
and dually.

**Lemma SPLIT-M (monotonicity + joint transfer) [PROVED — two
lines].**  (a) The SAT region is upward closed per coordinate (a
budget-(a1,a2) model is a model at any (a1', a2') ≥ (a1, a2)).
(b) A model at (a1, a2) is a joint model at v = a1 + a2; a joint-v
model has a per-seam split (s1, s2), s1 + s2 ≤ v, and is a model at
cell (s1, s2).  Hence

    UNSAT_joint(v)  ⟺  UNSAT at EVERY cell of the diagonal
                        {(a1, a2) : a1 + a2 = v}.

**Corollary WALL-BYPASS (diagonal decomposition).**  The joint
decision at budget v — the query family that times out at criticality
— decomposes into v + 1 per-cell decisions.  By SPLIT-M(a), a single
UNSAT RECTANGLE (a1, a2) certifies all diagonal cells with
coordinates ≤ (a1, a2); so a small antichain of easy-UNSAT rectangles
whose union of shadows covers the diagonal a1 + a2 = v certifies
v* > v without ever running a near-critical joint query.  The
per-seam lower-bound law that "sums to growth" is exactly this: an
easy-certificate cover of growing diagonals.

## 2. Measured frontier (2026-08-29, first wave; all SAT rows
## audit-passed; pod3 batches still streaming — see §5)

**M = 16 balanced.  BOTH axes are fully SAT — there is NO
unconditional single-seam floor:**

| cell (a1:a2) | verdict | time | witness per-seam payments (A; B) |
|---|---|---|---|
| (0:0) = joint v=0 | UNSAT | 64 s (local) | — [matches e127 v=0] |
| (0:n) | SAT | 1.9 s | s1 = 0, s2 = 380; 0, 405 |
| (1:n),(2:n),(4:n),(8:n),(16:n),(32:n) | SAT | ≤ 6 s | s2 ≈ 220–460 |
| (n:0) | SAT | 29 s (local) | s1 = 120, s2 = 0; 90, 0 |
| (0:256) | SAT | 42 s | s2 = 255, 253 |
| (64:0) | SAT | 19 s | s1 = 64, 60 |

So s1*(16) = s2*(16) = 0 in the axis sense: seam-1 cleanliness is
buyable (pay ~400 at seam-2), seam-2 cleanliness is buyable (pay
~100 at seam-1).  The corner prices bracket so far as
F(0) := min{a2 : (0, a2) SAT} ≤ 256 and
F⁻¹(0) := min{a1 : (a1, 0) SAT} ≤ 64; the descents (0:128..0:4),
(32:0..1:0) are in flight.

**M = 24 balanced — same shape at scale 2:** (n:0) SAT 29 s
(s1 = 282, 260), (0:n) SAT 26 s (s2 = 686, 780), (1:n), (2:n),
(4:n) SAT ≤ 57 s.  No unconditional single-seam floor at 24 either.

**Crossed/per-team cells at 16 — the no-per-team-price phenomenon
(notes/54 §1) holds at the per-seam level too, and sharper:**

| cell (A-budgets / B-budgets) | verdict | time |
|---|---|---|
| (0:n / n:0)  A seam-1-clean, B seam-2-clean | SAT | 1.9 s |
| (0:0 / n:n)  A FULLY seam-clean, B free | SAT | 1.0 s |
| (n:n / 0:0)  mirror | SAT | 0.8 s |

At exact balance one team can carry ZERO seam inversions total —
all demand dumped on the unpriced partner.  Every one-sided and
every single-seam hypothesis is escapable; only the symmetric joint
staircase binds.

## 3. Corner anatomy (why the corner families are the hand targets)

The (n:0) witness at 16 (seam-2 clean): its 74/36 monochromatic
H-triples are broken 74/36-by-seam-1-edges, 0-by-seam-2 — the §3
edge-injectivity (notes/47 §3) is tight and live: n_s1 ≥ #mono-H(col)
at the (·, 0) corner, dually n_s2 ≥ #mono-H(col) at (0, ·).  The
corner witnesses choose INTERVAL splits of B1 (A takes the top half
[49, 64] contiguously), not parity colorings — they pay the sumset
floor openly rather than dodge it.  Structurally, the (0, a2) family
forces wholesale in-team block order B0 ≺ B1 — the prefix-cohort
geometry of notes/62 §4c (L-PREFIX / Lemma K / SCHED-DEAD) ONE SEAM
UP: the corner cells are exactly where the C3-style hand machinery
attaches, while mid-staircase cells are pure mixed theory.

## 4. Reading: hypothesis verdict, honest

The front's motivating hypothesis ("the demand concentrates per-seam;
per-seam sub-queries are easily UNSAT far above the joint bounds") is
HALF right.  Concentration is real but it is a WITNESS phenomenon,
not a demand phenomenon: the v=160 witness concentrates on s1, the
v=80 witness on s2, and the axis scans show both concentrations are
legal to the extreme (either seam can be entirely clean).  So there
is no per-seam LOWER-bound law at the axes.  What survives — and is
better — is Corollary WALL-BYPASS: the per-cell queries so far run
SECONDS where joint near-critical queries ran hours-to-hopeless, and
the diagonal equivalence turns joint decisions into cell batches:

- diagonal f = 5 at 16 (six cells, in flight) DECIDES
  v*(bal,16) ∈ {5, 6} either way (all-UNSAT ⟹ 6; any SAT ⟹ 5);
- diagonal f = 5 at 24 pushes v*(bal,24) ≥ 6 past the 5.9 h wall;
  climbing f while cells stay minutes-cheap re-opens the v*-growth
  measurement (GAP-V*-growth) that the 22 h joint TIMEOUT closed;
- easy-UNSAT RECTANGLES (a1, a2) with a1 + a2 ≫ v* remain possible
  off-axis (mid16 batch: (8:8), (4:16), … in flight); each certifies
  a diagonal SEGMENT, and a small rectangle antichain certifies the
  whole diagonal.

The corner prices F_M(0), F⁻¹_M(0) are the 3-block analogues of the
4-block v_min(0) (notes/62 §5): the price of one seam's cleanliness,
paid on the other seam.  Their growth in M is measurable at seconds
per query (vs the joint wall), and their cell family carries the
L-PREFIX-species hand schema (§3).

## 5. In-flight (pod3, nohup, streaming to /root/e/data/e159_*.log;
## pull + merge with tools/pull_e159.sh)

- c0a16: (0:128),(0:64),(0:32),(0:16),(0:8),(0:4) — F(0) descent;
- ca016: (32:0),(16:0),(8:0),(4:0),(2:0),(1:0) — F⁻¹(0) descent;
- mid16: (1:64),(2:32),(4:16),(8:8),(16:4),(32:2),(64:1),(2:64),
  (4:64) — mid-staircase + rectangle hunting;
- corn24: (0:1024),(0:256),(0:64),(0:16),(128:0),(32:0),(8:0),(2:0);
- diag16f5 / diag24f5: (0:5),(1:4),(2:3),(3:2),(4:1),(5:0) — the
  v* deciders;
- budgets 900 s (16) / 1800 s (24) per cell, hard-killed; verdicts
  stream to data/e159_seam_split.jsonl on the pod.

Next wave (queue when these drain): rectangle covers for the largest
all-UNSAT diagonal at 24 (f = 6, 8, …); F(0)/F⁻¹(0) at 24 and 32
(growth law); asymmetric per-team staircase if the symmetric one
pins down.
