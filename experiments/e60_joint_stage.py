"""Joint stage+order SAT: find delay sets making the stage decomposition work.

Variables: per value v (block k): delay flags S1(v)=[delta>=1], S2(v)=[delta>=2]
(stage s(v) = k/2 + delta, window <= 2); order lits o(u,w) = T(u) < T(w).
Channeling: s(u) < s(w) forces o(u,w). Triples: standard non-monotone on o.
Lazy transitivity. Any solution = staged arrangement satisfying (A)+(B) at
horizon N; we mine the delayed sets per block for closed form.
Args: m [minimize]   (N = 4^m). With 'min': also try to minimize #delayed
via solver phases (not exact—heuristic pass).
"""
import sys, time, json
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def main(m):
    N = 4 ** m
    V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    Vs = set(V)
    var = 0
    S1, S2 = {}, {}
    for v in V:
        S1[v] = var + 1; S2[v] = var + 2; var += 2
    t = {}
    for i in range(n):
        for j in range(i + 1, n):
            var += 1
            t[(i, j)] = var
    def o(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]
    cl = []
    for v in V:
        cl.append([-S2[v], S1[v]])
    # channeling: for pair u<w (as values), stages s=k/2+delta.
    # enumerate delta_u in {0,1,2} x delta_w in {0,1,2}: if s_u<s_w -> o(u,w);
    # if s_u># -> o(w,u).
    def ind(v, d):
        # list of lits asserting delta(v)==d (as conjunction)
        if d == 0: return [-S1[v]]
        if d == 1: return [S1[v], -S2[v]]
        return [S2[v]]
    npairs = 0
    for a in range(n):
        u = V[a]
        ku = block(u) // 2
        for b in range(a + 1, n):
            w = V[b]
            kw = block(w) // 2
            if kw - ku > 2:
                # s_u <= ku+2 < kw <= s_w always -> forced order, no clause need
                cl.append([o(u, w)])
                continue
            for du in range(3):
                for dw in range(3):
                    su, sw = ku + du, kw + dw
                    if su == sw: continue
                    lit = o(u, w) if su < sw else o(w, u)
                    cl.append([-l for l in ind(u, du)] +
                              [-l for l in ind(w, dw)] + [lit])
            npairs += 1
    ntr = 0
    for y in V:
        d = 1
        while y + d <= N:
            x, z = y - d, y + d
            d += 1
            if x in Vs and z in Vs:
                cl.append([-o(x, y), -o(y, z)])
                cl.append([-o(z, y), -o(y, x)])
                ntr += 1
    print(f"N=4^{m}: n={n} pairs={npairs} triples={ntr} clauses={len(cl)}",
          flush=True)
    sol = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    for rnd in range(200000):
        if not sol.solve():
            print(f"JOINT-STAGE N=4^{m} window2: UNSAT ({time.time()-t0:.0f}s)",
                  flush=True)
            return
        model = set(l for l in sol.get_model() if l > 0)
        import numpy as np
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in t.items():
            if lit in model: B[i, j] = True
            else: B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool)
        miss &= B.T  # i->k->j but j->i: genuine 3-cycles only
        def lit(p, q):
            return t[(p, q)] if p < q else -t[(q, p)]
        new = []
        ii, jj = np.nonzero(miss)
        for i, j in zip(ii[:20000], jj[:20000]):
            ks = np.nonzero(B[i] & B[:, j])[0]
            k = int(ks[0])
            new.append([-lit(i, k), -lit(k, j), lit(i, j)])
        if not new:
            delays = {}
            for v in V:
                dv = 2 if S2[v] in model else (1 if S1[v] in model else 0)
                if dv: delays.setdefault(block(v), []).append((v, dv))
            print(f"JOINT-STAGE N=4^{m}: SAT ({time.time()-t0:.0f}s) "
                  f"delayed={sum(len(x) for x in delays.values())}", flush=True)
            for k in sorted(delays):
                print(f"  block {k}: {delays[k]}", flush=True)
            wins = B.sum(axis=1)
            ordv = [V[i] for i in sorted(range(n), key=lambda i: -int(wins[i]))]
            json.dump({"order": ordv,
                       "delays": {str(v): (2 if S2[v] in model else
                                           (1 if S1[v] in model else 0))
                                  for v in V}},
                      open(f"data/jointstage_{m}.json", "w"))
            return
        sol.append_formula(new)
        if rnd % 20 == 0:
            print(f"  round {rnd}: +{len(new)} ({time.time()-t0:.0f}s)",
                  flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]))
