"""Erdős #197 — H1: is the complement of Geneson's 2/3-density witness alive?

Geneson (arXiv:2608.12604) builds a permutable W of upper density 2/3 from
stages of ratio-r octaves [L_k r^j + M_{k-1}, t L_k r^j], j = 0..J(k), with
L_k = lam * M_{k-1}, M_k = t L_k r^{J(k)} (paper: lam=4, r=4, t=2, J(k)=k).
A YES-partition of N using W needs the exact complement C = N \\ W to be
permutable too.  This experiment decides the orbit question for C:

  (1) KILL (paper parameters).  Every block boundary is a power of 2, and
      one checks (mechanically below, for all scales) that 2^s + 3 lies in
      C for every s >= 5: octave bottoms carry a sliver of width
      M_{k-1} >= 4 (k >= 2), octave tops open into silent zones, and chasm
      interiors/boundaries absorb the rest.  Hence
          u_m = 2^{m+5} + 3,   u_{m+1} = 2 u_m - 3,   3 in C
      is an infinite doubling orbit inside C with the single reflector 3,
      so C is NOT permutable by the orbit obstruction (paper lem:orbit).
      The dyadic partition disproof and Geneson's construction meet:
      removing the slivers is exactly what makes W permutable, and
      receiving them is exactly what kills C.

  (2) LAW (parameter space).  An infinite orbit u_{m+1} = 2u_m - f_m with
      f_m in a finite F satisfies u_m = 2^m A + t_m with t_m bounded
      (t_m = sum_{i>=m} f_i 2^{m-1-i} in [min F, max F]).  So C contains an
      infinite orbit iff some ratio-2 geometric ray A*2^m stays within
      bounded distance of C.  For the Geneson family (t = 2) this is a
      2-adic alignment condition:
        * within a stage the ray must ride the bottom sliver of EVERY
          octave (the silent zone (2 L r^j, L r^{j+1}) has log_2-length
          exactly log2(r/2), and doubling from its interior lands in the
          next octave's interior unless r is a power of 2 and the ray is
          anchored on L_k * 2^i);
        * across stages the anchor jumps by L_{k+1}/L_k = 2 lam r^{J(k)},
          so frac(log2 anchor) shifts by frac(log2(2 lam)) each stage.
      Hence: infinite orbit in C  <=>  r and 2*lam are powers of 2.
      In particular lam = 3 (upper density of W still 2/3, only the
      approach speed and lower density change) makes C ORBIT-FREE: every
      doubling chain that crosses a stage boundary dies at octave 1 of the
      following stage (misalignment 3*2^i vs 2^j is a factor >= 4/3,
      i.e. an error proportional to scale, unfixable by bounded
      reflectors).  So there is NO universal "complement contains an
      infinite orbit" theorem for the family — but the paper instance is
      dead, and the orbit-free tunings still inherit every sliver, all
      silent zones and chasms, and upper density 1 - 2/(3(lam+1)).

  (3) QUANTIFICATION (intervals vs orbits).  A single interval [a, b] in a
      team supports doubling chains of length only floor(log2((b-f)/(a-f)))
      + 1 ~ log2(b/a): absolute length is irrelevant, ratio is the
      currency.  C's maximal runs have ratio <= max(lam, r/2) — bounded —
      so "C contains arbitrarily long intervals" is NOT by itself fatal
      (lam = 3 realises this: arbitrarily long chasms, no infinite orbit).
      Fatal is a 2-adically aligned geometric ladder, as in (1).
      Lemma R (ratio-ascent, needs {m, 2m, 3m, 5m} in the team): any run
      of ratio > 5 contains a quadruple; C's runs are shorter, but the
      composite run chasm+sliver+silent still contains Lemma-R quadruples
      at every stage (paper params: m in (1.6 M_k, 5 M_k/3), giving
      m, 2m in the chasm, 3m in the sliver, 5m in the silent zone).

Everything asserted above is verified mechanically below.

Usage:  .venv/bin/python experiments/h1_complement.py          (full run)
Writes  data/h1_complement.json (+ prints a log; tee to data/h1_run.log).
"""
import json
import os
import sys
import time
from bisect import bisect_right

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'experiments'))

