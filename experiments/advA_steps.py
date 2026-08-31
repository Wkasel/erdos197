import sys
sys.path.insert(0,'/private/tmp/claude-501/-Users-will-Dev-personal-tasks-math/2817dd94-f30a-4336-b6a4-72727bffa320/scratchpad')
from advA_closure import closure, ladder_edges

def lad(M):
    odds=list(range(M+1,2*M+1,2)); evens=list(range(M+2,2*M+1,2))
    A=[v for v in odds if (v-M)%4==1]; B=[v for v in odds if (v-M)%4==3]
    return odds,evens,A,B

def chk(M,name,facts,goals):
    contra,got,R,idx,vals=closure(M,facts,want=goals)
    bad=[(u,v) for (u,v,ok) in got if not ok]
    print(f"  M={M} {name}: derived={len(goals)-len(bad)}/{len(goals)}"
          + (f"  MISSING={bad}" if bad else "  OK") + (f"  [branch already contradictory]" if contra else ""))
    return not bad

def run(M):
    odds,evens,A,B=lad(M); m0=3*M//2
    b=lambda j:M+j; t=lambda i:2*M-i
    print(f"### M={M}")
    # ---- POLAR (odd ladder phase pinned): L1 uses phase 1 (S), FLIP uses phase 0
    for ph,tag in ((1,'L1(S)'),(0,'FLIP')):
        oe=ladder_edges(odds,2,ph)
        # inward: t5 prec m0  => every odd prec m0
        chk(M,f"POLAR-inward {tag}", oe+[(t(5),m0)], [(w,m0) for w in odds])
        chk(M,f"POLAR-outward {tag}", oe+[(m0,t(5))], [(m0,w) for w in odds])
    # ---- L1 case I step1: G4-inward at c*=m0+1 over class B  => b3 prec c*
    oe1=ladder_edges(odds,2,1)
    for q in (0,1):
        chk(M,f"L1-I(1) G4-inward c*=m0+1 classB phase{q}", oe1+ladder_edges(B,4,q), [(b(3),m0+1)])
    # ---- L1 case I step2: P2-outward at c* over evens, seed c* prec m0 => c* prec t10
    for q in (0,1):
        chk(M,f"L1-I(2) P2-outward c*=m0+1 even phase{q}", ladder_edges(evens,2,q)+[(m0+1,m0)], [(m0+1,t(10))])
    # ---- L1 case II step1: G4-outward at c**=m0-1 over class A => c** prec t3
    for q in (0,1):
        chk(M,f"L1-II(1) G4-outward c**=m0-1 classA phase{q}", oe1+ladder_edges(A,4,q), [(m0-1,t(3))])
    # ---- L1 case II step2: P2-inward at c** over evens, seed m0 prec c** => b6 prec c**
    for q in (0,1):
        chk(M,f"L1-II(2) P2-inward c**=m0-1 even phase{q}", ladder_edges(evens,2,q)+[(m0,m0-1)], [(b(6),m0-1)])
    # ---- FLIP case I
    oe0=ladder_edges(odds,2,0)
    for q in (0,1):
        chk(M,f"FLIP-I(1) P2-outward m0-1 even phase{q}", ladder_edges(evens,2,q)+[(m0-1,m0)], [(m0-1,t(10))])
    for q in (0,1):
        chk(M,f"FLIP-I(5) G4-inward m0-1 classA phase{q}", oe0+ladder_edges(A,4,q), [(b(5),m0-1)])
    # ---- FLIP case II
    for q in (0,1):
        chk(M,f"FLIP-II(1) P2-inward m0+1 even phase{q}", ladder_edges(evens,2,q)+[(m0,m0+1)], [(b(6),m0+1)])
    for q in (0,1):
        chk(M,f"FLIP-II(5) G4-outward m0+1 classB phase{q}", oe0+ladder_edges(B,4,q), [(m0+1,t(5))])

for M in [int(x) for x in sys.argv[1:]]: run(M)
