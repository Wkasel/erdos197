> **SUPERSEDED — THE TARGET OF THE CONDITIONAL THEOREM IS KNOWN
> FALSE.**  The conditional extension theorem below concludes
> "S_A is permutable … #197 = YES" from Σ/P-satisfiability
> hypotheses.  S_A is now PROVEN not 3-permutable (paper
> thm:main), so those hypotheses fail from some scale on; the
> constraint calculus retains descriptive value only.  The final
> YES-inference also rode the false S_B identity (see the notes/06
> banner and notes/11 §CORRECTION).  (Review remediation notes/88
> item 4.)

# The extension lemma: full constraint calculus, a derived invariant, and a conditional proof (2026-08-24)

Task: analyze the crux question of the viability hierarchy (notes/14) — does State(X)
extend to State(4X)? Outcome, in brief:

1. A complete enumeration of the constraint families shows a sharp geometric fact:
   **every completion of an (old, new-block) attacking pair lands in the top quarter
   of the new block, and every deep attacker (x ≤ X) targets only the bottom
   sixteenth**. This forces the shape of any workable reservoir and explains the
   e43 dead branch (spread mod-8 reservoirs put mass in the attack image).
2. Under the derived invariant H (**bottom-interval reservoir + append-only
   schedule with lag-2 reservoir deferral**), the extension State(X) → State(4X)
   becomes **independent of the old order's interior**: every H-state extends to an
   H-state iff a single finite, old-order-free system Σ(X) (plus a mild interval
   system P(L)) is satisfiable. The "dead branch" phenomenon is bypassed entirely,
   and fairness (order type ω) is automatic because positions are final at placement.
