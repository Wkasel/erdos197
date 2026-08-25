# 30 — Lemma OG: human proof draft (task S)

Machine companion: `experiments/e94_step_check.py`; full logs
`data/step_check.log` / `.json`.  Every step below tagged
**[PARAM-CHECKED]** was machine-verified at M = 44, 48, 52, 60 (plus
M = 40 as anchor); steps tagged **[PROVED]** are complete human
arguments valid for the stated M range; steps tagged **[M40-ONLY]**
are honest gaps — they hold (or have a hand derivation) only at
M = 40.  A consolidated gap list is Section 8.

Independent audits: `experiments/e95_adv_verify.py` re-derived every
machine-cited fact of this note with a fresh eager-transitivity
encoding (84/84 checks pass, `data/e95_adv_verify.log`, commit
7816865); `experiments/e95_uniformity_check.py` stress-tested the
draft at adversarial scales off the M ≡ 0 (mod 4) test class
(`data/uniformity_check*.log`) — its findings are folded into S11,
S12 (parity-scope paragraph), S13 and G6 below.

> **CORRECTION TO THE RECORD (important).**  The pivot story of notes
> 28 and `data/og40_backbone.txt` — "at M = 40 attacks 1–13 are
> consistent, force 47<78, and attack #14 (78<47) delivers the
> contradiction" — is a property of the *restricted* instance (the
> 59-triple MUS over 37 values), **not** of the full order gadget.
> On the full instance (all AP triples over (40, 80]) the attack
> prefix already becomes infeasible at attack #10 = 16-attack j = 3:
> the 15-family plus 16-attacks j = 1, 2 is consistent, and adding
> t_10 ≺ b_3 is UNSAT.  Verified by two independent encodings (lazy
> transitivity + eager full transitivity, `e94_step_check.py` Part 0/1).
> So on the full instance M = 40 behaves exactly like the generic
> M ≡ 0 (mod 4) case of probe P1 (j* = 3).  The note-28 refutation
> remains a *sound* derivation (its case trees only ever apply genuine
> AP triples and attacks), so OG(40) is still refuted by it; it is
> just not the earliest conflict.  Everything below is stated against
> the full instance.

---

## 0. Statement and proof status

**LEMMA OG.**  For every M ≥ 40 there is no linear order ≺ (the
"position order", u ≺ v meaning u is placed before v) of the integer
interval (M, 2M] such that

* (i) *(no monotone AP)* for every arithmetic progression
  a < b < c inside (M, 2M] (a + c = 2b), neither
  a ≺ b ≺ c nor c ≺ b ≺ a holds; and
* (ii) *(guards precede bottoms)* for x ∈ {15, 16} and 1 ≤ j ≤ x/2
  the value 2M + 2j − x precedes the value M + j.

Status: machine-proved infeasible (Cadical195 UNSAT) at every scale
tested: all of M = 16 … 200 and the dyadic scales M = 128, 512 (the
blocks (128, 256] and (512, 1024]).  The record is a union of
separate runs and the note should be read that way: e87/e89 cover
M = 40, 41, 50, 51, all of 60 … 200, and M = 128, 512; the e94
sweeps (Parts 3, 9) cover every M in 40 … 100, both parities; the
e95 audit closed 16 … 39 (all genuinely UNSAT; the instance is
well-formed at every M ≥ 16, because an attack collapses to v ≺ v —
t_{x−2j} = b_j — exactly at M = x − j ≤ 15, e.g. t₁₄ = b₁ at
M = 15, below which the gadget degenerates; for 16 ≤ M ≤ 22 a
guard can coincide with a *different* bottom, which is harmless —
every attack pair is still a genuine pair).  M = 2048 is unresolved (the e89
lazy-transitivity run made 200+ rounds in ~5700 s with no verdict).
Fresh independent recheck (e96): OG(128) UNSAT under a full eager
O(n³) transitivity encoding; OG(512) UNSAT re-run.  This note assembles the best current
*human* proof: a fully parametric top layer (Sections 1–3, 5) resting
on a finite family of forced-order lemmas (Section 4) that are
machine-certified at M = 44, 48, 52, 60 but whose hand derivations
exist today only at M = 40.  It is a draft of a proof, not a proof.

