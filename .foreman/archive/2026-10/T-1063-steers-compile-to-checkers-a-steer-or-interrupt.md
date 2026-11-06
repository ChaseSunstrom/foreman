---
id: T-1063
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/tests/test_steer_compile.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T07:12:41Z
base: 6075e73f7c2674ae3a7d63dd0337019cc2e6e67c
base_tree: 5303f3accf330b1e3f468d9ea85caed6800f423c
verified: strong
---
# Steers compile to checkers: a steer or interrupt is typed (scope, style, safety, wrong app
## Raw request
> FEATURE: Steers compile to checkers: a steer or interrupt is typed (scope, style, safety, wrong approach) and one that recurs is compiled into a guard pattern, gate or lint the next session can't skip (wild C4, joins T-1042)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Steers and interrupts get a type: scope, style, safety or wrong approach. A type that recurs is compiled into an enforced check. A repeated "no" steer becomes a block or warn rule (`fm rule add`) with its type as `--why`. A recurring interrupt (`escape` events) becomes a plan-time note or a gate. Already present: vetoes (`fmcore.py:2112`), `proposals()` from repeated steers (`fmideas.py:234`), `fm taste adopt` (`fmideas.py:305`), and `STANDING_STEER` (`fmcore.py:2094`). T-1042 (planned in the state ledger, not built) adds `correction_clusters` with a ready `fm rule add` line. Not covered: typing, and compiling to a pattern rather than a veto.
## Assumptions (confidence)
## Acceptance criteria
- [x] three "no/never" steers about force push give a proposal typed "safety"; `fm taste compile 1` adds a rule that blocks `git push --force` — verify with `python3 plugin/tests/run.py test_steer_compile`
- [x] after compile the proposal disappears from `fm taste` — verify with `python3 plugin/tests/run.py test_steer_compile`
## Non-goals
## Approach (options → choice → why)
(a) build only on T-1042's output; (b) classify in `fmideas.py` and compile in `fm taste compile`; (c) an LLM classifier. Choice (b): keyword classifier, no model. Add `classify(text)` in `fmideas.py` (safety: force/delete/secret/push; scope: only/also/outside/just; style: format/name/comment/lint; else wrong-approach). Add `type` to each proposal. `fm taste compile N` writes a rule via `c.add_rule` with the pattern from `_key_words`. A style steer is a path rule on `--on path`; a safety steer is a block on bash. Log `steer_compiled`. T-1042 should merge first; the builder re-uses its `correction_clusters`.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: log note events "steer: ..." with `c.log_event`; assert the type of each of four fixtures, the pattern and `action`, that a declined or covered proposal doesn't compile, and that the `rules.json` entry is valid via `c.rules(p)`.
2. [x] Add `classify` and the pattern builder in `fmideas.py`; add the `compile` action to the `taste` parser and `cmd_taste`.
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_steer_compile` → ✗ exit 1 · Ran 4 tests in 3.6s (1 classes, 16 at a time; slowest: SteerCompile 3s) / FAILED (1 classes) [ran] [tree 577e7e66fd6b] (2026-10-16T07:00:06Z)
- (step 2) `python3 plugin/tests/run.py test_steer_compile` → exit 0 · Ran 4 tests in 2.2s (1 classes, 16 at a time; slowest: SteerCompile 2s) / OK [ran] [tree 2f71a89d3f18] (2026-10-16T07:01:06Z)
- (step 2) `python3 plugin/tests/run.py test_steer_compile test_guard` → exit 0 · Ran 119 tests in 39.6s (48 classes, 16 at a time; slowest: GuardAgainstBash 38s, Hook 10s, SteerCompile 9s) / OK [ran] [tree acc1512af371] (2026-10-16T07:08:54Z)
- (ac 1) `python3 plugin/tests/run.py test_steer_compile` → exit 0 · Ran 8 tests in 3.0s (1 classes, 16 at a time; slowest: SteerCompile 3s) / OK [ran] [tree a1f9b5644c52] (2026-10-16T07:11:57Z)
- (ac 2) `python3 plugin/tests/run.py test_steer_compile` → exit 0 · Ran 8 tests in 3.0s (1 classes, 16 at a time; slowest: SteerCompile 3s) / OK [ran] [tree a1f9b5644c52] (2026-10-16T07:11:57Z)
- `python3 plugin/tests/run.py test_steer_compile test_guard test_taste` → exit 0 · Ran 129 tests in 10.3s (51 classes, 16 at a time; slowest: GuardAgainstBash 10s, CorrectionClusters 6s, Hook 4s) / OK [ran] [tree a1f9b5644c52] (2026-10-16T07:11:57Z)
- (audit intent) `review: one fm-reviewer pass (combined with T-1061); 1 HIGH (agent-made block rules) and 4 more fixed test-first: warn-only for the agent, --block user-only in USER_ONLY_FM, anchored two-word patterns, style rules on bash, whole-word typing on shape words, exact-shape suppression` → a steer the user keeps repeating becomes a check, not another reminder [tree a1f9b5644c52] (2026-10-16T07:11:57Z)
- (audit adversary) `review: one fm-reviewer pass (combined with T-1061); 1 HIGH (agent-made block rules) and 4 more fixed test-first: warn-only for the agent, --block user-only in USER_ONLY_FM, anchored two-word patterns, style rules on bash, whole-word typing on shape words, exact-shape suppression` → the agent can only add warn rules; a block (which only the user can remove) needs the user's own command; --block abbreviations are caught [tree a1f9b5644c52] (2026-10-16T07:11:57Z)
- (audit edge) `review: one fm-reviewer pass (combined with T-1061); 1 HIGH (agent-made block rules) and 4 more fixed test-first: warn-only for the agent, --block user-only in USER_ONLY_FM, anchored two-word patterns, style rules on bash, whole-word typing on shape words, exact-shape suppression` → one-word shapes refused; prose in commit messages and pushd don't match a push rule [tree a1f9b5644c52] (2026-10-16T07:11:57Z)
- (audit operator) `review: one fm-reviewer pass (combined with T-1061); 1 HIGH (agent-made block rules) and 4 more fixed test-first: warn-only for the agent, --block user-only in USER_ONLY_FM, anchored two-word patterns, style rules on bash, whole-word typing on shape words, exact-shape suppression` → output names the rule number and that removing it is the user's [tree a1f9b5644c52] (2026-10-16T07:11:57Z)
- (audit maintainer) `review: one fm-reviewer pass (combined with T-1061); 1 HIGH (agent-made block rules) and 4 more fixed test-first: warn-only for the agent, --block user-only in USER_ONLY_FM, anchored two-word patterns, style rules on bash, whole-word typing on shape words, exact-shape suppression` → classify/compile_rule/proposals in fmideas; command-word anchors in one small table [tree a1f9b5644c52] (2026-10-16T07:11:57Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:02:15Z set scope=['plugin/lib/fmideas.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_steer_compile.py']
- 2026-10-16T05:02:16Z set tier=M
- 2026-10-16T06:59:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1063.builder.md
- 2026-10-16T06:59:22Z focused
- 2026-10-16T07:11:27Z merged worktree-agent-ab76647c09630fa8a (5 file(s))
- 2026-10-16T07:11:33Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab76647c09630fa8a
- 2026-10-16T07:11:33Z focused
- 2026-10-16T07:11:43Z scope: CHANGELOG.md — release note; fmguard.py and test_guard.py (the user-only --block entry) came with the merge
- 2026-10-16T07:12:39Z done
- 2026-10-16T07:12:41Z committed 23ee9a3 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_ideas.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmideas.py, plugin/tests/test_steer_compile.py; re-ground the plan against them before editing
## Lessons
- Never let the agent create a restriction only the user can lift; give it the warn, leave the block to the user
## Plan gaps
- failed first: step 1 Failing tests: log note events "steer: ..." with `c.log_event`; assert the type of each of four fix…
## Files touched
- plugin/tests/test_steer_compile.py
- plugin/lib/fmcli.py
- plugin/lib/fmideas.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
