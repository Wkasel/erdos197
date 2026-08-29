# 67 — FRONT MAXSAT: core-guided lower bounds on v* (e172)

Task: GAP-V* (notes/54 §2) needs the price curve v*_c(M) bounded from
BELOW at scales where near-critical decision queries are hopeless
(bal@24: v = 4 UNSAT in 5.9 h, v = 16 decision TIMEOUT at 22 h;
brackets stuck at v*(bal,24) ∈ (4, 65], v*(bal,32) ∈ (2, 368]).
Reformulate the min-violations structure of the budget instance as
MaxSAT and harvest CORE-GUIDED lower bounds: RC2 certifies a
monotonically growing LB on the optimum long before solving it, one
UNSAT core at a time — anytime lower bounds instead of unattainable
decisions.

Machine: experiments/e172_maxsat_lb.py → data/e172_maxsat_lb.jsonl
(streaming; every bump timestamped), data/e172_{tag}.json, logs
data/e172_bal_M{16,16p,24,32,40}.log (local calibration + pod).

## 1. The instance and the exact objective relation

e172 keeps e127's encoding VERBATIM as the hard part — guarded APs
(both monotone directions, full window (M, 8M]), complete per-team
transitivity, per-team block balance cards, one-way inversion-indicator
semantics (color ∧ color ∧ order → x) — and replaces the per-team
budget cardinality by SOFT unit-weight clauses {¬x} over both teams'
indicators.  The MaxSAT optimum is therefore

    s*_c(M)  =  min { inv_A + inv_B :  coloring meets bounds c,
                      both orders monotone-AP-free }