3. What remains open is exactly the satisfiability of Σ(X) for all X — a concrete,
   machine-checkable family with an identified candidate UNSAT core (the "dual-duty
   top sliver"). Both outcomes are informative; §7 spells out the redirects.

Rigor note: all range computations below are hand-derived and should be
machine-audited; none has been run as an experiment in this session.

---

## 1. Notation and exact semantics

**Blocks.** $A_k := (2\cdot 4^{k-1},\, 4^k]$ for $k \ge 1$ (these are the even dyadic
blocks $B_{2k}$), $|A_k| = 2\cdot 4^{k-1}$. $S_A = \bigcup_k A_k$. Block tops
$X = 4^k$. Between consecutive A-blocks sit the B-team blocks
$(4^{k-1}, 2\cdot 4^{k-1}]$ and, above $A_k$, $(4^k, 2\cdot 4^k]$; completions
landing there are *free* (they belong to the other team's sequence).

**States.** For a block top $X = 4^k$, a *state at scale $X$* is a pair
$(\prec, R)$ where $R \subseteq (2X, 4X]$ with $|R| = \tfrac18 |A_{k+1}| = X/4$
(the *reservoir*), and $\prec$ is a linear order on the *placed set*
$$P(X) \;=\; \bigl(S_A \cap [1, X]\bigr) \;\cup\; \bigl((2X,4X] \setminus R\bigr),$$
subject to **doom-freeness**: for every pair $x \prec y$ (any relative magnitudes),
writing $z = 2y - x$ for the completion (the continuation of the progression
through $x, y$ in the direction of $y$):

- (**absorb**) if $z \in P(X)$ then $z \prec y$;
- (**doom**) if $z \in S_A \cap [1, 4X] \setminus P(X)$ (i.e. $z \in R$), the pair
  orientation $x \prec y$ is forbidden;
- if $z \notin S_A$ or $z > 4X$, no constraint. (Soundness of the last clause:
  $x, y \le 4X \Rightarrow z \le 8X - 2$, and $S_A \cap (4X, 8X] = \emptyset$
  since $(4X, 8X]$ is a B-block. So *all* team completions of in-state pairs are
  $\le 4X$: the doom horizon closes exactly at $4X$.)

Absorb subsumes 3-AP-freeness: a monotone placed 3-AP is precisely a monotone
pair whose in-set completion is placed after the pair's later element.

**Extension (restriction semantics).** $(\prec', R')$ at scale $4X$ *extends*
$(\prec, R)$ at scale $X$ if $\prec'\!\restriction_{P(X)} = \prec$. The new values
are $R$ (the old reservoir, now mandatory since $P(4X) \supseteq S_A\cap[1,4X]$)
and $N' := (8X, 16X] \setminus R'$; they may be interleaved anywhere.

**Empirical anchors** (repo): State(64) exists; State(64) with $R = \{v \equiv 1
\bmod 8\}$ does **not** extend to State(256) (e43, UNSAT 70s) — the SOME/EVERY
distinction is real. The flex-reservoir chain (e44) was inconclusive (log
truncated at the 64→256 stage). $g_{256}(64) = 153$: in every pure-complete-256
arrangement, $\ge 112/128 = 87.5\%$ of block $(128,256]$ precedes the completion
of $[1,64]$ — numerically the $7/8$ occupancy of the state shape.

---

## 2. The completions calculus: every constraint family

Fix the extension step $X \to 4X$. Partition the relevant values:
$$C = S_A \cap [1, X] \quad (\text{"deep"}), \qquad
  M = (2X, 4X] = N \cup R \quad (\text{"mid"}), \qquad
  K = (8X, 16X] = N' \cup R' \quad (\text{"new"}).$$
For a placed pair $(u \prec v)$ the completion is $2v - u$; increasing pairs
($u < v$) complete upward, decreasing pairs ($u > v$) complete downward. The
table below is exhaustive over which blocks the two placed elements lie in.
Throughout, "free" means the completion provably lands in a B-block or outside
$[1, 16X]\,\cup$ team range; "binding" families carry the constraint content.

**Increasing pairs $x \prec y$, $x < y$, $z = 2y - x$:**

| # | $x$ | $y$ | range of $z$ | status |
|---|-----|-----|--------------|--------|
| I1 | $C$ | $C$ | $z < 2X$ | binding iff $z \le X$: inherited from State(X) |
| I2 | $C$ | $M$ | $z \in (3X, 8X)$ | binding iff $z \le 4X$, i.e. $y \le 2X + x/2$; then $z \in (4X - x, 4X]$ (top sliver of $M$): inherited |
| I3 | $M$ | $M$ | $z \in (2X, 6X)$ | binding iff $z \le 4X$: inherited; $z \in (4X,6X)$ free |
| I4 | $C\cup M$ | $K$ | $z > 2\cdot 8X - 4X = 12X$ | **binding iff $z \le 16X$**, i.e. $y \le 8X + x/2$; then $z \in (16X - x, 16X] \subseteq (12X, 16X]$. **New.** |
| I5 | $K$ | $K$ | $z > y > 8X$ | binding iff $z \le 16X$ (in-block); $z \in (16X, 32X)$ free (B-block). **New.** |

**Decreasing pairs $u \prec w$, $u > w$, $z = 2w - u$:**

| # | $u$ | $w$ | range of $z$ | status |
|---|-----|-----|--------------|--------|
| D1 | $C$ | $C$ | $z < X$ | inherited |
| D2 | $M$ | $C$ | $z \le 2X - (2X{+}1) < 1$ | **always free** |
| D3 | $M$ | $M$ | $z \in (0, 4X)$ | binding iff $z \in S_A$: $z \le X$ or $z \in (2X, w)$: inherited; $z \in (X,2X]$ free |
| D4 | $K$ | $C \cup M$ | $z \le 8X - 8X < 1$ | **always free** |
| D5 | $K$ | $K$ | $z \in (2X, w)$ | binding iff $z \in S_A$: sub-cases $z \in (2X,4X]$ (mid, placed), $z \in (4X,8X]$ free, $z \in (8X, w)$ in-block. Note $z = 2w - u > 2\cdot 8X - 16X = 2X$: **decreasing completions from $K$ never reach below $2X$** — deep values are never targets. **New.** |

Two structural lemmas fall out of I4 immediately.

**Lemma A (top-quarter landing).** Every binding completion of an increasing
pair with $x$ placed-old ($x \le 4X$) and $y \in K$ lies in $(12X, 16X]$, the top
quarter of the new block. In particular, if $R' \cap (12X, 16X] = \emptyset$,
then **no (old, new) pair is ever doomed**: the only cross-scale constraints are
absorptions $z \prec' y$ with $z$ in the top quarter of $K$ (schedulable, since
$z$ is itself new), or the free flip $y \prec' x$ (whose completion is negative
by D4).

