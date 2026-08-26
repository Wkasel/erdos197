"""Erdős #197 — G4b: the stage-seam law + crown split-consistency (T-PIN-STAGE).

Geometry (the last YES-shape, STATUS 'Growing-sliver verdict' §4):
stage-alternating ownership.  Stage boundaries a_0 < a_1 < ... with stage
k = octaves (a_k, a_{k+1}] (octave j = (2^{j-1}, 2^j]), owner A for even k,
B for odd k, stage lengths L_k = a_{k+1} - a_k -> infinity.  Deviations
from pure super-block ownership:
  - bottom sliver sigma_k at seam a_k: new owner N (stage k) donates
    (2^{a_k}, 2^{a_k} + sigma_k] to old owner O (stage k-1);
  - top sliver tau_k at seam a_k: O donates (2^{a_k} - tau_k, 2^{a_k}] to N;
  - pair-split plants: for a split level j, one member of the crown pair
    Pi_j = {2^j - 1, 2^j} is donated to the partner of octave j's owner
    (orientation beta_j = 'T': plant 2^j; 'B': plant 2^j - 1).

THE SEAM LAW (derived in notes/42, machine-checked here as an exact iff
catalogue, CHECK A — the stage analogue of notes/39 SS4 CHECK-8):
with m = 2^{a_k}, O = owner(stage k-1), N = owner(stage k), for a fixed
in-team attacker x (x small relative to m), the COMPLETE list of channels
by which x attacks (in-team triples (x, y, 2y-x)) with middle y in the
4-octave seam window [a_k - 1, a_k + 2] is:

  C0   (either team T): y, z both kept in the SAME stage owned by T.
       Exists for EVERY fixed x in T (stage neck 2 lo - hi -> -infinity).
       NEW vs octave geometry: for y in a non-top block of the stage, the
       completion lands in the NEXT in-team block, so x attacks EVERY
       kept y of that block — Theta(M) forced units per block pair
       (octave geometry: Theta(x)).  Donation protects nobody: the
       completions off N's kept bottom land in N's own interior.
  X2   (closed): the cross-stage channel y in stage k, z in stage k+2
       (the d_t/NECK hot-potato seam of notes/38-39) is EMPTY as soon as
       L_{k+1} >= 2: 2 hi(stage k) < lo(stage k+2).
  C1   (hurts O, the sliver receiver): y in O's kept top octave a_k,
       z in O's received bottom sliver (m, m + sigma_k].
       Exists iff sigma_k >= 2, or sigma_k = 1 and x odd;
       count = ceil(sigma_k/2) if x odd else floor(sigma_k/2).
       NO x-threshold — receiving a bottom sliver at your stage top is
       fatal-shaped for every fixed attacker (contrast d_t law's
       receiver condition x <= d_t - 1: the attacking surface here is a
       FULL own octave, no schedule dial exists).
  C2   (hurts O): y in the received sliver, z = the planted member of
       pair a_k + 1 (if planted INTO O).  Exists iff that plant is in O
       and (beta = 'T': x even, 2 <= x <= 2 sigma_k;
            beta = 'B': x odd, 3 <= x <= 2 sigma_k + 1); count 1.
  C4   (hurts N, the top-sliver receiver): y in N's received top sliver
       (m - tau_k, m], z in N's kept first octave.  Exists for EVERY
       fixed x in N once tau_k >= 1; count = tau_k minus boundary
       corrections (exact set compared below).
  C5   (hurts N): y = the planted member of pair a_k - 1 (if planted
       into N), z in N's received top sliver.  Exists iff
       (beta_{a_k-1} = 'T': x <= tau_k - 1; 'B': x <= tau_k - 3); count 1.
  FAN  (hurts N, UNAVOIDABLE under seam-pair splitting): y = the planted
       seam-pair member p in {m-1, m} (either orientation), z = 2p - x
       in N's kept first octave.  Exists for EVERY fixed x in N; count 1.
       This is the seam analogue of the planted-crown landing pad: the
       completion octave a_k + 1 belongs to N under BOTH orientations,
       so every seam-pair split hands the NEW OWNER a fixed-cohort
       attack family — both teams are new owners at half the seams, so
       NO stage-alternating team with split seam pairs is 'clean' in
       the G3 sense.  (The per-seam gadget of FAN alone is single-middle
       and trivially SAT: signature, not yet death.)
  DUST (x = 1 only): y = plant(j), z = plant(j+1), the triple
       (1, 2^j, 2^{j+1} - 1) with both plants in the same team P and
       1 in P.  Occurs exactly at interior orientation junctures
       (beta_j, beta_{j+1}) = ('T','B') and seam junctures ('B','B') /
       ('T','T').  ORIENT lemma: consistent orientations avoiding all
       DUST exist (e.g. per-stage B...BT...T with a flip at each seam),
       so the split-consistency constraint system is satisfiable —
       the price of splitting is the FAN, not the dust.

CROWN SPLIT-CONSISTENCY (T-PIN-STAGE, notes/42 SS3):
  Theorem T-PIN-STAGE.  Let T be one team of ANY partition (no geometry
  needed).  If (i) both members of Pi_j = {2^j-1, 2^j} lie in T for some
  j >= 4; (ii) T contains infinitely many pairwise-disjoint INTACT
  dyadic blocks (M, 2M], M = 2^m >= 2^j; (iii) the per-scale gadget
  OG_j(M) (AP-free order of (M, 2M] + units z < y for every attack
  (c, y, z), c in Pi_j) is UNSAT for cofinitely many of those M — then
  T is not permutable.  Proof: thm:ogred's pigeonhole verbatim (the
  attacker pair has fixed positions; only finitely many of the disjoint
  blocks meet the initial segment before both; a full block past both
  realizes OG_j(M)).  The blocks are counted in TOTAL across stages —
  per-stage counts are irrelevant, which is the YES-candidate reading
  of the task memo: sum over stages of (blocks above the lowest kept
  pair) = sum_k (L_k - O(1)) diverges.
  For j = 4 hypothesis (iii) is thm:c3core (every interior scale is a
  power of two >= 8, hence == 0 mod 8): UNCONDITIONAL.
  Bookkeeping lemma: an interior block (octave neither first nor last
  of its stage) can only be punctured by a pair SPLIT (slivers touch
  only the boundary octaves), so a team keeping pairs at infinitely
  many levels keeps infinitely many intact blocks.  Contrapositive:
  survival forces splitting ALL BUT O(1) PAIRS PER STAGE (all but
  finitely many globally, given (iii) for the relevant j's).

Machine checks (data/g4b_results.json + this file's stdout):
  CHECK 0  partition sanity: A|B disjoint cover of [1, 2^14], all variants.
  CHECK A  the seam-law catalogue as an exact iff: brute-force
           enumeration of all in-team triples (x, y, 2y - x), x <= 24,
           y in the 4-octave seam window, on 9 stage-alternating
           variants x 2-3 seams (scales m = 32..4096): every found
           triple must classify into the channels above (completeness),
           and the C1/C2/C4/C5/FAN/DUST existence iffs + counts must
           match the formulas exactly (soundness), including the
           predicted ABSENCES (X2 empty; 'none'-variant: C0 only;
           halfBT variant: zero DUST).
  CHECK B  puncture robustness of the C3 core (the rung content of
           T-PIN-STAGE on split-crown blocks): AP + C3 units on
           (M, 2M] minus {2M} / {2M-1} / both, M = 64, 128, 256
           (all == 0 mod 8; expect UNSAT if the core survives losing
           the top pair), + intact control UNSAT + M == 4 mod 8
           control SAT (engine sanity).
  CHECK C  THE STAGE RUNG STG(M, F): AP-free order of TWO consecutive
           in-team blocks (M, 2M] u (2M, 4M] + units from a fixed
           attacker set F (all in-window attacks; the top-half of block
           1 is fully covered: Theta(M) units).  Configs: F = {3}, {15},
           {15,16}, {21,22}; intact and top-pair-punctured windows;
           M = 64, 128, 256.  If UNSAT at fixed-F: T-PIN (fixed finite
           attacker set + infinitely many disjoint octave-pair windows,
           which EVERY stage-alternating team has) kills the team —
           the stage-geometry analogue of RUNG-IN.
  CHECK D  per-j spot: the j = 5 pair rung OG_5(M) = AP + attacks of
           {31, 32} on (M, 2M], M = 64, 128, 256 (support for per-j
           splitting forcing beyond j = 4).
  CHECK E  T-PIN-STAGE bookkeeping arithmetic on the variants: interior
           blocks per stage, divergence of totals, disjointness.

Usage: .venv/bin/python experiments/g4b_seam_law.py [--fast]
       (--fast: skip the M = 256 SAT rows)
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from s2_growing_death import ap_order_sat  # noqa: E402

SANITY_N = 1 << 14
XMAX = 24
SPLIT_FROM = 3          # split levels j >= SPLIT_FROM (pair {7,8} upward)


# ---------------------------------------------------------------- variants

def tri_bounds(kmax=40):
    """a_0=0, a_k = 2 + k(k+1)/2 (k>=1): L = 3,2,3,4,5,..."""
    return [0] + [2 + k * (k + 1) // 2 for k in range(1, kmax)]


def quad_bounds(kmax=40):
    return [0] + [2 + k * k for k in range(1, kmax)]


class Variant:
    def __init__(self, name, bounds, sigma=None, tau=None, orient='top',
                 split='all'):
        """sigma/tau: functions seam-index k -> depth (None = 0).
        orient: 'top'|'bot'|'mixTB'|'halfBT' (beta_j policy).
        split: 'all' (every level >= SPLIT_FROM) | 'interior'
               (only levels that are not stage boundaries) | 'none'."""
        self.name = name
        self.a = bounds
        self.sigma = sigma or (lambda k: 0)
        self.tau = tau or (lambda k: 0)
        self.orient = orient
        self.split = split
        self.nstage = len(bounds) - 1

    # ---- structure maps
    def octave(self, v):
        return (v - 1).bit_length()

    def stage_of_octave(self, j):
        """k with a_k < j <= a_{k+1}; octaves 0..a_1 are stage 0."""
        a = self.a
        for k in range(self.nstage - 1):
            if j <= a[k + 1]:
                return k
        raise ValueError(f'octave {j} beyond bounds table')

    def owner(self, k):
        return 'A' if k % 2 == 0 else 'B'

    def is_seam_level(self, j):
        return j in self.a[1:]

    def seam_index_of_level(self, j):
        return self.a.index(j)

    def is_split_level(self, j):
        if self.split == 'none' or j < SPLIT_FROM:
            return False
        if self.split == 'interior' and self.is_seam_level(j):
            return False
        if j >= self.a[-1]:
            raise ValueError('level beyond table')
        return True

    def beta(self, j):
        if self.orient == 'top':
            return 'T'
        if self.orient == 'bot':
            return 'B'
        if self.orient == 'mixTB':
            return 'T' if j % 2 == 0 else 'B'
        if self.orient == 'halfBT':
            # B on the lower half of each stage's levels, T on the upper;
            # stage k levels are (a_k, a_{k+1}]; seam level a_{k+1} gets T,
            # first level of next stage gets B => seam juncture (T,B): OK.
            k = self.stage_of_octave(j)
            mid = (self.a[k] + self.a[k + 1]) / 2
            return 'B' if j <= mid else 'T'
        raise ValueError(self.orient)

    def planted_member(self, j):
        """The pair-j member donated to the partner (None if unsplit)."""
        if not self.is_split_level(j):
            return None
        return (1 << j) if self.beta(j) == 'T' else (1 << j) - 1

    # ---- membership with zones
    def zone(self, v):
        """(zone_kind, aux, team).  Kinds: plant/kpair/bsliv/tsliv/kept."""
        j = self.octave(v)
        k = self.stage_of_octave(j)
        own = self.owner(k)
        partner = 'B' if own == 'A' else 'A'
        # pair values at split levels (checked first: plants override
        # slivers; slivers never contain pair values of OTHER levels)
        if v in ((1 << j) - 1, 1 << j) and self.is_split_level(j):
            if v == self.planted_member(j):
                return ('plant', j, partner)
            return ('kpair', j, own)
        # top sliver of seam a_k' = j (v near the top of stage k's last
        # octave): j must be a boundary a_{k+1}; receiving team = owner
        # of stage k+1
        if self.is_seam_level(j):
            ks = self.a.index(j)          # seam index: boundary a_{ks}
            t = self.tau(ks)
            if t and v > (1 << j) - t:
                return ('tsliv', ks, self.owner(ks))
        # bottom sliver of seam a_k (v near the bottom of stage k's first
        # octave): j = a_k + 1; receiving team = owner of stage k-1
        if k >= 1 and j == self.a[k] + 1:
            s = self.sigma(k)
            if s and v <= (1 << self.a[k]) + s:
                return ('bsliv', k, self.owner(k - 1))
        return ('kept', k, own)

    def team(self, v):
        return self.zone(v)[2]


def make_variants():
    tri = tri_bounds()
    quad = quad_bounds()
    grow = lambda k: k + 2          # noqa: E731
    const6 = lambda k: 6            # noqa: E731
    tau4 = lambda k: 4              # noqa: E731
    return [
        Variant('tri_top', tri, orient='top'),
        Variant('tri_bot', tri, orient='bot'),
        Variant('tri_mixTB', tri, orient='mixTB'),
        Variant('tri_top_sliv', tri, sigma=grow, orient='top'),
        Variant('tri_tau4_int', tri, tau=tau4, orient='top',
                split='interior'),
        Variant('quad_top', quad, orient='top'),
        Variant('quad_bot_sliv6', quad, sigma=const6, orient='bot'),
        Variant('tri_halfBT', tri, orient='halfBT'),
        Variant('tri_none', tri, split='none'),
    ]


SEAMS = {'tri': [2, 3, 4], 'quad': [2, 3]}   # seam indices k: a_k = m-level


# ---------------------------------------------------------------- CHECK 0

def check0(variants):
    print('== CHECK 0: partition sanity ==')
    ok = True
    for V in variants:
        teams = [V.team(v) for v in range(1, SANITY_N + 1)]
        nA = teams.count('A')
        nB = teams.count('B')
        good = nA + nB == SANITY_N
        ok &= good
        print(f'  {V.name:16s} A={nA} B={nB} cover={good}')
        # spot: big values exact
        for v in (1 << 20, (1 << 20) - 1, (1 << 22) + 5):
            V.team(v)
    return ok


# ---------------------------------------------------------------- CHECK A

def pair_level(v):
    """j if v in {2^j - 1, 2^j} else None."""
    j = (v - 1).bit_length()
    return j if v in ((1 << j) - 1, 1 << j) else None


def classify(V, x, y, z, seam_k):
    """(channel, tag) for the in-team triple (x, y, z) with y in the
    window of seam seam_k, or raise.  tag = the seam index the channel
    instance belongs to (C1/C2/C4/C5/FAN/SLIVIN) or the level j (DUST).
    Only zones of y and z matter (x is any small in-team value)."""
    zy, zz = V.zone(y), V.zone(z)
    ky, ay = zy[0], zy[1]
    kz, az = zz[0], zz[1]
    # DUST first: both endpoints are pair-values at ADJACENT levels with
    # at least one planted — the (1, 2^j, 2^{j+1}-1) coupling family.
    py, pz = pair_level(y), pair_level(z)
    if py is not None and pz == py + 1 and 'plant' in (ky, kz):
        return 'DUST', py
    if ky in ('kept', 'kpair') and kz in ('kept', 'kpair'):
        sy = ay if ky == 'kept' else V.stage_of_octave(ay)
        sz = az if kz == 'kept' else V.stage_of_octave(az)
        if sy == sz:
            return 'C0', sy
        raise AssertionError(f'X2/cross-stage kept triple {x, y, z} '
                             f'stages {sy}->{sz}')
    if kz == 'bsliv' and ky in ('kept', 'kpair'):
        if V.octave(y) == V.a[az]:
            return 'C1', az
        raise AssertionError(f'C1 middle outside top octave {x, y, z}')
    if ky == 'bsliv' and kz == 'plant' and az == V.a[ay] + 1:
        return 'C2', ay
    if ky == 'bsliv' and kz == 'bsliv' and ay == az:
        # in-sliver AP: needs x = 2y - z >= 2 lo - hi of the sliver,
        # i.e. x scale-adapted at that seam — empty for fixed x once
        # 2^{a_k} outgrows x + sigma_k.  Bounded-description family.
        mp = 1 << V.a[ay]
        if x >= mp + 2 - V.sigma(ay):
            return 'SLIVIN', ay
        raise AssertionError(f'in-sliver AP with small x {x, y, z}')
    if ky == 'tsliv' and kz == 'tsliv' and ay == az:
        mp = 1 << V.a[ay]
        if x >= (mp - 2 * V.tau(ay)) - mp + 2 + 2 * 0:  # x >= 2lo-hi+2
            return 'TSLIVIN', ay
        raise AssertionError(f'in-tsliver AP with small x {x, y, z}')
    if ky == 'tsliv' and kz in ('kept', 'kpair'):
        return 'C4', ay
    if ky == 'plant' and kz == 'tsliv' and ay == V.a[az] - 1:
        return 'C5', az
    if ky == 'plant' and V.is_seam_level(ay) and kz in ('kept', 'kpair'):
        return 'FAN', V.seam_index_of_level(ay)
    raise AssertionError(
        f'unclassified triple {x, y, z} zones {zy} {zz} seam {seam_k}')


def checkA(variants):
    print('== CHECK A: seam-law catalogue (brute force vs formulas) ==')
    all_ok = True
    rows = []
    for V in variants:
        fam = 'tri' if V.a == tri_bounds() else 'quad'
        for sk in SEAMS[fam]:
            s_level = V.a[sk]
            m = 1 << s_level
            sig, tau = V.sigma(sk), V.tau(sk)
            O_team = V.owner(sk - 1)
            N_team = V.owner(sk)
            ylo, yhi = 1 << (s_level - 2), 1 << (s_level + 2)
            found = {}
            for x in range(1, XMAX + 1):
                tx = V.team(x)
                for y in range(max(ylo, x) + 1, yhi + 1):
                    if V.team(y) != tx:
                        continue
                    z = 2 * y - x
                    if V.team(z) != tx:
                        continue
                    ch, tag = classify(V, x, y, z, sk)
                    found.setdefault((x, ch, tag), []).append((y, z))
            # ---- formula assertions
            ok = True

            def expect(cond, label):
                nonlocal ok, all_ok
                if not cond:
                    ok = all_ok = False
                    print(f'  MISMATCH {V.name} seam a_{sk}={s_level}: '
                          f'{label}')

            for x in range(1, XMAX + 1):
                tx = V.team(x)
                # C1 at THIS seam: attacked team O; iff sigma>=2 or
                # (sigma=1 & x odd); count by parity
                c1 = found.get((x, 'C1', sk), [])
                if tx == O_team:
                    want = ((sig + 1) // 2) if x % 2 == 1 else (sig // 2)
                else:
                    want = 0
                expect(len(c1) == want,
                       f'C1 x={x} count {len(c1)} != {want}')
                # C2 at THIS seam: sliver middle -> plant(a_k+1) into O
                c2 = found.get((x, 'C2', sk), [])
                pm = V.planted_member(s_level + 1)
                w2 = 0
                if pm is not None and tx == O_team and sig \
                        and V.zone(pm)[2] == O_team:
                    if V.beta(s_level + 1) == 'T' and x % 2 == 0 \
                            and 2 <= x <= 2 * sig:
                        w2 = 1
                    if V.beta(s_level + 1) == 'B' and x % 2 == 1 \
                            and 3 <= x <= 2 * sig + 1:
                        w2 = 1
                expect(len(c2) == w2, f'C2 x={x} count {len(c2)} != {w2}')
                # C4 at THIS seam: top-sliver middles, team N: count =
                # #w in [0,tau-1] with completion 2m-2w-x a kept N value
                c4 = found.get((x, 'C4', sk), [])
                w4 = 0
                if tx == N_team and tau:
                    for w in range(0, tau):
                        zc = 2 * m - 2 * w - x
                        if zc <= m:
                            continue
                        kz, az, tz = V.zone(zc)
                        if tz == N_team and kz in ('kept', 'kpair'):
                            w4 += 1
                expect(len(c4) == w4, f'C4 x={x} count {len(c4)} != {w4}')
                # C5 at THIS seam: plant(a_k - 1) -> tsliv, team N
                c5 = found.get((x, 'C5', sk), [])
                pm5 = V.planted_member(s_level - 1)
                w5 = 0
                if pm5 is not None and tx == N_team and tau:
                    if V.zone(pm5)[2] == N_team:
                        # beta=T: z = 2^s - x is a pair value at x = 1
                        # (the DUST coupling (1, 2^{s-1}, 2^s - 1)), so
                        # C5 proper starts at x = 2
                        if V.beta(s_level - 1) == 'T' and 2 <= x <= tau - 1:
                            w5 = 1
                        if V.beta(s_level - 1) == 'B' and 1 <= x <= tau - 3:
                            w5 = 1
                expect(len(c5) == w5, f'C5 x={x} count {len(c5)} != {w5}')
                # FAN at THIS seam: planted seam member p, kept completion
                fan = found.get((x, 'FAN', sk), [])
                pms = V.planted_member(s_level)
                wf = 0
                if pms is not None and tx == N_team:
                    zc = 2 * pms - x
                    if zc > m and pair_level(zc) != s_level + 1:
                        kz, az, tz = V.zone(zc)
                        if tz == N_team and kz in ('kept', 'kpair'):
                            wf = 1
                expect(len(fan) == wf, f'FAN x={x} count {len(fan)} != {wf}')
                # DUST: x = 1 only, exactly at the predicted junctures
                du = [k for k in found
                      if k[0] == x and k[1] == 'DUST']
                wd = set()
                if x == 1 and tx == V.team(1):
                    for jj in range(s_level - 1, s_level + 3):
                        y_v = 1 << jj
                        z_v = (1 << (jj + 1)) - 1
                        if not (ylo < y_v <= yhi):
                            continue
                        if V.team(y_v) == tx and V.team(z_v) == tx:
                            zy, zz2 = V.zone(y_v), V.zone(z_v)
                            if 'plant' in (zy[0], zz2[0]):
                                wd.add(jj)
                expect({k[2] for k in du} == wd,
                       f'DUST x={x} levels {sorted(k[2] for k in du)} '
                       f'!= {sorted(wd)}')
                if x > 1:
                    expect(not du, f'DUST with x={x}')
            # global: C0 present for both teams; SLIVIN only scale-adapted
            c0_teams = {V.team(k[0]) for k in found if k[1] == 'C0'}
            expect(len(c0_teams) == 2, f'C0 teams {c0_teams}')
            if V.split == 'none' and sig == 0 and tau == 0:
                non_c0 = {k[1] for k in found if k[1] != 'C0'}
                expect(not non_c0, f'none-variant extra channels {non_c0}')
            if V.orient == 'halfBT':
                expect(not any(k[1] == 'DUST' for k in found),
                       'halfBT has DUST')
            counts = {}
            for k, lst in found.items():
                ch = k[1] if k[2] == sk or k[1] in ('C0', 'DUST') \
                    else f'{k[1]}@{k[2]}'
                counts[ch] = counts.get(ch, 0) + len(lst)
            rows.append({'variant': V.name, 'seam_level': s_level,
                         'm': m, 'sigma': sig, 'tau': tau,
                         'channel_counts': counts, 'ok': ok})
            print(f'  {V.name:16s} seam a_{sk}={s_level:2d} m={m:5d} '
                  f'sig={sig} tau={tau} channels={counts} '
                  f'{"OK" if ok else "FAIL"}')
    return all_ok, rows


# ------------------------------------------------------- CHECKs B, C, D

C3_UNITS = lambda M: [(2 * M - 5, M + 5), (2 * M - 3, M + 6),   # noqa: E731
                      (2 * M - 10, M + 3)]


def run_sat(tag, V, units, budget, results, want=None):
    t0 = time.time()
    r = ap_order_sat(sorted(V), units=units, budget=budget)
    r['tag'] = tag
    r['want'] = want
    verdict = r['result']
    star = ''
    if want and verdict != 'TIMEOUT':
        star = ' ***UNEXPECTED***' if verdict != want else ' (as expected)'
    print(f'  {tag:44s} {verdict:7s} n={r["n"]} units={r["units"]} '
          f'[{r["time"]}s]{star}', flush=True)
    results.append(r)
    return r


def checkB(results, budget):
    print('== CHECK B: C3 core vs top-pair puncture '
          '(rung content of T-PIN-STAGE on split-crown blocks) ==')
    for M in (64, 128, 256):
        W = list(range(M + 1, 2 * M + 1))
        run_sat(f'B intact M={M} (control)', W, C3_UNITS(M), budget,
                results, want='UNSAT')
        run_sat(f'B minus{{2M}} M={M}', [v for v in W if v != 2 * M],
                C3_UNITS(M), budget, results)
        run_sat(f'B minus{{2M-1}} M={M}', [v for v in W if v != 2 * M - 1],
                C3_UNITS(M), budget, results)
        run_sat(f'B minus both M={M}', [v for v in W if v < 2 * M - 1],
                C3_UNITS(M), budget, results)
    Mc = 68     # == 4 mod 8: C3 satisfiable -> engine sanity
    W = [v for v in range(Mc + 1, 2 * Mc + 1) if v != 2 * Mc]
    run_sat(f'B minus{{2M}} M={Mc} (4 mod 8 control)', W, C3_UNITS(Mc),
            budget, results, want='SAT')


def stg_units(V, F):
    Vs = set(V)
    units = []
    for x in F:
        for y in V:
            z = 2 * y - x
            if z in Vs and z != y:
                units.append((z, y))
    return units


def checkC(results, budget, fast):
    print('== CHECK C: stage rung STG(M, F) — two consecutive in-team '
          'blocks + fixed attackers ==')
    scales = (64, 128) if fast else (64, 128, 256)
    for M in scales:
        intact = list(range(M + 1, 4 * M + 1))
        punct = [v for v in intact if v not in (2 * M, 4 * M)]
        for F, ftag in (((3,), 'x3'), ((15,), 'x15'),
                        ((15, 16), 'p15_16'), ((21, 22), 'p21_22')):
            run_sat(f'C intact M={M} F={ftag}', intact,
                    stg_units(intact, F), budget, results)
            run_sat(f'C punct M={M} F={ftag}', punct,
                    stg_units(punct, F), budget, results)


def checkD(results, budget, fast):
    print('== CHECK D: per-j spot — OG_5 pair rung {31,32} on (M, 2M] ==')
    scales = (64, 128) if fast else (64, 128, 256)
    for M in scales:
        W = list(range(M + 1, 2 * M + 1))
        run_sat(f'D OG5 M={M} F={{31,32}}', W, stg_units(W, (31, 32)),
                budget, results)


# ---------------------------------------------------------------- CHECK E

def checkE(variants):
    print('== CHECK E: T-PIN-STAGE bookkeeping ==')
    ok = True
    for V in variants[:1] + variants[5:6]:
        a = V.a
        interior = [max(0, (a[k + 1] - a[k]) - 2)
                    for k in range(len(a) - 1)]
        totalA = sum(c for k, c in enumerate(interior) if k % 2 == 0)
        totalB = sum(c for k, c in enumerate(interior) if k % 2 == 1)
        grow = all(interior[k + 2] > interior[k]
                   for k in range(2, len(interior) - 2))
        ok &= grow and totalA > 50 and totalB > 50
        print(f'  {V.name:12s} interior blocks/stage (k<=8): '
              f'{interior[:9]} cumA={totalA} cumB={totalB} '
              f'strictly growing={grow}')
        # disjointness: octave windows are distinct scales — trivially
        # disjoint; assert on a sample
        blocks = []
        for k in range(2, 8):
            for j in range(a[k] + 2, a[k + 1]):
                blocks.append((1 << (j - 1), 1 << j))
        assert all(b1[1] <= b2[0] or b2[1] <= b1[0]
                   for i, b1 in enumerate(blocks)
                   for b2 in blocks[i + 1:])
    print(f'  disjointness + divergence: {"OK" if ok else "FAIL"}')
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fast', action='store_true')
    ap.add_argument('--budget', type=float, default=2400)
    ap.add_argument('--skip-sat', action='store_true')
    args = ap.parse_args()

    variants = make_variants()
    out = {'when': time.strftime('%Y-%m-%d %H:%M:%S')}
    out['check0'] = check0(variants)
    okA, rowsA = checkA(variants)
    out['checkA_ok'] = okA
    out['checkA_rows'] = rowsA
    out['checkE'] = checkE(variants)
    sat_rows = []
    if not args.skip_sat:
        checkB(sat_rows, args.budget)
        checkD(sat_rows, args.budget, args.fast)
        checkC(sat_rows, args.budget, args.fast)
    out['sat_rows'] = sat_rows
    path = os.path.join(REPO, 'data', 'g4b_results.json')
    with open(path, 'w') as f:
        json.dump(out, f, indent=1)
    print(f'wrote {path}')
    print(f'CHECK 0={out["check0"]} A={okA} E={out["checkE"]}')


if __name__ == '__main__':
    main()
