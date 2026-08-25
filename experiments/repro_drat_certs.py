"""repro_drat_certs: emit machine-checkable DRAT certificates for the two
headline C3-UNSAT instances of the reproducibility package (AUDIT A4).

Statement certified (per scale M, M = 0 mod 8):

    On the block (M, 2M] there is NO total order that
      (a) avoids monotone 3-term APs (for every AP x < y < z inside the
          block, forbid x,y,z appearing in that positional order or in
          the reversed order z,y,x), and
      (b) satisfies the C3 core units:
              A1: t5 < b5   i.e. 2M-5 before M+5
              A2: t3 < b6   i.e. 2M-3 before M+6
              A3: t10 < b3  i.e. 2M-10 before M+3.

Encodings (both are *order* encodings over pair variables x_{u,v} = "u
positioned before v", one variable per unordered pair, sign = direction):

  M = 128 (EAGER): full O(n^3) transitivity -- 2 clauses per unordered
    triple -- plus the AP clauses and the 3 units.  The DIMACS file is a
    complete axiomatization of "AP-free total order + C3"; the DRAT proof
    certifies its unsatisfiability with no side conditions at all.

  M = 512 (LAZY-AUDITED): eager transitivity would need ~44.5M clauses,
    so the CNF contains the AP clauses, the 3 units, and only those
    transitivity instances collected by a lazy refinement loop until the
    formula became UNSAT.  Every clause of the emitted CNF is then
    re-audited *from the file* by audit_cnf(): each one must decode to a
    C3 unit, a genuine AP-triple clause, or a syntactic transitivity
    instance (-x_{a,b} v -x_{b,c} v x_{a,c}).  Since units/AP/transitivity
    clauses are all sound for AP-free total orders, UNSAT of this CNF
    (certified by the DRAT proof) implies the full statement.

Verification (independent checker):
    tools/drat-trim/drat-trim data/certs/c3_M128.cnf data/certs/c3_M128.drat
    tools/drat-trim/drat-trim data/certs/c3_M512.cnf data/certs/c3_M512.drat
must print "s VERIFIED".

Run: .venv/bin/python experiments/repro_drat_certs.py [M ...]
     (default: 128 512)
Output: data/certs/c3_M{M}.cnf + .drat (+ audit report on stdout)
"""
import os
import sys
import time

import numpy as np
from pysat.solvers import Cadical153, Cadical195

# NB (audit A4 finding): the proof-logging solve uses Cadical153, NOT
# Cadical195.  python-sat 1.9.dev15's Cadical195 proof capture emits an
# INCOMPLETE DRAT trace at large scale: at M=512 the captured proof ends
# with the empty clause yet formula+lemmas do not unit-propagate to a
# conflict (drat-trim: "conflict claimed, but not detected"; confirmed
# independently by a propagate() check), while the same pipeline at
# M<=264 is complete.  Cadical153's file-based capture is complete at all
# scales tried and its proofs verify.  Cadical195 remains in use for the
# lazy clause-collection loop, which needs no proof.

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERTS = os.path.join(ROOT, "data", "certs")


# ---------------------------------------------------------------- encoding
def make_lit(M):
    """Pair-variable literal map.  Elements M+1..2M, indices 0..n-1,
    var id for index pair i<j is i*n + j + 1 (sparse but injective);
    lit(u, w) > 0 iff the variable asserts 'u before w'."""
    V = list(range(M + 1, 2 * M + 1))
    n = len(V)
    pos = {v: k for k, v in enumerate(V)}

    def lit(u, w):
        i, j = pos[u], pos[w]
        assert i != j
        s = 1 if i < j else -1
        if i > j:
            i, j = j, i
        return s * (i * n + j + 1)

    return V, n, pos, lit


def ap_triples(M):
    for y in range(M + 2, 2 * M):
        for d in range(1, min(y - M - 1, 2 * M - y) + 1):
            yield (y - d, y, y + d)


def c3_units(M):
    return [(2 * M - 5, M + 5), (2 * M - 3, M + 6), (2 * M - 10, M + 3)]


def base_cnf(M, lit):
    cl = [[lit(u, w)] for (u, w) in c3_units(M)]
    for (x, y, z) in ap_triples(M):
        cl.append([-lit(x, y), -lit(y, z)])
        cl.append([-lit(z, y), -lit(y, x)])
    return cl


# ------------------------------------------------------- clause collection
def eager_trans(M, n):
    """All transitivity clauses: for indices i<j<k with vars a=x_ij,
    b=x_jk, c=x_ik: (-a -b c) and (a b -c)."""
    cl = []
    for i in range(n):
        for j in range(i + 1, n):
            a = i * n + j + 1
            for k in range(j + 1, n):
                b = j * n + k + 1
                c = i * n + k + 1
                cl.append([-a, -b, c])
                cl.append([a, b, -c])
    return cl


