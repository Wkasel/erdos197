"""Erdős #197 — G1: Geneson arXiv:2608.12604 alpha_N(3) >= 2/3 witness generator.

Construction (paper Section 3, Lemmas 3.1-3.3):
  M_0 = 1, S_0 = {}.  For k >= 1:
    L_k = 4 * M_{k-1}                                (paper eq. 3.3)
    B_k = union_{j=0}^{k} [L_k 4^j + M_{k-1}, 2 L_k 4^j]   (paper eq. 3.4)
    M_k = 2 L_k 4^k,  S = union_k B_k               (paper eq. 3.5)
  Permutation: each block B_k is ordered by (any) finite 3-AP-free order —
  canonically the Ardal-Brown-Jungic binary order (bit-reversal /
  van der Corput order, paper Section 2) — and the blocks are concatenated
  sigma_1 sigma_2 sigma_3 ... (paper eq. 3.6).

  Lemma 3.1 (the geometry): with A subset [1,M], L > 2M, blocks
  [L 4^j + M, 2 L 4^j], NO 3-AP inside A u B meets both A and B: the
  reflection z = 2y - a of a in A through y in octave j lands in the silent
  zone (2 L 4^j, 4 L 4^j + M) strictly between octaves j and j+1.
  Hence the only 3-APs inside S live within a single B_k, and the in-block
  ABJ order kills those.  Middle-term rule (Lemma 2.2): in the ABJ order the
  midpoint of every 3-AP precedes both endpoints or follows both.

Free parameters generalizing the construction (proof survives verbatim):
  lam   >= 3 : L_k = lam * M_{k-1}      (Lemma 3.1 needs L > 2M; paper: 4)
  ratio >= 4 : octave spacing L r^j     (proof needs z <= 4 L r^j - 1 <
               L r^{j+1} + M, i.e. r >= 4; paper: 4 — max density)
  J(k) -> oo : number of octaves at stage k is J(k)+1 (paper: J(k) = k);
               any divergent J gives upper density -> 2/3 along n = M_k.
  top mult 2 : block top 2 L r^j; a top t*L r^j needs 2t <= r (paper t=2, r=4).
  sigma_k    : any 3-AP-free order per block (canonical: ABJ bit-reversal).

Usage:
  .venv/bin/python experiments/g1_geneson_gen.py            # full N=4096 run
  .venv/bin/python experiments/g1_geneson_gen.py --raw      # + unassisted SAT
"""
import json
import os
import sys
import time
from functools import cmp_to_key


# ---------------------------------------------------------------- generator

def geneson_blocks(N, lam=4, ratio=4, J=None):
    """All octave-blocks of the stage construction intersected with [1, N].

    Returns list of dicts {k, j, lo, hi, lo_full, hi_full, M_prev, L}
    in construction (= permutation) order: k ascending, j ascending.
    lo/hi are the truncated-to-N endpoints; *_full the untruncated block.
    """
    J = J if J is not None else (lambda k: k)
    out = []
    M_prev = 1
    k = 0
    while True:
        k += 1
        L = lam * M_prev
        if L + M_prev > N:          # first block of stage k already beyond N
            break
        for j in range(J(k) + 1):
            lo = L * ratio ** j + M_prev
            hi = 2 * L * ratio ** j
            if lo > N:
                break
            out.append(dict(k=k, j=j, lo=lo, hi=min(hi, N),
                            lo_full=lo, hi_full=hi, M_prev=M_prev, L=L))
        M_prev = 2 * L * ratio ** J(k)     # M_k (untruncated)
    return out


def geneson_witness(N, lam=4, ratio=4, J=None):
    """Sorted list W(params) intersect [1, N]."""
    W = []
    for b in geneson_blocks(N, lam, ratio, J):
        W.extend(range(b['lo'], b['hi'] + 1))
    return W


# ------------------------------------------------- ABJ / bit-reversal order

