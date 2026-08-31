# 84 — FRONT GAP-RES: ODD-KILL for the clustered/low-pair regime,
# the spiral schema family, and the low-zone lattice law

Companion to notes/77 §7 (GAP-RES = the consolidated N6a crux),
notes/66 §5 (the ODD-KILL reduction: three halving levels → one
cross-parity statement), notes/59 §A (the fan-walk calculus: Lemma CC,
Lemma FW, Theorem AFF — all [PROVED] there and imported here).
Instrument: experiments/e187_oddkill.py → data/e187_oddkill_*.json,
data/e187_oddkill.log.  Status tags [PROVED] / [MACHINE-CHECKED] /
[GAP] / [RESISTS] as always.

## 0. The target and the verdict up front

GAP-RES (notes/77 §7): classify, uniformly in the window length, the
SAT-alive attacker pairs of the double-fan theory
F(N, A) — window O = [1, N], attackers at offsets 0 ≤ q < p ≤ A,
fan units (2a+r) ≺ a (r ∈ {p, q}, a ≥ 1, 2a+r ≤ N).  ODD-KILL
(notes/66 §5) is its cross-parity core: EVERY pair with odd gap
g = p − q should be dead; three levels of halving (Lemma PURE /
HALVE-PURE) then pin the alive-gap lattice ≡ 0 mod 8 (H-LAT).

**Verdict of this front:**

1. For odd g the entire descent calculus is PARITY-FORCED — every
   rule application has exactly one admissible residue — and the
   rule-(i) iteration at a head becomes a deterministic SPIRAL whose
   deviation dynamics is base-(−2) digit extraction in units of g
   (Lemma LAND, §1.2 [PROVED]).  Landing is governed by one
   divisibility, g | δ₀, which a free translation parameter absorbs.
   This is the exact mechanism behind the "affine-cycle certificates,
   med ≈ 14 facts" of notes/55 §5.3b: the med-14 DAGs are spiral
   2-cycles.
2. **Theorem S1 + Corollary COR [PROVED, §1.3-1.4]: every odd-gap
   pair with 7q + 10g ≤ 2N is dead**, by a single explicit 2-cycle
   schema (one seed unit, one RL lift, one spiral).  This covers the
   clustered bulk (in particular every clustered pair with
   17 max(q, g) ≤ 2N) and is EXACT within its species: the spiral
   lands iff g | δ₀ (mod-g exactness, §1.2(c)).
3. **The region law [MACHINE-CHECKED, 8 full scales + 16 tower
   windows + 2 fresh windows]: every odd-gap pair in
   R(N) = {3q + g ≤ N − 24, 2p ≤ N − 7} is closure-dead with a
   VERIFIED certificate** from the proved cycle species (S ∪ FG-high
   ∪ FW 2-cycles ∪ FW k-cycles; soundness = Lemma FW, imported).
   Zero soundness violations: no closure-alive pair ever acquires a
   certificate (8 scales, ~10⁴ alive-pair trials).
4. The residue beyond R is exactly the known scaled-zone species
   (§3): the deep corner q ≳ (N−24)/3 (the notes/77 §1.4 RESISTS
   zone), the E1 attacker columns 2p > N − 7, and the high wing
   g > q beyond FG-high's window.  The odd STALL corner (closure-
   alive, SAT-dead) stays q ≥ M − 8 at all eight audited scales.
5. Consequence (§4): the alive-gap lattice law 8 | g holds
   [PROVED modulo the machine region law] on the low zone
   3q + g ≤ N − 100, 2p ≤ N − 32 — the ODD-KILL reduction of
   notes/66 executed on the region where the halving tower stays
   inside R at all levels.

## 1. The spiral schema

### 1.1 Parity-forcing  [PROVED]

