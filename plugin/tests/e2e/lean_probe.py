"""T-1354 live probe (costs three short claude calls; not part of run.py): fm code's lean claude launches on this machine.

1. One planner call launched as before T-1354 and one launched lean: both answer, and the lean one reads fewer input
   tokens (both counts printed).
2. A lean worker asked to write note.txt and .env in a scratch repo: note.txt lands (it can work), .env doesn't
   (Foreman's guard, its only hooks, refuses a credentials file).
Exit 0 when both hold."""
import os
import shlex
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "lib"))
import fmcode  # noqa: E402
import fmmodels  # noqa: E402


def run(argv, cwd):
    env = dict(fmcode.worker_env(), FOREMAN_QUIET="1", FOREMAN_WORKER_OF="fm-code-probe")
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
    res = next(filter(None, map(fmmodels.stream_result, reversed(p.stdout.splitlines()))), None) or {}
    u = res.get("usage") or {}
    seen = sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    return res, seen, p


def main():
    claude = fmcode.RUNNERS["claude"]
    ok = True
    with tempfile.TemporaryDirectory() as repo:
        subprocess.run(["git", "init", "-q", repo], check=True)
        ask = "Reply with the word OK and nothing else."
        today = [w.replace("{prompt}", ask) for w in shlex.split(claude["plan"])]
        lean = today + fmcode.lean_args(claude, "plan")
        (r1, before, _), (r2, after, p2) = run(today, repo), run(lean, repo)
        print(f"planner input tokens: as before {before}, lean {after}")
        if not (r1.get("result") and r2.get("result") and 0 < after < before):
            ok = False
            print(f"✗ lean planner: {r2.get('result')!r} {p2.stderr[-300:]}")
        work = fmcode.worker_argv("claude", "Use the Write tool twice: create note.txt containing OK, then create .env "
                                            "containing X=1. Then say what happened.")
        r3, _, p3 = run(work, repo)
        note, env = (os.path.exists(os.path.join(repo, f)) for f in ("note.txt", ".env"))
        print(f"lean worker: note.txt {'written' if note else 'missing'}, .env {'WRITTEN' if env else 'refused'}; "
              f"it said: {(r3.get('result') or p3.stderr)[-300:]!r}")
        ok = ok and note and not env
    print("✓ lean launches hold" if ok else "✗ lean probe failed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
