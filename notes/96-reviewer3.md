# Reviewer 3 — pre-arXiv patch source text

Third external reviewer, fresh context, read the compiled PDF. Verdict: the
load-bearing chain (Theorem `thm:ogred` ⟹ Theorem `thm:c3core` ⟹
Theorem `thm:main`) has **no fatal flaw**. The manuscript nevertheless ships
several lemmas that are **false as stated** (missing AP-free hypotheses) and
several unfinished exploratory sections that must not appear in v1 as
mainline mathematics.

This file records the reviewer's verbatim replacement text so the patch is
auditable. The execution log is `notes/95-prearxiv-patch.md`.

---

## Abstract (verbatim replacement, ~1,423 characters)

> Call a permutation of a set of positive integers admissible if it contains
> no increasing or decreasing three-term arithmetic progression in position
> order. Davis, Entringer, Graham, and Simmons proved that the positive
> integers are not admissibly permutable, partitioned them into three
> admissibly permutable sets, and asked whether two sets suffice. We study
> the canonical dyadic candidate S_A = ∪_{k≥1, k even} (2^{k−1},2^k]. We
> establish several structural restrictions on admissible permutations,
> including an orbit obstruction, an asymmetric balance law, and the
> impossibility of placing all sufficiently large dyadic blocks as
> contiguous runs. For the main result, we reduce admissibility of S_A to
> feasibility of an order gadget on (M,2M]: the order must avoid monotone
> three-term progressions and satisfy fifteen precedence constraints induced
> by the values 15 and 16. We then prove that a three-constraint core of
> this gadget is inconsistent for every M ≡ 0 (mod 8), using zigzag
> propagation on arithmetic-progression ladders, a transfer lock, and
> mirror-flood induction. Since every relevant dyadic scale lies in this
> residue class, S_A admits no admissible permutation. Thus the canonical
> dyadic partition does not solve the two-set problem, which remains open.
> Independent SAT encodings and certificate checks provide auxiliary
> verification of the human-readable proof.

## Ladder toolkit — required hypothesis restatements (verbatim)

**Zigzag.** "Let ≺ be an AP-free linear order of an interval containing the
d-ladder w_0,…,w_r. Suppose w_e ≺ w_{e'} for some |e−e'| = 1. Then every
rung w_i with i ≡ e (mod 2) precedes each of its existing neighbors."

**Phase dichotomy.** "Let ≺ be an AP-free linear order of a d-ladder
w_0,…,w_r with r ≥ 1. Then the ladder is globally in exactly one of its two
zigzag phases: either all even-index rungs lead their existing neighbors, or
all odd-index rungs do."

**Transfer lock.** "Let M be even, M ≥ 12, and let ≺ be an AP-free linear
order of (M, 2M]. On the odd d = 2 ladder …" (rest of the existing statement
unchanged).

**Flood.** Begins "Let ≺ be an AP-free linear order of (M, 2M]. Let C be the
residue class r mod g …". Also: the ill-typed congruence
`c ≡ C + g/2 (mod g)` must read `c ≡ r + g/2 (mod g)`.

## Orbit obstruction — missing tail condition (verbatim)

> Let q be the largest position of an element of F in the permutation. Since
> the u_k are distinct, only finitely many occupy positions at most q; and
> since u_k → ∞, eventually u_k > max F. Choose K so that, for every k ≥ K,
> pos(u_k) > q and u_k > max F. Then f_k < u_k and pos(f_k) < pos(u_k), so
> the pair (f_k, u_k) is increasingly placed …

## Class-sink algebra — the surviving fragment (verbatim)

> For m = 2^k, the map φ_r(b) = 2b − r on Z/mZ is conjugate to doubling
> under b ↦ b − r; hence every orbit eventually reaches the unique fixed
> point r.

(No scheduling conclusions are to be drawn from it in v1.)

## Other prescribed strings (verbatim)

- g_256(64): "The equality g_256(64) = 153 means that at least 153 − 42 = 111
  of the 128 values in (128,256] precede the last-placed member of
  S_A ∩ [1,64]."
- Order gadget, odd block above: "All other completions lie above 2M; at the
  dyadic scales used in Theorem [ogred], they lie in the intervening odd
  dyadic block and hence outside S_A."
- DEGS-via-chunks domain: "The definitions and Theorem [chunk] hold verbatim
  with S_A replaced by any countable set S ⊆ Z^+. Applying that formulation
  to S = Z^+ gives:"
- Empirical remark opening: "Three recurring computational observations
  across the tested scales shaped the proof…"
- Schema-instance count: "The parametric proof was machine-executed over a
  large finite range of scales by three independent checking layers."
- Reproducibility: header chain "paper/main.tex: thm:ogred -> thm:c3core ->
  thm:main"; DRAT line "CaDiCaL proof logging through pysat Cadical153";
  Data Availability "reproduce.sh reruns the load-bearing verification stack
  for the main theorem".

## Structural prescriptions

- DELETE "Suffix-stacked class deferral" and "Historical note:
  suffix-stacked deferral"; keep only the class-sink algebraic fact above,
  as a short remark.
- MOVE the Negative Atlas and Displacement Ladder material into an appendix
  titled "Computational observations and conjectures", explicitly labelled
  as finite-scale observations.
- Balance law: drop the O(1) — for u ∈ (v,2v), 2v − u ∈ (0,v) exactly.
- Section order: Introduction and definitions → General obstructions →
  Contiguous-block result → Order-gadget reduction → C3 proof and main
  theorem → Machine verification and data availability → Appendix (chunk
  reduction + computational observations).
- Front matter: machine-assistance disclosure moves out of the author
  footnote into an "Acknowledgments and computational assistance" section;
  `\date{August 2026}`.