Notation: **b_j := M + j** (bottoms), **t_i := 2M − i** (tops/guards),
**m_a := (3M + a)/2** (midband; integer iff a ≡ M mod 2),
**q_a := (7M + a)/4** (quarterband; integer iff a ≡ M mod 4).
The 15-attacks are t_{15−2j} ≺ b_j (j = 1..7), the 16-attacks
t_{16−2j} ≺ b_j (j = 1..8).

---

## 1. Setup and the reflection rule

**Step S1 (midpoint-extremal rule) [PROVED].**
Constraint (i) says exactly: *in the position order, the arithmetic
midpoint of any 3-AP of (M, 2M] is never the middle element*.  For in
a linear order on {a, b, c} the only patterns with b in the middle
position are a ≺ b ≺ c and c ≺ b ≺ a — precisely the two forbidden
ones.  Equivalently: for every AP (a, b, c), either b precedes both a
and c ("b leads") or b follows both ("b trails").

**Step S2 (the four reflection rules) [PROVED].**
For any AP (a, b, c) in (M, 2M], S1 gives four unit-propagation
rules, used silently everywhere below (together with transitivity of
≺):

* R1: a ≺ b ⟹ c ≺ b  (b cannot lead once a is before it, so b trails)
* R2: b ≺ c ⟹ b ≺ a  (b cannot trail, so b leads)
* R3: c ≺ b ⟹ a ≺ b  (b trails)
* R4: b ≺ a ⟹ b ≺ c  (b leads)

**Step S3 (attack/AP interface) [PROVED].**
For a bottom b_j and top t_i the arithmetic midpoint is
(b_j + t_i)/2 = m_{j−i}, an element of (M, 2M] whenever j − i ≡ M
(mod 2) (and inside the interval for the small i, j used here).  So
an attack pair (t_i, b_j) with j − i ≡ M (mod 2) spans an AP
(b_j, m_{j−i}, t_i) of the interval; when j − i ≢ M (mod 2) the
midpoint is a half-integer and that attack engages the reflection
rules only through longer APs (e.g. at even M the 15-attacks with
even j — such as (t₁₁, b₂), midpoint (3M−9)/2 — span no midband
AP).  The parity-matching half of the attacks are thus not isolated
order axioms: they immediately engage the reflection rules through
the midband.  This is the mechanism of the whole refutation: guards
forced early push their midpoints via R1–R4, midpoints collide
inside the midband, and the collision eventually forces some
*bottom* before its own guard, contradicting (ii).

---

## 2. Anchor coordinates and the M = 40 coincidences

**Step S4 (anchor bands) [PROVED].**
Every parametric family used below is affine of the form
v(M) = (pM + q)/4 with slope p ∈ {4, 5, 6, 7, 8}: bottoms (p = 4),
five-quarter points (p = 5), midband (p = 6), seven-quarter points
(p = 7), tops (p = 8).  A triple of anchor forms is an AP
*identically in M* iff the slopes satisfy p₁ + p₃ = 2p₂ and the
offsets q₁ + q₃ = 2q₂ (probe P3).

**Step S5 (coincidence lemma) [PROVED].**
M = 40 is the unique M at which the following band collisions happen
(each is a one-line linear equation):

* M + 17 = m_{−6} ⟺ M = 40  (the value 57)
* M + 19 = m_{−2} ⟺ M = 40  (the value 59)
* M + 21 = m_{2} = t_{19} ⟺ M = 40  (the value 61)
* m_{12} = q_{−16} = t_{14} ⟺ M = 40  (the value 66)

Consequence: a single value of the M = 40 instance can play several
parametric roles at once, and the M = 40 refutation of note 28
exploits such collisions.  For M > 40 the roles separate into
distinct values, so **no verbatim lift of the M = 40 derivation can
exist**; the parametric proof must choose, for every literal of the
derivation, *which* anchor lift of it survives.  Section 4 reports
exactly that (machine-scanned).  This also explains probe P3's
parity locks: midband anchors exist only for a ≡ M (mod 2),
quarterband only for a ≡ M (mod 4), so no anchor pattern is common
to all residues of M.

---

