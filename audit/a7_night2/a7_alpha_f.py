#!/usr/bin/env python3
"""a7 audit: INDEPENDENT computation of the notes/57 catalogue
quantities alpha_c(M), f_c(M) and the mechanistic K* prediction

    K*(M) = m + 9 + max(alpha_E - f_O, alpha_O - f_E),   m = M/2,

implemented from the notes/57 SS0.2/SS3 DEFINITIONS alone (no code
shared with experiments/e153_dich_lemmas.py).  No SAT solver is used.

Definitions implemented:
  * block-2 pattern: catalogue entry with blk == 2; attackers =
    S cap P1 (asserted to have size 2), support = S cap P2.
  * dead-pure pair {x, x'} (same-parity, class c): some pattern with
    attacker set {x, x'} whose support lies entirely in class c.
  * alpha_c: maximum subset of the class-c band values with offset
    in [-(M-1), 0] (values in [3M+1, 4M]) containing no dead-pure
    pair (max clique of the alive graph; exact branch-and-bound).
  * f_c: 8 iff the bottom singleton z0 ({4M+1} for O, {4M+2} for E)
    is SELF-SERVING: for every dead-pure class-c pair inside
    I(z0) cap c, EVERY pure pattern of that pair contains z0 in its
    support (admissibility under fan-cleanness: a pure pattern whose
    support misses the defector set would be monochromatic).
    Else f_c = 9.  I(4M+1) = [3M-15, 3M], I(4M+2) = [3M-15, 3M+1]
    (Lemma FI(i), independently re-verified in a7_hand_checks A).

Usage: a7_alpha_f.py M [M ...]   (reads data/e146_catalogue_M{M}.json)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data')


def max_clique(verts, alive):
    """Exact max clique of graph (verts, alive-edge set) by
    branch and bound; alive = set of frozensets."""
    verts = list(verts)
    best = [0, []]

    def grow(clique, cands):
        if len(clique) + len(cands) <= best[0]:
            return
        if not cands:
            if len(clique) > best[0]:
                best[0], best[1] = len(clique), list(clique)
            return
        v = cands[0]
        rest = cands[1:]
        # include v
        grow(clique + [v],
             [w for w in rest if frozenset((v, w)) in alive])
        # exclude v
        grow(clique, rest)

    grow([], verts)
    return best[0], sorted(best[1])


def analyze(M):
    m = M // 2
    path = os.path.join(DATA, f'e146_catalogue_M{M}.json')
    cat = json.load(open(path))
    P1lo, P1hi = 3 * M - 15, 4 * M
    P2lo, P2hi = 4 * M + 1, 6 * M + 15

    # dead-pure pair map: frozenset({x,x'}) -> list of pure supports;
    # and dead map (any-pattern) for the shape assertion
    pure_supports = {}
    n_blk2 = 0
    for pat in cat:
        if pat['blk'] != 2:
            continue
        n_blk2 += 1
        att = [v for v in pat['S'] if P1lo <= v <= P1hi]
        sup = [v for v in pat['S'] if P2lo <= v <= P2hi]
        assert len(att) == 2, (M, pat)
        assert len(att) + len(sup) == len(pat['S']), (M, pat)
        x1, x2 = att
        if (x1 - x2) % 2 != 0:
            continue  # cross-parity attacker pair: never pure-relevant
        c = x1 % 2
        if all(v % 2 == c for v in sup):
            pure_supports.setdefault(frozenset(att), []).append(
                frozenset(sup))

    # ---- alpha_c: shallow-zone alive cliques --------------------
    alpha = {}
    wit = {}
    for c, name in ((0, 'E'), (1, 'O')):
        zone = [v for v in range(3 * M + 1, 4 * M + 1) if v % 2 == c]
        dead = set(k for k in pure_supports
                   if all(v in zone for v in k))
        # alive edge set on the zone
        alive = set()
        for i, u in enumerate(zone):
            for w in zone[i + 1:]:
                if frozenset((u, w)) not in pure_supports:
                    alive.add(frozenset((u, w)))
        alpha[name], wit[name] = max_clique(zone, alive)

    # ---- f_c: bottom-singleton self-service ---------------------
    f = {}
    fail_ex = {}
    for c, name, z0, itop in ((1, 'O', 4 * M + 1, 3 * M),
                              (0, 'E', 4 * M + 2, 3 * M + 1)):
        I = [v for v in range(3 * M - 15, itop + 1) if v % 2 == c]
        selfserv = True
        for i, y1 in enumerate(I):
            for y2 in I[i + 1:]:
                key = frozenset((y1, y2))
                if key not in pure_supports:
                    continue
                for sup in pure_supports[key]:
                    if z0 not in sup:
                        selfserv = False
                        if name not in fail_ex:
                            fail_ex[name] = (y1 - 4 * M, y2 - 4 * M,
                                             sorted(v - 4 * M
                                                    for v in sup))
        f[name] = 8 if selfserv else 9

    kstar = m + 9 + max(alpha['E'] - f['O'], alpha['O'] - f['E'])
    return dict(M=M, n_blk2=n_blk2, alpha_E=alpha['E'],
                alpha_O=alpha['O'],
                wit_E=[v - 4 * M for v in wit['E']],
                wit_O=[v - 4 * M for v in wit['O']],
                f_O=f['O'], f_E=f['E'],
                fail_O=fail_ex.get('O'), fail_E=fail_ex.get('E'),
                K_star_pred=kstar)


def main():
    for M in [int(a) for a in sys.argv[1:]]:
        r = analyze(M)
        print(f"M={r['M']}: blk2={r['n_blk2']}  "
              f"alpha_E={r['alpha_E']} (wit {r['wit_E']})  "
              f"alpha_O={r['alpha_O']} (wit {r['wit_O']})  "
              f"f_O={r['f_O']} f_E={r['f_E']}  "
              f"K*pred={r['K_star_pred']}", flush=True)
        if r['fail_O']:
            print(f"   f_O failure exemplar: pair offs "
                  f"({r['fail_O'][0]},{r['fail_O'][1]}) pure support "
                  f"offs {r['fail_O'][2]}", flush=True)
        if r['fail_E']:
            print(f"   f_E failure exemplar: pair offs "
                  f"({r['fail_E'][0]},{r['fail_E'][1]}) pure support "
                  f"offs {r['fail_E'][2]}", flush=True)


if __name__ == '__main__':
    main()
