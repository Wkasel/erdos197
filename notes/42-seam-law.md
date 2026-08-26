# G4b: the stage-seam law, T-PIN-STAGE, and the price of crown splitting

## Question (TASK G4b)
THE LAST SHAPE (STATUS "Growing-sliver verdict" §4): stage-alternating
ownership — team A owns super-blocks (2^{a_k}, 2^{a_{k+1}}] for even k,
B for odd, stage lengths L_k = a_{k+1} − a_k → ∞, donated slivers only
at stage seams.  Deliverables: (1) the stage-seam analogue of the d_t
law (which fixed values attack which surfaces across a seam, exact iff,
mirroring notes/39 §4 CHECK-8); (2) the crown split-consistency theory:
derive T-PIN-STAGE precisely — does the thm:ogred overflow work with
pair and blocks inside one stage / across stages? — and, if splitting
is forced, quantify the landing-pad price of the planted values and its
compatibility with the partner's cleanliness.

**Answers.**
1. The seam law is a 7-channel catalogue (§2), machine-exact on 9
   stage-alternating variants × 26 seam instances × 24 attackers
   (CHECK A, experiments/g4b_seam_law.py, data/g4b_results.json).
   Headlines: the d_t dial DOES NOT EXIST in stage geometry — the
   hot-potato cross-stage channel of notes/38-39 is CLOSED (X2), and in
   exchange (a) bottom slivers are pure poison (C1: EVERY fixed x of
   the receiving team attacks, no x-threshold, no schedule escape),
   (b) donation protects nobody (the donor's kept bottom is attacked
   in-stage regardless, C0), and (c) a NEW dense channel opens that
   octave-alternation never had: a fixed x attacks EVERY value of a
   non-top in-stage block with completions in the NEXT in-team block —
   Θ(M) forced precedences per block pair per attacker (vs Θ(x) in
   OG).  This is the stage rung STG (§4), the shape's real exposure.
