# Spot-verify FRONT 83 (Q-g chart facts, mod-3 test case) + FRONT 86 (C3(p) identities)
# Independent reconstruction; fresh scales: t up to 17 (charts), p up to 47 (identities).
import sys

fails = []

def chk(name, cond):
    if not cond:
        fails.append(name)
        print("FAIL:", name)

# ---- 1. Q-g chart facts: phi_g maps class sections onto ratio-2 windows, <=1 dust/end
for g in (3, 5, 6, 7, 9, 12, 4, 8):
    for c in range(g):
        for t in range(6, 18):  # includes fresh t=13..17
            lam = [v for v in range(2**t + 1, 2**(t+1) + 1) if v % g == c % g]
            img = sorted((v - c) // g for v in lam)
            # contiguity
            chk(f"contig g={g} c={c} t={t}", img == list(range(img[0], img[-1] + 1)))
            lo, hi = img[0], img[-1]
            # ratio-2 window with <=1 dust each end: exists M with |lo-(M+1)|<=1, |hi-2M|<=1
            M = (2**t - c) // g
            ok = any(abs(lo - (Mv + 1)) <= 1 and abs(hi - 2 * Mv) <= 1 for Mv in (M - 1, M, M + 1))
            chk(f"window g={g} c={c} t={t}", ok)
            if g in (4, 8) and c == 0:
                k = 2 if g == 4 else 3
                chk(f"dyadic-exact g={g} t={t}",
                    lam[0] - 0 == 2**t + g and img[0] * g == 2**t + g and len(lam) == 2**(t - k))

# anchor residue cycles mod 8 (c=0 charts), M_t = floor(2^t/g)
seq3 = [((2**t) // 3) % 8 for t in range(6, 18)]
chk("anchor g=3 alternates 5,2", all(r in (5, 2) for r in seq3) and all(seq3[i] != seq3[i+1] for i in range(len(seq3)-1)))
seq5 = [((2**t) // 5) % 8 for t in range(6, 22)]
chk("anchor g=5 cycles 3,6,4,1", seq5[:4] in ([3,6,4,1],[6,4,1,3],[4,1,3,6],[1,3,6,4]) and all(seq5[i] == seq5[i+4] for i in range(len(seq5)-4)))
seq7 = [((2**t) // 7) % 8 for t in range(6, 22)]
chk("anchor g=7 cycles len3 {4,1,2}", sorted(set(seq7)) == [1,2,4] and all(seq7[i] == seq7[i+3] for i in range(len(seq7)-3)))
print("anchor seqs:", seq3, seq5[:8], seq7[:6])

# ---- 2. mod-3 lattice: HSPLIT-compatible (fresh t = 13, 14), minority gaps identically 3
for t in (6, 13, 14):
    B = range(2**t + 1, 2**(t+1) + 1)
    for mod in (4, 8, 16, 32):
        for c in range(mod):
            sec = [v for v in B if v % mod == c]
            has_min = any(v % 3 == 0 for v in sec)
            has_maj = any(v % 3 != 0 for v in sec)
            chk(f"mod3 bichrom t={t} mod={mod} c={c}", has_min and has_maj)
    mins = [v for v in B if v % 3 == 0]
    chk(f"mod3 gaps t={t}", all(b - a == 3 for a, b in zip(mins, mins[1:])))
# and mod-3 minority is closed under doubling (axis-(e) failure as claimed)
chk("3Z doubling-closed", all((2*v) % 3 == 0 for v in range(3, 300, 3)))

# ---- 3. C3(p) identities at fresh p (independent re-derivation; p beyond the p<=39 record)
for p in (5, 29, 31, 37, 41, 43, 47):
    # units
    A1 = (3*p - 2*p, p)        # t_p < b_p
    A2 = (3*p - 2*(p+1), p+1)  # t_{p-2} < b_{p+1}
    A3 = (3*p + 1 - 2*(p-2), p-2)
    chk(f"units p={p}", A1 == (p, p) and A2 == (p-2, p+1) and A3 == (p+5, p-2))
    chk(f"flipclass p={p}", (2*p + 6) % 4 == 0)
    for M in range(2*p + 6, 2*p + 6 + 8*20, 8):  # M in the flip class
        m0 = 3 * M // 2
        b = lambda j: M + j
        tt = lambda i: 2*M - i
        chk(f"M/2 cong p={p} M={M}", (M // 2) % 4 == (p + 3) % 4)
        chk(f"mod4 tp p={p} M={M}", tt(p) % 4 == (p + 2) % 4 and tt(p-2) % 4 == p % 4)
        chk(f"mod4 bp p={p} M={M}", b(p) % 4 == p % 4 and b(p-2) % 4 == (p + 2) % 4)
        chk(f"parity p={p} M={M}", tt(p+5) % 2 == 0 and b(p+1) % 2 == 0 and m0 % 2 == 0)
        chk(f"POLAR p={p} M={M}", 2*m0 - tt(p) == b(p))
        chk(f"flipmirr p={p} M={M}", b(p-2) + tt(p) == 3*M - 2 == 2*(m0 - 1) and b(p) + tt(p-2) == 3*M + 2 == 2*(m0 + 1))
    # Lemma E collision scales
    from sympy import symbols, Eq, solve
    Ms = symbols('M')
    chk(f"E coll p={p}", solve(Eq(Ms + p, 2*Ms - (p-2)), Ms) == [2*p - 2]
        and solve(Eq(Ms + p - 2, 2*Ms - p), Ms) == [2*p - 2]
        and solve(Eq(Ms + p - 2, 2*Ms - (p-2)), Ms) == [2*p - 4]
        and solve(Eq(Ms + p, 2*Ms - p), Ms) == [2*p])
    # the notes/86 slip: betweenness p-2 < M/2-1 < M-p  <=>  M > 2p-2  (NOT 2p+2)
    for M in range(2, 300, 2):
        left = (p - 2 < M/2 - 1)
        right = (M/2 - 1 < M - p)
        chk(f"slip p={p} M={M}", (left and right) == (M > 2*p - 2))
    # index gap parity
    for M in range(2*p + 2, 2*p + 60, 2):
        gap = (M - p + 1)//2 - (p - 1)//2
        chk(f"idxgap p={p} M={M}", gap % 2 == (M//2) % 2)

print("TOTAL FAILS:", len(fails))
sys.exit(0 if not fails else 1)
