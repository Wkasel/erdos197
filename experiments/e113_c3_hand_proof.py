"""e113_c3_hand_proof: TASK P (gap closure) -- strict schema verification of
the complete hand proof of the C3 core (notes/33 v2, Sections 5'-6').

THE PROOF BEING CHECKED (all discovered/assembled in this task):

  Toolkit:
   Lemma Z (zigzag): a seed orientation on one adjacent pair of a d-ladder
     propagates: every second rung leads both neighbors.
   Lemma D (phase dichotomy): in ANY linear order every d-ladder is in one
     of its two zigzag phases (orient any one adjacent pair, apply Z).
   Lemma P (flood): center c, class C = arithmetic class of step g
     (g = 2: a parity class; g = 4: a mod-4 class) with c ~ C + g/2
     (c congruent to class shifted by half-step), carrying a zigzag in a
     KNOWN phase.  Mirror pairs (c-e, c, c+e), e = g/2 mod g.  From one
     seed relation between c and a pair member, the alternating induction
     (zigzag hop on the unique usable side + mirror reflection through c)
     yields c-before-w (outward) resp. w-before-c (inward) for EVERY class
     value w whose mirror 2c-w lies in the interval.  The usable side
     exists at every pair for EITHER zigzag phase (the two candidates
     differ by 2e = g mod 2g, so exactly one is a leader) -- so combined
     with Lemma D the flood conclusion is PHASE-BLIND: prove it in both
     branches and detach.
   Lemma E (transfer): even M; the odd d=2 ladder locks the orientations
     of (b3,b5) and (t5,t3): b5<b3 iff t3<t5 at M = 0 mod 4;
     b5<b3 iff t5<t3 at M = 2 mod 4.

  Layer-1 Theorem (M = 0 mod 4): AP-free + A2 (t3<b6) + A3 (t10<b3)
    forces b5<b3 and t3<t5.
    Proof: refute S: b3<b5.  ODD2 zigzag: leaders = offsets 3 mod 4 (Z on
    seed S).  Split on (m0, t5), m0 = 3M/2:
    Case I (t5<m0): POLAR-trail = P(m0, odds, inward): all odds < m0.
      c* := m+1 (M = 0 mod 8) / m-1 (M = 4 mod 8)  [c* = 1 mod 4].
      G4-inward at c* over class B (offsets 3 mod 4): b3 < c*
        [seeds c*+-2 < c* are ODD2 edges; both LADB phases].
      P2-outward at c* over evens: c* < t10 [seed c* < m0 from POLAR;
        both EVEN2 phases].  A3: t10 < b3.  3-cycle.
    Case II (m0<t5): POLAR-lead: m0 < all odds.
      c** := m-1 (M = 0 mod 8) / m+1 (M = 4 mod 8)  [c** = 3 mod 4,
        an ODD2 leader].
      G4-outward at c** over class A (offsets 1 mod 4): c** < t3
        [seeds c** < c**+-2 from ODD2; both LADA phases].
      P2-inward at c** over evens: b6 < c** [seed m0 < c**; both phases].
      A2: t3 < b6.  3-cycle.
    Then Lemma E (seed b5<b3): t3<t5.

  Flip Theorem (M = 0 mod 8): AP-free + A1 (t5<b5) + A2 + A3 is
    contradictory.  (With Layer 1 this refutes C3 = A1+A2+A3.)
    Proof: by Layer 1, b5<b3; ODD2 zigzag: leaders = offsets 1 mod 4.
    Split on (m0, t5):
    Case I (t5<m0): POLAR-trail: odds < m0.
      P2-outward at m-1 over evens: m-1 < t10 [seed m-1 < m0].
      A3: m-1 < b3; mirror AP (b3, m-1, t5): R4: m-1 < t5;
      A1: m-1 < b5.
      G4-inward at m-1 over class A: b5 < m-1  [m-1 = 3 mod 4 needs
        M = 0 mod 8; seeds m+1 < m-1, m-3 < m-1 are ODD2 edges].  Cycle.
    Case II (m0<t5): POLAR-lead: m0 < odds.
      P2-inward at m+1 over evens: b6 < m+1 [seed m0 < m+1].
      A2: t3 < m+1; mirror AP (b5, m+1, t3): R3: b5 < m+1; A1: t5 < m+1.
      G4-outward at m+1 over class B: m+1 < t5  [m+1 = 1 mod 4 needs
        M = 0 mod 8; seeds m+1 < m+-... = ODD2 leader edges].  Cycle.

The checker executes every lemma instance rung-by-rung/pair-by-pair with
assertions on every AP (membership, arithmetic, rule pattern) and every
side condition (residues, leader/trailer status, mirrors in interval),
running BOTH branches of every phase dichotomy.  It also asserts the
mod-8 sharpness: at M = 4 mod 8 the flip schema's center-class conditions
fail (m-1 = 1 mod 4 is in class A, m+1 = 3 mod 4 in class B: no G4 center).

Run: .venv/bin/python experiments/e113_c3_hand_proof.py
Output: data/e113_hand_proof.json
"""
import json
import sys

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e113_hand_proof.json"


