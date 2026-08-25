"""e95c: supplement to e95 — the M == 2 (mod 4) class (42, 46, 50, 54),
which the prescribed adversarial set (41..53 odd, 100, 128) misses.

Findings (log data/uniformity_check_c.log):
  * j* = 1 at all four scales (H* = bare 15-family);
  * b5<t6 IS forced by the 15-family alone (contradicts the S11
    sub-claim "not forced by the 15-family alone" when read beyond
    the M == 0 mod 4 test scales);
  * O5 (b7 < b21) is REVERSE-forced (b21 < b7): the S14 chain's first
    link is provably false on this class;
  * O6b/O7a (m2 literals) undetermined; b7<t2 undetermined — the
    Section 5 chain fails on the whole class, consistent with the
    draft's own caveat (c) at M = 50.
"""
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e94_step_check import OG  # noqa: E402

OUT = "/Users/will/Dev/personal/tasks/math/erdos197/data/uniformity_check_c.log"
t0 = time.time()
out = open(OUT, "w")


def log(s=""):
    print(s, flush=True)
    out.write(s + "\n")
    out.flush()


def forced(g, H, u, v):
    if not g.solve(H + [g.o(v, u)]):
        return "F"
    if not g.solve(H + [g.o(u, v)]):
        return "R"
    return "-"


log("== supplement: M == 2 mod 4 scales (42,46,50,54): j*, S11, "
    "S12-key, S14 ==")
for M in (42, 46, 50, 54):
    g = OG(M)
    js = next(j for j in range(1, 9)
              if not g.solve(g.fam15() + g.pre16(j)))
    H = g.fam15() + g.pre16(js - 1)
    assert g.solve(H)
    m2 = (3 * M + 2) // 2
    row = {}
    for name, (u, v) in [
            ("b3<t10", (M + 3, 2 * M - 10)),
            ("b5<t6", (M + 5, 2 * M - 6)),
            ("b7<t2", (M + 7, 2 * M - 2)),
            ("O5:b7<b21", (M + 7, M + 21)),
            ("O6a:b21<t2", (M + 21, 2 * M - 2)),
            ("O6b:m2<t2", (m2, 2 * M - 2)),
            ("O7a:m2<b4", (m2, M + 4)),
            ("O1b:t21<t27", (2 * M - 21, 2 * M - 27)),
            ("O4a:t9<t11", (2 * M - 9, 2 * M - 11))]:
        row[name] = forced(g, H, u, v)
    log(f"  M={M} (mod8={M % 8}): j*={js}  "
        + "  ".join(f"{k}:{v}" for k, v in row.items())
        + f"   ({time.time()-t0:.0f}s)")
    g.sol.delete()
out.close()
