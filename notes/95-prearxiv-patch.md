# notes/95 — Reviewer-3 pre-arXiv patch: execution log

Source text: `notes/96-reviewer3.md`. Target: `paper/main.tex`,
`reproduce.sh`, `publish/`. Reviewer's verdict going in: the load-bearing
chain `thm:ogred` ⟹ `thm:c3core` ⟹ `thm:main` has **no fatal flaw**;
everything below is remediation of lemmas that were false as literally
stated, exploratory material presented as mainline mathematics, and
front-matter / reproducibility wording.

**Concurrency note.** A parallel session ("Adversary C", notes/93) was
editing `paper/main.tex` at the same time this patch began. It committed at
`8ed5cf8` / `c16ca92` and went quiet; work resumed only after the file was
verified stable for 3 minutes. Adversary C had already applied items 6 and
16–24, so those are verified-not-redone below. It also swept my item-1 edits
into `8ed5cf8`.

## Item status

| # | Item | Status |
|---|---|---|
| 1 | AP-free hypotheses on Zigzag / Phase / Transfer / Flood; `C + g/2` → `r + g/2` | DONE (verification below) |
| 2 | Orbit obstruction: missing tail condition | DONE |
| 3 | Explicit dyadic indexing, `block(v)`, `k ≥ 2`, Lean `N_0` | DONE |
| 4 | Delete suffix-stacked deferral; keep algebraic fact as remark | DONE (`rem:classsink`) |
| 5 | Appendix + full reorder; `F_b`, "machine, instant", softening | DONE |
| 6 | Balance law: drop `O(1)` | ALREADY DONE (Adv C, A6) — verified |
| 7 | DEGS-via-chunks domain | DONE — chose **generalize**, not delete |
| 8 | `g_256(64) = 153` interpretation | DONE (exact wording) |
| 9 | "odd block above" scoped to dyadic scales | DONE |
| 10 | Discovery remark → observed/suggested/motivated | DONE |
| 11 | Abstract replaced (1,371 chars) | DONE (one deviation: `k ≥ 2`) |
| 12 | Disclosure out of footnote → Acknowledgments; `\date` | DONE |
| 13 | `reproduce.sh` chain + `Cadical153`; Data Availability | DONE |
| 14 | Final battery | DONE (results below) |
| 15 | vdC attribution + ABJ/Nathanson refs | DONE (`Nat77` added) |
| 16–24 | Adversary A/B items A1–A11, B1–B5 | ALREADY DONE (Adv C) — all verified |

## Item 1 verification (the blocker)

The four lemmas were stated for "any linear order", which is false: a
linear order with no AP-freeness hypothesis admits arbitrary rung
orientations. Checked that AP-freeness is what each proof actually consumes:

| lemma | what the proof uses |
|---|---|
| Zigzag | "any three consecutive rungs form an AP with the middle as midpoint, so each rung leads or trails both" = the midpoint-extremal rule; then R1 and R4 |
| Phase dichotomy | orients `(w_0, w_1)`, then Zigzag — AP-freeness via Zigzag |
| Transfer lock | Zigzag only |
| Flood | R1–R4 on genuine in-block APs, zigzag alternation, transitivity |

All four are invoked only inside AP-free orders: `thm:l1` and `thm:flip`
both hypothesize "an AP-free order of `(M, 2M]`", and `thm:c3core` says "no
AP-free linear order". So adding the hypothesis strengthens nothing
downstream and breaks no use. `Zigzag`'s conclusion is now "precedes each of
its **existing** neighbors", which also fixes the endpoint rungs `w_0, w_r`.

## Judgement calls

- **Item 7**: generalized rather than deleted. Adv C had already widened
  `thm:chunk` to arbitrary infinite `S ⊆ Z^+`; added the reviewer's bridging
  sentence before `thm:degs`. `thm:degs` kept — it is short and shows what
  the chunk coordinates do to the DEGS argument.
- **Item 11**: abstract writes the union as `k ≥ 2` even, not the reviewer's
  `k ≥ 1` even. Identical sets (`k = 1` is odd); the body pins `k ≥ 2`
  everywhere per A5, and the abstract must match.
- **Item 5**: "Local realizability and the tower characterization" was moved
  to Appendix B too. The reviewer's target outline does not list it in the
  main body, and apart from the two-line tower theorem its content is
  finite-scale measurement.
- **Item 21**: no `δ ≤ 2` witness at `N = 256` exists in `data/` (notes/27
  records only `L(4) ≥ 2`), so Adv C's `L(4) ≥ 2` stands.

## Final battery

| check | result |
|---|---|
| `git status --porcelain` | empty |
| `./reproduce.sh` | ALL CHECKS PASSED, 6/6 steps, 316s |
| `tectonic --keep-logs` | no errors; **21 pages** |
| undefined / multiply-defined refs | none |
| remaining LaTeX warnings | 1 × `Underfull \hbox (badness 1107)` — one loose line in the references, cosmetic |
| `publish/arxiv-bundle.tar.gz` | rebuilt, contains `main.tex` only; 0 non-ASCII bytes |
| tag | `arxiv-v1` |

Section order now: Introduction → Definitions → General obstructions →
Contiguous blocks → Order gadget → C3 core + main theorem → Machine
verification and data availability → Acknowledgments → Appendix A (chunk
reduction) → Appendix B (computational observations and conjectures).

## Independent post-patch verification (session hand-off)

Re-checked the two items the patch agent could not confirm by grep, plus the
artifact chain, before releasing the GO.

