# 97 — Six-angle attack on the 4-adic 3× supply surplus (2026-08-31)

Target: GAP-AFFORD‴-SPLIT, blocked by notes/80-pincer §3.4 — "per 4-adic
window, demand ≥ (window presence) but supply of colored values is 3× that;
no counting contradiction". Six independent angles, each attacked by two
adversaries (a refuter and a novelty/sufficiency checker).

## Verdict: ALL SIX REFUTED. The gap stands. No proof.

Recording because the negatives are sharp and three artifacts survived the
adversaries and were then re-verified by hand here.

## 1. Clean negatives (each localizes exactly where the idea dies)

**MULTIPLICITY** (make the 3× supply collapse by showing values are already
committed elsewhere) — dies at its *first* premise. By P1 anchor-locality,
every inversion pair with low member `v` covers only anchors in `[v/4, v)`,
and block geometry pins `v`'s window. Values are **not** multiply committed;
there is no hidden commitment to collapse.

**TELESCOPE** (sum the deficit over infinitely many anchors) — the load-
bearing implication is invalid: anchor-disjointness of payments (T-LEDGER)
does not imply the summed demand outgrows the summed supply.

**ORDER-DODGE** — the underlying measurements are correct and reproduce
(comply density → exactly `1/4`; DODGE-CHAR: `COMPLY(j,s) ⟺ w_j` is both an
`s`-trailer and a `2s`-trailer; DODGE-PRICE `λ(j) ≥ 5j/28`). The *reading*
was backwards; see §2c.

**BUILD-YES / "seam conservation"** — the identity `w_T + u_S = M_S − m0_T − 3`
is a **tautology**: `w_T = (2q−p′) − m0_T`, `u_S = −(2q−p′) + M_S − 3`, so
`p′` and `q` cancel by construction and it holds for *every* 2-partition,
carrying no partition content. The budget closure separately fails: `w_max`
and `u_max` were measured only with the old set a **full initial interval**
`O = [1,M]`, and both are functions of old-set density, not constants.

## 2. What survived, re-verified here independently

### (a) SC7 — a genuine split-setting forced configuration [VERIFIED]

`X = {10,14,15}` required to precede `V = {36,40,44,57,70,78,100}`.
In-set APs: `(10,40,70) (10,44,78) (14,57,100) (15,36,57) (36,40,44)
(36,57,78) (40,70,100) (44,57,70)`.

* exhaustive over all `3!·7! = 30240` orders: **0 AP-free**
* control — `V` alone IS orderable: `36,44,40,78,100,70,57`
* control — the full 10-set with no prefix demand IS orderable:
  `10,14,36,15,70,78,44,40,100,57`
* **minimality (mine): releasing ANY one of 10, 14, 15 from the prefix
  restores orderability** — all three attackers are load-bearing

No prior mention of SC7 or this attacker set in the repository. Honest
scope: the *vehicle* proposed for it (SPLIT-OG) is **not** new — it is
notes/42 `T-PIN-STAGE` over Definition `STG(M,F)` + notes/81 `PIN-Ω-k` +
notes/89 §1.1 Lemma PIN, which already allow an arbitrary finite attacker
menu, multi-octave windows and no cleanliness hypothesis. SC7 is a concrete
new instance, not a new theorem, and its value depends entirely on whether
it extends to a scale-indexed family.

### (b) CENTRE-CAP / X-CAP / X-DIFF [VERIFIED CORRECT — adversary could not break them]

For team `T`, `P_v = {x ∈ T : x < v, pos(x) < pos(v)}`,
`H_T(v) = #{z ∈ T ∩ (v,2v) : pos(z) < pos(v)}`; `v` is an *H-free centre* if
`H_T(v) = 0`; records are H-free, so the set `Z_T` is infinite.

1. **CENTRE-CAP.** `#{x ∈ P_v : 2v − x ∈ T} ≤ H_T(v)`; at an H-free centre
   `2v − P_v ⊆ T^c`. (Exact-set form of `lem:balance`, which the campaign
   states only as a count.)
