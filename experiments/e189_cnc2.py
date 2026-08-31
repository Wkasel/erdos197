"""e189_cnc2: cube-and-conquer for the e127 bal family, cadical backend
(notes/87).  v2 after the kissat-per-cube fiasco: kissat is ~2 orders
slower than cadical on this family, so cubes are solved by PERSISTENT
pysat Cadical195 instances (one per worker, loaded once, cubes as
assumptions, conflict-budgeted).  Learned clauses persist across cubes
inside a worker — the incremental advantage monolithic solving never
shares across restarts.

Cubes: colorings of a prefix of B0 (b0full = all balanced B0 colorings
with M+1 pinned to team A by the team-swap symmetry; b0part k = 2^k
prefix colorings, balance-pruned).  UNDET cubes (conflict budget hit)
are re-split on the next --k2 free values with a doubled budget, up to
--rounds times.  All-UNSAT => UNSAT.  Any SAT => SAT (model decoded and
audited via e127.audit before the verdict is trusted).

Usage:
  e189_cnc2.py --cnf data/cnf/bal16v5.cnf --M 16 --v 5 --mode b0full \
      --workers 48 --conf 3000000 --tag bal16v5
"""
import argparse
import itertools
import json
import multiprocessing as mp
import os
import sys
import time

sys.path.insert(0, "/root/e/experiments")

G = {}


def init_worker(cnf_path):
    from pysat.formula import CNF
    from pysat.solvers import Cadical195
    cnf = G.get("clauses")
    if cnf is None:
        cnf = CNF(from_file=cnf_path).clauses
    s = Cadical195(bootstrap_with=cnf)
    G["solver"] = s


def solve_cube(task):
    cid, units, conf = task
    s = G["solver"]
    s.conf_budget(conf)
    t0 = time.time()
    r = s.solve_limited(assumptions=units)
    el = round(time.time() - t0, 1)
    if r is True:
        model = s.get_model()
        return {"cube": cid, "verdict": "SAT", "time": el,
                "model": model, "units": units}
    if r is False:
        return {"cube": cid, "verdict": "UNSAT", "time": el}
    return {"cube": cid, "verdict": "UNDET", "time": el, "units": units}


