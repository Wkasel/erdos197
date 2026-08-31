#!/usr/bin/env python3
"""e187: FRONT GAP-RES — ODD-KILL for the clustered/low-pair regime
(notes/84-res.md SS1-2).

Setting (notes/59 SSA.0): window O = [1, N], attackers at offsets q < p
(gap g = p - q ODD), fan units (2a+r) < a for r in {p, q}, 2a+r <= N,
a >= 1; calculus T/RL/RT (Lemma CC, notes/59 — PROVED).

KEY STRUCTURE (odd gap): each descent-rule residue is parity-forced, so
the rule-(i) iteration at a head h is DETERMINISTIC — the SPIRAL:
    x0 = (h - r0)/2,  r0 == h (mod 2) unique;
    x_{n+1} = (2h - x_n - r_{n+1})/2,  r_{n+1} == x_n (mod 2) unique
    [each step: RL on (h < x_n) to 2h - x_n <= N, then the unit, then T]
giving facts h < x_n.  Deviation from the r*-fixed point tau
(3 tau = 2h - r*, tau == r* mod 2) obeys
    delta_{n+1} = -(delta_n + eps_n * g * s)/2,  eps_n = delta_n mod 2,
s = +-1 — base-(-2) digit extraction in units of g (Lemma LAND):
    * delta_n == delta_0 * (-2)^{-n} (mod g)  [exactness],
    * if g | delta_0 the spiral LANDS on tau in <= O(log) steps,
    * |delta_n| <= max(|delta_0|, g) throughout.

THE S FAMILY (two-sided spiral, transient landing):
    u = base + 2t (base in {q, p}, t >= 1)     [low head]
    x = x_m(u), the m-th value of u's spiral   [facts u < x]
    w = 2u - x   (RL on u < x_m; w <= N)       [high head]
    w's spiral hits u at some step K           [fact w < u]
    => u < w < u, contradiction (T + irreflexivity).
S1 = the clean sub-family m = 0, u the r*-fixed point of w (r* = base):
then w = 3t + 2q (base q), delta_0(w) = -(t + r0)/2, landing iff
g | (t + r0)/2 <=> t == -q (mod 2g) or t == -p (mod 2g); minimal valid
t <= g; windows reduce to the FIRST reflection: 9t + 6q + r0 <= 2N.
COROLLARY (region): every odd-gap pair with 7q + 10g <= 2N is dead.

Every emitted certificate is re-verified by check_cert(), an
independent Lemma-CC step-walker sharing no code with the generator.

Modes:
  map  M...    coverage vs e146 ground truth (dead lists) + soundness
               (alive pairs MUST get no certificate)
  fresh M...   fresh windows: construct+verify on the odd grid, region
               predicate cross-check, e142 closure spot-checks
  tower m...   halved tower shapes W2e/W2o(m) (F(2m+7/8, m+7))

Output: data/e187_oddkill_{map,fresh,tower}.json, data/e187_oddkill.log.
"""
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, '..', 'data')

LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ---------------- the forced spiral ----------------

