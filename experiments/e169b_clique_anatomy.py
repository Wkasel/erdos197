"""e169b: anatomy of ALL 4-cliques (and max 3-cliques) of the
SAT-alive graphs stored by e169 (notes/66 SS6).

For each (m, window): enumerate EVERY 4-clique of the SAT-alive
pair graph; report count, spans, and whether each contains a
sub-shallow member (attacker value <= 3m, i.e. pi = 4m - x >= m,
outside alpha's shallow zone [3m+1, 4m]).  The machine statement
under test (ANCHOR-4): every SAT-alive 4-clique has a sub-shallow
member — equivalently the SHALLOW clique number is <= 3, i.e.
alpha-hat(2m) <= 3.

Run: python3 experiments/e169b_clique_anatomy.py
Reads: data/e169_alive_lattice.json
"""
import json
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'e169_alive_lattice.json')


def main():
    with open(OUT) as f:
        store = json.load(f)
    scans = store.get('scan', {})
    print(f'{"m":>4} {"win":>4} {"#SAT-alive":>10} {"#4cl":>5} '
          f'{"all-anchored":>12} {"min-span":>8} {"spans":>20}')
    ok_all = True
    for ms in sorted(scans, key=int):
        m = int(ms)
        for name in ('W2e', 'W2o'):
            r = scans[ms][name]
            edges = set(map(tuple, r['sat_alive']))
            verts = sorted({v for e in edges for v in e})
            adj = {v: set() for v in verts}
            for (a, b) in edges:
                adj[a].add(b)
                adj[b].add(a)
            cliques4 = []
            for (a, b) in sorted(edges):
                common = adj[a] & adj[b]
                for c, d in combinations(sorted(x for x in common
                                                if x > b), 2):
                    if d in adj[c]:
                        cliques4.append((a, b, c, d))
            anchored = [q for q in cliques4 if q[0] <= 3 * m]
            spans = sorted({q[3] - q[0] for q in cliques4})
            allanch = (len(anchored) == len(cliques4))
            ok_all = ok_all and allanch
            print(f'{m:>4} {name:>4} {len(edges):>10} '
                  f'{len(cliques4):>5} '
                  f'{"YES" if allanch else "NO!!!":>12} '
                  f'{min(spans) if spans else "-":>8} '
                  f'{str(spans[:6]):>20}')
            if not allanch:
                bad = [q for q in cliques4 if q[0] > 3 * m]
                print(f'      UNANCHORED 4-CLIQUES (shallow!): '
                      f'{bad[:5]}')
    print(f'ANCHOR-4 across all scans: '
          f'{"HOLDS" if ok_all else "VIOLATED"}')


if __name__ == '__main__':
    main()
