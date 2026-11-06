**Verdict:** approve with nits. I found no HIGH findings. I read the diff and `fmcore`'s `find_project`/`routing` but did not run any tests.

**Intent lens: ok.** All three requests are covered, and the changes match what the acceptance criteria describe. I found nothing that was asked for and left undone, and nothing added that wasn't asked for.

**Edge lens: changes needed (both LOW)**

- **LOW — `plugin/lib/fmdoctor.py:122` and `:130`.** The empty-git-object scope test uses `root in mine`. `mine` holds `current.root`, and in a lane worktree `find_project` sets that to the worktree path. `integrity_roots` lists the main checkout's root, not the worktree's. Run from a lane, damage in the current project's own repo (the shared `.git/objects`) therefore only warns, though the criterion says the current project must still fail. The same-slug check on the state files at line 133 is fine.
  - Fix: also add `c.main_worktree(current.root)` to `mine`, or compare git common dirs.
  - Confidence: medium.

- **LOW — `plugin/lib/fmdoctor.py:130` and `:133`.** `current is None or …` turns every project's damage into FAIL when doctor runs from outside any project. The request was that another project's damage should warn. For a non-project cwd (a CI run or a plain `fm doctor` from `~`), one damaged unrelated repo fails the gate again. If that is intended, say so in the docstring; otherwise treat `current=None` as warn-only for projects, with Foreman's own repo still failing.
  - Confidence: medium.

Everything else I checked is fine:
- `check_routing` reads the same file as `c.routing()` (`PLUGIN = c.PLUGIN_ROOT`) and reports a missing or unparsable file as FAIL.
- `_contender` resolves a folder by realpath against the installed list. A symlinked folder whose real path matches an installed plugin is accepted, which looks intended.
- `--model` on `second plan` and `second session` keeps its `"sonnet"` default through `args.model or "sonnet"`.

**Acceptance criteria**
- **T-0292 (docs): met.**
  - The MASTER CLI line now has landscape, deps, `replay [--days N --accept] [--cmd TEXT --cwd DIR]`, and `bench` duel/versions/court/soak.
  - The T-0271 bullet no longer mentions `git apply`.
  - The file-map entry for `fmbench` names the new subcommands.
  - The `prove --hunks` ponytail comment was updated.
  - I did not run `test_followups.py -k Docs`.
- **T-0293 (operator): met except for the two edge cases above.**
  - Doctor adds a `routing` check.
  - `replay --cwd` without `--cmd` is refused (`fmreplay.py:87`).
  - `second debate --model` is refused (`fmsecond.py:204`).
  - Integrity scoping works at the project level, with the lane-worktree and no-project-cwd exceptions noted.
- **T-0294 (rival): met.**
  - `_contender` accepts only an installed plugin's id or folder.
  - Anything else gets a `UsageError` at `fmbench.py:575`, before any arm runs.

**Not checked:** the adversary, operator and maintainer lenses, and test execution.
