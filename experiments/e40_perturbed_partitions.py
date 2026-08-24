"""Perturbed-partition harness: pure-complete systems for team-sets that are
dyadic-with-boundary-shifts. Usage (after a dyadic UNSAT): scan perturbations
to test obstruction robustness for the general-NO bridge."""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def make_team(shifts, N):
    """team = union over even k of (2^(k-1)+s_lo(k), 2^k+s_hi(k)];
    shifts: dict k -> (lo, hi) small ints."""
    team = set()
    k = 2
    while 2 ** (k - 1) <= N:
        lo, hi = shifts.get(k, (0, 0))
        a = 2 ** (k - 1) + lo
        b = min(2 ** k + hi, N)
        if k % 2 == 0:
            team.update(range(a + 1, b + 1))
        k += 1
    return sorted(team)

def decide_team(team, closure_check=True, max_rounds=100000):
    """pure system for an arbitrary team set: monotone triples fully inside;
    NOTE: completions beyond max(team) assumed OUTSIDE team — caller must pick
    the horizon so that this holds (dyadic-top-like)."""
    V = team
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    Vs = set(V)
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
    mx = V[-1]
    for y in V:
        d = 1
        while y + d <= mx:
            x, z = y - d, y + d
            if x in Vs and z in Vs:
                cl.append([-before(x, y), -before(y, z)])
                cl.append([-before(z, y), -before(y, x)])
            d += 1
    s = Cadical195(bootstrap_with=cl)
    rounds = 0
    import numpy as np
    while True:
        rounds += 1
        if not s.solve():
            return False
        model = s.get_model()
        posb = np.zeros(top + 1, dtype=bool)
        for l in model:
            if 0 < l <= top: posb[l] = True
        B = np.zeros((n, n), dtype=bool)
        for (i, j), var in t.items():
            if posb[var]: B[i, j] = True
            else: B[j, i] = True
        wins = B.sum(axis=1)
        order = np.argsort(-wins, kind='stable')
        R = B[np.ix_(order, order)]
        iu = np.triu_indices(n, 1)
        bad_idx = np.nonzero(~R[iu])[0]
        if len(bad_idx) == 0:
            return [V[i] for i in order]
        added = 0
        for bi in bad_idx[:40000]:
            a_, b_ = iu[0][bi], iu[1][bi]
            i, j = int(order[a_]), int(order[b_])
            ks = np.nonzero(B[i] & B[:, j])[0]
            if len(ks):
                k = int(ks[0])
                s.add_clause([-before(V[i], V[k]), -before(V[k], V[j]),
                              before(V[i], V[j])])
                added += 1
                if added > 30000: break

if __name__ == "__main__":
    # smoke test: unperturbed = pure system
    team = make_team({}, 1024)
    t0 = time.time()
    r = decide_team(team)
    print(f"unperturbed 1024: {'SAT' if r else 'UNSAT'} ({time.time()-t0:.0f}s)")
