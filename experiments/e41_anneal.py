"""Simulated annealing for pure-complete-X witnesses (SAT-side only)."""
import sys, time, json, random
import numpy as np

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa_set(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def violations_full(pos, triples):
    cnt = 0
    for (x, y, z) in triples:
        px, py, pz = pos[x], pos[y], pos[z]
        if (px < py < pz) or (px > py > pz):
            cnt += 1
    return cnt

def main(X, seed=0, iters=20_000_000):
    rng = random.Random(seed)
    V = sa_set(X)
    n = len(V)
    Vs = set(V)
    # all AP triples within the set
    triples = []
    for y in V:
        d = 1
        while y + d <= X:
            x, z = y - d, y + d
            if x in Vs and z in Vs:
                triples.append((x, y, z))
            d += 1
    print(f"n={n} triples={len(triples)}", flush=True)
    tri_of = {v: [] for v in V}
    for tr in triples:
        for v in tr:
            tri_of[v].append(tr)
    # init: heuristic order (doubled pure-1024 if available else value order)
    try:
        W = json.load(open('data/pure1024.json'))
        posW = {v: i for i, v in enumerate(W)}
        def hkey(v):
            p = v; steps = 0
            while p not in posW and p >= 4:
                p //= 4; steps += 1
            return (posW.get(p, len(W)), steps, v)
        order = sorted(V, key=hkey)
    except Exception:
        order = list(V)
        rng.shuffle(order)
    pos = {v: i for i, v in enumerate(order)}
    cur = violations_full(pos, triples)
    print(f"init violations: {cur}", flush=True)
    best = cur
    T = 3.0
    t0 = time.time()
    for it in range(iters):
        # move: pick a violated triple's middle & move it near a resolving spot,
        # or random swap
        if rng.random() < 0.7:
            a, b = rng.randrange(n), rng.randrange(n)
            va, vb = order[a], order[b]
        else:
            va = rng.choice(V)
            a = pos[va]
            b = rng.randrange(n)
            vb = order[b]
        # delta for swapping positions of va, vb
        affected = set(tri_of[va]) | set(tri_of[vb])
        before_cnt = 0
        for (x, y, z) in affected:
            px, py, pz = pos[x], pos[y], pos[z]
            if (px < py < pz) or (px > py > pz): before_cnt += 1
        pos[va], pos[vb] = pos[vb], pos[va]
        order[a], order[b] = vb, va
        after_cnt = 0
        for (x, y, z) in affected:
            px, py, pz = pos[x], pos[y], pos[z]
            if (px < py < pz) or (px > py > pz): after_cnt += 1
        delta = after_cnt - before_cnt
        if delta <= 0 or rng.random() < pow(2.718, -delta / max(T, 1e-9)):
            cur += delta
        else:
            pos[va], pos[vb] = pos[vb], pos[va]
            order[a], order[b] = va, vb
        if cur < best:
            best = cur
            if best == 0:
                print(f"FOUND at iter {it} ({time.time()-t0:.0f}s)", flush=True)
                json.dump(order, open(f'data/pure{X}_anneal.json', 'w'))
                return
        T = 3.0 * (1 - it / iters) + 0.02
        if it % 1000000 == 0:
            print(f"iter {it}: cur={cur} best={best} T={T:.2f} ({time.time()-t0:.0f}s)", flush=True)
    print(f"exhausted: best={best}", flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]), seed=int(sys.argv[2]) if len(sys.argv) > 2 else 0)
