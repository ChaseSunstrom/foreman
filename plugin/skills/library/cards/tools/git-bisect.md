---
name: git-bisect
title: Git bisect
area: tools
tags: [git, bisect, regression, debugging, history, automation]
detect: []
related: [git, git-rebase, git-worktrees]
---
Find the commit that introduced a regression by binary search, automated with a script that exits 0, 1 or 125.

## Verify
- `git bisect log`: the good and bad marks recorded so far.
- `git bisect run ./repro.sh`: the search runs unattended and prints the first bad commit.
- `git show --stat BAD_SHA`: the culprit commit really touches the failing area.
- `git bisect reset`: you are back on your original branch afterward.

## Test first
Write the repro script first and prove it on both ends before bisecting.
```sh
#!/bin/sh
# repro.sh: exit 0 = good, 1-127 except 125 = bad, 125 = cannot test, skip
make build >/dev/null 2>&1 || exit 125
./run-test.sh test_parses_empty_input
```
```sh
git checkout GOOD_SHA && ./repro.sh; echo $?   # expect 0
git checkout BAD_SHA  && ./repro.sh; echo $?   # expect 1
```

## Do
- Start with `git bisect start BAD GOOD`; mark with `git bisect good|bad`.
- Automate with `git bisect run CMD`; the script must be outside the work tree or untracked so checkouts do not change it.
- Return 125 (skip) when the commit does not build, so it is not misjudged as bad.
- Use `git bisect skip` by hand for commits you cannot test.
- Test one behavior; a flaky test gives a wrong answer. Run it several times first.
- Use `git bisect start --term-old=OLD --term-new=NEW` for non-regression searches such as when a behavior changed.
- Use `git bisect start --first-parent` on a merge-heavy mainline to find the merge that broke it.

## Avoid
- A repro that exits non-zero for setup failures: they are blamed as bad. Return 125 for those.
- Exit codes above 127: bisect run aborts. Keep codes within 0 to 127.
- Marking good and bad backward: the search converges on the fix. Check with the two sanity runs.
- Bisecting with uncommitted changes: checkouts fail or carry edits. Commit or `git stash` first.
- Forgetting `git bisect reset`: you stay on a detached HEAD.
- Trusting a bisect across a broken-build range without skipping: the result may blame an unrelated build fix.

## Review
- [ ] The repro passes at the good commit and fails at the bad one before the run.
- [ ] The reported commit is read and plausibly causes the failure.
- [ ] A fix and regression test are added, not just the revert.
- [ ] The bisect was reset and the work tree is clean.
