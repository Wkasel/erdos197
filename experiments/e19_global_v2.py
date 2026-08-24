"""Global incremental solve v2: sparse constrained-pair vars + digraph
acyclicity (no tournament). Commit one A-level per step, solve with
mandatory TWO levels beyond the commitment.
"""
import sys, time
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def in_sa(v):
    return v >= 2 and block(v) % 2 == 0

def sa(hi):
    return [v for v in range(2, hi + 1) if in_sa(v)]

class Solver:
    def __init__(self):
        self.committed = []

    def solve(self, mandatory, horizon, commit_to):
        pool = [v for v in sa(horizon) if v not in set(self.committed)]
        V = self.committed + pool
        Vset = set(V)
        var = 0
        p = {}
        for v in V:
            var += 1
            p[v] = var
        tv = {}
        edges = []  # (u, w, var) meaning var true => u before w
        def before(u, w):
            nonlocal var
            key = (u, w) if u < w else (w, u)
            if key not in tv:
                var += 1
                tv[key] = var
            return tv[key] if u < w else -tv[key]
        cl = []
        for v in self.committed:
            cl.append([p[v]])
        comm = self.committed
        for i in range(len(comm)):
            for j in range(i + 1, len(comm)):
                cl.append([before(comm[i], comm[j])])
        commset = set(comm)
        for v in comm:
            for w in pool:
                cl.append([-p[w], before(v, w)])
        for v in pool:
            if v <= mandatory:
                cl.append([p[v]])
        # constraints
        n = len(V)
        Vs = sorted(V)
        for a in Vs:
            for b in Vs:
                if b <= a: continue
                c = 2 * b - a
                need = False
                if c in Vset:
                    cl.append([-p[a], -p[b], -before(a, b), p[c]])
                    cl.append([-p[a], -p[b], -before(a, b), before(c, b)])
                elif in_sa(c):
                    cl.append([-p[a], -p[b], -before(a, b)])
                d = 2 * a - b
                if d >= 1:
                    if d in Vset:
                        cl.append([-p[a], -p[b], -before(b, a), p[d]])
                        cl.append([-p[a], -p[b], -before(b, a), before(d, a)])
                    elif in_sa(d):
                        cl.append([-p[a], -p[b], -before(b, a)])
        s = Cadical195(bootstrap_with=cl)
        rounds = 0
        while True:
            rounds += 1
            if rounds > 3000:
                raise RuntimeError("rounds")
            if not s.solve():
                return False
            model = s.get_model()
            ms = set(l for l in model if l > 0)
            placed = set(v for v in V if p[v] in ms)
            # build digraph on placed from tv
            adj = {v: [] for v in placed}
            for (u, w), var_ in tv.items():
                if u in placed and w in placed:
                    if var_ in ms:
                        adj[u].append(w)
                    else:
                        adj[w].append(u)
            # batched cycle elimination: find many cycles per SAT round
            def find_cycle(adjx):
                WHITE, GRAY, BLACK = 0, 1, 2
                color = {v: WHITE for v in placed}
                parent = {}
                for start in placed:
                    if color[start] != WHITE: continue
                    stack = [(start, iter(adjx[start]))]
                    color[start] = GRAY
                    while stack:
                        node, it = stack[-1]
                        adv = False
                        for nxt in it:
                            if color[nxt] == WHITE:
                                color[nxt] = GRAY
                                parent[nxt] = node
                                stack.append((nxt, iter(adjx[nxt])))
                                adv = True
                                break
                            elif color[nxt] == GRAY:
                                path = [node]
                                cur = node
                                while cur != nxt:
                                    cur = parent[cur]
                                    path.append(cur)
                                path.reverse()
                                return path
                        if not adv:
                            color[node] = BLACK
                            stack.pop()
                return None

            nfound = 0
            cycle = find_cycle(adj)
            while cycle is not None and nfound < 400:
                lits = []
                for i3 in range(len(cycle)):
                    u, w = cycle[i3], cycle[(i3 + 1) % len(cycle)]
                    lits.append(-before(u, w))
                s.add_clause(lits)
                nfound += 1
                # remove one edge of this cycle from working graph
                u0, w0 = cycle[0], cycle[1]
                adj[u0] = [x for x in adj[u0] if x != w0]
                cycle = find_cycle(adj)
            if nfound:
                continue
            if True:
                # topological order of placed
                indeg = {v: 0 for v in placed}
                for u in adj:
                    for w in adj[u]:
                        indeg[w] += 1
                import heapq
                h = [v for v in placed if indeg[v] == 0]
                out = []
                seen = set()
                # stable: process smaller first
                h.sort()
                from collections import deque
                dq = deque(h)
                indeg2 = dict(indeg)
                avail = sorted(v for v in placed if indeg2[v] == 0)
                import bisect
                while avail:
                    v = avail.pop(0)
                    out.append(v)
                    for w in adj[v]:
                        indeg2[w] -= 1
                        if indeg2[w] == 0:
                            bisect.insort(avail, w)
                return out

    def run(self, plan):
        for (commit_to, mandatory, horizon) in plan:
            t0 = time.time()
            r = self.solve(mandatory, horizon, commit_to)
            dt = time.time() - t0
            if r is False:
                print(f"commit_to={commit_to} mand={mandatory} hor={horizon}: UNSAT ({dt:.1f}s)", flush=True)
                return False
            need = set(v for v in sa(commit_to))
            seen = set()
            cut = 0
            for i, v in enumerate(r):
                seen.add(v)
                if need <= seen:
                    cut = i + 1
                    break
            self.committed = r[:cut]
            print(f"commit_to={commit_to}: ok ({dt:.1f}s) committed {cut} "
                  f"(max {max(self.committed)})", flush=True)
        return True

if __name__ == "__main__":
    sv = Solver()
    plan = [(16, 256, 1024), (64, 1024, 4096)]
    sv.run(plan)
    print("prefix:", sv.committed, flush=True)
