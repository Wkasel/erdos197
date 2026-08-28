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

**Out-of-sample validation (112/128).**  e153 run on the sibling
front's catalogues BEFORE seeing their thresholds
(data/e153_dich_lemmas_112_128.log): α_E = α_O = 3 and f_O = f_E = 8
at both scales (both mechanisms simultaneously active), predicting
K*(112) = 56+4 = 60 and K*(128) = 64+4 = 68 — matching the notes/58
direct measurements (K*(112) = 60, K*(128) = 68) EXACTLY.  The
formula is now exact at six scales, the last two as blind
predictions.  The drift toward balance ((M+16)/2 − K* = 6, 5, 6, 5,
4, 4 at 48..128) is explained: the resonance lattice widens (α:
2→3, with mod-32-spaced alive triples {−110,−78,−14} at 112) and
the deep supports lengthen until the bottom singleton self-serves
(f: 9→8) — both monotone-in-M trends, quantifying the GAP-ASM′
narrowing (notes/56 §4b, notes/58 §1.1).

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
        ℓ(z) ≥ m−8 ≥ 16;  n_c(z) ≥ 8, with equality ONLY at the top
        odd singleton s = 2M+15 (interval [4M−16, 4M], top-anchored).

Moreover for a defector SET D ⊆ Z_T ∩ c the forced set
F(D) := ⋃_{z∈D} I(z) ⊆ Y_{T′} satisfies

  (iv)  f_c(D) := |F(D) ∩ (class c of P1)| ≥ 8, and ≥ 9 UNLESS D is
        exactly the bottom singleton ({4M+1} / {4M+2}) or the
        top-odd singleton {6M+15}: any second defector strictly
        extends the union (distinct z give intervals with distinct
        endpoints; a low second defector extends the bottom-anchored
        interval upward by ≥ 1 value, reaching n_c ≥ 9; a
        middle/high second defector contributes an interval of
        n_c ≥ 8 with at most partial overlap — e153 verifies the
        exact count for every singleton AND every pair at all four
        scales; the singleton values are (i)–(iii)).

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

## 3. The fan-side finite facts F1–F4  [MACHINE-CHECKED at
## 48/64/80/96 — e153; uniformization ⊆ GAP-FG-schema]

All facts are properties of the block-2 catalogue 𝔇(M) alone
(plus interval arithmetic); they are the ONLY per-scale inputs of the
§4 theorem.  Verifier: experiments/e153_dich_lemmas.py →
data/e153_dich_lemmas.log.

**F0 (purity — total).**  Every same-parity attacker pair's pattern
has its entire support in the attackers' parity class: 863/863
(M=48), 1428/1428 (64), 2095/2095 (80), 2907/2907 (96).
Consequence: the service constraints of class-c patterns are
class-local — a class-c pattern monochromatic in team T is dodged
iff some support member lies in T′ ∩ P2 ∩ c.  (This is the machine
form of "the closure of a class-c fan pair lives in the class"; a
hand proof should follow from Lemma PAR-style parity bookkeeping on
the R1–R4 closure — part of GAP-FG-schema.)

**F1 (shallow alive-clique numbers).**  α_c(M) := max subset of
{class-c band values with offset ≥ −(M−1)} with no dead-pure pair:

    M      48   64   80   96   112  128
    α_E     2    3    2    2    3    3    (E-triple at 64: {−48, −32, 0})
    α_O     2    2    2    2    3    3