(the minimum TOTAL adjacent-seam inversion count; in any model
#x-true ≥ actual inversions and the honest setting achieves equality).

**The objective is max, not sum — the exact translation.**  The
symmetric price is v*_c(M) = min over models of max(inv_A, inv_B).
Both directions of the relation, each one line:

  (i)  every model has inv_A + inv_B ≥ s*, so
       max(inv_A, inv_B) ≥ ⌈s*/2⌉; hence U(M; c; v, v) is UNSAT for
       every v < ⌈s*/2⌉, i.e.  **v*_c(M) ≥ ⌈s*_c(M)/2⌉** — and the
       same holds for every intermediate certified LB s ≤ s*:
       **v*_c(M) ≥ ⌈s/2⌉**.  This feeds Theorem LT verbatim
       (notes/54 Cor. D1/Lemma M(a): max_T Inv_T(N) ≥ v*_c(N) ≥
       ⌈s/2⌉ at every qualifying Case-2 anchor N = M).
  (ii) a min-max model pays ≤ v* per team, so s* ≤ 2 v*_c(M).
       Together: **s*_c(M) ∈ [v*_c(M), 2 v*_c(M)]** — the sum route
       loses at most a factor 2, and the RC2 LB stream is a valid
       v*-LB stream after halving.
  (iii) bonus on OPT: the optimal-sum witness's own max is an UPPER
       bound on v*_c(M) (any model's max is).  So a completed RC2 run
       brackets v* from both sides: v* ∈ [⌈s*/2⌉, max(witness)].

Per-team soft minimization is useless by itself: the asym/majb rows
(notes/47 §4) are SAT at v = 0, so min_models inv_T = 0 for either
single team — the SUM is the only objective with a nonzero floor,
exactly as the two-sidedness verdict predicted.

**Soundness of the LB stream.**  RC2's cost after each processed core
is a lower bound on the optimum of the CURRENT (reformulated) formula,
which is weight-equivalent to the input WCNF (standard RC2 invariant:
each relaxation is cost-preserving).  No solver-trust beyond the same
CDCL kernel every decision run already trusts; each bump's core is
logged (size + the seam pairs of its original soft literals when ≤ 16)
as an auditable certificate chain.  Independent cross-checks: (a) the
local and pod M = 16 runs are separate processes/machines; (b) OPT
models are re-audited by e127's independent audit() (bounds,
AP-freedom, inversion recount) and must satisfy #inv = cost; (c) the
LB trajectory must respect the known decision verdicts (UNSAT at v ⇒
s* > v… strictly: max ≤ sum, so decision-UNSAT at symmetric v forces
s* ≥ v+1; SAT witnesses cap s* ≤ inv_A + inv_B of the witness).

## 2. Calibration at M = 16 (v*(bal,16) ∈ {5,6} known)

Prediction committed before the runs: s*(16) ∈ [5, 12] (§1(ii) with
the known bracket), and the LB stream should clear 5 quickly and land
near 2·5-ish if the two teams' prices are balanced at the optimum.

RESULTS-16 (filled as the runs land; see §4 table)

## 3. The runs (2026-08-29, launched 23:32 UTC on the pod, nice 15)

- bal@16 local (tag bal_M16) + pod (bal_M16p, 12 h cap) — calibration
  and cross-machine agreement;
- bal@24 (bal_M24, 48 h cap), bal@32 (bal_M32, 48 h), bal@40
  (bal_M40, 48 h) — the growth measurement GAP-V*-growth needs;
  every LB bump streams to the jsonl even if the process is killed.
- RC2 settings: g3 oracle, adapt + exhaust + minz, trim 0.  The
  first oracle call assumes all indicators off (= the v = 0 instance
  for both teams), so the stream starts from the e120/e127 core.

Early observation (minutes in): the MaxSAT route reaches the small
LBs far faster than the corresponding decision queries — bal@16
sum ≥ 2 in 5 s (the v = 2 decision UNSAT took 244 s in e127),
sum ≥ 3 in 26 s.  Assumption cores localize; cardinality networks do
not.  Whether the speedup persists into the interesting range is the
run's own question.

## 4. LB trajectories (the deliverable)

News thresholds per scale (from the pre-existing decision brackets;
consistency floors the stream MUST clear, novelty levels where it
beats every known bound):

| M  | known v* bracket        | consistency floor s ≥ | first NEW sum LB |
|----|-------------------------|-----------------------|------------------|
| 16 | {5, 6} (decisions)      | 5 (s* ≥ v*)           | OPT itself + witness-max (could pin v* = 5 or 6 exactly) |
| 24 | (4, 65]                 | 5                     | s ≥ 11 ⇒ v* ≥ 6; each +2 in s bumps the v*-LB by 1 |
| 32 | (2, 368]                | 3                     | s ≥ 7 ⇒ v* ≥ 4 |
| 40 | — (never measured)      | —                     | every bump (first bal@40 data ever) |

A stream that STOPS below its consistency floor at OPT would falsify
the encoding (s* < v* is impossible) — a built-in audit.

(trajectories filled from data/e172_maxsat_lb.jsonl as bumps land)

## 5. What feeds forward

- Every row "bal@M: s ≥ σ" is, by §1(i) + notes/54 Cor. D1, the
  theorem-grade statement  max_T Inv_T(M-anchor) ≥ ⌈σ/2⌉  for every
  valid balanced-profile pair — the v* wall is bypassed for LOWER
  bounds; decisions are only needed for upper bounds now.
- GAP-V*-growth's measurement changes character: instead of one
  near-critical decision per scale, one anytime run per scale with a
  monotone certified curve; growth of the ⌈s/2⌉ stream across
  M = 16/24/32/40 is the pump measurement.
- If the streams flatten at small constants while SAT witnesses stay
  far above, the truth is likely BOUNDED v* (notes/54 degenerate
  branch → notes/47 §5.4 fallback: attack DNP(v̄−1) as a positional
  covering invariant); if they keep climbing with M, GAP-V*-growth
  gains its first real trajectory.
- **Sum-LBs are the better SCHEMA target too (GAP-V*-schema).**  The
  max objective needs cardinality reasoning; the sum objective is
  ADDITIVE over disjoint certificates: if the window contains
  value-disjoint sub-structures S_1..S_k such that every coloring
  meeting the bounds forces ≥ 1 inversion with both members inside
  S_i (an UNSAT sub-core in the restriction sense), then s* ≥ k by k
  independent restrictions — no counting network, exactly an N2-style
  rung family repeated k times.  RC2's early behavior is the machine
  shadow of this: its pre-relaxation cores are soft-disjoint by
  construction, so the first phase of every stream IS a disjoint-core
  certificate.  CAVEAT that shapes the hand target: the sub-cores
  must inherit their hypotheses from the WINDOW's bounds (arbitrary
  value subsets inherit color counts, not balance), so the natural
  candidates are bound-free forcing patterns — e.g. Lemma-K-style
  prefix chains (notes/62 §4d) and the H-edge-injectivity floor
  (notes/47 §3), both of which charge inversions without any balance
  hypothesis on the sub-structure.  A k(M) → ∞ family of these =
  GAP-V*-growth proved.  The measured core anatomy (core_pairs in the
  jsonl once cores shrink) is the mining ground.
