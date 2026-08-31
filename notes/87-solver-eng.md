# notes/87 — solver-engineering sprint (kissat / cryptominisat / cube-and-conquer / gmpy2)

Goal: attack the stuck decision instances with better engines, not
better mathematics.  Four tracks: (1) kissat + cryptominisat benchmarks
on representative stuck instances via eager DIMACS export; (2)
cube-and-conquer on the open near-critical cells; (3) gmpy2 port of the
erdos97 Farkas certifier hot path; (4) redeploy any >5x winner on the
stuck measurement queue.

## 0. Representative instance set (baselines from the record)

| instance | encoder | baseline (Cadical195) | status |
|---|---|---|---|
| c3core@512 — AP+C3 on (M,2M], M=512 | e166 lazy-transitivity | UNSAT, e166@2048 = 11169 s (512 not separately recorded; re-measured this sprint) | known UNSAT (mod-8 law + e104) |
| coupled (2,2,2)@128 core support | e165b lazy | e165b@256 = 930 s, @512 = 13435 s (128 re-measured this sprint) | known UNSAT |
| bal@16 v=5 (vA=vB=5, exact balance) | e127 solve_budget, eager | TIMEOUT (~40000 s class; v=4 UNSAT 5500 s pinned, v=8 TIMEOUT 17024 s) | OPEN — v*3(16) ∈ {5,6} |
| growth24 v=16 (bal@24, vA=vB=16) | e127 solve_budget, eager | bal24 v=0 3.3 s, v=1 54.1 s UNSAT; v≥2 unmeasured | OPEN — v*3(24) growth point |

DIMACS export = e189_dimacs_export.py (this sprint).  Soundness: the
bal/growth export is the SAME eager clause set as e127.solve_budget
(complete transitivity, guarded APs, seqcounter cards), variable
numbering identical; c3core/coupled exports are the e166/e165b clause
generators with FULL transitivity materialized instead of lazy CEGAR
(a superset of every lazily-added clause; UNSAT/SAT semantics of the
full theory, no closure caveat).

## 1. Track 3 (gmpy2) — DONE first: measured multipliers

nk_cert.py (erdos97) now takes --gmpy2: module-level Q = Fraction |
gmpy2.mpq, hot-path functions (solve_exact_on_support,
verify_cert_inline, shortcut normalization) all routed through Q;
worker init propagates the flag.  Benchmark nk_bench_gmpy2.py, single
core, same 1000 n=10 types, warmed up, cross-verified (every mpq cert
re-verified exactly under Fraction — 1000/1000 OK):

| config | total | exact-arith inside | per-type |
|---|---|---|---|
| Fraction, production (shortcut on) | 24.55 s | 0.22 s | 24.6 ms |
| gmpy2, production | 23.72 s | 0.38 s | 23.7 ms |
| Fraction, LP path forced | 38.36 s | 4.97 s | 38.4 ms |
| gmpy2, LP path forced | 25.54 s | 0.89 s | 25.5 ms |

**Multipliers: exact-arithmetic hot path 5.6x (mpq); end-to-end LP path
1.50x; production end-to-end 1.03x** — because at n = 10 the
nonpositive-row shortcut kills ~everything and Fraction work is < 1 %
of runtime; the float LP dominates the non-shortcut path.  gmpy2 is
real but only matters where the exact path fires.  (Production
exact-arith shows 0.59x = mpq constructor overhead on the trivial
shortcut normalizations — the shortcut path does almost no rational
arithmetic at all.)

n=11/n=12 feasibility — SETTLED (negative), with measurements:

- Sharded enumerator (nk_enum_par.c, -first fixes W[0]): NV=10
  shard-sum reproduces the canonical 9,936,815 leaves / 497,399 reps
  EXACTLY (126 shards, 339 s wall on 12 sprint-D cores) — sharding
  validated.
- The full n = 11 count is itself infeasible (shard 0 alone passed 35M
  types before being killed), so counts come from a Knuth Monte-Carlo
  tree-size estimator (nk_est.c, same feasibility predicate, unbiased
  for leaves; calibration at NV=10: est 1.02–1.10e7 vs true 9.94e6).
- **n=11: ~1.4e12 leaves, ~6.2e10 types** (est_reps = leaves/22,
  trivial-stabilizer approximation; stderr ~3 %).
- **n=12: ~1.9e17 leaves, ~8e15 types.**
- Measured per-type cost at n = 11 (1000-type sample from the head of
  shard 0, real n11 masks): 31.1 ms Fraction / 30.8 ms mpq — all 1000
  shortcut kills, same shape as n = 10.
- Verdict: n=11 direct certification = 6.2e10 x 31 ms ~ **61
  core-years** (plus ~18 core-years just to enumerate at the measured
  2400 leaves/s/core) — infeasible at any gmpy2 multiplier, since the
  hot path gmpy2 accelerates is < 1 % of the pipeline.  n=12 is 5
  orders beyond that.  The n >= 12 frontier needs the schema/lcomb
  compression route (per-family certificates), not faster rationals.

## 2. Track 1 interim — benchmark rows landing

Correction to the sprint brief: the recorded 13435 s Cadical-lazy UNSAT
is the **coupled (2,2,2)@512 core** (e165b_M512_core.log, main pod),
not the C3 core@512 — C3@512 is cheap under Cadical-lazy (108 s,
re-measured, 11 rounds).  The C3-family stuck scale is 2048+ (e166
lazy: 11169 s @2048; @4096 still running on main pod since Aug 29).

