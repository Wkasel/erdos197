"""Corrected schema sufficiency at M=64: absolute-anchor CORE'(M)."""
import sys, time
sys.path.insert(0, 'experiments')
from e120_density_cores import solve_coupled3
M = 64
core = sorted(set(
    list(range(M+1, 2*M+1)) +            # all of B0 (generous)
    list(range(3*M-15, 4*M+1)) +         # B1 absolute band
    list(range(4*M+1, 6*M+16))           # B2 bottom..flood+15 (generous)
))
print(f"M={M} |support|={len(core)}", flush=True)
t0 = time.time()
r = solve_coupled3(M, None, None, budget=43200.0, seams='both',
                   abs_bounds=(2,2,2), support=core)
print(f"SCHEMA-CHECK2 M={M}: {r[0] if isinstance(r,tuple) else r} [{time.time()-t0:.0f}s]", flush=True)
