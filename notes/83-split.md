# 83-split — FRONT SPLIT-RESIDUE: GAP-AFFORD‴-SPLIT, the last
# Case-2 residue (inhabitant hunt + gap-g descent)

Session 2026-08-30 (continuation of notes/81 §3 / notes/82 §5).
Mandate: (1) finish the weak-censor HSPLIT battery — the F = 12
cells notes/81 pre-registered and lost when the pods were killed;
UNSAT ⟹ the residue has NO finite inhabitant at weak-censor
strength (state the exact closure that follows, honest tags);
SAT ⟹ first certified inhabitant — audit it and run the descent
trick ON IT (gap-g chart, Lemma Q generalized to gap g);
(2) either way, exact statement of what remains of Case 2.

## 0. Pre-flight: the residue, the instrument, cells, predictions

**The residue (notes/82 §5).**  GAP-AFFORD‴-SPLIT = supply cap for
2-adically split gap-≥3 minorities: colorings that are
(a) everywhere-split with floor f(t) = max(2, t−5);
(b) window-diffuse (each team ≥ 1/4 of every ratio-2 window
(a, 2a], a ≥ 32);
(c) per-block minority pair-sparse — all minority gaps ≥ 3
(notes/46 §5 axis (iii) verbatim);
(d) HSPLIT-compatible — every class mod 4 AND mod 8 bichromatic
in every block t ≥ 6 (Cor. HSPLIT is a PROVED necessary condition
at ω; imposing it finitely bans exactly the lattice shapes
ALT-DEAD already kills);
(e) orbit-censored (subcriticality proxy): no in-team doubling
chain of depth ≥ D = 2 with reflectors ≤ F, seed > u₀.

Known facts going in [corrected per notes/88 item 1]: at the
ROT4-strength censor F = 64, e186 partHSPLIT is UNSAT ×3 (≤ 30 s;
hor = 2048 AND 4096, mod-4-only included) — i.e. every finite
corner inhabitant there carries ≥ 1 monochromatic class-section
within the tested horizon (NOT "tolerates only lattices", and no
ω conclusion follows — see the notes/81 §3 retraction);
the censor-off alternating coloring altw IS fully
HSPLIT-compatible (0 mono sections at t ≥ 6), so the coloring
class (a)–(d) is inhabited — the question is whether it coexists
with ANY orbit censor.  The e179 un-HSPLIT builds were SAT at
BOTH F = 12 and F = 64 (witnesses = mod-4 lattices, now dead
at ω).

**Instrument.**  e186.partHSPLIT unchanged (committed, audited
encoding: split floor + reified minority gap-≥3 + HSPLIT sections
+ prefix-sum window floor + reach-var censor, forcing implications
only — sound for UNSAT on the censor side, and SAT witnesses are
independently auditable colorings).  Driver
experiments/e187_split_hunt.py (parametrized cells; rows merge
into data/e186_altclosure.json partHSPLIT as pre-registered).

**Cells (this session):**

| cell | hor | F | u₀ | HSPLIT mods | where |
|---|---|---|---|---|---|
| C1 main | 4096 | 12 | 32 | 4+8 | local |
| C2 attribution | 4096 | 12 | 32 | 4 only | pod |
| C3 scale control | 2048 | 12 | 32 | 4+8 | pod |
| C4 escalation (if C1 SAT) | 8192 | 12 | 32 | 4+8 | pod |
| C5 escalation (if C1 UNSAT) | 4096 | 6 | 16 | 4+8 | pod |

Budgets 7200 s each (2× the notes/81 registration; these are the
decisive cells and the fleet is idle).

**Predictions (committed before any run; notes/81 §2 said F = 12
SAT 55 % — retained):**

- P-1. C1 SAT 55 %.  The F = 12 censor is 5× weaker than the
  F = 64 one that needed lattices; the (i)/(iii) tension of
  notes/74 §II.4 was resolved BY lattice minorities, and HSPLIT
  bans those — but at F = 12 the censor fires on far fewer
  triples, and altw-style aperiodic minorities may thread it.
- P-2. C2 verdict = C1 verdict (85 %) — mod-8 sections are few
  clauses; attribution should show mod-4 already decides.
- P-3. C3 = C1 verdict at half horizon (80 %).
- P-4. If C1 SAT: the witness minority is NOT eventually-periodic
  mod any 2^k (forced by HSPLIT), and I predict (70 %) its
  in-block gap multiset concentrates on {3, 4, 5} with NO single
  dominant gap g on long runs — i.e. it will dodge the gap-g
  chart too, and the descent arm will need the interval-system
  form of Lemma Q, not the verbatim one.
