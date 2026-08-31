import itertools, sys
sys.path.insert(0,'/private/tmp/claude-501/-Users-will-Dev-personal-tasks-math/2817dd94-f30a-4336-b6a4-72727bffa320/scratchpad')
from advA_sat import solve

def Zunits(M):
    """(b): for every y<z in (M,2M] with 2y-z in (M/4,M/2], z precedes y."""
    lo, hi = M/4, M/2
    u=[]
    for y in range(M+1,2*M+1):
        for z in range(y+1,2*M+1):
            x=2*y-z
            if lo < x <= hi:
                u.append((z,y))
    return u

print("--- Lemma bases: Z(M) for 16<=M<=31 (expect UNSAT) ---")
for M in range(16,32):
    r,_,_=solve(M, Zunits(M))
    print(f"  Z({M}) = {'SAT' if r else 'UNSAT'}", flush=True)
print("--- Z(M) for 12..15 and 32..40 ---")
for M in list(range(12,16))+list(range(32,41)):
    r,_,_=solve(M, Zunits(M))
    print(f"  Z({M}) = {'SAT' if r else 'UNSAT'}", flush=True)
