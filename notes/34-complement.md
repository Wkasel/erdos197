# notes/34 — The complement of Geneson's 2/3 witness (TASK H1)

Companion to the g1/g2 records (`data/g1_geneson_4096.json`,
`data/g2_geneson_c.json`) and to `experiments/h1_complement.py`
(records: `data/h1_complement.json`, `data/h1_run.log`,
`data/h1_g2_geneson_c_4096.json`, `data/h1_g2_c_lam3_262144.json`).

**Question (THE complement question).** Geneson (arXiv:2608.12604)
constructs a permutable W of upper density 2/3.  A YES-partition of
Erdős #197 using W must permute the exact complement C = N \ W.  Is any
Geneson-complement plausibly permutable — or does every set of density
2/3 "built this way" have a provably dead complement?

**Overall status.**  Two theorems and one open door:

1. **The paper-exact complement is DEAD** (unconditional, lem:orbit +
   an explicit orbit; §1).
2. **There is NO universal orbit theorem for the family**: the orbit
   obstruction applies to C(λ, r) iff r and 2λ are powers of two
   (§3).  λ = 3 keeps W's upper density at 2/3 and makes C orbit-free.
3. Orbit-free complements remain S_A-patterned (CROWN + SLIVER flags,
   upper density ≥ 5/6) but are not killed by current machinery (§5).

---

## 1. Theorem: the complement of Geneson's witness is not permutable

**Theorem H1.**  Let W be Geneson's witness with the paper parameters
(M₀ = 1, L_k = 4·M_{k−1}, octaves [L_k·4^j + M_{k−1}, 2·L_k·4^j] for
j = 0..k, M_k = 2·L_k·4^k), and C = N \ W.  Then C is not permutable:
it contains the infinite doubling orbit

    u_s = 2^s + 3   (s ≥ 5),      u_{s+1} = 2·u_s − 3,    3 ∈ C,

with the single reflector F = {3} ⊆ C, contradicting the orbit
obstruction (paper `lem:orbit`).

**Proof.**  u_{s+1} = 2u_s − 3 is immediate.  3 ∈ C since C ⊇ [1, 3]
(everything below L₁ = 4).  It remains to check 2^s + 3 ∈ C for all
s ≥ 5.  With the paper parameters every structural boundary is a power
of two, and each power 2^s (s ≥ 5) is exactly one of:

* **an octave bottom** L_k·4^j (k ≥ 2): then 2^s + 3 lies in the
  removed bottom sliver [L_k·4^j, L_k·4^j + M_{k−1} − 1] ⊆ C, because
  its width M_{k−1} ≥ M₁ = 32 > 3;
* **an octave top** 2·L_k·4^j with j < k: then 2^s + 3 lies in the
  silent zone (2·L_k·4^j, L_k·4^{j+1}) ⊆ C;
* **the stage top** M_k or **the chasm midpoint** 2·M_k: then
  2^s + 3 lies in the inter-stage chasm (M_k, 4·M_k) ⊆ C
  (its length 3·M_k ≥ 96 > 3; the chasm's only interior power of two
  is 2·M_k).

Only s ∈ {2, 4} fail (octave bottoms of stage 1, sliver width
M₀ = 1 < 4), which is why the orbit starts at s = 5.  ∎

Mechanical verification: `explicit_orbit_kill` in
`experiments/h1_complement.py` checks u_s ∈ C for **all 5 ≤ s ≤ 200**
by exact big-integer interval arithmetic (horizon 2^201), together
with the boundary classification above (`data/h1_complement.json`,
field `kill`).  The g2 orbit scan independently flags the pattern at
finite horizons (`data/g2_geneson_c.json`, N = 2^18: FLAGGED
[ORBIT, CROWN, SLIVER]; fresh 4096-record with CDCL cross-check in
`data/h1_g2_geneson_c_4096.json`).

**Interpretation.**  This is the same mechanism as the dyadic-partition
disproof, seen from the other side: removing the bottom slivers is
exactly what makes W permutable (they absorb the 15/16-style attacks),
and *receiving* every sliver at every scale — 2-adically aligned — is
exactly what kills C.  So the paper-exact Geneson witness admits **no**
YES-partition partner: the partition (W, N\W) fails, unconditionally.

