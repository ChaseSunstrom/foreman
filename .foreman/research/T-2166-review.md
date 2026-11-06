## Verdict
Changes needed. `put` is gated correctly, but the lock handling breaks concurrent `select` and `seed`. The request's writer list and the live-file sweep (AC3) are also unfinished.

## lens: intent
- MEDIUM — `plugin/lib/fmgenesis.py:80, 1065, 1459, 1555` — The request names the tower's own writers "exam_line, drift, sweep, seed". Only `put` reads, and `spec`, `select` and `seed` get the read because they call `put`. `exam_line`, `drift` and `sweep` write through `_file` or directly and are never read. The CHANGELOG lists only `spec`, `select` and `seed`, so the omission isn't flagged as a decision. — Say so in the CHANGELOG and the task log. Or read `drift.md` and `sweep.md` before `_file`, if the user meant them. — high
- MEDIUM — `plugin/lib/fmgenesis.py:80-81` — AC3 asks for every live tower file to be put through the read again and verified by `fm genesis check`. No code in the diff does this. `check` doesn't consult `genesis_read` events. A file written before this change, or edited on disk, still counts. The request's "held as pending, step/check/select ignore it" is replaced by refusing at the door. — Do the sweep and record the evidence. Say that refusal replaces the pending state. Or have `check` flag files with no `pass` event newer than their mtime. — medium

## lens: edge
- MEDIUM — `plugin/lib/fmgenesis.py:1155-1156, 1205, 1217-1218, 1287` — `select` and `seed` hold the `genesis-lineage` lock (`c.lock`, 5 s timeout, `fmcore.py:949`) around `put`. `put` now runs a subprocess read of up to 120 s inside that lock. A second `fm genesis select 2` or `seed 2` from another session waits 5 s, then raises `LockTimeout`. That is a plain `Exception` (`fmcore.py:94`), and `cmd_genesis` catches only `OSError` and `ValueError` (`:1653`), so the user gets a traceback. Before this change the lock was held for milliseconds. — Read before taking the lock, for example by splitting `put` into `_read` plus `_file` and calling `_read` ahead of the lock. Or catch `LockTimeout` in `cmd_genesis`. — high
- MEDIUM — `plugin/lib/fmgenesis.py:931, 942, 1205` — `spec()` runs `fmexam.gen` and creates the exam run before `put("spec.md")`. A refused read leaves an orphan run, and every retry makes another with a new id. For `select`, a refused read means the computed verdict (even a `revert`) is never recorded. The writers have no way to revise the generated text, so they can only retry a nondeterministic reader. — Read the generated text before the side effects, or treat a `FAIL` on generated docs as advisory. Say which in the CHANGELOG. — medium

## lens: maintainer
- LOW — `plugin/tests/test_genesis.py:1272-1340` — The CHANGELOG claims `spec`, `select` and `seed` go through the read. Every new test puts `coverage.md`, so removing `_read` from those paths would pass. — Add one test where the reader FAILs a seed or `select` and nothing is written. — high
- LOW — `plugin/tests/test_statusline_ui.py:374` — Two comments sit on one line, and the older one is now misplaced after the new one. — Move the T-2166 comment above the call. — high
- LOW — `plugin/lib/fmgenesis.py:1447` — `stray = [h for h, _ in named if not h]` builds a list of empty lists, and only `len(stray)` is used. — `stray = sum(not h for h, _ in named)`, as `_read` does at `:1119`. — high

## lens: adversary
- LOW — `plugin/lib/fmgenesis.py:70-71` — The steers fed to the reader come from `fm decide --cites "user steer…"`, which the policed session writes. The match is now case-insensitive and also takes "the user's steer", so a forged "steer" can tell the reader to pass things. This is the same trust level as T-2114 and `_fence` blocks fence closing, but the reader remains advisory. — Mention it in the docs. — low

## Acceptance criteria
- AC1 (cold Haiku read of redacted file with charter, steers and exam; write only on plain CLEAN): met. `_read` (`:102-130`) and `test_a_clean_read_files_it…`. I did not run the tests.
- AC2 (a FAIL naming a held line refuses with that line and why; a stray quote, no verdict or a read that didn't run also refuses): met. The code at `:113-130` and `test_a_fail_naming…` and `test_no_read_is_no_pass` cover it.
- AC3 (every live file re-put through the read and verified with `fm genesis check`): not met. Nothing in the diff does it, and `check` has no read check.

Pre-audit: the "secret-looking" hit is `password: [REDACTED] at `test_genesis.py:1298`, a fixture marked `# pragma: allowlist secret`. The audit diff had redacted it. `test_exam.py` and `test_statusline_ui.py` needed these edits and no more. I did not look at the CHANGELOG and MASTER hotspots beyond the diff.

## Implicit decisions
- Fail closed: no gen-0, an exhausted budget, no `claude` on PATH, or a timeout all refuse the put.
- A hand-written `put` now needs `fm genesis init` first.
- Haiku with a 120 s timeout and a budget fallback of $0.05 per read.
- Only the newest 20 exam lines per run and agent go to the reader.
- Refusal replaces "held as pending", and the older file stays on disk.
- `CLEAN` is accepted when it starts any line, matched case-sensitively.

## Not checked
I ran no tests. I did not measure prompt size for a large `coverage.md` against Haiku's context, which could make a big file refuse forever. I did not check `MASTER.md`'s one-line change (it was left out of the diff) or the `fm genesis check` implementation beyond grep.

**Noticed:** `drift` and the new `_read` both use `^[\s*]*CLEAN\b` (so "CLEAN" at the start of any line passes). It could be a shared constant with a test for "CLEANUP needed" or "Not CLEAN".
