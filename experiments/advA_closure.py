"""Independent branch-closure verifier for Theorems L1 and FLIP of main.tex.
Sound rules only: R1-R4 on genuine in-block APs + transitivity. Phase case splits
justified by Lemma 'Phase dichotomy'."""
import itertools, sys

def ladder_edges(vals, d, phase):
    """vals: increasing list forming AP with difference d. phase in {0,1}: leaders are i%2==phase.
       Returns edges (leader -> neighbour)."""
    E=[]
    n=len(vals)
    for i in range(n):
        if i%2==phase:
            for j in (i-1,i+1):
                if 0<=j<n: E.append((vals[i],vals[j]))
    return E

def closure(M, facts, want=None):
    vals=list(range(M+1,2*M+1))
    idx={v:i for i,v in enumerate(vals)}
    n=len(vals)
    # relation matrix as list of bytearrays / python sets of ints
    R=[set() for _ in range(n)]   # R[i] = {j : v_i prec v_j}
    def add(u,v):
        return R[idx[u]].add(idx[v])
    APs=[]
    for b in vals:
        for d in range(1,M):
            a,c=b-d,b+d
            if a in idx and c in idx: APs.append((idx[a],idx[b],idx[c]))
    for (u,v) in facts: add(u,v)
    changed=True
    while changed:
        changed=False
        # transitivity
        for i in range(n):
            Ri=R[i]
            new=set()
            for j in list(Ri):
                new |= R[j]
            new -= Ri
            new.discard(i)
            if new:
                Ri|=new; changed=True
        # AP rules
        for (a,b,c) in APs:
            if a in R and False: pass
            if b in R[a] and c not in R[b]: R[b].add(c) if False else None
        for (a,b,c) in APs:
            # R1: a<b => c<b
            if b in R[a] and b not in R[c]: R[c].add(b); changed=True
            # R3: c<b => a<b
            if b in R[c] and b not in R[a]: R[a].add(b); changed=True
            # R2: b<c => b<a
            if c in R[b] and a not in R[b]: R[b].add(a); changed=True
            # R4: b<a => b<c
            if a in R[b] and c not in R[b]: R[b].add(c); changed=True
    # contradiction?
    contra=[]
    for i in range(n):
        for j in R[i]:
            if i==j or i in R[j]: contra.append((vals[i],vals[j]))
    got=None
    if want is not None:
        got=[(u,v,(idx[v] in R[idx[u]])) for (u,v) in want]
    return contra, got, R, idx, vals

def branches(M, base, pin_odd_phase):
    """yield (label, facts) over the 8 phase combos (odd pinned)."""
    odds=list(range(M+1,2*M+1,2))
    evens=list(range(M+2,2*M+1,2))
    A=[v for v in odds if (v-M)%4==1]
    B=[v for v in odds if (v-M)%4==3]
    for qe in (0,1):
        for qa in (0,1):
            for qb in (0,1):
                f=list(base)
                f+=ladder_edges(odds,2,pin_odd_phase)
                f+=ladder_edges(evens,2,qe)
                f+=ladder_edges(A,4,qa)
                f+=ladder_edges(B,4,qb)
                yield (f"even={qe},A={qa},B={qb}", f)

def run(M):
    m0=3*M//2
    b=lambda j: M+j
    t=lambda i: 2*M-i
    A1=(t(5),b(5)); A2=(t(3),b(6)); A3=(t(10),b(3))
    out=[]
    # ---- L1: assume A2,A3 and S: b3 prec b5 -> contradiction (both cases)
    # S seeds odd ladder: b3=w1 prec b5=w2 -> odd indices lead -> phase=1
    for cname, case in (("I: t5<m0",(t(5),m0)), ("II: m0<t5",(m0,t(5)))):
        allc=[]
        for lbl,f in branches(M, [A2,A3,(b(3),b(5)),case], pin_odd_phase=1):
            contra,_,_,_,_=closure(M,f)
            allc.append((lbl,bool(contra)))
        out.append(("L1 "+cname, all(x[1] for x in allc), [l for l,c in allc if not c]))
    # ---- FLIP: assume A1,A2,A3 and b5 prec b3 -> contradiction
    # b5=w2 prec b3=w1 -> even indices lead -> phase=0
    for cname, case in (("I: t5<m0",(t(5),m0)), ("II: m0<t5",(m0,t(5)))):
        allc=[]
        for lbl,f in branches(M, [A1,A2,A3,(b(5),b(3)),case], pin_odd_phase=0):
            contra,_,_,_,_=closure(M,f)
            allc.append((lbl,bool(contra)))
        out.append(("FLIP "+cname, all(x[1] for x in allc), [l for l,c in allc if not c]))
    return out

if __name__=='__main__':
    for M in [int(x) for x in sys.argv[1:]]:
        print(f"=== M={M} (M%8={M%8}) ===")
        for name,ok,fails in run(M):
            print(f"  {name:16s} all-branches-refuted={ok}  failed={fails}")
