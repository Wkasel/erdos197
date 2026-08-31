# notes/95 — Reviewer-3 pre-arXiv patch: execution log

Source text: `notes/96-reviewer3.md`. Target: `paper/main.tex` (plus
`reproduce.sh`, `publish/arxiv-checklist.md`, `publish/arxiv-bundle.tar.gz`).

Reviewer's verdict going in: the load-bearing chain
`thm:ogred` ⟹ `thm:c3core` ⟹ `thm:main` has no fatal flaw. Everything below
is remediation of (a) lemmas that are false as literally stated, (b)
exploratory material that should not appear as mainline mathematics in v1,
and (c) front-matter / reproducibility wording.

One commit per item. Recompiled with `tectonic` after each structural
change.

---

## Item 0 — baseline

Working tree had uncommitted reviewer-2 edits to `paper/main.tex` plus
data reruns. Committed as-is first so that every subsequent diff is
attributable to this patch.

