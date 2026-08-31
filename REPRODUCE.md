# Reproducibility package

Machine verification for the paper *"Structural rigidity in the
Erdős–Graham two-set permutation problem"* (`paper/main.tex`), whose main
theorem is:

> **Theorem.** `S_A` = the union of even dyadic blocks `(2^{2k-1}, 2^{2k}]`
> is **not 3-permutable**: no permutation of `S_A` of order type omega
> avoids monotone 3-term arithmetic progressions.

Consequently the canonical dyadic 2-set partition cannot witness a positive
resolution of Erdős problem #197. **Scope note: Erdős #197 itself remains
open** — this package certifies only the theorem above, i.e. the failure of
one specific partition; nothing here claims the full problem in either
direction.

The proof chain is `thm:chunk` (chunk reduction) → `thm:ogred`
(order-gadget reduction) → `thm:c3core` (hand proof that the C3 core
`{t5<b5, t3<b6, t10<b3}` is inconsistent with AP-freeness on `(M, 2M]` for
all `M ≡ 0 (mod 8)`, `M ≥ 16`; full hand proof in `notes/33-og-proof.md`)
→ `thm:main`. Every machine-checkable link in that chain is exercised by
`reproduce.sh`.

## Environment

Verified on macOS 26.5 (arm64), Python 3.11.15. Requirements:

* Python 3.11 with the exact pins in `requirements-frozen.txt`
  (the load-bearing packages are `python-sat==1.9.dev15`, which bundles
  CaDiCaL 1.5.3/1.9.5 as `Cadical153`/`Cadical195`, and `numpy`):

  ```sh
  python3.11 -m venv .venv
  .venv/bin/pip install -r requirements-frozen.txt
  ```

* A C compiler (`cc`) — used once, to build the vendored `drat-trim`
  proof checker (`tools/drat-trim/drat-trim.c`, MIT license).

* To build the paper: any LaTeX engine. This machine has no `pdflatex`;
  `tectonic paper/main.tex` works (Homebrew `tectonic`).

## One-shot run

```sh
./reproduce.sh          # full run; ~17 min wall on an M-series MacBook
./reproduce.sh --fast   # skips the M >= 512 work; ~2 min
```

Each step ends with an explicit `PASS step N` line; any failure prints
`FAIL step N` and aborts with exit code 1. The final lines of a good run:

```
ALL CHECKS PASSED   (total wall time: <seconds>s)
```

## What each step verifies

### Step 1 — hand-proof schema checker (`experiments/repro_e113_subset.py`)

Runs `e113_c3_hand_proof.py`'s rung-by-rung verifier of the notes/33 hand
proof. Every lemma application (zigzag Lemma Z, polarization, flood,
case splits I/II, FLIP) is executed with strict per-step assertions, and
each branch context passes a hypothesis-discipline `audit()`: the branch
may assume **exactly** its declared hypothesis set, and every other
ordering fact must be produced by the assertion-checked derivation
primitives (no smuggled facts). Scales: Layer-1 at `M = 12, 16, …, 100`
and `M = 512`; FLIP at `M = 16, 24, …, 104` and `M = 512`; plus the
`M ≡ 4 (mod 8)` sharpness checks (schema inapplicability where the
theorem must NOT apply). Full-scale run (`M ≤ 400` plus 512/1024):
`.venv/bin/python experiments/e113_c3_hand_proof.py`
(archived output: `data/e113_hand_proof.json`).

### Step 2 — independent closure cross-validation (`repro_e113b_subset.py`)

Re-derives every branch of the hand proof with the **independent** e109
closure engine (rules R1–R4 + transitivity fixpoint), which has no
knowledge of the proof schemas: from each branch's hypotheses alone the
engine must reach the same contradiction. Subset scales: Layer-1 at
`M = 12..60` step 4 and 128; FLIP at `M = 16..64` step 8 and 128.
Full-scale run: `.venv/bin/python experiments/e113b_closure_crossval.py`
(archived output: `data/e113b_crossval.json`).

### Step 3 — fresh direct SAT checks (`repro_sat_direct.py`)

The theorem statement checked end-to-end by the independent e115 audit
encoder (its own pair-variable order encoding + lazy transitivity
refinement; any SAT verdict is accepted only after full model validation:
total-order reconstruction, exhaustive AP scan, unit check):