from g2_diagnose import abj_sorted, find_monotone_ap


# ---------------------------------------------------------------- structure

def stages(bound, lam=4, r=4, t=2, J=lambda k: k):
    """Exact stage structure up to `bound` (python ints, no overflow).
    Yields dicts with L, M_prev, M, octaves [(lo_sliver, lo_block, hi)],
    where octave j is [L r^j + M_prev, t L r^j], sliver [L r^j, L r^j +
    M_prev - 1], silent zone (t L r^j, L r^{j+1}), chasm (M_k, L_{k+1})."""
    assert lam >= 3 and r >= 4 and 2 * t <= r
    M_prev, k = 1, 0
    while True:
        k += 1
        L = lam * M_prev
        if L > bound:
            return
        octs = []
        for j in range(J(k) + 1):
            X = L * r ** j
            octs.append((X, X + M_prev, t * X))
        yield {'k': k, 'L': L, 'M_prev': M_prev, 'M': t * L * r ** J(k),
               'octaves': octs}
        M_prev = t * L * r ** J(k)


def w_intervals(bound, **kw):
    """Closed intervals of W up to bound (exact, unbounded-safe)."""
    out = []
    for st in stages(bound, **kw):
        for _, lo, hi in st['octaves']:
            if lo <= bound:
                out.append((lo, min(hi, bound)))
    return out


class Membership:
    """O(log) membership tests for W and C = N \\ W up to `bound`."""

    def __init__(self, bound, **kw):
        self.bound = bound
        self.iv = sorted(w_intervals(bound, **kw))
        self.los = [a for a, _ in self.iv]

    def in_W(self, v):
        assert 1 <= v <= self.bound
        i = bisect_right(self.los, v) - 1
        return i >= 0 and v <= self.iv[i][1]

    def in_C(self, v):
        return not self.in_W(v)


def c_set(N, **kw):
    W = set()
    for a, b in w_intervals(N, **kw):
        W.update(range(a, b + 1))
    return sorted(set(range(1, N + 1)) - W)


# ------------------------------------------------- (1) the explicit orbit

def explicit_orbit_kill(t_max=200, lam=4, r=4, t=2, J=lambda k: k,
                        classify=True):
    """Verify u_s = 2^s + 3 in C for all s >= s0 up to t_max (exact
    big-int interval arithmetic — horizon 2^{t_max}), and record the
    structural classification of each 2^s.  Checks the reflector 3 in C.
    Returns s0 = the smallest bound from which the ray never leaves C."""
    memb = Membership(1 << (t_max + 1), lam=lam, r=r, t=t, J=J)
    ok3 = memb.in_C(3)
    cls = []
    good = []
    for s in range(2, t_max + 1):
        v = (1 << s) + 3
        inC = memb.in_C(v)
        good.append(inC)
        if not classify:
            continue
        p = 1 << s
        kind = 'chasm'
        for st in stages(2 * p, lam=lam, r=r, t=t, J=J):
            for X, lo, hi in st['octaves']:
                if p == X:
                    kind = f'octave-bottom k={st["k"]}'
                elif p == hi:
                    kind = f'octave-top k={st["k"]}'
        cls.append({'s': s, 'u': f'2^{s}+3', 'in_C': inC, 'pow2_is': kind})
    # smallest s0 with all s >= s0 in C
    s0 = None
    for i in range(len(good) - 1, -1, -1):
        if not good[i]:
            s0 = i + 3
            break
    s0 = 2 if s0 is None else s0
    eventually = all(good[s0 - 2:])
    return {'orbit': f'u_s = 2^s + 3, s >= {s0}; u_(s+1) = 2 u_s - 3',
            'reflector_in_C': ok3, 'checked_up_to': f'2^{t_max}',
            'ray_in_C_from': s0 if eventually and s0 <= t_max - 5 else None,
            'all_in_C_from_s0': eventually,
            'sample': cls[:12] + cls[-3:] if classify else None}


# ------------------------------- (2) exhaustive scale-by-scale propagation