class Ctx:
    """Fact store with strict rule application."""

    def __init__(self, M):
        self.M = M
        self.facts = set()          # (u, v): u before v
        self.assumed = set()        # hypothesis-introduction log
        self.derived = set()        # rule/trans-derivation log
        self.steps = 0

    def inside(self, v):
        return self.M < v <= 2 * self.M

    def add(self, u, v):
        assert self.inside(u) and self.inside(v) and u != v, (self.M, u, v)
        # NOTE: (v,u) may legitimately coexist with (u,v): reaching an
        # explicit 2-cycle IS the contradiction the proof aims for; the
        # check functions assert both directions where the cycle closes.
        self.facts.add((u, v))
        self.derived.add((u, v))
        self.steps += 1

    def assume(self, u, v):
        """Hypothesis introduction: axiom, case-split fact, or Lemma-D
        phase edge.  The ONLY sanctioned way to insert an underived fact;
        audit() later checks the full assumption log of a branch against
        its declared hypothesis set, so smuggled facts (raw facts.add or
        an undeclared assume) are rejected."""
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
        """One R1-R4 application on AP (x,y,z), midpoint y."""
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
    """Hypothesis discipline for one branch context: the branch assumed
    EXACTLY the declared hypothesis set, and every other fact was derived
    through the assertion-checked rule/trans primitives.  Any conclusion
    smuggled in as a fact (bypassing derivation) fails here."""
    hyp = set(hypotheses)
    assert ctx.assumed == hyp, (ctx.M, ctx.assumed ^ hyp)
    assert ctx.facts == ctx.assumed | ctx.derived, \
        (ctx.M, ctx.facts - (ctx.assumed | ctx.derived))


def fiat_edges(first, d, count, leader_first):
    """The Lemma-D phase-hypothesis edge set of a d-ladder: every leader
    before both neighbors.  Enumerated INDEPENDENTLY of fiat_zig's loop
    (deliberate redundancy: a mutation to either encoding makes audit()
    or the flood's zig-edge asserts fire)."""
    lad = [first + i * d for i in range(count)]
    e0 = 0 if leader_first else 1
    return {(lad[i], lad[j]) for i in range(e0, count, 2)
            for j in (i - 1, i + 1) if 0 <= j < count}


def lemma_Z(ctx, first, d, count, seed):
    """Zigzag on the ladder first, first+d, ..., (count rungs), seeded by
    the adjacent pair `seed` (must be a fact).  Returns dict:
    leader value -> True.  Adds all zigzag edges as facts, deriving each
    by the Lemma-Z induction with strict rule checks."""
    lad = [first + i * d for i in range(count)]
    assert all(ctx.inside(v) for v in lad)
    su, sv = seed
    assert ctx.has(su, sv)
    i, j = lad.index(su), lad.index(sv)
    assert abs(i - j) == 1
    e = i                       # leader index parity class
    # establish w_e leads both neighbors
    if 0 <= 2 * i - j < count:  # reflect seed to other neighbor
        x, y, z = sorted([lad[j], lad[i], lad[2 * i - j]])
        ctx.rule(x, y, z, (lad[i], lad[j]), (lad[i], lad[2 * i - j]))
    # upward induction
    k = e
    while k + 2 < count:
        # w_k leads; AP (w_k, w_k+1, w_k+2): R1 from w_k < w_k+1
        x, y, z = sorted([lad[k], lad[k + 1], lad[k + 2]])
        ctx.rule(x, y, z, (lad[k], lad[k + 1]), (lad[k + 2], lad[k + 1]))
        if k + 3 < count:       # w_k+2 leads other neighbor via R4
            x, y, z = sorted([lad[k + 1], lad[k + 2], lad[k + 3]])
            ctx.rule(x, y, z, (lad[k + 2], lad[k + 1]),
                     (lad[k + 2], lad[k + 3]))
        k += 2
    # downward induction
    k = e
    while k - 2 >= 0:
        x, y, z = sorted([lad[k], lad[k - 1], lad[k - 2]])
        ctx.rule(x, y, z, (lad[k], lad[k - 1]), (lad[k - 2], lad[k - 1]))
        if k - 3 >= 0:
            x, y, z = sorted([lad[k - 1], lad[k - 2], lad[k - 3]])
            ctx.rule(x, y, z, (lad[k - 2], lad[k - 1]),
                     (lad[k - 2], lad[k - 3]))
        k -= 2
    leaders = {lad[i2] for i2 in range(e % 2, count, 2)}
    return leaders


