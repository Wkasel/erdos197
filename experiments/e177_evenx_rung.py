"""e177_evenx_rung: FRONT N2-PARAMETRIC side probe -- the full rung
for EVEN-x adjacent pairs {x, x+1} (x = 12, 14, 16, 18, 20, 22).

The N2 catalogue/lane theory is built on odd-x pairs (attackers
{odd, even}).  Theorem N2-COMPLETE is stated for odd x; this probe
records the machine status of the even-x pairs' FULL single-block
rung (all units of both attackers, j >= 1, i >= 0, values in-block)
at every M in 16..120 -- if UNSAT everywhere, even-x pairs are rung-
dead too (their own lane anatomy left to future work); any SAT scale
is an honest scope note.

Run: python3 e177_evenx_rung.py [Mmax]
Output: data/e177_evenx_rung.json
"""
import json
import os
import sys
import time

from e124b_lane_probe import build_base

BASE = os.environ.get(
    "E_BASE", "/Users/will/Dev/personal/tasks/math/erdos197/data")


def rung_units(x, M):
    out = []
    for a in (x, x + 1):
        for j in range(1, (a - 1) // 2 + 1):
            i = a - 2 * j
            if i < 0:
                continue
            z, y = 2 * M - i, M + j
            if M < z <= 2 * M and M < y <= 2 * M and z != y:
                out.append((i, j))
    return out


def main():
    mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    xs = [12, 14, 16, 18, 20, 22]
    verdicts = {x: [] for x in xs}
    t0 = time.time()
    for M in range(16, mmax + 1):
        all_units = set()
        for x in xs:
            all_units |= set(rung_units(x, M))
        sol, sel = build_base(M, all_units)
        row = []
        for x in xs:
            us = [u for u in rung_units(x, M) if u in sel]
            sat = sol.solve(assumptions=[sel[u] for u in us])
            verdicts[x].append((M, "SAT" if sat else "UNSAT"))
            if sat:
                row.append(f"SAT:{x}")
        sol.delete()
        if row or M % 24 == 0:
            print(f"M={M}: {' '.join(row) or 'all UNSAT'} "
                  f"({time.time()-t0:.0f}s)", flush=True)
    out = {}
    for x in xs:
        sats = [m for m, v in verdicts[x] if v == "SAT"]
        out[x] = {"sat_scales": sats,
                  "verdict": "UNSAT everywhere" if not sats else
                  f"SAT at {sats}"}
        print(f"pair {{{x},{x+1}}}: {out[x]['verdict']}")
    json.dump(out, open(f"{BASE}/e177_evenx_rung.json", "w"), indent=1)


if __name__ == "__main__":
    main()
