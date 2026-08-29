"""Erdős #197 — e166: HEROIC single-block lazy-transitivity solver.

Two instance families on the block (M, 2M], order-variable encoding
o(u,w) = "u placed before w", AP triples non-monotone both directions,
lazy transitivity (e89-style CEGAR: solve, find order-cycle triangles
via boolean matmul, add violated triangle clauses, repeat) plus an
upfront transitivity SEED on all index-window-w triples (a sound subset
of full transitivity, converges far faster than bare e89).

  --attacks c3 : the 3-axiom core C3 = {t5<b5, t3<b6, t10<b3}
                 (b_j = M+j, t_i = 2M-i; = OG attacks (15,5),(15,6),(16,3);
                 unit clauses o(t,b)).  Mod-8 law predicts UNSAT iff
                 M = 0 mod 8 (M >= 16).
  --attacks og : the full 15-attack OG(M) gadget (e89 families x=15,16,
                 j in [1, x/2]: z = 2M+2j-x before y = M+j).

UNSAT under lazy transitivity is sound: every added clause belongs to the
full encoding, and UNSAT of a subset implies UNSAT of the whole.
SAT requires closure (zero violated triangles) + independent witness check.

Usage: e166_block_lazy.py M --attacks {c3,og} [--seed-w 32] [--cap 300000]
"""
import argparse, json, sys, time

import numpy as np
from pysat.solvers import Cadical195


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('M', type=int)
    ap.add_argument('--attacks', choices=('c3', 'og'), required=True)
    ap.add_argument('--seed-w', type=int, default=32)
    ap.add_argument('--cap', type=int, default=300000)
    ap.add_argument('--tag', default='')
    args = ap.parse_args()
    M, w, cap = args.M, args.seed_w, args.cap
    lo, hi = M, 2 * M
    V = list(range(lo + 1, hi + 1))
    n = len(V)
    # var ids: pair (i<j) -> row[i] + (j-i), ids 1..C(n,2)
    row = [i * (2 * n - i - 1) // 2 for i in range(n)]
    nP = n * (n - 1) // 2

    def o(u, v):
        i, j = u - lo - 1, v - lo - 1
        if i < j:
            return row[i] + (j - i)
        return -(row[j] + (i - j))

    t_build = time.time()
    sol = Cadical195()
    nap = 0
    for y in V:
        d = 1
        while y - d > lo and y + d <= hi:
            x, z = y - d, y + d
            sol.add_clause([-o(x, y), -o(y, z)])
            sol.add_clause([-o(z, y), -o(y, x)])
            nap += 1
            d += 1
    if args.attacks == 'c3':
        atk = [(2 * M - 5, M + 5), (2 * M - 3, M + 6), (2 * M - 10, M + 3)]
    else:
        atk = []
        for x in (15, 16):
            for j in range(1, x // 2 + 1):
                z = hi + 2 * j - x
                if lo < z <= hi:
                    atk.append((z, M + j))
    for z, y in atk:
        sol.add_clause([o(z, y)])
    nseed = 0
    for i in range(n):
        top = min(n, i + w + 1)
        for j in range(i + 1, top):
            xij = row[i] + (j - i)
            for k in range(j + 1, top):
                xjk = row[j] + (k - j)
                xik = row[i] + (k - i)
                sol.add_clause([-xij, -xjk, xik])
                sol.add_clause([xij, xjk, -xik])
                nseed += 1
    print(f"e166 M={M} attacks={args.attacks} n={n} vars={nP} "
          f"apTriples={nap} attacks={len(atk)} seedTriples={nseed} "
          f"build={time.time()-t_build:.0f}s", flush=True)

    iu, ju = np.triu_indices(n, 1)
    t0 = time.time()
    rounds = 0
    added = 0
    while True:
        ok = sol.solve()
        el = time.time() - t0
        if not ok:
            print(f"VERDICT e166 M={M} {args.attacks}: UNSAT "
                  f"({el:.0f}s, {rounds} rounds, {added} lazy clauses)",
                  flush=True)
            return
        model = np.array(sol.get_model(), dtype=np.int64)
        truth = model[:nP] > 0          # model sorted by |var|
        B = np.zeros((n, n), dtype=bool)
        B[iu, ju] = truth
        B[ju, iu] = ~truth
        Bf = B.astype(np.float32)
        R2 = (Bf @ Bf) > 0
        miss = R2 & ~B & B.T
        np.fill_diagonal(miss, False)
        ii, jj = np.nonzero(miss)
        nv = len(ii)
        rounds += 1
        if nv == 0:
            wins = B.sum(axis=1)
            order = [V[i] for i in sorted(range(n),
                                          key=lambda i: -int(wins[i]))]
            perr = verify(order, V, atk)
            tagf = f"_{args.tag}" if args.tag else ""
            fn = f"data/e166_{args.attacks}_M{M}{tagf}_witness.json"
            json.dump(order, open(fn, "w"))
            print(f"VERDICT e166 M={M} {args.attacks}: SAT ({el:.0f}s, "
                  f"{rounds} rounds) witness->{fn} check={perr or 'OK'}",
                  flush=True)
            if perr:
                sys.exit(2)
            return
        def lit(p, q):
            return (row[p] + (q - p)) if p < q else -(row[q] + (p - q))
        new = []
        for i, j in zip(ii[:cap], jj[:cap]):
            i, j = int(i), int(j)
            k = int(np.nonzero(B[i] & B[:, j])[0][0])
            new.append([-lit(i, k), -lit(k, j), lit(i, j)])
        sol.append_formula(new)
        added += len(new)
        print(f"  round {rounds}: viol={nv} added={len(new)} "
              f"tot={added} t={el:.0f}s", flush=True)


def verify(order, V, atk):
    """Independent check: AP-free (no monotone 3-AP) + attack order."""
    pos = {v: i for i, v in enumerate(order)}
    if sorted(order) != sorted(V):
        return "not a permutation"
    lo, hi = V[0] - 1, V[-1]
    for z, y in atk:
        if pos[z] > pos[y]:
            return f"attack ({z},{y}) violated"
    for y in V:
        d = 1
        while y - d > lo and y + d <= hi:
            x, z = y - d, y + d
            if pos[x] < pos[y] < pos[z] or pos[z] < pos[y] < pos[x]:
                return f"monotone AP ({x},{y},{z})"
            d += 1
    return None


if __name__ == '__main__':
    main()
