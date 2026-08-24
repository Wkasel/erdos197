# The HS identity web (2026-08-24 afternoon)

From the Hirose–Saito deep-dive (notes/15): finite-ray versions of their
chaotic-order identities apply wherever S_A contains AP-runs: for every ray
a, a+d, ..., a+2(t+2)d ⊆ S_A (t odd) and even s < t:
    f(a) ≺ f(a+d)  ⟺  f(a+sd) ≺ f(a+td).

Results:
- Web sizes: 294 identities at X=64; 30k at 256; 2,212,008 at 1024.
- Pure system + full web: SAT at 64/256/1024 (65s at 1024!). The HS-based
  NO-route (identity accumulation contradicting ω-type) FAILS at these scales;
  the identities are consistent with doom-free arrangements.
- Quotient: linked pairs collapse ~95× (64,734 linked pairs → 162 components
  at 1024). The web rigidly orients whole ray-bundles from single choices —
  matching the observed low-bit class rigidity of witnesses. ~72% of raw pairs
  are unlinked (mostly cross-ray comparisons; many appear in no constraint).

Interpretation:
- YES-side: the web is free constraint-propagation — any construction only
  needs to choose component orientations + genuinely-free pairs; candidate
  uniformization: orient components by a scale-invariant rule (components are
  ray-bundles = naturally indexed by (d-odd-part-class, position-band)).
- The ray-run-length profile of a set S (long runs at low ν₂, short at high
  ν₂ for dyadic-blocks S) emerges as the governing invariant: HS theory rigidly
  constrains low levels, leaves block-scale placement free — precisely the
  structure our witnesses exhibit. Classification conjecture: 3-permutability
  of S is governed by its ray-run profile (details to develop).

## Viability breakthrough (same afternoon)
Pinned-fraction states (7/8 etc.) refuted at c=1 — but CLEAN joints (free
extras) are SAT at X=16 and X=64 (108s): viable State(64) = complete-256 MINUS
A SINGLE VALUE (215). Viable states are "complete minus O(1) defect", not
fraction-shaped. New working conjecture: defect size stays O(1) across scales;
extension lemma reduces to bounded-defect states. Rolling chain (fixed viable
state → next joint) running on pod (roll_256.log).

## THE DEFECT LAW (evening breakthrough)
Verified-chain anatomy (exact ladder witnesses): each completion level
withholds EXACTLY one thin 2-adic class of its top block:
  scale 64: class ≡2 mod 8 (4 values); scale 256: ≡2 mod 16 (8 values);
  scale 1024: ≡2 mod 16 + spillover. LAW: defect(comp) = {v ∈ top block:
  v ≡ 2 mod 2^{k/2}}, k = log2(comp); all defect values have ν₂ = 1 (2·odd).
LAW-PINNED LADDERS: SAT at d=2 (4s) and d=3 (172s) — the first finitely-
describable invariant surviving multi-level exact verification. d=4 running.
Proof target: "every law-state extends to the next law-state" — defect values
are 2·odd in a thinning class; the absorption/class calculus applies directly.
