---
id: T-1123
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py]
depends_on: []
source: discovered
created: 2026-10-16T06:20:28Z
updated: 2026-10-16T06:48:27Z
base: 03f194bedbc50318c25d05a806be5293b1c87389
base_tree: 16837e28ac1f3107bd67f6715b07d2b5181bca4b
verified: strong
---
# Guard gaps a review found: (1) non-recursive rm fed targets on stdin (echo <core file> | x
## Raw request
> Guard gaps a review found: (1) non-recursive rm fed targets on stdin (echo <core file> | xargs rm) isn't checked (only recursive rm with stdin targets is; _write_targets returns explicit operands only); (2) eval of a command substitution that prints a dangerous command (eval "$(printf 'rm -rf ~')") is allowed. Guard both, with tests, and rerun fm bench guard --mutate
## Interpretation
Two guard gaps a review found. (1) Non-recursive rm whose targets come from stdin (echo <file> | xargs rm, find … | xargs rm) isn't checked: only recursive rm with stdin targets is (fmguard ~2775-2780), and _write_targets returns explicit operands only. Guard it the same way the recursive case is (the upstream find's paths when known; otherwise rm-outside 'rm with targets from stdin'), but keep plain deletes of explicit in-project files allowed. (2) eval of a command substitution whose output is a dangerous command (eval "$(printf 'rm -rf ~')") is allowed: the eval readings don't evaluate printf/echo output. Read literal printf/echo output inside the substitution as the eval text and check it; an unknown substitution in eval stays as today unless it downloads (pipe-shell already).
## Assumptions (confidence)
## Acceptance criteria
- [x] echo X | xargs rm (X a core or out-of-project path) and eval "$(printf 'rm -rf ~')" are blocked; xargs rm on files the upstream find lists inside the project and eval "$(echo ls)" stay allowed — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing table rows for both gaps and their allowed forms
2. [x] Guard stdin-fed rm and literal printf/echo eval substitutions; run fm bench guard --mutate --only rm-outside
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 107 tests in 8.3s (46 classes, 16 at a time; slowest: GuardAgainstBash 8s, Hook 3s, RuleIds 1s) / FAILED (1 classes) [ran] [tree fa4868285a1b] (2026-10-16T06:26:03Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 107 tests in 6.9s (46 classes, 16 at a time; slowest: GuardAgainstBash 7s, Hook 2s, KnownVars 1s) / OK [ran] [tree 49ec95a9f1d9] (2026-10-16T06:26:52Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 107 tests in 18.6s (46 classes, 16 at a time; slowest: GuardAgainstBash 18s, Hook 4s, RuleIds 1s) / OK [ran] [tree 1d894a195371] (2026-10-16T06:31:34Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 111 tests in 6.0s (47 classes, 16 at a time; slowest: GuardAgainstBash 6s, Hook 2s, KnownVars 1s) / OK [ran] [tree 170b315089ed] (2026-10-16T06:40:51Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 111 tests in 5.1s (47 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, RuleIds 0s) / OK [ran] [tree 2793c04a5b8e] (2026-10-16T06:45:24Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 111 tests in 5.7s (47 classes, 16 at a time; slowest: GuardAgainstBash 6s, Hook 2s, RuleIds 0s) / OK [ran] [tree 8f493b98091f] (2026-10-16T06:47:56Z)
- (audit adversary) `review: one fm-reviewer security pass; 4 bypass classes found and closed test-first (whitespace/escapes in echo operands, intermediate filters and xargs -a, explicit operands hiding stdin, unreadable eval substitutions), plus combined xargs option clusters; mutation: rm-outside 5/5, pipe-shell 4/4 killed` → every reviewer bypass is a blocked table row (echo 'src /etc', echo -e escapes, printf formats, cat/sed between echo and xargs, xargs -a/-d/-I/-0 and -n1da clusters, explicit operand plus stdin, eval with %, flags, command/bin echo, quoted parens); doubt reads as unknown targets [tree 8f493b98091f] (2026-10-16T06:47:56Z)
- (audit edge) `review: one fm-reviewer security pass; 4 bypass classes found and closed test-first (whitespace/escapes in echo operands, intermediate filters and xargs -a, explicit operands hiding stdin, unreadable eval substitutions), plus combined xargs option clusters; mutation: rm-outside 5/5, pipe-shell 4/4 killed` → over-broad on purpose: xargs -L1 now blocks a delete that would pass; plain in-project echo targets and eval of a plain echo stay allowed [tree 8f493b98091f] (2026-10-16T06:47:56Z)
- (audit self) `review: one fm-reviewer security pass; 4 bypass classes found and closed test-first (whitespace/escapes in echo operands, intermediate filters and xargs -a, explicit operands hiding stdin, unreadable eval substitutions), plus combined xargs option clusters; mutation: rm-outside 5/5, pipe-shell 4/4 killed` → no findings [tree 8f493b98091f] (2026-10-16T06:47:56Z)
## Log
- 2026-10-16T06:20:28Z created
- 2026-10-16T06:25:24Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py']
- 2026-10-16T06:25:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1123.builder.md
- 2026-10-16T06:25:33Z focused
- 2026-10-16T06:47:39Z merged worktree-agent-a9c7ee3c167f7bf3d (2 file(s))
- 2026-10-16T06:47:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9c7ee3c167f7bf3d
- 2026-10-16T06:47:41Z focused
- 2026-10-16T06:47:50Z scope: CHANGELOG.md — release note
- 2026-10-16T06:48:26Z done
- 2026-10-16T06:48:27Z committed e935d9f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1120 [SECURITY S, active, 1 steps] Guard tests for the six rules fm bench guard --mutate found untested (T-1066 real run): pi
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- research T-0384-review: Changes needed.** I found four concrete bypasses by reading the code. I could not run bash or the tests, because I only had read tools. For each …
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A rule that trusts an upstream command's output must prove that output is exactly its operands; any rewriting stage or option turns it unknown
## Plan gaps
- failed first: step 1 Failing table rows for both gaps and their allowed forms
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
