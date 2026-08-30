# Master assembly: the complete NO — FINAL dependency graph
# (rewritten 2026-08-30 end-of-day, post five-front merge + notes/76 audit;
# adjudication pass applied same night — notes/80: six-species spot-audit
# clean, champion = S4/MINT-LOC, S5 witnesses = mod-4 lattice colorings;
# supersedes all earlier versions of this file — history in git)

Target: **Theorem (conditional assembly).**  No partition of ℤ⁺ into two
sets has both parts 3-permutable — Erdős #197 = NO — modulo the tagged
gaps of §6.  This document is the authoritative dependency graph: every
node is tagged

    [PROVED]   hand proof, written, audit-cleared where audited
    [MACHINE+SCHEMA]  machine-locked at the stated scales/lattice WITH a
               verified per-instance schema; uniform write-up pending
               (the tag names the write-up gap)
    [MACHINE]  machine-true at stated scales, no schema layer yet
    [GAP-*]    unproven link (exact statement + species in §6)

**Verdict up front: the NO-proof is NOT complete.**  Both kill chains
are structurally closed, machine-locked, and twice audit-cleared, but
the graph still contains genuinely open links.  The two that carry the
program: [GAP-AFFORD′] (Case 2's terminal supply statement — new
mathematics; champion route S4 + MINT-LOC after the notes/79/80
tournament + adjudication) and the uniformization pool (finite
catalogue/classification write-ups of one proved-in-instances species:
GAP-N3-GROW's (N3-b), the GAP-N6a sub-pool residue led by GAP-RES,
GAP-CMIN; GAP-N2-DIAG left this pool 2026-08-30 late — Theorem C3(p),
notes/78, [PROVED — spot-audited notes/80]).  No announcement-shape
document exists or should.

---

## 0. The frame (N4) [PROVED]

Fix a partition (A, B).  Over dyadic blocks (anchor-free per e121):

- **Case 1**: some team has infinitely many C₀-clean blocks (its
  in-block complement ≤ C₀), for some constant C₀.
- **Case 2**: both teams' in-block presence diverges (everywhere-split).

Exactly one holds (notes/43 §2, notes/46 §4A).  Composition across
scales is window-local + pigeonhole [PROVED, trivial].

Direct support (independent of both chains): lem:orbit [PROVED,
paper] kills doubling-supercritical teams; T-SHARP [PROVED, notes/39]
shows orbit growth hypotheses cannot replace finiteness (no shortcut).
The canonical partition and every block-granular/octave/stage shape is
already dead unconditionally or modulo the Case-1 rungs (thm:main
[PROVED, paper]; notes/35-43).

## 1. Case-1 kill chain

    N1 (T-PIN)  ──►  B1 (bridge)  ──►  rung family {C3(p), punctured}
    [PROVED]         [PROVED mod H1′]   [MACHINE+SCHEMA mod N2-DIAG, N3-GROW]

