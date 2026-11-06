---
id: T-1929
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T07:03:45Z
updated: 2026-10-29T07:24:32Z
base: ecc55cd87efca840ef21b5a3e516b78c6e7570bb
base_tree: ca7c48d13da8b6de582769a846dafffd1b758335
plan0_at: 2026-10-29T07:13:28Z
plan0_scope: []
verified: strong
---
# Guard refusals for lines too tangled to analyse are never lifted by a grant
## Raw request
> Guard: both folder caps (nested commands, folder sets) refuse under rm-outside; a task's rm-outside grant may lift them and let an unanalysed line pass: give them a category no grant lifts
## Interpretation
The three refusals for a line the guard can't finish reading (nesting too deep, nested commands in too many folders, the line in too many folders) are rm-outside, so a task's rm-outside grant lifts them and the unread rest of the line runs. They must refuse under any grant; splitting the command is the way through.
## Assumptions (confidence)
## Acceptance criteria
- [x] an rm-outside grant leaves both folder caps and the nesting cap refused; a plain rm-outside is still lifted — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Options: (1) a new category in NOT_AUTHORIZABLE: touches CATEGORIES order, rule ids, docs, dojo and replay labels; (2) check() treats a refusal whose detail says 'to analyse' as no grant lifts, and message() says so instead of offering --allow: one helper, rule ids unchanged; (3) drop the grant on lines that hit a cap by re-checking: more code, same effect. Choice: (2), the smallest change that keeps categories and rule ids stable. The 3rd-repeat hint in fmhooks stops offering fm ask for these too.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test: caps refused under an rm-outside grant (red); check() and the message treat a 'to analyse' refusal as no grant lifts (green)
## Resume here
<!-- auto -->
- 2026-10-29T07:19:07Z steps 1/1 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/tests/test_guard.py
- touched since last checkpoint: plugin/tests/test_guard.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, CHANGELOG.md
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.TokenFallback.test_a_line_too_tangled_to_analyse_is_refused_under_any_grant` → ✗ exit 1 · run.py: no test matches test_guard.TokenFallback.test_a_line_too_tangled_to_analyse_is_refused_under_any_grant [ran] [tree ca7c48d13da8] (2026-10-29T07:13:20Z)
- (step 1) `python3 plugin/tests/run.py test_guard.TokenFallback.test_a_line_too_tangled_to_analyse_is_refused_under_any_grant` → ✗ exit 1 · Ran 1 tests in 6.3s (1 classes, 16 at a time; slowest: TokenFallback 5s) / FAILED (1 classes) [ran] [tree 228938707e7b] (2026-10-29T07:13:45Z)
- (step 1) `python3 plugin/tests/run.py test_approve_reads test_guard test_guard_diff test_guard_evasions test_guard_pipes` → exit 0 · Ran 300 tests in 8.3s (89 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 9e41949a8c38] (2026-10-29T07:16:28Z)
- (step 1) `python3 plugin/tests/run.py test_approve_reads test_guard test_guard_diff test_guard_evasions test_guard_pipes test_hooks` → exit 0 · Ran 504 tests in 58.3s (115 classes, 16 at a time; slowest: Stop 58s, NoTaskGate 45s, PreToolUse 40s) / OK [ran] [tree 59a2a5e09cc3] (2026-10-29T07:17:45Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 297 tests in 8.2s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 5ef27458d931] (2026-10-29T07:23:40Z)
- (audit intent) `one fm-reviewer pass (adversary, intent, maintainer); 5 findings fixed test-first: eval of computed text now unliftable, exact frozenset instead of substring, getattr fallback, hint names the way through, end-to-end cap tests; 504 guard and hook tests green` → grants still lift plain refusals; only the 4 never-read-to-the-end details are unliftable [tree 5ef27458d931] (2026-10-29T07:23:40Z)
- (audit adversary) `one fm-reviewer pass (adversary, intent, maintainer); 5 findings fixed test-first: eval of computed text now unliftable, exact frozenset instead of substring, getattr fallback, hint names the way through, end-to-end cap tests; 504 guard and hook tests green` → eval of printed text and a 6-deep nest stay refused under rm-outside; a path named to analyse stays liftable [tree 5ef27458d931] (2026-10-29T07:23:40Z)
- (audit edge) `one fm-reviewer pass (adversary, intent, maintainer); 5 findings fixed test-first: eval of computed text now unliftable, exact frozenset instead of substring, getattr fallback, hint names the way through, end-to-end cap tests; 504 guard and hook tests green` → non-string details never match (isinstance), fallback guard without unanalysed degrades to the old hint [tree 5ef27458d931] (2026-10-29T07:23:40Z)
- (audit operator) `one fm-reviewer pass (adversary, intent, maintainer); 5 findings fixed test-first: eval of computed text now unliftable, exact frozenset instead of substring, getattr fallback, hint names the way through, end-to-end cap tests; 504 guard and hook tests green` → each refusal names its way through (split the command, run the text itself); no fm ask offered [tree 5ef27458d931] (2026-10-29T07:23:40Z)
- (audit maintainer) `one fm-reviewer pass (adversary, intent, maintainer); 5 findings fixed test-first: eval of computed text now unliftable, exact frozenset instead of substring, getattr fallback, hint names the way through, end-to-end cap tests; 504 guard and hook tests green` → UNANALYSED holds the exact strings; tests assert real caps produce a member, so rewording fails loudly [tree 5ef27458d931] (2026-10-29T07:23:40Z)
## Log
- 2026-10-29T07:03:45Z created
- 2026-10-29T07:13:19Z planned from capture
- 2026-10-29T07:13:28Z focused
- 2026-10-29T07:21:08Z review: eval of computed text was still liftable; substring match fragile (path 'to analyse'). Fix: exact frozenset UNANALYSED of 4 self-contained details, getattr fallback in fmhooks, end-to-end tests for nesting cap + eval under grant
- 2026-10-29T07:24:30Z done
- 2026-10-29T07:24:32Z committed acf3807c (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1924 [PERFORMANCE M, done, 1 steps] Guard: repeated 'cd X; …; cd ..' in a ; line grows its folder sets exponentially (_moved/_ — lesson: Tails after a substitution wer…
- research T-1924-review: Verdict: changes needed.** One adversary finding is real and new. The relative-`cd` change lets a line pass that was refused before. I ran nothin…
- T-1849 [FEATURE M, done, 2 steps] 3D showpiece: the guard airlock, a scene of what the guard let through and held (from T-16 — lesson: A playbook trim can delete text a …
- decision 2026-10-21: T-1298: refusals for programs the guard couldn't read drop the --allow system route instead of keeping it
- similar finished tasks took 1–2 steps
## Lessons
- Match refusal kinds on exact strings, never substrings of text that can hold user paths
## Plan gaps
- failed first: step 1 Test: caps refused under an rm-outside grant (red); check() and the message treat a 'to analyse' re…
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
