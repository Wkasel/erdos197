"""Erdős #197 — e175: FRONT PUMP-SCHEMA (notes/75).

The 4-block downward gadget's uniform law.  Three parts:

CATALOGUE (pure counting, no solver):
  P1. 4-block AP pattern catalogue: over blocks Bm1/B0/B1/B2 of
      (M/2, 8M], exactly FOUR of the twenty nondecreasing block
      patterns are arithmetically empty: (-1,-1,1), (-1,-1,2),
      (-1,0,2), (0,0,2).  The three cross-window families are
      H_dn = (-1,0,1), H_up = (0,1,2), SKIP = (-1,1,2); exact counts
      verified against closed forms (the SKIP closed form is the
      13M^2/16 + M/2 law whose quarter is notes/62's schedule mass).
  P2. LEAK identity (the parametric '8'): for any coloring with
      Bm1∩T single-parity, mu_dn(T) = sum over leak values
      z in (B1∩T) of Bm1∩T's parity of #{u in Bm1∩T : (u+z)/2 in
      B0∩T}.  Verified against brute-force mu_dn on the recorded
      e158/e173 witnesses (C1@16 has leak {36,40,44,48}, count 8).
  P3. Band pigeonhole: balance at anchor 2m forces >= 16 / >= 15
      values of each team in CORE'(m)'s P1 / P2 bands (all m).
  P4. MUS-vs-CORE' anchors: the (16;6,0) MUS's B2 stub = bottom 6 of
      S3(16) = [4M+1, 4M+16]; its lower-window support sits inside
      CORE'(8)'s (degenerate) bands.

COLLAPSE (solver — the L-PROJ reduction made machine-explicit):
  C1. proj@32-bal: the 4-block instance at M=32 RESTRICTED to the
      lower window (16,128] with vdn=0 is exactly the balanced
      two-seam coupled core at anchor 16 — UNSAT (e120 reproduction
      through the e158 encoder).
  C2. full@32-bal (none,0): UNSAT — THE collapse cell.  By T-FORCE-4
      this is v_min(0)(32) = INFINITY (supersedes the >256 bracket).
  C3. proj@48-bal (support (24,192]): UNSAT (= bal@24 v=0 core).
  C4. proj@64-const (support (32,256], bounds 3,3,3): UNSAT
      (= the (3,3,3)@32 const core).
  C5. CORE'(48)@96: support = P0/P1/P2 bands of CI(48), bounds
      (2,2,2,0), vdn=0: UNSAT — the certified N6a engine reached
      through the 4-block encoder at a scale only CI covers.

PUMP-SMALL (solver — the finite regime, task-mandated 8/16/24):
  S1. (11,0)@8 UNSAT, (12,0)@8 SAT  (v_min(0)(8) = 12 exact).
  S2. (6,0)@16 UNSAT.
  S3. (65,0)@24 UNSAT.

Usage: e175_pump_schema.py {catalogue|collapse|small|all}
Artifacts: data/e175_pump.jsonl (streaming) + stdout log.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
JSONL = os.path.join(DATA, 'e175_pump.jsonl')
sys.path.insert(0, HERE)

from e158_joint4 import blocks_of, solve_joint, audit  # noqa: E402


def stream(row):
    row['ts'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    with open(JSONL, 'a') as f:
        f.write(json.dumps(row) + '\n')
    print(json.dumps(row), flush=True)


FAILURES = []


def check(name, ok, detail=''):
    tag = 'PASS' if ok else 'FAIL'
    if not ok:
        FAILURES.append((name, detail))
    print(f'  [{tag}] {name} {detail}', flush=True)
    return ok


# ---------------------------------------------------------------- catalogue

def blk_of(v, M):
    if v <= M:
        return -1
    if v <= 2 * M:
        return 0
    if v <= 4 * M:
        return 1
    return 2


def pattern_catalogue(M):
    """Enumerate every 3-AP of (M/2, 8M]; classify by block pattern."""
    lo, hi = M // 2 + 1, 8 * M
    pat = {}
    for b in range(lo, hi + 1):
        for d in range(1, min(b - lo, hi - b) + 1):
            a, c = b - d, b + d
            key = (blk_of(a, M), blk_of(b, M), blk_of(c, M))
            pat[key] = pat.get(key, 0) + 1
    return pat


def closed_forms(M):
    """Exact closed-form counts of the three cross-window families."""
    # H_up = (0,1,2): u in (M,2M], y in (2M,4M], z = 2y-u in (4M,8M].
    h_up = sum(2 * M - u // 2 for u in range(M + 1, 2 * M + 1))
    # H_dn = (-1,0,1): u in (M/2,M], y in (M,2M], z = 2y-u in (2M,4M].
    h_dn = sum(M - u // 2 for u in range(M // 2 + 1, M + 1))
    # SKIP = (-1,1,2): u in (M/2,M], y in (2M,4M], z = 2y-u in (4M,8M].
    skip = sum(2 * M - u // 2 for u in range(M // 2 + 1, M + 1))
    return h_up, h_dn, skip


def part_catalogue():
    print('== CATALOGUE ==', flush=True)
    # P1: pattern completeness + family counts
    allpats = [(i, j, k) for i in (-1, 0, 1, 2) for j in (-1, 0, 1, 2)
               for k in (-1, 0, 1, 2) if i <= j <= k]
    empty_pred = {(-1, -1, 1), (-1, -1, 2), (-1, 0, 2), (0, 0, 2)}
    for M in (16, 24, 32, 48, 64, 96):
        pat = pattern_catalogue(M)
        missing = {p for p in allpats if p not in pat}
        check(f'P1 empty-set M={M}', missing == empty_pred,
              f'missing={sorted(missing)}')
        h_up, h_dn, skip = closed_forms(M)
        check(f'P1 counts M={M}',
              pat[(0, 1, 2)] == h_up and pat[(-1, 0, 1)] == h_dn
              and pat[(-1, 1, 2)] == skip,
              f'H_up={pat[(0,1,2)]}=={h_up} H_dn={pat[(-1,0,1)]}=={h_dn} '
              f'SKIP={pat[(-1,1,2)]}=={skip}')
        # closed-closed forms (M ≡ 0 mod 4): H_up = 5M^2/4,
        # H_dn = 5M^2/16, SKIP = 13M^2/16
        if M % 4 == 0:
            check(f'P1 family-laws M={M}',
                  h_up == 5 * M * M // 4 and h_dn == 5 * M * M // 16
                  and skip == 13 * M * M // 16,
                  f'H_up={h_up}(5M^2/4={5*M*M//4}) '
                  f'H_dn={h_dn}(5M^2/16={5*M*M//16}) '
                  f'SKIP={skip}(13M^2/16={13*M*M//16})')
        stream({'part': 'P1', 'M': M, 'families':
                {'H_up': h_up, 'H_dn': h_dn, 'SKIP': skip},
                'n_patterns': len(pat)})

    # P2: LEAK identity on recorded witnesses
    def mu_families(colT, M):
        s = set(colT)
        _, (Bm1, B0, B1, B2) = blocks_of(M)
        bm1 = [v for v in colT if v in set(Bm1)]
        b0 = set(v for v in colT if v in set(B0))
        b1 = set(v for v in colT if v in set(B1))
        b2 = set(v for v in colT if v in set(B2))
        mu_dn = sum(1 for u in bm1 for y in b0
                    if 2 * y - u in b1)
        mu_up = sum(1 for u in b0 for y in b1 if 2 * y - u in b2)
        mu_sk = sum(1 for u in bm1 for y in b1 if 2 * y - u in b2)
        return mu_dn, mu_up, mu_sk, (bm1, b0, b1, b2)

    def leak_formula(bm1, b0, b1):
        pars = {u % 2 for u in bm1}
        if len(pars) != 1:
            return None
        p = pars.pop()
        L = sorted(z for z in b1 if z % 2 == p)
        total = sum(1 for z in L for u in bm1 if (u + z) // 2 in b0
                    and (u + z) % 2 == 0)
        return p, L, total

    recs = [('C1@16', 'e158_c1_M16_up6.json', 16),
            ('C2@16', 'e158_c2_M16_dn0.json', 16),
            ('C2@24', 'e158_c2_M24_dn0.json', 24),
            ('f384@16', 'e158_f_M16_up384_dn0.json', 16),
            ('pump12@8', 'e173_pump_M8_up12_dn0.json', 8)]
    for name, fn, M in recs:
        path = os.path.join(DATA, fn)
        if not os.path.exists(path):
            check(f'P2 {name} present', False, 'record missing')
            continue
        r = json.load(open(path))
        colA = r['colorA']
        V, _ = blocks_of(M)
        colB = [v for v in V if v not in set(colA)]
        out = {}
        for tn, col in (('A', colA), ('B', colB)):
            mu_dn, mu_up, mu_sk, (bm1, b0, b1, b2) = mu_families(col, M)
            rec_dn = r.get('anatomy', {}).get(tn, {}).get('n_H_dn')
            rec_up = r.get('anatomy', {}).get(tn, {}).get('n_H_up')
            if rec_dn is not None:
                check(f'P2 {name}/{tn} mu_dn==n_H_dn', mu_dn == rec_dn,
                      f'{mu_dn} vs {rec_dn}')
            if rec_up is not None:
                check(f'P2 {name}/{tn} mu_up==n_H_up', mu_up == rec_up,
                      f'{mu_up} vs {rec_up}')
            lf = leak_formula(bm1, b0, b1)
            if lf is not None:
                p, L, tot = lf
                check(f'P2 {name}/{tn} leak-identity', tot == mu_dn,
                      f'leak={L} sum={tot} vs mu_dn={mu_dn}')
                out[tn] = {'parity': p, 'leak': L, 'mu': [mu_dn, mu_up,
                                                          mu_sk]}
            else:
                out[tn] = {'parity': None, 'mu': [mu_dn, mu_up, mu_sk]}
        stream({'part': 'P2', 'witness': name, 'M': M, 'teams': out})

    # P3: band pigeonhole under balance at anchor 2m
    for m in range(16, 401, 16):
        p1_lo, p1_hi = 3 * m - 15, 4 * m
        p2_lo, p2_hi = 4 * m + 1, 6 * m + 15
        n_p1 = p1_hi - p1_lo + 1          # m + 16
        n_p2 = p2_hi - p2_lo + 1          # 2m + 15
        # blocks of CI(m): B1' = (2m,4m] size 2m, bal bound m;
        #                  B2' = (4m,8m] size 4m, bal bound 2m
        guar_p1 = m - (2 * m - n_p1)       # = 16
        guar_p2 = 2 * m - (4 * m - n_p2)   # = 15
        check(f'P3 pigeonhole m={m}', guar_p1 == 16 and guar_p2 == 15,
              f'P1>= {guar_p1}, P2>= {guar_p2}')
    stream({'part': 'P3', 'guarantee': {'P1': 16, 'P2': 15},
            'range': '16..400 step 16'})

    # P4: MUS stub vs S3(M) and CORE'(m) bands
    r = json.load(open(os.path.join(DATA, 'e158b_mus_M16_up6_dn0.json')))
    sup = set(r['necessary'])
    M = 16
    b2sup = sorted(v for v in sup if v > 4 * M)
    s3 = list(range(4 * M + 1, 4 * M + 17))
    check('P4 stub==bottom-6-of-S3', b2sup == s3[:6], f'{b2sup}')
    m = M // 2
    p2m = set(range(4 * m + 1, 6 * m + 16))        # [33, 63]
    b1sup = [v for v in sup if 2 * M < v <= 4 * M]
    check('P4 lower-support-in-CORE\'(8)-P2',
          all(v in p2m for v in b1sup),
          f'B1-support {b1sup[0]}..{b1sup[-1]}, P2(8)=[33,63], 64 absent='
          f'{64 not in sup}')
    stream({'part': 'P4', 'stub': b2sup, 'S3_16': [s3[0], s3[-1]],
            'B1_support_max': max(b1sup), 'P2m_hi': 6 * m + 15})


# ----------------------------------------------------------------- collapse

def run_cell(tag, M, abs_bounds, vup, vdn, support=None, expect=None):
    t0 = time.time()
    verdict, el, info = solve_joint(M=M, abs_bounds=abs_bounds, vup=vup,
                                    vdn=vdn, support=support)
    row = {'part': 'cell', 'tag': tag, 'M': M, 'bounds': abs_bounds,
           'vup': vup, 'vdn': vdn,
           'support': None if support is None else
           [min(support), max(support), len(support)],
           'verdict': verdict, 'time': el}
    if verdict == 'SAT' and support is None:
        errs, anat = audit(M, info['bounds'], vup, vdn, info)
        if errs:
            row['verdict'] = 'WITNESS-FAIL'
            row['errs'] = errs[:8]
        row['anatomy'] = {t: {k: a[k] for k in
                              ('sizes', 'n_s0', 'n_s1', 'n_s2', 'n_up',
                               'n_dn', 'n_H_up', 'n_H_dn')}
                          for t, a in anat.items()}
    ok = (expect is None) or (row['verdict'] == expect)
    check(tag, ok, f"{row['verdict']} [{el}s] expect={expect}")
    stream(row)
    return row


def part_collapse():
    print('== COLLAPSE (L-PROJ made machine-explicit) ==', flush=True)
    # C1: projected instance at M=32 == the balanced coupled core @16
    M = 32
    lower = list(range(M // 2 + 1, 4 * M + 1))
    run_cell('C1 proj@32-bal (support=(16,128], none,0)', M, None,
             None, 0, support=lower, expect='UNSAT')
    # C2: THE collapse cell — full 4-block, upper anchor unpriced
    run_cell('C2 full@32-bal (none,0)', 32, None, None, 0,
             expect='UNSAT')
    # C3: projected @48-bal == bal@24 core
    M = 48
    lower = list(range(M // 2 + 1, 4 * M + 1))
    run_cell('C3 proj@48-bal (support=(24,192], none,0)', M, None,
             None, 0, support=lower, expect='UNSAT')
    # C4: projected @64-const(3,3,3) == (3,3,3)@32 const core
    M = 64
    lower = list(range(M // 2 + 1, 4 * M + 1))
    run_cell('C4 proj@64-const333 (support=(32,256], none,0)', M,
             (3, 3, 3, 0), None, 0, support=lower, expect='UNSAT')
    # C5: CORE'(48) through the 4-block encoder at M=96
    m = 48
    core = (list(range(m + 1, 2 * m + 1))              # P0 = (48,96]
            + list(range(3 * m - 15, 4 * m + 1))       # P1 = [129,192]
            + list(range(4 * m + 1, 6 * m + 16)))      # P2 = [193,303]
    assert len(core) == 4 * m + 31
    run_cell('C5 CORE\'(48)@96 (bounds 2,2,2,0; none,0)', 2 * m,
             (2, 2, 2, 0), None, 0, support=core, expect='UNSAT')


def part_small():
    print('== PUMP-SMALL (the finite regime) ==', flush=True)
    run_cell('S1a (11,0)@8-bal', 8, None, 11, 0, expect='UNSAT')
    run_cell('S1b (12,0)@8-bal', 8, None, 12, 0, expect='SAT')
    run_cell('S2 (6,0)@16-bal', 16, None, 6, 0, expect='UNSAT')
    run_cell('S3 (65,0)@24-bal', 24, None, 65, 0, expect='UNSAT')


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    os.makedirs(DATA, exist_ok=True)
    if which in ('catalogue', 'all'):
        part_catalogue()
    if which in ('collapse', 'all'):
        part_collapse()
    if which in ('small', 'all'):
        part_small()
    print(f'== DONE: {len(FAILURES)} failures ==', flush=True)
    for name, det in FAILURES:
        print(f'  FAIL {name}: {det}', flush=True)
    stream({'part': 'summary', 'which': which,
            'failures': [n for n, _ in FAILURES]})
    sys.exit(1 if FAILURES else 0)


if __name__ == '__main__':
    main()
