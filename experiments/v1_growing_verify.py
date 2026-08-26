"""Erdős #197 — TASK V: adversarial re-verification of the G3 death certificates.

G3 (notes/38, data/g3_summary.json) reported all 8 growing-sliver-swap
candidates DEAD by the portable-crown signature, governed by the d_t law
(d_t = 2 s_t - s_{t+1}).  This script re-verifies everything with FRESH code:
no imports from g3 except for one cross-validation of the membership arrays.

CHECK 0  independent membership oracle (pure-int, any scale) vs g3.build_labels
         at N = 2^16, all 8 candidates, exact array equality + random spot.
CHECK 1  d_t law re-derivation, exact iff, octaves t in [8, 40], x in 1..8:
         for the NAT variants the two sliver-mediated channels are exhaustive
         (y in octave t, fixed x < 2^{t-1}; completions land in octave t+1),
         so we assert attack-exists(x, t)  <=>  the d_t prediction:
           receiver sliver-top:  x <= d_t - 1   (team = owner(t+1))
           owner kept-bottom:    x >= d_t + 2   (team = owner(t))
         both positive and negative directions, membership via the oracle.
CHECK 2  crown recurrences at HIGH octaves (exact ints, t up to 60): the
         claimed fixed attackers hit every octave of their claimed class
         (lin A x=2 odd, lin B x=1 even, geo B x=1 even + x=3/4 odd,
          nearfull A x=2 odd, B x=1 even, genstage per computed plateau/jump
          lists, geo_alt A crown-plant family (2, 2^j-1, 2^{j+1}-4) odd j);
         plus the notes' concrete example triples.
CHECK 3  brute-force channel-agnostic attack scan at N = 2^16 (numpy):
         for every in-team x <= 64 the exact attacked-octave sets, asserted
         EQUAL to the d_t predictions on nat variants (t in [8,14]) and
         superset-with-plants on alt; geo_nat/A cleanliness: NO in-team
         x <= 64 attacks any octave t >= 12.
CHECK 4  ray re-walks: the stored RAY-GROW witness chains (lin_nat/B,
         geo_nat/B) re-verified step by step with the oracle (u' = 2u - f,
         u, u', f in-team, f <= 4 s_t + 64), then DFS-extended to octave 80
         with the same growing cap — the censoring claim is not a horizon
         artifact of the g3 FFT scan.
CHECK 5  independent SAT sanity at 2^12: bit-reversal (ABJ) order built from
         scratch, full-order monotone-3-AP-freeness verified exhaustively,
         then team-restricted checks for geo_nat/A and lin_nat/B.

Usage: .venv/bin/python experiments/v1_growing_verify.py
Artifacts: data/v1_verify.json (machine record; every assert also raises).
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

REC = {'checks': {}, 'failures': []}
T0 = time.time()


def log(msg):
    print(f'[{time.time() - T0:7.1f}s] {msg}', flush=True)


# ---------------------------------------------------------------- schedules
# Re-typed from notes/38 (NOT imported from g3).

def genstage_s(t):
    M_prev, k = 1, 0
    while True:
        k += 1
        M_k = 8 * M_prev * 4 ** k
        if (1 << t) <= M_k:
            return M_prev
        M_prev = M_k


SCHEDULES = {
    'lin': lambda t: t,
    'geo': lambda t: 1 << (t // 2),
    'nearfull': lambda t: (1 << t) // t,
    'genstage': genstage_s,
}
CANDS = [(s, v) for s in ('lin', 'geo', 'nearfull', 'genstage')
         for v in ('nat', 'alt')]
A, B = 1, 2


def octave(v):
    """t with 2^{t-1} < v <= 2^t (v >= 2)."""
    t = v.bit_length()
    return t - 1 if v & (v - 1) == 0 else t


def st_trunc(sched, t):
    """Donated depth actually used in block t (truncated to block size)."""
    return min(SCHEDULES[sched](t), 1 << (t - 1))


def owner(t):
    return A if t % 2 == 0 else B


def make_member(sched, variant):
    """team(v) in {1=A, 2=B}; pure ints, valid at any scale."""
    fn = SCHEDULES[sched]

    def base(v):
        if v == 1:
            return B
        t = octave(v)
        lo = 1 << (t - 1)
        st = min(fn(t), lo)
        o = owner(t)
        return (3 - o) if (v - lo) <= st else o

    if variant == 'nat':
        return base

    def member(v):
        if v >= 3 and (v + 1) & v == 0:          # v = 2^j - 1, j >= 2
            return 3 - base(v + 1)               # flipped opposite team(2^j)
        return base(v)
    return member


def d_tilde(sched, t):
    return 2 * st_trunc(sched, t) - st_trunc(sched, t + 1)


# ------------------------------------------------------------------ CHECK 0
def check0():
    import g3_growing_sliver as g3
    N = 1 << 16
    ok = True
    for sched, var in CANDS:
        lab = g3.build_labels(g3.SCHEDULES[sched][1], var, N)
        member = make_member(sched, var)
        mine = np.zeros(N + 1, dtype=np.uint8)
        for v in range(1, N + 1):
            mine[v] = member(v)
        same = bool((mine[1:] == lab[1:]).all())
        ok &= same
        if not same:
            bad = np.nonzero(mine[1:] != lab[1:])[0][:10] + 1
            REC['failures'].append(f'CHECK0 {sched}_{var} mismatch at {bad}')
        log(f'CHECK0 {sched}_{var}: oracle == g3.build_labels on [1,2^16]: {same}')
    REC['checks']['0_oracle_vs_g3'] = ok
    assert ok, 'membership oracle disagrees with g3 generator'


# ------------------------------------------------- channel attack primitives
def recv_attack(member, team, sched, x, t, tries=64):
    """Sliver-top channel: y = 2^{t-1}+o, o <= s_t, z = 2^t + (2o - x).
    Complete o-range for an in-octave-(t+1)-kept landing is
    [ceil((s_{t+1}+1+x)/2), s_t]; we probe from the top (largest landings).
    Returns a verified triple or None."""
    lo = 1 << (t - 1)
    st = st_trunc(sched, t)
    o_lo = (st_trunc(sched, t + 1) + 1 + x + 1) // 2
    if member(x) != team or x >= lo:
        return None
    o = st
    while o >= max(1, o_lo) and tries > 0:
        y, z = lo + o, 2 * (lo + o) - x
        if member(y) == team and member(z) == team and x < y:
            return (x, y, z)
        o -= 1
        tries -= 1
    return None


def kept_attack(member, team, sched, x, t, tries=64):
    """Kept-bottom channel: y = 2^{t-1}+o, o > s_t, z = 2^t + (2o - x) with
    landing in [1, s_{t+1}].  Complete o-range is
    [max(s_t+1, ceil((x+1)/2)), (s_{t+1}+x)//2]; probe from the bottom."""
    lo = 1 << (t - 1)
    st = st_trunc(sched, t)
    o_hi = (st_trunc(sched, t + 1) + x) // 2
    if member(x) != team or x >= lo:
        return None
    o = max(st + 1, (x + 1 + 1) // 2)
    while o <= min(o_hi, lo) and tries > 0:
        y, z = lo + o, 2 * (lo + o) - x
        if member(y) == team and member(z) == team and x < y:
            return (x, y, z)
        o += 1
        tries -= 1
    return None


def verify_triple(member, team, trip):
    x, y, z = trip
    return (z - y == y - x > 0 and member(x) == team and member(y) == team
            and member(z) == team)


# ------------------------------------------------------------------ CHECK 1
def check1():
    """d_t law, exact iff, nat variants, t in [8,40], x in 1..8."""
    ok = True
    for sched in SCHEDULES:
        member = make_member(sched, 'nat')
        n_pos = n_neg = 0
        for t in range(8, 41):
            d = d_tilde(sched, t)
            recv_team, own_team = owner(t + 1), owner(t)
            for x in range(1, 9):
                # receiver sliver-top channel
                if member(x) == recv_team:
                    got = recv_attack(member, recv_team, sched, x, t) is not None
                    want = x <= d - 1
                    if got != want:
                        ok = False
                        REC['failures'].append(
                            f'CHECK1 {sched} recv t={t} x={x}: got={got} want={want}')
                    n_pos += want
                    n_neg += not want
                # owner kept-bottom channel
                if member(x) == own_team:
                    got = kept_attack(member, own_team, sched, x, t) is not None
                    want = x >= d + 2
                    if got != want:
                        ok = False
                        REC['failures'].append(
                            f'CHECK1 {sched} kept t={t} x={x}: got={got} want={want}')
                    n_pos += want
                    n_neg += not want
        log(f'CHECK1 {sched}: d_t law iff on t in [8,40], x<=8: '
            f'{n_pos} predicted attacks + {n_neg} predicted blanks all match: {ok}')
    REC['checks']['1_dt_law_iff'] = ok
    assert ok, 'd_t law violated'


# ------------------------------------------------------------------ CHECK 2
def check2():
    """Crown recurrences at high octaves + concrete example triples."""
    ok = True
    results = {}

    def claim(name, member, team, sched, chan, xs, octs):
        nonlocal ok
        found = None
        for x in xs:
            trips = []
            for t in octs:
                f = (recv_attack if chan == 'recv' else kept_attack)(
                    member, team, sched, x, t, tries=512)
                if f is None:
                    trips = None
                    break
                trips.append(f)
            if trips is not None:
                found = (x, trips)
                break
        if found is None:
            ok = False
            REC['failures'].append(f'CHECK2 {name}: no fixed x in {xs} covers all octaves')
            log(f'CHECK2 {name}: FAIL')
        else:
            x, trips = found
            results[name] = {'x': x, 'octaves': [int(o) for o in octs],
                             'sample': [list(map(int, trips[0])), list(map(int, trips[-1]))]}
            log(f'CHECK2 {name}: x={x} attacks all {len(octs)} claimed octaves '
                f'(t={octs[0]}..{octs[-1]}), e.g. {trips[0]} .. {trips[-1]}')

    odd = list(range(9, 60, 2))
    even = list(range(8, 61, 2))
    for var in ('nat', 'alt'):
        lin = make_member('lin', var)
        claim(f'lin_{var}/A recv@odd', lin, A, 'lin', 'recv', [2, 6], odd)
        claim(f'lin_{var}/B recv@even', lin, B, 'lin', 'recv', [1, 3], even)
        geo = make_member('geo', var)
        claim(f'geo_{var}/B recv@even', geo, B, 'geo', 'recv', [1], even)
        claim(f'geo_{var}/B kept@odd', geo, B, 'geo', 'kept', [3, 4], odd)
        nf = make_member('nearfull', var)
        claim(f'nearfull_{var}/A recv@odd', nf, A, 'nearfull', 'recv', [2, 6], odd)
        claim(f'nearfull_{var}/B recv@even', nf, B, 'nearfull', 'recv', [1, 3], even)
        gm = make_member('genstage', var)
        # plateau/jump lists computed from the truncated d_t itself
        a_recv = [t for t in odd if d_tilde('genstage', t) >= 3]
        b_recv = [t for t in even if d_tilde('genstage', t) >= 2]
        a_jump = [t for t in range(8, 61) if owner(t) == A and d_tilde('genstage', t) < 0]
        b_jump = [t for t in range(8, 61) if owner(t) == B and d_tilde('genstage', t) < 0]
        claim(f'genstage_{var}/A recv@odd-plateau', gm, A, 'genstage', 'recv', [2, 6], a_recv)
        claim(f'genstage_{var}/B recv@even-plateau', gm, B, 'genstage', 'recv', [1, 3], b_recv)
        claim(f'genstage_{var}/A kept@jumps{a_jump}', gm, A, 'genstage', 'kept', [2, 6], a_jump)
        claim(f'genstage_{var}/B kept@jumps{b_jump}', gm, B, 'genstage', 'kept', [1, 3], b_jump)

    # geo_alt/A crown-plant family (2, 2^j - 1, 2^{j+1} - 4), odd j
    geo_alt = make_member('geo', 'alt')
    for j in range(9, 60, 2):
        trip = (2, (1 << j) - 1, (1 << (j + 1)) - 4)
        if not verify_triple(geo_alt, A, trip):
            ok = False
            REC['failures'].append(f'CHECK2 geo_alt/A plant j={j} fails')
    log(f'CHECK2 geo_alt/A crown-plant family (2, 2^j-1, 2^(j+1)-4) verified at odd j in [9,59]')

    # concrete triples from notes/38 + S1 report
    concrete = [
        ('lin', 'nat', B, (1, 12, 23)), ('lin', 'nat', B, (1, 37, 73)),
        ('geo', 'alt', A, (2, 31, 60)), ('geo', 'alt', A, (2, 127, 252)),
        ('geo', 'alt', A, (2, 511, 1020)), ('geo', 'alt', A, (3, 17, 31)),
        ('geo', 'alt', A, (5, 66, 127)),
    ]
    for sched, var, team, trip in concrete:
        good = verify_triple(make_member(sched, var), team, trip)
        ok &= good
        if not good:
            REC['failures'].append(f'CHECK2 concrete {sched}_{var} {trip} fails')
    log(f'CHECK2 concrete example triples from notes/38: all verified: {ok}')
    REC['checks']['2_crown_recurrences'] = ok
    REC['checks']['2_details'] = results
    assert ok, 'crown recurrence verification failed'


# ------------------------------------------------------------------ CHECK 3
def check3():
    """Brute-force attack scan at 2^16; equality with d_t predictions (nat);
    geo_nat/A cleanliness; alt plants as the only extras."""
    N = 1 << 16
    ok = True
    for sched, var in CANDS:
        member = make_member(sched, var)
        lab = np.zeros(N + 1, dtype=np.uint8)
        for v in range(1, N + 1):
            lab[v] = member(v)
        oct_vals = {t: np.arange((1 << (t - 1)) + 1, (1 << t) + 1)
                    for t in range(5, 16)}
        for team in (A, B):
            team_oct = {t: vals[lab[vals] == team] for t, vals in oct_vals.items()}
            attacked = {}
            for x in range(1, 65):
                if lab[x] != team:
                    continue
                ts = []
                for t in range(8, 15):
                    if x >= (1 << (t - 1)):
                        continue
                    ys = team_oct[t]
                    zs = 2 * ys - x
                    zs = zs[zs <= N]
                    if np.any(lab[zs] == team):
                        ts.append(t)
                attacked[x] = ts
            # d_t predictions
            pred = {}
            for x in attacked:
                p = []
                for t in range(8, 15):
                    d = d_tilde(sched, t)
                    if owner(t + 1) == team and x <= d - 1:
                        p.append(t)
                    elif owner(t) == team and x >= d + 2:
                        p.append(t)
                pred[x] = p
            extras = {x: sorted(set(attacked[x]) - set(pred[x])) for x in attacked}
            missing = {x: sorted(set(pred[x]) - set(attacked[x])) for x in attacked}
            n_extra = sum(len(v) for v in extras.values())
            n_missing = sum(len(v) for v in missing.values())
            tname = 'A' if team == A else 'B'
            if n_missing:
                ok = False
                REC['failures'].append(
                    f'CHECK3 {sched}_{var}/{tname}: predicted attacks missing: '
                    f'{ {x: v for x, v in missing.items() if v} }')
            if var == 'nat' and n_extra:
                ok = False
                REC['failures'].append(
                    f'CHECK3 {sched}_{var}/{tname}: unpredicted attacks (nat!): '
                    f'{ {x: v for x, v in extras.items() if v} }')
            note = ''
            if var == 'alt' and n_extra:
                note = f' (+{n_extra} alt-plant extras, expected)'
            log(f'CHECK3 {sched}_{var}/{tname}: brute-force attacked octaves == '
                f'd_t prediction for all in-team x<=64, t in [8,14]: '
                f'{n_missing == 0 and (var == "alt" or n_extra == 0)}{note}')
            if sched == 'geo' and var == 'nat' and team == A:
                worst = max((max(ts) for ts in attacked.values() if ts), default=0)
                clean = all(t < 12 for ts in attacked.values() for t in ts)
                log(f'CHECK3 geo_nat/A cleanliness: no in-team x<=64 attacks any '
                    f'octave >= 12 (max attacked octave = {worst}): {clean}')
                ok &= clean
                if not clean:
                    REC['failures'].append('CHECK3 geo_nat/A not clean')
    REC['checks']['3_bruteforce_2e16'] = ok
    assert ok, 'brute-force scan contradicts predictions'


# ------------------------------------------------------------------ CHECK 4
def cap_of(sched, t):
    return 4 * st_trunc(sched, t) + 64


def bteam_runs(sched, f_lo, f_hi):
    """Maximal intervals of team-B values within [f_lo, f_hi] (nat variant),
    read off the block structure instead of scanning value by value: odd
    blocks keep (2^{t-1}+s_t, 2^t], even blocks donate (2^{t-1},
    2^{t-1}+s_t] to B.  (The original linear scan here dead-ended whenever
    the nearest in-team reflector lay past a full donated sliver — runs of
    ~s_t/2 > 4096 out-of-team values at octave >= 47 — which is what made
    the first CHECK4 geo/B DFS fail on search budget.)"""
    runs = []
    f_lo = max(1, f_lo)
    if f_hi < f_lo:
        return runs
    if f_lo == 1:
        runs.append((1, 1))                   # 1 -> B by convention
    t = max(1, octave(max(2, f_lo)))
    while (1 << (t - 1)) < f_hi:
        lo = 1 << (t - 1)
        st = st_trunc(sched, t)
        if t % 2 == 1:
            a, b = lo + st + 1, 1 << t        # B kept body
        else:
            a, b = lo + 1, lo + st            # B received sliver
        a2, b2 = max(a, f_lo), min(b, f_hi)
        if a2 <= b2:
            runs.append((a2, b2))
        t += 1
    return runs


def ray_candidates(member, sched, u, cap, branch=24, per_run=8):
    """In-team reflectors f <= cap with 2u - f in-team, small-f first,
    enumerated over the analytic team-B runs (no scan budget)."""
    t = octave(u)
    r = u - (1 << (t - 1))
    tp = t + 1
    stp = st_trunc(sched, tp)
    if owner(tp) == B:
        w_lo, w_hi = stp + 1, 1 << t          # B kept
    else:
        w_lo, w_hi = 1, stp                   # B holds A's donated sliver
    w_hi = min(w_hi, 2 * r - 1)
    w_lo = max(w_lo, 2 * r - cap)
    if w_hi < w_lo:
        return []
    out = []
    for a, b in bteam_runs(sched, 2 * r - w_hi, 2 * r - w_lo):
        for f in range(a, min(b, a + per_run - 1) + 1):
            if not (1 <= f <= cap) or member(f) != B:
                continue
            u2 = 2 * u - f
            if member(u2) == B:
                out.append((f, u2))
                if len(out) >= branch:
                    return out
    return out


def check4():
    """Re-walk stored ray witnesses; DFS-extend to octave 80."""
    ok = True
    stored = {
        ('lin', 'B'): ([8, 12, 23, 38, 72, 135, 266, 522, 1040, 2058, 4112,
                        8201, 16401, 32779, 65554, 131073],
                       [4, 1, 8, 4, 9, 4, 10, 4, 22, 4, 23, 1, 23, 4, 35]),
        ('geo', 'B'): ([4, 7, 10, 12, 23, 37, 73, 138, 275, 529, 1057, 2083,
                        4165, 8257, 16513, 32897, 65793, 131073],
                       [1, 4, 8, 1, 9, 1, 8, 1, 21, 1, 31, 1, 73, 1, 129, 1, 513]),
    }
    for (sched, _), (chain, refl) in stored.items():
        member = make_member(sched, 'nat')
        good = len(refl) == len(chain) - 1
        for i, f in enumerate(refl):
            u, u2 = chain[i], chain[i + 1]
            t = octave(u)
            good &= (u2 == 2 * u - f and member(u) == B and member(f) == B
                     and member(u2) == B and f <= cap_of(sched, t))
        ok &= good
        log(f'CHECK4 {sched}_nat/B stored ray witness ({len(chain)} nodes, '
            f'max reflector {max(refl)}): every step re-verified: {good}')
        # DFS extension: start from the latest stored node that continues.
        # (g3's FFT scan tracks full octave SETS; an individual witness node —
        #  e.g. an offset-1 element — need not continue, so we try each stored
        #  node, latest first.)
        ext, start_u = None, None
        for start in reversed(chain):
            # iterative DFS, small-reflector-first, limited branching
            stack = [(start, iter(ray_candidates(member, sched, start,
                                                 cap_of(sched, octave(start)))))]
            path = []
            nodes = 0
            while stack and nodes < 30000 and ext is None:
                u, it = stack[-1]
                if octave(u) >= 80:
                    ext, start_u = list(path), start
                    break
                step = next(it, None)
                if step is None:
                    stack.pop()
                    if path:
                        path.pop()
                    continue
                nodes += 1
                f, u2 = step
                path.append((f, u2))
                stack.append((u2, iter(ray_candidates(member, sched, u2,
                                                      cap_of(sched, octave(u2))))))
            if ext is not None:
                break
        if ext is None:
            ok = False
            REC['failures'].append(f'CHECK4 {sched}/B: DFS extension to octave 80 failed')
            log(f'CHECK4 {sched}_nat/B: DFS extension FAILED')
        else:
            u_end = ext[-1][1]
            fs = [f for f, _ in ext]
            # re-verify extension
            u = start_u
            g2 = True
            for f, u2 in ext:
                g2 &= (u2 == 2 * u - f and member(f) == B and member(u2) == B
                       and f <= cap_of(sched, octave(u)))
                u = u2
            ok &= g2
            log(f'CHECK4 {sched}_nat/B: ray DFS-extended from stored node '
                f'{start_u} (octave {octave(start_u)}) {len(ext)} steps to '
                f'octave {octave(u_end)} (u ~ 2^{u_end.bit_length()}, max new '
                f'reflector {max(fs)}), all steps verified: {g2} — '
                f'censoring at 2^18 was not a horizon artifact')
            REC['checks'].setdefault('4_extensions', {})[f'{sched}_nat_B'] = {
                'from': int(start_u), 'steps': len(ext),
                'end_octave': octave(u_end), 'max_reflector': int(max(fs))}
    REC['checks']['4_ray_rewalk'] = ok
    assert ok, 'ray witness verification failed'


# ------------------------------------------------------------------ CHECK 5
def check5():
    """Independent bit-reversal order, full + team-restricted AP-freeness at 2^12."""
    N = 1 << 12
    W = 13
    keys = np.zeros(N + 1, dtype=np.int64)
    for v in range(1, N + 1):
        keys[v] = int(format(v, f'0{W}b')[::-1], 2)
    order = np.argsort(keys[1:], kind='stable') + 1
    pos = np.zeros(N + 1, dtype=np.int64)
    pos[order] = np.arange(N)
    def count_monotone(mask):
        cnt = 0
        for d in range(1, N // 2 + 1):
            a = np.arange(1, N - 2 * d + 1)
            sel = mask[a] & mask[a + d] & mask[a + 2 * d]
            if not sel.any():
                continue
            aa = a[sel]
            up = (pos[aa] < pos[aa + d]) & (pos[aa + d] < pos[aa + 2 * d])
            dn = (pos[aa] > pos[aa + d]) & (pos[aa + d] > pos[aa + 2 * d])
            cnt += int(up.sum() + dn.sum())
        return cnt
    full = count_monotone(np.ones(N + 1, dtype=bool))
    log(f'CHECK5 bit-reversal order on [1,4096]: monotone 3-APs = {full}')
    ok = full == 0
    for sched, team, tname in (('geo', A, 'geo_nat/A'), ('lin', B, 'lin_nat/B')):
        member = make_member(sched, 'nat')
        mask = np.zeros(N + 1, dtype=bool)
        for v in range(1, N + 1):
            mask[v] = member(v) == team
        c = count_monotone(mask)
        ok &= c == 0
        log(f'CHECK5 {tname} restricted to bit-reversal order at 2^12: '
            f'monotone 3-APs = {c} (SAT confirmed independently)')
    REC['checks']['5_sat_sanity'] = ok
    assert ok, 'independent SAT sanity failed'


def main():
    check0()
    check1()
    check2()
    check3()
    check4()
    check5()
    REC['all_ok'] = not REC['failures']
    out = os.path.join(REPO, 'data', 'v1_verify.json')
    with open(out, 'w') as fh:
        json.dump(REC, fh, indent=1, default=str)
    log(f'ALL CHECKS PASS: {REC["all_ok"]} -> {out}')


if __name__ == '__main__':
    main()