All witnesses are resonance configurations (gaps 16/32/48/64 —
cf. notes/55 §5.3b; per notes/58's e155 lattice law, alive gaps are
≡ 0 mod 8/16, so α's uniformization is a resonance-lattice count).

**F2 (bottom-singleton self-service law).**  The bottom singleton
D = {4M+1} (odd) resp. {4M+2} (even) is *self-serving* — every
dead-pure same-class pair inside its forced interval has the bottom
value in its support — exactly:

    M        48     64     80     96    112    128
    {4M+1}   NO     NO     NO     YES   YES    YES   (f_O = 9,9,9,8,8,8)
    {4M+2}   NO     YES    NO     YES   YES    YES   (f_E = 9,8,9,8,8,8)

Failure exemplars (the e152 cores): at 48, pair (−55,−49) has pure
support {+3,+7,+15,…} ∌ +1; at 80, pair (−95,−81) support
{+3,+17,+31,…} ∌ +1.  NO other singleton self-serves at any scale
(D2 scan) — but non-bottom singletons have n_c ≥ 9 anyway (FI), so
only the bottom ones matter for f.

**F3 (admissible-minimum windows).**  Exact SAT scan (D5) over
defector sets D of one class with prescribed minimum offset s₀,
against pure self-service alone: admissible minima are exactly
LOW ∪ a bounded window just above:

    M=48: O ≤ 41, E ≤ 42;   M=64: O ≤ 55, E ≤ 56;
    M=80: O ≤ 67, E ≤ 68;   M=96: O ≤ 79, E ≤ 80.

In particular EVERY admissible minimum is ≤ M−1, so every admissible
defector set's forced interval meets the bottom window
[3M−15, 3M−15+(m−1)] — this is what makes the two-sided collision
argument (§4, case H2) close.  (The windows are ≈ (M−31) + m/2‑ish;
their uniform law is the service-reach of the deep supports —
GAP-FG-schema material.)

**F4 (one-sided branch closure).**  The ABSTRACT branch instance —
defector class c with minimum s₀, one-sided (no opposite-class
defectors), constraints ONLY: forced-set definitions (Lemma FI),
pure self-service of class-c pairs inside F(D), "class-c dead pair
in Y_T needs a support member outside D", "class-c′ dead-pure pair
in Y_T forbidden", |Y_T| ≥ K* — is UNSAT for EVERY minimum s₀, both
classes, all four scales (D6), and at K*−1 it is SAT exactly at the
bottom minima (D6s) — the abstraction is faithful: it reproduces
the sharp threshold.  This instance is a WEAKENING of the full
DICH instance (it drops Y_{T′}-side and mixed-pair constraints), so
its UNSAT is the stronger statement.

Interpretation of F4's anatomy: for minima in the low zone the kill
is the §4 counting (f + α); for minima in the deep end of the F3
window the kill is the CASCADE — admissibility forces the defector
set to grow (a D5 witness at (48, O, s₀ = 41) has 21 defectors and
forced mass f_O = 22) until the counting closes.  At 64/80/96 the
single-interval counting (n_c = m/2, ᾱ from C3) already closes
every surviving minimum; at 48 four minima (O:41; E:38,40,42) need
the cascade (E2 line of e153).

---

## 4. The hatch theorem: DICH in the HATCH case  [PROVED given
## F0–F4]

**Theorem H-DICH(M).**  Let χ be straddle-free, (2,2,2)-bounded,
fan-clean, with hatched U (U_A = O, U_B = E up to swap) and
Φ(χ) ≥ 1.  Then min(|Y_A|, |Y_B|) ≤ K*(M) − 1, where
K*(M) = m + 9 + max(α_E − f_O, α_O − f_E) with the F1/F2 constants.

*Proof.*  By Lemma T, D_A = Z_A ∩ odd or D_B = Z_B ∩ even is
nonempty.  Write s₀(D) for the minimum offset of a nonempty
defector set.

Case H0 (an inadmissible defector set).  If D_A ≠ ∅ violates pure
self-service — some dead-pure odd pair inside F(D_A) ⊆ Y_B (Lemma
FI) has a pattern with support ∩ D_A = ∅ — then that pattern is
monochromatic in B (attackers forced into Y_B; support all-odd by
F0, inside Z_B = odds ∖ D_A), contradicting fan-cleanness.  By F3
this disposes of every D_A with s₀ above the admissible window, in
particular every s₀ > M−1; mirror for D_B.  So from here on every
nonempty defector set is admissible with s₀ ≤ M−1.

Case H1 (two-sided: D_A ≠ ∅ and D_B ≠ ∅).  Both minima are ≤ M−1
(H0/F3).  If both are LOW (≤ M−31): Lemma COLL — 3M−15 forced both
ways, contradiction.  If say s₀(D_A) ∈ (M−31, M−1] (surviving-mid):
I(z₀) is an interval of length m with bottom 3M−15+δ_A,
δ_A = ⌈(s₀−(M−31))/2⌉ ≤ 15, hence I(z₀) ⊇ [3M−15+δ_A, 3M−15+m−1]
⊇ [3M, 3M+m−16] …; concretely: F(D_A) and F(D_B) both meet the
bottom window [3M−15, 3M+15]: a low opposite minimum's interval
covers [3M−15, 3M] and a mid minimum's interval covers
[3M−15+δ, 3M−15+δ+m−1] ⊇ [3M, 3M+δ−1+…] — since δ ≤ 15 ≤ m−1 the
two intervals intersect (their spans [3M−15, 3M] and
[3M−15+δ, …+m−1] overlap whenever δ ≤ 15).  If BOTH minima are mid:
both intervals have length m and bottoms within [3M−14, 3M],
distance |δ_A − δ_B| ≤ 14 < m: they intersect.  In every two-sided
sub-case some band value is forced into both Y_A and Y_B —
contradiction.  [PROVED: interval arithmetic + F3's s₀ ≤ M−1.]

Case H2 (one-sided; WLOG D_A ≠ ∅, D_B = ∅).  Since Z_B ∩ even = ∅:
every dead-pure even pair {x, x′} ⊆ Y_A would have its (all-even,
F0) support inside Z_A, making the pattern monochromatic in A — so
Y_A ∩ E is an alive-clique.  Sub-case by s₀ := s₀(D_A):

  H2a (LOW, s₀ ≤ M−31):  F(D_A) ⊇ I(z₀) ⊇ [3M−15, 3M] (FI(i)), so
  Y_A ∩ E lives in the shallow zone (offsets ≥ −(M−1) up to the
  even shift): |Y_A ∩ E| ≤ α_E.  And |Y_A ∩ O| ≤ (m+8) − f_O(D_A)
  with f_O(D_A) ≥ 9 unless D_A = {4M+1} exactly (FI(iv)); if
  D_A = {4M+1}, admissibility (H0) requires the F2 law, giving
  f_O = 8 exactly at the scales where {4M+1} self-serves.  Hence
  |Y_A| ≤ m + 8 − f_O + α_E ≤ K* − 1 by the definition of K*.

  H2b (surviving-mid, M−31 < s₀ ≤ M−1):  the D6 branch instance is
  UNSAT (F4): |Y_A| ≥ K* is impossible.  [For most minima this is
  the transparent counting |Y_A| ≤ (m+8 − m/2) + ᾱ(s₀) ≤ K*−1 with
  ᾱ from e153-C3; the deep-window minima at M = 48 additionally
  need the cascade — both inside F4.]

Mirror the sub-cases for D_B (constants α_O, f_E).  In every branch
min|Y| ≤ |Y_defector-side team| ≤ K* − 1.  ∎

**Sharpness.**  At K* − 1 the e149 frontier witnesses realize the
bound at every scale, with the §0.3 anatomy: bottom-cluster
defectors ({+1,+3} / {+1,+3} / {+2,+4,+6} / {+1}), forced interval
of same-class mass exactly f, minority band = the α alive-clique.
The D6s sharpness runs confirm the abstract branch is SAT at K*−1
exactly at the bottom minima.  [MACHINE-CHECKED.]

Status of §4: theorem PROVED given F0–F4 (each machine-checked at
the four scales; uniformization of F0–F4 is scoped in §6).

---

## 5. The SPLIT case  [reduction PROVED; finish MACHINE-CHECKED
## per scale — e154]

Let some parity class c of P0 be split.  Index the class-c values:
u = M + 2i − ε (i ∈ [1, m]), z = 4M + 2j − ε (j ∈ [1, n],
n = m+8 for c = O, m+7 for c = E); the midpoint of (u, z) sits at
band position determined by i + j (an integer interval [w₁, w₂] of
the sums corresponds to the band window; sums below ≈ m−15 fall
under the band, sums above 3m never exceed it for m ≥ 24).  Let
I_A ⊔ I_B = [1, m] and J_A ⊔ J_B = [1, n] be the induced index
bipartitions of P0 ∩ c and P2 ∩ c.

**Lemma SP (structure).**  (i) F_B ⊇ σ(I_A + J_A) ∩ W and
F_A ⊇ σ(I_B + J_B) ∩ W, where σ is the affine index-to-band map and
W the band window — the straddle forcing is a SUMSET on indices.
(ii) [MID] (I_A + J_A) and (I_B + J_B) are disjoint inside W.
(iii) |A + B| ≥ |A| + |B| − 1 (Cauchy–Davenport on ℤ) gives: total
visible forced mass |F_A| + |F_B| ≥ m + n − w_hidden, and when one
side hides its entire sumset below the window (the extremal
contiguous "staircase" split: I_A, J_A bottom segments with
max I_A + max J_A < w₁), the other side's forced set has
|F| ≥ |I_B| + |J_B| − 1 ≥ (m − |I_A|) + (n − |J_A|) − 1
≥ m + n − 1 − (w₁ − 2) ≥ m + 22, exceeding the allowance m + 14:
DEAD.  In general the staircase with cut a + b =: t ∈ [w₁, 2m+…]
yields two complementary near-intervals F_B ≈ σ([w₁, t]),
F_A ≈ σ([t+2, m+n−1]) with |F_A| + |F_B| ≈ m + 22, individually
≤ m+14 only for t in a middle range — the split survives straddle
counting alone, and the finish is the fan layer: the two forced
near-intervals sit at the band bottom and top respectively; the
top-interval team's class-c pairs must be served by its OWN class-c
P2 part (= the top segment J of the staircase, by F0-purity), which
reproduces the D4/D5 service-reach question; the bottom-interval
team symmetric.  [Sumset structure and the m+22 bound: PROVED; the
service finish: per-scale machine, below.]

**Machine closure (e154).**  The full DICH instance (straddles +
fan patterns + bounds + min|Y| ≥ K*) with the pin "class O is
split" (both teams meet O) — and separately "class E is split" — is
UNSAT at all four scales.  Together with Lemma T this covers the
SPLIT case entirely.  [experiments/e154_dich_split.py →
data/e154_dich_split.log.]

Status of §5: reduction and the extremal-staircase kill [PROVED];
the middle-staircase fan finish [MACHINE-CHECKED per scale;
GAP-DICH-SPLIT, low risk — same service species as F3/F4].

Machine record: e154 UNSAT at all SIX scales, both classes, ≤ 0.5 s
each — split colorings die far below threshold; the DICH frontier is
entirely inside the hatch regime, as the §0.3 witnesses already
showed.

---

## 6. DICH assembled, and sharpness

**Theorem DICH(M), structured form (M ∈ {48, 64, 80, 96, 112,
128}).**  Every straddle-free, (2,2,2)-bounded, fan-clean coloring
with Φ ≥ 1 has min|Y| ≤ K*(M) − 1, K*(M) = m + 9 +
max(α_E − f_O, α_O − f_E); equivalently min|Y| ≥ K*(M) ⟹ Φ = 0.

*Proof.*  Lemma T splits into SPLIT and HATCH.  SPLIT: §5 (Lemma SP
extremal cases proved; residual staircase machine-closed, e154).
HATCH: Theorem H-DICH (§4), proved from the §2 calculus given the
F0–F4 catalogue facts.  ∎

**Sharpness.**  e149's frontier witnesses at K*−1 (§0.3) at
48/64/80/96; notes/58's runs at 112/128 (K = 59/67 SAT); the D6s
abstract-branch SAT at bottom minima reproduces the threshold
per-branch.  So K* is exact at all six scales, and the theory
explains the witness anatomy value-by-value (e153 part F asserts
it).

**Where this leaves the notes/56 reading.**  (i) The mod-32
periodic law for K* is DEAD (already falsified at 112 by notes/58;
here replaced by the mechanistic formula, blind-validated at
112/128).  (ii) The task-prompt's "the proof lives in one parity
class at half scale" is confirmed and sharpened: every load-bearing
object (defector classes, forced intervals, pure supports, alive
cliques) is class-local; the only cross-class interaction is the
band-partition counting (both parities share the band) and the
bottom-anchor collision.  (iii) The e151 MUS anatomy is fully
explained: the 852 straddles are the FI intervals of bottom-cluster
defectors (E1 midpoints, low attackers, S3 completions); the 305
same-parity fans are the α-cap certificates plus the self-service
certificates.

---

## 7. Status, the GAP-DICH ledger after this note

### Proved uniformly in M (any M ≡ 0 mod 16, M ≥ 48)

| item | statement | where |
|------|-----------|-------|
| Lemma T | trichotomy SPLIT / HATCH(+defector) under Φ ≥ 1 | §1 |
| Lemma FI | forced interval: formulas, anchor iff s ≤ M−31, ℓ ≥ 16, n_c ≥ 8, n_c = 8 only at bottom/top singletons, f ≥ 9 for non-singleton D | §2.1 |
| Lemma ANCHOR/COLL | low defector pins 3M−15; two-sided low collision | §2.2 |
| Lemma MID/MONO | same-midpoint exclusion; split-class monotonicity | §2.3 |
| H-DICH case tree | H0/H1/H2 reduction of the hatch case to F0–F4 | §4 |
| Lemma SP (partial) | split ⟹ index-sumset staircase; extremal staircase dies (mass ≥ m+22) | §5 |

### The catalogue layer (machine-checked at 48/64/80/96 + 112/128)

F0 purity (total), F1 α-values, F2 bottom-singleton law, F3
admissible-minimum windows (all ≤ M−1), F4 one-sided branch closure
(sharp).  Verifier: e153_dich_lemmas.py (NB: distinct from the
concurrent notes/58 file e153_dich_probes.py — cite by filename).

### GAP-DICH, rescoped (replaces the notes/56 §5.2 row)

| sub-gap | statement to uniformize | species | risk |
|---------|------------------------|---------|------|
| GAP-DICH-F0 | same-parity closure supports are class-pure | parity bookkeeping on R1–R4 closure (Lemma-PAR species) | low |
| GAP-DICH-ALPHA | α_c(M) = the resonance-lattice clique number; observed 2 → 3, mod-32-spaced witnesses | resonance law (= notes/58 e155 lattice law; shared with GAP-FG-schema) | medium |
| GAP-DICH-F2 | bottom-singleton self-service iff deep gap-2/4/6 supports contain the bottom offset; observed monotone-in-M onset | deep-pair support schema (GAP-FG-deep species) | medium |
| GAP-DICH-CASC | F3 windows + F4 cascade closure (incl. the 48-deep minima) | service-reach counting; the D5/D6 instances are the exact finite forms | medium-low |
| GAP-DICH-SPLIT | middle-staircase fan finish | same service species; e154 record | low |

Honest accounting: DICH's uniformization no longer has a
"structure" gap — every sub-gap is a fan-catalogue schema question,
i.e. lands in the SAME species pool as GAP-FG-schema/-deep
(notes/59).  The threshold law itself is now a theorem-shaped
formula with six-scale exactness including two blind predictions —
the strongest evidence yet that the catalogue quantities α, f are
the RIGHT uniformization targets, and the direct bridge from this
note to GAP-ASM′: the assembly overlap question is exactly "does
K*(M) = m + 9 + max(α−f) stay ≤ cap_LLOP(M) + 1", with α, f now
computable per scale by linear scans instead of full e149 sweeps.

### Session artifacts

* experiments/e152_dich_probe.py — pinned-configuration prober
  (hatch pin, defector pin, core extraction);
  data/e152_dich_probe.log.
* experiments/e153_dich_lemmas.py — the F0–F4 verifier + K*
  formula; data/e153_dich_lemmas.log,
  data/e153_dich_lemmas_112_128.log.
* experiments/e154_dich_split.py — SPLIT branch closure at six
  scales; data/e154_dich_split.log.