| node | statement | tag | certificates |
|------|-----------|-----|--------------|
| N1 / T-PIN(-STAGE/-BLOCKS) | fixed pair + infinitely many disjoint UNSAT windows ⟹ not permutable | [PROVED] | notes/37/42/43; thm:ogred verbatim |
| Theorem B1 | a team with ∞ many C₀-clean blocks is not 3-permutable, NO partner hypothesis; Step-1 patched to extract pairs with 3p ≥ x₀(C₀) = 4C₀+6 | [PROVED mod (H1′)] | notes/52 + patch notes/74 §I.4; audit-cleared (60-audit §4, 60-audit-1 §1/§3); adversarial colorings incl. fresh p=21 |
| (H1′) part 1 = GAP-N2-DIAG | the diagonal rung C3(p) = {t_p≺b_p, t_{p−2}≺b_{p+1}, t_{p+5}≺b_{p−2}} UNSAT on its flip class M ≡ 2p+6 mod 8, uniformly in odd p ≥ 5 | **[PROVED — notes/78 Part I (Theorem C3(p)); SPOT-AUDITED notes/80 §1.1]**: affine-in-p Z/D/E/P write-up complete (L1(p) all 4 \| M ≥ p+7, FLIP(p) in-class M ≥ 2p+6, boundaries machine-EXACT); schema p = 5..25 (11 odd values incl. fresh 23/25 in the audit, both mod-4 classes), 0 fail; solver x-val at 9 p-values (5..13, 17, 21, 23, 25 — 20/20 rows at each of the last four); identity layer re-derived independently p ≤ 39; residual formality = referee prose pass at paper time | p = 5 instance is thm:c3core [PROVED, audited ×3] |
| (H1′) part 2 = GAP-N3-GROW | punctured-rung tolerance d*(x) = ⌊(x−1)/4⌋ → ∞: rung stays UNSAT under any < ⌊(x−1)/4⌋ punctures, uniformly | (N3-a) ≤-side [PROVED mod GAP-SA-HALF] — ONE hypothesis after the notes/78 correction (both parity classes halve onto SA((x+1)/2; M/2), Lemma PS; identities re-derived + exact at x ≤ 31, notes/80); (N3-b) ≥-side [MACHINE]: exact global at x = 11/15/19/23/27 with x = 19 at TWO scales (d*(19; 112) = 4 fresh, notes/80) and d*(27) at two; severed-ladder closures complete at M = 112 (e174b); uniform skeleton LANE + SEV + (N3-b′) stated (notes/78 §II.3; LANE numeric to x = 99) | notes/74 Part I + notes/78 Part II; e130/e130b/e130c/e132; e184 |
| N2-COMPLETE (feeds BRIDGE1-AF + supply 1/12→1/2; NOT consumed by B1) | every odd pair {x, x+1}, x ≥ 11, fires at all 8 residues, M ≥ x+57 | [MACHINE+SCHEMA mod GAP-N2-UNIF]: 108/108 lane laws x = 11..33 ≤ 152; 36/36 template grid, 7 x-values/cell to x≈73, ~2.3k lattice checks, 0 anomalies; MP/D/PC/MIR + Metatheorem T [PROVED, x-free]; audit: K4e(23) fresh at M = 160/164 (notes/76) | notes/73; e174_param_lanes, e175_param_template, e176/e176b, e177 |

Case-1 residual: **GAP-N3-GROW(N3-b) alone** (notes/78: N2-DIAG's
write-up is done, tag [PROVED — audit pending]) — single species,
with every instance ever attempted discharged and zero machine
anomalies; skeleton LANE + SEV + (N3-b′) stated.

## 2. Case-2 kill chain

### 2a. The engine: the two-seam coupled core [GAP-N6a to uniformize]

CI(m)/CORE′(m): 3 blocks (m, 8m], both teams block-ordered at both
seams, bounds bal or const.

- Machine layer [MACHINE, closed everywhere asked]: bal UNSAT at
  m = 16, 20, 24, **28 (NEW, notes/76 fresh-encoder audit, 3.2s)**,
  32, 48, 64, 80; const (2,2,2) at 48/64/80; full bridge chains at
  SIX scales (48/64/80/96 exact COV-W + robust COV-W′ at 128 AND
  160); mechanistic K* law exact at 8 scales with 4 blind hits; cap
  law flat at 96..160; (OV) at all 8 scales.  (e120/e125/e126/e135,
  notes/55-59, audits 60/60-1/61-2, e178.)
- Proved skeleton [PROVED]: Lemma U, A1–A9, E2/C, P′, W, PAR,
  FG-high, Theorem H, Lemma J (independently re-established), DICH
  case tree (H-DICH), Lemma D3, Lemma PH+, ASM′/COV-W′ compositions.
