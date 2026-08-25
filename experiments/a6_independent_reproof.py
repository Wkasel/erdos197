#!/usr/bin/env python3
"""AUDIT A6: independent re-proof of the two smallest keystone claims.

Written from the PAPER's definitions alone (paper/main.tex, Definition
[Order gadget] and the statements of the transfer lock / FLIP).  No code
imported or copied from the existing experiment suite.

Definitions used (from main.tex):
  - interval (M, 2M], values M+1 .. 2M
  - b_j = M + j (bottoms), t_i = 2M - i (tops)
  - A1: t5 < b5,  A2: t3 < b6,  A3: t10 < b3   ("<" = precedes)
  - AP-free (condition (i)): for every arithmetic progression a<b<c inside
    (M, 2M], neither a<b<c nor c<b<a holds in the placement order.

Claims checked:
  (a) TRANSFER LOCK (unconditional form, as stated in notes/33 Lemma E and
      paper lem:transfer): for M = 0 mod 4, in any AP-free linear order of
      (M,2M]:  b5 < b3  <=>  t3 < t5.
      Verified as two UNSAT queries:
        T1: AP-free  &  (b5<b3) & (t5<t3)   -> UNSAT
        T2: AP-free  &  (b3<b5) & (t3<t5)   -> UNSAT
      plus two SAT sanity checks that the two consistent orientations are
      realizable (the lock is not vacuous):
        T3: AP-free  &  (b5<b3) & (t3<t5)   -> SAT
        T4: AP-free  &  (b3<b5) & (t5<t3)   -> SAT
  (b) FLIP: for M = 0 mod 8, M >= 16:
        F1: AP-free & A1 & A2 & A3 & (b5<b3) -> UNSAT
      plus sanity:
        F2: AP-free & A2 & A3 & (b5<b3)      -> SAT   (A1 alone is the killer)

Encoding (mine): one boolean x_{u,v} per value pair u<v meaning "u precedes v".
AP-freeness: for AP (a,b,c):  clause (~x_ab | ~x_bc)  [kills a<b<c]
                              clause ( x_ab |  x_bc)  [kills c<b<a]
Transitivity: eager O(n^3) for M <= 200 (both cyclic tournament patterns
banned); lazy refinement for large M (sound for UNSAT verdicts; SAT verdicts
are only accepted when the model's relation is verified to be a total order
and AP-free by an independent model checker).
"""

import sys
import time
from itertools import combinations

from pysat.solvers import Cadical195


def make_vars(M):
    vals = list(range(M + 1, 2 * M + 1))
    var = {}
    nv = 0
    for u, v in combinations(vals, 2):
        nv += 1
        var[(u, v)] = nv
    return vals, var


def lit(var, u, v):
    """Literal asserting u precedes v (u != v, both in block)."""
    if u < v:
        return var[(u, v)]
    return -var[(v, u)]


def ap_clauses(M, vals, var):
    cls = []
    lo, hi = M + 1, 2 * M
    for b in vals:
        dmax = min(b - lo, hi - b)
        for d in range(1, dmax + 1):
            a, c = b - d, b + d
            xab = lit(var, a, b)
            xbc = lit(var, b, c)
            cls.append([-xab, -xbc])   # not (a<b and b<c)
            cls.append([xab, xbc])     # not (c<b and b<a)
    return cls


def trans_clauses_eager(vals, var):
    cls = []
    for u, v, w in combinations(vals, 3):
        xuv, xvw, xuw = var[(u, v)], var[(v, w)], var[(u, w)]
        cls.append([-xuv, -xvw, xuw])   # u<v & v<w -> u<w
        cls.append([xuv, xvw, -xuw])    # v<u & w<v -> w<u
    return cls


def axioms(M, var, which):
    """which: subset of {'A1','A2','A3','b5b3','b3b5','t5t3','t3t5'}"""
    b3, b5, b6 = M + 3, M + 5, M + 6
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    table = {
        'A1': lit(var, t5, b5),
        'A2': lit(var, t3, b6),
        'A3': lit(var, t10, b3),
        'b5b3': lit(var, b5, b3),
        'b3b5': lit(var, b3, b5),
        't5t3': lit(var, t5, t3),
        't3t5': lit(var, t3, t5),
    }
    return [table[w] for w in which]


def check_model_total_apfree(M, vals, var, model_set):
    """Independent verification that a SAT model encodes an AP-free linear
    order: build the relation, verify antisymmetry+totality by construction,
    verify acyclicity via topological sort, verify no monotone AP."""
    prec = {}
    for (u, v), x in var.items():
        prec[(u, v)] = (x in model_set)
    # build position order by counting predecessors (valid iff total order)
    npred = {v: 0 for v in vals}
    for (u, v), p in prec.items():
        if p:
            npred[v] += 1
        else:
            npred[u] += 1
    positions = sorted(npred.values())
    if positions != list(range(len(vals))):
        return False, "relation is not a linear order (cycle present)"
    pos = {v: npred[v] for v in vals}
    lo, hi = M + 1, 2 * M
    for b in vals:
        dmax = min(b - lo, hi - b)
        for d in range(1, dmax + 1):
            a, c = b - d, b + d
            if pos[a] < pos[b] < pos[c] or pos[c] < pos[b] < pos[a]:
                return False, f"monotone AP {(a, b, c)}"
    return True, "model verified: total order, AP-free"


