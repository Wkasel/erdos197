"""Erdős #197 — e178: MASTER-ASSEMBLY spot audit of notes/71-75.

One independently reconstructed load-bearing check per front document,
each at a FRESH scale, all encoders written from scratch in this file
(no imports from prior experiment code).  Pre-registered expectations:

  part71a  Lemma K brute force (notes/71 §2a-3, notes/62 §4d):
           interval [1..n], prefix [1..k] wholesale first, monotone-
           3AP-free order exists iff n <= k+4 (k = 2,3,4 grid).
  part71b  Budgeted K cross-check (notes/71 §2c/6), fresh encoder:
           K(9,3) = 3, K(12,4) = 4; plus FRESH diagonal point K(27,9)
           (k = 9 never measured; expect strictly between K(24,8)=40
           and K(30,10)=69).
  part71c  cmin at FRESH scale M = 20 (measured M at 8/12/16):
           min over balanced mu_dn=0 low-impure splits of low u B1 of
           sum_z min(c_A, c_B) — expect 20 = M (GAP-CMIN's basis).
  part72   L-MID at FRESH scale M = 48 (machine-checked 16..40):
           no U (|U|=M/2 in (M,2M]), W (|W|=M/4 in (M/2,M]) with
           (2U-W) missing (2M,3M] — expect UNSAT; |U|=M/4 control SAT;
           independent brute force at M = 16.
  part73   Lane law at FRESH scale: K4e(23) core {t12<b6, t15<b4,
           t18<b3} + in-block AP-freeness UNSAT at M = 160 (beyond the
           probed 152), SAT control at M = 164 (== 4 mod 8).
  part74   ROT4 (notes/74 Part II): window law max_a(6|T cap (a,2a]|
           - 5a) = 0 for both teams to FRESH horizon 2^17; doubling
           chains die at depth <= 2 for all f <= 64 from FRESH seed
           octave (2^12, 2^13], horizon 2^23.
  part75   P-CAT family laws at FRESH scale M = 200 (4 empty patterns;
           |H_up| = 5M^2/4, |H_dn| = 5M^2/16, |SKIP| = 13M^2/16);
           balanced two-seam coupled core at FRESH anchor m = 28
           (between tested 24 and 32) — expect UNSAT (feeds J-DOWN:
           v_min(0)(56) = infinity).

Usage: e178_audit_spot.py {71a|71b|71c|72|73|74|75cat|75core|all}
Record: data/e178_audit_spot.jsonl (streaming).
"""
import itertools
import json
import sys
import time

DATA = "data/e178_audit_spot.jsonl"


def rec(part, **kw):
    kw["part"] = part
    kw["t"] = round(time.time() - T0, 1)
    with open(DATA, "a") as f:
        f.write(json.dumps(kw) + "\n")
    print(json.dumps(kw), flush=True)


T0 = time.time()


# ---------------------------------------------------------------- 71a
def ap_free_order(seq):
    """seq = tuple of values in temporal order; True if no monotone 3AP."""
    n = len(seq)
    pos = {v: i for i, v in enumerate(seq)}
    for a in seq:
        for b in seq:
            if b <= a:
                continue
            c = 2 * b - a
            if c in pos:
                pa, pb, pc = pos[a], pos[b], pos[c]
                if pa < pb < pc or pc < pb < pa:
                    return False
    return True


def lemma_k_sat(n, k):
    """Exists order of [1..n] with [1..k] wholesale first, AP-free?"""
    lows = list(range(1, k + 1))
    highs = list(range(k + 1, n + 1))
    for lo in itertools.permutations(lows):
        for hi in itertools.permutations(highs):
            if ap_free_order(lo + hi):
                return True
    return False


def part71a():
    ok = True
    for k in (2, 3, 4):
        for n in range(k + 3, k + 8):
            sat = lemma_k_sat(n, k)
            expect = n <= k + 4
            good = sat == expect
            ok &= good
            rec("71a", n=n, k=k, sat=sat, expect_sat=expect, ok=good)
    rec("71a", verdict="PASS" if ok else "FAIL")


