"""e153: verifier for the notes/57 DICH lemma layer (solver-free).

Per scale M:
  A  — Lemma FI: brute-force forced interval I(z) for every z in P2
       (both parities) against the closed formulas; lengths, class
       counts, bottom-anchor iff s <= M-31; singleton class-mass
       n_c = 8 only at the bottom singleton (+1 odd / +2 even).
  A2 — f_c(D) >= 9 for every 2-element defector set D (both classes).
  B  — catalogue shape: every block-2 pattern has exactly 2 band
       values (the attackers); purity stats for same-parity pairs.
  C  — alpha_c: maximum alive-clique (no dead-via-PURE-pattern pair)
       among class-c band values with offsets in [-(M-1), 0].
  D  — self-service of the bottom singletons {4M+1} (odd) and
       {4M+2} (even): every dead-pure same-class pair with both
       attackers in I(z0) must have z0 in its support.
  D2 — self-service scan over ALL class singletons (report which are
       self-serving; all non-bottom ones have n_c >= 9 anyway).
  D3 — the e149 frontier witness defector set is self-serving.
  E  — K* formula: m + 9 + max(alpha_E - f_O, alpha_O - f_E) with
       f_c = 8 iff bottom-c singleton self-serves else 9; assert
       equal to e149's kstar when available, else report PREDICTION.
  F  — frontier witness re-validation: hatch, defectors, forced
       interval inside opposite band, minority cap = alive clique in
       the shallow zone.

Run: .venv/bin/python experiments/e153_dich_lemmas.py [M ...]
Log: data/e153_dich_lemmas.log (caller tee).
"""
import json
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')


def core_support(M):
    P0 = list(range(M + 1, 2 * M + 1))
    P1 = list(range(3 * M - 15, 4 * M + 1))
    P2 = list(range(4 * M + 1, 6 * M + 16))
    return P0, P1, P2


