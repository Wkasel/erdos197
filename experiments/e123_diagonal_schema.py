"""e123_diagonal_schema: FRONT N2 step 3 -- the C3 hand-proof skeleton
(Z / D / E / P, notes/33) generalized to the whole DIAGONAL family.

For every odd p >= 5 let x = 3p and consider the pair {x, x+1} with the
diagonal core

    C3(p) = { A1: t_p < b_p,          (attacker x,   j = p)
              A2: t_{p-2} < b_{p+1},  (attacker x,   j = p+1)
              A3: t_{p+5} < b_{p-2} } (attacker x+1, j = p-2)

(C3(5) is the original C3 of notes/33).  The claim verified here,
schema-level, rung-by-rung, with the e113 strictness (every AP checked,
every leader/trailer claim asserted, both branches of every phase
dichotomy, hypothesis audit per branch):

  LAYER-1(p):  M = 0 mod 4:  AP-free + A2 + A3 force b_p < b_{p-2}
    (refute S: b_{p-2} < b_p; ODD2 leaders = offsets p-2 mod 4;
     c* = the element of {m0-1, m0+1} = p mod 4 (exists for every
     M = 0 mod 4), c** = the other one;
     Case I (t_p < m0): G4-inward at c* over offset-class (p-2) mod 4:
       b_{p-2} < c*; P2-outward at c*: c* < t_{p+5}; A3 closes 3-cycle.
     Case II (m0 < t_p): G4-outward at c** over offset-class (2-p) mod 4:
       c** < t_{p-2}; P2-inward at c**: b_{p+1} < c**; A2 closes.)

  FLIP(p):  M/2 = p+3 mod 4  (i.e. M = 0 mod 8 when p = 1 mod 4,
    M = 4 mod 8 when p = 3 mod 4):  AP-free + A1 + A2 + A3 +
    (b_p < b_{p-2}) is contradictory
    (ODD2 leaders = offsets p mod 4; Case I: P2-out at m0-1 -> t_{p+5},
     A3, mirror AP (b_{p-2}, m0-1, t_p), A1, then G4-inward at m0-1
     over offset-class p mod 4 kills b_p; Case II: P2-in at m0+1 ->
     b_{p+1}, A2, mirror AP (b_p, m0+1, t_{p-2}), A1, then G4-outward
     at m0+1 over offset-class (-p) mod 4 kills t_p.)

  SHARPNESS(p): at M/2 = p+1 mod 4 the flip schema is inapplicable
    (the centers m0-+1 land in the wrong mod-4 classes and the ODD2
    leader statuses invert) -- and AP + C3(p) is in fact SAT there
    (checked by solver in e122).

  ==> AP + C3(p) is UNSAT for all M = 2(p+3) mod 16... precisely:
      M = 0 mod 4 gives layer 1; the flip class within it is
      M/2 = p+3 mod 4.  Together: the diagonal core kills its pair on
      one full residue class mod 8, for EVERY p -- same skeleton, same
      lemmas, constants shifted by p.

The machinery (Ctx, audit, lemma_Z, fiat_zig, lemma_P) is e113's,
verbatim; only the offset constants and residue conditions are
parametrized by p.

Run: .venv/bin/python experiments/e123_diagonal_schema.py [pmax]
Output: data/e123_diagonal_schema.json
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = str(ROOT / "data" / "e123_diagonal_schema.json")


class Ctx:
    """Fact store with strict rule application (e113 verbatim)."""

    def __init__(self, M):
        self.M = M
        self.facts = set()
        self.assumed = set()
        self.derived = set()

    def inside(self, v):
        return self.M < v <= 2 * self.M

    def add(self, u, v):
        assert self.inside(u) and self.inside(v) and u != v, (self.M, u, v)
        self.facts.add((u, v))
        self.derived.add((u, v))

    def assume(self, u, v):
        assert self.inside(u) and self.inside(v) and u != v, (self.M, u, v)
        self.facts.add((u, v))
        self.assumed.add((u, v))

    def assume_all(self, pairs):
        for (u, v) in pairs:
            self.assume(u, v)

    def has(self, u, v):
        return (u, v) in self.facts

    def ap_ok(self, x, y, z):
        assert x < y < z and x + z == 2 * y, (x, y, z)
        assert self.inside(x) and self.inside(z), (self.M, x, z)

    def rule(self, x, y, z, prem, conc):
        self.ap_ok(x, y, z)
        assert self.has(*prem), (self.M, 'missing premise', prem)
        p, c = prem, conc
        valid = (
            (p == (x, y) and c == (z, y)) or   # R1
            (p == (z, y) and c == (x, y)) or   # R3
            (p == (y, x) and c == (y, z)) or   # R4
            (p == (y, z) and c == (y, x)))     # R2
        assert valid, (self.M, x, y, z, prem, conc)
        self.add(*conc)

    def trans(self, u, v, w):
        assert self.has(u, v) and self.has(v, w), (self.M, u, v, w)
        self.add(u, w)


def audit(ctx, hypotheses):
    hyp = set(hypotheses)
    assert ctx.assumed == hyp, (ctx.M, ctx.assumed ^ hyp)
    assert ctx.facts == ctx.assumed | ctx.derived, \
        (ctx.M, ctx.facts - (ctx.assumed | ctx.derived))


def fiat_edges(first, d, count, leader_first):
    lad = [first + i * d for i in range(count)]
    e0 = 0 if leader_first else 1
    return {(lad[i], lad[j]) for i in range(e0, count, 2)
            for j in (i - 1, i + 1) if 0 <= j < count}


def lemma_Z(ctx, first, d, count, seed):
    lad = [first + i * d for i in range(count)]
    assert all(ctx.inside(v) for v in lad)
    su, sv = seed
    assert ctx.has(su, sv)
    i, j = lad.index(su), lad.index(sv)
    assert abs(i - j) == 1
    e = i
    if 0 <= 2 * i - j < count:
        x, y, z = sorted([lad[j], lad[i], lad[2 * i - j]])
        ctx.rule(x, y, z, (lad[i], lad[j]), (lad[i], lad[2 * i - j]))
    k = e
    while k + 2 < count:
        x, y, z = sorted([lad[k], lad[k + 1], lad[k + 2]])
        ctx.rule(x, y, z, (lad[k], lad[k + 1]), (lad[k + 2], lad[k + 1]))
        if k + 3 < count:
            x, y, z = sorted([lad[k + 1], lad[k + 2], lad[k + 3]])
            ctx.rule(x, y, z, (lad[k + 2], lad[k + 1]),
                     (lad[k + 2], lad[k + 3]))
        k += 2
    k = e
    while k - 2 >= 0:
        x, y, z = sorted([lad[k], lad[k - 1], lad[k - 2]])
        ctx.rule(x, y, z, (lad[k], lad[k - 1]), (lad[k - 2], lad[k - 1]))
        if k - 3 >= 0:
            x, y, z = sorted([lad[k - 1], lad[k - 2], lad[k - 3]])
            ctx.rule(x, y, z, (lad[k - 2], lad[k - 1]),
                     (lad[k - 2], lad[k - 3]))
        k -= 2
    return {lad[i2] for i2 in range(e % 2, count, 2)}


def fiat_zig(ctx, first, d, count, leader_first):
    lad = [first + i * d for i in range(count)]
    assert all(ctx.inside(v) for v in lad)
    e0 = 0 if leader_first else 1
    leaders = set()
    for i in range(e0, count, 2):
        leaders.add(lad[i])
        if i > 0:
            ctx.assume(lad[i], lad[i - 1])
        if i + 1 < count:
            ctx.assume(lad[i], lad[i + 1])
    return leaders


def lemma_P(ctx, c, g, leaders, seed, direction, targets):
    M = ctx.M
    step = g

    def in_class(v):
        return (v - c) % g == g // 2 and ctx.inside(v)

    v0, tag = seed
    assert in_class(v0), (M, c, v0)
    e0 = abs(v0 - c)
    assert ctx.inside(2 * c - v0), (M, c, v0, 'seed mirror outside')
    out = (tag == 'out')
    lo, hi = min(v0, 2 * c - v0), max(v0, 2 * c - v0)
    if out:
        assert ctx.has(c, v0)
        ctx.rule(lo, c, hi, (c, v0), (c, 2 * c - v0))
    else:
        assert ctx.has(v0, c)
        ctx.rule(lo, c, hi, (v0, c), (2 * c - v0, c))
    covered = {e0}

    def leader(v):
        return v in leaders

    def pair_ok(e):
        return ctx.inside(c - e) and ctx.inside(c + e)

    e = e0
    while pair_ok(e + step):
        if out:
            cand = [s for s in (+1, -1) if leader(c + s * e)]
            assert len(cand) == 1, (M, c, e, 'leader count', cand)
            s = cand[0]
            u, u_out = c + s * e, c + s * (e + step)
            assert ctx.has(u, u_out), (M, c, e, 'zig edge missing')
            ctx.trans(c, u, u_out)
            lo, hi = min(u_out, 2 * c - u_out), max(u_out, 2 * c - u_out)
            ctx.rule(lo, c, hi, (c, u_out), (c, 2 * c - u_out))
        else:
            cand = [s for s in (+1, -1) if leader(c + s * (e + step))]
            assert len(cand) == 1, (M, c, e, 'leader count in', cand)
            s = cand[0]
            v, v_in = c + s * (e + step), c + s * e
            assert ctx.has(v, v_in), (M, c, e, 'zig edge missing in')
            ctx.trans(v, v_in, c)
            lo, hi = min(v, 2 * c - v), max(v, 2 * c - v)
            ctx.rule(lo, c, hi, (v, c), (2 * c - v, c))
        e += step
        covered.add(e)
    e = e0
    while e - step >= step // 2 and e - step > 0:
        if out:
            cand = [s for s in (+1, -1) if not leader(c + s * (e - step))]
            assert len(cand) == 1, (M, c, e, 'trailer count', cand)
            s = cand[0]
            w, w_out = c + s * (e - step), c + s * e
            assert leader(w_out)
            assert ctx.has(w_out, w), (M, c, e, 'zig edge missing down')
            ctx.trans(c, w_out, w)
            lo, hi = min(w, 2 * c - w), max(w, 2 * c - w)
            ctx.rule(lo, c, hi, (c, w), (c, 2 * c - w))
        else:
            cand = [s for s in (+1, -1) if leader(c + s * (e - step))]
            assert len(cand) == 1, (M, c, e, 'leader count down', cand)
            s = cand[0]
            w, w_out = c + s * (e - step), c + s * e
            assert ctx.has(w, w_out)
            ctx.trans(w, w_out, c)
            lo, hi = min(w, 2 * c - w), max(w, 2 * c - w)
            ctx.rule(lo, c, hi, (w, c), (2 * c - w, c))
        e -= step
        covered.add(e)
    for t in targets:
        e = abs(t - c)
        assert e in covered, (M, c, t, 'target not covered')
        assert (ctx.has(c, t) if out else ctx.has(t, c)), (M, c, t)
    return covered


def odd_ladder(M):
    return M + 1, 2, M // 2


def even_ladder(M):
    return M + 2, 2, M // 2


def lad4(M, a):
    first = M + a
    count = (2 * M - first) // 4 + 1
    return first, 4, count


def polar(ctx, M, p, odd_leaders, direction):
    """P2 flood at m0 over the odd class, seeded by the split value t_p."""
    m0 = 3 * M // 2
    tp = 2 * M - p
    tag = 'out' if direction == 'lead' else 'in'
    odds = [v for v in range(M + 1, 2 * M + 1, 2)]
    targets = [v for v in odds if ctx.inside(3 * M - v)]
    lemma_P(ctx, m0, 2, odd_leaders, (tp, tag), direction, targets)
    return targets


def check_layer1(M, p):
    """LAYER-1(p) at scale M = 0 mod 4."""
    assert M % 4 == 0 and p % 2 == 1 and p >= 5
    m0 = 3 * M // 2
    tp, tp2, tp5 = 2 * M - p, 2 * M - (p - 2), 2 * M - (p + 5)
    bp, bp2, bp1 = M + p, M + (p - 2), M + (p + 1)

    def base():
        ctx = Ctx(M)
        ctx.assume_all([(tp2, bp1), (tp5, bp2), (bp2, bp)])
        return ctx

    AX = frozenset({(tp2, bp1), (tp5, bp2), (bp2, bp)})

    def with_odd2(ctx):
        L = lemma_Z(ctx, *odd_ladder(M), (bp2, bp))
        assert all((v - M) % 4 == (p - 2) % 4 for v in L)
        return L

    # centers: c* = p mod 4 among m0 -+ 1 (G4 center for the class of
    # b_{p-2}); c** = the other (= -p mod 4, G4 center for class of
    # t_{p-2}, itself an ODD2 leader).
    cands = [m0 - 1, m0 + 1]
    cs = [c for c in cands if c % 4 == p % 4]
    assert len(cs) == 1, (M, p)
    cstar = cs[0]
    cstar2 = cands[0] if cstar == cands[1] else cands[1]
    assert cstar2 % 4 == (-p) % 4

    assert tp % 2 == 1 and m0 % 2 == 0 and tp != m0
    discharged = set()

    aB = (p - 2) % 4          # offset class of b_{p-2}
    aA = (2 - p) % 4          # offset class of t_{p-2}
    # ---- Case I: t_p < m0 ----
    for lf in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.assume(tp, m0)
        polar(ctx, M, p, L, 'trail')
        assert (cstar - 2) in L and (cstar + 2) in L
        assert ctx.has(cstar - 2, cstar) and ctx.has(cstar + 2, cstar)
        lb = fiat_zig(ctx, *lad4(M, aB), lf)
        lemma_P(ctx, cstar, 4, lb, (cstar + 2, 'in'), 'trail', [bp2])
        assert ctx.has(bp2, cstar)
        audit(ctx, AX | {(tp, m0)} | fiat_edges(*lad4(M, aB), lf))
        discharged.add(('I-G4', lf))
        for lf2 in (True, False):
            ctx2 = base()
            L2 = with_odd2(ctx2)
            ctx2.assume(tp, m0)
            polar(ctx2, M, p, L2, 'trail')
            assert ctx2.has(cstar, m0)
            ev = fiat_zig(ctx2, *even_ladder(M), lf2)
            lemma_P(ctx2, cstar, 2, ev, (m0, 'out'), 'lead', [tp5])
            assert ctx2.has(cstar, tp5)
            audit(ctx2, AX | {(tp, m0)} | fiat_edges(*even_ladder(M), lf2))
            discharged.add(('I-P2', lf, lf2))
    ctxc = base()
    ctxc.assume(bp2, cstar)
    ctxc.assume(cstar, tp5)
    ctxc.trans(cstar, tp5, bp2)          # consumes A3
    assert ctxc.has(cstar, bp2) and ctxc.has(bp2, cstar)
    audit(ctxc, AX | {(bp2, cstar), (cstar, tp5)})
    # ---- Case II: m0 < t_p ----
    for lf in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.assume(m0, tp)
        polar(ctx, M, p, L, 'lead')
        assert cstar2 in L
        assert ctx.has(cstar2, cstar2 - 2) and ctx.has(cstar2, cstar2 + 2)
        la = fiat_zig(ctx, *lad4(M, aA), lf)
        lemma_P(ctx, cstar2, 4, la, (cstar2 + 2, 'out'), 'lead', [tp2])
        assert ctx.has(cstar2, tp2)
        audit(ctx, AX | {(m0, tp)} | fiat_edges(*lad4(M, aA), lf))
        discharged.add(('II-G4', lf))
        for lf2 in (True, False):
            ctx2 = base()
            L2 = with_odd2(ctx2)
            ctx2.assume(m0, tp)
            polar(ctx2, M, p, L2, 'lead')
            assert ctx2.has(m0, cstar2)
            ev = fiat_zig(ctx2, *even_ladder(M), lf2)
            lemma_P(ctx2, cstar2, 2, ev, (m0, 'in'), 'trail', [bp1])
            assert ctx2.has(bp1, cstar2)
            audit(ctx2, AX | {(m0, tp)} | fiat_edges(*even_ladder(M), lf2))
            discharged.add(('II-P2', lf, lf2))
    ctxc = base()
    ctxc.assume(cstar2, tp2)
    ctxc.assume(bp1, cstar2)
    ctxc.trans(cstar2, tp2, bp1)         # consumes A2
    assert ctxc.has(cstar2, bp1) and ctxc.has(bp1, cstar2)
    audit(ctxc, AX | {(cstar2, tp2), (bp1, cstar2)})
    assert discharged == {
        ('I-G4', True), ('I-G4', False),
        ('I-P2', True, True), ('I-P2', True, False),
        ('I-P2', False, True), ('I-P2', False, False),
        ('II-G4', True), ('II-G4', False),
        ('II-P2', True, True), ('II-P2', True, False),
        ('II-P2', False, True), ('II-P2', False, False)}, (M, discharged)
    # ---- Lemma E: b_p < b_{p-2} implies t_{p-2} < t_p ----
    ctx = Ctx(M)
    ctx.assume(bp, bp2)
    L = lemma_Z(ctx, *odd_ladder(M), (bp, bp2))
    assert all((v - M) % 4 == p % 4 for v in L)
    # transfer: t_{p-2} has offset M-(p-2) = p mod 4 at every M = 0 mod 4
    # (odd p), so it is a leader and t_{p-2} < t_p is derived.
    assert tp2 in L and ctx.has(tp2, tp)
    audit(ctx, {(bp, bp2)})
    return True


def check_flip(M, p):
    """FLIP(p) at scale M/2 = p+3 mod 4."""
    assert M % 4 == 0 and (M // 2) % 4 == (p + 3) % 4
    m0 = 3 * M // 2
    tp, tp2, tp5 = 2 * M - p, 2 * M - (p - 2), 2 * M - (p + 5)
    bp, bp2, bp1 = M + p, M + (p - 2), M + (p + 1)
    cI, cII = m0 - 1, m0 + 1
    # the mod-8 lock, p-shifted: cI must be a G4 center for the value
    # class of b_p (= p mod 4), i.e. cI = p+2 mod 4; cII a G4 center for
    # the value class of t_p (= -p mod 4), i.e. cII = 2-p mod 4 -- and
    # for odd p, 2-p = p mod 4, so cII = p mod 4.  Both need
    # M/2 = p+3 mod 4.
    assert cI % 4 == (p + 2) % 4 and cII % 4 == (2 - p) % 4 == p % 4

    def base():
        ctx = Ctx(M)
        ctx.assume_all([(tp, bp), (tp2, bp1), (tp5, bp2), (bp, bp2)])
        return ctx

    AXF = frozenset({(tp, bp), (tp2, bp1), (tp5, bp2), (bp, bp2)})

    def with_odd2(ctx):
        L = lemma_Z(ctx, *odd_ladder(M), (bp, bp2))
        assert all((v - M) % 4 == p % 4 for v in L)
        return L

    assert tp % 2 == 1 and m0 % 2 == 0 and tp != m0
    discharged = set()
    concIa, concIb = (bp, cI), (cI, bp)
    concIIa, concIIb = (cII, tp), (tp, cII)

    aI = p % 4                # offset class of b_p (Case I G4)
    aII = (-p) % 4            # offset class of t_p (Case II G4)
    # ---- Case I: t_p < m0 ----
    for lf in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.assume(tp, m0)
        polar(ctx, M, p, L, 'trail')
        assert (cI + 2) in L and (cI - 2) in L
        assert ctx.has(cI + 2, cI) and ctx.has(cI - 2, cI)
        la = fiat_zig(ctx, *lad4(M, aI), lf)
        lemma_P(ctx, cI, 4, la, (cI + 2, 'in'), 'trail', [bp])
        assert ctx.has(*concIa)
        audit(ctx, AXF | {(tp, m0)} | fiat_edges(*lad4(M, aI), lf))
        discharged.add(('I-LAD', lf))
    for lf2 in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.assume(tp, m0)
        polar(ctx, M, p, L, 'trail')
        assert ctx.has(cI, m0)
        ev = fiat_zig(ctx, *even_ladder(M), lf2)
        lemma_P(ctx, cI, 2, ev, (m0, 'out'), 'lead', [tp5])
        ctx.trans(cI, tp5, bp2)                      # A3
        ctx.rule(bp2, cI, tp, (cI, bp2), (cI, tp))   # mirror R4
        ctx.trans(cI, tp, bp)                        # A1
        assert ctx.has(*concIb)
        audit(ctx, AXF | {(tp, m0)} | fiat_edges(*even_ladder(M), lf2))
        discharged.add(('I-EVEN2', lf2))
    assert concIa == concIb[::-1] and concIa != concIb
    # ---- Case II: m0 < t_p ----
    for lf in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.assume(m0, tp)
        polar(ctx, M, p, L, 'lead')
        assert cII in L
        assert ctx.has(cII, cII + 2) and ctx.has(cII, cII - 2)
        lb = fiat_zig(ctx, *lad4(M, aII), lf)
        lemma_P(ctx, cII, 4, lb, (cII + 2, 'out'), 'lead', [tp])
        assert ctx.has(*concIIa)
        audit(ctx, AXF | {(m0, tp)} | fiat_edges(*lad4(M, aII), lf))
        discharged.add(('II-LAD', lf))
    for lf2 in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.assume(m0, tp)
        polar(ctx, M, p, L, 'lead')
        assert ctx.has(m0, cII)
        ev = fiat_zig(ctx, *even_ladder(M), lf2)
        lemma_P(ctx, cII, 2, ev, (m0, 'in'), 'trail', [bp1])
        ctx.trans(tp2, bp1, cII)                     # A2
        ctx.rule(bp, cII, tp2, (tp2, cII), (bp, cII))  # mirror R3
        ctx.trans(tp, bp, cII)                       # A1
        assert ctx.has(*concIIb)
        audit(ctx, AXF | {(m0, tp)} | fiat_edges(*even_ladder(M), lf2))
        discharged.add(('II-EVEN2', lf2))
    assert concIIa == concIIb[::-1] and concIIa != concIIb
    assert discharged == {
        ('I-LAD', True), ('I-LAD', False),
        ('I-EVEN2', True), ('I-EVEN2', False),
        ('II-LAD', True), ('II-LAD', False),
        ('II-EVEN2', True), ('II-EVEN2', False)}, (M, discharged)
    return True


def sharpness(M, p):
    """At M/2 = p+1 mod 4 (the other half of the 0-mod-4 class) the flip
    schema is inapplicable: both centers land in the wrong mod-4 class
    for their G4 floods and cII's ODD2 leader status inverts."""
    assert M % 4 == 0 and (M // 2) % 4 == (p + 1) % 4
    m0 = 3 * M // 2
    ok1 = (m0 - 1) % 4 == (p + 2) % 4
    ok2 = (m0 + 1) % 4 == p % 4
    ok3 = (m0 + 1 - M) % 4 == p % 4     # ODD2 leader condition for cII
    assert not ok1 and not ok2 and not ok3
    return True


def main():
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    out = {"runs": [], "fail": []}
    for p in range(5, pmax + 1, 2):
        flip_res = (2 * (p + 3)) % 8        # M mod 8 class of the flip
        l1_scales = [M for M in list(range(4 * p, 4 * p + 400, 4))
                     + [512, 516, 1024, 1028] if M % 4 == 0]
        fl_scales = [M for M in l1_scales if (M // 2) % 4 == (p + 3) % 4]
        sh_scales = [M for M in l1_scales if (M // 2) % 4 == (p + 1) % 4]
        okL = okF = okS = 0
        for M in l1_scales:
            try:
                check_layer1(M, p)
                okL += 1
            except AssertionError as ex:
                out["fail"].append(["layer1", p, M, repr(ex.args[:2])])
        for M in fl_scales:
            try:
                check_flip(M, p)
                okF += 1
            except AssertionError as ex:
                out["fail"].append(["flip", p, M, repr(ex.args[:2])])
        for M in sh_scales:
            try:
                sharpness(M, p)
                okS += 1
            except AssertionError as ex:
                out["fail"].append(["sharp", p, M, repr(ex.args[:2])])
        out["runs"].append({
            "p": p, "x": 3 * p, "pair": [3 * p, 3 * p + 1],
            "flip_class_mod8": flip_res,
            "layer1_ok": okL, "layer1_total": len(l1_scales),
            "flip_ok": okF, "flip_total": len(fl_scales),
            "sharp_ok": okS, "sharp_total": len(sh_scales),
            "l1_first": l1_scales[0], "fl_scales_sample": fl_scales[:5]})
        print(f"p={p} (pair {{{3*p},{3*p+1}}}): layer1 {okL}/{len(l1_scales)}"
              f" scales, flip {okF}/{len(fl_scales)} (M = {flip_res} mod 8),"
              f" sharpness {okS}/{len(sh_scales)}", flush=True)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"failures: {len(out['fail'])}")
    for f in out["fail"][:20]:
        print("  ", f)
    print(f"-> {DATA}")
    if out["fail"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