# ---------------------------------------------------------------- 71b
def order_var_pool(n):
    """o[(u,v)] for 0<=u<v<n: True = u temporally before v."""
    idx = {}
    c = 0
    for u in range(n):
        for v in range(u + 1, n):
            c += 1
            idx[(u, v)] = c
    return idx, c


def order_clauses(n, idx):
    cls = []
    for u in range(n):
        for v in range(u + 1, n):
            for w in range(v + 1, n):
                ouv, ovw, ouw = idx[(u, v)], idx[(v, w)], idx[(u, w)]
                cls.append([-ouv, -ovw, ouw])
                cls.append([ouv, ovw, -ouw])
    return cls


def ap_clauses_block(vals, idx, vpos):
    """Middle-extremity (MP) for every AP triple within vals."""
    cls = []
    vs = set(vals)
    for a in vals:
        for b in vals:
            if b <= a:
                continue
            c = 2 * b - a
            if c in vs:
                ia, ib, ic = vpos[a], vpos[b], vpos[c]
                oab = idx[(min(ia, ib), max(ia, ib))] * (1 if ia < ib else -1)
                obc = idx[(min(ib, ic), max(ib, ic))] * (1 if ib < ic else -1)
                # forbid a<b<c monotone up (oab & obc) and down (~oab & ~obc)
                cls.append([-oab, -obc])
                cls.append([oab, obc])
    return cls


def budgeted_K_query(n, k, v):
    """SAT iff [1..n], low [1..k], <=v inverted (low,high) pairs, AP-free."""
    from pysat.solvers import Cadical195
    from pysat.card import CardEnc
    from pysat.formula import IDPool

    vals = list(range(1, n + 1))
    vpos = {val: val - 1 for val in vals}
    idx, top = order_var_pool(n)
    cls = order_clauses(n, idx) + ap_clauses_block(vals, idx, vpos)
    pool = IDPool(start_from=top + 1)
    inv = []
    for l in range(1, k + 1):
        for h in range(k + 1, n + 1):
            iv = pool.id(("inv", l, h))
            o = idx[(vpos[l], vpos[h])]  # l before h
            cls.append([o, iv])      # ~o -> iv
            cls.append([-iv, -o])    # iv -> ~o
            inv.append(iv)
    card = CardEnc.atmost(inv, bound=v, vpool=pool)
    with Cadical195(bootstrap_with=cls + card.clauses) as s:
        return s.solve()


def part71b():
    ok = True
    for (n, k, kval) in ((9, 3, 3), (12, 4, 4)):
        below = budgeted_K_query(n, k, kval - 1)
        at = budgeted_K_query(n, k, kval)
        good = (not below) and at
        ok &= good
        rec("71b", n=n, k=k, claimed_K=kval, unsat_below=not below,
            sat_at=at, ok=good)
    # fresh diagonal point K(27,9): bisect in (40, 69)
    lo, hi = 40, 69  # K(24,8)=40 SAT-side known shape; bracket wide
    # establish bracket ends first
    if budgeted_K_query(27, 9, lo):
        rec("71b", fresh="K(27,9)", note="SAT already at 40 — below bracket",
            ok=False)
        ok = False
    else:
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if budgeted_K_query(27, 9, mid):
                hi = mid
            else:
                lo = mid
            rec("71b", fresh_probe=mid, sat=hi == mid)
        rec("71b", fresh="K(27,9)", value=hi,
            monotone_between=(40 < hi <= 69))
    rec("71b", verdict="PASS" if ok else "FAIL")


