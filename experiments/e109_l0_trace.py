"""e109_l0_trace: TASK P -- extract explicit derivation traces for the S1
layer lemmas from R1-R4 + transitivity closure (provenance-tracking).

e105 established that L0a and L0b refute by PURE closure (no case splits)
at every tested even M.  For the hand proof (notes/33) we need the actual
derivation: each derived precedence with its rule and premises, sliced
backward from the contradiction.  If the sliced DAG is scale-uniform
(fixed offset families + arithmetic ladders), the lemma is hand-provable.

Rules on an AP triple (x, y, z), y the midpoint (z = 2y - x):
  R1: x<y => z<y      R3: z<y => x<y      (y trails)
  R4: y<x => y<z      R2: y<z => y<x      (y leads)
plus transitivity.  BFS worklist; first derivation of each edge is kept.

Usage: .venv/bin/python experiments/e109_l0_trace.py STEP M [M ...]
   STEP in {L0a, L0b, L1a-1, L1a-2, L1b-1, L1b-2, L2-1, L2-2, ...}
   (L1a-1 = leaf 1 of the L1a case tree, etc.; see units_for)
Output: printed trace (offset coordinates) + data/e109_traces.json
"""
import json
import sys
from collections import deque

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e109_traces.json"


def name(M, v):
    """Offset name: b_j = M+j for lower half, t_i = 2M-i for upper half,
    m+ notation if exactly midband-ish. Keep simple: b for v-M <= M/2."""
    j = v - M
    i = 2 * M - v
    return f"b{j}" if j <= M // 2 else f"t{i}"