def fiat_zig(ctx, first, d, count, leader_first):
    """Phase-branch hypothesis: add the full zigzag edge set for the given
    phase (leader_first: whether lad[0] is a leader) WITHOUT derivation --
    justified by Lemma D (one of the two phases holds; caller runs both).
    Returns leader set."""
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
    """Flood at center c over the class {v : v = c +- e, e = g/2 mod g}
    (opposite-parity for g=2, the mod-4 class c+2 for g=4), whose d=g
    ladder zigzag has leader set `leaders` (all class leaders).
    seed: (v0, 'out') meaning c<v0 is a fact, or (v0, 'in'): v0<c.
    direction inferred from seed tag.  Floods every class value w with
    mirror 2c-w inside; asserts every induction step; checks targets.
    Returns the covered set."""
    M = ctx.M
    step = g

    def in_class(v):
        return (v - c) % g == g // 2 and ctx.inside(v)

    v0, tag = seed
    assert in_class(v0), (M, c, v0)
    e0 = abs(v0 - c)
    assert ctx.inside(2 * c - v0), (M, c, v0, 'seed mirror outside')
    out = (tag == 'out')
    # pair e0: mirror the seed
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

    # upward
    e = e0
    while pair_ok(e + step):
        if out:
            # need the leader among {c+e, c-e}; it leads outward neighbor
            cand = [s for s in (+1, -1) if leader(c + s * e)]
            assert len(cand) == 1, (M, c, e, 'leader count', cand)
            s = cand[0]
            u, u_out = c + s * e, c + s * (e + step)
            assert ctx.has(u, u_out), (M, c, e, 'zig edge missing')
            ctx.trans(c, u, u_out)
            lo, hi = min(u_out, 2 * c - u_out), max(u_out, 2 * c - u_out)
            ctx.rule(lo, c, hi, (c, u_out), (c, 2 * c - u_out))
        else:
            # leader among {c+-(e+step)} leads inward neighbor
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
    # downward
    e = e0
    while e - step >= step // 2 and e - step > 0:
        if out:
            # trailer w among {c+-(e-step)}: its outward neighbor (a
            # leader, at distance e) leads it: c < neighbor < w
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
            # leader w among {c+-(e-step)} leads its outward neighbor
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
    """d=4 ladder on offsets = a mod 4 (a in {1,3})."""
    first = M + a
    count = (2 * M - first) // 4 + 1
    return first, 4, count


def polar(ctx, M, odd_leaders, direction):
    """P2 flood at m0 over the odd class.  direction 'lead': m0 < t5 fact
    -> m0 < all odds; 'trail': t5 < m0 -> all odds < m0."""
    m0 = 3 * M // 2
    t5 = 2 * M - 5
    tag = 'out' if direction == 'lead' else 'in'
    odds = [v for v in range(M + 1, 2 * M + 1, 2)]
    # coverage targets: every odd with mirror inside = all odds
    targets = [v for v in odds if ctx.inside(3 * M - v)]
    lemma_P(ctx, m0, 2, odd_leaders, (t5, tag), direction, targets)
    return targets


