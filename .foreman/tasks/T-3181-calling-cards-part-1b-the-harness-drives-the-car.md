---
id: T-3181
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T08:37:54Z
updated: 2026-11-06T03:47:04Z
builder_model: haiku
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T20:57:44Z
plan0_scope: []
recoveries: [uncommitted@2026-11-06T03:46:39Z]
builder: 2026-11-06T03:46:42Z
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a58c52b8f814ca4ca
lane_branch: worktree-agent-a58c52b8f814ca4ca
---
# Calling cards part 1b: the harness drives the cards, not the model: before the first turn Sampo runs the read cards a task needs (failing frame, outline, callers) and puts their facts in the prompt; a failure signature picks a fix card Sampo applies with the model filling only its open slot; and done is refused while verify is red with no edit (T-3157, after the T-3160 pilot)
## Raw request
> Calling cards part 1b: the harness drives the cards, not the model: before the first turn Sampo runs the read cards a task needs (failing frame, outline, callers) and puts their facts in the prompt; a failure signature picks a fix card Sampo applies with the model filling only its open slot; and done is refused while verify is red with no edit (T-3157, after the T-3160 pilot)
## Interpretation
Reading 1 (chosen): the T-3160 pilot showed the 27B rarely calls a card (1 of 10) and often stops early (1/10 passes either way); so Sampo, not the model, decides when a card runs: read cards from the plan's targets and the failing test, fix cards from the failure signature, the model answering one narrow structured question per card. Reading 2: better card descriptions so the model calls them; rejected: the pilot's runs mostly never reached a choice.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Before Smith's first turn on a task with a failing check, Sampo runs the failing-frame and outline cards on the files the frame names and puts their facts in the prompt; a failure whose signature matches a fix card is applied by Sampo with the model filling only the card's open slot under a JSON schema — verify with `python3 plugin/tests/run.py test_smith_cards`
- [ ] research/callcards/slice.md gains a paired 10-scenario pilot of harness-driven cards against plain fm code on the same local model; 'proven' only when cards win by the sign test over 40 pairs, else 'not proven' with what failed — verify with `test -s research/callcards/slice.md`
## Non-goals
## Approach (options → choice → why)
1) Use what exists: T-3160's runner, cards and bench (merged first), Smith's plan step and turn loop, and T-3180's refusal of early done; likely outcome: facts in the prompt and applied fixes without the model choosing. fails if: the plan's targets are wrong (then read cards on the failing test's frame only). 2) Do less: only the early-done refusal (T-3180); fails if: the model still can't find the code. 3) A bigger model per step; fails if: it gives up on the small-model goal. Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: read cards run before turn 1; a matched fix card is applied with one model slot
2. [x] the harness-driven card step in Smith
3. [ ] the paired pilot, then 40 pairs if it shows a gain  <- CURRENT
## Resume here
<!-- auto -->
- 2026-11-05T21:04:07Z step 1/3: failing tests: read cards run before turn 1; a matched fix card is applied with one model slot
- git: worktree-agent-a615cb8d3c1e381e4; 4 uncommitted: plugin/cards/py-none-guard/card.json, plugin/lib/sampo/callcards.py, plugin/lib/sampo/smith.py, plugin/tests/test_smith_cards.py
- touched since last checkpoint: plugin/cards/py-none-guard/card.json, plugin/lib/sampo/smith.py, plugin/lib/sampo/callcards.py, plugin/tests/test_smith_cards.py
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_smith_cards 2>&1 | tail -60` → ✗ exit 1 · Ran 12 tests in 16.6s (8 jobs, 16 at a time; slowest: Harness 15s, Cards.test_a_native_card_call_changes_the_file_and_the_model_reads_its_diff 8s, Cards.test_the_json_action_path_calls_a_read_card 7s) [ran] [tree 670d4a50435a] [world 2f1906870a] (2026-11-05T21:02:03Z)
- (step 1) `python3 plugin/tests/run.py test_smith_cards` → ✗ exit 1 · Ran 12 tests in 3.4s (12 jobs, 16 at a time; slowest: Cards.test_a_native_card_call_changes_the_file_and_the_model_reads_its_diff 3s, Cards.test_the_json_action_path_calls_a_read_card 2s, Cards.test_a [ran] [tree 670d4a50435a] [world 2f1906870a] (2026-11-05T21:02:09Z)
- (ac 1) `python3 plugin/tests/run.py test_smith_cards 2>&1 | tail -80` → ✗ exit 1 · Ran 73 tests in 4.1s (12 jobs, 16 at a time; slowest: Cards.test_a_native_card_call_changes_the_file_and_the_model_reads_its_diff 3s, Cards.test_the_json_action_path_calls_a_read_card 3s, Cards.test_a [ran] [tree 410b4f5c9ec0] [world 2f1906870a] (2026-11-05T21:03:48Z)
- (step 2) `python3 plugin/tests/run.py test_smith_cards` → exit 0 · Ran 12 tests in 4.2s (12 jobs, 16 at a time; slowest: Harness.test_a_matched_fix_card_is_applied_and_the_model_fills_one_schema_slot 4s, Cards.test_a_native_card_call_changes_the_file_and_the_model_re [ran] [tree e6830635125d] [world 2f1906870a] (2026-11-05T21:05:46Z)
- (step 1) `nice python3 plugin/tests/run.py test_smith_cards` → exit 0 · Ran 12 tests in 10.1s (12 jobs, 16 at a time; slowest: Cards.test_a_native_card_call_changes_the_file_and_the_model_reads_its_diff 9s, Harness.test_a_matched_fix_card_is_applied_and_the_model_fills_on [ran] [tree 020488b5f35e] [world 2f1906870a] (2026-11-05T23:59:33Z)
- (step 2) `nice python3 plugin/tests/run.py test_callcards` → exit 0 · Ran 51 tests in 11.5s (9 jobs, 16 at a time; slowest: Apply 10s, Confinement 10s, Calls 8s) / OK [ran] [tree 020488b5f35e] [world 2f1906870a] (2026-11-05T23:59:47Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_brainstorm_skill test_budget test_callcards test_clean_helpers test_cli test_code_close_scaffold test_code_hardening test_code_worker test_cognition test_core test_docs test_doctor test_ecosystem test_find test_goal test_hooks test_ideas test_ideation test_kalevala test_knowledge test_lake test_learning2 test_left_out test_loop test_mcp test_models test_moons_scale test_night test_outcomes test_outside test_page test_panic test_portability test_proof test_recall test_reliability_tools test_rename_scan test_research test_research_rigor test_roles test_safety test_scout test_second test_site test_site_sections test_smith_cards test_sync test_tidy test_trust test_ui test_verbs_nopipe test_verifier && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2172 tests in 262.7s (723 jobs, 16 at a time; slowest: Recall 91s, TaskLifecycle 82s, Survival 79s) / FAILED (1 classes: test_ui.UiView) [ran] [tree d1bc55d37085] [world 2f1906870a] (2026-11-06T00:04:14Z)
- (step 2) `nice python3 plugin/tests/run.py test_ui` → exit 0 · Ran 58 tests in 9.7s (35 jobs, 16 at a time; slowest: UiView.test_today_done_counts_tasks_closed_today 8s, UiView.test_unproven_count_and_top_kind_ride_in_the_view_model 7s, UiView.test_closed_tasks_a [ran] [tree b9665f71c866] [world 2f1906870a] (2026-11-06T00:06:38Z)
## Log
- 2026-11-05T08:37:54Z created
- 2026-11-05T08:37:56Z blocked: after T-3160's slice merges (review running) and T-3180 (early done refused)
- 2026-11-05T17:52:08Z unblocked
- 2026-11-05T20:57:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3181.builder.md
- 2026-11-05T20:57:43Z focused
- 2026-11-05T20:57:44Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T23:57:05Z focused
- 2026-11-06T03:46:39Z builder stopped: lane ~/.claude/foreman/.claude/worktrees/agent-a615cb8d3c1e381e4 removed, work kept on worktree-agent-a615cb8d3c1e381e4 — recovery 1 of 2: process ended with work uncommitted
- 2026-11-06T03:46:42Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3181.builder.md
- 2026-11-06T03:47:04Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3160 [FEATURE M, done, 6 steps] Calling cards part 1, the thin slice: a card runner (template and py generators, checkers) confined to the target worktree with no netw…
- T-3180 [FIX S, done, 2 steps] Smith refuses done while the plan's verify is red and no edit was made: the model gets the failing check back and keeps going; early-done s…
- T-2936 [FEATURE M, done, 5 steps] Small-model plan scaffold: for a local profile Smith asks the plan one field at a time… — lesson: A small model answers a one-word ques…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
