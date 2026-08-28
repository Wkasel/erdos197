"""e152_bridge1_check: machine checks for notes/52 (BRIDGE1), as
mandated by the task brief: each branch of the dichotomy exercised on
3 constructed colorings at 2 scales.

Colorings:
  chi1 (branch (a), the direct kill): Case-1 team T with C0 = 3 dust
       per clean block; dust placed ADVERSARIALLY on the C3(9)
       minimal-core values of the window blocks.  Checks: Step-1 pair
       extraction (assert), then R(27, 28; M, D) UNSAT at M = 128 and
       M = 256 (solver), plus two encoding controls at M = 128
       (AP-only SAT; single-attacker SAT).
  chi2 (branch (b), the splitter): T' = {3p : p = 1 mod 4}; exact
       per-block counts confirm SPLIT-QUANT >= (2^m - 13)/12 and the
       vacuity corollary (no C0-clean block for either team) at
       m = 7, 8.  Arithmetic only.
  chi3 (the fixed-pair splitter of SS4.3): catalogue pairs x=11..21
       and all crown pairs split (T' = lo halves); T is Case-1 with
       dust -> 1/block; landing-pad facts LP(alpha,beta,gamma)
       verified by enumeration; the diagonal pair {27,28} survives in
       T and kills through the crown-dusted windows: R(27,28; M,
       {2M-1}) UNSAT at M = 128, 256 (solver).

Solver discipline: ONE query at a time, sequential; complete encoding
(all transitivity triples) -- UNSAT needs no soundness argument.

Run: .venv/bin/python experiments/e152_bridge1_check.py
Artifacts: data/e152_bridge1.json, data/e152_bridge1.log
"""
import json
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197"
LOG = []


def log(s):
    print(s, flush=True)
    LOG.append(s)


def solve_R(M, D, attackers, ap_free=True, units=True):
    """Complete encoding of R(attackers; M, D) on S = (M, 2M] \\ D.
    Returns (verdict_str, n, n_clauses, seconds)."""
    S = [v for v in range(M + 1, 2 * M + 1) if v not in D]
    idx = {v: i for i, v in enumerate(S)}
    n = len(S)
    var = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            var[(i, j)] = c            # True <=> S[i] placed before S[j]
    cl = []
    if ap_free:
        # in-block APs (u, y, z) within S: y leads both or trails both
        for yi in range(n):
            y = S[yi]
            d = 1
            while y - d > M and y + d <= 2 * M:
                u, z = y - d, y + d
                if u in idx and z in idx:
                    a = var[(idx[u], yi)] if idx[u] < yi else None
                    assert idx[u] < yi < idx[z]
                    ouy = var[(idx[u], yi)]
                    oyz = var[(yi, idx[z])]
                    cl.append([-ouy, -oyz])
                    cl.append([ouy, oyz])
                d += 1
    if units:
        for a in attackers:
            for y in S:
                if y <= a:
                    continue
                z = 2 * y - a
                if z in idx and (y - a) % 1 == 0:
                    # unit: z before y, i.e. NOT (y before z)
                    cl.append([-var[(idx[y], idx[z])]])
    # complete transitivity
    for i in range(n):
        for j in range(i + 1, n):
            vij = var[(i, j)]
            for k in range(j + 1, n):
                vjk = var[(j, k)]
                vik = var[(i, k)]
                cl.append([-vij, -vjk, vik])
                cl.append([vij, vjk, -vik])
    t0 = time.time()
    with Cadical195(bootstrap_with=cl) as s:
        sat = s.solve()
    dt = time.time() - t0
    return ("SAT" if sat else "UNSAT"), n, len(cl), dt


def diag_pairs_in_block(m, team):
    """Diagonal usable pairs {3p,3p+1}, p=1 mod 4, fully inside
    B(m) and fully owned by `team` (a membership predicate)."""
    lo, hi = 2 ** m, 2 ** (m + 1)
    out = []
    p = 5
    while 3 * p + 1 <= hi:
        if 3 * p > lo and p % 4 == 1 and team(3 * p) and team(3 * p + 1):
            out.append(p)
        p += 2
    return out


