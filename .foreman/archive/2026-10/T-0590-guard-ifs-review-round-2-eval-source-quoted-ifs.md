---
id: T-0590
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:13:02Z
updated: 2026-10-09T15:15:25Z
base: 2f5a0d4c6667f45ddfe207acfacbca87fe77f13e
base_tree: 11554eeb68c75e30f4b621233d425cdc56cc04a3
verified: strong
---
# Guard: IFS review round 2 — eval/source/quoted IFS sets, # after a rewritten IFS, quoted spans, read across a newline
## Raw request
> Guard: IFS review round 2 — eval/source/quoted IFS sets, # after a rewritten IFS, quoted spans, read across a newline
## Interpretation
Security review of T-0585 (six findings): an IFS set inside quoted eval/bash -c text or a sourced file beside a plain IFS use was missed (the name check ran on quote-masked text); the plain rewrite reached into quoted text a nested shell reads, and made a literal # after it a comment; IFS=… scoping to read spanned a newline.
## Assumptions (confidence)
## Acceptance criteria
- [x] the review-2 IFS rows are refused or read right and the volt arithmetic line passes — verify with `python3 plugin/tests/run.py -k IfsReview2`
## Non-goals
## Approach (options → choice → why)
Options: (a) never rewrite IFS, refuse every plain use — the fuzzer's class-1 rows would all be refusals with no reading, acceptable but loses real findings; (b) keep the rewrite but read raw text (quotes and heredocs included) for any IFS name when a plain use or eval/source is on the line, rewrite only unquoted spans (quoted spans are read by their own nested check), escape a following #, one-line read scoping. Choice: (b): closed where bash can set IFS, unchanged for data.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: IfsReview2 rows
2. [x] _ifs_unreadable reads raw text beside a plain IFS use or eval/source; rewrite only unquoted spans, escaping a # after; read scoping on one line; arithmetic computed names only at an assignment
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k IfsReview2` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: IfsReview2 0s) / FAILED (1 classes) [ran] [tree 86d856e7d868] (2026-10-09T15:13:15Z)
- (step 2) `python3 plugin/tests/run.py -k IfsReview2` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: IfsReview2 0s) / OK [ran] [tree bd1aafa9ae44] (2026-10-09T15:14:44Z)
- (ac 1) `python3 plugin/tests/run.py -k IfsReview2` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: IfsReview2 0s) / OK [ran] [tree 519a7b59c105] (2026-10-09T15:15:24Z)
- (audit intent) `self: every review-2 form has a row (eval/source/quoted IFS beside a plain use, nested bash -c, # after the rewrite on one line and across a newline, read across a newline, arithmetic false positive, wrapper shells); suites green; 30-day replay over 5000 real commands: 0 newly blocked, 0 newly allowed` → all six review findings refused or read right [tree 519a7b59c105] (2026-10-09T15:15:24Z)
- (audit adversary) `self: every review-2 form has a row (eval/source/quoted IFS beside a plain use, nested bash -c, # after the rewrite on one line and across a newline, read across a newline, arithmetic false positive, wrapper shells); suites green; 30-day replay over 5000 real commands: 0 newly blocked, 0 newly allowed` → plain IFS beside eval/source refuses outright; raw (unmasked) text is searched whenever bash could run it; quoted spans are no longer rewritten, so a nested shell reads its own original text [tree 519a7b59c105] (2026-10-09T15:15:24Z)
- (audit edge) `self: every review-2 form has a row (eval/source/quoted IFS beside a plain use, nested bash -c, # after the rewrite on one line and across a newline, read across a newline, arithmetic false positive, wrapper shells); suites green; 30-day replay over 5000 real commands: 0 newly blocked, 0 newly allowed` → grep for IFS= text with no plain use still passes; the volt arithmetic line passes; a # after the rewrite stays literal [tree 519a7b59c105] (2026-10-09T15:15:24Z)
## Log
- 2026-10-09T15:13:02Z created
- 2026-10-09T15:13:09Z focused
- 2026-10-09T15:14:40Z scope: + wrapper-launched shells fed a heredoc (review of T-0589: env/exec/timeout/nohup)
- 2026-10-09T15:14:44Z confirmed: _name already strips env/exec/timeout/nohup wrappers, so the review's wrapper rows pass with no code change
- 2026-10-09T15:15:25Z done
- 2026-10-09T15:15:25Z committed b81b35f (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0411-review: Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the co…
- research T-0384-review: Changes needed.** I found four concrete bypasses by reading the code. I could not run bash or the tests, because I only had read tools. For each …
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
## Lessons
- a text rewrite before parsing must not change lexing: rewrite only unquoted spans and keep the next character's meaning (a # after a new space becomes a comment)
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- CHANGELOG.md
