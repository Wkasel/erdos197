"""e168: parallel e146 catalogue generation for large M (pod, 64 cores).

Semantically IDENTICAL to e146_dp_catalogue.py: same closure engine
(e142 close), same dag_support, same greedy deletion minimization per
attacker pair (each pair is independent), same dedup in (p,q) scan
order, same part2 (J patterns).  Only the pair loop is farmed out to a
multiprocessing pool; results are re-serialized in e146's iteration
order before dedup, so the output JSON is byte-equivalent to a
single-process e146 run.

Run: python3 experiments/e168_catalogue_par.py M [M ...] [--workers N]
Output: data/e146_catalogue_M{M}.json  (e146's canonical path)
Log: data/e146_catalogue.log (append, same format)
"""
import json
import os
import sys
import time
from collections import Counter
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e142_fg_closure import close
from e146_dp_catalogue import (dag_support, th2_restricted_unsat,
                               minimize_pattern, part2)

_M = None


def _init(M):
    global _M
    _M = M


def _work(pq):
    p, q = pq
    X = (4 * _M - p, 4 * _M - q)
    cyc, fact = close(_M, X, verbose=False)
    if not cyc:
        return (p, q, None)
    S = dag_support(cyc, fact)
    assert th2_restricted_unsat(_M, S), (_M, (q, p), 'support fails')
    S = minimize_pattern(_M, S, th2_restricted_unsat)
    return (p, q, sorted(S))


def part1_par(M, workers):
    t0 = time.time()
    pairs = [(p, q) for p in range(1, M + 16) for q in range(0, p)]
    results = {}
    with Pool(workers, initializer=_init, initargs=(M,)) as pool:
        for (p, q, S) in pool.imap_unordered(_work, pairs, chunksize=16):
            results[(p, q)] = S
    # rebuild in e146's exact scan order for identical dedup/src
    patterns = {}
    n_dead = n_alive = 0
    for p in range(1, M + 16):
        for q in range(0, p):
            S = results[(p, q)]
            if S is None:
                n_alive += 1
                continue
            n_dead += 1
            key = tuple(S)
            if key not in patterns:
                patterns[key] = f'fg({q},{p})'
    el = time.time() - t0
    sizes = Counter(len(k) for k in patterns)
    print(f'  part1 M={M}: {n_dead} closure-dead pairs, {n_alive} alive; '
          f'{len(patterns)} distinct minimized patterns '
          f'[{el:.0f}s, {workers}w]', flush=True)
    print(f'    size histogram: {dict(sorted(sizes.items()))}', flush=True)
    return [{'blk': 2, 'S': list(k), 'src': v} for k, v in patterns.items()]


def main():
    args = [a for a in sys.argv[1:]]
    workers = 44
    if '--workers' in args:
        i = args.index('--workers')
        workers = int(args[i + 1])
        del args[i:i + 2]
    scales = [int(a) for a in args] or [176]
    for M in scales:
        cat = part1_par(M, workers) + part2(M)
        path = os.path.join(HERE, '..', 'data', f'e146_catalogue_M{M}.json')
        with open(path, 'w') as f:
            json.dump(cat, f)
        print(f'M={M}: catalogue size {len(cat)} -> {path}', flush=True)
    print('e168: DONE', flush=True)


if __name__ == '__main__':
    main()
