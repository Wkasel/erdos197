# 66 — THE W-HOLE FRONT: α_max at 176/192/224/256, and the lattice route to bounding it

Mandate (from notes/64 (a.3)): the Case-2 chain's only open seam is
W(M) = 3 − α_max(M) (F2 regime); α_max ≥ 4 at any unmeasured scale
opens a width-1 hole in COV-W's overlap.  Tasks: (1) MEASURE α at
M = 176, 192, 224, 256 (notes/57 catalogue-scan method); (2) PROVE
what is provable about α via the H-LAT lattice recursion;
(3) if a hole is confirmed (α_max = 4 AND the robust chain fails),
characterize the escapes.  Instruments this session: e168 (parallel
e146 catalogue generation, pod), e169 (HALVE-PURE iso check + halved
lattice scans), e153 re-runs at the new scales.

Status tags: [PROVED] / [MACHINE-CHECKED] / [GAP].

---

## 1. Lemma HALVE-PURE  [PROVED; machine-checked §2]

**Setting.**  At scale M (m = M/2), the class-c *pure fan subsystem*
of an attacker pair X = {4M−p, 4M−q}, p ≡ q ≡ ε (mod 2), is the
order theory on V_ε = P2 ∩ (class ε) with (i) all 3-term APs inside
V_ε, (ii) R1–R4 + transitivity, (iii) the double-fan units
z = 2y − x restricted to y, z ∈ V_ε.  (Every pure death pattern's
Th2[S] is a subtheory of this system, so pure-catalogue-dead ⟹
pure-SAT-dead; and any refutation of the pure subsystem is a
refutation of the full window system.)

**Lemma HALVE-PURE.**  The class-ε pure fan subsystem at scale M is
isomorphic, as an order theory, to the e155 halved double-fan system
on W2ε(m) with attacker window W1 = [3m−7, 4m]:

    ε = 1 (odd):   4M+s ↦ 4m + (s+1)/2,  4M−p ↦ 4m − (p−1)/2,
                   window [4m+1, 6m+8]   (2m+8 values);
    ε = 0 (even):  4M+s ↦ 4m + s/2,      4M−p ↦ 4m − p/2,
                   window [4m+1, 6m+7]   (2m+7 values);

attacker gaps halve: g ↦ g/2.  The shallow zone maps to the shallow
zone: offsets −(M−1)..0 at scale M ↦ attackers [3m+1, 4m] (exactly
the m shallowest halved attackers).

*Proof.*  Write class-ε P2 values as 4M+s, s ≡ ε; substitute
s = 2t−ε′ (t the halved coordinate).  (a) Values: s odd ∈ [1, 2M+15]
↦ t ∈ [1, 2m+8]; s even ∈ [2, 2M+14] ↦ t ∈ [1, 2m+7] — bijections
onto the halved windows.  (b) APs: a class-ε AP has even step
d = 2δ and maps to the t-AP of step δ; conversely every t-AP of step
δ pulls back to the class-ε AP of step 2δ — bijection, and R1–R4
are defined per AP.  (c) Units: for attacker x = 4M−p (p ≡ ε) and
midpoint y = 4M+s_y, the forced value z = 2y−x has offset
s_z = 2s_y + p; in t-coordinates this reads t_z = 2·t_y + π with
π = ⌊p/2⌋ — exactly the fan unit of the halved attacker 4m−π on the
halved window; the correspondence of (attacker, midpoint) pairs is
bijective, with attacker range p ∈ [0, M+15] ↦ π ∈ [0, m+7], i.e.
W1 = [3m−7, 4m].  (d) Transitivity is order-isomorphic.  Hence
derivations (closure) and refutations (SAT) correspond exactly in
both directions.  Shallow zone: p ≤ M−1 ⟺ π ≤ m−1.  ∎

**Consequences.**
(i)  A pair is pure-SAT-dead at scale M iff its halved image is
     SAT-dead in W2ε(m); same for plain R1–R4+transitivity closure.
(ii) Defining α̂_ε(M) := max alive-clique (no pure-SAT-dead pair)
     among shallow class-ε band values — the SAT-tightened version
     of notes/57's catalogue α_ε — we get EXACTLY
     α̂_ε(M) = ω(SAT-alive graph of W2ε(m) restricted to [3m+1, 4m]).
     Since pure-catalogue-dead ⟹ pure-SAT-dead, α̂_ε(M) ≤ α_ε(M)
     (catalogue-α can only exceed the SAT truth when e146's greedy
     minimization happens to emit an impure pattern for a pair that
     also has a pure refutation).
