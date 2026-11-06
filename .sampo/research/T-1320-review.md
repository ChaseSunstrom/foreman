## Verdict
Changes needed. Resume breaks for CLI-planned runs, and the planner's read-only mode is trusted with no check afterwards.

## lens: adversary
- MEDIUM — plugin/lib/fmmodels.py:489 (profile built at plugin/lib/fmcode.py:1036) — The planner CLI runs with the user's real HOME and sign-in, and nothing checks the tree afterwards. `work()` takes `_snapshot` and runs `judge`; `_cli` does neither. Claude's allow rules in `~/.claude/settings.json` (for example `Bash(*)` or `Edit`) may still apply under `--permission-mode plan`, so planning could edit files that nobody judges. I did not run this, so it is PLAUSIBLE. Fix: take `_snapshot(run.root)` before the planner call and run `judge` after it, or at least fail if `_dirty` changed. Add `--disallowedTools Bash Edit Write NotebookEdit` for claude. — PLAUSIBLE
- LOW — plugin/lib/fmcode.py:1115 (via `emit`, :245-247) — The answer text is printed and written to the `--json` stream raw. A repo file carrying a prompt injection can make the planner answer with `\x1b]52;…` or `\x1b[2J`, which reaches the terminal. The TUI is safe (`isprintable` at fmcodetui.py:294). Fix: strip control characters from `text` and pass it through `run.redact` before emitting. — CONFIRMED by code path
- LOW — plugin/lib/fmmodels.py:489-491 — `start_new_session=True` is set, but on timeout `subprocess.run` kills only the child. The CLI's own children keep running as orphans and can still be editing. `work()` uses `run_bounded(reap=True)` with `killpg` instead. Fix: reuse `run_bounded`, or use Popen with `os.killpg`.
- Checked and sound:
  - The prompt is one argv element and starts with "SYSTEM:", so it cannot be read as a flag.
  - `act()` is the only dispatcher, and the `read_only` gate at fmcode.py:347 covers every action name, including unknown ones.
  - The filtered tool list at :472 is only a hint.

## lens: edge
- MEDIUM — plugin/lib/fmcode.py:1029-1032, :1279 — `--resume` of a run planned by the CLI fails. The journal's start record stores model="claude (plan, read-only)", so `m.resolve` raises "no model profile named …" (fmmodels.py:184). The error carries no hint because `run.model_name` is set. README line 307 promises a killed run carries on. Reproducer: `fm code "<req>" --worker claude` with no model, kill it mid-step, then `fm code --resume`. Fix: factor a `_planner_profile(run)` helper and use it when the saved name matches or `run.worker in PLANNERS`. — CONFIRMED
- LOW — plugin/lib/fmcode.py:160-161, :1089, :1050 — A reply with both `answer` and a valid full plan passes `check_plan` as a plan. It is then treated as a question because only `"answer" in run.plan` is tested, so the plan is dropped and no work runs. Fix: use one predicate, `"answer" in v and "type" not in v`, in all three places.
- LOW — plugin/lib/fmcli.py:1359 — A new, untracked file that matches `ARTEFACT` is dropped from the commit with no message, for example a deliberate `tests/fixtures/x.pyc` or `vendor/node_modules/…`. The task is still marked done. Fix: print "left out N build artefact(s): …".
- Not a problem: a tracked artefact is kept (`f in known`). Non-JSON output falls back to raw text. A CLI that exits 0 with `is_error` raises. An empty repo gives an empty `head`.

## lens: operator
- Both messages are clear: no model gives `NO_MODEL_HINT`, and an unknown or custom `--worker` names `--verify`, `claude`, `codex` and `gemini`.
- The README resume claim is wrong for the CLI-planned path (see the edge lens).

## lens: maintainer
- LOW — plugin/tests/test_code_worker.py:624 — Only the success path of `_cli` is tested. Nothing covers non-zero exit, `is_error`, non-JSON output, timeout, the CLI planner returning an `answer`, or resume.
- LOW — plugin/tests/test_code.py:569 — No test for `answer` plus `type` in one reply.

## lens: intent
- LOW — site/build.py:749 — The acceptance criterion says "a recording replayed from its own events". The card shows a static SVG of the last screen plus a replay command, not a replay.
- LOW — site/build.py:733 — The command is built as `fm code "{request}"` with no shell quoting. A request containing `"` shows a command that does not run.

## Acceptance criteria
- Gallery of at least six runs: met on the code side (seven examples, `test_docs` asserts at least six). The recording part is not met, see intent.
- Each kind runs end to end, with a fake-model test for each kind the probe found failing: partly met. Tests cover the question, unrunnable-check, artefact and no-model-planner cases. The CLI failure paths are not covered.
- README "What you can ask": met (README.md:296).

## Implicit decisions
- The CLI planner gets the full `worker_env()`, including model keys.
- The claude planner prompt is flattened to a single user message.
- The CLI profile's context is fixed at 200000.
- The planner timeout equals the worker timeout.
- Any `ModelError`, not only "no model", falls back to the CLI planner.

## Not checked
- I ran no tests. I did not run `claude` or `gemini` to see how they behave in plan or default mode. I skimmed the recorded `demo/examples` files (no home-directory paths found), and I did not read style.css or the CHANGELOG and MASTER hunks.

Noticed: none
