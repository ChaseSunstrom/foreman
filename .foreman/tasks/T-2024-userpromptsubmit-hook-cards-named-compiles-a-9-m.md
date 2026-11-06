---
id: T-2024
type: PERFORMANCE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T18:07:40Z
updated: 2026-10-29T18:21:43Z
base: 10f148a9faa123deca26235d7f3611b7261fdd0e
base_tree: 4a8a3291ed993306bf0c6fb84ef91e71bd06e526
plan0_at: 2026-10-29T18:11:37Z
plan0_scope: []
---
# UserPromptSubmit hook: cards_named compiles a ~9 ms alternation of every card name each…
## Raw request
> PERF: UserPromptSubmit hook: cards_named compiles a ~9 ms alternation of every card name each turn — prefilter names by substring first; then attack the rest of its ~22 ms of regex compiles and the twice-loaded briefs
## Interpretation
The hook that runs on every user prompt spends ~22 ms compiling regexes, 9 ms of it on cards_named's alternation of every card name, plus module-level patterns in fmlib/fmplugins/fmbus; it also scans the ledger twice for the active task's last change. Make it faster without changing what it says.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a prompt naming one card still gets exactly that card; module-level patterns in fmlib/fmplugins/fmbus compile lazily — verify with `python3 plugin/tests/run.py test_cards_at_prompt test_library -k named`
## Non-goals
## Approach (options → choice → why)
Options: (1) prefilter card names by substring, compile only the candidates (same matches, chosen); (2) a word-index lookup instead of a regex (more code, subtle on multi-word names); (3) cache the compiled alternation across processes (not possible for re patterns). Module patterns: c.lazy (T-2020 pattern). last_change: per-process memo keyed on the ledger's size and mtime.
## Risks and rollback
## Execution prompt
## Steps
1. [x] baseline: time UserPromptSubmit on HEAD; red test: cards_named compiles only the names the text contains
2. [x] prefilter cards_named, lazy module patterns, memo last_change; measure
## Resume here
<!-- auto -->
- 2026-10-29T18:12:37Z step 2/2: prefilter cards_named, lazy module patterns, memo last_change; measure
- git: foreman/build; 5 uncommitted: plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmlib.py, plugin/lib/fmplugins.py, plugin/tests/test_cards_at_prompt.py
- touched since last checkpoint: plugin/tests/test_cards_at_prompt.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/edit24b.json, plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmlib.py, plugin/lib/fmplugins.py
## Docs impact
## Verification evidence
- (step 1) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/hook_t.py /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/base4/plugin/hooks/hook UserPromptSubmit:ups.json` → exit 0 · UserPromptSubmit min  115 ms, median  119 ms [ran] [tree 9ad593d302ff] (2026-10-29T18:12:18Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_chain test_nudges test_cards_at_prompt test_hooks test_core test_library test_plugins 2>&1 | grep -E "^FAIL|^ERROR|Error:|^OK|Ran" | head -12` → exit 0 · Ran 413 tests in 48.2s (70 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 39s, PreToolUse 33s) / OK [ran] [tree 5981924a35f4] (2026-10-29T18:16:59Z)
- (step 2) `python3 plugin/tests/run.py test_cards_at_prompt test_library test_ledger_chain test_nudges -k named -k last_change -k loads_briefs` → ✗ exit 1 · run.py: no test matches test_library with -k named -k last_change -k loads_briefs [ran] [tree 38eefc5a578f] (2026-10-29T18:17:37Z)
- (step 2) `python3 plugin/tests/run.py test_cards_at_prompt test_ledger_chain test_nudges` → exit 0 · Ran 53 tests in 4.0s (7 classes, 16 at a time; slowest: Chain 4s, Receipt 2s, Revisit 1s) / OK [ran] [tree 38eefc5a578f] (2026-10-29T18:17:45Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmlib.py, plugin/lib/fmplugins.py — commit it throu; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    32.9     150  [0] / SessionEnd                  24.8    26.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 38eefc5a578f] (2026-10-29T18:21:08Z)
- (ac 1) `python3 plugin/tests/run.py test_cards_at_prompt test_library -k named` → ✗ exit 1 · run.py: no test matches test_library with -k named [ran] [tree 38eefc5a578f] (2026-10-29T18:21:21Z)
- (ac 1) `python3 plugin/tests/run.py test_cards_at_prompt test_library -k named` → ✗ exit 1 · run.py: no test matches test_library with -k named [ran] [tree 38eefc5a578f] (2026-10-29T18:21:32Z)
## Log
- 2026-10-29T18:07:40Z created
- 2026-10-29T18:11:32Z planned: it has criteria and steps
- 2026-10-29T18:11:37Z focused
- 2026-10-29T18:21:43Z dropped: criterion 1 named a -k filter test_library has no test for; recreated with a check that runs
- 2026-10-29T18:21:43Z work at drop saved: 7f45032a5506 (restore: git -C ~/.claude/foreman restore --source=7f45032a5506 --worktree -- :/)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2020 [PERFORMANCE M, done, 2 steps] Hooks compile regexes on first use: importing fmcore, fmguard and fmhooks compiles none of their 191 module-level patterns — lesson…
- T-2022 [PERFORMANCE M, done, 2 steps] load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs — lesson: A stat-checked JSON ind…
- research T-1036-review: Verdict** — changes needed. Three correctness gaps in the injection path (displaced cards, wildcard deps, files outside the project). The rest is…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
