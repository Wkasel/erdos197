"""Synthesize per-node child orders on the binary tree (depth d) such that
for all pairs of paths p (x, from an earlier cell => arbitrary) and q (y),
the completion path r = path(2y - x drift automaton) precedes q, whenever
the completion stays "in range" (no boundary escape; conservative).

Completion recursion on bit strings (low->high), state = drift delta:
  t_z = 2 t_y - t_x + delta   (start delta = 0)
  bit: b_z = (b_x + delta) mod 2 ... derive:
    t_z = 2 t_y - t_x + delta
    b_z = (delta - t_x) mod 2 = (delta + b_x) mod 2
    s_z = t_y - (t_x + b_x')/2 ... we compute exactly:
    t_z = 2 t_y - t_x + delta
    write t_x = 2 s_x + b_x, t_y = 2 s_y + b_y, t_z = 2 s_z + b_z:
    2 s_z + b_z = 4 s_y + 2 b_y - 2 s_x - b_x + delta
    b_z = (2 b_y - b_x + delta) mod 2 = (b_x + delta) mod 2
    s_z = (4 s_y + 2 b_y - 2 s_x - b_x + delta - b_z) / 2
        = 2 s_y - s_x + (2 b_y - b_x + delta - b_z)/2   (integer)
    new delta' = 2 b_y - b_x + delta - b_z  ... then s_z = 2 s_y - s_x + delta'/... 
    check: s_z = 2 s_y - s_x + (delta') where delta' = (2 b_y - b_x + delta - b_z)/2? 
    No: s_z = 2 s_y - s_x + D where D = (2 b_y - b_x + delta - b_z)/2, integer since
    b_z == (b_x + delta) mod 2. D in small range.
We verify the tree-order condition by exhaustive paths at depth d.
"""
from itertools import product

def completion_path(px, py, d):
    """bits low->high; returns bits of t_z (mod 2^d) and final drift."""
    delta = 0
    out = []
    for i in range(d):
        bx = px[i]
        by = py[i]
        bz = (bx + delta) % 2
        D = (2 * by - bx + delta - bz) // 2
        out.append(bz)
        delta = D
    return tuple(out), delta

def tree_rank(path, orders, d):
    """rank of path under per-node child-order; orders: dict node-prefix -> (first, second)"""
    r = 0
    prefix = ()
    for i in range(d):
        first, _ = orders[prefix]
        bit = path[i]
        if bit != first:
            r = 2 * r + 1
        else:
            r = 2 * r
        prefix = prefix + (bit,)
    return r

def check(orders, d, require_cross=True, require_same=True):
    paths = list(product((0, 1), repeat=d))
    ranks = {p: tree_rank(p, orders, d) for p in paths}
    for py in paths:
        for px in paths:
            pz, drift = completion_path(px, py, d)
            # conservative: require rank(pz) < rank(py) (strict; pz==py impossible? maybe equal)
            if require_cross:
                # cross-cell: x arbitrary earlier; need pz before py
                if ranks[pz] >= ranks[py] and pz != py:
                    return False, ('cross', px, py, pz)
                if pz == py:
                    # completion in same path-class as y: deeper bits decide; conservative fail
                    return False, ('equal', px, py, pz)
            if require_same:
                # same-cell increasing pair: only when rank(px) < rank(py)
                if ranks[px] < ranks[py]:
                    if ranks[pz] >= ranks[py] and pz != py:
                        return False, ('same', px, py, pz)
    return True, None

if __name__ == "__main__":
    d = 3
    # enumerate all per-node order assignments: nodes = prefixes of len < d
    nodes = []
    for l in range(d):
        nodes.extend(product((0, 1), repeat=l))
    print(f"depth {d}: {len(nodes)} nodes, {2**len(nodes)} assignments")
    found = 0
    for bits in product((0, 1), repeat=len(nodes)):
        orders = {}
        for node, b in zip(nodes, bits):
            orders[node] = (b, 1 - b)
        ok, why = check(orders, d, require_cross=True, require_same=False)
        if ok:
            found += 1
            if found <= 5:
                print("CROSS-OK assignment:", {n: o for n, o in orders.items()})
    print(f"cross-only satisfiable assignments: {found}")
    # same-cell only
    found2 = 0
    for bits in product((0, 1), repeat=len(nodes)):
        orders = {}
        for node, b in zip(nodes, bits):
            orders[node] = (b, 1 - b)
        ok, why = check(orders, d, require_cross=False, require_same=True)
        if ok:
            found2 += 1
    print(f"same-cell-only satisfiable assignments: {found2}")
