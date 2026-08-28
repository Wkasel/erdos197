"""e159: MONSTER-SCALE stress of the e113 C3 hand-proof checker
(FRONT MEGA-SCHEMA, notes/63).

Runs the UNMODIFIED e113_c3_hand_proof schema executors (check_layer1,
check_flip, sharpness_4mod8) at M = 2^13, 2^14, 2^16, 2^20 — pure
big-int rule execution, every lemma instance rung-by-rung, both phase
branches, full audit() hypothesis discipline.  Records wall time and
peak RSS per scale.  Sharpness controls at M = 2^k + 4 (== 4 mod 8).

Run: .venv/bin/python experiments/e159_mega_e113.py [exponents...]
Output: data/e159_mega_e113.json
"""
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e113_c3_hand_proof import check_layer1, check_flip, sharpness_4mod8

DATA = os.path.join(HERE, '..', 'data', 'e159_mega_e113.json')


def rss_mb():
    ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes, linux KB
    return ru / (1024 * 1024) if sys.platform == 'darwin' else ru / 1024


def main():
    exps = [int(a) for a in sys.argv[1:]] or [13, 14, 16, 20]
    out = {'rows': [], 'fail': []}
    for e in exps:
        M = 1 << e
        assert M % 8 == 0
        row = {'exp': e, 'M': M}
        t0 = time.time()
        try:
            check_layer1(M)
            row['layer1_s'] = round(time.time() - t0, 2)
            row['layer1'] = 'PASS'
        except Exception as ex:
            row['layer1'] = f'FAIL {ex!r}'
            out['fail'].append(['layer1', M, repr(ex)])
        t1 = time.time()
        try:
            check_flip(M)
            row['flip_s'] = round(time.time() - t1, 2)
            row['flip'] = 'PASS'
        except Exception as ex:
            row['flip'] = f'FAIL {ex!r}'
            out['fail'].append(['flip', M, repr(ex)])
        t2 = time.time()
        try:
            sharpness_4mod8(M + 4)          # 2^e + 4 == 4 mod 8 control
            row['sharp_M+4'] = 'PASS'
        except Exception as ex:
            row['sharp_M+4'] = f'FAIL {ex!r}'
            out['fail'].append(['sharp', M + 4, repr(ex)])
        row['sharp_s'] = round(time.time() - t2, 4)
        row['peak_rss_mb'] = round(rss_mb(), 1)
        out['rows'].append(row)
        print(f"M=2^{e}={M}: layer1 {row['layer1']} "
              f"[{row.get('layer1_s', '-')}s]  flip {row['flip']} "
              f"[{row.get('flip_s', '-')}s]  sharp(M+4) {row['sharp_M+4']}  "
              f"peakRSS {row['peak_rss_mb']} MB", flush=True)
        json.dump(out, open(DATA, 'w'), indent=1)
    print(f"failures: {out['fail']}")
    print(f"-> {DATA}")
    if out['fail']:
        sys.exit(1)


if __name__ == '__main__':
    main()
