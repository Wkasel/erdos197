"""e123b_diagonal_solver_xval: solver cross-validation of the diagonal
schema (e123).  For p in {5,7,9,11,13} (pairs {15,16}..{39,40}):

  - AP + C3(p) = {t_p<b_p, t_{p-2}<b_{p+1}, t_{p+5}<b_{p-2}} must be
    UNSAT at every M in the flip class M/2 = p+3 mod 4 (sample scales),
    and SAT at every M in the complementary class M/2 = p+1 mod 4
    (schema sharpness is real, not just schema inapplicability);
  - the FULL rung OG_{3p,3p+1}(M) must be UNSAT in BOTH classes
    (the other catalogue cores cover the complementary class).

Complete encoding (AP + full transitivity), Cadical195.

Run: .venv/bin/python experiments/e123b_diagonal_solver_xval.py
Output: data/e123b_diagonal_xval.json
"""
import json
import time

from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e123b_diagonal_xval.json"


def build_base(M, units):
    n = M
    var = {}
    c = 0
    for p_ in range(n):
        for q in range(p_ + 1, n):
            c += 1
            var[(p_, q)] = c

    def o(u, w):
        p_, q = u - M - 1, w - M - 1
        return var[(p_, q)] if p_ < q else -var[(q, p_)]

    cl = []
    for y in range(M + 2, 2 * M):
        d = 1
        while y + d <= 2 * M and y - d > M:
            a, b = y - d, y + d
            cl.append([-o(a, y), -o(y, b)])
            cl.append([-o(b, y), -o(y, a)])
            d += 1
    for p_ in range(n):
        for q in range(p_ + 1, n):
            vpq = var[(p_, q)]
            for r in range(q + 1, n):
                vqr, vpr = var[(q, r)], var[(p_, r)]
                cl.append([-vpq, -vqr, vpr])
                cl.append([vpq, vqr, -vpr])
    sel = {}
    nv = c
    for (i, j) in sorted(units):
        z, y = 2 * M - i, M + j
        assert M < z <= 2 * M and z != y
        nv += 1
        sel[(i, j)] = nv
        cl.append([o(z, y), -nv])
    return Cadical195(bootstrap_with=cl), sel


def main():
    out = {"rows": [], "fail": []}
    for p in (5, 7, 9, 11, 13):
        x = 3 * p
        core = [(p, p), (p - 2, p + 1), (p + 5, p - 2)]
        rung = [(a - 2 * j, j) for a in (x, x + 1)
                for j in range(1, a // 2 + 1)]
        flip_mod8 = (2 * (p + 3)) % 8
        comp_mod8 = (2 * (p + 1)) % 8
        base = ((4 * p + 15) // 16) * 16
        flip_ms = [M for M in range(base, base + 130, 4)
                   if M % 8 == flip_mod8][:4] + \
                  [M for M in (256, 260) if M % 8 == flip_mod8]
        comp_ms = [M for M in range(base, base + 130, 4)
                   if M % 8 == comp_mod8][:4] + \
                  [M for M in (256, 260) if M % 8 == comp_mod8]
        for M in sorted(set(flip_ms + comp_ms)):
            t0 = time.time()
            sol, sel = build_base(M, set(core) | set(rung))
            v_core = sol.solve(assumptions=[sel[u] for u in core])
            v_rung = sol.solve(assumptions=[sel[u] for u in rung])
            sol.delete()
            cls = "flip" if M % 8 == flip_mod8 else "comp"
            exp_core = "SAT" if cls == "comp" else "UNSAT"
            got_core = "SAT" if v_core else "UNSAT"
            got_rung = "SAT" if v_rung else "UNSAT"
            ok_core = got_core == exp_core
            ok_rung = got_rung == "UNSAT"
            row = {"p": p, "x": x, "M": M, "class": cls,
                   "core": got_core, "core_expected": exp_core,
                   "rung": got_rung, "t": round(time.time() - t0, 1)}
            out["rows"].append(row)
            mark = "OK" if (ok_core and ok_rung) else "MISMATCH"
            if not (ok_core and ok_rung):
                out["fail"].append(row)
            print(f"p={p} M={M} ({cls}, M%8={M%8}): C3(p) {got_core} "
                  f"(exp {exp_core}), rung {got_rung} (exp UNSAT) "
                  f"[{mark}, {row['t']}s]", flush=True)
        json.dump(out, open(DATA, "w"), indent=1)
    print(f"failures: {len(out['fail'])}")
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}")


if __name__ == "__main__":
    main()
