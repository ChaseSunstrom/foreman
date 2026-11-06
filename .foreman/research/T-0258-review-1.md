**Verdict:** changes needed. I found one HIGH cross-feature issue, two MEDIUM, and the rest are LOW doc or maintainer drift. I read the whole diff and spot-checked `fmguard.py`, `fmcore.py` and `fmresearch.py` in the repo. I did not run any code.

## Findings, ranked

**1. HIGH (adversary), `fm export agents --out PATH` is a write the guard never sees.**
- The write is at `plugin/lib/fmcost.py` `cmd_export`: `c.write_atomic(abspath(args.out), agents_md(p))`.
- The guard's `fm` branch (`plugin/lib/fmguard.py:1348-1366`) only inspects `--run`, `--allow`, `plugins` and `serve`. `_write_targets` (`:1610`) has no `fm` case, and a grep for `--out` in `fmguard.py` finds nothing.
- Triggering input: `fm export agents --out ~/.claude/skills/x/SKILL.md`, or any nonexistent path such as `~/.claude/rules/x.md` or `~/.config/autostart/…`. The existing-file check passes for a missing file, so Foreman writes outside the project with no guard category.
- The content is not fixed text. It includes lessons, decisions and corrections that the agent itself wrote (`fm task finish --lesson`). That is a way to plant instruction files or persistence.
- With `--force`, any non-symlink file is overwritten, for example `--out ~/.bashrc --force`. That is data loss.
- Fix: in the guard, treat `fm export … --out`/`-o` as a write target, using the same classification as `cp`. Also make `cmd_export` refuse a path outside the project root unless the user granted it.
- Confidence: high that the guard misses it. Medium on how far the planted-skill chain goes.

**2. MEDIUM (adversary/intent), `fm second session` says "confirm-first" but full autonomy self-approves.**
- `plugin/lib/fmsecond.py` (the `_create(... explore=True)` call, comment "confirm first: the words came through a child") and the MASTER and CHANGELOG T-0276 lines all say confirm-first.
- `plugin/lib/fmcore.py:1506` (`needs_approval`) returns False for explore items when `autonomy == "full"`.
- Chain: a pasted page in a past transcript, up to 300 characters per message, reaches the child. The child's "missed request" becomes a FEATURE item, and in full autonomy it is worked unattended.
- Fix: for items captured via `second session`, set a marker that `needs_approval` honours even in full autonomy. Otherwise remove "confirm-first" from the docs.

**3. MEDIUM (adversary), the judge's `git add -A` runs filter drivers.**
- `plugin/lib/fmbench.py` `_judge` runs `_git(wt, "add", "-A")` after a bypass-mode session. The T-0280 review hardening only adds `-c core.fsmonitor=` and `core.hooksPath=/dev/null` in `_git`.
- `filter.<n>.clean/process` keys, together with a `.gitattributes` the session wrote, still execute during `git add`. `_GIT_EXEC_KEYS` knows these keys, but only the guard uses it.
- The session's own guard blocks `git config filter.*`. A write to the shared `.git/config` by another route would still land here.
- Fix: stage with `-c core.attributesFile=/dev/null` and drop `.gitattributes` from the worktree before staging, or diff with `diff -ruN` against a pristine export instead.
- Confidence: medium.

**4. LOW (operator), MASTER line 60 (T-0271) is stale.**
- It still says each hunk is reverted with `git apply -R --unidiff-zero`.
- The pass-4 bullet (line 61) says that was replaced by `_revert_hunk` because it mutated the wrong line.
- The `# ponytail:` comment at `plugin/lib/fmcli.py` `task_prove_hunks` still says "a whole new function is one hunk", but T-0279 now splits new Python files by definition.
- Fix: edit both.

**5. LOW (operator), the MASTER CLI line and file map were not updated for several commands.**
- The CLI line lists `tour`, `second` and `export`. It does not list `landscape`, `deps`, `replay [--cmd --cwd]` or `bench duel|versions|court|soak`.
- The `fmbench` file-map entry still says `build|run|list|compare`.
- Fix: add them.

**6. LOW (operator), a broken `routing.json` fails silently.**
- `c.routing()` returns `{}` on any problem, which empties `STAGE_WORDS`, `LENS_WORDS` and `SPLIT_GROUPS`. `SPLIT_GROUPS` and `fmplugins._ROUTES` are read once at import.
- `fmdoctor` never calls `routing_problem`; a grep confirms only tests and `fmevolve` do.
- An `fm evolve` change or a hand edit that breaks the file therefore degrades `--split` to one reviewer and removes the hints, with no warning.
- Fix: add a doctor check that calls `routing_problem`.

**7. LOW (operator), `fm replay --cwd` does nothing without `--cmd`, and nothing says so.** `fm second debate` also accepts `--model` and ignores it. Fix: reject or document both.

**8. LOW (adversary), `fm bench duel` does not guard-check the rival plugin.**
- `has_guard` runs only on `plugin`. The `extra` plugin dirs are loaded into a bypass-mode session unchecked.
- MASTER says "candidates should be Foreman's own reviewed code", and duel breaks that for arbitrary folders.
- Fix: document it, or require the rival to be an installed id.

**9. LOW (edge), `fm doctor`'s `integrity` check scans every project's repo and state JSON.**
- One damaged unrelated repo makes `FAIL` for all of them. If doctor is a configured gate, as in Foreman's own project, that fails unrelated work.
- Fix: scope the gate to the current project, or report other projects' damage as WARN.

**10. LOW (maintainer), duplicated helpers.**
- Test-file regexes: `c.TESTISH`, `fmbench.TEST_FILE` and `fmmap._TEST`. T-0266 shared only `CODE`.
- Word-overlap thresholds: `fmoutside._same` (half the shorter), `fmresearch.cross_check` (half the union), `fmsecond.session` (70%) and `fmrecall.covered`.
- Tool-less child runners: `fmsecond._child` and the older ones in `fmideas`, `fmresearch` and `fmevolve`.

## Per lens

- **Operator:** 4, 5, 6, 7.
- **Adversary:** 1, 2, 3, 8. The soak chain (repo file, to agent reply, to shadow user, to next prompt) is defanged and capped at 1000 characters, and the replay is guarded, so I am not flagging it.
- **Maintainer:** 10, plus the stale comment in 4. I found no dead imports.
- **Edge:** 9 only. The meta keys `landscape_at` and `second_session` are written under the lock, and the shared `hints.json` race is documented in the code.
- **Intent:** 2, and the stale `git apply -R` claim in 4.

## Not checked

- Guard heredoc and git-channel parsing correctness; I only looked at how the guard handles `fm`.
- The test suite, and the foreman-ui rendering.
- Whether `c.defang` neutralises `$(…)` in `AGENTS.md` content.
