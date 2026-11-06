## Verdict: changes needed

## Findings

**HIGH — plugin/lib/fmguard.py:188-198 (`_protected_roots`) vs plugin/lib/fmguard.py:165-171 (`_is_core`) — tree-write guard misses project-level `.claude/settings*.json`, only `classify_write` (single-file) catches it**

`_is_core` protects any path matching `re.search(r"/\.claude/settings(\.local)?\.json$", path)` — this fires for a project's `.claude/settings.json` **or** `.claude/settings.local.json` anywhere, not just under `ctx.home`. That's confirmed by the pre-existing test `plugin/tests/test_guard.py:260`: `("{repo}/.claude/settings.local.json", "core")` for a direct write.

`_protected_roots` (used by the new `classify_tree`, added this round to catch checkouts/extractions/recursive copies over a folder that contains a protected path) only adds `(os.path.join(ctx.home, ".claude"), "settings.json")` as a root — hardcoded to `ctx.home`, and only `settings.json`, never `settings.local.json`.

Concrete bypass: from `{repo}`, `cp -r evil/. .claude/` (or `tar -xzf x.tar -C {repo}/.claude`, or `git checkout evil -- .claude/`) rewrites `{repo}/.claude/settings.local.json`. `classify_tree` resolves the target to `{repo}/.claude`, then checks it against `_protected_roots(ctx)`, whose only `.claude` root is `{ctx.home}/.claude/settings.json` — not under `{repo}/.claude` (different directory) — so no category is produced and the tree write is **not** flagged `core`, even though the same single-file write already is (per the test above). None of the new tests (`test_guard.py:580-593`) exercise a project-level `.claude` tree write, so this regression is untested.

Fix: build `_protected_roots` from the same source `_is_core` uses (or have `_is_core` consult `_protected_roots`) instead of maintaining two independently-hand-written lists; at minimum add `(os.path.join(ctx.project_root, ".claude", "settings.json"), "core")`, `...settings.local.json`, and the equivalent under `ctx.home`, when `ctx.project_root` is set.
Confidence: high (verified by direct code/test reading, no execution needed).

**LOW — plugin/lib/fmcore.py:1210-1212 — `plain_lines` docstring says "tabs kept" but tabs are replaced with spaces**

```
def plain_lines(text):
    """plain() for each line of a multi-line text (newlines and tabs kept)."""
    return "\n".join(plain(l.replace("\t", "    ")) for l in (text or "").split("\n"))
```
Tabs are converted to 4 spaces (necessary because `plain()` strips `\t` as Unicode category `Cc`), not "kept" as tabs. The comment reads as literally false to a future maintainer. Fix: reword to e.g. "tabs become spaces so plain() doesn't delete them, newlines are preserved by the per-line split".
Confidence: high.

**Observation — `fmhooks._clean`/`_plain` (plugin/lib/fmhooks.py:79-80, 498) don't duplicate `plain`/`plain_lines`**: `_plain` is just `c.plain` (an alias, not a reimplementation); `_clean` strips ASCII control + `;` with a length cap for building outgoing terminal escape payloads (different job: constructing safe OSC sequences, not sanitizing pulled/typed titles for display) and predates this diff unchanged. No drift introduced by this round; not otherwise verified beyond reading.

**Observation — `task_done_in` (plugin/lib/fmcli.py:239-259)** duplicates the lock/save/log/regen_views shape of `mutate()` (fmcli.py:56-64) but legitimately can't reuse it since it mutates two briefs and logs one combined event; not flagged as unjustified duplication.

## Acceptance criteria
- Round-5 additions (`--from-agent`, `audit prep --note`, `--done-in`, step in progress line, doctor's latest hook error) each have a failing-without-it test and match neighbouring code style: met, verified by reading `plugin/tests/test_cli.py:475-527`, `test_doctor.py:543-555`, `test_visibility.py:118-124` against the implementation.
- `--done-in` cannot close started work without its own gates: met — `task_done_in` (fmcli.py:249-251) blocks unless the *dropped* task's own status is `captured`/`planned` and it has no evidence; verified against `test_cli.py:520-527` (evidence present → exit 2, "started" in stderr).
- Round-4 fixes (tree writes, `core.hooksPath` spellings, fallback repo identity) behave as documented: partially met — the `core.hooksPath`/`direnv`/persistence-path changes are correct and tested; the tree-write coverage has the gap above.
- New CLI options documented consistently: met for `--from-agent`, `--done-in`; `--note`'s repeatability isn't called out in MASTER.md but matches the existing terse style used for `--lens` (also `append`), so consistent with precedent rather than a new inconsistency.

## Not checked
- Did not execute the test suite (read-only review); correctness of test assertions taken on trust where code matches them.
- `fmsync.py` conflict/merge logic beyond the `_from_mirror` sanitization line.
- `fmdoctor.py` beyond `check_hook_errors`.
- Guard behavior for tools other than Bash/Write (Edit, WebFetch, etc.) — out of this diff's scope.
- Performance of `_agent_report` on very large transcripts (no size cap observed, but out of stated focus).
