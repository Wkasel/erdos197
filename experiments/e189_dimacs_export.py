"""e189_dimacs_export: eager DIMACS export of the stuck-instance families
(notes/87 solver-engineering sprint).

Families:
  bal      : the e127.solve_budget JOINT decision (window (M,8M], exact
             balance when --bounds omitted, per-team seam-inversion
             budgets vA=vB=v).  Clauses captured VERBATIM from
             e127_seam_budget.solve_budget via a recording solver class
             (zero transcription risk); var numbering identical.
  c3core   : e166 single-block AP+C3 (or og) on (M,2M], order vars
             o(u,w), with FULL transitivity materialized (2*C(n,3)
             clauses) instead of the lazy CEGAR loop.  Same var ids as
             e166 (pair (i<j) -> row[i]+(j-i)).
  coupled  : e165b coupled 3-block (2,2,2) core with FULL per-team
             transitivity materialized.  Base (AP/seam/card) clauses
             replicated from e165b's generator; var ids identical.

Sidecar meta json: var counts + the color-var map (for cube-and-conquer
and model decode).  decode-bal re-audits a SAT model with e127.audit.

Usage:
  e189_dimacs_export.py bal --M 16 --v 5 --out bal16v5.cnf
  e189_dimacs_export.py c3core --M 512 --out c3_512.cnf [--attacks c3]
  e189_dimacs_export.py coupled --M 128 --out cpl128.cnf [--bounds 2,2,2]
  e189_dimacs_export.py decode-bal --M 16 --v 5 --model kissat_out.txt
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


# ------------------------------------------------------------ recorder
class Recorder:
    """pysat-solver-shaped clause sink; returns UNSAT without solving."""
    captured = None

    def __init__(self, bootstrap_with=None, **kw):
        self.cls = [list(c) for c in (bootstrap_with or [])]
        Recorder.captured = self

    def add_clause(self, c):
        self.cls.append(list(c))

    def append_formula(self, cs):
        for c in cs:
            self.add_clause(c)

    def solve(self, **kw):
        return False

    def get_model(self):
        return []

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def write_dimacs(path, clauses, nvars=None, extra_comment=""):
    if nvars is None:
        nvars = max((max(abs(l) for l in c) for c in clauses if c), default=0)
    with open(path, "w") as f:
        if extra_comment:
            f.write(f"c {extra_comment}\n")
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        buf = []
        for c in clauses:
            buf.append(" ".join(map(str, c)) + " 0")
            if len(buf) >= 1000000:
                f.write("\n".join(buf) + "\n")
                buf = []
        if buf:
            f.write("\n".join(buf) + "\n")
    return nvars, len(clauses)


# ------------------------------------------------------------ bal (e127)
def export_bal(M, v, out, bounds_arg=None):
    import e127_seam_budget as e127
    abs_bounds = None
    if bounds_arg:
        abs_bounds = tuple(int(x) for x in bounds_arg.split(","))
    verdict, el, info = e127.solve_budget(M, abs_bounds, v, v,
                                          solver=Recorder)
    rec = Recorder.captured
    assert verdict == "UNSAT" and rec is not None
    n = 7 * M
    nP = n * (n - 1) // 2
    V = list(range(M + 1, 8 * M + 1))
    ai = {V[i]: 2 * nP + 1 + i for i in range(n)}
    nvars, ncl = write_dimacs(out, rec.cls,
                              extra_comment=f"e189 bal M={M} v={v} "
                                            f"bounds={bounds_arg or 'bal'}")
    meta = {"family": "bal", "M": M, "v": v, "bounds": bounds_arg,
            "n": n, "nP": nP, "nvars": nvars, "nclauses": ncl,
            "ai": {str(val): var for val, var in ai.items()},
            "info_bounds": info.get("bounds")}
    with open(out + ".meta.json", "w") as f:
        json.dump(meta, f)
    print(f"bal M={M} v={v}: vars={nvars} clauses={ncl} -> {out}")


def decode_bal(M, v, model_path, bounds_arg=None):
    """Parse a kissat/cms 'v ' model, rebuild the e127 info dict, audit."""
    import e127_seam_budget as e127
    lits = []
    for line in open(model_path):
        if line.startswith("v ") or line.startswith("v\t"):
            lits += [int(x) for x in line.split()[1:] if x != "0"]
    model = set(l for l in lits if l > 0)
    n = 7 * M
    nP = n * (n - 1) // 2
    V = list(range(M + 1, 8 * M + 1))
    idx = {val: i for i, val in enumerate(V)}
    ai = {V[i]: 2 * nP + 1 + i for i in range(n)}
    offA, _ = e127._mk_vars(n, start=1)
    offB, _ = e127._mk_vars(n, start=nP + 1)

    def posneg(l):
        return (l in model) if l > 0 else (abs(l) not in model)

    def litT(off):
        def lit(u, w):
            i, j = idx[u], idx[w]
            return off[(i, j)] if i < j else -off[(j, i)]
        return lit

    litA, litB = litT(offA), litT(offB)
    colA = [val for val in V if ai[val] in model]
    colB = [val for val in V if ai[val] not in model]
    import math
    B0 = [x for x in V if x <= 2 * M]
    B1 = [x for x in V if 2 * M < x <= 4 * M]
    B2 = [x for x in V if x > 4 * M]
    abs_bounds = None
    if bounds_arg:
        abs_bounds = tuple(int(x) for x in bounds_arg.split(","))
    bounds = {}
    for bi, (bn, blk) in enumerate((("B0", B0), ("B1", B1), ("B2", B2))):
        base = (math.ceil(len(blk) / 2) if abs_bounds is None
                else abs_bounds[bi])
        bounds[bn] = {"A": base, "B": base}
    info = {"A": colA, "B": colB, "bounds": bounds}
    for team, lit, col in (("A", litA, colA), ("B", litB, colB)):
        wins = {val: 0 for val in col}
        for i, u in enumerate(col):
            for w in col[i + 1:]:
                if posneg(lit(u, w)):
                    wins[u] += 1
                else:
                    wins[w] += 1
        info[f"order{team}"] = sorted(col, key=lambda val: -wins[val])
    errs, anatomy = e127.audit(M, bounds, v, v, info)
    print(f"decode-bal M={M} v={v}: audit errs={errs or 'NONE'}")
    print(json.dumps({k: anatomy[k] for k in anatomy} if not errs else {},
                     default=str)[:2000])
    return 0 if not errs else 2


# ------------------------------------------------------------ chain (e173)
def export_chain(kind, M, v, out):
    """e173_telescope solve_chain cells (pump / fresh), captured
    verbatim by patching e173.Cadical195 with a dumping recorder that
    writes the DIMACS inside solve_chain's fork before reporting UNSAT.
    kind fresh + M=24, v=65 is the F(24;65) stuck cell."""
    import e173_telescope as e173

    class DumpSolver(Recorder):
        def solve(self, **kw):
            write_dimacs(out, self.cls,
                         extra_comment=f"e189 chain {kind} M={M} v={v}")
            return False

    orig = e173.Cadical195
    e173.Cadical195 = DumpSolver
    try:
        blocks = e173.dyadic_blocks(M // 2, 8 * M)
        if kind == "pump":
            budgets = [("vdn", [0, 1], 0), ("vup", [1, 2], v)]
        else:
            budgets = [("s0_zero", [0], 0), ("vup", [1, 2], v)]
        verdict, el, info = e173.solve_chain(blocks, budgets,
                                             f"e189_{kind}_M{M}_v{v}",
                                             time_budget=86400.0)
        assert verdict == "UNSAT", verdict
    finally:
        e173.Cadical195 = orig
    V = [x for blk in blocks for x in blk]
    n = len(V)
    nP = n * (n - 1) // 2
    ai = {V[i]: 2 * nP + 1 + i for i in range(n)}
    meta = {"family": "chain", "kind": kind, "M": M, "v": v, "n": n,
            "nP": nP, "blocks": [list(b) for b in blocks],
            "ai": {str(val): var for val, var in ai.items()}}
    with open(out + ".meta.json", "w") as f:
        json.dump(meta, f)
    print(f"chain {kind} M={M} v={v}: n={n} -> {out} (+meta)")


# ------------------------------------------------------------ c3core (e166)
def export_c3core(M, out, attacks="c3"):
    lo, hi = M, 2 * M
    V = list(range(lo + 1, hi + 1))
    n = len(V)
    row = [i * (2 * n - i - 1) // 2 for i in range(n)]
    nP = n * (n - 1) // 2

    def o(u, v):
        i, j = u - lo - 1, v - lo - 1
        if i < j:
            return row[i] + (j - i)
        return -(row[j] + (i - j))

    if attacks == "c3":
        atk = [(2 * M - 5, M + 5), (2 * M - 3, M + 6), (2 * M - 10, M + 3)]
    else:
        atk = []
        for x in (15, 16):
            for j in range(1, x // 2 + 1):
                z = hi + 2 * j - x
                if lo < z <= hi:
                    atk.append((z, M + j))
    nap = sum(min(y - lo - 1, hi - y) for y in V)
    ntr = n * (n - 1) * (n - 2) // 6
    ncl = 2 * nap + len(atk) + 2 * ntr
    t0 = time.time()
    with open(out, "w") as f:
        f.write(f"c e189 c3core M={M} attacks={attacks} eager-full-trans\n")
        f.write(f"p cnf {nP} {ncl}\n")
        buf = []

        def flush(force=False):
            if len(buf) >= 1000000 or force:
                f.write("\n".join(buf) + "\n")
                buf.clear()

        for y in V:
            d = 1
            while y - d > lo and y + d <= hi:
                x, z = y - d, y + d
                buf.append(f"{-o(x, y)} {-o(y, z)} 0")
                buf.append(f"{-o(z, y)} {-o(y, x)} 0")
                d += 1
            flush()
        for z, y in atk:
            buf.append(f"{o(z, y)} 0")
        for i in range(n):
            ri = row[i]
            for j in range(i + 1, n):
                xij = ri + (j - i)
                rj = row[j]
                for k in range(j + 1, n):
                    xjk = rj + (k - j)
                    xik = ri + (k - i)
                    buf.append(f"-{xij} -{xjk} {xik} 0")
                    buf.append(f"{xij} {xjk} -{xik} 0")
                flush()
        flush(force=True)
    meta = {"family": "c3core", "M": M, "attacks": attacks, "n": n,
            "nvars": nP, "nclauses": ncl}
    with open(out + ".meta.json", "w") as f:
        json.dump(meta, f)
    print(f"c3core M={M} {attacks}: vars={nP} clauses={ncl} "
          f"({time.time()-t0:.0f}s) -> {out}")


# ------------------------------------------------------------ coupled (e165b)
def export_coupled(M, out, bounds="2,2,2", support="core"):
    from pysat.card import CardEnc, EncType
    bnds = tuple(int(x) for x in bounds.split(","))
    if support == "core":
        V = sorted(set(range(M + 1, 2 * M + 1))
                   | set(range(3 * M - 15, 6 * M + 16)))
    else:
        V = list(range(M + 1, 8 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    row = [i * (2 * n - i - 1) // 2 for i in range(n)]
    nP = n * (n - 1) // 2
    ai = {v: 2 * nP + 1 + i for i, v in enumerate(V)}

    def mk_lit(off):
        def lit(u, v):
            i, j = idx[u], idx[v]
            if i < j:
                return off + row[i] + (j - i)
            return -(off + row[j] + (i - j))
        return lit

    litA, litB = mk_lit(0), mk_lit(nP)
    Vs = set(V)
    B0 = [v for v in V if v <= 2 * M]
    B1 = [v for v in V if 2 * M < v <= 4 * M]
    B2 = [v for v in V if v > 4 * M]
    base = []
    for team, lit, g in (("A", litA, lambda v: -ai[v]),
                         ("B", litB, lambda v: ai[v])):
        for b in V:
            for d in range(1, min(b - V[0], V[-1] - b) + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    gg = [g(a), g(b), g(c)]
                    base.append(gg + [-lit(a, b), -lit(b, c)])
                    base.append(gg + [lit(a, b), lit(b, c)])
        for lowblk, highblk in ((B0, B1), (B1, B2), (B0, B2)):
            for u in lowblk:
                for v in highblk:
                    base.append([g(u), g(v), lit(u, v)])
    tid = 2 * nP + n
    for bi, blk in enumerate((B0, B1, B2)):
        bnd = bnds[bi]
        if bnd <= 0:
            continue
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blk],
                                  bound=bnd, top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            base += [list(c) for c in enc.clauses]
    ntr = n * (n - 1) * (n - 2) // 6
    ncl = len(base) + 4 * ntr
    nvars = max(tid, max((max(abs(l) for l in c) for c in base)))
    t0 = time.time()
    with open(out, "w") as f:
        f.write(f"c e189 coupled M={M} bounds={bnds} support={support} "
                f"eager-full-trans\n")
        f.write(f"p cnf {nvars} {ncl}\n")
        buf = [" ".join(map(str, c)) + " 0" for c in base]
        f.write("\n".join(buf) + "\n")
        buf = []
        for off in (0, nP):
            for i in range(n):
                ri = row[i] + off
                ri0 = row[i]
                for j in range(i + 1, n):
                    xij = ri + (j - i)
                    rj = row[j] + off
                    for k in range(j + 1, n):
                        xjk = rj + (k - j)
                        xik = ri + (k - i)
                        buf.append(f"-{xij} -{xjk} {xik} 0")
                        buf.append(f"{xij} {xjk} -{xik} 0")
                    if len(buf) >= 1000000:
                        f.write("\n".join(buf) + "\n")
                        buf = []
        if buf:
            f.write("\n".join(buf) + "\n")
    meta = {"family": "coupled", "M": M, "bounds": bnds,
            "support": support, "n": n, "nP": nP, "nvars": nvars,
            "nclauses": ncl,
            "ai": {str(v): var for v, var in ai.items()}}
    with open(out + ".meta.json", "w") as f:
        json.dump(meta, f)
    print(f"coupled M={M} {bnds} {support}: vars={nvars} clauses={ncl} "
          f"({time.time()-t0:.0f}s) -> {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=("bal", "c3core", "coupled",
                                       "chain", "decode-bal"))
    ap.add_argument("--kind", default="fresh",
                    choices=("pump", "fresh"))
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--v", type=int, default=0)
    ap.add_argument("--out", default=None)
    ap.add_argument("--attacks", default="c3")
    ap.add_argument("--bounds", default=None)
    ap.add_argument("--support", default="core")
    ap.add_argument("--model", default=None)
    a = ap.parse_args()
    if a.family == "bal":
        export_bal(a.M, a.v, a.out, a.bounds)
    elif a.family == "c3core":
        export_c3core(a.M, a.out, a.attacks)
    elif a.family == "coupled":
        export_coupled(a.M, a.out, a.bounds or "2,2,2", a.support)
    elif a.family == "chain":
        export_chain(a.kind, a.M, a.v, a.out)
    else:
        sys.exit(decode_bal(a.M, a.v, a.model, a.bounds))


if __name__ == "__main__":
    main()
