"""Erdős #197 — TASK V stage 1: TUNED per-parity growing-sliver schedules.

S1 (g3, notes/38) found the first clean partition team ever: geo_nat/A
(s_t = 2^{floor(t/2)}), clean because d_t = 2 s_t - s_{t+1} satisfies
d_even -> infinity (A's kept bottoms recede) AND d_odd = 0 (A's received
slivers are one-way).  Team B died exactly where its d_t stalls at 0.
The tuned question: can a PER-PARITY schedule give BOTH teams what A got —
donated depth growing on every block, kept bottoms receding on all blocks
of both teams?  The d_t law says NO (on each parity class, owner-safe
needs d_t -> inf while the receiver on the same class needs d_t bounded
by its smallest attacker), but the law was derived on parity-uniform
schedules; this screen adversarially tests it on six per-parity tunes,
natural crown ownership only, both teams, horizons 2^12 / 2^15 / 2^18,
with the full g3 instrument suite (ORBIT, RAY-GROW, CROWN, CROWNP,
ADAPT, SLIVER, pure-complete SAT).

Schedules (all with s_t -> infinity on both parities):
  geomix    s_t = 2^{t/2+1} (even) | 3*2^{(t-1)/2} (odd)
            d_even = 2^{t/2}, d_odd = 2^{(t+1)/2}: BOTH kept bottoms
            recede exponentially — the task's headline tune.
  geomirror s_t = 2^{floor((t-1)/2)}: the parity mirror of geo —
            d_odd = 2^{(t-1)/2} -> inf, d_even = 0.  Prediction: team B
            clean this time, team A doubly dead (symmetry control).
  geo3      s_t = 2^{floor(t/3)}: d_t = 0 at t = 2 mod 3 else
            2^{floor(t/3)} — the stall octaves alternate parity classes,
            so BOTH teams get infinitely many d=0 kept bottoms AND
            infinitely many d->inf received slivers.
  addgeo    s_t = 2^{floor(t/2)} + t: additive offset atop geo —
            d_even = 2^{t/2} + t - 1, d_odd = t - 1: the gentlest tune
            making both kept bottoms recede (odd class only linearly).
  linmix    s_t = 3t (even) | 2t (odd): per-parity linear —
            d_even = 4t - 2, d_odd = t - 3, both -> inf.
  neck2     s_t = floor(7*2^t/128) + 2: constant neck d_t = 2 (t >= 8) —
            the bounded-positive-neck corner (RUNG-IN/T-PIN regime):
            receivers attacked by x <= 1, owners by every x >= 4.

d_t-law predictions per candidate are computed and printed up front and
the observed death signatures are checked against them.

Usage: .venv/bin/python experiments/v2_tuned_screen.py [--quick]
Artifacts: data/v2_<name>.json + data/v2_summary.json.
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

import g2_diagnose as g2                # noqa: E402
import g3_growing_sliver as g3          # noqa: E402


def s_geomix(t):
    return (1 << (t // 2 + 1)) if t % 2 == 0 else 3 * (1 << ((t - 1) // 2))


def s_geomirror(t):
    return 1 << ((t - 1) // 2) if t >= 1 else 0


def s_geo3(t):
    return 1 << (t // 3)


def s_addgeo(t):
    return (1 << (t // 2)) + t


def s_linmix(t):
    return 3 * t if t % 2 == 0 else 2 * t


def s_neck2(t):
    return (7 << t >> 7) + 2


TUNED = {
    'geomix': ('s = 2^{t/2+1} even | 3*2^{(t-1)/2} odd  '
               '(d_even = 2^{t/2}, d_odd = 2^{(t+1)/2})', s_geomix),
    'geomirror': ('s = 2^{floor((t-1)/2)}  (mirror of geo: d_odd -> inf, '
                  'd_even = 0)', s_geomirror),
    'geo3': ('s = 2^{floor(t/3)}  (d = 0 at t = 2 mod 3, else 2^{t/3})',
             s_geo3),
    'addgeo': ('s = 2^{floor(t/2)} + t  (d_even ~ 2^{t/2}, d_odd = t-1)',
               s_addgeo),
    'linmix': ('s = 3t even | 2t odd  (d_even = 4t-2, d_odd = t-3)',
               s_linmix),
    'neck2': ('s = floor(7*2^t/128) + 2  (constant neck d_t = 2)',
              s_neck2),
}


def st_trunc(fn, t):
    return min(fn(t), 1 << (t - 1))


def d_of(fn, t):
    return 2 * st_trunc(fn, t) - min(fn(t + 1), 1 << t)


def predict(fn, t_lo=10, t_hi=40):
    """d_t-law prediction per team: which surfaces carry recurring fixed
    attackers.  Team A owns even octaves (kept-bottom surface there,
    receiver on odd); B mirrors.  Returns {'A': [...], 'B': [...]} of
    predicted death surfaces (attacked at infinitely many octaves by a
    fixed x <= 8, per the law's iffs, sampled on [t_lo, t_hi])."""
    out = {}
    for team, own_par in (('A', 0), ('B', 1)):
        surf = []
        kept_hit = [t for t in range(t_lo, t_hi) if t % 2 == own_par
                    and d_of(fn, t) + 2 <= 8]
        recv_hit = [t for t in range(t_lo, t_hi) if t % 2 != own_par
                    and d_of(fn, t) - 1 >= 1]
        if len(kept_hit) >= (t_hi - t_lo) // 8:
            surf.append(f'kept-bottom (d<=6 at {len(kept_hit)} octaves, '
                        f'e.g. t={kept_hit[:4]})')
        if len(recv_hit) >= (t_hi - t_lo) // 8:
            surf.append(f'recv-top (d>=2 at {len(recv_hit)} octaves, '
                        f'e.g. t={recv_hit[:4]})')
        out[team] = surf or ['CLEAN predicted']
    return out


def run(quick=False, only=None):
    os.makedirs(os.path.join(REPO, 'data'), exist_ok=True)
    g3.calibrate()
    summary = {'NMAX': g3.NMAX, 'horizons': g3.HORIZONS,
               'purpose': 'tuned per-parity schedules: can BOTH teams be '
                          'clean? (d_t law says no)',
               'candidates': []}
    survivors = []
    for name, (desc, fn) in TUNED.items():
        if only and name not in only:
            continue
        t0 = time.time()
        lab = g3.build_labels(fn, 'nat', g3.NMAX)
        A, B = g3.teams_from_labels(lab)
        g3.verify_partition(lab, A, B, g3.NMAX, g3.HORIZONS)
        pred = predict(fn)
        print(f"\n== v2 {name}: {desc} ==\n"
              f"   |A|={len(A)} |B|={len(B)}  "
              f"d_t (t=10..21): {[d_of(fn, t) for t in range(10, 22)]}\n"
              f"   d_t-law prediction A: {pred['A']}\n"
              f"   d_t-law prediction B: {pred['B']}", flush=True)
        repA = g3.screen_team(A, lab, f'v2_{name}/A', fn, 0, quick)
        repB = g3.screen_team(B, lab, f'v2_{name}/B', fn, 1, quick)
        deathA = repA['death_signatures_at_top']
        deathB = repB['death_signatures_at_top']
        verdict = 'DEAD-SIGNATURE' if deathA or deathB else 'SURVIVOR'
        both_clean = not deathA and not deathB
        sat_ok = all(e['result'] == 'SAT'
                     for r in (repA, repB) for e in r['sat'])
        agree = {}
        for team, death in (('A', deathA), ('B', deathB)):
            want_dead = pred[team] != ['CLEAN predicted']
            agree[team] = bool(want_dead == bool(death))
        cand = {'name': name, 'desc': desc,
                's_values': {t: int(st_trunc(fn, t)) for t in range(1, 19)},
                'd_values': {t: int(d_of(fn, t)) for t in range(1, 18)},
                'prediction': pred, 'prediction_matches': agree,
                'sizeA': int(len(A)), 'sizeB': int(len(B)),
                'teamA': repA, 'teamB': repB,
                'sat_all_ok': bool(sat_ok), 'verdict': verdict,
                'both_teams_clean': bool(both_clean),
                'time': round(time.time() - t0, 1)}
        with open(os.path.join(REPO, 'data', f'v2_{name}.json'), 'w') as fh:
            json.dump(cand, fh, indent=1)
        summary['candidates'].append(
            {'name': name, 'verdict': verdict,
             'deathA': deathA, 'signalsA': repA['signals_at_top'],
             'deathB': deathB, 'signalsB': repB['signals_at_top'],
             'prediction_matches': agree, 'sat_all_ok': bool(sat_ok),
             'both_teams_clean': bool(both_clean)})
        if both_clean:
            survivors.append(name)
        print(f"   -> {verdict}  A death={deathA or '-'} | "
              f"B death={deathB or '-'}  law-match={agree} "
              f"({cand['time']}s)", flush=True)
    summary['both_clean_survivors'] = survivors
    with open(os.path.join(REPO, 'data', 'v2_summary.json'), 'w') as fh:
        json.dump(summary, fh, indent=1)
    print(f"\nboth-teams-clean survivors: {survivors or 'NONE'}", flush=True)
    return summary


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--quick', action='store_true')
    ap.add_argument('--only', help='comma list of tuned schedule names')
    a = ap.parse_args()
    run(quick=a.quick, only=set(a.only.split(',')) if a.only else None)
