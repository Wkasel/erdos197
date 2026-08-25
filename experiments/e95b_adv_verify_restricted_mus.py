"""Adversarial verification round 2.

 W1  restricted 59-triple MUS instance at M=40 (triples from
     data/og_mus_40.log, transitivity over all 40 values):
     attacks 1-13 SAT; 47<78 forced; attack #14 (78<47) UNSAT.
     (the CORRECTION paragraph's account of the old record)
 W2  in-some-MUS spot check of F1..F7 at M=44 on the full-attack
     instance: protect the F-triple, deletion-minimize the rest,
     confirm the F-triple sits in the resulting MUS (i.e. removing
     it from the final core restores SAT).
"""
import re
import time

from pysat.solvers import Cadical195

T0 = time.time()
FAILS = []


def log(s=""):
    print(s, flush=True)


def chk(name, cond, detail=""):
    tag = "ok" if cond else "FAIL"
    if not cond:
        FAILS.append((name, detail))
    log(f"  [{tag}] {name} {detail}")


# ---------- W1: restricted instance at M=40 ----------
mus = []
for line in open("/Users/will/Dev/personal/tasks/math/erdos197/data/"
                 "og_mus_40.log"):
    m = re.match(r"\s*\((\d+), (\d+), (\d+)\)", line)
    if m:
        mus.append(tuple(int(x) for x in m.groups()))
log(f"parsed {len(mus)} MUS triples")
chk("59 triples parsed", len(mus) == 59)
vals = sorted(set(v for t in mus for v in t))
log(f"values covered by MUS: {len(vals)}")

M = 40
V = list(range(M + 1, 2 * M + 1))
idx = {v: i for i, v in enumerate(V)}
n = len(V)
var = {}
c = 0
for i in range(n):
    for j in range(i + 1, n):
        c += 1
        var[(i, j)] = c


def o(u, w):
    i, j = idx[u], idx[w]
    return var[(i, j)] if i < j else -var[(j, i)]


cl = []
for (a, b, cc) in mus:
    cl.append([-o(a, b), -o(b, cc)])
    cl.append([o(a, b), o(b, cc)])
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            vij, vjk, vik = var[(i, j)], var[(j, k)], var[(i, k)]
            cl.append([-vij, -vjk, vik])
            cl.append([vij, vjk, -vik])
s = Cadical195(bootstrap_with=cl)
# attacks in gadget order: 15-attacks j=1..7 then 16-attacks j=1..8
atk = [(2 * M + 2 * j - 15, M + j) for j in range(1, 8)] + \
      [(2 * M + 2 * j - 16, M + j) for j in range(1, 9)]
chk("attack #14 is (78,47)", atk[13] == (78, 47), str(atk[13]))
a13 = [o(z, y) for (z, y) in atk[:13]]
chk("restricted: attacks 1-13 SAT", s.solve(assumptions=a13))
chk("restricted: attacks 1-13 force 47<78",
    not s.solve(assumptions=a13 + [o(78, 47)]))
chk("restricted: attacks 1-14 UNSAT",
    not s.solve(assumptions=a13 + [o(*atk[13])]))
# count the full backbone: forced pairs under attacks 1-13 (claim: 69)
forced = 0
for i in range(n):
    for j in range(i + 1, n):
        u, w = V[i], V[j]
        fu = not s.solve(assumptions=a13 + [o(w, u)])
        fw = not s.solve(assumptions=a13 + [o(u, w)])
        if fu != fw:
            forced += 1
chk(f"restricted backbone size = {forced}", forced == 69,
    "(og40_backbone.txt claims 69)")
s.delete()
log(f"  ({time.time()-T0:.0f}s)")

# ---------- W2: in-some-MUS for F1..F7 at M=44, full attacks ----------
M = 44
V = list(range(M + 1, 2 * M + 1))
idx = {v: i for i, v in enumerate(V)}
n = len(V)
var = {}
c = 0
for i in range(n):
    for j in range(i + 1, n):
        c += 1
        var[(i, j)] = c


def o2(u, w):
    i, j = idx[u], idx[w]
    return var[(i, j)] if i < j else -var[(j, i)]


triples = []
for b in V:
    d = 1
    while b + d <= 2 * M:
        a, cc = b - d, b + d
        if a > M:
            triples.append((a, b, cc))
        d += 1
sel = {}
cl = []
for t in triples:
    a, b, cc = t
    c += 1
    sel[t] = c
    cl.append([-c, -o2(a, b), -o2(b, cc)])
    cl.append([-c, o2(a, b), o2(b, cc)])
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            vij, vjk, vik = var[(i, j)], var[(j, k)], var[(i, k)]
            cl.append([-vij, -vjk, vik])
            cl.append([vij, vjk, -vik])
s = Cadical195(bootstrap_with=cl)
attacks = [o2(2 * M + 2 * j - 15, M + j) for j in range(1, 8)] + \
          [o2(2 * M + 2 * j - 16, M + j) for j in range(1, 9)]
Fpat = {
    "F1": (M + 1, (3 * M - 6) // 2, 2 * M - 7),
    "F2": (M + 5, (3 * M + 2) // 2, 2 * M - 3),
    "F3": (M + 7, (3 * M + 2) // 2, 2 * M - 5),
    "F4": (M + 17, (3 * M - 2) // 2, 2 * M - 19),
    "F5": (M + 19, (3 * M + 14) // 2, 2 * M - 5),
    "F6": ((3 * M - 2) // 2, (3 * M + 6) // 2, (3 * M + 14) // 2),
    "F7": ((3 * M + 2) // 2, (7 * M - 16) // 4, 2 * M - 9),
}
allsel = [sel[t] for t in triples]
chk("M=44 full instance UNSAT (all attacks, all triples)",
    not s.solve(assumptions=attacks + allsel))
for name, pat in Fpat.items():
    chk(f"{name} {pat} is a listed triple", pat in sel)
    keep = list(triples)
    for t in list(triples):
        if t == pat:
            continue
        trial = [sel[x] for x in keep if x != t]
        if not s.solve(assumptions=attacks + trial):
            keep.remove(t)
    core = [sel[x] for x in keep]
    still_unsat = not s.solve(assumptions=attacks + core)
    minus = [sel[x] for x in keep if x != pat]
    needed = s.solve(assumptions=attacks + minus)
    chk(f"{name}: in-some-MUS at M=44 (core size {len(keep)}, "
        f"needed={needed})", still_unsat and needed,
        f"  ({time.time()-T0:.0f}s)")
s.delete()

log()
log(f"== TOTAL {time.time()-T0:.0f}s; failures: {len(FAILS)}")
for nm, d in FAILS:
    log(f"  FAIL: {nm} {d}")
