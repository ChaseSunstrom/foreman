---
id: T-3170
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T06:58:05Z
updated: 2026-11-05T13:26:46Z
builder_model: haiku
base: 76bebce4399ddda463c4886bdd479974804b049c
base_tree: 308b40164580b941d7c0b0d100930a3901f031f6
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T09:56:19Z
plan0_scope: []
builder_returned: 2026-11-05T10:07:38Z
lane_stop: merged 2026-11-05T13:23:50Z
verified: strong
unproven: [meaning, ui-unshot]
---
# The live page's 'At work: N builders' and the network view's agents count only builders still working (not ones returned and waiting on a merge, nor merged lanes), with waiting lanes shown apart
## Raw request
> The live page's 'At work: 15 builders' and the network view's agent column count every lane, including ones whose builder returned and only waits on a merge; 3 builders were running. Count running builders (not builder_returned, not merged) and show waiting lanes apart
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the live snapshot's builder count excludes lanes marked builder_returned or merged (lane_stop merged) and reports them as waiting; the page shows 'N at work · M waiting to merge' — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test then the count
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 86 tests in 206.9s (11 classes, 16 at a time; slowest: Page 206s, Serve 18s, Act 16s) / OK [ran] [tree 14a50f151705] [world 2f1906870a] (2026-11-05T10:03:02Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_guard test_instruments test_left_out test_library test_live test_live_page test_models test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [12.82s] [ran] [tree 6e0f3eac64a2] [world 2f1906870a] (2026-11-05T10:07:26Z)
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 87 tests in 21.0s (60 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 21s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree b4b94d978ad8] [world 2f1906870a] (2026-11-05T13:24:24Z)
- `python3 plugin/tests/run.py test_live` → ✗ exit 1 · Ran 87 tests in 21.9s (34 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 19s, Page.test_the_network_view_draws_three_columns_and_pulses_ (start tree + this task's tests) [ran] [tree b4b94d978ad8] [world 2f1906870a] (2026-11-05T13:25:10Z)
- `python3 plugin/tests/run.py test_live` → exit 0 · Ran 87 tests in 23.0s (76 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 23s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree b4b94d978ad8] [world 2f1906870a] (2026-11-05T13:25:10Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 87 tests in 22.6s (60 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 22s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree 923130124f63] [world 2f1906870a] (2026-11-05T13:25:50Z)
- (audit edge) `re-ran test_live + test_live_page on main after the merge; proved red→green on test_live` → a lane marked builder_returned or merged counts as waiting, not at work; a lane with no marks counts at work as before [tree 923130124f63] (2026-11-05T13:25:50Z)
- (audit self) `re-ran test_live + test_live_page on main after the merge; proved red→green on test_live` → no findings [tree 923130124f63] (2026-11-05T13:25:50Z)
## Log
- 2026-11-05T06:58:05Z created
- 2026-11-05T09:55:54Z planned from capture
- 2026-11-05T09:55:55Z set approved=True
- 2026-11-05T09:56:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3170.builder.md
- 2026-11-05T09:56:19Z focused
- 2026-11-05T09:56:19Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T13:23:50Z merged worktree-agent-abe12f809a2f6706a (5 file(s))
- 2026-11-05T13:23:54Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abe12f809a2f6706a
- 2026-11-05T13:24:02Z focused
- 2026-11-05T13:26:44Z done
- 2026-11-05T13:26:46Z committed ee83a569 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3034 [FEATURE M, done, 3 steps] Can you have a graph/neural net like visualization mode for the different… — lesson: Check git log --grep ID before briefing a builder:…
- T-3147 [FIX S, done, 2 steps] A returned or merged builder lane is never called STALLED: untracked leftovers, the T-3145 return mark and any earlier lane_merge event all…
- T-3135 [FIX S, done, 2 steps] The builder cap counts builders still working, not finished lanes waiting on a merge; unmerged finished lanes get their own larger cap, so …
- decision 2026-10-31: [reverses: a later Mission's lane waits only for earlier-Mission lanes launched before it] Mission-order merging, revised: lanes that are ready merg…
## Files touched
- plugin/tests/test_live.py
- plugin/lib/sampo/live.py
- plugin/web/live/live.js
- plugin/tests/fixtures/live/snap-5.json
- plugin/web/live/live.css
- CHANGELOG.md
