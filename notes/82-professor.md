# 82 — PROFESSOR PASS: the elegance review of GAP-AFFORD″-ALT
# (pure thought; no solvers, no experiments; 2026-08-30 night)

Mandate: the NO-proof is complete except GAP-AFFORD″-ALT
(notes/80-pincer §3.4): everywhere-split colorings whose minority is
mod-4-lattice-like — unbounded-run alternating ownership, punctured
variants, gap-≥3 non-lattice variants.  Current attack = siege
(run-length thresholds, puncture budgets, catalogues).  Question:
is there an elegant kill, or certify none exists.

**VERDICT UP FRONT.  There is an elegant kill, and it is a
one-page restriction argument: direction (2), self-similarity
descent — executed not as infinite descent but as a ONE-STEP
descent onto the already-proved Case-1 chain.**  The mod-4 lattice
corner (any ownership sequence: constant, alternating, unbounded
runs, procrastinating — the entire S5-ALT siege target) and the
on-class punctured variants are DEAD with ZERO new gaps: the only
inputs are Lemma PIN [PROVED], DIAG-DENSE [PROVED], Theorem C3(p)
[PROVED, spot-audited notes/80], and a two-line affine-restriction
transport of exactly the L-NOTAIL species.  No supply cap, no
T-TEL″, no censor, no run-length threshold is needed anywhere.
Directions (1), (3), (4) FAIL as posed — each against a hard,
already-measured obstruction — but (1)'s instinct is correct one
level up and becomes (2), and (4)'s CONCLUSION (emptiness of the
lattice-like family as valid pairs) is true and is what (2)
proves.  The full proof of Theorem ALT-DEAD is §2.  What survives
GAP-AFFORD″-ALT after this note is only the non-lattice gap-≥3
residue, in a strictly sharper, 2-adically-generic form (§5).

Sources read: STATUS.md (full), notes/50 (final graph), notes/80-
pincer (AFFORD-CORNER, L-NOTAIL, S5-ALT), notes/79 (tournament +
witnesses), notes/52 (B1, PIN, DIAG-DENSE — the load-bearing
statements re-read line by line), notes/78 Part I (Theorem C3(p)
statement + status), notes/62 §4d (Lemma K, SCHED-DEAD), notes/33
(toolkit skim), paper/main.tex (thm:ogred, thm:c3core, thm:main,
thm:degs, thm:blockgranular, thm:restriction).

---

## 1. Direction (1) — AFFINE TRANSFER of the interval theorems.
## Verdict: FAILS AS POSED; correct one level up (= §2)

The hope was: an in-team d=4 run of modest length, under the
forced-first structure the anchor demands impose, dies by affine
Lemma K; R* a small explicit constant.  Two independent failures,
both already in the record:

**(1a) The anchor demands do not supply forced-first.**  Lemma K
(notes/62 §4d) needs the run's bottom k placed before the rest of
the run.  What AFFORD-CORNER actually forces per anchor is the P5
orientation: each H-triple (x, y, z) has pos(y) < pos(x) OR
pos(z) < pos(y) — a per-triple DISJUNCTION of seam inversions.  A
disjunction over cross-block pairs never pins a prefix of one run
first; the freedom to procrastinate is exactly what survived the
DNP engagement (notes/47: X-INTERLEAVE re-descends at every
anchor; positions interleave), and that refutation is final.  The
one place Lemma K fires in the corpus — SCHED-DEAD — fires under
the HYPOTHESIS vdn = 0, i.e. block order, which is the thing that
cannot be forced at ω.  Any Lemma-K-via-anchors kill would be a
DNP revival in affine clothing.  No.

**(1b) Short runs are unattackable by fixed pairs — a two-line
geometry fact.**  Let the run be R = {s, s+4, …, s+4L} (class c,
height s, length L), image interval [σ, σ+L], σ = Θ(s).  An AP
(x, y, z) with y, z in the image interval has
x = 2y − z ∈ [σ − L, σ + 2L].  A FIXED attacker pair (the T-PIN
currency) needs x = O(1), hence σ ≤ L + O(1): **a run is
reachable by fixed attackers only if its length is a positive
fraction of its height** — i.e. only at block scale.  For
sub-block runs the attacker must scale with t (T-REGRESS
territory, closed only per-schedule, notes/39).  So the posed
R*-threshold ("small explicit constant, independent of height")
provably does not exist.

