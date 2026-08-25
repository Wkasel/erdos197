"""e102_kernel_mine: TASK T round 2 -- enriched half-scale kernel for the C3 flip.

Round-1 (e101) killed the bare kernel: the three residue-free A2+A3
consequences among the odd anchors (b5<b3, t3<b3, t3<t5), descended by
h+(v) = (v+1)/2 to scale m = M/2, do NOT force b3'<t2' at m == 0 mod 4.

Round-2 idea: the correct kernel hypotheses are the descents of ALL odd-odd
literals forced by AP + FULL C3 at level 1.  These are minable at the SAT
residues (M == 4 mod 8, where AP+C3 has models); in offset language at scale
m = M/2 they should be M-independent.  Pipeline:

  E. mine: for M in R4 = {44,52,60,68}: probe every odd-odd pair (u,w) under
     AP + C3; record forced literals; map to level-2 offset labels
     (u -> (u+1)/2 -> b_i / t_j relative to m = M/2); intersect across M.
  F. kernel: for m in sweep (even 16..64): AP(m) + core units -> SAT/UNSAT.
     Predict UNSAT iff m == 0 mod 4  (matching C3 UNSAT iff 2m == 0 mod 8).
  G. minimize: greedy deletion at the smallest UNSAT scale; re-sweep the
     minimal kernel across all m; sanity: SAT at every m == 2 mod 4.
  H. overfit guard: each minimal-kernel pullback literal re-probed as forced
     at fresh r4 scales M = 76, 84 (not used in mining).

Usage: python e102_kernel_mine.py
Output: data/e102_kernel.json
"""
import itertools
import json
import time

import numpy as np
from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e102_kernel.json"


