"""Schema sufficiency: (2,2,2) two-seam instance at M=64 restricted to the
CORE(M) support of notes/51 (generous margins). UNSAT => schema sufficient."""
import sys, time
sys.path.insert(0, 'experiments')
from e120_density_cores import solve_coupled3
# solve_coupled3 supports support= (surviving values) per its signature
M = 64
S1 = list(range(2*M-7, 2*M+1))
S2 = list(range(4*M-7, 4*M+1))
S3 = list(range(4*M+1, 4*M+17))
S5 = list(range(2*M + M//3, 3*M + M//4))          # generous central band
S6 = list(range(5*M, 6*M + 17))                    # flood band to 6M+16
S4 = list(range(M+1, M+41))                        # generous B0 low margin
support = sorted(set(S1+S2+S3+S4+S5+S6))
print(f"M={M} |support|={len(support)}", flush=True)
t0 = time.time()
r = solve_coupled3(M, None, None, budget=43200.0, seams='both',
                   abs_bounds=(2,2,2), support=support)
verdict = r[0] if isinstance(r, tuple) else r
print(f"SCHEMA-CHECK M={M}: {verdict} [{time.time()-t0:.0f}s]", flush=True)
