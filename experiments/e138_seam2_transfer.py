"""e138: machine checks for notes/55 SS3 (band ladders + seam-2 transfer).

Part A (no solver): side conditions of SS3.1-3.3 at every M = 0 mod 16
  in 48..400:
  - every A4 parent pair of 4M+s is the TOPMOST adjacent pair of its
    gap-(s+t) ladder inside the band (the rung above it leaves P1);
  - a d-ladder of the band has exactly ONE high adjacent pair (its
    topmost), completing to 4M + (d - (4M - top rung));
  - the seesaw partners named in SS3.3 are genuine in-band APs.

Part B (tiny SAT, M-independent): LEMMA J enumeration.  Offset
  coordinates w_0..w_15 for the top run R = [4M-15, 4M].  For
  J subseteq [1,15], theory T(J) =
      AP-freeness on the 16-interval (56 APs)
    + transitivity
    + units w_{15-t} < w_{15-j-2t}  for j in J, t >= 0, j+2t <= 15
  (the units fired by S3-memberships 4M+j in T when R subseteq T).
  Enumerate all J by increasing size with downset pruning; report
  minimal forbidden (UNSAT) sets and maximal admissible size.

Part C: same with the run truncated to top length r+1 (units with
  j+2t <= r), r = 8..14: minimal forbidden sets per r.

Run: .venv/bin/python experiments/e138_seam2_transfer.py
Log: data/e138_transfer.log
"""
import itertools
import json
import time

from pysat.solvers import Cadical195

DATA = 'data/e138_transfer.json'


# ----------------------------------------------------------------------
# Part A
# ----------------------------------------------------------------------

def partA():
    for M in range(48, 401, 16):
        lo1, hi1 = 3 * M - 15, 4 * M
        # A4 parents are topmost adjacent ladder pairs
        for s in range(1, M + 16):
            t = 0
            while s + 2 * t <= M + 15:
                a, b = 4 * M - s - 2 * t, 4 * M - t
                g = b - a
                assert g == s + t
                assert lo1 <= a < b <= hi1, (M, s, t)
                assert b + g > hi1, (M, s, t, 'not topmost')
                assert 2 * b - a == 4 * M + s
                t += 1
        # one high adjacent pair per d-ladder
        for d in range(1, (M + 15) // 2):
            for res in range(d):
                lad = [v for v in range(lo1, hi1 + 1) if v % d == res % d]
                lad = [v for v in lad if lo1 <= v <= hi1]
                high = [(y - d, y) for y in lad
                        if y - d >= lo1 and 2 * y - (y - d) >= 4 * M + 1]
                top = max(lad)
                expect = [(top - d, top)] if top + d > hi1 and \
                    top - d >= lo1 and top + d >= 4 * M + 1 else []
                assert high == expect, (M, d, res, high, expect)
    print('  partA: ladder side conditions OK (M = 48..400 step 16)',
          flush=True)


# ----------------------------------------------------------------------
# Parts B/C: Lemma J
# ----------------------------------------------------------------------

def build_base(n=16):
    """Order vars + transitivity + AP-freeness clauses on 0..n-1."""
    off = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            off[(i, j)] = top

    def lit(u, w):
        return off[(u, w)] if u < w else -off[(w, u)]

    cls = []
    for b in range(n):
        for d in range(1, min(b, n - 1 - b) + 1):
            a, c = b - d, b + d
            cls.append([-lit(a, b), -lit(b, c)])
            cls.append([lit(a, b), lit(b, c)])
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                cls.append([-lit(i, j), -lit(j, k), lit(i, k)])
                cls.append([lit(i, j), lit(j, k), -lit(i, k)])
    return lit, cls


def units_for(J, r=15):
    """Units in offset coords for S3-set J with top run length r+1
    (run = offsets 15-r .. 15)."""
    out = []
    for j in J:
        t = 0
        while j + 2 * t <= r:
            out.append((15 - t, 15 - j - 2 * t))
            t += 1
    return out


def lemma_J(r=15, jmax=15, tag='B'):
    lit, base = build_base(16)
    t0 = time.time()
    forbidden_min = []
    admissible = []
    n_solve = 0
    for size in range(0, jmax + 1):
        for J in itertools.combinations(range(1, jmax + 1), size):
            Js = set(J)
            if any(set(f) <= Js for f in forbidden_min):
                continue
            cls = base + [[lit(u, w)] for (u, w) in units_for(J, r)]
            n_solve += 1
            with Cadical195(bootstrap_with=cls) as s:
                ok = s.solve()
            if ok:
                admissible.append(J)
            else:
                forbidden_min.append(J)
    mx = max((len(J) for J in admissible), default=0)
    maximal = [J for J in admissible
               if not any(set(J) < set(K) for K in admissible)]
    print(f'  part{tag} r={r}: {n_solve} solves '
          f'[{time.time()-t0:.0f}s]; minimal forbidden '
          f'({len(forbidden_min)}): {forbidden_min[:20]}'
          f'{" ..." if len(forbidden_min) > 20 else ""}; '
          f'max |J| admissible = {mx}; '
          f'#maximal admissible = {len(maximal)}', flush=True)
    if len(maximal) <= 12:
        print(f'    maximal admissible: {maximal}', flush=True)
    return {'r': r, 'minimal_forbidden': [list(f) for f in forbidden_min],
            'max_admissible_size': mx,
            'n_maximal': len(maximal),
            'maximal': [list(m) for m in maximal] if len(maximal) <= 40
            else None}


def main():
    partA()
    out = {'partB': lemma_J(15, 15, 'B'), 'partC': {}}
    for r in range(14, 7, -1):
        out['partC'][r] = lemma_J(r, r, f'C')
    with open(DATA, 'w') as f:
        json.dump(out, f, indent=1)
    print('e138: DONE', flush=True)


if __name__ == '__main__':
    main()
