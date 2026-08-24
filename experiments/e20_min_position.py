"""Measure d_X(v) = min #predecessors of value v over pure-complete-X
doom-free arrangements. Divergence in X => Erdős #197 is NO (provably)."""
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
    # doom pairs: completions inside S_A(<=2X handled: (X,2X] odd -> free)
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

def min_pos(X, target, ub=None):
    V, before, cl, top = build(X)
    lits = [before(u, target) for u in V if u != target]
    lo, hi = 0, (ub if ub else len(V) - 1)
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        card = CardEnc.atmost(lits=lits, bound=mid, top_id=top + 1, encoding=EncType.seqcounter)
        s = Cadical195(bootstrap_with=cl + card.clauses)
        # lazy transitivity loop
        ok = None
        rounds = 0
        while True:
            rounds += 1
            if rounds > 400:
                ok = None; break
            if not s.solve():
                ok = False; break
            model = set(l for l in s.get_model() if l > 0)
            def bef(u, w):
                l = before(u, w)
                return (l in model) if l > 0 else (-l not in model)
            wins = {v: 0 for v in V}
            for i in range(len(V)):
                for j in range(i + 1, len(V)):
                    u, w = V[i], V[j]
                    if bef(u, w): wins[u] += 1
                    else: wins[w] += 1
            order = sorted(V, key=lambda v: -wins[v])
            added = 0
            for i in range(len(order)):
                for j in range(i + 1, len(order)):
                    u, w = order[i], order[j]
                    if not bef(u, w):
                        for x in order:
                            if x != u and x != w and bef(u, x) and bef(x, w):
                                s.add_clause([-before(u, x), -before(x, w), before(u, w)])
                                added += 1
                                break
                        if added > 10000: break
                if added > 10000: break
            if not added:
                ok = True
                break
        if ok is True:
            best = mid
            hi = mid - 1
        elif ok is False:
            lo = mid + 1
        else:
            print(f"  (indeterminate at bound {mid})", flush=True)
            lo = mid + 1  # conservative
    return best

if __name__ == "__main__":
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for X in [16, 64, 256, 1024]:
        t0 = time.time()
        d = min_pos(X, target)
        print(f"X={X}: d_X({target}) = {d}  ({time.time()-t0:.1f}s)", flush=True)
