---
id: T-2985
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T14:27:30Z
updated: 2026-11-04T14:59:02Z
builder_model: sonnet
base: 44919471c433778cf4e5fb6b42a35a9092778c44
base_tree: 47970712112556221fe15ab61bf0fbd2e87e05fd
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T14:27:53Z
plan0_scope: []
lane_stop: merged 2026-11-04T14:54:01Z
verified: strong
---
# The card grower repairs a refused card once: send the writer its own card with admit's…
## Raw request
> The card grower repairs a refused card once: send the writer its own card with admit's reason (a chained command, an unknown first word, a vague step) and keep the corrected card when it passes; the 12B kept 2 of 12 with 10 refused for commands, mostly fixable (sqlfluff, a redirect)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a card refused by admit for a fixable reason (command, vague, traps, steps count) is sent back once with its reason and kept when the repair passes; a card still refused is dropped; repairs are counted in the grow line — verify with `python3 plugin/tests/run.py test_small_cards`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a fake writer whose first card chains a command and whose repair doesn't
2. [x] one repair call per refused batch in grow, reusing ms._ask and admit; the grow line counts repairs
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_small_cards test_left_out` → exit 0 · Ran 17 tests in 1.0s (4 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / OK [ran] [tree c0ab711f6224] [world 2f1906870a] (2026-11-04T14:28:25Z)
- (step 1) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 14 tests in 1.0s (3 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / OK [ran] [tree 91280612dddf] [world 2f1906870a] (2026-11-04T14:58:26Z)
- `python3 plugin/tests/run.py test_small_cards` → ✗ exit 1 · Ran 14 tests in 2.4s (3 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / FAILED (1 classes: test_small_cards.Grow) (start tree + this task's tests) [ran] [tree 91280612dddf] [world 2f1906870a] (2026-11-04T14:58:30Z)
- `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 14 tests in 1.0s (3 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / OK [ran] [tree 91280612dddf] [world 2f1906870a] (2026-11-04T14:58:30Z)
- (ac 1) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 14 tests in 1.0s (3 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / OK [ran] [tree 0b4e6b97fc4f] [world 2f1906870a] (2026-11-04T14:58:41Z)
- (audit edge) `branch diff read before merge (smallcards _repair_prompt, grow's one repair per refused batch; test_small_cards); prove red on the start tree, green now` → a repair that is still refused is dropped, never retried twice (tested); a repair reply with no card counts as a failed call; the repair prompt quotes the card as data [tree 0b4e6b97fc4f] (2026-11-04T14:58:41Z)
- (audit self) `branch diff read before merge (smallcards _repair_prompt, grow's one repair per refused batch; test_small_cards); prove red on the start tree, green now` → no findings [tree 0b4e6b97fc4f] (2026-11-04T14:58:41Z)
## Log
- 2026-11-04T14:27:30Z created
- 2026-11-04T14:27:43Z planned: it has criteria and steps
- 2026-11-04T14:27:43Z set approved=True
- 2026-11-04T14:27:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2985.builder.md
- 2026-11-04T14:27:52Z focused
- 2026-11-04T14:27:53Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T14:54:01Z merged worktree-agent-a635f96af896685be (2 file(s))
- 2026-11-04T14:58:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a635f96af896685be
- 2026-11-04T14:58:24Z focused
- 2026-11-04T14:59:00Z done
- 2026-11-04T14:59:02Z committed 84095a29 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2909 [FEATURE M, done, 5 steps] Small-model cards part 1: a store of cards written for small models (research/cards/cards.jsonl), a grid (kind of work x stack x stage …
- research T-2049-review: Changes needed. The lint logic is sound and the AC-named test looks right. One MEDIUM finding is on the card-admission path. I had no shell, so I…
- T-1923 [SECURITY M, done, 1 steps] Guard judges tree writes after a cd to a folder it can't name — lesson: bare is None whenever a command word is computed: branches gat…
- decision 2026-11-04: Moon growth runs both endpoint slots with reasoning off; reasoning on stays an A/B sample (32 rows) judged by the funnel
- similar past tasks were M: consider --tier M
## Lessons
- Telling a small model exactly which strict check its own card failed is cheaper than a new card: one repair call per refused batch
## Files touched
- plugin/tests/test_small_cards.py
- plugin/lib/sampo/smallcards.py
- CHANGELOG.md