## 3. Top-level reduction: ten attack units suffice (generically)

**Step S6 (prefix conflict, j*) [PARAM-CHECKED].**
Let j*(M) be the least j such that constraint (i) + the seven
15-attacks + the 16-attacks 1..j is infeasible.  Machine facts
(Part 1/3 of e94_step_check):

* the 15-family alone is always consistent (checked at all test M;
  known SAT for the whole gadget when the 16-family is dropped);
* j*(40) = j*(44) = j*(52) = j*(60) = 3, j*(48) = 2 — and from probe
  P1: j*(50) = 1, j*(56) = 3, j*(64) = j*(72) = j*(80) = 2.

**Step S7 (Theorem A, the 10-unit core) [PARAM-CHECKED].**
For every M in {40, …, 100} ∪ {104, 108, 112, 120, 128, 150, 200}
**except** M ∈ {51, 67, 83, 99}, constraint (i) together with only
the ten attack units

  15-family: t₁₃≺b₁, t₁₁≺b₂, t₉≺b₃, t₇≺b₄, t₅≺b₅, t₃≺b₆, t₁≺b₇
  16-attacks j = 1, 2, 3: t₁₄≺b₁, t₁₂≺b₂, t₁₀≺b₃

is infeasible.  Since these ten units are among OG(M)'s attacks,
**Lemma OG follows for all such M**.  The exceptional M are exactly
M ≡ 3 (mod 16) in the swept range; they are handled in Step S9.

**Step S8 (four- and three-unit cores on the dyadic-relevant
classes) [PARAM-CHECKED].**
Sharper cores exist on arithmetic subclasses (Part 8, swept
M = 40..100 both parities plus {104, 112, 120, 128, 150, 200}):

* **C4 = {t₁₃≺b₁, t₁₁≺b₂, t₅≺b₅, t₁₀≺b₃}** (15-attacks j = 1, 2, 5
  and the 16-attack j = 3) is infeasible with (i) at **every swept
  M ≡ 0 (mod 4)** — and at no other swept M (it is satisfiable at
  every non-multiple of 4 in the sweep).
* **C3 = {t₅≺b₅, t₃≺b₆, t₁₀≺b₃}** (15-attacks j = 5, 6 and the
  16-attack j = 3) is infeasible with (i) at **every swept
  M ≡ 0 (mod 8)** — and satisfiable at every other swept M,
  including the class M ≡ 4 (mod 8).

Since every dyadic scale M = 2^k (k ≥ 3) is ≡ 0 (mod 8), the
campaign's dyadic case of Lemma OG reduces to: *the two 15-attacks
j = 5, 6 and the 16-attack j = 3 alone are inconsistent with the
no-monotone-AP constraint*.  Three order axioms.  This is the
sharpest known parametric target for a human proof, and its mod-8
rigidity (true at 0, false at 4 mod 8) again reflects the
quarterband parity locks of S5/P3.

**Step S9 (the exceptional family M ≡ 3 mod 16) [PARAM-CHECKED].**
At the four exceptions of S7 — and at 115, 131 as well — j*(M) = 4:
the 15-family + 16-attacks 1..4 is infeasible (Part 9).  Hence the
uniform version of Theorem A over the whole sweep:

> **Theorem A′.**  For every swept M (all of 40..100 and
> {104, 108, 112, 120, 128, 150, 200}, both parities), constraint
> (i) plus the eleven attack units 15{1..7} ∪ 16{1..4} is
> infeasible; hence OG(M) is infeasible.

Why the residue class M ≡ 3 (mod 16) resists the 16{1..3} prefix
and needs 16:4 is not understood — a structural explanation is
lacking [GAP].

**Step S10 (what remains for a full proof) [GAP].**
Steps S6–S9 are finite machine verifications.  No human induction on
M is known; the support-size data of Section 4 (growing linearly in
M) suggests the refutation cannot be certified by a fixed finite set
of parametric triples, so a human proof of Theorem A for all M will
need a genuinely new idea (e.g. a compactness/limit argument on the
order types of (M, 2M] as M → ∞, or an explicit strategy argument in
the midband).  This is the principal open gap.

---

## 4. The forced-order lemmas, parametrically

