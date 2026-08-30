# 72 — FRONT VMIN0-GROWTH: the diverging demand series — growth
# theorem attempt + the composed T-TEL′ keystone

Task: (1) prove v_min(0)(M) ≥ c·M from the band-exhaustion mechanism
(notes/68) by layer counting; (2) write the composed statement
T-LEDGER + T-FRESH + v_min(0) → ∞ ⟹ demand side of L-AFFORD for the
linear regime, with every link's status.  This is the keystone
document for the Case-2 ledger chain.

Verdict in one line: **the demand calculus of the (v,0) cell is now a
proved three-channel theorem (T-CHAN), the sumset floor is exactly
computable and its ONLY zero is the parity schedule already killed by
SCHED-DEAD at every budget — the growth theorem reduces to one
extremal coverage inequality [GAP-BAND-COV] plus one robustness
radius [GAP-K-ROB], both stated exactly, with the coverage arm
PROVED on the canonical range family (demand ≥ M − O(1)); the series
itself is harvested to five scales (v_min(0)(32) > 512, const-bounds
(65,0)@24 UNSAT) after quarantining a fleet mis-launch that was
solving the WRONG CELL.**

## 0. The object

The (v, 0) pump cell (e158/e173 4-block encoder — the ONLY encoder
that defines v_min(0)):

- blocks Bm1 = (M/2, M], B0 = (M, 2M], B1 = (2M, 4M], B2 = (4M, 8M];
  seams s0 = β(M) (Bm1×B0), s1 = β(2M) (B0×B1), s2 = β(4M) (B1×B2);
- coloring A/B with per-block bounds (bal = exact balance; const =
  lower bounds (2, 3, 6, 12)); per-team AP-free orders;
- per-ANCHOR budgets: anchor M/2 pays x_{s0} + x_{s1} = 0 (vdn = 0),
  anchor M pays x_{s1} + x_{s2} ≤ v (vup) — per team.

Under vdn = 0 both teams are wholesale block-ordered
[Bm1∩T] ≺ [B0∩T] ≺ [B1∩T] (L-PREFIX, notes/62 §4c), so the effective
budget is x_{s2} ≤ v.  v_min(0)(M) := least v with the cell SAT =
the price of a FREE lower anchor (notes/62 §5).

## 1. The series (harvest complete as of this session)

bal mode (exact balance):

| M | UNSAT at v (time) | SAT at v (time) | v_min(0)(M) |
|---|-------------------|-----------------|-------------|
| 8 | 6 (2.1s), 8 (7.3s), 9 (11.5s), 10 (24.5s), 11 (40.6s) | 12 (8.6s), 16, 64, 256 | **= 12 EXACT** |
| 16 | 6 (2.1s ×2 encoders) | 384 (17.2s); TIMEOUT@3600s at 96, 192 | ∈ (6, 384] |
| 24 | 65 (46.0s) | — | > 65 |
| 32 | 100 (62.6s), 256 (137.2s), **512 (98.6s)** | — | **> 512** |
| 48 | — (512 TIMEOUT @43200s, main pod) | — | open (5th scale) |

const mode (bounds (2, 3, 6, 12) — NO balance):

| M | verdict | reading |
|---|---------|---------|
| 24 | (6,0) UNSAT [106.0s]; **(65,0) UNSAT [14797.6s]** | **the const-bounds ladder has a second point: v_min^const(0)(24) > 65** — the pump demand at 24 is not a balance artifact at any measured budget |
| 32 | (100,0) TIMEOUT @43200s | open |

Freshness refinement F(M; v) (s0 = 0 only, s1 freed below,
x_{s1} + x_{s2} ≤ v):

| cell | verdict |
|------|---------|
| F(16; 6) | UNSAT — TWICE independently (983.5s local, 1350.2s main pod) |
| F(24; 65) | TIMEOUT @43200s (relaunched on sprint-C at 86400s) |

Key monotone facts: v_min(0)(8) = 12 = 1.5M; v_min(0)(24) > 65 ≈
2.7M; v_min(0)(32) > 512 = 16M.  The lower-bound curve is
super-linear on its face between 24 and 32 (both are only lower
bounds; no curve-fitting per campaign rule).  Every point sits far
above the balanced v*₃ bracket at its scale (v*(bal,8) = 0;
v*(bal,32) witness 368 < 512) — zeroing an anchor costs
qualitatively more than paying the floor, at every measured scale.
Deep-UNSAT stays cheap through v = 512 at M = 32 (98.6s); the wall
is scale (M = 48), not budget depth.

## 2. FLEET INCIDENT (quarantine + fix, this session) — the wrong cell

The three sprint pods had been launched (previous infra hand-off)
with drivers calling **e127's solve_budget(M, None, v, 0)** — the
3-block window (M, 8M] with per-TEAM budgets (team A ≤ v, team B ≤ 0)
— NOT the 4-block per-anchor pump cell that defines v_min(0).  The
mismatch was caught by the first landed point: sprint-C printed
"CERT M=8 (up=11,dn=0): SAT [0s]" where the true pump cell (11,0)@8
is UNSAT [40.6s, data/e173_pump_M8_up11_dn0.json].  The e127 cell is
SAT there because a per-team (v, 0) budget is the one-sided
weakening already known toothless (notes/47: asym one-sided variants
SAT at v = 0).

Actions: all three pod runs killed before any wrong point could
enter the series; e173_telescope.py deployed to all pods; drivers
rewritten against solve_chain with the exact budget vectors
[("vdn", [0,1], 0), ("vup", [1,2], v)] (sprint-B bisect grid
16: 12/24/48/96, 24: 128/256, 32: 768/1024; sprint-D fifth scale
48: 64/128/256 + interp 40: 256/512 + long (512,0)@48; sprint-C
cross-encoder cert battery (11,0)@8 / (12,0)@8 / (6,0)@16 /
(65,0)@24 + F(16;6) third run + F(24;65) at 86400s).  **Quarantine
rule: no number enters the v_min(0) table unless its record carries
the e173/e158 4-block budget vector.**  (§1's table is built
exclusively from such records: local e173_telescope.jsonl +
e158_c3/f_* + main-pod e158_tel_*.)

Also harvested from the main pod this session (correct encoder,
previously unlogged in notes): (512,0)@32 UNSAT [98.6s] and the
const-bounds (65,0)@24 UNSAT [14797.6s] — both now in §1.
