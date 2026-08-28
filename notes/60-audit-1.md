# 60-audit-1 — Referee audit of notes/52 (BRIDGE1) and notes/57 (DICH)

Second referee pass (2026-08-28), scoped to exactly TWO drafts:
notes/52-bridge1.md (Theorem B1 + the §4.3 descent analysis) and
notes/57-dich.md (mechanistic K* law + Theorem H-DICH).  Independent
of notes/60 (the night-2 audit): no code shared with
audit/a7_night2/*; fresh adversarial colorings; fresh scales.
Instruments in audit/a8_referee1/; solver data data/a8_*.log.

Standard: a claim survives only if I would defend it as referee.
Verdict tags: SOUND / GAPS(list) / BROKEN(where), per draft.

---

## 1. notes/52 (BRIDGE1) — reconstruction and line-by-line

### 1.1 Lemma PIN (§1.3) — re-derived  [SOUND]

Independent reconstruction: fix mono-AP-free arrangement π, Q =
max(pos(a₁), pos(a₂)), F = positions ≤ Q (finite).  Blocks are
disjoint, so ≤ |F| scales meet F; at every other clean scale order
S = B(m) ∩ T by position.  (i) a positionally monotone in-block AP
would be a monotone AP of π.  (ii) for AP (a, y, z), a ∈ {a₁,a₂},
y,z ∈ S: pos(a) ≤ Q < pos(y), pos(z) kills the decreasing pattern;
forbidding the increasing one forces pos(z) < pos(y) = the unit
z ≺ y.  Both directions check.  One presentational nit: (ii)'s APs
have y < z automatically (a < 2^m < y and a+z = 2y), used silently.

### 1.2 DIAG-DENSE (§2.1) and CROWN-2ADIC (§2.2)  [SOUND, one nit]

Counting re-derived: {3p, 3p+1} ⊆ B(m) ⟺ p ∈ (2^m/3, (2^{m+1}−1)/3],
a HALF-OPEN interval of length (2^m−1)/3; a half-open (a, a+ℓ]
contains ≥ ⌊ℓ/4⌋ members of any residue class mod 4.  NIT: the note
says "any real interval of length ℓ contains at least ⌊ℓ/4⌋" — false
for open intervals (e.g. (1,5) contains no p ≡ 1 mod 4); the applied
instance is half-open, so the lemma is fine, but the stated form
should say half-open.  Machine: brute counts at m ≤ 22 match the
bound (a8_bridge1_fresh.py part 1).  CROWN-2ADIC residues re-derived
and brute-checked j ≤ 30.

### 1.3 Theorem B1 (§3.1)  [SOUND modulo (H1), as tagged]

Chain re-derived: 2^{m₀} ≥ 12C₀+25 ⟹ N(m₀) ≥ C₀+1 disjoint pairs;
≤ C₀ dust punctures ≤ C₀ of them; survivor pair ⊆ T with
p > 2^{m₀}/3 ≥ 8 ⟹ p ≥ 9; PIN on 𝕄′ (infinite: only finitely many
scales dropped) gives cofinitely many consistent windows; (H1) at
m ≥ m*(p, C₀), |D_m| ≤ C₀ gives inconsistency everywhere on 𝕄′.
Contradiction correct.  The dependency accounting is honest: the
only inputs beyond the note are GAP-N2-DIAG (uniform p) and GAP-N3
(uniform C), both pre-existing; B1.2's unconditional route touches
only thm:c3core (p=5, C=0).  Machine checks §3 below add fresh-p
evidence for (H1) itself — the load-bearing open input.

### 1.4 §4.1–4.2 (dichotomy form, SPLIT-QUANT, B2-VAC)  [SOUND]

B2-VAC re-derived: branch (b) ⟹ dust ≥ N(m) ≥ (2^m−13)/12 > C₀ at
any clean scale with 2^m ≥ 12C₀+26 — one-shot, no order theory.
Machine: fresh hi-half splitter coloring (§3, χB) confirms the
counts at scales the author never used.

### 1.5 §4.3 (the descent/well-ordering analysis) — line by line

The historical failure point; scrutinized clause by clause.

* The splitter-adversary construction is well-defined and
  non-adaptive (a single fixed coloring; completions are in T
  automatically because T = complement of the planted lo halves).
* "T is Case-1, dust → 1/block": correct — both crown halves
  2^j−1, 2^j lie in the SAME block B(j−1), and only the lo half is
  planted; re-verified in χ3's dust counts and my χB analogue.
* Lemma LP(α)(β)(γ): all elementary claims re-derived; the (γ)
  four-case enumeration (u = 1, 0, −1, −2) checks; brute AP
  classification over 𝒞 ∪ {1} extended to 4096 (author: 512) —
  β family only (a8_bridge1_fresh.py part 4).
* Obstruction claim 1 (bounded-count families can be split while
  keeping T (b+1)-clean, dodging both branches): correct counting;
  re-derived.
* Obstruction claim 2 (the inheritance moves strictly up in scale,
  so no well-founded descent exists): the arithmetic input — the
  landing pad of a split pair at level j lives in B(j), above the
  pair — is LP(α) and is correct; given the fixed point, the
  conclusion that the planned induction has no base is right.

FINDINGS (both minor, neither load-bearing for B1 — §4.3 is
explicitly not used by §3):

* **(52-G1)** §4.3 bullet 3 states "NO fixed finite attacker cohort
  of either team ever fires an unsatisfiable per-window system."
  Literally false: χ3's OWN §6 check fires R(27,28; M, {2M−1})
  UNSAT with the cohort {27,28} ⊆ T.  The claim is true only for
  cohorts drawn from the finite usable family 𝒫₀ (the intended
  reading, clear from context).  The sentence needs the scoping
  clause; with it, the fixed point is genuine.
* **(52-G2)** §4.3 splitter item (ii) claims every fan completion
  is donated to T.  Corner case: the completion of a fan through a
  T′ lo half can itself be a planted lo half — exemplar at j = 4,
  x = 11: fan (11, 15, 19) with {11,12}, {15,16}, {19,20} all split
  lo-to-T′ puts the completion 19 in T′, and T′ ⊇ {11,13,15,17,19,21}
  contains several 3-APs ((11,13,15), (11,15,19), (13,17,21), …).
  Harmless — a sparse finite set with a few APs imposes only
  trivially satisfiable order constraints, and nothing in the dodge
  depends on T′ being AP-free — but "every completion is in T" and
  the LP(γ)-based "only the β chain" narrative are stated too
  broadly (LP(γ) is about the CROWN set; the catalogue lo halves
  add APs outside its scope).
* Scope note (not a gap, a reading instruction): the [PROVED] tag
  on §4.3 covers "the enumerated mechanism (per-window PIN kills
  through a finite usable list + landing-pad fans) admits a dodging
  coloring".  The broader "any BRIDGE1 argument MUST use an
  unbounded family" is informal meta-mathematics quantifying over
  arguments; as ledgered knowledge it is fine, as a theorem it is
  not one.  The note's own §4.3 wording ("more precisely: …") shows
  the author knows this; the headline sentence does not.

### 1.6 Fresh machine checks (a8_bridge1_fresh.py)  [details §3]

---

## 2. notes/57 (DICH) — reconstruction and case-tree logic

### 2.1 Lemma T (§1) as pure logic  [SOUND]

Exhaustive: no split ⟹ each parity class owned; owners differ (else
some |U| < 2 against the (2,2,2) bounds); hatch up to swap.  Φ ≥ 1 +
hatch ⟹ a same-parity U×Z pair on some side ⟹ D_A ∪ D_B ≠ ∅ (A's U
odd forces the pair odd, i.e. D_A; mirror).  Mutually exclusive by
definition.  Checks.

### 2.2 Forced-interval calculus (§2)  [SOUND; brute-verified]

FI re-derived from (u+z)/2 ∈ P1 ⟺ u ∈ [6M−30−z, 8M−z]; anchor value
(6M−30−z + z)/2 = 3M−15 exact; parity bookkeeping correct (6M−30
even).  Brute verification at M = 144 AND M = 176 (a scale no
session ever touched): every z, both parities — interval structure,
anchor ⟺ s ≤ M−31, ℓ formulas, ℓ ≥ 16, n_c ≥ 8 with equality only
at {+1}/{+2}/top-odd; A2 (f ≥ 9 for every 2-element D) at both
scales.  Zero exceptions (a8_dich_indep.py part A).
ANCHOR/COLL immediate.  H1's interval-intersection claims verified
EXHAUSTIVELY: for every pair (z_A odd, z_B even) with both offsets
≤ M−1, I(z_A) ∩ I(z_B) ≠ ∅ — checked at 48..176 (part C).  This
closes the one hand-wavy-looking paragraph in H1 ("… the two
intervals intersect …") by exhaustive machine sweep.

### 2.3 Theorem H-DICH case tree as pure logic  [SOUND given F0–F4]

Re-derived with attention to quantifier order:
* H0 uses F0 (purity) + fan-cleanness correctly: support ∩ D_A = ∅
  puts the whole pattern in B.  Valid.
* H1 needs BOTH minima ≤ M−1 — exactly F3's load-bearing half
  (machine, D5); given that, the three sub-cases (low/low, low/mid,
  mid/mid) are exhaustive and each yields a Y_A ∩ Y_B value; my
  part-C sweep proves the intersection claim outright at each
  audited scale, so H1 needs only F3.
* H2 preamble: D_B = ∅ ⟹ P2 evens ⊆ Z_A ⟹ Y_A ∩ E is a pure-alive
  clique.  Valid (uses F0 again).
* H2a counting: |Y_A| ≤ (m+8−f_O) + α_E.  The f-value logic is
  subtle and CORRECT: non-singleton D has f ≥ 9 by FI(iv) (which
  reduces to brute facts A + A2); the top-odd singleton is excluded
  because its minimum 2M+15 > M−1 is inadmissible (F3); the bottom
  singleton needs admissibility = self-service (H0), which is
  exactly F2's switch.  So min over admissible D is 8 iff F2 says
  YES, else 9 — the formula's f_c is the right constant.
* H2b = F4 (machine per scale).  Case coverage s₀ ≤ M−31 vs
  (M−31, M−1] exhaustive given F3.
* Assembly (§6): SPLIT by e154 per scale (+ my 144 run), HATCH by
  the above, Lemma T glues.  Valid.

Honest-accounting check: the note NEVER claims F0–F4 are proved
uniformly; the five sub-gaps of §7 are real and correctly scoped.
The one soft spot: §5's middle-staircase text is avowedly heuristic
("≈") and correctly excluded from the [PROVED] list; the m+22
extremal bound re-derived exactly (w₁ = m−14 (O) / m−15 (E), forced
mass ≥ m+23 > allowance m+14).

### 2.4 The K* formula — independent recomputation + blind test

a8_dich_indep.py (no code shared with e153_dich_lemmas.py or
a7_alpha_f.py; clique search and self-service scan rewritten from
the §0.2/§3 definitions):

* Catalogue shape at all 8 scales incl. 144/160: every blk-2
  pattern has exactly 2 band attackers, support ⊆ P2, no P0
  values.  F0 purity: TOTAL at every scale incl. 144 (6115/6115)
  and 160 (7440/7440 same-parity pairs) — eighth scale of the
  perfect record.
* α, f, K* at 48/64/80/96/112/128: reproduces the published tables
  EXACTLY (values + witnesses + F2 exemplars).
* M = 144: α_E = α_O = 3, f_O = f_E = 8 ⟹ K*(144) = 76, matching
  the notes/60 §5.1 blind record (independent third computation).
* M = 160 (catalogue landed this morning; NO α/f ever computed):
  **α_E = α_O = 2** (witnesses {−158, −94} / {−159, −95}; the
  gap-64 triples that work at 144 are dead at 160), f_O = f_E = 8
  ⟹ **K*(160) = 83 predicted by the mechanistic law** —
  DISAGREEING with both the notes/58 §6 flat-law pre-registration
  (84) and the notes/60 §5.0 trend expectation (α = 3 ⟹ 84).  This
  is a live discriminating experiment: probe K = 83 (mechanistic ⟹
  UNSAT, flat law ⟹ SAT).  Prediction committed BEFORE any 160
  probe, per the blind protocol.
* F3's load-bearing half at 144 and 160: exact D5-style scan (my
  own encoding) — every admissible defector minimum ≤ M−1.  [runs
  logged in data/a8_dich_indep.log]

### 2.5 The M = 144 measurement (blind-protocol completion)  [§3]

---

## 3. Machine verdicts (filled as runs land)

(placeholder — solver batteries run sequentially, one at a time)

---

## 4. Verdicts

(pending §3)
