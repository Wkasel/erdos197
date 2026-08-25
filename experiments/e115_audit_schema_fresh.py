"""e115_audit_schema_fresh: run the e113 strict schema checker at
adversarially chosen scales the author did NOT test (e113 swept 12..400 +
{512, 1024}); here: 404, 408, 520, 808, 1000, 1004, 2048, 4096 (layer 1,
M = 0 mod 4) and 408, 520, 808, 1000, 2048, 4096 (flip, M = 0 mod 8), plus
sharpness at fresh 4-mod-8 scales 404, 1004, 2052.

Also: halving bookkeeping (Lemma H, notes/33 A.1) verified exhaustively --
bijectivity of h_E, h_O onto (m, 2m] and exact AP preservation/reflection
within each parity class -- for every even M in 4..240, plus the descended
C3 offset table.

Run: .venv/bin/python experiments/e115_audit_schema_fresh.py
Output: data/e115_audit_schema.json
"""
import json
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e113_c3_hand_proof import check_layer1, check_flip, sharpness_4mod8

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e115_audit_schema.json"


def halving_check(M):
    """Lemma H, exact bookkeeping."""
    assert M % 2 == 0
    m = M // 2
    evens = list(range(M + 2, 2 * M + 1, 2))
    odds = list(range(M + 1, 2 * M, 2))
    hE = {v: v // 2 for v in evens}
    hO = {v: (v + 1) // 2 for v in odds}
    half = list(range(m + 1, 2 * m + 1))
    assert sorted(hE.values()) == half, ("h_E not bijective", M)
    assert sorted(hO.values()) == half, ("h_O not bijective", M)

    for vals, h in ((evens, hE), (odds, hO)):
        vset = set(vals)
        # preservation: source AP maps to image AP
        for x in vals:
            for y in vals:
                if x >= y:
                    continue
                z = 2 * y - x
                if z in vset:
                    assert 2 * h[y] == h[x] + h[z], \
                        ("AP not preserved", M, x, y, z)
        # reflection: any image AP pulls back to a source AP
        inv = {w: v for v, w in h.items()}
        for a in half:
            for b in half:
                if a >= b:
                    continue
                c = 2 * b - a
                if c in inv and a in inv and b in inv:
                    x, y, z = inv[a], inv[b], inv[c]
                    assert x + z == 2 * y, ("AP not reflected", M, a, b, c)
    # descended C3 images (notes/33 A.1 table); needs all six in-block
    if M >= 12:
        t3, t5, b3, b5 = 2 * M - 3, 2 * M - 5, M + 3, M + 5
        t10, b6 = 2 * M - 10, M + 6
        assert hO[t3] == 2 * m - 1 and hO[t5] == 2 * m - 2
        assert hO[b3] == m + 2 and hO[b5] == m + 3
        assert hE[t10] == 2 * m - 5 and hE[b6] == m + 3
    return True


def main():
    out = {"layer1": [], "flip": [], "sharp": [], "halving": [], "fail": []}
    for M in [404, 408, 520, 808, 1000, 1004, 2048, 4096]:
        t0 = time.time()
        try:
            check_layer1(M)
            out["layer1"].append(M)
            print(f"e113 layer1 schema OK at fresh M={M} "
                  f"({time.time()-t0:.0f}s)", flush=True)
        except Exception as ex:
            out["fail"].append(["layer1", M, repr(ex)[:200]])
            print(f"e113 layer1 FAILED at M={M}: {ex}", flush=True)
    for M in [408, 520, 808, 1000, 2048, 4096]:
        t0 = time.time()
        try:
            check_flip(M)
            out["flip"].append(M)
            print(f"e113 flip schema OK at fresh M={M} "
                  f"({time.time()-t0:.0f}s)", flush=True)
        except Exception as ex:
            out["fail"].append(["flip", M, repr(ex)[:200]])
            print(f"e113 flip FAILED at M={M}: {ex}", flush=True)
    for M in [404, 1004, 2052]:
        try:
            sharpness_4mod8(M)
            out["sharp"].append(M)
        except Exception as ex:
            out["fail"].append(["sharp", M, repr(ex)[:200]])
    for M in range(4, 241, 2):
        try:
            halving_check(M)
            out["halving"].append(M)
        except AssertionError as ex:
            out["fail"].append(["halving", M, repr(ex.args)[:200]])
    print(f"halving OK at {len(out['halving'])} even scales 4..240", flush=True)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}; failures: {out['fail']}")
    sys.exit(1 if out["fail"] else 0)


if __name__ == "__main__":
    main()
