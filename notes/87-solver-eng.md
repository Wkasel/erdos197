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

n=11/n=12 feasibility: parallel sharded count of the n = 11 witness
enumeration launched (nk_enum_par.c, -first shard on W[0], sprint-D;
NV=10 shard-sum validation first).  Projection to follow from the
measured count + per-type cost at n = 11 (sampled from the head of the
n = 11 enumeration).

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