**The salvage.**  What DOES transfer verbatim under x ↦ 4x + c is
not Lemma K but the entire Case-1 kill chain — Lemma PIN,
DIAG-DENSE, Theorem C3(p) — because every one of its statements
is a statement about 3-APs and order, and 3-APs are affine
invariants.  Then the "run" that dies is the full class-section
of a block (length exactly 2^{t−2} = block/4, at height 2^t —
precisely the (1b) boundary case), the forced-first structure is
supplied by Lemma PIN's pigeonhole (positions of a fixed pair are
finite — no anchor demands needed), and the run-length threshold
is R*(t) = 2^{t−2}: **the lattice family sits exactly on the
reachable boundary, and it is the family we need to kill.**  That
reframing is direction (2).

---

## 2. Direction (2) — SELF-SIMILARITY DESCENT.  Verdict: WORKS.
## Theorem ALT-DEAD, complete hand proof

The key structural observation, missed because the corner was
always approached from the order/affordability side: **in a
blockwise mod-4 lattice coloring, EVERY mod-4 residue class is
monochromatic within every lattice block** — the minority is one
full class, so the other three classes lie wholly in the
majority, and the minority class lies wholly in the minority
team.  A lattice coloring is everywhere-split as a partition of
ℤ⁺ (Case 2), but its 4-adic shadow is block-granular — Case 1.
The N4 dichotomy is not stable under affine restriction, and
permutability IS.  That asymmetry is the whole kill.

### 2.1 Lemma Q (quarter-tail lemma)

Notation: B(t) = (2^t, 2^{t+1}]; for c ∈ {0,1,2,3} and t ≥ 2 let

    Λ_c(t) := {v ∈ B(t) : v ≡ c (mod 4)}

(the class-c section of block t — a d=4 run of length 2^{t−2}).

**Lemma Q.**  No 3-permutable set contains Λ_c(t) for one fixed c
and infinitely many t.

*Proof.*  Suppose T ⊇ Λ_c(t) for all t in an infinite set 𝕋, and
let π be an arrangement of T with no monotone 3-AP.

(i) *The affine chart.*  Define φ on the class c + 4ℤ by
φ(x) = x/4 if c = 0, φ(x) = (x − c + 4)/4 if c ∈ {1,2,3} — an
increasing affine bijection onto a tail of ℤ⁺.  Exact block
alignment: for c ∈ {1,2,3}, Λ_c(t) = {2^t + c, …, 2^{t+1} − 4 + c}
and φ maps it onto {2^{t−2}+1, …, 2^{t−1}} = B(t−2); for c = 0,
Λ_0(t) = {2^t + 4, …, 2^{t+1}} and φ = x/4 maps it onto B(t−2)
likewise.  **φ(Λ_c(t)) = B(t−2), exactly — no boundary dust.**

(ii) *Transport of AP-freeness.*  Restrict π to T ∩ (c + 4ℤ) and
reindex: an arrangement (order type ω) of that subset, and any
monotone 3-AP in it is a monotone 3-AP of π (positions restrict;
a 3-AP of class-c values is a 3-AP in ℤ⁺).  Push forward by φ:
S′ := φ(T ∩ (c + 4ℤ)) inherits an arrangement.  A 3-AP of S′
pulls back under φ^{-1} to a triple x, y, z ∈ c + 4ℤ with
x + z = 2y (affinity, both directions; note the pulled-back
midpoint is automatically in class c because φ^{-1} is affine).
So a monotone 3-AP of the image arrangement would be a monotone
3-AP of π.  **S′ is 3-permutable.**