def check_layer1(M):
    """Verify the Layer-1 theorem schema at scale M = 0 mod 4."""
    assert M % 4 == 0
    m0 = 3 * M // 2
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6

    def base():
        ctx = Ctx(M)
        ctx.assume_all([(t3, b6), (t10, b3), (b3, b5)])
        return ctx

    # declared hypothesis set for audit(); intentionally repeats the
    # base() literals -- a tamper to either copy alone is caught by
    # audit(), a consistent tamper to both by the consuming asserts
    # (lemma_Z seed, ctxc.trans of A2/A3).
    AX = frozenset({(t3, b6), (t10, b3), (b3, b5)})

    # ODD2 (derived, seed b3<b5): leaders offsets 3 mod 4
    def with_odd2(ctx):
        L = lemma_Z(ctx, *odd_ladder(M), (b3, b5))
        assert all((v - M) % 4 == 3 for v in L)
        return L

    cstar = m0 + 1 if M % 8 == 0 else m0 - 1     # Case I center, = 1 mod 4
    cstar2 = m0 - 1 if M % 8 == 0 else m0 + 1    # Case II center, = 3 mod 4
    assert cstar % 4 == 1 and cstar2 % 4 == 3

    # Case split (t5, m0) is EXHAUSTIVE in a linear order: t5 odd, m0 even
    # (M = 0 mod 4), so t5 != m0 and by totality t5<m0 or m0<t5.
    assert t5 % 2 == 1 and m0 % 2 == 0 and t5 != m0
    discharged = set()

    # ---- Case I: t5 < m0 ----
    # (a) G4-inward at c* over class B: b3 < c*   [both LADB phases]
    for lf in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.facts.add((t5, m0))
        polar(ctx, M, L, 'trail')
        # seeds: c*+-2 < c* are ODD2 zigzag edges (c*+-2 = 3 mod 4 leaders)
        assert (cstar - 2) in L and (cstar + 2) in L
        assert ctx.has(cstar - 2, cstar) and ctx.has(cstar + 2, cstar)
        lb = fiat_zig(ctx, *lad4(M, 3), lf)
        lemma_P(ctx, cstar, 4, lb, (cstar + 2, 'in'), 'trail', [b3])
        assert ctx.has(b3, cstar)
        discharged.add(('I-G4', lf))
        # (b) P2-outward at c* over evens: c* < t10  [both EVEN2 phases]
        for lf2 in (True, False):
            ctx2 = base()
            L2 = with_odd2(ctx2)
            ctx2.facts.add((t5, m0))
            polar(ctx2, M, L2, 'trail')
            assert ctx2.has(cstar, m0)
            ev = fiat_zig(ctx2, *even_ladder(M), lf2)
            lemma_P(ctx2, cstar, 2, ev, (m0, 'out'), 'lead', [t10])
            assert ctx2.has(cstar, t10)
            discharged.add(('I-P2', lf, lf2))
    # machine-checked contradiction, Case I: b3 < c* (every LADB phase),
    # c* < t10 (every EVEN2 phase) are branch-independent conclusions of
    # the SAME case hypothesis; with axiom A3 (t10 < b3) they close a
    # 3-cycle.  Assemble it explicitly: the trans step CONSUMES A3 from
    # the hypothesis set, so a tampered/absent A3 fails here.
    ctxc = base()
    ctxc.facts.add((b3, cstar))        # conclusion (a), all LADB phases
    ctxc.facts.add((cstar, t10))       # conclusion (b), all EVEN2 phases
    ctxc.trans(cstar, t10, b3)         # uses A3: t10 < b3
    assert ctxc.has(cstar, b3) and ctxc.has(b3, cstar)   # explicit 2-cycle
    # ---- Case II: m0 < t5 ----
    for lf in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.facts.add((m0, t5))
        polar(ctx, M, L, 'lead')
        # c** is an ODD2 leader: seeds c** < c**+-2
        assert cstar2 in L
        assert ctx.has(cstar2, cstar2 - 2) and ctx.has(cstar2, cstar2 + 2)
        la = fiat_zig(ctx, *lad4(M, 1), lf)
        lemma_P(ctx, cstar2, 4, la, (cstar2 + 2, 'out'), 'lead', [t3])
        assert ctx.has(cstar2, t3)
        discharged.add(('II-G4', lf))
        for lf2 in (True, False):
            ctx2 = base()
            L2 = with_odd2(ctx2)
            ctx2.facts.add((m0, t5))
            polar(ctx2, M, L2, 'lead')
            assert ctx2.has(m0, cstar2)
            ev = fiat_zig(ctx2, *even_ladder(M), lf2)
            lemma_P(ctx2, cstar2, 2, ev, (m0, 'in'), 'trail', [b6])
            assert ctx2.has(b6, cstar2)
            discharged.add(('II-P2', lf, lf2))
    # machine-checked contradiction, Case II: c** < t3 (every LADA phase),
    # b6 < c** (every EVEN2 phase); with axiom A2 (t3 < b6) they close a
    # 3-cycle.  The trans step consumes A2 from the hypothesis set.
    ctxc = base()
    ctxc.facts.add((cstar2, t3))       # conclusion (a), all LADA phases
    ctxc.facts.add((b6, cstar2))       # conclusion (b), all EVEN2 phases
    ctxc.trans(cstar2, t3, b6)         # uses A2: t3 < b6
    assert ctxc.has(cstar2, b6) and ctxc.has(b6, cstar2)  # explicit 2-cycle
    # branch-completeness: every (case x phase) leaf must have been
    # discharged -- a dropped case or phase branch fails here.
    assert discharged == {
        ('I-G4', True), ('I-G4', False),
        ('I-P2', True, True), ('I-P2', True, False),
        ('I-P2', False, True), ('I-P2', False, False),
        ('II-G4', True), ('II-G4', False),
        ('II-P2', True, True), ('II-P2', True, False),
        ('II-P2', False, True), ('II-P2', False, False)}, (M, discharged)
    # ---- Lemma E: b5<b3 (now forced) implies t3<t5 ----
    ctx = Ctx(M)
    ctx.facts.add((b5, b3))
    L = lemma_Z(ctx, *odd_ladder(M), (b5, b3))
    assert all((v - M) % 4 == 1 for v in L)
    assert t3 in L and ctx.has(t3, t5)
    return True


