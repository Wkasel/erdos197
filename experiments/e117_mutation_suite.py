"""e117_mutation_suite: AUDIT A2 -- mutation testing of the two C3-core
proof checkers:

  e113_c3_hand_proof.py    (schema checker: executes the notes/33 hand
                            proof rung-by-rung through assertion-guarded
                            rule/trans primitives)
  e113b_closure_crossval.py (independent cross-validation by the e109
                            closure engine)

Method: for each mutation, textually edit a COPY of the checker source
(exact-match anchors, uniqueness asserted), exec it in a fresh namespace,
and run the checking entry points at small scales.  A mutation is
REJECTED when either the exec or any entry-point call raises, or a
crossval entry point returns False (its failure signal).  A mutation
that runs to completion is a HOLE in the checker.

Mutation kinds (per the audit brief):
  (i)    AP triple with wrong arithmetic            MUT-01
  (ii)   rule applied with violated precondition    MUT-02, MUT-16
  (iii)  wrong residue condition (G4 center at
         M = 4 mod 8)                               MUT-03, MUT-03b
  (iv)   flipped conclusion literal                 MUT-04
  (v)    off-by-one interval end                    MUT-05, MUT-05b
  (vi)   dropped case/phase branch                  MUT-06, MUT-17,
                                                    MUT-14, MUT-14b
  (vii)  wrong mirror value                         MUT-07
  (viii) transitivity gap in a chain                MUT-08
  (ix)   wrong leader/trailer status                MUT-09a, MUT-09b
  (x)    tampered final contradiction / axiom set   MUT-10, MUT-10b,
                                                    MUT-15a/b/c
  (+)    derivation-bypass probes (fact smuggling)  MUT-11, MUT-11b
  (+)    closure-engine integrity probes            MUT-12, MUT-13

Anchors are given as candidate lists so the suite runs against both the
pre-patch and the patched (hypothesis-discipline) e113.

Run: .venv/bin/python experiments/e117_mutation_suite.py [--json PATH]
Output: data/e117_mutation_suite.json
"""
import json
import sys

ROOT = "/Users/will/Dev/personal/tasks/math/erdos197"
E113 = f"{ROOT}/experiments/e113_c3_hand_proof.py"
E113B = f"{ROOT}/experiments/e113b_closure_crossval.py"
DATA = f"{ROOT}/data/e117_mutation_suite.json"


def mutate(src, subs):
    """subs: list of candidate lists [(old, new), ...]; per list, exactly
    one candidate `old` must occur (exactly once) in src -- the others
    must be absent.  Applies the matching replacement."""
    for cands in subs:
        hits = [(o, n) for (o, n) in cands if src.count(o) > 0]
        assert len(hits) == 1, f"anchor matches: {len(hits)} of {len(cands)}"
        o, n = hits[0]
        assert src.count(o) == 1, f"anchor not unique ({src.count(o)}x)"
        src = src.replace(o, n)
    return src


def brief(ex):
    s = repr(ex)
    return s if len(s) <= 200 else s[:200] + "..."


def run_mutant(path, subs, calls):
    """Returns (verdict, detail, per_call).  verdict CAUGHT/PASSED."""
    src = mutate(open(path).read(), subs)
    ns = {"__name__": "e117_mutant", "__file__": path}
    try:
        exec(compile(src, path + "[mutant]", "exec"), ns)
    except Exception as ex:
        return "CAUGHT", f"at exec/import: {brief(ex)}", []
    per_call = []
    caught = None
    for fn, arg in calls:
        try:
            r = ns[fn](arg)
            if r is False:
                per_call.append([fn, arg, "returned False"])
                caught = caught or f"{fn}({arg}) returned False"
            else:
                per_call.append([fn, arg, "ok"])
        except Exception as ex:
            per_call.append([fn, arg, brief(ex)])
            caught = caught or f"{fn}({arg}): {brief(ex)}"
    if caught:
        return "CAUGHT", caught, per_call
    return "PASSED", None, per_call


