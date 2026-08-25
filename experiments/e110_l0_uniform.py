"""e110_l0_uniform: TASK P -- strict schema checker for the UNIFORM hand
proof of the S1 layer-0 forcing lemmas (notes/33 Lemma L0):

  L0a: AP-free + A2 (t3<b6) + A3 (t10<b3)  |-  t3 < b3   (every even M)
  L0b: AP-free + A2 + A3                   |-  t10 < b6  (every even M)

Hand proof shape (notes/33, Sections 3-4): assume the negation; two
zigzag ladders (Lemma Z) + a seam offset p chosen by CRT + a fixed
10-step tail gadget on offsets {p-7, p, p+3, p+7, p+11, ..., p+23}
yield a 2-cycle on {b_{p+7}, b_{p+13}}.

  L0a: p == 0 (mod 6), p == M-10 (mod 14)   [B-leaders 3 mod 6,  T-leaders 10 mod 14]
  L0b: p == 3 (mod 6), p == M-3  (mod 14)   [B-leaders 0 mod 6,  T-leaders 3  mod 14]
Constraints: 8 <= p <= M-24 (all gadget offsets in range and ladders reach).

This script DOES NOT trust the closure engine: it re-implements the proof
as a linear sequence of justified steps, checking every step:
  - every AP used is a genuine in-interval AP (arithmetic re-check),
  - every rule application matches its premise literally,
  - every ladder rung is derived by induction from the seed,
  - the final contradiction is a literal 2-cycle.
It also verifies the parity obstruction: at odd M the CRT system for p
has no solution (the proof correctly does not exist there).

Run: .venv/bin/python experiments/e110_l0_uniform.py [Mmax]
Checks every even M in 74..Mmax (default 300) plus spot scales
512, 1024, 4096 (dyadic family) -- pure arithmetic, no SAT solver.
Output: data/e110_l0_uniform.json
"""
import json
import sys

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e110_l0_uniform.json"


class Proof:
    """A checked forward derivation over the interval (M, 2M]."""

    def __init__(self, M):
        self.M = M
        self.facts = set()      # (u, w): u before w
        self.log = []

    def inside(self, v):
        return self.M < v <= 2 * self.M

    def ap(self, x, y, z):
        assert x < y < z and z - y == y - x, f"not an AP: {x},{y},{z}"
        assert self.inside(x) and self.inside(z), f"AP outside: {x},{y},{z}"

    def axiom(self, u, w, tag):
        assert self.inside(u) and self.inside(w)
        self.facts.add((u, w))
        self.log.append(("axiom", tag, u, w))

    def trans(self, u, v, w):
        assert (u, v) in self.facts and (v, w) in self.facts, "trans premise"
        self.facts.add((u, w))
        self.log.append(("trans", u, v, w))

    def refl(self, x, y, z, premise):
        """Apply the reflection rule on AP (x,y,z) from a known premise.
        premise in facts; derives its forced partner:
          (x,y) -> (z,y);  (z,y) -> (x,y);  (y,x) -> (y,z);  (y,z) -> (y,x)."""
        self.ap(x, y, z)
        assert premise in self.facts, f"refl premise {premise} unknown"
        table = {(x, y): (z, y), (z, y): (x, y),
                 (y, x): (y, z), (y, z): (y, x)}
        assert premise in table, "premise does not touch the midpoint"
        c = table[premise]
        self.facts.add(c)
        self.log.append(("refl", (x, y, z), premise, c))
        return c

    def zigzag(self, u, delta, r, seed):
        """Lemma Z, checked rung by rung: ladder w_i = u + i*delta,
        i = 0..r (all in interval); seed = (i, j) adjacent indices with
        w_i before w_j already known.  Derives w_k < w_{k+-1} for every
        k = seed lead index mod 2.  Returns the parity of lead indices."""
        w = [u + i * delta for i in range(r + 1)]
        for v in w:
            assert self.inside(v), f"ladder value {v} outside"
        i, j = seed
        assert abs(i - j) == 1 and (w[i], w[j]) in self.facts, "bad seed"
        lead = i % 2

        def refl3(k, premise):
            trip = sorted((w[k - 1], w[k], w[k + 1]))
            assert trip[1] == w[k]
            self.refl(trip[0], trip[1], trip[2], premise)
        # propagate to lower indices from the lowest known rise/fall,
        # and to higher indices: do both by sweeping repeatedly.
        # known(k) means w_k < w_{k+1} direction resolved as:
        #   k lead: w_k < w_{k+1} and w_k < w_{k-1}
        def srt(a, b):
            return (min(a, b), max(a, b))
        for _ in range(2):      # two sweeps suffice (up then down)
            for k in range(0, r + 1):
                if k % 2 != lead:
                    continue
                for nb in (k - 1, k + 1):
                    if 0 <= nb <= r and (w[k], w[nb]) not in self.facts:
                        # derive via the AP containing both, midpoint one of them
                        if nb == k + 1 and k - 1 >= 0 and \
                                (w[k], w[k - 1]) in self.facts:
                            refl3(k, (w[k], w[k - 1]))
                        elif nb == k - 1 and k + 1 <= r and \
                                (w[k], w[k + 1]) in self.facts:
                            refl3(k, (w[k], w[k + 1]))
                        elif nb == k + 1 and k + 2 <= r and \
                                (w[k + 2], w[k + 1]) in self.facts:
                            refl3(k + 1, (w[k + 2], w[k + 1]))
                        elif nb == k - 1 and k - 2 >= 0 and \
                                (w[k - 2], w[k - 1]) in self.facts:
                            refl3(k - 1, (w[k - 2], w[k - 1]))
        # verify everything claimed is now present
        got = all((w[k], w[nb]) in self.facts
                  for k in range(lead % 2, r + 1, 2)
                  for nb in (k - 1, k + 1) if 0 <= nb <= r)
        assert got, "zigzag incomplete"
        return lead


