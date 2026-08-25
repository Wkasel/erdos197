#!/usr/bin/env python3
"""AUDIT A6 — independent re-proof of the two keystone claims.

Written from scratch, solely from the definitions in paper/main.tex
(Definition def:og, Section sec:og / sec:c3 statements). No code imported
or adapted from experiments/.

Objects (paper, sec:og): interval (M, 2M]; bottoms b_j = M + j;
tops t_i = 2M - i.  AP-free order = for every arithmetic progression
a < b < c inside (M, 2M] (c = 2b - a), neither a<b<c nor c<b<a in
position order.  Equivalently (midpoint-extremal rule): on each AP the
midpoint b either precedes both endpoints or follows both, i.e.
    orient(a,b) != orient(b,c)
where orient(x,y) for x < y (as values) is True iff x precedes y.

Claims audited:
  (a) Lemma E / lem:transfer, M = 0 mod 4:  b5<b3  <=>  t3<t5
      (tested in the STRONGER form: no A2/A3 hypotheses at all;
       both violating combinations must be UNSAT under AP-freeness alone)
  (b) FLIP (thm:flip), M = 0 mod 8:  AP-free + A2 + A3 + (b5<b3) + A1 UNSAT
      where A1: t5<b5, A2: t3<b6, A3: t10<b3.

Two independent methods:
  1. SAT (pysat Cadical195), pair variables + AP xor clauses + FULL EAGER
     transitivity (M <= 200), or lazy transitivity refinement (M = 1000;
     sound for UNSAT verdicts: clauses added are all logically valid).
  2. My own derivation engine (a6_engine.py): parity union-find over the
     AP xor constraints + digraph transitive closure + tiny DPLL splits.
"""
import sys, time
sys.setrecursionlimit(100000)
from pysat.solvers import Cadical195


# ---------- shared: instance construction from the paper's definitions ----

def block(M):
    return list(range(M + 1, 2 * M + 1))          # (M, 2M]

