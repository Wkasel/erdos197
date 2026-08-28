#!/usr/bin/env python3
"""FRONT LAW-CONSISTENCY (notes/64): cross-check the exact laws at massive
scales.  Formulas + exact big-int arithmetic ONLY — no solving.

Laws under test (certification pedigree in notes/57/58/61/62/51/50):
  L1  K* mechanistic law   K*(M) = m + 9 + max(a_E - f_O, a_O - f_E), m=M/2
      measured (a_E,a_O,f_O,f_E) at 48..160 -> K* = 26/35/42/51/60/68/76/83
  L2  L-LOP flat cap law   cap(M) = (M+16)/2 - 5  for M >= 96
      (C(M) := cap+1 = (M+16)/2 - 4 = kmax_unsat); measured caps
      29/36/44/51/59/67/75/83 at 48..160
  L3  overlap width        W(M) = C(M) - K*(M)  (= cap - K* + 1)
      requirement (OV): W >= 0
  L4  skip-mass law        mu_skip^A(M) = 13M^2/64 + M/8   (7 scales 16..128)
  L5  v* witness curve     6 / 65 / 368 at M = 16 / 24 / 32 (3-block SAT pts)
  L6  CORE'(M) bands       P0=[M+1,2M], P1=[3M-15,4M], P2=[4M+1,6M+15]
      (canonical per experiments/e153 core_support; |CORE'| = 4M+31)
  L7  window tiling        W_t = (M*8^t, M*8^t*8]; C3 mod-8; DICH mod-16;
      SCHED-DEAD (M>=12, M=0 mod 4); Lemma K (k=M/4, n=3M/4, n>=k+5)
"""
from fractions import Fraction
import math

ok = True
def check(name, cond, detail=""):
    global ok
    tag = "PASS" if cond else "FAIL"
    if not cond:
        ok = False
    print(f"[{tag}] {name} {detail}")

# ----------------------------------------------------------------------
# (a) K* law vs cap law vs DICH thresholds -- reproduce the 8 scales
# ----------------------------------------------------------------------
print("=" * 72)
print("(a) K*/cap/DICH reproduction at the eight certified scales")
# per-scale catalogue inputs (F1/F2, notes/57 + audits): (a_E, a_O, f_O, f_E)
CAT = {
    48:  (2, 2, 9, 9),
    64:  (3, 2, 9, 8),
    80:  (2, 2, 9, 9),
    96:  (2, 2, 8, 8),
    112: (3, 3, 8, 8),
    128: (3, 3, 8, 8),
    144: (3, 3, 8, 8),
    160: (2, 2, 8, 8),
}
KSTAR_MEAS = {48: 26, 64: 35, 80: 42, 96: 51, 112: 60, 128: 68, 144: 76, 160: 83}
CAP_MEAS   = {48: 29, 64: 36, 80: 44, 96: 51, 112: 59, 128: 67, 144: 75, 160: 83}

def kstar_law(M, aE, aO, fO, fE):
    return M // 2 + 9 + max(aE - fO, aO - fE)

for M in sorted(CAT):
    aE, aO, fO, fE = CAT[M]
    k = kstar_law(M, aE, aO, fO, fE)
    check(f"K*({M}) law -> {k}", k == KSTAR_MEAS[M], f"(measured {KSTAR_MEAS[M]})")

# flat cap law scope
for M in sorted(CAP_MEAS):
    flat = (M + 16) // 2 - 5
    inscope = M >= 96
    hit = flat == CAP_MEAS[M]
    if inscope:
        check(f"flat cap law at {M}: {flat}", hit, f"(measured {CAP_MEAS[M]})")
    else:
        print(f"[info] flat cap law OUT OF SCOPE at {M}: predicts {flat}, measured {CAP_MEAS[M]}"
              f" (off by {CAP_MEAS[M]-flat})")

