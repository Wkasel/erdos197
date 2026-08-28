"""a8_bridge1_fresh: referee machine checks for notes/52 (BRIDGE1)
on TWO fresh adversarial colorings the author never tested, plus
extended arithmetic sweeps.  Encoding written fresh (no code shared
with experiments/e152_bridge1_check.py).

chiA (branch (a), greedy-low-puncture adversary): C0 = 2; in every
     block B(m) the dust is {3p, 3p'} for the TWO SMALLEST diagonal
     p in the block (the author's chi1 instead dusted core values of
     a single pair).  Step-1 extraction then lands on a FRESH p the
     machine layer never verified: at m0 = 5 the survivor is p = 21
     (pair {63, 64} — the j = 6 crown, a CROWN-2ADIC instance).
     Kills probe hypothesis (H1) at p = 21, outside the verified
     p <= 13 layer:
       R(63,64; 256, {267,279})   [chiA's actual B(8) dust]
       R(63,64; 128, {135,147})   [threshold probe, ratio 2 — record]
     Controls at 256: AP-only SAT, single-attacker-63 SAT.
chiA' (H1 robustness, adversarial D): same T but dust placed ON the
     C3(21) core values in B(8): D = {277, 278} (= b_21, b_22) and
     D = {491, 277} (= t_21, b_21).  Expect UNSAT both (the kill
     must reroute around the destroyed minimal core, as (H1)'s
     forall-D form demands).
chiB (branch (b), hi-half splitter): T' = {3p+1 : p = 1 mod 4} —
     the author's chi2 used lo halves {3p}; the hi-half version also
     exercises the crown claim (2^j = 3p_j + 1 in T' for even j).
     SPLIT-QUANT / B2-VAC exact counts at the fresh scales m = 9..12.

Plus: DIAG-DENSE brute m <= 22; CROWN-2ADIC j <= 30; LP(gamma)
brute to 4096; the 52-G2 corner-case exemplar (fan (11,15,19) lands
in T' of chi3).

Run: .venv/bin/python audit/a8_referee1/a8_bridge1_fresh.py
Log: data/a8_bridge1_fresh.log (caller tee).
"""
import time

from pysat.solvers import Cadical195


# ---------------------------------------------------------------- solver
def R_verdict(M, dust, attackers, with_aps=True):
    """Fresh encoding of R(attackers; M, dust) on S = (M,2M] - dust.
    Order var o[i][j] (i<j in S-index) True <=> S[i] before S[j]."""
    S = [v for v in range(M + 1, 2 * M + 1) if v not in dust]
    pos = {v: i for i, v in enumerate(S)}
    n = len(S)
    vid = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            vid[(i, j)] = c
    t0 = time.time()
    s = Cadical195()
    ncl = 0
    if with_aps:
        for y in S:
            d = 1
            while y - d > M and y + d <= 2 * M:
                u, z = y - d, y + d
                if u in pos and z in pos:
                    a = vid[(pos[u], pos[y])]
                    b = vid[(pos[y], pos[z])]
                    s.add_clause([-a, -b])   # not (u<y and y<z)
                    s.add_clause([a, b])     # not (z<y and y<u)
                    ncl += 2
                d += 1
    for a in attackers:
        for y in S:
            z = 2 * y - a
            if z > y and z in pos:
                s.add_clause([-vid[(pos[y], pos[z])]])   # z before y
                ncl += 1
    for i in range(n):
        for j in range(i + 1, n):
            vij = vid[(i, j)]
            for k in range(j + 1, n):
                s.add_clause([-vij, -vid[(j, k)], vid[(i, k)]])
                s.add_clause([vij, vid[(j, k)], -vid[(i, k)]])
                ncl += 2
    ok = s.solve()
    s.delete()
    return ('SAT' if ok else 'UNSAT'), n, ncl, time.time() - t0


