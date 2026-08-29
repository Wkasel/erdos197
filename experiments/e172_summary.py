"""e172 helper: render LB trajectories from e172_maxsat_lb.jsonl
files (local + synced pod copies).  Usage:
    e172_summary.py [jsonl ...]        (default: data/e172_maxsat_lb.jsonl)
"""
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')


def main():
    paths = sys.argv[1:] or [os.path.join(DATA, 'e172_maxsat_lb.jsonl')]
    tags = {}
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                tags.setdefault((p, r['tag']), []).append(r)
    for (p, tag), rows in sorted(tags.items()):
        lbs = [(r['lb_sum'], r['t']) for r in rows if r['event'] == 'lb']
        term = [r for r in rows if r['event'] in ('opt', 'partial',
                                                  'hard-unsat')]
        cur = lbs[-1][0] if lbs else 0
        line = f"{tag} [{os.path.basename(p)}]: "
        if term and term[-1]['event'] == 'opt':
            t = term[-1]
            wa, wb = t['witness_inv']
            line += (f"OPT sum={t['opt_sum']} -> v* in "
                     f"[{t['vstar_lb']}, {t['vstar_ub']}] "
                     f"(witness {wa}/{wb}) t={t['t']}s "
                     f"audit_errs={len(t.get('audit_errs', []))}")
        else:
            st = term[-1]['event'] if term else 'running'
            line += (f"LB sum>={cur} -> v*>={(cur + 1) // 2} "
                     f"({st}, {len(lbs)} bumps, "
                     f"last t={lbs[-1][1] if lbs else 0}s)")
        print(line)
        # compact trajectory: lb@t milestones
        traj = ' '.join(f"{lb}@{int(t)}s" for lb, t in lbs)
        print(f"   {traj}")


if __name__ == '__main__':
    main()
