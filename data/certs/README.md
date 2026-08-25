# DRAT certificates for C3-UNSAT

Machine-checkable unsatisfiability certificates for the C3 core of the
main theorem (see `notes/33-og-proof.md`, `paper/main.tex` thm:c3core):

> On the block (M, 2M], M = 0 mod 8, there is no total order that avoids
> monotone 3-term APs and satisfies
> A1: 2M-5 before M+5, A2: 2M-3 before M+6, A3: 2M-10 before M+3.

## Files

| file | scale | encoding | contents |
|---|---|---|---|
| `c3_M128.cnf.gz` | M=128 | eager | 3 units + 8,064 AP clauses + 682,752 transitivity clauses (ALL of them: complete O(n^3) axiomatization) |
| `c3_M128.drat.gz` | M=128 | | DRAT refutation emitted by CaDiCaL 1.9.5 (pysat `Cadical195`, `with_proof=True`) |
| `c3_M512.cnf.gz` | M=512 | lazy-audited | 3 units + 130,560 AP clauses + 1,400,000 transitivity instances collected by a lazy refinement loop |
| `c3_M512.drat.gz` | M=512 | | DRAT refutation of that CNF |

Variable encoding: elements are M+1..2M, indexed 0..n-1 (n = M); the
variable for index pair i < j is `i*n + j + 1`; positive polarity means
"element i is positioned before element j".

## What the certificates prove

* **M=128 (eager)**: the CNF is a *complete* encoding of "AP-free total
  order on (128, 256] satisfying A1-A3" (every transitivity axiom is
  present).  `s VERIFIED` from drat-trim certifies it is unsatisfiable,
  with no side conditions.
* **M=512 (lazy)**: the CNF contains only the transitivity instances the
  refinement loop needed.  Every clause in the file is audited by
  `experiments/repro_drat_certs.py::audit_cnf` (re-read from disk) to be
  a C3 unit, a genuine in-block AP clause, or a syntactic transitivity
  instance -- all of which are sound constraints for any AP-free total
  order satisfying A1-A3.  Hence UNSAT of this CNF (certified by the
  DRAT proof) implies no such order exists at M=512.

## How to verify

```sh
# build the verifier (vendored source, MIT license):
cc -std=c99 -O2 -o tools/drat-trim/drat-trim tools/drat-trim/drat-trim.c

gunzip -k data/certs/c3_M128.cnf.gz data/certs/c3_M128.drat.gz
tools/drat-trim/drat-trim data/certs/c3_M128.cnf data/certs/c3_M128.drat
#  -> must end with "s VERIFIED"

gunzip -k data/certs/c3_M512.cnf.gz data/certs/c3_M512.drat.gz
tools/drat-trim/drat-trim data/certs/c3_M512.cnf data/certs/c3_M512.drat
#  -> must end with "s VERIFIED"

# independent clause audit of the CNFs themselves:
.venv/bin/python - <<'EOF'
import sys; sys.path.insert(0, "experiments")
from repro_drat_certs import audit_cnf
audit_cnf("data/certs/c3_M128.cnf", 128)
audit_cnf("data/certs/c3_M512.cnf", 512)
EOF
```

drat-trim is not packaged on PyPI or Homebrew; the single-file C source
is vendored at `tools/drat-trim/` (from
github.com/marijnheule/drat-trim @ 2e3b2dc, MIT license), and
`reproduce.sh` builds it automatically.

## Regenerating

`.venv/bin/python experiments/repro_drat_certs.py 128 512` rebuilds both
certificates from scratch (~5 min; the DRAT files are not byte-identical
across runs -- CaDiCaL's search is not deterministic across platforms --
but each emitted proof verifies against its paired CNF).
