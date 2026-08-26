"""e124_prep_catalogue: rebuild the e122 core catalogue (core -> firing
scales + inferred residue law) from data/e122_n2_residue_partial.json
(the final e122 output was lost with the session at M=135; the partial
checkpoint covers the complete sweep M = 16..128, every residue).

Output: data/e122_n2_residue_recon.json with the same "cores"/"rungs"
schema e124_family_miner expects, plus a law survey printed per pair.

Run: .venv/bin/python experiments/e124_prep_catalogue.py
"""
import json

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"


def infer_law(unsat_ms, sweep):
    if not unsat_ms:
        return {"law": "never"}
    uset = set(unsat_ms)
    for r in (1, 2, 3, 4, 5):
        mod = 2 ** r
        S = sorted({m % mod for m in unsat_ms})
        cand = [m for m in sweep if m % mod in S]
        misses = [m for m in cand if m not in uset]
        if not misses:
            return {"law": f"M mod {mod} in {S}", "mod": mod, "S": S,
                    "from": min(unsat_ms), "anomalies": []}
        m0 = max(misses) + 1
        cand_above = [m for m in cand if m >= m0]
        if cand_above and all(m in uset for m in cand_above) \
                and len(cand_above) >= 5:
            spor = sorted(m for m in unsat_ms if m < m0)
            return {"law": f"M mod {mod} in {S}, M >= {m0}"
                           f" ({len(spor)} sporadic below)",
                    "mod": mod, "S": S, "from": m0, "anomalies": spor}
    return {"law": "irregular", "unsat_n": len(unsat_ms)}


def main():
    d = json.load(open(f"{BASE}/e122_n2_residue_partial.json"))
    per_m = d["per_m"]
    sweep = [row["M"] for row in per_m]
    print(f"sweep reconstructed: M = {sweep[0]}..{sweep[-1]} "
          f"({len(sweep)} scales)")
    core_ms = {}
    rung_unsat = {}
    for row in per_m:
        M = row["M"]
        for xs, rec in row["pairs"].items():
            x = int(xs)
            if rec["full"] == "UNSAT":
                rung_unsat.setdefault(x, []).append(M)
            for cr in rec["cores"]:
                sig = tuple(map(tuple, cr))
                core_ms.setdefault((x, sig), []).append(M)
    out = {"sweep": sweep, "rungs": {}, "cores": []}
    for x in sorted(rung_unsat):
        law = infer_law(rung_unsat[x], sweep)
        out["rungs"][str(x)] = {"unsat": rung_unsat[x], "law": law}
        print(f"FULL RUNG {{{x},{x+1}}}: {law['law']} "
              f"[{len(rung_unsat[x])}/{len(sweep)} scales]")
    for (x, sig), ms in sorted(core_ms.items()):
        law = infer_law(ms, sweep)
        out["cores"].append({"x": x, "core": [list(u) for u in sig],
                             "ms": ms, "law": law})
    json.dump(out, open(f"{BASE}/e122_n2_residue_recon.json", "w"),
              indent=1)
    # ---- survey: per pair, laws by size, with an eye on 2 mod 4 ----
    for x in sorted(rung_unsat):
        ent = [e for e in out["cores"] if e["x"] == x]
        print(f"\n=== pair {{{x},{x+1}}}: {len(ent)} distinct cores ===")
        bysize = {}
        for e in ent:
            bysize.setdefault(len(e["core"]), []).append(e)
        for sz in sorted(bysize):
            rows = sorted(bysize[sz], key=lambda e: -len(e["ms"]))
            print(f"  size {sz}: {len(rows)} cores")
            for e in rows[:12]:
                pretty = ",".join(f"t{i}<b{j}" for i, j in e["core"])
                print(f"    {{{pretty}}}: {e['law']['law']} "
                      f"[{len(e['ms'])} scales, "
                      f"{e['ms'][0]}..{e['ms'][-1]}]")
    print(f"\n-> {BASE}/e122_n2_residue_recon.json")


if __name__ == "__main__":
    main()