def diag_ps_in_block(m):
    lo, hi = 2 ** m, 2 ** (m + 1)
    return [p for p in range(5, hi // 3 + 2, 2)
            if p % 4 == 1 and 3 * p > lo and 3 * p + 1 <= hi]


def main():
    # ---------------- part 1: DIAG-DENSE brute ----------------
    for m in range(4, 23):
        ps = diag_ps_in_block(m)
        vals = [w for p in ps for w in (3 * p, 3 * p + 1)]
        assert len(set(vals)) == 2 * len(ps)          # disjoint
        bound = (2 ** m - 13) / 12
        assert len(ps) >= bound, (m, len(ps), bound)
    print('P1: DIAG-DENSE brute m=4..22: count >= (2^m-13)/12, pairs '
          'disjoint  OK', flush=True)

    # ---------------- part 2: CROWN-2ADIC ----------------
    for j in range(4, 31, 2):
        assert (2 ** j - 1) % 3 == 0
        p = (2 ** j - 1) // 3
        assert p % 8 == 5 and p >= 5, (j, p)
    for j in range(3, 30, 2):
        assert (2 ** j - 1) % 8 == 7 and (2 ** j - 1) % 3 != 0, j
    print('P2: CROWN-2ADIC j<=30: even j => p_j = 5 mod 8; odd j => '
          '7 mod 8, 3 does not divide  OK', flush=True)

    # ---------------- part 3: chiA ----------------
    print('== chiA: greedy-low-puncture adversary, C0 = 2 ==', flush=True)
    dust = {m: set(3 * p for p in diag_ps_in_block(m)[:2])
            for m in range(4, 15)}
    for m in range(4, 15):
        assert len(dust[m]) <= 2, m                    # C0-clean
    surv = {}
    for m in range(5, 15):
        ps = diag_ps_in_block(m)
        alive = [p for p in ps
                 if 3 * p not in dust[m] and 3 * p + 1 not in dust[m]]
        assert alive, (m, 'extraction failed')
        surv[m] = alive[0]
    print(f'P3: chiA blocks 2-clean; extraction survivors '
          f'{[(m, surv[m]) for m in range(5, 10)]}', flush=True)
    assert surv[5] == 21 and 3 * 21 == 63
    print('P3: chiA survivor at m0=5 is p=21 -> pair {63,64} '
          '(fresh p, = crown j=6)', flush=True)

    D8 = sorted(dust[8])
    D7 = sorted(dust[7])
    print(f'P3: chiA window dust: B(7) {D7}, B(8) {D8}', flush=True)
    v, n, ncl, dt = R_verdict(256, set(D8), [], with_aps=True)
    print(f'P3: control AP-only     M=256 (n={n}, {ncl} cl): {v} '
          f'[{dt:.1f}s]', flush=True)
    assert v == 'SAT'
    v, n, ncl, dt = R_verdict(256, set(D8), [63])
    print(f'P3: control single-63   M=256 (n={n}, {ncl} cl): {v} '
          f'[{dt:.1f}s]', flush=True)
    assert v == 'SAT'
    v, n, ncl, dt = R_verdict(256, set(D8), [63, 64])
    print(f'P3: KILL R(63,64; 256, {D8}): {v} [{dt:.1f}s]  '
          f'(H1 at FRESH p=21, C=2)', flush=True)
    kill_256 = v
    v, n, ncl, dt = R_verdict(128, set(D7), [63, 64])
    print(f'P3: threshold probe R(63,64; 128, {D7}): {v} [{dt:.1f}s]  '
          f'(ratio 2 — record only)', flush=True)

    # ---------------- part 4: chiA' core-targeted dust ----------------
    print('== chiA\': dust ON the C3(21) minimal core at M=256 ==',
          flush=True)
    # core units of C3(p): t_p<b_p, t_{p-2}<b_{p+1}, t_{p+5}<b_{p-2};
    # values t_i = 2M - i, b_j = M + j.  p = 21, M = 256:
    core = {'t21': 512 - 21, 'b21': 256 + 21, 'b22': 256 + 22,
            't19': 512 - 19, 't26': 512 - 26, 'b19': 256 + 19}
    for D in ({core['b21'], core['b22']}, {core['t21'], core['b21']}):
        v, n, ncl, dt = R_verdict(256, D, [63, 64])
        print(f'P4: R(63,64; 256, {sorted(D)}): {v} [{dt:.1f}s]',
              flush=True)
        assert v == 'UNSAT', 'H1 robustness fails at p=21?!'

    # ---------------- part 5: chiB hi-half splitter ----------------
    print('== chiB: hi-half splitter T\' = {3p+1 : p=1 mod 4} ==',
          flush=True)
    tp = lambda v: v % 3 == 1 and ((v - 1) // 3) % 4 == 1 and v >= 16
    for m in range(9, 13):
        lo, hi = 2 ** m, 2 ** (m + 1)
        cnt = sum(1 for v in range(lo + 1, hi + 1) if tp(v))
        bound = (2 ** m - 13) / 12
        ps = diag_ps_in_block(m)
        meets = [p for p in ps if tp(3 * p) or tp(3 * p + 1)]
        owned_by_T = [p for p in ps if not tp(3 * p) and not tp(3 * p + 1)]
        assert cnt >= bound and meets == ps and not owned_by_T
        assert cnt > 8 and (hi - lo - cnt) > 8      # B2-VAC shape
        print(f'P5: m={m}: |B^T\'| = {cnt} >= {bound:.1f}; all {len(ps)} '
              f'diagonal pairs split; both dusts > 8  OK', flush=True)
    for j in range(4, 21, 2):
        assert tp(2 ** j), j       # 2^j = 3 p_j + 1, p_j = 1 mod 4
    print('P5: crown hi halves 2^j (even j <= 20) all in T\' '
          '(SPLIT-QUANT crown inheritance, hi side)  OK', flush=True)

    # ---------------- part 6: LP(gamma) to 4096 ----------------
    C = sorted({2 ** j - 1 for j in range(3, 13)}
               | {2 ** j for j in range(3, 13)} | {1})
    aps = [(u, y, z) for u in C for y in C for z in C
           if u < y < z and u + z == 2 * y]
    beta = [(1, 2 ** j, 2 ** (j + 1) - 1) for j in range(3, 12)]
    assert sorted(aps) == sorted(beta), aps
    print(f'P6: LP(gamma) brute to 4096: APs in crown-set u {{1}} = '
          f'beta family only ({len(aps)})  OK', flush=True)

    # ---------------- part 7: the 52-G2 corner case ----------------
    Tp = {11, 13, 15, 17, 19, 21} | {2 ** j - 1 for j in range(3, 13)}
    assert 11 + 19 == 2 * 15 and {11, 15, 19} <= Tp
    inaps = [(u, y, z) for u in sorted(Tp) for y in sorted(Tp)
             for z in sorted(Tp) if u < y < z and u + z == 2 * y]
    print(f'P7: 52-G2 exemplar: fan (11,15,19) lies ENTIRELY in chi3\'s '
          f'T\' (completion 19 is a planted lo half, NOT donated to T); '
          f'T\' contains {len(inaps)} 3-APs: {inaps}', flush=True)

    print(f'a8_bridge1_fresh: DONE (kill at 256 = {kill_256})', flush=True)


if __name__ == '__main__':
    main()
