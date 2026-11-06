## intent: changes needed

**MEDIUM** — `plugin/lib/fmloop.py:14,36` — "past every earlier ideas.md" is only the newest 6.
- file: plugin/lib/fmloop.py; line: 36; short_summary: Only newest 6 earlier brainstorms passed as --seen
- summary: `seen()` returns `files[-SEEN_MAX:]`, but the request, README, the rules line and the docstring all say "every earlier".
- failure_scenario: With 7 or more earlier runs, round 1 re-proposes ideas from the oldest runs. Those get grounded and queued, which inflates the yield and delays the dry stop.
- category: spec-mismatch; verdict: CONFIRMED
- fix: Pass all of them and let `fm ideas` cap the titles, or reword the docs to "the newest 6".

**MEDIUM** — `plugin/lib/fmloop.py:84` and `plugin/lib/fmhooks.py:2447` — the dry stop depends on the model remembering `fm loop yield`.
- summary: `round_brief` sets `yielded=None` but nothing reads it.
- failure_scenario: The model runs `fm loop round`, queues nothing and skips `yield`. The next Stop sees a changed key `[round, len(briefs)]` and pushes the next round. There is no dry count, and only `DRIVE_MAX` or `_pace()` ends it.
- failure_scenario: `fm loop yield 0` run twice for the same round stops the loop after one round.
- category: unenforced-invariant; verdict: CONFIRMED
- fix: In `round_brief`, if `round > 0` and `yielded is None`, call `record_yield(p, 0)` first. Make `yield` refuse when `yielded` is already set.

**LOW** — Docs say "the budget ... end it" (README, CHANGELOG), but the code only pauses. `_pace()` returns None in `fmhooks.py:2447`, the loop stays on, and the next session resumes. Reword the docs.

## adversary: ok
No new trust boundary. Task titles in the brief are the user's own data.

## edge: changes needed

**MEDIUM** — `plugin/lib/fmloop.py:47` — raw `subprocess.run(["git", ...], timeout=20)` with no handling.
- summary: `fmcore._git(..., proc=True)` already exists at `fmcore.py:2754` and handles timeouts and a missing git. This call duplicates it.
- failure_scenario: With git missing, `FileNotFoundError` escapes and `fm loop round` tracebacks. A slow repo gives an uncaught `TimeoutExpired`. `GIT_DIR` in the environment points git at another repo.
- category: unhandled-error; verdict: CONFIRMED
- fix: `c._git(p.root, "log", "--oneline", f"--since={since}", "-n", "40", timeout=20)`.

**MEDIUM** — `plugin/lib/fmhooks.py:2445,2449` — each loop push counts toward `DRIVE_MAX` (50), shared with ordinary drive pushes.
- failure_scenario: One round that queues about 20 tasks plus its build pushes can exhaust the cap. The loop then stalls silently while `fm next` still says "round N". "Stops only on dry/budget/user" is not what happens.
- category: silent-stall; verdict: PLAUSIBLE
- fix: Say so in the README, or emit an event or a notice when the cap ends a loop.

**LOW** — `fmloop.py:43` — a brief whose `updated` is unparseable counts as shipped every round.

**LOW** — `fmloop.py:61` — `--seen` paths are not quoted, so a state dir containing spaces breaks the command line.

## operator: ok
- MASTER.md, README, CHANGELOG and the rules line match the code.
- The rules file grows by one clause on an existing line, so the line count is unchanged.
- `plugin/evals/guard-force-push/prompt.md` needs no edit, because this change touches no guard text.

## maintainer: changes needed

**MEDIUM** — `plugin/tests/test_loop.py` — no test for any of these:
- the `yield` before `round` path
- git failure
- `_pace()` or `DRIVE_MAX` suppressing the push
- `--seen` being capped
- a missing or double `yield`

The drive test covers full autonomy only.

## Acceptance criteria
- `fm next` names the round and the drive continues into it: **met**. `fmcore.py:2503` and `fmhooks.py:2444` implement it, and `test_the_drive_continues_into_each_round` covers it.
- `fm loop yield` counts dry rounds and two in a row stop the loop with a recorded decision: **met**, with the gaps in the yield-enforcement finding above.
- `fm ui` and the pane show the loop: **met**. `fmwatch.py` provides the view, and the band and pane in `register.tsx` render `∞ round N`.
- `python3 plugin/tests/run.py test_loop` passes: **not verifiable**, because this review is read-only.

## Not checked
I did not run the tests. I did not read `fm ideas` or `fm mission` internals. I only skimmed the `register.tsx` layout. I did not review the demo binaries.

**Noticed:**
- The diff base (33137fa) predates commit 61b1bde, so `demo/live.*` and `CHANGELOG` from T-1035 show up as part of T-1057. Re-base the audit diff.
- `fmhooks.py:2455` has a `d.get("drained") == len(briefs)` pattern that the new loop key `[round, len(briefs)]` copies. Both treat a changed brief count as progress, which is fragile.
