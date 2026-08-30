# 75 — FRONT PUMP-SCHEMA: the 4-block gadget's uniform law
# (the pump collapses into the CORE′ engine one window down)

Task: (1) the gadget's exact geometry as a parametric constraint
family; (2) Theorem J uniformly from the CORE′ engine one window
down — identify the S3 = 2×S2 correspondence exactly; (3) machine
checks at 8/16/24/32.  Inputs: notes/62 (the gadget, MUS,
attribution controls, Theorem J), notes/51/55 (CORE′/CI), notes/70
(telescope), notes/54 (T-FORCE).  Machine companion:
experiments/e175_pump_schema.py → data/e175_pump.jsonl,
e175_collapse.log, e175_small.log.  All parts ran with **0
failures** (2026-08-30).

**TL;DR.**  The lower window of the 4-block gadget at anchor M IS
the two-seam coupled-core window at anchor m = M/2, block for
block, and vdn = 0 is exactly the core's block-order hypothesis.
Hence (Theorem J-DOWN, a three-line restriction proof): whenever
the anchor-m coupled core fires, U4(M; v, 0) is UNSAT for EVERY
vup — machine-confirmed by the new cell (none,0)@32-bal UNSAT
[7.4 s].  Consequences: **v_min(0)(M) = ∞ for every M ≥ 32**
(bal; const via the (2,2,2) cores) — the notes/70 demand curve
[GAP-VMIN0-growth] is discharged by collapse, the queued
(512,0)@32 and (512,0)@48 pod cells are moot, and GAP-J-schema's
(·,0) family at large anchors is GAP-N6a verbatim.  What is
genuinely left of GAP-J: the margin family (w ≥ v*₃(m)) and the
freshness family F(N; v), which do NOT project.  The '8' of the C1
witness is now a proved counting identity (Lemma LEAK) with the
witness's leak set {36,40,44,48} × 2 parents each.

---

## 1. The gadget as a parametric constraint family  [PROVED]

### 1.1 Definition U4(M; b; vup, vdn)

Values V(M) = (M/2, 8M], blocks

    Bm1 = (M/2, M],  B0 = (M, 2M],  B1 = (2M, 4M],  B2 = (4M, 8M]

(sizes M/2, M, 2M, 4M).  A *state* is a 2-coloring χ : V → {A, B}
plus a linear order ≺_T per team.  Feasible iff (i) per-team
monotone-3-AP-freeness over the WHOLE range; (ii) bounds b —
`bal` = exact balance per block, or `const` = per-team lower
bounds (c₋₁, c₀, c₁, c₂); (iii) budgets — with seam pair sets
s0 = Bm1×B0, s1 = B0×B1, s2 = B1×B2 (in-team, later-before-earlier
= inverted): Inv_T(M) = #inv(s1 ∪ s2) ≤ vup and
Inv_T(M/2) = #inv(s0 ∪ s1) ≤ vdn, each per team, `none` =
unpriced.  T-FORCE-4 and L-PROJ (notes/62 §1) give soundness at ω
and both projections.

### 1.2 Pattern catalogue (the 4-block analogue of notes/55 §1.2)

Classify every 3-AP of V(M) by its nondecreasing block pattern in
{−1, 0, 1, 2}³ (20 conceivable).  **Lemma P-CAT [PROVED +
machine-exact at M = 16, 24, 32, 48, 64, 96]: exactly four
patterns are arithmetically empty:**

    (−1,−1,1), (−1,−1,2):  a, b ∈ Bm1 ⟹ c = 2b−a ≤ 3M/2 − 1 < 2M
    (−1, 0, 2):            a ∈ Bm1, b ∈ B0 ⟹ c ≤ 7M/2 − 1 ≤ 4M − 1
    (0, 0, 2):             a, b ∈ B0 ⟹ c ≤ 3M − 1 < 4M + 1

