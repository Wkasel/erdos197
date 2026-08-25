# notes/32 — What exactly flips at mod 8 (e100, task M3)

Setup: interval (M, 2M], AP-freeness; six values t5=2M-5, t3=2M-3, t10=2M-10,
b3=M+3, b5=M+5, b6=M+6; C3 axioms A1: t5<b5, A2: t3<b6, A3: t10<b3
("x<y" = x before y in T). Failed-literal probing of all 15 pair orders among
the six, under AP-freeness + each subset of C3, M = 40..120 step 4
(lazy transitivity, Cadical assumptions; experiments/e100_flip.py,
data/e100_flip.json). Key claims re-verified with an independent eager
full-transitivity encoding at M = 48, 52, 56, 60.

## Headline (the cleanest statement)

**For M ≡ 0 (mod 8), any TWO of the three C3 axioms force the NEGATION of
the third.** For M ≡ 4 (mod 8), no 2-subset forces anything residue-sensitive.
Stable across every swept M in each residue class (11 values at r0, 10 at r4).

- A1+A2 ⟹ b3<t10 (¬A3) at r0; at r4, A1+A2 force nothing beyond their units.
- A1+A3 ⟹ b6<t3 (¬A2) at r0; nothing extra at r4.
- A2+A3 ⟹ b5<t5 (¬A1) at r0; the *only* residue-sensitive literal for this pair.

## Forced sets (identical at every swept M in the residue class)

| subset | forced @ r0 (beyond units) | forced @ r4 (beyond units) |
|---|---|---|
| A1, A2, A3 alone | — | — |
| A1+A2 | b3<b6, b3<t10, b5<b6, t3<t10, t5<b6, t5<t10 | — |
| A1+A3 | b6<b3, b6<b5, b6<t3, t10<b5, t10<t3, t10<t5 | — |
| A2+A3 | b5<b3, t10<b6, t3<b3, t3<t5, **b5<t5** | b5<b3, t10<b6, t3<b3, t3<t5 |

Reading of A1+A2 @ r0: t10 becomes a *sink* among the six (everything forced
before t10 that can be: t5<t10, t3<t10, b3<t10) and b6 nearly so
(b3<b6, b5<b6, t5<b6). Symmetric for A1+A3 (roles of A2/A3, b6/b3, t3/t10
swapped: b6 and t3 become sinks). So the invariant's shadow is a forced
tail-ordering among the six, not just the single negated axiom.

## Invariant's shadow — the minimal flip

The minimal-diff 2-subset is **{A2, A3}**: its forced set differs between
residues by exactly ONE literal, **L = (b5 < t5) = ¬A1**, forced at
M ≡ 0 (mod 8), free at M ≡ 4 (mod 8). Note A2+A3 is intrinsically the most
binding pair — it forces 4 extra literals residue-independently
(b5<b3, t10<b6, t3<b3, t3<t5); only ¬A1 is residue-sensitive.

## Sanity / consistency with machine facts

- Full C3 (A1+A2+A3): UNSAT at every swept M ≡ 0, SAT at every M ≡ 4
  (reconfirms the mod-8 dichotomy inside this sweep).
- Every single axiom alone forces nothing — the flip needs two precedences.
- Eager re-verification (M=48,56 vs 52,60): base A1+A2 SAT everywhere;
  +A3 and +(t10<t5) UNSAT exactly at r0; A2+A3+A1 UNSAT exactly at r0;
  A2+A3+(b3<b5) UNSAT at both residues. All match e100.

Artifacts: experiments/e100_flip.py, data/e100_flip.json.