Hypothesis for this section: **H\*(M)** := 15-family + 16-attacks
1..j*(M)−1 — the maximal consistent attack prefix (so H\* is SAT and
"forces" is non-vacuous).  At the test scales H\*(M) = 15-family +
16{1,2} for M = 40, 44, 52, 60 and 15-family + 16{1} for M = 48.

Method (Part 5 of e94_step_check): each of the 27 literals of the
note-28 forcing DAG was lifted along every anchor slope
p ∈ {4,…,8} through its M = 40 value (values that appear in attacks
were pinned to their attack roles), and the lift was kept iff H\*(M)
forces it at *all* of M = 44, 48, 52, 60.  Results:

**Step S11 (bottom-vs-guard invariants) [PARAM-CHECKED].**
Under H\*(M), at every test M (all ≡ 0 mod 4; e95 adds M = 100 and
128 with identical outcomes):

* t₁₄ ≺ b₁ (16-attack j = 1, an axiom of H\*), and
* **b₃ ≺ t₁₀**, **b₅ ≺ t₆**, **b₇ ≺ t₂** are *forced* — bottoms
  are pushed before their own 16-guards.  At M = 44, 52, 60
  additionally **b₆ ≺ t₄** is forced (so *four* bottoms there, not
  three; Part 4 / e95 V2 — the b₆ row is undetermined at M = 40 and
  48).  (At M = 40, 44, 52, 60 also t₁₂ ≺ b₂ is an axiom; at M = 48
  the *reverse* b₂ ≺ t₁₂ is forced, which is exactly the
  j*(48) = 2 conflict.)
* b₅ ≺ t₆ is NOT forced by the 15-family alone (checked at all test
  M) — *some* 16-attack is needed to start the cascade.  (At M = 48
  the consistent prefix contains only 16{1} and b₅ ≺ t₆ is still
  forced, so the earlier phrasing "the 16-attacks j ≤ 2 are needed"
  overstated it.)  Scope warning (e95): this bullet is specific to
  M ≡ 0 (mod 4).  At M = 42, 46, 50, 54 (≡ 2 mod 4) b₅ ≺ t₆ IS
  forced by the 15-family alone; at the odd scales tested it is not
  forced under H\* at all (see the parity-scope paragraph below).

**Step S12 (parametric mid-order lemmas) [PARAM-CHECKED].**
The following lifts of DAG literals are forced by H\*(M) at all test
M — including the anchor M = 40 itself (e95 V4: all 19 literals
forced at all five scales) and, by the e95 audit, at M = 100 and
128 (selection; full table in `data/step_check.log`, Part 5):

| # | forced order | lift of (M=40) |
|---|--------------|----------------|
| O1 | M+19 ≺ M+13 and t₂₁ ≺ t₂₇ | 59<53 |
| O2 | M+11 ≺ M+21 and t₂₉ ≺ t₁₉ | 51<61 |
| O3 | t₁₃ ≺ t₁₉, t₁₃ ≺ t₂₃, t₁₃ ≺ M+17 | 67<61, 67<57 |
| O4 | t₉ ≺ t₁₁, t₉ ≺ t₇, t₁₁ ≺ t₂ | 71<69, 71<73, 69<78 |
| O5 | **M+7 ≺ M+21** | 47<61 |
| O6 | **M+21 ≺ t₂**, m₂ ≺ t₂, t₁₉ ≺ t₂ | 61<78 |
| O7 | **m₂ ≺ M+4**, M+21 ≺ M+4, t₁₉ ≺ M+4 | 61<44 |
| O8 | M+31 ≺ M+21, t₉ ≺ M+21 | 71<61 |

Two structural remarks, both machine-facts:

* **The note-28 kernel does not lift.**  The literal 66<53 — the
  root lemma d1 of the whole M = 40 DAG — admits *no* forced anchor
  lift at all ([M40-ONLY]; see S5: 66 is a triple band-collision
  point).  Originally this was scanned only under the PIN slope
  restriction, which excluded exactly the interesting midband
  (3M+12)/2 and quarterband (7M−16)/4 lifts of 66; the e95 V6
  extended scan over all 25 slope pairs (PIN-excluded ones
  included) still finds no forced lift, so the claim now stands on
  the full slope grid.  The M = 40 derivation's foundation is an
  artifact of the coincidences, even though most of its
  *conclusions* survive.