def bitrev(u, T):
    """Reverse the T-bit binary expansion of u (0 <= u < 2^T)."""
    r = 0
    for _ in range(T):
        r = (r << 1) | (u & 1)
        u >>= 1
    return r


def abj_precedes(u, v):
    """Paper Section 2 definition: q = 1 + nu_2(v-u); u < v in ABJ order
    iff rho_{2^q}(u mod 2^q) < rho_{2^q}(v mod 2^q) (bit-reversal ranks)."""
    assert u != v
    d = v - u
    q = 1 + ((d & -d).bit_length() - 1)          # 1 + nu_2(v - u)
    return bitrev(u % (1 << q), q) < bitrev(v % (1 << q), q)


def abj_sort(vals):
    """Sort positive integers by the ABJ order.  Equivalent fast form:
    lexicographic on reversed bit strings = bitrev key at common width."""
    T = max(vals).bit_length()
    return sorted(vals, key=lambda u: bitrev(u, T))


def geneson_permutation(N, lam=4, ratio=4, J=None):
    """The paper's omega-permutation restricted to [1, N]: sigma_1 sigma_2 ...
    where sigma_k is the ABJ order on the ENTIRE stage B_k (all its octaves
    together — intra-stage cross-octave APs exist and sigma_k must kill them;
    Lemma 3.1 only excludes cross-STAGE APs)."""
    perm = []
    stage_vals = {}
    for b in geneson_blocks(N, lam, ratio, J):
        stage_vals.setdefault(b['k'], []).extend(
            range(b['lo'], b['hi'] + 1))
    for k in sorted(stage_vals):
        perm.extend(abj_sort(stage_vals[k]))
    return perm


# ----------------------------------------------------------- verifications

def find_monotone_3ap(perm):
    """Return a violating (x, y, z) or None.  O(n^2): for each ordered pair
    of positions (u at i) < (v at j), the continuation w = 2v - u is a
    monotone 3-AP iff w in set and pos[w] > j."""
    pos = {v: i for i, v in enumerate(perm)}
    n = len(perm)
    for i in range(n):
        u = perm[i]
        for j in range(i + 1, n):
            v = perm[j]
            w = 2 * v - u
            if w != v and w in pos and pos[w] > j:
                return (u, v, w)
    return None


def cross_stage_aps(blocks):
    """Empirical Lemma 3.1: count 3-APs of W meeting >= 2 distinct STAGES
    (intra-stage cross-octave APs are allowed — sigma_k handles them)."""
    owner = {}
    for b in blocks:
        for v in range(b['lo'], b['hi'] + 1):
            owner[v] = b['k']
    vals = sorted(owner)
    bad = 0
    for a in vals:
        for y in vals:
            if y <= a:
                continue
            z = 2 * y - a
            if z in owner and len({owner[a], owner[y], owner[z]}) > 1:
                bad += 1
    return bad


def pure_complete_clauses(W):
    """The pure-complete-X system on W (e22_pure4096.py conventions):
    vars t[(i,j)] i<j meaning W[i] precedes W[j]; monotone-3-AP clauses plus
    in-team completion clauses.  Returns (clauses, before, nvars)."""
    V = sorted(W)
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    t = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            t[(i, j)] = top

    def before(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]

    cl = []
    Vs = set(V)
    X = V[-1]
    for y in V:
        d = 1
        while y + d <= X:
            a, c = y - d, y + d
            if a in Vs and c in Vs:
                cl.append([-before(a, y), -before(y, c)])
                cl.append([-before(c, y), -before(y, a)])
            d += 1
    for a in V:
        for b in V:
            if b <= a:
                continue
            c = 2 * b - a
            if c in Vs:
                cl.append([-before(a, b), before(c, b)])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                cl.append([-before(b, a), before(d2, a)])
    return cl, before, top


