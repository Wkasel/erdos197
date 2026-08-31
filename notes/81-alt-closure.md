# 81-alt-closure — GAP-AFFORD″-ALT: the exterior machinery enters
# the corner (PIN is dust-free; the minority IS the dust)

Session 2026-08-30 (continuation of notes/80-pincer).  Mandate:
(1) execute the pre-registered S5 runs (R-scan at F = 64, ν-growth
at m = 64/128, the F12 run≥2 boundary cells at long budgets);
(2) the structural kill for unbounded runs (run-length threshold
R*); (3) puncture budgets for near-lattices; (4) the non-lattice
mixed catalogue; (5) assemble what closes.

Machine companion: experiments/e186_altclosure.py →
data/e186_altclosure.json / .log.  Pods: sprint-B/C/D + main for
the long cells.  This §0 is committed BEFORE any e186 run
(campaign rule).

## 0. Pre-flight: desk facts, instrument, predictions

**Desk facts (derived tonight before any run; proofs in §2):**

- (D1) **Lemma PIN is dust-free.**  Re-read of notes/52 §1.3: the
  proof of Lemma PIN never uses |D_m| ≤ C.  It needs only: T
  3-permutable, a₁ < a₂ ∈ T fixed, and S = B(m) ∩ T; the finite
  prefix F = {pos ≤ Q} meets only finitely many blocks; position
  order on S then satisfies (i) + (ii) verbatim.  So (PIN-Ω): for
  ANY team T and fixed pair a₁ < a₂ ∈ T, for all but finitely many
  m, R(a₁, a₂; 2^m, B(m) ∖ T) is consistent — the dust bound was
  only ever needed by the RUNG law, not the pigeonhole.
  Multi-pair form PIN-Ω-k (same proof, Q = max over the 2k
  positions): the window theory may take ANY fixed finite attacker
  menu ⊆ T.
- (D2) **The corner reduction.**  Axis (iii) says every block
  minority is gap-≥3.  The minority of block m IS the dust
  B(m) ∖ Y of the majority team Y there.  One team X owns the
  minority infinitely often (pigeonhole; under alternation both
  do); pigeonhole again onto one structure class.  So the fixed
  complement Y = X^c faces infinitely many windows whose theory is
  the STRUCTURALLY-PUNCTURED rung — punctures = the gap-≥3
  minority.  If those rungs are UNSAT, PIN-Ω kills Y.  **No run
  length is needed: R* = 1** — every X-owned block is a usable
  window for Y; bounded and unbounded runs, alternating or
  constant ownership, all inherit the same kill.  The
  pre-registered R*-dichotomy (notes/80 task shape) is superseded
  IF the punctured-rung law lands; if it does not land, the run
  interior is exactly a class-punctured rung and the dichotomy
  route dies with it (recorded either way).
- (D3) **The PS-dodge classes (from notes/78 II.2).**  For dyadic
  M ≡ 0 (mod 4): lane t-endpoints t_{x−2j} (j even) all lie in
  class −x (mod 4); b-endpoints b_j = M + j (j even) lie in the
  even classes {0, 2} (half each by j mod 4).  Hence for minority
  class c: (a) c ≡ −x (mod 4) ⟹ class-c contains a FULL lane
  transversal ⟹ Lemma PS + SA-half predicts the class-punctured
  rung R(x; M) ∖ class-c is SAT — attacker class −c is USELESS
  against a class-c lattice; (b) c even punctures exactly half
  the lane (the j ≡ c side); (c) c odd ≢ −x punctures NO lane
  endpoint.  Extraction of {x, x+1} ⊆ Y from a uniform class-c
  lattice forbids x ≡ c and x ≡ c−1 (mod 4).  Net per-class menu:
  c = 0 → x ≡ 1 (mod 4) (lanes = N2-COMPLETE species); c = 2 →
  x ≡ 3 (mod 4) (the PROVED diagonal C3(p), p ≡ 1 mod 4);
  c = 1 → only x ≡ 3 extractable and it is PS-DODGED; c = 3 →
  only x ≡ 1 extractable and it is PS-DODGED.  The odd minority
  classes are the resistant ones — and the realized corner
  (pureL3, the S5 witnesses) sits at c = 3.  For c odd the
  single-pair route dies by design and the JOINT menu (PIN-Ω-k)
  is the escalation: the PS split's residual is then a
  MULTI-even-attacker half-window system, satisfiability unknown
  ("singles always SAT" does not extend) — machine decides.
