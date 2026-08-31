"""Erdős #197 — e188: FRONT CMIN machine companion (notes/85).

Instruments (all on the SPLIT layer of low = (M/2,2M] and B1 =
(2M,4M]; B2 never enters — S = Σ_z min(c_A,c_B) is split-invariant):

  cmin       — exact cmin(M): min S over balanced μ_dn = 0 LOW-IMPURE
               splits (CP-SAT, adversarial side-selection; port of
               e178 part71c).  --tmin 2 gives cmin_{t≥2}(M): impurity
               ≥ 2 per parity per team (the exchange-lemma floor,
               notes/71 §11: 10/22 at M = 8/12).
  bm1vac     — Lemma BM1-VAC check: balance + μ_dn = 0 + Bm1∩A
               mixed-parity.  Hand claim (notes/85): infeasible for
               impurity t ≤ ⌊M/8⌋ − 1; this query has NO t-cap, so
               UNSAT = stronger than the lemma, SAT = a big-t
               inhabitant (dump it).
  sweepaudit — t = 1 accounting audit at a hand-theorem scale: for
               sampled (r, d) ∈ B0-odd × B0-even force the exact
               near-pure low split, CP-SAT-minimize S over B1
               colorings, then recompute the notes/85 proof
               quantities (N candidates, f_A, f_B failures, corner
               constants) on the optimal witness and verify
               S ≥ N − f_A − f_B and S ≥ M.

Records: data/e188_cmin.jsonl (+ stdout).
"""
import argparse
import json
import os
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e188_cmin.jsonl')


def stream(row):
    os.makedirs(DATA, exist_ok=True)
    with open(JSONL, 'a') as f:
        f.write(json.dumps(row) + '\n')
    print(json.dumps(row), flush=True)


