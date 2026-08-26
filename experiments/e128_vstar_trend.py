"""Serialized v*(M) trend scan: the ledger's decisive measurement.
Runs e127 queries one at a time to respect memory. Order: bisect bal@16
(known UNSAT v<=2, SAT v>=160), then bal@24 base points."""
import subprocess, sys, time

QUERIES = [
    ("bal", 16, "8"),
    ("bal", 16, "32"),   # bisection continues based on log inspection
    ("bal", 16, "80"),
    ("bal", 24, "0"),
    ("bal", 24, "1"),
]
for mode, M, vs in QUERIES:
    t0 = time.time()
    cmd = [".venv/bin/python", "experiments/e127_seam_budget.py", mode,
           "--M", str(M), "--vs", vs, "--budget", "14400",
           "--tag", f"e128_{mode}{M}_v{vs}"]
    print(f"RUN {' '.join(cmd)}", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout[-2000:], flush=True)
    if r.returncode != 0:
        print(f"STDERR: {r.stderr[-500:]}", flush=True)
    print(f"({time.time()-t0:.0f}s)", flush=True)
print("E128 COMPLETE", flush=True)
