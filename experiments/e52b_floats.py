"""e52b — quantify the escape: minimal removals (part-1 semantics) and
minimal floats (era semantics with selectors) + e51 extras inspection.

CAVEAT (see notes/18 §3): min_floats pins the P0 history order to
increasing, which adds spurious constraints (the fully-interleaved system
is UNSAT with increasing P0 but SAT with free P0, defects or not).  Its
float counts are therefore NOT meaningful as stated; superseded by the
state-suffix systems in e52c_suffix.py."""
import sys, time, random
sys.path.insert(0, '/Users/will/Dev/personal/tasks/math/erdos197/experiments')
from e3_sat import OrderSAT
from e52_subset_escape import (zone1, zone_full, defect, defect_of_block,
                               team_below)
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195


def solve_with_extras(enc, extra_clauses, top):
    """OrderSAT-style lazy-transitivity solve with extra clauses/vars."""
    s = Cadical195(bootstrap_with=enc.clauses + extra_clauses)
    while True:
        if not s.solve():
            return False
        model = s.get_model()
        ms = set(l for l in model if l > 0)

        def bef(i, j):
            if i < j:
                return enc.varmap[(i, j)] in ms
            return enc.varmap[(j, i)] not in ms
        n = enc.n
        wins = [0] * n
        for i in range(n):
            for j in range(n):
                if i != j and bef(i, j):
                    wins[i] += 1
        order = sorted(range(n), key=lambda i: -wins[i])

        def lit(i2, j2):
            if i2 < j2:
                return enc.varmap[(i2, j2)]
            return -enc.varmap[(j2, i2)]
        added = 0
        for a in range(n):
            for b in range(a + 1, n):
                i, j = order[a], order[b]
                if not bef(i, j):
                    for c in range(n):
                        k = order[c]
                        if k != i and k != j and bef(i, k) and bef(k, j):
                            s.add_clause([-lit(j, i), -lit(i, k), lit(j, k)])
                            added += 1
                            break
                    if added > 10000:
                        break
            if added > 10000:
                break
        if not added:
            return ms


def min_removal(M, zname="Zfull", tmax=None):
    """part-1 semantics: zone preplaced (as unit (b) constraints), order B;
    selectors r_v disable all constraints touching v.  Find min #removed."""
    B = sorted(range(M + 1, 2 * M + 1))
    Bset = set(B)
    Z = zone_full(M) if zname == "Zfull" else zone1(M)
    enc = OrderSAT(B)
    top = enc.n * (enc.n - 1) // 2
    sel = {}
    for v in B:
        top += 1
        sel[v] = top
    extra = []
    for y in B:
        d = 1
        while y + d <= B[-1]:
            x, z = y - d, y + d
            if x in Bset and z in Bset:
                extra.append([sel[x], sel[y], sel[z], -enc.before(x, y), -enc.before(y, z)])
                extra.append([sel[x], sel[y], sel[z], -enc.before(z, y), -enc.before(y, x)])
            d += 1
    for y in B:
        for x in Z:
            z = 2 * y - x
            if z > y and z in Bset:
                extra.append([sel[y], sel[z], enc.before(z, y)])
    lo, hi = 0, tmax or len(B)
    best = None
    for t in range(1, hi + 1):
        card = CardEnc.atmost([sel[v] for v in B], bound=t, top_id=top + 10000 * t,
                              encoding=EncType.seqcounter)
        r = solve_with_extras(enc, extra + card.clauses, top)
        if r is not False:
            removed = sorted(v for v in B if sel[v] in r)
            return t, removed, r
    return None, None, None


def min_floats(M, DB_mode="law", DZ_mode="law", report=True):
    """era semantics: P0 = team∩[1,M/2] ∖ D_Z fixed first; era1 = D_Z ∪ B∖D_B;
    selectors s_w (w in era1) remove the 'after all P0' boundary for w.
    Find min #floats for SAT; report which values float."""
    B = set(range(M + 1, 2 * M + 1))
    DB = defect_of_block(M, 2 * M)[0] if DB_mode == "law" else set()
    DZ = defect_of_block(M // 4, M // 2)[0] if DZ_mode == "law" else set()
    below = team_below(M)
    P0 = [v for v in below if v not in DZ]
    era1 = sorted(set(DZ) | (B - DB))
    U = sorted(set(P0) | set(era1))
    enc = OrderSAT(U)
    preset = set(P0)
    for i in range(len(P0) - 1):
        enc.add(enc.before(P0[i], P0[i + 1]))
    top = enc.n * (enc.n - 1) // 2
    sel = {}
    for w in era1:
        top += 1
        sel[w] = top
    extra = []
    for u in P0:
        for w in era1:
            extra.append([sel[w], enc.before(u, w)])
    Uset = set(U)
    for y in U:
        d = 1
        while y + d <= U[-1]:
            x, z = y - d, y + d
            if x in Uset and z in Uset:
                if not (x in preset and y in preset and z in preset):
                    enc.add(-enc.before(x, y), -enc.before(y, z))
                    enc.add(-enc.before(z, y), -enc.before(y, x))
            d += 1
    for t in range(0, len(era1) + 1):
        cls = []
        if t == 0:
            cls = [[-sel[w]] for w in era1]
        else:
            card = CardEnc.atmost([sel[w] for w in era1], bound=t,
                                  top_id=top + 100000 + 10000 * t,
                                  encoding=EncType.seqcounter)
            cls = card.clauses
        r = solve_with_extras(enc, extra + cls, top)
        if r is not False:
            fl = sorted(w for w in era1 if sel[w] in r)
            if report:
                print(f"    min floats = {t}; floating set = {fl}")
            return t, fl
    return None, None


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "rem":
        for M in [32, 64]:
            for zname in ["Z1", "Zfull"]:
                t0 = time.time()
                t, rem, _ = min_removal(M, zname)
                print(f"M={M} {zname}: min removal = {t}, e.g. {rem} ({time.time()-t0:.0f}s)", flush=True)
    if which == "fl":
        for M in [32, 64, 128]:
            print(f"M={M}:")
            for DBm, DZm in [("law", "law"), ("none", "law"), ("law", "none"), ("none", "none")]:
                print(f"  D_B={DBm}, D_Z={DZm}:")
                t0 = time.time()
                min_floats(M, DBm, DZm)
                print(f"    ({time.time()-t0:.0f}s)", flush=True)
