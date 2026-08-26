"""Deeper scale-stability of the Case-2 constant-2 schema: (2,2,2) at M=80, 96."""
import sys, time
sys.path.insert(0, 'experiments')
from e120_density_cores import solve_coupled3

for M in (80, 96):
    t0 = time.time()
    r = solve_coupled3(M, None, None, budget=86400.0, seams='both',
                       abs_bounds=(2, 2, 2))
    verdict = r[0] if isinstance(r, tuple) else r
    print(f"C3abs M={M} bounds=(2,2,2): {verdict} [{time.time()-t0:.0f}s]",
          flush=True)
