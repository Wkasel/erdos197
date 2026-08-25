"""e115_audit_closure: ADVERSARIAL AUDIT of notes/33 -- proof-level branch
closure by an independent, from-scratch closure engine (NOT the e109 Tracer;
different data structures and worklist policy).

Verifies at fresh scales that every branch of the hand-proof case trees is
closed by R1-R4 + transitivity alone (the e113b claim), and -- soundness
control -- that at M = 4 mod 8 the flip tree does NOT fully close (C3 is
SAT there, so some branch must stay open; an engine that closes everything
would be unsound).

  Layer-1 tree (M = 0 mod 4): A2 + A3 + [b3<b5]
      x split {t5<m0, m0<t5} x one phase pair {(b3,b7)+-, (b1,b5)+-}: 8.
  Flip tree (M = 0 mod 8): A1 + A2 + A3 + [b5<b3]
      Case I (t5<m0) x (b1,b5)+- ; Case II (m0<t5) x (b3,b7)+- : 4.

Run: .venv/bin/python experiments/e115_audit_closure.py [--big]
Output: data/e115_audit_closure.json
"""
import json
import sys
import time

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e115_audit_closure.json"


def closes(M, units, cap=None):
    """Forward closure of R1-R4 + transitivity from unit facts.
    Returns True iff a contradiction (u before v and v before u) is reached.
    Own implementation: successor/predecessor bitmasks, LIFO worklist."""
    lo, hi = M, 2 * M
    n = M
    off = lo + 1                       # value v <-> index v - off in [0, n)
    succ = [0] * n
    pred = [0] * n
    # implication lists per directed pair (midpoint rules)
    imp = {}
    for y in range(lo + 2, hi):
        dmax = min(y - lo - 1, hi - y)
        for d in range(1, dmax + 1):
            x, z = y - d, y + d
            ix, iy, iz = x - off, y - off, z - off
            imp.setdefault((ix, iy), []).append((iz, iy))   # R1
            imp.setdefault((iz, iy), []).append((ix, iy))   # R3
            imp.setdefault((iy, ix), []).append((iy, iz))   # R4
            imp.setdefault((iy, iz), []).append((iy, ix))   # R2
    stack = []

    def add(i, j):
        if succ[i] >> j & 1:
            return False
        succ[i] |= 1 << j
        pred[j] |= 1 << i
        stack.append((i, j))
        return succ[j] >> i & 1 == 1   # contradiction?

    for (u, w) in units:
        assert lo < u <= hi and lo < w <= hi and u != w
        if add(u - off, w - off):
            return True
    steps = 0
    while stack:
        i, j = stack.pop()
        steps += 1
        if cap and steps > cap:
            raise RuntimeError("cap exceeded")
        for (a, b) in imp.get((i, j), ()):
            if add(a, b):
                return True
        m = pred[i] & ~pred[j]
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if add(x, j):
                return True
        m = succ[j] & ~succ[i]
        while m:
            y = (m & -m).bit_length() - 1
            m &= m - 1
            if add(i, y):
                return True
    return False


def branches_l1(M):
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b1, b3, b5, b6, b7 = M + 1, M + 3, M + 5, M + 6, M + 7
    m0 = 3 * M // 2
    base = [(t3, b6), (t10, b3), (b3, b5)]
    for s in [(t5, m0), (m0, t5)]:
        for ph in [(b3, b7), (b7, b3), (b1, b5), (b5, b1)]:
            yield base + [s, ph]


def branches_flip(M):
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b1, b3, b5, b6, b7 = M + 1, M + 3, M + 5, M + 6, M + 7
    m0 = 3 * M // 2
    base = [(t5, b5), (t3, b6), (t10, b3), (b5, b3)]
    for ph in [(b1, b5), (b5, b1)]:
        yield base + [(t5, m0), ph]
    for ph in [(b3, b7), (b7, b3)]:
        yield base + [(m0, t5), ph]


def main():
    big = "--big" in sys.argv
    out = {"l1_ok": [], "flip_ok": [], "control": [], "fail": []}
    l1_scales = [204, 244, 404, 520] + ([1000] if big else [])
    fl_scales = [208, 328, 520] + ([1000] if big else [])
    for M in l1_scales:
        t0 = time.time()
        ok = all(closes(M, u) for u in branches_l1(M))
        (out["l1_ok"] if ok else out["fail"]).append(M)
        print(f"L1 branches M={M}: {'all closed' if ok else 'OPEN BRANCH'} "
              f"({time.time()-t0:.0f}s)", flush=True)
    for M in fl_scales:
        t0 = time.time()
        ok = all(closes(M, u) for u in branches_flip(M))
        (out["flip_ok"] if ok else out["fail"]).append(M)
        print(f"FLIP branches M={M}: {'all closed' if ok else 'OPEN BRANCH'} "
              f"({time.time()-t0:.0f}s)", flush=True)
    # soundness control: at M = 4 mod 8 the flip tree must NOT fully close
    for M in [204, 332]:
        assert M % 8 == 4
        res = [closes(M, u) for u in branches_flip(M)]
        ok = not all(res)
        (out["control"] if ok else out["fail"]).append([M, res])
        print(f"CONTROL M={M} (4 mod 8): branch closures = {res} "
              f"(engine {'sane' if ok else 'UNSOUND?'})", flush=True)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}; failures: {out['fail']}")
    sys.exit(1 if out["fail"] else 0)


if __name__ == "__main__":
    main()
