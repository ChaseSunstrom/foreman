"""failing-frame's checker: every frame names a worktree file and the code on its line, and where is the deepest frame
outside the tests (or the deepest frame when only tests ran)."""
import re
import sys

from cardkit import fail, read_input, source

inp = read_input()
facts, files = inp["facts"], set(inp["files"])
if not isinstance(facts, dict) or not isinstance(facts.get("failed"), bool):
    fail("the result isn't an object with failed true or false")
frames = facts.get("frames") or []
if not facts["failed"]:
    if frames:
        fail("the result says nothing failed but lists frames")
    sys.exit(0)
if not isinstance(frames, list):
    fail("frames isn't a list")
exc = facts.get("exception")
if exc is not None and not (isinstance(exc, str) and re.fullmatch(r"[A-Za-z_][\w.]*", exc)):
    fail(f"exception {exc!r:.80} isn't an exception's name")


def is_test(rel):
    base, parts = rel.rsplit("/", 1)[-1], rel.split("/")[:-1]
    return base.startswith("test") or base.endswith("_test.py") or base == "conftest.py" or "tests" in parts \
        or "test" in parts


for fr in frames + ([facts["where"]] if facts.get("where") else []):
    rel, n, code = (fr.get(k) if isinstance(fr, dict) else None for k in ("file", "line", "code"))
    if rel not in files:
        fail(f"frame {fr!r:.160} names {rel!r}, which isn't a file of the worktree")
    lines = source(rel).splitlines()
    if not isinstance(n, int) or not 1 <= n <= len(lines):
        fail(f"{rel} has no line {n!r} ({len(lines)} lines)")
    if lines[n - 1].strip() != str(code or "").strip():
        fail(f"{rel} line {n} reads {lines[n - 1].strip()[:100]!r}, not {str(code)[:100]!r}")
where = facts.get("where")
if frames:
    if not where:
        fail("the result lists frames but no where")
    code_frames = [f for f in frames if not is_test(f["file"])]
    want = (code_frames or frames)[-1]
    if (where["file"], where["line"]) != (want["file"], want["line"]):
        fail(f"where is {where['file']}:{where['line']}, but the deepest frame "
             f"{'outside the tests' if code_frames else ''} is {want['file']}:{want['line']}")
