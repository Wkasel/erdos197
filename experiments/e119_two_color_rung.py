"""H3(b): COUPLED 2-COLORED RUNG — chunk conditions (A)+(B) for BOTH teams
of a 2-coloring of [2, 4^m], coupled only through the coloring.

Model (per paper thm:chunk + lem:normal, portable to any team with base
g(v) = ceil(log4 v)): each value v gets a color c_v (A/B) and a stage
s(v) = g(v) + delta(v), delta in [0, cap(v)].  Within each team the order
must respect stages (s(u) < s(w) forces u before w) and every same-team AP
triple must be non-monotone; this is exactly (A) and (B) of thm:chunk at
finite horizon.  Displacement caps: crowncap mode caps delta(15), delta(16)
<= CAP with everything else free <= DMAX (the crown-rung metric; dyadic
rungs proved max(d15,d16) >= 2 at N=256 and >= 3 at N=1024); fullcap mode
caps all v <= 16 (the e77/e83 L(m) metric).

Modes:
  dyadicAonly  dyadic coloring, team-A constraints only (validation vs
               e77/e83/crown rung)
  dyadic       dyadic coloring, both teams
  same         c15 = c16 = A (WLOG), all other colors FREE
  split        c15 = A, c16 = B, all other colors FREE
  free         all colors free
  richD        (D a digit, e.g. rich0, rich2): c15 = c16 = A and every EVEN
               dyadic block k >= 6 (the (M, 2M] with M = 2^{k-1} = 0 mod 8)
               donates at most D values to B; odd blocks + small values free.
               The block-rich crown team of the portable-crown dichotomy:
               measures the donation price of bounded crown displacement.
Verdicts: UNSAT at (mode, m, CAP) = NO coloring of that class admits a
coupled scheme with crown displacement <= CAP at horizon 4^m.
Usage: e119_two_color_rung.py m CAP [DMAX=8] [mode=same] [fullcap]
"""
import json
import sys
import time

import numpy as np
from pysat.solvers import Cadical195

m = int(sys.argv[1])
CAP = int(sys.argv[2])
DMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 8
mode = sys.argv[4] if len(sys.argv) > 4 else "same"
crowncap = "fullcap" not in sys.argv
richD = int(mode[4:]) if mode.startswith("rich") else None
N = 4 ** m
V = list(range(2, N + 1))
n = len(V)
idx = {v: i for i, v in enumerate(V)}
Vs = set(V)

def g(v):                                    # ratio-4 base stage
    t = 0
    while 4 ** t < v:
        t += 1
    return t

def block(v):                                # dyadic block index
    k = (v - 1).bit_length()
    if 2 ** k < v:
        k += 1
    return k

def cap_of(v):
    if crowncap:
        return CAP if v in (15, 16) else DMAX
    return CAP if v <= 16 else DMAX

var = 0
col = {}
for v in V:
    var += 1
    col[v] = var
L = {}                                       # unary ladder: L[v][j] = "delta(v) >= j"
for v in V:
    L[v] = {}
    for j in range(1, cap_of(v) + 1):
        var += 1
        L[v][j] = var
ov = {"A": {}, "B": {}}
for T in ("A", "B"):
    for i in range(n):
        for j in range(i + 1, n):
            var += 1
            ov[T][(i, j)] = var

def o(T, u, w):
    i, j = idx[u], idx[w]
    return ov[T][(i, j)] if i < j else -ov[T][(j, i)]

def notT(T, v):
    return -col[v] if T == "A" else col[v]

def geq(v, t):                               # literal / bool for s(v) >= t
    if t <= g(v):
        return True
    d = t - g(v)
    if d > cap_of(v):
        return False
    return L[v][d]

cl = []
for v in V:                                  # ladder monotone
    for j in sorted(L[v])[1:]:
        cl.append([-L[v][j], L[v][j - 1]])

teams = ("A",) if mode == "dyadicAonly" else ("A", "B")
nforce = 0
for a in range(n):                           # stage-forced order, thresholds
    u = V[a]
    for b in range(a + 1, n):
        w = V[b]
        for (p, q) in ((u, w), (w, u)):      # s(p) < s(q) forces p before q
            lo_t = g(p) + 1
            hi_t = g(q) + cap_of(q)
            for t in range(lo_t, hi_t + 1):
                gq = geq(q, t)
                gp = geq(p, t)
                if gq is False or gp is True:
                    continue
                for T in teams:
                    c_ = [notT(T, p), notT(T, q)]
                    if gq is not True:
                        c_.append(-gq)
                    if gp is not False:
                        c_.append(gp)
                    c_.append(o(T, p, q))
                    cl.append(c_)
                    nforce += 1
