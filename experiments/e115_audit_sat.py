"""e115_audit_sat: ADVERSARIAL AUDIT of notes/33 (independent implementation).

Theorem-level SAT checks at scales the author never touched, written from
scratch (encoder + refinement loop independent of e89/e113/e114 code):

  A. Layer-1 (Thm L1): AP + A2 + A3 + (b3<b5) UNSAT, and
     AP + A2 + A3 + (t5<t3) UNSAT, at fresh M = 0 mod 4
     (404 = 4 mod 8 exercises the c* = m0-1 schema branch; 520 = 0 mod 8).
  B. C3 core: AP + A1 + A2 + A3 UNSAT at fresh M = 0 mod 8 (408, 520).
  C. Sharpness: AP + C3 SAT at M = 412 (4 mod 8) and M = 413 (odd), with
     the returned model INDEPENDENTLY validated as a genuine AP-free total
     order satisfying C3 (guards against encoder bugs making things UNSAT).
  D. Lemma L0 statement at fresh even scale 302: AP + A2 + A3 forces
     t3<b3 and t10<b6 (negations UNSAT).
  E. Lemma E lock at M = 2 mod 4 (46): AP + (b5<b3) + (t3<t5) UNSAT
     (the lock says b5<b3 <=> t5<t3 there); and at M = 0 mod 4 (52):
     AP + (b5<b3) + (t5<t3) UNSAT.

UNSAT verdicts are sound under lazy transitivity (clauses added are all
sound consequences of the order axioms).  SAT verdicts are only accepted
after full independent model validation (total order reconstruction +
exhaustive AP scan + C3 units).

Run: .venv/bin/python experiments/e115_audit_sat.py [--big]
Output: data/e115_audit_sat.json
"""
import json
import sys
import time

import numpy as np
from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e115_audit_sat.json"


def ap_triples(M):
    for y in range(M + 2, 2 * M):
        for d in range(1, min(y - M - 1, 2 * M - y) + 1):
            yield (y - d, y, y + d)


def solve(M, units):
    """Own encoder. Returns ('UNSAT', rounds) or ('SAT', order-list)."""
    V = list(range(M + 1, 2 * M + 1))
    n = len(V)
    pos = {v: k for k, v in enumerate(V)}

    def lit(u, w):
        i, j = pos[u], pos[w]
        assert i != j
        s = 1 if i < j else -1
        if i > j:
            i, j = j, i
        return s * (i * n + j + 1)   # sparse var ids, fine for Cadical

    cnf = [[lit(u, w)] for (u, w) in units]
    for (x, y, z) in ap_triples(M):
        cnf.append([-lit(x, y), -lit(y, z)])   # no rising monotone
        cnf.append([-lit(z, y), -lit(y, x)])   # no falling monotone
    sol = Cadical195(bootstrap_with=cnf)
    rounds = 0
    while True:
        if not sol.solve():
            return ("UNSAT", rounds)
        model = set(sol.get_model())
        B = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(i + 1, n):
                if (i * n + j + 1) in model:
                    B[i, j] = True
                else:
                    B[j, i] = True
        Bu = B.astype(np.uint8)
        viol = ((Bu @ Bu) > 0) & B.T          # i->k->j but j->i : broken
        ii, jj = np.nonzero(viol)
        if len(ii) == 0:
            # candidate genuine order: validate exhaustively
            wins = B.sum(axis=1)
            order = sorted(V, key=lambda v: -int(wins[pos[v]]))
            rank = {v: k for k, v in enumerate(order)}
            # validation 1: rank is consistent with B
            for i in range(n):
                for j in range(n):
                    if B[i, j]:
                        assert rank[V[i]] < rank[V[j]], "rank mismatch"
            # validation 2: all units
            for (u, w) in units:
                assert rank[u] < rank[w], ("unit violated", u, w)
            # validation 3: AP-freeness, exhaustive
            for (x, y, z) in ap_triples(M):
                rx, ry, rz = rank[x], rank[y], rank[z]
                assert not (rx < ry < rz) and not (rz < ry < rx), \
                    ("monotone AP", x, y, z)
            return ("SAT", order[:10])
        new = []
        for i, j in zip(ii[:20000], jj[:20000]):
            ks = np.nonzero(B[i] & B[:, j])[0]
            k = int(ks[0])
            new.append([-lit(V[i], V[k]), -lit(V[k], V[j]), lit(V[i], V[j])])
        sol.append_formula(new)
        rounds += 1


def main():
    big = "--big" in sys.argv
    out = {"checks": [], "fail": []}

    def C3(M):
        return [(2 * M - 5, M + 5), (2 * M - 3, M + 6), (2 * M - 10, M + 3)]

    def A23(M):
        return [(2 * M - 3, M + 6), (2 * M - 10, M + 3)]

    tests = []
    # A. Layer 1 at fresh scales
    for M in [404, 520]:
        tests.append((f"L1.b5b3.M{M}", M,
                      A23(M) + [(M + 3, M + 5)], "UNSAT"))
    tests.append(("L1.t3t5.M404", 404,
                  A23(404) + [(2 * 404 - 5, 2 * 404 - 3)], "UNSAT"))
    # B. C3 core at fresh mod-8 scales
    for M in [408, 520] + ([808] if big else []):
        tests.append((f"C3.M{M}", M, C3(M), "UNSAT"))
    # C. sharpness
    tests.append(("C3sat.M412", 412, C3(412), "SAT"))
    tests.append(("C3sat.M413", 413, C3(413), "SAT"))
    # D. L0 at fresh even scale
    tests.append(("L0a.M302", 302,
                  A23(302) + [(302 + 3, 2 * 302 - 3)], "UNSAT"))
    tests.append(("L0b.M302", 302,
                  A23(302) + [(302 + 6, 2 * 302 - 10)], "UNSAT"))
    # E. Lemma E lock
    tests.append(("E.lock.M46", 46,
                  [(46 + 5, 46 + 3), (2 * 46 - 3, 2 * 46 - 5)], "UNSAT"))
    tests.append(("E.lock.M52", 52,
                  [(52 + 5, 52 + 3), (2 * 52 - 5, 2 * 52 - 3)], "UNSAT"))

    for name, M, units, expect in tests:
        t0 = time.time()
        try:
            verdict, info = solve(M, units)
            ok = verdict == expect
            rec = [name, M, verdict, expect, ok, round(time.time() - t0, 1)]
            (out["checks"] if ok else out["fail"]).append(rec)
            print(rec, flush=True)
        except AssertionError as ex:
            out["fail"].append([name, M, "ASSERT", repr(ex.args[:2])])
            print("FAIL", name, ex, flush=True)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}; failures: {out['fail']}")
    sys.exit(1 if out["fail"] else 0)


if __name__ == "__main__":
    main()