def spiral_vals(h, q, p, N, maxlen=200):
    """Forced rule-(i) spiral at head h: values x with derived fact
    h < x.  Stops (exactly) at window breach, positivity breach,
    self-hit, or period."""
    r0 = q if (h - q) % 2 == 0 else p
    if h < r0 + 2:
        return []
    xs = [(h - r0) // 2]
    seen = {xs[0]}
    while len(xs) < maxlen:
        x = xs[-1]
        refl = 2 * h - x
        if refl > N:
            break
        r = q if (refl - q) % 2 == 0 else p
        y = (refl - r) // 2
        if y < 1 or y == h or y in seen:
            break
        xs.append(y)
        seen.add(y)
    return xs


# ---------------- S-family search ----------------

def s_cert(q, p, N):
    """Smallest S-family certificate (base, t ascending).  Returns the
    full data needed by the independent checker, or None."""
    for base in (q, p):
        t = 1
        while True:
            u = base + 2 * t
            if u > N:
                break
            O1 = spiral_vals(u, q, p, N)
            for m, x in enumerate(O1):
                w = 2 * u - x
                if w == u or not (1 <= w <= N):
                    continue
                O2 = spiral_vals(w, q, p, N)
                if u in O2:
                    K = O2.index(u)
                    return dict(q=q, p=p, N=N, base=base, t=t, u=u, m=m,
                                x=x, w=w, K=K, up=O1[:m + 1],
                                down=O2[:K + 1])
            t += 1
    return None


# ---------------- general FW 2-cycle (full forced descent) ----------------

def descent_words(h, q, p, N):
    """Full forced descent set D(h) (e152d rules seed/(i)/(ii)/(iii);
    for odd gap every residue is parity-forced) with parent pointers."""
    D = {}
    stack = []
    for r in (q, p):
        if (h - r) % 2 == 0 and (h - r) // 2 >= 1:
            a = (h - r) // 2
            if a != h and a not in D:
                D[a] = ('s', None, r)
                stack.append(a)
    i = 0
    while i < len(stack):
        x = stack[i]
        i += 1
        refl = 2 * h - x
        if 1 <= refl <= N:
            for r in (q, p):
                if (refl - r) % 2 == 0 and (refl - r) // 2 >= 1:
                    y = (refl - r) // 2
                    if y != h and y not in D:
                        D[y] = ('i', x, r)
                        stack.append(y)
        for r in (q, p):
            if (x - r) % 2 == 0 and (x - r) // 2 >= 1:
                b = (x - r) // 2
                if b != h and b not in D:
                    D[b] = ('III', x, r)
                    stack.append(b)
                z = 2 * x - b
                if z <= N and z != h and z not in D:
                    D[z] = ('II', x, r)
                    stack.append(z)
    return D


def _dpath(D, x):
    path = []
    while x is not None:
        rule, par, r = D[x]
        path.append((rule, x, r))
        x = par
    return list(reversed(path))


def fw2_cert(q, p, N, umax=None):
    """Smallest general FW 2-cycle: x in D(u), w = 2u - x, u in D(w).
    Returns checker-ready data or None."""
    for u in range(1, (umax or N) + 1):
        Du = descent_words(u, q, p, N)
        for x in sorted(Du):
            w = 2 * u - x
            if 1 <= w <= N and w != u:
                Dw = descent_words(w, q, p, N)
                if u in Dw:
                    return dict(q=q, p=p, N=N, u=u, x=x, w=w,
                                up=_dpath(Du, x), down=_dpath(Dw, u))
    return None


def check_fw2(c):
    """Independent Lemma-CC/FW step-walker for general 2-cycles."""
    q, p, N = c['q'], c['p'], c['N']
    u, w, x = c['u'], c['w'], c['x']
    _walk_path(q, p, N, u, c['up'], x)
    assert w == 2 * u - x and 1 <= w <= N and w != u, 'RL lift'
    _walk_path(q, p, N, w, c['down'], u)
    return True


def fwk_cert(q, p, N):
    """Shortest general FW cycle (any length): heads h_1..h_k, each
    edge h -> z a descent edge (z in D(h)) or an RL-head edge
    (z = 2h - x, x in D(h)).  Returns checker-ready data or None."""
    from collections import deque as _dq
    Ds = {}

    def D(h):
        if h not in Ds:
            Ds[h] = descent_words(h, q, p, N)
        return Ds[h]

    def outs(h):
        o = set(D(h))
        for x in D(h):
            z = 2 * h - x
            if 1 <= z <= N and z != h:
                o.add(z)
        o.discard(h)
        return o

    adj = {h: outs(h) for h in range(1, N + 1)}
    best = None
    for s in range(1, N + 1):
        prev = {s: None}
        bfs = _dq([s])
        hit = False
        while bfs and not hit:
            v = bfs.popleft()
            for zz in adj[v]:
                if zz == s:
                    path = [v]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])
                    path.reverse()
                    path.append(s)
                    if best is None or len(path) < len(best):
                        best = path
                    hit = True
                    break
                if zz not in prev:
                    prev[zz] = v
                    bfs.append(zz)
    if best is None:
        return None
    edges = []
    for i in range(len(best) - 1):
        h, z = best[i], best[i + 1]
        if z in D(h):
            edges.append(dict(h=h, z=z, kind='D', path=_dpath(D(h), z)))
        else:
            x = 2 * h - z
            assert x in D(h), 'RL edge without descent source'
            edges.append(dict(h=h, z=z, kind='RL', x=x,
                              path=_dpath(D(h), x)))
    return dict(q=q, p=p, N=N, cycle=best, edges=edges)


