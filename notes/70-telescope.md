# 70 — FRONT TELESCOPE: the boundary ledger, T-TEL, and what the
# 2-adic chain actually buys

Task: make GAP-V*-growth unnecessary.  The 4-block downward pump
(notes/62: (6,0)@16 and (65,0)@24 UNSAT, attribution-controlled) says
price at anchor N forces price at anchor N/2.  Formalize the
cross-scale accounting, state the candidate theorem T-TEL, prove
disjointness of forced payments from the gadget geometry — or find
the overlap that breaks it, honestly — and machine-test on the pump
witnesses at 16/24.

Machine companion: experiments/e173_telescope.py →
data/e173_telescope.jsonl, e173_audit.json, e173_{cell}.json.
Verdict of the front in one line: **naive T-TEL (consecutive-anchor
disjointness) is FALSE — the overlap is the shared seam and the C1
witness realizes it MAXIMALLY; but the accounting has an exact
repair (the boundary ledger: 4-adic subchains are perfectly
disjoint), the pump fires at every scale measured INCLUDING the
bottom one (new: (6,0)@8 UNSAT), and the surviving theorem T-TEL′ is
a dichotomy that replaces GAP-V*-growth with GAP-VMIN0-growth — a
curve measurable by cheap deep-UNSAT queries instead of hopeless
near-critical decisions.**

## 1. The right tower: boundary currency on the 2-adic chain

The pump couples N to N/2, which is not in the 8-adic tiling; the
correct frame drops tilings altogether and prices BOUNDARIES.

**Setup.**  Fix a base anchor N₀ and the 2-adic chain
A = {N_j = N₀·2^j}.  Octaves O_m = (N_{m-1}, N_m]; boundary β_m = the
seam between O_m and O_{m+1} (located at the value N_m).  An
*adjacent-octave pair* of team T at β_m is (u, w) with u ∈ O_m ∩ T,
w ∈ O_{m+1} ∩ T; it is *inverted* iff pos_T(w) < pos_T(u).  Write
x_m(T) = # inverted pairs of T at β_m.

**Lemma L-HOME (pair single-boundary) [PROVED — trivial; machine-
audited].**  Every adjacent-octave pair belongs to exactly one
boundary (the octave of its low member determines m).  Distinct
boundaries have disjoint pair sets.  Pairs two octaves apart (skip
pairs) belong to NO boundary of the chain — at chain anchors they are
never adjacent-seam pairs, only skip pairs, and P4 amplifies them
(one skip inversion at W(N) costs ≥ |B₁∩T| adjacent ones).  So the
chain accounting sees exactly the adjacent-octave currency.

**Lemma L-2PRICE (each pair priced by exactly two chain anchors)
[PROVED — four-line check; machine-audited on all witnesses].**
Anchor N_j has W(N_j) = O_{j+1} ∪ O_{j+2} ∪ O_{j+3} with seams
s1 = β_{j+1}, s2 = β_{j+2}.  Hence

    Inv_T(N_j) = x_{j+1}(T) + x_{j+2}(T),

and boundary β_m is priced by exactly two chain anchors: N_{m-1}
(as its s1) and N_{m-2} (as its s2).  Conversely an adjacent-octave
pair at β_m is an eligible seam pair of exactly those two anchors —
verified pair-by-pair on every e158 witness (e173 audit: L-2PRICE
true on 8/8 team-records, the covered-anchor set of every single
inversion pair equals {(N_{m-1}, s1), (N_{m-2}, s2)}).

**Theorem T-LEDGER (exact 4-adic disjointness) [PROVED from L-HOME +
L-2PRICE].**  Along either 4-adic subchain (j even, or j odd):

    Σ_{j even} Inv_T(N_j)  =  Σ_m x_m(T)      (each boundary once),

i.e. the per-anchor payments of a 4-adic subchain are PAIRWISE
DISJOINT pair families whose union is the whole boundary currency —
a perfect partition, no double count, no gap.  The full 2-adic chain
double-counts each pair exactly twice:
Σ_j Inv_T(N_j) = 2·Σ_m x_m(T).  Payments at anchors ≥ 4× apart are
disjoint outright (their boundary sets are disjoint; equivalently the
low members live in disjoint ranges).  ∎

This resolves the accounting question exactly: the 2-adic chain of
overlapping 4-block gadgets is the DEMAND instrument (the pump needs
consecutive anchors), the 4-adic subchain is the LEDGER (exact
disjointness), and value-single-use enters as: each VALUE is a
member of pairs at ≤ 2 boundaries (low member at its octave's upper
boundary, high member at the lower), so Σ_m x_m ≥ half the count of
distinct displaced/advanced values — the bridge to P3 and to the
donation currency.

## 2. The overlap that breaks naive T-TEL — measured, maximal