def solve_eager(M, extra_names, expect):
    vals, var = make_vars(M)
    t0 = time.time()
    cls = ap_clauses(M, vals, var) + trans_clauses_eager(vals, var)
    units = axioms(M, var, extra_names)
    with Cadical195(bootstrap_with=cls) as s:
        for u in units:
            s.add_clause([u])
        sat = s.solve()
        note = ""
        if sat:
            ok, note = check_model_total_apfree(M, vals, var, set(s.get_model()))
            if not ok:
                raise RuntimeError(f"model check failed: {note}")
    dt = time.time() - t0
    verdict = "SAT" if sat else "UNSAT"
    status = "AGREE" if verdict == expect else "**DISAGREE**"
    print(f"  M={M:5d} eager  [{'+'.join(extra_names):24s}] -> {verdict:5s} "
          f"(expected {expect:5s}) {status}  {dt:6.1f}s {note}")
    return verdict == expect


def find_cycles(vals, var, model_set, limit=20000):
    """Find violated transitivity triples in the model's tournament."""
    prec = {}
    for (u, v), x in var.items():
        prec[(u, v)] = (x in model_set)

    def before(u, v):
        if u < v:
            return prec[(u, v)]
        return not prec[(v, u)]

    # order candidate by predecessor count; check consecutive triples first,
    # then full scan for cyclic triples
    npred = {v: 0 for v in vals}
    for (u, v), p in prec.items():
        npred[v if p else u] += 1
    order = sorted(vals, key=lambda v: npred[v])
    bad = []
    n = len(order)
    for i in range(n):
        for j in range(i + 1, n):
            u, v = order[i], order[j]
            if before(v, u):
                # u should be before v by count; find w completing a cycle
                for w in order:
                    if w in (u, v):
                        continue
                    if before(u, w) and before(w, v):
                        bad.append((u, w, v))
                        if len(bad) >= limit:
                            return bad
                        break
    return bad


def solve_lazy(M, extra_names, expect, max_rounds=400):
    """Lazy transitivity refinement. UNSAT verdicts are sound at any round.
    SAT verdicts accepted only after the independent model checker passes."""
    vals, var = make_vars(M)
    t0 = time.time()
    cls = ap_clauses(M, vals, var)
    units = axioms(M, var, extra_names)
    s = Cadical195(bootstrap_with=cls)
    for u in units:
        s.add_clause([u])
    verdict = None
    note = ""
    for rnd in range(1, max_rounds + 1):
        if not s.solve():
            verdict = "UNSAT"
            note = f"round {rnd}"
            break
        model_set = set(s.get_model())
        ok, msg = check_model_total_apfree(M, vals, var, model_set)
        if ok:
            verdict = "SAT"
            note = f"round {rnd}; {msg}"
            break
        cyc = find_cycles(vals, var, model_set)
        if not cyc:
            raise RuntimeError("model rejected but no cycle found: " + msg)
        for (u, w, v) in cyc:
            # ban cycle u<w, w<v, v<u
            s.add_clause([-lit(var, u, w), -lit(var, w, v), -lit(var, v, u)])
    s.delete()
    dt = time.time() - t0
    if verdict is None:
        print(f"  M={M:5d} lazy   [{'+'.join(extra_names):24s}] -> NO VERDICT "
              f"after {max_rounds} rounds  {dt:6.1f}s")
        return False
    status = "AGREE" if verdict == expect else "**DISAGREE**"
    print(f"  M={M:5d} lazy   [{'+'.join(extra_names):24s}] -> {verdict:5s} "
          f"(expected {expect:5s}) {status}  {dt:6.1f}s ({note})")
    return verdict == expect


def run_scale(M, lazy):
    solve = (lambda names, exp: solve_lazy(M, names, exp)) if lazy else \
            (lambda names, exp: solve_eager(M, names, exp))
    ok = True
    print(f"-- scale M={M} (M mod 8 = {M % 8}) --")
    # (a) transfer lock, unconditional biconditional
    ok &= solve(['b5b3', 't5t3'], 'UNSAT')   # T1
    ok &= solve(['b3b5', 't3t5'], 'UNSAT')   # T2
    ok &= solve(['b5b3', 't3t5'], 'SAT')     # T3 sanity
    ok &= solve(['b3b5', 't5t3'], 'SAT')     # T4 sanity
    # (a') conditioned form exactly as the audit task words it (A2+A3 added)
    ok &= solve(['A2', 'A3', 'b5b3', 't5t3'], 'UNSAT')  # T1'
    # (b) FLIP
    ok &= solve(['A1', 'A2', 'A3', 'b5b3'], 'UNSAT')    # F1
    ok &= solve(['A2', 'A3', 'b5b3'], 'SAT')            # F2 sanity
    return ok


if __name__ == '__main__':
    scales = [int(a) for a in sys.argv[1:]] or [48, 56, 104, 200]
    all_ok = True
    for M in scales:
        all_ok &= run_scale(M, lazy=(M > 200))
    print("ALL AGREE" if all_ok else "DISAGREEMENT FOUND — FIVE-ALARM")
