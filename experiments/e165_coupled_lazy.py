"""Erdős #197 — e165: HEROIC coupled 3-block (2,2,2) core, lazy transitivity.

The e120_density_cores.solve_coupled3 gadget (B0 = (M,2M], B1 = (2M,4M],
B2 = (4M,8M]; coloring c_v in {A,B}; each team its own total order;
guarded APs — all three in team; block-order units at BOTH seams + outer
pair for both teams; absolute per-team-per-block lower bounds, default
(2,2,2)) — re-encoded with LAZY transitivity so it scales to M = 256:
full transitivity at M = 256 restricted support would be
2 teams x 2 x C(1054,3) ~ 7.8e8 clauses (full support ~ 3.8e9) — never
materializable.  Here: window-w transitivity seed (sound subset) + e89-
style CEGAR triangle refutation per team, per round.

  --support core : CORE'(M) = (M,2M] u (3M-15,4M] u [4M+1,6M+15]
                   (notes/51, locked at 5 scales; certified sufficient),
                   n = 4M + 30.
  --support full : full window (M, 8M], n = 7M.

UNSAT under lazy transitivity is sound (added clauses are a subset of the
full encoding).  SAT requires per-team closure + independent witness
verification (balance, seam order, in-team AP-freeness).

Usage: e165_coupled_lazy.py M [--support core] [--bounds 2,2,2]
       [--seed-w 32] [--cap 150000] [--tag x]
"""
import argparse, json, time

