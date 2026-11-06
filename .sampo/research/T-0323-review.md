## Verdict
Changes needed. No path-traversal hole found. Stop, hand-off and the message path have real defects.

## Findings

**MEDIUM — `plugin/lib/fmcli.py:2572` with `plugin/lib/fmsession.py:522,526`: message words are parsed as CLI options.**
- `rest` is `nargs="*"`, so argparse still takes options from inside the message.
- `fm session send ID fix the --follow flag` sets `follow=True` and drops "--follow" from the text. It also swallows `--arg`, `--model` and `--cwd` followed by a value.
- A message that starts with `-`, such as `-1`, errors outright. Abbreviations like `--mod` are accepted too.
- Fix: read the message from stdin or a `--message` option, or document `--`. Tests only use plain text.

**MEDIUM — `fmsession.py:324-337`, and `:329` only catches `ValueError`.**
- A parsed line with an unexpected shape raises `AttributeError`.
  - Example: `{"type":"turn.failed","error":"boom"}` makes `_codex` call `.get` on a str at :157.
  - Example: `{"type":"error","error":"x"}` does the same in `_opencode` at :238.
  - Example: `{"type":"assistant","message":"x"}` does the same in `_claude`.
- The exception kills the runner without killing the agent child, which is still running and writing to a pipe nobody reads.
- `meta` stays `running`, and `_status` later reports `died`. There is no result event, and the pending queue is stranded until the next send.
- Fix: `except Exception` around `normalise`, emitting raw, and a `try/finally` that kills `proc` around the read loop.

**MEDIUM — `fmsession.py:354-368` and `:410-412`: stop can kill the wrong group where `/proc` is absent.**
- Without `/proc`, `_alive` returns True for any live pid.
- `pid` is never cleared when the runner goes idle (:301 sets only `status`).
- On macOS, `fm session stop ID` on an idle session sends `killpg` to whatever now owns the stale pid if it leads a group. `remove` at :462 would spuriously refuse as well.
- Fix: set `pid=None` on the idle transition at :301. Optionally compare process start time or `ps -o command` on non-Linux.

**MEDIUM — `fmsession.py:395-398` and `:54-58`: unlocked read-modify-write of `meta.json` can lose `agent_session`.**
- `send` runs `_set(status="starting")` while the old runner is exiting or the new runner is in `_turn`.
- Interleaving: `send` reads meta, the runner writes `agent_session` at :334, `send` writes back the stale copy.
- The next turn then has `resume=None` and starts a fresh agent conversation without warning.
- Fix: lock `meta.json` writes with the same flock approach, or have `send` not write meta at all (the runner sets status).

**LOW — `fmsession.py:404-421`: a `stop` right after `start` or `send` is ineffective.**
- If the runner has not set `pid` yet, or the old pid is stale, `_alive` is False and nothing is killed.
- `stop` returns "stopped". The runner may already have taken the message at :299 and then runs the turn, setting `running` over `stopped`.
- Fix: have `stop` write a `stop` marker file that `run()` and `_turn` check, or hold `run.lock` while stopping.

**LOW — `fmsession.py:28`: `$` also matches before a trailing newline.** `"20260101-000000-abcd\n"` passes `_ID`. It stays inside the `agent-sessions` folder and then fails to find a session. Use `fullmatch`.

**LOW — `fmsession.py:487-496`: `tail --follow` on a removed session.** The `a+` open is not covered by an `except OSError`, so a concurrent `rm` gives a traceback. The loop also never exits once the turn has ended, which is by design.

**LOW — `fmsession.py:314,288` and `fmsession.py:316`: encoding.**
- The `raw.log` open and the `Popen` do not set `encoding="utf-8"`. Under a non-UTF-8 locale, the `log.write` at :325 can raise `UnicodeEncodeError` and kill the runner as in the second finding.
- A resume id starting with `-` becomes an option for codex, because it is a positional at :76. Python's UTF-8 coercion makes the encoding case rare.

## Acceptance criteria
- **Detached start, normalised events, resume on send (stub claude):** met by `test_a_session_runs_detached_and_resumes_on_send`. I did not run it.
- **codex, gemini and opencode normalise to the same schema:** met by the three agent tests, on well-formed lines only.
- **Stop kills the process group and list reconciles dead pids:** met on Linux by `test_stop_ends_the_whole_process_group` and `test_a_dead_runner_reads_as_died`. The non-`/proc` path is untested.

## Not checked
I did not run the tests. I did not review the rest of the diff (`CHANGELOG.md`, `MASTER.md`) or the operator and maintainer lenses. I did not test the lock race empirically. Reading the code, the `run()` hand-off at :298-305 looks correct.
