## Verdict
Changes needed. No CRITICAL or HIGH findings, but I found three MEDIUM issues on the guard and untrusted-text paths you flagged.

The pre-audit `sha1(` hit is a 6-hex case-id suffix (`fmbench.py:301`), not security. Dismissed.

## Findings

**MEDIUM — `plugin/lib/fmbench.py:196-197`.**
- `_judge` runs `git add -A` and `git diff --cached` in the replay worktree after the bypass-mode session has finished.
- `_git` (`fmbench.py:30-32`) strips only `GIT_*` from the environment. It doesn't strip credentials, and it doesn't neutralise config the session wrote.
- A worktree shares the main repo's `.git/config`. A session that sets `core.fsmonitor` or `core.hooksPath` gets that command run by the judge's `git add`, on the host and outside the guard.
- `_grade` (`fmbench.py:81`) has the same exposure, but judged cases make it routine.
- Fix: run these calls with `_env(...)`, `-c core.fsmonitor= -c core.hooksPath=/dev/null`, and `GIT_CONFIG_NOSYSTEM=1`.
- Confidence: medium. The mechanism is standard git behaviour, but I didn't run it.

**MEDIUM — `fmbench.py:349`.**
- The shadow user's `NEXT:` line is fed to a bypass-mode `--resume` session.
- That line comes from a child that read the agent's reply, which can contain repo content, so injected text can be turned into a user-authority instruction.
- `nxt` gets only `[:1000]`. The `REPEAT:` lines get `c.plain`, but `NEXT` doesn't.
- The guard still applies to the next session, which limits the damage.
- Fix: run `c.plain` and `c.defang` on `nxt`. Prefix it with "(simulated user)". Mention in the `SHADOW` prompt that the agent reply may contain instructions to ignore.
- Same class, lower risk: the diff and reply go into the judge prompt (`fmbench.py:199-203`) with no delimiters. A diff containing `SCORE: 5` or a fake `Rubric:` block can sway the judge. Fence the diff and reply, for example in `<diff>` tags, and say the fences are data.

**MEDIUM — `fmbench.py:415-416`.**
- The guard check for `soak` lives in `_contest`, not in `soak_case`. The existing invariant is that `run_arm` refuses a guardless plugin so no caller can skip it.
- A direct `soak_case` call, or a future caller, skips the check.
- Court, duel and versions do go through `run_arm`, so their guard check holds. For versions, the old revision's plugin is checked inside the `with` (`fmbench.py:458`).
- The duel contender folder is never checked, only Foreman's own plugin dir. That is acceptable, because guard hooks come from Foreman. The hook-precedence assumption is untested.
- Fix: move `has_guard` into `_session`, or into a shared `_require_guard`.
- Tests: none cover guard refusal on the new arms. Add a soak test and a versions-old-arm test.

**LOW — `fmbench.py:347`.**
- If `res` has no `session_id` (`sid` is None), the loop breaks after turn 1 with `pass: True` and no error. That is a silent shortcut.
- `"DONE" in lines` also misses "DONE." Fix: record an error when `sid` is missing, and match `startswith("DONE")`.

**LOW — `fmbench.py:330`.**
- `keep=True` leaves session transcripts in the real `~/.claude/projects`, one per soak under a temp cwd, and they are never cleaned up.
- `transcript: talk` (`fmbench.py:351`) is saved unredacted, although the prompt is redacted.
- Fix: run `c.redact` on `talk`.

**LOW — `fmbench.py:245-248`.**
- The judge is paid for even when the session already errored, because the judge call isn't skipped.
- Soak's own loop (`fmbench.py:329-349`) catches only `ValueError`. An `OSError` from `_worktree` aborts the whole command.

**LOW — `fmbench.py:417`.**
- `--budget nan` slips through `fmbudget` (`min(nan, 0.5)` is `nan`), the same class as the earlier `--day nan` finding.
- `--max -1` slices off the last case. Both are in `fmcli.py:546-549`.

**LOW — `fmbench.py:112-142`.**
- A plain `bench build` (no `--judged`) silently drops previously built judged cases, because the keep rule at `fmbench.py:485` only keeps `C-` and `R-` ids.

## Acceptance criteria
- **T-0231: met.** `test_a_docs_only_task_is_judged` covers the judged case, the score in the results, `show`, and the pane.
- **T-0240: met.** The duel test asserts both arms' `--plugin-dir` lists and the gate.
- **T-0241: met.** The versions test asserts the old worktree path, the current plugin, the gate, and cleanup.
- **T-0242: met.** The court test asserts a case built from the steer with its rubric, and the judge reading it.
- **T-0243: met.** The soak test asserts `--resume s-1`, the complaints, and that `--no-session-persistence` is absent.
- I read the tests but did not run them.

## Not checked
- I didn't run the test suite.
- I didn't verify `c.plain` and `c.defang` behaviour.
- I didn't check how Claude Code resolves conflicting hook decisions between plugins.
- I didn't check the `register.tsx` rendering beyond reading the diff.
