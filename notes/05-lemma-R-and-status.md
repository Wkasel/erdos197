> **SUPERSEDED IN PART — ONE PROVEN-LIST ITEM KNOWN FALSE AS
> STATED.**  The "PROVEN (hand)" list below includes
> "Balanced-placement law + record corollary (notes/04)" — the
> symmetric balance bound is FALSE as stated there; the corrected
> asymmetric version is paper/main.tex lem:balance (see the
> notes/04 banner).  Lemma R, the orbit lemma, the round-robin
> marginality, and the contiguous-block descent stand.  (Review
> remediation notes/88 item 4.)

# Lemma R (proved, human-checkable)

**Lemma R.** For W ≥ 5 there is no arrangement of [1, W] that (i) contains no monotone 3-term AP and (ii) places w before u whenever u ≥ 2w ("ratio-2 pairs ascend"). More generally any set containing {k, 2k, 3k, 5k} admits no such arrangement.

*Proof.* Forced ascents: k≺2k, k≺3k, 2k≺5k (all ratio ≥ 2). The AP (k, 2k, 3k) with k≺2k and k≺3k forces 3k≺2k (else k,2k,3k increasing). Then 3k ≺ 2k ≺ 5k gives 3k≺5k, and k≺3k≺5k is the increasing AP (k, 3k, 5k). ∎

(SAT confirms: W=4 SAT, W ≥ 5 UNSAT — hand proof matches. First fully human-checkable impossibility gadget of the project.)

Where it arose: analyzing the "fatal zone" lemma (block (M,2M] with pre-placed zone (M/4,M/2] is UNSAT — machine-verified for M = 16..256). Chasing the cascade: with nothing placeable below, top runs must be arranged with all deep descents banned, which is R-structure → dead. The remaining work for a full hand proof of Lemma F (fatal zone, all M) is the bridging argument (formalizing "early phase ⊆ top region ⇒ R-structure applies"). SAT certificates exist for M ≤ 256; the theorem is safe to build on, proof debt noted.

# Consolidated state of Erdős #197 attack (end of session 1)

PROVEN (hand):
- Orbit Obstruction lemma (notes/03A).
- Balanced-placement law + record corollary (notes/04).
- Lemma R (above).
- Interval round-robin marginality: s=2 requires (r−1)²<0 (notes/01).
- In any contiguous-block schedule some own block k+2 plays after own block k (infinite-descent argument) ⇒ fatal zone applies.

MACHINE-VERIFIED (SAT, exact):
- Fatal zone UNSAT for M = 16, 32, 64, 128, 256.
- All 14 alternating interval growth schemes die by block 5.
- Dyadic per-block system: SAT at M=2,4,8, UNSAT at 16 (minimal core = 15 of 16 values).

STRUCTURAL CONCLUSIONS:
- Any YES-solution requires non-contiguous, delayed, non-scale-monotone placements (reservoirs) — all "greedy in scale" schedules are impossible.
- Full-problem prefix SAT (e7) is SAT at all tested N (finite prefixes cannot detect the infinite obstruction; exploration tool only).

OPEN THREADS (next session):
1. Close Lemma F bridge → theorem: "no contiguous-block solution exists" (paper-grade partial result).
2. NO-direction: balance law + two-team completion-absorption accounting toward α(3) + β(3) < 1 (would fully resolve #197 = NO). Check LV's original paper (paywalled; reconstruct proofs).
3. YES-direction: automatic-sequence synthesis with genuine reservoirs (delay-classes as automaton states); prefix SAT solutions as seeds.
4. Write up Lemma R + orbit lemma + interval impossibility as a short paper draft ("Structural obstructions for the Erdős–Graham two-set permutation problem") — worth posting regardless of final resolution.
