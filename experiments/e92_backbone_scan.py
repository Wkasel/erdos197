"""e92: backbone stability of the order gadget OG(M) across M.

For each M, build OG(M) on the interval (M, 2M]:
  - all AP-triple non-monotonicity clauses (for AP (a,b,c):
    forbid pos(a)<pos(b)<pos(c) and pos(c)<pos(b)<pos(a));
  - transitivity handled lazily (as in e87) -- learned cuts are valid for
    every total order, so they are appended permanently to one incremental
    solver per M while attacks/tests ride on assumptions.

Attacks (unit order literals "z before y") are added ONE AT A TIME in the
fixed order: 15-attacks j=1..7 (indices 1-7), then 16-attacks j=1..8
(indices 8-15).  Attack (x,j): y = b_j = M+j, z = t_{x-2j} = 2M+2j-x.

Reported per M:
  (a) first k such that attacks 1..k are jointly infeasible, and attack k;
  (b) under the maximal consistent prefix (attacks 1..k-1), which orders
      among {b_j} x {their own guards} are FORCED (each direction tested
      by assumption; UNSAT of one direction => other is forced).

Key question: is  b_7 < t_2  (M+7 before 2M-2) always forced by the prefix,
with attack 14 = (t_2 before b_7) always the first conflict?
"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

MS = [44, 48, 50, 56, 60, 64, 72, 80]
OUT = "/Users/will/Dev/personal/tasks/math/erdos197/data/backbone_scan.txt"
CAP = 30000  # max lazy transitivity cuts per refinement round


def scan(M, log):
    lo, hi = M, 2 * M
    V = list(range(lo + 1, hi + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    var = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            var[(i, j)] = c

    def o(u, w):
        i, j = idx[u], idx[w]
        return var[(i, j)] if i < j else -var[(j, i)]

    def ilit(p, q):  # index-based literal
        return var[(p, q)] if p < q else -var[(q, p)]

    cl = []
    ntr = 0
    for y in V:
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            d += 1
            if x > lo:
                cl.append([-o(x, y), -o(y, z)])
                cl.append([-o(z, y), -o(y, x)])
                ntr += 1

    # attacks in fixed order: 15-family j=1..7 then 16-family j=1..8
    attacks = []  # (label, lit, z, y)
    for x in (15, 16):
        for j in range(1, x // 2 + 1):
            y = lo + j
            z = hi + 2 * j - x
            if lo < z <= hi:
                attacks.append((f"{x}-attack j={j}: {z}<{y}", o(z, y), z, y))

    sol = Cadical195(bootstrap_with=cl)
    stats = {"rounds": 0, "cuts": 0}

    def solve_lazy(assumps):
        """SAT/UNSAT under assumptions with lazy transitivity refinement.
        Learned cuts are order-axioms, valid for every query -> kept."""
        while True:
            if not sol.solve(assumptions=assumps):
                return False
            model = set(l for l in sol.get_model() if l > 0)
            B = np.zeros((n, n), dtype=bool)
            for (i, j), lit in var.items():
                if lit in model:
                    B[i, j] = True
                else:
                    B[j, i] = True
            R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
            miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
            ii, jj = np.nonzero(miss)
            if len(ii) == 0:
                return True
            new = []
            for i, j in zip(ii[:CAP], jj[:CAP]):
                ks = np.nonzero(B[i] & B[:, j])[0]
                new.append([-ilit(i, int(ks[0])), -ilit(int(ks[0]), j),
                            ilit(i, j)])
            sol.append_formula(new)
            stats["rounds"] += 1
            stats["cuts"] += len(new)

    t0 = time.time()
    log(f"M={M}: n={n} triples={ntr} attacks={len(attacks)}")

    # (a) incremental attack prefix
    conflict_k, conflict_label = -1, "none (all attacks SAT)"
    for k in range(1, len(attacks) + 1):
        assumps = [a[1] for a in attacks[:k]]
        if not solve_lazy(assumps):
            conflict_k, conflict_label = k, attacks[k - 1][0]
            break
    log(f"M={M}: first conflict at attack #{conflict_k} = {conflict_label}"
        f"  ({time.time()-t0:.0f}s, {stats['rounds']} lazy rounds)")

    # (b) forced bottom-vs-guard orders under maximal consistent prefix
    prefix = [a[1] for a in attacks[:max(conflict_k - 1, 0)]]
    forced = []
    for j in range(1, 9):
        b = lo + j
        guards = []
        if j <= 7:
            guards.append(("t%d" % (15 - 2 * j), hi + 2 * j - 15))
        guards.append(("t%d" % (16 - 2 * j), hi + 2 * j - 16))
        for gname, g in guards:
            if not (lo < g <= hi) or g == b:
                continue
            b_first_ok = solve_lazy(prefix + [o(b, g)])
            g_first_ok = solve_lazy(prefix + [o(g, b)])
            if b_first_ok and not g_first_ok:
                forced.append(f"{b}<{g} (b_{j} before {gname}={g})")
            elif g_first_ok and not b_first_ok:
                forced.append(f"{g}<{b} ({gname}={g} before b_{j})")
            elif not b_first_ok and not g_first_ok:
                forced.append(f"CONTRADICTION b_{j}/{gname}")
    b7_lt_t2 = f"{lo+7}<{hi-2} (b_7 before t2={hi-2})" in forced
    log(f"M={M}: forced bottom-vs-guard orders under prefix 1..{conflict_k-1} "
        f"({len(forced)}):")
    for f in forced:
        log(f"    {f}")
    log(f"M={M}: b_7<t_2 forced: {b7_lt_t2}   "
        f"total {time.time()-t0:.0f}s, {stats['cuts']} cuts")
    log("")
    sol.delete()
    return dict(M=M, conflict_k=conflict_k, conflict_label=conflict_label,
                forced=forced, b7_lt_t2=b7_lt_t2)


if __name__ == "__main__":
    fh = open(OUT, "w")

    def log(s):
        print(s, flush=True)
        fh.write(s + "\n")
        fh.flush()

    results = []
    for M in MS:
        results.append(scan(M, log))
    log("=== SUMMARY: M -> (conflict index, conflict attack, b_7<t_2 forced)")
    for r in results:
        log(f"M={r['M']:3d}  #{r['conflict_k']:2d}  {r['conflict_label']:28s}"
            f"  b7<t2_forced={r['b7_lt_t2']}  n_forced={len(r['forced'])}")
    fh.close()
