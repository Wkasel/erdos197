import sys, time
import numpy as np
from pysat.solvers import Cadical195
def test(M, expect):
    lo, hi = M, 2*M
    V = list(range(lo+1, hi+1))
    n = len(V)
    idx = {v:i for i,v in enumerate(V)}
    var = {}
    c = 0
    for i in range(n):
        for j in range(i+1, n):
            c += 1; var[(i,j)] = c
    def o(u,w):
        i,j = idx[u], idx[w]
        return var[(i,j)] if i<j else -var[(j,i)]
    cl = [[o(2*M-5, M+5)], [o(2*M-3, M+6)], [o(2*M-10, M+3)]]
    for y in V:
        d = 1
        while y+d <= hi:
            x, z = y-d, y+d
            d += 1
            if x > lo:
                cl.append([-o(x,y), -o(y,z)])
                cl.append([-o(z,y), -o(y,x)])
    sol = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    while True:
        if not sol.solve():
            print(f"M={M} (mod8={M%8}): UNSAT ({time.time()-t0:.0f}s) expect={expect} {'OK' if expect=='UNSAT' else 'MISMATCH!!'}", flush=True)
            return
        model = set(l for l in sol.get_model() if l>0)
        B = np.zeros((n,n), dtype=bool)
        for (i,j),lit in var.items():
            if lit in model: B[i,j]=True
            else: B[j,i]=True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n,dtype=bool) & B.T
        def lit(p,q):
            return var[(p,q)] if p<q else -var[(q,p)]
        new = []
        ii,jj = np.nonzero(miss)
        for i,j in zip(ii[:30000], jj[:30000]):
            ks = np.nonzero(B[i] & B[:,j])[0]
            new.append([-lit(i,int(ks[0])), -lit(int(ks[0]),j), lit(i,j)])
        if not new:
            print(f"M={M} (mod8={M%8}): SAT ({time.time()-t0:.0f}s) expect={expect} {'OK' if expect=='SAT' else 'MISMATCH!!'}", flush=True)
            return
        sol.append_formula(new)
for (M, e) in [(232,"UNSAT"),(236,"SAT"),(936,"UNSAT"),(932,"SAT"),(1288,"UNSAT"),(1284,"SAT")]:
    test(M, e)
print("SPOTCHECK COMPLETE", flush=True)