**Lemma B (deep shielding).** A deep attacker $x \le X$ binds only against
$y \le 8X + x/2 \le 8.5X$. Hence if the bottom sixteenth $(8X, 8.5X]$ of $K$ is
withheld ($\subseteq R'$), deep attackers bind against *nothing*; if it is
placed, their completions lie in $[15X, 16X]$ — absorbable, or $>16X$ — free.
Deep zones are thus never a doom source; only the immediately-preceding block
$M$ has genuine reach into $K$, and only into $(8X, 10X]$.

**Lemma C (old pairs never complete into the new reservoir).** For $a, b \le 4X$:
$2b - a \le 8X - 2 < 8X$, so no already-placed pair can be doomed retroactively
by any choice of $R' \subseteq (8X, 16X]$. Symmetrically, the doom-freeness of
State(X) says exactly that **no old monotone pair completes into $R$** — this is
the property that will let $R$ be placed arbitrarily late at stage $4X$ without
creating monotone 3-APs. The state design's doom clause is precisely the
right induction load.

**Double dooms (existence of any State(4X)).** A pair $y_1 < y_2$ in $N'$ is
unplaceable if both orientations are doomed: $2y_2 - y_1 \in R'$ and
$2y_1 - y_2 \in R'$. Then $(2y_1 - y_2,\, y_1,\, y_2,\, 2y_2 - y_1)$ is a 4-term
AP with both endpoints in $R'$ and both middles placed. **If $R'$ is an
interval, the middles lie in $\mathrm{conv}(R') = R'$, so double dooms cannot
occur.** Spread reservoirs (e.g. a residue class mod 8, which is 3-AP-rich)
must dodge this family combinatorially — a second strike against them.

---

## 3. Necessity: what any append-only extension forces on $R'$

Call a tower *append-only* if new values are never inserted before old values
(each extension appends its new material after the entire old order). This is
the strongest possible fairness discipline: $\mathrm{pos}(v)$ is final the
moment $v$ is placed, so the limit order has type $\omega$ trivially.

**Proposition 1.** In any append-only extension, $R' \cap (12X + 2, 16X] $ is
essentially empty (at most boundary cases).

*Proof sketch.* Suppose $r \in R'$, $r > 12X$. Every old $x \le 4X$ with
$x \equiv r \pmod 2$ and $x > 2r - 16X$ produces $y = (x + r)/2 \in (8X, 16X]$
with $2y - x = r$. If such a $y$ is placed ($y \in N'$), the appended pair
$(x \prec' y)$ is doomed by $r$ — contradiction. So all such $y$ must lie in
$R'$. For $r > 12X + O(1)$ the midpoint set $\{(x+r)/2\}$ meets $(8X,16X]$ in
$\gg X$ values across the mid block alone (one full parity class of
$(2X,4X]\setminus R$, i.e. $\ge 7X/8 - |R|$ values), exceeding the total budget
$|R'| = X$. ∎

So **within the append-only regime the bottom half $(8X, 12X]$ is forced**, and
by Lemma B and the double-doom analysis the canonical choice is the *bottom
eighth interval*:
$$R' \;=\; (8X,\; 9X], \qquad |R'| = X.\; \checkmark$$
This choice simultaneously: (i) kills all (old,new) dooms (Lemma A); (ii)
absorbs all deep-attack targets, since the attacked window $(8X, 8.5X]$ is
withheld (Lemma B) — segments never see attackers from more than one block
down; (iii) excludes double dooms (interval); (iv) will be seen in §4 to make
the ascent- and descent-forced windows *disjoint*.

This also retro-explains e43: the reservoir $\{v \equiv 1 \bmod 8\}$ places
$1/4$ of its mass in the top quarter $(12X,16X]$, generating doom-forced flips
$y \prec' x$ against old values at solver-chosen (hence fragile, order-dependent)
positions; the extension question then genuinely depends on the old interior,
and dead branches are expected. The measured g-witness reservoir (one class mod
8) was optimal for *delaying small values*, not for *extendability* — two
different optimization targets.

---

## 4. The invariant H and the conditional extension theorem

**Definition (invariant H / the schedule).** For $k \ge 2$ set
$$R_k := \bigl(2\cdot 4^{k-1},\; \tfrac94\, 4^{k-1}\bigr] \quad (\text{bottom
eighth of } A_k), \qquad N_k := A_k \setminus R_k = \bigl(\tfrac94 4^{k-1},\, 4^k\bigr].$$
An *H-state at scale $X = 4^k$* is a state whose reservoir is $R_{k+1}$ and
whose order has the layered form
$$\pi_k \;=\; \text{(seed)} \;\oplus\; \Sigma\text{-arr}(N_{k_0+1}) \;\oplus\;
  \Sigma\text{-arr}(N_{k_0+2}) \oplus P\text{-arr}(R_{k_0+1}) \oplus \cdots
  \oplus \Sigma\text{-arr}(N_{k+1}) \oplus P\text{-arr}(R_{k}),$$
i.e. at each stage the new block's main part $N_{j}$ is appended as one run,
followed by the reservoir of the *previous* block $R_{j-1}$ (**lag-2 deferral**:
$R_{j-1}$ is placed after $N_j$, so every segment plays against a zone that is
permanently at $7/8$ occupancy). A finite seed handles the small scales where
$|A_k|/8 < 1$.

The extension $\pi_k \to \pi_{k+1}$ appends $\Sigma$-arr$(N_{k+2})$ then
$P$-arr$(R_{k+1}$). Its validity decomposes, by the calculus of §2, into two
finite systems that **do not mention the old order at all**:

**The segment system $\Sigma(X)$** ($X = 4^k$; values $V = (9X, 16X] = N_{k+1}$,
find a linear order such that):

- **(S1) internal absorption / 3-AP-freeness.** For every increasing placed pair
  $y_1 \prec y_2$: if $2y_2 - y_1 \le 16X$ then $2y_2 - y_1 \prec y_2$. For
  every decreasing placed pair $y_2 \prec y_1$ ($y_2 > y_1$) with
  $c = 2y_1 - y_2 \in (9X, 16X]$: $c \prec y_1$.
- **(S2) zone descents.** For $y < z$ in $V$ with $2y - z \in (\tfrac94 X,\, 4X]$
  (an attacker in $N_{k}$, which is wholly placed before the segment):
  $z \prec y$. [Attackers $x \le X$ never bind: $2y - x > 18X - X > 16X$
  (Lemma B with the segment starting at $9X$); attackers in
  $(X, 2X] \cup (4X, 8X]$ are B-team; attackers in $R_k = (2X, \tfrac94 X]$ are
  exempt — they are placed *after* the segment.]
- **(S3) forced ascents.** For $u < w$ in $V$ with
  $2u - w \in (2X, \tfrac94 X] \cup (8X, 9X]$: $u \prec w$. [First window: the
  completion is in $R_k$, placed after the segment, so a descent $w \prec u$
  would leave a decreasing pair completing into later material — a monotone
  3-AP. Second window: the completion is in $R' = R_{k+1}$, unplaced team —
  doom. Note both windows are *reservoirs seen from consecutive stages*; the
  system family is self-consistent under $X \mapsto 4X$.]
- Completions of decreasing pairs into $(\tfrac94 X, 4X]$ or below $2X$-in-team
  are automatically fine ($\le 4X$-team values are placed before the segment;
  and $2y_1 - y_2 > 2\cdot 9X - 16X = 2X$ shows nothing reaches deep — D5).

**The reservoir system $P(L)$** ($L = |R_k| = 4^{k-1}/4$; offsets
$o = v - 2\cdot4^{k-1} \in (0, L]$): a 3-AP-free, internally absorbing order on
an interval with the extra *far-pair ascents*: $c \prec r$ whenever
$o_c < 2 o_r - L$ (these come from placed attackers $x \in N_k$,
$x \in [2r - \tfrac94 4^{k-1},\, 2r - 2\cdot4^{k-1})$, whose decreasing-pair
completions $2r - x$ land inside $R_k$). All other external completions of
$R_k$-pairs are placed ($\le 4^{k-1}$-team, or $N_k$, or the *earlier-placed*
$R_{k-1}$ — the append order of reservoirs matters and works out) or free.
Hand-check: $P(4)$ is satisfiable by the order $1,3,2,4$. Without clause (γ) the
plain interval system is solved by any parity-nested (bit-recursive / van der
Corput) order: for an AP with odd difference the middle has opposite parity to
the endpoints, so class-before-class places it first or last of its triple;
even differences recurse. This is the vdC absorption mechanism of notes/07 in
interval clothing; (γ) is the only novelty and looks mild.

**Theorem (conditional extension).** Suppose $\Sigma(4^k)$ and $P(4^{k-1}/4)$
are satisfiable for all $k \ge k_0$, and a valid seed exists (finite check).
Then every H-state extends to an H-state one scale up by appending witnesses,
and the union of the tower is a 3-AP-free permutation of $S_A$ of order type
$\omega$. Hence $S_A$ is permutable — and, with the parallel (scale-shifted)
construction for $S_B$, Erdős #197 = YES.

*Proof of the reduction (why nothing else binds).* Every monotone 3-AP is an
oriented pair plus a late completion, so it suffices to check every pair
category of the appended order. (a) old–old: inherited. (b) old–segment: all
increasing; completions either $>16X$ free, or in $(12X,16X] \subseteq V$
top-quarter, where they are *placed* (S1/S2 govern their position; the
constraint "completion $\prec y$" is exactly S2 when the attacker is in $N_k$
and vacuous-by-freeness otherwise — deep attackers overshoot). Decreasing
old-after-segment pairs don't exist (append-only), and segment–old decreasing
completions are negative (D4). (c) segment internal: S1–S3. (d) segment pairs
completing into $R_k$ (placed later): excluded by S3 window 1. Into $R_{k+1}$
(unplaced): excluded by S3 window 2. (e) $R_k$ appended last: no old or segment
pair completes into it (old pairs: doom-freeness of State at scale
$4^{k-1}$ — Lemma C; segment pairs: S3). Its own pairs vs earlier material:
increasing pairs $(x, r)$ with $x \le 4^{k-1}$ complete into
$(3\cdot 4^{k-1}, 4.5\cdot4^{k-1})$, i.e. into $N_k$ (placed) or the B-block
above $4^k$ (free); with $x \in N_k$, decreasing completions $2r - x$ land in
$R_k$ (handled by P's clause (γ)), in $(4^{k-1}, 2\cdot4^{k-1}]$ (B, free), in
$R_{k-1}$ (placed one stage earlier — this is why reservoirs are appended in
block order), or below (complete, placed). Pairs $(y \in N_{k+1}, r)$:
decreasing, completion $2r - y < 0$, free. (f) $R_k$ or $R_{k-1}$ as future
attackers: $r \le \tfrac{9}{16} 4^{k}$ attacks segment
$N_{k+2} = (\tfrac94 4^{k+1}, 4^{k+2}]$ only for
$y \le 2\cdot4^{k+1} + r/2 < \tfrac94 4^{k+1}$ — empty window (this is Lemma B
again: reservoirs are deep by the time the next segment plays; the lag-2
deferral is exactly shallow enough to be legal and exactly deep enough to keep
zones at 7/8). Cross-reservoir pairs $(r' \in R_{k-1}, r \in R_k)$: completion
$2r - r' > 3.4\cdot4^{k-1} > \tfrac94 4^{k-1}$, lands in $N_k$, placed. All
categories close. Fairness: append-only. ∎

**Remark (relation to prior no-go results).** (i) The no-contiguous-run theorem
(paper §5) forbids cofinitely many blocks played as *single* runs; here every
block is played as exactly two runs (7/8 + deferred 1/8) — the minimal legal
splitting. (ii) The reduced zone system $Z(M)$ (UNSAT for $M \ge 16$) differs
from $\Sigma$ in three ways, each traceable to a line of §2: the zone is only
$7/8$ full with the *bottom* eighth missing (S2's carve-out), deep zones are
absent entirely (segment starts at $9X$, not $8X$ — Lemma B), and the price is
the new ascent family S3. $\Sigma$ is *not* among the systems certified UNSAT.
(iii) Note 09's "two-phase pipelines at split ratios $s \in \{5/4, 4/3, 7/5,
3/2, 8/5\}$ all UNSAT ($m \ge 32$)": the present scheme is a 9/8-split — outside
the tested set — and, more importantly, uses **lag-2** deferral (reservoir of
block $k$ plays after segment $k{+}1$), whereas a lag-1 pipeline completes the
zone before the next segment and so faces the full fatal-zone pressure. This
distinction should be audited against e6/e13 before claiming novelty, but no
log in the repo shows a lag-2 bottom-interval scheme being tested.
(iv) Consistency with the g-data is a genuine positive signal: in the H-tower,
$S_A \cap [1,64]$ completes only when $R_3 = (32,36]$ is appended — after the
whole of $N_4 \subseteq (128,256]$, i.e. $\ge 7/8$ of the block precedes
small-completion, matching the measured optimum $112/128$ ($g_{256}(64)=153$)
almost exactly. The state shape was reverse-engineered from that witness; the
present analysis derives it.

---

## 5. Why the EVERY-state version fails, and what replaces it

The EVERY-state extension lemma is false as posed: e43 is a counterexample, and
§3 explains it structurally (reservoir mass in the attack image $(12X,16X]$
generates doom-forced insertions of new values before old values at positions
that depend on the old interior; König-style navigation then meets dead
branches). The correct statement is:

> **Every H-state extends** (to an H-state), *conditionally on the old-order-free
> systems $\Sigma, P$* — the surprise dividend of the bottom-interval reservoir
> being that the extension problem decouples from the old order entirely.

So the invariant H needs *no* condition on the interior of the old arrangement
(no class-phase discipline, no g-profile bookkeeping, no frozen-prefix
condition): H is purely (reservoir = bottom eighth interval) + (layered
append form). This is the minimal invariant of the shape requested, and it is
strictly weaker than every candidate listed in notes/14 (class-phase structure,
occupancy profiles) — those may still be needed *inside* the $\Sigma$-witnesses,
but they are quarantined there.

---

## 6. The remaining gap: is $\Sigma(X)$ satisfiable? (rigor over optimism)

Everything now rides on one finite family. Honest assessment of both outcomes.

**Structure of the tension.** Fix $y$ in the segment bottom $(9X, 10X]$. Its
top-region partners $t$ split by the sliding threshold $2y - \tfrac94X$:

- $t \le 2y - \tfrac94 X$ (i.e. $2y - t \in (\tfrac94X, 4X]$, attacker in $N_k$):
  **$t \prec y$ forced** (S2, descents);
- $t \in (2y - \tfrac94X,\; 2y - 2X]$ (completion in $R_k$): **$y \prec t$
  forced** (S3, ascents);
- $t > 2y - 2X$ (completion in the B-block $(X, 2X]$): free.

The reservoir interval makes these windows disjoint — there is no *pairwise*
contradiction (this fails for spread reservoirs, a third strike against them).
But globally, each top value $t \in (14X, 16X]$ must sit *after* all bottom
values in $(\tfrac{t + 2X}2,\, \tfrac{t + 9X/4}2]$ and *before* all bottom
values in $(\tfrac{t+9X/4}2,\, 10X]$: the tops must thread through the bottoms
in a rigidly co-monotone pattern, while S1 simultaneously forbids long
ascending runs among the bottoms (an ascending pair $y \prec y'$ of bottoms has
completion $2y' - y \in (9X, 11X]$, again a low value, which must *precede*
$y'$ — the classic anti-sorted pressure) and the whole must remain 3-AP-free.
This three-way interaction — co-monotone threading vs. anti-sorted absorption
vs. AP-freeness — is exactly the braid that all closed-form keys have failed to
capture (notes/07, 11), now isolated in a system with no dependence on
anything else. **The candidate UNSAT core, if there is one, is the top sliver
$(15\tfrac34 X, 16X]$, whose members carry both duties against interleaved
bottom cohorts.** A Lemma-R-style hand obstruction does not fire directly (all
forced ascents have ratio $< 2$; forced descents have no common third element),
and I could not derive a contradiction by hand from S1–S3; equally I could not
exhibit a witness pattern. This is genuinely open.

**Upward UNSAT propagation.** Restricting a $\Sigma(4X)$-witness to even values
and halving maps the value set $(36X, 64X] \to (18X, 32X] = 2\cdot(9X,16X]$ and
scales all three constraint families exactly (the windows are linear in $X$;
boundary parities are routine but must be checked). Hence, as with Lemma
halving: **$\Sigma(X)$ UNSAT $\Rightarrow$ $\Sigma(4X)$ UNSAT.** Consequences:
a single small-scale UNSAT kills the scheme at all scales at once (clean
negative certificate); conversely SAT at small scales proves nothing about all
scales — a YES needs either a pumpable (e.g. self-similar: $u \prec w
\Leftrightarrow 4u \prec 4w$ with boundary lemma) $\Sigma$-witness family or an
inverse-limit-consistent family (witnesses whose even-restrictions halve to the
previous witness), which the halving map makes a well-posed search target.

**Calibration unknowns.** (i) Subset tolerance was measured only for tiny zone
subsets ($T \le 4$ of 8 at $M = 32$, near-total tolerance); the 7/8-occupancy
regime relevant to $\Sigma$ is unmeasured. (ii) The tested-UNSAT pipeline
inventory must be audited for the lag-2/9-8 configuration (see Remark iii).

**If $\Sigma$ is UNSAT (at any scale).** By Proposition 1 this does not yet
kill everything, but it kills more than one scheme: within append-only towers
the reservoir must live in $(8X, 12X]$, so the redirect is a finite scan over
bottom-half reservoir *shapes* (intervals at other offsets $\lambda \in
[1/16, 1/2)$ and fractions; unions of two intervals; the double-doom and
window-disjointness constraints prune the space sharply). If the entire
bottom-half family is UNSAT — a finite, decidable statement per scale, inherited
upward by halving — then **append-only towers are impossible**: every tower must
infinitely often insert new values before old ones, i.e. positions are never
final, and the fight moves back to quantitative fairness, materially
strengthening the NO-program (it would show the g-curve pressure cannot be
paid off by any withholding schedule, the precise mechanism note 10's
divergence skeleton needs at its step 2).

---

## 7. Immediate actionable checks (for the next experimental session)

1. **e45**: direct SAT of $\Sigma(X)$ for $X = 4, 16, 64, 256, 1024$ (system as
   specced in §4; $n = 7X$ values). This is the whole ballgame. If SAT at 256+,
   extract the witness's co-monotone threading profile and test self-similarity
   / halving-consistency.
2. $P(L)$ for $L = 16, 64, 256$ (expected easy).
3. Audit: rerun e44's flex chain and inspect the solver-chosen reservoir's
   shape at 64→256 (prediction: bottom-half heavy); audit e6/e13 configs for
   any lag-2 bottom-interval scheme.
4. Machine-audit the §2 range table (a 50-line script over random instances).
5. Seed construction at small scales (rounding regime $k < 3$), then assemble
   and brute-force-verify the explicit prefix of $\pi$ up to $4^6$ if 1–2 pass.