* **Supports are wide and grow with M.**  Deletion-minimal triple
  supports under H2 = 15-family + 16{1,2} (Part 6):

  | lemma | support at M=44 | at M=60 | shared APs (v−M coords) | shared APs (v−2M coords) |
  |-------|----------------|---------|-------------------------|--------------------------|
  | O5: b₇ ≺ M+21 | 124 triples | 246 | 41 | 37 |
  | O6: M+21 ≺ t₂ | 131 | 262 | 42 | 39 |
  | O7: m₂ ≺ M+4 | 131 | 262 | 37 | 36 |
  | b₇ ≺ t₂ (S14) | 138 | 270 | 41 | 42 |

  (Unit minimization keeps essentially all of H2 — 7 to 9 of the 9
  units — in every case.)  Support size grows roughly linearly in M
  (122–132 extra triples over ΔM = 16, i.e. ≈ 7.6–8.3 triples per
  unit of M between the two scales), while the *parametric* part —
  the bottom-anchored APs (M+α, M+β, M+γ) and top-anchored APs
  (2M−α′, 2M−β′, 2M−γ′) common to M = 44 and 60, listed in the log —
  stays near 40 + 40 triples; the growing remainder is M-dependent
  midband filler.  This *suggests* that none of O1–O8 has a bounded
  parametric certificate over a *fixed* triple list, but it does
  not prove it: the evidence is two scales of *deletion-minimal*
  (not minimum-cardinality) supports produced by a single
  randomized elimination order, and a different lemma architecture
  could in principle avoid these supports entirely.  What is
  unconditional is that a hand derivation in note-28 style (case
  tree over a fixed triple list) exists only at M = 40 [M40-ONLY].
  This is the second honest gap: Section 4's lemmas are
  *machine-certified parametric facts*, not yet human-derived ones.

**Parity scope [PARAM-CHECKED, e95 audit].**  The whole lemma layer
above is a property of the residue class M ≡ 0 (mod 4).  The e95
uniformity audit (`experiments/e95_uniformity_check.py`, logs
`data/uniformity_check*.log`) re-tested S11/S12/S14 at the
adversarial scales M = 41, 43, 45, 47, 49, 53 (odd) and
42, 46, 50, 54 (≡ 2 mod 4), plus M = 100 and 128:

* at M = 100 and 128 (≡ 0 mod 4) every S11 invariant, every
  O-lemma and the full S14 chain hold — the layer is scale-robust
  *within* its residue class;
* at odd M the layer breaks hard: O1b, O2b, O3a, O3b, O4a, O4b and
  O7b are **reverse-forced** — the stated orientation is provably
  false (cross-validated against the eager encoding, 8/8 AGREE) —
  most other O-literals are undetermined, and O6b/O7a (like F1–F7)
  are ill-formed there, since m₂ and q₋₁₆ are non-integral at odd
  M;
* at M ≡ 2 (mod 4) the maximal consistent prefix is the bare
  15-family (j\* = 1) and O5 (b₇ ≺ b₂₁) is **reverse-forced** — the
  first link of the S14 chain is provably false on this entire
  class;
* the cross-class survivors are the top layer (S6–S9) plus a few
  scattered literals (O3c, O4c, O6c, O8b at most odd scales;
  b₃ ≺ t₁₀ at M ≡ 3 mod 4).

Sections 4–5 therefore constitute an argument for M ≡ 0 (mod 4)
only; the other residue classes need per-class kernels (G6).

---

## 5. The final chain: b₇ before t₂, against the 16-attack j = 7

This section presents the chain in the form requested (pivot at the
16-attack j = 7).  Recall from S6 that on the full instance the
*earliest* conflict is at 16-attack j = j*(M) ≤ 3 (generically); the
j = 7 chain below is a valid, machine-checked alternative refutation
at every test M (and at M = 100 and 128, e95 audit), and is the
direct parametric descendant of the note-28 spine.

Assume, for contradiction, that ≺ satisfies (i) and all attacks.
In particular ≺ satisfies H\*(M), so all of Section 4 applies.