# dead laws double-check: floor(M/32) cap law and mod-32 K* law must fail
dead_cap_fail = [(M, (M+16)//2 - M//32 - 2, CAP_MEAS[M]) for M in CAP_MEAS
                 if (M+16)//2 - M//32 - 2 != CAP_MEAS[M]]
check("floor(M/32) cap law is dead (fails somewhere)", len(dead_cap_fail) > 0,
      f"first fail {dead_cap_fail[0] if dead_cap_fail else None}")
mod32_pred = {M: (M//2 + (2 if M % 32 == 16 else 3)) for M in KSTAR_MEAS}
mod32_fail = [(M, mod32_pred[M], KSTAR_MEAS[M]) for M in KSTAR_MEAS
              if mod32_pred[M] != KSTAR_MEAS[M]]
check("mod-32 K* law is dead (fails somewhere)", len(mod32_fail) > 0,
      f"fails at {[t[0] for t in mod32_fail]}")

# measured overlap widths
print("\nmeasured W(M) = cap - K* + 1:")
for M in sorted(CAT):
    W = CAP_MEAS[M] - KSTAR_MEAS[M] + 1
    print(f"  M={M:4d}  cap={CAP_MEAS[M]:3d}  K*={KSTAR_MEAS[M]:3d}  W={W}")

# ----------------------------------------------------------------------
# (a) continued: W at M = 2^k, k = 6..40, and spot values to 2^1000
# ----------------------------------------------------------------------
print("\n(a) W(2^k) from the laws (flat cap + K* mechanism), scenarios over alpha")
print("    W = C - K* = (m+4) - (m+9+max(aE-fO,aO-fE)) = min(fO-aE, fE-aO) - 5")
print("    with F2 regime f=8 (onset M>=96, both parities): W = 3 - alpha_max")
rows = []
for k in list(range(6, 41)) + [100, 500, 1000]:
    M = 2 ** k
    m = M // 2
    C = (M + 16) // 2 - 4
    # scenarios: alpha_max = 2 / 3 / 4  (f = 8 throughout, the F2 regime)
    Ws = {a: (8 - a) - 5 for a in (2, 3, 4)}
    known = ""
    if M in KSTAR_MEAS:
        known = f"  [MEASURED: W={CAP_MEAS[M]-KSTAR_MEAS[M]+1}]"
    rows.append((k, M, C, Ws, known))
for k, M, C, Ws, known in rows[:12]:
    print(f"  k={k:4d} M=2^{k}  C={C}  W(a=2)={Ws[2]} W(a=3)={Ws[3]} W(a=4)={Ws[4]}{known}")
print("  ... (W scenario values are k-independent: 1 / 0 / -1 for alpha=2/3/4)")
k = 1000
M = 2 ** k
C = (M + 16) // 2 - 4
check("C(2^1000) integer & = m+4", C == M // 2 + 4, f"digits={len(str(C))}")
check("K*(2^1000) integer for any (a,f) in envelope",
      all(isinstance(kstar_law(M, a, a, f, f), int) for a in (2, 3, 4) for f in (8, 9)))

# alpha=2 forever -> W=1 forever;  alpha=3 -> W=0;  alpha=4 -> W=-1 (HOLE).
# measured alpha series is non-monotone: 2,3,2,2,3,3,3,2 -> W already hit 0
# at 112/128/144.  No certified law bounds alpha <= 3; the half-scale
# SAT-alive clique bound (notes/58 3.5d) is 4, realized at m=24/28/32.
print("\n  verdict inputs: alpha series 48..160 =",
      [max(CAT[M][0], CAT[M][1]) for M in sorted(CAT)])

# ----------------------------------------------------------------------
# (b) skip-mass law vs v* witness curve
# ----------------------------------------------------------------------
print("=" * 72)
print("(b) skip-mass law: independent recount (schedule (1,0,0,1))")

def mu_skip_count(M, team):
    """Exact count of skip triples (u,y,z) in (Bm1 x B1 x B2) ∩ T^3, z=2y-u,
    for the H-voiding schedule (1,0,0,1): team A = odds Bm1, evens B0/B1,
    odds B2; team B = complement parities."""
    # parity of team in each block: A: Bm1 odd, B1 even, B2 odd
    #                               B: Bm1 even, B1 odd, B2 even
    pu = 1 if team == 'A' else 0
    py = 0 if team == 'A' else 1
    n = 0
    for u in range(M // 2 + 1, M + 1):
        if u % 2 != pu:
            continue
        for y in range(2 * M + 1, 4 * M + 1):
            if y % 2 != py:
                continue
            z = 2 * y - u
            if 4 * M < z <= 8 * M and z % 2 == (pu):  # z parity == u parity
                n += 1
    return n

lawA = lambda M: 13 * M * M // 64 + M // 8
lawB = lambda M: 13 * M * M // 64 - M // 8
for M in (16, 24, 32, 48, 64, 96, 128, 192, 256):
    cA, cB = mu_skip_count(M, 'A'), mu_skip_count(M, 'B')
    check(f"mu_skip A/B at M={M}: {cA}/{cB}",
          cA == lawA(M) and cB == lawB(M),
          f"law {lawA(M)}/{lawB(M)}")
# integrality at 2^k and at M*8^t
for k in (6, 10, 20, 40, 100, 1000):
    M = 2 ** k
    check(f"13M^2/64+M/8 integer at M=2^{k}",
          (13 * M * M) % 64 == 0 and M % 8 == 0)

print("\n(b) v* witness curve fit (SAT-point upper bounds 6/65/368 at 16/24/32)")
pts = [(16, 6), (24, 65), (32, 368)]
for (M1, v1), (M2, v2) in zip(pts, pts[1:]):
    e = math.log(v2 / v1) / math.log(M2 / M1)
    print(f"  local power exponent {M1}->{M2}: {e:.3f}")
e_global = math.log(368 / 6) / math.log(32 / 16)
print(f"  global exponent 16->32: {e_global:.3f}")
for M, v in pts:
    print(f"  M={M}: v_wit={v}   (M/8)^6*3/32 = {3*(M//8)**6/32:.1f}   "
          f"13M^2/64+M/8 = {lawA(M)}   ratio wit/skip = {v/lawA(M):.3f}")
# exponential fit residual: log-increments per +8 in M
inc = [math.log(65 / 6) / 8, math.log(368 / 65) / 8]
print(f"  exponential-fit log-increments per unit M: {inc[0]:.4f} vs {inc[1]:.4f}"
      f"  (non-constant -> exponential fit worse than power fit)")
# skip-law predictions vs witnesses
print("  skip-law growth 16->32 factor:", lawA(32) / lawA(16),
      " witness growth factor:", 368 / 6)
# crossing point of the two curves (witness fit c*M^6 vs 13M^2/64)
c = 6 / 16 ** 6
lo, hi = 16, 64
while hi - lo > 1e-9:
    mid = (lo + hi) / 2
    if c * mid ** 6 < 13 * mid * mid / 64 + mid / 8:
        lo = mid
    else:
        hi = mid
print(f"  curves cross near M ~= {lo:.1f} (witness below skip-mass before, above after)")

# ----------------------------------------------------------------------
# (c) CORE'(M) band arithmetic composed across the window tiling M*8^t
# ----------------------------------------------------------------------
print("=" * 72)
print("(c) band composition across M*8^t, t = 0..1000, exact big ints")

def band_checks(M):
    """All affine residue/integrality/containment conditions of the schema
    stack at one window scale M.  Returns list of (name, bool)."""
    m = M // 2
    P0 = (M + 1, 2 * M)
    P1 = (3 * M - 15, 4 * M)
    P2 = (4 * M + 1, 6 * M + 15)
    conds = [
        ("DICH residue M=0 mod 16", M % 16 == 0),
        ("C3 core residue M=0 mod 8", M % 8 == 0),
        ("P-ARM halved line m=0 mod 8", m % 8 == 0),
        ("SCHED-DEAD scope M>=12, M=0 mod 4", M >= 12 and M % 4 == 0),
        ("Lemma K n>=k+5 (k=M/4,n=3M/4)", 3 * M // 4 >= M // 4 + 5),
        ("P1 inside B1: 3M-15 > 2M", P1[0] > 2 * M),
        ("P1 nonempty ordered", P1[0] <= P1[1]),
        ("P2 inside B2: 6M+15 <= 8M", P2[1] <= 8 * M),
        ("P1 size M+16 even split", (P1[1] - P1[0] + 1) == M + 16 and (M + 16) % 2 == 0),
        ("P1 parity counts m+8/m+8", (M + 16) // 2 == m + 8),
        ("P2 size 2M+15", (P2[1] - P2[0] + 1) == 2 * M + 15),
        ("P2 odd count M+8", (P2[1] - P2[0]) // 2 + 1 == M + 8),
        ("|CORE'| = 4M+31", M + (M + 16) + (2 * M + 15) == 4 * M + 31),
        ("P1 bottom odd (3M-15 odd)", (3 * M - 15) % 2 == 1),
        ("core disjoint from next window core: 6M+15 < 8M+1", 6 * M + 15 < 8 * M + 1),
        ("halved crown window CW=[3m-7,3m-1] inside halved band",
         3 * m - 7 > 2 * m and 3 * m - 1 < 4 * m),
        ("W2e=[4m+1,6m+7] inside halved B2", 6 * m + 7 <= 8 * m),
        ("E1 window [3M-15,3M-1] inside P1", 3 * M - 1 <= 4 * M),
        ("droppable completions 3M-8,3M-9,3M-12,3M-13 in E1",
         all(3 * M - 15 <= 3 * M - i <= 3 * M - 1 for i in (8, 9, 12, 13))),
        ("skip-mass integrality 64 | 13M^2 and 8 | M",
         (13 * M * M) % 64 == 0 and M % 8 == 0),
        ("flood centre 6M is P2 interior", P2[0] < 6 * M < P2[1]),
        ("seam-2 doubling image (6M,6M+15] = 2*4M - (2M-15,2M]",
         (2 * 4 * M - (2 * M), 2 * 4 * M - (2 * M - 15)) == (6 * M, 6 * M + 15)),
    ]
    return conds

bases = [16, 48, 64, 80, 96, 112, 128, 144, 160, 2 ** 6, 2 ** 20, 2 ** 40]
worst = []
for base in bases:
    fails = []
    for t in range(0, 1001):
        M = base * 8 ** t
        for name, c in band_checks(M):
            if not c:
                fails.append((t, name))
    if fails:
        worst.append((base, fails[:5]))
check(f"band composition: {len(bases)} bases x t<=1000, all conditions",
      not worst, f"fails: {worst[:2]}")

# k=0 boundary: which base scales FAIL (the only residue constraint is on the base)
bad_bases = []
for base in (8, 24, 40, 48, 56, 2 ** 5):
    names = [n for n, c in band_checks(base) if not c]
    if names:
        bad_bases.append((base, names))
print("[info] base-scale (t=0) constraint: failing bases ->")
for b, names in bad_bases:
    print(f"       M={b}: {names}")

# mod-2^j saturation: any mod-2^j condition is satisfied at M*8^t once
# 3t + v2(M) >= j; for the stack's largest modulus 16, t >= ceil((4-v2(M))/3)
for base in (48, 24, 40):
    v2 = (base & -base).bit_length() - 1
    t_need = max(0, -(-(4 - v2) // 3))
    Ms = [base * 8 ** t for t in range(4)]
    sat = [M % 16 == 0 for M in Ms]
    print(f"[info] base {base} (v2={v2}): M*8^t = 0 mod 16 from t={t_need}: {sat}")

print("=" * 72)
print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
