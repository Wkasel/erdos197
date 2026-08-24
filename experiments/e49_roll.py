"""CLEAN joint viability: State(X) = complete-X + ANY extras within the next
c own-blocks; extension = complete-4X + ANY extras within its next c blocks.
No cardinality pins. UNSAT => genuine 'spillover exceeds c blocks' theorem
at this scale. Args: X c"""
import sys, time, json
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def clean_joint(X, c, max_rounds=8000, fixed_prefix=None):
    # state window: blocks (2X,4X], (8X,16X], ... c of them; ext shifted by one level
    def own_blocks_above(Y, count):
        out = []
        lo = 2 * Y
        for _ in range(count):
            out.append((lo, 2 * lo))
            lo *= 4
        return out
    sb = own_blocks_above(X, c)
    eb = own_blocks_above(4 * X, c)
    horizon = max(eb[-1][1], sb[-1][1])
    V = sa(horizon)
    Vs = set(V)
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    var = 0
    p1, p2 = {}, {}
    for v in V:
        var += 1; p1[v] = var
    for v in V:
        var += 1; p2[v] = var
    t = {}
    for i in range(n):
        for j in range(i + 1, n):
            var += 1
            t[(i, j)] = var
    def before(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]
    def in_win(v, wins):
        return any(lo < v <= hi for (lo, hi) in wins)
    cl = []
    for v in V:
        cl.append([-p1[v], p2[v]])
        if v <= X: cl.append([p1[v]])
        elif not in_win(v, sb): cl.append([-p1[v]])
        if v <= 4 * X: cl.append([p2[v]])
        elif not in_win(v, eb): cl.append([-p2[v]])
    # doom (completions beyond horizon: land in (horizon, 2*horizon] = odd block
    # if horizon is an own-block top: own_blocks tops are 2^k tops ✓ free)
    for a in V:
        for b in V:
            if b <= a: continue
            cc = 2 * b - a
            if cc in Vs:
                cl.append([-p2[a], -p2[b], -before(a, b), p2[cc]])
                cl.append([-p2[a], -p2[b], -before(a, b), before(cc, b)])
                cl.append([-p1[a], -p1[b], -before(a, b), p1[cc]])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                cl.append([-p2[a], -p2[b], -before(b, a), p2[d2]])
                cl.append([-p2[a], -p2[b], -before(b, a), before(d2, a)])
                cl.append([-p1[a], -p1[b], -before(b, a), p1[d2]])
    for u in V:
        for w in V:
            if u == w: continue
            cl.append([-p1[u], p1[w], -p2[w], before(u, w)])
    if fixed_prefix:
        fo = fixed_prefix
        for i in range(len(fo)):
            cl.append([p1[fo[i]] if False else p2[fo[i]]])
            for j in range(i + 1, len(fo)):
                cl.append([before(fo[i], fo[j])])
        # fixed prefix values are the earliest placed: before all other placed
        foset = set(fo)
        for u in fo:
            for w in V:
                if w in foset: continue
                cl.append([-p2[w], before(u, w)])
    print(f"X={X} c={c}: n={n} clauses={len(cl)}", flush=True)
    s = Cadical195(bootstrap_with=cl)
    rounds = 0
    while True:
        rounds += 1
        if rounds > max_rounds:
            raise RuntimeError("rounds")
        if not s.solve():
            return False
        model = s.get_model()
        ms = set(l for l in model if l > 0)
        placed2 = [v for v in V if p2[v] in ms]
        def bef(u, w):
            l = before(u, w)
            return (l in ms) if l > 0 else (-l not in ms)
        k = len(placed2)
        wins = {v: 0 for v in placed2}
        for i in range(k):
            for j in range(i + 1, k):
                u, w = placed2[i], placed2[j]
                if bef(u, w): wins[u] += 1
                else: wins[w] += 1
        order = sorted(placed2, key=lambda v: -wins[v])
        added = 0
        for i in range(k):
            for j in range(i + 1, k):
                u, w = order[i], order[j]
                if not bef(u, w):
                    for x in order:
                        if x != u and x != w and bef(u, x) and bef(x, w):
                            s.add_clause([-before(u, x), -before(x, w), before(u, w)])
                            added += 1
                            break
                    if added > 30000: break
            if added > 30000: break
        if not added:
            return [v for v in order if p1[v] in ms], order

if __name__ == "__main__":
    X, c = int(sys.argv[1]), int(sys.argv[2])
    fp = None
    if len(sys.argv) > 3:
        import json as _j
        fp = _j.load(open(sys.argv[3]))
    t0 = time.time()
    r = clean_joint(X, c, fixed_prefix=fp)
    tag = 'UNSAT' if r is False else 'SAT'
    print(f"CLEAN-JOINT X={X} c={c}: {tag} ({time.time()-t0:.0f}s)", flush=True)
    if r is not False:
        json.dump(r[0], open(f'data/clean_state_{X}_{c}.json', 'w'))
