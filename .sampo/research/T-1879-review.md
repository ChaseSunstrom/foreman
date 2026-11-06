**Verdict:** changes needed (two small gaps against the acceptance criterion). I read the diff and the surrounding code but did not run `plugin/tests/run.py test_robustness`.

## lens: intent
- MEDIUM — plugin/lib/fmcli.py:851-852 — A repeated `fm task defer|block T --reason R --until D` is not a no-op. `change()` logs `"deferred: R (revisit D)"` (fmcli.py:826), but the guard tests `last.endswith(" deferred: R")`, which fails on the `(revisit D)` suffix. The second run appends another log line, so the "run twice is a no-op" criterion is only met without `--until` — fix: build the expected log text exactly as `change()` does, including the revisit suffix, and compare the whole last line's tail; add a test with `--until` — confidence high (read from code).
- MEDIUM — plugin/tests/test_robustness.py:95-126 — The request and criterion say "malformed brief **or meta**" (truncated frontmatter, binary bytes). The test only corrupts briefs and never touches `meta.json`. `read_meta` (fmcore.py:739) raises `CorruptState` on bad JSON, and I did not check that every verb in `READ_VERBS` turns that into a message instead of a traceback. The hooks list also omits PreToolUse and Stop, which read briefs on every tool call. Fix: add a case that writes truncated and binary `meta.json`, and run the PreToolUse and Stop hooks — confidence medium (a coverage gap, not a proven crash).

## lens: adversary: ok
The `sha1` in the test (test_robustness.py:53) only fingerprints files for comparison and is not a security use. `redact(reason)` in the guard matches what `append_log` writes (fmcore.py:1315), so no secret leaks through the comparison. I found no new untrusted-input sink.

## lens: edge
- LOW — plugin/lib/fmcore.py:3393-3403 — A skipped rewrite leaves STATE.md's `_Generated <ts>` at the time of the last content change. A reader judging freshness from that line will think the view is stale. `fmdoctor.py:341` already strips this line when comparing, so no code depends on it. Fix: reword the line to "Updated" or note it in the CHANGELOG — confidence medium.
- Concurrency is fine. The no-op check reads outside the lock, but `mutate` re-reads inside it. A missing or unreadable view file falls through to `write_atomic`, so views self-heal.

## lens: operator: ok
`put()` reads six small files per `regen_views`, which saves an fsync and a rename each, so the cost is small. The `fmtidy` reorder takes the lock twice in sequence, not nested.

## lens: maintainer
- LOW — plugin/tests/test_robustness.py:143-147 — The verbs run with `check=False`. For `drive off`, `sensitive on`, `tidy --apply` and `checkpoint`, a first run that fails the same way both times still leaves the snapshots equal, so the test passes. Only `drop` and `defer` are confirmed later by their "already …" asserts. Fix: assert exit 0 on the first run of each — confidence medium.
- LOW — plugin/tests/test_robustness.py:155 — `open(...)` has no `encoding=`, which breaks the python checklist's explicit-encoding item. Fix: add `encoding="utf-8"`.
- LOW — The `fmcli.py`, `fmcore.py` and `fmtidy.py` hunks, and the new test file, are named by no plan step (only CHANGELOG is, step 3). They are in scope for the CLEAN task, so the plan's steps need updating, not the code.
- `plugin/tests/test_tidy.py` needs no edit. Its only `last_tidy` assertion (line 121) is order-independent.

## Acceptance criteria
- "no read verb tracebacks on a malformed brief or meta": **partly met.** Briefs are covered, meta is not, and I did not run the test.
- "mutating verbs run twice leave state unchanged": **partly met.** It holds for the verbs tested, but not `defer` or `block` with `--reason` plus `--until`.

## Implicit decisions
- A repeat is detected by comparing status, revisit and the last log line, not by a stored flag.
- A no-op exits 0 with "is already X" and writes no log or event.
- A view counts as unchanged when only the line-2 `_Generated` stamp differs.
- The test excludes the logs directory and the `last_tidy` stamp from its snapshot.
- `fm tidy --apply` records `last_tidy` before regenerating views.

## Not checked
Whether the other `READ_VERBS` handle a corrupt `meta.json` cleanly, the PreToolUse and Stop hooks against bad briefs, and `fmsync.export` behaviour.

**Noticed:** `read_meta` (plugin/lib/fmcore.py:741) opens `meta.json` without `encoding=`, so it depends on the locale.
