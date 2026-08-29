"""Erdős #197 — e173: FRONT TELESCOPE (notes/70).

Three instruments for the telescoping ledger:

  audit  — pure analysis of existing e158 witnesses: verify the
           boundary-currency accounting (L-HOME: every adjacent-seam
           inversion pair lives at exactly ONE dyadic boundary;
           L-2PRICE: every adjacent-octave pair is an inversion pair
           at EXACTLY TWO chain anchors — the two that price its home
           boundary; skip pairs at ZERO chain anchors), and measure
           the consecutive-anchor overlap Inv(M) ∩ Inv(M/2) (= the
           shared seam s1, predicted MAXIMAL on the C1 witness).

  fresh  — the freshness cells F(M; v): 4-block gadget with per-seam
           budgets  [s0 = 0 exactly, s1+s2 <= v]  (s1 NOT re-priced
           below: the lower anchor may spend freely on the shared
           boundary, only NEW-boundary currency is banned).
           UNSAT  ==>  (T-FORCE-4) every valid pair meeting the block
           bounds with Inv_T(M) <= v for both teams has a team with
           an inverted pair at boundary beta(M) — currency DISJOINT
           from every pair priced at anchor M and above.
           SAT   ==>  the pump payment can ride entirely on the
           doubly-priced shared seam; naive freshness fails.

  five   — the 3-anchor chain gadget U5(M): values (M/4, 8M], five
           blocks, budgets at anchors M (beta(2M)+beta(4M)), M/2
           (beta(M)+beta(2M)) and M/4 (beta(M/2)+beta(M)).  Note the
           middle anchor is auto-priced by the outer two (its seams
           are shared) — the chain has no parking space.

  pump8  — v_min(0) scan for the 4-block gadget at small M (M = 8:
           values (4,64]): the bottom step of the 16-chain.

Solver discipline: one heavy solve at a time; every SAT witness
independently audited.  Streams: data/e173_telescope.jsonl, per-cell
data/e173_{tag}.json.
"""
import argparse
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e173_telescope.jsonl')

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def stream(row):
    with open(JSONL, 'a') as f:
        f.write(json.dumps(row) + '\n')


# ---------------------------------------------------------------- audit

def _pair_boundary(u, w):
    """Home boundary of an adjacent-octave pair: the power of 2 (times
    odd part of the chain base) separating u's and w's octaves.  Here
    all e158 gadgets are dyadic (base a power of 2), so boundaries are
    the values 2^j themselves — return the boundary value b with
    u <= b < w and octaves adjacent, else None (skip/same-octave)."""
    ou = u.bit_length() - (1 if u & (u - 1) == 0 else 0)  # octave idx: (2^{o-1}, 2^o]
    ow = w.bit_length() - (1 if w & (w - 1) == 0 else 0)
    if ow == ou + 1:
        return 1 << ou
    return None


def _chain_anchors_covering(u, w, jmax=30):
    """Chain anchors N = 2^j at which (u, w) is an adjacent-seam
    inversion-eligible pair of W(N): s1-type iff N < u <= 2N < w <= 4N,
    s2-type iff 2N < u <= 4N < w <= 8N."""
    out = []
    for j in range(jmax):
        N = 1 << j
        if N < u <= 2 * N < w <= 4 * N:
            out.append((N, 's1'))
        if 2 * N < u <= 4 * N < w <= 8 * N:
            out.append((N, 's2'))
    return out