- (D4) **Puncture monotonicity (PUNCT-MONO).**  D′ ⊆ D ⟹ any
  valid order of (M, 2M] ∖ D′ restricts to one of (M, 2M] ∖ D
  (constraints on the smaller survivor set are a subset), so
  R ∖ D UNSAT ⟹ R ∖ D′ UNSAT.  Consequence: UNSAT at the FULL
  class-c puncture kills every sub-puncture — a punctured
  near-lattice (minority ⊊ class c) inherits the kill with NO
  budget counting; the N3-GROW budget instrument is needed only
  for OFF-class deviations (handled as ≤ C extra punctures,
  partROB).
- (D5) **Supply survives sparsity.**  Disjoint consecutive pairs
  {2k+1, 2k+2} in a block number M/2; a gap-≥3 dust set has
  ≤ ⌈M/3⌉ values and kills ≤ 1 disjoint pair each: ≥ M/6 − 2
  pairs fully in Y in EVERY window — linear usable supply, so the
  splitter adversary of notes/52 §4.3 cannot starve the menu.
  For lattices: c ∈ {1, 2} keeps every diagonal pair (classes
  {3, 0}); c ∈ {0, 3} keeps every x ≡ 1 (mod 4) pair (classes
  {1, 2}).
- (D6) **The known SAT escape is in the record**: d*(27; 112) = 6
  via the MIXED transversal {b₂, b₈, b₁₂, t₁₉, t₁₅, t₇} = values
  {114, 120, 124, 205, 209, 217} — all gaps ≥ 3.  So the bare law
  "every gap-≥3 puncture set leaves the single-pair rung UNSAT"
  is ALREADY FALSE.  The corner question is therefore the JOINT
  form: can one gap-≥3 set dodge a 2–3-pair menu simultaneously
  (and, for lattices, can a residue class do it) — this is what
  the instrument asks.

**Instrument (e186_altclosure.py), parts:**

- partLATRUNG: R(x; M) ∖ (class-c ∩ (M, 2M]) — full rung of the
  pair {x, x+1}, guarded units, complete transitivity encoding —
  for x ∈ {15, 17, 25, 27} × c ∈ {0, 1, 2, 3} × M ∈ {128, 256}
  (512 on pods), plus D = ∅ controls.
- partJOINT: the 2-pair menus under full class punctures:
  {15, 27} vs c ∈ {1, 2}; {17, 25} vs c ∈ {3, 0}; same M grid.
- partSPARSE: existential punctures — membership vars, D free
  subject only to gap-≥3 (pairwise distance ≥ 3 within D), joint
  menu fired: is ANY sparse minority consistent with the menu
  rung?  Positive control first: single pair x = 27, M = 112 must
  be SAT (D6).  Menus at M ∈ {64, 96, 128}.
- partROB: where partLATRUNG is UNSAT: class-c plus existential
  ≤ C extra off-class punctures, C ∈ {4, 8} — the off-class
  deviation budget for near-lattices.
- partRSCAN (pre-registered, notes/80 §4.5): S5-ALT at F = 64
  censor, maxrun R = 3, 4, 5, budget 4 h each (pods).
- partF12 (pre-registered): the undecided F = 12 run ≤ 2 / ≤ 3
  cells at 6 h budgets (pods).
- partNUGROW (pre-registered): ν-scan on the alternating witness
  (e185 censor-off coloring) at m = 64, budgets {12, 16, 24, 32};
  pure lattice m = 32 frontier push toward the predicted ≈ 230.

**Predictions (committed before any run):**

- P-1. partLATRUNG: SAT at every PS-dodge cell c ≡ −x (mod 4)
  (85 %); UNSAT at c even (70 %) and at c odd ≢ −x (75 %);
  D = ∅ controls UNSAT wherever M ≥ x + 57 or in-flip-class per
  C3(p).
- P-2. partJOINT: genuinely uncertain; lean UNSAT 55 % even in
  the PS-dodge classes (the halved residual is multi-attacker).
  If UNSAT at 2+ scales for both menus: EVERY uniform-class
  lattice has a dead majority team modulo the schema layer — the
  entire lattice corner (any ownership sequence) closes at the
  machine level.