def aps(M):
    """All APs a<b<c inside (M,2M]."""
    out = []
    for d in range(1, (M - 1) // 2 + 1):
        for a in range(M + 1, 2 * M + 1 - 2 * d):
            out.append((a, a + d, a + 2 * d))
    return out

def c3_pairs(M):
    b = lambda j: M + j
    t = lambda i: 2 * M - i
    return {
        "A1": (t(5), b(5)),    # t5 < b5
        "A2": (t(3), b(6)),    # t3 < b6
        "A3": (t(10), b(3)),   # t10 < b3
        "b5<b3": (b(5), b(3)),
        "b3<b5": (b(3), b(5)),
        "t3<t5": (t(3), t(5)),
        "t5<t3": (t(5), t(3)),
    }


# ---------- method 1: SAT ------------------------------------------------

class SatOrder:
    """Pair-variable encoding. var(u,v) for u<v (values), True = u precedes v."""

    def __init__(self, M, eager_transitivity=True):
        self.M = M
        self.vals = block(M)
        self.n = len(self.vals)
        self.idx = {v: i for i, v in enumerate(self.vals)}
        self.clauses = []
        self._mkvars()
        self._ap_clauses()
        self.eager = eager_transitivity
        if eager_transitivity:
            self._trans_clauses()

    def _mkvars(self):
        self.var = {}
        c = 0
        n = self.n
        for i in range(n):
            for j in range(i + 1, n):
                c += 1
                self.var[(i, j)] = c
        self.nv = c

    def lit(self, u, v):
        """literal for 'value u precedes value v'"""
        iu, iv = self.idx[u], self.idx[v]
        if iu < iv:
            return self.var[(iu, iv)]
        return -self.var[(iv, iu)]

    def _ap_clauses(self):
        for a, b, c in aps(self.M):
            la, lb = self.lit(a, b), self.lit(b, c)
            # forbid a<b<c  (la & lb)  and  c<b<a  (~la & ~lb)  => la xor lb
            self.clauses.append([-la, -lb])
            self.clauses.append([la, lb])

    def _trans_clauses(self):
        n = self.n
        V = self.var
        cl = self.clauses
        for i in range(n):
            for j in range(i + 1, n):
                xij = V[(i, j)]
                for k in range(j + 1, n):
                    xjk = V[(j, k)]
                    xik = V[(i, k)]
                    cl.append([-xij, -xjk, xik])   # i<j & j<k -> i<k
                    cl.append([xij, xjk, -xik])    # j<i & k<j -> k<i
    def solve(self, assumptions):
        """assumptions: list of (u,v) meaning u precedes v. Returns 'UNSAT'/'SAT'."""
        s = Cadical195(bootstrap_with=self.clauses)
        assum = [self.lit(u, v) for (u, v) in assumptions]
        r = s.solve(assumptions=assum)
        if not r:
            s.delete()
            return "UNSAT", None
        model = s.get_model()
        s.delete()
        return "SAT", model

    # ---- lazy transitivity refinement (for large M). Sound for UNSAT. ----
    def solve_lazy(self, assumptions, max_rounds=400, add_per_round=30000,
                   verbose=False):
        assert not self.eager
        n = self.n
        s = Cadical195(bootstrap_with=self.clauses)
        assum = [self.lit(u, v) for (u, v) in assumptions]
        t0 = time.time()
        for rnd in range(1, max_rounds + 1):
            if not s.solve(assumptions=assum):
                s.delete()
                return "UNSAT", rnd
            model = s.get_model()
            pol = {}
            for i in range(n):
                for j in range(i + 1, n):
                    pol[(i, j)] = model[self.var[(i, j)] - 1] > 0
            # succ/pred bitsets from tournament
            succ = [0] * n
            pred = [0] * n
            for (i, j), p in pol.items():
                if p:
                    succ[i] |= 1 << j
                    pred[j] |= 1 << i
                else:
                    succ[j] |= 1 << i
                    pred[i] |= 1 << j
            # find violated transitivity triples: u->v, and w with v->w, w->u
            added = 0
            for i in range(n):
                for j in range(i + 1, n):
                    u, v = (i, j) if pol[(i, j)] else (j, i)
                    W = succ[v] & pred[u]
                    if W:
                        w = W.bit_length() - 1
                        # add both transitivity clauses for the triple {u,v,w}
                        trip = sorted([u, v, w])
                        a, b_, c = trip
                        xab, xbc, xac = (self.var[(a, b_)], self.var[(b_, c)],
                                         self.var[(a, c)])
                        s.add_clause([-xab, -xbc, xac])
                        s.add_clause([xab, xbc, -xac])
                        added += 2
                        if added >= add_per_round:
                            break
                if added >= add_per_round:
                    break
            if verbose:
                print(f"    [lazy] round {rnd}: SAT, added {added} clauses "
                      f"({time.time()-t0:.1f}s)", flush=True)
            if added == 0:
                s.delete()
                return "SAT", rnd   # genuine total order found
        s.delete()
        return "UNKNOWN", max_rounds


# ---------- sanity: a known AP-free order must satisfy the AP clauses ----

def oddeven_order(vals):
    """Odds before evens, recursively (paper: parity heuristic, DEGS)."""
    if len(vals) <= 2:
        return list(vals)
    odds = [v for v in vals if v % 2]
    evens = [v for v in vals if v % 2 == 0]
    # recurse on (v-1)/2 resp v/2 images to keep AP-freeness
    o = [2 * x + 1 for x in oddeven_order(sorted(set((v - 1) // 2 for v in odds)))]
    e = [2 * x for x in oddeven_order(sorted(set(v // 2 for v in evens)))]
    return o + e

def check_order_apfree(M, order):
    pos = {v: i for i, v in enumerate(order)}
    bad = 0
    for a, b, c in aps(M):
        pa, pb, pc = pos[a], pos[b], pos[c]
        if pa < pb < pc or pc < pb < pa:
            bad += 1
    return bad


# ---------- driver -------------------------------------------------------

def run_scale(M, eager=True, lazy_verbose=False):
    P = c3_pairs(M)
    print(f"== M = {M}  (mod 8 = {M % 8})  n = {M} ==", flush=True)
    t0 = time.time()
    enc = SatOrder(M, eager_transitivity=eager)
    print(f"   built: {enc.nv} vars, {len(enc.clauses)} clauses "
          f"({time.time()-t0:.1f}s)", flush=True)

    def go(name, assumptions, expect):
        t = time.time()
        if eager:
            verdict, _ = enc.solve(assumptions)
            extra = ""
        else:
            verdict, rnds = enc.solve_lazy(assumptions, verbose=lazy_verbose)
            extra = f" [{rnds} lazy rounds]"
        ok = "AGREE" if verdict == expect else "*** DISAGREE ***"
        print(f"   {name:34s} -> {verdict:7s} (expect {expect}) {ok}{extra} "
              f"({time.time()-t:.1f}s)", flush=True)
        return verdict

    results = {}
    # T0 sanity: AP alone satisfiable
    results["T0"] = go("T0: AP-freeness alone", [], "SAT")
    # Lemma E, strong form (no A2/A3): both mismatched orientations UNSAT
    results["E1"] = go("E1: AP + b5<b3 + t5<t3", [P["b5<b3"], P["t5<t3"]], "UNSAT")
    results["E2"] = go("E2: AP + b3<b5 + t3<t5", [P["b3<b5"], P["t3<t5"]], "UNSAT")
    # Lemma E, exact task form (with A2+A3) — implied by E1/E2 but run anyway
    results["E1h"] = go("E1h: + A2,A3 as well", [P["A2"], P["A3"], P["b5<b3"], P["t5<t3"]], "UNSAT")
    results["E2h"] = go("E2h: + A2,A3 as well", [P["A2"], P["A3"], P["b3<b5"], P["t3<t5"]], "UNSAT")
    # FLIP
    results["F"] = go("F:  AP + A2 + A3 + b5<b3 + A1", [P["A2"], P["A3"], P["b5<b3"], P["A1"]], "UNSAT")
    # FLIP sanity: without A1 should be SAT (otherwise FLIP would be vacuous)
    results["Fs"] = go("Fs: AP + A2 + A3 + b5<b3 (no A1)", [P["A2"], P["A3"], P["b5<b3"]], "SAT")
    # C3 itself
    results["C3"] = go("C3: AP + A1 + A2 + A3", [P["A1"], P["A2"], P["A3"]], "UNSAT")
    return results


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "small"
    # sanity of the AP enumeration via a known valid order
    for M in (48, 56):
        o = oddeven_order(block(M))
        assert sorted(o) == block(M)
        bad = check_order_apfree(M, o)
        print(f"sanity M={M}: odd-even order violates {bad} APs (expect 0)")
        assert bad == 0
    if which == "small":
        for M in (48, 52, 56, 104):
            if M == 52:
                # control scale, 4 mod 8: C3 should be SAT there (prop:cores)
                P = c3_pairs(M)
                enc = SatOrder(M)
                v, _ = enc.solve([P["A1"], P["A2"], P["A3"]])
                print(f"== M = 52 control (4 mod 8): C3 -> {v} (expect SAT) "
                      f"{'AGREE' if v == 'SAT' else '*** DISAGREE ***'}")
                continue
            run_scale(M, eager=True)
    elif which == "200":
        run_scale(200, eager=True)
    elif which == "1000":
        run_scale(1000, eager=False, lazy_verbose=True)
