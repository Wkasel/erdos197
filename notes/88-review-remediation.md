# 88 — EXTERNAL REVIEW REMEDIATION (2026-08-30)

An external adversarial review found real issues.  The four paper
fixes shipped separately (commits 7add1b0, 59655a9).  This note is
the running log of the remaining remediation; one section per item,
committed item by item.  Terse.

---

## Item 1 — HSPLIT downgrade (review item 6): the F = 64 UNSAT does
## NOT close the strong-censor corner; "dead end-to-end" RETRACTED

**What e186 partHSPLIT actually proves.**  For hor ∈ {2048, 4096},
censor F = 64 (D = 2, u₀ = 64), the constraint system
  corner axes (split floor + minority gap-≥3 + window floor + censor)
  ∧ (every mod-4 [resp. mod-4 AND mod-8] class-section bichromatic
     at every scale 6 ≤ t ≤ t_max(hor))
is UNSAT.  Equivalently: **every finite strong-censor corner
inhabitant on [1, hor] has at least one monochromatic residue-class
section at some tested scale.**  That is ALL it proves.

**What it does not prove.**  It does NOT prove "every finite
inhabitant is a lattice" (one monochromatic section ≠ a lattice),
and it does NOT prove "every ω-inhabitant has infinitely many 4-pure
scales."  There is NO valid compactness step from the tested cells
to ω: an ω-coloring that is 4-pure at finitely many scales only
(e.g. only in the boot window t ≤ 11) is consistent with every
tested cell — its truncations simply fail the imposed t ≥ 6
bichromaticity inside the horizon — and Theorem ALT-DEAD does not
touch it.

**RETRACTED:** the notes/81 §3 inference "the strong-censor corner
is now dead END TO END: finitely, every inhabitant is a lattice; at
ω, every lattice is invalid."  Both halves fail as stated: the
finite half overstates the UNSAT, and the ω half needs the
applicability hypothesis below.

**What would be needed (open).**  *Shifted-window uniform
infeasibility*: for EVERY T ≥ 6, no corner model with all
class-sections bichromatic at all scales ≥ T (finitely: for every T
there is a horizon h(T) at which the corner axes ∧ bichromaticity
imposed only at scales T ≤ t ≤ t_max(h(T)) is UNSAT).  The ∀T
family would force every ω-inhabitant to carry monochromatic
sections at arbitrarily large scales — i.e. infinitely many 4-pure
scales — and ALT-DEAD would then close the corner.  Only the T = 6
instance was ever run.

**Unaffected:** Theorem ALT-DEAD itself (infinitely many 4-pure
scales ⟹ not a valid pair) is a proved conditional theorem and
stands; so do Lemma Q and Cor. HSPLIT.  What is now explicitly OPEN
is ALT-DEAD's applicability hypothesis on the strong-censor corner:
nothing proved forces its ω-inhabitants to have infinitely many
4-pure scales.

Edits: notes/81 §2 (pre-registered reading annotated) + §3
(corrected reading, retraction in place), notes/83 §0 "known facts",
STATUS.md FRONT ALT-CLOSURE (verdicts recorded with the downgraded
reading), notes/50 §6 GAP-AFFORD′ row + §6 closing (iv) bracket,
notes/82 §5 (pointer).

---

## Item 2 — "HSPLIT ⟹ aperiodic" RETRACTED (review item 7):
## the mod-3 counterexample is correct

**The error.**  Several places inferred "2-adically split
(HSPLIT-generic), hence aperiodic" / "stripped of every arithmetic
example".  FALSE.  Cor. HSPLIT rules out persistent monochromatic
POWER-OF-TWO residue charts only.