- P-3. partSPARSE: control (27, 112) SAT (95 % — D6 is a
  certificate); joint menus lean UNSAT 55 %.  UNSAT ⟹ no gap-≥3
  minority whatever dodges a fixed 2-pair menu at that scale —
  the non-lattice corner kill's machine layer.
- P-4. partROB: UNSAT persists at C ≤ 8 where the base cell is
  UNSAT (70 %).
- P-5. partRSCAN: R = 3 UNSAT 60 %; R = 4/5 undecided-risk high
  (timeouts count as boundary data, recorded as such).
- P-6. partF12: run ≤ 2 at 6 h: 50/50.  SAT would be the first
  bounded-run alternating inhabitant (audit its H-census); UNSAT
  extends the bounded-run UNSAT regime to the weak censor.
- P-7. partNUGROW: alternating witness m = 64 both teams UNSAT
  through 32 (80 %); pureL3 m = 32 minority frontier lands in
  [180, 280] if the scan completes (else lower bound recorded).

Survival protocol: §1 machine harvest; §2 the kill assembled by
hand (whatever survives); §3 near-lattices + non-lattice; §4 the
pre-registered S5 rows; §5 ledger + assembly.  Honest tags
throughout; SAT rows are structure, not failure.

---

## 1. SUPERSEDED MID-SESSION by notes/82 (professor pass) — and
## the §0 instrument's data is the measured COMPLEMENT of the kill

Between §0 and the first harvest, notes/82 landed Lemma Q +
Theorem ALT-DEAD: the mod-4 lattice corner (ANY ownership law) and
all on-class punctured variants are dead by a one-step 4-adic
chart onto the PROVED Case-1 chain (PIN + DIAG-DENSE + C3(p)).
The §0 siege (run scans, ν-growth, F12 boundary, puncture budgets)
stands down as pre-registered next steps — moot at ω.  Pod jobs
killed (rscan/f12 after launch, nugrow unstarted); partial rows,
if any, are not read as mathematics.

**What the §0 grid measured before standing down (e186 partLATRUNG
/ partJOINT / partSPARSE, all rows in data/e186_altclosure.json)
— kept as the measured complement:**

| instrument | verdict |
|---|---|
| single-pair rung ∖ class-c, M = 256, x ∈ {15,17,25,27} × c ∈ {0..3} | UNSAT ONLY where an attacker sits ON class c (unextractable cells); every EXTRACTABLE cell SAT |
| 2-pair menus ∖ class-c, M = 128/256 | same law exactly: UNSAT ⟺ menu touches c |
| existential gap-≥3 punctures vs 2-pair menus, M = 64..128 | SAT everywhere (D ≈ M/4, min-gap 3, mixed classes) |
| PS-dodge prediction (§0 D3) | confirmed where it applied (c ≡ −x cells SAT); the c-even/odd-alive UNSAT leans were WRONG at extractable cells |

