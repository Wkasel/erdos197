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
true on 10/10 team-records incl. the q = 3 chain at M = 24; the
covered-anchor set of every single inversion pair equals
{(N_{m-1}, s1), (N_{m-2}, s2)}).

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

**Lemma L-SQUEEZE (no parking space) [PROVED — one line].**  For
each team, Inv_T(N_j) = x_{j+1} + x_{j+2} ≤ Inv_T(N_{j-1}) +
Inv_T(N_{j+1}): per-anchor prices are subadditive along the chain,
because each of the anchor's two boundaries is shared with one
neighbour.  Consequences: (i) bounding one 4-adic subchain bounds
the whole chain (the odd-subchain price is dominated by adjacent
even-subchain prices); (ii) in any multi-anchor gadget, pricing
alternate anchors auto-prices the anchors between them — e.g. in
the 5-block U5(M) cell (v, ·, 0), the middle anchor is forced ≤ v
with no constraint imposed on it directly; a lavish middle dodge is
geometrically impossible.  Demand statements need only be proved on
a 4-adic subchain; dodges need only be excluded there.

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
- **Scale 24 (chain base q = 3, boundaries 3·2^j):** the only SAT
  record at 24 (C2 (none, 0)) passes all three laws with the octave
  logic run on the odd-base chain — all payment on β(96) = β(4M)
  (894/913), boundaries 24/48 clean: the lavish top-boundary export
  is scale- and base-stable.  10/10 team-records pass in total.

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

- **F(16; 6): UNSAT [983.5 s local under load-140 contention;
  landed after the pre-registration below was committed].**  Note
  F(M; v) is a RELAXATION of (v, 0) (s1 freed below), so this is
  strictly stronger than the (6,0) pump cell.
- F(24; 65): running on the pod (same shape at the second pump
  scale), with an independent pod F(16;6) as cross-check.

**Lemma L-FRESH-DECOMP [PROVED — L-PREFIX part (i) machinery, one
seam only].**  Under x_{β(M)} = 0 alone, each team is block-ordered
at the s0 seam ([Bm1∩T] ≺ [B0∩T]), so every mono H_dn triple
(u, y, 2y−u) ∈ (Bm1×B0×B1)∩T³ has u ≺ y forced and must break on
its s1 edge (2y−u ≺ y), edge-injectively.  Hence in any F-model,
n_s1 ≥ μ_dn(col) and the upper budget obeys
v ≥ n_s1 + n_s2 ≥ μ_dn(col) + n_s2: **the F-cell is the (v, 0) cell
with the forced μ_dn = 0 relaxed to "μ_dn charged against the upper
budget".**  F(M; v) SAT would require a balanced coloring with
μ_dn ≤ v AND joint mixed-order price ≤ v; F UNSAT says even paying
for its own H_dn floor on the shared seam, no coloring clears the
upper anchor at v.

Pre-registered readings (committed before the verdict; the UNSAT
branch is now operative).  UNSAT ⟹ by T-FORCE-4, every valid
balanced pair with Inv_T(16) ≤ 6 for both teams has a team with an
inverted pair at β(16) — currency DISJOINT from everything priced at
anchor 16 and above: the pump is NOT ledger-neutral, cheap upper
anchors mint fresh currency one boundary down, booked disjointly by
T-LEDGER.  SAT ⟹ the forced lower payment can ride entirely on the
doubly-priced shared seam: the pump's fresh-currency claim fails,
disjoint demand lives only at the 4-adic granularity, and T-TEL′
branch (b) weakens from "one fresh pair per 2 octaves" to the D3
covering constant.

**Verdict: freshness is FORCED at the first pump scale.**  With
L-FRESH-DECOMP this reads: even when a coloring is allowed to pay
its own μ_dn floor on the shared seam inside the upper budget, no
balanced coloring of (8, 128] clears Inv(16) ≤ 6 with β(16) clean —
the fresh mint is not an artifact of the vdn = 0 collapse.
Corollary (a fortiori, by restriction): the 2-step chain cell
U5(16) (6, ·, 0) is UNSAT — cheapness at 16 with a free bottom
anchor 4 is impossible REGARDLESS of the middle anchor's behavior
(which L-SQUEEZE auto-prices ≤ 6 anyway); no run needed.

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
- [GAP-VMIN0-growth] v_min(0)(M) → ∞ (measured, four scales, all
  monotone: > 6 at 8, > 6 at 16 with SAT at 384, > 65 at 24, and NEW
  this session **> 256 at 32** ((100,0)@32 UNSAT 62.6 s, (256,0)@32
  UNSAT 137.2 s on the pod — deep-UNSAT stays cheap at the fourth
  scale; (512,0)@32 queued).  The curve exceeds the entire v*₃
  bracket at every measured scale, grows ≈ ×4 per scale step
  24 → 32, and its lower bound at 32 (256) already approaches the
  16-scale UPPER bound (384)).