def split_sets(M):
    low = list(range(M // 2 + 1, 2 * M + 1))
    bm1 = [v for v in low if v <= M]
    b0 = [v for v in low if v > M]
    b1 = list(range(2 * M + 1, 4 * M + 1))
    return low, bm1, b0, b1


def anatomy(M, Aset):
    """Defector anatomy of a split: canonical labeling by low majority."""
    low, bm1, b0, b1 = split_sets(M)
    a_odds = [v for v in low if v in Aset and v % 2 == 1]
    a_evens = [v for v in low if v in Aset and v % 2 == 0]
    # canonical: team holding more low odds is 'oddteam'
    if len(a_odds) >= len(a_evens):
        D = sorted(a_evens)                      # evens held by odd-team
        R = sorted(v for v in low if v not in Aset and v % 2 == 1)
    else:
        D = sorted(v for v in low if v not in Aset and v % 2 == 0)
        R = sorted(a_odds)
    t1 = len([v for v in D if v <= M])
    t0 = len([v for v in D if v > M])
    corner = 7 * M // 2 - 12
    a_b1_odd = [y for y in b1 if y in Aset and y % 2 == 1]
    b_b1_even = [y for y in b1 if y not in Aset and y % 2 == 0]
    return {'R': R, 'D': D, 't': len(D), 't_bm1': t1, 't_b0': t0,
            'corner_from': corner + 1,
            'oddteam_B1_odds': a_b1_odd if len(a_odds) >= len(a_evens)
            else [y for y in b1 if y not in Aset and y % 2 == 1],
            'eventeam_B1_evens': b_b1_even if len(a_odds) >= len(a_evens)
            else [y for y in b1 if y in Aset and y % 2 == 0]}


def compute_S(M, Aset):
    """Exact S = Σ_z min(c_A, c_B) for a full split of low ∪ B1."""
    low, bm1, b0, b1 = split_sets(M)
    cA, cB = defaultdict(int), defaultdict(int)
    for u in low:
        for y in b1:
            z = 2 * y - u
            if z <= 4 * M or z > 8 * M:
                continue
            if u in Aset and y in Aset:
                cA[z] += 1
            elif u not in Aset and y not in Aset:
                cB[z] += 1
    return sum(min(cA[z], cB[z]) for z in set(cA) | set(cB))


def mu_dn_clauses_cp(m, M, A):
    low, bm1, b0, b1 = split_sets(M)
    for w in bm1:
        for u in b0:
            y = 2 * u - w
            if 2 * M < y <= 4 * M:
                m.AddBoolOr([A[w].Not(), A[u].Not(), A[y].Not()])
                m.AddBoolOr([A[w], A[u], A[y]])


def run_cmin(M, tmin, timeout, workers):
    from ortools.sat.python import cp_model
    low, bm1, b0, b1 = split_sets(M)
    m = cp_model.CpModel()
    A = {v: m.NewBoolVar(f'a{v}') for v in low + b1}
    m.Add(sum(A[v] for v in bm1) == M // 4)
    m.Add(sum(A[v] for v in b0) == M // 2)
    m.Add(sum(A[v] for v in b1) == M)
    mu_dn_clauses_cp(m, M, A)
    lo = sum(A[v] for v in low if v % 2 == 1)
    le = sum(A[v] for v in low if v % 2 == 0)
    m.Add(lo >= tmin)
    m.Add(le >= tmin)
    m.Add(lo <= 3 * M // 4 - tmin)
    m.Add(le <= 3 * M // 4 - tmin)
    pairs = defaultdict(list)
    for u in low:
        for y in b1:
            z = 2 * y - u
            if 4 * M < z <= 8 * M:
                pairs[z].append((u, y))
    total = []
    for z, ps in sorted(pairs.items()):
        ca, cb = [], []
        for (u, y) in ps:
            pa = m.NewBoolVar(f'pa{u}_{y}')
            m.AddBoolAnd([A[u], A[y]]).OnlyEnforceIf(pa)
            m.AddBoolOr([A[u].Not(), A[y].Not()]).OnlyEnforceIf(pa.Not())
            pb = m.NewBoolVar(f'pb{u}_{y}')
            m.AddBoolAnd([A[u].Not(), A[y].Not()]).OnlyEnforceIf(pb)
            m.AddBoolOr([A[u], A[y]]).OnlyEnforceIf(pb.Not())
            ca.append(pa)
            cb.append(pb)
        mz = m.NewIntVar(0, len(ps), f'm{z}')
        sel = m.NewBoolVar(f's{z}')
        m.Add(mz >= sum(ca)).OnlyEnforceIf(sel)
        m.Add(mz >= sum(cb)).OnlyEnforceIf(sel.Not())
        total.append(mz)
    m.Minimize(sum(total))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout
    solver.parameters.num_search_workers = workers
    t0 = time.time()
    st = solver.Solve(m)
    el = round(time.time() - t0, 1)
    name = solver.StatusName(st)
    val = (int(solver.ObjectiveValue())
           if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
    lb = int(solver.BestObjectiveBound()) if val is not None else None
    row = {'tag': f'cmin_t{tmin}_M{M}', 'status': name, 'value': val,
           'lb': lb, 'time': el}
    if val is not None:
        Aset = {v for v in low + b1 if solver.Value(A[v])}
        row['anatomy'] = anatomy(M, Aset)
        row['S_check'] = compute_S(M, Aset)
        row['colorA_low'] = sorted(v for v in Aset if v <= 2 * M)
        row['colorA_b1'] = sorted(v for v in Aset if v > 2 * M)
    stream(row)


def run_bm1vac(M, tcap=None):
    from pysat.solvers import Cadical195
    from pysat.card import CardEnc, EncType
    low, bm1, b0, b1 = split_sets(M)
    V = low + b1
    ai = {v: i + 1 for i, v in enumerate(V)}
    nxt = len(V)
    cls = []
    for w in bm1:
        for u in b0:
            y = 2 * u - w
            if 2 * M < y <= 4 * M:
                cls.append([-ai[w], -ai[u], -ai[y]])
                cls.append([ai[w], ai[u], ai[y]])
    for blkvals, half in ((bm1, M // 4), (b0, M // 2), (b1, M)):
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blkvals],
                                  bound=half, top_id=nxt,
                                  encoding=EncType.seqcounter)
            nxt = max(nxt, enc.nv)
            cls += enc.clauses
    # Bm1∩A mixed-parity (⟺ Bm1∩B mixed, since |Bm1∩A| = #odds(Bm1))
    cls.append([ai[v] for v in bm1 if v % 2 == 1])
    cls.append([ai[v] for v in bm1 if v % 2 == 0])
    if tcap is not None:
        # impurity t ≤ tcap in the canonical (majority-odd) labeling:
        # t = #evens in A-low if A majority-odd.  Symmetrize: cap BOTH
        # (#evens in A-low) and (#odds in A-low) by "≥ 3M/4 − tcap on
        # the majority side" — i.e. one parity count ≤ tcap.
        lo = [ai[v] for v in low if v % 2 == 1]
        le = [ai[v] for v in low if v % 2 == 0]
        selo, nxt = nxt + 1, nxt + 1        # A majority-odd selector
        for lits, s in ((le, selo), (lo, -selo)):
            enc = CardEnc.atmost(lits=lits, bound=tcap, top_id=nxt,
                                 encoding=EncType.seqcounter)
            nxt = max(nxt, enc.nv)
            cls += [c + [-s] for c in enc.clauses]
        cls.append([selo, -selo])
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        ok = s.solve()
        model = set(l for l in s.get_model() if l > 0) if ok else None
    el = round(time.time() - t0, 1)
    row = {'tag': f'bm1vac_M{M}' + ('' if tcap is None else f'_t{tcap}'),
           'verdict': 'SAT' if ok else 'UNSAT', 'time': el}
    if ok:
        Aset = {v for v in V if ai[v] in model}
        row['anatomy'] = anatomy(M, Aset)
        row['S_check'] = compute_S(M, Aset)
        row['colorA'] = sorted(Aset)
    stream(row)


def proof_quantities(M, Aset, r, d):
    """notes/85 accounting on a concrete t=1 witness (channels r, d)."""
    low, bm1, b0, b1 = split_sets(M)
    corner = 7 * M // 2 - 12          # last below-corner value
    Alow_odds = [v for v in low if v % 2 == 1 and v != r]
    Blow_evens = [v for v in low if v % 2 == 0 and v != d]
    dA = sorted((u - r) // 2 for u in Alow_odds)
    dB = sorted((u - d) // 2 for u in Blow_evens)
    Ir = [y for y in b1 if 2 * y - r > 4 * M]
    Id = [y for y in b1 if 2 * y - d > 4 * M]
    Bcand = [y for y in Ir if y not in Aset]
    Acand = [y for y in Id if y in Aset]
    fB = [y for y in Bcand
          if not any(y + o in Aset for o in dA if 2 * M < y + o <= 4 * M)]
    fA = [y for y in Acand
          if not any(y + o not in Aset for o in dB
                     if 2 * M < y + o <= 4 * M)]
    N = len(Bcand) + len(Acand)
    rigid_ok = all(
        (y in Aset) == (y % 2 == 0)
        for y in b1 if y <= corner)
    return {'N': N, 'fA': len(fA), 'fB': len(fB),
            'fA_at': fA, 'fB_at': fB, 'N_minus_f': N - len(fA) - len(fB),
            'rigid_below_corner': rigid_ok, 'corner_last': corner}


def run_sweepaudit(M, cells, timeout, workers):
    from ortools.sat.python import cp_model
    low, bm1, b0, b1 = split_sets(M)
    b0_odds = [v for v in b0 if v % 2 == 1]
    b0_evens = [v for v in b0 if v % 2 == 0]
    # sample cells: extremal corner + spread
    rs = sorted(set([b0_odds[0], b0_odds[len(b0_odds) // 2],
                     b0_odds[-1]]))
    ds = sorted(set([b0_evens[0], b0_evens[len(b0_evens) // 2],
                     b0_evens[-1]]))
    todo = [(r, d) for r in rs for d in ds][:cells]
    for (r, d) in todo:
        m = cp_model.CpModel()
        A = {v: m.NewBoolVar(f'a{v}') for v in b1 + low}
        for v in low:      # fixed near-pure split
            m.Add(A[v] == (1 if (v % 2 == 1 and v != r) or v == d
                           else 0))
        m.Add(sum(A[v] for v in b1) == M)
        mu_dn_clauses_cp(m, M, A)
        pairs = defaultdict(list)
        for u in low:
            for y in b1:
                z = 2 * y - u
                if 4 * M < z <= 8 * M:
                    pairs[z].append((u, y))
        total = []
        for z, ps in sorted(pairs.items()):
            ca, cb = [], []
            for (u, y) in ps:
                pa = m.NewBoolVar(f'pa{u}_{y}')
                m.AddBoolAnd([A[u], A[y]]).OnlyEnforceIf(pa)
                m.AddBoolOr([A[u].Not(),
                             A[y].Not()]).OnlyEnforceIf(pa.Not())
                pb = m.NewBoolVar(f'pb{u}_{y}')
                m.AddBoolAnd([A[u].Not(), A[y].Not()]).OnlyEnforceIf(pb)
                m.AddBoolOr([A[u], A[y]]).OnlyEnforceIf(pb.Not())
                ca.append(pa)
                cb.append(pb)
            mz = m.NewIntVar(0, len(ps), f'm{z}')
            sel = m.NewBoolVar(f's{z}')
            m.Add(mz >= sum(ca)).OnlyEnforceIf(sel)
            m.Add(mz >= sum(cb)).OnlyEnforceIf(sel.Not())
            total.append(mz)
        m.Minimize(sum(total))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = timeout
        solver.parameters.num_search_workers = workers
        t0 = time.time()
        st = solver.Solve(m)
        el = round(time.time() - t0, 1)
        name = solver.StatusName(st)
        row = {'tag': f'sweepaudit_M{M}', 'r': r, 'd': d, 'status': name,
               'time': el}
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            val = int(solver.ObjectiveValue())
            Aset = {v for v in low if (v % 2 == 1 and v != r) or v == d}
            Aset |= {v for v in b1 if solver.Value(A[v])}
            q = proof_quantities(M, Aset, r, d)
            row.update({'S': val, 'S_check': compute_S(M, Aset),
                        'S_ge_M': val >= M,
                        'accounting_ok': val >= q['N_minus_f'],
                        'bound_ge_M_when_no_fail':
                            q['N'] >= M if q['fA'] + q['fB'] == 0
                            else None, **q})
        elif name == 'INFEASIBLE':
            row['note'] = 'cell infeasible (mu_dn=0 unreachable here)'
        stream(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['cmin', 'bm1vac', 'sweepaudit'])
    ap.add_argument('--M', type=str, default='16')
    ap.add_argument('--tmin', type=int, default=1)
    ap.add_argument('--timeout', type=float, default=3600)
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--cells', type=int, default=9)
    args = ap.parse_args()
    for Ms in args.M.split(','):
        M = int(Ms)
        if args.cmd == 'cmin':
            run_cmin(M, args.tmin, args.timeout, args.workers)
        elif args.cmd == 'bm1vac':
            run_bm1vac(M)
        else:
            run_sweepaudit(M, args.cells, args.timeout, args.workers)


if __name__ == '__main__':
    main()
