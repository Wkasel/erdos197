# Master assembly: the complete NO — FINAL dependency graph
# (rewritten 2026-08-30 end-of-day, post five-front merge + notes/76 audit;
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
mathematics, no surviving proof strategy) and the uniformization pool
(finite catalogue-schema write-ups of one proved-in-instances species:
GAP-N3-GROW's (N3-b), the GAP-N6a sub-pool, GAP-CMIN; GAP-N2-DIAG
left this pool 2026-08-30 late — Theorem C3(p), notes/78, [PROVED —
audit pending]).  No announcement-shape document exists or should.

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
| (H1′) part 1 = GAP-N2-DIAG | the diagonal rung C3(p) = {t_p≺b_p, t_{p−2}≺b_{p+1}, t_{p+5}≺b_{p−2}} UNSAT on its flip class M ≡ 2p+6 mod 8, uniformly in odd p ≥ 5 | **[PROVED — notes/78 Part I (Theorem C3(p)); adversarial audit pending]**: affine-in-p Z/D/E/P write-up complete (L1(p) all 4 \| M ≥ p+7, FLIP(p) in-class M ≥ 2p+6, boundaries machine-EXACT); schema executed p = 5..21 (fresh 15/17/19/21), 104+52+52 scales each, 0 fail (e123 rerun); solver x-val p = 5..13 (e123b) + fresh 17/21 20/20 (e180) | p = 5 instance is thm:c3core [PROVED, audited ×3] |
| (H1′) part 2 = GAP-N3-GROW | punctured-rung tolerance d*(x) = ⌊(x−1)/4⌋ → ∞: rung stays UNSAT under any < ⌊(x−1)/4⌋ punctures, uniformly | (N3-a) ≤-side [PROVED mod GAP-SA-HALF] — ONE hypothesis after the notes/78 correction (both parity classes halve onto SA((x+1)/2; M/2), Lemma PS); (N3-b) ≥-side [MACHINE]: exact global at x = 11/15/19/23/27 (e174/e180 KCRIT, cardinality-exhaustive; 19 and 23 FRESH, 23 ≡ 7 mod 8; d*(27) at TWO scales), severed-ladder closures complete at M = 112 (e174b); uniform skeleton LANE + SEV + (N3-b′) stated (notes/78 §II.3) | notes/74 Part I + notes/78 Part II; e130/e130b/e130c/e132 |
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
- **Sub-gap pool (the uniformization residue — all one species:
  finite catalogue-schema write-ups):** GAP-DICH (5 rows, notes/57
  §7), GAP-LLOP-α/β, GAP-PARM (⊇ GAP-PARM-CORNER ⊇ FG-deep 20-pair
  core), GAP-ASM′ = (OV-∀) only (8-scale-true + robust-chain
  insurance), GAP-FG-schema, GAP-FG-deep.

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
lemma: **L-DOUBLE-DUTY** [PROVED, sharp ×2 blind] — consecutive-
boundary mints are VALUE-disjoint below presence-scale prices
(threshold exactly |O_m ∩ T| + 1).  One new machine core family:
**GAP-SPARSE-CORE** — the dodger corner's own axis (iii) (donation
material gap ≥ 3) makes the coupled core fire at bounds (1,1,1)
from m = 16 (7 scales, 4 residues, boot ≤ 12, full control
triangle, gap-≥2 discriminator = the parity-lattice escape, AAA
hand skeleton via spacing-2 covering; J-DOWN transfers the pump
collapse verbatim).  And the corner (i)+(ii)+(iii) is FINITELY
INHABITED (CP-SAT witnesses at 2^12 and 2^13, rung-safe sup
density < 13/16, ROT4-strength orbit censors, always dodged one
reflector band up — T-SHARP realized): corner emptiness is NOT a
viable NO-route.  AFFORD′ remains open and terminal, now in its
sharpest form: can a sparse-corner coloring afford one displaced
value per octave forever, with explicit witnesses to instrument.

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
GAP-N2-DIAG; now proved, notes/78 Part I, audit pending),
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
| **GAP-AFFORD′** | for every valid Case-2 pair, the donation supply (single-use colored values, P3-accounted) cannot fund the T-TEL″ mint system (≥ 1 displaced value per 2 octaves) forever | **genuinely new ledger statement** — no template in the campaign | no-go results (NG1–NG4, GAP-COMP refuted) + tournament (notes/79): S2/S3 routes refuted, L-DOUBLE-DUTY [PROVED] joins the bookkeeping, GAP-SPARSE-CORE [MACHINE ×7 scales] pincers the (iii)-corner, corner finitely INHABITED (2^12/2^13 witnesses) — supply cap itself still has zero surviving proof strategies |
| **GAP-N6a sub-pool** | the CI(m) core fires for ALL m (bal ≥ 16; const (2,2,2) ≥ 48): remaining = GAP-DICH (5 catalogue rows), GAP-LLOP-α/β, GAP-PARM (⊇ CORNER ⊇ FG-deep), GAP-ASM′ = (OV-∀), GAP-FG-schema/-deep | uniformization (catalogue-schema write-ups; discharged instances exist for each) | machine-closed everywhere asked (8 scales + 2 robust + m = 28 fresh); laws mechanistic with blind hits |
| **GAP-N2-DIAG** | C3(p) UNSAT on its flip class for every odd p ≥ 5 (uniform-in-p write-up) | uniformization — **DISCHARGED: Theorem C3(p), notes/78 Part I [PROVED — audit pending]** | schema-verified p = 5..21 (0 fail), boundaries exact, solver x-val ×6 p-values |
| **GAP-N3-GROW (N3-b)** | < ⌊(x−1)/4⌋ punctures leave the rung UNSAT, uniformly in x and puncture set | uniformization + robustness (severed-ladder closures = machine shadow); skeleton LANE + SEV + (N3-b′), notes/78 §II.3 | exact at x = 11/15/19/23/27 global (2 fresh, ≡ 7 mod 8 covered); closures complete at M = 112 |

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
| GAP-SPARSE-CORE (new, notes/79) | CI(m) at (1,1,1) + per-block minority gap ≥ 3 UNSAT for all m ≥ 16 | machine ×7 scales (16..48, boot ≤ 12), control triangle + gap-≥2 discriminator; AAA designation hand skeleton (spacing-2 covering); strengthens Case-2 demand on the (iii)-corner to presence-1 bounds — does not gate the assembly (the (2,2,2) core suffices) but arms it |

**If any critical tag BREAKS instead of clearing**: (i)/(ii) breaking
re-opens Case 1 only via a coloring evading every lane at every
residue — excluded at machine level through x = 33, M = 152; (iii)
breaking contradicts an 8-scale mechanistic law family with blind
hits; (iv) has a live negative shape: the notes/46 dodger corner
(i)+(ii)+(iii) — now REALIZED JOINTLY at finite level (notes/79
S5: CP-SAT witnesses at 2^12/2^13, rung-safe density, ROT4-strength
orbit censors; asymptotic (i) undecided — every witness carries
depth ~10 chains one reflector band above its censor, T-SHARP
shape).  That corner is the entire known YES-space; by
GAP-SPARSE-CORE its inhabitants pay T-TEL″ mints at EVERY anchor
from presence 1.

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
- notes/79: L-DOUBLE-DUTY [PROVED, sharp ×2 blind]; SPARSE-CORE [MACHINE ×7 + controls]; S2/S3 refutations; dodger-corner witnesses (e179)
