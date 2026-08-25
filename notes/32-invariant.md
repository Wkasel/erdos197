# notes/32-invariant — Invariant synthesis for the C3 mod-8 rigidity (TASK T)

Companion to notes/32-mod8-flip.md (e100).  Setup: interval (M,2M], AP-free
linear order T; t_j = 2M-j, b_j = M+j; C3 axioms A1: t5≺b5, A2: t3≺b6,
A3: t10≺b3.  Machine dichotomy: AP+C3 UNSAT iff M ≡ 0 (mod 8).
Halving h+(v) = (v+1)/2 on odds, h_E(v) = v/2 on evens (notes/31, e99);
for an AP triple with common difference d define the **act level**
ν₂(d) + 1 — the tower level at which the triple first couples the two
parity cells (it descends ν₂(d) levels intact, difference halving each
level).

Three rounds of candidate synthesis → falsification were run.  Surviving
invariants S1–S4 below; kill list at the end.  Experiments: e101, e101b,
e102, e103, e103b; data: e101_invariant.json, e101b_pair_grading.json,
e102_kernel.json, e103_coupling.json, e103b_layers.json.

---

## S1 (SURVIVES) — the graded 2-adic forcing law

**In any AP-free order of (M,2M] satisfying A2 and A3, the forced
consequences grow one layer per factor of 2 in ν₂(M):**

| layer | condition | forced literals | half-scale image under h+ (m = M/2) |
|---|---|---|---|
| 0 | ν₂(M) ≥ 1 (M even) | t3 ≺ b3, t10 ≺ b6 | 2m−1 ≺ m+2 (odd cls), 2m−5 ≺ m+3 (even cls) |
| 1 | ν₂(M) ≥ 2 (M ≡ 0 mod 4) | + t3 ≺ t5, b5 ≺ b3 | 2m−1 ≺ 2m−2, m+3 ≺ m+2 |
| 2 | ν₂(M) ≥ 3 (M ≡ 0 mod 8) | + **b5 ≺ t5 = ¬A1** | m+3 ≺ 2m−2 |

Layer 2 contradicts A1, so **AP+C3 is UNSAT at every M ≡ 0 (mod 8)** —
this is the e100 flip, now embedded in a 2-adic tower of lemmas.  Each
layer is *sharp*: its literals are free (machine: both orientations SAT)
at every swept M of smaller 2-adic valuation, including all odd M
(nothing at all is forced there).

Machine status (e101 Part A): verdicts at **every even M in 40..128**
(44 scales — covers the requested sweep {40,48,...,128} and the r4
sanity 44..124) + odd spot checks 41,45,49,53,57; lazy-transitivity
Cadical195.  Independently re-verified with an **eager full-transitivity
encoding** at fresh scales M = 72 (r0: all five literals forced),
76 (r4: layers 0–1 forced, flip free), 58 (r2: layer 0 only), 41 (odd:
none).  Extends e100 (which swept only M ≡ 0 mod 4) to the full even
grading and to odd M.

Uniqueness of the pair (e101b): the graded structure belongs to {A2,A3}
alone.  A1+A2 and A1+A3 force *nothing* beyond their units at every
even M ≢ 0 (mod 8) — all-or-nothing at the mod-8 gate (their r0 forced
sets are the e100 sink structures).  {A2,A3} is also the only pair whose
flip literal (¬A1) is within-parity, i.e. survives one halving.
(Isolated odd-class events, single samples: A1+A2 at M=43 (mod8=3)
forces {b6<b3, b6<b5, t3<b3, t3<b5, t3<t10, t5<t10}; A1+A3 at M=47
(mod8=7) forces the mirror set.  Not investigated further.)

Proof-program reading: layer 0 should be the base case (an even-M lemma
provable by direct AP/reflection arguments), and each further layer a
descent step.  But S2 constrains the form of that descent.

## S2 (SURVIVES, negative law) — no parity-projection certificate at any depth

Round-1/2 candidates tried to *prove* S1's layer 2 by projecting to the
odd class and refuting at half scale.  Both died, and the failure is
structural:

* (e101 B) The bare kernel — AP(m) + {m+3≺m+2, 2m−1≺m+2, 2m−1≺2m−2} +
  [2m−2≺m+3] (= layers 0–1 descended + descended A1) — is **SAT at every
  even m in 16..100** and every tested odd m.  Kill confirmed by subset
  tests.
* (e102) The *enriched* kernel — descend the **complete forced odd-odd
  backbone of AP+C3**: all forced literals among all odd pairs, mined at
  M = 44, 52, 60, 68 (126/234/243/392 literals), whose offset-language
  intersection is a 119-literal core stable across scales and containing
  descended A1 (t2′≺b3′) — is still **SAT at every even m in 16..64**,
  both residues of m mod 4.

Since any deeper parity-branch cell's unit theory is a sub-projection of
the level-2 one (a level-k forced literal between co-resident values
pulls back to a level-2 forced literal, and cell AP constraints pull
back to odd-only AP constraints), **no unit-projection kernel exists at
any depth**.  Every halving-recursion proof of the flip must transport
cross-parity (interleave) information.  Corroborated at the window
level: under the layer-0/1 hypotheses at scale m, the forced end-window
literal set (22 literals, e101 Part D) is *identical* for m ≡ 0 and
2 (mod 4) — unit forcing in the projection is mod-4 blind.

## S3 (SURVIVES) — the coupling-depth law k*

Classify the AP triples of the r0 refutation by act level (L_k = triples
with ν₂(d) = k−1, coupling the parity cells at level k).  Machine facts
(e103, e103b; eager encoding, per-triple selectors, Cadical cores):

