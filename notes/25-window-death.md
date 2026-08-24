# The ×4-restriction principle and window death (session 5)

## Theorem (×4 restriction).
Fix window w (i.e., δ(v) = s(v) − block(v)/2 ∈ [0, w] for all v). If a
window-w stage scheme satisfying (A)+(B) exists at horizon 4N, then one
exists at horizon N.

*Proof.* v ↦ 4v embeds S_A∩[1,N] into S_A∩[1,4N], sends block j → block j+2
(so natural stage +1), preserves AP triples. Given a valid (s, orders) at 4N,
set s'(v) := s(4v) − 1 and order fiber-images by the induced order. Every
constraint of the N-instance (the 9-case table applied to its triples) is the
image of the corresponding constraint at 4N, shifted by one stage: stage
comparisons are shift-invariant, so forced pairs and triple constraints
correspond exactly, and (A)-violations would pull back. δ'(v) = δ(4v) ∈ [0,w]
preserves the window. ∎

**Corollary (window death is permanent).** Window-2 schemes are INFEASIBLE at
N = 1024 (machine: CP-SAT e61, 746s; pysat cross-check e60 running). Hence
window-2 schemes are infeasible at every horizon 4^j·1024 — so no infinite
window-2 solution exists (an infinite solution restricts to every finite
horizon).

## Machine atlas (all tonight)
| scheme family                          | verdict                         |
|----------------------------------------|---------------------------------|
| block-granular (fibers = whole blocks) | DEAD all scales (×4 embedding + F_6 base, notes/24) |
| bottom-half relief, depth 1            | INFEASIBLE at 256 (e65)         |
| bottom-half relief, depth ≤ 2          | INFEASIBLE at 256 (e66)         |
| window ≤ 2 (any deferral pattern)      | feasible 256 (merge-degenerate, Σδ=41); INFEASIBLE 1024 → dead ∀ horizons |
| window ≤ 3                             | e68 running at 1024 (fleet2)    |
| free δ ≤ 8, min Σδ                     | e69 running at 1024 (local) — always feasible via coarse merge; the QUANTITY of interest is min Σδ growth (Θ(n) ⟹ locality dead) |

## Emerging conjecture (NO-side quantitative form)
H(w) := max horizon at which window-w schemes survive. Data: H(2) ∈
[256, 1024). If H(w) < ∞ for every w (predicted pattern H(w) ≈ 4^{w+3}),
then no bounded-displacement solution exists; the remaining YES-space is
unbounded-displacement chunk structures (triangular/depth-based schemes).
The exact reduction (any solution chunks) + a proof that (A)-clean schemes
with unbounded displacement still contain fatal cores would give
**S_A not permutable** — and, with the S_B mirror + a partition-exchange
argument, potentially #197 = NO. Alternatively a single surviving structured
family at growing horizons flips this to YES. The free-δ profile at 1024
points the way.