**The counterexample (reviewer's; machine-verified this session).**
Minority = 3ℤ⁺: fully periodic (period 3), yet every class-section
mod 2^k is bichromatic in every long block — gcd(2^k, 3) = 1 puts
both multiples and non-multiples of 3 into every class c mod 2^k of
any section of length ≥ 3·2^k.  Check: 0 monochromatic sections at
mods 4/8/16/32, t = 6..12; in-block minority gaps identically 3.
[Precision fix, grand assembly 2026-08-30: the machine sentence
above overstates at the boundary (mod 32, t = 6), where sections
have only 2 < 3 elements and 11 of the 32 classes are indeed
majority-pure — exactly the case the "length ≥ 3·2^k" hypothesis
excludes (need t ≥ k + 2).  Independently re-checked: mods 4 + 8
(the HSPLIT instrument) are bichromatic at ALL t ≥ 6, and mods
16/32 from t = k + 2 on; zero other violations t ≤ 14.  Argument
unaffected — HSPLIT imposes mods 4 + 8 only.]

**Corrected characterization (now propagated everywhere the claim
appeared):** the SPLIT residue excludes eventually-2^k-periodic
minorities [PROVED, Cor. HSPLIT] but NOT odd-periodic,
mixed-modulus, or automatic ones.  Those die, if at all, by:
L-NOTAIL [PROVED] when one team owns an infinite AP
(constant-ownership case), or Lemma Q-g / Cor. Q-ODD [stated, mod
BRIDGE1-AF + GAP-N2-UNIF + N3-GROW at C = 2] for block-alternating
ownership — open gates, so block-alternating odd-periodic
minorities are LIVE candidates.

**Test case added to notes/83 §2b** with kill attribution:
constant-ownership mod-3 dies by L-NOTAIL (equivalently B1₀ after
the gap-3 chart — the full AP transports to all of ℤ⁺, no Q-ODD
gate consumed); alternating mod-3 is killed by no fully-proved
instrument.

Edits: notes/82 §5 (×3) + §6, STATUS.md FRONT ALT-CLOSURE (×2),
notes/50 §6 row + (iv) bracket, paper2/main.tex hyp:afford,
notes/86 gating list, notes/83 axis (d) + new §2b.

---

## Item 3 — Theorem B1₀, standalone (review item 3): the
## unconditional zero-dust bridge, extracted from conditional B1

Lemma Q previously cited "Theorem B1 [PROVED mod (H1)] at C₀ = 0",
making the unconditional chain look conditional.  The standalone
statement and its direct proof:

**Theorem B1₀.**  Let T ⊆ ℤ⁺ contain the complete dyadic block
B(m) = (2^m, 2^{m+1}] for infinitely many m.  Then T is not
3-permutable.  (The scales 2^m automatically lie in the needed
residue class: 2^m ≡ 0 ≡ 2p+6 (mod 8) for m ≥ 3, p ≡ 1 (mod 4).)

*Proof.*  Suppose π is an arrangement of T with no monotone 3-AP,
and let 𝕄 be the infinite set of scales with B(m) ⊆ T.
(1) Fix m₀ ∈ 𝕄 with 2^{m₀} ≥ 32.  By Lemma DIAG-DENSE [PROVED,
notes/52 §2.1], B(m₀) contains ≥ (2^{m₀} − 13)/12 ≥ 1 diagonal
pair {3p, 3p+1} with p ≡ 1 (mod 4); p > 2^{m₀}/3 > 8, so p ≥ 9.
Both members lie in T because B(m₀) is complete.
(2) Apply Lemma PIN [PROVED, notes/52 §1.3] to the fixed pair
a₁ = 3p < a₂ = 3p+1 ∈ T with dust bound C = 0 and the infinite
scale family {m ∈ 𝕄 : 2^m > 3p+1}: for all but finitely many such
m, the rung theory R(3p, 3p+1; 2^m, ∅) is consistent.
(3) But for every m ≥ 3 with 2^m ≥ 2p+6, the scale M = 2^m
satisfies M ≡ 0 ≡ 2p+6 (mod 8) (p ≡ 1 mod 4), i.e. M is in the
flip class, so Theorem C3(p) [PROVED, notes/78 Part I; unpunctured
instance only] makes AP-freeness of (M, 2M] inconsistent with the
three C3(p) units — which are among R(3p, 3p+1; M, ∅)'s fired
units (attackers 3p, 3p, 3p+1; machine-checked exactly, e186
partQVERIFY 6/6).  Hence R(3p, 3p+1; 2^m, ∅) is inconsistent for
every such m — contradicting (2).  ∎

Inputs: PIN + DIAG-DENSE + unpunctured C3(p), all [PROVED].  No
(H1), no dust tolerance, no N3-GROW anywhere.  **Tag: [PROVED,
unconditional].**  Conditional B1 (general C₀, notes/52 §3.1)
remains as stated, mod (H1′); B1₀ is not an instance of its
STATEMENT-form (no "Assume (H1)") — it is the C₀ = 0 proof run
directly on proved inputs.

Repointed: notes/82 §2.1 step (iii) and paper2/main.tex (lem:q's
proof + the zero-dust node in the dependency graph) now cite
Theorem B1₀ instead of "B1 at C₀ = 0".

---

## Item 4 — quarantine banners (review items 4, 5): notes/01-30
## swept for claims contradicted by later results

Banners added ("SUPERSEDED — KNOWN FALSE AS STATED" or scoped
variant, each with a pointer to the superseding result):

| note | false/stale content | superseded by |
|---|---|---|
| 04-balance-law | symmetric balance bound \|H−L\| ≤ \|S^c ∩ (v,2v)\| + O(1) — downward completions land in (0, v) | paper/main.tex lem:balance (asymmetric; Geneson correction) |
| 05-lemma-R-and-status | PROVEN list includes the notes/04 balance law | same |
| 06-corrected-landscape | S_B = {1,2} ∪ 2·S_A identity + the "⇒ #197 = YES" chain on it | notes/11 §CORRECTION; paper thm:main |
| 08-paper-outline | outline items 2 (symmetric balance law) and 8 (S_B identity) | lem:balance; notes/11 |
| 12-fragility-and-endgame | "universal fragility" anti-pumping/anti-Lipschitz inferences | notes/14 (withdrawal); paper fix 59655a9 |
| 16-extension-lemma-attempt | conditional "S_A permutable ⇒ #197 = YES" — hypotheses now known to fail | paper thm:main |
| 17-identity-web | defect law D = {v ≡ 2 mod 2^{k/2}}, O(1)-defect conjecture, defect-removal repair | notes/18 §0 (refutation) |
| 19-main-theorem-skeleton | target "S_A is 3-permutable" + L1 defect-removal mechanism | paper thm:main; notes/18 §0 |

Swept clean (no false claims found; proved content stands or notes
self-correct inline): 01, 02, 03, 07, 09 (inline corrected
assessment), 10, 11 (inline §CORRECTION), 13, 14, 15, 18 (is
itself the refutation), 20–30 (technical/NO-direction notes;
notes/30 is a draft with honest per-step gap tags, superseded by
notes/33 as marked in STATUS).  MORNING-REPORT.md already carries
a historical-snapshot banner.

---

## Item 5 — Roth sentence fixed (review item 8)

notes/82 §3.2 said "one team always has upper density ≥ 1/2, so
Roth already floods both teams with 3-APs" — wrong quantifier:
subadditivity of upper density guarantees d̄ ≥ 1/2 for at least
ONE team only; the other may have upper density below any Roth
threshold (even 0).  Fixed in place ("floods THAT team"); the
argumentative point (containing 3-APs is not an obstruction)
survives unchanged.

---

## Item 6 — e180 boundary audit fixed and reran (review item 9)

**The discrepancy.**  e180 partMINM asserted the SLACK boundaries
M ≥ 2p+10 (L1) / 2p+14 (FLIP) while notes/78 §I.5 prose claimed
the sharp ones (first 4 | M ≥ p+7; in-class M ≥ 2p+6) and cited
partMINM as having verified them — a code/prose gap.

**The fix (reviewer's exact shape).**  New partMINMsharp:
first_l1 / first_flip are COMPUTED from the full scan (smallest
scanned scale from which every later scanned scale passes) and
ASSERTED equal to the sharp affine values; every scanned scale
BELOW the sharp boundary is explicitly checked to FAIL (flip scan
extended down to M = 8 so the below-set is non-empty at every p —
vacuity is recorded if it ever occurs).  Original partMINM kept
for the record with a discrepancy docstring.

**Rerun (2026-08-30).**  Registered cells p ∈ {5, 13, 21}: all
sharp, 0 mismatches (L1 first-pass 12/20/28 = sharp; FLIP
first-pass 16/32/48 = 2p+6; below-sets all-fail).  Corroboration
at all nine p ∈ {5..21}: same, 0 mismatches.  Data:
data/e180_diag_grow.json keys partMINM_sharp / partMINM_sharp_full.

**Prose aligned** (notes/78 header verdict, §I.5 boundaries
paragraph, §I.6 machine-record table, session summary; STATUS
FRONT N2-DIAG): the certified statement is now "passes from the
sharp affine boundary AND fails at every scanned scale below it";
the old prose's "fails at the ONE in-class scale below (M = 2p−2)"
was also wrong in count — for most p several in-class scales below
2p+6 fail (e.g. p = 13: M = 8, 16, 24), all with value collisions.

---

## Item 7 — reproducibility: path portability + reproduce2.sh

**Path portability.**  e123_diagonal_schema, e123b (the independent
C3 solver), e180_diag_grow, e174_n3_growth: absolute
/Users/will/... paths replaced with repo-root-relative paths
derived from __file__ (e186 was already portable).  e123b gained a
CLI p-list and a nonzero exit on mismatch; e186 gained hsplit64 /
hsplit64ctl CLI cells and the downgraded-reading docstring on
partHSPLIT.

**reproduce2.sh** (new; documented in REPRODUCE.md "Package 2"):
step 1 C3(p) schema executor p ∈ {5,7,9}; step 2 independent
solver p ∈ {5,9,13} (incl. M = 256/260); step 3 sharp boundaries
partMINMsharp p ∈ {5,13,21}; step 4 Lemma Q chart checks + B1₀
machine layer + Geneson Λ-scan with explicit JSON gates; step 5
HSPLIT F = 64 × {4096, 2048} re-solved fresh, gated UNSAT, printed
with the DOWNGRADED interpretation only.

**End-to-end run (2026-08-30): ALL 5 STEPS PASS, 127 s** (fresh
HSPLIT UNSAT reproduced at 38.4 s / 19.0 s; qverify 44/44 chart,
44,400/44,400 transport, 6/6 units, R(39,40;128) UNSAT; Geneson
hits only at boot t = 2, 4).

---

## Item 8 — rhetoric pass (review items 11, 14): regression tests
## vs universal verification

The partQVERIFY battery was described as "every machine-checkable
layer attacked, ALL PASS … SOUND, no hole found" (notes/81 §2
heading + verdict; STATUS FRONT ALT-CLOSURE; notes/50 §2d
"Adversarially verified"; paper2 §chart \source "adversarial
machine verification").  Reality: finite regression-style
spot-checks of each proof layer's machine-checkable shadow at
stated instances (chart cells t = 4..14, transport on [1, 600],
6 unit cells, one fresh rung, two witnesses' top scales) —
consistency evidence; soundness rests on the hand proofs.  All
four locations rewritten to say exactly that; "8/8 exact" scoped
to "top two pure scales per witness (8/8 cells)"; the notes/82 §5
"sharply characterized" aperiodicity phrasing was already replaced
under item 2.  ALT-DEAD/Lemma Q claims themselves are untouched
(they are hand theorems).

---

## Item 9 — percentage reframe (review item 15)

STATUS.md's "NO ≈ 96–97 %" headline (FRONT ALT-CLOSURE) replaced
with the reviewer's formulation: **a conditional NO architecture —
open theorems exactly: GAP-AFFORD′ (residue GAP-AFFORD‴-SPLIT),
the GAP-N6a sub-pool, GAP-N3-GROW (N3-b), plus ALT-DEAD's
applicability hypothesis on the SPLIT corner (item 1) and the
Q-ODD gates (item 2); many structured candidate families
eliminated unconditionally.**  The grand-assembly final section's
probability line kept but demoted to an explicitly labeled
informal internal heuristic, led by the claim-grade formulation.
A labeling rule added at the top of STATUS covers every historical
"NO ≈ X %" line in the dated FRONT sections (informal heuristics
of record, not claims).  notes/50 contains no percentage claims
(checked).

---

## Item 10 — notes/89-clean-chain.md (the reviewer's deliverable)

Written: the chain **C3(p) → B1₀ → Lemma Q → ALT-DEAD** as a
self-contained hand-off document.  Full statements throughout;
full proofs in-document for PIN, DIAG-DENSE, B1₀, Lemma Q,
ALT-DEAD, Corollaries 1–3 (lattices, on-class punctures, HSPLIT),
plus the three-line units-in-rung computation (Fact 1.3.1) so the
a-fortiori step needs no machine citation; exact pointers for the
one long proof (Theorem C3(p): notes/78 Part I; p = 5 =
paper thm:c3core + notes/33).  §4's scope remark records the mod-3
non-aperiodicity boundary (item 2); §5 states the explicitly open
applicability hypothesis of ALT-DEAD (infinitely many 4-pure
scales) and says plainly the chain does not resolve #197.  Zero
AFFORD material, zero percentages, zero censor interpretation.
Machine layer referenced only as optional corroboration
(reproduce2.sh).

---

## Item 11 — novelty guard (review item 13)

**Sweep performed** (case-insensitive, all *.md/*.tex/*.txt in the
repo incl. publish/, plus the extracted arXiv bundle main.tex,
README.md, both papers, STATUS, MORNING-REPORT): patterns
"first impossibility", "first non-permutable", "first
proof/result/theorem/example/known/such", "novel", "to our
knowledge", "no prior", "nobody has".

**Finding: no literature-novelty claim of the flagged shape exists
anywhere in the tree.**  Every "first …" hit is either (a) a
campaign-internal first, explicitly scoped ("first firing Case-2
core", "first clean partition team of the campaign", notes/05's
"first fully human-checkable impossibility gadget OF THE PROJECT",
notes/38's "first infinite CLASS death beyond S_A" — all internal
milestones, not literature claims), or (b) "the natural first
candidate" (describing the dyadic partition, both papers +
erdosproblems comment — not a novelty claim).  The one comparative
novelty sentence in the published paper ("what is new here is its
boundary-quantitative form", vs Geneson's Lemmas 2.1–2.2) is
already narrowly scoped.  MORNING-REPORT's "mapped at a depth
nobody has published" is internal, historical, and sits under a
SUPERSEDED banner — left as a dated snapshot.

**Already-public artifacts needing follow-up correction: NONE**
(checked: README.md, publish/erdosproblems-comment.md,
publish/arxiv-bundle.tar.gz::main.tex, publish/arxiv-checklist.md,
paper/main.tex, paper2/main.tex).

**Guard for future use (the reviewer's template, binding for any
forthcoming announcement or paper-2 prose):** any novelty claim
about the S_A theorem or the Lemma-Q family must be phrased as —
"to our knowledge, the first impossibility result for a natural
set that is not an affine copy of ℤ⁺ (in particular, one
containing no infinite arithmetic progression)" — never an
unqualified "first impossibility" / "first non-permutable set"
(affine copies of ℤ⁺ are non-permutable already by DEGS 1977, and
prior-literature coverage is not exhaustively known).
