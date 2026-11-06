---
id: T-0589
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:09:18Z
updated: 2026-10-09T15:12:55Z
base: 7a5c8455736abfa64700fa9da078c0da77246f88
base_tree: d5aabcd9c394560ca297343a0e66554b98436071
verified: strong
---
# Guard: a heredoc or here-string a shell reads as its script is checked as commands
## Raw request
> Guard: a heredoc or here-string a shell reads as its script is checked as commands
## Interpretation
Found while replaying T-0585: the guard drops input redirections, so bash <<'EOF' with rm -rf ~ in the body, sh -s with a heredoc and bash <<< 'rm -rf ~' all run with no finding.
## Assumptions (confidence)
## Acceptance criteria
- [x] bash/sh reading a heredoc or here-string as its script is checked (rm -rf ~ inside is refused); data heredocs, bash -c with a heredoc and python heredocs are unchanged — verify with `python3 plugin/tests/run.py -k ShellStdin`
## Non-goals
## Approach (options → choice → why)
Options: (a) treat any heredoc on a line with a shell word as a script — over-blocks notes; (b) map each << to its exact body by order — fragile if the tokenizer and the heredoc scanner disagree; (c) record << and <<< on the command; a here-string word is checked exactly, and when a sh-family shell reads its script from a heredoc every heredoc body on the line is checked (over-inclusive only when a data heredoc shares the line). Choice: (c).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: ShellStdin rows
2. [x] _split records << and <<< on the command; check_bash checks the bodies when a sh-family shell reads stdin as its script
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k ShellStdin` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ShellStdin 0s) / FAILED (1 classes) [ran] [tree e458c544778a] (2026-10-09T15:09:31Z)
- (step 2) `python3 plugin/tests/run.py -k ShellStdin` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ShellStdin 0s) / OK [ran] [tree 6b225f2d73d3] (2026-10-09T15:11:14Z)
- (ac 1) `python3 plugin/tests/run.py -k ShellStdin` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ShellStdin 0s) / OK [ran] [tree 11554eeb68c7] (2026-10-09T15:12:54Z)
- (audit intent) `self: ShellStdin rows red then green; the security review's /dev/stdin, group, busybox, source and -c-reads-stdin forms added and blocked by failing closed (every feed on a line that runs a shell/source/eval); suites green; 30-day replay 0 newly allowed, the 1 newly blocked is T-0585's arithmetic false positive (fixed next)` → the heredoc and here-string forms that ran unread are refused [tree 11554eeb68c7] (2026-10-09T15:12:54Z)
- (audit adversary) `self: ShellStdin rows red then green; the security review's /dev/stdin, group, busybox, source and -c-reads-stdin forms added and blocked by failing closed (every feed on a line that runs a shell/source/eval); suites green; 30-day replay 0 newly allowed, the 1 newly blocked is T-0585's arithmetic false positive (fixed next)` → no per-shell argument model to outguess (the review beat the first one); a data heredoc on a shell line is read too, which over-blocks rather than under [tree 11554eeb68c7] (2026-10-09T15:12:54Z)
- (audit edge) `self: ShellStdin rows red then green; the security review's /dev/stdin, group, busybox, source and -c-reads-stdin forms added and blocked by failing closed (every feed on a line that runs a shell/source/eval); suites green; 30-day replay 0 newly allowed, the 1 newly blocked is T-0585's arithmetic false positive (fixed next)` → cat > f heredocs, python heredocs and a grep here-string pass; nested $( bash <<E ) is covered because its tokens join the line's commands [tree 11554eeb68c7] (2026-10-09T15:12:54Z)
## Log
- 2026-10-09T15:09:18Z created
- 2026-10-09T15:09:25Z focused
- 2026-10-09T15:12:55Z done
- 2026-10-09T15:12:55Z committed 2f5a0d4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0586 [SECURITY M, dropped, 0 steps] SECURITY!: guard never reads a heredoc or here-string fed to a shell: bash <<'EOF' rm -rf
- research T-0158-review: Verdict: changes needed.** I found four verified bypasses and one regression. I could not run code here (read-only), so every trace is by hand ag…
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
## Lessons
- when the guard can't tell which input a program runs as code, read every candidate input as code; argument models of shells get outguessed
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- CHANGELOG.md