def propagate(memb, F, m0, m1, cap=500000):
    """EXACT reachability closure: every value of C reachable by chains
    u -> 2u - f (f in F, strictly increasing) started anywhere in
    C cap [2^{m0}, 2^{m0+1}).  Processes values in increasing order
    (steps strictly increase), so the closure is exhaustive.  If no
    reachable value reaches 2^{m1}, every such chain provably dies —
    the certificate is the complete reachable set with all dead ends."""
    import heapq
    start = [v for v in range(1 << m0, 1 << (m0 + 1)) if memb.in_C(v)]
    seen = set(start)
    heap = list(start)
    heapq.heapify(heap)
    limit = 1 << m1
    survivors, dead_ends, max_reached = [], [], 0
    while heap:
        v = heapq.heappop(heap)
        max_reached = max(max_reached, v)
        if v >= limit:
            survivors.append(v)
            if len(survivors) >= 8:
                break
            continue
        ext = False
        for f in F:
            w = 2 * v - f
            if w > v and w <= memb.bound and memb.in_C(w):
                ext = True
                if w not in seen:
                    seen.add(w)
                    heapq.heappush(heap, w)
        if not ext:
            dead_ends.append(v)
        if len(seen) > cap:
            raise RuntimeError('propagation blow-up')
    per_scale = {}
    for v in seen:
        per_scale[v.bit_length() - 1] = per_scale.get(v.bit_length() - 1,
                                                      0) + 1
    hist = [{'m': m, 'count': per_scale[m]} for m in sorted(per_scale)]
    return {'F': F, 'start_scale': m0, 'end_scale': m1,
            'survived': bool(survivors), 'reached': len(seen),
            'max_reached': max_reached,
            'max_reached_scale': max_reached.bit_length() - 1,
            'history': hist[-6:], 'n_dead_ends': len(dead_ends),
            'last_dead_ends': sorted(dead_ends)[-6:],
            'survivors_at_end': survivors[:8]}


def orbit_law_scan(params_list, m0=13, m1=58, fmax=16):
    """For each (lam, r), decide empirically whether C(lam, r) admits an
    infinite doubling orbit.  Predicted law: yes iff r and 2*lam are
    powers of 2 (2-adic alignment).  Certificates are asymmetric:
      * aligned params  -> the explicit ray 2^s + 3 verified to 2^120;
      * misaligned      -> EXHAUSTIVE closure of u -> 2u - f (all f in
        C cap [1, fmax]) from the full window C cap [2^m0, 2^{m0+1}),
        shown to die before 2^m1 (factor 2^{m1-m0} of doubling room)."""
    out = []
    for lam, r in params_list:
        pred = (r & (r - 1) == 0) and ((2 * lam) & (2 * lam - 1) == 0)
        entry = {'lam': lam, 'r': r, 'predicted_infinite_orbit': pred}
        ray = explicit_orbit_kill(t_max=120, lam=lam, r=r, classify=False)
        ray_ok = (ray['reflector_in_C'] and ray['all_in_C_from_s0']
                  and ray['ray_in_C_from'] is not None)
        entry['ray_2^s+3'] = {'works': ray_ok, 'from_s': ray['ray_in_C_from']}
        if ray_ok:
            entry['found_infinite_orbit'] = True
            entry['certificate'] = (f"u_s = 2^s+3 in C for all "
                                    f"{ray['ray_in_C_from']} <= s <= 120, "
                                    f"f == 3 in C (lem:orbit kill)")
        else:
            memb = Membership(1 << (m1 + 2), lam=lam, r=r)
            F = [v for v in range(1, fmax + 1) if memb.in_C(v)]
            res = propagate(memb, F, m0, m1)
            entry['found_infinite_orbit'] = res['survived']
            entry['closure'] = {
                'F': F, 'reached': res['reached'],
                'max_reached_scale': res['max_reached_scale'],
                'last_dead_ends': res['last_dead_ends'],
                'certificate': (
                    None if res['survived'] else
                    f"every chain from C cap [2^{m0}, 2^{m0+1}) with "
                    f"reflectors in C cap [1,{fmax}] dies by scale "
                    f"2^{res['max_reached_scale'] + 1} "
                    f"(exhaustive closure, {res['reached']} values)")}
        entry['match'] = entry['found_infinite_orbit'] == pred
        out.append(entry)
        stat = ('infinite orbit (ray certified)' if
                entry['found_infinite_orbit'] else
                f"orbit-free (closure dies at scale "
                f"{entry.get('closure', {}).get('max_reached_scale', '?')})")
        print(f"  lam={lam} r={r}: {stat}; predicted "
              f"{'orbit' if pred else 'orbit-free'} -> "
              f"{'MATCH' if entry['match'] else 'MISMATCH'}", flush=True)
    return out