Then every valid pair in regime (I) satisfies, along any 2-adic
chain, at least one of:

  (a) **de facto price divergence, with an echo:** limsup_j
      max_T Inv_T(N_j) = ∞.  Indeed if I(N_j) = 0 for infinitely
      many j, then at each such j: x_{j+1} = x_{j+2} = 0 for both
      teams, and the pump forces some team T with
      Inv_T(N_{j+1}) = x_{j+2}(T) + x_{j+3}(T) ≥ v_min(0)(N_{j+1});
      since x_{j+2}(T) = 0, the whole payment sits on x_{j+3}(T) —
      whence **L-ECHO [PROVED]**: the SAME team also pays
      Inv_T(N_{j+2}) ≥ x_{j+3}(T) ≥ v_min(0)(N_{j+1}).  A zero
      anchor forces the giant payment to echo at TWO consecutive
      anchors above, same team — the lavish dodge is booked twice;
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

**Bounds caveat (standard but load-bearing) — and its measured
answer.**  The bal pump cells do NOT transfer to ε-linear bounds
(Lemma M(b); Corollary D1 applies a cell only at anchors with
μ(N) ≥ its bound vector), so T-TEL′ on all of regime (I) needs the
pump at constant or c_ε bounds.  MEASURED this session: **the
const-bounds pump fires — (6,0)@24 at bounds (2,3,6,12) UNSAT
[106 s, pod]**.  By D1 + D2 this demand applies at EVERY Case-2
anchor with μ(N) ≥ (2,3,6,12), i.e. cofinitely many anchors of
every Case-2 pair: the pump is not a balance artifact.  The
const-bounds growth ladder ((65,0)@24, (100,0)@32 const) is queued;
[GAP-J-schema] should be stated and proved at const bounds.

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
| audit (10 team-records, 5 witnesses, chains q = 1 and q = 3) | ALL PASS | — | L-HOME, seam-disjointness, L-2PRICE exact; overlap ≡ s1 identically; C1 overlap maximal (6/6); fresh mass 32; lavish witnesses export to the top boundary at both scales |
| pump (6,0)@16 via e173 encoder | UNSAT | 2.1 s | cross-validates the new generalized encoder against e158 verbatim |
| **pump (6,0)@8** | **UNSAT** | 2.1 s | **NEW: v_min(0)(8) > 6 — the pump fires at the BOTTOM scale, where BOTH standalone anchors are free (v*(bal,8) = 0); the chain step exists at every measured scale** |
| **bal (100,0)@32** [pod] | **UNSAT** | 62.6 s | v_min(0)(32) > 100 |
| **bal (256,0)@32** [pod] | **UNSAT** | 137.2 s | **v_min(0)(32) > 256** — the growth curve's 4th monotone point; (512,0)@32 queued |
| **const (6,0)@24 at (2,3,6,12)** [pod] | **UNSAT** | 106.0 s | **the pump exists at constant bounds — regime-wide demand (D1+D2), not a balance artifact**; const growth ladder queued ((65,0)@24, (100,0)@32) |
| **fresh F(16;6)** | **UNSAT** | 983.5 s | **freshness FORCED: cheap upper anchors mint β(M)-currency disjoint from all upper-priced pairs (§3); strictly stronger than the (6,0) pump cell** |
| fresh F(24;65) | pod, in flight | | scale-2 freshness; + independent pod F(16;6) cross-check |
| five U5(16): (6,·,0) | UNSAT (implied) | — | a fortiori from F(16;6) by restriction; middle anchor auto-priced ≤ 0+6 (L-SQUEEZE — no parking space); not run |

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
