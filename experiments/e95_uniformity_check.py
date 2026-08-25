"""e95_uniformity_check: ADVERSARIAL scale-uniformity audit of
notes/30-og-proof-draft.md.

The draft's lemma layer (S11/S12/S13/S14, O1-O8) was certified only at
M in {40,44,48,52,60} -- all == 0 mod 4.  This script re-tests every
parametric step at the adversarial scales

    M_ADV = 41, 43, 45, 47, 49, 53, 100, 128

(six odd scales, one == 4 mod 8, one dyadic), plus a threshold scan
M = 30..40 of the full gadget to locate the true M0.

Steps audited (tags refer to notes/30):
  S6  : 15-family SAT alone; j*(M) = least j with 15fam+16{1..j} UNSAT
  S7  : 10-unit core 15{1..7}+16{1..3} infeasible (except M==3 mod 16)
  S9  : 11-unit core 15{1..7}+16{1..4} infeasible (Theorem A')
  S8  : C4 = {15:1,15:2,15:5,16:3} UNSAT iff M==0 mod 4;
        C3 = {15:5,15:6,16:3}      UNSAT iff M==0 mod 8
  S11 : under H*(M)=15fam+16{1..j*-1}: b3<t10, b5<t6, b7<t2 forced;
        b5<t6 NOT forced under the 15-family alone
  S12 : O1..O8 forced under H*(M)  (non-integer anchors => PARITY-SKIP)
  S13 : even M: AP (b4,m2,t2) + forced m2<b4;  odd M analogue (G6):
        AP (b5,m3,t2), is m3<b5 forced? is m3<t2 forced?
  S14 : b7<b21, b21<t2, b7<t2 forced under H*(M)
  S16 : F1..F7 arithmetic instantiation (integrality + in-interval + AP)
  M0  : full OG(M) (15{1..7}+16{1..8}) SAT/UNSAT for M = 30..40

Verdict rule: a step FAILS at M if the draft asserts it for that M's
class and the machine refutes it there.  Steps the draft itself
restricts to even M / M==0 mod 4 are logged as PARITY-SKIP (gap
evidence, not a contradiction) unless the draft's text claims more.

Output: data/uniformity_check.log + .json
"""
import json
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e94_step_check import OG  # noqa: E402

M_ADV = [41, 43, 45, 47, 49, 53, 100, 128]
M_THRESH = list(range(30, 41))
OUT = "/Users/will/Dev/personal/tasks/math/erdos197/data/uniformity_check.log"

t0 = time.time()
fh = open(OUT, "w")
results = {"M_adv": M_ADV, "steps": {}, "failures": []}


def log(s=""):
    print(s, flush=True)
    fh.write(s + "\n")
    fh.flush()


def fail(step, M, msg):
    results["failures"].append({"step": step, "M": M, "msg": msg})
    log(f"  *** FAIL [{step} @ M={M}] {msg}")


def forced(g, H, u, v):
    """'F' if u<v forced by H, 'R' if v<u forced, '-' undetermined."""
    if not g.solve(H + [g.o(v, u)]):
        return "F"
    if not g.solve(H + [g.o(u, v)]):
        return "R"
    return "-"


def in_iv(g, *vals):
    return all(v is not None and g.M < v <= 2 * g.M for v in vals)


def half(num):
    return num // 2 if num % 2 == 0 else None


