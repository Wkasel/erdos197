"""Schema lock: absolute-anchor CORE'(M) sufficiency at M=32,48,80,96."""
import sys, time
sys.path.insert(0, 'experiments')
from e120_density_cores import solve_coupled3
for M, bounds in ((32,(3,3,3)), (48,(2,2,2)), (80,(2,2,2)), (96,(2,2,2))):
    core = sorted(set(
        list(range(M+1, 2*M+1)) +
        list(range(3*M-15, 4*M+1)) +
        list(range(4*M+1, 6*M+16))))
    t0 = time.time()
    r = solve_coupled3(M, None, None, budget=43200.0, seams='both',
                       abs_bounds=bounds, support=core)
    print(f"SCHEMA-LOCK M={M} {bounds}: {r[0] if isinstance(r,tuple) else r} "
          f"[{time.time()-t0:.0f}s] |core|={len(core)}", flush=True)