2. T-PIN-STAGE holds (§3): the ogred pigeonhole works verbatim with
   the attacked blocks counted in TOTAL across stages (per-stage counts
   irrelevant, exactly as the task memo's YES-candidate guessed), so a
   team keeping any crown pair whole plus infinitely many in-team
   blocks above it is dead (unconditionally for pair {15, 16}; modulo
   per-j cores otherwise — and the j = 5 core {31, 32} is now
   machine-UNSAT at 3 scales, CHECK D).  Slivers can only puncture the
   two boundary octaves of a stage, so interior blocks are punctured by
   pair SPLITS alone — and the machine closes the last escape hatch
   (CHECK B): **the C3 core SURVIVES the puncture that splitting
   creates** — AP+C3 stays UNSAT on (M, 2M] minus {2M}, minus {2M−1},
   and minus both, at M = 64, 128, 256 (mod-8 SAT control passes), so
   split-punctured blocks inherit the death core no matter the
   orientation.  Hence survival FORCES splitting all but O(1) pairs
   per stage, with no orientation loophole.
3. The landing-pad price (§5): splitting is combinatorially FREE at the
   dust level (ORIENT lemma: consistent orientations kill every fixed-x
   dust coupling; machine: the engineered halfBT variant has ZERO dust
   triples at all seams) but structurally UNAVOIDABLE at seams: every
   split of a seam pair {2^{a_k}−1, 2^{a_k}} hands the NEW OWNER a
   fixed-cohort attack fan (EVERY fixed x of the new owner attacks,
   both orientations — the completion octave belongs to the new owner
   either way).  Both teams are new owners at half the seams, so **no
   stage-alternating team with split seam pairs is clean in the G3
   sense** — the two clean teams of notes/38-40 have no analogue here.
   The fan's own per-seam gadget is single-middle and trivially SAT
   (signature, not death); death, if it comes, comes from the Θ(M)
   channel — see the STG verdict (§4).

Everything below is machine-checked by experiments/g4b_seam_law.py
(CHECK 0/A/E structural, CHECK B/C/D SAT; data/g4b_results.json,
data/g4b_run.log).

## 1. Geometry and notation

Stage boundaries a_0 = 0 < a_1 < a_2 < ..., stage k = octaves
(a_k, a_{k+1}] (octave j = (2^{j−1}, 2^j]), owner W_k = A for even k.
Seam k: the boundary a_k, seam value m = 2^{a_k}, old owner
O = W_{k−1}, new owner N = W_k.  Deviations from pure super-blocks:
- bottom sliver σ_k: N donates (m, m + σ_k] to O;
- top sliver τ_k: O donates (m − τ_k, m] to N;
- pair-split plants: for a split level j, one member of the crown pair
  Π_j = {2^j − 1, 2^j} (both live at the top of octave j) goes to the
  partner of octave j's owner; orientation β_j = T plants the top 2^j,
  β_j = B plants the bottom 2^j − 1.
Necks: with I = (lo, hi] a team's super-block, 2·lo − hi ≈ −2^{a_{k+1}}
→ −∞ once L_k ≥ 2 — the interval-view neck of notes/39 §4 is hugely
NEGATIVE, so in-interval attacks by every fixed x are unconditional
(channel C0), and conversely 2·hi(stage k) < lo(stage k+2) once
L_{k+1} ≥ 2, so the cross-interval seam channel of Lemma NECK is EMPTY
(X2).  Stage geometry sits at the opposite pole from octave geometry:
all attack surface is in-stage, none is cross-stage.

## 2. The seam law (exact channel catalogue)

For a fixed in-team attacker x (fixed = not growing with the scale) and
middle y in the 4-octave window around seam k, the COMPLETE list of
in-team attack channels (x, y, 2y − x):

| ch | attacked team | middle y | completion z | exists for fixed x iff |
|----|----|----|----|----|
| C0 | either T | kept, stage s | kept, SAME stage s | always (neck → −∞); for y in a non-top block: z in the next in-team block — Θ(M) units per block pair |
| X2 | — | stage s | stage s+2 | NEVER (L ≥ 2 closes it) |
| C1 | O | O's kept top octave a_k | O's received bottom sliver (m, m+σ_k] | σ_k ≥ 2, or σ_k = 1 ∧ x odd; count ⌈σ_k/2⌉ (x odd) / ⌊σ_k/2⌋ (x even) |
| C2 | O | received bottom sliver | planted member of Π_{a_k+1}, if planted into O | β=T: x even, 2 ≤ x ≤ 2σ_k; β=B: x odd, 3 ≤ x ≤ 2σ_k+1 |
| C4 | N | received top sliver (m−τ_k, m] | N's kept first octave | every x, count ≈ τ_k (exact set: w ∈ [0, τ_k) with 2m−2w−x kept-N) |
| C5 | N | planted member of Π_{a_k−1}, if in N | received top sliver | β=T: 2 ≤ x ≤ τ_k−1; β=B: 1 ≤ x ≤ τ_k−3 |
| FAN | N | planted seam-pair member p ∈ {m−1, m} | N's kept first octave | EVERY x ∈ N (count 1; x = 1 may reclassify as DUST) |
| DUST | the team holding 1 | pair-j value | pair-(j+1) value | x = 1 only: (1, 2^j, 2^{j+1}−1) at orientation junctures (β_j, β_{j+1}) = (T,B) interior / (B,B), (T,T) at seams, with ≥ 1 plant among the two and 1 in the same team |
| SLIVIN | O | in-sliver | in-sliver | only x ≥ m + 2 − σ_k (scale-adapted; empty for fixed x as m → ∞) |

Reading against the d_t law (notes/38):
- The octave-geometry receiver condition "x ≤ d_t − 1" had a schedule
  dial; C1's condition has NONE — the attacking surface (the receiver's
  own stage-top octave) is full and in-team, so every fixed attacker
  fires as soon as σ ≥ 2.  Bottom slivers at seams are strictly
  harmful; the optimal stage-alternating schedule is σ ≡ 0.
- The octave-geometry owner condition "x ≥ d_t + 2" is replaced by
  "always" (C0): donation cannot protect the donor because the
  completions off its kept bottom land in its OWN second octave, not in
  the partner's territory.  Growth of σ has no defensive function at
  all — the d_t zero-sum dial degenerates to a single loser.