ntr = 0
for y in V:                                  # same-team AP triples non-monotone
    d = 1
    while y + d <= N:
        x, z = y - d, y + d
        d += 1
        if x in Vs:
            for T in teams:
                gate = [notT(T, x), notT(T, y), notT(T, z)]
                cl.append(gate + [-o(T, x, y), -o(T, y, z)])
                cl.append(gate + [-o(T, z, y), -o(T, y, x)])
            ntr += 1

if mode in ("dyadic", "dyadicAonly"):
    for v in V:
        cl.append([col[v]] if block(v) % 2 == 0 else [-col[v]])
elif mode == "same":
    cl += [[col[15]], [col[16]]]
elif mode == "split":
    cl += [[col[15]], [-col[16]]]
elif mode == "free":
    pass
elif richD is not None:
    from pysat.card import ITotalizer
    cl += [[col[15]], [col[16]]]
    for k in range(6, 2 * m + 1, 2):         # even blocks (M, 2M], M = 0 mod 8
        blk = [v for v in V if block(v) == k]
        lits = [-col[v] for v in blk]        # true <=> donated to B
        if richD == 0:
            cl += [[col[v]] for v in blk]
            continue
        tot = ITotalizer(lits=lits, ubound=richD, top_id=var)
        var = tot.top_id
        cl += tot.cnf.clauses + [[-tot.rhs[richD]]]
else:
    raise SystemExit(f"unknown mode {mode}")

capname = "crown" if crowncap else "full"
print(f"m={m} N={N} CAP={CAP} DMAX={DMAX} mode={mode} cap={capname}: "
      f"n={n} vars={var} clauses={len(cl)} force={nforce} triples={ntr}",
      flush=True)
sol = Cadical195(bootstrap_with=cl)
t0 = time.time()
rounds = 0
tag = f"e119_{m}_{CAP}_{DMAX}_{mode}_{capname}"
while True:
    if not sol.solve():
        print(f"RUNG2C {tag}: UNSAT ({time.time()-t0:.0f}s, {rounds} rounds)"
              f" => every {mode}-coloring needs crown displacement > {CAP}"
              f" at N={N}" if crowncap else
              f"RUNG2C {tag}: UNSAT ({time.time()-t0:.0f}s, {rounds} rounds)",
              flush=True)
        json.dump({"tag": tag, "verdict": "UNSAT"},
                  open(f"data/{tag}.json", "w"))
        break
    model = set(l for l in sol.get_model() if l > 0)
    new = []
    for T in teams:
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in ov[T].items():
            if lit in model:
                B[i, j] = True
            else:
                B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
        def lit_of(p, q, T=T):
            return ov[T][(p, q)] if p < q else -ov[T][(q, p)]
        ii, jj = np.nonzero(miss)
        for i, j in zip(ii[:30000], jj[:30000]):
            k = int(np.nonzero(B[i] & B[:, j])[0][0])
            new.append([-lit_of(i, k), -lit_of(k, j), lit_of(i, j)])
    if not new:
        c = {v: ("A" if col[v] in model else "B") for v in V}
        delta = {v: max([0] + [j for j in L[v] if L[v][j] in model])
                 for v in V}
        blocks = {}
        for v in V:
            k = block(v)
            blocks.setdefault(k, [0, 0])
            blocks[k][0 if c[v] == "A" else 1] += 1
        slivmix = {}
        for k in range(5, 2 * m + 1):        # blocks of length >= 16
            lo = 2 ** (k - 1)
            maj = "A" if blocks[k][0] >= blocks[k][1] else "B"
            slivmix[k] = sorted(v for v in range(lo + 1, lo + 9)
                                if v in c and c[v] != maj)
        low = {v: (c[v], delta[v]) for v in V if v <= 16}
        print(f"RUNG2C {tag}: SAT ({time.time()-t0:.0f}s, {rounds} rounds)",
              flush=True)
        print(f"  crown: 15->{c[15]} d={delta[15]}  16->{c[16]} "
              f"d={delta[16]}", flush=True)
        print(f"  low values (v<=16): {low}", flush=True)
        print(f"  block (nA,nB): { {k: tuple(x) for k, x in sorted(blocks.items())} }",
              flush=True)
        print(f"  sliver values off-majority per block: {slivmix}", flush=True)
        json.dump({"tag": tag, "verdict": "SAT",
                   "coloring": {str(v): c[v] for v in V},
                   "delta": {str(v): delta[v] for v in V},
                   "blocks": {str(k): blocks[k] for k in sorted(blocks)},
                   "sliver_offmajority": {str(k): slivmix[k]
                                          for k in slivmix}},
                  open(f"data/{tag}.json", "w"))
        break
    sol.append_formula(new)
    rounds += 1
    if rounds % 25 == 0:
        print(f"  round {rounds} ({time.time()-t0:.0f}s)", flush=True)
