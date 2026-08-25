"""e113b_closure_crossval: independent cross-validation of the e113 hand
proof (notes/33 v2) by the e109 closure engine (R1-R4 + transitivity
fixpoint, an encoding independent of the schema checker).

For every branch of the hand proof's case trees the closure must reach a
contradiction on its own:

  Layer-1 tree (M = 0 mod 4):  A2 + A3 + [b3<b5]
      x split (t5<m0 | m0<t5)
      x phase axiom, one adjacent pair per relevant d=4 class:
        (b3,b7) both ways [class B] and (b1,b5) both ways [class A].
    8 branches; the hand proof needs only class B in Case I and class A
    in Case II, but all 8 close -- checked as the stronger statement.

  Flip tree (M = 0 mod 8):  A1 + A2 + A3 + [b5<b3 (layer-1 theorem)]
      Case I  (t5<m0) x LADA phase axiom (b1,b5) both ways;
      Case II (m0<t5) x LADB phase axiom (b3,b7) both ways.
    4 branches.

Note the phase axioms are NOT extra hypotheses of the theorems: by Lemma D
(phase dichotomy) one orientation of each adjacent pair holds in any
linear order, and the conclusion is derived under both.

Run: .venv/bin/python experiments/e113b_closure_crossval.py [--full]
Output: data/e113b_crossval.json
"""
import json
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e109_l0_trace import Tracer

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e113b_crossval.json"


def cross_l1(M):
    t3, t10 = 2 * M - 3, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    b1, b7 = M + 1, M + 7
    m0, t5 = 3 * M // 2, 2 * M - 5
    base = [(t3, b6), (t10, b3), (b3, b5)]
    for s1 in [(t5, m0), (m0, t5)]:
        for ph in [(b3, b7), (b7, b3), (b1, b5), (b5, b1)]:
            if not Tracer(M).run(base + [s1, ph]):
                return False
    return True


def cross_flip(M):
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    b1, b7 = M + 1, M + 7
    m0 = 3 * M // 2
    base = [(t5, b5), (t3, b6), (t10, b3), (b5, b3)]
    for ph in [(b1, b5), (b5, b1)]:                # Case I x LADA
        if not Tracer(M).run(base + [(t5, m0), ph]):
            return False
    for ph in [(b3, b7), (b7, b3)]:                # Case II x LADB
        if not Tracer(M).run(base + [(m0, t5), ph]):
            return False
    return True


def main():
    full = "--full" in sys.argv
    t0 = time.time()
    l1_scales = list(range(12, 201, 4)) + [256, 400, 512]
    fl_scales = list(range(16, 201, 8)) + [256, 400, 512]
    if full:
        l1_scales += [1024]
        fl_scales += [1024]
    out = {"layer1_ok": [], "flip_ok": [], "fail": []}
    for M in l1_scales:
        (out["layer1_ok"] if cross_l1(M) else out["fail"]).append(M)
    for M in fl_scales:
        (out["flip_ok"] if cross_flip(M) else out["fail"]).append(M)
    print(f"layer1: {len(out['layer1_ok'])}/{len(l1_scales)} scales OK")
    print(f"flip:   {len(out['flip_ok'])}/{len(fl_scales)} scales OK")
    print(f"failures: {out['fail']}  ({time.time()-t0:.0f}s)")
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}")
    if out["fail"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
