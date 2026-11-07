---
id: T-1921
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T05:55:46Z
updated: 2026-10-29T06:32:43Z
base: 71996c224507a2f36ded2c655f8f1b0ce1b5a445
base_tree: a1586d85545b0eaabec12bbc40b636bcb75d4a00
plan0_at: 2026-10-29T06:05:24Z
plan0_scope: []
verified: strong
---
# Guard reads a substitution behind 'cd /abs &&' from the starting folder too
## Raw request
> FIX: guard reads the text after any $( from the starting folder too (T-0158 tails), so 'cd <scratch> && echo $(ls) && git reset --hard' blocks as core though the cd is certain; give a tail the folders of the command its $( sits in
## Interpretation
Substitution bodies and the text after each $( (T-0158 tails) are read before the walk, from the starting folders plus every cd target. So 'cd <scratch> && echo $(ls) && git reset --hard' and 'cd <scratch> && x=$(git cherry-pick a)' block as tree writes over Foreman, though nothing in an && chain runs where the line starts once its head cd fails or succeeds.
## Assumptions (confidence)
## Acceptance criteria
- [x] a substitution or tail behind a literal absolute head cd in an && chain is read from the cd target only; adversarial heads (relative, quoted, option, redirect with substitution, ; or || later, pipe) still read from the start — verify with `python3 plugin/tests/run.py test_guard`
- [x] nested text (eval, sh -c, sh <<<, find -exec, backticks) is judged from the folders the caller may be in, so cd <foreman> && sh -c '<tree write>' from scratch blocks; a mover after the head cd keeps the start folder — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
When the line is an && chain (top-level and_chain) whose raw text starts with 'cd /literal-abs-path &&' (no quotes, expansions, globs, options or substitutions in the head), the nested-read starts become that cd's target instead of the starting folders; other cd targets still join. Rejected: moving the substitution reads into the walk (needs body positions, large diff); prefixing each tail with the line text before it (a stray ) confuses the split). Relative heads, CDPATH, cd options, redirects or prefix assignments on the head keep today's behavior.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Table test: cd {scratch} && echo $(ls) && tar xf - allowed; adversarial heads block
2. [x] Fix in check_bash's pre-walk _DCWD
3. [x] Review, full test_guard
## Resume here
<!-- auto -->
- 2026-10-29T06:29:07Z step 3/3: Review, full test_guard
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/mem1922.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/fails1922.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1922.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/probe1921.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/count1921.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/prof1921.py, plugin/lib/fmguard.py
- failures met: modulenotfounderror: no module named 'fmguard'
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 295 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 572fe9d110cc] (2026-10-29T06:15:11Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 295 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 572fe9d110cc] (2026-10-29T06:15:22Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 295 tests in 8.7s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 572fe9d110cc] (2026-10-29T06:15:39Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 295 tests in 7.8s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 572fe9d110cc] (2026-10-29T06:15:39Z)
- (ac 1) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)|row" | head` → ✗ exit 1 · Ran 295 tests in 11.9s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 9s, Trust 6s) / FAILED (1 classes) [ran] [tree 50275799cd00] (2026-10-29T06:31:32Z)
- (ac 2) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)|row" | head` → ✗ exit 1 · Ran 295 tests in 11.9s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 9s, Trust 6s) / FAILED (1 classes) [ran] [tree 50275799cd00] (2026-10-29T06:31:32Z)
- (ac 1) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|KeyError|Ran|OK|FAILED)" | head` → exit 0 · Ran 295 tests in 11.6s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 10s, Trust 8s) / OK [ran] [tree 2d94b2c106e7] (2026-10-29T06:31:48Z)
- (ac 2) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|KeyError|Ran|OK|FAILED)" | head` → exit 0 · Ran 295 tests in 11.6s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 10s, Trust 8s) / OK [ran] [tree 2d94b2c106e7] (2026-10-29T06:31:48Z)
- (step 3) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|KeyError|Ran|OK|FAILED)" | head` → exit 0 · Ran 295 tests in 11.6s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 10s, Trust 8s) / OK [ran] [tree 2d94b2c106e7] (2026-10-29T06:31:48Z)
- (step 3) `python3 plugin/tests/run.py test_approve_reads test_guard test_guard_diff test_guard_evasions test_guard_exec_vectors` → exit 0 · Ran 298 tests in 8.0s (89 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree ef93eea8b045] (2026-10-29T06:32:17Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 295 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree ef93eea8b045] (2026-10-29T06:32:31Z)
- (ac 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 295 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree ef93eea8b045] (2026-10-29T06:32:31Z)
- (audit intent) `One fm-reviewer pass; its six findings were verified with probes against the committed guard, then fixed with test rows.` → cd <scratch> && echo $(ls) && git reset --hard passes; nested text after a cd into Foreman blocks from scratch [tree ef93eea8b045] (2026-10-29T06:32:31Z)
- (audit adversary) `One fm-reviewer pass; its six findings were verified with probes against the committed guard, then fixed with test rows.` → fused words, quoted backticks, eval/source/pushd, a pipe head and python -c after the head all block [tree ef93eea8b045] (2026-10-29T06:32:31Z)
- (audit edge) `One fm-reviewer pass; its six findings were verified with probes against the committed guard, then fixed with test rows.` → a six-folder cd loop is allowed now that a memo counts distinct pairs; depth-0 calls clear folder state for fmmcp [tree ef93eea8b045] (2026-10-29T06:32:31Z)
## Log
- 2026-10-29T05:55:46Z created
- 2026-10-29T06:05:22Z set type=FIX, tier=M, title=Guard reads a substitution behind 'cd /abs &&' from the starting folder too
- 2026-10-29T06:05:22Z planned: it has criteria and steps
- 2026-10-29T06:05:23Z focused
- 2026-10-29T06:13:22Z hypothesis: the None pass (rd None for a CDPATH cd) starts with lost=[''] only, so the nested walk loses the caller's lost tails (plugin) and can't guess R/plugin/lib; test: read _target_cats' guess words
- 2026-10-29T06:13:42Z ruled in: unknown-folder guesses use only the read text's words; same at top level (cd $X && git reset --hard allowed). Pre-existing, captured separately; rd CDPATH edit reverted
- 2026-10-29T06:32:41Z done
- 2026-10-29T06:32:43Z committed f236445b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1920 [FIX M, done, 3 steps] Guard reads a compound after 'cd <scratch> &&' as a tree write over Foreman — lesson: When masking text for one check, keep it length-align…
- T-0384 [FIX M, done, 3 steps] FIX: guard false positives seen on JARVIS: (1) cd ABS && A > f; B > g resolves f/g against — lesson: Making the guard more precise means re…
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar finished tasks took 3–3 steps
- start here (files T-1920 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py, CHANGELOG.md
## Why not caught
Nested text reused the hook's context, and no test ran a nested payload from a scratch folder behind a cd into Foreman, or the reverse.
## Lessons
- When the guard trusts a cd folder, check the parsed argv words, not masked text: fused words and quotes defeat regex masking.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
