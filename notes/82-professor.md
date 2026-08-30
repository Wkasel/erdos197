# 82 — PROFESSOR PASS: the elegance review of GAP-AFFORD″-ALT
# (pure thought; no solvers, no experiments; 2026-08-30 night)

Mandate: the NO-proof is complete except GAP-AFFORD″-ALT
(notes/80-pincer §3.4): everywhere-split colorings whose minority is
mod-4-lattice-like — unbounded-run alternating ownership, punctured
variants, gap-≥3 non-lattice variants.  Current attack = siege
(run-length thresholds, puncture budgets, catalogues).  Question:
is there an elegant kill, or certify none exists.

**VERDICT UP FRONT.  There is an elegant kill, and it is a
one-page restriction argument: direction (2), self-similarity
descent — executed not as infinite descent but as a ONE-STEP
descent onto the already-proved Case-1 chain.**  The mod-4 lattice
corner (any ownership sequence: constant, alternating, unbounded
runs, procrastinating — the entire S5-ALT siege target) and the
on-class punctured variants are DEAD with ZERO new gaps: the only
inputs are Lemma PIN [PROVED], DIAG-DENSE [PROVED], Theorem C3(p)
[PROVED, spot-audited notes/80], and a two-line affine-restriction
transport of exactly the L-NOTAIL species.  No supply cap, no
T-TEL″, no censor, no run-length threshold is needed anywhere.
Directions (1), (3), (4) FAIL as posed — each against a hard,
already-measured obstruction — but (1)'s instinct is correct one
level up and becomes (2), and (4)'s CONCLUSION (emptiness of the
lattice-like family as valid pairs) is true and is what (2)
proves.  The full proof of Theorem ALT-DEAD is §2.  What survives
GAP-AFFORD″-ALT after this note is only the non-lattice gap-≥3
residue, in a strictly sharper, 2-adically-generic form (§5).

Sources read: STATUS.md (full), notes/50 (final graph), notes/80-
pincer (AFFORD-CORNER, L-NOTAIL, S5-ALT), notes/79 (tournament +
witnesses), notes/52 (B1, PIN, DIAG-DENSE — the load-bearing
statements re-read line by line), notes/78 Part I (Theorem C3(p)
statement + status), notes/62 §4d (Lemma K, SCHED-DEAD), notes/33
(toolkit skim), paper/main.tex (thm:ogred, thm:c3core, thm:main,
thm:degs, thm:blockgranular, thm:restriction).

---

## 1. Direction (1) — AFFINE TRANSFER of the interval theorems.
## Verdict: FAILS AS POSED; correct one level up (= §2)

The hope was: an in-team d=4 run of modest length, under the
forced-first structure the anchor demands impose, dies by affine
Lemma K; R* a small explicit constant.  Two independent failures,
both already in the record:

**(1a) The anchor demands do not supply forced-first.**  Lemma K
(notes/62 §4d) needs the run's bottom k placed before the rest of
the run.  What AFFORD-CORNER actually forces per anchor is the P5
orientation: each H-triple (x, y, z) has pos(y) < pos(x) OR
pos(z) < pos(y) — a per-triple DISJUNCTION of seam inversions.  A
disjunction over cross-block pairs never pins a prefix of one run
first; the freedom to procrastinate is exactly what survived the
DNP engagement (notes/47: X-INTERLEAVE re-descends at every
anchor; positions interleave), and that refutation is final.  The
one place Lemma K fires in the corpus — SCHED-DEAD — fires under
the HYPOTHESIS vdn = 0, i.e. block order, which is the thing that
cannot be forced at ω.  Any Lemma-K-via-anchors kill would be a
DNP revival in affine clothing.  No.

**(1b) Short runs are unattackable by fixed pairs — a two-line
geometry fact.**  Let the run be R = {s, s+4, …, s+4L} (class c,
height s, length L), image interval [σ, σ+L], σ = Θ(s).  An AP
(x, y, z) with y, z in the image interval has
x = 2y − z ∈ [σ − L, σ + 2L].  A FIXED attacker pair (the T-PIN
currency) needs x = O(1), hence σ ≤ L + O(1): **a run is
reachable by fixed attackers only if its length is a positive
fraction of its height** — i.e. only at block scale.  For
sub-block runs the attacker must scale with t (T-REGRESS
territory, closed only per-schedule, notes/39).  So the posed
R*-threshold ("small explicit constant, independent of height")
provably does not exist.

**The salvage.**  What DOES transfer verbatim under x ↦ 4x + c is
not Lemma K but the entire Case-1 kill chain — Lemma PIN,
DIAG-DENSE, Theorem C3(p) — because every one of its statements
is a statement about 3-APs and order, and 3-APs are affine
invariants.  Then the "run" that dies is the full class-section
of a block (length exactly 2^{t−2} = block/4, at height 2^t —
precisely the (1b) boundary case), the forced-first structure is
supplied by Lemma PIN's pigeonhole (positions of a fixed pair are
finite — no anchor demands needed), and the run-length threshold
is R*(t) = 2^{t−2}: **the lattice family sits exactly on the
reachable boundary, and it is the family we need to kill.**  That
reframing is direction (2).

---
