# 60 — Night-2 audit: adversarial verification of notes/52, 57, 58, 59 + assembly

Referee shift (2026-08-28).  Mandate: reconstruct the four night-shift
fronts' arguments independently, machine-check at scales the authors
did NOT use, complete the lost M = 160 endgame (the e146(160) build
was in flight at handoff and never landed — data/ has no
e146_catalogue_M160.json; the queued e152/e153/e154(160) probes and
e155c never ran), then update the ledgers.  A gap clears here only if
I would defend it as referee.

Written incrementally; every section ends with a verdict tag
[CONFIRMED] / [CONFIRMED WITH CORRECTION] / [REFUTED] / [NOT CHECKED].
Audit instruments live in audit/a7_night2/; new solver data in data/
with the e157+ prefix to avoid ordinal collisions.

## 0. Scope and inputs

Audited artifacts: notes/52 (BRIDGE1), notes/57 (GAP-DICH), notes/58
(GAP-LLOP/PARM + robust P-ARM), notes/59 (low gaps + Theorem ASM′),
against the proved layer of notes/55/56.  All night-shift logs in
data/ re-read and cross-checked against the notes' claims (e152_llop,
e153_dich_lemmas + _112_128, e153_dich_probes, e154_rparm,
e154_dich_split, e156_d3, e152_bridge1, e152_mc_schema, e153_j_pencil,
e154_deep_classify, e154b, e155_parm_hyp): NO discrepancy between any
note claim and its cited log found.  [CONFIRMED at the
bookkeeping level; substantive checks below.]

Planned checks (status filled in as sections land):

1. §1 Hand reconstruction, DICH front: Lemma T / FI / ANCHOR / COLL /
   H-DICH counting; K* formula arithmetic at all six measured scales.
2. §2 Hand reconstruction, LLOP/PARM front: Lemma AO / D3 (full range
   audit at fresh scales) / PH+ / PARM-HALVE bookkeeping / COV-W′
   composition.
3. §3 Hand reconstruction, LOWGAPS front: Lemma CC soundness, Γ₂′
   algebra, S6/JP/JP′ enumeration vs Lemma J's minimal sets,
   ASM′ composition logic.
4. §4 Hand reconstruction, BRIDGE1: PIN / DIAG-DENSE / CROWN-2ADIC /
   B1 counting / descent obstruction.
5. §5 NEW-SCALE machine tests: M = 144 (a scale NO session ever
   touched — blind test of the notes/57 mechanistic K* law AND the
   notes/58 flat-offset cap law, which DISAGREE with the dead mod-32
   law there), M = 160 (the pre-registered endgame: C = 84, K* = 84
   predicted), e156 D3 at 80/112, e155c (pre-registered ThW1′
   puncture-tolerance prediction), deep-classify resonance law at 64.
6. §6 Ledger updates + final inventory.

---

## 1. DICH front (notes/57)  [CONFIRMED — proved layer defended]

Independent reconstruction (no code shared with e153_dich_lemmas.py;
audit/a7_night2/a7_hand_checks.py sections A, D):

* **Lemma T**: re-derived; exhaustive and mutually exclusive under
  Φ ≥ 1 + bounds.  The SPLIT-side remark (Φ ≥ m+7 automatic) checks.
* **Lemma FI**: brute-forced at M = 112 AND at the untouched scale
  M = 144 — every formula exact (interval structure, anchor iff
  s ≤ M−31, ℓ formulas (s+31)/2 / (s+32)/2, ℓ = m in the middle zone,
  n_c ≥ 8 with equality only at bottom singletons {+1}/{+2} and the
  top odd singleton, and FI(iv): f_c(D) ≥ 9 for EVERY 2-element
  defector set, both classes).  Zero exceptions.
* **Lemma ANCHOR/COLL**: re-derived; the two-line collision at 3M−15
  is exactly the e152_dich_probe core (straddles (M+17, 3M−15, 4M+1),
  (M+16, 3M−15, 4M+2)).
* **Theorem H-DICH counting re-derived**: H2a gives |Y_A| ≤
  (m+8) − f_O + α_E; with K* := m + 9 + max(α_E−f_O, α_O−f_E) this is
  ≤ K* − 1 exactly.  H1's interval-intersection: low interval covers
  [3M−15, 3M] (ℓ ≥ 16 bottom-anchored), mid interval bottom
  3M−15+δ with δ = ⌈(s₀−M+31)/2⌉ ∈ [1, 15] ⟹ overlap with the low
  interval iff δ ≤ 15 (always), and two mid intervals have bottoms
  within 14 < m — both re-derived, sound.
* **The K* formula arithmetic**: recomputed from the logged
  (α_E, α_O, f_O, f_E) tables at all six scales — reproduces
  26/35/42/51/60/68 exactly, including the two different +1
  mechanisms at 64 (α_E = 3) and 96 (f = 8).
* Status tags in notes/57 are honest: F0–F4 correctly carried as
  per-scale machine facts, the case tree correctly conditional on
  them; the five sub-gaps are real and correctly speciated.

Verdict: the notes/57 [PROVED] layer stands as refereed; the
catalogue layer's blind-prediction claim at 112/128 is genuine (the
e153_dich_lemmas_112_128.log prediction lines carry "no e149 data"
and the notes/58 probes are a separate instrument).  §5 adds a THIRD
blind scale (144).

## 2. LLOP/PARM front (notes/58)  [CONFIRMED — D3 and PH+ defended]

* **Lemma AO**: classical even/odd recursion re-derived — a mono AP
  has same-parity endpoints; cross-parity midpoints are placed on the
  wrong side; induction on diameter.  Sound.
