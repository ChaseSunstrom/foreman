<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Ship a branch to main

Use when finished work on a working branch goes to main: push to main, fast-forward main, publish a release commit, or a CI job on main fails after a push.

1. **Start from fetched main**, not the local copy: fetch, then make a scratch worktree at the fetched head and cherry-pick or merge the work there. The working tree stays untouched.
2. **Check the trees match:** the shipped files in the scratch worktree equal the branch's (`git diff --quiet HEAD branch -- <paths>`). A difference means a missed or extra commit.
3. **Run the suite under the oldest supported runtime** there, once. Newer-runtime-only syntax and stdlib calls fail only on CI otherwise.
4. **Fast-forward only:** fetch again and check main is an ancestor of the commit to push; if main moved, start over from step 1. Never force-push main.
5. **Read every exit code:** don't chain the push after `;` or pipe a gate through `tail`; a green-looking tail can hide a failed step.
6. **When CI fails only there:** look for OS differences (paths, case, line endings), missing tools, suite deadlines on slow runners and stale action versions before touching the code.
7. **Clean up:** remove the scratch worktree and refresh the remote-tracking ref so the next ship starts clean.

Mined from T-1801, T-1805, T-1828, T-1840, T-1799.