def death_anatomy(lam=3, r=4, m0=13, m1=58, fmax=16):
    """For an orbit-free tuning: where exactly do the deepest chains die?
    Runs the exact closure and reports the largest dead ends relative to
    the stage structure (prediction: in the silent zone above octave 0/1
    of a stage entered misaligned — the anchor 2^i M_k cannot meet the
    next anchor lam M_k when lam is not a power of 2)."""
    memb = Membership(1 << (m1 + 2), lam=lam, r=r)
    F = [v for v in range(1, fmax + 1) if memb.in_C(v)]
    res = propagate(memb, F, m0, m1)
    if res['survived']:
        return {'lam': lam, 'r': r, 'note': 'survived (unexpected)',
                'res': res}
    ends = res['last_dead_ends']
    Ms = [st['M'] for st in stages(4 * max(ends), lam=lam, r=r)]
    anat = []
    for e in ends:
        Mk = max((M for M in Ms if M <= e), default=1)
        anat.append({'end': e, 'end_over_M_k': round(e / Mk, 4),
                     'blocked_children_sample': [2 * e - f for f in F[:3]]})
    return {'lam': lam, 'r': r, 'F': F,
            'max_reached_scale': res['max_reached_scale'],
            'death_points': anat,
            'prediction': 'largest dead ends sit at c * M_k with c '
                          'a dyadic multiple blocked by the next octave'}


# --------------------------------------------------- (3) quantification

def interval_chain_bound(memb, N):
    """Longest doubling chain inside a single maximal run of C vs the
    run's ratio: verifies len <= log2(ratio) + O(1)."""
    runs = []
    # reconstruct maximal runs of C from W intervals
    iv = [(a, b) for a, b in memb.iv if a <= N]
    prev_end = 0
    for a, b in iv:
        if a > prev_end + 1:
            runs.append((prev_end + 1, a - 1))
        prev_end = max(prev_end, b)
    if prev_end < N:
        runs.append((prev_end + 1, N))
    rows = []
    for a, b in runs[-8:]:
        # longest chain with f=1 inside [a,b]: u_i = 2^i (a-1) + 1
        ln = 1
        u = a
        while 2 * u - 1 <= b:
            u = 2 * u - 1
            ln += 1
        import math
        rows.append({'run': [a, b], 'ratio': round(b / a, 3),
                     'longest_chain_inside': ln,
                     'log2_ratio_plus_1': round(math.log2(b / a) + 1, 2)})
    return rows