- **Sub-gap pool — REDUCED (notes/77 front + notes/80 adjudication;
  authoritative inventory notes/77 §7).**  CLEARED: GAP-DICH-F0
  (Lemma PURE [PROVED]; SAT-level bijection ×3 scales 48/56/64),
  GAP-PARM-CORNER (Theorem P-ARM‴, modular at M = 48..128 — e155c
  battery + e182 independent encoder + fresh m = 64 chain),
  GAP-FG-schema's fixed-pair half (Theorem AFF⁺ + Lemma MON: one
  certificate per pair valid at all larger M).  Multi-scale laws:
  RES-LAW/CLOSE-LAW′ ×8 scales 48..160; H-LAT/H-RW0′/cliques ×6-7
  half-scales — all descriptive or GAP-RES instances.  **Residue:
  GAP-RES (the consolidated crux — classify the SAT-alive fan pairs
  uniformly in window length; provably carries FG-scaled-zone,
  FG-deep taxonomy, DICH-ALPHA, H-LAT via Cor. PURE-2)** +
  ThW1′-ROBUST/-TOL uniformization (finite packed-quad breaker
  family, hand-listable) + GAP-DICH-F2/CASC + SPLIT finish +
  GAP-LLOP-α/β + GAP-ASM′ = (OV-∀) (8-scale + robust insurance;
  176/192 extension pre-registered, catalogues building).

### 2b. Demand side — a THEOREM modulo N6a (T-TEL″, notes/72 §6)

    J-DOWN [PROVED] + core ──► no zero anchors (v_min(0) = ∞, M ≥ 32)
    T-LEDGER [PROVED]      ──► disjoint payment bookkeeping (4-adic)
    T-FRESH [PROVED mod GAP-F-schema] ──► fresh mints density 1/octave
    D1+D2 [PROVED]         ──► transfer to every Case-2 anchor
    ⟹ every valid Case-2 pair pays ≥ 1 disjoint fresh inversion pair
      per two octaves FOREVER (per octave mod GAP-F-schema), each mint
      P3-convertible to a displaced value — no budget hypothesis.

Certificates: J-DOWN three-line restriction [PROVED, notes/75 §2.2;
re-walked notes/76]; collapse cells (none,0) UNSAT direct at
M = 32/40/48/**64** (7.4/12.6/22.0/56.0 s) + m = 28 via e178;
v_min(0) finite regime exactly M ∈ {8, 16, 24} = 12 exact /
(48, 384] / (65, 1440].  [GAP-VMIN0-growth DISCHARGED; GAP-J-schema
large-M = GAP-N6a verbatim.]

### 2c. Boot window + independent floors (no N6a dependency)

- **Theorem J-BOOT [PROVED mod GAP-CMIN]** (notes/71 §3): (v,0)
  UNSAT for v < M/2, all M ≡ 0 mod 4, M ≥ 12 — Lemma K [PROVED;
  re-proved exhaustively k = 2..4, notes/76] + the counting floor
  f(M) ≥ M/2 [GAP-FHALF → GAP-CMIN].  f(M) = M/2 EXACT at 7 scales
  8..32 (two instruments); cmin(M) = M exact at 8/12/16/**20 (NEW,
  e178 OPT)**.
- **Theorem F-BOOT [PROVED mod GAP-FTOT]** (notes/71 §5): F(M; v)
  UNSAT for v < ⌈M/4⌉ — first uniform freshness law; machine
  F(12;2), F(16;6)×3, F(20;4), F(12;5).
- **Margin family**: low-pure arm [PROVED] (Lemma MARGIN-LP +
  K-diagonal 0/3/4/11/20/28/40/**51 (k=9, NEW e178)**/69/111 —
  K(36,12) = 111 adjudicated by fresh encoder, notes/76 §2); impure
  arm [GAP-MARGIN-MASS, scoped].
- Proved infrastructure: T-CHAN/L-PREFIX, SCHED-DEAD, L-MID
  (re-verified fresh M = 48 + brute@16, notes/76), L-SEESAW, L-HIT,
  L-RANGE, L-HOME, L-2PRICE, T-LEDGER, L-SQUEEZE, L-ECHO, P-CAT
  (fresh M = 200), LEAK, NEST, band pigeonhole.

### 2d. Supply side — THE terminal gap [GAP-AFFORD′]