def sat_certify(W, perm):
    """Certify SAT of the pure-complete system with the explicit witness:
    (1) python-check every clause is satisfied under the permutation's
    assignment; (2) hand Cadical the clauses PLUS the assignment as unit
    clauses and solve once (unit propagation confirms consistency)."""
    from pysat.solvers import Cadical195
    cl, before, top = pure_complete_clauses(W)
    pos = {v: i for i, v in enumerate(perm)}
    V = sorted(W)
    truth = [False] * (top + 1)          # truth[|lit|] for positive lit
    units = []
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            u, w = V[i], V[j]
            lit = before(u, w)
            val = pos[u] < pos[w]
            truth[abs(lit)] = val if lit > 0 else not val
            units.append([abs(lit)] if truth[abs(lit)] else [-abs(lit)])

    def sat_lit(l):
        return truth[l] if l > 0 else not truth[-l]

    unsat_clauses = sum(1 for c in cl if not any(sat_lit(l) for l in c))
    s = Cadical195(bootstrap_with=cl + units)
    ok = s.solve()
    s.delete()
    return ok and unsat_clauses == 0, len(cl), top


def sat_raw(W, max_rounds=4000, verbose=False):
    """Unassisted lazy-transitivity solve (e22 style).  Returns order or False."""
    import numpy as np
    from pysat.solvers import Cadical195
    V = sorted(W)
    n = len(V)
    cl, before, top = pure_complete_clauses(W)
    t = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            t[(i, j)] = c
    s = Cadical195(bootstrap_with=cl)
    rounds = 0
    t0 = time.time()
    while True:
        rounds += 1
        if rounds > max_rounds:
            raise RuntimeError("rounds exhausted")
        if not s.solve():
            return False
        model = s.get_model()
        posv = np.zeros(top + 1, dtype=bool)
        for l in model:
            if 0 < l <= top:
                posv[l] = True
        B = np.zeros((n, n), dtype=bool)
        for (i, j), var in t.items():
            if posv[var]:
                B[i, j] = True
            else:
                B[j, i] = True
        wins = B.sum(axis=1)
        order = np.argsort(-wins, kind='stable')
        R = B[np.ix_(order, order)]
        iu = np.triu_indices(n, 1)
        bad_idx = np.nonzero(~R[iu])[0]
        if len(bad_idx) == 0:
            return [V[i] for i in order]
        added = 0
        for bi in bad_idx[:30000]:
            a_, b_ = iu[0][bi], iu[1][bi]
            i, j = order[a_], order[b_]
            ks = np.nonzero(B[i] & B[:, j])[0]
            if len(ks):
                k = int(ks[0])
                u, w, x = V[i], V[k], V[j]
                s.add_clause([-before(u, w), -before(w, x), before(u, x)])
                added += 1
                if added > 20000:
                    break
        if verbose and rounds % 20 == 0:
            print(f"  raw round {rounds}: {len(bad_idx)} viol, "
                  f"{time.time()-t0:.0f}s", flush=True)


# -------------------------------------------------------------- complement

