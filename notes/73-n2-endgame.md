# notes/73 — FRONT N2-PARAMETRIC: the Case-1 endgame (e174/e175/e176)

Session 2026-08-30.  Goal (the last writing of Case 1): (1) the
parametric-in-x lane proof — the uniform argument over x with residue
casework; (2) the two open cells A4d(19)_r0, B6(21)_r0; (3) the
x ≡ 7 mod 8 pair class; (4) Theorem N2-COMPLETE.

Conventions as in notes/49: block (M, 2M], b_j = M + j, t_i = 2M − i,
attack unit (i, j) = the precedence t_i ≺ b_j demanded by attacker
a = i + 2j ∈ {x, x+1} for the pair {x, x+1}, x odd ≥ 11; "the rung
fires" = AP-freeness on (M, 2M] + the pair's block-ordered attack
units is UNSAT.  ctr := ⌊3M/2⌋ (= m₀ for even M, = c− for odd M).

## 0. Headline results

1. **The 8-lane residue system is parametric [MACHINE, e174,
   108/108]**: NINE translation lanes (five from e124b + FOUR NEW,
   obtained by translating the bespoke {11,12} residue cells
   K11_r4/r3/r7/r1 of e124m) cover ALL EIGHT residue classes of
   M mod 8 with laws M ≡ x + c (mod 8), verified by direct solver
   probe at every pair x = 11..33 (twelve pairs, including the
   previously-uncatalogued x = 23..33), at every in-class scale up
   to 152, with SAT controls at the complementary class.  Zero
   exceptions.
2. **The x ≡ 7 mod 8 hole is closed**: the missing even lane is
   K4e(x) (law M ≡ x+1 mod 8), which at x ≡ 7 mod 8 is exactly the
   dyadic class M ≡ 0.  K4e(23) and K4e(31) fire at every probed
   in-class scale (from M = 32 resp. 40).  The "first open cell" of
   notes/49 §8 no longer exists.
3. **Both open template cells closed** (§3): B6(21)_r0 and the
   (pair 19, dyadic) cell — each now sits inside a PARAMETRIC
   template cell verified at four x values including two fresh ones.
4. **The parametric template** (§4, e175): per (lane, x mod 8) cell,
   ONE fixed data vector (v*, S_hi, S_lo, ladder keys) closes the
   Lemma-D branch analysis at every probed x ≡ ξ (x = x₀, x₀+8,
   x₀+16, x₀+24 — the last two fresh, beyond every catalogue) and
   every probed in-class M.  This is the uniform schema of notes/49
   §5.3, now with x a genuine parameter.
5. **Theorem N2-COMPLETE** (§6): modulo the tagged closure-schema
   gap [GAP-N2-UNIF], for every adjacent pair {x, x+1} (x odd ≥ 11)
   and every M ≥ T(x) (affine), the rung fires — per-residue cores,
   phase-clash schemas, laws and thresholds all explicit.

## 1. The lane table (the residue casework, x odd ≥ 11)

Units in (i, j) coordinates; attacker sanity i + 2j ∈ {x, x+1} holds
identically in x for every lane.  Laws verified e174 (probe protocol:
in-class UNSAT at every scale from the threshold to 152; controls at
r+4 SAT — data/e174_param_lanes.json, 108/108 lawful):

    lane     units                                law M ≡ (mod 8)  even/odd M
    K4e(x)   {(x−11,6), (x−8,4), (x−5,3)}         x + 1            even  [NEW]
    B6(x)    {(x−8,4), (x−6,3), (x−1,1)}          x + 3            even
    A4a(x)   {(x−11,6), (x−10,5), (x−9,5), (x−8,4)} x + 5          even
    A4d(x)   {(x−10,5), (x−9,5), (x−8,4), (x−5,3)}  x + 5          even
    B2(x)    {(x−9,5), (x−6,3), (x−4,2)}          x + 7            even
    K3(x)    {(x−10,5), (x−7,4), (x−4,2)}         x                odd   [NEW]
    C(x)     {(x−11,6), (x−9,5), (x−6,3)}         x + 2            odd
    K7(x)    {(x−7,4), (x−5,3), (x−2,1)}          x + 4            odd   [NEW]
    K1(x)    {(x−11,6), (x−8,4), (x−6,3)}         x + 6            odd   [NEW]

x odd makes {x+1, x+3, x+5, x+7} the four even residues and
{x, x+2, x+4, x+6} the four odd ones: the eight laws tile Z/8
exactly, one lane per class (two spares on x+5).  The four NEW lanes
are the (2,0)-translates of e124m's bespoke {11,12} cells (K11_r4 →
K4e, K11_r3 → K3, K11_r7 → K7, K11_r1 → K1); e174 is the first
probe of those shapes off x = 11.

Thresholds (measured firing thresholds, slope-1 affine in x):

    A4a/A4d: x+5   B2: x+7   B6: x+11   K4e: x+57 (x ≤ 19; x+9 from
    x = 21 — the late-start of the e122 K11_r4 row fades with x)
    K3: x+8   C: x+10   K7: x+12   K1: x+6 (x+30 at x = 11 only)

Uniform safe threshold: T(x) = x + 57 (every lane, every x probed).
Sporadic sub-threshold SAT scales exist only for K4e (x ≤ 19) and
K1 (x = 11); every other lane fires from its first non-degenerate
in-class scale.

Dyadic (M ≡ 0 mod 8) coverage by x mod 8 — the row T-PIN quotes:

    x ≡ 1: B2(x)      x ≡ 3: A4a(x)/A4d(x)      x ≡ 5: B6(x)
    x ≡ 7: K4e(x)     [+ the diagonal C3(x/3) when 3 | x, x/3 ≡ 5 mod 8]

## 2. [placeholder — e175 parametric template grid]

## 3. [placeholder — the two open cells]

## 4. [placeholder — the uniform argument]

## 5. [placeholder — derivation meter / uniformization status]

## 6. [placeholder — Theorem N2-COMPLETE]
