# GAP-N6a: the all-M schema of the Case-2 coupled core (session 12, inline)

Data: e126 MUS finals — M=32 (3,3,3), n=116, all-necessary, Glucose-verified;
M=48 (2,2,2), n=153, Glucose-verified. Anchor coordinates below.

## Scale-STABLE anchor families (identical at both M)
- **S1 (B0 top-run):** top_off 0..7 — the top 8 values of B0. Exact at both.
- **S2 (B1 top-run):** top_off 0..7 — the top 8 values of B1. Exact at both.
- **S3 (B2 bottom-run):** bot_off 1..16 — the bottom 16 values of B2. Exact
  at both. NOTE 16 = 2×8: S3 is the seam-2 doubling image of S2 —
  completions 2y − u with y in S2 (y ≈ 4M) and u ∈ B1 land exactly on
  (4M, 4M+16]-type material; the coupling is the sumset layer.

## SCALING families
- **S5 (B1 central band):** a contiguous run centred near 3M (bot_off
  ~M/3..~M−ε at both scales, width Θ(M)).
- **S6 (B2 midband/flood run):** contiguous band ending at/just past 6M —
  6M is B2's own centre, the analogue of the C3 proof's flood centre m₀ =
  3M/2 for a block (M, 2M] (centre-of-block law: the flood zone sits at the
  arithmetic centre of the top block). Width Θ(M); at M=48 it crosses 6M by
  +16 (= |S3|), at M=32 it ends at 6M exactly — the crossing amount tracks
  the S3 run, another seam-coupling signature.
- **S4 (B0 scattered anchors):** the only non-uniform family
  (M=32: {1,2},{9,10},{13,15,16}; M=48: {17,18,19},{29,30}) — differs
  between the (3,3,3) and (2,2,2) bounds regimes. Working hypothesis:
  these are witness midpoints of S1×S5 and S1×S6 pairs (the (u+z)/2
  geometry), hence derived, not primitive; the parametric schema should
  generate them from the primitive families.

## mod-4 structure
Near-uniform across all classes in every block at both scales — the schema
is INTERVAL-RUN based, not residue-class based. Residues should enter only
through the flood-centre condition (as in C3, where the single mod-8 appeal
is the class of m₀±1) — here the candidate condition is the class of 6M±ε
relative to the S3 run, i.e. a condition on M mod small powers of 2 that is
VACUOUS for the balanced core (which fires at every M ≥ 32 tested, all
residues) — consistent with the machine's no-residue-law finding for the
coupled core.

## Candidate all-M schema (primitive families)
CORE(M) := S1(8) ∪ S2(8) ∪ S3(16) ∪ S5(central band of B1, width cM) ∪
S6(flood band of B2 ending at 6M + |S3|, width c'M) ∪ S4(derived
midpoints). Conjecture: the (2,2,2)-bounded two-seam instance restricted
to CORE(M) is UNSAT for every M ≥ 48 (and the (3,3,3) variant for M ≥ 32).

## What a Z/D/E/P hand proof needs (assessment)
- Ladders: the S5→S6 cross-seam ladders (difference families 2M±small) play
  the role of C3's d=2 odd ladders; S2→S3 doubling coupling replaces the
  transfer lock (E) — the lock now transfers orientation ACROSS the seam.
- Flood: mirror-flood at centre 6M over the S6 band (phase-blind per
  Lemma P's template), with S3 as the anchored boundary rung.
- The bounds (2,2,2) enter as the supply of "against-type" values that the
  flood cannot route around — the quantitative hook where the ledger's
  minority profile plugs in.

Sufficiency check queued: e133 (restricted-support UNSAT at M=64 with
generous margins) — running.

## Sufficiency check verdict (e133, M=64): **SAT (11s) — schema as
parameterized is NOT sufficient.** The generous-margin CORE(64) guess
(|support| = 212) admits a satisfying restricted instance: the true core
uses values outside the guessed bands — the S4/S5/S6 scaling between
M=32→48 does not extrapolate linearly to 64 (two data points were not
enough). Action: extract the true M=64 MUS (e126 extractor, launched) and
re-fit the schema on three points before any hand-proof attempt. The
stable families S1/S2/S3 and the seam-coupling observation stand (they
are present in both existing MUSes); the scaling laws are what's wrong.

## THREE-POINT RE-FIT (M=32/48/64 finals) — the schema is ABSOLUTE-anchored
The scaling families are not fractions of M; they are absolute offsets, and
the offset constant is 15/16 — the crown numbers — again:
- **B1 support = (3M−15, 4M]** exactly at all three scales (bot_off starts
  M−15: 17 at 32, 33 at 48, 49 at 64). The last M+15 values of B1.
- **B2 support = [4M+1, ~6M−c] ∪ (6M, 6M+15]**: the full bottom-to-flood
  band plus a width-15 band above the centre — and (6M, 6M+15] is the
  doubling image 2·(4M) − (2M−15): the seam-2 reflection of B1's top
  against B0's top-15 region. The S3 = 2×S2 coupling in refined form.
- B0: top-8..10 run + scattered witness-midpoints (derivable; small).
My earlier fraction-based CORE(64) missed B1's top quarter (209..256 minus
the top-8) — exactly why it went SAT. Corrected sufficiency check: e134.

## SUFFICIENCY CONFIRMED (e134): CORE'(64) UNSAT in 67s (|support| = 287).
The absolute-anchored schema is machine-sufficient at M=64; the M=32/48 MUS
supports are subsets of the same bands (B1 = (3M−15, 4M] exactly). Lock runs
at M = 32, 48, 80, 96 in flight (e135). GAP-N6a status: schema LOCKED
(machine); remaining = the Z/D/E/P hand proof over the anchored bands —
ladders on B1's (3M−15, 4M] band, transfer across seam 2 via the doubling
image, flood at 6M with the width-15 boundary rung.