- P-5. If C1 UNSAT: honest reading is "the SPLIT residue has no
  finite inhabitant at weak-censor strength on [1, 4096]" — NOT
  an ω-emptiness theorem by itself (the D = 2 censor is a proxy,
  not a proved necessary condition; a valid ω-pair may contain
  depth-2 chains).  The closure statement it DOES license is
  drafted in §0b below, so the tag discipline is fixed before the
  verdict is known.

**§0b — what each verdict yields (drafted blind):**

- UNSAT ×(C1,C2,C3): Theorem SPLIT-EMPTY(F) [MACHINE-CHECKED]:
  no 2-coloring of [1, hor] satisfies (a)–(e) at F ∈ {12, 64}.
  Combined with ALT-DEAD/HSPLIT [PROVED]: every finite
  inhabitant of the corner axioms (a)+(b)+(c)+(e) at these
  censors is a mod-2^k near-lattice, and every such coloring is
  dead at ω.  Case 2 then rests ONLY on colorings that defeat
  every finite orbit censor tried — supercritical-looking at
  every finite depth — while keeping (a)–(d); the residue
  statement sharpens to that class ([GAP], exact wording in §3).
  CASE2-DEAD is NOT claimable from this alone; it needs the
  censor to be replaced by a proved necessary condition
  (L-CASCADE species) — recorded as the honest gap.
- SAT (C1): first certified inhabitant of the SPLIT residue.
  Audit battery: (i) exact re-verification of every axiom on the
  witness (independent checker, no CP-SAT); (ii) minority gap
  census per block + purity at mods 4/8/16/32; (iii) doubling
  H-census (which reflectors/depths appear at F′ > 12);
  (iv) window minority profile ν(a); (v) THE DESCENT: mine the
  minority for maximal gap-g AP runs, chart each by
  φ(x) = (x − c + g)/g, test whether the image contains dyadic
  blocks / interval systems in dead territory (B1 at C₀,
  RUNG-IN interval rungs, CORE′) — the Lemma-Q move at gap g.
  Descent verdicts recorded per run; a witness ALL of whose
  long runs chart into dead territory is YES-material that
  self-destructs at ω — that would be the strongest possible
  outcome short of emptiness.

Survival protocol: §1 harvest; §2 witness anatomy / emptiness
assembly; §3 the exact residue statement + ledger.  Honest tags
throughout.

---

## 1. Harvest (weak-censor HSPLIT battery)

(cells in flight; table filled as rows land — checker calibration
below done while waiting)