| instance | expected |
|---|---|
| C3 on `(M, 2M]`, `M = 128` | UNSAT (the theorem, `M ≡ 0 mod 8`) |
| C3 on `(M, 2M]`, `M = 512` | UNSAT |
| C3 on `(M, 2M]`, `M = 132` | SAT (sharpness control, `M ≡ 4 mod 8`) |
| C3 on `(M, 2M]`, `M = 516` | SAT |

The SAT controls show the mod-8 hypothesis is doing real work — the same
harness does not manufacture UNSAT everywhere.

### Step 4 — DRAT certificates (`repro_drat_certs.py` + `tools/drat-trim`)

Both headline UNSAT instances are re-certified **from scratch on every
run**: the CNFs are rebuilt, solved by CaDiCaL with proof logging (pysat
`Cadical153`, `with_proof=True`), and the emitted DRAT refutations are
checked by the independent `drat-trim` verifier (must print
`s VERIFIED`).

> **Toolchain finding (audit A4).** The proof-logging solve deliberately
> uses `Cadical153`, not `Cadical195`: python-sat 1.9.dev15's
> `Cadical195` proof capture was found to emit an *incomplete* DRAT
> trace at large scale — at `M = 512` the captured proof ends with the
> empty clause, yet formula + lemmas do not unit-propagate to a conflict
> (drat-trim: `c conflict claimed, but not detected`; confirmed by an
> independent `propagate()` check), while the identical pipeline at
> `M ≤ 264` is complete. `Cadical153`'s file-based capture is complete
> and its proofs verify at both scales. `Cadical195` is still used where
> no proof is needed (the lazy clause-collection loop, and the direct
> solves of steps 3/5). This is exactly the failure mode independent
> proof checking exists to catch — solver verdicts are never trusted
> bare in this package.

* `M = 128` — **eager** encoding: the CNF contains the 3 C3 units, all
  8,064 AP clauses, and **all** 682,752 transitivity clauses; it is a
  complete axiomatization of "AP-free total order on `(128, 256]` + C3",
  so `s VERIFIED` certifies the statement with no side conditions.
* `M = 512` — **lazy-audited** encoding: only the transitivity instances
  collected by a lazy refinement loop are present; `audit_cnf()` then
  re-reads the DIMACS file from disk and proves every single clause is a
  C3 unit, a genuine in-block AP clause, or a syntactic transitivity
  instance — all sound for AP-free total orders — so UNSAT of the file
  still implies the full statement.

Artifacts land in `data/certs/` (`c3_M{128,512}.cnf` + `.drat`, with
`.gz` archives refreshed from the freshly verified files; DRAT output is
not byte-stable across runs, so the archives change — each committed
archive is simply the last verified run). See `data/certs/README.md` for
the variable encoding and standalone verification commands.

**Verifier note:** `drat-trim` is not packaged on PyPI or Homebrew, so
the single-file C source is vendored at `tools/drat-trim/` (from
github.com/marijnheule/drat-trim @ 2e3b2dc, MIT license); `reproduce.sh`
builds it with `cc -std=c99 -O2`. Any other DRAT checker (e.g.
`dpr-trim`, or `cake_lpr` after DRAT→LRAT elaboration with
`drat-trim -L`) can be substituted — the certificate format is standard.

### Step 5 — reduction checks (`experiments/e96_reduction_check.py`)

Machine checks for the reduction layers of the paper (`thm:chunk`,
`thm:ogred`, Normalization lemma): gadget boundary arithmetic across
scales up to `M = 8192` with brute-force well-formedness for
`M = 8..299`; exhaustive verification of the chunk case-table; attack
forcing; running-max normalization on random permutations; and a fresh
OG(128) UNSAT under an eager `O(n^3)` transitivity encoding independent
of the lazy loop used in the discovery experiments. The step passes iff
the script reports `TOTAL failures: 0`.

## File map

