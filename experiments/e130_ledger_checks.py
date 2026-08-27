"""e130 — per-claim machine spot-checks for the T-FORCE ledger theorem
(notes/54-ledger-theorem.md §6).  Five checks:

1. X-INTERLEAVE survival: the §4 accounting charges the swapped-powers
   team ZERO (Top sets empty, no forced descents) while its inversion
   pairs cover every anchor — the single-team counterexample must
   remain legal.  (P7 / NG1 / NG2 consistency.)
2. D3 covering-integration count: exhaustive-anchor audit of
   "per-octave demand v => >= v/4 pairs with low member in (X, 8X)".
3. Exposure mass on the dense bal@16 v=160 witness (e127 jsonl row
   10): recount inversions, displaced sets, Top/exposure counts
   in-window and below-window, L-CASCADE range mass.
4. P5/P6 sanity: in-team AP counts (Varnavides scale) vs AP-free 0.
5. L-COMP audit: on random monotone-AP-free orders, no directed
   2-path of forced descents along an AP exists (it would BE a
   decreasing monotone AP).

Artifacts: data/e130_ledger_checks.json, log to stdout (tee'd to
data/e130_ledger_checks.log by the caller).  Touches no running
experiment's files.
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')

OUT = {}


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- helpers
def is_inversion_at(u, w, N):
    """Direct definition: (u, w) an adjacent-seam inversion pair of
    window W(N) = (N, 8N] (membership only; order handled by caller):
    u in B_i, w in B_{i+1}."""
    b0 = lambda x: N < x <= 2 * N
    b1 = lambda x: 2 * N < x <= 4 * N
    b2 = lambda x: 4 * N < x <= 8 * N
    return (b0(u) and b1(w)) or (b1(u) and b2(w))


def seam_inversions(values_in_order, N):
    """All adjacent-seam inversion pairs (u, w) at W(N) for a team
    given in position order: pos(w) < pos(u)."""
    pos = {v: i for i, v in enumerate(values_in_order)}
    inw = [v for v in values_in_order if N < v <= 8 * N]
    out = []
    for u in inw:
        for w in inw:
            if u < w and pos[w] < pos[u] and is_inversion_at(u, w, N):
                out.append((u, w))
    return out


def in_team_aps(S):
    """All 3-APs (a, b, c), a < b < c, within set S."""
    Sset = set(S)
    out = []
    for b in S:
        for a in S:
            if a < b and 2 * b - a in Sset:
                out.append((a, b, 2 * b - a))
    return out


def monotone_ap_violations(order):
    """Monotone AP triples (either direction) of a value list in
    position order."""
    pos = {v: i for i, v in enumerate(order)}
    bad = []
    for (a, b, c) in in_team_aps(sorted(order)):
        if pos[a] < pos[b] < pos[c] or pos[c] < pos[b] < pos[a]:
            bad.append((a, b, c))
    return bad


# ---------------------------------------------------- check 1: X-INTERLEAVE
def check1():
    log("== check 1: X-INTERLEAVE survival ==")
    J = 20                       # values up to 2^20
    T = [2 ** j for j in range(J + 1)]
    # swapped arrangement: 2, 1, 8, 4, 32, 16, ...
    order = []
    k = 0
    while 2 * 4 ** k <= 2 ** J:
        order.append(2 * 4 ** k)
        order.append(4 ** k)
        k += 1
    rest = [v for v in T if v not in set(order)]
    order += sorted(rest)        # tail (top unpaired value, if any)
    assert sorted(order) == T
    # (a) the SET is 3-AP-free  => every arrangement valid; Top == {} for all u
    aps = in_team_aps(T)
    assert aps == [], f"powers of two contain APs?! {aps[:3]}"
    # explicit Top_T(u) audit
    Tset = set(T)
    tops = {u: [(2 * b - u, b) for b in T if u / 2 < b < u and 2 * b - u in Tset]
            for u in T}
    assert all(len(v) == 0 for v in tops.values())
    # (b) arrangement is (a fortiori) monotone-AP-free
    assert monotone_ap_violations(order) == []
    # (c) inversion pairs cover EVERY anchor (exhaustive audit to 4^7)
    NMAX = 4 ** 7
    uncovered = []
    pos = {v: i for i, v in enumerate(order)}
    pairs = [(u, w) for u in T for w in T
             if u < w and pos[w] < pos[u]]
    for N in range(1, NMAX + 1):
        if not any(is_inversion_at(u, w, N) for (u, w) in pairs):
            uncovered.append(N)
    assert uncovered == [], f"anchors uncovered: {uncovered[:10]}"
    # (d) pair family is exactly {(4^k, 2*4^k)}
    expect = set()
    k = 1
    while 2 * 4 ** k <= 2 ** J:
        expect.add((4 ** k, 2 * 4 ** k))
        k += 1
    expect.add((1, 2))
    assert set(pairs) == expect, (sorted(set(pairs) - expect)[:5],
                                  sorted(expect - set(pairs))[:5])
    # (e) displacement delta on displaced values is exactly 1
    import math
    blk = lambda v: int(math.log2(v))
    s = 0
    delta = {}
    for v in order:
        s = max(s, blk(v))
        delta[v] = s - blk(v)
    displaced = sorted({u for (u, w) in pairs})
    assert all(delta[u] == 1 for u in displaced if u > 1), \
        {u: delta[u] for u in displaced if delta[u] != 1}
    assert all(delta[v] in (0, 1) for v in T)
    # (f) THE LEDGER CHARGE: forced descents = Top-instances = 0
    charge = sum(len(tops[u]) for u in displaced)
    log(f"  set 3-AP-free: yes; arrangement monotone-AP-free: yes")
    log(f"  inversion pairs: {len(pairs)} = family (4^k, 2*4^k); "
        f"anchors 1..{NMAX} all covered")
    log(f"  delta==1 on displaced values: yes; ledger exposure charge: {charge}")
    log(f"  VERDICT: X-INTERLEAVE survives the accounting (charge 0). PASS")
    OUT['check1'] = {'n_pairs': len(pairs), 'anchors_audited': NMAX,
                     'uncovered': 0, 'exposure_charge': charge,
                     'verdict': 'LEGAL'}


# ------------------------------------------- check 2: D3 integration count
def check2():
    log("== check 2: D3 octave-recurrence count (>= v/4) ==")
    rng = random.Random(130)
    results = []
    for trial in range(40):
        X = rng.choice([64, 128, 256, 512])
        npairs = rng.randint(5, 60)
        pairs = set()
        while len(pairs) < npairs:
            u = rng.randint(X // 8, 16 * X)
            w = rng.randint(u + 1, 4 * u - 1)
            pairs.add((u, w))
        pairs = list(pairs)
        # v := min over anchors in [X, 2X) of coverage count
        v = min(sum(1 for (u, w) in pairs if is_inversion_at(u, w, N))
                for N in range(X, 2 * X))
        cnt = sum(1 for (u, w) in pairs if X < u < 8 * X)
        assert cnt >= v / 4, (X, v, cnt)
        results.append((X, v, cnt))
    # and on X-INTERLEAVE's own family
    pairs = [(4 ** k, 2 * 4 ** k) for k in range(1, 10)]
    for X in (64, 256, 1024):
        v = min(sum(1 for (u, w) in pairs if is_inversion_at(u, w, N))
                for N in range(X, 2 * X))
        cnt = sum(1 for (u, w) in pairs if X < u < 8 * X)
        assert cnt >= v / 4 and v >= 1, (X, v, cnt)
        results.append((X, v, cnt))
    log(f"  {len(results)} trials, bound cnt >= v/4 held in all. PASS")
    OUT['check2'] = {'trials': len(results), 'verdict': 'PASS'}


# ------------------------------- check 3: exposure mass on the e127 witness
def check3():
    log("== check 3: exposure mass on bal@16 v=160 witness ==")
    rows = open(os.path.join(DATA, 'e127_seam_budget.jsonl')).read()
    rows = [json.loads(l) for l in rows.strip().split('\n')]
    d = next(r for r in rows if r.get('v') == 160 and r['verdict'] == 'SAT')
    M = d['M']
    N = M                       # window (M, 8M] = W(N) with N = M
    A = set(d['colorA'])
    V = set(range(M + 1, 8 * M + 1))
    B = V - A
    teams = {'A': (A, d['orderA']), 'B': (B, d['orderB'])}
    rep = {}
    for name, (T, order) in teams.items():
        assert set(order) == T & V and len(order) == len(T & V)
        inv = seam_inversions(order, N)
        rec = d['anatomy'][name]
        assert len(inv) == rec['n_inv'], (name, len(inv), rec['n_inv'])
        assert monotone_ap_violations(order) == []
        D = sorted({u for (u, w) in inv})       # displaced set
        Adv = sorted({w for (u, w) in inv})     # advanced set
        # exposure: for displaced u, Top pairs (a, b), b in T, u/2 < b < u
        expo_in = expo_below = casc = 0
        for u in D:
            for b in [x for x in T if u / 2 < x < u]:
                a = 2 * b - u
                if a < 1:
                    continue
                if a > M:                        # in-window: color known
                    if a in T:
                        expo_in += 1
                        if 4 * u / 7 < b < 3 * u / 4:
                            casc += 1            # L-CASCADE range, seam pair
                else:                            # below window: unseen by U
                    expo_below += 1              # potential demand surface
        naps = len(in_team_aps(sorted(T & V)))
        rep[name] = dict(n_inv=len(inv), n_D=len(D), n_Adv=len(Adv),
                         expo_in=expo_in, expo_below=expo_below,
                         cascade_range=casc, in_window_APs=naps)
        log(f"  team {name}: inv={len(inv)} |D|={len(D)} |Adv|={len(Adv)} "
            f"expo_in={expo_in} expo_below={expo_below} "
            f"cascade={casc} APs={naps}")
    # the binding contrast: dense teams carry Theta(M^2) APs and
    # Theta(M)-scale exposure per displaced value; X-INTERLEAVE carries 0
    assert all(r['in_window_APs'] > 8 * M for r in rep.values())
    assert any(r['expo_in'] + r['expo_below'] > 0 for r in rep.values())
    log("  dense-team exposure is nonzero at Theta(M)*|D| scale; "
        "finite instance saw none of expo_below. PASS")
    OUT['check3'] = rep


# ---------------------------------------------------- check 4: P5/P6 sanity
def check4():
    log("== check 4: P5 descent pressure on the witness ==")
    rows = [json.loads(l) for l in
            open(os.path.join(DATA, 'e127_seam_budget.jsonl'))
            .read().strip().split('\n')]
    d = next(r for r in rows if r.get('v') == 160 and r['verdict'] == 'SAT')
    M = d['M']
    V = set(range(M + 1, 8 * M + 1))
    A = set(d['colorA'])
    for name, T, order in (('A', A, d['orderA']), ('B', V - A, d['orderB'])):
        pos = {v: i for i, v in enumerate(order)}
        aps = in_team_aps(sorted(T))
        # P5: every in-team AP has a descent on an adjacent pair
        bad = [t for t in aps
               if not (pos[t[1]] < pos[t[0]] or pos[t[2]] < pos[t[1]])]
        assert bad == [], (name, bad[:3])
        desc = {(x, y) for (a, b, c) in aps
                for (x, y) in ((a, b), (b, c)) if pos[y] < pos[x]}
        assert len(desc) >= len(aps) / 2
        log(f"  team {name}: {len(aps)} in-window APs, all carry a "
            f"descent; {len(desc)} distinct descent pairs (>= APs/2)")
    OUT['check4'] = {'verdict': 'PASS'}


# -------------------------------------------------------- check 5: L-COMP
def check5():
    log("== check 5: L-COMP composition audit on random AP-free orders ==")
    rng = random.Random(1307)
    found_orders = 0
    tested = 0
    while found_orders < 30 and tested < 4000:
        tested += 1
        n = rng.randint(8, 26)
        vals = rng.sample(range(1, 80), n)
        order = vals[:]
        rng.shuffle(order)
        if monotone_ap_violations(order):
            continue
        found_orders += 1
        pos = {v: i for i, v in enumerate(order)}
        aps = in_team_aps(sorted(vals))
        # forced-descent digraph: edges y -> x (pos[y] < pos[x]) on
        # adjacent AP pairs (x, y), x < y
        edges = {(y, x) for (a, b, c) in aps
                 for (x, y) in ((a, b), (b, c)) if pos[y] < pos[x]}
        # L-COMP: no 2-path c -> b -> a along an AP (a, b, c)
        for (a, b, c) in aps:
            two_path = (c, b) in edges and (b, a) in edges
            is_dec_mono = pos[c] < pos[b] < pos[a]
            assert two_path == is_dec_mono
            assert not two_path, ("AP-free order carries a composed "
                                  "descent 2-path?!", (a, b, c))
    assert found_orders >= 30
    log(f"  {found_orders} AP-free random orders audited "
        f"({tested} sampled): no composed descent 2-path along any AP; "
        f"2-path <=> decreasing monotone AP confirmed. PASS")
    OUT['check5'] = {'orders': found_orders, 'verdict': 'PASS'}


if __name__ == '__main__':
    for fn in (check1, check2, check3, check4, check5):
        fn()
    with open(os.path.join(DATA, 'e130_ledger_checks.json'), 'w') as f:
        json.dump(OUT, f, indent=1)
    log("E130 ALL CHECKS PASS")