def complement_structure(N, lam=4, ratio=4, J=None):
    """Predicted maximal intervals of [1, N] \\ W with labels.

    Every complement interval is one of:
      initial            [1, lam*M_0 + M_0 - 1]  (= [1, 4] at defaults)
      inter-stage chasm  (M_k, L_{k+1})          pure gap, factor lam
      bottom sliver      [L r^j, L r^j + M_{k-1} - 1]  width M_{k-1},
                         shaved off the bottom of every octave
      inter-octave gap   (2 L r^j, L r^{j+1})    the silent zone of Lemma 3.1
    Adjacent gap+sliver pieces merge into single maximal intervals; we report
    both the labeled pieces and the merged maximal intervals.
    """
    blocks = geneson_blocks(N, lam, ratio, J)
    pieces = []
    prev_hi = 0
    for b in blocks:
        if b['lo'] > prev_hi + 1:
            lo_gap, hi_gap = prev_hi + 1, b['lo'] - 1
            sliver_lo = b['lo'] - b['M_prev']            # = L r^j
            labels = []
            if sliver_lo > lo_gap:
                kind = ('initial' if prev_hi == 0 else
                        ('inter-octave gap' if b['j'] > 0
                         else 'inter-stage chasm'))
                labels.append((lo_gap, sliver_lo - 1, kind,
                               dict(k=b['k'], j=b['j'])))
                labels.append((sliver_lo, hi_gap, 'bottom sliver',
                               dict(k=b['k'], j=b['j'],
                                    width=b['M_prev'])))
            else:                                        # gap entirely sliver
                labels.append((lo_gap, hi_gap, 'bottom sliver (truncated)',
                               dict(k=b['k'], j=b['j'],
                                    width=b['M_prev'])))
            pieces.append(dict(lo=lo_gap, hi=hi_gap, parts=labels))
        prev_hi = max(prev_hi, b['hi'])
    if prev_hi < N:
        pieces.append(dict(lo=prev_hi + 1, hi=N,
                           parts=[(prev_hi + 1, N, 'tail (next stage chasm)',
                                   {})]))
    return pieces


# ------------------------------------------------------------------- main

