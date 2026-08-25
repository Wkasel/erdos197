"""e99_tower_trace.py -- halving-tower traces of the six C3 values (TASK M2).

================================ HAND DERIVATION ================================

HALVING MAPS.  Let T be an AP-free linear order on (M, 2M], M even.

(1) EVENS  E = {M+2, M+4, ..., 2M},  |E| = M/2.   Map  h_E(v) = v/2.
    Image = {M/2+1, ..., M} = (M/2, M]  -- a STANDARD half-interval.
    h_E is a strictly increasing bijection E -> (M/2, M].
    AP-freeness preserved: a 3-AP a'<b'<c' in (M/2,M] pulls back to
    (2a', 2b', 2c'), equal gaps, inside E subset (M,2M]; the induced order is
    the restriction of T, so relative positions are unchanged; a monotone AP
    downstairs would be a monotone AP upstairs.  QED.

(2) ODDS   O = {M+1, M+3, ..., 2M-1},  |O| = M/2.  Two candidate maps:
      h-(v) = (v-1)/2 : image {M/2, ..., M-1} = [M/2, M-1] = (M/2-1, M-1].
              This is a SHIFTED half-interval: NOT of the form (M', 2M']
              (2*(M/2-1) = M-2 != M-1), so it breaks the uniform bookkeeping.
      h+(v) = (v+1)/2 : image {M/2+1, ..., M} = (M/2, M]  -- EXACTLY the
              standard half-interval, the same target as the evens.
    Both are strictly increasing affine bijections; an affine bijection
    preserves 3-term APs in BOTH directions ((a,b,c) AP  <=>  images AP),
    so AP-freeness is preserved by either (same pullback argument as (1):
    a 3-AP a'<b'<c' in the image pulls back under h+ to
    (2a'-1, 2b'-1, 2c'-1), equal gaps, all odd).
    CANONICAL CHOICE HERE: h+(v) = (v+1)/2, so that BOTH parity cells map
    onto the same half-interval (M/2, M] and the tower is uniform.

TOWER.  Level 1 = (M, 2M].  Level k = (m_k, 2 m_k], m_k = M / 2^{k-1},
reached by k-1 halvings; at each level we choose a parity cell
E (v even, v -> v/2) or O (v odd, v -> (v+1)/2).  Clean descent from level k
needs m_k EVEN (if m is odd the images are shifted intervals as in h- above).
    M == 0 mod 8:  m1=M, m2=M/2, m3=M/4 all even -> THREE clean halvings
                   (levels 1,2,3,4 exist; m4 = M/8).
    M == 4 mod 8:  m3 = M/4 is ODD -> only TWO clean halvings (levels 1,2,3;
                   level 3 is terminal for clean bookkeeping).

OFFSET RECURSION.  Write v = m + db (bottom offset) = 2m - dt (top offset),
db + dt = m, db in [1,m], dt in [0,m-1].
    E-cell (v even):  v/2   = m/2 + db/2        = 2(m/2) - dt/2
                      db -> db/2,        dt -> dt/2.
    O-cell (v odd):   (v+1)/2 = m/2 + (db+1)/2  = 2(m/2) - (dt-1)/2
                      db -> ceil(db/2),  dt -> floor(dt/2).
So bottom-near values stay bottom-near and top-near stay top-near, with the
end-distance halving each level.  CELL PARITY:
    top value:    parity(v) = parity(2 m_k - dt) = parity(dt)
                  -> the cell of a TOP value is RESIDUE-FREE at every level
                     (depends only on its own top offset).
    bottom value: parity(v) = parity(m_k + db)
                  -> at levels 1,2 (m even since M == 0 mod 4) this is
                     parity(db); at LEVEL 3 it is parity(M/4 + db), which
                     READS OFF M mod 8.  This is exactly where the
                     0-mod-8 and 4-mod-8 addresses diverge.

HAND TRACES of the six C3 values (both residues M == 0, 4 mod 8; entries are
value v_k / bottom-or-top offset / cell at that level).  m2=M/2, m3=M/4,
m4=M/8 (level 4 only for M == 0 mod 8).

  value      L1 (m1=M)         L2 (m2=M/2)        L3 (m3=M/4)             L4 (m4=M/8)
  b3=M+3     db=3  cell O      v=m2+2 db=2 E      v=m3+1 db=1  0(8): O    v=m4+1 db=1
                                                              4(8): E    --
  b5=M+5     db=5  cell O      v=m2+3 db=3 O      v=m3+2 db=2  0(8): E    v=m4+1 db=1
                                                              4(8): O    --
  b6=M+6     db=6  cell E      v=m2+3 db=3 O      v=m3+2 db=2  0(8): E    v=m4+1 db=1
                                                              4(8): O    --
  t3=2M-3    dt=3  cell O      v=2m2-1 dt=1 O     v=2m3 dt=0   E (both)   v=2m4   dt=0
  t5=2M-5    dt=5  cell O      v=2m2-2 dt=2 E     v=2m3-1 dt=1 O (both)   v=2m4   dt=0
  t10=2M-10  dt=10 cell E      v=2m2-5 dt=5 O     v=2m3-2 dt=2 E (both)   v=2m4-1 dt=1

BRANCH PATHS (cells at levels 1,2,3):
  M == 0 mod 8:  b3: O,E,O   b5: O,O,E   b6: E,O,E
                 t3: O,O,E   t5: O,E,O   t10: E,O,E
  M == 4 mod 8:  b3: O,E,E   b5: O,O,O   b6: E,O,O
                 t3: O,O,E   t5: O,E,O   t10: E,O,E

DIFFERING CELLS (the key question, part 1).  The two residues' address
tables agree EVERYWHERE except in the LEVEL-3 CELL of the three BOTTOM
values, each of which flips:
      b3: O (0 mod 8)  <->  E (4 mod 8)
      b5: E (0 mod 8)  <->  O (4 mod 8)
      b6: E (0 mod 8)  <->  O (4 mod 8)
All values v_k, all offsets, all level-1/2 cells, and ALL cells of the top
values t3, t5, t10 are residue-independent (tops: cell = parity(dt), which
never sees M).

CO-RESIDENCY (same cell = same branch path, i.e. both values survive into
the same level-(k+1) suborder).
  depth 1 (level-1 cells): O = {b3, b5, t3, t5},  E = {b6, t10}.
  depth 2 (paths, both residues): OE = {b3, t5}, OO = {b5, t3}, EO = {b6, t10}
      -- the three CROSSED top/bottom pairs, already paired off at depth 2.
  depth 3:
      M == 0 mod 8:  OEO = {b3, t5},  OOE = {b5, t3},  EOE = {b6, t10}
          -- the crossed pairs SURVIVE a third halving, landing at the
             extreme ends of the level-4 interval: every bottom at m4+1
             (the bottom element), tops at 2m4, 2m4, 2m4-1 (the top).
      M == 4 mod 8:  OEE={b3} OOO={b5} EOO={b6} OOE={t3} OEO={t5} EOE={t10}
          -- SIX SINGLETONS: every co-resident pair is destroyed at the
             level-3 descent (in each depth-2 cell the two residents have
             opposite level-3 parities).

C3 PRECEDENCES IN THE SAME CELL (the key question, part 2).
The precedence pairs are (t5 -> b5), (t3 -> b6), (t10 -> b3)  (top before
bottom).  Parities: t3, t5, b3, b5 odd; t10, b6 even.  Hence:
  * (t5, b5): both in the level-1 O cell -- the ONLY precedence pair that is
    co-resident below the root.  It descends into the level-2 O-suborder as
    the induced constraint  "2m2-2 before m2+3"  (i.e. t2' before b3' in
    level-2 coordinates).  At level 2 the pair splits (t5 even, b5 odd).
  * (t3, b6) and (t10, b3): opposite parities, split at level 1; no
    level-local conflict from a single precedence at any depth.
So a SINGLE precedence gives a level-local constraint only for (t5,b5) at
level 2.  The residue-separating structure is instead carried by the CROSSED
pairs: the precedences connect the three depth-3 cells in a directed 3-CYCLE
      OEO --(t5>b5)--> OOE --(t3>b6)--> EOE --(t10>b3)--> OEO
(source cell of the top -> cell of the target bottom).  For M == 0 mod 8 all
three cells are genuinely 2-element (top + bottom co-resident, straddling the
whole level-4 interval), closing the cycle after three halvings; for
M == 4 mod 8 the six values sit in six distinct depth-3 cells and the cycle
degenerates.  This matches the machine dichotomy (UNSAT iff M == 0 mod 8).

MACHINE VERIFICATION BELOW:
  A. arithmetic lemmas: h_E, h+, h- are increasing bijections onto the stated
     intervals and preserve 3-APs both ways (exhaustive, M = 8..96).
  B. SAT (lazy transitivity, Cadical195): at M = 40, 44, 48, 52 find AP-free
     orders (with the C3 precedences added at M = 44, 52 where SAT), then
     restrict/halve along EVERY branch of the tower (3 halvings when
     m even permits, using h+ for odds) and brute-check every induced order
     is AP-free; also check h- images are AP-free at level 1.
  C. verify the address table above numerically at M = 40, 44, 48, 52
     (trace via parity, compare against the closed-form table).
  D. verify the co-residency / differing-cell / precedence-cell claims.
  E. in the C3-SAT orders (M = 44, 52): check the descended (t5,b5)
     constraint really holds in the level-2 O-suborder (M-2 before M/2+3).
"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

C3 = [("t5", "b5"), ("t3", "b6"), ("t10", "b3")]          # top before bottom

def c3_values(M):
    return {"b3": M + 3, "b5": M + 5, "b6": M + 6,
            "t3": 2 * M - 3, "t5": 2 * M - 5, "t10": 2 * M - 10}

# ---------------------------------------------------------------- tracing
def halve(v):
    """Canonical halving map: E-cell v/2, O-cell (v+1)/2."""
    return v // 2 if v % 2 == 0 else (v + 1) // 2

def trace(M, v, max_halvings=3):
    """Numeric tower trace of value v on (M,2M]. Returns list of records
    (level, m, v, cell, db, dt); cell is None on a terminal level."""
    recs, m, lvl = [], M, 1
    for _ in range(max_halvings):
        cell = "E" if v % 2 == 0 else "O"
        recs.append((lvl, m, v, cell, v - m, 2 * m - v))
        if m % 2 != 0:
            recs[-1] = (lvl, m, v, None, v - m, 2 * m - v)  # cannot descend
            return recs
        v, m, lvl = halve(v), m // 2, lvl + 1
    recs.append((lvl, m, v, "E" if v % 2 == 0 else "O", v - m, 2 * m - v))
    return recs

def predicted_table(M):
    """Closed-form table from the hand derivation. Entries:
    name -> list of (level, m, v, cell, db, dt)."""
    r = M % 8
    assert r in (0, 4)
    m2, m3 = M // 2, M // 4
    b3c, b56c = ("O", "E") if r == 0 else ("E", "O")   # level-3 bottom cells
    P = {
      "b3":  [(1, M, M + 3, "O", 3, M - 3), (2, m2, m2 + 2, "E", 2, m2 - 2),
              (3, m3, m3 + 1, b3c, 1, m3 - 1)],
      "b5":  [(1, M, M + 5, "O", 5, M - 5), (2, m2, m2 + 3, "O", 3, m2 - 3),
              (3, m3, m3 + 2, b56c, 2, m3 - 2)],
      "b6":  [(1, M, M + 6, "E", 6, M - 6), (2, m2, m2 + 3, "O", 3, m2 - 3),
              (3, m3, m3 + 2, b56c, 2, m3 - 2)],
      "t3":  [(1, M, 2*M - 3, "O", M - 3, 3), (2, m2, 2*m2 - 1, "O", m2 - 1, 1),
              (3, m3, 2*m3, "E", m3, 0)],
      "t5":  [(1, M, 2*M - 5, "O", M - 5, 5), (2, m2, 2*m2 - 2, "E", m2 - 2, 2),
              (3, m3, 2*m3 - 1, "O", m3 - 1, 1)],
      "t10": [(1, M, 2*M - 10, "E", M - 10, 10), (2, m2, 2*m2 - 5, "O", m2 - 5, 5),
              (3, m3, 2*m3 - 2, "E", m3 - 2, 2)],
    }
    if r == 0:
        m4 = M // 8
        l4 = {"b3": m4 + 1, "b5": m4 + 1, "b6": m4 + 1,
              "t3": 2 * m4, "t5": 2 * m4, "t10": 2 * m4 - 1}
        for k, v4 in l4.items():
            P[k].append((4, m4, v4, "E" if v4 % 2 == 0 else "O",
                         v4 - m4, 2 * m4 - v4))
    else:
        # level 3 terminal (m3 odd): cell recorded above is the level-3
        # parity, but no clean descent exists -> numeric trace stores None.
        P = {k: recs[:2] + [(3, m3, recs[2][2], None, recs[2][4], recs[2][5])]
             for k, recs in P.items()}
        # keep the *parity* separately for the differing-cell claim:
    return P

def level3_parity_cell(M, name):
    v3 = trace(M, c3_values(M)[name])[2][2]
    return "E" if v3 % 2 == 0 else "O"

# ------------------------------------------------- A. arithmetic lemmas
def check_affine_lemmas(Ms):
    for M in Ms:
        assert M % 2 == 0
        E = list(range(M + 2, 2 * M + 1, 2))
        O = list(range(M + 1, 2 * M, 2))
        half = list(range(M // 2 + 1, M + 1))
        assert [v // 2 for v in E] == half                    # h_E onto (M/2,M]
        assert [(v + 1) // 2 for v in O] == half              # h+  onto (M/2,M]
        assert [(v - 1) // 2 for v in O] == list(range(M // 2, M))  # h- shifted
        for cls, h in ((E, lambda v: v // 2), (O, lambda v: (v + 1) // 2),
                       (O, lambda v: (v - 1) // 2)):
            s = set(cls)
            for a in cls:                       # forward: class AP -> image AP
                for d in range(2, 2 * M, 2):    # same-parity APs have even d
                    if a + 2 * d > 2 * M: break
                    if a + d in s and a + 2 * d in s:
                        assert h(a + d) - h(a) == h(a + 2 * d) - h(a + d)
            img = sorted(h(v) for v in cls)     # backward: image AP -> class AP
            si, inv = set(img), {h(v): v for v in cls}
            for a in img:
                for d in range(1, M):
                    if a + 2 * d > img[-1]: break
                    if a + d in si and a + 2 * d in si:
                        x, y, z = inv[a], inv[a + d], inv[a + 2 * d]
                        assert y - x == z - y
    print(f"[A] affine halving lemmas OK for M in {Ms[0]}..{Ms[-1]} even "
          "(h_E, h+, h- are AP-preserving bijections; h_E,h+ -> (M/2,M], "
          "h- -> [M/2,M-1])")

# ------------------------------------------------- B. SAT machinery
def solve_order(M, add_c3):
    """AP-free order on (M,2M] via lazy transitivity (e89 style).
    Returns list of values in position order (earliest first) or None."""
    V = list(range(M + 1, 2 * M + 1)); n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    var, c = {}, 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1; var[(i, j)] = c
    def o(u, w):
        i, j = idx[u], idx[w]
        return var[(i, j)] if i < j else -var[(j, i)]
    cl = []
    for y in V:
        d = 1
        while y + d <= 2 * M:
            x, z = y - d, y + d
            d += 1
            if x > M:
                cl.append([-o(x, y), -o(y, z)])   # no rising monotone AP
                cl.append([-o(z, y), -o(y, x)])   # no falling monotone AP
    if add_c3:
        val = c3_values(M)
        for t, b in C3:
            cl.append([o(val[t], val[b])])
    sol = Cadical195(bootstrap_with=cl)
    while True:
        if not sol.solve():
            return None
        model = set(l for l in sol.get_model() if l > 0)
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in var.items():
            if lit in model: B[i, j] = True
            else: B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
        def lit(p, q):
            return var[(p, q)] if p < q else -var[(q, p)]
        new = []
        for i, j in zip(*np.nonzero(miss)):
            k = int(np.nonzero(B[i] & B[:, j])[0][0])
            new.append([-lit(int(i), k), -lit(k, int(j)), lit(int(i), int(j))])
        if not new:
            wins = B.sum(axis=1)
            return [V[i] for i in sorted(range(n), key=lambda i: -int(wins[i]))]
        sol.append_formula(new)

def is_ap_free(seq):
    """seq = values in position order; check no monotone 3-AP."""
    pos = {v: i for i, v in enumerate(seq)}
    vals = sorted(seq); s = set(vals)
    for a in vals:
        d = 1
        while a + 2 * d <= vals[-1]:
            b, c = a + d, a + 2 * d
            d += 1
            if b in s and c in s:
                pa, pb, pc = pos[a], pos[b], pos[c]
                if pa < pb < pc or pa > pb > pc:
                    return False
    return True

def tower_check(order, m, path, depth, report):
    """Recursively halve `order` on (m,2m] along all parity branches,
    checking AP-freeness everywhere; `depth` halvings remain."""
    assert is_ap_free(order), f"AP violated at branch {path or 'root'}"
    report.append((path or "root", m, len(order)))
    if depth == 0 or m % 2 != 0:
        return
    for parity, tag in ((0, "E"), (1, "O")):
        sub = [v for v in order if v % 2 == parity]
        img = [v // 2 if parity == 0 else (v + 1) // 2 for v in sub]
        assert sorted(img) == list(range(m // 2 + 1, m + 1))
        tower_check(img, m // 2, path + tag, depth - 1, report)

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    check_affine_lemmas(list(range(8, 98, 2)))

    for M in (40, 44, 48, 52):
        r = M % 8
        val = c3_values(M)

        # --- C. address table: numeric trace vs closed-form prediction
        P = predicted_table(M)
        for name, v in val.items():
            tr = trace(M, v)
            assert tr == P[name], (M, name, tr, P[name])
        print(f"\n[C] M={M} (== {r} mod 8): address table verified "
              f"(numeric trace == closed form)")
        hdr = "  {:>4} | ".format("val") + " | ".join(
            f"L{l}: v/cell/db/dt" for l in range(1, len(P['t3']) + 1))
        print(hdr)
        for name in ("b3", "b5", "b6", "t3", "t5", "t10"):
            cells = "  {:>4} | ".format(name) + " | ".join(
                f"{v}/{c or '-'}/{db}/{dt}" for (_, m, v, c, db, dt) in P[name])
            print(cells)

        # --- D. branch paths, co-residency, differing cells, precedences
        paths = {}
        for name, v in val.items():
            tr = trace(M, v)
            cells3 = [rec[3] for rec in tr[:3]]
            if cells3[2] is None:                       # terminal level 3:
                cells3[2] = level3_parity_cell(M, name)  # record parity anyway
            paths[name] = "".join(cells3)
        by = {}
        for name, p in paths.items():
            for k in (1, 2, 3):
                by.setdefault((k, p[:k]), []).append(name)
        d3 = {p: sorted(ns) for (k, p), ns in by.items() if k == 3}
        d2 = {p: sorted(ns) for (k, p), ns in by.items() if k == 2}
        assert d2 == {"OE": ["b3", "t5"], "OO": ["b5", "t3"],
                      "EO": ["b6", "t10"]}, d2
        if r == 0:
            assert d3 == {"OEO": ["b3", "t5"], "OOE": ["b5", "t3"],
                          "EOE": ["b6", "t10"]}, d3
            assert paths["b3"][2] == "O" and paths["b5"][2] == "E" \
                   and paths["b6"][2] == "E"
        else:
            assert all(len(v) == 1 for v in d3.values()) and len(d3) == 6, d3
            assert paths["b3"][2] == "E" and paths["b5"][2] == "O" \
                   and paths["b6"][2] == "O"
        for name in ("t3", "t5", "t10"):     # top cells residue-free
            assert paths[name] == {"t3": "OOE", "t5": "OEO", "t10": "EOE"}[name]
        # precedence-pair co-residency: only (t5,b5) shares even depth 1
        share = {(t, b): next((k for k in (3, 2, 1)
                               if paths[t][:k] == paths[b][:k]), 0)
                 for t, b in C3}
        assert share == {("t5", "b5"): 1, ("t3", "b6"): 0, ("t10", "b3"): 0}
        print(f"[D] M={M}: paths {paths}; depth-2 cells {d2}; "
              f"depth-3 cells {d3}; precedence shared-prefix depths {share}")

        # --- B. SAT tower: AP-free (+C3 where SAT) order, halve everywhere
        add_c3 = (r == 4)                    # C3 is UNSAT for r == 0 (known)
        order = solve_order(M, add_c3=add_c3)
        assert order is not None, f"M={M} unexpectedly UNSAT"
        report = []
        tower_check(order, M, "", 3, report)
        print(f"[B] M={M}: SAT order ({'AP+C3' if add_c3 else 'AP only'}), "
              f"tower AP-free at all {len(report)} nodes: "
              f"{[p for p, _, _ in report]}")
        hm = [(v - 1) // 2 for v in order if v % 2 == 1]     # h- variant, L1
        assert is_ap_free(hm)
        if add_c3:
            # --- E. descended (t5,b5) constraint in the level-2 O-suborder
            sub = [(v + 1) // 2 for v in order if v % 2 == 1]
            pos = {v: i for i, v in enumerate(sub)}
            assert pos[M - 2] < pos[M // 2 + 3], "descended t5<b5 violated"
            print(f"[E] M={M}: level-2 O-suborder has {M-2} before "
                  f"{M//2+3} (descended t5<b5) -- OK")
    print(f"\nall checks passed ({time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
