---
id: T-1064
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/tests/test_proxy.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T07:37:16Z
base: bf79bbb69e610f128531b923b02cb8e7d8733146
base_tree: 611d53cbb1714016b99e2b5d4a1d1bf15354cfa6
plan0_at: 2026-10-16T07:34:52Z
plan0_scope: [plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/tests/test_proxy.py]
verified: strong
---
# User proxy for asks: under standard autonomy an ask identical to one the user answered bef
## Raw request
> FEATURE: User proxy for asks: under standard autonomy an ask identical to one the user answered before is answered from that precedent, labelled as a proxy answer, gated by calibration (wild C5)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Under standard autonomy, an `fm decide --ask` identical to one the user answered in the ask digest is answered at once from that precedent. The answer is labelled "proxy answer" and a decision row is written. It is gated: a proxy is allowed only if enough precedents agree and the proxy's own track record is good. Present today: `_decide_ask` (`fmcli.py:2689`) queues asks with a taste default; it never uses past user answers. `_answer` (`fmcli.py:2763`) records user answers in `decisions.md` with why "the user's answer (ask digest)". Guard-category asks are never pre-answered (`fmcli.py:2693`); that stays.
## Assumptions (confidence)
## Acceptance criteria
- [x] after two user answers to the same ask, a third `fm decide --ask` returns `proxy: true` with that answer — verify with `python3 plugin/tests/run.py test_proxy`
- [x] two proxied answers overruled stop proxying; guard-named asks never proxy — verify with `python3 plugin/tests/run.py test_proxy`
## Non-goals
## Approach (options → choice → why)
(a) match on `decisions.md` rows; (b) a `precedents` ledger event; (c) fuzzy match. Choice (a) plus event: in `_answer`, add `c.log_event(p, "ask_answered", data={"q": norm(q), "a": answer})`. Add `fmideas.precedent(p, q)`, which returns the answer when at least 2 normalized-identical past asks have the same answer and none disagree. Gate on the proxy's record: log `proxy_answer`, and when the user later changes it (`_answer` on a proxied n), log `proxy_overruled`. Refuse a proxy when overruled/total is above 20% once at least 3 proxies exist, reusing the calibration style of `fmoutcomes.calibration`. Wire it into `_decide_ask` before the standing-autonomy queueing. Text: "Proxy answer (from N earlier answers): …".
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: drive `fm decide --ask` and `--answer N` through `self.fm_json`; cover single-precedent (no proxy), disagreeing precedents (no proxy), overruled gate, guard-named ask.
2. [x] Implement `precedent` and the gate in `fmideas.py`; update `_decide_ask` and `_answer` in `fmcli.py`.
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_proxy` → ✗ exit 1 · Ran 4 tests in 2.9s (1 classes, 16 at a time; slowest: Proxy 3s) / FAILED (1 classes) [ran] [tree b8e0ec73e3ce] (2026-10-16T07:14:03Z)
- (step 2) `python3 plugin/tests/run.py test_proxy` → ✗ exit 1 · Ran 4 tests in 3.0s (1 classes, 16 at a time; slowest: Proxy 3s) / FAILED (1 classes) [ran] [tree b8e0ec73e3ce] (2026-10-16T07:14:06Z)
- (step 2) `python3 plugin/tests/run.py test_proxy` → exit 0 · Ran 4 tests in 8.9s (1 classes, 16 at a time; slowest: Proxy 9s) / OK [ran] [tree b86a413e3fe0] (2026-10-16T07:15:25Z)
- (step 2) `python3 plugin/tests/run.py test_proxy test_guard` → exit 0 · Ran 117 tests in 20.9s (48 classes, 16 at a time; slowest: GuardAgainstBash 21s, Proxy 11s, Hook 5s) / OK [ran] [tree 7e7f3c2b5ad7] (2026-10-16T07:21:48Z)
- (step 1) `python3 plugin/tests/run.py test_proxy test_guard` → exit 0 · Ran 117 tests in 13.3s (48 classes, 16 at a time; slowest: GuardAgainstBash 13s, Proxy 8s, Hook 4s) / OK [ran] [tree 080f022d6d3e] (2026-10-16T07:35:10Z)
- (ac 1) `python3 plugin/tests/run.py test_proxy` → exit 0 · Ran 6 tests in 12.6s (1 classes, 16 at a time; slowest: Proxy 12s) / OK [ran] [tree 428f31cf0ee6] (2026-10-16T07:35:32Z)
- (ac 2) `python3 plugin/tests/run.py test_proxy` → exit 0 · Ran 6 tests in 12.6s (1 classes, 16 at a time; slowest: Proxy 12s) / OK [ran] [tree 428f31cf0ee6] (2026-10-16T07:35:32Z)
- (audit intent) `fm-reviewer (security + edge): --answer is self-answerable → guard user-only; options missing from the key → included; unbounded window → 180 days; empty key matched everything → never proxies; all fixed test-first on the builder's branch` → repeats of the user's own answers are proxied; nothing new is decided for them [tree 428f31cf0ee6] (2026-10-16T07:35:32Z)
- (audit adversary) `fm-reviewer (security + edge): --answer is self-answerable → guard user-only; options missing from the key → included; unbounded window → 180 days; empty key matched everything → never proxies; all fixed test-first on the builder's branch` → Claude can't seed answers (decide --answer is user-only, guard-tested) [tree 428f31cf0ee6] (2026-10-16T07:35:32Z)
- (audit edge) `fm-reviewer (security + edge): --answer is self-answerable → guard user-only; options missing from the key → included; unbounded window → 180 days; empty key matched everything → never proxies; all fixed test-first on the builder's branch` → empty key, changed options and old answers don't proxy [tree 428f31cf0ee6] (2026-10-16T07:35:32Z)
- (audit operator) `fm-reviewer (security + edge): --answer is self-answerable → guard user-only; options missing from the key → included; unbounded window → 180 days; empty key matched everything → never proxies; all fixed test-first on the builder's branch` → proxy answers are marked in the decision and listed in the digest [tree 428f31cf0ee6] (2026-10-16T07:35:32Z)
- (audit maintainer) `fm-reviewer (security + edge): --answer is self-answerable → guard user-only; options missing from the key → included; unbounded window → 180 days; empty key matched everything → never proxies; all fixed test-first on the builder's branch` → one key function, reuses ledger_events [tree 428f31cf0ee6] (2026-10-16T07:35:32Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:02:19Z set scope=['plugin/lib/fmideas.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_proxy.py']
- 2026-10-16T05:02:20Z set tier=M
- 2026-10-16T07:12:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1064.builder.md
- 2026-10-16T07:13:01Z focused
- 2026-10-16T07:34:48Z merged worktree-agent-a8ecd37872b3b305f (5 file(s))
- 2026-10-16T07:34:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8ecd37872b3b305f
- 2026-10-16T07:34:52Z focused
- 2026-10-16T07:35:18Z scope: CHANGELOG.md — release note
- 2026-10-16T07:37:15Z done
- 2026-10-16T07:37:16Z committed 4584fb0 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_ideas.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmideas.py, plugin/tests/test_proxy.py; re-ground the plan against them before editing
## Lessons
- Anything that answers for the user must be fed only by input Claude can't write
## Plan gaps
- failed first: step 1 Failing tests: drive `fm decide --ask` and `--answer N` through `self.fm_json`; cover single-preced…
- failed first: step 2 Implement `precedent` and the gate in `fmideas.py`; update `_decide_ask` and `_answer` in `fmcli.py…
## Files touched
- plugin/tests/test_proxy.py
- plugin/lib/fmideas.py
- plugin/lib/fmcli.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
- CHANGELOG.md
