"""e191_land_s1_check: integrity-patch item 2 (second external review).

Machine check of the CORRECTED Lemma LAND recurrence bounds (notes/84
SS1.2) on random parameter tuples in BOTH sigma cases, plus a fresh
re-verification of Theorem S1 (notes/84 SS1.3) by direct simulation of
the forced spiral.

Part LAND (10^4 tuples per sigma):
  the abstract deviation recurrence  delta' = -delta/2 (delta even),
  delta' = -(delta + sigma*g)/2 (delta odd), g odd:
  (G)  general bound |delta'| <= (|delta| + g)/2         [both sigma]
  (P+) sigma = +1: every positive deviation arises from a negative
       one and equals |delta|/2 (even) or (|delta|-g)/2 (odd) —
       hence <= |delta|/2                                 [sigma=+1 ONLY]
  (P-) sigma = -1: the (P+) bound FAILS — violations are counted and
       REQUIRED to occur (>= 1), incl. the reviewer's explicit
       counterexample q=1, p=4, g=3, r*=p, tau=8, h=14 run through
       the REAL spiral map (not the abstract recurrence)
  (L)  g | delta0: lands at 0 in K <= |delta0/g| + 2 steps with
       sup bound |delta_n| <= max(|delta0|, g); if delta0 < 0 the
       orbit minimum is delta0                            [both sigma]
  (X)  g not| delta0: never lands (checked to 400 steps) and
       delta_n == (-inv2)^n delta0 (mod g)                [both sigma]

Part S1 (10^4 admissible tuples (q, g, t, N)):
  simulate the ACTUAL forced spiral at head w = 3t + 2q with target
  u = 2t + q (residues forced by parity of x_n, as in notes/84
  SS1.1-1.3), and assert every claim of the S1 proof: seed/RL AP in
  window, landing x_K = u, positivity with x0 the orbit minimum,
  head-avoidance x_n < w via A/2 < t + q, all reflections in [1, N].

Run: .venv/bin/python experiments/e191_land_s1_check.py
Artifacts: data/e191_land_s1_check.json
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "e191_land_s1_check.json"
random.seed(191)

N_TUPLES = 10_000


def step(delta, sigma, g):
    if delta % 2 == 0:
        return -delta // 2
    return -(delta + sigma * g) // 2


def part_land():
    res = {"tuples_per_sigma": N_TUPLES, "general_bound_fail": 0,
           "pos_dev_from_pos_fail": 0, "pos_dev_bound_fail_plus": 0,
           "pos_dev_bound_viol_minus": 0, "land_fail": 0,
           "sup_bound_fail": 0, "min_orbit_fail": 0,
           "nonland_fail": 0, "mod_track_fail": 0}
    for sigma in (+1, -1):
        for _ in range(N_TUPLES):
            g = 2 * random.randint(0, 120) + 1
            m0 = random.randint(-60, 60)
            offr = random.choice([0, 0, 0, random.randint(1, g - 1)
                                  if g > 1 else 0])
            delta0 = sigma * g * m0 + offr  # g | delta0 iff offr == 0
            landed = False
            deltas = [delta0]
            d = delta0
            for _n in range(400):
                nd = step(d, sigma, g)
                # (G) general bound, both sigma
                if abs(nd) > (abs(d) + g) // 2:
                    res["general_bound_fail"] += 1
                if nd > 0:
                    if sigma == +1 and d > 0:
                        # (b1) claim, sigma=+1 ONLY: positives only
                        # arise from negatives
                        res["pos_dev_from_pos_fail"] += 1
                    if sigma == +1:
                        exact = (abs(d) // 2 if d % 2 == 0
                                 else (abs(d) - g) // 2)
                        if d > 0 or nd != exact or 2 * nd > abs(d):
                            res["pos_dev_bound_fail_plus"] += 1
                    elif 2 * nd > abs(d):
                        res["pos_dev_bound_viol_minus"] += 1  # expected!
                d = nd
                deltas.append(d)
                if d == 0:
                    landed = True
                    break
            if offr == 0:
                K = deltas.index(0) if landed else None
                if (not landed) or K > abs(m0) + 2:
                    res["land_fail"] += 1
                if max(abs(x) for x in deltas) > max(abs(delta0), g):
                    res["sup_bound_fail"] += 1
                if delta0 < 0 and min(deltas) != delta0:
                    res["min_orbit_fail"] += 1
            else:
                if landed:
                    res["nonland_fail"] += 1
                # (X) delta_n == (-inv2)^n delta0 (mod g), g odd > 1
                if g > 1:
                    inv2 = pow(2, -1, g)
                    for n, dn in enumerate(deltas):
                        if dn % g != (pow(-inv2, n, g) * delta0) % g:
                            res["mod_track_fail"] += 1
                            break
    return res


def real_spiral(h, q, p, N, target, max_steps=10_000):
    """The forced spiral of notes/84 SS1.2 at head h: x0 = (h-r0)/2
    with r0 = the unique residue in {q,p} with r0 == h (mod 2);
    x_{n+1} = h - (x_n + r_{n+1})/2, r_{n+1} == x_n (mod 2).
    Returns (xs, ok_admissible, landed)."""
    r0 = q if (h - q) % 2 == 0 else p
    xs = [(h - r0) // 2]
    ok = True
    for _ in range(max_steps):
        x = xs[-1]
        if x == target:
            return xs, ok, True
        # admissibility of the step ABOUT to be taken (RL then unit)
        refl = 2 * h - x
        if not (1 <= x and x != h and h + 1 <= refl <= N):
            ok = False
            return xs, ok, False
        r = q if x % 2 == q % 2 else p
        xs.append(h - (x + r) // 2)
    return xs, ok, False


def part_counterexample():
    """Reviewer tuple through the REAL map: q=1, p=4, g=3, r*=p,
    tau=8, h=14: x0=5 (delta0=-3), x1=11 (delta1=+3)."""
    q, p, h, tau = 1, 4, 14, 8
    xs, _ok, landed = real_spiral(h, q, p, N=10**6, target=tau)
    d0, d1 = xs[0] - tau, xs[1] - tau
    row = {"xs_prefix": xs[:6], "delta0": d0, "delta1": d1,
           "violates_half_bound": abs(d1) > abs(d0) / 2,
           "lands_eventually": landed}
    assert (d0, d1) == (-3, 3) and row["violates_half_bound"], row
    return row


def part_s1():
    res = {"tuples": 0, "fail": 0, "examples_fail": [],
           "max_K": 0, "min_N": None, "max_N": 0}
    tried = 0
    while res["tuples"] < N_TUPLES and tried < 60 * N_TUPLES:
        tried += 1
        q = random.randint(1, 400)
        g = 2 * random.randint(0, 100) + 1
        p = q + g
        # C1: t == -q or -p (mod 2g), parity-consistent lifts
        base = random.choice([-q, -p])
        t = (base % (2 * g)) + 2 * g * random.randint(0, 6)
        if t < 1:
            continue
        r0 = q if t % 2 == q % 2 else p
        if (t + r0) % (2 * g) != 0:   # C1 (g | (t+r0)/2)
            continue
        if 2 * q + 3 * t - r0 < 2:    # C2
            continue
        lo = 9 * t + 6 * q + r0       # C3: 2N >= lo
        N = (lo + 1) // 2 + random.randint(0, 500)
        u, w = 2 * t + q, 3 * t + 2 * q
        # seed unit u -> t and RL AP (t, u, w) in window
        okc = (1 <= t < u < w <= N)
        xs, ok_adm, landed = real_spiral(w, q, p, N, target=u)
        A = (t + r0) // 2
        ok = (okc and ok_adm and landed
              and min(xs) == xs[0] >= 1
              and max(xs) < w
              and max(xs) <= u + A // 2
              and 2 * A % (2 * g) == 0 and A >= g
              and 2 * (A // 2) < 2 * (t + q))
        res["tuples"] += 1
        res["max_K"] = max(res["max_K"], len(xs) - 1)
        res["min_N"] = N if res["min_N"] is None else min(res["min_N"], N)
        res["max_N"] = max(res["max_N"], N)
        if not ok:
            res["fail"] += 1
            if len(res["examples_fail"]) < 5:
                res["examples_fail"].append(
                    {"q": q, "g": g, "t": t, "N": N, "r0": r0,
                     "xs_prefix": xs[:8], "landed": landed})
    return res


if __name__ == "__main__":
    out = {}
    out["LAND"] = part_land()
    out["counterexample_sigma_minus"] = part_counterexample()
    out["S1"] = part_s1()
    OUT.write_text(json.dumps(out, indent=1))
    land, s1 = out["LAND"], out["S1"]
    hard_fail = (land["general_bound_fail"] or land["pos_dev_from_pos_fail"]
                 or land["pos_dev_bound_fail_plus"] or land["land_fail"]
                 or land["sup_bound_fail"] or land["min_orbit_fail"]
                 or land["nonland_fail"] or land["mod_track_fail"]
                 or s1["fail"])
    need = land["pos_dev_bound_viol_minus"] < 1
    print(json.dumps(out, indent=1))
    print(f"\nLAND: {land['tuples_per_sigma']} tuples/sigma; "
          f"sigma=-1 half-bound violations found: "
          f"{land['pos_dev_bound_viol_minus']} (must be >= 1)")
    print(f"S1: {s1['tuples']} admissible tuples, {s1['fail']} failures, "
          f"max spiral length {s1['max_K']}, N in "
          f"[{s1['min_N']}, {s1['max_N']}]")
    if hard_fail or need:
        print("VERDICT: FAIL")
        sys.exit(1)
    print("VERDICT: PASS -- corrected LAND bounds + S1 hold; "
          "sigma=-1 scoping is necessary")
