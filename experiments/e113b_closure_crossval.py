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


def verify_engine(M):
    """Do not trust the imported closure engine blindly: (1) re-derive the
    full R1-R4 implication table for scale M by independent brute force and
    compare EXACTLY with Tracer's; (2) soundness canary: AP-free
    permutations of the block (M, 2M] exist (shift of [1..M], classic
    even/odd construction), so the closure must NOT refute both
    orientations of an adjacent pair."""
    tr = Tracer(M)
    V = list(range(M + 1, 2 * M + 1))
    idx = {v: i for i, v in enumerate(V)}
    exp = {}
    for x in V:
        for z in V:
            if x < z and (x + z) % 2 == 0:
                y = (x + z) // 2          # midpoint; M < x < y < z <= 2M
                ix, iy, iz = idx[x], idx[y], idx[z]
                t = (x, y, z)
                exp.setdefault((ix, iy), []).append(((iz, iy), "R1", t))
                exp.setdefault((iz, iy), []).append(((ix, iy), "R3", t))
                exp.setdefault((iy, ix), []).append(((iy, iz), "R4", t))
                exp.setdefault((iy, iz), []).append(((iy, ix), "R2", t))
    got = {k: sorted(v) for k, v in tr.imp.items()}
    want = {k: sorted(v) for k, v in exp.items()}
    assert got == want, f"closure engine implication table mismatch at M={M}"
    b1, b2 = M + 1, M + 2
    assert not (Tracer(M).run([(b1, b2)]) and Tracer(M).run([(b2, b1)])), \
        f"closure engine UNSOUND at M={M}: refutes both orders of (b1,b2)"
    return True


# engine self-check at import time (cheap; two small scales)
verify_engine(12)
verify_engine(20)


def cross_l1(M):
    t3, t10 = 2 * M - 3, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    b1, b7 = M + 1, M + 7
    m0, t5 = 3 * M // 2, 2 * M - 5
    base = [(t3, b6), (t10, b3), (b3, b5)]
    splits = [(t5, m0), (m0, t5)]
    phases = [(b3, b7), (b7, b3), (b1, b5), (b5, b1)]
    # branch completeness: both orders of the split pair, both orientations
    # of both class pairs (Lemma D dichotomy) -- 8 leaves, all run.
    assert set(splits) == {(t5, m0), (m0, t5)} and len(splits) == 2
    assert set(phases) == {(b3, b7), (b7, b3), (b1, b5), (b5, b1)} \
        and len(phases) == 4
    runs = 0
    for s1 in splits:
        for ph in phases:
            if not Tracer(M).run(base + [s1, ph]):
                return False
            runs += 1
    assert runs == 8, (M, runs)
    return True


def cross_flip(M):
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    b1, b7 = M + 1, M + 7
    m0 = 3 * M // 2
    base = [(t5, b5), (t3, b6), (t10, b3), (b5, b3)]
    caseI = [(b1, b5), (b5, b1)]                   # Case I x LADA
    caseII = [(b3, b7), (b7, b3)]                  # Case II x LADB
    assert set(caseI) == {(b1, b5), (b5, b1)} and len(caseI) == 2
    assert set(caseII) == {(b3, b7), (b7, b3)} and len(caseII) == 2
    runs = 0
    for ph in caseI:
        if not Tracer(M).run(base + [(t5, m0), ph]):
            return False
        runs += 1
    for ph in caseII:
        if not Tracer(M).run(base + [(m0, t5), ph]):
            return False
        runs += 1
    assert runs == 4, (M, runs)
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