* **Lemma D3**: the entire proof re-derived step by step, then EVERY
  range inequality brute-forced at M = 48 and at the untouched
  M = 144 (section B of the audit script): the MID characterization
  PW(y) ∩ C ≠ ∅ ⟺ y ∈ [3M−14, (7M+14)/2] has zero exceptions; the
  punch window at ŷ ≥ y₀ lands in C′ with both parity candidates z₀
  inside P2; the descent value y′ = (u+z₀)/2 lands in P1 with
  3M−14 ≤ y′ < ŷ and y′ ≠ 3M−15 for EVERY (ŷ, u) — the Step-4
  contradiction fires unconditionally.  (Fine print: y′ ≥ 3M+8.5 at
  the extremes, so the note's "3M+8 ≤ y′" is safe.)  D3 is a genuine
  uniform coloring lemma; [PROVED] tag defended.
* **Lemma PH+**: class counts |P2 ∩ even| = M+7, |P2 ∩ odd| = M+8
  verified at 8 scales; the Φ = (M/2)·#defectors quantization
  re-derived (a defector meets a full P0 class of size M/2).
* **PARM-HALVE**: parity bookkeeping of (b)/(c) re-derived, incl.
  the no-support-caveat point ((1,2,2) completions of even pairs are
  even, hence hatch-owned) and the crown window CW = [3m−7, 3m−1]
  with 3m unreachable (c ≤ 3M−3 for odd a, b).
* **COV-W′ composition**: logic re-checked — the three machine
  instances quantify over supersets of the normalized coloring, swap
  invariance discharges both WLOGs.  Sound given the per-scale UNSAT
  verdicts (present for 128; 160 in §5).
* Honest-accounting check: the H-FG6/H-RW0 falsification and the
  §3.5 corrected P-ARM″ with GAP-PARM-CORNER match the e155/e155b
  logs; nothing is overclaimed.

## 3. LOWGAPS front (notes/59)  [CONFIRMED — Lemma J's upgrade to
## PROVED independently defended]

* **Lemma CC**: soundness re-derived from R1–R4 (RL = midpoint-leads,
  RT = midpoint-trails, T = transitivity of a linear order).
* **Independent closure engine** (fresh implementation, ~30 lines,
  sharing no code with e153_j_pencil.py): running it on all 36
  minimal forbidden sets of Lemma J reproduces EXACTLY the split
  29 pure-closure refutations / 7 stalls, with the stall set
  {(7,8), (8,9), (8,11), (5,10,12), (7,10,12), (9,10,12),
  (10,11,12)}; adding the logged totality splits closes ALL branches
  of all 7.  Lemma J's [PROVED] status is hereby independently
  re-established end-to-end.
* **JP/JP′**: the window enumeration {j′ ≥ 2j, 5j′−6j ≤ 15} ∪
  {2j′ ≥ 3j, 9j′−10j ≤ 15} yields exactly the nine pairs
  (1,2),(1,3),(1,4),(2,3),(2,4),(2,5),(3,5),(3,6),(4,6) — matching
  the nine 6-fact derivations in e153_j_pencil.log — and each
  instance's 6-fact derivation was re-validated as rule-applications
  (units present, b = 2a−t_A, c = 2b−t_B, window).
* **Γ₁/Γ₂′ affine identities**: full-sweep verification at M = 48 and
  144 (every admissible (q,p) resp. (q,a)): all displayed chain
  identities hold; windows correct.
* **Lemma FW rules (i)–(iii)**: re-derived as unit+RL+T compositions;
  sound.  Theorem AFF's affine bookkeeping checks.  The 0/165
  false-positive control at every coverage level is the right
  soundness discipline.
* **Theorem ASM′**: composition logic re-checked (same analysis as
  COV-W′; the (OV) reduction is correct).  The overlap table
  W = 4/2/3/1/0/0 recomputed from the measured K*/C values.
* e154 deep data re-read: R(48) gap histogram {8,16,24,32,40,48,56}
  all ≡ 0 (mod 8) — the resonance law claim is exactly what the log
  shows; D(48) q-range [48, 62] = E1×E1 confirmed.

## 4. BRIDGE1 (notes/52)  [CONFIRMED]

* **Lemma PIN** re-derived (finite prefix F, disjoint blocks, position
  order; unit direction z ≺ y forced exactly as claimed).
* **Theorem B1 counting**: (2^m−13)/12 ≥ C₀+1 ⟺ 2^m ≥ 12C₀+25;
  dust punctures ≤ C₀ of the ≥ C₀+1 disjoint pairs; p > 2^{m₀}/3 ≥ 8
  forces p ≥ 9 — all re-derived.  DIAG-DENSE brute-verified for
  m ≤ 20; CROWN-2ADIC residues brute-verified for j ≤ 20 (even j:
  p_j ≡ 5 (mod 8); odd j: 2^j−1 ≡ 7 (mod 8), 3 ∤).
* **The dependency claim audited**: B1 uses (H1) only through the
  quantifiers stated; B1.2's unconditional路线 (p = 5, C = 0 =
  thm:c3core) touches no open tag.  The "no new gap" ledger claim is
  correct: GAP-N2-DIAG + GAP-N3 are pre-existing.
* **§4.3 descent obstruction**: the splitter fixed point is a
  coherent counterexample schema and χ3 machine-realizes it; the
  conclusion (density necessary, no well-ordering) is sound and
  valuable negative knowledge.
* e152_bridge1 checks re-read: encodings complete (all transitivity
  triples), controls present (AP-only SAT, single-attacker SAT).
  One economy note: the χ1/χ3 kills at 128/256 use p = 9 — inside
  the machine-verified layer, as intended (they exercise (H1)'s
  robustness form, not the open parametric form).

