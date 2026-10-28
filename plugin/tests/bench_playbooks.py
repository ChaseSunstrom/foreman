#!/usr/bin/env python3
"""T-1833: fm playbooks route over a synthetic library: builds one in a temp dir, then reports the index build, one
edit's refresh and the route's wall and CPU p50/p95. Exits 1 when the warm route's CPU p95 passes 50 ms, a refresh
passes 2 s, or fewer than 95% of the planted books are the top hit for their query.

Usage: bench_playbooks.py [--books N] [--runs N] [--json]. Also imported by test_playbook_route (make_library).
"""
import argparse
import json
import os
import random
import statistics
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "lib"))

ROUTE_CPU_P95_MS = 50
REFRESH_S = 2.0
ACCURACY = 0.95
STAGES = 50
_SYL = ["ba", "ko", "ri", "tu", "me", "do", "la", "ni", "so", "ve", "pu", "ga", "he", "zi", "wo", "fa"]


def _word(n):
    """A pronounceable 6-8 letter word from a number: the same n, the same word."""
    out = []
    for _ in range(3 + n % 2):
        out.append(_SYL[n % len(_SYL)])
        n //= len(_SYL)
    return "".join(out)


def _unique(i):
    """The i-th planted word: a q-prefixed base-26 name no vocabulary word starts with."""
    s, n = "", i
    while True:
        s = chr(97 + n % 26) + s
        n //= 26
        if not n:
            break
    return "qx" + s.rjust(3, "a") + "zq"


def make_library(root, books, planted=40, seed=1):
    """references/<stage>/<name>.md x `books` under root, ~600 characters each; `planted` of them carry three words
    nothing else has. Returns {query: path} for the planted ones (the query is a sentence using those words)."""
    rnd = random.Random(seed)
    vocab = [_word(i * 7 + 3) for i in range(4000)]
    pick = lambda k: " ".join(vocab[int(len(vocab) * rnd.random() ** 2)] for _ in range(k))  # skewed: common words recur
    marks = set(rnd.sample(range(books), min(planted, books)))
    asked = {}
    for i in range(books):
        rel = f"references/s{i % STAGES:02d}/book{i:05d}.md"
        title, use, body = pick(3), pick(6), pick(60)
        if i in marks:
            a, b, d = _unique(3 * len(asked)), _unique(3 * len(asked) + 1), _unique(3 * len(asked) + 2)
            title, use, body = f"{title} {a}", f"{use} {b}", f"{body} {d}"
            asked[f"{pick(4)} {a} {b} {d}"] = rel
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\nUse when {use}.\n\n## {pick(2)}\n\n1. {body}\n2. {pick(12)}\n\n## {pick(2)}\n\n{pick(30)}\n")
    return asked


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * q))]


def timed(fn):
    """(wall seconds, cpu seconds, result) of one call."""
    w, c0 = time.perf_counter(), time.process_time()
    got = fn()
    return time.perf_counter() - w, time.process_time() - c0, got


def run(books, runs=30):
    import fmplaybooks as pb
    with tempfile.TemporaryDirectory() as tmp:
        root, state = os.path.join(tmp, "pb"), os.path.join(tmp, "state")
        os.makedirs(state)
        os.environ["FOREMAN_STATE"] = state
        t = time.perf_counter()
        asked = make_library(root, books)
        made = time.perf_counter() - t
        queries = list(asked)
        build = timed(lambda: pb.find(queries[0], 5, root))
        walls, cpus, hits = [], [], 0
        for i in range(runs):
            q = queries[i % len(queries)]
            w, cpu, (mode, got) = timed(lambda: pb.find(q, 5, root))
            walls.append(w)
            cpus.append(cpu)
        for q, want in asked.items():
            hits += bool(pb.find(q, 5, root)[1]) and pb.find(q, 5, root)[1][0]["path"] == want
        victim = os.path.join(root, asked[queries[0]])
        with open(victim, "a", encoding="utf-8") as f:
            f.write("\nedited\n")
        os.utime(victim, ns=(time.time_ns() + 10**9, time.time_ns() + 10**9))
        refresh = timed(lambda: pb.find(queries[0], 5, root))
        mode = build[2][0]
    r = {"books": books, "mode": mode, "library_s": round(made, 2), "build_s": round(build[0], 2),
         "refresh_s": round(refresh[0], 3), "accuracy": round(hits / len(asked), 3),
         "route_wall_ms": {"p50": round(statistics.median(walls) * 1000, 1), "p95": round(pct(walls, 0.95) * 1000, 1)},
         "route_cpu_ms": {"p50": round(statistics.median(cpus) * 1000, 1), "p95": round(pct(cpus, 0.95) * 1000, 1)}}
    r["problems"] = ([f"warm route CPU p95 {r['route_cpu_ms']['p95']} ms over {ROUTE_CPU_P95_MS}"]
                     if r["route_cpu_ms"]["p95"] > ROUTE_CPU_P95_MS else []) \
        + ([f"refresh {r['refresh_s']} s over {REFRESH_S}"] if r["refresh_s"] > REFRESH_S else []) \
        + ([f"planted accuracy {r['accuracy']} under {ACCURACY}"] if r["accuracy"] < ACCURACY else [])
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--books", type=int, default=20000)
    ap.add_argument("--runs", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = run(a.books, a.runs)
    if a.json:
        print(json.dumps(r))
    else:
        print(f"{r['books']} books ({r['mode']}): library {r['library_s']} s, index build {r['build_s']} s, one-edit "
              f"refresh {r['refresh_s']} s, accuracy {r['accuracy']:.0%}")
        for k in ("route_wall_ms", "route_cpu_ms"):
            print(f"  {k[:-3]}: p50 {r[k]['p50']} ms, p95 {r[k]['p95']} ms")
        for x in r["problems"]:
            print(f"✗ {x}")
    return 1 if r["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