def check_fwk(c):
    """Independent checker for general FW cycles: validates every
    descent path (as in check_fw2) and every RL lift; the cycle then
    composes by T to a contradiction (Lemma FW(c))."""
    q, p, N = c['q'], c['p'], c['N']
    cyc = c['cycle']
    assert len(cyc) >= 3 and cyc[0] == cyc[-1], 'cycle shape'
    assert len(c['edges']) == len(cyc) - 1, 'edge count'
    for i, e in enumerate(c['edges']):
        h, z = e['h'], e['z']
        assert h == cyc[i] and z == cyc[i + 1], f'edge endpoints @{i}'
        target = e['x'] if e['kind'] == 'RL' else z
        _walk_path(q, p, N, h, e['path'], target)
        if e['kind'] == 'RL':
            assert z == 2 * h - e['x'] and 1 <= z <= N and z != h, \
                f'RL lift @{i}'
    return True


def _walk_path(q, p, N, h, path, target):
    """Validate a forced-descent derivation path at head h (rules
    s/i/III/II with explicit residues); arithmetic assertions only."""
    assert 1 <= h <= N, 'head in window'
    derived = set()
    for j, (rule, val, r) in enumerate(path):
        assert r in (q, p) and val >= 1 and val != h, f'node @{j}'
        if rule == 's':
            assert j == 0 and h == 2 * val + r and h <= N, 'seed'
        else:
            par = path[j - 1][1]
            assert par in derived, f'parent @{j}'
            if rule == 'i':
                refl = 2 * h - par
                assert 1 <= refl <= N and refl == 2 * val + r, f'i @{j}'
            elif rule == 'III':
                assert par == 2 * val + r and par <= N, f'III @{j}'
            elif rule == 'II':
                b = (par - r) // 2
                assert par == 2 * b + r and b >= 1, f'II-b @{j}'
                assert val == 2 * par - b and val <= N, f'II @{j}'
            else:
                raise AssertionError(f'rule {rule}')
        derived.add(val)
    assert path[-1][1] == target, 'path target'