# ---------------------------------------------------------------- anchors
# e113: blocks shared pre/post-patch
FLIP_EVEN2_I_BLOCK = """\
        lemma_P(ctx, cI, 2, ev, (m0, 'out'), 'lead', [t10])
        ctx.trans(cI, t10, b3)                       # A3
        ctx.rule(b3, cI, t5, (cI, b3), (cI, t5))     # mirror R4
        ctx.trans(cI, t5, b5)                        # A1
"""

LEMMA_P_OUT_UP = """\
            ctx.trans(c, u, u_out)
            lo, hi = min(u_out, 2 * c - u_out), max(u_out, 2 * c - u_out)
            ctx.rule(lo, c, hi, (c, u_out), (c, 2 * c - u_out))
"""

LEMMA_P_OUT_UP_MUT = """\
            ctx.trans(c, u, u_out)
            lo, hi = min(u_out, 2 * c - u_out + 2), max(u_out, 2 * c - u_out + 2)
            ctx.rule(lo, c, hi, (c, u_out), (c, 2 * c - u_out + 2))
"""

MUTATIONS = [
    dict(
        id="MUT-01", kind="(i) wrong AP arithmetic", target="e113",
        desc="mirror AP (b3, m-1, t5) in flip Case I replaced by the "
             "non-AP triple (b3, m-1, t3): b3+t3 = 3M != 2(m0-1)",
        subs=[[(
            "        ctx.rule(b3, cI, t5, (cI, b3), (cI, t5))     # mirror R4",
            "        ctx.rule(b3, cI, t3, (cI, b3), (cI, t3))     # mirror R4",
        )]],
        calls=[("check_flip", 16), ("check_flip", 24)]),
    dict(
        id="MUT-02", kind="(ii) violated precondition", target="e113",
        desc="G4-inward flood in flip Case I seeded with tag 'out' "
             "(claims m-1 < m+1) though only (m+1, m-1) is a fact",
        subs=[[(
            "        lemma_P(ctx, cI, 4, la, (cI + 2, 'in'), 'trail', [b5])",
            "        lemma_P(ctx, cI, 4, la, (cI + 2, 'out'), 'trail', [b5])",
        )]],
        calls=[("check_flip", 16), ("check_flip", 24)]),
    dict(
        id="MUT-03", kind="(iii) wrong residue (G4 center at 4 mod 8)",
        target="e113",
        desc="flip schema run at M = 4 mod 8 with BOTH the entry residue "
             "guard and the explicit mod-8 lock assert stripped -- the "
             "deep leader-membership asserts must still reject",
        subs=[
            [("    assert M % 8 == 0", "    assert M % 4 == 0")],
            [("    assert cI % 4 == 3 and cII % 4 == 1   # the mod-8 lock",
              "    _ = (cI, cII)   # [MUT] mod-8 lock assert stripped")],
        ],
        calls=[("check_flip", 20), ("check_flip", 28)]),
    dict(
        id="MUT-03b", kind="(iii) wrong residue (sharpness tamper)",
        target="e113",
        desc="sharpness check claims m0-1 = 1 mod 4 is a valid Case-I "
             "G4 center residue at M = 4 mod 8",
        subs=[[(
            "    ok1 = (m0 - 1) % 4 == 3     # class condition for Case I center",
            "    ok1 = (m0 - 1) % 4 == 1     # class condition for Case I center",
        )]],
        calls=[("sharpness_4mod8", 20), ("sharpness_4mod8", 28)]),
    dict(
        id="MUT-04", kind="(iv) flipped conclusion literal", target="e113",
        desc="mirror R3 on (b5, m+1, t3) in flip Case II concludes "
             "(m+1, b5) instead of (b5, m+1)",
        subs=[[(
            "        ctx.rule(b5, cII, t3, (t3, cII), (b5, cII))  # mirror R3",
            "        ctx.rule(b5, cII, t3, (t3, cII), (cII, b5))  # mirror R3",
        )]],
        calls=[("check_flip", 16), ("check_flip", 24)]),
    dict(
        id="MUT-05", kind="(v) off-by-one interval end", target="e113",
        desc="odd ladder gets one extra rung: last value 2M+1 lies "
             "outside (M, 2M]",
        subs=[[(
            "    return M + 1, 2, M // 2",
            "    return M + 1, 2, M // 2 + 1",
        )]],
        calls=[("check_layer1", 16), ("check_layer1", 20),
               ("check_flip", 16)]),
    dict(
        id="MUT-05b", kind="(v) off-by-one interval end (d=4)",
        target="e113",
        desc="d=4 ladder count off by one: rung beyond 2M",
        subs=[[(
            "    count = (2 * M - first) // 4 + 1",
            "    count = (2 * M - first) // 4 + 2",
        )]],
        calls=[("check_layer1", 16), ("check_flip", 16)]),
    dict(
        id="MUT-06", kind="(vi) dropped case branch", target="e113",
        desc="layer1 Case I runs only one LADB phase branch",
        subs=[[(
            "    # ---- Case I: t5 < m0 ----\n"
            "    # (a) G4-inward at c* over class B: b3 < c*   "
            "[both LADB phases]\n"
            "    for lf in (True, False):",
            "    # ---- Case I: t5 < m0 ----\n"
            "    # (a) G4-inward at c* over class B: b3 < c*   "
            "[both LADB phases]\n"
            "    for lf in (True,):",
        )]],
        calls=[("check_layer1", 16), ("check_layer1", 20)]),
    dict(
        id="MUT-17", kind="(vi) dropped case branch", target="e113",
        desc="flip Case II (LADB loop) dropped entirely",
        subs=[[(
            "    # ---- Case II: m0 < t5 ----\n"
            "    for lf in (True, False):        # LADB phases",
            "    # ---- Case II: m0 < t5 ----\n"
            "    for lf in ():                   # LADB phases [MUT]",
        )]],
        calls=[("check_flip", 16), ("check_flip", 24)]),
    dict(
        id="MUT-07", kind="(vii) wrong mirror value", target="e113",
        desc="lemma_P outward-up induction reflects through the wrong "
             "mirror 2c-w+2 (consistently, so only the AP arithmetic "
             "check can see it)",
        subs=[[(LEMMA_P_OUT_UP, LEMMA_P_OUT_UP_MUT)]],
        calls=[("check_layer1", 16), ("check_layer1", 20)]),
    dict(
        id="MUT-08", kind="(viii) transitivity gap", target="e113",
        desc="flip Case II chain t3 < b6 < m+1 replaced by broken chain "
             "t3 < t10 < m+1 ((t3, t10) never derived)",
        subs=[[(
            "        ctx.trans(t3, b6, cII)                       # A2",
            "        ctx.trans(t3, t10, cII)                      # A2",
        )]],
        calls=[("check_flip", 16), ("check_flip", 24)]),
    dict(
        id="MUT-09a", kind="(ix) wrong leader/trailer status",
        target="e113",
        desc="lemma_Z returns the trailer rungs as the leader set",
        subs=[[(
            "    leaders = {lad[i2] for i2 in range(e % 2, count, 2)}",
            "    leaders = {lad[i2] for i2 in range((e + 1) % 2, count, 2)}",
        )]],
        calls=[("check_layer1", 16), ("check_flip", 16)]),
    dict(
        id="MUT-09b", kind="(ix) wrong leader/trailer status",
        target="e113",
        desc="fiat_zig claims leaders but orients their downward edges "
             "as trailers",
        subs=[[
            ("            ctx.facts.add((lad[i], lad[i - 1]))",
             "            ctx.facts.add((lad[i - 1], lad[i]))"),
            ("            ctx.assume(lad[i], lad[i - 1])",
             "            ctx.assume(lad[i - 1], lad[i])"),
        ]],
        calls=[("check_layer1", 16), ("check_flip", 16)]),
    dict(
        id="MUT-10", kind="(x) tampered final contradiction",
        target="e113",
        desc="axiom A3 (t10, b3) silently removed from the layer1 "
             "hypothesis base; the Case-I closing 3-cycle must fail to "
             "consume it",
        subs=[[
            ("        ctx.facts.update([(t3, b6), (t10, b3), (b3, b5)])",
             "        ctx.facts.update([(t3, b6), (b3, b5)])"),
            ("        ctx.assume_all([(t3, b6), (t10, b3), (b3, b5)])",
             "        ctx.assume_all([(t3, b6), (b3, b5)])"),
        ]],
        calls=[("check_layer1", 16), ("check_layer1", 20)]),
    dict(
        id="MUT-10b", kind="(x) tampered final contradiction",
        target="e113",
        desc="flip Case I branch conclusions tampered to the non-"
             "opposite pair (b5, m-1) vs (m-1, b3) -- both derivable, "
             "but they close no cycle",
        subs=[[(
            "    concIa, concIb = (b5, cI), (cI, b5)      "
            "# Case I: LADA vs EVEN2",
            "    concIa, concIb = (b5, cI), (cI, b3)      "
            "# Case I: LADA vs EVEN2",
        )]],
        calls=[("check_flip", 16), ("check_flip", 24)]),
    dict(
        id="MUT-11", kind="(+) derivation bypass", target="e113",
        desc="flip Case I EVEN2 derivation chain replaced by directly "
             "injecting the conclusion into ctx.facts (raw set add, "
             "bypassing rule/trans)",
        subs=[[(
            FLIP_EVEN2_I_BLOCK,
            "        ctx.facts.add((cI, b5))  # [MUT] fiat conclusion\n",
        )]],
        calls=[("check_flip", 16), ("check_flip", 24)]),
    dict(
        id="MUT-11b", kind="(+) derivation bypass via assume",
        target="e113",
        desc="flip Case I EVEN2 derivation chain replaced by smuggling "
             "the conclusion in as a hypothesis (assume); only "
             "meaningful against the patched checker",
        subs=[[(
            FLIP_EVEN2_I_BLOCK,
            "        ctx.assume(cI, b5)  # [MUT] smuggled hypothesis\n",
        )]],
        calls=[("check_flip", 16), ("check_flip", 24)],
        note="pre-patch this dies on AttributeError (no assume method): "
             "vacuous; the post-patch run is the real test"),
    dict(
        id="MUT-16", kind="(ii)/(ix) wrong flood class", target="e113",
        desc="layer1 Case I G4 flood fed the mod-4 class A ladder "
             "(offsets 1 mod 4) instead of class B",
        subs=[[(
            "        lb = fiat_zig(ctx, *lad4(M, 3), lf)\n"
            "        lemma_P(ctx, cstar, 4, lb, (cstar + 2, 'in'), "
            "'trail', [b3])",
            "        lb = fiat_zig(ctx, *lad4(M, 1), lf)\n"
            "        lemma_P(ctx, cstar, 4, lb, (cstar + 2, 'in'), "
            "'trail', [b3])",
        )]],
        calls=[("check_layer1", 16), ("check_layer1", 20)]),
    # ------------------------------------------------ e113b mutations
    dict(
        id="MUT-12", kind="(+) implication table tamper", target="e113b",
        desc="one implication dropped from the closure engine's table; "
             "verify_engine's brute-force re-derivation must catch the "
             "mismatch at import",
        subs=[[(
            "    tr = Tracer(M)\n",
            "    tr = Tracer(M)\n"
            "    _k = sorted(tr.imp)[0]\n"
            "    tr.imp[_k] = tr.imp[_k][1:]  # [MUT]\n",
        )]],
        calls=[("cross_l1", 16)]),
    dict(
        id="MUT-13", kind="(+) unsound closure engine", target="e113b",
        desc="engine wrapped to report contradiction unconditionally; "
             "the AP-free-witness canary must fire at import",
        subs=[[(
            "from e109_l0_trace import Tracer",
            "from e109_l0_trace import Tracer as _BaseTracer\n\n\n"
            "class Tracer(_BaseTracer):  # [MUT] unsound wrapper\n"
            "    def run(self, units):\n"
            "        _BaseTracer.run(self, units)\n"
            "        return True",
        )]],
        calls=[("cross_l1", 16)]),
    dict(
        id="MUT-14", kind="(vi) dropped phase branch", target="e113b",
        desc="one of the four phase axioms dropped from the layer1 "
             "crossval tree",
        subs=[[(
            "    phases = [(b3, b7), (b7, b3), (b1, b5), (b5, b1)]",
            "    phases = [(b3, b7), (b7, b3), (b1, b5)]",
        )]],
        calls=[("cross_l1", 16)]),
    dict(
        id="MUT-14b", kind="(vi) dropped case branch", target="e113b",
        desc="one order of the (t5, m0) split dropped from the layer1 "
             "crossval tree",
        subs=[[(
            "    splits = [(t5, m0), (m0, t5)]",
            "    splits = [(t5, m0)]",
        )]],
        calls=[("cross_l1", 16)]),
    dict(
        id="MUT-15a", kind="(x) tampered axiom set (removal)",
        target="e113b",
        desc="axiom A3 removed from the layer1 crossval base: the "
             "closure must fail to close some branch",
        subs=[[(
            "    base = [(t3, b6), (t10, b3), (b3, b5)]",
            "    base = [(t3, b6), (b3, b5)]",
        )]],
        calls=[("cross_l1", 16), ("cross_l1", 20)]),
    dict(
        id="MUT-15b", kind="(x) tampered axiom set (orientation flip)",
        target="e113b",
        desc="axiom A3 flipped to (b3, t10) in the layer1 crossval base",
        subs=[[(
            "    base = [(t3, b6), (t10, b3), (b3, b5)]",
            "    base = [(t3, b6), (b3, t10), (b3, b5)]",
        )]],
        calls=[("cross_l1", 16), ("cross_l1", 20)]),
    dict(
        id="MUT-15c", kind="(x) tampered axiom set (flip tree)",
        target="e113b",
        desc="axiom A1 (t5, b5) removed from the flip crossval base",
        subs=[[(
            "    base = [(t5, b5), (t3, b6), (t10, b3), (b5, b3)]",
            "    base = [(t3, b6), (t10, b3), (b5, b3)]",
        )]],
        calls=[("cross_flip", 16), ("cross_flip", 24)]),
]