Fix an odd gap g = p − q.  For any value v, exactly one r ∈ {q, p}
has r ≡ v (mod 2).  Consequently, in the descent rules of the
fan-walk calculus (notes/59 §A.2 — seed, (i), (ii), (iii)), the
residue of every application is uniquely determined by the parity of
its input.  In particular every value v ≥ p + 2 (and every v ≥ q + 2
of q's parity) carries exactly one unit v ≺ (v − r(v))/2: the DROP
MAP is total above p + 1.  This totality is precisely what even gaps
lack (their drop map lives on one parity class — the origin of the
halving recursion), and is why odd gaps admit a uniform kill.

### 1.2 Lemma LAND (the landing dynamics)  [PROVED]

**Setting.**  Head h ∈ O with a seed (h ≥ r₀ + 2, r₀ ≡ h mod 2).
The (forced) SPIRAL at h is x₀ = (h − r₀)/2 and

    x_{n+1} = h − (x_n + r_{n+1})/2,   r_{n+1} ≡ x_n (mod 2) unique,

each step being: RL on the fact h ≺ x_n (valid while
1 ≤ 2h − x_n ≤ N), then the unit (2h − x_n) = 2x_{n+1} + r_{n+1} ≺
x_{n+1} (valid while x_{n+1} ≥ 1, ≠ h), then T.  So h ≺ x_n is a
derived fact for every n reached (Lemma FW(a)).

**Fixed points.**  τ is a fixed point of the r*-step iff
3τ = 2h − r*; it is genuinely fixed under forcing iff furthermore
τ ≡ r* (mod 2).

**Lemma LAND.**  Let τ ≥ 1 satisfy 3τ = 2h − r*, τ ≡ r* (mod 2),
and write δ_n := x_n − τ.  Then:

(a) δ_{n+1} = −δ_n/2 when δ_n is even, and
    δ_{n+1} = −(δ_n + σg)/2 when δ_n is odd, where σ = +1 if
    r* = q and σ = −1 if r* = p.  Uniformly:
    δ_{n+1} = −(δ_n + ε_n σ g)/2, ε_n = δ_n mod 2.

(b) If g | δ₀, the spiral reaches x_K = τ for some
    K ≤ |δ₀/g| + 2 (indeed K = O(log(|δ₀|/g))), PROVIDED the window
    and positivity conditions of each step hold; and
    |δ_n| ≤ max(|δ₀|, g) for every n ≤ K.  Moreover if δ₀ < 0 then
    min_n x_n = x₀.

(c) (Exactness)  Modulo g the recursion reads
    δ_{n+1} ≡ −2⁻¹ δ_n, so δ_n ≡ (−2⁻¹)ⁿ δ₀ (mod g): if g ∤ δ₀ the
    spiral NEVER lands on τ.

*Proof.*  (a) If δ_n is even, x_n ≡ τ ≡ r* (mod 2) forces
r_{n+1} = r*; substituting h = (3τ + r*)/2 gives
x_{n+1} = τ − δ_n/2.  If δ_n is odd, r_{n+1} is the other residue
r* + σg (σ as displayed), and x_{n+1} = τ − (δ_n + σg)/2, integral
because δ_n and g are both odd.

(b) Write δ_n = σ g m_n (m₀ := δ₀/(σg) ∈ ℤ by hypothesis).  By (a),
m_{n+1} = −(m_n + ε_n)/2 with ε_n = m_n mod 2 (g odd).  This is
base-(−2) digit extraction, and it terminates at 0 from EVERY
integer: m = 0 is fixed; ±1 reach 0 in ≤ 2 steps (1 → −1 → 0,
−1 → 0); and |m| ≥ 2 gives |m_{n+1}| ≤ (|m| + 1)/2 < |m|.  For the
sup bound, |δ_{n+1}| ≤ (|δ_n| + g)/2, so |δ_n| ≤ D := max(|δ₀|, g)
by induction.  Two refinements used later, both for δ₀ < 0:
(b1) POSITIVE deviations satisfy δ_{n+1} > 0 ⟹ δ_n < 0 and
δ_{n+1} ≤ |δ_n|/2 ≤ D/2;  (b2) NEGATIVE deviations satisfy
|δ_{n+1}| ≤ (|δ_{n}| + g)/2 ≤ D, with the minimum orbit value
attained at x₀ (every later negative deviation has magnitude
≤ (D + g)/2 ≤ D = |δ₀| when |δ₀| ≥ g; and when |δ₀| < g, all
|δ_n| < g by induction — equality |δ_{n+1}| = g would force
|δ_n| = g).  So x₀ = τ + δ₀ is the orbit minimum.

(c) The correction term ε_n σ g vanishes mod g; 2 is invertible mod
the odd g.  ∎

### 1.3 Theorem S1 (the clustered spiral kill)  [PROVED]

**Theorem S1.**  Let g = p − q be odd and let t ≥ 1 satisfy, with
u := q + 2t, w := 3t + 2q, r₀ := (q if t ≡ q mod 2, else p),

    (C1)  g | (t + r₀)/2          [equivalently t ≡ −q or −p (mod 2g),
                                   both lifts parity-consistent]
    (C2)  2q + 3t − r₀ ≥ 2        [x₀(w) ≥ 1; automatic for r₀ = q]
    (C3)  9t + 6q + r₀ ≤ 2N       [the first reflection 2w − x₀ ≤ N]

Then ThFG(q, p; N) is inconsistent.

*Proof.*  u = 2t + q is the source of the seed unit u ≺ t (valid:
t ≥ 1, u ≤ N by (C3) since u < w ≤ (2N − r₀)/3 ≤ N).  RL on u ≺ t
gives u ≺ 2u − t = w (the AP (t, u, w) lies in O by (C3)).  Now run
the spiral at w with target τ = u and r* = q: indeed
3u = 6t + 3q = 2w − q and u ≡ q (mod 2).  The seed of w has residue
r₀ (w = 3t + 2q ≡ t mod 2, and r₀ ≡ t by its definition), so
δ₀ = x₀ − u = (w − r₀)/2 − u = −(t + r₀)/2 < 0.  By (C1) and Lemma
LAND(b) the spiral lands: x_K = u, giving the derived fact w ≺ u —
provided each step is admissible, which we check.  (Positivity)
the orbit minimum is x₀ = (w − r₀)/2 ≥ 1 by (C2) (LAND(b2)).
(Head-avoidance x_n ≠ w)  x_n ≤ u + D/2 by LAND(b1), and
D = max((t + r₀)/2, g) ≤ t + q — the first argument is
≤ (t + q + g)/2 ≤ t + q and the second is ≤ t + q, both because
(C1) forces (t + r₀)/2 ≥ g, i.e. t + q ≥ 2g − (r₀ − q) ≥ g —
so x_n ≤ u + (t + q)/2 < u + t + q = w.  (Window) every reflection
2w − x_n ≤ 2w − x₀ = (3w + r₀)/2 ≤ N by (C3), and every
reflection ≥ w + 1 ≥ 1.  So u ≺ w and w ≺ u, contradicting
irreflexivity through T (Lemma CC).  ∎

Remark (exactness).  By LAND(c), for the S1 shape the divisibility
(C1) is NECESSARY as well: the schema's arithmetic is sharp, not an
artifact of the search.

Remark (species).  The S1 certificate is one seed unit + one RL +
one spiral of length K = O(log): an affine-cycle derivation word of
the fan-walk calculus.  At (q, p) = (10, 11), N = 111 it is the
med-≈14-fact DAG of the e142o survey verbatim: the notes/55 §5.3b
"affine cycle families … certificates in hand" ARE the spirals.

### 1.4 Corollary COR (the clean region)  [PROVED]

**Corollary.**  Every odd-gap pair with 7q + 10g ≤ 2N is dead.

*Proof.*  Produce a valid t for Theorem S1.  The two admissible
residue classes of (C1) are t ≡ −q and t ≡ −p (mod 2g) (both
parity-consistent: −q ≡ q and −p ≡ p mod 2, as g is odd and 2g
even — t ≡ −q mod 2g forces t ≡ q mod 2, matching r₀ = q).

Case q ≥ g (the clustered side).  The two lifts differ by g mod 2g,
so the smaller valid t is ≤ g.  (C2): for r₀ = q it is automatic;
for r₀ = p it reads q + 3t ≥ g + 2, and (C1) with r₀ = p forces
t + q + g ≡ 0 (mod 2g) hence t + q ≥ g, so q + 3t ≥ g + 2t ≥ g + 2.
(C3): 9t + 6q + r₀ ≤ 9g + 6q + (q + g) = 7q + 10g ≤ 2N.

Case q < g.  Take t = g − q ≥ 1, which lies in the −p class
(t + p = 2g ≡ 0), r₀ = p.  (C2): 2q + 3(g − q) − (q + g) =
2g − 2q ≥ 2.  (C3): 9(g − q) + 6q + (q + g) = 10g − 2q ≤ 10g + 7q
≤ 2N.

Case q = g (p = 2q): t = g is in the −q class (t + q = 2g), r₀ = q,
(C3): 9g + 7q = 16g ≤ 17g = 7q + 10g ≤ 2N.  ∎

In particular, for the CLUSTERED regime g ≤ q the corollary kills
every odd-gap pair with p + … ≤ 2N/…: e.g. every pair with
17 max(q, g) ≤ 2N, and for the extreme clustered case g ≪ q every
pair with q ≤ (2N − 10g)/7 ≈ 0.286 N.

### 1.5 Machine record for §1  [MACHINE-CHECKED]

e187 `map` at M = 48, 64, 80, 96, 112, 128, 144, 160 (ground truth =
the e146 catalogues' closure-dead lists; independent engine):

* S1-certificates built and INDEPENDENTLY re-verified (check_cert:
  a Lemma-CC step-walker sharing no code with the generator) for
  305/496/743/1046/1391/1775/2233/2737 odd-dead pairs;
* the COR region is contained in the S1-satisfiable set at every
  scale (assert, 0 failures);
* SOUNDNESS: not one of the ~10⁴ closure-ALIVE odd pairs across the
  eight scales admits an S-certificate or satisfies the S1 predicate
  (0 violations — the standard strongest test of the calculus);
* the full S-family (§2) additionally covers the transient-landing
  instances; totals below.

## 2. The full family and the region law

### 2.1 The S family (two-sided spiral, transient landing)

Generalize S1: u = base + 2t (base ∈ {q, p}), x = x_m(u) the m-th
value of u's own spiral (facts u ≺ x_m), w = 2u − x_m (RL), and w's
spiral required to HIT u transiently (x_K(w) = u for some K), not
necessarily at its fixed point.  Landing analysis: by LAND(c) the
w-spiral's deviation trajectory from ITS fixed point is determined,
and hitting u is one more affine condition along the same dynamics —
each (base, t, m, K) shape is an affine word schema (Theorem AFF⁺,
notes/77 §1.3).  The search is deterministic and cheap; every found
certificate is replayed by the independent checker.

### 2.2 FW cycles (the full walk species)

Where S does not reach, the general fan-walk graph does: 2-cycles
x ∈ D(u), w = 2u − x, u ∈ D(w) over the FULL forced descent sets
(rules seed/(i)/(ii)/(iii), all parity-forced), and, in two cases at
M = 160 and a handful on towers, shortest k-cycles (k = 3, 4).
Soundness is Lemma FW(c) [PROVED, notes/59]; every emitted
derivation path and RL lift is validated step-by-step by the
independent checker (check_fw2 / check_fwk / _walk_path).

### 2.3 The REGION LAW  [MACHINE-CHECKED, 8 + 16 + 2 windows]

    R(N) := { (q, p) : g odd, 3q + g ≤ N − 24, 2p ≤ N − 7 }.

**Law: every pair in R(N) is closure-dead, with a verified
certificate from S ∪ FG-high ∪ FW2 ∪ FWK.**  Checked exhaustively:

* full scales M = 48..160 (N = 111..335): all in-R odd pairs
  certified (R-pair counts 570/882/1373/1970/2674/3485/4402/5426);
  FW2 needed for 68..138 pairs/scale, FWK for 2 (M = 160);
  additionally NO closure-alive pair lies in R (0/8 scales);
* tower windows W2e/W2o(m), m = 24, 32, 40, 48, 56, 64 (on-grid)
  and m = 104, 120 (FRESH half-scale windows, never before scanned):
  all 16 windows clean, R-pairs 83..2878 all certified;
* FRESH full-scale windows M = 208, 240 (N = 431, 495 — scales
  never measured by any prior instrument): every in-R odd pair
  certified; e142 closure spot-checks agree (see data).

Coverage beyond R: the union S ∪ FG-high ∪ FW2/FWK certifies
80.0/81.0/82.8/83.1/83.4/83.8/84.3/84.4 % of ALL odd-dead pairs at
M = 48..160.  The uncovered remainder decomposes exactly into the
known scaled-zone species (§3).

### 2.4 What is proved vs machine here — the honest split

* Species soundness: [PROVED] (Lemmas CC, FW, GL — notes/59/77;
  every certificate this front emits is independently replayed).
* S1 + COR sub-region: [PROVED] (§1.3-1.4) — a hand theorem with
  no machine residue.
* R(N) coverage: [MACHINE-CHECKED at 26 windows] — the uniform-in-N
  claim is NOT proved; its species is the per-cell affine
  verification of the S/FW words (Theorem AFF⁺ gives uniformity of
  each shape; what varies with (q, g, N) is WHICH shape fires, i.e.
  a cell decomposition that this front did not finish classifying).
  This is the same epistemic grade as (RES-LAW)/(CLOSE-LAW′)
  (notes/77 §2), now with the far stronger property that every
  instance carries a verifiable certificate, constructed and checked
  at two fresh windows on first contact.  [GAP: the cell table for
  R ∖ COR.]

## 3. The residue map (what remains of ODD-KILL)

The uncovered odd-dead pairs at every audited scale lie in:

1. **The deep corner** q > (N − 24 − g)/3: FW stalls here (the
   e179/notes-77 §1.4 scaled zone, RESISTS — needs RT-glue on
   T-composed facts / per-scale certificates).  For odd gaps the
   closure kill empirically extends to q ≈ M − 9; the segment
   between the region law and the stall corner is closure-dead with
   certificates OUTSIDE the walk fragment.
2. **The E1 attacker columns** 2p > N − 7 (deep attacker in/below
   the band bottom): certificates exist (closure) but not in the
   walk fragment; same species as 1.
3. **The high wing** g > q with 5g − q > N (beyond FG-high's
   window): the resonance-line zone of notes/59 §A.5.
4. **The odd STALL corner** [MACHINE, e180, 8 scales]: closure-alive
   odd-gap pairs occupy exactly q ≥ M − 8 (min-q series M+2 / M /
   M−2 / −1 / −4 / −6 / −6 / −8 at 48..160), all SAT-UNSAT.  For
   the α application: the shallow zone touches this corner only in
   its bottom 8 q-values.

ODD-KILL as a UNIVERSAL statement therefore remains open exactly on
the scaled zone + stall corner — the pre-existing GAP-RES residue;
what this front changed is that the low zone now has a PROVED
sub-region (COR), a machine-certified region law with per-instance
verifiable certificates (R), and an exact mechanism (LAND) replacing
the "certificates in hand" folklore.

## 4. The low-zone lattice law (the ODD-KILL reduction, executed)

**Theorem LAT-LOW.**  [PROVED modulo the §2.3 region law at the
halved shapes]  Let (q, p) be any pair of a window of length N with

    3q + g ≤ N − 100   and   2p ≤ N − 32,   g = p − q.

If the pair is closure/SAT-alive, then g ≡ 0 (mod 8).

*Proof (the notes/66 §5 reduction, run inside R).*  Suppose
2^j ∥ g, j ≤ 2.  Halve j times through Lemma PURE (notes/77 §3.1;
per notes/66 §5 the proof uses only the F(N, A) shape, so it
applies at every level).  Each level maps the class-ε pure
subsystem isomorphically onto the fan system of window
N_{ℓ+1} ∈ {⌊N_ℓ/2⌋, (N_ℓ+1)/2} ≥ (N_ℓ − 1)/2 with q̂ = (q−ε)/2,
p̂ = (p−ε)/2, ĝ = g_ℓ/2.  Track the integer budgets
B_ℓ := N_ℓ − (3q_ℓ + g_ℓ) and C_ℓ := N_ℓ − 2p_ℓ.  Since
3q̂ + ĝ ≤ (3q_ℓ + g_ℓ)/2 and 2p̂ = p_ℓ − ε ≤ p_ℓ,

    B_{ℓ+1} ≥ (N_ℓ − 1)/2 − (3q_ℓ + g_ℓ)/2 = (B_ℓ − 1)/2,
    C_{ℓ+1} ≥ (N_ℓ − 1)/2 − p_ℓ = (C_ℓ − 1)/2,

and by integrality B_{ℓ+1} ≥ ⌈(B_ℓ − 1)/2⌉, likewise for C.  From
B₀ ≥ 100, C₀ ≥ 32: B₁ ≥ 50, B₂ ≥ 25 ≥ 24 and C₁ ≥ 16, C₂ ≥ 8 ≥ 7.
So after j ≤ 2 halvings the (now odd-gap) image lies in R(N_j); by
the region law it is dead; by Lemma PURE(ii) inconsistency of the
class-ε subsystem refutes the full theory — the original pair is
dead.  Alive ⟹ 8 | g.  ∎  [The level shapes are exactly the e187
`tower` windows; the region law is audited there.]

This is the front's "alive-gap lattice law" on the low zone: the
H-LAT/DICH-ALPHA/(RES-LAW) input is now theorem-shaped there, with
machine support at 26 windows and the single remaining uniformity
gap being §2.4's cell table (plus, beyond the low zone, the §3
residue).

## 5. Session ledger

| claim | status |
|-------|--------|
| parity-forcing / drop-map totality (odd g) | [PROVED] §1.1 |
| Lemma LAND (base-(−2) landing + exactness) | [PROVED] §1.2 |
| Theorem S1 (spiral 2-cycle schema) | [PROVED] §1.3 |
| Corollary COR: 7q + 10g ≤ 2N ⟹ dead | [PROVED] §1.4 |
| region law R(N) (3q + g ≤ N−24, 2p ≤ N−7) | [MACHINE-CHECKED ×26 windows, all certificates independently verified; 0 soundness violations] |
| ODD-KILL beyond R | [RESISTS] — scaled zone / E1 columns / high wing / stall corner (§3), unchanged species |
| Theorem LAT-LOW (8 | g on the low zone) | [PROVED modulo region law] §4 |
| α_max ≤ 3 uniformly / (OV-∀) | NOT concluded — still gated by the §3 residue at shallow depths ∈ (N/3, N/2); see §6 |

## 6. What the front still owes (exact statements)

1. The cell table for R ∖ COR (finite classification of which
   S/FW word fires per congruence cell of (q, g) — would upgrade the
   region law to [PROVED] and with it LAT-LOW to a full theorem).
2. The scaled-zone odd kills q ∈ ((N−24)/3, M−9] and the E1
   columns: species = notes/77 §1.4 RESISTS (glue calculus).
3. The odd stall corner q ≥ M−8 (SAT-dead only): finite-width in
   bottom-offset coordinates at every audited scale; candidate for a
   PARM-style fixed-shape analysis.
4. The base-window clique catalogue + α̂ at the fresh scales
   (M = 208/240 catalogues building on sprint-C/main at close) —
   §7 below when they land.

## 7. The clique transport and the conditional α assembly
## (front items (2)-(3))

### 7.1 Lemma CLIQUE-HALVE  [PROVED]

Let V = {o₁ < … < o_k} be attacker offsets of F(N, A) with all
pairwise gaps ≡ 0 (mod 2^j), j ≤ 3, and suppose every pair
(o_i, o_{i'}) is alive (its double-fan theory consistent).  Then all
o_i share one parity ε, and the halved set
V̂ = {(o_i − ε)/2} is an alive set of pairwise gaps ≡ 0 (mod
2^{j−1}) in the halved fan system of Lemma PURE.  Iterating j
times: **every mod-8 alive k-clique of F(N, A) transports to an
alive k-clique of the level-j window (length ≈ N/2^j)**; and if V
lies in the shallow zone, so does its image at every level
(notes/66 §1, HALVE-PURE consequence).

*Proof.*  Gaps even ⟹ common parity.  For each pair, Lemma
PURE(ii) gives: halved pair fan-dead ⟺ original pair pure-dead ⟹
original dead.  Contrapositive: original alive ⟹ halved alive.
Gaps halve.  Shallow maps to shallow by the HALVE-PURE window
bookkeeping.  ∎

### 7.2 The base-window reduction (the notes/66 §5 program, made
### exact)

Combining LAT-LOW (§4) with CLIQUE-HALVE: **every alive clique
inside the low zone (each member pair satisfying the LAT-LOW
inequalities) has all gaps ≡ 0 (mod 8) and transports, three levels
down, to an alive clique — shallow to shallow — of the base window
of length ≈ N/8.**  Hence

    α_low(M) := max alive-clique among shallow band values with all
                pairs in the LAT-LOW zone
    ≤ max shallow alive-clique of the base window.

The measured base-window catalogue (e155b/e169, 22 + fresh windows;
notes/66 §4b): full-window cliques ≤ 4, SHALLOW cliques ≤ 3, every
4-clique of span exactly m (ANCHOR-4/SPAN-4 — its deepest member
always falls one lattice step below the shallow boundary), 5-cliques
impossible outright (SPAN-4 arithmetic).

### 7.3 α_max ≤ 3: the exact conditional statement

**Claim (α-UNIFORM, the front's item (3)).**  α_max(M) ≤ 3 for all
M ≡ 0 (mod 16).  STATUS: NOT a theorem yet.  It follows from:

    (α-1) the §2.3 region law uniformly in N        [MACHINE ×26 — the
          §6.1 cell table would prove it];
    (α-2) the mid-deep sector: no alive pair with a member at depth
          ∈ ((N−24)/3, (N−7)/2] escapes the mod-8 lattice — this is
          the §3 residue (scaled zone + stall corner)   [MACHINE:
          (RES-LAW) 0 violations / 631+ escapes, 8 scales; stall
          corner all SAT-dead, 8 scales];
    (α-3) SPAN-4 at the base windows (shallow cliques ≤ 3)
          [MACHINE at all 22+2 scanned windows; the sharp uniform
          form of GAP-DICH-ALPHA, notes/66 §4b].

Given (α-1)-(α-3): a shallow alive 4-clique would either live in
the low zone — transported by §7.2 to a shallow base 4-clique,
contradicting (α-3) — or touch the mid-deep sector, where (α-2)
pins its gaps mod 8 and the same transport applies (the clique's
DEEPEST member may then sit outside the low zone; this is where
(α-2) is genuinely consumed, not just the lattice law but deadness
of the odd/2-adic sectors there).  So α ≤ 3.  The consumer is the
K* mechanistic law (K* = m + 9 + max(α−f), exact at ten scales,
notes/66) which feeds the ROBUST chain — NOT the plain overlap
(OV-∀), which notes/66 showed is false at 224/256; the claudeMd
phrasing "⟹ (OV-∀), retiring GAP-ASM′" is superseded by the
notes/66 robust-first restatement: what α ≤ 3 buys is that the
robust chain's α-arm is law-pinned at every scale.

### 7.4 Fresh-scale data (T1/T2 tracks; filled as pod runs land)

    T2 (e169 --scan, sprint-D): m = 104, 120 — the half-scale alive
    graphs of the fresh full scales 208/240.  [PENDING at first
    commit of this section]
    T1 (e168 catalogue + e153 scan): M = 208, 240.  [PENDING]

Pre-registration (BEFORE any of these runs printed): H-LAT (alive
gaps ≡ 0 mod 8) at both fresh m; shallow cliques ≤ 3 at both;
full-window cliques ≤ 4 with any 4-clique of span exactly m and
deepest member below the shallow boundary; α̂ values in {2, 3}; if
the catalogue track lands, α_catalogue = α̂ at both scales.