**Step S13 (m₂ ≺ t₂ by one reflection) [PROVED from O7].**
(b₄, m₂, t₂) = (M+4, (3M+2)/2, 2M−2) is an AP identically in M:
(M+4) + (2M−2) = 3M+2 = 2·m₂, valid for every even M.  O7 gives
m₂ ≺ b₄; rule R4 (midpoint leads) yields **m₂ ≺ t₂**.  (This is
the parametric form of the note-28 step d18→d19,
61<44 ⟹ 61<78; it machine-agrees with the m₂-entry of O6.)

*Parity case.*  m₂ exists only for even M.  For odd M the analogous
AP into t₂ is (b₅, m₃, t₂) = (M+5, (3M+3)/2, 2M−2), so the
analogous step would be m₃ ≺ b₅ ⟹ m₃ ≺ t₂ (R4).  The e95 audit
tested it: m₃ ≺ b₅ (and hence m₃ ≺ t₂) is forced at
M = 41, 43, 45, 49, 53 — but **not** at M = 47 (undetermined), so
the proposed odd-parity repair is itself non-uniform on the odd
class — [GAP G6].

**Step S14 (b₇ ≺ t₂ by transitivity) [PROVED from O5, O6].**
O5: b₇ = M+7 ≺ M+21.  O6: M+21 ≺ t₂.  Transitivity:
**b₇ ≺ t₂** — the bottom b₇ = M+7 precedes its own 16-guard
t₂ = 2M−2.  (Note the route goes through M+21, the *bottom-band*
lift of the M = 40 value 61; the mid-band route through m₂ cannot
be used, because b₇ ≺ m₂ is forced only at M ∈ {40, 48} of the
test set and is undetermined under H\* at M = 44, 52, 60
(supplemental check) — only the bottom-lift chain survives at all
test M.  At M = 40 the two routes coincide, S5.)

**Step S15 (contradiction) [PROVED].**
OG(M)'s 16-attack j = 7 demands t₂ ≺ b₇.  With S14, ≺ cannot
exist.  ∎ (for every M at which O5, O6, O7 hold)

**Caveats [GAP].**  (a) O5–O7 are machine-certified at
M ∈ {40, 44, 48, 52, 60} only; (b) at M = 48 the hypothesis H2 =
15+16{1,2} is itself already contradictory (j* = 2), so there the
chain is sound but redundant — the honest earliest conflict is at
16-attack j = 2; (c) from probe P1, at M = 50 the maximal prefix is
the bare 15-family and b₇ ≺ t₂ is *not* forced — the j = 7
presentation genuinely fails there and only the j* = 1 route
refutes; the e95 audit extends this failure to the *whole* class
M ≡ 2 (mod 4) (b₇ ≺ t₂ undetermined and O5 reversed at
42, 46, 50, 54) and to every odd scale tested (chain literals
undetermined) — see the Section 4 parity-scope paragraph; (d) the
chain's last-attack identity (j = 7) is therefore
*presentational*: the universal shape (P1 + S11) is "some bottom
b_j is forced before its own 16-guard t_{16−2j}, and the 16-attack
for that j closes the contradiction", with j ∈ {1, 2, 3, 7}
depending on M.

---

## 6. The complete human refutation at M = 40 [M40-ONLY]

Note 28 (`notes/28-chains-M40.md`) contains a complete,
pencil-checkable refutation of OG(40): a 27-node lemma DAG rooted at
the 8-attack core {15:1, 15:2, 15:4, 15:5, 15:6, 16:1, 16:3, 16:4},
with machine-minimized case-tree certificates (≤ 3 splits per node,
only 4 nodes need any splits), culminating in 47 ≺ 78 = b₇ ≺ t₂
against the 16-attack j = 7.  Its inferences use only R1–R4 and
transitivity over genuine AP triples of (40, 80], so it is a sound
refutation of the full OG(40) even though it was extracted on the
restricted 59-triple MUS.  It is the [M40-ONLY] instantiation of
Sections 4–5; its kernel lemma (66<53) is precisely the part that
does not survive parametrically (S12).

---

## 7. The P3 skeleton: the invariant triple stock