class Tracer:
    def __init__(self, M):
        self.M = M
        self.V = list(range(M + 1, 2 * M + 1))
        self.n = len(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.succ = [0] * self.n           # succ[i] bit j: i before j
        self.reason = {}                   # (i,j) -> reason tuple
        self.depth = {}                    # (i,j) -> BFS depth
        # implication table: (i,j) -> list of ((k,l), rule, triple)
        self.imp = {}
        for y in self.V:
            d = 1
            while y + d <= 2 * M:
                x, z = y - d, y + d
                d += 1
                if x <= M:
                    continue
                ix, iy, iz = self.idx[x], self.idx[y], self.idx[z]
                t = (x, y, z)
                self.imp.setdefault((ix, iy), []).append(((iz, iy), "R1", t))
                self.imp.setdefault((iz, iy), []).append(((ix, iy), "R3", t))
                self.imp.setdefault((iy, ix), []).append(((iy, iz), "R4", t))
                self.imp.setdefault((iy, iz), []).append(((iy, ix), "R2", t))
        self.queue = deque()
        self.contra = None                 # ((i,j),(j,i)) when found

    def add(self, i, j, reason, depth):
        if self.succ[i] >> j & 1:
            return
        self.succ[i] |= 1 << j
        self.reason[(i, j)] = reason
        self.depth[(i, j)] = depth
        self.queue.append((i, j))
        if self.succ[j] >> i & 1 and self.contra is None:
            self.contra = ((i, j), (j, i))

    def run(self, units):
        """units: list of (u,w) value pairs. Returns True if contradiction."""
        for (u, w) in units:
            self.add(self.idx[u], self.idx[w], ("axiom",), 0)
        pred = [0] * self.n
        for (i, j) in list(self.reason):
            pred[j] |= 1 << i
        while self.queue and self.contra is None:
            i, j = self.queue.popleft()
            d = self.depth[(i, j)]
            pred[j] |= 1 << i
            # reflection
            for (e, rule, t) in self.imp.get((i, j), ()):
                self.add(e[0], e[1], (rule, t, (i, j)), d + 1)
                if self.contra:
                    return True
            # transitivity: x -> i -> j  and  i -> j -> y
            t = pred[i]
            while t:
                x = (t & -t).bit_length() - 1
                t &= t - 1
                self.add(x, j, ("T", (x, i), (i, j)), d + 1)
                if self.contra:
                    return True
            t = self.succ[j]
            while t:
                y = (t & -t).bit_length() - 1
                t &= t - 1
                self.add(i, y, ("T", (i, j), (j, y)), d + 1)
                if self.contra:
                    return True
        return self.contra is not None

    def slice(self):
        """Backward slice from the contradiction; returns ordered list of
        (edge, reason) with axioms first (topological by dependency)."""
        assert self.contra
        need, order, seen = list(self.contra), [], set()

        def visit(e):
            if e in seen:
                return
            seen.add(e)
            r = self.reason[e]
            if r[0] == "T":
                visit(r[1])
                visit(r[2])
            elif r[0] != "axiom":
                visit(r[2])
            order.append((e, r))

        for e in need:
            visit(e)
        return order

    def fmt_edge(self, e):
        return f"{name(self.M, self.V[e[0]])}<{name(self.M, self.V[e[1]])}"

    def fmt(self, order):
        M = self.M
        out = []
        for k, (e, r) in enumerate(order):
            lhs = self.fmt_edge(e)
            if r[0] == "axiom":
                out.append(f"{k:3d}. {lhs:14s} [axiom]")
            elif r[0] == "T":
                out.append(f"{k:3d}. {lhs:14s} [trans {self.fmt_edge(r[1])}"
                           f" + {self.fmt_edge(r[2])}]")
            else:
                x, y, z = r[1]
                out.append(
                    f"{k:3d}. {lhs:14s} [{r[0]} on AP ({name(M,x)},"
                    f"{name(M,y)},{name(M,z)}) d={y-x} from"
                    f" {self.fmt_edge(r[2])}]")
        return "\n".join(out)


def units_for(step, M):
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    A2, A3 = (t3, b6), (t10, b3)
    L0 = [(t3, b3), (t10, b6)]
    L1 = [(t3, t5), (b5, b3)]
    b1, b2, b4, b7 = M + 1, M + 2, M + 4, M + 7
    steps = {
        "L0a": [A2, A3, (b3, t3)],
        "L0b": [A2, A3, (b6, t10)],
        # L1a case-tree leaves (split on b1 vs b5; e105 shape)
        "L1a-1": [A2, A3] + L0 + [(t5, t3), (b1, b5)],
        "L1a-2": [A2, A3] + L0 + [(t5, t3), (b5, b1)],
        # L1b leaves
        "L1b-1": [A2, A3] + L0 + [(b3, b5), (b1, b5)],
        "L1b-2": [A2, A3] + L0 + [(b3, b5), (b5, b1)],
        # L1a fixed-tree leaves: split1 b1/b2, split2 b1/b5
        "L1a-11": [A2, A3] + L0 + [(t5, t3), (b1, b2), (b1, b5)],
        "L1a-12": [A2, A3] + L0 + [(t5, t3), (b1, b2), (b5, b1)],
        "L1a-21": [A2, A3] + L0 + [(t5, t3), (b2, b1), (b1, b5)],
        "L1a-22": [A2, A3] + L0 + [(t5, t3), (b2, b1), (b5, b1)],
        # L1b fixed-tree leaves
        "L1b-11": [A2, A3] + L0 + [(b3, b5), (b1, b2), (b1, b5)],
        "L1b-12": [A2, A3] + L0 + [(b3, b5), (b1, b2), (b5, b1)],
        "L1b-21": [A2, A3] + L0 + [(b3, b5), (b2, b1), (b1, b5)],
        "L1b-22": [A2, A3] + L0 + [(b3, b5), (b2, b1), (b5, b1)],
        # L2 leaves (splits to be determined)
        "L2": [A2, A3] + L0 + L1 + [(t5, b5)],
        "L2-11": [A2, A3] + L0 + L1 + [(t5, b5), (b1, b2), (b1, b5)],
        "L2-12": [A2, A3] + L0 + L1 + [(t5, b5), (b1, b2), (b5, b1)],
        "L2-21": [A2, A3] + L0 + L1 + [(t5, b5), (b2, b1), (b1, b5)],
        "L2-22": [A2, A3] + L0 + L1 + [(t5, b5), (b2, b1), (b5, b1)],
    }
    return steps[step]


def main():
    step = sys.argv[1]
    Ms = [int(x) for x in sys.argv[2:]] or [40, 42]
    try:
        out = json.load(open(DATA))
    except Exception:
        out = {}
    out.setdefault(step, {})
    for M in Ms:
        tr = Tracer(M)
        got = tr.run(units_for(step, M))
        print(f"===== {step} M={M}: "
              f"{'CONTRADICTION' if got else 'no contradiction (closure)'}")
        if got:
            order = tr.slice()
            print(tr.fmt(order))
            gen = []
            for (e, r) in order:
                lhs = [name(M, tr.V[e[0]]), name(M, tr.V[e[1]])]
                if r[0] == "axiom":
                    gen.append([lhs, "axiom"])
                elif r[0] == "T":
                    gen.append([lhs, "T",
                                [name(M, tr.V[r[1][0]]),
                                 name(M, tr.V[r[1][1]])],
                                [name(M, tr.V[r[2][0]]),
                                 name(M, tr.V[r[2][1]])]])
                else:
                    gen.append([lhs, r[0],
                                [name(M, v) for v in r[1]],
                                [name(M, tr.V[r[2][0]]),
                                 name(M, tr.V[r[2][1]])]])
            out[step][str(M)] = {"n_steps": len(order), "steps": gen}
        else:
            out[step][str(M)] = None
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}")


if __name__ == "__main__":
    main()
