# H2: sliver-swap partition screening (session H2)

## Question
Notes/37 left "alternating crown ownership + sliver swaps" as the surviving
candidate shape for a YES-partition: give both teams block structures, but
have each team DONATE the first s values of each of its own blocks to the
other team, so that neither team owns its own crown attack surface (the
bottom slivers that killed S_A via 15/16). Does any such partition evade
the S_A death pattern?

**Answer: no. All 14 family members die at every tested horizon, and the
dyadic bottom-swap variants die at theorem level (lem:orbit), not just by
heuristic flags. Survivors: NONE.**

## The family (exact partitions of [1, N], N = 2^16 = 4^8)
- family `dyadic`: blocks (2^{t-1}, 2^t]; even t -> team A, odd -> B;
  1 always joins B (paper convention, `dyadic_none` == S_A | S_B exactly,
  asserted against g2's gen_sa/gen_sb).
- family `quad`: blocks (4^{k-1}, 4^k] (Geneson-style ratio-4 spacing
  between a team's consecutive blocks); even k -> A, odd -> B; 1 -> B.
- swap `none` | `bottom` | `top` (control: donate the harmless end);
  depth s in {8, 12, 16}; donation is min(s, |block|) values per block
  (small blocks are donated whole).

## Screens (experiments/h2_sliver_swap.py, reusing the g2 kit)
Teams are fixed sets — no coloring freedom. Per team:
1. **Pure-complete SAT** at H = 512/1024/4096: ABJ bit-reversal witness +
   independent monotone-3-AP verification; Cadical195 (lazy transitivity)
   cross-check at H <= 1024. As proven in the g2 header, the
   pure-complete window of ANY fixed set is satisfiable (the ABJ order on
   Z has no monotone 3-AP), so this is a consistency check only. Result:
   all 28 team-windows SAT, all witnesses verified, CDCL agrees. Death
   evidence lives in the structural screens.
2. **Orbit scan** (g2, fmax raised 16 -> 48) at H = 512/1024/4096/65536.
3. **Crown scans**, two modes: g2's recurrence-ratio scan (occupied
   octaves, occ 0.25) and a new **persistence scan** (this file): flag
   in-team x <= 64 whose attacked pairs (y, 2y - x) both in-team occur in
   >= 4 octaves reaching within 1 of the team's top octave. The ratio
   test's denominator mixes octave parities and dilutes every-other-octave
   attacks (exactly what swap teams produce) to ratio 0.5; the persistence
   test is parity-robust. Calibration at 2^16: S_A flagged, Geneson W
   clean (only stage-1 relic attacks in octaves {3,5}), W-complement
   flagged — matching the G2 calibration.
4. **Sliver load** (g2, width 8, occ 0.25).

### Two screen fixes forced by this study (both in g2_diagnose.py / h2)
- **Censoring bug**: g2 declared a chain censored iff `2*end - max(F) > N`
  (ALL successors beyond horizon). The bottom8/B orbit chain ends at
  32776 where the f=16 successor is exactly N (in-window, out-of-team)
  but the f=4 successor 65548 — the one the true orbit uses — is beyond
  the horizon. Fixed to `2*end - min(F) > N` (continuation cannot be
  ruled out). Recalibrated all five g2 references: verdicts unchanged
  (sa/sb CROWN+SLIVER, geneson CLEAN, zplus ORBIT+, geneson_c ORBIT+),
  data/g2_*.json refreshed.
- **fmax**: bottom-swap orbit reflectors live at up to ~3s (<= 48 for
  s <= 16); g2's default fmax=16 sees only a fraction of them.

## Results (flags at any of H = 512/1024/4096/65536; full per-horizon
table in data/h2_summary.json, per-candidate detail in data/h2_<name>.json)

| candidate        | team A                | team B                | verdict |
|------------------|-----------------------|-----------------------|---------|
| dyadic_none      | CROWN CROWNP SLIVER   | CROWN CROWNP SLIVER   | DEAD (paper theorem) |
| dyadic_bottom8   | CROWN CROWNP **ORBIT**| CROWN CROWNP **ORBIT**| DEAD (lem:orbit) |
| dyadic_bottom12  | CROWN CROWNP **ORBIT**| CROWN CROWNP **ORBIT**| DEAD (lem:orbit) |
| dyadic_bottom16  | CROWN CROWNP **ORBIT**| CROWN CROWNP **ORBIT**| DEAD (lem:orbit) |
| dyadic_top8/12/16| CROWN CROWNP SLIVER   | CROWN CROWNP SLIVER   | DEAD |
| quad_none        | CROWN CROWNP SLIVER   | CROWN CROWNP SLIVER   | DEAD |
| quad_bottom8/12/16| CROWN CROWNP SLIVER  | CROWN CROWNP SLIVER   | DEAD |
| quad_top8/12/16  | CROWN CROWNP SLIVER   | CROWN CROWNP SLIVER   | DEAD |

## Failure mechanisms

