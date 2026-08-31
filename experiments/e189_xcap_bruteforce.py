"""Brute-force verification of two order laws for Erdos #197.

Setup: N = [1..n], 2-colored A/B, each team given a total order (a
"prefix order" = an initial segment of an omega-order).  A configuration is
ADMISSIBLE if neither team contains a monotone 3-AP entirely inside [1,n].

Law GL (generalized center cap):  for every v in T,
    #{x in T : x<v, pos(x)<pos(v), 2v-x in T, 2v-x <= n}  <=  H_T(v)
    where H_T(v) = #{z in T : v<z<2v, z<=n, pos(z)<pos(v)}.

Law XCAP (cross-reflection cap at H=0 centers): if v in A with H_A(v)=0 and
v' in B with H_B(v')=0 then there is NO pair (x,y), x in A placed before v
with x<v, y in B placed before v' with y<v', such that 2v-x = 2v'-y <= n.

Both are claimed THEOREMS; this script tries to falsify them.
"""
import itertools, sys

def mono_ap_free(order, members):
    """order: list of values in placement order; members: set."""
    pos = {v: i for i, v in enumerate(order)}
    vals = sorted(members)
    for i, a in enumerate(vals):
        for b in vals[i+1:]:
            c = 2*b - a
            if c in members:
                pa, pb, pc = pos[a], pos[b], pos[c]
                if (pa < pb < pc) or (pc < pb < pa):
                    return False
    return True

def check(n, verbose=False):
    vals = list(range(1, n+1))
    gl_viol = xcap_viol = 0
    configs = 0
    for mask in range(1 << n):
        A = {v for i, v in enumerate(vals) if mask >> i & 1}
        B = set(vals) - A
        if not A or not B:
            continue
        ordersA = [o for o in itertools.permutations(sorted(A)) if mono_ap_free(o, A)]
        if not ordersA:
            continue
        ordersB = [o for o in itertools.permutations(sorted(B)) if mono_ap_free(o, B)]
        if not ordersB:
            continue
        for oA in ordersA:
            posA = {v: i for i, v in enumerate(oA)}
            for oB in ordersB:
                posB = {v: i for i, v in enumerate(oB)}
                configs += 1
                # ---- Law GL, both teams
                for (T, pos) in ((A, posA), (B, posB)):
                    for v in T:
                        H = sum(1 for z in T if v < z < 2*v and z <= n and pos[z] < pos[v])
                        D = sum(1 for x in T if x < v and pos[x] < pos[v]
                                and (2*v - x) in T and 2*v - x <= n)
                        if D > H:
                            gl_viol += 1
                            if verbose:
                                print("GL VIOL", sorted(A), oA, oB, v, D, H)
                # ---- Law XCAP at H=0 centers
                zeroA = [v for v in A
                         if not any(v < z < 2*v and z <= n and posA[z] < posA[v] for z in A)]
                zeroB = [v for v in B
                         if not any(v < z < 2*v and z <= n and posB[z] < posB[v] for z in B)]
                for v in zeroA:
                    Pv = [x for x in A if x < v and posA[x] < posA[v]]
                    for w in zeroB:
                        Pw = [y for y in B if y < w and posB[y] < posB[w]]
                        refl_v = {2*v - x for x in Pv if 2*v - x <= n}
                        refl_w = {2*w - y for y in Pw if 2*w - y <= n}
                        clash = refl_v & refl_w
                        if clash:
                            xcap_viol += 1
                            if verbose:
                                print("XCAP VIOL", sorted(A), oA, oB, v, w, clash)
    return configs, gl_viol, xcap_viol

for n in range(3, 10):
    c, g, x = check(n, verbose=(n <= 9))
    print(f"n={n}: admissible (coloring,orderA,orderB) configs={c}  GL violations={g}  XCAP violations={x}")
    sys.stdout.flush()
