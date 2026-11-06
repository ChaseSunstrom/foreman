## intent: changes needed

- MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user explicitly asked for faster/fewer-token turns; this round adds two new mandatory stops (a lesson string on every M/L `task done`, and red→green proof or a written waiver on every FIX `task done`). Each is a small tax, but it's real friction added in the same round that claims speed gains, and it's easy to satisfy with boilerplate ("none: fixture") rather than substance — worth calling out explicitly rather than folding silently into "leaner and cheaper."
- LOW — `plugin/lib/fmideas.py:17` — default brainstorm lenses cut from 6 to 4, dropping `performance` and `security and safety` unless asked. Faster, but a quiet reduction in default diligence exactly where "wayyy smarter" might most want it; docs do say to add them back when relevant (`plugin/skills/brainstorm/SKILL.md:13`), so this is disclosed, not hidden.
- Otherwise the round genuinely targets both stated goals: `fm check` caching/`--affected` (fmcli.py:203-238), the review brief written once to a file instead of printed per-lens (fmcli.py:891-909), and the UserPromptSubmit dedup (fmhooks.py:333-360) are real, verifiable token/latency wins.

## adversary: changes needed

- MEDIUM — `plugin/lib/fmcli.py:163-172` — a failing gate is rerun once; if it passes it's unconditionally labelled "flaky" and the run reports exit 0. A genuinely intermittent (racy) bug is indistinguishable from environmental flakiness here, so a real, reproducible-50%-of-the-time regression can pass `fm check --evidence` on the lucky rerun with no cap on how often a gate may be "flaky." Fix: track flaky-count per gate over recent runs and stop treating repeat offenders as flaky-pass.
- LOW — `plugin/lib/fmcore.py:850-861` (`red_green`) — proof only requires the *same command string* to have failed then passed; the shipped test (`plugin/tests/test_recall.py:1508-1515`, `test -e {flag}`) demonstrates it's satisfiable with a synthetic probe unrelated to the actual fix. The gate can't tell a real regression test from a placeholder.
- The `_cached_pass` reuse (fmcli.py:203-214) correctly keys off `worktree_id` + exact gate list and only looks at the *immediately preceding* run, so a changed tree or changed gate list does invalidate it — no forgery found there.

## edge: changes needed

- HIGH — `plugin/lib/fmmap.py:49-54` — `open(os.path.join(root, "Makefile")).read()` has no encoding/errors handling, and the `try/except OSError` doesn't catch `UnicodeDecodeError` (a `ValueError` subclass). A non-UTF-8 Makefile (common: a stray Latin-1 author name in a comment) makes `fm map`/`fm focus` raise uncaught, and since `fmcli.py:435-437`'s `fmmap.load(p)` call inside `cmd_focus` has no try/except, `fm focus` on *any* scoped task in such a repo crashes outright. Fix: `except (OSError, UnicodeDecodeError):` and open with `errors="replace"` (as `fmmap._git` already does at fmmap.py:9-13, and as `_gates`'s own `package.json` handler does via its broader `ValueError` catch at fmmap.py:39-44).
- MEDIUM — `plugin/lib/fmrecall.py:136-146` (`note_failure`) — the 1 MB trim (`tail_jsonl` + `write_atomic`) races with concurrent `PostToolUseFailure` hooks from parallel sessions/subagents with no `c.lock`, unlike `_auto_evidence` which does lock (`plugin/lib/fmhooks.py:308`). A concurrent appender opened before the trim's rename can silently lose its record to the orphaned inode. Fix: wrap the whole read-trim-write-append in `c.lock(p.dir, timeout=LOCK_QUICK)`.
- MEDIUM — `plugin/lib/fmmap.py:60-61` (`build`) and `plugin/lib/fmcli.py:222-225` (`_check_affected`) — git filenames are split with plain `.split()`; a path containing a space (git renders as a quoted/escaped token without `-z`) is mis-tokenized into bogus entries, silently corrupting the layout/hot-file/test-link data and `--affected`'s changed-file set (no injection risk since `shlex.quote` is applied downstream, but selection is wrong). Fix: use `git ... -z` and split on `\0`.

## operator: ok

New state (`map.json`, `failures.jsonl`) stays under the project dir and is outside `fmsync`'s mirror whitelist (`plugin/lib/fmsync.py:71`, briefs/research/decisions.md only), so it won't leak into the shared repo. `sessions/*.note` files fall under the existing generic old-snapshot sweep in `fmtidy.py:282-292`. Docs (CHANGELOG, MASTER.md, rules, audit.md) were updated consistently with the code in this diff.

## maintainer: changes needed

- MEDIUM — `plugin/lib/fmmap.py:9-16` duplicates `fmcore._git` (`plugin/lib/fmcore.py:1498-1504`) with different timeout/env/error handling instead of extending the existing helper — exactly the "two git helpers" drift risk the review brief calls out. Fix: add optional `timeout`/`env` params to `fmcore._git` and delete the copy.
- LOW — `fmmap._stem` (path stemming) and `fmrecall._stem` (word stemming) share a name for unrelated logic in sibling modules; confusing for future readers, not a bug. Rename one.

## Not checked

fmserve.py/fmrun changes (test-file-only diffs), fmguard.py's `fetch --update-head-ok` logic beyond the shown test table, the BM25 scoring math's correctness in detail, fmideas.py subagent sandboxing, and any C++/Rust/TS code (none present — Python-only diff).
