"""e139: machine check of notes/55 SS4 — floods inside P2-core.

Generalizes e113's strict schema engine (Ctx / lemma_Z / fiat_zig /
lemma_P) from the block (M, 2M] to an arbitrary integer interval,
then executes, at M = 48, 64, 80, with full audit discipline
(assertions on every AP's membership+arithmetic, every R-rule
pattern, every leader/trailer claim, every mirror bound; both
zigzag phases; both flood directions):

  F6-g2 : flood at centre 6M over the odd class, clipped mirror
          window e <= 15 (the width-15 boundary rung) — covers the
          16 odd values of [6M-15, 6M+15].
  F6-g4 : flood at centre 6M over the class = 2 mod 4 relative to
          6M, window e in {2,6,10,14}.  Needs 6M = 0 mod 4 (M even).
  MID-g2 (5M+7 | 5M+9, class evens): FULL-WIDTH floods across
          P2-core; the mirror of 6M through 5M+7 is 4M+14 and
          through 5M+9 is 4M+18 — the F <-> S3 mirror coupling.
  MID-g4 (5M+7 over class 1 mod 4 | 5M+9 over class 3 mod 4):
          full width; needs M = 0 mod 4.

All floods are CONDITIONAL lemmas: mono material (all rungs one
team) is a hypothesis, introduced by fiat (assume) exactly as e113's
phase branches; the audit() check rejects any smuggled fact.

Run: .venv/bin/python experiments/e139_flood6M.py
Log: data/e139_flood.log
"""


class ICtx:
    """e113 Ctx generalized to interval [lo, hi]."""

    def __init__(self, lo, hi):
        self.lo, self.hi = lo, hi
        self.M = (lo, hi)               # error-message tag
        self.facts = set()
        self.assumed = set()
        self.derived = set()

    def inside(self, v):
        return self.lo <= v <= self.hi

    def add(self, u, v):
        assert self.inside(u) and self.inside(v) and u != v, (self.M, u, v)
        self.facts.add((u, v))
        self.derived.add((u, v))

    def assume(self, u, v):
        assert self.inside(u) and self.inside(v) and u != v, (self.M, u, v)
        self.facts.add((u, v))
        self.assumed.add((u, v))

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


def lemma_P(ctx, c, g, leaders, seed, targets):
    """e113 lemma_P verbatim, interval bounds via ctx.inside."""
    step = g

    def in_class(v):
        return (v - c) % g == g // 2 and ctx.inside(v)

    v0, tag = seed
    assert in_class(v0), (ctx.M, c, v0)
    e0 = abs(v0 - c)
    assert ctx.inside(2 * c - v0), (ctx.M, c, v0, 'seed mirror outside')
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
            assert len(cand) == 1, (ctx.M, c, e, 'leader count', cand)
            s = cand[0]
            u, u_out = c + s * e, c + s * (e + step)
            assert ctx.has(u, u_out), (ctx.M, c, e, 'zig edge missing')
            ctx.trans(c, u, u_out)
            lo, hi = min(u_out, 2 * c - u_out), max(u_out, 2 * c - u_out)
            ctx.rule(lo, c, hi, (c, u_out), (c, 2 * c - u_out))
        else:
            cand = [s for s in (+1, -1) if leader(c + s * (e + step))]
            assert len(cand) == 1, (ctx.M, c, e, 'leader count in', cand)
            s = cand[0]
            v, v_in = c + s * (e + step), c + s * e
            assert ctx.has(v, v_in), (ctx.M, c, e, 'zig edge missing in')
            ctx.trans(v, v_in, c)
            lo, hi = min(v, 2 * c - v), max(v, 2 * c - v)
            ctx.rule(lo, c, hi, (v, c), (2 * c - v, c))
        e += step
        covered.add(e)
    e = e0
    while e - step >= step // 2 and e - step > 0:
        if out:
            cand = [s for s in (+1, -1) if not leader(c + s * (e - step))]
            assert len(cand) == 1, (ctx.M, c, e, 'trailer count', cand)
            s = cand[0]
            w, w_out = c + s * (e - step), c + s * e
            assert leader(w_out)
            assert ctx.has(w_out, w), (ctx.M, c, e, 'zig edge missing dn')
            ctx.trans(c, w_out, w)
            lo, hi = min(w, 2 * c - w), max(w, 2 * c - w)
            ctx.rule(lo, c, hi, (c, w), (c, 2 * c - w))
        else:
            cand = [s for s in (+1, -1) if leader(c + s * (e - step))]
            assert len(cand) == 1, (ctx.M, c, e, 'leader cnt dn', cand)
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
        assert e in covered, (ctx.M, c, t, 'target not covered')
        assert (ctx.has(c, t) if out else ctx.has(t, c)), (ctx.M, c, t)
    return covered


