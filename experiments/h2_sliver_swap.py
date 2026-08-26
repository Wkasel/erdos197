"""Erdős #197 — H2: sliver-swap partition screening.

The dyadic disproof kills S_A because each team owns the bottom sliver of
every one of its own blocks: crowns 15/16 sit low, and every block's bottom
offers in-team attacked pairs (y bottom, z = 2y - x in-team).  Notes/37
suggests the remaining candidate YES shape is "alternating crown ownership
+ sliver swaps": both teams get block structures, but each team DONATES the
first s values of each of its blocks to the other team, so neither team
owns its own crown attack surface.  This driver builds that family and
screens every member with the G2 death diagnostics plus a new CROWN
PERSISTENCE scan tuned to catch relocated attack surfaces.

Candidate family (exact partitions of [1, N]):
  family 'dyadic': blocks (2^{t-1}, 2^t], t >= 1; even t -> team A, odd ->
                   team B; the value 1 always rides with team B (paper
                   convention: S_B = {1} + odd blocks).
  family 'quad'  : blocks (4^{k-1}, 4^k], k >= 1 (Geneson-style ratio-4
                   spacing between a team's consecutive blocks); even k ->
                   A, odd k -> B; 1 -> B.
  swap 'none'    : no donation (dyadic none == the proven-dead S_A | S_B —
                   calibration row; asserted equal to g2's gen_sa/gen_sb).
  swap 'bottom'  : each block's first min(s, |block|) values go to the
                   OTHER team (neither team owns its own bottom slivers).
  swap 'top'     : each block's last min(s, |block|) values go to the other
                   team (control: donation at the harmless end).
  s in {8, 12, 16}.

Screens per TEAM (teams are fixed sets — no coloring freedom):
  (i)   pure-complete SAT at horizons 512/1024/4096: ABJ bit-reversal
        witness + independent monotone-3-AP verification; CDCL (Cadical195,
        lazy transitivity) cross-check at H <= 1024.  THEOREM (g2 header):
        the pure-complete window of ANY fixed set is satisfiable (the ABJ
        order on Z has no monotone 3-AP at all), so (i) is a consistency
        check, never a death certificate; death signals are (ii)-(iv).
  (ii)  ORBIT scan (g2, lem:orbit): censored in-team doubling chains.
  (iii) CROWN scans, two modes:
        - g2 recurrence scan (occ_thresh 0.25): attackers x <= 64 whose
          attacked pairs recur at >= 90% of occupied octaves above them.
        - H2 PERSISTENCE scan (new, this file): attacker x <= 64 in-team
          is flagged iff its attacked octaves number >= 4 AND reach within
          1 of the team's top octave (attacks persist to the horizon).
          Rationale: thm:ogred's pigeonhole needs attacks at infinitely
          many scales, not at a fixed density of octaves; a swap team's
          attacks can live on every OTHER octave (donated slivers), which
          the ratio test's mixed-parity denominator would dilute to 0.5.
          Calibrated below: S_A -> flagged (15/16 et al.), Geneson W ->
          clean (attacked octaves {3,5} only, stage-1 relics), W-complement
          -> flagged.
  (iv)  SLIVER load (g2): bottom-8 in-team fraction of occupied octaves.

Verdict: a candidate SURVIVES iff neither team raises any flag at any
horizon in {512, 1024, 4096} nor in the deep structural scan at 2^16.

Usage: .venv/bin/python experiments/h2_sliver_swap.py  [--quick]
Artifacts: data/h2_<candidate>.json per candidate + data/h2_summary.json.
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

import g2_diagnose as g2  # noqa: E402  (reuse the calibrated kit)

NMAX = 1 << 16            # 2^16 = 4^8: block boundary for BOTH families
SAT_HORIZONS = [512, 1024, 4096]
SCAN_HORIZONS = [512, 1024, 4096, NMAX]
CDCL_MAX_H = 1024         # CDCL cross-check where windows are small
ATTACKER_MAX = 64
# Bottom-swap orbit systems use reflectors up to ~3s (hand-verified:
# s=16 team A rides 2^{e-1}+24 -> 2^e+16 -> 2^{e+1}+24 with f in {32, 8});
# fmax = 48 covers all s <= 16 patterns.  g2's default 16 misses them.
ORBIT_FMAX = 48
SLIVER_WIDTH = 8


# ------------------------------------------------------------ generators

def blocks(family, N):
    """Block list [(index, lo, hi)] covering (1, N]; index parity = owner."""
    r = 2 if family == 'dyadic' else 4
    out, i = [], 1
    while r ** (i - 1) < N:
        out.append((i, r ** (i - 1) + 1, min(r ** i, N)))
        i += 1
    return out

def build_partition(family, swap, s, N):
    """Return (A, B): exact partition of [1, N].  Even-index blocks belong
    to A, odd-index to B; 'bottom'/'top' donate min(s, |block|) end values
    of every block to the other team; 1 always joins B (never donated)."""
    A, B = [], [1]
    for i, lo, hi in blocks(family, N):
        owner, other = (A, B) if i % 2 == 0 else (B, A)
        size = hi - lo + 1
        se = min(s, size) if swap != 'none' else 0
        if swap == 'bottom':
            other.extend(range(lo, lo + se))
            owner.extend(range(lo + se, hi + 1))
        elif swap == 'top':
            owner.extend(range(lo, hi - se + 1))
            other.extend(range(hi - se + 1, hi + 1))
        else:
            owner.extend(range(lo, hi + 1))
    return sorted(A), sorted(B)


# ----------------------------------------------- H2 crown persistence scan

def crown_persistence_scan(S, N, attacker_max=ATTACKER_MAX,
                           min_octs=4, top_gap=1, max_examples=3):
    """Flag in-team attackers x <= attacker_max whose attacked pairs
    (y, z = 2y - x), y and z in-team, y in an octave fully above x, occur
    in >= min_octs octaves AND reach within top_gap of the team's top
    octave.  Unlike g2's ratio test this is parity-robust: attacks that
    recur on every other octave (e.g. via donated slivers) still flag."""
    Sarr = np.asarray(S, dtype=np.int64)
    top_t = g2.octave(int(Sarr[-1]))
    octs = []
    t = 1
    while (1 << (t - 1)) < N:
        lo, hi = 1 << (t - 1), min(1 << t, N)
        a, b = np.searchsorted(Sarr, [lo + 1, hi + 1])
        if b > a:
            octs.append((t, lo, int(a), int(b)))
        t += 1
    rows = []
    for x in (int(v) for v in S if v <= attacker_max):
        ts, ex = [], []
        for (t, lo, a, b) in octs:
            if lo < x:
                continue
            y = Sarr[a:b]
            z = 2 * y - x
            j = np.searchsorted(Sarr, z)
            ok = j < len(Sarr)
            jj = np.where(ok, j, 0)
            ok &= Sarr[jj] == z
            if ok.any():
                ts.append(t)
                if len(ex) < max_examples:
                    yy = int(y[ok][0])
                    ex.append([x, yy, 2 * yy - x])
        persists = len(ts) >= min_octs and ts[-1] >= top_t - top_gap
        if ts:
            rows.append({'x': x, 'n_attacked': len(ts),
                         'attacked_octaves': ts[:24], 'top_attacked': ts[-1],
                         'persists': persists, 'examples': ex})
    flagged = [r['x'] for r in rows if r['persists']]
    shown = [r for r in rows if r['persists']][:16] or rows[:8]
    return {'attacker_max': attacker_max, 'top_octave': top_t,
            'min_octs': min_octs, 'top_gap': top_gap,
            'flagged_attackers': flagged, 'rows': shown,
            'flag': bool(flagged),
            'flag_reason': (
                f"attackers {flagged[:12]} attack in >= {min_octs} octaves "
                f"persisting to the horizon (top octave {top_t})"
                if flagged else
                'no attacker persists to the horizon in >= 4 octaves')}


# ----------------------------------- infinite-orbit certificates (dyadic)

# Period-2 orbit systems u -> 2u - f in the dyadic bottom-swap teams,
# found by the (fmax=48) orbit scan and verified here for ALL octaves:
# the team with kept-body offset o1 (in its own blocks, o1 > s) and
# received-sliver offset o2 (in the other team's blocks, o2 <= s) rides
#   2^{t-1} + o1  --f1-->  2^t + o2  --f2-->  2^{t+1} + o1  --> ...
# forever, with fixed in-team reflectors {f1, f2}.  Membership of each
# link is octave-periodic, so checking the offset algebra
# (2 o1 - f1 = o2, 2 o2 - f2 = o1) plus one octave of memberships proves
# the infinite orbit; the walk below to 2^60 is gratuitous confirmation.
# By the paper's lem:orbit (DEGS-via-chunks) any team containing such a
# system is NOT permutable — a hard death, not a heuristic flag.
ORBIT_SYSTEMS = {                     # (s, team) -> offsets & reflectors
    (8, 'A'): dict(o1=14, o2=8, f1=20, f2=2),
    (8, 'B'): dict(o1=12, o2=8, f1=16, f2=4),
    (12, 'A'): dict(o1=19, o2=12, f1=26, f2=5),
    (12, 'B'): dict(o1=13, o2=11, f1=15, f2=9),
    (16, 'A'): dict(o1=24, o2=16, f1=32, f2=8),
    (16, 'B'): dict(o1=23, o2=13, f1=33, f2=3),
}

def member_dyadic_bottom(v, s, team):
    """Closed-form membership for the dyadic bottom-swap partition."""
    if v == 1:
        return team == 'B'
    t = (v - 1).bit_length()
    lo = 1 << (t - 1)
    donated = (v - lo) <= min(s, lo)
    in_A = ((t % 2 == 0) and not donated) or ((t % 2 == 1) and donated)
    return in_A if team == 'A' else not in_A

def verify_orbit_certificates():
    """Verify ORBIT_SYSTEMS (algebra + membership walk to 2^60) and
    cross-check member_dyadic_bottom against build_partition at NMAX."""
    for s in (8, 12, 16):
        A, B = build_partition('dyadic', 'bottom', s, NMAX)
        As = set(A)
        assert all(member_dyadic_bottom(v, s, 'A') == (v in As)
                   for v in range(1, NMAX + 1)), f'membership rule s={s}'
    out = {}
    for (s, team), y in sorted(ORBIT_SYSTEMS.items()):
        o1, o2, f1, f2 = y['o1'], y['o2'], y['f1'], y['f2']
        assert o1 > s >= o2, (s, team)
        assert 2 * o1 - f1 == o2 and 2 * o2 - f2 == o1, (s, team)
        assert member_dyadic_bottom(f1, s, team), (s, team, f1)
        assert member_dyadic_bottom(f2, s, team), (s, team, f2)
        t = 6 if team == 'A' else 7          # kept-octave parity
        u, steps, fs = (1 << (t - 1)) + o1, 0, (f1, f2)
        chain0 = [u]
        while u < (1 << 60):
            assert member_dyadic_bottom(u, s, team), (s, team, u)
            u = 2 * u - fs[steps % 2]
            steps += 1
            if len(chain0) < 6:
                chain0.append(u)
        out[f'{s}/{team}'] = dict(y, start=chain0[0], steps=steps,
                                  chain_head=chain0,
                                  verified_to=int(u).bit_length() - 1)
    return out


# ------------------------------------------------------------- per team

def screen_team(T, label, quick=False):
    """Run all screens on the fixed team T; return (report, flags)."""
    rep = {'label': label, 'size': len(T), 'min': T[0], 'max': T[-1]}
    flags = []

    sat = []
    for H in SAT_HORIZONS:
        V = [v for v in T if v <= H]
        t0 = time.time()
        e = {'H': H, 'n': len(V)}
        seq = g2.abj_sorted(V)
        bad = g2.find_monotone_ap(seq)
        if bad is not None:                      # impossible per ABJ theorem
            e.update(result='WITNESS-FAIL', counterexample=list(bad))
            flags.append(f'WITNESS-FAIL@{H}')
        else:
            e.update(result='SAT', method='abj-witness', witness_verified=True)
            if H <= CDCL_MAX_H and not quick:
                res = g2.pure_complete_sat(V, hint=seq)
                if res is False:
                    e.update(result='UNSAT', method='cadical-lazy-trans')
                    flags.append(f'UNSAT@{H}')
                else:
                    e.update(method='abj-witness+cadical',
                             cdcl_verified=g2.find_monotone_ap(res) is None)
        e['time'] = round(time.time() - t0, 2)
        sat.append(e)
    rep['sat'] = sat

    scans = []
    for H in (SCAN_HORIZONS[:-1] if quick else SCAN_HORIZONS):
        V = [v for v in T if v <= H]
        orb = g2.orbit_scan(V, H, ORBIT_FMAX)
        crn = g2.crown_scan(V, H, ATTACKER_MAX, 0.25)
        per = crown_persistence_scan(V, H)
        slv = g2.sliver_scan(V, H, SLIVER_WIDTH, 0.25)
        here = []
        if orb.get('flag'):
            here.append('ORBIT')
        if crn['flag']:
            here.append('CROWN')
        if per['flag']:
            here.append('CROWNP')
        if slv['flag']:
            here.append('SLIVER')
        flags.extend(f'{f}@{H}' for f in here)
        scans.append({'H': H, 'n': len(V), 'flags': here,
                      'orbit': orb, 'crown_g2': crn,
                      'crown_persistence': per, 'sliver': slv})
    rep['scans'] = scans
    rep['flags'] = flags
    return rep, flags


# --------------------------------------------------------------- driver

def candidate_names():
    out = []
    for family in ('dyadic', 'quad'):
        out.append((family, 'none', 0))
        for swap in ('bottom', 'top'):
            for s in (8, 12, 16):
                out.append((family, swap, s))
    return out


def summarize_flags(flags):
    """Collapse ['CROWN@512', 'CROWN@1024', ...] -> {'CROWN': [512, ...]}."""
    d = {}
    for f in flags:
        kind, h = f.split('@')
        d.setdefault(kind, []).append(int(h))
    return d


def run(quick=False):
    os.makedirs(os.path.join(REPO, 'data'), exist_ok=True)

    # --- calibration of the persistence scan on the known references
    print('== calibrating crown persistence scan (N=2^16) ==', flush=True)
    calib = {}
    for name, gen, expect in (('sa', g2.gen_sa, True),
                              ('geneson', g2.gen_geneson, False),
                              ('geneson_c', g2.gen_geneson_c, True)):
        S = gen(NMAX)
        r = crown_persistence_scan(S, NMAX)
        calib[name] = {'flag': r['flag'], 'expected': expect,
                       'flagged_attackers': r['flagged_attackers'][:12],
                       'pass': r['flag'] == expect}
        print(f"  {name:10s} flag={r['flag']} (expected {expect}) "
              f"attackers={r['flagged_attackers'][:8]}", flush=True)
    assert all(c['pass'] for c in calib.values()), \
        'persistence scan mis-calibrated'

    # --- dyadic none must reproduce the paper partition exactly
    A0, B0 = build_partition('dyadic', 'none', 0, NMAX)
    assert A0 == g2.gen_sa(NMAX) and B0 == g2.gen_sb(NMAX), \
        'dyadic none != S_A | S_B'

    # --- lem:orbit hard-death certificates for the dyadic bottom teams
    print('== verifying infinite-orbit certificates (to 2^60) ==', flush=True)
    certs = verify_orbit_certificates()
    for k, c in certs.items():
        print(f"  s={k}: {c['chain_head'][:4]}... reflectors "
              f"{{{c['f1']}, {c['f2']}}} verified {c['steps']} steps",
              flush=True)

    summary = {'NMAX': NMAX, 'sat_horizons': SAT_HORIZONS,
               'scan_horizons': SCAN_HORIZONS[:-1] if quick else SCAN_HORIZONS,
               'attacker_max': ATTACKER_MAX, 'orbit_fmax': ORBIT_FMAX,
               'persistence_calibration': calib,
               'orbit_certificates': certs, 'candidates': []}
    survivors, deaths = [], []

    for family, swap, s in candidate_names():
        name = f'{family}_{swap}' + (str(s) if swap != 'none' else '')
        t0 = time.time()
        A, B = build_partition(family, swap, s, NMAX)
        assert len(A) + len(B) == NMAX and not set(A) & set(B), \
            f'{name}: not a partition'
        print(f'== {name}: |A|={len(A)} |B|={len(B)} ==', flush=True)
        repA, flagsA = screen_team(A, f'{name}/A', quick)
        repB, flagsB = screen_team(B, f'{name}/B', quick)
        verdict = ('SURVIVOR' if not flagsA and not flagsB else 'DEAD')
        if family == 'dyadic' and swap == 'bottom':
            mech = ('lem:orbit HARD DEATH both teams (verified infinite '
                    'period-2 orbit systems: '
                    f"A {ORBIT_SYSTEMS[(s, 'A')]}, B {ORBIT_SYSTEMS[(s, 'B')]}"
                    '); donation gives each team a landing pad in every '
                    'other octave, restoring the doubling orbits S_A broke '
                    '+ portable crown pairs one octave up')
        elif family == 'dyadic' and swap == 'none':
            mech = ('paper theorem: S_A dead via crowns 15/16 + C3; '
                    'screens show CROWN+SLIVER on both teams')
        elif family == 'dyadic':
            mech = ('top donation leaves own block bottoms intact: full '
                    'S_A crown/sliver pattern on both teams, plus donated '
                    'top slivers reflect into the next octave top '
                    '(2(2^t - i) - f = 2^{t+1} - 2i - f in-team)')
        else:
            mech = ('ratio-4 blocks trap reflections in-block '
                    '(2y - x <= 4^k for y in the lower half), so every '
                    'small in-team x attacks every own block regardless '
                    'of sliver donation: CROWN(+P)+SLIVER on both teams')
        cand = {'name': name, 'family': family, 'swap': swap, 's': s,
                'mechanism': mech,
                'sizeA': len(A), 'sizeB': len(B),
                'A_upto_4096': [v for v in A if v <= 4096],
                'teamA': repA, 'teamB': repB,
                'flagsA': summarize_flags(flagsA),
                'flagsB': summarize_flags(flagsB),
                'verdict': verdict, 'time': round(time.time() - t0, 1)}
        path = os.path.join(REPO, 'data', f'h2_{name}.json')
        with open(path, 'w') as fh:
            json.dump(cand, fh, indent=1)
        row = {'name': name, 'verdict': verdict, 'mechanism': mech,
               'flagsA': cand['flagsA'], 'flagsB': cand['flagsB']}
        summary['candidates'].append(row)
        (survivors if verdict == 'SURVIVOR' else deaths).append(name)
        print(f"   A: {sorted(set(f.split('@')[0] for f in flagsA)) or 'clean'}"
              f"   B: {sorted(set(f.split('@')[0] for f in flagsB)) or 'clean'}"
              f"   -> {verdict}  ({cand['time']}s)", flush=True)

    summary['survivors'] = survivors
    summary['deaths'] = deaths
    spath = os.path.join(REPO, 'data', 'h2_summary.json')
    with open(spath, 'w') as fh:
        json.dump(summary, fh, indent=1)
    print(f'\nsurvivors: {survivors or "NONE"}', flush=True)
    print(f'saved {spath}', flush=True)
    return summary


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--quick', action='store_true',
                    help='skip CDCL cross-checks and the deep 2^16 scan')
    run(quick=ap.parse_args().quick)