def gen_cubes(M, ai, mode, k, B0=None):
    if B0 is None:
        B0 = list(range(M + 1, 2 * M + 1))
    import math
    half = math.ceil(len(B0) / 2)
    pin = ai[B0[0]]
    if mode == "b0full":
        rest = B0[1:]
        for i, asub in enumerate(itertools.combinations(rest, half - 1)):
            aset = set(asub)
            yield str(i), [pin] + [ai[v] if v in aset else -ai[v]
                                   for v in rest]
    else:
        rest = B0[1:1 + k]
        for i in range(1 << k):
            bits = [(i >> j) & 1 for j in range(k)]
            na, nb = 1 + sum(bits), k - sum(bits)
            if na > half or nb > half:
                continue
            yield str(i), [pin] + [ai[v] if b else -ai[v]
                                   for v, b in zip(rest, bits)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cnf", required=True)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--v", type=int, required=True)
    ap.add_argument("--mode", choices=("b0full", "b0part"),
                    default="b0full")
    ap.add_argument("--k", type=int, default=12)
    ap.add_argument("--k2", type=int, default=4)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--workers", type=int, default=48)
    ap.add_argument("--conf", type=int, default=3000000)
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    meta = json.load(open(a.cnf + ".meta.json"))
    ai = {int(v): var for v, var in meta["ai"].items()}
    cube_B0 = meta["blocks"][0] if "blocks" in meta else None
    chain = "blocks" in meta
    outdir = os.path.dirname(a.cnf)
    resf = os.path.join(outdir, f"cnc2_{a.tag}.jsonl")
    from pysat.formula import CNF
    print(f"loading {a.cnf} ...", flush=True)
    G["clauses"] = CNF(from_file=a.cnf).clauses
    done = set()
    if os.path.exists(resf):
        for line in open(resf):
            try:
                r = json.loads(line)
                if r["verdict"] in ("UNSAT", "SAT"):
                    done.add(r["cube"])
            except Exception:
                pass
    cubes = [(cid, u, a.conf)
             for cid, u in gen_cubes(a.M, ai, a.mode, a.k, B0=cube_B0)
             if cid not in done]
    allv = (sorted(int(v) for v in meta["ai"]) if chain
            else list(range(a.M + 1, 8 * a.M + 1)))
    print(f"cnc2 {a.tag}: {len(cubes)} cubes ({len(done)} done), "
          f"conf={a.conf}, workers={a.workers}", flush=True)
    t0 = time.time()
    ctx = mp.get_context("fork")
    sat_row = None
    stats = {"UNSAT": len(done), "SAT": 0, "UNDET": 0}
    rnd = 0
    conf = a.conf
    while cubes and rnd < a.rounds and not sat_row:
        rnd += 1
        undet = []
        nd = 0
        with ctx.Pool(a.workers, initializer=init_worker,
                      initargs=(a.cnf,)) as pool:
            for r in pool.imap_unordered(solve_cube, cubes,
                                         chunksize=1):
                nd += 1
                with open(resf, "a") as f:
                    row = dict(r)
                    row.pop("model", None)
                    f.write(json.dumps(row) + "\n")
                if r["verdict"] == "SAT":
                    sat_row = r
                    with open(os.path.join(
                            outdir, f"cnc2_{a.tag}.model.json"),
                            "w") as f:
                        json.dump(r, f)
                    pool.terminate()
                    break
                stats[r["verdict"]] += 1
                if r["verdict"] == "UNDET":
                    undet.append(r)
                if nd % 250 == 0:
                    print(f"  r{rnd} {nd}/{len(cubes)} {stats} "
                          f"t={time.time()-t0:.0f}s", flush=True)
        if sat_row:
            break
        # resplit undetermined cubes
        nxt = []
        for r in undet:
            base = r["units"]
            used = {abs(u) for u in base}
            free = [ai[v] for v in allv if ai[v] not in used][:a.k2]
            for i in range(1 << a.k2):
                bits = [(i >> j) & 1 for j in range(a.k2)]
                nxt.append((f"{r['cube']}.{i}",
                            base + [f if b else -f
                                    for f, b in zip(free, bits)],
                            conf * 2))
        stats["UNDET"] = 0
        conf *= 2
        cubes = nxt
        if cubes:
            print(f"round {rnd+1}: {len(cubes)} resplit cubes, "
                  f"conf={conf}", flush=True)
    if sat_row and chain:
        print(f"CNC2 VERDICT {a.tag}: SAT cube={sat_row['cube']} "
              f"(chain family: model saved, audit via e173 decode "
              f"pending)", flush=True)
    elif sat_row:
        # decode + audit before trusting
        import e127_seam_budget as e127
        model = set(l for l in sat_row["model"] if l > 0)
        n = 7 * a.M
        nP = n * (n - 1) // 2
        V = list(range(a.M + 1, 8 * a.M + 1))
        idx = {v: i for i, v in enumerate(V)}
        offA, _ = e127._mk_vars(n, start=1)
        offB, _ = e127._mk_vars(n, start=nP + 1)
        aiv = {V[i]: 2 * nP + 1 + i for i in range(n)}

        def posneg(l):
            return (l in model) if l > 0 else (abs(l) not in model)

        colA = [v for v in V if aiv[v] in model]
        colB = [v for v in V if aiv[v] not in model]
        import math
        bounds = {}
        for bn, blk in (("B0", [v for v in V if v <= 2 * a.M]),
                        ("B1", [v for v in V
                                if 2 * a.M < v <= 4 * a.M]),
                        ("B2", [v for v in V if v > 4 * a.M])):
            base = math.ceil(len(blk) / 2)
            bounds[bn] = {"A": base, "B": base}
        info = {"A": colA, "B": colB, "bounds": bounds}
        for team, off, col in (("A", offA, colA), ("B", offB, colB)):
            def lit(u, w):
                i, j = idx[u], idx[w]
                return off[(i, j)] if i < j else -off[(j, i)]
            wins = {v: 0 for v in col}
            for i2, u in enumerate(col):
                for w in col[i2 + 1:]:
                    if posneg(lit(u, w)):
                        wins[u] += 1
                    else:
                        wins[w] += 1
            info[f"order{team}"] = sorted(col, key=lambda v: -wins[v])
        errs, anatomy = e127.audit(a.M, bounds, a.v, a.v, info)
        print(f"CNC2 VERDICT {a.tag}: SAT cube={sat_row['cube']} "
              f"audit={'OK' if not errs else errs}", flush=True)
    else:
        rows = [json.loads(l) for l in open(resf)]
        solved = {str(r["cube"]) for r in rows
                  if r["verdict"] == "UNSAT"}
        unres = []
        for r in rows:
            c = str(r["cube"])
            if r["verdict"] != "UNDET":
                continue
            kids = [str(x["cube"]) for x in rows
                    if str(x["cube"]).startswith(c + ".")]
            if not kids:
                unres.append(c)
        # a cube counts refuted iff all its children are (recursively);
        # simplest sound check: no UNDET leaf without a complete refuted
        # child set — verify by checking every UNDET has 2^k2 UNSAT kids
        def refuted(c):
            if c in solved:
                return True
            kids = [str(x["cube"]) for x in rows
                    if str(x["cube"]).startswith(c + ".")
                    and str(x["cube"]).count(".") == c.count(".") + 1]
            if len(kids) < (1 << a.k2):
                return False
            return all(refuted(kc) for kc in set(kids))
        top = sorted({str(r["cube"]) for r in rows
                      if "." not in str(r["cube"])})
        bad = [c for c in top if not refuted(c)]
        if not bad:
            print(f"CNC2 VERDICT {a.tag}: UNSAT (all "
                  f"{len(top)} cubes refuted, "
                  f"{time.time()-t0:.0f}s wall)", flush=True)
        else:
            print(f"CNC2 VERDICT {a.tag}: UNDECIDED "
                  f"({len(bad)} unresolved of {len(top)}) {bad[:10]}",
                  flush=True)
    print(f"final {stats} wall={time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
