# The dyadic partition cannot resolve Erdős Problem #197

**Theorem.** S_A = ⋃_{k even} (2^{k−1}, 2^k] admits no permutation of order
type ω avoiding monotone 3-term arithmetic progressions. Consequently the
canonical dyadic partition of ℤ⁺ does not witness a positive answer to
[Erdős Problem #197](https://www.erdosproblems.com/197) (which itself
remains open).

- **Paper:** [`paper/main.pdf`](paper/main.pdf) — the full proof:
  chunk reduction → order-gadget reduction (unconditional) → the C3 core
  theorem (hand proof; sharp mod-8 phase diagram).
- **One-command verification:** `./reproduce.sh` (see
  [`REPRODUCE.md`](REPRODUCE.md)) — re-runs the strict schema checker on
  every hand-proof instance, two independent cross-validators, fresh
  direct SAT checks, and verifies the DRAT certificates in
  [`data/certs/`](data/certs/).
- **Status one-pager:** [`STATUS.md`](STATUS.md).
- **Research log:** `notes/01–33` — the complete discovery trail,
  including the negative results (window death, bottom-relief death,
  compactness failure) that funneled the search to the C3 core.
- **Hand proof:** [`notes/33-og-proof.md`](notes/33-og-proof.md).

Discovery was machine-assisted (CaDiCaL / OR-Tools via
[Claude](https://claude.com)); the final proof chain is human-readable and
solver-independent, with its finitely many schema instances machine-audited
by three independently written checkers (mutation-tested in
`experiments/e117_mutation_suite.py`).

Author: Will Kasel, 2026. Questions/refutations welcome — the entire
verification stack is designed to be run by a skeptic.