### 1. Dyadic bottom-swap: donation CREATES orbit deaths (hard, lem:orbit)
S_A itself breaks every doubling chain in two steps because doubling flips
octave parity out of team. Donating bottom slivers hands each team a
landing pad at the bottom of EVERY opposite-parity octave — restoring
period-2 infinite orbits u -> 2u - f. With kept-body offset o1 > s and
received-sliver offset o2 <= s, the system

    2^{t-1} + o1  --f1-->  2^t + o2  --f2-->  2^{t+1} + o1  --> ...
    (f1 = 2*o1 - o2,  f2 = 2*o2 - o1, both fixed in-team values)

runs forever. Machine-verified certificates (offset algebra + closed-form
membership rule cross-checked against the generator at 2^16, chain walked
to 2^60; `verify_orbit_certificates` in the script, results in
data/h2_summary.json):

| s  | team | orbit offsets (o1, o2) | reflectors {f1, f2} | sample chain |
|----|------|------------------------|---------------------|--------------|
| 8  | A    | (14, 8)                | {20, 2}             | 46, 72, 142, 264, ... |
| 8  | B    | (12, 8)                | {16, 4}             | 76, 136, 268, 520, ... |
| 12 | A    | (19, 12)               | {26, 5}             | 51, 76, 147, 268, ... |
| 12 | B    | (13, 11)               | {15, 9}             | 77, 139, 269, 523, ... |
| 16 | A    | (24, 16)               | {32, 8}             | 56, 80, 152, 272, ... |
| 16 | B    | (23, 13)               | {33, 3}             | 87, 141, 279, 525, ... |

By the paper's lem:orbit (DEGS-via-chunks: no permutable team contains an
infinite orbit u_{k+1} = 2u_k - f_k with f_k from a finite in-team set),
**all six teams are non-permutable — dyadic bottom-swap is dead as a
theorem, for both teams simultaneously, at every tested depth s.** The
reflectors scale like <= 3s, so any fixed s appears to admit such a system
(choose o2 <= s < o1 with both values 2*o1 - o2 and 2*o2 - o1 in-team;
verified here for s = 8, 12, 16).

On top of that, the crowns are only translated, not removed: the portable
crown pairs {31, 32} (team B) and {63, 64} (team A) recur at 100% of
occupied octaves — attacks ride the kept bottom offsets (s, s + x/2]
(e.g. (18, 137, 256): 18 in A's received sliver, 137 at A's kept bottom,
256 at A's kept top) — the notes/37 portable-crown prediction in vivo.

### 2. Dyadic top-swap (control): S_A pattern simply intact
Donating TOP slivers leaves every team owning its own block bottoms: the
crown/sliver machinery of the S_A disproof applies essentially unchanged
(sliver load 1.0 at every scale on both teams; crown pairs {31,32} etc.
at recurrence ratio 1.0). Additionally the donated top slivers reflect
into the next octave's kept top: 2(2^t - i) - f = 2^{t+1} - (2i + f),
giving a second persistent attack family. Dead on both teams, as expected
for the control.

### 3. Quad family (ratio-4 blocks): reflections are trapped in-block
For a block (4^{k-1}, 4^k] and any y in its lower half, the reflection
z = 2y - x stays INSIDE the block. So every small in-team x attacks every
one of its own blocks regardless of what happens at the block bottom —
sliver donation is irrelevant. quad_bottom8/A even keeps the original
crown pair {15, 16} (recurrence 1.0); quad teams also carry loaded
slivers (their blocks contain full dyadic octaves). This is the exact
inverse of Geneson's Lemma 3.1 design, where ratio-2 blocks force every
reflection to EXIT into a silent zone. Blocks of ratio > 2 are
self-attacking; no sliver policy can fix them.

## The structural lesson
Crown death and orbit death trade off against each other in any
octave-periodic partition:
- Keep your own bottom slivers -> crown attacks (S_A, top-swap, quads).
- Donate them -> the partner's foothold in your scales becomes an orbit
  landing pad (bottom-swap).
Geneson's construction escapes only because the removed slivers fall into
SILENT ZONES owned by nobody — impossible in a partition, where one
team's gap is the other team's block. **Within fixed-depth, octave-
periodic block partitions, the sliver-swap idea is exhausted: the attack
surface is conserved, only relocated.**

The screen also points at the one direction it does NOT kill: make the
donated depth GROW with the scale (s_t -> infinity). A fixed attacker
x needs kept offsets <= x/2 + s... precisely, in-block crown attacks need
kept offsets in (s_t, s_t + x/2] with x <= 2 s_t eventually failing for
every fixed x, and the orbit reflectors f = 2*o1 - o2 > s_t grow out of
every finite reflector set, breaking lem:orbit's hypothesis. Growing
slivers are exactly Geneson's own stage geometry (width M_{k-1} ->
infinity). **Next candidate family (H3): dyadic/quad partitions with
stage-growing donated slivers, e.g. s_t = t or s_t = 2^{t/2}** — the only
member of the sliver-swap idea left standing after this screen.

## Reproduce
    .venv/bin/python experiments/h2_sliver_swap.py          # ~4 min
Artifacts: data/h2_summary.json (verdicts, per-horizon flags, orbit
certificates, persistence-scan calibration), data/h2_<candidate>.json
(14 files: full per-team scans + teams up to 4096), data/h2_run.log,
refreshed data/g2_{sa,sb,geneson,zplus,geneson_c}.json.
