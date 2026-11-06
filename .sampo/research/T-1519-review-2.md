All six review points are fixed test-first, in one commit on top of a clean `foreman/build` merge. The 12 tests in `test_docs` (Fences, HelpAnswers and CardDates) pass.

**Branch:** `worktree-agent-a95e79731a41dd6d8` · **Commit:** `ae719826e2b91e14f8e63bf83c4b237c83d0db87` (the merge is `6b52c82d`)

1. **`fm new check` no longer runs just any `.py`.**
   - It applies fm code's own rule first: the file must be yours and writable by no one else. That holds even with `--run`.
   - A file with a `.git` above it, outside fm code's `tui/` folder, is refused unless `--run` is given. The test confirms the file didn't run (marker file absent).
   - `fm new -h` now says "check runs the file for a panel".
   - `--run` works at the end (`fm new check PATH --run`). argparse rejects it between `check` and the path, so the docs and messages show the trailing form.
2. **The panel check runs in a child process** through `fmplaybooks._run`, which now takes a `stdout` argument. It gets limits, a 20 s timeout and a process-group kill.
   - Its result only counts on a line carrying a random token made for that run.
   - So `sys.exit`, `os._exit`, a swallowed exception or a hang can't end it green.
   - Tests cover: `sys.exit(0)` at import and while drawing, a bare-except loop, `signal.alarm(0)` plus a loop, and `os._exit(0)`. The earlier in-process alarm is gone.
3. **Fences:**
   - README, MASTER, the release-check output line and the docstrings now say runnable fences are trusted like tests (they can reach any file and the network).
   - TMPDIR now points inside the fence's own folder (tested).
   - The "empty temporary folder" wording is fixed.
4. **Copies:** without `--force` the file is created with O_EXCL, so anything already there or appearing meanwhile stays put. `--force` replaces a symlink itself, never what it points to; the help, the error message and the module doc say so. A test plants a dangling link to prove it.
5. **`verified:`** dates now allow one day ahead for time zones (tested).
6. **`fm help`:**
   - Answer lines stay within 100 columns, and a long help is cut to the part holding the question's words (e.g. "… new: scaffold a tested MCP server …").
   - `--all` together with a question is refused.
   - A question made only of asking words like "can it do that?" is refused with "nothing to look up".
   - The plain-no reply is now two lines, both under 100 columns.

**Evidence:**
- Red first: `run.py -k test_docs.Fences -k test_docs.HelpAnswers -k test_docs.CardDates` → ✗, as expected.
- Green: the same command passes.
- `fm check --affected --evidence T-1519` → 661 tests OK.
- test_playbook_check, test_help, test_board_verbs, test_doctor and test_planning all pass.
- The criterion's literal `cd plugin/tests && python3 -m unittest test_docs.Fences` still needs a run from the main checkout, since the lane refuses `cd` chains.

**Weakest link:** the token only stops a file that exits early by accident. A file written to cheat could still dig the token out of the checking process and fake a pass.

**Files to read first:** `plugin/lib/fmnew.py`, `plugin/lib/fmcli.py` (`cmd_help`, the `new` registration), `plugin/tests/test_docs.py`.

**Noticed:**
- With a positional that takes any number of words, argparse rejects a flag placed between those words. `fm new check --run PATH` hits this, and other `fm` verbs with word lists likely do too.
- A home folder that is itself a git repo (dotfiles) makes every panel under it need `--run`.
