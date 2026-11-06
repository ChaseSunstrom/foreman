## Verdict: changes needed

## Findings

**HIGH — ADVERSARY — `plugin/lib/fmserve.py:304,315`** — The usage-limit check runs `USAGE_LIMIT.search(output)` where `output = r.stdout + r.stderr` (line 304). The code's own comment (line 27) says Claude Code prints these messages "on stderr," but the match is against stdout+stderr combined. Stdout in `claude -p` mode is the model's own generated text/tool output, which is attacker/task-influenceable. A task whose model output or an echoed tool error happens to contain one of the broad phrases (e.g. "out of usage," "You've reached your…" — plausible if the task discusses APIs, quotas, or even this very source file) combined with *any* unrelated nonzero exit (a real crash, a script bug) will be misclassified as a usage limit. `fm run` then silently waits up to the full `--wait` budget (6 h default) and finally reports "usage limit still in effect" instead of the real failure — masking a genuine crash for hours. Fix: match only against `r.stderr`, and ideally anchor to the start of stripped stderr rather than `.search` anywhere in it, e.g. `USAGE_LIMIT.search(r.stderr)` or check the last non-empty line. No test currently covers a non-usage-limit crash whose text happens to contain the phrase — add one. Confidence: high (verified by direct read).

**MEDIUM — EDGE — `plugin/lib/fmserve.py:293,316-319` / `plugin/lib/fmcli.py:56`** — `--wait` is `type=float` with no validation. `fm run --wait nan` gives `budget = nan`. `budget <= 0` is always `False` for NaN, so the stop condition at line 316 never fires; `min(step, budget)` always returns `step` (NaN comparisons are false), so `budget -= pause` stays NaN forever. The run retries indefinitely (up to 1 h sleep per cycle, uncapped total), burning sessions forever with no way to stop except killing the process. Fix: validate `args.wait` (`if not math.isfinite(args.wait) or args.wait < 0: raise UsageError(...)`) in `cmd_run` before computing `budget`. Confidence: high (traced Python's NaN/min semantics manually).

**LOW — EDGE — `plugin/lib/fmserve.py:320`** — The printed/logged "retrying at HH:MM" uses `time.localtime()`; a timezone or clock change during the wait makes the displayed time wrong. Cosmetic only, actual sleep duration is unaffected. No fix needed unless log accuracy matters.

## Acceptance not otherwise scored — this is a two-lens audit, not a full review

## Not checked
- Doc-only changes (CHANGELOG.md, MASTER.md, README.md).
- `run.lock`/two-`fm run` interaction and SIGTERM/Ctrl-C behavior during sleep — traced only (lock is held by the open fd through the sleep; process exit releases it; no signal handler, so an interrupt propagates as before) — not executed.
- Suspend/resume timing effects on `time.sleep` — not empirically tested.
- Pre-existing `_next_runnable`, `waits_on_user`, session/no-progress logic — unchanged by this diff, not re-audited.
- Systemd/`fm serve` code paths — untouched by this diff.
