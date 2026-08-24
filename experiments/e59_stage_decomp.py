"""Stage-decomposition test: THE reduction of #197's dyadic side.

T = concatenation of finite stage fibers, each internally ordered. For AP
triple (x,y,z) in S_A (z = 2y - x), with s = stage function:
  s(x),s(z) same side of s(y) (both < or both >): safe.
  s(x)<s(y)<s(z) or s(z)<s(y)<s(x): AUTO-VIOLATION (condition A fails).
  s(x)<s(y)=s(z): forced z BEFORE y  (in stage s(y))
  s(z)<s(y)=s(x): forced x BEFORE y
  s(x)=s(y)<s(z): forced y BEFORE x
  s(y)=s(z)<s(x): forced y BEFORE z
  s(x)=s(y)=s(z): within-stage triple: forbid both monotone.
If A holds for ALL triples and every fiber's order problem (forced pairs +
triples, transitivity) is SAT, then S_A is permutable. Fibers independent.

stage(v) = max(depth(v) - DSHIFT, block(v)//2), depth = v2(v-2).
Exact for stages s with 4^s <= N (completions of fiber pairs <= 2*4^s, and
in S_A implies <= 4^s). Args: m [DSHIFT]   (N = 4^m; checks stages <= m-1).
"""
import sys, time
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def depth(v):
    w = v - 2
    if w == 0: return 10 ** 9
    return (w & -w).bit_length() - 1

def main(m, dshift=2):
    N = 4 ** m
    V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
    Vs = set(V)
    stg = {v: max(depth(v) - dshift, block(v) // 2) for v in V}
    autoviol = []
    forced = {}   # stage -> set of (u,w) meaning u BEFORE w
    triples = {}  # stage -> list of (x,y,z)
    for y in V:
        d = 1
        while y + d <= N:
            x, z = y - d, y + d
            d += 1
            if x not in Vs or z not in Vs: continue
            sx, sy, sz = stg[x], stg[y], stg[z]
            if (sx < sy < sz) or (sz < sy < sx):
                if len(autoviol) < 20: autoviol.append(((x, y, z), (sx, sy, sz)))
                else: autoviol.append(None)
                continue
            if sx < sy == sz: forced.setdefault(sy, set()).add((z, y))
            elif sz < sy == sx: forced.setdefault(sy, set()).add((x, y))
            elif sx == sy < sz: forced.setdefault(sy, set()).add((y, x))
            elif sy == sz < sx: forced.setdefault(sy, set()).add((y, z))
            elif sx == sy == sz: triples.setdefault(sy, []).append((x, y, z))
    print(f"N=4^{m} DSHIFT={dshift}: auto-violations(A) = {len(autoviol)}", flush=True)
    for a in autoviol[:20]:
        if a: print(f"  A-viol {a[0]} stages {a[1]} depths "
                    f"{tuple(depth(t) for t in a[0])}", flush=True)
    if autoviol: return
    maxs = max(s for s in range(1, m) )
    for s in sorted(set(list(forced) + list(triples))):
        if 4 ** s > N: continue
        F = sorted(v for v in V if stg[v] == s)
        idx = {v: i for i, v in enumerate(F)}
        n = len(F)
        t0 = time.time()
        # order vars
        var = {}
        cnt = 0
        for i in range(n):
            for j in range(i + 1, n):
                cnt += 1
                var[(i, j)] = cnt
        def bef(u, w):
            i, j = idx[u], idx[w]
            return var[(i, j)] if i < j else -var[(j, i)]
        cl = [[bef(u, w)] for (u, w) in forced.get(s, ())]
        for (x, y, z) in triples.get(s, ()):
            # not (x<y and y<z); not (z<y and y<x)
            cl.append([-1 * bef(x, y), -1 * bef(y, z)])
            cl.append([-1 * bef(z, y), -1 * bef(y, x)])
        sol = Cadical195(bootstrap_with=cl)
        verdict = None
        for rnd in range(100000):
            if not sol.solve():
                verdict = "UNSAT"
                break
            model = set(l for l in sol.get_model() if l > 0)
            ordkey = [0] * n
            # topological check via wins count is wrong; do cycle repair:
            new = []
            # find transitivity violations u<v<w but w<u
            # build order by sorting with comparator from model (may be cyclic)
            lt = [[False] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    if var[(i, j)] in model: lt[i][j] = True
                    else: lt[j][i] = True
            # check for 3-cycles lazily
            import random
            bad = 0
            for i in range(n):
                for j in range(n):
                    if lt[i][j]:
                        row_j = lt[j]
                        for k in range(n):
                            if row_j[k] and lt[k][i]:
                                a, b, c = i, j, k
                                l1 = var[(a, b)] if a < b else -var[(b, a)]
                                l2 = var[(b, c)] if b < c else -var[(c, b)]
                                l3 = var[(c, a)] if c < a else -var[(a, c)]
                                new.append([-l1, -l2, -l3])
                                bad += 1
                                break
                        if bad > 5000: break
                if bad > 5000: break
            if not new:
                verdict = "SAT"
                break
            sol.append_formula(new)
        print(f"  stage {s}: |F|={n} forced={len(forced.get(s, ()))} "
              f"triples={len(triples.get(s, []))}: {verdict} "
              f"({time.time()-t0:.0f}s)", flush=True)
        if verdict == "UNSAT":
            return

if __name__ == "__main__":
    m = int(sys.argv[1])
    ds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    main(m, ds)