The demand theorem produces an infinite disjoint system of forced
fresh payments; a NO needs the matching supply cap: **no valid pair
of teams can fund one displaced value per octave forever in donation
currency (single-use colored values)**.  Proved no-go results pin its
shape: NG4 (budget rectangles are demand-only), GAP-COMP refuted
(descent digraphs have zero AP 2-paths), inversion-currency closure
impossible (X-INTERLEAVE pays every boundary legally), one-sided and
counting routes dead (notes/47).  This is the program's single
genuinely new open statement.
UPDATE (notes/79, AFFORD-TOURNAMENT, 2026-08-30 night): five
strategies pre-registered and machine-attacked.  Two refuted and
added to the no-retry list (band-depth weighting — the mint band
map is FULL; single-team density drift — payer identity alternates
with scale, ROT4 measured to m = 80).  One new proved bookkeeping
lemma: **L-DOUBLE-DUTY** [PROVED, sharp ×2 blind + fresh M = 24] —
consecutive-boundary mints are VALUE-disjoint below presence-scale
prices (threshold exactly |O_m ∩ T| + 1).  One new machine core
family: **GAP-SPARSE-CORE** — the dodger corner's own axis (iii)
(donation material gap ≥ 3) makes the coupled core fire at bounds
(1,1,1) from m = 16 (8 scales 16..48 incl. fresh 36, boot ≤ 12,
full control triangle, gap-≥2 discriminator = the parity-lattice
escape; **AAA designation now HAND-CLOSED for m ≥ 26** by the
spacing-2 covering bound ⌈n/2⌉+⌈n/3⌉ < n, n = m/2 ≥ 13 — notes/80
§1.4; J-DOWN transfers the pump collapse verbatim).  And the corner
(i)+(ii)+(iii) is FINITELY INHABITED (CP-SAT witnesses at 2^12 and
2^13, rung-safe sup density < 13/16, ROT4-strength orbit censors).

