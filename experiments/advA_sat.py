import sys, itertools
from pysat.solvers import Cadical195
from pysat.formula import IDPool

def solve(M, units, transitivity='eager', verbose=False):
    """Order of (M,2M]. units: list of (u,v) meaning u prec v.
       (i): no monotone AP a<b<c inside block."""
    vals = list(range(M+1, 2*M+1))
    idx = {v:i for i,v in enumerate(vals)}
    pool = IDPool()
    def P(u,v):  # u prec v
        i,j = idx[u], idx[v]
        if i<j: return pool.id(('p',u,v))
        else:   return -pool.id(('p',v,u))
    cls = []
    n=len(vals)
    # totality is implicit (P(u,v) = not P(v,u)); need transitivity
    for a,b,c in itertools.combinations(vals,3):
        # transitivity both directions
        cls.append([-P(a,b),-P(b,c),P(a,c)])
        cls.append([-P(c,b),-P(b,a),P(c,a)])
    # AP constraints: a<b<c, c-b == b-a
    napcnt=0
    for b in vals:
        for d in range(1, M):
            a,c = b-d, b+d
            if a in idx and c in idx:
                # forbid a<b<c positional monotone and c<b<a
                cls.append([-P(a,b),-P(b,c)])
                cls.append([-P(c,b),-P(b,a)])
                napcnt+=1
    for (u,v) in units:
        assert u in idx and v in idx, (M,u,v)
        cls.append([P(u,v)])
    s = Cadical195(bootstrap_with=cls)
    r = s.solve()
    model=None
    if r:
        m=set(x for x in s.get_model() if x>0)
        def key(v):
            return sum(1 for w in vals if w!=v and P(w,v) in m or (w!=v and -P(v,w) in m and False))
        # build order by counting predecessors
        pred={v:0 for v in vals}
        for u,v in itertools.combinations(vals,2):
            lit=P(u,v)
            val = (lit>0 and lit in m) or (lit<0 and -lit not in m)
            if val: pred[v]+=1
            else: pred[u]+=1
        model=sorted(vals,key=lambda v:pred[v])
    s.delete()
    return r, model, napcnt

def C3(M): return [(2*M-5, M+5), (2*M-3, M+6), (2*M-10, M+3)]
def C4(M): return [(2*M-13,M+1),(2*M-11,M+2),(2*M-5,M+5),(2*M-10,M+3)]
def OG(M):
    u=[]
    for x in (15,16):
        for j in range(1, x//2+1):
            u.append((2*M+2*j-x, M+j))
    return u
def A11(M):
    u=[]
    for j in range(1,8): u.append((2*M+2*j-15, M+j))
    for j in range(1,5): u.append((2*M+2*j-16, M+j))
    return u

if __name__=='__main__':
    which=sys.argv[1]
    lo,hi=int(sys.argv[2]),int(sys.argv[3])
    f={'C3':C3,'C4':C4,'OG':OG,'A11':A11}[which]
    for M in range(lo,hi+1):
        r,mod,nap = solve(M, f(M))
        print(f"M={M:4d} M%8={M%8} {which}: {'SAT' if r else 'UNSAT'}", flush=True)
