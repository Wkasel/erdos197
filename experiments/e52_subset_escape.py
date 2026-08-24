"""e52 — the subset-escape algebra (notes/18).

Part 1: B = (M,2M], zone Z = (M/4,M/2] (optionally full multi-level zone).
Full B is UNSAT for M >= 16 (fatal zone). Question: does removing the
defect class D = {v in B : v == 2 mod 2^{k//2}}, k = log2(2M), restore SAT?
Controls: other classes (==2 mod other moduli, ==1 / ==6 mod same modulus),
random removals of the same cardinality.

Part 2 (M=32): constraint census touching D; minimal UNSAT value-cores of
the full system and their intersection with D; residue algebra mod 2^{k//2}.

Part 4: can D be appended strictly after a valid (zone, B\\D) arrangement?
Exact formalization: order = [zone (fixed, first)] + [sigma over B\\D] +
[tau over D]; constraints = no monotone 3-AP within the team's value set
(zone included as AP members) restricted to pairs/triples inside zone+B,
plus doom-freeness is inherited.  We decide SAT over tau given sigma, and
also the joint problem (sigma free, D-last).
"""
import sys, random, time
sys.path.insert(0, '/Users/will/Dev/personal/tasks/math/erdos197/experiments')
from e3_sat import OrderSAT, decide, verify