def lazy_trans(M, cnf, V, n, pos, lit):
    """Refinement loop (same style as e115_audit_sat): solve, find broken
    transitivity in the model, add those instances, repeat until UNSAT.
    Returns the collected transitivity clauses."""
    sol = Cadical195(bootstrap_with=cnf)
    got = []
    rounds = 0
    while True:
        if not sol.solve():
            print(f"  lazy loop: UNSAT after {rounds} rounds, "
                  f"{len(got)} transitivity clauses", flush=True)
            sol.delete()
            return got
        model = set(sol.get_model())
        B = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(i + 1, n):
                if (i * n + j + 1) in model:
                    B[i, j] = True
                else:
                    B[j, i] = True
        Bu = B.astype(np.uint8)
        viol = ((Bu @ Bu) > 0) & B.T
        ii, jj = np.nonzero(viol)
        assert len(ii) > 0, "SAT with closed model: instance is SAT!"
        new = []
        for i, j in zip(ii[:20000], jj[:20000]):
            ks = np.nonzero(B[i] & B[:, j])[0]
            k = int(ks[0])
            new.append([-lit(V[i], V[k]), -lit(V[k], V[j]),
                        lit(V[i], V[j])])
        got.extend(new)
        sol.append_formula(new)
        rounds += 1


# ------------------------------------------------------------ file output
def write_dimacs(path, nvars, clauses):
    with open(path, "w") as f:
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def write_drat(path, proof):
    with open(path, "w") as f:
        for line in proof:
            f.write(line + "\n")


# ---------------------------------------------------------------- auditing
def audit_cnf(path, M):
    """Re-read the emitted DIMACS and prove every clause is sound for
    AP-free total orders with C3: it must decode to (1) a C3 unit,
    (2) an AP clause of a genuine in-block AP, or (3) a transitivity
    instance.  Anything else fails the audit."""
    V, n, pos, lit = make_lit(M)

    def unvar(v):
        i, j = divmod(v - 1, n)
        assert 0 <= i < j < n, ("bad var", v)
        return i, j

    units = {tuple(sorted((lit(u, w),))) for (u, w) in c3_units(M)}
    aps = set()
    for (x, y, z) in ap_triples(M):
        aps.add(tuple(sorted((-lit(x, y), -lit(y, z)))))
        aps.add(tuple(sorted((-lit(z, y), -lit(y, x)))))
    kinds = {"unit": 0, "ap": 0, "trans": 0}
    with open(path) as f:
        header = f.readline().split()
        assert header[:2] == ["p", "cnf"], header
        for ln, raw in enumerate(f):
            c = [int(t) for t in raw.split()]
            assert c[-1] == 0, ("no terminator", ln)
            c = c[:-1]
            key = tuple(sorted(c))
            if len(c) == 1 and key in units:
                kinds["unit"] += 1
                continue
            if len(c) == 2 and key in aps:
                kinds["ap"] += 1
                continue
            if len(c) == 3:
                # transitivity instance iff, reading the clause as the
                # implication (~p & ~q) -> r for SOME choice of conclusion
                # literal r, the premise edges chain and the conclusion
                # closes the chain: edges (a,b),(b,c) => (a,c).
                def edge(l):
                    i, j = unvar(abs(l))
                    return (i, j) if l > 0 else (j, i)

                ok = False
                for r in range(3):
                    concl = edge(c[r])
                    prem = [edge(-c[s]) for s in range(3) if s != r]
                    (a1, b1), (a2, b2) = prem
                    if b1 == a2 and concl == (a1, b2):
                        ok = True
                    if b2 == a1 and concl == (a2, b1):
                        ok = True
                assert ok, ("unauditable 3-clause", ln, c)
                kinds["trans"] += 1
                continue
            raise AssertionError(("unauditable clause", ln, c))
    assert kinds["unit"] == 3, kinds
    assert kinds["ap"] == 2 * len(list(ap_triples(M))), kinds
    print(f"  audit {os.path.basename(path)}: OK -- "
          f"{kinds['unit']} units, {kinds['ap']} AP clauses, "
          f"{kinds['trans']} transitivity instances, nothing else")
    return True


# -------------------------------------------------------------------- main
def emit(M):
    t0 = time.time()
    V, n, pos, lit = make_lit(M)
    cnf = base_cnf(M, lit)
    mode = "eager" if M <= 256 else "lazy-audited"
    print(f"== C3 cert at M={M} ({mode}) ==", flush=True)
    if mode == "eager":
        cnf += eager_trans(M, n)
    else:
        cnf += lazy_trans(M, cnf, V, n, pos, lit)
    print(f"  final CNF: {len(cnf)} clauses; proof-logging solve...",
          flush=True)
    sol = Cadical153(bootstrap_with=cnf, with_proof=True)
    res = sol.solve()
    assert res is False, f"M={M}: expected UNSAT, got {res}"
    proof = sol.get_proof()
    sol.delete()
    os.makedirs(CERTS, exist_ok=True)
    cnf_path = os.path.join(CERTS, f"c3_M{M}.cnf")
    drat_path = os.path.join(CERTS, f"c3_M{M}.drat")
    write_dimacs(cnf_path, n * n, cnf)
    write_drat(drat_path, proof)
    print(f"  UNSAT; proof {len(proof)} lines "
          f"({os.path.getsize(drat_path)//1024} KiB); "
          f"cnf {os.path.getsize(cnf_path)//1024} KiB; "
          f"{time.time()-t0:.0f}s", flush=True)
    audit_cnf(cnf_path, M)
    return cnf_path, drat_path


def main():
    scales = [int(a) for a in sys.argv[1:]] or [128, 512]
    for M in scales:
        assert M % 8 == 0, "C3-UNSAT certs are for M = 0 mod 8"
        emit(M)
    print("ALL CERTS EMITTED + AUDITED")


if __name__ == "__main__":
    main()
