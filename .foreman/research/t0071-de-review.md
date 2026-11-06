## intent: changes needed

- MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?` only restricts the *second* word to that list. For stages whose actual suggested command uses a second word outside it (e.g. "documenting"'s `fm task set … --section …`, `fmcore.py:1347`), the match degrades to just `"fm task"`. `cmd_usage`'s later check `target.lstrip().startswith(pending[sid])` then counts *any* subsequent `fm task …` command (log, block, drop, set, ac…) as "followed", inflating the stat for those stages. Fix: add the missing subcommands (`set`, `log`, `block`, `drop`, `check`) to the allowed second-word set, or match on the literal command fmcore emits.
- Rest of the intent surface (finish→done reuse of `args`, self-audit ordering vs `done_blockers` freshness, cost attribution via `_task_at`) traced through and is correct.

## adversary: changes needed

- MEDIUM — `plugin/lib/fmcore.py:764-770` (`add_audit`) — `how`/`result` are redacted but never passed through `defang()`, unlike `add_evidence` (`fmcore.py:749`), research files, recall labels and tripwires. An adversary-lens audit's whole job is to quote injection payloads found in the repo; that quoted text now lands verbatim, unmarked, in "Verification evidence" for a future session to re-read as if it were data-but-unflagged. Fix: `result = defang(_unmarked(redact(...)))` (and arguably `how`) in `add_audit`, matching `add_evidence`.
- LOW — `plugin/lib/fmrecall.py:816-828` (`private()`) is a regex allowlist/denylist scrubber (urls, emails, paths, filenames, task ids, project name). It won't catch prose that identifies a project another way (client names, internal service names). Since `fm share` explicitly sells this as privacy-preserving, worth a one-line caveat in `fm share`'s help text.
- LOW — `defang()`'s instruction regex (`fmcore.py:300-303`) is trivially rephrased around; expected limitation of a regex heuristic, not a regression.
- Checked and clean: `fm quiet` (shlex.join before `bash -c`), `_notify` ($1 passed as a separate argv element, never shell-interpolated), `--models` (validated, and even an adversarial value is consumed as a single `--model` argv slot, not a new flag), `fm evals add` (folder name sanitized via `kebab`, confined to `p.dir/evals` or operator-given `--out`).

## edge: changes needed

- MEDIUM — `plugin/lib/fmhooks.py:147-157` + `fmcost.py:441-464` — `digest_offered` is only stamped when `weekly_line` returns non-None. A project with no finished work in 7+ days re-runs `_week()` → `load_briefs(p, include_archive=True)` (walks/parses every archived brief) on **every** SessionStart, inside the project lock (`fmhooks.py:141`), unthrottled. Fix: stamp `digest_offered` regardless of whether there was anything to show.
- MEDIUM — `plugin/lib/fmrecall.py:195-196` — thrash hint fires only on `same == REPEATS` (exact 3) over a trailing 200-record window across the whole project; a noisy task with 200+ interleaved failures of other signatures can push the earlier occurrence out of the window so the count never hits exactly 3, and the hint silently never fires. The count is also read after the lock (`fmrecall.py:187-194`) is released, so a concurrent writer could shift it. Fix: use `>=` with a per-task "already hinted" flag.
- LOW — `plugin/lib/fmrecall.py:836-844` — `shared/lessons.jsonl` has no size cap/trim (unlike `failures.jsonl`'s `FAILURES_KEEP`), and is a single cross-project file every opted-in project appends to forever.

## maintainer: changes needed

- MEDIUM — three independent copies of the criterion-verify regex: `fmcli.py:287`, `fmhooks.py:888`, `fmcost.py:185` (plus the writer in `fmcore.py:827`). Fix: one shared helper in fmcore.
- LOW — `cmd_gates`'s `gates()` (`fmcli.py:290-303`) hand-duplicates the requirements already encoded in `Brief.done_blockers`/`REQUIRED_AUDITS`/`plan_gaps` (`fmcore.py:553-557, 794-869`); they will drift.
- LOW — `plugin/lib/fmcore.py:296-297` `task_files()` is now a trivial wrapper with zero remaining callers in `plugin/lib` — dead code, delete it.

## Not checked
Test files (`test_speed.py`, `test_unattended.py`), rounds A–C's own fixes (only re-verified as touched by D/E), `fm serve`/remote wiring beyond `_notify`/`_models`, exact uninstall/state-wipe coverage of the new files (`shared/lessons.jsonl`, `tripwires.json`, `evals/`) — found the wiring-undo path in `fmsetup.py` but not where/if project state itself gets purged, `fmdoctor.py` schema-bump migration path, transcript-scan correctness on malformed/huge real transcripts (code reads look sound but not exercised).
