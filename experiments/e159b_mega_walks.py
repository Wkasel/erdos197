"""e159b: MONSTER-SCALE exact seam/interval walk battery
(FRONT MEGA-SCHEMA, notes/63; extends g4c partA's exact walks).

The g4c battery (STATUS: 'exact big-int walks confirm X2 closure and
neck divergence to seam ~2^20000 and FAN arithmetic at 2^20102') is
re-run with the SAME stage schedules pushed until the seam exponent
passes 100000, plus a monster spot battery at exponent ~10^6:

  - tri  schedule a_k = 2 + k(k+1)/2  (stage-alternating, Geneson-like)
  - quad schedule a_k = 2 + k^2
  For every stage k in range:
    X2 closure:   2 * 2^{a_{k+1}} < 2^{a_{k+2}}  whenever L_{k+1} >= 2
    C0 neck:      2 * 2^{a_k} - 2^{a_{k+1}} < -2^{a_k}  (k >= 3)
  FAN arithmetic at the first seam with a_j >= 100000: planted member
  p in {2^j - 1, 2^j} of the seam pair has completion 2p - x inside
  the new owner's first octave (2^j, 2^{j+1}] for every fixed attacker
  1 <= x < 2^j tested (x up to 10^18 and x = 2^j - 1), and OUTSIDE it
  for x >= 2^j  (exact big-int, no float anywhere).
  Monster spot battery: same checks at exponent ~10^6.

Run: .venv/bin/python experiments/e159b_mega_walks.py
Output: data/e159b_mega_walks.json
"""
import json
import os
import sys
import time

sys.set_int_max_str_digits(2_000_000)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'e159b_mega_walks.json')


def schedule(name, kmax):
    if name == 'tri':
        return [0] + [2 + k * (k + 1) // 2 for k in range(1, kmax + 1)]
    return [0] + [2 + k * k for k in range(1, kmax + 1)]


def walk_battery(name, a, kmax):
    ok = True
    for k in range(1, kmax - 1):
        lo_k = 1 << a[k]
        hi_k = 1 << a[k + 1]
        lo_k2 = 1 << a[k + 2]
        if a[k + 2] - a[k + 1] >= 2:
            ok &= 2 * hi_k < lo_k2                      # X2 closed
        if k >= 3:
            ok &= 2 * lo_k - hi_k < -(1 << a[k])        # neck -> -inf
    return ok


def fan_at(j):
    """FAN arithmetic at seam 2^j, exact big ints.

    Original g4c form (small fixed x): completion 2p - x of planted
    member p in {2^j - 1, 2^j} lands in the new owner's octave
    (m, 2m] iff x < m.  EXACT boundary form for all x >= 1:
    m < 2p - x <= 2m  iff  x < 2p - m  (2p - 2m <= 0 <= x always) —
    for p = m this is x < m, for p = m - 1 it is x < m - 2 (boundary
    attackers x in {m-2, m-1} land ON/below the seam, not inside).
    The battery checks the small-x law verbatim AND the exact
    boundary predicate at x around the seam."""
    m = 1 << j
    ok = True
    xs_small = [1, 2, 3, 5, 999983, 10 ** 6, 10 ** 18]
    for p in (m - 1, m):
        for x in xs_small:
            z = 2 * p - x
            ok &= (m < z <= 2 * m) == (x < m)        # g4c small-x law
        for x in xs_small + [m - 3, m - 2, m - 1, m, m + 1, 2 * m - 1]:
            z = 2 * p - x
            ok &= (m < z <= 2 * m) == (x < 2 * p - m)  # exact boundary
    return ok


def main():
    out = {'batteries': [], 'fail': []}
    # full battery: tri to k=450 (a_450 = 101477), quad to k=320
    # (a_320 = 102402) — both pass exponent 100000.
    for name, kmax in (('tri', 450), ('quad', 320)):
        a = schedule(name, kmax + 2)
        t0 = time.time()
        ok = walk_battery(name, a, kmax)
        t_walk = time.time() - t0
        # first seam exponent >= 100000
        j = next(x for x in a if x >= 100000)
        t1 = time.time()
        okf = fan_at(j)
        t_fan = time.time() - t1
        seam_digits = len(str(1 << j))
        row = {'schedule': name, 'kmax': kmax, 'a_kmax': a[kmax],
               'seam_exp': j, 'seam_decimal_digits': seam_digits,
               'walk_ok': ok, 'fan_ok': okf,
               'walk_s': round(t_walk, 2), 'fan_s': round(t_fan, 4)}
        out['batteries'].append(row)
        if not (ok and okf):
            out['fail'].append(row)
        print(f"{name}: stages k<= {kmax} (top exponent {a[kmax]}), "
              f"X2+neck {'OK' if ok else 'FAIL'} [{t_walk:.2f}s]; "
              f"FAN at seam 2^{j} ({seam_digits} digits) "
              f"{'OK' if okf else 'FAIL'} [{t_fan:.4f}s]", flush=True)
    # monster spot battery at exponent ~10^6
    t0 = time.time()
    jM = 10 ** 6 + 3
    okm = fan_at(jM)
    # X2 + neck spot at the same magnitude (synthetic stages
    # a = (10^6, 10^6+3, 10^6+8): L = 3, 5)
    aa = [10 ** 6, 10 ** 6 + 3, 10 ** 6 + 8]
    okm &= 2 * (1 << aa[1]) < (1 << aa[2])
    okm &= 2 * (1 << aa[0]) - (1 << aa[1]) < -(1 << aa[0])
    t_m = time.time() - t0
    row = {'monster_exp': jM, 'decimal_digits': len(str(1 << jM)),
           'ok': okm, 's': round(t_m, 3)}
    out['monster'] = row
    if not okm:
        out['fail'].append(row)
    print(f"monster: FAN + X2 + neck at 2^{jM} "
          f"({row['decimal_digits']} digits) {'OK' if okm else 'FAIL'} "
          f"[{t_m:.3f}s]", flush=True)
    json.dump(out, open(DATA, 'w'), indent=1)
    print(f"failures: {out['fail']}")
    print(f"-> {DATA}")


if __name__ == '__main__':
    main()