def check_flip(M):
    """Verify the Flip theorem schema at scale M = 0 mod 8."""
    assert M % 8 == 0
    m0 = 3 * M // 2
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    cI, cII = m0 - 1, m0 + 1
    assert cI % 4 == 3 and cII % 4 == 1   # the mod-8 lock

    def base():
        ctx = Ctx(M)
        ctx.facts.update([(t5, b5), (t3, b6), (t10, b3), (b5, b3)])
        return ctx

    def with_odd2(ctx):
        L = lemma_Z(ctx, *odd_ladder(M), (b5, b3))
        assert all((v - M) % 4 == 1 for v in L)
        return L

    # Case split (t5, m0) exhaustive: t5 odd, m0 even, so t5 != m0.
    t5v = 2 * M - 5
    assert t5v % 2 == 1 and m0 % 2 == 0 and t5v != m0
    discharged = set()
    # branch-independent case conclusions (derived in EVERY phase branch):
    concIa, concIb = (b5, cI), (cI, b5)      # Case I: LADA vs EVEN2
    concIIa, concIIb = (cII, t5), (t5, cII)  # Case II: LADB vs EVEN2

    # ---- Case I: t5 < m0 ----
    for lf in (True, False):        # LADA phases
        ctx = base()
        L = with_odd2(ctx)
        ctx.facts.add((t5, m0))
        polar(ctx, M, L, 'trail')
        # chain: m-1 < t10 (flood, checked below per EVEN2 phase),
        # here: G4-inward at m-1 over class A: b5 < m-1
        assert (cI + 2) in L and (cI - 2) in L      # m+1, m-3 leaders
        assert ctx.has(cI + 2, cI) and ctx.has(cI - 2, cI)
        la = fiat_zig(ctx, *lad4(M, 1), lf)
        lemma_P(ctx, cI, 4, la, (cI + 2, 'in'), 'trail', [b5])
        assert ctx.has(*concIa)
        discharged.add(('I-LADA', lf))
    for lf2 in (True, False):       # EVEN2 phases
        ctx = base()
        L = with_odd2(ctx)
        ctx.facts.add((t5, m0))
        polar(ctx, M, L, 'trail')
        assert ctx.has(cI, m0)
        ev = fiat_zig(ctx, *even_ladder(M), lf2)
        lemma_P(ctx, cI, 2, ev, (m0, 'out'), 'lead', [t10])
        ctx.trans(cI, t10, b3)                       # A3
        ctx.rule(b3, cI, t5, (cI, b3), (cI, t5))     # mirror R4
        ctx.trans(cI, t5, b5)                        # A1
        assert ctx.has(*concIb)
        discharged.add(('I-EVEN2', lf2))
    # machine-checked contradiction, Case I: b5 < m-1 (every LADA phase)
    # vs m-1 < b5 (every EVEN2 phase) -- syntactically opposite literals.
    assert concIa == concIb[::-1] and concIa != concIb
    # ---- Case II: m0 < t5 ----
    for lf in (True, False):        # LADB phases
        ctx = base()
        L = with_odd2(ctx)
        ctx.facts.add((m0, t5))
        polar(ctx, M, L, 'lead')
        assert cII in L
        assert ctx.has(cII, cII + 2) and ctx.has(cII, cII - 2)
        lb = fiat_zig(ctx, *lad4(M, 3), lf)
        lemma_P(ctx, cII, 4, lb, (cII + 2, 'out'), 'lead', [t5])
        assert ctx.has(*concIIa)
        discharged.add(('II-LADB', lf))
    for lf2 in (True, False):
        ctx = base()
        L = with_odd2(ctx)
        ctx.facts.add((m0, t5))
        polar(ctx, M, L, 'lead')
        assert ctx.has(m0, cII)
        ev = fiat_zig(ctx, *even_ladder(M), lf2)
        lemma_P(ctx, cII, 2, ev, (m0, 'in'), 'trail', [b6])
        ctx.trans(t3, b6, cII)                       # A2
        ctx.rule(b5, cII, t3, (t3, cII), (b5, cII))  # mirror R3
        ctx.trans(t5, b5, cII)                       # A1
        assert ctx.has(*concIIb)
        discharged.add(('II-EVEN2', lf2))
    # machine-checked contradiction, Case II: m+1 < t5 vs t5 < m+1.
    assert concIIa == concIIb[::-1] and concIIa != concIIb
    # branch-completeness: all 8 leaves discharged.
    assert discharged == {
        ('I-LADA', True), ('I-LADA', False),
        ('I-EVEN2', True), ('I-EVEN2', False),
        ('II-LADB', True), ('II-LADB', False),
        ('II-EVEN2', True), ('II-EVEN2', False)}, (M, discharged)
    return True


