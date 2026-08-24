"""Erdős #197 — chained two-block games with carried order.

Solve game (block K-2, block K) freely; then game (block K, block K+2)
with block K's INTERNAL order fixed from the previous solution; iterate.
If the chain runs forever (tested: several links), the dyadic team's
permutation can be assembled scale by scale.
Each game: lower L = (M/4, M/2], upper U = (M, 2M]; constraints as e12.
"""
import sys
import time
sys.path.insert(0, 'experiments')
from e3_sat import OrderSAT


def solve_game(M, lower_order=None):
    L = list(range(M // 4 + 1, M // 2 + 1))
    U = list(range(M + 1, 2 * M + 1))
    enc = OrderSAT(L + U)
    for part in (L, U):
        ps = set(part)
        for y in part:
            d = 1
            while y + d <= max(part):
                a, c = y - d, y + d
                if a in ps and c in ps:
                    enc.add(-enc.before(a, y), -enc.before(y, c))
                    enc.add(-enc.before(c, y), -enc.before(y, a))
                d += 1
    Us = set(U)
    for x in L:
        for y in U:
            z = 2 * y - x
            if z in Us:
                enc.add(-enc.before(x, y), enc.before(z, y))
    if lower_order is not None:
        assert sorted(lower_order) == L
        for i in range(len(lower_order)):
            for j in range(i + 1, len(lower_order)):
                enc.add(enc.before(lower_order[i], lower_order[j]))
    r = enc.solve()
    if r is None:
        raise RuntimeError("indet")
    return r


if __name__ == "__main__":
    M = 16
    lower_order = None
    for link in range(6):
        t0 = time.time()
        r = solve_game(M, lower_order)
        dt = time.time() - t0
        if r is False:
            print(f"link {link}: game(M={M}) with carried order: UNSAT ({dt:.1f}s)")
            break
        upper = [v for v in r if v > M]
        print(f"link {link}: game(M={M}) SAT ({dt:.1f}s); carrying order of ({M},{2*M}]")
        if M <= 64:
            print("   upper order:", upper)
        lower_order = upper  # becomes lower block of the next game (M *= 4)
        M *= 4