def run_audit():
    files = ['e158_c1_M16_up6.json', 'e158_c2_M16_dn0.json',
             'e158_f_M16_up384_dn0.json', 'e158_c0_M16_free.json']
    report = {}
    for fn in files:
        path = os.path.join(DATA, fn)
        if not os.path.exists(path):
            print(f'-- {fn}: missing, skipped')
            continue
        rec = json.load(open(path))
        if rec.get('verdict') != 'SAT':
            print(f'-- {fn}: verdict {rec.get("verdict")}, skipped')
            continue
        M = rec['M']
        ent = {'M': M, 'vup': rec['vup'], 'vdn': rec['vdn'], 'teams': {}}
        for team in ('A', 'B'):
            a = rec['anatomy'][team]
            s0 = set(map(tuple, a['inv_s0']))
            s1 = set(map(tuple, a['inv_s1']))
            s2 = set(map(tuple, a['inv_s2']))
            # L-HOME: each pair at exactly one boundary; seam label
            # must match the home boundary (s0->M, s1->2M, s2->4M).
            homes_ok = all(_pair_boundary(u, w) == b
                           for ps, b in ((s0, M), (s1, 2 * M), (s2, 4 * M))
                           for (u, w) in ps)
            # seam sets pairwise disjoint (distinct boundaries)
            disj = not (s0 & s1) and not (s1 & s2) and not (s0 & s2)
            # L-2PRICE on every inversion pair: exactly two chain
            # anchors, namely the two pricing the home boundary.
            twoprice_ok = True
            for ps, b in ((s0, M), (s1, 2 * M), (s2, 4 * M)):
                for (u, w) in ps:
                    cov = _chain_anchors_covering(u, w)
                    expect = {(b // 2, 's1'), (b // 4, 's2')}
                    if set(cov) != expect:
                        twoprice_ok = False
            up = s1 | s2       # Inv(anchor M) as a pair set
            dn = s0 | s1       # Inv(anchor M/2) as a pair set
            inter = up & dn
            ent['teams'][team] = {
                'n_s0': len(s0), 'n_s1': len(s1), 'n_s2': len(s2),
                'L_HOME': homes_ok, 'seams_disjoint': disj,
                'L_2PRICE': twoprice_ok,
                'n_up': len(up), 'n_dn': len(dn),
                'overlap': len(inter),
                'overlap_is_exactly_s1': inter == s1,
                'upper_payment_fully_shared': up and inter == up or len(up) == 0,
                'fresh_lower_mass': len(dn - up),
            }
        report[fn] = ent
        print(f'== {fn} (M={M}, vup={rec["vup"]}, vdn={rec["vdn"]})')
        for team, t in ent['teams'].items():
            print(f'   {team}: s0/s1/s2 = {t["n_s0"]}/{t["n_s1"]}/{t["n_s2"]}'
                  f' | L-HOME {t["L_HOME"]} | disjoint {t["seams_disjoint"]}'
                  f' | L-2PRICE {t["L_2PRICE"]}')
            print(f'      Inv(M)={t["n_up"]}, Inv(M/2)={t["n_dn"]}, '
                  f'overlap={t["overlap"]} (== s1: {t["overlap_is_exactly_s1"]}), '
                  f'upper fully shared: {t["upper_payment_fully_shared"]}, '
                  f'fresh lower mass={t["fresh_lower_mass"]}')
    out = os.path.join(DATA, 'e173_audit.json')
    json.dump(report, open(out, 'w'), indent=1)
    stream({'tag': 'audit', 'report': {k: v for k, v in report.items()}})
    print(f'-> {out}')


# ------------------------------------------------- generalized chain SAT

def _mk_vars(n, start=1):
    off = {}
    nxt = start
    for i in range(n):
        for j in range(i + 1, n):
            off[(i, j)] = nxt
            nxt += 1
    return off, nxt - 1


def solve_chain(blocks, seam_budgets, tag, time_budget=3600.0):
    """blocks: list of value-lists (consecutive dyadic blocks, low to
    high).  seam_budgets: list of (name, [seam_idx...], bound) — seam
    i = adjacent pairs blocks[i] x blocks[i+1]; bound applies PER TEAM
    to the total inverted pairs over the listed seams.  Balance bounds
    (ceil(|blk|/2)) per team per block.  Complete encoding as e158."""
    V = [v for blk in blocks for v in blk]
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    offA, top = _mk_vars(n, start=1)
    offB, top = _mk_vars(n, start=top + 1)
    ai = {}
    for v in V:
        top += 1
        ai[v] = top

    def litT(off):
        def lit(u, w):
            i, j = idx[u], idx[w]
            return off[(i, j)] if i < j else -off[(j, i)]
        return lit

    litA, litB = litT(offA), litT(offB)
    Vs = set(V)
    seams = [[(u, w) for u in blocks[i] for w in blocks[i + 1]]
             for i in range(len(blocks) - 1)]
    need = sorted({si for (_, sis, _) in seam_budgets for si in sis})
    cls = []
    xvar = {}
    for team, lit, g in (('A', litA, lambda v: -ai[v]),
                         ('B', litB, lambda v: ai[v])):
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    cls.append(gg + [-lit(a, b), -lit(b, c)])
                    cls.append(gg + [lit(a, b), lit(b, c)])
        for si in need:
            for (u, w) in seams[si]:
                top += 1
                xvar[(team, si, u, w)] = top
                cls.append([g(u), g(w), lit(u, w), top])
    for off in (offA, offB):
        for i in range(n):
            for j in range(i + 1, n):
                xij = off[(i, j)]
                for kk in range(j + 1, n):
                    cls.append([-xij, -off[(j, kk)], off[(i, kk)]])
                    cls.append([xij, off[(j, kk)], -off[(i, kk)]])
    cards = []
    tid = top
    for blk in blocks:
        base = math.ceil(len(blk) / 2)
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blk],
                                  bound=base, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            cards += enc.clauses
    for team in ('A', 'B'):
        for (name, sis, bound) in seam_budgets:
            lits = [xvar[(team, si, u, w)] for si in sis
                    for (u, w) in seams[si]]
            if bound <= 0:
                cards += [[-l] for l in lits]
            else:
                enc = CardEnc.atmost(lits=lits, bound=bound, top_id=tid,
                                     encoding=EncType.seqcounter)
                tid = max(tid, enc.nv)
                cards += enc.clauses

    import multiprocessing as mp
    import queue as _q

    def _work(outq):
        t0 = time.time()
        with Cadical195(bootstrap_with=cls) as s:
            for c in cards:
                s.add_clause(c)
            ok = s.solve()
            el = round(time.time() - t0, 1)
            if not ok:
                outq.put(('UNSAT', el, None))
                return
            model = set(l for l in s.get_model() if l > 0)
        colA = [v for v in V if ai[v] in model]
        colB = [v for v in V if ai[v] not in model]
        pn = lambda l: (l in model) if l > 0 else (abs(l) not in model)
        orders = {}
        for team, lit, col in (('A', litA, colA), ('B', litB, colB)):
            wins = {v: 0 for v in col}
            for i, u in enumerate(col):
                for w in col[i + 1:]:
                    if pn(lit(u, w)):
                        wins[u] += 1
                    else:
                        wins[w] += 1
            orders[team] = sorted(col, key=lambda v: -wins[v])
        outq.put(('SAT', el, {'A': colA, 'B': colB,
                              'orderA': orders['A'], 'orderB': orders['B']}))

    ctx = mp.get_context('fork')
    outq = ctx.Queue()
    p = ctx.Process(target=_work, args=(outq,))
    t0 = time.time()
    p.start()
    try:
        verdict, el, info = outq.get(timeout=time_budget)
        p.join()
    except _q.Empty:
        p.terminate()
        p.join()
        return 'TIMEOUT', round(time.time() - t0, 1), None
    return verdict, el, info


def audit_chain(blocks, seam_budgets, info):
    """Independent witness audit: balance, monotone-AP freedom, seam
    recounts vs budgets.  Returns (errs, anatomy)."""
    errs, anatomy = [], {}
    for team in ('A', 'B'):
        col = set(info[team])
        order = info[f'order{team}']
        p = {v: i for i, v in enumerate(order)}
        if set(order) != col:
            errs.append(f'{team}: order/color mismatch')
        vals = sorted(col)
        vs = set(vals)
        for b in vals:
            for d in range(1, min(b - vals[0], vals[-1] - b) + 1):
                a, c = b - d, b + d
                if a in vs and c in vs:
                    if p[a] < p[b] < p[c] or p[c] < p[b] < p[a]:
                        errs.append(f'{team}: monotone AP {(a, b, c)}')
        for bi, blk in enumerate(blocks):
            got = len([v for v in blk if v in col])
            if got < math.ceil(len(blk) / 2):
                errs.append(f'{team}: block {bi} balance {got}')
        counts = []
        for i in range(len(blocks) - 1):
            inv = [(u, w) for u in blocks[i] if u in col
                   for w in blocks[i + 1] if w in col and p[w] < p[u]]
            counts.append(len(inv))
        anatomy[team] = {'seam_counts': counts}
        for (name, sis, bound) in seam_budgets:
            tot = sum(counts[si] for si in sis)
            anatomy[team][name] = tot
            if tot > bound:
                errs.append(f'{team}: budget {name}: {tot} > {bound}')
    return errs, anatomy


def dyadic_blocks(lo, hi):
    """Consecutive octaves (lo, 2lo], (2lo, 4lo], ..., (hi/2, hi]."""
    out = []
    b = lo
    while b < hi:
        out.append(list(range(b + 1, 2 * b + 1)))
        b *= 2
    return out


def run_cell(tag, blocks, seam_budgets, time_budget):
    verdict, el, info = solve_chain(blocks, seam_budgets, tag,
                                    time_budget)
    row = {'tag': tag, 'blocks': [[b[0] - 1, b[-1]] for b in blocks],
           'budgets': [(nm, sis, bd) for (nm, sis, bd) in seam_budgets],
           'verdict': verdict, 'time': el}
    if verdict == 'SAT':
        errs, anat = audit_chain(blocks, seam_budgets, info)
        if errs:
            row['verdict'] = 'WITNESS-FAIL'
            row['errs'] = errs[:8]
        row['anatomy'] = anat
        row['colorA'] = info['A']
        row['orderA'] = info['orderA']
        row['orderB'] = info['orderB']
    stream(row)
    print(f'{tag}: {row["verdict"]} [{el}s] '
          + json.dumps({t: a for t, a in row.get('anatomy', {}).items()}),
          flush=True)
    with open(os.path.join(DATA, f'e173_{tag}.json'), 'w') as f:
        json.dump(row, f, indent=1)
    return row['verdict']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['audit', 'fresh', 'five', 'pump8'])
    ap.add_argument('--M', type=int, default=16)
    ap.add_argument('--v', type=int, default=6)
    ap.add_argument('--budget', type=float, default=3600.0)
    args = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)
    if args.cmd == 'audit':
        run_audit()
    elif args.cmd == 'fresh':
        M = args.M
        blocks = dyadic_blocks(M // 2, 8 * M)     # Bm1,B0,B1,B2
        budgets = [('s0_zero', [0], 0), ('vup', [1, 2], args.v)]
        run_cell(f'fresh_M{M}_v{args.v}', blocks, budgets, args.budget)
    elif args.cmd == 'five':
        M = args.M
        blocks = dyadic_blocks(M // 4, 8 * M)     # 5 blocks
        budgets = [('vbot', [0, 1], 0), ('vtop', [2, 3], args.v)]
        run_cell(f'five_M{M}_top{args.v}_bot0', blocks, budgets,
                 args.budget)
    elif args.cmd == 'pump8':
        M = args.M
        blocks = dyadic_blocks(M // 2, 8 * M)
        budgets = [('vdn', [0, 1], 0), ('vup', [1, 2], args.v)]
        run_cell(f'pump_M{M}_up{args.v}_dn0', blocks, budgets,
                 args.budget)


if __name__ == '__main__':
    main()
