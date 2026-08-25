"""Round 3: independent joint-protection in-some-MUS check at M=44
(replicates P3 method with the eager encoding; shuffled retries for
any pattern not certified by the first pass)."""
import random
import time

from pysat.solvers import Cadical195

T0 = time.time()
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


def o(u, w):
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
    cl.append([-c, -o(a, b), -o(b, cc)])
    cl.append([-c, o(a, b), o(b, cc)])
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            vij, vjk, vik = var[(i, j)], var[(j, k)], var[(i, k)]
            cl.append([-vij, -vjk, vik])
            cl.append([vij, vjk, -vik])
# attacks as hard units (mirrors P3)
for x in (15, 16):
    for j in range(1, x // 2 + 1):
        cl.append([o(2 * M + 2 * j - x, M + j)])
s = Cadical195(bootstrap_with=cl)

Fpat = {
    "F1": (M + 1, (3 * M - 6) // 2, 2 * M - 7),
    "F2": (M + 5, (3 * M + 2) // 2, 2 * M - 3),
    "F3": (M + 7, (3 * M + 2) // 2, 2 * M - 5),
    "F4": (M + 17, (3 * M - 2) // 2, 2 * M - 19),
    "F5": (M + 19, (3 * M + 14) // 2, 2 * M - 5),
    "F6": ((3 * M - 2) // 2, (3 * M + 6) // 2, (3 * M + 14) // 2),
    "F7": ((3 * M + 2) // 2, (7 * M - 16) // 4, 2 * M - 9),
}
prot = set(Fpat.values())
found = {}


def attempt(order):
    keep = list(order)
    for t in order:
        if t in prot:
            continue
        trial = [sel[x] for x in keep if x != t]
        if not s.solve(assumptions=trial):
            keep.remove(t)
    assert not s.solve(assumptions=[sel[x] for x in keep])
    res = {}
    for name, pat in Fpat.items():
        minus = [sel[x] for x in keep if x != pat]
        res[name] = s.solve(assumptions=minus)  # SAT => essential => in MUS
    return len(keep), res


sz, res = attempt(list(triples))
print(f"pass 0 (fixed order): protected-min {sz}: "
      + " ".join(f"{k}={'IN' if v else '?'}" for k, v in res.items()),
      flush=True)
for k, v in res.items():
    if v:
        found[k] = True
rng = random.Random(7)
p = 0
while len(found) < 7 and p < 12:
    p += 1
    order = list(triples)
    rng.shuffle(order)
    sz, res = attempt(order)
    for k, v in res.items():
        if v:
            found[k] = True
    print(f"pass {p}: protected-min {sz}: "
          + " ".join(f"{k}={'IN' if res[k] else '?'}" for k in Fpat)
          + f"  cumulative {sorted(found)}  ({time.time()-T0:.0f}s)",
          flush=True)
print(f"RESULT: certified in-some-MUS at M=44: {sorted(found)}; "
      f"missing: {sorted(set(Fpat) - set(found))}  ({time.time()-T0:.0f}s)")
