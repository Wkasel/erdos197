# Erdős #197 — BOTTOM LINE (grand assembly, 2026-08-30)

*One page, referee-grade.  Authoritative dependency graph:
notes/50-assembly.md.  Full state: STATUS.md (final section).
Verification commands: REPRODUCE.md, reproduce2.sh.*

## What is proven (unconditional, hand proofs, machine-audited)

1. **Theorem (paper/main.tex, thm:main).**  S_A = ∪_{k even}
   (2^{k−1}, 2^k] is not 3-permutable.  The canonical dyadic
   partition does not resolve #197.  (Audited ×3; adversarial
   engines; fresh scales to M = 4096.)
2. **Theorem C3(p)** (notes/78 Part I): the diagonal rung is UNSAT
   on its flip class uniformly in odd p ≥ 5.  Referee prose pass
   done (notes/86 §1); identity layer independently re-derived to
   p = 47 (grand assembly), machine boundaries sharp.
3. **Theorem B1₀** (notes/88 item 3): a set containing complete
   dyadic blocks at infinitely many scales is not 3-permutable.
   Inputs PIN + DIAG-DENSE + C3(p) only.
4. **Lemma Q + Theorem ALT-DEAD + Cor. HSPLIT** (notes/82, verified
   notes/81): a valid pair has no team owning a full mod-2^k
   class-section at infinitely many scales; infinitely many 4-pure
   scales ⟹ invalid; every valid pair is everywhere-split in every
   2-adic chart.  Rider-free.  Kills the ENTIRE lattice/2^k-periodic
   YES-corner at ω — every corner witness ever found.
5. A large proved support layer: N4 frame, T-PIN, J-DOWN, T-TEL″
   composition, J-BOOT (unconditional 12 ≤ M ≤ 32), Lemma LAND +
   Theorem S1 + Cor. COR (odd-gap spiral kill, 7q + 10g ≤ 2N),
   LAT-LOW + CLIQUE-HALVE, BM1-VAC + CMIN-SMALLT, AFFORD-CORNER,
   L-NOTAIL, L-DOUBLE-DUTY, Lemma Q-g/Cor. ASPLIT (2^k arm; odd arm
   gated).  Each independently spot-verified at fresh scales at
   least once (STATUS.md grand-assembly table: 5/5 fronts confirmed,
   zero breaks; one cosmetic precision fix, notes/88 item 2).

## What is NOT proven

**Erdős #197 itself is open in both directions.**  The NO-assembly
(notes/50 §5) is conditional on exactly three hypotheses:

- **GAP-AFFORD′ / GAP-AFFORD‴-SPLIT** (terminal, genuinely new
  mathematics): no valid Case-2 pair — now necessarily a gap-≥3,
  m-adically-split-for-all-m, diffuse minority — can fund one
  displaced value per two octaves forever.  Zero completed proof
  strategies; the decisive F = 12 weak-censor inhabitant hunt was
  still running at close (no verdict).
- **GAP-N6a sub-pool** (uniformization species): region-law cell
  table (R ∖ COR), scaled zone / stall corner, ThW1′-ROBUST, (OV-∀)
  etc. — every instance ever attempted discharged, ×40-window
  machine support, but not uniform theorems yet.
- **GAP-N3-GROW (N3-b)** (uniformization species): puncture
  tolerance ⌊(x−1)/4⌋, exact at x = 11..27, skeleton stated.

Two of the three are classification write-ups with zero anomalies;
the first is not, and no phrasing should launder it.  Known
overclaim modes are quarantined (notes/88: no finite-to-ω
compactness step for the censored corners; odd-periodic minorities
only conditionally dead via the Q-ODD gates).

## How to verify

- `reproduce2.sh` (127 s): C3(p) ×3, independent solver ×3, sharp
  boundaries, Lemma Q chart + B1₀ machine layer, Geneson scan.
- Grand-assembly spot-checks: independent reconstructions in the
  session scratchpad, results tabled in STATUS.md (final section);
  the S1 spiral walker at N = 600/222 and the from-scratch CMIN
  encoder are ~100-line self-contained scripts re-derivable from
  the theorem statements in notes/84 §1 and notes/85 §0.
- Paper-grade artifacts: paper/main.tex (Theorem A material),
  paper2/main.tex (conditional assembly, three hypotheses).

## Honest probability

**NO ≈ 95 %, YES ≈ 5 %** (was 93/7 at notes/80).  Up: the realized
YES-space (lattice corner) is now dead at ω, rider-free; 5/5 fresh
spot-verifications clean.  Held back: the split residue provably
exists as a coloring class, its supply cap has no strategy, the
F = 12 cells are undecided, and this week's review found (and we
fixed) two finite-to-ω overclaims — the honesty tax is real.
