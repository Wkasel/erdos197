#!/usr/bin/env python3
"""AUDIT A6 — independent derivation engine (method 2; NO SAT solver).

Written from scratch from paper/main.tex definitions only.

Idea: AP-freeness is a pure xor system over pair-orientation variables:
for each AP (a,b,c) in (M,2M], orient(a,b) != orient(b,c). These xor
constraints are handled exactly by a parity union-find over the C(n,2)
pair variables. Transitivity is handled by building the digraph of all
currently-assigned orientations and taking its transitive closure with
bitsets (a cycle = contradiction). New closure edges are fed back into
the parity structure until fixpoint. A tiny DPLL split (branch on an
undecided pair, both ways) finishes: if every branch reaches a
contradiction, the assumption set is refuted — a constructive proof,
independent of any SAT solver.

Verdicts: "UNSAT" (refuted; sound — every derivation step is a logical
consequence), "SAT" (a total AP-free order was actually constructed and
verified), "UNKNOWN" (search gave up; no claim).
"""
import sys, time


class Parity:
    """Union-find with parity over pair-ids, plus truth assignment."""
    def __init__(self, npairs):
        self.par = list(range(npairs))
        self.off = bytearray(npairs)      # parity to parent
        self.rank = bytearray(npairs)
        self.val = {}                     # root -> bool

    def find(self, x):
        # path compression, iterative, tracking parity
        root, p = x, 0
        while self.par[root] != root:
            p ^= self.off[root]
            root = self.par[root]
        # second pass: compress
        cur, cp = x, 0
        while self.par[cur] != cur:
            nxt = self.par[cur]
            noff = self.off[cur]
            self.par[cur] = root
            self.off[cur] = p ^ cp
            cp ^= noff
            cur = nxt
        return root, p

    def union(self, x, y, parity):
        """impose var_x = var_y ^ parity. Returns False on contradiction."""
        rx, px = self.find(x)
        ry, py = self.find(y)
        if rx == ry:
            return (px ^ py) == parity
        want = px ^ py ^ parity          # off between roots
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        vx = self.val.get(rx)
        vy = self.val.pop(ry, None)
        self.par[ry] = rx
        self.off[ry] = want
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] = min(self.rank[rx] + 1, 255)
        if vy is not None:
            vy2 = vy ^ want
            if vx is None:
                self.val[rx] = vy2
            elif vx != vy2:
                return False
        return True

    def assign(self, x, v):
        """set var_x = v. Returns False on contradiction."""
        r, p = self.find(x)
        cur = self.val.get(r)
        if cur is None:
            self.val[r] = v ^ p
            return True
        return (cur ^ p) == v

    def value(self, x):
        r, p = self.find(x)
        cur = self.val.get(r)
        return None if cur is None else (cur ^ p)

    def snapshot(self):
        return (list(self.par), bytes(self.off), bytes(self.rank),
                dict(self.val))

    def restore(self, snap):
        par, off, rank, val = snap
        self.par = list(par)
        self.off = bytearray(off)
        self.rank = bytearray(rank)
        self.val = dict(val)