Reading: **the majority team of a sparse-minority window cannot be
killed through its own punctured rung** — the corner's gap-≥3 dust
severs every rung the majority would actually face (P-1/P-2/P-3
falsified in the informative direction).  This is the instrument-
level confirmation of notes/82 §1's verdict that the direct/siege
attack fails, and of WHY the kill must route through the MINORITY
class-section (Lemma Q's chart) instead: the minority's own
material is the only window content that cannot dodge.  The
scale-flip rows (several cells SAT at M = 128, UNSAT at 256) and
the exact touch-the-class law are recorded as structure for the
Q-ODD/N2-UNIF write-ups.

## 2. Machine spot-checks of Lemma Q / ALT-DEAD [all checks pass
## at the tested instances] + the notes/82 machine errand

[Language aligned per notes/88 item 8: these are finite
REGRESSION-style checks of the machine-checkable shadows of the
proof's layers at the stated instances/scales — consistency
evidence, not a universal verification of the proofs.]

partQVERIFY (e186; the machine-checkable shadow of each notes/82
§2 proof layer exercised at the stated instances):

1. **Chart exactness**: φ(Λ_c(t)) = B(t−2) as EXACT sets — 44/44
   cells (c ∈ {0..3}, t = 4..14), 0 fail.  Both endpoint
   conventions (c = 0 vs c ∈ {1,2,3}) verified.
2. **AP transport**: 44 400 triples exhaustive on [1, 600]: 3-APs
   map to 3-APs under φ and pull back under φ⁻¹ with midpoint
   automatically in class c — 0 fail, both directions.
3. **C3(p) ⊆ R fired-unit membership** (the a-fortiori step):
   the three C3(p) units are among R(3p, 3p+1; M, ∅)'s fired
   units at p = 5, 9, 13 × M = 128, 256 — 6/6, 0 fail.
4. **Rung UNSAT direct**: R(39, 40; 128, ∅) UNSAT (p = 13 fresh);
   R(15,16)/R(27,28) at M = 128 AND 256 already UNSAT as §1's ctl
   rows — three C3(p) lanes solver-confirmed in this session's
   fresh encoder.
5. **Witness 4-purity + transported clean blocks**: h8192_F64
   4-pure at ALL 8 classes×blocks scales; h4096_F64 pure at
   t = 5, 7–11 (t = 6 boot-contaminated, n_pure = 2); lin4 pure
   from t = 7; pureL3 everywhere.  Transported image contains the
   predicted CLEAN blocks (checked exactly at the top two pure
   scales per witness — 8/8 True).  The finite shadow of ALT-DEAD
   is exactly realized on every S5 witness.
6. **Geneson Λ-scan (the free adversarial audit of the proved
   layer)**: Geneson's density-2/3 permutable W contains a full
   class-section Λ_c(t) ONLY at t = 2 and t = 4 (boot octaves);
   ZERO hits for t = 5..200, any c.  Lemma Q predicts finiteness;
   the sharpest permutable set known complies with ~196 scales to
   spare.  No indictment of B1/C3(p).

**One genuine adversarial finding (structure, not a flaw):** the
alternating CENSOR-OFF coloring (e185 altw, nA = 1703) is NOT
4-pure — every class-section is bichromatic at every t ≥ 6
(n_pure = 0).  So ALT-DEAD does not touch it; it was never a
corner-certified inhabitant (censor off), but it shows alternating
(ii)+(iii)+split colorings need not be lattices — the
GAP-AFFORD‴-SPLIT residue is a real, inhabited-as-COLORING class,
and the professor's residue table is honest.  Verification
verdict: **no inconsistency found — every machine-checkable shadow
passes at the tested instances, and the restriction/transport
steps (order-type, position-preservation, midpoint-class,
B1₀ threshold arithmetic) were re-derived by hand.**  This is
supporting evidence for Lemma Q + ALT-DEAD, not a proof audit of
universal scope: the checks are finite spot checks (e.g. chart
exactness at t = 4..14, transport on [1, 600], two witnesses' top
scales), and soundness of the theorems rests on the hand proofs.

**HSPLIT build pre-registration (the errand's part (c); committed
before the run):** e179 s5dodger axes verbatim + Cor. HSPLIT as a
constraint (every class mod 4 AND mod 8 bichromatic in every
block t ≥ 6), hor = 4096, D = 2, cells: (F = 12, u₀ = 32),
(F = 64, u₀ = 64), + mod-4-only attribution control at F = 12.
Predictions: F = 12 SAT 55 % (HSPLIT bans the lattice shape the
solver always chose, but is mild — few clauses per block; the
(i)/(iii) tension of notes/74 §II.4 was resolved BY orbit-closed
lattice minorities, so banning them may re-expose it); F = 64 SAT
35 %; mod-4-only ≥ k8 rate.  SAT ⟹ first certified inhabitant of
the SPLIT residue (audit gap structure + purity + H-census);
UNSAT ×2 censors ⟹ the residue is finitely EMPTY at ROT4 strength
— the entire corner would then be machine-rejected at the finite
level while ω-dead on every arithmetic sub-family: probability
moves accordingly.  [CORRECTION, review remediation notes/88 item
1: the UNSAT reading in this pre-registration was overdrawn — an
UNSAT here shows only that every finite inhabitant of the corner
axes at these parameters carries ≥ 1 monochromatic class-section
within the tested horizon; it does not machine-reject the corner
and licenses no ω conclusion.  See the corrected §3.]

## 3. HSPLIT battery — the SPLIT residue's first instrument

Attribution baseline established WITHOUT a run: the e185
censor-off alternating coloring (altw) satisfies the FULL HSPLIT
constraint (every mod-4 AND mod-8 class-section bichromatic at
every t ≥ 6 — machine-checked, 0 monochromatic sections).  So
HSPLIT-generic corner COLORINGS exist; the build tests whether
the orbit censor tolerates them.

| cell (hor 4096, D = 2, lin4, split floor) | verdict | secs |
|---|---|---|
| F = 64, u₀ = 64, HSPLIT mod 4+8 | **UNSAT** | 30 |
| F = 64, hor = 2048 (scale control) | **UNSAT** | 13 |
| F = 64, mod-4-only HSPLIT (attribution) | **UNSAT** | 28 |
| F = 12, u₀ = 32, HSPLIT mod 4+8 | TIMEOUT (undecided) | 7200 |
| F = 12, mod-4-only (attribution) | TIMEOUT (undecided) | 7200 |

Reading (F = 64 rows), **as corrected by the external review
(notes/88 item 1; the original reading below is RETRACTED)**: the
UNSAT cells prove exactly this — **every finite strong-censor
corner inhabitant on [1, hor], hor ∈ {2048, 4096}, has at least
one monochromatic residue-class section (mod 4 already suffices)
at some tested scale 6 ≤ t ≤ t_max** — the un-HSPLIT build was SAT
at exactly these parameters (e179: 45 s, witness = mod-4 lattice),
so full bichromaticity is what the censor refuses, not the corner
axes themselves.

**RETRACTED (invalid inference, original text of this section):**
"the corner tolerates NOTHING but lattices … the strong-censor
corner is now dead END TO END: finitely, every inhabitant is a
lattice; at ω, every lattice is invalid."  One monochromatic
section is not a lattice, and there is NO compactness step from
these cells to ω: an ω-inhabitant that is 4-pure at finitely many
scales only (e.g. only at t ≤ 11) is consistent with every tested
cell, and ALT-DEAD (which needs INFINITELY many 4-pure scales)
does not touch it.  What the end-to-end kill would need is the
open *shifted-window uniform infeasibility* statement: for EVERY
T ≥ 6, no corner model with all class-sections bichromatic at all
scales ≥ T.  Only the T = 6 instance was run.  ALT-DEAD itself —
the conditional theorem "infinitely many 4-pure scales ⟹ not a
valid pair" — is UNAFFECTED and stands [PROVED]; its
applicability hypothesis on this corner is explicitly OPEN.  The
weak-censor cells decide whether GAP-AFFORD‴-SPLIT has ANY finite
inhabitant at these horizons — nothing more.

## 4. Close-out (weak-censor rows landed; front hands off)

The F = 12 cells ran their full 7200 s budgets on pods main and
sprint-D and returned **TIMEOUT — genuinely undecided**, at BOTH
HSPLIT strengths (mod 4+8 and mod-4-only).  This matches the e185
partS5ALT weak-censor boundary exactly (the F = 12 run ≥ 2 cells
timed out there too): F = 12 sits at the solver's decision
frontier for every corner-family variant tried.  Recorded as
boundary data, no verdict claimed in either direction; the cells
are duplicated (independent replication, longer budgets) in the
notes/83 C1/C2 program, which owns the weak-censor follow-up.

Final state of this front (everything else is in notes/82/88/89):

- Lemma Q / ALT-DEAD / HSPLIT: verified adversarially (§2, ALL
  PASS incl. the Geneson Λ-scan 0/196 scales) — [PROVED], with
  the applicability hypothesis on the SPLIT corner explicitly
  OPEN (notes/89 §5).
- Machine record: data/e186_altclosure.json — partQVERIFY,
  partGENESON, partLATRUNG/JOINT/SPARSE (the measured complement:
  exact touch-the-class law; majority-side punctured-rung siege
  provably void), partHSPLIT (7 rows: UNSAT ×3 at F = 64 per the
  corrected §3 reading; TIMEOUT ×2 at F = 12; + altw
  HSPLIT-compatibility).
- Residue: GAP-AFFORD‴-SPLIT, owned by notes/83; probability held
  at the notes/88-remediated NO ≈ 95 % (the F = 12 TIMEOUTs are
  boundary rows, not movement).