| path | role |
|---|---|
| `reproduce.sh` | master script (this package) |
| `requirements-frozen.txt` | exact `pip freeze` of the verified venv |
| `experiments/repro_e113_subset.py` | step 1 driver |
| `experiments/repro_e113b_subset.py` | step 2 driver |
| `experiments/repro_sat_direct.py` | step 3 driver |
| `experiments/repro_drat_certs.py` | step 4 emitter + CNF clause audit |
| `tools/drat-trim/` | vendored DRAT verifier (C source + LICENSE) |
| `data/certs/` | DRAT certificates + README |
| `experiments/e96_reduction_check.py` | step 5 checks |
| `experiments/e113_c3_hand_proof.py` | full schema checker (step 1 core) |
| `experiments/e113b_closure_crossval.py` | full cross-validation (step 2 core) |
| `experiments/e115_audit_sat.py` | independent SAT encoder (step 3 core) |
| `notes/33-og-proof.md` | the hand proof being verified |
| `paper/main.tex` | the paper (build: `tectonic paper/main.tex`) |

## Measured wall time

Full `./reproduce.sh` on an M-series MacBook (macOS 26.5, arm64,
Python 3.11.15), the end-to-end run recorded for this commit:
**1014 s (~17 min)**, all steps PASS. Breakdown: steps 0–2 ≈ 2 s
(the schema checker and closure engine are symbolic, not search);
step 3 ≈ 535 s (the two M=512-scale solves dominate); step 4 ≈ 475 s
(lazy loop + proof-logging solve + drat-trim on ~1.9M proof lines);
step 5 ≈ 3 s.

---

# Package 2: the unconditional chain (`reproduce2.sh`)

Machine layer for the chain **C3(p) → B1₀ → Lemma Q → ALT-DEAD**
(statements and proofs: `notes/89-clean-chain.md`; `paper2/main.tex`
Theorem A), plus the HSPLIT experiment in its **downgraded** reading
(review remediation, `notes/88-review-remediation.md` item 1).

```sh
./reproduce2.sh         # ~2-3 min wall; exit 0 iff every step passes
```

Extra requirement beyond Package 1: `ortools` (CP-SAT), used only by
step 5. All scripts invoked here are path-portable (paths derived from
the repo root; no absolute paths).

### What each step verifies

1. **C3(p) schema executor** (`e123_diagonal_schema.py 9`): strict
   rung-by-rung execution of the Theorem C3(p) hand proof (Layer-1,
   FLIP, complementary-class sharpness controls) at **three values of
   p** (5, 7, 9), ~100 scales each, 0 failures required.
2. **Independent C3 solver** (`e123b_diagonal_solver_xval.py 5 9 13`):
   complete AP + transitivity encoding, Cadical195, no knowledge of the
   schema; C3(p) UNSAT on the flip class, SAT on the complementary
   class, full rung UNSAT — at p = 5, 9, 13, scales up to M = 260.
3. **Sharp applicability boundaries** (`e180_diag_grow.py
   partMINMsharp`): the review-item-9 remediated audit — first-pass
   scales computed from the scan and asserted equal to the sharp
   affine boundaries (L1: first `4 | M ≥ p+7`; FLIP: in-class
   `2p+6`), with every scanned below-threshold scale checked to FAIL;
   p = 5, 13, 21.
4. **Lemma Q chart checks + B1₀ machine layer** (`e186_altclosure.py
   qverify geneson` + JSON gates): chart exactness
   `φ(Λ_c(t)) = B(t−2)` (44 cells), AP transport + midpoint-class
   (44,400 triples, both directions), C3(p)-units-⊆-rung (6 cells —
   B1₀'s a-fortiori step), fresh rung UNSAT `R(39,40;128)`, witness
   4-purity; Geneson Λ-scan gate: no full class-section above the
   boot octaves (t > 4) in the density-2/3 permutable W.
5. **HSPLIT, downgraded** (`e186_altclosure.py hsplit64 hsplit64ctl`):
   the strong-censor cells (F = 64, hor = 4096 and 2048) re-solved
   fresh; expected UNSAT.  **Interpretation (the only one licensed —
   notes/88 item 1):** every finite strong-censor corner inhabitant
   has ≥ 1 monochromatic residue-class section within the tested
   horizon.  It does NOT show inhabitants are lattices and licenses
   no ω conclusion; ALT-DEAD's applicability hypothesis (infinitely
   many 4-pure scales) remains open on this corner.

### Measured wall time (package 2)

End-to-end run recorded for this commit: **127 s**, all steps PASS
(step 2 ≈ 60 s, step 5 ≈ 58 s dominate; steps 1/3/4 ≈ 5 s total).