2. **X-CAP [new].** For every valid pair `(A,B)`, `v ∈ Z_A`, `v' ∈ Z_B`:
   `P_v ∩ (P_{v'} + 2(v − v')) = ∅`; budgeted form
   `#{x ∈ P_v : x − 2(v−v') ∈ P_{v'}} ≤ H_A(v) + H_B(v')`.
   **Genuinely joint** — denominated in colored values, not positions, and
   not statable for one team alone. This is the NG1/NG2-compliant shape the
   campaign has lacked.
3. **X-DIFF [new].** For every `d ≠ 0`, `{(v,v') ∈ Z_A × Z_B : v − v' = d}`
   is finite (modulo L-NOTAIL, which is proved).

Machine falsification reproduced **independently here**
(`experiments/e189_xcap_bruteforce.py`): admissible configs
`12 / 64 / 336 / 1912 / 11108 / 71848 / 471180` for `n = 3..9`
(**556,460 total**), **0 GL violations, 0 XCAP violations**.

**What these do NOT do:** they do not deliver the censor replacement that
notes/83 §117 requires. The proposed `(e-sound)` is a depth-1 *existential*
with an unbounded uncontrolled witness, so no finite encoding is faithful;
and censor axis (e) is itself just a finite truncation of `lem:orbit`, which
is already proved and published. X-CAP is a correct new lemma of currently
unclear leverage.

### (c) The total-dodger density VANISHES [measured, robust]

The order-dodge angle claimed "33%/27%/21% of top-half values dodge their
entire cascade band, so dodging is realized in bulk". Extending its own scan
two octaves: `0.328, 0.266, 0.215, 0.174, 0.141` at `n = 256…4096`, with
successive ratios `0.811, 0.808, 0.809, 0.810` — clean geometric decay
`~ n^−0.304 → 0`. Four random members of the parity-recursive family give the
same exponent. So **asymptotically almost every top-half value complies
somewhere in its band**; the claim quoted the three smallest `n` of a
vanishing sequence. This points *toward* NO, not away from it, and the
proved quarter law (an average over `(j,s)`) gives no lower bound on the
total-dodger density at all.

## 3. The sharpest diagnostic: a currency mismatch

`P = 5n²/32` counts **adjacent-seam pairs**. The notes/80 obstruction is
denominated in **colored values**. Every ledger built in this campaign is a
pair ledger; the gap is a value ledger. That is why they keep failing to
engage the 3× — *they never touch it*.

Two hard numbers from the same exchange (CP-SAT, all OPTIMAL, reproduced):

| n | 16 | 24 | 32 | 40 | 48 |
|---|---|---|---|---|---|
| true min seam inversions | 12 | 32 | 64 | 100 | 154 |
| min with transitivity dropped | 5 | 13 | 22 | 37 | 51 |
| `\|H\| = P/8` | 5 | 11 | 20 | 31 | 45 |

**Transitivity is worth 2.4×–3.4×.** The AP-constraint system alone (max
degree 2 ⟹ disjoint chains ⟹ one free bit per chain) can force only `≈ P/8`.
Any argument that uses solely consequences of the AP constraints is capped
there. Caveat, against the source's own claim: `min/P = 0.300, 0.356, 0.400,
0.400, 0.428` is monotone increasing and 14% short of `1/2` at `n = 48`, so
"`Inv = P/2 ± Θ(n)`" is **not** established, and `min + max = P` is a
tautology (order reversal is an involution) carrying no information about
where the min sits.

## 4. Where this leaves the front

GAP-AFFORD‴-SPLIT is unmoved. The value of the run is negative information:
four routes are now closed with a named failure point, and the currency
mismatch explains the pattern. The one lead worth carrying forward is
**X-CAP** — the first joint, value-denominated law the campaign has
produced — plus the empirical fact that total dodging vanishes.
