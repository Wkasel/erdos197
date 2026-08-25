"""e96: machine checks for the paper section 'The order gadget and the main
theorem' (and the Normalization lemma).  Five parts:

  P1  boundary arithmetic of the gadget: for x in {15,16} the in-block
      completions of (x, b_j) are exactly j <= x/2, land on the guards
      t_{x-2j}, include z = 2M at (x,j) = (16,8); guard/bottom collision
      scales; self-attack degeneracies at M = x - j only (all <= 15, so
      every M >= 16 is a well-formed instance; brute-forced to M = 299).
  P2  the chunk case-table (thm:chunk rows): exhaustive enumeration over
      stage patterns and fiber orders -- induced-order non-monotonicity
      of a triple  <=>  the (A) row plus the applicable (B) rows.
  P3  attack forcing: whenever s(x) < s(b_j), (A)+(B) force the guard
      before the bottom in the induced order (exhaustive, same model).
  P4  running-max normalization: on random permutations of
      S_A cap [1, 4096], s(v) = max_{q <= pos(v)} block(pi(q))/2 is
      non-decreasing along positions (fibers are consecutive segments,
      concatenation = pi) and delta(v) = s(v) - block(v)/2 >= 0 for all v.
  P5  fresh OG(128) UNSAT with an EAGER O(n^3) transitivity encoding
      (independent of the lazy loop of e87/e89).

Run: .venv/bin/python experiments/e96_reduction_check.py   (~1 min)
"""
import itertools, random, time

fails = []
def ck(cond, msg):
    tag = "ok" if cond else "FAIL"
    print(f"  [{tag}] {msg}", flush=True)
    if not cond:
        fails.append(msg)

