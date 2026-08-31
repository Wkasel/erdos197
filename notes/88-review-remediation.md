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
