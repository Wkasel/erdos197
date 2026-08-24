"""Erdős #197 — the two-block interleaving game G(M).

Merge X = (M/4, M/2] (block K-2) and Y = (M, 2M] (block K) into one
timeline (arbitrary interleaving). Necessary constraints for the dyadic
team (restriction of the full problem to these two blocks):

 (aX) no monotone 3-AP inside X's induced order;
 (aY) no monotone 3-AP inside Y's induced order;
 (bC) for x in X, y in Y with x before y and z = 2y - x in Y: z before y.
 (Other cross completions leave the team's blocks: free.)

If G(M) is UNSAT for any M, the dyadic partition's team S_A admits NO
3-AP-free permutation at all.
"""
import sys
import time
sys.path.insert(0, 'experiments')
from e3_sat import OrderSAT


def game(M, return_seq=False):
    X = list(range(M // 4 + 1, M // 2 + 1))
    Y = list(range(M + 1, 2 * M + 1))
    V = X + Y
    enc = OrderSAT(V)
    Xs, Ys = set(X), set(Y)
    # (aX), (aY): monotone 3-APs within each part
    for part in (X, Y):
        ps = set(part)
        for y in part:
            d = 1
            while y + d <= max(part):
                a, c = y - d, y + d
                if a in ps and c in ps:
                    enc.add(-enc.before(a, y), -enc.before(y, c))
                    enc.add(-enc.before(c, y), -enc.before(y, a))
                d += 1
    # (bC): x in X before y in Y, z = 2y - x in Y  =>  z before y
    for x in X:
        for y in Y:
            z = 2 * y - x
            if z in Ys:
                # before(x,y) -> before(z,y)
                enc.add(-enc.before(x, y), enc.before(z, y))
    res = enc.solve()
    if res is None:
        raise RuntimeError("indeterminate")
    return res


if __name__ == "__main__":
    for M in [16, 32, 64, 128, 256]:
        t0 = time.time()
        r = game(M)
        dt = time.time() - t0
        if r is False:
            print(f"G({M}): UNSAT ({dt:.1f}s)  <-- dyadic team NOT permutable")
            break
        print(f"G({M}): SAT ({dt:.1f}s)")
        if M <= 32:
            print("   ", r)