def s1_region(q, p, N):
    """The PROVED S1 sufficient predicate: exists t == -q or -p
    (mod 2g), t >= 1, with 9t + 6q + r0 <= 2N (r0 = q if t == q mod 2
    else p) and g | (t + r0)/2.  (Scanning t <= 2g suffices.)"""
    g = p - q
    for t in range(1, 2 * g + 1):
        r0 = q if (t - q) % 2 == 0 else p
        if (t + r0) % 2 == 0 and ((t + r0) // 2) % g == 0 \
                and 9 * t + 6 * q + r0 <= 2 * N:
            return t
    return None


def fg_high(q, p, N):
    """Gamma_1 (FG-high, notes/55 SS5.3b PROVED): p >= 2q+1, 5p-6q <= N."""
    return p >= 2 * q + 1 and 5 * p - 6 * q <= N


# ---------------- independent checker ----------------

def check_cert(c):
    """Replays the certificate as Lemma-CC applications.  Pure
    arithmetic assertions; no shared logic with the generator."""
    q, p, N = c['q'], c['p'], c['N']
    u, w, x = c['u'], c['w'], c['x']
    up, down = c['up'], c['down']
    g = p - q
    assert g % 2 == 1 and 0 <= q < p, 'pair shape'
    assert 1 <= u <= N and 1 <= w <= N and w != u, 'heads in window'

    def walk(h, xs):
        """verify xs are successive facts h < xs[i] of the forced walk"""
        r0 = q if (h - q) % 2 == 0 else p
        assert (h - r0) % 2 == 0, 'seed parity'
        assert xs[0] == (h - r0) // 2 and xs[0] >= 1, 'seed value'
        assert h == 2 * xs[0] + r0 and h <= N, 'seed unit'
        for i in range(len(xs) - 1):
            refl = 2 * h - xs[i]                    # RL on (h, xs[i])
            assert 1 <= refl <= N and refl != h, f'RL window @{i}'
            r = q if (refl - q) % 2 == 0 else p
            assert refl == 2 * xs[i + 1] + r, f'unit @{i}'
            assert xs[i + 1] >= 1 and xs[i + 1] != h, f'target @{i}'

    walk(u, up)                                     # facts u < x_j
    assert up[-1] == x, 'prefix ends at x'
    assert w == 2 * u - x and 1 <= w <= N and w != u, 'RL lift to w'
    walk(w, down)                                   # facts w < y_j
    assert down[-1] == u, 'landing on u'
    return True                                     # u < w and w < u


# ---------------- runs ----------------

def dead_from_catalogue(M):
    with open(os.path.join(DATA, f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    dead = set()
    for pat in cat:
        src = pat.get('src', '')
        if src.startswith('fg('):
            a, b = src[3:-1].split(',')
            dead.add((int(a), int(b)))
    return dead


def odd_grid(A):
    return [(q, p) for q in range(0, A) for p in range(q + 1, A + 1)
            if (p - q) % 2 == 1]


def in_region(q, p, N):
    """The ODD-KILL-LOW region R(N): 3q + g <= N - 24 and
    2p <= N - 7 (g = p - q)."""
    return 3 * q + (p - q) <= N - 24 and 2 * p <= N - 7


def classify(q, p, N):
    """Returns (covered?, tags).  Verifies every emitted certificate
    independently; asserts the proved-region implications."""
    tags = []
    c = s_cert(q, p, N)
    if c:
        check_cert(c)
        tags.append('S')
    if fg_high(q, p, N):
        tags.append('FG')
    t = s1_region(q, p, N)
    if t is not None:
        assert c is not None, f'S1 region without S cert at {(q, p, N)}'
        tags.append('S1')
    g = p - q
    if 7 * q + 10 * g <= 2 * N:
        assert t is not None, f'corollary region outside S1 at {(q, p, N)}'
        tags.append('COR')
    if not tags[:1] == ['S'] and 'FG' not in tags:
        c2 = fw2_cert(q, p, N)
        if c2:
            check_fw2(c2)
            tags.append('FW2')
        elif in_region(q, p, N):
            ck = fwk_cert(q, p, N)
            if ck:
                check_fwk(ck)
                tags.append('FWK')
    if in_region(q, p, N):
        assert ('S' in tags) or ('FG' in tags) or ('FW2' in tags) \
            or ('FWK' in tags), f'REGION LAW violated at {(q, p, N)}'
        tags.append('R')
    covered = ('S' in tags) or ('FG' in tags) or ('FW2' in tags) \
        or ('FWK' in tags)
    return covered, tags


def run_map(Ms):
    out = {}
    for M in Ms:
        t0 = time.time()
        N, A = 2 * M + 15, M + 15
        dead = dead_from_catalogue(M)
        odd = odd_grid(A)
        odd_dead = [qp for qp in odd if qp in dead]
        odd_alive = [qp for qp in odd if qp not in dead]
        ct = Counter()
        unc = []
        for (q, p) in odd_dead:
            cov, tags = classify(q, p, N)
            for tg in tags:
                ct[tg] += 1
            if not cov:
                unc.append((q, p))
        # region law also for pairs NOT in the dead list: no odd R-pair
        # may be closure-alive
        alive_in_R = [qp for qp in odd_alive if in_region(*qp, N)]
        viol = [qp for qp in odd_alive if s_cert(*qp, N)]
        viol_r = [qp for qp in odd_alive if s1_region(*qp, N) is not None]
        n_cov = len(odd_dead) - len(unc)
        log(f'M={M}: odd-dead {len(odd_dead)}; S {ct["S"]} FG {ct["FG"]} '
            f'FW2 {ct["FW2"]} FWK {ct["FWK"]} (R-pairs {ct["R"]}); S1 {ct["S1"]} COR '
            f'{ct["COR"]}; union {n_cov} '
            f'({100 * n_cov / len(odd_dead):.1f}%), uncovered {len(unc)}; '
            f'SOUNDNESS: S-cert on alive {len(viol)}, S1-region on alive '
            f'{len(viol_r)}, alive pairs inside R {len(alive_in_R)} '
            f'(all MUST be 0) [{time.time() - t0:.0f}s]')
        unc_R = [qp for qp in unc if in_region(*qp, N)]
        log(f'   uncovered inside R (MUST be 0 by the assert): {unc_R}')
        out[M] = dict(odd_dead=len(odd_dead), S=ct['S'], FG=ct['FG'],
                      FW2=ct['FW2'], FWK=ct['FWK'], R=ct['R'], S1=ct['S1'], COR=ct['COR'],
                      union=n_cov, uncovered=unc,
                      soundness=dict(s_alive=viol, s1_alive=viol_r,
                                     alive_in_R=alive_in_R))
    return out


def run_fresh(Ms):
    out = {}
    from e142_fg_closure import close
    import random
    for M in Ms:
        t0 = time.time()
        N, A = 2 * M + 15, M + 15
        odd = odd_grid(A)
        certs = {}
        reg = 0
        nR = nR_cov = nfw2 = 0
        for (q, p) in odd:
            c = s_cert(q, p, N)
            if c:
                check_cert(c)
                certs[(q, p)] = (c['base'], c['t'], c['m'], c['K'])
            t = s1_region(q, p, N)
            if t is not None:
                assert (q, p) in certs, f'region w/o cert {(q, p)}'
                reg += 1
            if in_region(q, p, N):
                nR += 1
                cov = (q, p) in certs or fg_high(q, p, N)
                if not cov:
                    c2 = fw2_cert(q, p, N)
                    if c2:
                        check_fw2(c2)
                    else:
                        ck = fwk_cert(q, p, N)
                        assert ck, f'REGION LAW violated at {(q, p, N)}'
                        check_fwk(ck)
                    nfw2 += 1
                nR_cov += 1
        log(f'FRESH M={M}: odd grid {len(odd)}; S certs built+VERIFIED '
            f'{len(certs)} ({100 * len(certs) / len(odd):.1f}%); '
            f'S1-region {reg}, all with certs; R-pairs {nR}, ALL covered '
            f'({nfw2} via FW2 certs, verified) [{time.time() - t0:.0f}s]')
        random.seed(187 + M)
        sample = random.sample(sorted(certs), min(10, len(certs)))
        bad = []
        for (q, p) in sample:
            cyc, _ = close(M, (4 * M - p, 4 * M - q), verbose=False)
            if not cyc:
                bad.append((q, p))
        log(f'   e142 closure spot-check x{len(sample)}: '
            f'mismatches {bad or "none"} [{time.time() - t0:.0f}s]')
        out[M] = dict(odd=len(odd), s=len(certs), region=reg,
                      closure_bad=bad,
                      certs={f'{k[0]},{k[1]}': v for k, v in certs.items()})
    return out


def run_tower(ms):
    out = {}
    for m in ms:
        for name, N in (('W2e', 2 * m + 7), ('W2o', 2 * m + 8)):
            A = m + 7
            odd = odd_grid(A)
            nc = 0
            reg = 0
            nR = nfw2 = 0
            for (q, p) in odd:
                c = s_cert(q, p, N)
                if c:
                    check_cert(c)
                    nc += 1
                if s1_region(q, p, N) is not None:
                    assert c, f'tower region w/o cert {(q, p, N)}'
                    reg += 1
                if in_region(q, p, N):
                    nR += 1
                    if not c and not fg_high(q, p, N):
                        c2 = fw2_cert(q, p, N)
                        if c2:
                            check_fw2(c2)
                        else:
                            ck = fwk_cert(q, p, N)
                            assert ck, \
                                f'TOWER REGION LAW violated {(q, p, N)}'
                            check_fwk(ck)
                        nfw2 += 1
            log(f'TOWER {name}(m={m}) N={N}: odd {len(odd)}, S certs '
                f'built+VERIFIED {nc} ({100 * nc / len(odd):.0f}%), '
                f'S1-region {reg}; R-pairs {nR} ALL covered '
                f'({nfw2} via FW2)')
            out[f'{name}_{m}'] = dict(odd=len(odd), s=nc, region=reg,
                                      R=nR, fw2=nfw2)
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'map'
    args = [int(a) for a in sys.argv[2:]]
    if mode == 'map':
        res = run_map(args or [48, 64, 80, 96, 112, 128, 144, 160])
        path = os.path.join(DATA, 'e187_oddkill_map.json')
    elif mode == 'fresh':
        res = run_fresh(args or [208, 240])
        path = os.path.join(DATA, 'e187_oddkill_fresh.json')
    elif mode == 'tower':
        res = run_tower(args or [24, 32, 40, 48, 56, 64, 104, 120])
        path = os.path.join(DATA, 'e187_oddkill_tower.json')
    else:
        raise SystemExit(f'unknown mode {mode}')
    with open(path, 'w') as f:
        json.dump({str(k): v for k, v in res.items()}, f)
    with open(os.path.join(DATA, 'e187_oddkill.log'), 'a') as f:
        f.write('\n'.join(LOG) + '\n')
    log('e187: DONE')


if __name__ == '__main__':
    main()