ADJUDICATION (notes/80, same night): witnesses independently
re-verified (fresh checker: all axes hold) and CHARACTERIZED —
**the corner's inhabitants are mod-4 lattice colorings** (minority
= a difference-4 AP on one residue class mod 4 per block, exact
1/4 splits).  The lattice minority is orbit-CLOSED (2c−c ≡ c mod
4), so the censor dodge is its essence (exact DP: depth 24–58 one
reflector band up — deeper than e179's ~10 estimate), and it is
AP-closed, so lattice-minority colorings are STRUCTURALLY void for
double block order (explicit cross-3-block certificates; they pay
at every anchor unconditionally).  **Champion: S4 (sparse-corner
pincer).  The decisive next statement is MINT-LOC** (notes/80
§3.1(b)): the mint's displaced value is forced within distance ≤ 2
of minority material — if true, paying mints eventually breaks
(iii) and the corner self-destructs; if false, first affordability
evidence for YES.  Pre-registered instrument: mint-region
enumeration ON the witnesses at m = 32/64/128.  AFFORD′ remains
open and terminal; its sharpest form: can the mod-4 lattice corner
afford one displaced value per octave forever.

PINCER EXECUTION (notes/80-pincer + e185, same night): MINT-LOC
resolved in the STRONG form — one-mint SAT region EMPTY at all
pre-registered cells (26/26 incl. the new alternating witness;
hand: Lemmas γ-RIGID/MINT-1); the literal ≤2-distance mechanism is
RETIRED (order payment never recolors, so paying never breaks
(iii)).  **Theorem AFFORD-CORNER [PROVED]**: on blockwise mod-4
lattice colorings (the corner's characterized inhabitants),
(a) L-NOTAIL (DEGS77 + restriction + affine: no permutable team
contains an infinite AP) forces class-ownership to alternate — the
verbatim ω-extensions of ALL THREE S5 witnesses are DEAD;
(b) every H-carrier team pays ≥ 5m²/64 − O(m) seam inversions per
anchor (P5 floor with H computed; exact orientation: one inverted
seam pair per H-triple) with ≥ presence-scale displaced values
confined to (m, 4m), Θ(N) cumulative (vs T-TEL″'s Θ(log N));
(c) no anchor is one-mint payable.  S5-ALT: forcing alternation on
the dodger build = UNSAT at both censors (controls: censor-off SAT
— alternating corner colorings exist and pay double-sided
presence-scale at every anchor; diffuse-off SAT only degenerately)
— the finite corner rejects alternation while ω requires it.
Residue on this family = **GAP-AFFORD″-ALT**: the supply cap for
unbounded-run (procrastinating) alternating lattices + punctured
near-lattices + non-lattice gap-≥3 minorities (the last two dodge
L-NOTAIL; permutable-set density theory at length 3 is open).

## 3. Retired / reframed tags (final dispositions)

| tag | disposition |
|-----|-------------|
| GAP-BRIDGE1 | DISCHARGED (Theorem B1, audited) |
| GAP-VMIN0-growth | DISCHARGED by collapse (J-DOWN) + floor (J-BOOT) |
| GAP-J-schema | large M absorbed into GAP-N6a; boot window = J-BOOT; residue = GAP-J-margin + GAP-F-schema |
| GAP-V*-growth | demoted (demand existence no longer needs it); GAP-V* survives for RATE sharpening only |
| GAP-G2 / DNP | DNP refuted (notes/47); reframed T-FORCE demand half now a theorem mod N6a (T-TEL″); supply half = GAP-AFFORD′ |
| GAP-L1′ | REFUTED (ROT4, notes/74 Part II; re-verified fresh horizons notes/76) — tag retired, nothing load-bearing lost |
| GAP-N3 (uniform-C) | REFUTED (transversal escapes); reshaped to GAP-N3-GROW |
| GAP-N2's three named remainders | DISCHARGED at stated level (notes/73); residue = GAP-N2-UNIF ⊃ GAP-N2-DIAG |
| L-ECHO | live only at M ∈ {8, 16, 24} (no zero anchors above) |

## 4. What the machine layer rests on (rung-finiteness caveat)

Every machine-true family is verified at finitely many scales; each
use at ω rides either a [PROVED] pigeonhole with a FIXED finite core
(T-PIN) or a pending uniformization write-up (§6).  The write-ups —
and nothing else — discharge this caveat.  Two full adversarial audit
cycles (2026-08-28 notes/60/60-1/61-2; 2026-08-30 notes/76) attacked
the verified layer at fresh scales with independent instruments:
zero structural breaks.

## 5. The composed conditional theorem (exact form)

**Theorem (assembly).**  Assume (i) Theorem C3(p) (= former
GAP-N2-DIAG; proved, notes/78 Part I; spot-audited notes/80),
(ii) GAP-N3-GROW (N3-b), (iii) GAP-N6a's sub-pool (§2a),
(iv) GAP-AFFORD′.  Then no 2-set partition of ℤ⁺ has both parts
3-permutable.

*Proof shape.*  By N4 either Case 1 — dead by N1 + B1 + (i) + (ii) —
or Case 2.  In Case 2, (iii) closes the coupled core at every large
anchor; T-TEL″ (whose other inputs are all [PROVED]) then forces the
infinite disjoint fresh-payment system on every valid pair; (iv)
caps supply below it.  Contradiction either way.  ∎

(GAP-CMIN/FHALF/FTOT are NOT hypotheses of the assembly — they give
the independent boot-window floors and the N6a-free second leg; they
harden the graph but do not gate it.  GAP-F-schema only sharpens
demand density 1/2 → 1 per octave.)

## 6. FINAL gap inventory (exact statements + species)

Critical path (all four needed; nothing else is):

| tag | exact statement | species | evidence state |
|-----|-----------------|---------|----------------|
| **GAP-AFFORD′** | for every valid Case-2 pair, the donation supply (single-use colored values, P3-accounted) cannot fund the T-TEL″ mint system (≥ 1 displaced value per 2 octaves) forever | **genuinely new ledger statement** — no template in the campaign | no-go results (NG1–NG4, GAP-COMP refuted) + tournament (notes/79) + adjudication (notes/80): S2/S3 refuted, L-DOUBLE-DUTY [PROVED, ×3 scales], SPARSE-CORE ×8 scales + AAA hand arm, corner INHABITED by mod-4 lattice colorings (verified + characterized) which pay STRUCTURALLY at every anchor — champion route S4, decisive statement MINT-LOC (pre-registered); PINCER EXECUTED (notes/80-pincer): MINT-LOC resolved strong-form, Theorem AFFORD-CORNER [PROVED] (L-NOTAIL + presence-scale demand + one-mint emptiness), S5-ALT UNSAT ×2 censors; residue = GAP-AFFORD″-ALT (unbounded-run alternating + punctured + non-lattice sparse) — the supply CAP itself still has zero completed proof strategies |
| **GAP-N6a sub-pool** | the CI(m) core fires for ALL m (bal ≥ 16; const (2,2,2) ≥ 48): remaining per notes/77 §7 = **GAP-RES** (consolidated: classify SAT-alive fan pairs uniformly in N — carries FG-scaled-zone, FG-deep taxonomy, DICH-ALPHA, H-LAT) + ThW1′-ROBUST/-TOL + DICH-F2/CASC + SPLIT + LLOP-α/β + ASM′ = (OV-∀) | uniformization/classification (discharged instances exist for each; PURE/P-ARM‴/AFF⁺+MON cleared out of the pool) | machine-closed everywhere asked (8 CI scales + robust ×2; P-ARM‴ modular 48..128; laws ×8 full + ×7 half scales; blind hits; 176/192 pre-registered) |
| **GAP-N2-DIAG** | C3(p) UNSAT on its flip class for every odd p ≥ 5 (uniform-in-p write-up) | uniformization — **DISCHARGED: Theorem C3(p), notes/78 Part I [PROVED — spot-audited notes/80]** | schema p = 5..25 (0 fail; 23/25 fresh both mod-4 classes), boundaries exact, solver x-val ×9 p-values, identity layer re-derived p ≤ 39; residual = referee prose pass |
| **GAP-N3-GROW (N3-b)** | < ⌊(x−1)/4⌋ punctures leave the rung UNSAT, uniformly in x and puncture set | uniformization + robustness (severed-ladder closures = machine shadow); skeleton LANE + SEV + (N3-b′), notes/78 §II.3 | exact at x = 11/15/19/23/27 global, x = 19 AND 27 each at two scales (d*(19; 112) = 4 fresh, notes/80); closures complete at M = 112 |

Hardening layer (not gating the assembly):

| tag | exact statement | state |
|-----|-----------------|-------|
| GAP-CMIN | Σ_z min(c_A, c_B) ≥ M for balanced μ_dn = 0 low-impure splits | extremal cell PROVED (M ≥ 32); near-pure reduced to O(1) bookkeeping + 2 scoped subcases; = M exact at 8/12/16/20 |
| GAP-FHALF / GAP-FTOT | f(M) ≥ M/2 resp. f_F(M) ≥ M/2 | follow from GAP-CMIN (verbatim reduction); f = M/2 exact ×7 |
| GAP-F-schema | F(N; v) UNSAT family (freshness; does not project) | F-BOOT gives v < ⌈N/4⌉ mod GAP-FTOT; machine ×3 cells |
| GAP-J-margin / GAP-MARGIN-MASS | U4(2m; v, v*₃(m)+b) family; impure mass at μ_dn ≤ w | low-pure arm PROVED (MARGIN-LP + K-diagonal incl. 51/111) |
| GAP-N2-UNIF ∖ N2-DIAG | remaining 35 template cells' uniform write-ups | feeds BRIDGE1-AF only |
| GAP-V* | v*₃(m; bounds) growth | rate sharpening only |
| GAP-ZERO | classify the sumset floor's zero variety | all zeros measured LOW-PURE (order-dead); N3-species |
| GAP-SPARSE-CORE (new, notes/79; adjudicated notes/80) | CI(m) at (1,1,1) + per-block minority gap ≥ 3 UNSAT for all m ≥ 16 | machine ×8 scales (16..48 incl. fresh 36, boot ≤ 12), control triangle + gap-≥2 discriminator; **AAA designation HAND-CLOSED m ≥ 26** (covering bound; machine covers 16..48) — residue = mixed-designation catalogue; lattice-minority sub-family void STRUCTURALLY (AP-closed minorities carry cross-3-block triples); strengthens Case-2 demand on the (iii)-corner to presence-1 bounds — does not gate the assembly but arms it |
| L-NOTAIL + Theorem AFFORD-CORNER (new, notes/80-pincer) | no 3-permutable team contains an infinite AP (DEGS77 import); blockwise-lattice corner: ownership must alternate, every H-carrier pays Θ(m²) seam inversions/anchor as an exact orientation with presence-scale displaced sets (Θ(N) cumulative), no anchor one-mint payable | [PROVED] + machine (e185: census closed-form exact, 26/26 one-mint cells empty, ν(8/12/16) = 9/31/58, S5-ALT UNSAT ×2 + controls) — arms the corner kill; does not gate the assembly |

**If any critical tag BREAKS instead of clearing**: (i)/(ii) breaking
re-opens Case 1 only via a coloring evading every lane at every
residue — excluded at machine level through x = 33, M = 152; (iii)
breaking contradicts an 8-scale mechanistic law family with blind
hits; (iv) has a live negative shape: the notes/46 dodger corner
(i)+(ii)+(iii) — REALIZED JOINTLY at finite level and now
CHARACTERIZED (notes/80 §4): its inhabitants are **mod-4 lattice
colorings** (minority = difference-4 AP on one mod-4 class per
block; orbit-closed, so T-SHARP procrastination is their essence —
exact DP depth 24–58 one reflector band above the censor; the pure
lattice family extends to ω as a coloring).  That corner is the
entire known YES-space; its inhabitants pay T-TEL″ mints at EVERY
anchor — for the lattice sub-family STRUCTURALLY (AP-closed
minorities cannot be double-block-ordered at all).  [Updated,
notes/80-pincer: the constant-ownership lattice corner — every
realized inhabitant — is DEAD at ω (L-NOTAIL); the live
(iv)-negative shrinks to unbounded-run alternating lattices
(rejected finitely at run-length 1 by S5-ALT, both censors),
punctured near-lattices, and non-lattice gap-≥3 minorities, none
realized.  The YES question is: can THOSE afford presence-scale
payments (GAP-AFFORD″-ALT).]

## 7. Certificates index (one line each)

- paper/main.tex + notes/33: thm:main, thm:ogred, thm:c3core [PROVED, audited ×3]
- notes/52 (+74 patch): Theorem B1 [PROVED mod H1′]
- notes/73: N2-COMPLETE + 36/36 grid [MACHINE+SCHEMA]
- notes/74: N3-GROW + L1′ refutation [MACHINE / PROVED]
- notes/78: Theorem C3(p) affine write-up [PROVED — audit pending] + N3-GROW skeleton (LANE/PS/SEV) + fresh law points d*(19)/d*(23)
- notes/55-59 + 51: N6a skeleton + bridge [PROVED skeleton + sub-pool]
- notes/75: J-DOWN + P-CAT + LEAK + NEST [PROVED]
- notes/71: J-BOOT, F-BOOT, MARGIN-LP, SZ/SZ′/WALL [PROVED mod CMIN/FTOT]
- notes/72: T-CHAN, L-MID/SEESAW/HIT/RANGE, T-TEL″ + link table [PROVED mod stated]
- notes/70: T-LEDGER, T-FRESH, L-HOME/2PRICE/SQUEEZE/ECHO [PROVED mod F-schema]
- notes/62: L-PREFIX, Lemma K, SCHED-DEAD, NG4 [PROVED]
- notes/47/54: DNP refutation, T-FORCE reframing, ledger theorem demand half
- audits: notes/60, 60-audit-1, 61-audit-2 (2026-08-28); notes/76 (2026-08-30) — all SOUND, 0 breaks
- notes/79: L-DOUBLE-DUTY [PROVED, sharp ×2 blind]; SPARSE-CORE [MACHINE ×8 + controls]; S2/S3 refutations; dodger-corner witnesses (e179)
- notes/80: six-species spot-audit (zero anomalies, e184); C3(p) audit rider discharged; AAA covering hand closure; S5 witnesses verified + characterized (mod-4 lattices, structural payment); champion S4 + MINT-LOC pre-registration
- notes/80-pincer: L-NOTAIL, γ-RIGID/MINT-1, D-FLOOR/D-SAT, Theorem AFFORD-CORNER [PROVED]; MINT-LOC executed as pre-registered (e185: 26/26 one-mint cells empty, census closed-form exact, ν frontiers 9/31/58); S5-ALT + attribution battery [MACHINE]