def main():
    res = {}
    t00 = time.time()

    # ---------------- chi1 ----------------
    log("== chi1: Case-1 team, C0 = 3, adversarial core-targeted dust ==")
    dust = {4: {17, 18, 31},
            7: {247, 137, 138},     # C3(9) core values at M = 128
            8: {503, 265, 266}}     # C3(9) core values at M = 256
    chi1_T = set()
    for m in (4, 5, 7, 8):
        chi1_T |= set(range(2 ** m + 1, 2 ** (m + 1) + 1)) - dust.get(m, set())

    # Step-1 extraction in the lowest clean block B(4)
    got = diag_pairs_in_block(4, lambda v: v in chi1_T)
    log(f"chi1 extraction in B(4): fully-T diagonal pairs p = {got}")
    assert got == [9], got
    nm = (2 ** 4 - 13) / 12
    log(f"chi1 DIAG-DENSE bound at m=4: N >= {nm:.2f}; found {len(got)}  OK")
    res["chi1_extraction"] = got

    # encoding controls at M = 128 (before the kills)
    v, n, nc, dt = solve_R(128, dust[7], [], units=False)
    log(f"chi1 control AP-only  M=128 (n={n}, {nc} cl): {v}  [{dt:.1f}s]")
    assert v == "SAT"
    res["ctl_ap_only_128"] = v
    v, n, nc, dt = solve_R(128, dust[7], [27])
    log(f"chi1 control single-27 M=128 (n={n}, {nc} cl): {v}  [{dt:.1f}s]")
    assert v == "SAT"
    res["ctl_single_128"] = v

    # the kills
    for M, m in ((128, 7), (256, 8)):
        v, n, nc, dt = solve_R(M, dust[m], [27, 28])
        log(f"chi1 R(27,28; {M}, core-dust {sorted(dust[m])}) "
            f"(n={n}, {nc} cl): {v}  [{dt:.1f}s]")
        assert v == "UNSAT"
        res[f"chi1_R_{M}"] = v

    # ---------------- chi2 ----------------
    log("== chi2: the splitter adversary (T' = {3p : p = 1 mod 4}) ==")
    tp = lambda v: v % 3 == 0 and (v // 3) % 4 == 1 and v // 3 >= 5
    for m in (7, 8):
        lo, hi = 2 ** m, 2 ** (m + 1)
        cnt = sum(1 for v in range(lo + 1, hi + 1) if tp(v))
        bound = (2 ** m - 13) / 12
        dust_T = cnt                 # T's dust = T' values
        dust_Tp = (hi - lo) - cnt    # T''s dust = T values
        log(f"chi2 m={m}: |B ^ T'| = {cnt} >= {bound:.2f} (SPLIT-QUANT); "
            f"dust_T = {dust_T} > 8, dust_T' = {dust_Tp} > 8")
        assert cnt >= bound and dust_T > 8 and dust_Tp > 8
        # every diagonal usable pair inside B(m) meets T'
        allp = diag_pairs_in_block(m, lambda v: True)
        meets = [p for p in allp if tp(3 * p) or tp(3 * p + 1)]
        assert meets == allp
        log(f"chi2 m={m}: all {len(allp)} diagonal pairs in B(m) meet T'  OK")
        res[f"chi2_m{m}"] = {"count": cnt, "bound": bound,
                             "pairs": len(allp)}

    # ---------------- chi3 ----------------
    log("== chi3: fixed-pair + crown splitter (SS4.3 fixed point) ==")
    cat_lo = {11, 13, 15, 17, 19, 21}
    crown_lo = {2 ** j - 1 for j in range(3, 10)}
    chi3_Tp = cat_lo | crown_lo
    chi3_T = lambda v: v not in chi3_Tp
    # SPLIT-QUANT inheritance on the sparse family
    for x in sorted(cat_lo):
        assert (x in chi3_Tp) != (x + 1 in chi3_Tp)
    for j in range(3, 10):
        assert (2 ** j - 1 in chi3_Tp) != (2 ** j in chi3_Tp)
    log("chi3: every catalogue pair and crown pair split 1-1  OK")
    # T is Case-1: dust per block
    dusts = {m: [v for v in range(2 ** m + 1, 2 ** (m + 1) + 1)
                 if not chi3_T(v)] for m in range(3, 9)}
    log(f"chi3 dust per block m=3..8: "
        f"{[len(dusts[m]) for m in range(3, 9)]}")
    assert all(len(dusts[m]) == 1 for m in range(5, 9))
    # landing-pad facts
    for j, x in ((5, 2), (7, 2), (9, 2)):
        a, b, c = x, 2 ** j - 1, 2 ** (j + 1) - 2 - x
        assert a + c == 2 * b and 2 ** j < c <= 2 ** (j + 1)
        assert chi3_T(c)     # the adversary donates every completion
    for j in range(3, 9):
        assert 1 + (2 ** (j + 1) - 1) == 2 * 2 ** j     # LP(beta)
    # LP(gamma): brute AP classification over C u {1} up to 512
    Cset = sorted({2 ** j - 1 for j in range(3, 10)}
                  | {2 ** j for j in range(3, 10)} | {1})
    aps = [(u, y, z) for u in Cset for y in Cset for z in Cset
           if u < y < z and u + z == 2 * y]
    beta = [(1, 2 ** j, 2 ** (j + 1) - 1) for j in range(3, 9)]
    assert sorted(aps) == sorted(beta), aps
    log(f"chi3 LP(gamma): APs within crown-set u {{1}} = beta family "
        f"only ({len(aps)} APs)  OK")
    # the diagonal pair survives and kills through the crown dust
    got = diag_pairs_in_block(4, chi3_T)
    log(f"chi3 extraction in B(4): fully-T diagonal pairs p = {got}")
    assert 9 in got
    for M in (128, 256):
        D = {2 * M - 1}              # chi3's actual dust: the lo crown
        v, n, nc, dt = solve_R(M, D, [27, 28])
        log(f"chi3 R(27,28; {M}, {sorted(D)}) (n={n}, {nc} cl): {v}"
            f"  [{dt:.1f}s]")
        assert v == "UNSAT"
        res[f"chi3_R_{M}"] = v

    log(f"ALL CHECKS PASS  [{time.time() - t00:.0f}s total]")
    with open(f"{BASE}/data/e152_bridge1.json", "w") as f:
        json.dump(res, f, indent=1)
    with open(f"{BASE}/data/e152_bridge1.log", "w") as f:
        f.write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