def l0_proof(M, which):
    """Checked uniform refutation of AP + A2 + A3 + not-L0{a,b} at even M.
    Returns the seam offset p used."""
    assert M % 2 == 0
    b = lambda j: M + j
    t = lambda i: 2 * M - i
    P = Proof(M)
    P.axiom(t(3), b(6), "A2")
    P.axiom(t(10), b(3), "A3")
    if which == "a":
        P.axiom(b(3), t(3), "neg-L0a")
        P.trans(t(10), b(3), t(3))          # t10 < t3
        P.trans(b(3), t(3), b(6))           # b3 < b6
        # B ladder: w_i = b(3+3i); seed rise at index 0 (b3 < b6)
        rB = (M - 3) // 3 - 1               # 3+3r <= M  -> values <= 2M
        P.zigzag(b(3), 3, rB, (0, 1))       # leaders: offsets 3 mod 6
        Blead = 3
        # T ladder: w_i = t(3+7i); seed t10 < t3 = (w_1, w_0)
        rT = (M - 4) // 7                   # 3+7r <= M-1
        P.zigzag(t(3), -7, rT, (1, 0))      # seed t10 < t3
        Tlead = 10                          # leaders: t-offsets 10 mod 14
        pmod6, pmod14 = 0, (M - 10) % 14
    else:
        P.axiom(b(6), t(10), "neg-L0b")
        P.trans(t(3), b(6), t(10))          # t3 < t10
        P.trans(b(6), t(10), b(3))          # b6 < b3
        # B ladder seed: fall at index 1 (b6 < b3): leaders 0 mod 6... i.e.
        # ladder w_i = b(3+3i), seed (1, 0)
        rB = (M - 3) // 3 - 1
        P.zigzag(b(3), 3, rB, (1, 0))       # leaders: offsets 6 mod 6 -> 0
        Blead = 0
        rT = (M - 4) // 7
        P.zigzag(t(3), -7, rT, (0, 1))      # seed t3 < t10
        Tlead = 3                           # leaders: t-offsets 3 mod 14
        pmod6, pmod14 = 3, (M - 3) % 14
    # seam offset p by CRT: p = pmod6 (6), p = pmod14 (14); 8 <= p <= M-24
    p = None
    for c in range(8, M - 23):
        if c % 6 == pmod6 and c % 14 == pmod14:
            p = c
            break
    assert p is not None, f"no seam offset at M={M}"
    # sanity: p+3 is a B-leader, p is a T-leader (as bottom offset)
    assert (p + 3) % 6 == Blead % 6
    assert (M - p) % 14 == Tlead
    # tail gadget
    P.trans(b(p + 3), b(p), b(p + 7))       # cross rise (d=4 ladder index 0)
    P.zigzag(b(p + 3), 4, 5, (0, 1))        # leaders p+3, p+11, p+19
    P.trans(b(p + 11), b(p + 15), b(p + 12))
    P.zigzag(b(p + 11), 1, 3, (0, 1))       # leaders p+11, p+13
    P.trans(b(p + 13), b(p + 14), b(p + 7))     # (*)  b_{p+13} < b_{p+7}
    P.trans(b(p + 3), b(p), b(p - 7))
    P.zigzag(b(p - 7), 10, 3, (1, 0))       # leaders p+3, p+23
    P.trans(b(p + 19), b(p + 23), b(p + 13))
    P.refl(b(p + 7), b(p + 13), b(p + 19),
           (b(p + 19), b(p + 13)))          # b_{p+7} < b_{p+13}
    # contradiction: 2-cycle
    assert (b(p + 13), b(p + 7)) in P.facts and \
           (b(p + 7), b(p + 13)) in P.facts
    return p


def crt_unsolvable_odd(M, which):
    pmod6 = 0 if which == "a" else 3
    pmod14 = (M - 10) % 14 if which == "a" else (M - 3) % 14
    return all(not (c % 6 == pmod6 and c % 14 == pmod14)
               for c in range(0, 42 * 2))


def main():
    Mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    out = {"checked": {}, "odd_obstruction": {}}
    scales = list(range(74, Mmax + 1, 2)) + [512, 1024, 4096]
    for M in scales:
        pa = l0_proof(M, "a")
        pb = l0_proof(M, "b")
        out["checked"][str(M)] = {"pa": pa, "pb": pb}
    for M in range(75, 130, 2):
        assert crt_unsolvable_odd(M, "a") and crt_unsolvable_odd(M, "b")
        out["odd_obstruction"][str(M)] = "no-seam (CRT parity)"
    n = len(out["checked"])
    print(f"L0a/L0b uniform schema CHECKED at {n} scales "
          f"(every even M in 74..{Mmax} + 512, 1024, 4096)")
    print("odd-M obstruction verified (no CRT seam) at 75..129 odd")
    ps = {m: v for m, v in list(out['checked'].items())[:6]}
    print("sample seam offsets:", ps)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}")


if __name__ == "__main__":
    main()