import numpy as np
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('M', type=int)
    ap.add_argument('--support', choices=('core', 'full'), default='core')
    ap.add_argument('--bounds', default='2,2,2')
    ap.add_argument('--seed-w', type=int, default=32)
    ap.add_argument('--cap', type=int, default=150000)
    ap.add_argument('--tag', default='')
    args = ap.parse_args()
    M, w, cap = args.M, args.seed_w, args.cap
    bounds = tuple(int(x) for x in args.bounds.split(','))
    if args.support == 'core':
        V = sorted(set(range(M + 1, 2 * M + 1))
                   | set(range(3 * M - 14, 6 * M + 16)))
    else:
        V = list(range(M + 1, 8 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    row = [i * (2 * n - i - 1) // 2 for i in range(n)]
    nP = n * (n - 1) // 2
    # team A order vars 1..nP, team B order vars nP+1..2nP, colors 2nP+1..2nP+n
    ai = {v: 2 * nP + 1 + i for i, v in enumerate(V)}

    def mk_lit(off):
        def lit(u, v):
            i, j = idx[u], idx[v]
            if i < j:
                return off + row[i] + (j - i)
            return -(off + row[j] + (i - j))
        return lit

    litA, litB = mk_lit(0), mk_lit(nP)
    Vs = set(V)
    B0 = [v for v in V if v <= 2 * M]
    B1 = [v for v in V if 2 * M < v <= 4 * M]
    B2 = [v for v in V if v > 4 * M]

    t_build = time.time()
    sol = Cadical195()
    nap = nseam = 0
    for team, lit, g in (('A', litA, lambda v: -ai[v]),
                         ('B', litB, lambda v: ai[v])):
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    sol.add_clause(gg + [-lit(a, b), -lit(b, c)])
                    sol.add_clause(gg + [lit(a, b), lit(b, c)])
                    nap += 1
        for lowblk, highblk in ((B0, B1), (B1, B2), (B0, B2)):
            for u in lowblk:
                for v in highblk:
                    sol.add_clause([g(u), g(v), lit(u, v)])
                    nseam += 1
    nseed = 0
    for off in (0, nP):
        for i in range(n):
            top = min(n, i + w + 1)
            for j in range(i + 1, top):
                xij = off + row[i] + (j - i)
                for k in range(j + 1, top):
                    xjk = off + row[j] + (k - j)
                    xik = off + row[i] + (k - i)
                    sol.add_clause([-xij, -xjk, xik])
                    sol.add_clause([xij, xjk, -xik])
                    nseed += 1
    tid = 2 * nP + n
    ncard = 0
    for bi, blk in enumerate((B0, B1, B2)):
        bnd = bounds[bi]
        if bnd <= 0:
            continue
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blk],
                                  bound=bnd, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            for c in enc.clauses:
                sol.add_clause(c)
                ncard += 1
    print(f"e165 M={M} support={args.support} bounds={bounds} n={n} "
          f"blocks=({len(B0)},{len(B1)},{len(B2)}) orderVars={2*nP} "
          f"apPairs={nap} seam={nseam} seed={nseed} card={ncard} "
          f"build={time.time()-t_build:.0f}s", flush=True)

    iu, ju = np.triu_indices(n, 1)
    t0 = time.time()
    rounds = 0
    added = 0
    while True:
        ok = sol.solve()
        el = time.time() - t0
        if not ok:
            print(f"VERDICT e165 M={M} {args.support} {bounds}: UNSAT "
                  f"({el:.0f}s, {rounds} rounds, {added} lazy clauses)",
                  flush=True)
            return
        model = np.array(sol.get_model(), dtype=np.int64)
        pos = model > 0                      # truth by var-1
        rounds += 1
        totv = 0
        new = []
        Bmats = {}
        for name, off in (('A', 0), ('B', nP)):
            truth = pos[off:off + nP]
            Bm = np.zeros((n, n), dtype=bool)
            Bm[iu, ju] = truth
            Bm[ju, iu] = ~truth
            Bmats[name] = Bm
            Bf = Bm.astype(np.float32)
            R2 = (Bf @ Bf) > 0
            miss = R2 & ~Bm & Bm.T
            np.fill_diagonal(miss, False)
            ii, jj = np.nonzero(miss)
            totv += len(ii)
            for i, j in zip(ii[:cap], jj[:cap]):
                i, j = int(i), int(j)
                k = int(np.nonzero(Bm[i] & Bm[:, j])[0][0])
                def L(p, q):
                    return (off + row[p] + (q - p)) if p < q \
                        else -(off + row[q] + (p - q))
                new.append([-L(i, k), -L(k, j), L(i, j)])
        if totv == 0:
            colA = [v for v in V if pos[ai[v] - 1]]
            colB = [v for v in V if not pos[ai[v] - 1]]
            info = {'A': colA, 'B': colB}
            fail = None
            for name, col in (('A', colA), ('B', colB)):
                Bm = Bmats[name]
                wins = Bm.sum(axis=1)
                order = sorted(col, key=lambda v: -int(wins[idx[v]]))
                err = verify_team(order, col, M, bounds)
                if err:
                    fail = f"{name}: {err}"
                    break
                info[f'order{name}'] = order
            tagf = f"_{args.tag}" if args.tag else ""
            fn = f"data/e165_M{M}_{args.support}{tagf}_witness.json"
            json.dump(info, open(fn, "w"))
            print(f"VERDICT e165 M={M} {args.support} {bounds}: SAT "
                  f"({el:.0f}s, {rounds} rounds) witness->{fn} "
                  f"check={fail or 'OK'}", flush=True)
            return
        sol.append_formula(new)
        added += len(new)
        print(f"  round {rounds}: viol={totv} added={len(new)} "
              f"tot={added} t={el:.0f}s", flush=True)


def verify_team(order, col, M, bounds):
    """Independent: balance, both+outer seam order, in-team AP-freeness."""
    b0 = [v for v in col if v <= 2 * M]
    b1 = [v for v in col if 2 * M < v <= 4 * M]
    b2 = [v for v in col if v > 4 * M]
    if (len(b0) < bounds[0] or len(b1) < bounds[1] or len(b2) < bounds[2]):
        return f"balance ({len(b0)},{len(b1)},{len(b2)}) < {bounds}"
    p = {v: i for i, v in enumerate(order)}
    for low, high in ((b0, b1), (b1, b2), (b0, b2)):
        for u in low:
            for v in high:
                if p[u] > p[v]:
                    return f"block order ({u},{v})"
    vs = set(col)
    vals = sorted(col)
    for b in vals:
        for d in range(1, min(b - vals[0], vals[-1] - b) + 1):
            a, c = b - d, b + d
            if a in vs and c in vs:
                if p[a] < p[b] < p[c] or p[c] < p[b] < p[a]:
                    return f"monotone AP ({a},{b},{c})"
    return None


if __name__ == '__main__':
    main()
