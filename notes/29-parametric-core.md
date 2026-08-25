# 29 — Parametric skeleton of the OG(M) triple-MUS (task P3)

Goal: does the minimal AP-triple core of the order gadget OG(M) follow a
single parametric family valid for all M >= 40, expressed in anchor
coordinates?  Anchor forms used (each value v in (M, 2M], v = (pM+q)/4):

| p | form        | exists iff            |
|---|-------------|-----------------------|
| 4 | M + a       | always                |
| 5 | (5M + a)/4  | a ≡ -M (mod 4)        |
| 6 | (3M + a)/2  | a ≡ M (mod 2)         |
| 7 | (7M + a)/4  | a ≡ M (mod 4)         |
| 8 | 2M - a      | always                |

A pattern that matches concrete MUS triples at two distinct M must be an AP
*identically in M*, which forces p1 + p3 = 2·p2 (e92 enumerates only these).

## Data

- e90 deletion-MUS rerun at 18 values: M = 40..56 (all), 60
  (`data/og_mus_M.log`; sizes 48..120).  M=40 reproduces the known
  59-triple MUS.
- e92 (`data/parametric_core.log`, `data/parametric_core.json`): anchor
  representations + intersections by residue class mod 4.
- e93: NO triple is in *every* MUS at any tested M (removing any single
  triple from the full instance leaves it UNSAT) — the refutation has many
  interchangeable supports, so deletion-MUS membership is a noisy signal.
- e94/e94b/e94c/e94d: order-independent *positive certificates* of
  "t lies in SOME MUS of OG(M)":
  - protected deletion: minimize everything except t, then check S−{t} SAT
    (⇒ S is a MUS containing t);
  - randomized-order variants (10–25 shuffles);
  - grow-witness: random maximal satisfiable A ⊆ F−{t} with A ∪ {t} UNSAT
    (⇒ any MUS of A∪{t} contains t).
  Logs: `data/og_pat_M.log`, `og_pat1_*`, `og_pat2_*`, `og_pat3_*`,
  `og_grow_*`.

## Result 1 — the seven-pattern skeleton on M ≡ 0 (mod 4)

The deletion-MUSes at the target set {40, 44, 48, 52} share EXACTLY these 7
anchor patterns, and every one carries an in-some-MUS certificate at **all**
tested M ≡ 0 (mod 4), i.e. 40, 44, 48, 52, 56, 60:

| # | pattern | M=40 instance | role |
|---|---------|---------------|------|
| F1 | (M+1, (3M−6)/2, 2M−7)   | (41, 57, 73) | bottom b₁ → mid → guard t₇ |
| F2 | (M+5, (3M+2)/2, 2M−3)   | (45, 61, 77) | b₅ → mid → t₃ |
| F3 | (M+7, (3M+2)/2, 2M−5)   | (47, 61, 75) | b₇ → mid → t₅ |
| F4 | (M+17, (3M−2)/2, 2M−19) | (57, 59, 61) | tight sub-mid spoke, step (M−36)/2 (2 at M=40, 12 at M=60) |
| F5 | (M+19, (3M+14)/2, 2M−5) | (59, 67, 75) | wide spoke into t₅ |
| F6 | ((3M−2)/2, (3M+6)/2, (3M+14)/2) | (59, 63, 67) | step-4 midpoint chain |
| F7 | ((3M+2)/2, (7M−16)/4, 2M−9) | (61, 66, 71) | mid → ¾-point → t₉ |

Shape census: 5 of 7 are **bottom→mid→top spokes** (M+a, (3M+a′)/2, 2M−a″)
with the identity a′ = 2(a − a″)+… (consistency: a′ = a − a″ in mid-units:
q₄ + q₈ = 2q₆), 1 is a **midpoint chain**, 1 is a **mid→¾→top** triple.
The (5M+a)/4 quarter-point form appears in NO shared pattern — the skeleton
lives on {bottom, midpoint, ¾-point, top} anchors only.

F1, F2, F6 are certified at *every* tested even M (40–60), including the
≡ 2 (mod 4) class.

## Result 2 — parity dependence

- **Hard arithmetic locks.** Every one of F1–F6 uses a midpoint anchor with
  even offset ⇒ instantiable only for even M.  F7 uses (7M−16)/4 ⇒
  instantiable only for M ≡ 0 (mod 4) (verified non-instantiable at
  M = 42, 46, 50, 54).  So NO exact pattern is common to all M: the
  all-18-M intersection is empty, forced by parity of the anchor forms.
- **Residue-class analogues.** Each class has its own offset variant of the
  same shapes (from e92 class intersections):
  - M ≡ 1 (mod 4): (M+17, (3M+9)/2, 2M−8); mid-chain ((3M−7)/2, (3M+1)/2,
    (3M+9)/2) (step 4); also (M+2,(3M+1)/2,2M−1)-type spokes at {41,45}.
  - M ≡ 2 (mod 4): spoke (M+7, (3M−8)/2, 2M−15); step-1 mid-chains
    ((3M−8)/2, (3M−6)/2, (3M−4)/2) — consecutive integers at the midpoint.
  - M ≡ 3 (mod 4): spokes (M+3, (3M+3)/2, 2M+0), (M+19,(3M+3)/2,2M−16)…;
    many step-4/step-8 mid-chains through (3M+3)/2; mid→¾→top
    ((3M+3)/2, (7M−13)/4, 2M−8).
  The **shape families are parity-free**; only the small offsets a shift
  with M mod 4 (mid offsets change parity with M, ¾ offsets track M mod 4).
- Pure bottom-chains (M+a, M+a′, M+a″) and pure top-chains appeared in the
  odd-class intersections only; no parity-free exact pattern exists because
  every shared pattern touches the midpoint or ¾-point.

## Caveats / open

- Certificates are one-sided.  Unresolved (no witness found; NOT proof of
  absence): F3 at {42, 50}, F4 at {42, 50}, F5 at {46, 50}.  All other
  (pattern, even-M) pairs are certified.
- e93: no "critical" (every-MUS) triples exist, so any parametric proof
  skeleton must argue with a *family* of interchangeable triples, not a
  unique core.  The 7-pattern skeleton is a canonical choice that provably
  embeds in a MUS at every tested M ≡ 0 (mod 4).
- The 7 patterns alone are far from UNSAT (a MUS needs ~50–120 triples);
  they are the *invariant* part, the complement varies with M.

## Takeaway for the NO-proof

Work in the class M ≡ 0 (mod 4) (dyadic blocks satisfy this: M = 2^k).
There the parametric skeleton {F1…F7} is stable across all tested scales,
built entirely from the four anchors {M+a, (3M+a)/2, (7M+a)/4, 2M−a} with
|a| ≤ 19.  A human-readable refutation should route the b_j-vs-guard
contradiction (note 28) through these seven parametric triples plus
residue-uniform filler chains around the midpoint.
