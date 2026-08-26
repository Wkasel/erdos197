# notes/49 — FRONT N2-OFF: off-diagonal core lanes (e124/e124b/e124c)

Session 2026-08-26 (post-front-merge).  Goal: per-residue hand schemas
for the (pair, residue) cells the diagonal C3(p) family misses —
closing Case 1 of the dichotomy outright.  Named targets from the
merge: the {11,12} size-4 lane (0 mod 8 — the dyadic class T-PIN
needs; {11,12} is the ONE pair with no size-3 core there), and one
≡ 2 mod 4 flip class.

Conventions as everywhere: block (M, 2M], b_j = M + j, t_i = 2M − i,
attack unit (i, j) = the precedence t_i ≺ b_j demanded by attacker
a = i + 2j (a ∈ {x, x+1} for pair {x, x+1}); "core" = minimal set of
units whose conjunction with in-block AP-freeness is UNSAT.

## 1. Catalogue reconstruction (e124_prep_catalogue)

The final e122_n2_residue.json died with its session at M = 135; the
partial checkpoint data/e122_n2_residue_partial.json holds the COMPLETE
per-M rows for M = 16..128 (113 consecutive scales, every residue).
Reconstructed catalogue → data/e122_n2_residue_recon.json (same schema
the miner expects).  Full-rung UNSAT at 113/113 scales for all six
pairs (re-confirms e122).  Distinct minimal cores per pair:
110 / 155 / 173 / 277 / 401 / 533 for x = 11..21.

Caveat carried through everything below: laws fitted on MINIMAL-core
appearance lists undercount the true firing sets (a core also fires
where a different core preempts minimality).  e124b re-probes the
interesting lanes DIRECTLY (solver, exact firing set at every M).

## 2. The miner (e124_family_miner, fixed and run)

Two fixes to the committed-but-unrun miner: (a) the constant-delta
requirement is now enforced during chain extension (was dead code —
subset chains and mixed deltas survived); (b) cores of different sizes
can no longer match (zip silently truncated).  Result:
data/e124_families.json — 3135 maximal affine families of length ≥ 3
(most are noise: "family" only requires a bijection with constant even
(di, dj) per unit and di + 2dj = lane step; the signal is in the
families whose member LAWS also slide).  Dyadic (0 mod 8, ≥ 5 scales)
sub-catalogue counts: x = 11: 23, 13: 3, 15: 7, 17: 9, 19: 13, 21: 22
— every pair has dyadic cores (the miner's second question: YES).

### The headline family (pure translation, laws slide mod 8)

    C(x) = { t_{x−11} ≺ b_6,  t_{x−9} ≺ b_5,  t_{x−6} ≺ b_3 }

(delta (2,0) per lane step of 2; attackers x+1, x+1, x).  Miner laws:
x = 11: M ≡ 5 (mod 8), x = 13: ≡ 7, x = 15: ≡ 1, x = 17: ≡ 3 — i.e.

    C(x) kills its pair on the ODD class  M ≡ x + 2 (mod 8)

(x = 19, 21 flagged irregular on minimal-appearance lists — direct
probe below).  An odd-M lane is beyond every schema we have (m₀ = 3M/2
is not an integer; the notes/33 machinery needs even M), so this is
recorded as a statement + machine law, not a hand target today.

### The ≡ 2 mod 4 flip candidates at x = 11

    B2(11) = {t2≺b5, t5≺b3, t7≺b2}   law M ≡ 2 (mod 8)
    B6(11) = {t3≺b4, t5≺b3, t10≺b1}  law M ≡ 6 (mod 8)

Together they cover the whole ≡ 2 mod 4 class for {11,12}.  Their
(2,0)-translates exist in the catalogue at higher x (with laws that
slide); direct probes in e124b.

### The {11,12} size-4 dyadic lane (0 mod 8)

Four size-4 cores fire at every M ≡ 0 mod 8 in 24..128 (14/14 scales):

    A4a = {t0≺b6, t1≺b5, t2≺b5, t3≺b4}
    A4b = {t0≺b6, t2≺b5, t3≺b4, t7≺b2}
    A4c = {t0≺b6, t2≺b5, t7≺b2, t9≺b1}
    A4d = {t1≺b5, t2≺b5, t3≺b4, t6≺b3}

({11,12} has NO size-3 core on 0 mod 8 at M ≥ 24 — e121's deletion-MUS
size-4 finding, now with the residue law.)  This is the hand-verify
target: same residue class as thm:c3core, so the whole notes/33
toolkit (odd/even ladders, centers m₀ ± 1, G4 floods) applies —
only the core anatomy is new (expected 2+2: two units force an
L1-type order, two close the flip).

## 3. Direct lane probes (e124b_lane_probe) — RUNNING

Sweep M = 16..160, all lanes at all x, exact firing sets.
[results to be filled in]

## 4. Hand schema for the {11,12} dyadic lane (e124c) — [in progress]
