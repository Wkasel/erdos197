# 77 — FRONT N6a-POOL: clearing the uniformization sub-pool

Companion to notes/50 §2a/§6 (the FINAL dependency graph; this note
works its GAP-N6a sub-pool row), notes/55 (proved skeleton), notes/56
(bridge), notes/57 (DICH case tree + catalogue facts F0–F4), notes/58
(LLOP/PARM + robust chain), notes/59 (FG-schema/J-pencil/FG-deep/ASM′).
Audit baseline: notes/60/60-1/61-2 (scales through 160), notes/76.

**This note is written incrementally; every section ends with its
verification pointer and a status tag [PROVED] / [MACHINE-CHECKED] /
[GAP] / [CLEARED] / [RESISTS].**

**Overall status: `in progress`.**

## 0. The pool, the clearing bar, and the dependency order

The notes/50 §2a sub-pool (all one species — finite catalogue-schema
write-ups of machine-proved-in-instances claims):

| item | uniform claim to write up | prior state |
|------|---------------------------|-------------|
| GAP-FG-schema | sound uniform calculus covering the closure-dead fan grid; residue = RT-glue rule + cross-scale boundary audit (notes/59 §A.6) | FW covers 1467/1851 at 48; deep block q ≥ M−12 uncovered |
| GAP-FG-deep | branch-certificate schema for the closure-alive UNSAT stalls D(M); resonance law 8 \| gap; E1×E1 characterization | exact at 48 only; 55/75 certs; 20-pair core → PARM |
| GAP-DICH (5 rows, notes/57 §7) | F0 purity / F1 α-law / F2 f-law / F3 windows / F4 cascade + SPLIT finish; K* = m + 9 + max(α_E−f_O, α_O−f_E) | K* law exact at 8 scales 48..160 (2 blind); facts checked at 6 scales |
| GAP-LLOP-α/β | band-major Th1 kill; cap law C(M); arms = punctured ThW1′ / robust Lemma J | cap flat law (M+16)/2−5 survives 96..160; arms scoped, unproved |
| GAP-PARM (⊇ CORNER ⊇ FG-deep 20-pair core) | hatch + any band split dead; H-LAT lattice law, ThW0 punctured {4,6} law, S2 corner | P-ARM machine-dead 48..96 + 56; laws at m = 24..40 |
| GAP-ASM′ = (OV-∀) | K*(M) ≤ C(M) for all M ≡ 0 (16) | true at 8 scales 48..160; robust chain COV-W′ verified 128/160 |

**Clearing bar (this front).**  An item is CLEARED when (a) its
uniform statement is written exactly, (b) the schema layer behind it
is proved (hand) or reduced to named finite facts, and (c) every
uniform claim it rests on is machine-checked at TWO scales fresh for
that claim.  Items that fail (b) at day's end get exact statements
and a RESISTS tag.

**Fresh scales for this front**: full-scale claims M = 176, 192
(never touched; catalogues built this session); half-scale claims
m = 48, 56 (e155 grid ran m = 24..40); FG-deep laws M = 64, 96
(e154 classification ran only at 48).

**Dependency order worked**: FG-schema → FG-deep → DICH → LLOP →
PARM → ASM′ (each later item consumes catalogue laws of the earlier).

Machine queue discipline: one local solver at a time; bulk (e146
catalogues at 176/192, deep classification at 96) on sprint pods.

---
