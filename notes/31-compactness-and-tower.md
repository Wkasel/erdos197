# Compactness attempt & the parity-tower program (session 8)

## Compactness/limit attempt — resolved NEGATIVE (important)
The reduction theorem needs OG(M) UNSAT for infinitely many dyadic M, all
≡ 0 mod 8, so a limit argument was natural: if OG-C3(M) were SAT for
infinitely many M, a König limit over end-anchored windows would give an
AP-free order of the band structure {q·M + a : q dyadic ∈ [1,2]} with the
three precedences. MACHINE VERDICT (e97): every fixed-denominator window is
SAT (r=1,2,3 with generous radii). So the limit exists and is satisfiable —
compactness along this presentation CANNOT close the theorem. This is the
same phenomenon as the linear support growth (~8 triples per unit M): the
finite-M infeasibility uses the full fractal density of the interval at
every scale; the obstruction is genuinely asymptotic-structural, not local.

## The surviving route: the 3-level parity tower
Facts: C3 = {t₅≺b₅, t₃≺b₆, t₁₀≺b₃} is UNSAT with AP-freeness at every
swept M ≡ 0 (mod 8) and SAT at every other residue (incl. 4 mod 8).
Mod-8 = three halvings. The halving map (restrict an AP-free order of
(M,2M] to a parity class, divide by 2) yields AP-free orders of
half-intervals; three levels deep the six axiom values occupy
residue-dependent positions — the mod-8 rigidity must be a level-3
invariant of AP-free interval orders. Program:
1. Mine OG-C3 witnesses at M ≡ 4 mod 8 (SAT side): how do witnesses
   arrange the six values; which tower cells absorb the precedences.
2. Identify the invariant I(order, level ≤ 3) with: C3 forces I = c₁,
   while AP-freeness at M ≡ 0 mod 8 forces I = c₂ ≠ c₁.
3. Prove both halves by hand (vdC absorption + halving recursion are the
   native tools). This closes Conjecture OG for the dyadic family, hence
   S_A not permutable, hence the dyadic partition of #197 fails.