(iii) The recursion is uniform: the halved system is again a fan
     system "window [L+1, L+N], attackers [L−A, L], units
     s_z = 2s_y + p" — the proof used only that shape — so the same
     halving applies to ITS same-parity pairs (quarter scale), which
     is the H-LAT mod-8 lattice structure (notes/58 §3.5a): alive
     gaps ≡ 0 mod 8 = three levels of "odd-gap pairs die".
(iv) Lemma FG-high (notes/55 §5.3b, [PROVED]) is automatically PURE
     for same-parity pairs: its four gadget values 4M+s, 4M+2p−3q,
     4M+3p−4q, 4M+5p−6q are all ≡ p (mod 2) when p ≡ q.  So for
     p ≡ q, p ≥ 2q+1, 5p−6q ≤ (window), the pair is pure-dead — a
     proved, scale-uniform kill that transfers through the iso to
     every level of the recursion.  (Not sufficient for a uniform
     clique bound: pairs with p < 2q+1 — e.g. any two shallow
     values in the top half of the zone — escape its hypothesis;
     those kills are the closure/affine-cycle families of
     GAP-FG-schema.)

## 2. Machine confirmation of the iso  [MACHINE-CHECKED]

e169 --iso M: for EVERY same-parity attacker pair at scale M, the
directly-computed full-scale pure closure verdict is compared to
close_window on the halved image; closure-alive pairs additionally
get both SAT verdicts (full-scale pure SAT vs fan_sat_unsat halved).

    M = 48: 992 pairs;  pure-closure dead 863,  alive 129;  0 / 0
    M = 64: 1560 pairs; pure-closure dead 1428, alive 132;  0 / 0
    M = 96: 3080 pairs; pure-closure dead 2907, alive 173;  0 / 0
            (final two columns: closure / SAT mismatches)

