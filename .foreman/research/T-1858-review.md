**Verdict:** approve with nits. The security guards hold. I found no HIGH or MEDIUM defects in the code, and two things are worth a decision.

The pre-audit "secret-looking value" hits are false positives. At `fmeco.py:437` the match is `accesskey="[REDACTED]"`, and at `fmeco.py:471` and `test_inbox_more.py:136` it is `fmsettingsserve.make(...)`. The large-file and hotspot flags are only size. The diff shows `[REDACTED]` in those places, but the working tree has the real code. I did not run the tests.

## lens: intent
- MEDIUM — `plugin/lib/fmeco.py:459-472` — The request says "through fm serve". `fm serve` is the Remote Control systemd unit (`fmcli.py:6916`). The change instead reuses `fm settings serve`'s loopback server and adds `inbox swipe --serve`. This reading is sensible, and the AC "settings serve unchanged" bakes it in. But no step or log records the choice, and a user who wanted the page reachable through Remote Control, such as from a phone, gets loopback only. — Fix: log the interpretation in the task or CHANGELOG, or confirm it with the user. — confidence 55%

## lens: adversary: ok
The guards are inherited and cover the new page. They are the one-use token, the cookie with SameSite=Strict, the Host and Origin checks, `Content-Length` handling, a duplicate-field refusal, and a CSP with no script. All page text goes through `html.escape`.
- The id must match `fullmatch(r"T-\d+")` (`fmeco.py:104`), so a batched value like `T-1,T-2` or an id with a newline is refused.
- A Unicode-digit id passes the regex but fails `by_id.get`, and the resulting `UsageError` comes back as a 422.

## lens: edge
- LOW — `plugin/lib/fmeco.py:598` — `fm inbox swipe --serve --json` ignores `--json` without saying so, against T-1855's "no flag silently unread" rule, which the diff itself extends at line 586. — Fix: refuse `--json` with `--serve`. — confidence 70%
- LOW — `plugin/lib/fmsettingsserve.py:280` — Each answer is a POST that renders the page directly. A browser reload re-posts it. After a drop or revive that shows a red 422 "not deferred" banner, and after a keep it appends a second "swept: kept" log line. — Fix: answer with a 303 to `/`, or accept this and document it. — confidence 75%

## lens: operator: ok
CHANGELOG, MASTER.md and `backlog.md` all name the feature. Cost is nil: the server is idle-bound at 30 minutes, makes no calls, and loads the pile only per request.

## lens: maintainer
- LOW — `plugin/lib/fmeco.py:412` — `SWIPE_VERDICTS` repeats `SWIPE_KEYS` (line 379) and the literal tuple in `swipe_apply` (line 346). `accesskey=[REDACTED] also silently relies on the first letters being unique. — Fix: derive `SWIPE_VERDICTS` from `SWIPE_KEYS` plus "skip". — confidence 70%
- LOW — `plugin/tests/test_inbox_more.py:134-143` — No test posts "revive" through the page, though it is one of the four buttons. The only conflict case tested is a double drop. — Fix: add `swipe("T-0001","revive")` and assert `captured`. — confidence 80%
- LOW — `plugin/tests/test_inbox_more.py:194` — `fmsettingsserve.serve` is mocked, so the server `run` was handed is never closed. The loopback socket stays bound until garbage collection. — Fix: close `served.call_args.args[0]` after the call. — confidence 70%

## Acceptance criteria
- Criterion 1, a card at a time, each answer applied at once, titles escaped, forged or batched posts refused: met, going by the code and test assertions (`test_inbox_more.py:152-181`). I did not run the tests.
- Criterion 2, settings serve unchanged and `--serve` with swipe alone: met by the code. The Handler defaults reproduce the old paths and messages, and `inbox first --serve` and `--serve --apply` both exit 1.

## Implicit decisions
- Reuses `fmsettingsserve.Handler` through the new `CMD`, `PATHS`, `draw` and `act` hooks, rather than `fm serve`.
- "Skip" and "keep" are tracked in a per-server set, so skipped items come back on the next run.
- A verdict of "skip" on an unknown id is accepted without any check.
- Post-and-render, with no post-redirect-get.
- The label is "Foreman backlog".

## Not checked
- I did not run the tests, and I looked at no browser rendering.
- Files vs steps: the work in `fmcli.py`, `fmeco.py` and the tests is named by no plan step. The plan only lists steps 2 and 3, so it is missing a step.

**Noticed:** `plugin/lib/fmsettingsserve.py:324` prints "Ctrl-C stops it, so do 30 idle minutes", which is garbled wording from the original and now shared by both pages.

Files: `~/.claude/foreman/plugin/lib/fmeco.py`, `~/.claude/foreman/plugin/lib/fmsettingsserve.py`, `~/.claude/foreman/plugin/tests/test_inbox_more.py`
