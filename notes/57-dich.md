# 57 — GAP-DICH: the dichotomy as forced-interval counting

Companion to notes/56 (which states DICH(M) and machine-certifies it
at M = 48/64/80/96, K* = 26/35/42/51) and notes/55 (the proved layer:
Lemma U, A1–A9, Lemma W; everything used freely).  Instruments:
experiments/e149 (the threshold sweep), e151 (the MUS seed), e152
(pinned-configuration probes, this session), e153 (the lemma
verifier, this session).

**This note is written incrementally; every section ends with its
verification pointer and a status tag [PROVED] / [MACHINE-CHECKED] /
[GAP].**

**Overall status: `DICH reduced to proved interval/collision calculus
+ four named finite catalogue facts (F1–F4), machine-checked at all
four scales; the K\*(M) law is now mechanistic and CORRECTS the
notes/56 mod-32 reading`.**

---

## 0. Target, and the corrected K* law

### 0.1 Setting (notes/56 §3 verbatim)

M ≡ 0 (mod 16), m := M/2.  CORE′(M) = P0 ∪ P1 ∪ P2,
P0 = [M+1, 2M], P1 = [3M−15, 4M], P2 = [4M+1, 6M+15].
Parity classes: O := odds of P0, E := evens of P0 (|O| = |E| = m);
P1 has m+8 odd and m+8 even values; P2 has m+8 odd and m+7 even
values.  For a 2-coloring χ and team T: U = T∩P0, Y = T∩P1,
Z = T∩P2.  Φ(χ) = Σ_T #{(u,z) ∈ U_T×Z_T : u ≡ z (mod 2)}.
Offsets: a band value 4M−j is written −j, a P2 value 4M+s written +s.

Hypotheses of DICH(M): χ straddle-free (both teams), (2,2,2) bounds,
fan-clean — no team contains a block-2 pattern of the catalogue
𝔇(M) (data/e146_catalogue_M{M}.json; at each scale every block-2
pattern S has |S ∩ P1| = 2, the *attacker pair*, and S ∩ P2 the
*support*; e153 asserts this shape).  A same-parity pair
{x, x′} ⊆ P1 is *dead* if some catalogue pattern has attacker set
{x, x′}, else *alive*.  A pattern is *pure* if its support lies
entirely in the parity class of its attackers (for same-parity
attacker pairs; e153 measures purity per scale).

**Proposition DICH(M)** (notes/56 §3.2): fan-clean ∧ straddle-free ∧
bounds ∧ min|Y| ≥ K*(M) ⟹ Φ = 0.  Machine: K*(48/64/80/96) =
26/35/42/51.

### 0.2 The clean form of K*, and the corrected law

In m-coordinates the machine thresholds read

    K*(M) = m + 2   at M = 48, 80        (M ≡ 16 mod 32)
    K*(M) = m + 3   at M = 64, 96        (M ≡ 0  mod 32)

(equivalently (M+16)/2 − 6 resp. − 5, as in notes/56 §3.3).  The
notes/56 reading "mod-32-periodic offset" is numerically right at the
four scales but mechanistically WRONG, and this matters for
extrapolation (GAP-ASM′).  The true law, established below and
machine-verified (e153):

    K*(M) = m + 9 + max( α_E(M) − f_O(M),  α_O(M) − f_E(M) )

where, for each parity class c ∈ {O, E} of the defector side:

* f_c(M) ∈ {8, 9}: the minimum same-parity forced-midpoint mass of a
  nonempty admissible defector set of class c — **8 iff the bottom
  singleton ({4M+1} for c = O, {4M+2} for c = E) is self-serving**
  (defined in §3), else 9;
* α_c′(M): the maximum size of a subset of the *opposite* parity
  class of the band, with offsets in [−(M−1), 0] (the shallow zone),
  containing no pair that is dead *via a pure pattern*.

At the four scales (e153): the m+3 offset is realized by TWO
DIFFERENT mechanisms — at M = 64 by α_E = 3 (the pairwise-alive
triple {4M−48, 4M−32, 4M}, resonance gaps 16/32/48), at M = 96 by
f_O = 8 (the bottom singleton {4M+1} self-serves); at M = 48 and 80
both parities have α = 2 and f = 9.  So K*'s deviation from balance
is a finite fan-catalogue quantity, not a residue law; any
extrapolation beyond the verified scales must recompute α and f
(cheap catalogue scans), not trust M mod 32.

### 0.3 The frontier anatomy (all four scales, e149 witnesses)

