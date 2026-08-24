"""e52c — the corrected subset-escape: DEFERRABLE-SUFFIX classes.
State V = team ∩ [1,2M] (team owning (M,2M]).  Question: which thin classes
C ⊆ (M,2M] admit an AP-free arrangement of V with C as a suffix?
(This is the exact content of the defect law at a completeness boundary:
the withheld class is released after everything else of the state.)
Nested version: [bulk | D_{M/2} | D_{2M}] (defects stack in scale order).
Witness-dependence: is D appendable after ANY valid bulk arrangement?"""
import sys, random, time
sys.path.insert(0, '/Users/will/Dev/personal/tasks/math/erdos197/experiments')
from e3_sat import OrderSAT
from e52_subset_escape import defect_of_block, team_below, stage_system


def team_upto(M):
    """team values in [1, 2M] for the team owning (M,2M]."""
    return sorted(set(team_below(M)) | set(range(M + 1, 2 * M + 1)))


def suffix_sat(V, stages_tail):
    """stages: [V minus tail | tail stages...]; all APs enforced, no pre."""
    tail = set()
    for s in stages_tail:
        tail |= set(s)
    bulk = sorted(set(V) - tail)
    return stage_system(list(stages_tail), [], ) if False else \
        stage_system([bulk] + [sorted(s) for s in stages_tail], [])


def runA(M):
    V = team_upto(M)
    B = set(range(M + 1, 2 * M + 1))
    D, m = defect_of_block(M, 2 * M)
    print(f"\nM={M}: V=team∩[1,{2*M}] (n={len(V)}), D=≡2 mod {m} = {sorted(D)}")
    cands = [("law D (≡2 mod %d)" % m, D)]
    if m >= 4:
        cands.append(("≡6 mod %d" % m, set(v for v in B if v % m == 6 % m and v not in D)))
    cands.append(("≡1 mod %d" % m, set(v for v in B if v % m == 1)))
    cands.append(("≡2 mod %d (half of D)" % (2 * m), set(v for v in B if v % (2 * m) == 2)))
    cands.append(("≡%d mod %d" % (m + 2, 2 * m), set(v for v in B if v % (2 * m) == m + 2)))
    for name, C in cands:
        if not C:
            continue
        t0 = time.time()
        r = suffix_sat(V, [C])
        print(f"  suffix {name} ({len(C)} vals): {'SAT' if r is not False else 'UNSAT'} ({time.time()-t0:.1f}s)", flush=True)
    rng = random.Random(11)
    sat = 0
    for t in range(10):
        C = set(rng.sample(sorted(B), len(D)))
        if suffix_sat(V, [C]) is not False:
            sat += 1
    print(f"  suffix random |D|-subsets of B: {sat}/10 SAT", flush=True)
    two_odd = [v for v in B if v % 4 == 2]
    sat = 0
    for t in range(10):
        C = set(rng.sample(two_odd, min(len(D), len(two_odd))))
        if suffix_sat(V, [C]) is not False:
            sat += 1
    print(f"  suffix random 2·odd subsets: {sat}/10 SAT", flush=True)


def runB(M):
    V = team_upto(M)
    DB, mB = defect_of_block(M, 2 * M)
    DZ, mZ = defect_of_block(M // 4, M // 2)
    t0 = time.time()
    r1 = suffix_sat(V, [DZ, DB])
    print(f"M={M} nested [bulk | D_Z | D_B]: {'SAT' if r1 is not False else 'UNSAT'} ({time.time()-t0:.1f}s)", flush=True)
    t0 = time.time()
    r2 = suffix_sat(V, [DB, DZ])
    print(f"M={M} nested [bulk | D_B | D_Z] (control): {'SAT' if r2 is not False else 'UNSAT'} ({time.time()-t0:.1f}s)", flush=True)
    if r1 is not False:
        print(f"  witness: {r1}")


def runD(M, trials=5):
    """witness-dependence: random AP-free arrangements of V∖D, then try
    appending D as a suffix (D internal order free)."""
    V = team_upto(M)
    D, m = defect_of_block(M, 2 * M)
    bulk = sorted(set(V) - D)
    rng = random.Random(3)
    ok = 0
    tried = 0
    for t in range(trials * 4):
        if tried >= trials:
            break
        # random witness of bulk (APs only)
        enc = OrderSAT(bulk)
        bs = set(bulk)
        for y in bulk:
            d = 1
            while y + d <= bulk[-1]:
                x, z = y - d, y + d
                if x in bs and z in bs:
                    enc.add(-enc.before(x, y), -enc.before(y, z))
                    enc.add(-enc.before(z, y), -enc.before(y, x))
                d += 1
        pairs = [(a, b) for i, a in enumerate(bulk) for b in bulk[i + 1:]]
        rng.shuffle(pairs)
        for (a, b) in pairs[:8]:
            enc.add(enc.before(a, b) if rng.random() < .5 else enc.before(b, a))
        sigma = enc.solve()
        if sigma is False:
            continue
        tried += 1
        # append D after fixed sigma
        r = stage_system([sorted(D)], list(sigma))
        ok += (r is not False)
    print(f"M={M}: D appendable after random bulk witnesses: {ok}/{tried}", flush=True)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "A"):
        print("=" * 72)
        print("RUN A: which thin classes are deferrable suffixes of the state?")
        for M in [16, 32, 64, 128]:
            runA(M)
    if which in ("all", "B"):
        print("=" * 72)
        print("RUN B: nested defect suffixes [bulk | D_Z | D_B]")
        for M in [32, 64, 128]:
            runB(M)
    if which in ("all", "D"):
        print("=" * 72)
        print("RUN D: witness-dependence of D-appendability")
        for M in [16, 32, 64]:
            runD(M)
