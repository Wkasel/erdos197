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

## 2. Machine confirmation of the iso  [MACHINE-CHECKED]

e169 --iso M: for EVERY same-parity attacker pair at scale M, the
directly-computed full-scale pure closure verdict is compared to
close_window on the halved image; closure-alive pairs additionally
get both SAT verdicts (full-scale pure SAT vs fan_sat_unsat halved).

    M = 48: 992 pairs; pure-closure dead 863, alive 129;
            closure mismatches 0; SAT mismatches 0.       [4 s local]
    (cross-checks: 863 = notes/57 F0's same-parity pattern count at
    48; 129 = e155's closure-alive 66 (W2e) + 63 (W2o) at m = 24.)

[M = 64, 96 iso runs + pod scans in flight; results below.]

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

## 4. α at the new scales  [pending: e168 catalogues → e153]

e168 (parallel e146, byte-identical output verified at M = 48) is
generating the 176/192/224/256 catalogues on the pod; e153 then
measures α_ε, f_ε and prints the K* prediction per the notes/57
formula.  Cross-track: e169's shallow clique numbers at
m = 88/96/112/128 give α̂ at the same scales independently of the
catalogue path.  Consistency standard: at the eight measured scales
48..160, shallow-ω(W2ε(m)) must equal the e153 catalogue α_ε(2m)
wherever the catalogue's purity bookkeeping is faithful.

[results to follow]