CONTROLS = [
    dict(id="CTRL-e113", target="e113", subs=[],
         calls=[("check_layer1", 16), ("check_layer1", 20),
                ("check_flip", 16), ("check_flip", 24),
                ("sharpness_4mod8", 20)]),
    dict(id="CTRL-e113b", target="e113b", subs=[],
         calls=[("cross_l1", 16), ("cross_flip", 16)]),
]


def main():
    json_path = DATA
    if "--json" in sys.argv:
        json_path = sys.argv[sys.argv.index("--json") + 1]
    paths = {"e113": E113, "e113b": E113B}
    results, holes = [], []
    # identity controls: unmutated checkers must accept the true proof
    for c in CONTROLS:
        verdict, detail, per_call = run_mutant(
            paths[c["target"]], c["subs"], c["calls"])
        ok = verdict == "PASSED"
        print(f"{c['id']:9s}  {'OK (true proof accepted)' if ok else 'BROKEN'}"
              f"  {detail or ''}")
        results.append(dict(id=c["id"], control=True, ok=ok, detail=detail,
                            per_call=per_call))
        assert ok, f"control failed: {c['id']} {detail}"
    # mutants: every one must be rejected
    for m in MUTATIONS:
        verdict, detail, per_call = run_mutant(
            paths[m["target"]], m["subs"], m["calls"])
        mark = "caught" if verdict == "CAUGHT" else "** HOLE (passed) **"
        print(f"{m['id']:9s}  {mark:20s} {m['kind']}")
        if detail:
            print(f"           `- {detail}")
        results.append(dict(id=m["id"], kind=m["kind"], target=m["target"],
                            desc=m["desc"], verdict=verdict, detail=detail,
                            per_call=per_call, note=m.get("note")))
        if verdict == "PASSED":
            holes.append(m["id"])
    n = len(MUTATIONS)
    caught = n - len(holes)
    print(f"\nmutations: {n} tested, {caught} caught, holes: {holes or 'none'}")
    json.dump(dict(tested=n, caught=caught, holes=holes, results=results),
              open(json_path, "w"), indent=1)
    print(f"-> {json_path}")
    if holes:
        sys.exit(1)


if __name__ == "__main__":
    main()