class Engine:
    def __init__(self, M):
        self.M = M
        self.n = M
        self.vals = list(range(M + 1, 2 * M + 1))
        self.idx = {v: i for i, v in enumerate(self.vals)}
        n = self.n
        self.pid = lambda i, j: i * n + j          # only used with i<j
        self.pf = Parity(n * n)
        # xor constraints from all APs
        for d in range(1, (M - 1) // 2 + 1):
            for a in range(M + 1, 2 * M + 1 - 2 * d):
                b, c = a + d, a + 2 * d
                ia, ib, ic = self.idx[a], self.idx[b], self.idx[c]
                ok = self.pf.union(self.pid(ia, ib), self.pid(ib, ic), 1)
                assert ok, "AP xor constraints alone can never clash"

    def _lit(self, u, v):
        """(pairid, polarity) for 'value u precedes value v'."""
        iu, iv = self.idx[u], self.idx[v]
        if iu < iv:
            return self.pid(iu, iv), True
        return self.pid(iv, iu), False

    def assume(self, u, v):
        p, pol = self._lit(u, v)
        return self.pf.assign(p, pol)

    def orient(self, u, v):
        """True if u<v known, False if v<u known, None unknown (u,v values)."""
        p, pol = self._lit(u, v)
        r = self.pf.value(p)
        if r is None:
            return None
        return r if pol else (not r)

    # ---- propagation: closure of assigned digraph, feed back, fixpoint ----
    def propagate(self):
        """Returns 'CONTRA' | 'FIX'. Mutates parity state."""
        n = self.n
        while True:
            # build succ bitsets from all assigned pairs
            succ = [0] * n
            npairs_assigned = 0
            for i in range(n):
                base = i * n
                for j in range(i + 1, n):
                    v = self.pf.value(base + j)
                    if v is None:
                        continue
                    npairs_assigned += 1
                    if v:
                        succ[i] |= 1 << j
                    else:
                        succ[j] |= 1 << i
            # Kahn toposort on the assigned digraph
            indeg = [0] * n
            for i in range(n):
                s = succ[i]
                while s:
                    lb = s & -s
                    indeg[lb.bit_length() - 1] += 1
                    s ^= lb
            stack = [i for i in range(n) if indeg[i] == 0]
            order = []
            while stack:
                u = stack.pop()
                order.append(u)
                s = succ[u]
                while s:
                    lb = s & -s
                    w = lb.bit_length() - 1
                    indeg[w] -= 1
                    if indeg[w] == 0:
                        stack.append(w)
                    s ^= lb
            if len(order) < n:
                return "CONTRA"      # cycle among forced relations
            # transitive closure by reverse topological DP
            reach = [0] * n
            for u in reversed(order):
                r = succ[u]
                s = succ[u]
                while s:
                    lb = s & -s
                    r |= reach[lb.bit_length() - 1]
                    s ^= lb
                reach[u] = r
                if r & (1 << u):
                    return "CONTRA"
            # feed closure edges back into parity structure
            new = 0
            for i in range(n):
                base_i = i * n
                r = reach[i]
                s = r
                while s:
                    lb = s & -s
                    j = lb.bit_length() - 1
                    s ^= lb
                    if i < j:
                        p, pol = base_i + j, True
                    else:
                        p, pol = j * n + i, False
                    cur = self.pf.value(p)
                    if cur is None:
                        if not self.pf.assign(p, pol):
                            return "CONTRA"
                        new += 1
                    elif cur != pol:
                        return "CONTRA"
            if new == 0:
                return "FIX"

    # ---- tiny DPLL ----
    def decide_candidates(self):
        """Branching pairs, hand-proof-guided: (m0,t5), then ladder-phase
        pairs (one adjacent pair per ladder fixes that ladder's phase via
        the xor chains), then any undecided pair."""
        M = self.M
        m0 = 3 * M // 2
        cands = [(m0, 2 * M - 5),            # POLAR split (m0 vs t5)
                 (m0, m0 + 2),               # even d=2 ladder phase
                 (m0 + 1, m0 + 5),           # d=4 ladder phase, class of m0+1
                 (m0 - 1, m0 + 3),           # d=4 ladder phase, other class
                 (M + 1, M + 3)]             # odd d=2 ladder phase
        return cands

    def refute(self, assumptions, depth=8, verbose=False, _level=0):
        """UNSAT / SAT / UNKNOWN for AP-freeness + assumptions."""
        snap = self.pf.snapshot()
        try:
            for (u, v) in assumptions:
                if not self.assume(u, v):
                    return "UNSAT"
            r = self.propagate()
            if r == "CONTRA":
                return "UNSAT"
            # fixpoint w/o contradiction: complete order?
            und = None
            for (u, v) in self.decide_candidates():
                if self.orient(u, v) is None:
                    und = (u, v)
                    break
            if und is None:
                # scan all pairs for any undecided
                n = self.n
                for i in range(n):
                    base = i * n
                    for j in range(i + 1, n):
                        if self.pf.value(base + j) is None:
                            und = (self.vals[i], self.vals[j])
                            break
                    if und:
                        break
            if und is None:
                return "SAT"      # total assigned acyclic order = witness
            if depth == 0:
                return "UNKNOWN"
            u, v = und
            res = []
            for pol in ((u, v), (v, u)):
                sub = self.refute([pol], depth - 1, verbose, _level + 1)
                if verbose:
                    print(f"{'  '*_level}branch {pol[0]}<{pol[1]}: {sub}",
                          flush=True)
                if sub == "SAT":
                    return "SAT"
                res.append(sub)
            if all(x == "UNSAT" for x in res):
                return "UNSAT"
            return "UNKNOWN"
        finally:
            self.pf.restore(snap)


def run(M, tests=("E1", "E2", "F", "Fs", "C3"), depth=8):
    b = lambda j: M + j
    t = lambda i: 2 * M - i
    A1, A2, A3 = (t(5), b(5)), (t(3), b(6)), (t(10), b(3))
    suites = {
        "E1": ([(b(5), b(3)), (t(5), t(3))], "UNSAT"),
        "E2": ([(b(3), b(5)), (t(3), t(5))], "UNSAT"),
        "F":  ([A2, A3, (b(5), b(3)), A1], "UNSAT"),
        "Fs": ([A2, A3, (b(5), b(3))], "SAT"),
        "C3": ([A1, A2, A3], "UNSAT"),
    }
    print(f"== ENGINE  M = {M} (mod 8 = {M % 8}) ==", flush=True)
    t0 = time.time()
    eng = Engine(M)
    print(f"   built ({time.time()-t0:.1f}s)", flush=True)
    out = {}
    for name in tests:
        assum, expect = suites[name]
        t1 = time.time()
        v = eng.refute(assum, depth=depth)
        ok = "AGREE" if v == expect else ("(no claim)" if v == "UNKNOWN"
                                          else "*** DISAGREE ***")
        print(f"   {name:3s} -> {v:8s} (expect {expect}) {ok} "
              f"({time.time()-t1:.1f}s)", flush=True)
        out[name] = v
    return out


if __name__ == "__main__":
    Ms = [int(x) for x in sys.argv[1:]] or [48, 56, 104]
    for M in Ms:
        run(M)
