## intent: changes needed

**HIGH — `plugin/lib/fmevolve.py:84-113`. The two arms differ by more than the proposed edit.**
- The live arm replays `os.path.join(repo, plugin_dir)`, which is the working tree, including uncommitted changes.
- The candidate worktree is created from `HEAD` (line 96).
- The target is read from the working tree (line 86) and then written over the `HEAD` copy (line 101). The same applies to the mutation child's input.
- Today `git status` shows `fmbench.py`, `fmcli.py` and `improve/SKILL.md` as modified, and `fmevolve.py` as untracked. The candidate plugin therefore lacks those changes, and the gate compares "working tree" against "HEAD plus edit".
- A pass, a fail or a cost swing can come from the uncommitted drift instead of the edit. The gate's result is then not evidence about the edit.
- The tests don't catch this, because the test repo has a clean tree.
- Fix, either of these:
  - Refuse to run when `git status --porcelain -- <plugin_dir>` is non-empty.
  - Run the live arm from a second `HEAD` worktree, so both arms differ only by the edit.

**MEDIUM — `fmevolve.py:82-85`. The target is not limited to a text component.**
- The request says "one Foreman text component (a skill, reference, rule section)". The only check is that the file is under `plugin/`.
- `--target plugin/lib/fmguard.py` or `plugin/hooks/hook` is accepted, and the child is told it is revising an "instruction file".
- A candidate could weaken the guard. Bench replays refuse a plugin that ships no guard, but they don't check that the guard is intact.
- Fix: allow only `skills/**/*.md`, `rules/*.md` and `agents/*.md`. Reject `lib/`, `hooks/` and `bin/`.

**MEDIUM — `fmevolve.py:113-118`. "Winner" means "no worse", not "better".**
- Any candidate with equal passes and cost within 15% is kept.
- With `--runs 1` and 3 cases, nearly every edit ties. Each tie leaves an `evolve/*` branch and a worktree beside the repo (`<repo>.evolve/`, in `~/.claude`) until someone cleans it up.
- The user asked that winners wait for their yes. Nothing marks a keeper as an improvement (fewer tokens or more passes), and nothing cleans up old keepers.
- Fix: report whether passes or cost actually improved. Mention `fm tidy` or a removal command in the output.

**LOW — `fmevolve.py:90-91`. A no-op revision returns a result without a `label`, `target` or `worktree`.**
- `cmd_evolve` handles this through `.get`, and `res['why']` is present, so it doesn't crash.
- A "child proposed no change" run exits 1, the same as a gate failure, so the two can't be told apart by exit code.

## Acceptance criteria
- **AC1 (stubbed generation, keep or remove, `--drop`):** covered by `test_evolve.py` (keep, drop and `--drop` cases). I did not run the tests. The clean-tree test cannot expose the HEAD-versus-working-tree drift above.
- **AC2 (one live generation on a real target, verified by `fm bench list`):** not verifiable from the code. The criterion also doesn't capture the request, because `fm bench list` shows that results exist and not that the gate was fair.

## Not checked
- I did not run the tests.
- I did not read the test file in full.
- I did not read the `improve/SKILL.md` change (its diff line was omitted as too long).
- I did not check `install.sh` or the doctor budgets.

Files: `~/.claude/foreman/plugin/lib/fmevolve.py`, `~/.claude/foreman/plugin/lib/fmbench.py`