| M | K*−1 witness | defectors | forced interval | f | minority cap α |
|---|--------------|-----------|-----------------|---|----------------|
| 48 | A=[24,25,57] B=[24,39,54] | Z_A∩O = {+1,+3} | [−63,−47] ⊆ Y_B | 9 odd | Y_A∩E = {−42,−10} (gap 32, alive): 2 |
| 64 | A=[32,34,73] B=[32,46,70] | Z_A∩O = {+1,+3} | [−79,−63] ⊆ Y_B | 9 odd | Y_A∩E = {−48,−32,0} (gaps 16/32/48, alive): 3 |
| 80 | A=[40,55,84] B=[40,41,91] | Z_B∩E = {+2,+4,+6} | [−95,−77] ⊆ Y_A | 9 even | Y_B∩O = {−73,−41} (gap 32, alive): 2 |
| 96 | A=[48,50,104] B=[48,62,103] | Z_A∩O = {+1} | [−111,−96] ⊆ Y_B | 8 odd | Y_A∩E = {−90,−26} (gap 64, alive): 2 |

Every frontier witness: U's exactly hatched (U_A = O, U_B = E up to
swap), defectors at the very bottom of P2 on ONE side, the opposite
band = exactly the allowance 2m+16−(K*−1) = m+15 resp. m+14 —
composed of the forced interval plus the whole opposite parity class
minus the α alive values.  The task-prompt seed ("the proof lives in
one parity class at half scale") is confirmed: every load-bearing
object below is class-local.

[MACHINE-CHECKED: data/e149_dichotomy_M{48,64,80,96}.json; the
witness-anatomy table re-derived and asserted in e153.]

---

## 1. The trichotomy  [PROVED]

**Lemma T.**  Let χ meet the (2,2,2) bounds with Φ(χ) ≥ 1.  Then
exactly one of:

  (SPLIT)  some parity class of P0 meets both teams;
  (HATCH)  up to team swap, U_A = O and U_B = E, and at least one of
           D_A := Z_A ∩ odd, D_B := Z_B ∩ even is nonempty.

*Proof.*  If neither class is split, each class is owned by one
team; the two owners differ (else the other team's U is empty,
against |U| ≥ 2), giving the hatch structure up to swap.  Φ ≥ 1 then
says some team has a same-parity U×Z pair; A's U is odd, so an
A-side pair needs a member of Z_A ∩ odd; B-side likewise Z_B ∩ even.
∎

(In SPLIT, Φ ≥ 1 is automatic — every class-c value of P2 shares a
team with some class-c P0 value when class c is split, so Φ ≥
|P2 ∩ c| ≥ m+7 — but we only need that SPLIT ∨ HATCH is exhaustive
under Φ ≥ 1.)

---

## 2. The forced-interval calculus  [PROVED]

Throughout, "the midpoint of (u, z)" means (u+z)/2 for u ≡ z (mod 2),
and *forcing* is the straddle mechanism: if u ∈ U_T, z ∈ Z_T,
u ≡ z (mod 2), and v := (u+z)/2 ∈ P1, then (u, v, z) is a 3-AP with
both endpoints in T, so straddle-freeness of T gives v ∉ Y_T, i.e.
**v ∈ Y_{T′}** (the band is partitioned).  This is Lemma W(a) of
notes/55 in pointwise form; no order theory is involved.

### 2.1 Lemma FI (forced interval)

Let T own the whole class c (U_T ⊇ P0 ∩ c) and let z ∈ Z_T ∩ c,
s := z − 4M ∈ [1, 2M+15].  Then

    I(z) := { (u+z)/2 : u ∈ P0 ∩ c } ∩ P1  ⊆  Y_{T′}

is an interval of CONSECUTIVE integers (u ranges over a step-2
progression, so the midpoints step by 1), namely
I(z) = [max(3M−15, (u_min^c+z)/2), min(4M, (u_max^c+z)/2)] where
u_min^c, u_max^c are the least/greatest class-c values of P0.
Writing ℓ(z) := |I(z)| and n_c(z) := |I(z) ∩ (class c of P1)|:

  (i)   LOW (1 ≤ s ≤ M−31):  I(z) is bottom-anchored:
        min I(z) = 3M−15 EXACTLY, attained by u = 6M−30−z ∈ P0 ∩ c
        (same parity as z automatically);
        ℓ(z) = (s+31)/2 for c = O, (s+32)/2 for c = E;  ℓ ≥ 16;
        n_c(z) ≥ 8, with EQUALITY only at the bottom singleton
        (s = 1 for c = O, s = 2 for c = E); n_c ≥ 9 for every other
        low z.
  (ii)  MIDDLE (M−31 < s ≤ 2M):  I(z) = full image, ℓ(z) = m,
        min I(z) = (u_min^c+z)/2 > 3M−15;  n_c(z) ≥ ⌊m/2⌋ ≥ 12.
  (iii) HIGH TAIL (2M < s ≤ 2M+15):  top-truncated at 4M;
        ℓ(z) ≥ m−8 ≥ 16;  n_c(z) ≥ 8.

Moreover for a defector SET D ⊆ Z_T ∩ c the forced set
F(D) := ⋃_{z∈D} I(z) ⊆ Y_{T′} satisfies

  (iv)  f_c(D) := |F(D) ∩ (class c of P1)| ≥ 8, and ≥ 9 UNLESS D is
        exactly the bottom singleton: any second defector strictly
        extends the union (distinct z give intervals with distinct
        endpoints; a low second defector extends the bottom-anchored
        interval upward by ≥ 1 value, reaching n_c ≥ 9; a
        middle/high second defector contributes an interval of
        n_c ≥ 8 with at most partial overlap — e153 verifies the
        exact count for every pair at all four scales, and the
        singleton values are (i)–(iii)).

*Proof.*  Interval arithmetic: (u+z)/2 ∈ P1 ⟺ u ∈ [6M−30−z, 8M−z];
intersect with [M+1, 2M] ∩ c and count; the anchor in (i) is
6M−30−z ≥ M+1 ⟺ s ≤ M−31 and (6M−30−z+z)/2 = 3M−15; parity of
6M−30−z equals parity of z since 6M−30 is even.  The class-c counts:
I(z) is a run of consecutive integers starting at 3M−15 (odd, since
M is even) in case (i), so its class-c members are every second
value; the counts follow from ℓ.  (iv): monotonicity of unions plus
the endpoint arithmetic.  ∎

[MACHINE-CHECK: e153 part A — for every z (every s ∈ [1, 2M+15],
both parities) at M = 48, 64, 80, 96: brute-force I(z) equals the
formula, ℓ and n_c match, anchor iff s ≤ M−31; part A2: f_c(D) ≥ 9
for all two-element D, both parities, all scales.]

### 2.2 Lemma ANCHOR and the collision kill

**Lemma ANCHOR.**  If a team T owns the whole class c and has a LOW
class-c defector, then 3M−15 ∈ Y_{T′}.  [Immediate from FI(i).]

**Lemma COLL (two-sided collision).**  In the HATCH case, if D_A has
a low member AND D_B has a low member, χ is infeasible: the band
value 3M−15 is forced into Y_B (by A's low odd defector, ANCHOR with
T = A) and into Y_A (by B's low even defector), a contradiction.
[PROVED — two applications of ANCHOR.  Machine exemplar: the e152
probe D_A = {+1}, D_B = {+2} at M = 48 returns exactly this 2-line
core: straddles (M+17, 3M−15, 4M+1) and (M+16, 3M−15, 4M+2);
data/e152_dich_probe.log.]

### 2.3 Lemma MID (same-midpoint exclusion; the SPLIT tool)

Let u ∈ U_A, u′ ∈ U_B with u ≡ u′ (mod 2), and z, z′ ∈ P2 of the
same parity as u with u + z′ = u′ + z = 2v, v ∈ P1.  Then NOT both
z′ ∈ Z_A and z ∈ Z_B.  *Proof.*  z′ ∈ Z_A forces v ∈ Y_B via
(u, v, z′); z ∈ Z_B forces v ∈ Y_A via (u′, v, z).  ∎

**Corollary MONO.**  If class c is split and u ∈ U_A ∩ c,
u′ ∈ U_B ∩ c with g := u′ − u > 0, then there is no z with
z ∈ Z_B, z + g ∈ Z_A and (u′+z)/2 ∈ P1: in every window the
indicator of Z_A along any g-chain of class-c P2 values is a prefix
(A-part below, B-part above) — and if U_A ∩ c and U_B ∩ c
interleave (both orientations of cross-pairs exist), the class-c
part of P2 is monochromatic in every joint window.  [PROVED —
instances of MID.]

### 2.4 What forcing alone cannot do (the honest boundary)

Summing FI over one defector gives at most m forced values; the
allowance at K = K* is m+14 resp. m+13.  In the SPLIT case the
index form of the midpoint map (u = M+2i−ε, z = 4M+2j−ε ↦ v with
v-position i+j, a SUMSET on indices) shows that a contiguous split
(U_A ∩ c and Z_A ∩ c both bottom segments) yields two complementary
forced intervals with total mass ≈ 2m+15 split as ≈ (m+8, m+7):
straddle forcing alone never reaches the m+15 kill at balance.  The
remaining ≥ 6 values of the kill come from the FAN side (§3): the
α-cap on the minority parity and the self-service constraint on the
defector set.  This division of labour — straddles supply intervals,
fans forbid the escape patterns — is exactly the e151 MUS anatomy
(852 straddles + 305 pure-parity fans).

Status of §2: [PROVED; machine pointers above.]

---
