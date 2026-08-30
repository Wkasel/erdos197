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