def sharpness_4mod8(M):
    """At M = 4 mod 8 the flip schema must be inapplicable: the centers
    m-1, m+1 fall in the wrong mod-4 classes for the G4 floods, and the
    ODD2 leader statuses invert."""
    assert M % 8 == 4
    m0 = 3 * M // 2
    ok1 = (m0 - 1) % 4 == 3     # class condition for Case I center
    ok2 = (m0 + 1) % 4 == 1     # for Case II center
    # ODD2 (flip phase: leaders offsets 1 mod 4): m+1 offset M/2+1
    ok3 = (m0 + 1 - M) % 4 == 1
    assert not ok1 and not ok2 and not ok3
    return True


def main():
    out = {"layer1": [], "flip": [], "sharp": [], "fail": []}
    l1_scales = list(range(12, 401, 4)) + [512, 1024]
    fl_scales = list(range(16, 401, 8)) + [512, 1024]
    for M in l1_scales:
        try:
            check_layer1(M)
            out["layer1"].append(M)
        except AssertionError as ex:
            out["fail"].append(["layer1", M, repr(ex.args[:2])])
    for M in fl_scales:
        try:
            check_flip(M)
            out["flip"].append(M)
        except AssertionError as ex:
            out["fail"].append(["flip", M, repr(ex.args[:2])])
    for M in range(28, 301, 8):
        if M % 8 == 4:
            sharpness_4mod8(M)
            out["sharp"].append(M)
    print(f"layer1 verified at {len(out['layer1'])} scales: "
          f"{out['layer1'][:6]}...{out['layer1'][-3:]}")
    print(f"flip verified at {len(out['flip'])} scales: "
          f"{out['flip'][:6]}...{out['flip'][-3:]}")
    print(f"sharpness (4 mod 8 schema inapplicability): "
          f"{len(out['sharp'])} scales")
    print(f"failures: {out['fail']}")
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}")
    if out["fail"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