# ---------------------------------------------------------------- 71c
def part71c(M=20):
    from ortools.sat.python import cp_model
    low = list(range(M // 2 + 1, 2 * M + 1))       # Bm1 u B0
    bm1 = [v for v in low if v <= M]
    b0 = [v for v in low if v > M]
    b1 = list(range(2 * M + 1, 4 * M + 1))
    m = cp_model.CpModel()
    A = {v: m.NewBoolVar(f"a{v}") for v in low + b1}
    m.Add(sum(A[v] for v in bm1) == M // 4)
    m.Add(sum(A[v] for v in b0) == M // 2)
    m.Add(sum(A[v] for v in b1) == M)
    # mu_dn = 0 both teams: AP (w, u, y) in Bm1 x B0 x B1 not monochromatic
    for w in bm1:
        for u in b0:
            y = 2 * u - w
            if 2 * M < y <= 4 * M:
                m.AddBoolOr([A[w].Not(), A[u].Not(), A[y].Not()])
                m.AddBoolOr([A[w], A[u], A[y]])
    # low-impure: A-low has both parities (forces B-low impure too, bal)
    m.Add(sum(A[v] for v in low if v % 2 == 1) >= 1)
    m.Add(sum(A[v] for v in low if v % 2 == 0) >= 1)
    m.Add(sum(A[v] for v in low if v % 2 == 1) <= 3 * M // 4 - 1)
    m.Add(sum(A[v] for v in low if v % 2 == 0) <= 3 * M // 4 - 1)
    # pair indicators and per-z min
    from collections import defaultdict
    pairs = defaultdict(list)  # z -> [(u,y)]
    for u in low:
        for y in b1:
            z = 2 * y - u
            if 4 * M < z <= 8 * M:
                pairs[z].append((u, y))
    total = []
    for z, ps in sorted(pairs.items()):
        ca, cb = [], []
        for (u, y) in ps:
            pa = m.NewBoolVar(f"pa{u}_{y}")
            m.AddBoolAnd([A[u], A[y]]).OnlyEnforceIf(pa)
            m.AddBoolOr([A[u].Not(), A[y].Not()]).OnlyEnforceIf(pa.Not())
            pb = m.NewBoolVar(f"pb{u}_{y}")
            m.AddBoolAnd([A[u].Not(), A[y].Not()]).OnlyEnforceIf(pb)
            m.AddBoolOr([A[u], A[y]]).OnlyEnforceIf(pb.Not())
            ca.append(pa)
            cb.append(pb)
        mz = m.NewIntVar(0, len(ps), f"m{z}")
        sel = m.NewBoolVar(f"s{z}")
        m.Add(mz >= sum(ca)).OnlyEnforceIf(sel)
        m.Add(mz >= sum(cb)).OnlyEnforceIf(sel.Not())
        total.append(mz)
    m.Minimize(sum(total))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 1200
    solver.parameters.num_search_workers = 4
    st = solver.Solve(m)
    val = int(solver.ObjectiveValue()) if st in (cp_model.OPTIMAL,
                                                 cp_model.FEASIBLE) else None
    rec("71c", M=M, status=solver.StatusName(st), cmin=val,
        expect=M, ok=(st == cp_model.OPTIMAL and val == M))


# ---------------------------------------------------------------- 72
def lmid_sat(M, usize):
    from pysat.solvers import Cadical195
    from pysat.card import CardEnc
    from pysat.formula import IDPool

    uvals = list(range(M + 1, 2 * M + 1))
    wvals = list(range(M // 2 + 1, M + 1))
    pool = IDPool()
    U = {u: pool.id(("u", u)) for u in uvals}
    W = {w: pool.id(("w", w)) for w in wvals}
    cls = []
    for u in uvals:
        for w in wvals:
            if 2 * M < 2 * u - w <= 3 * M:
                cls.append([-U[u], -W[w]])
    c1 = CardEnc.equals([U[u] for u in uvals], bound=usize, vpool=pool)
    c2 = CardEnc.equals([W[w] for w in wvals], bound=M // 4, vpool=pool)
    with Cadical195(bootstrap_with=cls + c1.clauses + c2.clauses) as s:
        return s.solve()


def part72():
    M = 48
    main = lmid_sat(M, M // 2)       # expect False (lemma holds)
    ctrl = lmid_sat(M, M // 4)       # expect True (U fits in safe zone)
    rec("72", M=M, lemma_unsat=not main, control_sat=ctrl,
        ok=(not main) and ctrl)
    # brute force at 16 (independent instrument)
    M = 16
    uvals = list(range(M + 1, 2 * M + 1))
    wvals = list(range(M // 2 + 1, M + 1))
    hits = {}  # per (u,w) whether it mints midband
    for u in uvals:
        for w in wvals:
            hits[(u, w)] = 2 * M < 2 * u - w <= 3 * M
    clean = 0
    for Uc in itertools.combinations(uvals, M // 2):
        for Wc in itertools.combinations(wvals, M // 4):
            if not any(hits[(u, w)] for u in Uc for w in Wc):
                clean += 1
                break
        if clean:
            break
    rec("72", M=16, brute_clean_pairs=clean, ok=clean == 0)


# ---------------------------------------------------------------- 73
def lane_core_sat(M, units):
    """units = [(i, j)] meaning t_i = 2M - i placed before b_j = M + j."""
    from pysat.solvers import Cadical195

    vals = list(range(M + 1, 2 * M + 1))
    vpos = {v: i for i, v in enumerate(vals)}
    idx, _ = order_var_pool(M)
    cls = order_clauses(M, idx) + ap_clauses_block(vals, idx, vpos)
    for (i, j) in units:
        t, b = 2 * M - i, M + j
        it, ib = vpos[t], vpos[b]
        lit = idx[(min(it, ib), max(it, ib))] * (1 if it < ib else -1)
        cls.append([lit])  # t before b
    with Cadical195(bootstrap_with=cls) as s:
        return s.solve()


def part73():
    x = 23
    units = [(x - 11, 6), (x - 8, 4), (x - 5, 3)]  # K4e(x)
    r_in = lane_core_sat(160, units)    # 160 == x+1 == 0 mod 8: expect UNSAT
    r_ctl = lane_core_sat(164, units)   # 164 == 4 mod 8: expect SAT
    rec("73", x=x, lane="K4e", M_in=160, in_class_unsat=not r_in,
        M_ctl=164, control_sat=r_ctl, ok=(not r_in) and r_ctl)


# ---------------------------------------------------------------- 74
def rot4_team(v):
    m = (v - 1).bit_length() - 1  # v in O_m = (2^m, 2^{m+1}]
    p = v - (1 << m) - 1
    q = (4 * p) >> m
    r = (q - m) % 4
    return r < 2  # True = team A


def part74():
    H = 1 << 18
    mem = [False] * (H + 1)
    for v in range(5, H + 1):
        mem[v] = rot4_team(v)
    pref = [0] * (H + 1)
    for v in range(1, H + 1):
        pref[v] = pref[v - 1] + (1 if mem[v] else 0)
    mx_a = mx_b = -10**9
    for a in range(32, (1 << 17) + 1):
        ca = pref[2 * a] - pref[a]
        cb = a - ca  # window size a, complement
        mx_a = max(mx_a, 6 * ca - 5 * a)
        mx_b = max(mx_b, 6 * cb - 5 * a)
    rec("74", horizon=1 << 17, max_excess_A=mx_a, max_excess_B=mx_b,
        ok=(mx_a == 0 and mx_b == 0))
    # chains, fresh seed octave (2^12, 2^13], horizon 2^23
    HZ = 1 << 23
    maxd = 0
    for f in range(1, 65):
        for u in range((1 << 12) + 1, (1 << 13) + 1):
            t = rot4_team(u)
            d = 0
            w = 2 * u - f
            while w <= HZ and w >= 5 and rot4_team(w) == t:
                d += 1
                w = 2 * w - f
            maxd = max(maxd, d)
    rec("74", chains_f_max=64, seed_octave=12, max_depth=maxd,
        ok=maxd <= 2)


# ---------------------------------------------------------------- 75
def part75cat():
    M = 200
    lo, hi = M // 2, 8 * M

    def blk(v):
        if v <= M:
            return -1
        if v <= 2 * M:
            return 0
        if v <= 4 * M:
            return 1
        return 2

    from collections import Counter
    cnt = Counter()
    for a in range(lo + 1, hi + 1):
        for b in range(a + 1, hi + 1):
            c = 2 * b - a
            if c > hi:
                break
            cnt[(blk(a), blk(b), blk(c))] += 1
    empty = [p for p in itertools.combinations_with_replacement((-1, 0, 1, 2), 3)
             if cnt[p] == 0]
    laws = {
        "H_up": (cnt[(0, 1, 2)], 5 * M * M // 4),
        "H_dn": (cnt[(-1, 0, 1)], 5 * M * M // 16),
        "SKIP": (cnt[(-1, 1, 2)], 13 * M * M // 16),
    }
    ok = (sorted(empty) == sorted([(-1, -1, 1), (-1, -1, 2), (-1, 0, 2),
                                   (0, 0, 2)])
          and all(a == b for a, b in laws.values()))
    rec("75cat", M=M, empty=sorted(empty),
        laws={k: v for k, v in laws.items()}, ok=ok)


def part75core(m=28):
    from pysat.solvers import Cadical195
    from pysat.card import CardEnc
    from pysat.formula import IDPool

    vals = list(range(m + 1, 8 * m + 1))
    n = len(vals)
    vpos = {v: i for i, v in enumerate(vals)}
    idx, top = order_var_pool(n)
    pool = IDPool(start_from=top + 1)
    team = {v: pool.id(("t", v)) for v in vals}
    cls = order_clauses(n, idx)
    # AP middle-extremity conditioned on same team
    vs = set(vals)
    nap = 0
    for a in vals:
        for b in vals:
            if b <= a:
                continue
            c = 2 * b - a
            if c in vs:
                ia, ib, ic = vpos[a], vpos[b], vpos[c]
                oab = idx[(min(ia, ib), max(ia, ib))] * (1 if ia < ib else -1)
                obc = idx[(min(ib, ic), max(ib, ic))] * (1 if ib < ic else -1)
                ta, tb, tc = team[a], team[b], team[c]
                # all-A
                cls.append([-ta, -tb, -tc, -oab, -obc])
                cls.append([-ta, -tb, -tc, oab, obc])
                # all-B
                cls.append([ta, tb, tc, -oab, -obc])
                cls.append([ta, tb, tc, oab, obc])
                nap += 1
    # block order (two seams + outer), same team only
    B0 = [v for v in vals if v <= 2 * m]
    B1 = [v for v in vals if 2 * m < v <= 4 * m]
    B2 = [v for v in vals if v > 4 * m]
    for (lob, hib) in ((B0, B1), (B1, B2), (B0, B2)):
        for u in lob:
            for v in hib:
                o = idx[(vpos[u], vpos[v])]
                cls.append([-team[u], -team[v], o])
                cls.append([team[u], team[v], o])
    # exact balance per block
    for b, k in ((B0, m // 2), (B1, m), (B2, 2 * m)):
        cc = CardEnc.equals([team[v] for v in b], bound=k, vpool=pool)
        cls.extend(cc.clauses)
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        satq = s.solve()
    rec("75core", m=m, n=n, n_ap=nap, n_clauses=len(cls),
        sat=satq, solve_s=round(time.time() - t0, 1), ok=not satq)


PARTS = {"71a": part71a, "71b": part71b, "71c": part71c, "72": part72,
         "73": part73, "74": part74, "75cat": part75cat,
         "75core": part75core}

if __name__ == "__main__":
    args = sys.argv[1:] or ["all"]
    todo = list(PARTS) if args == ["all"] else args
    for p in todo:
        print(f"== part {p} ==", flush=True)
        PARTS[p]()
    print("done", flush=True)