Consecutive chain anchors share a boundary (s1 of N_j = s2 of
N_{j-1}), so payments at consecutive anchors are NOT disjoint, and
no gadget refinement can make them so: the overlap is structural.

Machine (e173 audit, on the e158 pump witnesses at M = 16):

- **C1 (6, none):** each team's ENTIRE upper payment (6 pairs, all
  on s1 = β(2M)) is simultaneously lower-anchor payment —
  Inv(M) ∩ Inv(M/2) = the s1 set exactly, overlap 6/6 = maximal.
  The genuinely fresh forced lower mass is the 32 s0 pairs (β(M)),
  disjoint from every pair priced at anchor M or any anchor above.
- **C2 (none, 0) and the lavish (384, 0) witness:** all payment on
  s2 = β(4M) (392/442 resp. 384/384), boundaries M and 2M clean —
  the free-below dodge pays entirely on the TOP boundary, i.e.
  Inv(M/2) = 0 AND Inv(M/4)-side clean; the obligation is pushed UP:
  β(4M) is the s1 of anchor 2M, so this payment is fully visible to
  (and priced by) the anchor above.  "Lavish here, free below" =
  export the obligation one anchor up, exactly notes/62 §6.
- **C0 (free):** overlap = s1 in both teams (16 and 74) — the set
  identity Inv(N) ∩ Inv(N/2) = x_{β(2N)} holds on every record.

So: **any T-TEL that assumes payments at consecutive anchors demand
disjoint inversion pairs is FALSE, and the witnesses realize the
maximal allowed overlap.**  The exact repair is T-LEDGER: disjointness
is a 4-adic (alternate-anchor) fact, with the factor-2 overlap of the
full chain exact and harmless.

## 3. Freshness: what the pump forces BEYOND the shared seam

The overlap raises the sharp question: is the forced lower payment
absorbable into the doubly-priced shared seam (making the pump
ledger-neutral), or does it demand NEW-boundary currency?

**The freshness cell F(M; v):** 4-block gadget, per-seam budgets
[x_{β(M)} = 0; x_{β(2M)} + x_{β(4M)} ≤ v] — upper anchor priced at v,
new-boundary currency banned, the shared seam left free below (the
lower anchor may spend on it without limit beyond the upper cap).

- F(16; 6): RUNNING at the time of writing (verdict lands in
  data/e173_telescope.jsonl and §5; this paragraph records BOTH
  readings, committed before the verdict).
- F(24; 65): queued behind it (same shape at the second pump scale).

Pre-registered readings.  UNSAT ⟹ by T-FORCE-4, every valid balanced
pair with Inv_T(16) ≤ 6 for both teams has a team with an inverted
pair at β(16) — currency DISJOINT from everything priced at anchor 16
and above: the pump is NOT ledger-neutral, cheap upper anchors mint
fresh currency one boundary down, booked disjointly by T-LEDGER.
SAT ⟹ the forced lower payment can ride entirely on the doubly-priced
shared seam: the pump's fresh-currency claim fails, disjoint demand
lives only at the 4-adic granularity, and T-TEL′ branch (b) weakens
from "one fresh pair per 2 octaves" to the D3 covering constant.

## 4. T-TEL: dead version, live version

**T-TEL (naive; the version in the task prompt) — DEAD, twice.**
"Cumulative forced price along the 2-adic chain diverges because
payments at different anchors demand disjoint pairs; divergence
contradicts supply."  (i) Consecutive-anchor disjointness is false
(§2).  (ii) Even with T-LEDGER's exact repair, divergence of
Σ x_m is NOT a contradiction: pair supply is fresh per boundary (P1);
X-INTERLEAVE realizes x_m ≥ 1 at EVERY boundary with a valid single
team (e130 check 1).  No pair-count statement closes L-AFFORD —
NG1–NG4 apply to the telescope exactly as to every other counting
route.  The ledger can only ever be the demand bookkeeping.

**T-TEL′ (the surviving dichotomy) [PROVED modulo two tags].**
Assume:
- [GAP-J-schema] the pump family: (v, 0) at anchor M UNSAT for all
  v < v_min(0)(M), for all large anchors in the regime (machine-true
  at M = 8, 16, 24 — three scales after this session);
- [GAP-VMIN0-growth] v_min(0)(M) → ∞ (measured: > 6 at 8, > 6 at 16
  with SAT at 384, > 65 at 24 — the curve exceeds the entire v*₃
  bracket at every measured scale).

