---
id: T-0585
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:53:14Z
updated: 2026-10-09T15:05:28Z
base: f632a49eacd3005887ddd15b1f46f8d7ef1d8b2f
base_tree: 95e9b90f6d4acbfdbbe7435ed8b8d0fbbdd853f9
verified: strong
---
# Guard: IFS set by any name form, or expanded with an operator, is refused instead of erased
## Raw request
> Guard: IFS set by any name form, or expanded with an operator, is refused instead of erased
## Interpretation
Security review of T-0576: the IFS rewrite turned every IFS expansion (operator forms too) into a space, erasing payloads such as the alternate word of an IFS :+ expansion; and IFS set through a loop variable, a nameref, a split name (I""FS) or a plain IFS=/ before an unquoted expansion was never detected. All reproduced: the guard returned None.
## Assumptions (confidence)
## Acceptance criteria
- [x] the IFS probe rows (operator forms, for-loop IFS, IFS=/ then an unquoted var, declare -n, export with a split name) are blocked and the plain-IFS and IFS= read rows still pass — verify with `python3 plugin/tests/run.py -k IfsForms`
## Non-goals
## Approach (options → choice → why)
Options: (a) model IFS values fully (substitute and split) — large, still incomplete; (b) enumerate more setter forms in the old regex — the deny-list the review beat; (c) fail closed: rewrite only plain IFS / braced IFS to a space, and refuse when an IFS name appears anywhere after removing quotes and backslashes (IFS= read prefixes aside, they scope to read) while the line expands IFS or anything unquoted. Choice: (c), smallest and closed by default; legit IFS lines are rare and the block names the fix (quote the expansion). Ceiling: names built by substitution or ANSI-C quoting (declare with a computed name) — refused when the line also uses a computed assignment-builtin name.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: IfsForms rows in test_guard_pipes.py
2. [x] check_bash: rewrite only the plain IFS forms; refuse an IFS name anywhere (quotes and backslashes removed, IFS= read prefixes aside) when the line expands IFS or anything unquoted
## Resume here
## Docs impact
CHANGELOG: corrected the T-0576 line and added T-0585
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k IfsForms` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: IfsForms 0s) / FAILED (1 classes) [ran] [tree d23e294f48ab] (2026-10-09T14:54:50Z)
- (step 2) `python3 plugin/tests/run.py -k IfsForms` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: IfsForms 0s) / OK [ran] [tree 25212dceb5e7] (2026-10-09T15:00:42Z)
- (ac 1) `python3 plugin/tests/run.py -k IfsForms` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: IfsForms 0s) / OK [ran] [tree d5aabcd9c394] (2026-10-09T15:05:27Z)
- (audit intent) `self: probes for every review form block (operator, for-loop IFS, IFS=/ then an unquoted var, nameref, split and computed names, read redefined); 30-day replay: 0 newly allowed, 1 newly blocked (a session command quoting an IFS operator form, accepted friction); guard+pipes+diff+hooks suites green` → the security review's operator-erasure and IFS-set findings are refused; plain IFS still reads as a space [tree d5aabcd9c394] (2026-10-09T15:05:27Z)
- (audit adversary) `self: probes for every review form block (operator, for-loop IFS, IFS=/ then an unquoted var, nameref, split and computed names, read redefined); 30-day replay: 0 newly allowed, 1 newly blocked (a session command quoting an IFS operator form, accepted friction); guard+pipes+diff+hooks suites green` → refusal appended not returned, so allowing system can't let rm/core through; found two wider holes and captured them (T-0586 heredoc fed to bash is never read, T-0587 eval of a variable runs unread) [tree d5aabcd9c394] (2026-10-09T15:05:27Z)
- (audit edge) `self: probes for every review form block (operator, for-loop IFS, IFS=/ then an unquoted var, nameref, split and computed names, read redefined); 30-day replay: 0 newly allowed, 1 newly blocked (a session command quoting an IFS operator form, accepted friction); guard+pipes+diff+hooks suites green` → IFS= read and a tab-IFS read pass; quoted and heredoc text is data; the quote mask fails closed under ANSI-C quoting and substitutions [tree d5aabcd9c394] (2026-10-09T15:05:27Z)
## Log
- 2026-10-09T14:53:14Z created
- 2026-10-09T14:53:21Z focused
- 2026-10-09T14:57:31Z hypothesis: the 6 suite failures are rows still blocked but now under 'system' because the IFS refusal returned early; adding it last restores their own category (and a granted system can no longer let rm/core through)
- 2026-10-09T15:05:27Z done
- 2026-10-09T15:05:28Z committed 7a5c845 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0411-review: Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the co…
- T-0411 [FEATURE M, done, 3 steps] FEATURE: the guard reads a for loop over literal words (for w in agent-a agent-b; do … $w — lesson: A text rewrite ahead of the guard m…
- T-0576 [SECURITY M, done, 2 steps] Guard: ${IFS} as a word separator is read as bash splits it — lesson: A tokenizer that doesn't expand the separator variable can be to…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Lessons
- a guard rewrite that maps a family of forms to one reading must only map the forms that always mean it; refuse the rest, and append a refusal to the findings, never return it instead of them
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- plugin/tests/fixtures/guard_fuzz_escapes.txt
- plugin/tests/test_guard.py
- CHANGELOG.md
