"""e176b_deepx_sweep: full-branch closure verification of every
verified e175 cell at DEEP x (x0 + {32, 40, 48}), two in-class
scales each -- extends the parametric grid from 4 to ~7 x-values per
cell, closure-only (no solver).

Run: .venv/bin/python experiments/e176b_deepx_sweep.py
Output: data/e176b_deepx.{json,log}
"""
import json

from e174_param_lanes import lanes_for, LAW
from e175_param_template import (branches_ok, seeds_for,
                                 in_class_scales, e174_thr, OUT, BASE)


def main():
    recs = [r for r in json.load(open(OUT))["cells"] if r.get("ok")]
    out, allok = {}, True
    for rec in sorted(recs, key=lambda r: r["cell"]):
        lane, x0, istar = rec["lane"], rec["x0"], rec["istar"]
        r8 = (x0 + LAW[lane]) % 8
        rows = []
        for dx in (32, 40, 48):
            x = x0 + dx
            K = lanes_for(x)[lane]
            Ms = in_class_scales(r8, K, istar, 2, e174_thr(lane, x))
            for M in Ms:
                for hn, Sk, ph in (("hi", rec["S_hi"], "lo"),
                                   ("lo", rec["S_lo"], "hi")):
                    sv = branches_ok(M, seeds_for(
                        M, [tuple(K[k]) for k in Sk], istar, ph),
                        rec["ladders"][hn])
                    rows.append((x, M, hn, sv))
                    if sv:
                        allok = False
        bad = [r for r in rows if r[3]]
        out[rec["cell"]] = rows
        print(f"{rec['cell']}: x={[x0+32, x0+40, x0+48]} "
              f"{'ALL BRANCHES CLOSE' if not bad else bad}", flush=True)
    json.dump(out, open(f"{BASE}/e176b_deepx.json", "w"), indent=1)
    print("DEEP-X SWEEP:", "ALL OK" if allok else "FAILURES", flush=True)


if __name__ == "__main__":
    main()
