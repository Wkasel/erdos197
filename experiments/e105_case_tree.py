"""e105_case_tree: TASK P -- extract pencil-checkable case-tree derivations
for the graded forcing steps (S1 layers) from R1-R4 + transitivity alone.

Engine: state = set of known precedences on (M,2M].  Closure = fixpoint of
  - transitivity, and
  - the four reflection rules on every AP triple (x,y,z), z=2y-x:
      x<y => z<y ; z<y => x<y ; y<x => y<z ; y<z => y<x
Contradiction = a 2-cycle.  A step "axioms |- goal" is derivable with k
splits if the state axioms+NOT(goal) refutes by a case tree with <= k
binary splits on undetermined pairs.

We search shallow trees (iterative deepening over split count) with split
candidates restricted to pairs of a relevant window (values appearing in
the step's e104 MUS, expressed scale-generically).

Usage: .venv/bin/python experiments/e105_case_tree.py [L0a|L0b|L1a|L1b|L2] M...
Output: printed tree + data/e105_trees.json
"""
import json
import sys
import time

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e105_trees.json"


class Engine:
    def __init__(self, M):
        self.M = M
        self.V = list(range(M + 1, 2 * M + 1))
        self.n = len(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        # AP triples as index triples
        self.tri = []
        for y in self.V:
            d = 1
            while y + d <= 2 * M:
                x, z = y - d, y + d
                d += 1
                if x > M:
                    self.tri.append((self.idx[x], self.idx[y], self.idx[z]))

    def closure(self, succ):
        """succ: list of int bitmasks (succ[i] bit j set = i before j).
        Returns (succ', contradiction: bool).  Mutates a copy."""
        succ = list(succ)
        n = self.n
        changed = True
        while changed:
            changed = False
            # transitive closure by iterating until stable
            stable = False
            while not stable:
                stable = True
                for i in range(n):
                    s = succ[i]
                    new = s
                    t = s
                    while t:
                        j = (t & -t).bit_length() - 1
                        t &= t - 1
                        new |= succ[j]
                    if new != s:
                        succ[i] = new
                        stable = False
            # contradiction?
            for i in range(n):
                if succ[i] >> i & 1:
                    return succ, True
                t = succ[i]
                while t:
                    j = (t & -t).bit_length() - 1
                    t &= t - 1
                    if succ[j] >> i & 1:
                        return succ, True
            # reflection rules
            for (x, y, z) in self.tri:
                if succ[x] >> y & 1 and not (succ[z] >> y & 1):
                    succ[z] |= 1 << y
                    changed = True
                if succ[z] >> y & 1 and not (succ[x] >> y & 1):
                    succ[x] |= 1 << y
                    changed = True
                if succ[y] >> x & 1 and not (succ[y] >> z & 1):
                    succ[y] |= 1 << z
                    changed = True
                if succ[y] >> z & 1 and not (succ[y] >> x & 1):
                    succ[y] |= 1 << x
                    changed = True
        return succ, False

    def base(self, units):
        succ = [0] * self.n
        for (u, w) in units:
            succ[self.idx[u]] |= 1 << self.idx[w]
        return succ

    def known(self, succ, u, w):
        return succ[self.idx[u]] >> self.idx[w] & 1


def offsets_name(M, v):
    return f"b{v - M}" if v - M <= M // 2 else f"t{2 * M - v}"


def search_tree(eng, succ, cands, depth, memo=None):
    """Return tree or None.  Tree = 'X' (contradiction leaf) or
    (pair, tree_if_u<w, tree_if_w<u)."""
    succ, contra = eng.closure(succ)
    if contra:
        return "X"
    if depth == 0:
        return None
    # order candidates: prefer pairs where both branches derive many new facts
    scored = []
    for (u, w) in cands:
        iu, iw = eng.idx[u], eng.idx[w]
        if succ[iu] >> iw & 1 or succ[iw] >> iu & 1:
            continue
        s1 = list(succ)
        s1[iu] |= 1 << iw
        c1, x1 = eng.closure(s1)
        s2 = list(succ)
        s2[iw] |= 1 << iu
        c2, x2 = eng.closure(s2)
        if x1 and x2:
            return ((u, w), "X", "X")
        n1 = sum(bin(a).count("1") for a in c1)
        n2 = sum(bin(a).count("1") for a in c2)
        scored.append((min(n1 if not x1 else 10**9,
                           n2 if not x2 else 10**9),
                       (u, w), (c1, x1), (c2, x2)))
    scored.sort(key=lambda t: -t[0])
    for _, (u, w), (c1, x1), (c2, x2) in scored[:8]:
        t1 = "X" if x1 else search_tree(eng, c1, cands, depth - 1)
        if t1 is None:
            continue
        t2 = "X" if x2 else search_tree(eng, c2, cands, depth - 1)
        if t2 is None:
            continue
        return ((u, w), t1, t2)
    return None


def units_for(step, M):
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    A2, A3 = (t3, b6), (t10, b3)
    L0 = [(t3, b3), (t10, b6)]
    L1 = [(t3, t5), (b5, b3)]
    return {
        "L0a": [A2, A3, (b3, t3)],
        "L0b": [A2, A3, (b6, t10)],
        "L1a": [A2, A3] + L0 + [(t5, t3)],
        "L1b": [A2, A3] + L0 + [(b3, b5)],
        "L2": [A2, A3] + L0 + L1 + [(t5, b5)],
    }[step]


def cands_for(step, M):
    """Candidate split pairs: values from the e104 MUS of this step."""
    try:
        d = json.load(open(
            "/Users/will/Dev/personal/tasks/math/erdos197/data/"
            "e104_proof_steps.json"))["steps"][step]
        vals = set()
        entry = d.get(str(M))
        if isinstance(entry, dict):
            for b in entry["bot"]:
                vals |= {M + o for o in b}
        else:
            for MM, e in d.items():
                if MM.startswith("_") or not isinstance(e, dict):
                    continue
                for b in e["bot"]:
                    vals |= {M + o for o in b if M + o <= 2 * M}
    except Exception:
        vals = set(range(M + 1, 2 * M + 1))
    vals = sorted(vals)
    return [(u, w) for i, u in enumerate(vals) for w in vals[i + 1:]]


def fmt(tree, M, indent=0):
    pad = "  " * indent
    if tree == "X":
        return pad + "-> contradiction (closure)\n"
    (u, w), t1, t2 = tree
    s = pad + f"split {offsets_name(M, u)} vs {offsets_name(M, w)}:\n"
    s += pad + f" case {offsets_name(M, u)}<{offsets_name(M, w)}:\n"
    s += fmt(t1, M, indent + 1)
    s += pad + f" case {offsets_name(M, w)}<{offsets_name(M, u)}:\n"
    s += fmt(t2, M, indent + 1)
    return s


def tree_generic(tree, M):
    if tree == "X":
        return "X"
    (u, w), t1, t2 = tree
    return [[offsets_name(M, u), offsets_name(M, w)],
            tree_generic(t1, M), tree_generic(t2, M)]


def main():
    step = sys.argv[1]
    Ms = [int(x) for x in sys.argv[2:]] or [40]
    try:
        out = json.load(open(DATA))
    except Exception:
        out = {}
    out.setdefault(step, {})
    for M in Ms:
        t0 = time.time()
        eng = Engine(M)
        succ = eng.base(units_for(step, M))
        cands = cands_for(step, M)
        tree = None
        for depth in range(0, 5):
            tree = search_tree(eng, succ, cands, depth)
            if tree is not None:
                break
        dt = time.time() - t0
        if tree is None:
            print(f"[{step}] M={M}: NO tree with <=4 splits ({dt:.0f}s)",
                  flush=True)
            out[step][str(M)] = None
        else:
            print(f"[{step}] M={M}: tree found ({dt:.0f}s)", flush=True)
            print(fmt(tree, M), flush=True)
            out[step][str(M)] = tree_generic(tree, M)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}", flush=True)


if __name__ == "__main__":
    main()
