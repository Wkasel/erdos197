# Theorem 2: block-granular chunking is impossible (session 5)

**Theorem.** Let s: S_A → ℕ be any finite-fiber stage function whose fibers
are unions of whole even blocks, with some fiber boundary falling between
block b−2 and block b for some b ≥ 6. Then condition (B) fails: the fiber
containing block b is UNSAT. Consequently NO valid chunk structure of any
solution is block-granular (the only block-granular chunkings avoiding all
boundaries ≥ 6 have a single infinite fiber — not finite).

*Proof.* Define the fatal core F_b: variables = order of block b; constraints
= (i) forced pairs z ≺ y for every AP triple (x,y,z) with x ∈ block b−2 (a
lower fiber, placed earlier), y,z ∈ block b, z = 2y−x; (ii) non-monotonicity
for AP triples inside block b. Any fiber whose minimum block is b, in any
block-granular scheme with the boundary below it, contains F_b as a
subsystem (forced pairs come from the table's s(x)<s(y)=s(z) row; adding
more values or more constraints cannot make an UNSAT subsystem satisfiable).

Base case b = 6: F_6 is UNSAT (machine, e59: 51 forced pairs + 240 triples,
Cadical, instant; independently reproduced in e67 pairings).

Induction b → b+2: the map v ↦ 4v sends S_A into S_A (even blocks to even
blocks, block j → block j+2), preserves AP triples (4x, 4y, 4z with
4z = 2·4y − 4x), sends block b−2 → block b and block b → block b+2. Hence
it embeds F_b as a subsystem of F_{b+2} (every forced pair and triple of F_b
maps to one of F_{b+2}). UNSAT is inherited by supersystems of embedded UNSAT
systems, so F_{b+2} is UNSAT. ∎

Notes.
- This strictly generalizes Theorem 1 (contiguous-block schedules): fibers
  may now interleave internally in any way, include any number of whole
  blocks, and still die.
- Combined with the (A)-characterization (notes/23: only bottom-half values
  can be deferred out of a block) and the e65 verdict (bottom-half depth-1
  relief INFEASIBLE at N=256), the living candidates for the chunk shape are:
  (1) bottom-half relief at depth ≥ 2 (e66 running);
  (2) growing-window advancement schemes (block 2s+2's even half advanced
      into chunk s — the E*(16,2)=16 phenomenon; covered by e61 m=5 modulo
      relabeling, running);
  (3) chunk shapes with unbounded per-block spread (not yet searchable).
- NO-side program upgraded: if depth-2 relief and window-2 both die at
  growing scales with certified UNSATs, the target theorem becomes "every
  finite-fiber stage function fails (A) or (B)" — which by exactness of the
  chunk reduction IS "S_A is not permutable". The (A)-characterization
  already reduces the space to: per-block partitions into (kept, deferred ⊆
  bottom half at various depths, advanced). A complete case calculus over
  this per-block data may be within reach.