(the last is CORE′'s §1.2 emptiness one level up).  The sixteen
nonempty patterns split into: four in-block, six intra-window
mixed patterns (unit-bearing, as in notes/55 §1.2, once per
window), and the three **cross-window families** plus
(−1,−1,0)/(−1,0,0)/(−1,0,1)-style prefix mixes.  The three that
carry the pump are:

    H_dn  = (−1,0,1):  u ∈ Bm1, y ∈ B0, z = 2y−u ∈ B1
    H_up  = (0,1,2):   u ∈ B0,  y ∈ B1, z = 2y−u ∈ B2
    SKIP  = (−1,1,2):  u ∈ Bm1, y ∈ B1, z = 2y−u ∈ B2

**Family laws [machine-exact, 6 scales, M ≡ 0 mod 4]:**

    |H_up| = 5M²/4,   |H_dn| = 5M²/16 = |H_up|(M/2),
    |SKIP| = 13M²/16.

(Per attacker: #H_up(u) = 2M − ⌊u/2⌋ for u ∈ B0, and H_dn/SKIP
likewise with u ∈ Bm1 — the SKIP quarter-mass 13M²/64 + O(M) of a
parity class is notes/62 §4c's schedule law; the exact 13M²/16
total is confirmed here.)  Every family's endpoints share parity
(z ≡ u mod 2) — the arithmetic room for parity dodges, = Lemma
A7(a) at both anchors.

### 1.3 Lemma LEAK — the parametric '8'  [PROVED + machine]

The C1@16 witness (notes/62 §3b) voids H_up by donation and seeds
8 mono H_dn triples.  The '8' is an instance of:

**Lemma LEAK (counting identity).**  For any coloring in which
Bm1 ∩ T is single-parity p, define the *leak set*
L(T) = {z ∈ B1 ∩ T : z ≡ p (mod 2)} and, for z ∈ L(T), the parent
count c(z) = #{u ∈ Bm1 ∩ T : (u+z)/2 ∈ B0 ∩ T}.  Then

    μ_dn(T) := #mono-H_dn(T) = Σ_{z ∈ L(T)} c(z).

*Proof.*  A mono triple (u, y, z) ∈ H_dn ∩ T³ has z ≡ u ≡ p, so
z ∈ L(T), and y = (u+z)/2 determines the bijection with the
counted pairs.  ∎

[MACHINE: e175 P2 — verified against brute-force μ_dn AND the
recorded n_H_dn anatomy on five witnesses × both teams: C1@16
(leak {36,40,44,48} / {35,39,43,47}, c ≡ 2, μ_dn = 8 = the '8'),
C2@16, C2@24, f384@16, pump12@8 (all leak sums = 0 as recorded).]

Parametric reading of the donation-dodge mechanism: voiding H_up
costs nothing at the coloring level (any schedule with
B2-parity ≠ B0-parity, per the notes/62 §4c laws μ_up = 0 ⟺
s ≠ q); what the dodge CANNOT do for free is keep the leak set
empty at both windows once orders are priced — μ_dn = 0 forces
either r ≠ p (the pure schedules, killed under vdn = 0 by
SCHED-DEAD/L-PREFIX) or an empty leak inside a mixed B1.  Every
leak value z pays c(z) forced H_dn breaks (n_dn ≥ μ_dn, edge
injectivity — notes/47 §3, notes/62 §3b).  The '8' is not a
constant of the gadget; it is Σ c(z) of whatever leak the escape
chooses, and the identity is what a hand ladder should charge.

### 1.4 Band pigeonhole  [PROVED]

For every m: |P1(m)| = m+16 inside B1′ (size 2m, bal bound m) and
|P2(m)| = 2m+15 inside B2′ (size 4m, bal bound 2m) give

    |T ∩ P1(m)| ≥ 16,   |T ∩ P2(m)| ≥ 15   (balance, every team),

and P0(m) is a full block (bal m/2).  So balance implies CI(m)'s
bounds (≥ 2, even ≥ 3) with margin 13+, at every scale.
[MACHINE: e175 P3, m = 16..400.]

---

## 2. The correspondence: the pump IS two nested cores  [PROVED]

### 2.1 Observation NEST (change of coordinates)

Let m = M/2.  The lower window (M/2, 4M] of U4(M) is EXACTLY the
3-block window (m, 8m] at anchor m:

    (Bm1, B0, B1) = (B0′, B1′, B2′),   s0, s1 = its two seams,
    vdn = its anchor budget.

Under vdn = 0 and |B0 ∩ T| ≥ 1, transitivity forces the outer
Bm1×B1 order too, i.e. FULL block order — hypothesis (ii) of
CI(m) / the two-seam coupled core (with straddle-freeness (S)
enforced through the AP clauses, exactly as in Lemma U).  The
dictionary, entry by entry:

| pump object (anchor M)                | coupled-core object (anchor m = M/2)        |
|---------------------------------------|----------------------------------------------|
| lower window (M/2, 4M]               | the window (m, 8m]                           |
| vdn = 0                               | block order (ii), both seams + outer         |
| H_dn family                           | the straddle family (0,1,2) of CI(m) — A7@m  |
| L-PREFIX(i): μ_dn = 0 forced          | condition (S) of Lemma U(m)                  |
| parity dodge on H_dn                  | A7(a)@m: straddle endpoints share parity     |
| H_up family                           | the straddle family of CI(M) itself          |
| vup-charging (L-PREFIX ii/iii: forced s2 units) | the seam-2 wall A3/A4/E2@M — **S3 = 2×S2 one level up** |
| (16; 6,0)-MUS B2 stub = (4M, 4M+6]    | bottom 6 of S3(M) = [4M+1, 4M+16]  ✓machine  |
| SKIP family                           | A7-type straddles with the attacker one block below the window (new to the 4-block extension) |

So U4(M; v, 0) = CI-geometry at anchor m, FULLY enforced, glued
along the shared blocks B0, B1 to CI-geometry at anchor M whose
seam-2 wall is budget-relaxed to v (seams s0, s1 are clean by
vdn = 0, so the upper window's only currency is s2 — and by
L-PREFIX every mono H_up/SKIP triple pays a distinct s2 unit on
exactly the A3/A4 doubling material, the S3 = 2×S2 lock of
notes/51 in budgeted form; the MUS stub confirms the charge
support machine-exactly).

### 2.2 Theorem J-DOWN (the uniform (·,0)/(·,w) law)

**Theorem J-DOWN.**  Let m = M/2 and w ≥ 0, and suppose the
3-block coupled instance at anchor m — bounds b′ = the restriction
of b to (Bm1, B0, B1), seam budget w — is infeasible.  Then
U4(M; b; v, w) is infeasible for EVERY vup v (including `none`).

*Proof.*  L-PROJ downward (notes/62 §1): restrict a feasible state
to the lower window; every AP clause, bound, and s0/s1 indicator
of the 3-block instance is a constraint of U4; the restriction is
a feasible anchor-m state at budget w.  ∎

**Instances (all machine-anchored):**

| M  | bounds | half-core cited | consequence |
|----|--------|------------------|-------------|
| 32 | bal    | bal@16 UNSAT at w = 0,1,2 (e120/e127) | (v,w≤2)@32 UNSAT ∀v |
| 48 | bal    | bal@24 UNSAT w=0 (e120) | (v,0)@48 UNSAT ∀v |
| 64 | bal    | bal@32 UNSAT w=0 (e120) | (v,0)@64 UNSAT ∀v |
| 64 | const ⊇(3,3,3,·) | (3,3,3)@32 UNSAT (e120-family) | (v,0)@64 UNSAT ∀v |
| 96/128/160 | const ⊇(2,2,2,·) | (2,2,2)@48/64/80 UNSAT (e125/e126) | (v,0) UNSAT ∀v |
| 2m, m ≡ 0 mod 16, m ≥ 48 | bal | **Theorem N6a** (CI(m), GAP-N6a) + §1.4 pigeonhole | (v,0) UNSAT ∀v, uniformly |

The last row is the collapse: restrict further to CORE′(m)'s
support (allowed — a sub-restriction of the model); §1.4 gives the
bounds; CI(m) does the killing.  **GAP-J-schema's (·,0) family at
large anchors is GAP-N6a verbatim — one schema engine.**

[MACHINE, e175 collapse, all UNSAT, 0 failures:
C1 proj@32-bal (support (16,128], none,0) 1.5 s — the e120 bal@16
core reproduced through the 4-block encoder; C2 **full (none,0)@32
7.4 s — THE collapse cell**; C3 proj@48-bal 4.5 s (= bal@24);
C4 proj@64-const333 52.9 s (= (3,3,3)@32); C5 **CORE′(48)@96
(2,2,2,0) 39.2 s** — the locked CI(48) engine reached through the
4-block encoder, an independent cross-validation of e135.]

### 2.3 Corollary VMIN0 — the demand curve is not a growth curve

    v_min(0)(M) = ∞  for every M ≥ 32 covered above
    (bal: all M ∈ {32, 48, 64} machine; all M = 2m, m ≡ 0 mod 16,
    m ≥ 48 modulo GAP-N6a; const (2,2,2): M = 96/128/160 machine).

The finite regime is exactly the boot window M ≤ 24, where the
half-anchor core does not yet fire (v*₃(bal, m) = 0 for
m ∈ {4, 8, 12}):

    v_min(0)(8) = 12 (exact),  v_min(0)(16) ∈ (6, 384],
    v_min(0)(24) ∈ (65, 1440]  (finite: C2@24 (none,0) SAT).

[MACHINE, e175 small, 0 failures: (11,0)@8 UNSAT 39.6 s /
(12,0)@8 SAT 7.7 s (fresh replication of the exact point;
all-s2 witness, n_dn = 0), (6,0)@16 UNSAT 3.2 s, (65,0)@24 UNSAT
56.9 s — the task's 8/16/24/32 sweep, with 32 covered by C2.]

**Ledger consequences (notes/70 re-pointing).**
- [GAP-VMIN0-growth] is DISCHARGED BY COLLAPSE: the curve exits
  the finite range at M = 32; "growth of v_min(0)" is not a
  quantity any ω-argument should quote.  What T-TEL′ branch (b)
  actually uses at large anchors — "some team pays ≥ 1 at every
  anchor" — is the half-anchor core's own statement, i.e.
  GAP-N6a (const form), full stop.
- The queued pod cells (512,0)@32 and (512,0)@48 are MOOT
  (both UNSAT by Theorem J-DOWN rows 1–2; no compute needed).
- The quantitative per-anchor demand at ω is therefore the
  BUDGETED half-core frontier v*₃(m)-at-bounds (the e127/e159
  family) — [GAP-V*] regains the demand-side load that notes/70
  had shifted onto v_min(0), PLUS the margin family below.

### 2.4 The honest residue: what GAP-J still is

Theorem J-DOWN covers exactly the rectangle w < v*₃(m; b′).  NOT
covered, and genuinely joint:

1. **The margin family** U4(2m; v, v*₃(m) + b), b ≥ 0 — the lower
   anchor payable standalone, the joint cell dead anyway.  ALL the
   measured pump content lives here: (6,0)@16 and (65,0)@24 have
   m ∈ {8, 12} with v*₃(m) = 0, and the unresolved (368,6)@32
   (TIMEOUT 10800 s) has w = 6 ≥ v*₃(16) ∈ {5,6}.  At ω this
   family is what would push per-anchor demand ABOVE the 3-block
   floor; it is the surviving content of [GAP-J-schema], now
   precisely scoped.  Its boot-window instances are calibration,
   not ω-material — the three-arm (·,0) hand schema of notes/62
   §4c–4d (L-PREFIX / Lemma K / SCHED-DEAD) is hereby DEMOTED from
   ledger-load-bearing to boot-window documentation.
2. **The freshness family** F(N; v) [GAP-F-schema] does NOT
   project: F frees the shared seam below (only s0-currency is
   banned), and a one-seam-only 3-block theory is SAT (e120 seam
   controls) — so T-FRESH keeps genuine joint content at every
   scale and its tag is untouched by this front.
3. **Residues/bounds off the covered classes** (odd m·2, bounds
   between (1,1,1) and (2,2,2), M not ≡ 0 mod 32 in the uniform
   row) inherit exactly N6a's own residue caveats — nothing new is
   introduced by the pump.

### 2.5 Relation to notes/62's frontier reading (corrections)

- notes/62 §5 asked for "v_min(0) growth (16 vs 24)" as the
  decisive measurement and notes/70 promoted [GAP-VMIN0-growth]
  to THE demand curve: both are superseded — the decisive object
  was the collapse threshold (M = 32), not a growth law.  The
  "lavish dodge" of the cascade calculus is priced ∞ from M = 32
  on: there IS no lavish escape at the half-anchor once the core
  fires below.
- notes/62 §4's floor-bootstrapping channel (C1-type cells) and
  NG4 are unaffected: budget rectangles remain demand-only; the
  collapse strengthens demand maximally at the (·,0) corner but
  contributes nothing to supply [GAP-AFFORD′ unchanged, still THE
  terminal statement].
- The (16; 6,0) MUS reading in notes/62 §3d ("the (·,0) core is a
  lower-window object with a thin upper boundary family") is now
  structural: lower-window object = CI(8)-degenerate-band material
  (its whole B1-support sits inside P2(8) = [33, 63], with 64
  absent — machine, e175 P4), thin upper family = the bottom of
  S3(16) (the budgeted seam-2 wall).

---

## 3. Machine record (e175_pump_schema.py, 2026-08-30, all parts
## 0 failures)

- catalogue: P1 pattern emptiness {(−1,−1,1),(−1,−1,2),(−1,0,2),
  (0,0,2)} + family counts vs enumeration at 6 scales + the three
  closed-form laws; P2 Lemma LEAK on 5 recorded witnesses × 2
  teams (incl. the C1 '8'); P3 pigeonhole 16/15 at m = 16..400;
  P4 MUS anchors (stub ⊂ S3, lower support ⊂ CORE′(8) bands).
- collapse: C1–C5 (see §2.2) — the two NEW verdicts of this front
  are C2 (none,0)@32-bal UNSAT and C5 CORE′(48)@96 UNSAT; C1/C3/C4
  re-derive the recorded half-cores through the 4-block encoder.
- small: S1–S3 (see §2.3), fresh re-runs, verdicts identical to
  the e158/e173 records.
- Data: data/e175_pump.jsonl (streaming, every check),
  data/e175_collapse.log, data/e175_small.log.

## 4. Next steps (for the fronts that own the residue)

1. [J/F-SCHEMA front, notes/71] Re-scope to the margin family +
   F-family only (§2.4); the (·,0) uniform law is done here.
2. [TELESCOPE/ledger] Re-derive branch (b) demand directly from
   the const-bounds half-core at every large Case-2 anchor
   (D1+D2 + Theorem J-DOWN row 5) and re-point the demand curve at
   the budgeted frontier v*₃(m; 2,2,2) [GAP-V* const form].
3. [pods] Cancel/ignore (512,0)@32 and (512,0)@48; spend the freed
   budget on the margin cell (368,6)@32 (unresolved) and a first
   margin point at 48: (v, 3)@48-bal for v large (w = 3 is the
   first budget above bal@24's known UNSAT w ≤ ... measure
   v*₃(bal,24) bracket first — (4,65] per notes/60).
4. [N6a] Nothing new needed: every (·,0) demand at ω now rides
   Theorem N6a — the intended collapse, achieved.
