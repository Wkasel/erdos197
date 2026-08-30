#!/usr/bin/env python3
"""e179: GAP-FG-schema — the glued fan-walk calculus GFW and its
coverage of the closure-dead grid (notes/77 SS1; executes the notes/59
SSA.6 "RT-glue extension" designated next step).

Calculus (offsets from 4M, window O = [1, N], N = 2M+15, attackers
r in {p, q}, fan units (2a+r) < a):

  GFW edge set E+(q,p;M) := the least set of ordered pairs (u, v)
  ["u placed before v"] such that
    (U)   every fan unit (2a+r, a) is in E+;
    (W)   every fan-walk fact (h, x), x in D(h) (the e152d descent
          sets), and every RL-head fact (h, 2h-x), x in D(h), is in E+;
    (RL)  (u, v) in E+, 1 <= 2u-v <= N, 2u-v != u  =>  (u, 2u-v) in E+;
    (RT)  (u, v) in E+, 1 <= 2v-u <= N, 2v-u != v  =>  (2v-u, v) in E+.
  Verdict: GFW refutes ThFG(q,p;M) iff E+ has a directed cycle.

Soundness is Lemma GL (notes/77 SS1): every edge is a T/RL/RT-derivable
fact (Lemma CC + Lemma FW), and a directed cycle composes by T to
u < u.  The (RT) closure of walk facts is exactly the "RT-glue"
fragment notes/59 SSA.5 identified in the deep-block DAGs (e152b).

Run:  .venv/bin/python experiments/e179_glue_walk.py M [M ...]
Ground truth: closure-dead pair lists from data/e146_catalogue_M{M}.json
(independent engine e142 via e146; at 48 matches e152/e142o exactly).
Output: data/e179_glue_walk_M{M}.json, data/e179_glue_walk.log (append).

Report per scale:
  * FW coverage (re-derivation of the e152d number at 48; fresh at
    64/80);
  * GFW coverage of the dead grid + residual list w/ (q,p,gap) anatomy;
  * deep-block boundary: min q of any FW-residual pair vs M-12;
  * soundness: alive pairs with a GFW cycle (MUST be 0).
"""
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, '..', 'data')
from e152d_fanwalk import descent

LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gfw_edges(M, p, q):
    """Build E+(q,p;M).  Returns adjacency dict."""
    N = 2 * M + 15
    edges = set()
    queue = []

    def add(u, v):
        if u == v or not (1 <= u <= N and 1 <= v <= N):
            return
        if (u, v) not in edges:
            edges.add((u, v))
            queue.append((u, v))

    # (U) units
    for r in (p, q):
        a = 1
        while 2 * a + r <= N:
            add(2 * a + r, a)
            a += 1
    # (W) walk facts + RL heads
    for h in range(1, N + 1):
        Dh = descent(h, p, q, N)
        for x in Dh:
            add(h, x)
            w = 2 * h - x
            if 1 <= w <= N:
                add(h, w)
    # (RL)/(RT) edge-wise closure
    while queue:
        u, v = queue.pop()
        w = 2 * u - v
        if 1 <= w <= N and w != u:
            add(u, w)
        w = 2 * v - u
        if 1 <= w <= N and w != v:
            add(2 * v - u, v)
    adj = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v)
    return adj


def has_cycle(adj):
    color = {}
    for s in list(adj):
        if color.get(s):
            continue
        stack = [(s, iter(adj.get(s, ())))]
        color[s] = 1
        while stack:
            v, it = stack[-1]
            adv = False
            for w in it:
                c = color.get(w, 0)
                if c == 1:
                    return True
                if c == 0:
                    color[w] = 1
                    stack.append((w, iter(adj.get(w, ()))))
                    adv = True
                    break
            if not adv:
                color[v] = 2
                stack.pop()
    return False


def fw_only_refutes(M, p, q):
    """The plain e152d fan-walk verdict (for the boundary audit)."""
    N = 2 * M + 15
    adj = {}
    for h in range(1, N + 1):
        Dh = descent(h, p, q, N)
        out = set(Dh)
        for x in Dh:
            w = 2 * h - x
            if 1 <= w <= N and w != h:
                out.add(w)
        out.discard(h)
        adj[h] = out
    return has_cycle(adj)


def run(M):
    t0 = time.time()
    log(f'== e179 glued fan-walk, M={M} (N={2*M+15}) ==')
    with open(os.path.join(DATA, f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    dead = set()
    for pat in cat:
        src = pat.get('src', '')
        if src.startswith('fg('):
            qq, pp = src[3:-1].split(',')
            dead.add((int(qq), int(pp)))
    grid = [(q, p) for q in range(0, M + 15)
            for p in range(q + 1, M + 16)]
    alive = [qp for qp in grid if qp not in dead]
    log(f'grid {len(grid)}: dead {len(dead)} / alive {len(alive)} '
        f'(ground truth: e146 catalogue)')

    fw_cov, gfw_cov, resid = [], [], []
    for (q, p) in sorted(dead):
        fw = fw_only_refutes(M, p, q)
        if fw:
            fw_cov.append((q, p))
            gfw_cov.append((q, p))          # GFW extends FW
            continue
        if has_cycle(gfw_edges(M, p, q)):
            gfw_cov.append((q, p))
        else:
            resid.append((q, p))
    log(f'FW  coverage: {len(fw_cov)}/{len(dead)}')
    log(f'GFW coverage: {len(gfw_cov)}/{len(dead)}; residual {len(resid)}')
    fw_resid = sorted(set(map(tuple, dead)) - set(fw_cov))
    qmin_fwres = min((q for q, p in fw_resid), default=None)
    log(f'FW-residual: {len(fw_resid)}; min q = {qmin_fwres} '
        f'(deep-block edge M-12 = {M-12})')
    deep_fwres = [qp for qp in fw_resid if qp[0] >= M - 12]
    log(f'  FW-residual inside deep block q >= M-12: {len(deep_fwres)}; '
        f'outside: {len(fw_resid) - len(deep_fwres)}')
    if resid:
        gh = Counter(p - q for q, p in resid)
        qh = Counter(q for q, p in resid)
        log(f'GFW residual gap histogram: {dict(sorted(gh.items()))}')
        log(f'GFW residual q histogram: {dict(sorted(qh.items()))}')
        log(f'GFW residual pairs: {resid}')
    # soundness: no alive pair may have a GFW cycle
    bad = []
    for (q, p) in alive:
        if has_cycle(gfw_edges(M, p, q)):
            bad.append((q, p))
    log(f'soundness (alive pairs with GFW cycle, MUST be 0): '
        f'{len(bad)} {bad or ""}')
    log(f'M={M} done in {time.time()-t0:.0f}s')
    out = {'M': M, 'n_dead': len(dead), 'n_alive': len(alive),
           'fw_cov': len(fw_cov), 'gfw_cov': len(gfw_cov),
           'gfw_residual': resid, 'fw_residual_n': len(fw_resid),
           'fw_residual_qmin': qmin_fwres,
           'fw_residual_deep': len(deep_fwres),
           'alive_bad': bad}
    with open(os.path.join(DATA, f'e179_glue_walk_M{M}.json'), 'w') as f:
        json.dump(out, f)
    return out


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [48]
    for M in Ms:
        run(M)
    with open(os.path.join(DATA, 'e179_glue_walk.log'), 'a') as f:
        f.write('\n'.join(LOG) + '\n')
    log('e179: DONE')


if __name__ == '__main__':
    main()