def run_flood(M, c, g, first, d, count, e0, targets, tag):
    """Execute the flood at centre c over the ladder (first, d, count)
    in all 4 (phase x direction) branches, audited."""
    lo, hi = 4 * M + 1, 6 * M + 15
    for leader_first in (True, False):
        for direction in ('out', 'in'):
            ctx = ICtx(lo, hi)
            v0 = c + e0
            if direction == 'out':
                ctx.assume(c, v0)
                seed_fact = {(c, v0)}
            else:
                ctx.assume(v0, c)
                seed_fact = {(v0, c)}
            leaders = fiat_zig(ctx, first, d, count, leader_first)
            lemma_P(ctx, c, g, leaders, (v0, direction), targets)
            audit(ctx, fiat_edges(first, d, count, leader_first)
                  | seed_fact)
    print(f'  M={M} {tag}: centre {c} g={g} rungs={count} '
          f'targets={len(targets)} — 4 branches OK', flush=True)


def check_M(M):
    assert M % 4 == 0
    lo, hi = 4 * M + 1, 6 * M + 15
    # F6-g2: odds around 6M, window 15
    run_flood(M, 6 * M, 2,
              first=6 * M - 15, d=2, count=16, e0=1,
              targets=[6 * M + e for e in range(-15, 16, 2)],
              tag='F6-g2 ')
    # F6-g4: class 2 mod 4 around 6M (6M = 0 mod 4 since M even)
    assert (6 * M) % 4 == 0
    run_flood(M, 6 * M, 4,
              first=6 * M - 14, d=4, count=8, e0=2,
              targets=[6 * M + e for e in
                       list(range(-14, 0, 4)) + list(range(2, 15, 4))],
              tag='F6-g4 ')
    # MID-g2 at 5M+7 over evens: full width
    c = 5 * M + 7
    emax = M + 5                                # largest odd admissible e
    assert c - emax == 4 * M + 2 and c + emax == 6 * M + 12
    run_flood(M, c, 2,
              first=4 * M + 2, d=2, count=M + 6, e0=M - 7,
              targets=list(range(4 * M + 2, 6 * M + 13, 2)),
              tag='MIDg2-')
    assert 2 * c - 6 * M == 4 * M + 14          # F<->S3 mirror (via 5M+7)
    # MID-g2 at 5M+9 over evens
    c = 5 * M + 9
    emax = M + 5                                # min(M+8, M+6) -> odd M+5
    assert c - emax == 4 * M + 4 and c + emax == 6 * M + 14
    run_flood(M, c, 2,
              first=4 * M + 4, d=2, count=M + 6, e0=M - 9,
              targets=list(range(4 * M + 4, 6 * M + 15, 2)),
              tag='MIDg2+')
    assert 2 * c - 6 * M == 4 * M + 18
    # MID-g4 at 5M+7 over class 1 mod 4 (c = 3 mod 4 at M = 0 mod 4)
    c = 5 * M + 7
    assert c % 4 == 3
    emax = M + 6                                # = 2 mod 4 at M = 0 mod 4
    assert emax % 4 == 2
    rungs = list(range(c - emax, c + emax + 1, 4))
    assert all(v % 4 == 1 for v in rungs) and rungs[0] == 4 * M + 1 \
        and rungs[-1] == 6 * M + 13
    run_flood(M, c, 4,
              first=rungs[0], d=4, count=len(rungs), e0=2,
              targets=rungs,
              tag='MIDg4-')
    # MID-g4 at 5M+9 over class 3 mod 4 (c = 1 mod 4)
    c = 5 * M + 9
    assert c % 4 == 1
    emax = M + 6
    rungs = list(range(c - emax, c + emax + 1, 4))
    assert all(v % 4 == 3 for v in rungs) and rungs[0] == 4 * M + 3 \
        and rungs[-1] == 6 * M + 15
    run_flood(M, c, 4,
              first=rungs[0], d=4, count=len(rungs), e0=2,
              targets=rungs,
              tag='MIDg4+')


def main():
    for M in (48, 64, 80):
        check_M(M)
    # residue side conditions across the sweep
    for M in range(48, 401, 16):
        assert (6 * M) % 4 == 0 and (5 * M + 7) % 4 == 3 \
            and (5 * M + 9) % 4 == 1 and (M + 6) % 4 == 2
    print('  residue sweep M=48..400 step 16: OK', flush=True)
    print('e139: ALL CHECKS PASSED', flush=True)


if __name__ == '__main__':
    main()