def zone1(M):
    return set(range(M // 4 + 1, M // 2 + 1))


def zone_full(M):
    Z = set()
    hi, lo = M // 2, M // 4
    while lo >= 1:
        Z.update(range(lo + 1, hi + 1))
        hi //= 4
        lo //= 4
    return Z


def defect(M, mod=None, res=2):
    k = (2 * M).bit_length() - 1
    m = mod if mod is not None else 2 ** (k // 2)
    return set(v for v in range(M + 1, 2 * M + 1) if v % m == res), m


def part1():
    print("=" * 72)
    print("PART 1: subset escape — feasibility of B \\ D and controls")
    for M in [16, 32, 64, 128]:
        B = set(range(M + 1, 2 * M + 1))
        k = (2 * M).bit_length() - 1
        for zname, Z in [("Z1", zone1(M)), ("Zfull", zone_full(M))]:
            print(f"\nM={M} (k={k}) zone={zname}={sorted(Z)}")
            t0 = time.time()
            r = decide(B, Z)
            print(f"  full B:            {'SAT' if r else 'UNSAT'}  ({time.time()-t0:.1f}s)")
            D, m = defect(M)
            t0 = time.time()
            r = decide(B - D, Z, return_seq=True)
            tag = 'SAT' if r is not False else 'UNSAT'
            print(f"  B \\ D (==2 mod {m}, {len(D)} vals {sorted(D)}): {tag} ({time.time()-t0:.1f}s)")
            if r is not False:
                err = verify(B - D, Z, r)
                assert err is None, err
            # controls: ==2 mod other moduli
            for mod in [4, 8, 16, 32]:
                if mod == m or mod > M:
                    continue
                Dm, _ = defect(M, mod=mod)
                r2 = decide(B - Dm, Z)
                print(f"    ctrl ==2 mod {mod:2d} ({len(Dm)} vals): {'SAT' if r2 else 'UNSAT'}")
            # ==1 and ==6 mod same modulus
            for res in [1, 6]:
                if res >= m:
                    continue
                Dr, _ = defect(M, res=res)
                r2 = decide(B - Dr, Z)
                print(f"    ctrl =={res} mod {m:2d} ({len(Dr)} vals): {'SAT' if r2 else 'UNSAT'}")
            # random removals of |D| values, 10 trials
            rng = random.Random(197)
            sat = 0
            for t in range(10):
                Dr = set(rng.sample(sorted(B), len(D)))
                if decide(B - Dr, Z):
                    sat += 1
            print(f"    ctrl random |D|={len(D)} removals: {sat}/10 SAT")


def census(M=32):
    print("=" * 72)
    print(f"PART 2a: constraint census at M={M}, zone Z1")
    B = sorted(range(M + 1, 2 * M + 1))
    Bset = set(B)
    Z = zone1(M)
    D, m = defect(M)
    # (b)-forced pairs
    forced = []
    for y in B:
        for x in sorted(Z):
            z = 2 * y - x
            if z > y and z in Bset:
                forced.append((x, y, z))
    fD = [t for t in forced if t[1] in D or t[2] in D]
    print(f"  (b)-forced pairs (x,y,z): {len(forced)} total, {len(fD)} touch D")
    print(f"    z in D: {[t for t in forced if t[2] in D]}")
    print(f"    y in D: {[t for t in forced if t[1] in D]}")
    # 3-AP triples
    aps = []
    for y in B:
        d = 1
        while y + d <= B[-1]:
            if y - d in Bset and y + d in Bset:
                aps.append((y - d, y, y + d))
            d += 1
    aD = [t for t in aps if set(t) & D]
    print(f"  3-AP triples in B: {len(aps)} total, {len(aD)} touch D")
    # residue algebra
    print(f"\n  residue algebra mod {m} (D is class 2):")
    print(f"    zone residues mod {m}: {sorted(set(x % m for x in Z))} (Z = {sorted(Z)})")
    # for x in Z, y in B, z = 2y - x: z in D iff x == 2y-2 mod m
    from collections import Counter
    cnt = Counter()
    for (x, y, z) in forced:
        cnt[(y in D, z in D)] += 1
    print(f"    (b)-pairs by (y in D, z in D): {dict(cnt)}")
    cnt = Counter()
    for t in aps:
        cnt[tuple(v in D for v in t)] += 1
    print(f"    APs by D-membership pattern (x,y,z): {dict(cnt)}")


def cores(M=32, trials=8):
    print("=" * 72)
    print(f"PART 2b: minimal UNSAT value-cores of full system, M={M}, zone Z1")
    B = sorted(range(M + 1, 2 * M + 1))
    Z = zone1(M)
    D, m = defect(M)
    assert decide(B, Z) is False
    rng = random.Random(7)
    seen = set()
    for t in range(trials):
        order = list(B)
        if t == 0:
            order.sort(key=lambda x: -x)
        elif t == 1:
            order.sort()
        else:
            rng.shuffle(order)
        core = list(B)
        for v in order:
            trial = [u for u in core if u != v]
            if decide(trial, Z) is False:
                core = trial
        key = tuple(sorted(core))
        if key in seen:
            continue
        seen.add(key)
        cd = sorted(set(core) & D)
        print(f"  core ({len(core)}): {sorted(core)}")
        print(f"    core ∩ D = {cd} ({len(cd)} of {len(D)})")
        # is core minus its D part SAT?
        r = decide(set(core) - D, Z)
        print(f"    core \\ D: {'SAT' if r else 'UNSAT'}")


def append_D(M, n_witnesses=3, seed=0):
    """Part 4: zone first, then B\\D in a witness order sigma, then D in
    some order tau.  Constraints on the FULL sequence over V = Z ∪ B:
      - no monotone 3-AP with all three values in V,
      - (equivalently (b) is the zone-rooted instance of the AP ban).
    Zone internal order: increasing (zone values were placed in earlier
    blocks; any relative order among them is fixed history — we take
    increasing; APs wholly inside the zone are the previous block's business
    and are excluded).
    We decide tau by SAT with sigma fixed; and also the joint problem where
    sigma is free but all of D must come after all of B\\D."""
    print("=" * 72)
    print(f"PART 4: append-D after a valid B\\D arrangement, M={M}")
    B = set(range(M + 1, 2 * M + 1))
    Z = zone1(M)
    D, m = defect(M)
    BD = B - D
    # obstruction scan: (b)-pairs with y in B\D, z in D (z must precede y,
    # but append forces z after y) — these make ANY append UNSAT.
    obstr = [(2 * y - z, y, z) for y in BD for z in sorted(D)
             if z > y and (2 * y - z) in Z]
    print(f"  hard obstructions (x in Z, y in B\\D, z in D, z=2y-x): {obstr}")
    # joint problem: order all of Z ∪ B, zone increasing first, D last.
    V = sorted(Z | B)
    enc = OrderSAT(V)
    Vset = set(V)
    zs = sorted(Z)
    # fix zone order and zone-first
    for i in range(len(zs) - 1):
        enc.add(enc.before(zs[i], zs[i + 1]))
    for x in zs:
        for v in sorted(B):
            enc.add(enc.before(x, v))
    # D after B\D
    for y in sorted(BD):
        for r in sorted(D):
            enc.add(enc.before(y, r))
    # AP ban over V, except triples wholly inside the zone
    for y in V:
        d = 1
        while y + d <= V[-1]:
            x, z = y - d, y + d
            if x in Vset and z in Vset and not (x in Z and y in Z and z in Z):
                enc.add(-enc.before(x, y), -enc.before(y, z))
                enc.add(-enc.before(z, y), -enc.before(y, x))
            d += 1
    r = enc.solve()
    print(f"  joint [zone, then B\\D free, then D free]: "
          f"{'SAT' if r is not False else 'UNSAT'}")
    if r is not False:
        print(f"    witness: {r}")
    # per-witness variant: sample distinct B\D witnesses, then try tau
    rng = random.Random(seed)
    found = 0
    tried = 0
    while found < n_witnesses and tried < 30:
        tried += 1
        # random SAT witness for B\D: randomize by forcing a few random pairs
        sub = decide_random_witness(BD, Z, rng)
        if sub is False:
            continue
        found += 1
        ok = try_append(sub, D, Z, B)
        print(f"  witness #{found} sigma={sub}")
        print(f"    append tau exists: {ok}")


def decide_random_witness(BD, Z, rng):
    """get a (a)+(b) witness for BD with randomized tie-breaking."""
    enc = OrderSAT(sorted(BD))
    Bs = sorted(BD)
    Bset = set(Bs)
    for y in Bs:
        d = 1
        while y + d <= Bs[-1]:
            x, z = y - d, y + d
            if x in Bset and z in Bset:
                enc.add(-enc.before(x, y), -enc.before(y, z))
                enc.add(-enc.before(z, y), -enc.before(y, x))
            d += 1
    for y in Bs:
        for x in Z:
            z = 2 * y - x
            if z > y and z in Bset:
                enc.add(enc.before(z, y))
    # random polarity hints: a few random soft pair preferences as hard tries
    pairs = [(a, b) for i, a in enumerate(Bs) for b in Bs[i + 1:]]
    rng.shuffle(pairs)
    for (a, b) in pairs[:6]:
        enc.add(enc.before(a, b) if rng.random() < .5 else enc.before(b, a))
    r = enc.solve()
    return r


def try_append(sigma, D, Z, B):
    """given fixed sigma over B\\D (zone before all), decide tau over D
    appended after; returns tau or False."""
    V = sorted(Z) + list(sigma) + sorted(D)  # candidate full ordering domain
    pos = {}
    for i, v in enumerate(sorted(Z) + list(sigma)):
        pos[v] = i
    n0 = len(pos)
    enc = OrderSAT(sorted(D))
    Vset = set(Z) | set(B)
    ok_unit = True
    # triples over zone ∪ B with at least one D member
    allv = sorted(Vset)
    for y in allv:
        d = 1
        while y + d <= allv[-1]:
            x, z = y - d, y + d
            if x in Vset and z in Vset:
                trip = (x, y, z)
                nd = sum(v in D for v in trip)
                if nd == 0:
                    d += 1
                    continue
                if all(v in Z for v in trip):
                    d += 1
                    continue
                # positions: D-values all after non-D
                if nd == 3:
                    enc.add(-enc.before(x, y), -enc.before(y, z))
                    enc.add(-enc.before(z, y), -enc.before(y, x))
                elif nd == 2:
                    if y not in D:  # x,z in D: incr needs pos(x)<pos(y) no; decr needs pos(z)<pos(y) no
                        pass
                    elif x not in D:  # y,z in D: incr iff x placed & y<z in tau
                        enc.add(enc.before(z, y))
                    else:  # x,y in D, z placed: decr iff tau y before x
                        enc.add(enc.before(x, y))
                else:  # nd == 1
                    if y in D:
                        pass  # impossible both ways
                    elif z in D:  # incr iff pos(x)<pos(y) in placed part
                        if x in pos and y in pos and pos[x] < pos[y]:
                            ok_unit = False
                    else:  # x in D: decr iff pos(z)<pos(y)
                        if z in pos and y in pos and pos[z] < pos[y]:
                            ok_unit = False
            d += 1
    if not ok_unit:
        return False
    r = enc.solve()
    return r


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "1"):
        part1()
    if which in ("all", "2"):
        census(32)
        cores(32)
    if which in ("all", "4"):
        for M in [16, 32, 64]:
            append_D(M)


# ---------------------------------------------------------------------------
# PART 1b / 4: era semantics.  Boundary structure of the ladder, no extras:
#   P0   = (team ∩ [1, M/2]) \ D_Z   preplaced (fixed increasing order)
#   era1 = D_Z ∪ (B \ D_B)           free order, all after P0
#   era2 = D_B ∪ (B' \ D_B')         free order, all after era1   [optional]
# where B = (M,2M], B' = (4M,8M], D_X = defect class of the enclosing block.
# Constraints: no monotone 3-AP among team values (triples wholly inside P0
# excluded — they are the previous eras' already-verified history).
# Completions beyond the horizon land in other-team blocks: free (exact).
def stage_system(stages, pre, seq_hint=False):
    """stages: list of sorted value-lists, placed in stage order; pre: fixed
    prefix (list, fixed order).  Returns witness or False."""
    U = list(pre)
    for s in stages:
        U += list(s)
    enc = OrderSAT(sorted(U))
    Uset = set(U)
    preset = set(pre)
    # fix pre order
    for i in range(len(pre) - 1):
        enc.add(enc.before(pre[i], pre[i + 1]))
    # stage ordering
    prev = list(pre)
    for s in stages:
        for u in prev:
            for w in s:
                enc.add(enc.before(u, w))
        prev = list(s)
        # note: only adjacent-stage clauses needed (transitivity closes it),
        # but add pre-to-every-stage for safety of unit propagation:
    for i, s in enumerate(stages):
        for j in range(i + 1, len(stages)):
            for u in s:
                for w in stages[j]:
                    enc.add(enc.before(u, w))
    for x in pre:
        for s in stages:
            for w in s:
                enc.add(enc.before(x, w))
    # AP clauses
    allv = sorted(Uset)
    for y in allv:
        d = 1
        while y + d <= allv[-1]:
            x, z = y - d, y + d
            if x in Uset and z in Uset:
                if not (x in preset and y in preset and z in preset):
                    enc.add(-enc.before(x, y), -enc.before(y, z))
                    enc.add(-enc.before(z, y), -enc.before(y, x))
            d += 1
    return enc.solve()


def team_below(M):
    """team values in [1, M/2] for team owning (M, 2M] (== zone_full)."""
    return sorted(zone_full(M))


def defect_of_block(lo, hi):
    """defect class of block (lo, hi]: v == 2 mod 2^{k//2}, k = log2(hi)."""
    k = hi.bit_length() - 1
    m = 2 ** (k // 2)
    return set(v for v in range(lo + 1, hi + 1) if v % m == 2), m


def part1b():
    print("=" * 72)
    print("PART 1b: era semantics — zone missing its own defect D_Z,")
    print("         D_Z released among the block era")
    for M in [16, 32, 64, 128]:
        B = set(range(M + 1, 2 * M + 1))
        DB, mB = defect_of_block(M, 2 * M)
        DZ, mZ = defect_of_block(M // 4, M // 2)
        below = team_below(M)
        P0 = [v for v in below if v not in DZ]
        print(f"\nM={M}: D_B(mod {mB})={sorted(DB)}  D_Z(mod {mZ})={sorted(DZ)}")
        cases = [
            ("A: P0 full-zone,  era1 = B          (fatal zone)",
             list(below), [sorted(B)]),
            ("B: P0 full-zone,  era1 = B\\D_B      (part-1 semantics)",
             list(below), [sorted(B - DB)]),
            ("C: P0 zone\\D_Z,   era1 = D_Z ∪ B\\D_B (ladder era)",
             P0, [sorted(set(DZ) | (B - DB))]),
            ("D: P0 zone\\D_Z,   era1 = D_Z ∪ B     (no block defect)",
             P0, [sorted(set(DZ) | B)]),
            ("E: P0 zone\\D_Z,   era1 = B\\D_B      (D_Z never released)",
             P0, [sorted(B - DB)]),
        ]
        for name, pre, stages in cases:
            t0 = time.time()
            r = stage_system(stages, pre)
            print(f"  {name}: {'SAT' if r is not False else 'UNSAT'} ({time.time()-t0:.1f}s)")


def part1c_controls(M=32, trials=10):
    print("=" * 72)
    print(f"PART 1c: controls in era semantics at M={M} (case C skeleton)")
    B = set(range(M + 1, 2 * M + 1))
    DB, mB = defect_of_block(M, 2 * M)
    DZ, mZ = defect_of_block(M // 4, M // 2)
    below = team_below(M)
    Zblk = [v for v in below if M // 4 < v <= M // 2]

    def run(DZv, DBv, name):
        P0 = [v for v in below if v not in DZv]
        r = stage_system([sorted(set(DZv) | (B - set(DBv)))], P0)
        print(f"  {name}: {'SAT' if r is not False else 'UNSAT'}")

    run(DZ, DB, f"law D_Z={sorted(DZ)}, D_B={sorted(DB)}")
    # vary D_B class, keep law D_Z
    for mod in [4, 8, 16]:
        for res in [1, 2, 6]:
            if res >= mod: continue
            Dv = set(v for v in B if v % mod == res)
            if set(Dv) == DB: continue
            run(DZ, Dv, f"law D_Z, D_B == {res} mod {mod} ({len(Dv)} vals)")
    # vary D_Z class, keep law D_B
    for mod in [4, 8]:
        for res in [1, 2, 3]:
            if res >= mod and mod != 4: continue
            Dv = set(v for v in Zblk if v % mod == res)
            if Dv == DZ or not Dv: continue
            run(Dv, DB, f"D_Z == {res} mod {mod} ({sorted(Dv)}), law D_B")
    # random controls, same cardinalities
    rng = random.Random(42)
    satc = 0
    for t in range(trials):
        DZv = set(rng.sample(Zblk, len(DZ)))
        DBv = set(rng.sample(sorted(B), len(DB)))
        P0 = [v for v in below if v not in DZv]
        r = stage_system([sorted(DZv | (B - DBv))], P0)
        satc += (r is not False)
    print(f"  random (|D_Z|,|D_B|) removals: {satc}/{trials} SAT")
    # random D_B only, law D_Z
    satc = 0
    for t in range(trials):
        DBv = set(rng.sample(sorted(B), len(DB)))
        P0 = [v for v in below if v not in DZ]
        r = stage_system([sorted(set(DZ) | (B - DBv))], P0)
        satc += (r is not False)
    print(f"  law D_Z + random D_B: {satc}/{trials} SAT")


def part4_chain(M):
    print("=" * 72)
    print(f"PART 4: two-era chain (D_B released in next era), M={M}")
    B = set(range(M + 1, 2 * M + 1))
    B2 = set(range(4 * M + 1, 8 * M + 1))
    DB, _ = defect_of_block(M, 2 * M)
    DB2, _ = defect_of_block(4 * M, 8 * M)
    DZ, _ = defect_of_block(M // 4, M // 2)
    below = team_below(M)
    P0 = [v for v in below if v not in DZ]
    era1 = sorted(set(DZ) | (B - DB))
    era2 = sorted(DB | (B2 - DB2))
    t0 = time.time()
    r = stage_system([era1, era2], P0)
    print(f"  [P0 | era1 | era2] chain: {'SAT' if r is not False else 'UNSAT'}"
          f" ({time.time()-t0:.1f}s)  (n={len(P0)+len(era1)+len(era2)})")
    if r is not False:
        # sanity: check stagewise structure and report era2 position of D_B
        pos = {v: i for i, v in enumerate(r)}
        assert all(pos[u] < pos[w] for u in P0 for w in era1)
        assert all(pos[u] < pos[w] for u in era1 for w in era2)
        print(f"  era2 order: {[v for v in r if v in set(era2)]}")
    return r


if __name__ == "__main__2":
    pass
