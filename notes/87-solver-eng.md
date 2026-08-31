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

## Log

- [launch] note created; export tooling next.
