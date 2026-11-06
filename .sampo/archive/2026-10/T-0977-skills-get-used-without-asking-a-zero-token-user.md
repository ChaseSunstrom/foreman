---
id: T-0977
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T22:20:26Z
updated: 2026-10-15T22:39:18Z
base: 138ec4b58c2732a7e5ef8ef39390dc2971b3a144
base_tree: abdc13b7d0b6f28aae85aa4cd3a2acbed8d405e7
verified: strong
---
# Skills get used without asking: a zero-token UserPromptSubmit note names the one Foreman s
## Raw request
> Skills get used without asking: a zero-token UserPromptSubmit note names the one Foreman skill or stack card that matches the request (trigger words and the map), once per task; fm doctor -v shows 7-day skill and card use (8 Skill calls in 24k tool calls this week)
## Interpretation
Skills and stack cards barely get used (8 Skill calls in 24k tool calls this week; no card injected before T-0980). Make them reach the model without being asked: when a request names a library or topic a card covers, the prompt hook names those cards (read on demand, so a few words of context), once per session per card; doctor -v counts the use.
## Assumptions (confidence)
## Acceptance criteria
- [x] A work prompt naming react and postgres gets one note naming those cards with the fm lib show line; the same cards aren't named again in that session; a prompt naming none, a common word that is also a card name ('make it work', 'go ahead') or a task notification gets none; matching reads a cached index — verify with `python3 plugin/tests/run.py -k CardsAtPrompt`
- [x] fm doctor -v's enforcement row also counts stack cards read and named at prompt time over 7 days — verify with `python3 plugin/tests/run.py -k CardsAtPrompt`
## Non-goals
## Approach (options → choice → why)
Options: whole-word card-name match on the prompt from a cached name index, common-word names skipped (chosen: zero tokens to match, precise, cheap per prompt); fm lib search ranking on every prompt (parses 1,078 cards, ~50 ms, fuzzier); inject the cards' text (token burn the user asked to avoid).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing CardsAtPrompt tests
2. [x] fmlib.cards_named with a cached index; the UserPromptSubmit note; doctor counts; docs
## Resume here
## Docs impact
MASTER, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k CardsAtPrompt` → ✗ exit 1 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: CardsAtPrompt 1s) / FAILED (1 classes) [ran] [tree deff37db499a] (2026-10-15T22:36:52Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_doctor test_library test_cards_at_prompt test_docs` → exit 0 · Ran 239 tests in 32.9s (51 classes, 16 at a time; slowest: Stop 33s, Command 26s, PreToolUse 18s) / OK [ran] [tree 755e60f36a28] (2026-10-15T22:39:11Z)
- (ac 1) `python3 plugin/tests/run.py -k CardsAtPrompt` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: CardsAtPrompt 1s) / OK [ran] [tree 755e60f36a28] (2026-10-15T22:39:13Z)
- (ac 2) `python3 plugin/tests/run.py -k CardsAtPrompt` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: CardsAtPrompt 1s) / OK [ran] [tree 755e60f36a28] (2026-10-15T22:39:13Z)
- (step 1) `python3 plugin/tests/run.py -k CardsAtPrompt` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: CardsAtPrompt 1s) / OK [ran] [tree 755e60f36a28] (2026-10-15T22:39:13Z)
- (audit intent) `self-review: whole-word match from a cached index, common-word names excluded, once per session per card; timed at ~30 ms cold` → named libraries and topics get their cards at prompt time without being asked, at no token cost until read [tree 755e60f36a28] (2026-10-15T22:39:13Z)
- (audit edge) `self-review: whole-word match from a cached index, common-word names excluded, once per session per card; timed at ~30 ms cold` → common words, notifications and repeats stay quiet; longest phrase wins; the index rebuilds only when the card count changes [tree 755e60f36a28] (2026-10-15T22:39:13Z)
- (audit operator) `self-review: whole-word match from a cached index, common-word names excluded, once per session per card; timed at ~30 ms cold` → doctor -v shows cards named and read, so use is measurable [tree 755e60f36a28] (2026-10-15T22:39:13Z)
## Log
- 2026-10-15T22:20:26Z created
- 2026-10-15T22:36:40Z focused
- 2026-10-15T22:39:15Z done
- 2026-10-15T22:39:18Z committed 14fba41 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0949 [FEATURE M, done, 4 steps] Enforce: the right stack card's pitfalls injected at edit time, and a compliance count — lesson: A ranking rule (framework before langu…
- T-0939 [FEATURE M, done, 3 steps] Pane shows skill use: skills invoked, stack cards read, and this repo's suggested cards — lesson: A mechanical sed over JSX props must …
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
## Lessons
- A library nobody reads needs a pointer at the moment of need, not a better index: name it when the request names its topic
## Plan gaps
- failed first: step 1 Failing CardsAtPrompt tests
## Files touched
- plugin/tests/test_cards_at_prompt.py
- plugin/lib/fmlib.py
- plugin/lib/fmhooks.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
- demo/live.cast