* **Every layer L1, L2, L3 is necessary at every swept M ≡ 0 (mod 8)**:
  deleting all triples of any one of these layers makes AP+C3 SAT
  (M = 40, 48, 56, 64, 72, 80).
* **Prefix threshold:** k*(M) := least k with AP[act ≤ k] + C3 UNSAT.
  k* = 3 at every swept M with ν₂(M) ≥ 4 (48, 64, 80) — the refutation
  is expressible with coupling depth ≤ 3, matching "mod 8 = three
  halvings".  At ν₂(M) = 3 deeper layers are required: k*(40) = 5,
  k*(56) = 4, k*(72) = 5 (top layers necessary there; at M = 40, L4 is
  dispensable while L5 is necessary).  Sanity: at M ≡ 4 (mod 8)
  (44, 52) every prefix is SAT.
* Conjecture (3 scales each side): **k* = 3 ⟺ ν₂(M) ≥ 4**.  For the
  campaign's dyadic family M = 2^k (k ≥ 4) the clean k* = 3 law applies.
  Why exactly ν₂(M) = 3 (terminal tower: m₄ = M/8 odd) needs deeper
  coupling is open — likely the terminal level's structure must be
  simulated by deeper-d APs when it cannot be halved again.

## S4 (SURVIVES, negative law) — no bounded level-3 certificate

Deletion-minimal supports of AP+C3 at r0 grow linearly overall
(|MUS| = 74, 87, 106, 134 at M = 40, 48, 56, 64; ≈ 2.5 triples per unit
M — same phenomenon as notes/30 §4).  Crucially this holds **per
layer**: with the elimination order biased to delete high act levels
first (minimizing retained L3), the retained L3 counts are 12, 12, 21,
34, 36, 43 at M = 40..80 — linear growth.  **No fixed finite set of
level-3 coupling triples certifies the flip.**  Cross-M anchored
coordinates: only the L2 layer of the unbiased MUS shows a stable common
core (13–14 triples in both bottom- and top-anchored frames across all
four scales); L1/L3 supports share no anchored triples across scales
(caveat: single elimination order — a lower bound of 0 on commonality,
not a proof of none).

## Bonus law (from complete six-order enumerations, e98 data + check)

The crossed same-mod-8-class pairs under full C3, at SAT scales: forced
t5≺b3 and t3≺b5 iff M ≡ 0 or 3 (mod 4); forced t10≺b6 iff M ≡ 0 or 2
(mod 4); none at M ≡ 1 (mod 4).  (Read off the complete feasible
six-order enumerations, M ≤ 100.)  Killed as a *universal* lemma — it is
a per-class law.

## Kill list (exact status)

1. **K2 bare kernel** (layers 0–1 descended ⇒ flip at m ≡ 0 mod 4):
   SAT at every even m 16..100 — killed round 1 (e101 B, incl. subset
   minimality probes).
2. **K2″ enriched kernel** (full 119-literal odd backbone descended):
   SAT at every even m 16..64 — killed round 2 (e102), with the
   corollary S2 closing the whole projection family.
3. **Universal crossed-pair law** (t5≺b3, t3≺b5, t10≺b6 forced under C3
   at every SAT M): false at M ≡ 1, 2, 3 (mod 4) — killed round 3;
   survives only as the residue table above.

## Where this leaves the proof program

The human proof of Lemma OG's C3 core must now: (a) prove S1 layer 0 as
a uniform even-M lemma (base case); (b) find the *interleave-carrying*
descent mechanism for layers 1–2 — S2 says unit projection is
insufficient, S3 says coupling depth ≤ 3 suffices when ν₂(M) ≥ 4, S4
says the level-3 content is not a finite triple list, so the mechanism
must be a *structural* statement about how the two level-k suborders
interleave (candidate language: the vdC bit-reversal absorption of
paper thm:vdc, which is exactly a statement about odd-class orders mod
2^k absorbing completions).  The dyadic case may assume ν₂(M) ≥ 4 and
use the clean k* = 3 form.

## Verification pointers

* e101_invariant.py — parts A (graded law sweep), B (bare kernel),
  C (factorization audit: chain closes nowhere at r0 through the bare
  kernel; direct C3 re-checks at M = 128 UNSAT / 124 SAT), D (window
  probe).  Lazy transitivity per e89.
* e101b_pair_grading.py — A1+A2 / A1+A3 grading sweep, M = 40..64 + odd.
* e102_kernel_mine.py — odd-backbone mining at r4, offset-language
  intersection, enriched-kernel sweep.
* e103_coupling_anatomy.py — eager encoding + per-triple selectors,
  MUS by core-shrink + greedy deletion, act-level histograms,
  whole-layer drop tests, cross-M anchored stability.
* e103b_layer_bounds.py — prefix thresholds k*, exact-layer necessity,
  biased (high-act-first) MUS for L3 boundedness, r4 sanity.
* Eager independent re-verification of S1 at M = 72, 76, 58, 41: inline
  (documented in the session log; reproducible from e103b's build()).

---

## Addendum (post-TASK-P): program executed

The proof program sketched above is now carried out in notes/33 (v2):
S1 layers 0-2 are hand-proved (layer 0 by the ladder-seam-gadget of
notes/33 A.2; layers 1-2 by the transfer lemma E + flood lemma P with
the (m0, t5) interleave split), the C3 core is refuted for every
M = 0 (mod 8), M >= 16, and the interleave-transport prediction of S2
is realized exactly as stated (one cross-parity split + cross-parity
mirror APs).  See notes/33 sections 4-7; verification e113/e113b.