(iii) *The contradiction.*  S′ ⊇ B(t−2) for every t ∈ 𝕋: S′ has
infinitely many 0-clean dyadic blocks.  Theorem B1 (notes/52
§3.1) applies with C₀ = 0.  Its proof at C₀ = 0 consumes: Lemma
DIAG-DENSE [PROVED] to extract a diagonal pair {3p, 3p+1},
p ≡ 1 (mod 4), from one clean block of S′; Lemma PIN [PROVED] to
force the pair before cofinitely many later clean blocks; and the
rung hypothesis (H1) only at C = 0 — which is exactly Theorem
C3(p) [PROVED, notes/78 Part I; spot-audited notes/80 §1.1]: for
p ≡ 1 (mod 4) the flip class is M ≡ 2p+6 ≡ 0 (mod 8), and every
dyadic scale 2^m, m ≥ 3, is in it.  (The three C3(p) units are
among R(3p, 3p+1; 2^m, ∅)'s fired units — attackers 3p, 3p, 3p+1
— so C3(p)'s inconsistency kills R a fortiori.)  So S′ is not
3-permutable.  Contradiction.  ∎

Remarks.  (a) The species is exactly L-NOTAIL: restriction
closure + affine invariance; where L-NOTAIL feeds the restricted
permutation to DEGS77, Lemma Q feeds it to the campaign's own B1.
L-NOTAIL needs one team to own an infinite AP — the CONSTANT-
ownership tail; Lemma Q needs only the block-aligned finite
truncations, each owned by SOMEBODY, and pigeonholes ownership.
That is precisely the upgrade the alternating corner was built to
dodge, and it cannot dodge this one: alternation redistributes
the sections but cannot make them stop existing.  (b) The map
v ↦ 4v is already a proof device in the paper (thm:blockgranular
lifts UNSAT cores along it; thm:restriction restricts along it);
Lemma Q is the same move pointed at a coloring instead of a
window class.

### 2.2 Theorem ALT-DEAD

Call scale t *4-pure* for a partition (A, B) if some mod-4 class
is monochromatic on B(t) (contained in one team).

**Theorem ALT-DEAD.**  If infinitely many scales are 4-pure, then
A and B are not both 3-permutable.  Consequently:

1. **Every blockwise mod-4 lattice coloring is dead** — minority
   of each block = one full class ⟹ every class is pure at every
   lattice scale.  The ownership sequence never enters: constant,
   alternating at any run-length law, unbounded runs,
   T-SHARP-procrastinating — all dead.  GAP-AFFORD″-ALT's
   alternating-lattice component is CLOSED.
2. **Every punctured near-lattice with on-class dust is dead** —
   if the minority of block t is CONTAINED in class c_t
   (punctures = class values ceded to the majority, the
   L-NOTAIL-dodging shape), the three classes ≠ c_t are still
   pure at t; some fixed c* differs from c_t infinitely often
   (for each t three classes qualify, so one class qualifies on a
   set of density ≥ 3/4 of scales), so infinitely many scales are
   4-pure.  Dead — at ANY puncture count, bounded or not, with or
   without constant ownership.  GAP-AFFORD″-ALT's punctured
   component is CLOSED, and no puncture-budget catalogue is
   needed.
3. **Off-class dust reduces to an existing gate, not a new one**:
   if the minority strays off its class but some class c* is pure
   up to ≤ C₀ dust at infinitely many scales, step (i)–(ii)
   transport verbatim and the image blocks are C₀-clean; B1 at
   C₀ needs (H1) at C = C₀ = GAP-N3-GROW — gating gap (4) of
   notes/50, already on the critical path.  Nothing new.

*Proof of the theorem.*  Each 4-pure scale t yields a pair
(c, S) ∈ {0,1,2,3} × {A, B} with S ⊇ Λ_c(t).  Eight cells,
infinitely many scales: some (c, S) recurs infinitely.  Lemma Q
kills S.  ∎

*Dependency audit.*  Lemma Q + ALT-DEAD consume: Lemma PIN
[PROVED, notes/52 §1.3 = thm:ogred's pigeonhole], DIAG-DENSE
[PROVED, notes/52 §2.1], Theorem C3(p) [PROVED, notes/78;
spot-audit clean, residual = referee prose pass], restriction +
affine transport (steps i–ii above, same rigor class as
L-NOTAIL).  **No open tag is touched for conclusions 1 and 2.**
ALT-DEAD inherits exactly one rider: the C3(p) prose pass at
paper time.

### 2.3 The general corollary (paper-grade) and the odd-modulus
### sibling

The same chart at modulus 2^k (φ(x) = (x − c + 2^k)/2^k, resp.
x/2^k) maps class-c sections of B(t) EXACTLY onto B(t−k).  Hence:

**Corollary HSPLIT (hereditary splitness).**  For every valid
pair (A, B), every k ≥ 1 and every c mod 2^k, the section
(c + 2^k ℤ) ∩ B(t) is bichromatic for all but finitely many t.
*A valid partition must be everywhere-split in every 2-adic
chart, not just the identity chart.*  [Modulo nothing beyond the
C3(p) prose rider.]  In particular any coloring eventually
2^k-periodic on blocks is dead; k = 1 says no team may own all
odds (or all evens) of infinitely many dyadic blocks.

Odd modulus q (e.g. the spacing-3 minority, a legal gap-≥3
shape): the chart maps class sections onto ratio-2 windows at
NON-dyadic anchors M_t = (2^t − c)/q + O(1) with O(1) seam dust.
For q = 3 the anchors alternate between ≡ 5 (mod 8) (the
(4^k−1)/3 ≡ 5 identity of CROWN-2ADIC) and ≡ 2 (mod 8) — exactly
the C-lane and B2-lane residues with verified off-diagonal
schemas.  So odd-q lattice-like minorities die modulo
BRIDGE1-AF + GAP-N2-UNIF (+ N3-GROW at C = 2 for the seam dust)
— known species, catalogued, not gating the assembly; tag as
Corollary Q-ODD [stated, not claimed].

### 2.4 Consistency checks (done by hand against the corpus)

- *Geneson's W (density 2/3, permutable).*  Lemma Q predicts W
  misses a value of every class-section at cofinitely many
  scales.  Verified consistent at modulus 2: W's complement
  contains 2^s + 3 (the H1 orbit, notes/34), which is odd and
  ≡ 3 mod 4, so W never owns the full odd section, nor Λ_3.
  Recommended machine check (e186): scan W's generator for full
  Λ_c(t) at all c — Lemma Q says the count is finite.  A failure
  would indict B1/C3(p), not the transport — this is a genuine
  adversarial audit of the proved layer, for free.
- *geo/A, geomirror/B (the clean teams).*  Their blocks miss
  growing slivers (s_t → ∞), which meet every class; no full
  class-section recurs.  Lemma Q is SILENT — correctly: these
  teams were never proven non-permutable by Case-1 tools.  The
  block-alignment requirement in Lemma Q is real, not pedantry.
- *ROT4.*  Quarters are intervals, every interval of length ≥ 4
  meets all classes; silent.  Consistent — ROT4 is killed by the
  coupled core, not Case 1.
- *X-INTERLEAVE.*  Sparse; silent.  Consistent.
- *S5/S5-ALT witnesses.*  Finite colorings; Lemma Q is an ω
  statement — no tension with their finite SAT cells.  Their
  ω-extensions: constant-ownership ones were already dead
  (L-NOTAIL); ALL are now dead (Cor. 1), including every
  alternating extension the S5-ALT siege was bracketing, and the
  weak-censor TIMEOUT cells (run ≥ 2 at F = 12) are MOOT at ω.
- *Canonical S_A / block-granular shapes.*  4-pure at every
  scale; ALT-DEAD re-derives their death — consistent with
  thm:main and thm:blockgranular.

---

## 3. Direction (3) — DENSITY/CLASSICAL.  Verdict: FAILS

Three walls, each already measured by the campaign:

1. **Density never fires rungs.**  N5's resolved verdict: the
   single-block rung tolerance is O(1) punctures — ρ* = 1 − O(1)/M
   → 1.  A positive-density union of d=4 runs is far below every
   firing threshold; "positive density ⇒ rung configuration" is
   not merely unproven, it is REFUTED at the instrument level.
2. **APs in the SET are not obstructions.**  Szemerédi/vdW
   applied to the minority yields long APs inside the team — but
   permutable sets can have density 2/3 (Geneson) and every
   finite set is permutable (DEGS77 constructions); one team
   always has upper density ≥ 1/2, so Roth already floods both
   teams with 3-APs.  Death never comes from containing APs; it
   comes from pair+window ORDER theories.  Only the infinite AP
   is fatal (L-NOTAIL) — and the alternating corner contains
   none by construction.
3. **Varnavides-species counting gives demand, not death.**
   Positive-density AP counts on the corner are exactly
   AFFORD-DEMAND's Θ(m²) floor — already proven, and explicitly
   insufficient: NG4 (demand instruments cannot cap supply) plus
   the measured 3× per-window supply slack (notes/80-pincer
   §3.4).  "Unbounded-run alternation is self-defeating by
   density" would need a density-only bridge from demand to
   contradiction, which is the refuted budget-rectangle shape.

What is true in (3)'s direction is only this: the runs the rungs
CAN reach are the block-scale ones ((1b) geometry), and for those
the correct classical import is not Szemerédi but restriction —
i.e. §2.

---

## 4. Direction (4) — EMPTINESS BY ACCOUNTING.  Verdict: the
## accounting route FAILS; the emptiness CONCLUSION is TRUE via §2

As accounting: no.  The proved constraints (forced alternation +
T-FRESH minting + AFFORD-CORNER's Θ(m²)) are all demand-side; the
pincer's own §3.4 already recorded the honest arithmetic — per
4-adic window, demand ≤ presence, supply = 3× presence, no
counting contradiction — and NG1–NG4 stand.  S5-ALT's censor-off
SAT shows the alternating family is finitely inhabited AS
COLORINGS, so no finite theory refutes it at the coloring level
either; any pure-accounting emptiness proof would have to
contradict one of these measured facts.

But the family IS empty as a class of VALID PAIRS — that is
Theorem ALT-DEAD, and the mechanism is orthogonal to accounting:
the corner colorings are Case 1 in disguise (in the 4-adic
chart), and Case 1 is closed.  Direction (4) asked the right
question with the wrong instrument.

---

## 5. Residue, ledger, and the next (single) experiment

**GAP-AFFORD″-ALT after this note:**

| component | status |
|---|---|
| unbounded-run alternating mod-4 lattices | **DEAD (ALT-DEAD Cor. 1; zero new gaps)** — the S5-ALT siege, run-length scans, and censor escalation are obsolete at ω |
| punctured near-lattices, on-class dust (any count) | **DEAD (ALT-DEAD Cor. 2; zero new gaps)** |
| near-lattices with bounded off-class dust | DEAD mod GAP-N3-GROW (existing gate (4); no new tag) |
| eventually-2^k-periodic minorities, any k | DEAD (Cor. HSPLIT) |
| odd-q periodic minorities (e.g. spacing-3) | DEAD mod BRIDGE1-AF + GAP-N2-UNIF (known species; Cor. Q-ODD) |
| non-lattice, 2-adically split gap-≥3 minorities | **SURVIVES** — rename the tag |

The surviving object is sharply characterized and is NOT
"mod-4-lattice-like": by HSPLIT it must, at every modulus 2^k,
split every class in cofinitely many blocks — a 2-adically
generic sparse minority, aperiodic by construction, of which the
campaign has never produced a single inhabitant (all realized
corner witnesses were lattices — notes/80 §4).  Proposed rename:
**GAP-AFFORD‴-SPLIT** — the supply cap for gap-≥3, 2-adically
split minorities — patrolled as before by SPARSE-CORE (demand,
8 scales + AAA hand arm) and MINT-1, with L-CASCADE/arm B
unchanged.  Honest note: for THIS residue I certify that none of
directions (1)–(4) yields an elegant kill — (1b)'s geometry
blocks fixed attackers (no class-section structure to align on),
(3) and (4) fail as above — it remains genuine AFFORD′-type
mathematics, but it is now a strictly smaller and stranger
target, stripped of every arithmetic example.

**Ledger moves (for notes/50 §2d and §6):**

- NEW [PROVED]: Lemma Q, Theorem ALT-DEAD (+ Cor. HSPLIT) —
  inputs PIN + DIAG-DENSE + C3(p) only; rider = C3(p) referee
  prose pass.  The Case-2 corner inherits a Case-1 kill; N4's
  dichotomy is not restriction-stable, and HSPLIT is the correct
  hereditary form of "everywhere-split".
- GAP-AFFORD″-ALT: RETIRED in favor of GAP-AFFORD‴-SPLIT (above).
  All run-length/puncture siege lines (S5-ALT escalation, R-scans
  at F = 64, puncture catalogues) can stand down.
- L-NOTAIL: now a corollary of Lemma Q on the lattice family
  (kept for its classical self-audit value).
- The YES-composition shifts: of the residual YES-mass, the
  "canonical arithmetic family with trivial ω-extension" argument
  (notes/80 adjudication, the reason the estimate was held) is
  VOID — every arithmetic inhabitant is dead; a YES now requires
  a 2-adically generic sparse coloring nobody has constructed AND
  ¬AFFORD on it.

**One machine errand (cheap, adversarial, not gating):** e186 —
(a) scan Geneson's W for full Λ_c(t) (Lemma Q predicts finitely
many; a counterexample would indict the B1/C3(p) layer); (b) on
the S5/S5-ALT witnesses, verify 4-purity at every lattice scale
and exhibit the transported image's clean blocks (the finite
shadow of ALT-DEAD); (c) re-run the S5 dodger build with the
HSPLIT constraint (every class mod 4 and mod 8 bichromatic per
block) added — the first honest instrument for GAP-AFFORD‴-SPLIT's
inhabitants.

**Ranking of survivors by shortest path:** only (2) survived, and
it is finished above.  Within it: Cor. 1 + Cor. 2 (zero gaps,
~1 page, paper-ready now) ≺ Cor. 3 / HSPLIT bookkeeping (zero
gaps, half page) ≺ Q-ODD (rides the N2-UNIF pool) ≺
GAP-AFFORD‴-SPLIT (open mathematics, no elegant kill certified).

---

## 6. Summary

The siege was aimed at a family that a one-page restriction
argument kills outright: mod-4 lattice minorities make every
residue class blockwise monochromatic, the 4-adic chart carries
class sections EXACTLY onto dyadic blocks, permutability restricts,
and the image is Case 1 — dead by PIN + DIAG-DENSE + C3(p), all
proved.  Alternation, run lengths, punctures on the class, and
censors never enter.  What remains of the corner is only the
2-adically split gap-≥3 residue — no known inhabitant, no
arithmetic shape — and the terminal supply question lives there
alone now.