**Checker calibration (e187b on altw, the censor-off coloring):**
the independent auditor (no CP-SAT) reports EXACTLY the expected
profile — censor violations only (15 322 depth-2 chains at F = 12:
altw is deep in supercritical territory), all other axioms pass:
split floor ✓, minority gap-≥3 ✓ (ownership ALTERNATES B,B,A,B,…),
window floor ✓ (ν(a) = a/4 at the floor from a = 256 up), HSPLIT
mods 4+8 ✓ (0 mono sections, matching e186's compat record) — and
the anatomy is P-4's predicted shape verbatim: gap multiset
concentrated on {3, 4, 5} (mod-6 profile mixed), longest fixed-gap
run ≤ 8 out of minority 512 at t = 11, descent miner finds NO
recurring one-team class section at any modulus 2..12 (sporadic
hits at 7/10/11/12 only, ≤ 2 each, non-recurring).  So the
COLORING class dodges the gap-g descent by construction — the
whole question is whether any of it coexists with the censor.
data/e187b_audit_e185_s5alt_h4096_F12_r1_noorb_a6.json.

---

## 2. The gap-g descent: Lemma Q-g and Corollary ASPLIT (desk,
## verdict-independent)

Notation: for g ≥ 2, c ∈ {0..g−1}, let Λ^g_c(t) = {v ∈ B(t) :
v ≡ c (mod g)} and φ_g(x) = (x − c)/g + 1, the increasing affine
bijection (c + gℤ) → ℤ⁺-tail.

**Chart facts [MACHINE-CHECKED this session, §1 desk rows]:**
φ_g(Λ^g_c(t)) is an INTERVAL of length 2^t/g ± 1 = a ratio-2
window (M_t, 2M_t] with ≤ 1 value of dust at each end,
M_t = ⌊(2^t − c)/g⌋ ± 1.  For g = 2^k: exactly B(t−k), zero dust
(Cor. HSPLIT's case).  Anchor residues mod 8 CYCLE with t: g = 3
alternates 5, 2 (the CROWN-2ADIC identity (4^k−1)/3 ≡ 5 confirmed);
g = 5 cycles (3, 6, 4, 1); g = 7 cycles (4, 1, 2); g = 6, 12
reindex the g = 3 law.  Every anchor class is hit cofinally.

**Lemma Q-g.**  No 3-permutable set contains Λ^g_c(t) for one
fixed (g, c) and infinitely many t.
[g = 2^k: PROVED — Lemma Q verbatim at k′ = k, C3(p) prose rider
only.  g with odd part: stated, PROVED mod BRIDGE1-AF +
GAP-N2-UNIF + GAP-N3-GROW at C = 2 — exactly Cor. Q-ODD's gates,
now for ALL g, not just odd g.]

*Proof shape.*  Steps (i)–(ii) of Lemma Q are modulus-agnostic:
restriction of the arrangement to T ∩ (c + gℤ) preserves order
type and monotone 3-APs; φ_g transports 3-APs both ways (affine),
pulled-back midpoints land in class c automatically.  The image
S′ then contains, at infinitely many t, ratio-2 windows
(M_t, 2M_t] clean up to C₀ ≤ 2 end dust.  g = 2^k: the windows
are 0-dust dyadic blocks — B1 at C₀ = 0 (PIN + DIAG-DENSE +
C3(p)), done.  General g: non-dyadic anchors — the anchor-free
Case-1 assembly (BRIDGE1-AF species) + all-residue pair rungs
(N2-COMPLETE: every odd pair {x, x+1}, x ≥ 11, fires at ALL 8
residues, M ≥ x + 57) + dust robustness (N3-GROW at C = 2 for the
seam dust) kill S′; the cycling anchor residues cannot escape a
law that covers all 8.  ∎-shape; the odd-part tags are the gates
above, no new species.

**Corollary ASPLIT (all-modulus hereditary splitness; same
tags).**  For every valid pair, every m ≥ 2 and c mod m, the
section (c + mℤ) ∩ B(t) is bichromatic for all but finitely
many t.  *Proof.*  2m cells (c, team); infinitely many
monochromatic scales pigeonhole onto one cell; Lemma Q-g kills
that team.  ∎

**What ASPLIT does to the residue (the sharpening):**

1. Every eventually-periodic minority dies at EVERY modulus, not
   just 2^k — and both containment directions die: minority ⊇
   Λ^q_c(t) infinitely often kills the minority's team (Q-g
   direct); minority ⊆ Λ^q_c(t) (on-class punctured mod-q
   lattice) kills the MAJORITY (the other q−1 classes are pure —
   ALT-DEAD Cor.-2 argument at modulus q).  The "spacing-3
   minority" of notes/82 §2.3 is the special case q = 3.
2. Hence the surviving minority must, for EVERY m, in cofinitely
   many blocks, TOUCH every class mod m and MISS ≥ 1 value of
   every class mod m: totally aperiodic, m-adically generic for
   all m — not merely 2-adically split.  (Touching all classes
   mod m needs minority size ≥ m: consistent with the diverging
   split floor, but it pins the floor's ROLE — a slow-divergence
   inhabitant has LESS room, not more, against large-m ASPLIT.)
3. The reach boundary is honest and sharp: Q-g needs co-full
   class sections (clean blocks in the image).  Fixed-gap runs of
   length εM/g that do NOT exhaust their section chart onto
   positive-density subsets of the image window — N5 territory,
   ρ* → 1, REFUTED as a kill.  So the descent kills every
   arithmetic (periodic-pattern) shape and NOTHING diffuse: the
   gap-≥3 minority that mixes gaps {3, 4, 5} aperiodically
   (altw's measured shape, P-4) is untouchable by any chart in
   this family.  The (1b) geometry lesson repeats one level up.

**Ledger effect:** GAP-AFFORD‴-SPLIT's inhabitant must now be
m-adically split for ALL m (mod the Q-ODD gates) — rename residue
axis (d) from HSPLIT-compatible to ASPLIT-compatible at ω.  The
finite instrument keeps mods 4+8 (imposing all m finitely is
neither possible nor needed: ASPLIT is the ω-law that kills
whatever periodic structure a finite witness would extrapolate
to).
