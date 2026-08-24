"""ω-order construction: duty-driven closure batches, each arranged by exact
SAT against the placed context. Fairness: duty v placed by its turn."""
import sys, time, json
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(N):
    return [v for v in range(2, N + 1) if block(v) % 2 == 0]

def solve_batch(batch, placed, pos, N, teamset):
    """arrange 'batch' after the placed prefix. Constraints:
    - pairs (x placed, u in batch): completion z = 2u - x (in team, ≤ N):
        z placed already? fine. z in batch: z ≺ u. z unplaced outside: FAIL(caller adds).
      (downward completions 2u - x with x placed > u: same closure treatment)
    - batch-internal pairs both directions: completion in batch: order constraint;
      placed: fine; in team unplaced outside batch: FAIL.
    Returns ordered batch or None if closure incomplete or False if UNSAT."""
    B = sorted(batch)
    Bs = set(B)
    idx = {v: i for i, v in enumerate(B)}
    n = len(B)
    top = 0
    t = {}
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            t[(i, j)] = top
    def before(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]
    cl = []
    need_more = set()
    for u in B:
        for x in placed:
            for z in (2 * u - x,):
                if z <= 0 or z > N or z == u: continue
                if z in Bs:
                    if z != x:
                        cl.append([before(z, u)])
                elif z in teamset and z not in pos:
                    need_more.add(z)
    for a in B:
        for b in B:
            if b <= a: continue
            c = 2 * b - a
            if 0 < c <= N:
                if c in Bs:
                    cl.append([-before(a, b), before(c, b)])
                elif c in teamset and c not in pos:
                    need_more.add(c)
            d2 = 2 * a - b
            if 0 < d2 <= N:
                if d2 in Bs:
                    cl.append([-before(b, a), before(d2, a)])
                elif d2 in teamset and d2 not in pos:
                    need_more.add(d2)
    if need_more:
        return ('grow', need_more)
    s = Cadical195(bootstrap_with=cl)
    # lazy transitivity
    rounds = 0
    while True:
        rounds += 1
        if rounds > 2000:
            return ('indet', None)
        if not s.solve():
            return ('unsat', None)
        model = set(l for l in s.get_model() if l > 0)
        def bef(u, w):
            l = before(u, w)
            return (l in model) if l > 0 else (-l not in model)
        wins = {v: 0 for v in B}
        for i in range(n):
            for j in range(i + 1, n):
                u, w = B[i], B[j]
                if bef(u, w): wins[u] += 1
                else: wins[w] += 1
        order = sorted(B, key=lambda v: -wins[v])
        added = 0
        for i in range(n):
            for j in range(i + 1, n):
                u, w = order[i], order[j]
                if not bef(u, w):
                    for x in order:
                        if x != u and x != w and bef(u, x) and bef(x, w):
                            s.add_clause([-before(u, x), -before(x, w), before(u, w)])
                            added += 1
                            break
                    if added > 5000: break
            if added > 5000: break
        if not added:
            return ('sat', order)

def construct(N, batch_cap=4000):
    team = sa(N)
    teamset = set(team)
    placed = []
    pos = {}
    t0 = time.time()
    for i, v in enumerate(team):
        if v in pos: continue
        batch = {v}
        while True:
            res = solve_batch(batch, placed, pos, N, teamset)
            if res[0] == 'grow':
                batch |= res[1]
                if len(batch) > batch_cap:
                    print(f"duty {v}: batch explosion ({len(batch)})", flush=True)
                    return None
            elif res[0] == 'unsat':
                print(f"duty {v}: batch UNSAT (size {len(batch)})", flush=True)
                return None
            elif res[0] == 'indet':
                print(f"duty {v}: indeterminate", flush=True)
                return None
            else:
                order = res[1]
                for u in order:
                    pos[u] = len(placed)
                    placed.append(u)
                break
        if i % 200 == 0:
            print(f"duty {v}: placed {len(placed)} ({time.time()-t0:.0f}s)", flush=True)
    return placed

def doom_check(seq, teamset, maxv, cap=20):
    pos = {v: i for i, v in enumerate(seq)}
    bad = []
    n = len(seq)
    for i in range(n):
        x = seq[i]
        for j in range(i + 1, n):
            y = seq[j]
            z = 2 * y - x
            if z <= 0 or z == y or z > maxv: continue
            if z in teamset and (z not in pos or pos[z] > j):
                bad.append((x, y, z))
                if len(bad) >= cap: return bad
    return bad

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1024
    seq = construct(N)
    if seq is None:
        sys.exit(1)
    print(f"constructed n={len(seq)}; checking...", flush=True)
    bad = doom_check(seq, set(sa(N)), N)
    print(f"violations: {len(bad)}")
    if not bad:
        json.dump(seq, open(f'data/omega_{N}.json', 'w'))
        print(f"CLEAN ω-order prefix at {N} — SAVED", flush=True)