Note (b) of the task brief is thereby moot, but for the record:
pure-complete SAT on C is SAT at H = 256/1024/4096 (Cadical,
`data/h1_g2_geneson_c_4096.json`) — as it must be: pure-complete
windows are *always* SAT (ABJ soundness ceiling, see g2 header), so
finite SAT never contradicts asymptotic death.

## 2. What exactly an infinite orbit needs (quantification)

Write an orbit u_{m+1} = 2·u_m − f_m, f_m ∈ F, |F| < ∞.  Then
c_m = Σ_{i<m} f_i·2^{−i−1} converges, and

    u_m = 2^m·A + t_m,   A = u₀ − lim c_m,   t_m = Σ_{i≥m} f_i·2^{m−1−i},

with t_m ∈ [min F, max F] **bounded**.  So:

> **Criterion.**  A team S admits an infinite doubling orbit with
> reflectors from a finite F ⊆ S iff some geometric ray A·2^m stays
> within bounded distance of S for all large m (and S contains the
> bounded defect values f_m = 2u_m − u_{m+1}; any team containing an
> initial segment [1, λ−1], λ ≥ 3, has reflectors to spare).

Consequences, answering the "intervals" speculation precisely:

* A single interval [a, b] ⊆ S supports doubling chains of length only
  ⌊log₂((b−f)/(a−f))⌋ + 1 ≈ log₂(b/a): **absolute length is
  irrelevant; ratio is the currency.**  Verified per-run in
  `data/h1_complement.json` (`interval_chains`: every maximal run of C
  has chain length ≤ log₂(ratio) + 1; runs have ratio ≤ 5).
* Hence "C contains arbitrarily long intervals" is NOT by itself
  fatal.  λ = 3 realises this: arbitrarily long chasms, yet no
  infinite orbit (§3).  Fatality requires a **2-adically aligned
  geometric ladder** of intervals/slivers, as in §1.
* **Lemma R quantification**: a ratio-ascent quadruple
  {m, 2m, 3m, 5m} ⊆ S appears inside any run of ratio > 5.  C's runs
  all have ratio ≤ 5 (chasm ∪ fused sliver just misses at 4.999…), but
  the *composite* run chasm → sliver → silent still contains Lemma-R
  quadruples at every stage: m ∈ (1.6·M_k, 5·M_k/3) puts m, 2m in the
  chasm, 3m in the sliver, 5m in the silent zone (paper params;
  306 quadruples below 2^18, exactly the predicted windows —
  `lemma_r` field).  Lemma R is an order-constraint (no global
  "small-first-by-ratio" strategies for C), not a standalone death
  certificate; C's death in §1 comes from the orbit, not from R.

## 3. Theorem (orbit dichotomy for the Geneson family)

Family: λ ≥ 3 (L_k = λ·M_{k−1}), octave ratio r ≥ 4, octave top
t = 2 (block tops 2·L_k·r^j; 2t ≤ r), J(k) → ∞ octaves per stage.
Upper density of W is r/(2(r−1)) — equal to 2/3 **iff r = 4** — and is
independent of λ (λ only sets the lower density 2/(3(λ+1)) and the
convergence speed).

> **Theorem (dichotomy).**  C(λ, r) contains an infinite doubling
> orbit iff **r and 2λ are both powers of two**.

*Sufficiency*: all structural boundaries are then powers of two and
the ray 2^s + 3 works verbatim as in §1 (mechanically verified for
(λ, r) = (4,4), (8,4), (16,4), (4,8) up to 2^120; the ray enters C for
good at s = 5, 6, 7, 6 respectively).

*Necessity (sketch + finite certificates)*: by §2 an orbit is a ray
2^m·A + O(1).  With t = 2 the silent zone (2·L·r^j, L·r^{j+1}) has
log₂-length exactly log₂(r/2), and a ray crossing a stage must re-enter
the bottom sliver of *every* octave (the forbidden octave has
log₂-length 1 − o(1), leaving only the sliver's absolute O(M_{k−1})
of slack per dyadic window).  Riding octave j then forces the entry
offset s_{j+1} = r·s_j − O(1), so surviving all J(k) octaves pins the
ray to the anchor L_k·2^i up to bounded error; consecutive slivers are
a factor r apart, which a doubling ray meets iff log₂ r ∈ Z.  Across
stages the anchor jumps by L_{k+1}/L_k = 2λ·r^{J(k)}, adding
frac(log₂ 2λ) to the anchor's 2-adic phase at every stage — an error
*proportional to scale*, unfixable by bounded reflectors, unless
log₂(2λ) ∈ Z.