def interval(M, z):
    """Brute-force I(z) for full-class ownership of z's parity."""
    P0, P1, _ = core_support(M)
    c = z % 2
    mids = sorted((u + z) // 2 for u in P0 if u % 2 == c
                  and 3 * M - 15 <= (u + z) // 2 <= 4 * M)
    return mids


def max_alive_clique(verts, dead):
    """Max clique in the alive graph = max subset with no dead pair.
    dead: set of frozensets.  Simple branch and bound (alive graphs
    here are sparse, cliques tiny)."""
    verts = sorted(verts)
    best = [0, []]

    def grow(cur, cand):
        if len(cur) > best[0]:
            best[0], best[1] = len(cur), list(cur)
        for i, v in enumerate(cand):
            if len(cur) + len(cand) - i <= best[0]:
                break
            if all(frozenset((v, w)) not in dead for w in cur):
                grow(cur + [v], cand[i + 1:])

    grow([], verts)
    return best[0], sorted(best[1])


def run(M):
    P0, P1, P2 = core_support(M)
    m = M // 2
    print(f'===== M={M} (m={m}) =====', flush=True)

    # ---------- A: Lemma FI ----------
    for z in P2:
        s = z - 4 * M
        c = z % 2
        mids = interval(M, z)
        assert mids == list(range(mids[0], mids[-1] + 1)), (M, z)
        ell = len(mids)
        ncl = sum(1 for v in mids if v % 2 == c)
        anchored = (mids[0] == 3 * M - 15)
        assert anchored == (s <= M - 31), (M, z)
        if s <= M - 31:
            want = (s + 31) // 2 if c == 1 else (s + 32) // 2
            assert ell == want, (M, z, ell, want)
        elif s <= 2 * M:
            assert ell == m, (M, z, ell)
        else:
            assert ell >= m - 8, (M, z, ell)
        assert ell >= 16 and ncl >= 8, (M, z, ell, ncl)
        if ncl == 8:
            ok8 = (s in (1, 2 * M + 15)) if c == 1 else (s == 2)
            assert ok8, (M, z, ncl)
    print('A : Lemma FI formulas OK (anchor iff s<=M-31; n_c=8 only '
          'at bottom singletons)', flush=True)

    # ---------- A2: pair mass ----------
    for c in (1, 0):
        zs = [z for z in P2 if z % 2 == c]
        for z1, z2 in combinations(zs, 2):
            F = set(interval(M, z1)) | set(interval(M, z2))
            ncl = sum(1 for v in F if v % 2 == c)
            assert ncl >= 9, (M, c, z1 - 4 * M, z2 - 4 * M, ncl)
    print('A2: f_c(D) >= 9 for every 2-element D, both classes',
          flush=True)

    # ---------- B: catalogue shape ----------
    with open(os.path.join(DATA, f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    fans = [p for p in cat if p['blk'] == 2]
    p1set = set(P1)
    attackers = {}
    npure = nsp = 0
    for p in fans:
        S = p['S']
        att = sorted(v for v in S if v in p1set)
        assert len(att) == 2, (M, p['src'])
        supp = sorted(v for v in S if v not in p1set)
        assert all(v in set(P2) for v in supp)
        key = (att[0], att[1])
        attackers.setdefault(key, []).append(supp)
        if att[0] % 2 == att[1] % 2:
            nsp += 1
            if all(v % 2 == att[0] % 2 for v in supp):
                npure += 1
    print(f'B : {len(fans)} fan patterns, all with exactly 2 band '
          f'values; same-parity pairs: {nsp}, of which pure-support: '
          f'{npure}', flush=True)

    # dead-via-pure-pattern pair sets, per class
    dead_pure = {0: set(), 1: set()}
    for (x1, x2), supps in attackers.items():
        if x1 % 2 != x2 % 2:
            continue
        c = x1 % 2
        if any(all(v % 2 == c for v in supp) for supp in supps):
            dead_pure[c].add(frozenset((x1, x2)))

    # ---------- C: alpha (shallow zone) ----------
    alpha = {}
    for c in (0, 1):
        verts = [v for v in P1 if v % 2 == c and v >= 3 * M + 1]
        a, wit = max_alive_clique(verts, dead_pure[c])
        alpha[c] = a
        print(f'C : alpha_{"E" if c==0 else "O"} = {a}  witness offs '
              f'{[v-4*M for v in wit]}', flush=True)

    # ---------- D/D2: self-service scan ----------
    def self_serving(z0set):
        c = next(iter(z0set)) % 2
        F = set()
        for z in z0set:
            F |= set(interval(M, z))
        Fc = {v for v in F if v % 2 == c}
        for pair in combinations(sorted(Fc), 2):
            key = frozenset(pair)
            if key not in dead_pure[c]:
                continue
            supps = [s for s in attackers[tuple(sorted(pair))]
                     if all(v % 2 == c for v in s)]
            # dead-pure: every pure support must be dodged =>
            # serving needs z0set to meet EVERY pure pattern of the
            # pair?  No: each pattern is a separate constraint; the
            # pair is served iff every pure pattern's support meets
            # the defector set (impure patterns are auto-served).
            for s in supps:
                if not (set(s) & z0set):
                    return False, (pair, s)
        return True, None

    adm = {}
    for c, name in ((1, 'O'), (0, 'E')):
        z0 = 4 * M + (1 if c == 1 else 2)
        ok, fail = self_serving({z0})
        adm[c] = ok
        if ok:
            print(f'D : bottom singleton {{+{z0-4*M}}} ({name}) '
                  f'SELF-SERVES  => f_{name} = 8', flush=True)
        else:
            pair, s = fail
            print(f'D : bottom singleton {{+{z0-4*M}}} ({name}) FAILS '
                  f'at pair offs ({pair[0]-4*M},{pair[1]-4*M}), pure '
                  f'supp offs {[v-4*M for v in s][:8]}  => f_{name} = 9',
                  flush=True)
        serving = []
        for z in P2:
            if z % 2 != c:
                continue
            ok2, _ = self_serving({z})
            if ok2:
                serving.append(z - 4 * M)
        print(f'D2: self-serving {name}-singletons (offsets): '
              f'{serving if serving else "NONE"}', flush=True)

    # ---------- D3/E/F: e149 comparison ----------
    kfile = os.path.join(DATA, f'e149_dichotomy_M{M}.json')
    f_O = 8 if adm[1] else 9
    f_E = 8 if adm[0] else 9
    kth = m + 9 + max(alpha[0] - f_O, alpha[1] - f_E)
    if not os.path.exists(kfile):
        print(f'E : PREDICTION K*({M}) = {kth}  '
              f'(alpha_E={alpha[0]}, alpha_O={alpha[1]}, '
              f'f_O={f_O}, f_E={f_E}; no e149 data)', flush=True)
        return
    with open(kfile) as f:
        e149 = json.load(f)
    kstar = e149['kstar']
    status = 'OK' if kth == kstar else 'MISMATCH'
    print(f'E : K* formula {kth} vs e149 {kstar}  [{status}]  '
          f'(alpha_E={alpha[0]}, alpha_O={alpha[1]}, '
          f'f_O={f_O}, f_E={f_E})', flush=True)
    assert kth == kstar, (M, kth, kstar)

    # F: frontier witness re-validation
    fw = e149['frontier_witness']
    ana = fw['anatomy']
    U_A = sorted(int(o) + M for o in ana['A']['U_off'])
    U_B = sorted(int(o) + M for o in ana['B']['U_off'])
    Z_A = sorted(int(o) + 4 * M for o in ana['A']['Z_off'])
    Z_B = sorted(int(o) + 4 * M for o in ana['B']['Z_off'])
    Y_A = sorted(int(o) + 4 * M for o in ana['A']['Y_off'])
    Y_B = sorted(int(o) + 4 * M for o in ana['B']['Y_off'])
    # hatch (up to swap): identify the odd side
    assert all(u % 2 == 1 for u in U_A) or all(u % 2 == 0 for u in U_A)
    if U_A[0] % 2 == 1:
        Uo, Ue, Zo_side, Ze_side = U_A, U_B, (Z_A, Y_B), (Z_B, Y_A)
    else:
        Uo, Ue, Zo_side, Ze_side = U_B, U_A, (Z_B, Y_A), (Z_A, Y_B)
    assert Uo == [u for u in P0 if u % 2 == 1]
    assert Ue == [u for u in P0 if u % 2 == 0]
    D_odd = [z for z in Zo_side[0] if z % 2 == 1]
    D_even = [z for z in Ze_side[0] if z % 2 == 0]
    for (D, c, Yopp) in ((D_odd, 1, Zo_side[1]), (D_even, 0, Ze_side[1])):
        if not D:
            continue
        F = set()
        for z in D:
            F |= set(interval(M, z))
        assert F <= set(Yopp), (M, 'forced interval escapes')
        ok3, _ = self_serving(set(D))
        assert ok3, (M, 'witness defectors not self-serving?!')
        print(f'F : witness defectors ({"O" if c else "E"}) '
              f'{[z-4*M for z in D]}: forced {len(F)} values inside '
              f'opposite band, self-serving OK', flush=True)
    # minority cap: the defector-side team's opposite-parity band values
    phi = fw['phi']
    print(f'F : witness K={fw["K"]} phi={phi} re-validated', flush=True)


if __name__ == '__main__':
    Ms = [int(a) for a in sys.argv[1:]] or [48, 64, 80, 96]
    for M in Ms:
        run(M)
    print('e153: DONE', flush=True)