**Step S16 (skeleton instantiation) [PARAM-CHECKED].**
The seven anchor patterns F1–F7 of probe P3 instantiate as genuine
APs of (M, 2M] at every test M — this *arithmetic* half is Part 7
of e94_step_check, and it carries a parity restriction the earlier
draft left implicit: the midband anchors of F1–F6 are integral only
for even M, and F7's quarterband anchor q₋₁₆ only for
M ≡ 0 (mod 4), so the patterns are well-formed statements only on
that class:

  F1 (b₁, m₋₆, t₇) · F2 (b₅, m₂, t₃) · F3 (b₇, m₂, t₅) ·
  F4 (M+17, m₋₂, t₁₉) · F5 (M+19, m₁₄, t₅) · F6 (m₋₂, m₆, m₁₄) ·
  F7 (m₂, q₋₁₆, t₉)

The *in-some-MUS* half is certified at every tested M ≡ 0 (mod 4)
by the separate P3 scripts (`e94_pattern_in_some_mus.py`, logs
`data/og_pat_*.log`) — not by Part 7 — and was independently
re-certified at M = 44 by joint-protection deletion (e95c: all
seven patterns protected simultaneously survive into a MUS).  The
joint/shuffled method is essential: single-pattern fixed-order
protection *fails* for F2, F3, F4, F7 (e95b) — those patterns are
in-*some*-MUS but not in every deletion-order's MUS.
Note how they line up with Section 4–5: F2/F3 are the two attacks'
APs through the pivot midpoint m₂ (S13 uses the AP (b₄, m₂, t₂),
the j = 4 analogue); F6 is the midband chain that drives the
mid-order lemmas O1–O3; F4 contains the S5 coincidence values.  The
skeleton is the invariant ~7% of the refutation; the remaining
~50–250 triples vary with M (S12), which is why the skeleton alone
does not yield a parametric certificate.

---

## 8. Consolidated gap list

* **G1 (general-M closure).**  The top layer (S7–S9: Theorems A, A′
  and the C4/C3 cores) is a finite machine verification (sweep
  M = 40..100 both parities, plus 104–200 selections and the
  exceptional family to 131).  No proof for *all* M ≥ 40 exists;
  no induction on M is known.  The support growth measured in S12
  (≈ 7.6–8.3 triples per unit of M) *suggests* that no fixed finite
  list of parametric triples can certify the infeasibility for all
  M, but this is an inference from two scales of deletion-minimal
  supports, not a proven impossibility — a bounded certificate
  under a different lemma architecture is not excluded.  Either
  way, closing this gap appears to need a genuinely new argument
  (limit/compactness over order types, a direct combinatorial
  argument in the midband, or a certificate family found by better
  search).
* **G2 (exceptional residues).**  M ≡ 3 (mod 16) defeats the
  generic 10-unit core and needs the 16-attack j = 4 (j* = 4,
  verified at 51, 67, 83, 99, 115, 131).  No structural explanation
  for this residue-16 phenomenon; and the sweep beyond 131 in this
  class is unexplored.
* **G3 (machine-only lemmas) [M40-ONLY hand derivations].**  Every
  forced-order lemma of Section 4 (O1–O8 and the S11 invariants) is
  machine-certified at M ∈ {40, 44, 48, 52, 60} only.  Hand
  derivations (case trees over an explicit triple list) exist only
  at M = 40 — note 28, and on the restricted instance at that.  No
  human derivation of any of these lemmas is known at any M > 40.
* **G4 (the kernel does not lift) [M40-ONLY].**  The root lemma
  66<53 of the note-28 DAG admits *no* forced anchor lift under
  H\* (Part 5; confirmed on the full 25-slope-pair grid including
  the PIN-excluded midband/quarterband lifts by e95 V6): the
  foundation of the only complete human refutation we have is an
  artifact of the M = 40 band collisions (S5).  A parametric human
  proof must be rebuilt from different kernels (candidates: the C3
  core of S8).