# ---------- P1: boundary arithmetic ----------
print("== P1: gadget boundary arithmetic ==")
for M in [40, 44, 47, 128, 512, 2048, 2 ** 13]:
    for x in (15, 16):
        inblock = []
        for j in range(1, 30):
            y = M + j
            if y > 2 * M:
                break
            z = 2 * y - x
            if M < z <= 2 * M:
                inblock.append(j)
                # z is the guard t_{x-2j}
                if z != 2 * M - (x - 2 * j):
                    fails.append(f"M={M} x={x} j={j}: z != t_(x-2j)")
        ck(inblock == list(range(1, x // 2 + 1)),
           f"M={M} x={x}: in-block completions exactly j=1..{x//2}")
    # (x,j)=(16,8): z = 2M, inside the half-open block (M, 2M]
    ck(2 * (M + 8) - 16 == 2 * M, f"M={M}: (16,8) completion is 2M (in block)")
    # guard-bottom pair's own downward completion is the crown itself
    for x in (15, 16):
        for j in range(1, x // 2 + 1):
            b, t = M + j, 2 * M - (x - 2 * j)
            if 2 * b - t != x:
                fails.append(f"M={M}: 2b_j - t_(x-2j) != {x}")
    # guards distinct from bottoms globally for M > 22
    G = {2 * M - i for i in range(0, 15)}
    B = {M + j for j in range(1, 9)}
    if M > 22:
        ck(not (G & B), f"M={M}: guards (>=2M-14) and bottoms (<=M+8) disjoint")
# self-attack degeneracies t_{x-2j} = b_j  <=>  M = x - j  (all <= 15):
# 2M + 2j - x = M + j  <=>  M = x - j.  Verify by brute force that for
# every M >= 16 no attack pair collapses to v < v, and that M = x - j
# does collapse (e.g. t_14 = b_1 at M = 15).
degens = sorted({x - j for x in (15, 16) for j in range(1, x // 2 + 1)})
ck(max(degens) == 15, f"self-attack degeneracies only at M in {degens} (max 15)")
brute = [M for M in range(8, 300)
         if any(2 * M + 2 * j - x == M + j
                for x in (15, 16) for j in range(1, x // 2 + 1))]
ck(brute == degens,
   f"brute force M=8..299 confirms: collision iff M in {degens};"
   " every M >= 16 is a well-formed instance")

# ---------- P2 + P3: chunk case-table, exhaustively ----------
print("== P2/P3: chunk case-table and attack forcing (exhaustive) ==")
# model: triple (x,y,z) value-ordered x<y<z, stages (a,b,c) in {0,1,2}^3,
# within each stage the members get a rank (all permutations); induced order
# by (stage, rank).  monotone := x,y,z or z,y,x in induced position order.
bad_table, bad_force = 0, 0
cases = 0
for a, b, c in itertools.product(range(3), repeat=3):
    groups = {}
    for name, st in (("x", a), ("y", b), ("z", c)):
        groups.setdefault(st, []).append(name)
    # all fiber orders = product of permutations of each group
    # (perm tuple aligns with groups.values() iteration order)
    gkeys = list(groups)
    for perm in itertools.product(*[itertools.permutations(groups[k])
                                    for k in gkeys]):
        rank = {}
        for st, order in zip(gkeys, perm):
            for r, name in enumerate(order):
                rank[name] = r
        pos = {n: (dict(x=a, y=b, z=c)[n], rank[n]) for n in "xyz"}
        mono = (pos["x"] < pos["y"] < pos["z"]) or \
               (pos["z"] < pos["y"] < pos["x"])
        violA = (a < b < c) or (c < b < a)
        violB = False
        if a < b == c and not (pos["z"] < pos["y"]): violB = True
        if c < b == a and not (pos["x"] < pos["y"]): violB = True
        if a == b < c and not (pos["y"] < pos["x"]): violB = True
        if b == c < a and not (pos["y"] < pos["z"]): violB = True
        if a == b == c:
            r = (rank["x"], rank["y"], rank["z"])
            if (r[0] < r[1] < r[2]) or (r[2] < r[1] < r[0]): violB = True
        if mono != (violA or violB):
            bad_table += 1
        # P3: attack forcing -- s(x) < s(y) and constraints satisfied
        if a < b and not (violA or violB):
            if not (pos["z"] < pos["y"]):
                bad_force += 1
        cases += 1
ck(bad_table == 0, f"case table exact over {cases} stage/fiber cases")
ck(bad_force == 0, "s(x)<s(y) + (A)+(B)  ==>  z before y (attack forced)")

# ---------- P4: running-max normalization ----------
print("== P4: running-max normalization on random permutations ==")
SA = [v for v in range(1, 4097)
      if ((v - 1).bit_length() % 2 == 0)]  # v in B_k = (2^(k-1), 2^k], k = (v-1).bit_length()
def block(v):
    return (v - 1).bit_length()
rng = random.Random(96)
ok_all = True
for trial in range(200):
    pi = SA[:]
    rng.shuffle(pi)
    run, s = 0, {}
    for v in pi:
        run = max(run, block(v) // 2)
        s[v] = run
    # non-decreasing along positions by construction; check delta >= 0
    if any(s[v] - block(v) // 2 < 0 for v in SA):
        ok_all = False
    # fibers are consecutive segments: stage sequence along pi sorted
    seq = [s[v] for v in pi]
    if seq != sorted(seq):
        ok_all = False
ck(ok_all, "200 random pi: s nondecreasing along pos; delta(v) >= 0 for all v")

# ---------- P5: OG(128) UNSAT, eager encoding ----------
print("== P5: OG(128) with eager transitivity (independent encoding) ==")
from pysat.solvers import Cadical195
M = 128
V = list(range(M + 1, 2 * M + 1))
n = len(V)
idx = {v: i for i, v in enumerate(V)}
var = {}
cnt = 0
for i in range(n):
    for j in range(i + 1, n):
        cnt += 1
        var[(i, j)] = cnt
def o(u, w):
    i, j = idx[u], idx[w]
    return var[(i, j)] if i < j else -var[(j, i)]
cl = []
for i in range(n):            # eager transitivity
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            a_, b_, c_ = var[(i, j)], var[(j, k)], var[(i, k)]
            cl.append([-a_, -b_, c_])
            cl.append([a_, b_, -c_])
ntr = 0
for y in V:                   # AP non-monotonicity
    d = 1
    while y + d <= 2 * M:
        x, z = y - d, y + d
        d += 1
        if x > M:
            cl.append([-o(x, y), -o(y, z)])
            cl.append([-o(z, y), -o(y, x)])
            ntr += 1
natk = 0
for x in (15, 16):            # attacks
    for j in range(1, x // 2 + 1):
        y, z = M + j, 2 * M + 2 * j - x
        if M < z <= 2 * M:
            cl.append([o(z, y)])
            natk += 1
t0 = time.time()
sol = Cadical195(bootstrap_with=cl)
res = sol.solve()
ck(res is False,
   f"OG(128) eager: UNSAT ({len(cl)} clauses, {natk} attacks, "
   f"{ntr} triples, {time.time()-t0:.0f}s)")

print(f"\nTOTAL failures: {len(fails)}")
for f in fails:
    print("  FAIL:", f)