| check | result |
|---|---|
| `[Gen26]` at the vdC statement | present — `thm:vdc` header reads "van der Corput absorption; \cite{Gen26}", followed by "This is not new: it is Lemma 2.1 of \cite{Gen26} in different coordinates" |
| `3-permutable` defined | yes — Definition at §2 (`permutable`, then "When the progression length matters we write *3-permutable*"); `thm:main` uses it with an inline gloss |
| author byline | `\author{William Kasel}` |
| bundle | single `main.tex`, byte-identical to `paper/main.tex` (sha256 matches) |
| scale coverage of `thm:main` | `thm:ogred` hypothesises `t ≥ 4`, so every invoked `M = 2^{2t-1} ≥ 128`, all `≡ 0 mod 8` and `≥ 16` — inside `thm:c3core`'s range. No uncovered scale. |

### One defect found and fixed

The data-availability paragraph cited the repository at its **mutable**
default branch. A reader arriving later would get whatever `main` had drifted
to, not the reviewed state. Replaced with the immutable tag
`arxiv-v1` (`.../tree/arxiv-v1`), plus a note that the branch may advance
past it. The tag was then **moved onto the commit containing that citation**,
so the tag the paper names contains the paper that names it — done before
anything external referenced the old tag, which was the only safe window.

Recompiled after the edit: 21 pages, no undefined refs, same single cosmetic
underfull hbox in the references.

### arXiv submission 7993526 — stale metadata found

The uploaded source and the metadata were both **pre-patch**. Three fixes:

1. **Abstract** — the live abstract still advertised "a van der Corput
   absorption theorem for odd residue classes" among our contributions.
   This is exactly the priority hazard Adversary A flagged (the result is
   Geneson's Lemma 2.1). The paper had been corrected; the arXiv field had
   not. Replaced with an abstract matching the patched manuscript.
2. **Comments** — said "17 pages" (now 21) and cited the mutable repo URL.
   Now cites the `arxiv-v1` tag and discloses machine assistance.
3. **Source** — `main.tex` replaced; arXiv recompiled with pdflatex /
   TeX Live 2025, status SUCCEEDED, "Output written on main.pdf (21 pages)",
   which independently confirms the swap landed.

Submission is staged at Preview with the Submit button live. The final click
is the author's.

## Round 2: full word-for-word verification (pre-submission)

Two independent passes over the exact arXiv-staged PDF, plus a third external
review, run because the author asked for every word to be checked before the
irreversible click.

* **Adversarial audit** (4 lenses x attribution/chain/overclaim/consistency,
  each finding attacked by 2 refuters): 4 confirmed, 1 refuted.
* **Word-for-word pass** (11 readers over all 21 pages + 1 cross-page
  consistency agent, every finding independently re-checked): 47 distinct
  findings, 14 adjudicated, **14/14 confirmed, 0 false positives**.
* **External review** independently confirmed the same three prose defects and
  supplied sharper wordings, which were adopted.

Mechanical layer was clean beforehand: 0 undefined refs, no TODO/FIXME,
no genuine doubled words, 12,085 words.

### Two findings where verification changed the answer

**The `51 forced pairs` count is CORRECT; the definition was wrong.**
A reviewer flagged `$F_6$ has 51 forced pairs` as contradicting item (a),
which restricts `x` to `B_{b-2}`. Direct computation:

| forced pairs | source of `x` |
|---|---|
| 48 | `x in B_4` only (= item (a) as written) |
| 3  | `x in B_2` |
| **51** | `x in B_2 u B_4` (all lower `S_A` blocks) |

240 AP triples inside `B_6` also confirmed exactly. `e59` iterates over all of
`S_A`, so 51 is what was actually solved and the *definition* was too narrow.
Both systems were then checked with CaDiCaL: **48-pair UNSAT and 51-pair
UNSAT**, so the argument never depended on the wider set. Fixed by widening (a)
to `x in S_A` lying below `B_b`.

**The mod-8 observation was stated backwards.** The paper said the *early*
values of `(128,256]` concentrate in one residue class mod 8 — impossible,
since a class holds 16 values and >=111 are early. Recomputed from the repo's
own `data/g256_witness.json`:

* 112 early, 16 deferred (`|S_A cap [1,64]| = 42` confirmed)
* early values mod 8: `{0:16, 1:1, 2:16, 3:16, 4:16, 5:15, 6:16, 7:16}` — spread evenly
* **deferred** values mod 8: `{1:15, 5:1}` — essentially exactly class 1

It is the *reservoir* that is structured, not the early values. Corrected to
the true, checkable statement.

### Everything corrected (24 edits, all prose/typography; no mathematics changed)

Substantive: van der Corput lemma falsely described as used (0 `\ref`s);
Section 3 "used freely later" contradicting the introduction's "Neither is
used later"; finite sweep promoted to an infinite claim at two sites;
**Geneson/Adenwalla citations paired with the wrong papers**; fatal-core
definition; mod-8 observation.

Presentation: `hyperref` loaded bare, so every reference and URL was drawn
inside a coloured link box throughout the PDF (fixed with `hidelinks`);
`S_B` italic against upright `\SA` (new `\SB` macro); bare math-mode `:`
typeset as a relation; `\prec` used ~180 lines before its definition (now
defined in section 2); stray `\mp`; `Cadical195` -> `CaDiCaL`; incomplete Lean
path; anacoluthon in the roadmap; duplicated "at every tested scale";
"reductions" -> "reduction"; "countable" -> "countably"; "triple" -> "AP
triple"; -ise/-isation normalized to the paper's -ize convention.

Result: 21 pages, 0 undefined/multiply-defined refs, one cosmetic underfull
hbox in the bibliography.