Then every valid pair in regime (I) satisfies, along any 2-adic
chain, at least one of:

  (a) **de facto price divergence:** limsup_j Inv_T-max(N_j) = ∞ —
      indeed if Inv(N_j) = 0 for infinitely many j, the pump gives
      Inv(N_{j+1}) ≥ v_min(0)(N_{j+1}) → ∞ at those j; moreover the
      huge payment sits on β(4N_j)-side currency shared with anchor
      N_{j+2}, which is then also forced ≥ that height minus its own
      β(8N_j)-freedom — the lavish dodge is itself booked;
  (b) **everywhere-payment:** Inv(N_j) ≥ 1 for all large j, and by
      T-LEDGER the 4-adic bookkeeping of these payments is a family
      of pairwise-disjoint fresh pairs — one new pair per 2 octaves
      forever, the notes/47 §5.4 covering statement DERIVED rather
      than assumed.

In both branches the cumulative fresh demand Σ_m x_m diverges with
exactly-disjoint bookkeeping.  ∎ (two-line case split on whether
{j : Inv(N_j) = 0} is infinite.)

**What T-TEL′ buys — the point of the front.**  Theorem D / Theorem
LT (notes/54) needed [GAP-V*-growth]: v*(N) → ∞, a curve only
measurable by near-critical decisions (hopeless: v=16@24 timed out at
22 h).  T-TEL′ replaces it: the demand side of the ledger theorem now
runs on v_min(0)-growth, whose lower bounds come from DEEP-UNSAT
(v, 0) cells — cheap, because vdn = 0 collapses the lower window's
order theory to wholesale block order (L-PREFIX): 2.1 s at 16, 46 s
at 24, 2.1 s at 8.  GAP-V*-growth is demoted from load-bearing to
nice-to-have: **if v* stays bounded forever, Theorem LT's demand
still diverges through T-TEL′ branch (a)/(b).**  The measured
ordering v_min(0)(M) ≫ v*₃(M) at every scale (6 > [0], >65 ≥ bracket
(4,65] at 24) is exactly why: zeroing an anchor is far more expensive
than merely paying the per-anchor floor.

**What T-TEL′ does NOT buy — honest.**  The supply cap.  Branch (b)
is satisfiable in pair currency by AP-free teams (X-INTERLEAVE); for
Θ(M)-dense teams no supply contradiction is known.  The terminal
statement is unchanged: [GAP-AFFORD′] — an upper bound on overpayment
capacity denominated in DONATIONS (single-use colored values), per
notes/62 §6.  The telescope sharpens its target: the donation ledger
must charge branch (a)'s diverging payments (which L-2PRICE books on
TWO anchors each — overpayment is never private) or branch (b)'s
everywhere-fresh minting (which P3 converts to an infinite displaced
set with δ ≥ 1 — one displaced value per 2 octaves forever).

## 5. Machine record (this session)

| cell | verdict | time | reading |
|------|---------|------|---------|
| audit (8 team-records, 4 witnesses) | ALL PASS | — | L-HOME, seam-disjointness, L-2PRICE exact; overlap ≡ s1; C1 overlap maximal (6/6); fresh mass 32 |
| pump (6,0)@16 via e173 encoder | UNSAT | 2.1 s | cross-validates the new generalized encoder against e158 verbatim |
| **pump (6,0)@8** | **UNSAT** | 2.1 s | **NEW: v_min(0)(8) > 6 — the pump fires at the BOTTOM scale, where BOTH standalone anchors are free (v*(bal,8) = v*(bal,4)-side = 0); the chain step exists at every measured scale** |
| fresh F(16;6) | see jsonl | | the freshness discriminator (§3) |
| fresh F(24;65) | see jsonl | | scale-2 freshness |
| five U5(16): (6,·,0) | see jsonl | | 2-step chain cell; note the middle anchor is auto-priced ≤ 0+6 by the outer budgets (its seams are shared — the chain has NO parking space); F(16;6) UNSAT ⟹ this cell UNSAT a fortiori by restriction |

(The jsonl is the live record; the table's open rows are filled by
the queue as cells land.)

## 6. Ledger movement

| tag | before | after |
|-----|--------|-------|
| GAP-V*-growth | load-bearing for Theorem D | **demoted**: T-TEL′ runs demand on v_min(0)-growth; v*-growth now only sharpens constants |
| GAP-VMIN0 (notes/62) | side measurement | **promoted to THE demand curve**; lower bounds by deep-UNSAT cells; measured > 6 / > 6 / > 65 at 8 / 16 / 24 |
| GAP-J-schema | 2-scale machine family | 3-scale (8 added); schema target unchanged (L-PREFIX + three-arm architecture, notes/62 §4c-d) |
| T-TEL (naive) | candidate | **refuted honestly** (maximal overlap measured; P1/NG4 kill divergence-as-contradiction) |
| T-TEL′ dichotomy | — | proved modulo GAP-J-schema + GAP-VMIN0-growth |
| GAP-AFFORD′ | terminal statement | unchanged, target sharpened (§4) |
