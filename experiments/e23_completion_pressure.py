"""g_X(L) = min over pure-complete-X arrangements of max_{v in S_A∩[1,L]}
#predecessors(v). If g_X(L) diverges in X for fixed L => Erdős #197 dyadic NO."""
import sys, time
sys.path.insert(0, 'experiments')
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def build(X):
    V = sa(X)
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    top = 0
    t = {}
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            t[(i, j)] = top
    def before(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]
    cl = []
    Vs = set(V)
    for y in V:
        d = 1
        while y + d <= X:
            a, c = y - d, y + d
            if a in Vs and c in Vs:
                cl.append([-before(a, y), -before(y, c)])
                cl.append([-before(c, y), -before(y, a)])
            d += 1
    for a in V:
        for b in V:
            if b <= a: continue
            c = 2 * b - a
            if c in Vs:
                cl.append([-before(a, b), before(c, b)])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                cl.append([-before(b, a), before(d2, a)])
    return V, before, cl, top

def g(X, L):
    V, before, cl0, top = build(X)
    small = [v for v in V if v <= L]
    lo, hi = len(small) - 1, len(V) - 1
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        cl = list(cl0)
        tid = top
        for v in small:
            lits = [before(u, v) for u in V if u != v]
            card = CardEnc.atmost(lits=lits, bound=mid, top_id=tid + 1,
                                  encoding=EncType.seqcounter)
            tid = card.nv
            cl.extend(card.clauses)
        s = Cadical195(bootstrap_with=cl)
        ok = None
        rounds = 0
        while True:
            rounds += 1
            if rounds > 600:
                ok = None; break
            if not s.solve():
                ok = False; break
            model = set(l for l in s.get_model() if l > 0)
            def bef(u, w):
                l = before(u, w)
                return (l in model) if l > 0 else (-l not in model)
            wins = {v: 0 for v in V}
            n = len(V)
            for i in range(n):
                for j in range(i + 1, n):
                    u, w = V[i], V[j]
                    if bef(u, w): wins[u] += 1
                    else: wins[w] += 1
            order = sorted(V, key=lambda v: -wins[v])
            added = 0
            for i in range(n):
                for j in range(i + 1, n):
                    u, w = order[i], order[j]
                    if not bef(u, w):
                        for x in order:
                            if x != u and x != w and bef(u, x) and bef(x, w):
                                s.add_clause([-before(u, x), -before(x, w),
                                              before(u, w)])
                                added += 1
                                break
                        if added > 15000: break
                if added > 15000: break
            if not added:
                ok = True; break
        if ok is True:
            best = mid; hi = mid - 1
        elif ok is False:
            lo = mid + 1
        else:
            print(f"  indeterminate at {mid}", flush=True)
            lo = mid + 1
    return best

if __name__ == "__main__":
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    for X in [64, 256, 1024]:
        if X < L: continue
        t0 = time.time()
        r = g(X, L)
        print(f"g_{X}({L}) = {r}   (|S_A∩[1,{L}]|={len(sa(L))})  ({time.time()-t0:.0f}s)", flush=True)
