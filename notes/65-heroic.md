# FRONT HEROIC-SOLVES (notes/65) — largest blind solver checks

Session 2026-08-28/29.  Fleet note: the listed pods (64.119.209.250:8764,
194.26.196.173:33606) were gone; RunPod API shows one live pod —
**erdos-ledger-3 (wb23t7m7x3wog0), 64.119.209.250 ssh port 13289**, 64
host cores / 251 GB RAM, $0.22/hr; the rest of the fleet EXITED
2026-08-28 16:33 UTC.  Everything below runs on this one box (load ~11
of 64 after both batches; RAM 61/251 GB — headroom fine).  Scripts in
/root/e/experiments, logs in /root/e/data.

## Tools (committed here: experiments/e165*, e166*)

- **e166_block_lazy.py** — single-block (M, 2M] order gadget, lazy
  transitivity (e89-style CEGAR: solve → boolean-matmul closure →
  add violated triangles, capped/round) + upfront window-w transitivity
  seed.  `--attacks c3` = the 3-axiom core {t5≺b5, t3≺b6, t10≺b3};
  `--attacks og` = the full 15-attack OG(M).  UNSAT is sound (lazy
  clauses ⊂ full encoding); SAT requires closure + independent witness
  verifier (permutation, attacks, exhaustive AP scan).
- **e165_coupled_lazy.py** — the e120 solve_coupled3 gadget (3 blocks,
  2 seams + outer, per-team orders, guarded APs, (2,2,2) bounds)
  re-encoded with the same lazy-transitivity loop.  `--support core` =
  CORE′ open variant (M,2M] ∪ [3M−14, 6M+15], n = 4M+30; `--support
  full` = (M, 8M], n = 7M.  Full transitivity at these n would be
  0.8–3.8 G clauses — never materializable; lazy is the only route.
- **e165b_coupled_lazy.py** — same, but the EXACT locked CORE′
  (closed [3M−15, 4M] per notes/64 arbitration, n = 4M+31).

## Sanity battery (all match known verdicts; witnesses re-verified)

- e165 M=24 full (3,3,3) SAT [3s, check OK]; M=32 full (3,3,3) UNSAT
  [6s]; M=40 full (2,2,2) SAT [9s, check OK]; M=48 core (2,2,2) UNSAT
  [7s] — reproduces e120/e125/e135 exactly.
- e165b M=48 core-closed (2,2,2) UNSAT [9s] — matches e135's lock.
- e166 c3 M=20 SAT (witness OK; 20 ≡ 4 mod 8) and M=24 UNSAT [0s]
  — the mod-8 law's both sides.

## HEADLINE (landed 00:13 UTC, 930s wall): coupled (2,2,2) UNSAT at M=256

**VERDICT e165 M=256 core (2,2,2): UNSAT (930s, 18 rounds, 5.4M lazy
clauses)** — n=1054, orderVars 1.11M, log data/e165_M256_core.log.
The coupled two-seam constant-bound core fires at M = 256 — previous
record M=96 (e126_deep in flight then; certified 48/64/80).  This is a
**3.2× scale jump for GAP-N6a's schema**, on the CORE′-restricted
support (certified sufficient at 5 moderate scales; open-interval
variant, n = 4M+30 — its own 48-scale sanity UNSAT above).  Blind in
the relevant sense: no schema knowledge in the encoding, fresh solver
run, UNSAT sound under lazy transitivity.

Confirmation on the EXACT locked closed-interval CORE′ (n = 4M+31) is
in flight (e165b_M256_core, round 11 at 122s — tracking the original's
trajectory, which verdicted at round 18); expect it within the hour.

## In flight (batch 1, launched 00:00 UTC via launch_heroic.sh)

| job | log | state at 00:45 | expectation |
|-----|-----|----------------|-------------|
| e165 M=256 FULL support (n=1792) | e165_M256_full.log | round 45, 13.5M clauses | the unrestricted record; hours–1 day |
| e166 c3 M=2048 | e166_c3_2048.log | round 88, 26.4M clauses, viol ~2M flat | days; UNSAT predicted (mod-8) |
| e166 c3 M=4096 | e166_c3_4096.log | round 171, 51.3M, viol ~8.4M FLAT | days+; plateau concerning → hedge below |
| e166 c3 M=8192 (cap 500k) | e166_c3_8192.log | round 109, 54.5M, viol 25M→21M declining | weeks; the largest-ever attempt |
| e166 og M=2048 | e166_og_2048.log | round 82, 24.6M clauses | days; finishes og_12's 2019-rounds-no-verdict attempt |

## Batch 2 (launched 00:50 UTC via launch_heroic2.sh, this session)

| job | log | purpose | expectation |
|-----|-----|---------|-------------|
| e165b M=256 core-closed (n=1055) | e165b_M256_core.log | definitional exactness vs notes/64 | ~15–25 min |
| e165b M=512 core-closed (n=2079, 4.3M ordervars) | e165b_M512_core.log | record extension 2× | hours |
| e165b M=1024 core-closed (n=4127, 17M ordervars) | e165b_M1024_core.log | moonshot 4× | days; may not land |
| e166 c3 4096 --seed-w 128 --cap 1M (32.6M seed) | e166_c3_4096_h2.log | hedge vs viol plateau | days |
| e166 c3 8192 --seed-w 64 --cap 2M (16.5M seed) | e166_c3_8192_h2.log | hedge, faster accumulation | days–weeks |

Monitors: tail the VERDICT lines; every SAT verdict self-checks its
witness (check=OK or hard exit 2).  Nothing needs babysitting; pod
costs $0.22/hr.  If the box wedges: RunPod pod id wb23t7m7x3wog0,
API key in memory/runpod-access.md.

## Delta log (append verdicts here)

- 2026-08-29 00:13 UTC: e165 M=256 core (2,2,2) **UNSAT** [930s, 18
  rounds, 5.4M lazy clauses] — the record attempt landed first try.