| instance | Cadical195 lazy (baseline) | kissat 4.0.4 (eager DIMACS) | CMS 5.14.7 (eager DIMACS) |
|---|---|---|---|
| c3core@512 (44.6M cl eager) | **108 s** | 2189 s | **31 s solve** (+303 s python DIMACS load) |
| coupled (2,2,2)@128 core (105.7M cl eager) | **690 s** | 5196 s | 1246 s solve (1906 s total) |
| bal@16 v=1 (940K cl, known UNSAT 24 s) | 24 s (record) | **> 300 s TIMEOUT** | — |
| bal@16 v=5 (OPEN) | TIMEOUT ~40000 s class | running (1h+, no verdict) | running (1h+, restarts) |

Early reading: kissat is the WRONG engine for both families (loses
20x to Cadical-lazy on c3core@512, 10x+ on tiny bal cells).  CMS is a
genuine winner on the parity-heavy c3core (31 s where lazy-Cadical
needs 108 s and kissat 2189 s) — c3core@1024 eager (357M clauses)
generating now to see if the CMS edge scales to where the lazy loop
hurts (11169 s @2048).  No explicit XOR constraints exist to hand CMS:
the mod-8 law lives in the value indices, not as variable parities —
CMS's win is its inprocessing on the dense transitivity structure, not
recovered XORs (verbose log shows no xor recovery on c3@512).

First C&C attempt (e189_cnc.py, kissat per cube, 6435 balanced-B0
cubes on bal@16 v=1): every cube TIMEOUT at 120 s — kissat again, not
the splitting.  v2 driver (e189_cnc2.py) switches to persistent
Cadical195 workers (base CNF loaded once per worker, cubes as
assumptions, conflict-budgeted, learned clauses shared across cubes
within a worker).

**C&C v2 validation (bal@16 v=1, known UNSAT 24 s mono): UNSAT, all
6435 balanced-B0 cubes refuted, 541 s wall on 32 workers.**  Per-cube
avg ~2.6 s (first cube per worker ~25 s, then the incremental effect
kicks in).  Notable control datum: a single fixed-B0 cube costs ~27 s
on a FRESH solver — as much as the whole mono query — so the cube win
comes from incremental reuse, not from the split shrinking the theory;
and re-solving mono on a solver polluted by a prior assumption query
took 575 s vs 24 s fresh (incremental reuse cuts both ways across
heterogeneous queries).

## 3. OPERATIONAL DISCOVERY — the pods are cgroup-quota'd far below nproc

cpu.cfs_quota/period measured mid-sprint after C&C workers sat at 20 %
CPU in R state: **sprint-B 10.2 cores (nproc 48), sprint-C 10.2 (nproc
64), sprint-D 10.2 (nproc 24), main 13.6 (nproc 64)** — the fleet is
~44 quota-cores total, not ~200.  Every historical "60 workers" run has
been time-slicing ~10 cores.  All C&C swarms resized to quota:
bal16v5 -> sprint-D (idle, 10 w), growth24v16 -> sprint-B (8 w),
fresh24v65 -> sprint-C (5 w, shares quota with the sibling session's
e174/vmus/e168 jobs).  This also recalibrates every wall-clock in the
measurement record: monolithic TIMEOUT cells were competing inside the
same 10-core quota as their neighbors.

Additional engine rows: CMS via pycryptosat CRASHED on both big
attempts (SIGABRT loading c3core@1024 = 357M clauses; SIGILL 1.5 h into
bal16v5) — the pip wheel is not trustworthy at this scale; a proper
cryptominisat5 CLI build is in progress (pip-installed cmake, zlib
disabled).  CMS-lazy loop (e189_cms_lazy) validated correct at 24/20
(UNSAT/SAT+witness) but is slower than Cadical-lazy at 512 (>305 s vs
108 s): CMS's restart-heavy incremental behavior wastes the CEGAR
loop's warm state.  kissat on bal16v5 mono: SIGSEGV at 9538 s (no
verdict).  Windowed-transitivity subsets (hoped to make 2048+ eager
exports feasible): minimal UNSAT window scales as w*(M) ~ M-8
(8/16/24/32 at M=16/24/32/40) — half the block, no asymptotic savings;
route dead.

## Log

- [launch] note created; export tooling next.
- e189_dimacs_export.py: bal (verbatim e127 clause capture via recording
  solver class), c3core (e166 + full transitivity), coupled (e165b +
  full transitivity).  Local sanity: bal16v0 UNSAT 1.2s / c3@16 UNSAT /
  c3@20 SAT / coupled(2,2,2)@32 UNSAT 6.5s — all match the record.
- kissat 4.0.4 built on sprint-B + sprint-C; pycryptosat 5.14.7 (CMS)
  installed both; cryptominisat CLI not buildable (no cmake on pods) —
  CMS driven via e189_cms.py (DIMACS -> pycryptosat, verbose stats).
- In flight: kissat c3core@512 + coupled@128 + CMS c3@512 + cadical-lazy
  baselines e166@512/e165b@128 (sprint-B); kissat + CMS bal16v5
  (sprint-C); bal24v16 export (sprint-C).
