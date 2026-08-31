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
