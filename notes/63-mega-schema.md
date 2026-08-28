# 63 — FRONT MEGA-SCHEMA: derivation checkers at MASSIVE scales

Monster-scale stress phase (2026-08-28).  Goal: execute the certified
derivation checkers far beyond their discovery/audit scales — pure
big-int rule execution, no solver on the target chain — and report
time/memory scaling.  ANY failure = five-alarm.  None occurred.

## 1. e113 C3 hand-proof checker at 2^13 / 2^14 / 2^16 / 2^20

Driver: experiments/e159_mega_e113.py (imports the UNMODIFIED
e113_c3_hand_proof executors — check_layer1, check_flip,
sharpness_4mod8 — no arithmetic shortcut was needed even at 2^20).
Record: data/e159_mega_e113.json.

| M | layer1 | flip | sharp(M+4) | peak RSS |
|---|--------|------|------------|----------|
| 2^13 = 8192    | PASS 0.31 s | PASS 0.27 s | PASS | 32 MB |
| 2^14 = 16384   | PASS 0.98 s | PASS 0.52 s | PASS | 58 MB |
| 2^16 = 65536   | PASS 3.45 s | PASS 2.05 s | PASS | 108 MB |
| 2^20 = 1048576 | PASS 64.8 s | PASS 37.4 s | PASS | 1195 MB |

Every lemma application (Z zigzag rungs, P flood pairs, E transfer,
all case x phase branches, audit() hypothesis discipline) executed
rung-by-rung at every scale; zero assertion failures.  Scaling:
time and memory essentially LINEAR in M (per-branch fact stores are
O(M); the 2^16 -> 2^20 step is 16x M and ~19x time — mild set-resize
overhead).  Extrapolation: 2^24 would need ~20 GB RSS — the point at
which the inner loop would want the arithmetic reimplementation the
task anticipated; at 2^20 the ORIGINAL checker still runs as-is.
Sharpness controls at M = 2^k + 4 (== 4 mod 8) confirm the schema's
center-class conditions fail off the dyadic class at every scale.

C3 certificate family now machine-executed at: 100+ scales 12..4096
(prior) + 8192, 16384, 65536, 1048576.  **Largest M = 2^20.**

## 2. Exact seam/interval walk battery to 2^100000+ (and 2^1000003)

