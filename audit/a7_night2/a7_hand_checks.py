#!/usr/bin/env python3
"""a7 night-2 audit: independent pure-python reconstruction checks.

No SAT solver is used anywhere in this file (the shared solver slot is
occupied by the e146 catalogue build).  Every check is a from-scratch
reimplementation from the LEMMA STATEMENTS in notes/52/57/58/59 —
no code is imported from experiments/.

Sections:
  A  Lemma FI (notes/57 §2.1) brute-force formula audit at M = 112, 144
  B  Lemma D3 (notes/58 §2.2) full-range inequality audit at M = 48, 144
  C  Lemma PH+ (notes/58 §4.1) class-count arithmetic at 6 scales
  D  the K* mechanistic formula vs the six measured thresholds
  E  independent T/RL/RT closure engine: all 36 Lemma-J minimal sets
     (29 pure closure + 7 with the logged totality splits), and the
     JP/JP' instance enumeration = exactly the nine 6-fact pairs
  F  Gamma1 / Gamma2' / S6 affine algebra identities over full sweeps
  G  BRIDGE1 arithmetic: DIAG-DENSE counts, CROWN-2ADIC residues
"""
import sys, json

ok_all = True
def report(tag, ok, detail=""):
    global ok_all
    ok_all = ok_all and ok
    print(f"{'OK ' if ok else 'FAIL'} {tag}" + (f"  {detail}" if detail else ""))