Finite certificates for necessity (exhaustive closures — every value
reachable from C ∩ [2^13, 2^14) by u → 2u − f, f ∈ C ∩ [1, 16],
computed to extinction; `law` field of `data/h1_complement.json`):

| (λ, r) | verdict | certificate |
|---|---|---|
| (4,4) paper | **orbit** | ray 2^s+3, s ≥ 5, checked to 2^200 |
| (8,4), (16,4), (4,8) | **orbit** | ray 2^s+3 checked to 2^120 |
| (3,4) | orbit-free | closure dies at 2^23 (35 712 values) |
| (5,4) | orbit-free | closure dies at 2^24 (177 476 values) |
| (6,4) | orbit-free | closure dies at 2^25 (261 243 values) |
| (12,4) | orbit-free | closure dies at 2^19 (10 218 values) |
| (3,8) | orbit-free | closure dies at 2^19 (1 729 values) |
| (4,5) | orbit-free | closure dies at 2^18 (79 813 values) |

10/10 match the predicted law; reflector cap 64 instead of 16 changes
nothing ((4,4), (3,4) re-run, `law_fmax64`).

**Death anatomy (λ = 3)**: the deepest chains die at exactly
8·M_k − O(1) (observed dead ends 7 077 880–85 = 8·M₃ − O(1)): they sit
in the silent zone (6·M_k, 12·M_k) above octave 0 of the next stage,
and their children 16·M_k − O(1) land inside octave 1
[13·M_k, 24·M_k] — the sliver at 12·M_k = 3·4·M_k is unreachable from
the 2-adic anchor (`death_anatomy_lam3`).  The same signature appears
in g2's scan of the λ=3 complement at N = 2^18: longest chain ends at
18 429 ≈ 8·M₂, **not censored** — ORBIT flag correctly False
(`data/h1_g2_c_lam3_262144.json`).

## 4. Corollary: no universal complement-death theorem via orbits

Within the upper-density-2/3 subfamily (r = 4, t = 2 forced; λ ≥ 3,
J(k) → ∞ free), the complement is orbit-dead **iff λ is a power of
two**.  Geneson happened to choose λ = 4; the hoped-for clean theorem
"the complement of any density-2/3 set built this way contains fatal
orbit structure" is **false** — λ = 3 (or 5, 6, 7, …) is a
counterexample.  W(λ=3) is still a valid permutable witness
(per-stage ABJ permutation clean and zero cross-stage 3-APs at
N = 8192, `witness_lam3`; A1's earlier spot-check at 2048 concurs).

## 5. Verdict and what survives

* **Paper-exact Geneson complement: provably not permutable**
  (Theorem H1).  The specific partition (W, N\W) is a NO.
* **Tuned complements C(λ, 4), λ not a power of two: open.**  They
  dodge lem:orbit — but they inherit every bottom sliver, all silent
  zones and chasms, carry upper density 1 − 2/(3(λ+1)) ≥ 5/6
  (minimum 5/6 at λ = 3, vs 13/15 at λ = 4), and g2 flags them
  [CROWN, SLIVER]: attackers 7–12 recur at ≥ 92 % of occupied octaves
  with crown pairs {7,8}, {31,32}, {63,64}, and bottom-sliver load 1.0
  at every W-sliver scale — the S_A death pattern minus the orbit.
  Nothing known permutes at upper density above 2/3; a permutable
  C(3, 4) would smash that record at 5/6.  Plausibility: low.
* **Next attack** on C(3,4): the portable-crown machinery (notes/37)
  at the octave bottoms C inherits from W, or a chunk-stage reduction
  (paper thm:chunk) exploiting the forced sliver→silent→sliver
  transport that §3 shows is *almost* an orbit — the misalignment that
  saves C(3,4) from lem:orbit is a factor 3/2 at every stage crossing,
  which may be expressible as a crown/order gadget instead.

All artifacts: `experiments/h1_complement.py` (self-contained except
g2 imports), `data/h1_complement.json`, `data/h1_run.log`,
`data/h1_g2_geneson_c_4096.json` (paper C at 4096, CDCL-verified SAT +
flags), `data/h1_g2_c_lam3_262144.json` + `data/h1_c_lam3_r4_262144.json`
and `data/h1_c_lam8_r4_262144.json` (tuned complements at 2^18).
