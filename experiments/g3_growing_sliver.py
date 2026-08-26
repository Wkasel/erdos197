"""Erdős #197 — G3: growing-sliver swap partitions (TASK S1 build + screen).

THE LAST SURVIVING SHAPE after H1-H3 (STATUS.md 'General case', notes/34-37):
ratio-2 blocks (2^{t-1}, 2^t] alternate teams (A gets even t, B odd t; 1 -> B)
and each team donates the bottom s_t values of each of its own blocks to the
partner, with the donated depth s_t GROWING.  Growth defeats the two proven
death mechanisms of the fixed-depth family (notes/35):
  - fixed-attacker crowns: an in-block sliver-mediated attack by fixed x on
    the kept bottom needs x >= d_t + 2 where d_t := 2 s_t - s_{t+1}, so
    d_t -> infinity starves every fixed attacker of kept-bottom attacks;
  - lem:orbit: the period-2 orbit reflectors f = 2 o1 - o2 ~ d_t outgrow
    every finite reflector set, voiding the lemma's hypothesis.
UNTESTED death routes screened here: slowly-growing reflector sets (ratio-2
rays staying within O(s_t) of the team) and scale-adapted attacker families.

Schedules s_t:  lin s_t = t;  geo s_t = 2^{floor(t/2)};
                nearfull s_t = floor(2^t / t);
                genstage s_t = M_{k-1} matched to Geneson's stage widths
                (M_0 = 1, M_k = 8 M_{k-1} 4^k: s = 1, 32, 4096 on octaves
                 1-5, 6-12, 13-21).
Crown variants: nat  = crown pairs {2^j - 1, 2^j} land per the partition
                       (both at the top of block j -> whole pair to the
                       block owner, pair ownership alternating with j);
                alt  = forced-alternating/split crowns: 2^j - 1 is moved to
                       the partner of team(2^j), so NO team ever owns a
                       full crown pair (trichotomy escape (1), notes/36).

Screens per team at horizons 2^12, 2^15, 2^18:
  (i)   pure-complete SAT: ABJ bit-reversal witness + independent
        no-monotone-3-AP verification (full to 2^15, sampled d at 2^18,
        the ABJ order applies to every subset of Z) + Cadical195
        cross-check at 2^12 (lazy transitivity, ABJ phase hint).
  (ii)  ORBIT (finite reflectors, lem:orbit proper): g2 orbit scan at
        fmax = 64, plus the RAY scan below with the same fixed cap.
  (iii) RAY-GROW (new instrument, this file): exact octave-reachability of
        ratio-2 rays u -> 2u - f with in-team reflectors f <= cap(t) =
        4 s_t + 64 (i.e. reflectors allowed to grow WITH the schedule —
        exactly the regime lem:orbit does not cover).  Per start octave t0
        the full in-team octave is seeded and pushed upward by exact
        boolean sumsets (FFT convolution); a censored ray spanning >= 6
        octaves at the top horizon is the growing-reflector analogue of an
        orbit death — a SIGNAL (no theorem for growing F yet), not a
        certificate.  Witness chains are reconstructed and re-verified.
  (iv)  CROWN scans: g2 recurrence scan (fixed x <= 64, occupied-octave
        ratio) + H2 persistence scan (parity-robust; run at top_gap 1 and
        2 — donation pushes completions one octave up, so the last
        attackable y-octave for a receiving surface is top - 2) +
        ADAPTIVE surface scan (new): per octave, the exact attacker sets
        that reach the kept bottom (y in the first 8 kept values) and the
        received-sliver top (y in the last 8 donated values), with the
        d_t-law prediction: kept-bottom attackers are x >= d_t + 2,
        received-sliver attackers are x <= d_t - 1.  Flags ADAPT if a
        surface is attackable at >= 80% of large octaves (bounded-
        description scale-adapted family).
  (v)   SLIVER load (g2, width 8; structurally blind here — received
        slivers fall below the occupancy threshold at large t — kept for
        continuity).

The d_t law (proved in notes/38 from the two surface inequalities): on each
octave-parity class, the block OWNER escapes fixed kept-bottom attackers
iff d_t -> infinity on that class, while the RECEIVER escapes fixed
sliver-top attackers iff d_t stays <= its smallest attacker on that class.
Both cannot hold on the same class, so EVERY schedule hands at least one
team a scale-persistent fixed attacker (portable-crown death pattern).
This screen is the machine check of that law on 8 concrete candidates.

Usage: .venv/bin/python experiments/g3_growing_sliver.py [--quick]
Artifacts: data/g3_<sched>_<variant>.json + data/g3_summary.json.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import g2_diagnose as g2            # noqa: E402  (calibrated kit)
import h2_sliver_swap as h2         # noqa: E402  (persistence scan)

NMAX = 1 << 18
HORIZONS = [1 << 12, 1 << 15, 1 << 18]
CDCL_H = 1 << 12                    # CDCL cross-check horizon
WIT_FULL_H = 1 << 15                # full witness verification up to here
ATTACKER_MAX = 64
ORBIT_FMAX = 64                     # finite-F instrument (lem:orbit proper)
RAY_SPAN_FLAG = 6
ADAPT_WINDOW = 8                    # y-window width for the adaptive scan


# ------------------------------------------------------------- schedules

def _genstage_s(t):
    """Geneson stage width M_{k-1} at scale 2^t (M_0=1, M_k = 8 M_{k-1} 4^k):
    s_t = M_{k-1} for the stage k with M_{k-1} < 2^t <= M_k."""
    M_prev, k = 1, 0
    while True:
        k += 1
        M_k = 8 * M_prev * 4 ** k
        if (1 << t) <= M_k:
            return M_prev
        M_prev = M_k


SCHEDULES = {
    'lin': ('s_t = t', lambda t: t),
    'geo': ('s_t = 2^{floor(t/2)}', lambda t: 1 << (t // 2)),
    'nearfull': ('s_t = floor(2^t/t)', lambda t: (1 << t) // t),
    'genstage': ('s_t = M_{k-1} (Geneson stages)', _genstage_s),
}
VARIANTS = {
    'nat': 'natural crown ownership (pair rides with its block)',
    'alt': 'forced-alternating crowns: 2^j-1 moved opposite team(2^j)',
}


# ------------------------------------------------------------- generator

def build_labels(sched_fn, variant, N):
    """Label array over [0, N]: 1 = team A, 2 = team B (0 = unused index 0).
    Blocks (2^{t-1}, 2^t]: even t owned by A, odd by B; owner donates the
    bottom min(s_t, |block|) values to the partner; 1 -> B."""
    lab = np.zeros(N + 1, dtype=np.uint8)
    lab[1] = 2
    t = 1
    while (1 << (t - 1)) < N:
        lo, hi = 1 << (t - 1), min(1 << t, N)
        st = min(sched_fn(t), hi - lo)
        owner = 1 if t % 2 == 0 else 2
        lab[lo + 1: lo + st + 1] = 3 - owner
        lab[lo + st + 1: hi + 1] = owner
        t += 1
    if variant == 'alt':
        j = 2
        while (1 << j) <= N:
            p = 1 << j
            lab[p - 1] = 3 - lab[p]
            j += 1
    assert int((lab[1:] == 0).sum()) == 0, 'labeling not total'
    return lab


def teams_from_labels(lab):
    A = np.nonzero(lab == 1)[0].astype(np.int64)
    B = np.nonzero(lab == 2)[0].astype(np.int64)
    return A, B


def verify_partition(lab, A, B, N, horizons):
    """Disjoint + covering, at N and at every screening horizon."""
    assert len(A) + len(B) == N
    assert not np.intersect1d(A, B).size
    merged = np.union1d(A, B)
    assert merged[0] == 1 and merged[-1] == N and len(merged) == N
    for H in horizons:
        a, b = int(np.searchsorted(A, H + 1)), int(np.searchsorted(B, H + 1))
        assert a + b == H, f'not a partition of [1,{H}]'
    return True


# ------------------------------------------------- exact ray scan (new)

def _conv_counts(a, b):
    """Integer counts of the sumset convolution of two 0/1 arrays."""
    n = len(a) + len(b) - 1
    if len(a) * len(b) <= (1 << 18):
        return np.convolve(a.astype(np.float64), b.astype(np.float64))
    size = 1 << (n - 1).bit_length()
    fa = np.fft.rfft(a.astype(np.float64), size)
    fb = np.fft.rfft(b.astype(np.float64), size)
    return np.fft.irfft(fa * fb, size)[:n]


def ray_scan(S, N, cap_fn, cap_desc, span_flag=RAY_SPAN_FLAG,
             keep_arrays_for=None):
    """Exact reachability of increasing ratio-2 rays u -> 2u - f with
    in-team reflectors 1 <= f <= cap_fn(t) (t = octave of u).  For each
    start octave t0 the whole in-team octave is seeded; propagation is by
    exact boolean sumset {2u - f} (FFT convolution, counts thresholded),
    with up to 4 within-octave closure rounds before stepping up.  Returns
    per-start spans; flag iff the best ray is censored (alive at the top
    octave, where every successor exceeds N) and spans >= span_flag
    octaves.  If keep_arrays_for = t0, per-octave reach sets are kept so a
    witness chain can be reconstructed."""
    S = np.asarray(S, dtype=np.int64)
    member = np.zeros(N + 1, dtype=bool)
    member[S] = True
    T = g2.octave(N)

    farrs, caps = {}, {}
    for t in range(1, T + 1):
        lo = 1 << (t - 1)
        capF = max(1, min(int(cap_fn(t)), lo))
        caps[t] = capF
        fa = np.zeros(capF, dtype=bool)          # index m <-> f = capF - m
        fs = np.nonzero(member[1: capF + 1])[0] + 1
        fa[capF - fs] = True
        farrs[t] = fa

    def propagate(t0, keep=False):
        """Push the full in-team octave t0 upward; return (last octave with
        a nonempty reach set, kept per-octave reach arrays if keep)."""
        arrays = {}
        lo, hi = 1 << (t0 - 1), 1 << t0
        R = member[lo + 1: hi + 1].copy()        # index i <-> value lo+1+i
        t, last = t0, None
        while t <= T and R.any():
            last = t
            lo, hi = 1 << (t - 1), 1 << t
            capF, fa = caps[t], farrs[t]
            nxt = np.zeros(hi, dtype=bool)       # index i <-> value hi+1+i
            if fa.any():
                for _ in range(4):               # within-octave closure
                    dbl = np.zeros(2 * (hi - lo), dtype=bool)
                    dbl[::2] = R                 # index 2i <-> value 2u
                    cnt = _conv_counts(dbl, fa)  # index j <-> value base+j
                    base = 2 * lo + 2 - capF     # = hi + 2 - capF > lo + 1
                    succ = cnt > 0.5             # values [base, 2*hi - 1]
                    # next-octave part: values (hi, 2*hi - 1]
                    a = hi + 1 - base
                    b = min(len(succ), 2 * hi - base)
                    if b > a:
                        nxt[: b - a] |= succ[a: b]
                    # same-octave part: values [base, hi] (all > lo + 1)
                    m = hi - base + 1            # count of such values
                    if m <= 0:
                        break
                    same = succ[:m] & member[base: hi + 1]
                    off = base - (lo + 1)
                    new = same & ~R[off: off + m]
                    if not new.any():
                        break
                    R[off: off + m] |= new
            if keep:
                arrays[t] = R.copy()
            if t == T:
                break
            R = nxt & member[hi + 1: 2 * hi + 1]
            t += 1
        return last, arrays

    rows = []
    for t0 in range(1, T + 1):
        lo, hi = 1 << (t0 - 1), 1 << t0
        if not member[lo + 1: hi + 1].any():
            continue
        last, _ = propagate(t0)
        rows.append({'t0': t0, 't_last': last, 'span': last - t0,
                     'censored': last == T})
    best = max(rows, key=lambda r: (r['span'], r['censored'])) if rows \
        else {'span': 0, 'censored': False, 't0': 0, 't_last': 0}
    flag = bool(best['censored'] and best['span'] >= span_flag)

    witness = None
    if flag or keep_arrays_for is not None:
        t0 = keep_arrays_for if keep_arrays_for is not None else best['t0']
        _, arrays = propagate(t0, keep=True)
        witness = _reconstruct(arrays, member, caps, t0)
    return {'cap': cap_desc, 'caps_per_octave': {t: caps[t] for t in caps},
            'per_start': rows, 'best': best, 'flag': flag,
            'witness': witness,
            'flag_reason': (
                f"censored ray of span {best['span']} octaves (start octave "
                f"{best['t0']}) alive at horizon with reflectors <= cap — "
                f"growing-reflector orbit analogue" if flag else
                f"no censored ray of span >= {span_flag} "
                f"(best span {best['span']})")}


def _reconstruct(arrays, member, caps, t0):
    """Greedy backward chain from the highest nonempty reach set; verify."""
    if not arrays:
        return None
    t_last = max(arrays)
    lo = 1 << (t_last - 1)
    idx = np.nonzero(arrays[t_last])[0]
    if not idx.size:
        return None
    v = int(lo + 1 + idx[0])
    chain, refl = [v], []
    for _ in range(400):
        tv = g2.octave(v)
        found = None
        for tu in (tv - 1, tv):
            if tu not in arrays:
                continue
            capF = caps[tu]
            ulo, uhi = 1 << (tu - 1), 1 << tu
            lo_u = max(ulo + 1, (v + 2) // 2)
            hi_u = min(uhi, (v + capF) // 2, v - 1)
            if hi_u < lo_u:
                continue
            seg = arrays[tu][lo_u - ulo - 1: hi_u - ulo]
            cand = np.nonzero(seg)[0]
            for c in cand:
                u = int(lo_u + c)
                f = 2 * u - v
                if 1 <= f <= capF and member[f]:
                    found = (u, f)
                    break
            if found:
                break
        if not found:
            break
        u, f = found
        chain.append(u)
        refl.append(f)
        v = u
    chain.reverse()
    refl.reverse()
    ok = all(member[u] for u in chain) and \
        all(chain[i + 1] == 2 * chain[i] - refl[i] and member[refl[i]]
            for i in range(len(refl))) and \
        all(chain[i + 1] > chain[i] for i in range(len(chain) - 1))
    return {'start': chain[0], 'end': chain[-1], 'len': len(chain),
            'verified': bool(ok), 'chain': chain[:40],
            'reflectors': refl[:39],
            'max_reflector': max(refl) if refl else 0}


# --------------------------------------- adaptive surface scan (new)

def adaptive_scan(S, member, N, sched_fn, own_parity, window=ADAPT_WINDOW,
                  rate_flag=0.8, t_lo=8):
    """Per octave, the EXACT attacker sets x (in-team, x <= 2^{t-1}) that
    attack (a) the kept bottom: y in the first `window` kept values of an
    own-parity block, and (b) the received-sliver top: y in the last
    `window` donated values of a partner-parity block; attack = completion
    z = 2y - x in-team.  Reports each set against the d_t-law prediction
    (kept: x >= d_t + 2; recv: x <= d_t - 1, both via octave-(t+1)
    completions; kept surfaces additionally admit in-block completions at
    x >= 2o).  Flags ADAPT-<surface> if the surface is attackable at >=
    rate_flag of octaves t in [t_lo, T-1]."""
    S = np.asarray(S, dtype=np.int64)
    T = g2.octave(N)
    rows = []
    for t in range(5, T):
        lo = 1 << (t - 1)
        bs = lo
        st = min(sched_fn(t), bs)
        snx = min(sched_fn(t + 1), 1 << t)
        d_t = 2 * st - snx
        if t % 2 == own_parity:
            surface = 'kept-bottom'
            ys = range(lo + st + 1, min(lo + st + window, 1 << t) + 1)
        else:
            surface = 'recv-top'
            if st == 0:
                continue
            ys = range(max(lo + 1, lo + st - window + 1), lo + st + 1)
        xs = []
        for y in ys:
            if y > N or not member[y]:
                continue
            a = int(np.searchsorted(S, y + 1))
            b = int(np.searchsorted(S, 2 * y))     # z <= 2y - 1
            z = S[a:b]
            x = 2 * y - z
            x = x[(x >= 1) & (x <= lo)]
            x = x[member[x]]
            if x.size:
                xs.append(x)
        xs = np.unique(np.concatenate(xs)) if xs else np.array([], np.int64)
        rows.append({'t': t, 'surface': surface, 's_t': int(st),
                     'd_t': int(d_t), 'n_attackers': int(xs.size),
                     'x_min': int(xs.min()) if xs.size else None,
                     'x_max': int(xs.max()) if xs.size else None,
                     'has_fixed_x_le_64': bool(xs.size and xs.min() <= 64),
                     'pred': (f'x >= d_t+2 = {d_t + 2} (sliver-mediated)'
                              if surface == 'kept-bottom' else
                              f'x <= d_t-1 = {d_t - 1}')})
    summary, flags = {}, []
    for surface in ('kept-bottom', 'recv-top'):
        rs = [r for r in rows if r['surface'] == surface and r['t'] >= t_lo]
        if not rs:
            continue
        hit = [r for r in rs if r['n_attackers'] > 0]
        rate = len(hit) / len(rs)
        summary[surface] = {
            'octaves': len(rs), 'attackable': len(hit),
            'rate': round(rate, 3),
            'flag': bool(rate >= rate_flag),
            'fixed_attacker_octaves':
                sum(1 for r in rs if r['has_fixed_x_le_64'])}
        if rate >= rate_flag:
            flags.append(f'ADAPT-{surface}')
    return {'rows': rows, 'summary': summary, 'flags': flags,
            'flag': bool(flags),
            'flag_reason': (f"scale-adapted attacker families recur on "
                            f"{flags}" if flags else
                            'no surface attackable at >= 80% of octaves')}


# ----------------------------------------------------- SAT screens

def verify_no_monotone_ap_np(seq, N, ds=None):
    """Numpy monotone-3-AP check of the sequence over [1, N]; ds = iterable
    of gaps to test (None = all).  Returns first bad triple or None."""
    pos = np.full(N + 1, -1, dtype=np.int64)
    arr = np.asarray(seq, dtype=np.int64)
    pos[arr] = np.arange(len(arr))
    if ds is None:
        ds = range(1, (N - 1) // 2 + 1)
    for d in ds:
        a, b, c = pos[1: N - 2 * d + 1], pos[1 + d: N - d + 1], \
            pos[1 + 2 * d: N + 1]
        m = (a >= 0) & (b >= 0) & (c >= 0)
        bad = m & (((a < b) & (b < c)) | ((a > b) & (b > c)))
        if bad.any():
            i = int(np.nonzero(bad)[0][0])
            return (i + 1, i + 1 + d, i + 1 + 2 * d)
    return None


def sat_screen(team, label, quick=False, rng=None):
    out = []
    for H in HORIZONS:
        V = team[team <= H]
        t0 = time.time()
        e = {'H': H, 'n': int(len(V))}
        seq = g2.abj_sorted([int(v) for v in V])
        if H <= WIT_FULL_H:
            bad = verify_no_monotone_ap_np(seq, H)
            e['witness'] = 'abj, fully verified' if bad is None else \
                f'ABJ WITNESS FAIL {bad}'
        else:
            rng = rng or np.random.default_rng(197)
            ds = sorted(set(range(1, 1025)) | set(
                int(d) for d in rng.integers(1025, H // 2, 1024)))
            bad = verify_no_monotone_ap_np(seq, H, ds)
            e['witness'] = (f'abj, verified on {len(ds)} sampled gaps'
                            if bad is None else f'ABJ WITNESS FAIL {bad}')
        e['result'] = 'SAT' if bad is None else 'WITNESS-FAIL'
        if H <= CDCL_H and not quick:
            res = g2.pure_complete_sat([int(v) for v in V], hint=seq)
            if res is False:
                e['result'] = 'UNSAT'
                e['cdcl'] = 'UNSAT'
            else:
                ver = g2.find_monotone_ap(res)
                e['cdcl'] = 'SAT, model verified' if ver is None \
                    else f'MODEL FAIL {ver}'
        e['time'] = round(time.time() - t0, 1)
        out.append(e)
        print(f"    [{label}] SAT H={H}: {e['result']} "
              f"({e.get('cdcl', e['witness'])}, {e['time']}s)", flush=True)
    return out


# ----------------------------------------------------- per-team screen

def screen_team(team, lab, name, sched_fn, own_parity, quick=False):
    rep = {'label': name, 'size': int(len(team)),
           'min': int(team[0]), 'max': int(team[-1])}
    flags = {}
    scans = []
    for H in HORIZONS:
        V = team[team <= H]
        Vl = [int(v) for v in V]
        member = np.zeros(H + 1, dtype=bool)
        member[V] = True
        here = []
        t0 = time.time()
        orb = g2.orbit_scan(Vl, H, ORBIT_FMAX)
        if orb.get('flag'):
            here.append('ORBIT')
        rayf = ray_scan(V, H, lambda t: ORBIT_FMAX, f'fixed {ORBIT_FMAX}')
        if rayf['flag'] and 'ORBIT' not in here:
            here.append('ORBIT')
        rayg = ray_scan(V, H, lambda t: 4 * sched_fn(t) + 64, '4*s_t + 64')
        if rayg['flag']:
            here.append('RAY-GROW')
        crn = g2.crown_scan(Vl, H, ATTACKER_MAX, 0.25)
        if crn['flag']:
            here.append('CROWN')
        per1 = h2.crown_persistence_scan(Vl, H, top_gap=1)
        per2 = h2.crown_persistence_scan(Vl, H, top_gap=2)
        if per1['flag'] or per2['flag']:
            here.append('CROWNP')
        slv = g2.sliver_scan(Vl, H, 8, 0.25)
        if slv['flag']:
            here.append('SLIVER')
        ada = adaptive_scan(V, member, H, sched_fn, own_parity)
        here.extend(ada['flags'])
        scans.append({'H': H, 'n': int(len(V)), 'flags': here,
                      'orbit_fmax64': orb, 'ray_fixed': rayf,
                      'ray_grow': rayg, 'crown_g2': crn,
                      'crown_persistence_gap1': {
                          'flag': per1['flag'],
                          'flagged_attackers': per1['flagged_attackers']},
                      'crown_persistence_gap2': per2,
                      'sliver': slv, 'adaptive': ada,
                      'time': round(time.time() - t0, 1)})
        flags[H] = here
        print(f"    [{name}] H=2^{g2.octave(H)}: "
              f"{here or 'clean'} ({scans[-1]['time']}s)", flush=True)
    rep['scans'] = scans
    rep['sat'] = sat_screen(team, name, quick=quick)
    if any(e['result'] == 'UNSAT' for e in rep['sat']):
        flags[CDCL_H] = flags.get(CDCL_H, []) + ['UNSAT']
    rep['flags_by_horizon'] = {str(k): v for k, v in flags.items()}
    top = flags[HORIZONS[-1]]
    death = sorted(set(f for f in top
                       if f in ('ORBIT', 'CROWN', 'CROWNP', 'UNSAT')))
    signals = sorted(set(f for f in top if f.startswith(('RAY', 'ADAPT'))
                         or f == 'SLIVER'))
    rep['death_signatures_at_top'] = death
    rep['signals_at_top'] = signals
    return rep


# ------------------------------------------------------- calibration

def calibrate():
    print('== G3 calibrations ==', flush=True)
    N = NMAX
    # 1. zero schedule reproduces S_A | S_B
    lab0 = build_labels(lambda t: 0, 'nat', N)
    A0, B0 = teams_from_labels(lab0)
    assert [int(v) for v in A0] == g2.gen_sa(N)
    assert [int(v) for v in B0] == g2.gen_sb(N)
    print('  s=0 == S_A | S_B: ok', flush=True)
    # 2. constant 8 reproduces h2 dyadic_bottom8 (at h2 NMAX = 2^16)
    lab8 = build_labels(lambda t: 8, 'nat', h2.NMAX)
    A8, B8 = teams_from_labels(lab8)
    hA, hB = h2.build_partition('dyadic', 'bottom', 8, h2.NMAX)
    assert [int(v) for v in A8] == hA and [int(v) for v in B8] == hB
    print('  s=8 == h2 dyadic_bottom8: ok', flush=True)
    # 3. ray scan controls at 2^15
    H = 1 << 15
    sa = np.asarray(g2.gen_sa(H))
    r = ray_scan(sa, H, lambda t: 64, 'fixed 64')
    assert not r['flag'] and r['best']['span'] <= 2, r['best']
    print(f"  ray(S_A, cap 64): span {r['best']['span']}, no flag: ok",
          flush=True)
    zp = np.arange(1, H + 1)
    r = ray_scan(zp, H, lambda t: 64, 'fixed 64')
    assert r['flag'] and r['best']['censored'], r['best']
    print(f"  ray(Z+, cap 64): span {r['best']['span']} censored, "
          f"flag: ok", flush=True)
    r = ray_scan(A8[A8 <= H], H, lambda t: 64, 'fixed 64')
    assert r['flag'], r['best']
    w = r['witness']
    assert w and w['verified']
    print(f"  ray(bottom8/A, cap 64): span {r['best']['span']} censored "
          f"flag, witness {w['chain'][:4]}... reflectors "
          f"{sorted(set(w['reflectors']))[:6]}: ok (h2 orbit rediscovered)",
          flush=True)
    # 4. persistence scan at top_gap=2 keeps its h2 calibration
    for gen, expect in (('sa', True), ('geneson', False)):
        S = g2.GENERATORS[gen](1 << 16)
        f = h2.crown_persistence_scan(S, 1 << 16, top_gap=2)['flag']
        assert f == expect, (gen, f)
    print('  persistence top_gap=2: sa flagged, geneson clean: ok',
          flush=True)


# ------------------------------------------------------------- driver

def run(quick=False, only=None):
    os.makedirs(os.path.join(REPO, 'data'), exist_ok=True)
    calibrate()
    summary = {'NMAX': NMAX, 'horizons': HORIZONS,
               'attacker_max': ATTACKER_MAX, 'orbit_fmax': ORBIT_FMAX,
               'ray_cap': '4*s_t + 64', 'candidates': []}
    survivors, deaths = [], []
    for skey, (sdesc, sfn) in SCHEDULES.items():
        for vkey, vdesc in VARIANTS.items():
            if only and f'{skey}_{vkey}' not in only:
                continue
            name = f'{skey}_{vkey}'
            t0 = time.time()
            lab = build_labels(sfn, vkey, NMAX)
            A, B = teams_from_labels(lab)
            verify_partition(lab, A, B, NMAX, HORIZONS)
            print(f"\n== {name}: {sdesc}, {vdesc} ==\n"
                  f"   |A|={len(A)} |B|={len(B)} "
                  f"densA={len(A)/NMAX:.3f}", flush=True)
            repA = screen_team(A, lab, f'{name}/A', sfn, 0, quick)
            repB = screen_team(B, lab, f'{name}/B', sfn, 1, quick)
            deathA, deathB = repA['death_signatures_at_top'], \
                repB['death_signatures_at_top']
            verdict = 'DEAD-SIGNATURE' if deathA or deathB else 'SURVIVOR'
            sat_ok = all(e['result'] == 'SAT'
                         for r in (repA, repB) for e in r['sat'])
            cand = {'name': name, 'schedule': skey, 'schedule_desc': sdesc,
                    'variant': vkey, 'variant_desc': vdesc,
                    's_values': {t: int(min(sfn(t), 1 << (t - 1)))
                                 for t in range(1, 19)},
                    'd_values': {t: int(2 * min(sfn(t), 1 << (t - 1))
                                        - min(sfn(t + 1), 1 << t))
                                 for t in range(1, 18)},
                    'sizeA': int(len(A)), 'sizeB': int(len(B)),
                    'teamA': repA, 'teamB': repB,
                    'sat_all_ok': bool(sat_ok),
                    'verdict': verdict,
                    'time': round(time.time() - t0, 1)}
            with open(os.path.join(REPO, 'data', f'g3_{name}.json'),
                      'w') as fh:
                json.dump(cand, fh, indent=1)
            row = {'name': name, 'verdict': verdict,
                   'deathA': deathA, 'signalsA': repA['signals_at_top'],
                   'deathB': deathB, 'signalsB': repB['signals_at_top'],
                   'sat_all_ok': bool(sat_ok)}
            summary['candidates'].append(row)
            (survivors if verdict == 'SURVIVOR' else deaths).append(name)
            print(f"   -> {verdict}  A death={deathA or '-'} "
                  f"signals={repA['signals_at_top'] or '-'} | "
                  f"B death={deathB or '-'} "
                  f"signals={repB['signals_at_top'] or '-'} "
                  f"({cand['time']}s)", flush=True)
    summary['survivors'] = survivors
    summary['deaths'] = deaths
    with open(os.path.join(REPO, 'data', 'g3_summary.json'), 'w') as fh:
        json.dump(summary, fh, indent=1)
    print(f"\nsurvivors: {survivors or 'NONE'}", flush=True)
    return summary


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--quick', action='store_true',
                    help='skip CDCL cross-checks')
    ap.add_argument('--only', help='comma list of <sched>_<variant> names')
    a = ap.parse_args()
    run(quick=a.quick, only=set(a.only.split(',')) if a.only else None)