* **G5 (final-attack identity) [NOT UNIVERSAL].**
  The requested j = 7 presentation (Section 5) is machine-valid at
  M ∈ {40, 44, 48, 52, 60} but provably fails at M = 50 (probe P1:
  under the maximal prefix — there the bare 15-family — b₇ ≺ t₂ is
  not forced; the refutation there runs through j* = 1).  The
  universal statement is the *shape*: some bottom b_j is forced
  before its own 16-guard t_{16−2j}, with j ∈ {1, 2, 3} generically
  (j = 7 also available at the tested M ≡ 0 mod 4 scales).  Within
  the chain, the mid-band route b₇ ≺ m₂ is forced only at
  M ∈ {40, 48} — at M = 40 by the S5 coincidence b₂₁ = m₂.
* **G6 (odd M and M ≡ 2 mod 4) [WORSE THAN FIRST STATED].**  The
  lemma layer (Section 4) and chain (Section 5) are not merely
  uncertified off M ≡ 0 (mod 4) — the e95 audit shows several of
  them are *false* there: at odd M seven O-lemmas (O1b, O2b, O3a,
  O3b, O4a, O4b, O7b) are reverse-forced and the chain literals
  are undetermined; at M ≡ 2 (mod 4) the chain's first link O5 is
  reverse-forced (Section 4, parity-scope paragraph).  The natural
  odd-M repair of S13 (m₃ ≺ b₅ ⟹ m₃ ≺ t₂) is itself non-uniform:
  m₃ ≺ b₅ is forced at M = 41, 43, 45, 49, 53 but *not* at M = 47.
  The other residue classes are genuinely covered only by the
  top-level sweeps (S7/S9, both parities) and the direct
  full-gadget UNSAT (e89/e95); a per-class lemma layer would have
  to be rebuilt from per-class kernels (the reverse-forced
  literals themselves are stable within their classes and are the
  natural candidates).  Only the top layer (A′/C4/C3 with
  per-residue cores) is a viable parametric spine across all
  residues.
* **G7 (unused invariant).**  b₅ ≺ t₆ is forced under H\* at every
  tested M (S11, and P1 at eight more M) yet is *not* forced by the
  15-family alone and is never used by the Section 5 chain.  It is
  the most stable single invariant across all probes and a
  satisfying human proof should explain and exploit it; this draft
  does not.

---

## 9. Verification pointers

* `experiments/e94_step_check.py` — all Parts referenced above;
  rerun: `.venv/bin/python experiments/e94_step_check.py`
  (≈ 300 s).  Outputs `data/step_check.log`, `.json`.
* Part 0 cross-validates the lazy-transitivity encoding against an
  eager O(n³) encoding at M = 40, 44 (AGREE).
* Independent full-gadget UNSAT: e87/e89 (M = 40..200 as detailed
  in Section 0, plus M = 128 and 512).  Probe scripts: e92 (P1),
  e93 (P2), e92–e94d (P3).
* Adversarial re-verification: `e95_adv_verify.py` (fresh eager
  encoding, 84/84 checks, `data/e95_adv_verify.log`);
  `e95b_adv_verify_restricted_mus.py` (restored the og40_backbone
  record on the restricted 59-triple MUS: attacks 1–13 SAT forcing
  47<78, attack #14 UNSAT, backbone exactly 69 pairs; also the
  single-pattern protection failures for F2/F3/F4/F7);
  `e95c_adv_verify_insomemus.py` (joint in-some-MUS
  re-certification of F1–F7 at M = 44).
* Parity/uniformity audit: `e95_uniformity_check.py` +
  `e95b_threshold_and_crossval.py` + `e95c_mod2class.py`
  (`data/uniformity_check*.log`): top layer uniform at
  M ∈ {41, 43, 45, 47, 49, 53, 100, 128}; lemma layer parity locks
  and reverse-forcings (S11/S12/S13/G6); full OG(M) UNSAT down to
  M = 16; eager cross-validation of the reverse-forcings (8/8).
* Reduction-side checks (paper section): `e96_reduction_check.py`
  (`data/e96_reduction_check.log`): gadget boundary arithmetic,
  the thm:chunk case table (exhaustive), attack forcing from
  s(x) < s(b_j), running-max normalization (δ ≥ 0), and a fresh
  eager-encoding OG(128) UNSAT; `data/e96_og512_recheck.log`
  re-runs OG(512) UNSAT.