# ---------------------------------------------------------------- per-M audit
inst = {}
jstar = {}
for M in M_ADV:
    log(f"==== M = {M}  (mod4={M % 4}, mod8={M % 8}, mod16={M % 16}) ====")
    g = OG(M)
    inst[M] = g
    st = results["steps"].setdefault(M, {})

    # ---- S6: 15-family SAT, prefix scan for j* ----
    s15 = g.solve(g.fam15())
    st["fam15_SAT"] = s15
    if not s15:
        fail("S6", M, "15-family alone UNSAT (draft: always consistent)")
    js = None
    for j in range(1, 9):
        if not g.solve(g.fam15() + g.pre16(j)):
            js = j
            break
    jstar[M] = js
    st["jstar"] = js
    log(f"  S6: 15-family SAT={s15}; j*={js}   ({time.time()-t0:.0f}s)")
    if js is None:
        fail("S6", M, "15fam+16{1..8} SAT -- full attack set fails!")
        continue

    # ---- S7: 10-unit core (claimed UNSAT unless M==3 mod 16) ----
    r10 = g.solve(g.fam15() + g.pre16(3))
    st["core10_SAT"] = r10
    exc = (M % 16 == 3)
    log(f"  S7: 10-unit core SAT={r10} (exception class: {exc})")
    if r10 and not exc:
        fail("S7", M, "10-unit core SAT at non-exceptional M")
    if (not r10) and exc:
        fail("S7", M, "draft says M==3 mod16 needs 16:4, but 10-unit UNSAT")

    # ---- S9: 11-unit core (Theorem A') ----
    r11 = g.solve(g.fam15() + g.pre16(4))
    st["core11_SAT"] = r11
    log(f"  S9: 11-unit core SAT={r11}")
    if r11:
        fail("S9", M, "Theorem A' core 15{1..7}+16{1..4} SAT")

    # ---- S8: C4 / C3 residue-class cores ----
    c4 = g.solve([g.a15(1), g.a15(2), g.a15(5), g.a16(3)])
    c3 = g.solve([g.a15(5), g.a15(6), g.a16(3)])
    st["C4_SAT"], st["C3_SAT"] = c4, c3
    log(f"  S8: C4 SAT={c4} (claim: UNSAT iff M==0 mod4; here mod4={M % 4})"
        f"   C3 SAT={c3} (claim: UNSAT iff M==0 mod8; here mod8={M % 8})")
    if (M % 4 == 0) != (not c4):
        fail("S8", M, f"C4 SAT={c4} contradicts mod-4 claim")
    if (M % 8 == 0) != (not c3):
        fail("S8", M, f"C3 SAT={c3} contradicts mod-8 claim")

    # ---- H*(M) ----
    H = g.fam15() + g.pre16(js - 1)
    if not g.solve(H):
        fail("S11", M, "H*(M) itself UNSAT -- prefix scan inconsistent")
        continue

    # ---- S11: bottom-vs-guard invariants under H* ----
    inv = {}
    for name, (u, v) in [("b3<t10", (M + 3, 2 * M - 10)),
                         ("b5<t6", (M + 5, 2 * M - 6)),
                         ("b7<t2", (M + 7, 2 * M - 2))]:
        inv[name] = forced(g, H, u, v)
    b5t6_15only = forced(g, g.fam15(), M + 5, 2 * M - 6)
    st["S11"] = {**inv, "b5<t6_under_15fam": b5t6_15only}
    log(f"  S11: {inv}  b5<t6 under 15fam alone: {b5t6_15only} "
        f"(draft: not forced)   ({time.time()-t0:.0f}s)")
    for name, r in inv.items():
        if r != "F":
            fail("S11", M, f"invariant {name} not forced (status {r})")
    if b5t6_15only == "F":
        fail("S11", M, "b5<t6 IS forced by 15-family alone (draft says not)")

    # ---- S12: O1..O8 under H* ----
    m2 = half(3 * M + 2)
    OLEMMAS = [
        ("O1a", M + 19, M + 13), ("O1b", 2 * M - 21, 2 * M - 27),
        ("O2a", M + 11, M + 21), ("O2b", 2 * M - 29, 2 * M - 19),
        ("O3a", 2 * M - 13, 2 * M - 19), ("O3b", 2 * M - 13, 2 * M - 23),
        ("O3c", 2 * M - 13, M + 17),
        ("O4a", 2 * M - 9, 2 * M - 11), ("O4b", 2 * M - 9, 2 * M - 7),
        ("O4c", 2 * M - 11, 2 * M - 2),
        ("O5", M + 7, M + 21),
        ("O6a", M + 21, 2 * M - 2), ("O6b", m2, 2 * M - 2),
        ("O6c", 2 * M - 19, 2 * M - 2),
        ("O7a", m2, M + 4), ("O7b", M + 21, M + 4),
        ("O7c", 2 * M - 19, M + 4),
        ("O8a", M + 31, M + 21), ("O8b", 2 * M - 9, M + 21),
    ]
    orow = {}
    for name, u, v in OLEMMAS:
        if not in_iv(g, u, v):
            orow[name] = "PARITY-SKIP" if (u is None or v is None) \
                else "RANGE-SKIP"
            continue
        orow[name] = forced(g, H, u, v)
    st["S12"] = orow
    log("  S12: " + "  ".join(f"{k}:{v}" for k, v in orow.items())
        + f"   ({time.time()-t0:.0f}s)")
    for name, r in orow.items():
        if r in ("R", "-"):
            fail("S12", M, f"lemma {name} not forced under H* (status {r})")

    # ---- S13: pivot AP into t2, both parities ----
    if M % 2 == 0:
        ap_ok = (M + 4) + (2 * M - 2) == 2 * m2 and in_iv(g, M + 4, m2,
                                                          2 * M - 2)
        r1 = forced(g, H, m2, M + 4)
        r2 = forced(g, H, m2, 2 * M - 2)
        st["S13"] = {"AP(b4,m2,t2)": ap_ok, "m2<b4": r1, "m2<t2": r2}
        log(f"  S13 (even): AP ok={ap_ok}; m2<b4:{r1}  m2<t2:{r2}")
        if not ap_ok:
            fail("S13", M, "AP (b4,m2,t2) arithmetic broken")
        if r1 != "F":
            fail("S13", M, f"m2<b4 not forced (status {r1})")
        if r2 != "F":
            fail("S13", M, f"m2<t2 not forced (status {r2})")
    else:
        m3 = half(3 * M + 3)
        ap_ok = (M + 5) + (2 * M - 2) == 2 * m3 and in_iv(g, M + 5, m3,
                                                          2 * M - 2)
        r1 = forced(g, H, m3, M + 5)
        r2 = forced(g, H, m3, 2 * M - 2)
        st["S13_oddG6"] = {"AP(b5,m3,t2)": ap_ok, "m3<b5": r1, "m3<t2": r2}
        log(f"  S13/G6 (odd): AP ok={ap_ok}; m3<b5:{r1}  m3<t2:{r2}"
            f"  (draft left this untested)")
        if r1 != "F":
            fail("S13/G6", M,
                 f"odd-M analogue m3<b5 NOT forced (status {r1}) -- "
                 "the proposed odd-parity pivot step fails")

    # ---- S14: the final chain ----
    ch = {}
    for name, (u, v) in [("b7<b21", (M + 7, M + 21)),
                         ("b21<t2", (M + 21, 2 * M - 2)),
                         ("b7<t2", (M + 7, 2 * M - 2))]:
        ch[name] = forced(g, H, u, v)
    st["S14"] = ch
    log(f"  S14: {ch}   ({time.time()-t0:.0f}s)")
    for name, r in ch.items():
        if r != "F":
            fail("S14", M, f"chain literal {name} not forced (status {r})")

    # ---- S16: F1..F7 arithmetic ----
    F = [
        ("F1", M + 1, half(3 * M - 6), 2 * M - 7),
        ("F2", M + 5, half(3 * M + 2), 2 * M - 3),
        ("F3", M + 7, half(3 * M + 2), 2 * M - 5),
        ("F4", M + 17, half(3 * M - 2), 2 * M - 19),
        ("F5", M + 19, half(3 * M + 14), 2 * M - 5),
        ("F6", half(3 * M - 2), half(3 * M + 6), half(3 * M + 14)),
        ("F7", half(3 * M + 2),
         (7 * M - 16) // 4 if (7 * M - 16) % 4 == 0 else None, 2 * M - 9),
    ]
    frow = {}
    for name, a, b, c in F:
        if a is None or b is None or c is None:
            frow[name] = "PARITY-SKIP"
            continue
        ok = a + c == 2 * b and in_iv(g, a, b, c) and a != b and b != c
        frow[name] = "ok" if ok else "BROKEN"
        if not ok:
            fail("S16", M, f"{name} instantiates but is not a valid AP")
    st["S16"] = frow
    log("  S16: " + "  ".join(f"{k}:{v}" for k, v in frow.items()))
    log()

# ------------------------------------------------------- M0 threshold scan
log("==== M0 threshold scan: full OG(M) = (i) + 15{1..7} + 16{1..8},"
    " M = 30..40 ====")
thresh = {}
for M in M_THRESH:
    g = OG(M)
    r = g.solve(g.fam15() + g.pre16(8))
    thresh[M] = "SAT" if r else "UNSAT"
    log(f"  M={M}: {'SAT' if r else 'UNSAT'}   ({time.time()-t0:.0f}s)")
    g.sol.delete()
results["threshold"] = thresh
unsat_from = None
for M in sorted(thresh):
    if thresh[M] == "UNSAT" and all(
            thresh.get(K, "UNSAT") == "UNSAT" for K in range(M, 41)):
        unsat_from = M
        break
results["M0_candidate"] = unsat_from
log(f"  => least M with OG(M') UNSAT for all M' in [M,40]: {unsat_from}")

log()
log(f"FAILURES: {len(results['failures'])}")
for f in results["failures"]:
    log(f"  [{f['step']} @ M={f['M']}] {f['msg']}")
json.dump(results, open(OUT.replace(".log", ".json"), "w"), indent=1)
log(f"total {time.time()-t0:.0f}s")
fh.close()