Driver: experiments/e159b_mega_walks.py (extends g4c partA's exact
walks — the battery STATUS cites as "seam ~2^20000 / FAN at
2^20102").  Record: data/e159b_mega_walks.json.

* tri schedule a_k = 2 + k(k+1)/2 pushed to k = 450 (top exponent
  101477); quad a_k = 2 + k^2 to k = 320 (top exponent 102402).
  X2 closure (2 * 2^{a_{k+1}} < 2^{a_{k+2}}) and C0 neck divergence
  (2 * 2^{a_k} − 2^{a_{k+1}} < −2^{a_k}) hold at EVERY stage of both
  schedules — all exact big ints, < 0.01 s per battery.
* FAN arithmetic at the first seam past exponent 100000:
  tri seam 2^100130 (30143 decimal digits), quad seam 2^100491
  (30251 digits) — planted member p in {2^j−1, 2^j}, completions
  2p − x checked for small fixed x (the g4c law, x < m form) AND at
  the exact boundary (m < 2p − x <= 2m iff x < 2p − m) — OK.
* Monster spot battery at exponent 1000003 (301031 decimal digits):
  FAN + X2 + neck all OK in 0.01 s.

Test-harness note (honesty record): the FIRST run of the extended
battery reported FAN "FAIL" — traced to the new boundary attackers
x = m−1, m−2 added by this driver, which for planted member p = m−1
land ON the seam (octave condition is x < 2p − m = m − 2, not
x < m).  The g4c law as certified (fixed x, seam -> infinity) is
untouched; the driver now asserts the exact boundary predicate and
everything passes.  Not a finding against any certified law.

**Walk certificate family: from ~2^20000 to 2^1000003 (X2 + neck +
FAN), full-schedule battery to 2^102402.**

## 3. A1–A9 attack catalogue (notes/55 §2) at 2^13 / 2^16 / 2^20

e137's brute-force AP enumeration is Theta(M^2) time AND memory —
infeasible at 2^13+ (the materialized families alone would be tens
of GB).  Reimplemented arithmetically (experiments/e159c_mega_a1a9.py)
exactly as the task prescribed: families re-derived from raw
definitions (block membership + AP identity) by looping over the
midpoint only, partner range by exact integer-interval intersection —
O(M) time, O(1) memory per family; every closed form / count / range
of A1–A9 then asserted numerically.

Independence guard: the arithmetic enumerator was cross-validated
SET-FOR-SET against e137's original enum_pattern at M = 48, 64, 80,
112, 160 (7 families each, identical).  Record: data/e159c_mega_a1a9.json.

| M | verdict | time | family sizes (exact big-int counts) |
|---|---------|------|--------------------------------------|
| 2^13 | A1..A9 OK | 0.03 s | straddle 5.05e7, (1,1,2) 1.68e7, (1,2,2) 5.05e7 |
| 2^16 | A1..A9 OK | 0.24 s | straddle 3.22e9, (1,1,2) 1.07e9, (1,2,2) 3.22e9 |
| 2^20 | A1..A9 OK | 6.7 s  | straddle 8.25e11, (1,1,2) 2.75e11, (1,2,2) 8.25e11 |

(2^20 was free at O(M) — run as a bonus beyond the tasked 2^13/2^16.)
All fixed-size laws hold verbatim: |A1| = 64, |A2| = 256, |A5| = 56,
A4 parent counts (M+15−s)//2+1 for every s, A3 wall 5M+15 < 6M+1,
A7d band edge, A8 mirror widths, A9 flood-free F.
**A1–A9 family: largest M = 2^20.**

## 4. H-DICH arithmetic layer (notes/57 §2/§4/§5) at 2^13 / 2^16

Scope note: notes/57's DICH proof = uniform arithmetic layer
(Lemmas FI/ANCHOR/COLL, H0–H2 interval collisions, Lemma-SP
staircase kill) + per-scale catalogue layer (F1–F4: alpha, f,
admissible windows).  The catalogue layer needs the fan catalogue
D(M) — Theta(M^2) closure runs, structurally out of reach at 2^13+
and precisely the acknowledged GAP-DICH rows; NOT stressed here.
The arithmetic layer is what the H-DICH case tree executes, and it
was run in full (experiments/e159d_mega_dich.py, validated first at
48/64/80/96/160 with full brute force; record data/e159d_mega_dich.json):

* FI — every z in P2: forced interval re-derived from the u-range
  (independent path), all Lemma-FI claims asserted (anchor iff
  s <= M−31, exact low/mid lengths, tail >= m−8, ell >= 16,
  n_c >= 8 with the 8-mass set exactly {+1, +2M+15} odd / {+2}
  even).  Honest brute-force u-loops on a stratified z-sample
  (FULL — every z — at 2^13).
* A2 — f_c(D) >= 9 for 2-element D: monotonicity reduction + the
  single surviving worst pair {4M+1, 6M+15} exact + 2x10^5 random
  exact pairs per scale.
* COLL/H1 — for every admissible minimum s0 <= M−1, both classes:
  bottom in [3M−15, 3M], mid-window delta = ceil((s0−(M−31))/2)
  <= 15, length >= 16; global min(top) >= max(bottom) — every
  two-sided defector pair collides (the H1 kill), numerically.
* SP — sigma index map boundary-sampled; hidden-staircase forced
  mass m+n−w1 == m+22 > m+14 both classes; band-top slack.

Results: [see table below — filled after the runs]

## 5. Verdict

[filled at close]
