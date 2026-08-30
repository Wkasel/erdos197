"""e174_param_lanes: FRONT N2-PARAMETRIC step 1 -- the full 8-lane
residue system, probed parametrically in x.

The claim under test (the N2-COMPLETE lane table): for pair {x, x+1},
x odd >= 11, EIGHT translation-invariant lanes cover all eight residue
classes of M mod 8 (units in (i, j) coords, t_i = 2M - i, b_j = M + j,
attacker i + 2j in {x, x+1}):

  even-M classes                               law (M mod 8)
  L1 = K4e(x) = {(x-11,6),(x-8,4),(x-5,3)}     x + 1   [NEW: from K11_r4]
  L3 = B6(x)  = {(x-8,4),(x-6,3),(x-1,1)}      x + 3   [e124b]
  L5 = A4a(x) = {(x-11,6),(x-10,5),(x-9,5),(x-8,4)}  x + 5  [e124b]
       A4d(x) = {(x-10,5),(x-9,5),(x-8,4),(x-5,3)}   x + 5  [e124b]
  L7 = B2(x)  = {(x-9,5),(x-6,3),(x-4,2)}      x + 7   [e124b]
  odd-M classes
  L0 = K3(x)  = {(x-10,5),(x-7,4),(x-4,2)}     x       [NEW: from K11_r3]
  L2 = C(x)   = {(x-11,6),(x-9,5),(x-6,3)}     x + 2   [e124b]
  L4 = K7(x)  = {(x-7,4),(x-5,3),(x-2,1)}      x + 4   [NEW: from K11_r7]
  L6 = K1(x)  = {(x-11,6),(x-8,4),(x-6,3)}     x + 6   [NEW: from K11_r1]

The four NEW lanes are the (2,0)-translates of the bespoke {11,12}
cells of e124m (K11_r4/r3/r7/r1); their laws were never probed off
x = 11.  x = 23..29 extends the catalogue past e122 (x = 23 is the
first x = 7 mod 8 pair off the diagonal; its dyadic cell M = 0 mod 8
is exactly the K4e lane: x + 1 = 0 mod 8).

Probe protocol per instance (x, lane): solver UNSAT at every in-class
M in [Mlo(x), Mmax] (threshold recorded = first M with all later
in-class M UNSAT), plus SAT controls at the complementary class r + 4
(three scales).  One solver per M with all units selectable
(e124b-style).

Run: .venv/bin/python experiments/e174_param_lanes.py [Mmax] [xs...]
Output: data/e174_param_lanes.json (+ .log via tee)
"""
import json
import sys
import time

from e124b_lane_probe import build_base, infer_law

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"


def lanes_for(x):
    out = {
        "K4e": [(x - 11, 6), (x - 8, 4), (x - 5, 3)],
        "B6": [(x - 8, 4), (x - 6, 3), (x - 1, 1)],
        "A4a": [(x - 11, 6), (x - 10, 5), (x - 9, 5), (x - 8, 4)],
        "A4d": [(x - 10, 5), (x - 9, 5), (x - 8, 4), (x - 5, 3)],
        "B2": [(x - 9, 5), (x - 6, 3), (x - 4, 2)],
        "K3": [(x - 10, 5), (x - 7, 4), (x - 4, 2)],
        "C": [(x - 11, 6), (x - 9, 5), (x - 6, 3)],
        "K7": [(x - 7, 4), (x - 5, 3), (x - 2, 1)],
        "K1": [(x - 11, 6), (x - 8, 4), (x - 6, 3)],
    }
    for name, us in out.items():
        for (i, j) in us:
            assert i + 2 * j in (x, x + 1), (x, name, i, j)
    return out


LAW = {"K4e": 1, "B6": 3, "A4a": 5, "A4d": 5, "B2": 7,
       "K3": 0, "C": 2, "K7": 4, "K1": 6}


def main():
    mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 152
    xs = [int(a) for a in sys.argv[2:]] or [11, 13, 15, 17, 19, 21,
                                            23, 25, 27, 29]
    inst, all_units = {}, set()
    for x in xs:
        for name, us in lanes_for(x).items():
            inst[(x, name)] = us
            all_units |= set(us)
    # which M values do we need?  in-class Ms and control Ms per inst
    need = {}          # M -> [(x, name, kind)]
    for (x, name), us in inst.items():
        r = (x + LAW[name]) % 8
        mlo = max(16, x + 5)
        ms = [m for m in range(mlo, mmax + 1) if m % 8 == r]
        ctrl = [m for m in range(mlo + 24, mmax + 1)
                if m % 8 == (r + 4) % 8][:3]
        for m in ms:
            need.setdefault(m, []).append((x, name, "class"))
        for m in ctrl:
            need.setdefault(m, []).append((x, name, "ctrl"))
    fires, ctrl_sat = {k: [] for k in inst}, {k: [] for k in inst}
    t00 = time.time()
    for M in sorted(need):
        t0 = time.time()
        sol, sel = build_base(M, all_units)
        row = []
        for (x, name, kind) in need[M]:
            us = inst[(x, name)]
            if any(u not in sel for u in us):
                continue
            sat = sol.solve(assumptions=[sel[u] for u in us])
            if kind == "class":
                if not sat:
                    fires[(x, name)].append(M)
                else:
                    row.append(f"SAT!{name}({x})")
            else:
                ctrl_sat[(x, name)].append((M, sat))
                if not sat:
                    row.append(f"CTRL-UNSAT!{name}({x})")
        sol.delete()
        print(f"M={M}: {' '.join(row) or 'ok'}  ({time.time()-t0:.1f}s,"
              f" total {time.time()-t00:.0f}s)", flush=True)
    print("\n=== per-instance verdicts (in-class UNSAT from threshold;"
          " controls at r+4) ===")
    out = {"mmax": mmax, "xs": xs, "lanes": []}
    bad = 0
    for (x, name), ms in sorted(fires.items(),
                                key=lambda kv: (kv[0][1], kv[0][0])):
        r = (x + LAW[name]) % 8
        mlo = max(16, x + 5)
        cls = [m for m in range(mlo, mmax + 1) if m % 8 == r]
        misses = [m for m in cls if m not in ms]
        thr = None
        if ms:
            thr = ms[0] if not misses else \
                (max(misses) + 8 if max(misses) < ms[-1] else None)
        ok = thr is not None
        ctl = ctrl_sat[(x, name)]
        ctl_ok = all(s for _, s in ctl)
        if not ok:
            bad += 1
        print(f"{name}(x={x}) r{r}: {'UNSAT from M=' + str(thr) if ok else 'LAW FAILS'}"
              f" ({len(ms)}/{len(cls)} in-class scales"
              f"{', misses ' + str(misses[:6]) if misses else ''});"
              f" controls {'all SAT' if ctl_ok else [c for c in ctl if not c[1]]}",
              flush=True)
        out["lanes"].append({"lane": name, "x": x, "r": r,
                             "units": [list(u) for u in inst[(x, name)]],
                             "fires": ms, "threshold": thr,
                             "misses": misses, "controls": ctl})
    json.dump(out, open(f"{BASE}/e174_param_lanes.json", "w"), indent=1)
    print(f"\n{len(inst) - bad}/{len(inst)} instances lawful"
          f" -> {BASE}/e174_param_lanes.json")


if __name__ == "__main__":
    main()
