> **SUPERSEDED — KNOWN FALSE AS STATED.**  The symmetric bound
> below ("Balance law: |H(v) − L(v)| ≤ |S^c ∩ (v, 2v)| + O(1)") is
> FALSE: the downward law's completions 2v − u land in (0, v), so
> that direction is bounded by |S^c ∩ (0, v)|, a DIFFERENT range —
> no symmetric single-range bound holds.  Corrected asymmetric
> version: paper/main.tex, Lemma "Balanced placement" (lem:balance;
> misstatement caught by J. Geneson).  The upward law (*) and the
> record special case are correct as stated.  (Review remediation
> notes/88 item 4.)

# The balanced-placement law (new, proved)

Let S be permutable with 3-AP-free permutation π. Consider the moment a value v is placed. Let
- L(v) = # already-placed values in [1, v),
- H(v) = # already-placed values in (v, 2v),
- δ_v·v = |S^c ∩ (v, 2v)| (non-members of S in the doubling window above v).

**Upward law (*).** Every already-placed x < v forms an increasingly-placed pair (x, v); its completion 2v − x ∈ (v, 2v) must be already placed if it lies in S. Distinct x give distinct completions, so
  H(v) ≥ L(v) − |S^c ∩ (v, 2v)|.

**Downward law (**).** Every already-placed u ∈ (v, 2v) forms a decreasingly-placed pair (u, v); its completion 2v − u ∈ (0, v) must be already placed if in S. Hence
  L(v) ≥ H(v) − |S^c ∩ (v, 2v)| − (boundary terms).

**Balance law.** |H(v) − L(v)| ≤ |S^c ∩ (v, 2v)| + O(1) at every single placement step, for every permutable S.

Special cases:
- Records (v larger than everything placed): H(v) = 0, so L(v) ≤ |S^c ∩ (v, 2v)|. **A record can be placed only when almost nothing below it is placed** (at most the codensity of its upper window). For S = ℤ⁺ this forces the second element ≤ a₁/2 etc. — a quantitative sharpening of the DEGS mechanism.
- "Last-placed of an initial segment" arguments force entire windows (v, 2v) to be pre-placed, giving doubling ladders.

Status: necessary, not sufficient; alone it does not reprove DEGS (the law admits infinite formal schedules for ℤ⁺), so the route to density upper bounds needs the law PLUS finer bookkeeping of who absorbs completions. Promising target: first-ever upper bounds α(3) < 1, and the LV-conjecture route to #197-NO (α + β < 1).

# Lessons from experiments today

1. e1/e4 (SAT, exact): ALL alternating interval schemes (14 growth patterns, both 1-conventions) are UNSAT by block ≤ 5. Minimal core at dyadic block (16,32]: 15 of 16 values — diffuse obstruction, no small gadget.
2. Pair/group-reversed block orders don't escape: in any contiguous-block schedule some own-block k+2 is played after own-block k (else infinite descending chain of naturals), recreating the fatal zone (M/4, M/2]. Verified UNSAT for that zone alone at M=16; TODO: verify M=32,64 and prove for all M.
3. Scale-monotone ("no-delay") schedules with MIXED windows collide on completion-claims (both teams' completion sets blanket the next window). Combined with (1)+(2): **any YES-solution requires non-contiguous, delayed placements at infinitely many scales.**
4. e7 (full-problem prefix SAT with IOUs): SAT for all tested N — as expected, finite prefixes cannot express the infinite pressure (even the known-impossible single-team case stays finitely SAT). Prefix SAT is an exploration tool, not a decider. The infinite structure must be captured by invariants (automaton/self-similar synthesis) or defeated by potential arguments (balance law + descent).

# Route map (both directions still open)

- NO-direction (currently favored by evidence): balance law + record lemma + completion-absorption accounting between two teams → target α(3) + β(3) < 1. LV proved α ≥ 1/2, β ≥ 1/4 and conjectured tightness; ANY upper bound < 1 is new.
- YES-direction: synthesize automatic-sequence solutions (assignment + order defined by finite automaton on binary digits), verified by finite checks + induction schema. The delay-necessity results say the automaton must implement genuine reservoirs.