def main():
    raw = '--raw' in sys.argv
    N = 4096
    t0 = time.time()

    blocks = geneson_blocks(N)
    W = geneson_witness(N)
    perm = geneson_permutation(N)
    print(f"Geneson witness W cap [1,{N}] (defaults lam=4 ratio=4 J(k)=k)")
    for b in blocks:
        print(f"  stage k={b['k']} j={b['j']}: [{b['lo']}, {b['hi']}] "
              f"({b['hi'] - b['lo'] + 1} elts, sliver width {b['M_prev']})")
    print(f"|W| = {len(W)}, density at N: {len(W)/N:.4f} "
          f"(paper bound at k=2: {2/3 - 1/96 - 3/128:.4f})")

    # |B_k| formula (3.7) check
    for k, Mprev, L in [(1, 1, 4), (2, 32, 128)]:
        pred = L * (4 ** (k + 1) - 1) // 3 - (k + 1) * (Mprev - 1)
        got = sum(b['hi'] - b['lo'] + 1 for b in blocks if b['k'] == k)
        print(f"|B_{k}| formula (3.7): predicted {pred}, generated {got}, "
              f"{'OK' if pred == got else 'MISMATCH'}")

    # sanity: permutation is a permutation of W
    assert sorted(perm) == W, "perm is not a permutation of W"

    # sanity: bitrev key order == ABJ definition on sample pairs
    import random
    random.seed(197)
    T = max(W).bit_length()
    for _ in range(2000):
        u, v = random.sample(W, 2)
        assert abj_precedes(u, v) == (bitrev(u, T) < bitrev(v, T)), (u, v)
    print("ABJ order: bitrev key == paper definition on 2000 random pairs OK")

    # empirical Lemma 3.1: zero cross-stage APs
    t1 = time.time()
    cb = cross_stage_aps(blocks)
    print(f"cross-stage 3-APs inside W: {cb} "
          f"({'OK — Lemma 3.1 confirmed' if cb == 0 else 'VIOLATION'}) "
          f"[{time.time()-t1:.0f}s]")
    assert cb == 0

    # direct global check: permutation has no monotone 3-AP
    t1 = time.time()
    bad = find_monotone_3ap(perm)
    print(f"monotone 3-AP in explicit permutation: "
          f"{bad or 'NONE — witness order verified'} [{time.time()-t1:.0f}s]")
    assert bad is None

    # pure-complete SAT with solver-checked witness assignment
    t1 = time.time()
    ok, ncl, nv = sat_certify(W, perm)
    print(f"pure-complete-{N} on W: n={len(W)} vars={nv} clauses={ncl} "
          f"-> {'SAT (witness assignment accepted by Cadical)' if ok else 'UNSAT?!'} "
          f"[{time.time()-t1:.0f}s]")
    assert ok

    # unassisted raw solve at N=1024 (small, fast independent confirmation)
    t1 = time.time()
    W1k = geneson_witness(1024)
    r = sat_raw(W1k)
    print(f"pure-complete-1024 raw solve: n={len(W1k)} -> "
          f"{'SAT' if r is not False else 'UNSAT?!'} [{time.time()-t1:.0f}s]")
    assert r is not False
    assert find_monotone_3ap(r) is None
    print("  raw-solver order independently 3-AP-free OK")

    # generalized parameters spot checks (direct order verification)
    for lam, ratio, Jf, tag in [(3, 4, None, 'lam=3'),
                                (4, 5, None, 'ratio=5'),
                                (4, 4, (lambda k: 2 * k), 'J(k)=2k'),
                                (5, 6, (lambda k: k + 1), 'lam=5 r=6 J=k+1')]:
        p = geneson_permutation(2048, lam=lam, ratio=ratio, J=Jf)
        b = find_monotone_3ap(p)
        print(f"generalized params {tag}: |W cap [1,2048]|={len(p)} "
              f"-> {'3-AP-free OK' if b is None else f'FAIL {b}'}")
        assert b is None

    # complement structure: predicted intervals == actual complement
    pieces = complement_structure(N)
    Wset = set(W)
    comp = [v for v in range(1, N + 1) if v not in Wset]
    pred = []
    for p in pieces:
        pred.extend(range(p['lo'], p['hi'] + 1))
    assert pred == comp, "complement prediction mismatch"
    print(f"complement [1,{N}] \\ W: {len(comp)} integers, "
          f"predicted intervals match exactly:")
    for p in pieces:
        for (lo, hi, kind, meta) in p['parts']:
            print(f"  [{lo:5d}, {hi:5d}] ({hi - lo + 1:5d}) {kind} {meta}")

    # running-density profile of W (lim sup 2/3, lim inf 2/15 at chasm ends)
    cnt = 0
    lows = []
    dens_at = {}
    for v in range(1, N + 1):
        if v in Wset:
            cnt += 1
        dens_at[v] = cnt / v
    for b in blocks:
        if b['j'] == 0 and b['k'] > 1:
            lows.append((b['lo'], dens_at[b['lo'] - 1]))
    print("density at stage-chasm ends (theory -> 2/15 = 0.1333):",
          [(v, round(d, 4)) for v, d in lows])
    print(f"density at N={N} (= M_2): {dens_at[N]:.4f} (theory -> 2/3)")

    # artifacts
    os.makedirs('data', exist_ok=True)
    with open('data/g1_geneson_4096.json', 'w') as f:
        json.dump(dict(N=N, params=dict(lam=4, ratio=4, J='k'),
                       blocks=[{k: b[k] for k in
                                ('k', 'j', 'lo', 'hi', 'M_prev', 'L')}
                               for b in blocks],
                       W_size=len(W), permutation=perm,
                       verification=dict(
                           cross_stage_aps=cb,
                           perm_3ap_free=bad is None,
                           pure_complete_4096='SAT' if ok else 'UNSAT',
                           n=len(W), nvars=nv, nclauses=ncl),
                       complement_pieces=[
                           dict(lo=p['lo'], hi=p['hi'],
                                parts=[dict(lo=lo, hi=hi, kind=kind, **meta)
                                       for (lo, hi, kind, meta) in p['parts']])
                           for p in pieces]), f)
    print("wrote data/g1_geneson_4096.json")

    if raw:
        t1 = time.time()
        r = sat_raw(W, verbose=True)
        print(f"pure-complete-{N} RAW solve: "
              f"{'SAT' if r is not False else 'UNSAT?!'} [{time.time()-t1:.0f}s]")

    print(f"total {time.time()-t0:.0f}s — ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
