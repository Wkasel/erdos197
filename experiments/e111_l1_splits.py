"""e111_l1_splits: search for STRUCTURED case splits for the L1/L2 forcing
steps -- split candidates are midband pivots vs the six C3 values, plus
small bottom/top pairs.  Goal: a fixed parametric tree, uniform over the
residue class, with closure at every leaf (checked by the e109 Tracer).

Usage: .venv/bin/python experiments/e111_l1_splits.py STEP M...
  STEP in {L1a, L1b, L2}
"""
import sys
sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e109_l0_trace import Tracer, name


def base_units(step, M):
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    A2, A3 = (t3, b6), (t10, b3)
    L0 = [(t3, b3), (t10, b6)]
    L1 = [(t3, t5), (b5, b3)]
    return {
        "L1a": [A2, A3] + L0 + [(t5, t3)],
        "L1b": [A2, A3] + L0 + [(b3, b5)],
        "L2": [A2, A3] + L0 + L1 + [(t5, b5)],
    }[step]


def closes(M, units):
    tr = Tracer(M)
    return tr.run(units)


def leaf_ok(M, units, splits, assign):
    extra = [(u, w) if bit else (w, u)
             for (u, w), bit in zip(splits, assign)]
    return closes(M, units + extra)


def tree_ok(M, step, splits):
    units = base_units(step, M)
    return all(leaf_ok(M, units, splits, tuple(bits))
               for bits in _assignments(len(splits)))


def _assignments(k):
    for x in range(2 ** k):
        yield [(x >> i) & 1 for i in range(k)]


def cands(M):
    t = lambda i: 2 * M - i
    b = lambda j: M + j
    m0 = 3 * M // 2
    out = []
    # pivot vs six values
    six = [t(5), t(3), t(10), b(3), b(5), b(6)]
    for a in (0, -2, -4, 2, 4):
        if (3 * M + a) % 2 == 0:
            ma = (3 * M + a) // 2
            for v in six:
                out.append((min(ma, v), max(ma, v)))
    # small bottom pairs
    for (u, w) in [(b(1), b(2)), (b(1), b(5)), (b(1), b(3)), (b(3), b(5)),
                   (b(2), b(4)), (b(1), b(9)), (b(2), b(6)),
                   (t(1), t(2)), (t(2), t(4)), (t(1), t(5)), (t(2), t(6)),
                   (t(1), t(9)), (t(4), t(8))]:
        out.append((u, w))
    return list(dict.fromkeys(out))


def main():
    step = sys.argv[1]
    Ms = [int(x) for x in sys.argv[2:]]
    M0 = Ms[0]
    C = cands(M0)
    # name candidates generically
    def gname(pair, M):
        return f"{name(M, pair[0])}/{name(M, pair[1])}"

    def geni(pair, M):
        # re-express candidate pair from M0 at M by generic name
        def tr(v):
            if v == 3 * M0 // 2:
                return 3 * M // 2
            if (3 * M0 - 4) // 2 == v:
                return (3 * M - 4) // 2
            if (3 * M0 - 2) // 2 == v:
                return (3 * M - 2) // 2
            if (3 * M0 + 2) // 2 == v:
                return (3 * M + 2) // 2
            if (3 * M0 + 4) // 2 == v:
                return (3 * M + 4) // 2
            if v - M0 <= M0 // 2:
                return M + (v - M0)
            return 2 * M - (2 * M0 - v)
        return (tr(pair[0]), tr(pair[1]))

    # single splits
    good1 = []
    for pair in C:
        if all(tree_ok(M, step, [geni(pair, M)]) for M in Ms):
            good1.append(pair)
            print(f"[1-split OK all M] {gname(pair, M0)}", flush=True)
    if good1:
        return
    # double splits (first found wins; prioritize pivot pairs)
    for i, p1 in enumerate(C):
        for p2 in C[i + 1:]:
            if all(tree_ok(M, step, [geni(p1, M), geni(p2, M)])
                   for M in Ms):
                print(f"[2-split OK all M] {gname(p1, M0)} + "
                      f"{gname(p2, M0)}", flush=True)
                return
    print("no 1/2-split uniform tree from candidate pool", flush=True)


if __name__ == "__main__":
    main()