# ---------------------------------------------------------------- A
def check_FI(M):
    m = M // 2
    P0 = range(M+1, 2*M+1); P1 = range(3*M-15, 4*M+1)
    bad = []
    for eps, cname in ((1, 'O'), (0, 'E')):
        cls0 = [u for u in P0 if u % 2 == eps]
        umin, umax = min(cls0), max(cls0)
        for s in range(1, 2*M+16):
            z = 4*M + s
            if z % 2 != eps: continue
            I = sorted((u+z)//2 for u in cls0 if 3*M-15 <= (u+z)//2 <= 4*M)
            if not I: bad.append((cname, s, 'empty')); continue
            # interval of consecutive integers
            if I != list(range(I[0], I[-1]+1)): bad.append((cname, s, 'notint')); continue
            ell = len(I)
            nc = sum(1 for v in I if v % 2 == eps)
            # formula checks
            lo_ok = (s <= M-31)
            if lo_ok:
                if I[0] != 3*M-15: bad.append((cname, s, 'anchor')); continue
                ell_f = (s+31)//2 if eps == 1 else (s+32)//2
                if ell != ell_f: bad.append((cname, s, 'ell')); continue
                if nc < 8: bad.append((cname, s, 'nc<8')); continue
                if nc == 8 and not (s in (1, 2)): bad.append((cname, s, 'nc=8')); continue
            else:
                if I[0] == 3*M-15 and s <= 2*M: bad.append((cname, s, 'anchor-high'))
                if s <= 2*M:
                    if ell != m: bad.append((cname, s, 'mid-ell')); continue
                    if nc < m//2: bad.append((cname, s, 'mid-nc')); continue
                else:
                    if ell < m-8: bad.append((cname, s, 'tail-ell')); continue
                    if nc < 8: bad.append((cname, s, 'tail-nc<8')); continue
                    if nc == 8 and s != 2*M+15: bad.append((cname, s, 'tail-nc=8')); continue
        # FI(iv) two-element sets: f_c(D) >= 9
        zs = [4*M+s for s in range(1, 2*M+16) if (4*M+s) % 2 == eps]
        Imap = {z: set((u+z)//2 for u in cls0 if 3*M-15 <= (u+z)//2 <= 4*M) for z in zs}
        for i in range(len(zs)):
            for jj in range(i+1, len(zs)):
                F = Imap[zs[i]] | Imap[zs[jj]]
                fc = sum(1 for v in F if v % 2 == eps)
                if fc < 9:
                    bad.append((cname, zs[i]-4*M, zs[jj]-4*M, 'pair f<9'))
    report(f"A FI(M={M})", not bad, str(bad[:5]))

# ---------------------------------------------------------------- B
def check_D3(M):
    y0 = (7*M+16)//2
    MID = range(3*M-14, (7*M+14)//2 + 1)
    P1 = range(3*M-15, 4*M+1); P2 = range(4*M+1, 6*M+16)
    bad = []
    # step-1 characterization
    for y in P1:
        PW = set(range(2*y-2*M, 2*y-2*M+31))
        hits = any(4*M+1 <= z <= 5*M+15 for z in PW)
        if hits != (y in MID): bad.append(('MID', y))
    # step 3+4 ranges
    for yh in range(y0, 4*M+1):
        base = 2*yh - 2*M
        for j in (0, 1):
            z0 = base + j
            if not (5*M+16 <= z0 <= 6*M+15): bad.append(('z0', yh, j)); continue
        for u in range(M+1, 2*M-30):     # u <= 2M-31
            j = (u - base) % 2
            z0 = base + j
            if (u + z0) % 2: bad.append(('par', yh, u)); continue
            yp = (u + z0)//2
            if not (yp in P1 and yp < yh and yp != 3*M-15 and yp >= 3*M-14):
                bad.append(('desc', yh, u, yp))
    report(f"B D3-ranges(M={M})", not bad, str(bad[:5]))

# ---------------------------------------------------------------- C
def check_PHplus():
    bad = []
    for M in (48, 64, 80, 96, 112, 128, 144, 160):
        P2 = range(4*M+1, 6*M+16)
        ev = sum(1 for z in P2 if z % 2 == 0); od = len(P2) - ev
        if ev != M+7 or od != M+8: bad.append((M, ev, od))
    report("C PH+ class counts", not bad, str(bad))

# ---------------------------------------------------------------- D
def check_Kstar():
    # (alpha_E, alpha_O, f_O, f_E) from data/e153_dich_lemmas*.log
    tab = {48: (2, 2, 9, 9), 64: (3, 2, 9, 8), 80: (2, 2, 9, 9),
           96: (2, 2, 8, 8), 112: (3, 3, 8, 8), 128: (3, 3, 8, 8)}
    meas = {48: 26, 64: 35, 80: 42, 96: 51, 112: 60, 128: 68}
    bad = []
    for M, (aE, aO, fO, fE) in tab.items():
        K = M//2 + 9 + max(aE - fO, aO - fE)
        if K != meas[M]: bad.append((M, K, meas[M]))
    report("D K* formula (6 scales)", not bad, str(bad))

# ---------------------------------------------------------------- E
def closure(N, facts, max_iter=100000):
    """T/RL/RT closure on window [0, N]; returns (facts, contradiction)."""
    facts = set(facts)
    changed = True
    while changed:
        changed = False
        new = set()
        for (u, v) in facts:
            if (v, u) in facts: return facts, True
            w = 2*u - v
            if 0 <= w <= N and w != u and (u, w) not in facts: new.add((u, w))
            w = 2*v - u
            if 0 <= w <= N and w != v and (w, v) not in facts: new.add((w, v))
        # transitivity
        succ = {}
        for (u, v) in facts: succ.setdefault(u, set()).add(v)
        for (u, v) in facts:
            for w in succ.get(v, ()):
                if w != u and (u, w) not in facts: new.add((u, w))
        if new - facts:
            facts |= new; changed = True
    contra = any((v, u) in facts for (u, v) in facts)
    return facts, contra

def junits(J, N=15):
    return set((t, j + 2*t) for j in J for t in range(0, (N - j)//2 + 1)
               if j + 2*t <= N and t != j + 2*t)

def check_lemmaJ():
    pairs = {1: [2,3,4,6,8], 2: [3,4,5,7,9,11], 3: [4,5,6,8,10,12],
             4: [5,6,7,9,11], 5: [6,8], 6: [7,9,11], 7: [8], 8: [9,11]}
    triples = [(1,10,12), (4,13,15), (5,10,12), (7,10,12), (9,10,12), (10,11,12)]
    allsets = [(a, b) for a, bs in pairs.items() for b in bs] + triples
    assert len(allsets) == 36
    stalls, refuted = [], []
    for J in allsets:
        _, contra = closure(15, junits(J))
        (refuted if contra else stalls).append(J)
    exp_stalls = [(7,8), (8,9), (8,11), (5,10,12), (7,10,12), (9,10,12), (10,11,12)]
    report("E1 J-closure 29/36 refuted", sorted(stalls) == sorted(exp_stalls),
           f"stalls={stalls}")
    # totality splits as logged in data/e153_j_pencil.log
    splits = {(7,8): [(0,1)], (5,10,12): [(0,2)], (7,10,12): [(0,2)],
              (8,9): [(0,1),(0,2)], (9,10,12): [(0,1),(0,2)],
              (8,11): [(0,1),(0,6)], (10,11,12): [(0,1),(1,3)]}
    bad = []
    for J, sp in splits.items():
        base = junits(J)
        # branch over all orientations of the split pairs
        import itertools
        for orient in itertools.product([0,1], repeat=len(sp)):
            facts = set(base)
            for (x, y), o in zip(sp, orient):
                facts.add((x, y) if o == 0 else (y, x))
            _, contra = closure(15, facts)
            if not contra: bad.append((J, orient))
    report("E2 J-splits all branches close", not bad, str(bad))
    # JP / JP' instance enumeration
    jp = [(j, jp_) for j in range(1, 16) for jp_ in range(j+1, 16)
          if jp_ >= 2*j and 5*jp_ - 6*j <= 15]
    jpp = [(j, jp_) for j in range(1, 16) for jp_ in range(j+1, 16)
           if 2*jp_ >= 3*j and 9*jp_ - 10*j <= 15 and 2*jp_ - 3*j >= 0]
    nine = sorted(set(jp) | set(jpp))
    exp9 = sorted([(1,2),(1,3),(1,4),(2,4),(2,5),(3,6),(2,3),(3,5),(4,6)])
    report("E3 JP∪JP' = nine 6-fact pairs", nine == exp9, f"got {nine}")
    # each JP instance: verify the displayed 6-fact derivation is rule-valid
    bad = []
    for (j, j2) in jp:
        t = j2 - 2*j; a = j + 2*t; b = j2 + 2*t; c = j2 + 2*a
        # units present?
        U = junits((j, j2))
        if not {(t, a), (t, b), (a, c)} <= U: bad.append((j, j2, 'units')); continue
        if b != 2*a - t or c != 2*b - t: bad.append((j, j2, 'alg')); continue
        # RT(t≺a): b≺a ; RT(t≺b): c≺b ; T(b≺a, a≺c): b≺c  → cycle (b,c)
        if not (0 <= c <= 15): bad.append((j, j2, 'win'))
    report("E4 JP derivations valid", not bad, str(bad))
    bad = []
    for (j, j2) in jpp:
        tA = 2*j2 - 3*j; tB = 3*j2 - 4*j
        a = 4*j2 - 5*j; b = 6*j2 - 7*j; c = 9*j2 - 10*j
        U = junits((j, j2))
        if not {(tA, a), (tB, b), (a, c)} <= U: bad.append((j, j2, 'units')); continue
        if b != 2*a - tA or c != 2*b - tB: bad.append((j, j2, 'alg')); continue
        if not (0 <= c <= 15): bad.append((j, j2, 'win'))
    report("E5 JP' derivations valid", not bad, str(bad))

# ---------------------------------------------------------------- F
def check_affine():
    bad = []
    # Gamma1 (FG-high): p >= 2q+1, 5p-6q <= N
    for M in (48, 144):
        N = 2*M + 15
        for q in range(0, M+16):
            for p in range(2*q+1, M+16):
                if 5*p - 6*q > N: continue
                s = p - 2*q; m1 = 2*p - 3*q; m2 = 3*p - 4*q; m3 = 5*p - 6*q
                if not (m1 == 2*s + q and m2 == 2*s + p and m3 == 2*m1 + p
                        and m2 == 2*m1 - s and m3 == 2*m2 - s
                        and 1 <= s and m3 <= N):
                    bad.append(('G1', M, q, p))
    # Gamma2': p = 5a+6q, 13a+12q <= N
    for M in (48, 144):
        N = 2*M + 15
        for q in range(0, M+16):
            for a in range(1, N):
                p = 5*a + 6*q
                if p > M+15 or 13*a + 12*q > N: continue
                m1 = 4*a + 3*q; m2 = 7*a + 6*q; m3 = 13*a + 12*q
                if not (m1 == 2*(2*a+q) + q and m2 == 2*m1 - a and m2 == 2*a + p
                        and m3 == 2*m2 - a and m3 == 2*m1 + p):
                    bad.append(('G2p', M, q, a))
    report("F affine identities Γ1/Γ2'", not bad, str(bad[:5]))

# ---------------------------------------------------------------- G
def check_bridge1():
    bad = []
    for m in range(0, 21):
        N = sum(1 for p in range(1, 2**(m+1))
                if p % 4 == 1 and 2**m < 3*p and 3*p + 1 <= 2**(m+1))
        if not N >= (2**m - 13)/12: bad.append(('DD', m, N))
    for j in range(4, 21, 2):
        pj = (2**j - 1)//3
        if 3*pj != 2**j - 1 or pj % 8 != 5: bad.append(('C2A-even', j))
    for j in range(3, 21, 2):
        if (2**j - 1) % 3 == 0 or (2**j - 1) % 8 != 7: bad.append(('C2A-odd', j))
    report("G BRIDGE1 arithmetic", not bad, str(bad))

if __name__ == '__main__':
    check_FI(112); check_FI(144)
    check_D3(48); check_D3(144)
    check_PHplus(); check_Kstar()
    check_lemmaJ(); check_affine(); check_bridge1()
    print("ALL OK" if ok_all else "SOME CHECKS FAILED")
    sys.exit(0 if ok_all else 1)
