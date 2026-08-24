"""Exact SAT scan of alternating interval schemes for Erdős #197."""
import math
import sys
import time
sys.path.insert(0, 'experiments')
from e3_sat import decide


def make_blocks(ratio_fn, s0=2, cap=3000):
    S = [1, s0]
    while S[-1] < cap:
        nxt = max(math.ceil(ratio_fn(len(S) - 1) * S[-1]), 2 * S[-1])
        S.append(nxt)
    return S


def scheme_zones(S, k, one_owner):
    """Own past territory of the team owning block k (alternating)."""
    Z = set()
    j = k - 2
    while j >= 1:
        Z.update(range(S[j - 1] + 1, S[j] + 1))
        j -= 2
    if one_owner == (k % 2):
        Z.add(1)
    return Z


def test_scheme(label, S, val_cap=3000, tmax=120):
    print(f"scheme {label}: S={S[:9]}")
    for one_owner in (0, 1):
        oks = []
        for k in range(1, len(S)):
            lo, hi = S[k - 1], S[k]
            if hi > val_cap:
                break
            Z = scheme_zones(S, k, one_owner)
            t0 = time.time()
            r = decide(range(lo + 1, hi + 1), Z)
            dt = time.time() - t0
            oks.append((k, 'SAT' if r else 'UNSAT', f"{dt:.1f}s"))
            if not r:
                break
            if dt > tmax:
                oks.append((k, 'SLOW-STOP', ''))
                break
        print(f"  one->team{one_owner}: " + " ".join(f"b{k}:{s}" for k, s, _ in oks))
    return


if __name__ == "__main__":
    cap = 3000
    for r in [2.0, 2.2, 2.5, 3.0, 3.5, 4.0, 5.0]:
        test_scheme(f"r={r}", make_blocks(lambda k: r, cap=cap), val_cap=cap)
    for a, b in [(2.0, 3.0), (3.0, 2.0), (2.0, 4.0), (4.0, 2.0), (2.5, 3.5), (2.0, 8.0), (8.0, 2.0)]:
        test_scheme(f"ab={a},{b}",
                    make_blocks(lambda k, a=a, b=b: a if k % 2 == 0 else b, cap=cap),
                    val_cap=cap)