class Interval:
    def __init__(self, lo):
        self.lo, self.hi = lo, 2 * lo
        self.V = list(range(lo + 1, 2 * lo + 1))
        self.n = len(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.var = {}
        c = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                c += 1
                self.var[(i, j)] = c
        self.ap = []
        for y in self.V:
            d = 1
            while y + d <= self.hi:
                x, z = y - d, y + d
                d += 1
                if x > self.lo:
                    self.ap.append([-self.o(x, y), -self.o(y, z)])
                    self.ap.append([-self.o(z, y), -self.o(y, x)])
        self.pool = []

    def lit(self, i, j):
        return self.var[(i, j)] if i < j else -self.var[(j, i)]

    def o(self, u, w):
        return self.lit(self.idx[u], self.idx[w])

    def solver(self, units):
        return Cadical195(bootstrap_with=self.ap + [[u] for u in units]
                          + self.pool)

    def lazy(self, sol, assum=()):
        n = self.n
        while True:
            if not sol.solve(assumptions=list(assum)):
                return "UNSAT"
            model = set(l for l in sol.get_model() if l > 0)
            B = np.zeros((n, n), dtype=bool)
            for (i, j), vv in self.var.items():
                if vv in model:
                    B[i, j] = True
                else:
                    B[j, i] = True
            R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
            miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
            ii, jj = np.nonzero(miss)
            if len(ii) == 0:
                return "SAT"
            new = []
            for i, j in zip(ii[:30000], jj[:30000]):
                ks = np.nonzero(B[i] & B[:, j])[0]
                new.append([-self.lit(i, int(ks[0])),
                            -self.lit(int(ks[0]), j), self.lit(i, j)])
            sol.append_formula(new)
            self.pool.extend(new)

    def status(self, units):
        sol = self.solver(units)
        try:
            return self.lazy(sol)
        finally:
            sol.delete()


def c3_units(iv, M):
    return [iv.o(2 * M - 5, M + 5), iv.o(2 * M - 3, M + 6),
            iv.o(2 * M - 10, M + 3)]


def lvl2_label(u, M):
    """Level-1 odd value u -> level-2 offset label at scale m = M/2."""
    m = M // 2
    w = (u + 1) // 2
    db, dt = w - m, 2 * m - w
    return f"b{db}" if db <= dt else f"t{dt}"


def label_to_value(lbl, m):
    if lbl.startswith("b"):
        return m + int(lbl[1:])
    return 2 * m - int(lbl[1:])


# ------------------------------------------------------- E. mining at r4
def mine_odd_forced(M):
    """All odd-odd literals forced by AP + C3 at scale M (M == 4 mod 8).
    Returns set of offset-literal strings 'L1<L2' in level-2 language."""
    iv = Interval(M)
    sol = iv.solver(c3_units(iv, M))
    odds = [v for v in iv.V if v % 2 == 1]
    forced = set()
    t0 = time.time()
    assert iv.lazy(sol) == "SAT", f"M={M}: AP+C3 unexpectedly UNSAT"
    for u, w in itertools.combinations(odds, 2):
        if iv.lazy(sol, [iv.o(u, w)]) == "UNSAT":
            forced.add((w, u))
        elif iv.lazy(sol, [iv.o(w, u)]) == "UNSAT":
            forced.add((u, w))
    sol.delete()
    lab = {f"{lvl2_label(u, M)}<{lvl2_label(w, M)}" for u, w in forced}
    print(f"[E] M={M}: {len(forced)} forced odd-odd literals "
          f"({time.time()-t0:.0f}s); offset-labels: {sorted(lab)}", flush=True)
    return lab


# ------------------------------------------------------- F. kernel sweep
def kernel_status(m, core):
    iv = Interval(m)
    units = []
    for s in core:
        a, b = s.split("<")
        units.append(iv.o(label_to_value(a, m), label_to_value(b, m)))
    return iv.status(units)


# ------------------------------------------------------- G. minimization
def minimize(m, core):
    """Greedy deletion: keep UNSAT at scale m; drop largest offsets first."""
    def offsz(s):
        a, b = s.split("<")
        return max(int(a[1:]), int(b[1:]))
    cur = sorted(core, key=offsz, reverse=True)
    i = 0
    while i < len(cur):
        trial = cur[:i] + cur[i + 1:]
        if kernel_status(m, trial) == "UNSAT":
            cur = trial
        else:
            i += 1
    return sorted(cur)


def main():
    t00 = time.time()
    out = {}

    # E: mine at r4 scales
    mined = {}
    for M in (44, 52, 60, 68):
        mined[M] = mine_odd_forced(M)
    core = set.intersection(*mined.values())
    out["mined_per_M"] = {str(M): sorted(s) for M, s in mined.items()}
    out["core"] = sorted(core)
    print(f"\n[E] intersection core ({len(core)} literals): {sorted(core)}",
          flush=True)

    # F: kernel sweep
    sweep = {}
    for m in range(16, 65, 2):
        st = kernel_status(m, core)
        sweep[m] = st
        print(f"[F] m={m} (mod4={m % 4}): kernel {st}", flush=True)
    out["kernel_sweep"] = {str(m): s for m, s in sweep.items()}
    ok0 = all(s == "UNSAT" for m, s in sweep.items() if m % 4 == 0)
    ok2 = all(s == "SAT" for m, s in sweep.items() if m % 4 == 2)
    print(f"[F] dichotomy: UNSAT at all m==0(4): {ok0}; "
          f"SAT at all m==2(4): {ok2}", flush=True)
    out["dichotomy"] = {"unsat_all_mod4_0": ok0, "sat_all_mod4_2": ok2}

    # G: minimize (only meaningful if some scale is UNSAT)
    if any(s == "UNSAT" for s in sweep.values()):
        m0 = min(m for m, s in sweep.items() if s == "UNSAT")
        mk = minimize(m0, core)
        out["minimal_kernel"] = mk
        print(f"\n[G] minimal kernel at m={m0} ({len(mk)} literals): {mk}",
              flush=True)
        resweep = {}
        for m in range(16, 65, 2):
            resweep[m] = kernel_status(m, mk)
        out["minimal_resweep"] = {str(m): s for m, s in resweep.items()}
        g0 = all(s == "UNSAT" for m, s in resweep.items() if m % 4 == 0)
        g2 = all(s == "SAT" for m, s in resweep.items() if m % 4 == 2)
        print(f"[G] minimal kernel dichotomy: UNSAT@0(4)={g0} SAT@2(4)={g2}",
              flush=True)
        print(f"[G] resweep detail: {resweep}", flush=True)
        out["minimal_dichotomy"] = {"unsat_all_mod4_0": g0,
                                    "sat_all_mod4_2": g2}

        # H: overfit guard at fresh r4 scales
        guard = {}
        for M in (76, 84):
            iv = Interval(M)
            sol = iv.solver(c3_units(iv, M))
            assert iv.lazy(sol) == "SAT"
            all_ok = True
            for s in mk:
                a, b = s.split("<")
                u = 2 * label_to_value(a, M // 2) - 1
                w = 2 * label_to_value(b, M // 2) - 1
                st = iv.lazy(sol, [iv.o(w, u)])
                if st != "UNSAT":
                    all_ok = False
                    print(f"[H] M={M}: pullback of {s} NOT forced!", flush=True)
            sol.delete()
            guard[M] = all_ok
            print(f"[H] M={M}: all minimal-kernel pullbacks forced: {all_ok}",
                  flush=True)
        out["fresh_r4_guard"] = {str(k): v for k, v in guard.items()}

    json.dump(out, open(DATA, "w"), indent=1)
    print(f"\nDone ({time.time()-t00:.0f}s) -> {DATA}", flush=True)


if __name__ == "__main__":
    main()
