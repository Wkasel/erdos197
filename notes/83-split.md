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

Known facts going in: at the ROT4-strength censor F = 64 the
corner tolerates ONLY lattices — HSPLIT (even mod-4-only) empties
it at hor = 2048 AND 4096 (e186 partHSPLIT, UNSAT ×3, ≤ 30 s);
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