- The one genuinely new exposure is C0's dense sub-channel: consecutive
  in-team octaves mean a fixed x attacks every y of block (M, 2M] with
  completion in (2M, 4M].  In octave-alternating partitions this
  channel does not exist (the next octave is always the partner's);
  it is the defining vulnerability of stage ownership (§4).

Machine (CHECK A): 9 variants (tri/quad stage growth × σ ∈ {0, k+2, 6}
× τ ∈ {0, 4} × orientations top/bot/mixTB/halfBT/none), seams at
m = 32...4096, all x ≤ 24: every found triple classifies into the
catalogue (completeness — the classifier RAISES on anything else), and
every per-channel existence iff + count formula matches exactly
(soundness), including predicted absences: X2 never occurs; the
no-split-no-sliver variant has C0 only; halfBT has zero DUST.  The one
catalogue surprise found and absorbed: in-sliver APs (SLIVIN) exist at
small seams where x ≤ 24 is not yet "fixed" relative to m — they
vanish for fixed x at large scales, the bounded-description boundary
family of G3 again.

## 3. T-PIN-STAGE and forced splitting

**Theorem T-PIN-STAGE.**  Let T be one team of ANY partition of Z⁺ (no
geometry hypothesis).  Suppose
(i) both members of Π_j = {2^j−1, 2^j} lie in T for some j ≥ 4;
(ii) T contains infinitely many INTACT dyadic blocks (M, 2M],
     M = 2^m ≥ 2^j (automatically pairwise disjoint);
(iii) OG_j(M) — AP-free linear order of (M, 2M] with units z ≺ y for
     every attack (c, y, z), c ∈ Π_j, z = 2y − c ∈ (M, 2M] — is UNSAT
     for all but finitely many of those M.
Then T is not permutable.
*Proof.*  thm:ogred's pigeonhole verbatim: pos(2^j−1), pos(2^j) are
fixed; at most max(pos) of the disjoint blocks meet the initial segment
before both attackers; some block (M, 2M] lies entirely after both; the
restriction of the arrangement to Π_j ∪ (M, 2M] is monotone-3-AP-free
and realizes OG_j(M) (both attackers precede the block, so each attack
forbids the increasing pattern, forcing z ≺ y).  Contradiction.  ∎

Remarks.
- The blocks are counted in TOTAL, across all stages: the overflow
  never cares which stage a block lives in — positions are global.
  This resolves the task memo's question with YES: pair and blocks may
  sit inside one stage, or spread over all of them; what must diverge
  is Σ_k #(intact in-team blocks above 2^j), and with L_k → ∞ each
  stage k of T contributes L_k − 2 interior octaves (CHECK E:
  divergence + disjointness asserted on both stage schedules).
- For j = 4: (iii) is thm:c3core — every interior scale is a power of
  two ≥ 8, hence ≡ 0 mod 8.  UNCONDITIONAL death.
- For j ≥ 5: (iii) is open per j (notes/37); CHECK D probes the j = 5
  pair rung OG_5(M) at M = 64, 128, 256 — see §4b for the verdict.

**Bookkeeping lemma (why splitting is forced).**  An interior block of
a stage (octave neither first nor last) contains no sliver values —
slivers live only in the boundary octaves.  Its only possible puncture
is a split of its own top pair Π_{m+1} (octave m+1 contains exactly the
pair Π_{m+1} as its top two values, no other pair).  Hence if T keeps
pairs whole at infinitely many levels of its own octaves, it keeps
infinitely many intact interior blocks; taking j = its lowest kept
level ≥ 4, T-PIN-STAGE applies.  Contrapositive: **a surviving
stage-alternating team splits all but finitely many of its pairs —
i.e. all but O(1) pairs per stage, Σ(L_k − O(1)) = ∞ engineered
exclave plants** (donations that are NOT seam slivers: the shape's
"slivers only at seams" definition cannot split interior pairs; the
shape must be extended by per-octave single-value plants).

### 3b. Puncture robustness (CHECK B) — no orientation loophole

The split itself punctures every block at its top pair, so the
machinery T inherits on its remaining blocks acts on (M, 2M] MINUS a
top-pair member.  Going in, this looked like a possible escape hatch
(the c3core ladder was "only proven for intact blocks" — STATUS).
Machine verdict (AP + C3 units, M = 64, 128, 256, plus M = 68 ≡ 4
mod 8 SAT control): **the C3 core survives every puncture pattern** —
UNSAT on (M, 2M] \ {2M}, \ {2M−1}, and minus both, at all three
scales; the ≡ 4 mod 8 control is SAT (engine sane).  This is the
expected direction (the puncture only REMOVES AP constraints through
the top values, and none of C3's six special values b₃, b₅, b₆, t₃,
t₅, t₁₀ is 2M or 2M−1), but it needed the machine because UNSAT is
not monotone under constraint removal.  Consequences:

- T-PIN-STAGE's hypothesis (ii) may read "intact or top-pair-punctured
  blocks": for a stage-alternating team EVERY interior block qualifies
  automatically (interior blocks lose at most their planted top-pair
  member — slivers cannot reach them, §3's bookkeeping lemma).  So
  keeping ANY pair Π_j whole (j = 4, or j = 5 by CHECK D, or any j
  with a per-j core) is fatal no matter what is split above: the
  forced-splitting conclusion has NO orientation or puncture loophole.
- The hand-schema extension of thm:c3core to punctured blocks should
  be a one-paragraph check (the flood/zigzag lemmas never use the top
  two values); flagged for the paper.
- CHECK D (per-j spot): the OG_5 pair rung — attacks of {31, 32} on
  (M, 2M], 31 units — is UNSAT at M = 64, 128, 256.  First machine
  evidence that the per-j analogue family exists at j = 5; on
  power-of-two scales every residue condition mod 2^r is free, so
  stage geometry is the friendliest possible home for per-j cores.

## 4. The stage rung STG — where death must come from

The seam law leaves exactly one dense per-scale structure: two (or
more) consecutive in-team blocks + fixed small attackers.

**Definition STG(M, F).**  AP-free linear order of W = (M, 4M] (blocks
B1 = (M, 2M], B2 = (2M, 4M]) with units z ≺ y for every attack
(x, y, z), x ∈ F, y, z ∈ W.  For y in the top half of B1 the
completion lands in B2: EVERY such y is attacked — Θ(M) units per
attacker, against OG's Θ(x).  Punctured form: W minus the planted
top-pair members (per §3b orientation).

**Theorem (T-PIN-STAGE, rung form).**  If a team T contains a fixed
finite set F and, for infinitely many scales M, two consecutive blocks
(M, 4M] with in-team content ⊇ the STG window, and STG(M, F) (in the
matching punctured form) is UNSAT at cofinitely many of those scales,
then T is not permutable.  (Same pigeonhole; the windows are disjoint
for distinct scales spaced ≥ 4×.)  EVERY stage-alternating team with
L_k ≥ 2 infinitely often has such windows; both teams do.  So
STG-UNSAT at fixed F would kill the whole shape class — and, combined
with notes/38-40 (octave-alternating dead by the d_t law), would close
ALL block-granular partitions: a partition of octaves either gives some
team infinitely many adjacent octave pairs (STG windows) or is
eventually exactly octave-alternating.

**Machine verdict (CHECK C + probes; every UNSAT via the UNSAT-sound
CEGAR path, every SAT with verified witness):**

| config on (M, 4M] | M = 64 | 128 | 256 |
|---|---|---|---|
| single x = 3 (intact / punct) | SAT / SAT | SAT / SAT | SAT / SAT |
| single x = 15 (intact / punct) | SAT / SAT | SAT / SAT | SAT / SAT |
| pair {15, 16} (intact / punct) | U / U | U / U | U [70 s] / U [38 s] |
| pair {21, 22} (intact / punct) | U / U | U / U | U [245 s] / U [92 s] |
| pairs {3,4}, {3,5}, {5,9}, {19,27}, {21,25} | U | U | — |
| puncture torture ({21,22}, {3,5} × bottom-orient / all-4-pair / 8 arbitrary) | U | U | — |
| single x = 3, 15 on THREE blocks (M, 8M], M = 32, 64 | SAT | SAT | — |

(data/g4b_results.json, g4b_stg_probes.json, g4b_stg_probes_q3.json.)
Reading:
- **Every fixed pair tested kills two consecutive blocks** — adjacency,
  parity, crown-ness, and puncture pattern all irrelevant (the {15,16}
  intact rows are implied by thm:c3core, the punctured ones by CHECK B;
  everything else is NEW, with no C3 available: the certificate rides
  an unknown core, same open crux as S2's truncated pair rungs).
- **Single attackers never force** — SAT even with Θ(M) units on two
  blocks and on three consecutive blocks (M, 8M].  The pair is the
  atom of death, now in fully generic form.
- With T-PIN this makes every stage-alternating team dead modulo the
  STG rung family: any team owns some fixed pair of generic adjacent
  values (splitting only relocates CROWN values), and infinitely many
  disjoint interior octave-pair windows in whatever puncture state the
  forced splitting left them — machine-true at 3 scales × many pairs ×
  5 puncture patterns, zero exceptions.

### 4b. The single-block collapse (discovered via controls): the
### portable crown goes generic

Control probes for §4 accidentally settled an old question: the pair
phenomenon on SINGLE full blocks is NOT crown-specific.  On (M, 2M]:

- {3,4}, {3,5}: SAT at M = 64, 128, 256 (too few units, ~x);
- **{21, 22}: UNSAT at M = 64, 128, 256** — a non-crown pair kills a
  single intact block;
- threshold map at M = 128: {7,8} SAT, {9,13} SAT, then {11,12},
  {13,14}, {15,17}, {17,18}, {41,42} all UNSAT — the classic {15, 16}
  was never magic, only conveniently located; adjacent (or gap-2)
  pairs from ≈ {11, 12} upward all carry a death core;
- **chain form: {65, 66} (a pair INSIDE the block (64, 128]) kills
  (128, 256], (256, 512], (512, 1024]; {100, 101} and {129, 130} kill
  (256, 512]** (data/g4b_stg_1block_controls.json,
  g4b_stg_1block_threshold.json, g4b_stg_chain_probes.json).

**Consequence (T-PIN-BLOCKS, the generic-pair portable crown).**  If
the generic-pair single-block rung family is UNSAT at all large
scales — machine-true at 15+ configurations, x = 11..130,
M = 64..512, zero exceptions — then ANY team of ANY partition
containing infinitely many full dyadic blocks is dead: take the
attacker pair inside the team's own lowest block (adjacent generic
values, abundant in any full block — crown splitting cannot remove
them), thin the remaining blocks to a disjoint family above it, and
run the T-PIN pigeonhole.  NO hypothesis about crowns, small values,
or geometry survives in the statement.  Its contrapositive is the
strongest structural forcing of the campaign:  **a surviving partition
must split all but finitely many dyadic blocks between the teams —
"block-poor" (trichotomy escape (2)) stops being one escape among
three and becomes the ONLY regime any YES-partition can live in.**
CHECK D (OG_5 {31, 32} UNSAT at 3 scales) is the special case j = 5
of the same picture.

## 5. The landing-pad price and cleanliness

The forced plants put, inside each stage of T, one partner value per
octave at the octave top: the partner's holdings across T's stages are
a geometric "crown dust" {p_j}, p_j ∈ {2^j−1, 2^j}.  Price analysis
(all machine-exact in CHECK A):

- **Dust is internally AP-free** under any consistent orientation
  (all-T: {2^j} contains no 3-AP; all-B: {2^j − 1} likewise), and all
  fixed-x channels into or out of the dust are CLOSED except the x = 1
  coupling (1, 2^j, 2^{j+1}−1), which exists exactly at orientation
  junctures (β_j, β_{j+1}) = (T, B) interior, (B, B)/(T, T) at seams,
  in the team holding 1.
- **ORIENT lemma.**  The juncture constraint system (avoid (T,B)
  inside stages, avoid (B,B) and (T,T) at seams) is satisfiable — e.g.
  per-stage B...BT...T with the flip at mid-stage (the seam juncture
  is then (T, B), allowed; interior junctures are (B,B), (B,T), (T,T),
  allowed).  Machine: the halfBT variant carries ZERO dust triples at
  every seam tested, while mixTB (which contains interior (T,B)
  junctures) and uniform top/bot (which contain (T,T)/(B,B) seams)
  carry exactly the predicted dust and nothing more.  Since §3b found
  no orientation forcing (the C3 core survives both puncture
  orientations), the dust-evading patterns are genuinely available:
  a surviving shape can be dust-free.  Dust is a consistency TAX only
  on naive (uniform) orientations, not an obstruction.
- **The seam fan is unavoidable regardless.**  Splitting the seam pair
  (forced, §3) hands its planted member to the new owner N (both
  members' completion octave a_k + 1 is N's first octave, either
  orientation), so EVERY fixed x ∈ N attacks at every seam where N is
  new owner.  Machine: FAN fires for every in-team x ≤ 24 at every
  split seam of every variant, count exactly 1, both orientations,
  minus exactly the predicted losses (x = 1 reclassified as dust;
  completions swallowed by the next level's plant).  Consequence:
  **both teams carry fixed-cohort attacks at infinitely many scales —
  no stage-alternating team is clean.**  The two clean teams of the
  octave-alternating world (geo/A, geomirror/B) are a phenomenon of
  octave alternation, not reproducible here.
- Compatibility with cleanliness, quantified: the dust + fan are
  Θ(1) units per seam (sparse, RUNG-X-lin-like: plausibly SAT forever
  as per-scale gadgets); the C1/C2 sliver channels are avoidable by
  σ ≡ 0; what is NOT sparse is C0's Θ(M) block-pair channel, which
  needs no plants at all.  So the landing-pad price of splitting is
  "signature everywhere, rung nowhere" — the decisive question is STG
  (§4), and the plants only modulate its puncture pattern (§3b).

## 6. Verdict and where the program stands

**THE LAST SHAPE IS DEAD MODULO MACHINE-TRUE RUNGS — and the death
argument found this session is bigger than the shape it was aimed at.**

1. **Stage-alternating ownership (G4's target): dead modulo the STG
   pair-rung family.**  The seam law closes every schedule dial (σ, τ
   are pure poison; X2 does not exist; no clean team exists because
   the forced seam-pair splits fan the new owner), T-PIN-STAGE +
   puncture-robust C3 force splitting all but O(1) pairs per stage,
   and the STG rungs then kill both teams through their consecutive
   blocks — UNSAT at 3 scales × 7 pairs × 5 puncture patterns, with
   T-SHARP-style escapes unavailable (the attackers are fixed values).
   Epistemic level: thm:ogred + thm:c3core before the C3 hand proof —
   the same level at which geo/B (RUNG-IN) and now gm/B sit.
2. **T-PIN-BLOCKS (§4b) retro-kills every block-granular geometry at
   once**: octave-alternating (notes/35, 38-40), stage-alternating
   (this note), and everything in between (irregular block ownership,
   mixed run lengths) — any partition leaving either team infinitely
   many full-or-O(1)-punctured blocks is dead modulo the generic-pair
   rung family.  The notes/38-40 d_t/NECK machinery remains the
   sharper, hand-proven route for its family, but the generic-pair
   rung is the uniform reason.
3. **What survives: exactly one regime.**  Both teams block-poor at
   cofinitely many scales — every dyadic block eventually split
   between the teams.  The 2-colored trichotomy (notes/36) collapses:
   escape (1) (crown split) is refuted as a survival mechanism
   (generic pairs replace crowns), escape (3) (endpoint donations) is
   a per-block tax whose price was already machine-mapped (exactly 3
   per attacked block), and escape (2) (block-poor) is no longer an
   escape but THE definition of the remaining YES-space.  The old
   "endgame" note (STATUS, NO-route (c)) guessed this: the burden
   transfer is now total.
4. **RUNG-X postscript (S2 closure):** the relaunched seam solvers
   from notes/39-40 came home during this session: gm/B t = 9 plateau
   seam rung — the one OG-density seam family — is **UNSAT**
   [667 s, n = 1280, 137 units, fixed 20-attacker cohort]
   (data/s2_rungx_gmB.json, s2_sg_rungs.jsonl); lin/B t = 9 (sparse
   seam, 11 units, expected SAT) still in flight at close.  With
   gm's stage-jump RUNG-IN (r = 8) and now its plateau RUNG-X, every
   parity class of every S1 schedule has a machine-true rung family
   or a proven-sparse seam.

**The single open crux, unchanged but enlarged:** a hand schema
("next-C3") for the per-scale cores.  The instance base now spans:
truncated pair rungs (S2), neck-0 interval rungs (RUNG-IN geo/B),
plateau seam rungs (RUNG-X gm/B), two-block STG rungs (any pair), and
generic-pair single-block rungs down to {11, 12} — all UNSAT, none
explained by C3 (which is one member of an evidently large family).
The right next step is core anatomy: MUS extraction across
{11,12}...{21,22} × scales to find a scale-stable schema the way
e88/e90 found C3.

**Program state after G4b:** every octave-granular geometry is dead
modulo rungs; the YES-space is squeezed into everywhere-split blocks
(both teams present in cofinitely every block) — a regime where
density 2/3 per side forces intricate per-block coordination whose
finite shadows (e118/e119) already showed strictly positive,
scale-stable prices.  NO-estimate rises accordingly (STATUS updated:
~85 %).  Decisive next experiments: (a) MUS anatomy of the generic
pair core; (b) the split-block coupled theory at two adjacent scales
(e120 of the old list, now THE front); (c) RunPod-scale confirmation
of STG/chain rungs at M = 1024, 2048.

## Reproduce
    PY=.venv/bin/python
    $PY experiments/g4b_seam_law.py --skip-sat   # CHECK 0/A/E, ~1 min
    $PY experiments/g4b_seam_law.py              # + CHECK B/C/D SAT
Artifacts: data/g4b_results.json, data/g4b_run.log.
