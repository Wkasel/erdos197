"""Extract a minimal UNSAT core (as a subset of block values) for the
failing per-block instances. Dropping values only removes constraints,
so a minimal UNSAT value-subset is a genuine witness of impossibility."""
import sys
sys.path.insert(0, 'experiments')
from e3_sat import decide


def shrink(B, Z):
    B = list(B)
    assert decide(B, Z) is False, "instance is not UNSAT"
    changed = True
    while changed:
        changed = False
        for v in sorted(B, key=lambda x: -x):
            trial = [u for u in B if u != v]
            if decide(trial, Z) is False:
                B = trial
                changed = True
    return B


if __name__ == "__main__":
    # dyadic block 5: (16,32], zone = (4,8] + {2} (+ {1} variant)
    for Z in [set(range(5, 9)) | {2}, set(range(5, 9)), set(range(5, 9)) | {1, 2}]:
        B = list(range(17, 33))
        if decide(B, Z) is False:
            core = shrink(B, Z)
            print(f"Z={sorted(Z)}: UNSAT, minimal core = {core}")
            # print the constraints among the core
            Bs = set(core)
            print("  forced (z before y):", [(y, 2*y-x) for y in core for x in Z
                                             if 2*y-x in Bs and 2*y-x > y])
            aps = [(x, y, z) for y in core for d in range(1, 16)
                   for x, z in [(y-d, y+d)] if x in Bs and z in Bs and x < y]
            print("  3-APs in core:", aps)
        else:
            print(f"Z={sorted(Z)}: SAT")