Cross-checks: 863/1428/2907 = notes/57 F0's same-parity pure-pattern
counts at 48/64/96 EXACTLY (so at these scales e146's minimized
pattern for a same-parity pair is pure precisely when the pure
closure kills — the catalogue's purity bookkeeping is faithful);
129 = e155's closure-alive 66 (W2e) + 63 (W2o) at m = 24.
[MACHINE-CHECKED at 48/64/96, zero mismatches at both the closure
and the SAT level; data/e169_alive_lattice.json.]

## 3. The scans (e169 part L): SAT-alive structure of W2ε(m)

Method per (m, window): closure-prefilter all C(m+8, 2) attacker
pairs (44-way parallel), SAT-adjudicate every closure-alive pair
(ONE incremental Cadical per window — static AP+transitivity
clauses, per-pair fan units as assumptions), then max cliques of the
SAT-alive graph on the full window and on the shallow zone
[3m+1, 4m].  By §1(ii) the shallow clique number IS α̂(M = 2m).

First result (m = 24, local, reproduces e155b exactly — SAT-alive
46/44, full cliques {65,69,77,93} both windows):

    m=24: full-window max clique 4, but SHALLOW max clique 2 = the
    measured α(48).  The feared e155b 4-cliques are DEEP objects —
    at m = 24 they have 2 members in/below the CW zone, outside α's
    vertex set entirely.

## 4. α at the new scales  [MACHINE-CHECKED as results land]

Two independent tracks per scale: (T1) e168 catalogue (parallel
e146, byte-identical output verified at M = 48) → e153 scan =
the notes/57 method verbatim; (T2) e169 shallow clique of the
SAT-alive graph of W2ε(m) = α̂ via Lemma HALVE-PURE.

### M = 176  (catalogue 17976 patterns, 635 s @ 44 cores)

    T1 (e153):  F0 total (8813/8813 same-parity patterns pure);
                α_E = 3  (offs −174, −142, −14; gaps 32, 128)
                α_O = 3  (offs −175, −143, −15)
                f_O = f_E = 8 (both bottom singletons self-serve;
                self-serving sets O:{1,5}, E:{2,6,10})
                D5: every admissible defector set has LOW minimum.
    T2 (e169):  m=88 W2e: 4560 pairs → 157 closure-alive → 82
                SAT-alive; gaps {16,32,64,80} — H-LAT(mod 8) HOLDS;
                shallow clique 3 = {265,281,345} (halved gaps 16/64)
                = EXACTLY the T1 α_E witness halved.  α̂_E(176) = 3.

    ⟹ K*(176) = 88 + 9 + (3−8) = 92;  cap+1 = C(176) = 92;
    **W(176) = 0.**  α_max(176) = 3: NO hole at 176, margin again
    exactly zero — the W = 0 club is now {112, 128, 144, 176}.

### M = 192 — T2 first (catalogue in flight)

    T2 (e169):  m=96 W2e: 5356 pairs → 184 closure-alive → 97
                SAT-alive; W2o: 173 → 96.  Gaps both windows
                {16,32,48,64,96} — H-LAT(mod 8) HOLDS.
                Full-window clique 3 = {281,297,329} (deep member
                281 < 3m+1); SHALLOW clique 2 = {289, 353} in BOTH
                windows.  α̂_E(192) = α̂_O(192) = 2.

    ⟹ if the catalogue track agrees (and f = 8): K*(192) =
    105 + (2−8) = 99, C = 100, **W(192) = 1** — the α relaxation
    at 160 (α: 3→2) REPEATS at 192.

### M = 224, 256 — T2 (catalogues in flight)

    m=112 (both windows): 7140 pairs → 209/202 closure-alive → 128
      SAT-alive; gaps {16,32,48,64,96,112} — H-LAT HOLDS.
      **Full-window max clique = 4**: {329,345,377,441}
      (π-offsets {119,103,71,7}, halved gaps 16/32/64) — the FIRST
      4-clique at an α-relevant tower level — but its deepest member
      is π = 119 > m−1 = 111: OUTSIDE the shallow zone by exactly
      ONE lattice step (8).  SHALLOW clique = 3 {337,369,433}.
      α̂_E(224) = α̂_O(224) = 3.

    m=128 W2e: 9180 pairs → 243 closure-alive → 139 SAT-alive;
      gaps {32,64,96,128} (all ≡ 0 mod 32) — H-LAT HOLDS.
      **Full-window max clique = 4**: {377,409,441,505} (π-offsets
      {135,103,71,7}) — deepest member π = 135 > m−1 = 127: again
      outside shallow by EXACTLY 8.  SHALLOW clique = 3
      {392,424,488}.  α̂_E(256) = 3.

    ⟹ predicted (catalogue tracks pending): α_max(224) =
    α_max(256) = 3, W = 0 at both.  The notes/64 fear is
    quantitatively real — shallow-adjacent 4-cliques EXIST from
    m = 112 up — but the shallow boundary excludes their deepest
    member by one lattice step at both scales.  NO five-alarm, and
    no W ≥ 1 relaxation either: the margin at 224/256 is zero.

### The full two-track consistency table (e169 scans COMPLETE)

    m    M    α̂_E  α̂_O   catalogue α_E, α_O (e153/notes-57)
    24   48    2    2      2, 2   ✓
    32   64    3    2      3, 2   ✓  (witness {104,112,128} = halved
                                      e153 witness EXACTLY)
    40   80    2    2      2, 2   ✓
    48   96    2    2      2, 2   ✓
    56  112    3    3      3, 3   ✓  (witness {169,185,217} = halved
                                      {−110,−78,−14} EXACTLY)
    64  128    3    3      3, 3   ✓
    72  144    3    3      3, 3   ✓
    80  160    2    2      2, 2   ✓
    88  176    3    3      3, 3   ✓  (new scale, both tracks fresh)
    96  192    2    2      2, 2   ✓  (new scale)
    112 224    3    3      [catalogue pending]
    128 256    3    3      [catalogue pending]

α̂ = α_catalogue at every scale where both exist — 10 scales × 2
classes, zero exceptions.  H-LAT (SAT-alive gaps ≡ 0 mod 8) HOLDS
at every scanned m (mod 4 at m = 24 as known).  [MACHINE-CHECKED:
data/e169_alive_lattice.json, data/e169_scan.log.]

## 4b. ANCHOR-4 / SPAN-4: why α stays ≤ 3  [MACHINE-CHECKED]

e169b enumerates EVERY 4-clique of every SAT-alive graph (34 total
across the 22 (m, window) scans; they exist at m = 32, 56, 64, 112,
128 only):

    * every 4-clique has span EXACTLY m — never more, never less
      (min-span = max-span = m at every occurrence);
    * hence every 4-clique sticks out of the shallow zone
      [3m+1, 4m] (width m−1): ANCHOR-4 — its deepest member is
      always ≤ 3m, one lattice step below the α boundary;
    * the outer pair of each 4-clique has halved gap m = full-scale
      gap M — precisely the "g = M escapes at every scale"
      universal resonance of notes/55 §5.3b(iv);
    * SPAN-4 = m exactly also FORBIDS 5-cliques outright: a
      5-clique {a<b<c<d<e} contains 4-subcliques of spans e−a, d−a,
      e−b which cannot all equal m.

So the machine statement "SPAN-4: every SAT-alive 4-clique of
W2ε(m) has span ≥ m" implies α̂(2m) ≤ 3, and it holds at all 22
scanned (m, window) pairs.  Uniformizing SPAN-4 is the new sharp
form of GAP-DICH-ALPHA — strictly easier than ODD-KILL (it is a
statement about the DEEP structure only: cliques avoiding the
bottom window must break).  [GAP: SPAN-4 for all m.]

---

## 5. The lattice recursion, formalized — what is proved and what
## remains for a uniform α bound

**The abstract family.**  F(N, A): order variables on window values
{L+1, …, L+N}; all in-window 3-term APs with R1–R4 + transitivity;
attackers at offsets −p, p ∈ [0, A]; the double-fan units
s_z = 2s_y + p.  Level 0 = the full-scale block-2 system
(N = 2M+15, A = M+15); by Lemma HALVE-PURE (whose proof uses ONLY
this shape), the class-ε pure subsystem of F(N, A) is
F(⌈(N−1)/2⌉ or ⌊N/2⌋, ⌊A/2⌋) — so the recursion applies at every
level, and level j exists for a pair of gap g iff 2^j | g.

**Level tower for M ≡ 0 (mod 16)** (α's scales): level 1 =
W2ε(M/2); level 2 ≈ W2 of M/4; level 3 ≈ W2 of M/8.  For
M = 176/192/224/256 the towers bottom out inside the e155-verified
range — every level of every new scale is itself scanned or
scannable.

**What is proved uniformly.**
* [PROVED] HALVE-PURE at every level (§1).
* [PROVED] FG-high kills, pure for same-parity pairs (§1(iv)), at
  every level: pair (q, p), p ≥ 2q+1, 5p−6q ≤ N is dead.
* [PROVED, notes/55] FG-high verified 48..400 at level 0
  (e143, 149 169 instances — includes level-0 windows of all four
  new scales).

**What the machine adds per scale** (e169): the SAT-alive graph of
each level, its gap law (H-LAT: gaps ≡ 0 mod 8 — HOLDS at every
scanned m incl. 88), and its shallow clique number = α̂.

**The remaining uniform gap, stated exactly.**  H-LAT(m) = "every
SAT-alive pair of F(N, A) has gap ≡ 0 mod 8" is THREE levels of the
single statement

    (ODD-KILL)  every pair with odd gap is SAT-dead in F(N, A)
                (for the (N, A) shapes of the tower),

because gap g with v₂(g) = j < 3 halves j times to an odd-gap pair.
ODD-KILL is a CROSS-parity statement (odd gap = attackers of
opposite parity), so the pure recursion does not reduce it further;
FG-high proves it for p ≥ 2q+1 within reach, and the
clustered/low-pair regime is exactly the affine-cycle-family
species of GAP-FG-schema (notes/55 §5.3b closure kills, med ≈ 14
facts, certificates in hand).  [GAP — same species as
GAP-DICH-ALPHA, sharpened: ODD-KILL + a base-window clique
catalogue would give α_max(M) ≤ max base clique UNIFORMLY.]

**Why the feared 4-cliques do not appear in α.**  The e155b
4-cliques ({65,69,77,93} at m=24 etc.) are DEEP objects — members
in/near the CW zone [3m−7, 3m−1], outside the shallow zone
[3m+1, 4m] that α quantifies over (shallow at scale M halves to
shallow at m, §1).  At every scanned (m, window) so far the SHALLOW
clique number is ≤ 3 even where the full-window number is 4.
