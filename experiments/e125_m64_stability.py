"""Scale-stability of the constant-bound coupled schema at M=64 (the
machine gap #1 of the NO program): (2,2,2) and (3,6,12) absolute bounds."""
import sys, time
sys.path.insert(0, 'experiments')
from e120_density_cores import solve_coupled3

for bounds in [(2, 2, 2), (3, 6, 12)]:
    t0 = time.time()
    r = solve_coupled3(64, None, None, budget=43200.0, seams='both',
                       abs_bounds=bounds)
    verdict = r[0] if isinstance(r, tuple) else r
    print(f"C3abs M=64 bounds={bounds}: {verdict} [{time.time()-t0:.0f}s]",
          flush=True)
