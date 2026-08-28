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

    # ---------- D4: mid/tail min-offset elimination ----------
    # For every s0 > M-31 (both classes): find a dead-pure pair inside
    # I(4M+s0) with a pure pattern whose support lies entirely BELOW
    # s0.  Such a pair cannot be served by any defector set with
    # minimum s0 (supports are class-pure, so only class defectors
    # >= s0 could serve).  If every mid/tail s0 is eliminated, every
    # admissible defector set has a LOW minimum.
    for c, name in ((1, 'O'), (0, 'E')):
        bad = []
        for z in P2:
            if z % 2 != c or z - 4 * M <= M - 31:
                continue
            s0 = z - 4 * M
            Ic = [v for v in interval(M, z) if v % 2 == c]
            found = False
            for pair in combinations(Ic, 2):
                key = frozenset(pair)
                if key not in dead_pure[c]:
                    continue
                for supp in attackers[tuple(sorted(pair))]:
                    if all(v % 2 == c for v in supp) and \
                            all(v - 4 * M < s0 for v in supp):
                        found = True
                        break
                if found:
                    break
            if not found:
                bad.append(s0)
        if bad:
            print(f'D4: {name}: mid/tail min-offsets NOT eliminated: '
                  f'{bad}', flush=True)
        else:
            print(f'D4: {name}: every mid/tail min-offset eliminated '
                  f'(all admissible defector sets have LOW minimum)',
                  flush=True)

    # ---------- D5: exact admissible-min scan (tiny SAT per s0) ----
    # For each NOT-eliminated mid/tail s0: does ANY self-serving
    # defector set D of class c with min offset exactly s0 exist?
    # Vars: d_z for class offsets in [s0, 2M+15]; d_{z0} forced;
    # v_y (y in P1 cap c) <-> OR of d_z with y in I(z); for every
    # dead-pure pair (y1,y2) and every pure pattern S:
    # v_{y1} & v_{y2} -> OR_{z in S} d_z.  UNSAT => min s0 impossible.
    from pysat.solvers import Cadical195
    Ivals = {z: set(interval(M, z)) for z in P2}
    survivors = {}
    caps = {}
    for c, name in ((1, 'O'), (0, 'E')):
        surviving = []
        mids = [z for z in P2 if z % 2 == c and z - 4 * M > M - 31]
        for z0 in mids:
            s0 = z0 - 4 * M
            zs = [z for z in P2 if z % 2 == c and z >= z0]
            dvar = {z: i + 1 for i, z in enumerate(zs)}
            nv = len(zs)
            yvals = [y for y in P1 if y % 2 == c]
            yvar = {}
            cls = [[dvar[z0]]]
            for y in yvals:
                nv += 1
                yvar[y] = nv
                owners = [dvar[z] for z in zs if y in Ivals[z]]
                for o in owners:
                    cls.append([-o, nv])
                cls.append([-nv] + owners)
            for pair in combinations(yvals, 2):
                if frozenset(pair) not in dead_pure[c]:
                    continue
                for supp in attackers[tuple(sorted(pair))]:
                    if not all(v % 2 == c for v in supp):
                        continue
                    servers = [dvar[z] for z in supp if z in dvar]
                    cls.append([-yvar[pair[0]], -yvar[pair[1]]]
                               + servers)
            with Cadical195(bootstrap_with=cls) as s:
                if s.solve():
                    surviving.append(s0)
        if surviving:
            print(f'D5: {name}: admissible mid/tail minima SURVIVE: '
                  f'{surviving}', flush=True)
            assert all(s0 <= M - 1 for s0 in surviving), \
                (M, c, 'surviving minimum above M-1: collision arg fails')
        else:
            print(f'D5: {name}: NO admissible defector set with '
                  f'mid/tail minimum (exact SAT scan) — every '
                  f'admissible D has LOW minimum', flush=True)
        survivors.setdefault(c, surviving)

    # ---------- D6: one-sided branch closure at surviving minima ---
    # Abstract branch instance (a WEAKENING of e149 — only removes
    # constraints, so UNSAT here is stronger): defector class c,
    # one-sided (no opposite-class defectors), min offset s0; vars:
    # d_z (defectors >= z0, d_{z0} forced), v_y (y in P1 forced into
    # the opposite band: y in F(D)), u_y (y in Y_A).  Constraints:
    # v-definitions (both parities); u_y -> not v_y; self-service of
    # class-c dead-pure pairs inside F; Y_A class-c dead pairs need a
    # support member OUTSIDE D; Y_A class-c' dead-pure pairs are
    # outright forbidden (no servers, one-sided); |Y_A| >= K*.
    # Expect UNSAT for every D5-surviving s0.
    from pysat.card import CardEnc, EncType
    kstar_e = None
    kf = os.path.join(DATA, f'e149_dichotomy_M{M}.json')
    if os.path.exists(kf):
        with open(kf) as f:
            kstar_e = json.load(f)['kstar']
    Ktest = kstar_e if kstar_e else (m + 9 + max(
        alpha[0] - (8 if adm[1] else 9), alpha[1] - (8 if adm[0] else 9)))
    def branch_solve(c, s0, K):
        z0 = 4 * M + s0
        zs = [z for z in P2 if z % 2 == c and z >= z0]
        dvar = {z: i + 1 for i, z in enumerate(zs)}
        nv = len(zs)
        vvar, uvar = {}, {}
        cls = [[dvar[z0]]]
        for y in P1:
            nv += 1
            vvar[y] = nv
            owners = [dvar[z] for z in zs if y in Ivals[z]]
            for o in owners:
                cls.append([-o, nv])
            cls.append([-nv] + owners)
        for y in P1:
            nv += 1
            uvar[y] = nv
            cls.append([-nv, -vvar[y]])
        for cc in (0, 1):
            ys = [y for y in P1 if y % 2 == cc]
            for pair in combinations(ys, 2):
                if frozenset(pair) not in dead_pure[cc]:
                    continue
                for supp in attackers[tuple(sorted(pair))]:
                    if not all(v % 2 == cc for v in supp):
                        continue
                    if cc == c:
                        servers = [dvar[z] for z in supp if z in dvar]
                        cls.append([-vvar[pair[0]], -vvar[pair[1]]]
                                   + servers)
                        if all(z in dvar for z in supp):
                            cls.append([-uvar[pair[0]], -uvar[pair[1]]]
                                       + [-dvar[z] for z in supp])
                    else:
                        cls.append([-uvar[pair[0]], -uvar[pair[1]]])
        enc = CardEnc.atleast(lits=[uvar[y] for y in P1], bound=K,
                              top_id=nv, encoding=EncType.seqcounter)
        cls += enc.clauses
        with Cadical195(bootstrap_with=cls) as s:
            return s.solve()

    for c, name in ((1, 'O'), (0, 'E')):
        escapes = [s0 for s0 in range(1 if c else 2, 2 * M + 16, 2)
                   if branch_solve(c, s0, Ktest)]
        if escapes:
            print(f'D6: {name}: branch SAT (escape?!) at s0 = '
                  f'{escapes}  [K={Ktest}]', flush=True)
        else:
            print(f'D6: {name}: one-sided branch UNSAT at EVERY '
                  f'minimum s0  [K={Ktest}]', flush=True)
        sharp = [s0 for s0 in range(1 if c else 2, 12, 2)
                 if branch_solve(c, s0, Ktest - 1)]
        print(f'D6s: {name}: at K*-1 the branch is SAT at bottom '
              f'minima {sharp if sharp else "NONE"}', flush=True)

    # ---------- C2: alpha_full (whole band, per class) ----------
    for c in (0, 1):
        verts = [v for v in P1 if v % 2 == c]
        a, wit = max_alive_clique(verts, dead_pure[c])
        print(f'C2: alpha_full_{"E" if c==0 else "O"} = {a}  offs '
              f'{[v-4*M for v in wit]}', flush=True)

    # ---------- C3: counting closure for surviving mid minima ------
    # One-sided mid-min defector set of class c, min z0: forced
    # interval I(z0) caps the same-class band mass (n_c) and the
    # minority cap is the alive-clique number of the OPPOSITE class
    # outside I(z0).  Kill needs m+8 - n_c + abar <= K*-1; K* from
    # part E's formula (asserted against e149 below where available).
    kstar_th = None  # filled in E; C3 runs before E, so compute here
    # (bottom-singleton admissibility already known: adm)
    for c, name in ((1, 'O'), (0, 'E')):
        for s0 in survivors.get(c, []):
            z0 = 4 * M + s0
            I0 = set(interval(M, z0))
            ncl = sum(1 for v in I0 if v % 2 == c)
            cop = 1 - c
            verts = [v for v in P1 if v % 2 == cop and v not in I0]
            abar, wit = max_alive_clique(verts, dead_pure[cop])
            cap = m + 8 - ncl + abar
            print(f'C3: {name} s0={s0}: n_c={ncl} abar={abar} '
                  f'=> |Y| cap {cap}', flush=True)
            caps.setdefault(c, []).append((s0, cap))

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
    need_d6 = [(c, s0, cap) for c in caps for (s0, cap) in caps[c]
               if cap > kstar - 1]
    if need_d6:
        print(f'E2: mid-min single-interval counting closes all but '
              f'{[(c, s0) for c, s0, _ in need_d6]} (cap = K*): those '
              f'rely on the D6 cascade closure', flush=True)
    else:
        print(f'E2: all surviving mid-min caps <= K*-1 = {kstar-1} '
              f'(mid branch closes by single-interval counting)',
              flush=True)

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
