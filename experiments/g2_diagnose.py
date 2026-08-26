"""Erdős #197 — G2: reusable death-diagnostic kit for candidate teams.

Given a finite truncation S ⊆ [1, N] of a candidate team (JSON file or a
named generator), run the four screens distilled from the S_A campaign:

  (i)   PURE-COMPLETE SAT at horizons H: linear order of S ∩ [1, H] with no
        monotone 3-AP among in-window triples (completions within S
        constrained, completions outside S free — exactly the e22/e39
        system, which is the restriction of the infinite problem).
        THEOREM (soundness ceiling): the pure-complete window is ALWAYS
        satisfiable — the Ardal–Brown–Jungić binary (bit-reversal) order on
        Z has no monotone 3-AP at all (Geneson 2026, Lemma 2.2), and its
        restriction to the window satisfies every clause.  So (i) is a
        consistency check and witness generator, never a death certificate
        by itself; finite-horizon death needs extra structure (caps, chunk
        stages, OG attacks).  That is what (ii)–(iv) screen for.  Default
        mode: ABJ witness + independent verification (instant).  --solver
        cross-checks with CDCL (lazy transitivity, Cadical195; inlined
        below as pure_complete_sat).
  (ii)  ORBIT SCAN (paper lem:orbit): longest in-team doubling chains
        u -> 2u - f with reflectors f in a small fixed F ⊆ S (default
        F = S ∩ [1, orbit-fmax]).  A permutable team admits NO infinite
        such orbit; a chain that spans many octaves and dies only because
        it hits the horizon (censored) is a candidate infinite orbit —
        an instant death certificate if it persists.  Reports the longest
        full-F, single-f and two-reflector {f, g} chains.
  (iii) CROWN SCAN: small in-team values x whose attack pairs (x, y) —
        y in-team, completion z = 2y - x in-team — recur at every occupied
        scale.  Once x sits at a fixed position of a permutation, all but
        finitely many attacked pairs force z ≺ y (thm:ogred's pigeonhole);
        attackers whose attacks recur at every scale are 15/16-analogues.
        Reports per-attacker recurrence ratio over occupied octaves above
        it, attack counts, attacked bottom offsets, and the recurring
        crown pairs {2^t - 1, 2^t}.
  (iv)  SLIVER LOAD: per occupied octave (2^{t-1}, 2^t], the fraction of
        the bottom w values (the attack surface, default w = 8 = matched
        to crowns 15/16) that is in-team.  Persistent load ~1 at large
        scales is the S_A death pattern; Geneson's construction removes
        exactly these slivers.

Self-contained: the Geneson witness (arXiv:2608.12604 eqs (3.3)-(3.5),
paper values M0=1, L_k = 4 M_{k-1}, ratio 4, J(k) = k), the ABJ
bit-reversal order, and the pure-complete CDCL are all inlined so this
tool has no dependency on the (independently evolving) G1 generator.
gen_geneson is cross-checked setwise against g1_geneson_gen's witness.

Calibration (this file's __main__, records in data/g2_*.json):
  --gen sa       -> CROWN flag: 15 and 16 (and every head pair
                    {2^t-1, 2^t}) attack with recurrence ratio 1.0 at ALL
                    occupied octaves; SLIVER load 1.0 everywhere; orbits
                    short (S_A breaks doubling orbits in two steps);
                    pure-complete SAT.
  --gen geneson  -> CLEAN: no recurring attacker, sliver load 0 at every
                    large scale, orbits short, SAT.
  --gen zplus    -> ORBIT flag fires (DEGS): full-span censored chain.

Usage:
  .venv/bin/python experiments/g2_diagnose.py --gen sa
  .venv/bin/python experiments/g2_diagnose.py --set myteam.json --name X
Options: --N, --sat-horizons 256,1024,4096, --solver, --solver-max,
  --orbit-fmax, --attacker-max, --sliver-width, --occ-thresh, --json PATH.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def octave(v):
    """t such that v in (2^{t-1}, 2^t] (v >= 2); octave(1) = 0."""
    return (v - 1).bit_length()


# ------------------------------------------- ABJ (bit-reversal) order

def abj_key(v, t):
    """Rank of v in the Ardal-Brown-Jungic order restricted to [0, 2^t):
    the bit-reversal of v's t-bit binary expansion.  (u < v in ABJ iff
    bit_{nu2(v-u)}(u) = 0, which is exactly bit-reversed comparison.)"""
    r = 0
    for _ in range(t):
        r = (r << 1) | (v & 1)
        v >>= 1
    return r


def abj_sorted(vals):
    t = max(vals).bit_length() + 1  # ensure 2^t > max
    return sorted(vals, key=lambda v: abj_key(v, t))


# ------------------------------------- Geneson witness (paper-exact)

def geneson_blocks(N, M0=1, Lmult=4, ratio=4):
    """Octave-blocks [L r^j + M_{k-1}, 2 L r^j] of Geneson's stage
    construction (arXiv:2608.12604 eqs (3.3)-(3.5), J(k) = k),
    truncated to [1, N], in stage order."""
    assert M0 >= 1 and Lmult >= 3 and ratio >= 4
    out, M_prev, k = [], M0, 0
    while True:
        k += 1
        L = Lmult * M_prev            # Lemma 3.1 needs L > 2 M_{k-1}
        if L + M_prev > N:
            return out
        for j in range(k + 1):
            lo = L * ratio ** j + M_prev
            if lo > N:
                break
            out.append((k, lo, min(2 * L * ratio ** j, N)))
        M_prev = 2 * L * ratio ** k   # M_k


def geneson_witness(N):
    """Sorted W cap [1, N] (upper density -> 2/3 along n = M_k)."""
    return [v for _, lo, hi in geneson_blocks(N) for v in range(lo, hi + 1)]


# --------------------------------- pure-complete CDCL (e22/e39 style)

def pure_complete_sat(V, hint=None, max_rounds=4000, verbose=False):
    """Decide the pure-complete system on the finite set V: a linear order
    with no monotone 3-AP among in-set triples (both directions).  Lazy
    transitivity via win-sorted tournament; optional phase hint order.
    Returns a satisfying sequence, or False (UNSAT)."""
    from pysat.solvers import Cadical195
    V = sorted(V)
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off = [0] * n
    for i in range(1, n):
        off[i] = off[i - 1] + (n - i)
    top = n * (n - 1) // 2

    def var(i, j):        # i < j
        return 1 + off[i] + (j - i - 1)

    def before(u, w):
        i, j = idx[u], idx[w]
        return var(i, j) if i < j else -var(j, i)

    Vs = set(V)
    hi = V[-1]
    cl = []
    for y in V:
        for d in range(1, min(y - 1, hi - y) + 1):
            x, z = y - d, y + d
            if x in Vs and z in Vs:
                cl.append([-before(x, y), -before(y, z)])
                cl.append([-before(z, y), -before(y, x)])
    if verbose:
        print(f"  pure-complete: n={n} vars={top} clauses={len(cl)}",
              flush=True)
    s = Cadical195(bootstrap_with=cl)
    if hint is not None:
        hp = [0] * n
        for p, v in enumerate(hint):
            hp[idx[v]] = p
        phases = []
        for i in range(n):
            for j in range(i + 1, n):
                phases.append(var(i, j) if hp[i] < hp[j] else -var(i, j))
        s.set_phases(phases)
    t0 = time.time()
    rounds = 0
    while True:
        rounds += 1
        if rounds > max_rounds:
            raise RuntimeError("transitivity rounds exhausted")
        if not s.solve():
            return False
        model = s.get_model()
        pos = np.zeros(top + 1, dtype=bool)
        for l in model:
            if 0 < l <= top:
                pos[l] = True
        B = np.zeros((n, n), dtype=bool)
        for i in range(n - 1):
            row = pos[var(i, i + 1): var(i, n - 1) + 1]
            B[i, i + 1:] = row
            B[i + 1:, i] = ~row
        wins = B.sum(axis=1)
        order = np.argsort(-wins, kind='stable')
        R = B[np.ix_(order, order)]
        iu = np.triu_indices(n, 1)
        bad = np.nonzero(~R[iu])[0]
        if len(bad) == 0:
            if verbose:
                print(f"  SAT in {rounds} round(s) ({time.time()-t0:.1f}s)",
                      flush=True)
            return [V[int(i)] for i in order]
        added = 0
        for bi in bad[:30000]:
            a_, b_ = int(iu[0][bi]), int(iu[1][bi])
            i, j = int(order[a_]), int(order[b_])
            ks = np.nonzero(B[i] & B[:, j])[0]
            if len(ks):
                k = int(ks[0])
                s.add_clause([-before(V[i], V[k]), -before(V[k], V[j]),
                              before(V[i], V[j])])
                added += 1
        if verbose and rounds % 10 == 0:
            print(f"  round {rounds}: {len(bad)} viol "
                  f"({time.time()-t0:.0f}s)", flush=True)


# ------------------------------------------------------------- generators

def gen_sa(N):
    """Canonical dyadic candidate: union of even blocks (2^{k-1}, 2^k]."""
    return [v for v in range(2, N + 1) if (v - 1).bit_length() % 2 == 0]


def gen_sb(N):
    """Complement of S_A: {1} + odd blocks."""
    return [v for v in range(1, N + 1)
            if v == 1 or (v - 1).bit_length() % 2 == 1]


def gen_zplus(N):
    """All of [1, N] (DEGS control: must be flagged dead)."""
    return list(range(1, N + 1))


def gen_geneson(N):
    """Geneson 2026 Thm 1.1 witness W (paper-exact, inlined above)."""
    return geneson_witness(N)


def gen_geneson_c(N):
    """[1, N] \\ W — the complement a YES-partition would have to permute."""
    W = set(geneson_witness(N))
    return [v for v in range(1, N + 1) if v not in W]


GENERATORS = {'sa': gen_sa, 'sb': gen_sb, 'zplus': gen_zplus,
              'geneson': gen_geneson, 'geneson_c': gen_geneson_c}


def load_set(args):
    if args.gen:
        S = GENERATORS[args.gen](args.N)
        return sorted(set(S)), args.gen
    with open(args.set) as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        data = data.get('S') or data.get('set') or data.get('W')
    S = sorted(set(int(v) for v in data))
    if not S or S[0] < 1:
        raise SystemExit("set must be positive integers")
    if args.N:
        S = [v for v in S if v <= args.N]
    name = args.name or os.path.splitext(os.path.basename(args.set))[0]
    return S, name


# --------------------------------------------------- (i) pure-complete SAT

def find_monotone_ap(seq):
    """First monotone 3-AP in the sequence, or None (independent verifier)."""
    pos = {v: i for i, v in enumerate(seq)}
    vals = set(seq)
    hi = max(seq)
    for y in seq:
        for d in range(1, min(y - 1, hi - y) + 1):
            x, z = y - d, y + d
            if x in vals and z in vals:
                if pos[x] < pos[y] < pos[z] or pos[x] > pos[y] > pos[z]:
                    return (x, y, z)
    return None


def sat_diagnostic(S, horizons, use_solver, solver_max):
    out = []
    for H in horizons:
        V = [v for v in S if v <= H]
        if len(V) < 3:
            out.append({'H': H, 'n': len(V), 'result': 'TRIVIAL'})
            continue
        t0 = time.time()
        entry = {'H': H, 'n': len(V)}
        seq = abj_sorted(V)
        bad = find_monotone_ap(seq)
        if bad is None:
            entry.update(result='SAT', method='abj-witness',
                         witness_verified=True)
        else:                       # cannot happen for pure windows; be safe
            entry.update(result='WITNESS-FAIL', method='abj-witness',
                         counterexample=list(bad))
        if use_solver or bad is not None:
            if len(V) <= solver_max:
                res = pure_complete_sat(V, hint=seq if bad is None else None,
                                        verbose=False)
                if res is False:
                    entry.update(result='UNSAT', method='cadical-lazy-trans')
                else:
                    ver = find_monotone_ap(res)
                    entry.update(result='SAT', method='cadical-lazy-trans',
                                 witness_verified=ver is None)
                    if ver is not None:
                        entry['result'] = 'SOLVER-WITNESS-FAIL'
            else:
                entry['solver'] = f'skipped (n={len(V)} > {solver_max})'
        entry['time'] = round(time.time() - t0, 2)
        out.append(entry)
    return out


# ------------------------------------------------------- (ii) orbit scan

def _longest_chain(Sarr, F, N):
    """Longest in-team chain u -> 2u - f (f in F, strictly increasing).
    Exact DP (values strictly increase => acyclic), vectorised rounds."""
    n = len(Sarr)
    succ = []                      # per f: (valid mask, successor index)
    for f in F:
        t = 2 * Sarr - f
        j = np.searchsorted(Sarr, t)
        ok = (j < n)
        jj = np.where(ok, j, 0)
        ok &= (Sarr[jj] == t) & (t > Sarr)
        succ.append((ok, jj))
    L = np.ones(n, dtype=np.int64)
    for _ in range(4 * int(Sarr[-1]).bit_length() + 64):
        best = L.copy()
        for ok, jj in succ:
            cand = np.where(ok, L[jj] + 1, 1)
            np.maximum(best, cand, out=best)
        if np.array_equal(best, L):
            break
        L = best
    i = int(np.argmax(L))
    chain, fs = [int(Sarr[i])], []
    while True:
        nxt = None
        for f, (ok, jj) in zip(F, succ):
            if ok[i] and L[jj[i]] == L[i] - 1:
                nxt = (int(jj[i]), f)
                break
        if nxt is None:
            break
        i = nxt[0]
        fs.append(nxt[1])
        chain.append(int(Sarr[i]))
    end = chain[-1]
    # Censored = continuation cannot be ruled out at this horizon: SOME
    # successor 2*end - f lies beyond N.  (The old max(F) test demanded
    # ALL successors exceed N and missed infinite orbits whose large-f
    # successor lands in-window but out-of-team while the small-f
    # successor — the one the true orbit uses — is beyond the horizon;
    # H2 found exactly this on the sliver-swap teams.)
    censored = bool(2 * end - min(F) > N)
    return {'len': len(chain), 'F': [int(f) for f in F],
            'span_octaves': octave(end) - octave(chain[0]),
            'start': chain[0], 'end': end, 'censored': censored,
            'chain': chain[:48], 'reflectors': fs[:47]}


def orbit_scan(S, N, fmax, span_flag=6):
    Sarr = np.asarray(S, dtype=np.int64)
    F = [v for v in S if v <= fmax]
    res = {'fmax': fmax, 'F_size': len(F)}
    if not F:
        res.update(note='no reflectors <= fmax in team', flag=False)
        return res
    full = _longest_chain(Sarr, F, N)
    singles = sorted((_longest_chain(Sarr, [f], N) for f in F),
                     key=lambda r: (-r['len'], -r['span_octaves']))
    top_f = [r['F'][0] for r in singles[:8]]
    pairs = []
    for a in range(len(top_f)):
        for b in range(a + 1, len(top_f)):
            pairs.append(_longest_chain(Sarr, sorted((top_f[a], top_f[b])), N))
    pairs.sort(key=lambda r: (-r['len'], -r['span_octaves']))
    res['full_F'] = full
    res['top_single'] = singles[:5]
    res['top_pair'] = pairs[:5]
    best = max([full] + pairs[:1] + singles[:1],
               key=lambda r: (r['span_octaves'], r['len']))
    res['flag'] = bool(best['span_octaves'] >= span_flag and best['censored'])
    res['flag_reason'] = (
        f"censored chain of span {best['span_octaves']} octaves "
        f"(len {best['len']}, F={best['F']}) still alive at horizon — "
        f"candidate infinite orbit (lem:orbit death if it persists)"
        if res['flag'] else 'no long censored doubling chain')
    return res


# ---------------------------------------------------------- scale blocks

def occupied_octaves(S, N, occ_thresh):
    """Occupied octaves (2^{t-1}, 2^t] fully inside the horizon."""
    Sarr = np.asarray(S, dtype=np.int64)
    out = []
    t = 1
    while (1 << t) <= N:
        lo, hi = 1 << (t - 1), 1 << t
        a, b = np.searchsorted(Sarr, [lo + 1, hi + 1])
        cnt = int(b - a)
        dens = cnt / lo
        if dens >= occ_thresh:
            out.append({'t': t, 'lo': lo, 'hi': hi, 'count': cnt,
                        'density': round(dens, 4), 'slice': (int(a), int(b))})
        t += 1
    return out


# --------------------------------------------------------- (iii) crowns

def crown_scan(S, N, attacker_max, occ_thresh,
               ratio_flag=0.9, min_octaves=3):
    Sarr = np.asarray(S, dtype=np.int64)
    octs = occupied_octaves(S, N, occ_thresh)
    attackers = [v for v in S if v <= attacker_max]
    rows = []
    for x in attackers:
        above = [o for o in octs if o['lo'] >= x]
        if not above:
            continue
        hit_octs, counts, offsets = 0, [], []
        for o in above:
            y = Sarr[o['slice'][0]:o['slice'][1]]
            z = 2 * y - x
            j = np.searchsorted(Sarr, z)
            ok = (j < len(Sarr))
            jj = np.where(ok, j, 0)
            ok &= Sarr[jj] == z
            c = int(ok.sum())
            counts.append(c)
            if c:
                hit_octs += 1
                offs = (y[ok] - o['lo'])
                offsets.append((o['t'], int(offs.min()), int(offs.max())))
        ratio = hit_octs / len(above)
        rows.append({'x': x, 'octaves_above': len(above),
                     'octaves_attacked': hit_octs,
                     'recurrence_ratio': round(ratio, 3),
                     'attacks_per_octave': counts,
                     'mean_attacks': round(sum(counts) / len(counts), 2),
                     'attacked_offsets': offsets[:12]})
    rows.sort(key=lambda r: (-r['recurrence_ratio'], -r['mean_attacks']))
    recurring = [r for r in rows
                 if r['recurrence_ratio'] >= ratio_flag
                 and r['octaves_attacked'] >= min_octaves]
    rec_x = {r['x'] for r in recurring}
    crown_pairs = [[(1 << t) - 1, 1 << t]
                   for t in range(2, octave(N) + 1)
                   if ((1 << t) - 1) in rec_x and (1 << t) in rec_x]
    pair_members = {v for p in crown_pairs for v in p}
    return {'attacker_max': attacker_max,
            'crown_pair_rows': [r for r in rows if r['x'] in pair_members],
            'occupied_octaves': [o['t'] for o in octs],
            'attackers_tested': len(rows),
            'top': rows[:12],
            'recurring_attackers': [r['x'] for r in recurring],
            'crown_pairs': crown_pairs,
            'flag': bool(recurring),
            'flag_reason': (
                f"attackers {[r['x'] for r in recurring][:12]} attack "
                f">= {int(100*ratio_flag)}% of occupied octaves above them "
                f"(15/16-analogues: crown pairs {crown_pairs})"
                if recurring else 'no attacker recurs across scales')}


# ------------------------------------------------------ (iv) sliver load

def sliver_scan(S, N, width, occ_thresh, load_flag=0.5):
    Sarr = np.asarray(S, dtype=np.int64)
    octs = occupied_octaves(S, N, occ_thresh)
    rows = []
    for o in octs:
        w = min(width, o['lo'])
        a, b = np.searchsorted(Sarr, [o['lo'] + 1, o['lo'] + w + 1])
        rows.append({'t': o['t'], 'block': [o['lo'] + 1, o['hi']],
                     'density': o['density'], 'sliver_width': int(w),
                     'sliver_load': round(int(b - a) / w, 3)})
    if rows:
        half = rows[len(rows) // 2:]
        top_mean = sum(r['sliver_load'] for r in half) / len(half)
    else:
        half, top_mean = [], 0.0
    flag = bool(rows and top_mean >= load_flag)
    return {'width': width, 'per_octave': rows,
            'large_scale_mean_load': round(top_mean, 3),
            'flag': flag,
            'flag_reason': (
                f"mean bottom-sliver load {top_mean:.2f} over the largest "
                f"{len(half)} occupied octaves (S_A death pattern: load 1.0)"
                if flag else 'slivers unloaded at large scales')}


# ------------------------------------------------------------------ main

def diagnose(S, name, args):
    N = max(S) if not args.N else args.N
    report = {'name': name, 'N': N, 'size': len(S),
              'min': S[0], 'max': S[-1],
              'params': {'sat_horizons': args.sat_horizons,
                         'solver': args.solver,
                         'orbit_fmax': args.orbit_fmax,
                         'attacker_max': args.attacker_max,
                         'sliver_width': args.sliver_width,
                         'occ_thresh': args.occ_thresh},
              'note': ('pure-complete windows are always SAT (ABJ order); '
                       '(i) is a consistency check, death signals are '
                       '(ii)-(iv) + UNSAT only under extra structure')}

    horizons = [h for h in args.sat_horizons if h <= N]
    print(f"== {name}: |S|={len(S)} on [1,{N}] ==", flush=True)

    print("(i) pure-complete SAT:", flush=True)
    report['sat'] = sat_diagnostic(S, horizons, args.solver, args.solver_max)
    for e in report['sat']:
        print(f"    H={e['H']:>6} n={e['n']:>5} -> {e['result']}"
              f" [{e.get('method', '-')}, {e.get('time', 0)}s]", flush=True)

    print("(ii) orbit scan:", flush=True)
    report['orbit'] = orbit_scan(S, N, args.orbit_fmax)
    ob = report['orbit']
    if 'full_F' in ob:
        f = ob['full_F']
        print(f"    full F (|F|={ob['F_size']}): len={f['len']} "
              f"span={f['span_octaves']} oct "
              f"[{f['start']}..{f['end']}] censored={f['censored']}",
              flush=True)
        s = ob['top_single'][0]
        print(f"    best single f={s['F'][0]}: len={s['len']} "
              f"span={s['span_octaves']}", flush=True)
        if ob['top_pair']:
            p = ob['top_pair'][0]
            print(f"    best pair F={p['F']}: len={p['len']} "
                  f"span={p['span_octaves']}", flush=True)
    print(f"    -> flag={ob['flag']}: {ob['flag_reason']}", flush=True)

    print("(iii) crown scan:", flush=True)
    report['crowns'] = crown_scan(S, N, args.attacker_max, args.occ_thresh)
    cr = report['crowns']
    for r in cr['top'][:6]:
        print(f"    x={r['x']:>4}: ratio={r['recurrence_ratio']:.2f} "
              f"({r['octaves_attacked']}/{r['octaves_above']} octaves) "
              f"mean_attacks={r['mean_attacks']}", flush=True)
    print(f"    -> flag={cr['flag']}: {cr['flag_reason']}", flush=True)

    print("(iv) sliver load:", flush=True)
    report['sliver'] = sliver_scan(S, N, args.sliver_width, args.occ_thresh)
    sl = report['sliver']
    loads = ' '.join(f"t{r['t']}:{r['sliver_load']:.2f}"
                     for r in sl['per_octave'])
    print(f"    {loads}", flush=True)
    print(f"    -> flag={sl['flag']}: {sl['flag_reason']}", flush=True)

    flags = []
    if any(e.get('result') == 'UNSAT' for e in report['sat']):
        flags.append('UNSAT')          # definitive finite death certificate
    if ob['flag']:
        flags.append('ORBIT')
    if cr['flag']:
        flags.append('CROWN')
    if sl['flag']:
        flags.append('SLIVER')
    if 'UNSAT' in flags:
        verdict = 'DEAD (finite pure-complete UNSAT — hard certificate)'
    elif flags:
        verdict = f"FLAGGED [{', '.join(flags)}] — S_A-style death pattern"
    else:
        verdict = f'CLEAN at N={N} (no death pattern detected)'
    report['flags'] = flags
    report['verdict'] = verdict
    print(f"VERDICT: {verdict}\n", flush=True)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument('--gen', choices=sorted(GENERATORS))
    src.add_argument('--set', help='JSON file: list of ints (or {"S": [...]})')
    ap.add_argument('--name', help='label for file input')
    ap.add_argument('--N', type=int, default=None,
                    help='horizon (default 2^18 for generators, max(S) '
                         'for files)')
    ap.add_argument('--sat-horizons', default='256,1024,4096',
                    type=lambda s: [int(x) for x in s.split(',') if x])
    ap.add_argument('--solver', action='store_true',
                    help='CDCL cross-check instead of ABJ-witness only')
    ap.add_argument('--solver-max', type=int, default=1500,
                    help='max window size for CDCL mode')
    ap.add_argument('--orbit-fmax', type=int, default=16)
    ap.add_argument('--attacker-max', type=int, default=64)
    ap.add_argument('--sliver-width', type=int, default=8)
    ap.add_argument('--occ-thresh', type=float, default=0.25)
    ap.add_argument('--json', default=None,
                    help="output path (default data/g2_<name>.json; '' skips)")
    args = ap.parse_args()
    if args.gen and args.N is None:
        args.N = 1 << 18

    S, name = load_set(args)
    if len(S) < 3:
        raise SystemExit('set too small')
    report = diagnose(S, name, args)

    path = args.json
    if path is None:
        path = os.path.join(REPO, 'data', f'g2_{name}.json')
    if path:
        with open(path, 'w') as fh:
            json.dump(report, fh, indent=1)
        print(f"saved {path}", flush=True)


if __name__ == '__main__':
    main()