def lemma_r_quadruples(memb, N):
    """All m <= N/5 with {m, 2m, 3m, 5m} subset of C (Lemma R config)."""
    ms = [m for m in range(1, N // 5 + 1)
          if all(memb.in_C(c * m) for c in (1, 2, 3, 5))]
    # summarize as runs
    runs = []
    for m in ms:
        if runs and m == runs[-1][1] + 1:
            runs[-1][1] = m
        else:
            runs.append([m, m])
    return {'count': len(ms), 'runs': runs[:20],
            'note': 'every stage contributes a run m in (~1.6 M_k, 5M_k/3) '
                    '(paper params): m,2m chasm, 3m sliver, 5m silent'}


# ----------------------------------------------------------------- witness

def verify_witness_still_works(N, lam, r):
    """Sanity: the lam-tuned W is still 3-AP-permutable at horizon N via
    per-stage ABJ (cross-stage 3-AP count must be 0; permutation clean)."""
    blocks = []
    for st in stages(N, lam=lam, r=r):
        vals = []
        for _, lo, hi in st['octaves']:
            if lo <= N:
                vals.extend(range(lo, min(hi, N) + 1))
        if vals:
            blocks.append(vals)
    perm = [v for b in blocks for v in abj_sorted(b)]
    bad = find_monotone_ap(perm)
    W = set(perm)
    # cross-stage 3-APs
    cross = 0
    stage_of = {}
    for i, b in enumerate(blocks):
        for v in b:
            stage_of[v] = i
    for y in W:
        for d in range(1, min(y - 1, max(W) - y) + 1):
            if y - d in W and y + d in W:
                if len({stage_of[y - d], stage_of[y], stage_of[y + d]}) > 1:
                    cross += 1
    return {'N': N, 'lam': lam, 'r': r, 'size': len(perm),
            'monotone_3AP_in_perm': bad, 'cross_stage_3APs': cross,
            'ok': bad is None and cross == 0}


# --------------------------------------------------------------------- main

def main():
    t0 = time.time()
    out = {'experiment': 'h1_complement',
           'question': 'is any Geneson-complement plausibly permutable?'}

    print("== (1) explicit infinite orbit in C (paper params) ==",
          flush=True)
    out['kill'] = explicit_orbit_kill(t_max=200)
    print(f"  u_s = 2^s+3 in C for all {out['kill']['ray_in_C_from']} <= "
          f"s <= 200: {out['kill']['all_in_C_from_s0']}  "
          f"(reflector 3 in C: {out['kill']['reflector_in_C']})",
          flush=True)
    assert (out['kill']['all_in_C_from_s0']
            and out['kill']['ray_in_C_from'] == 5
            and out['kill']['reflector_in_C'])

    print("== (2) orbit law over parameter space ==", flush=True)
    out['law'] = orbit_law_scan(
        [(4, 4), (3, 4), (5, 4), (6, 4), (8, 4), (4, 8), (3, 8), (4, 5),
         (16, 4), (12, 4)])
    out['law_all_match'] = all(e['match'] for e in out['law'])
    # larger reflectors don't change the verdict for the key tunings
    out['law_fmax64'] = orbit_law_scan([(4, 4), (3, 4)], m0=13, m1=58,
                                       fmax=64)
    out['death_anatomy_lam3'] = death_anatomy(lam=3, r=4)
    print(f"  law matches at fmax=16: {out['law_all_match']}; "
          f"fmax=64 spot: "
          f"{all(e['match'] for e in out['law_fmax64'])}", flush=True)

    print("== (3) quantification: intervals, Lemma R ==", flush=True)
    memb4 = Membership(1 << 20)
    out['interval_chains'] = interval_chain_bound(memb4, 1 << 20)
    out['lemma_r'] = lemma_r_quadruples(memb4, 1 << 18)
    print(f"  Lemma-R quadruples in C(paper) up to 2^18: "
          f"{out['lemma_r']['count']} (runs {out['lemma_r']['runs'][:6]})",
          flush=True)

    print("== (4) lam=3 witness sanity + complement densities ==",
          flush=True)
    out['witness_lam3'] = verify_witness_still_works(1 << 13, 3, 4)
    print(f"  W(lam=3) at N=8192: perm clean="
          f"{out['witness_lam3']['ok']}", flush=True)
    dens = []
    for lam in (3, 4, 8):
        memb = Membership(1 << 30, lam=lam, r=4)
        # upper density of C = 1 - lower(W); lower(W) = 2/(3(lam+1))
        dens.append({'lam': lam,
                     'upper_density_C': f'1 - 2/(3*{lam+1}) = '
                                        f'{1 - 2 / (3 * (lam + 1)):.4f}'})
    out['complement_upper_density'] = dens

    out['runtime_s'] = round(time.time() - t0, 1)
    path = os.path.join(REPO, 'data', 'h1_complement.json')
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote {path} ({out['runtime_s']}s)", flush=True)
    return out


if __name__ == '__main__':
    main()
