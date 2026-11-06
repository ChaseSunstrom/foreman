---
id: T-1664
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-22T20:59:06Z
updated: 2026-10-28T20:07:40Z
base: 992b28395bd29355048a9e892c3223eb9ac2d3c8
base_tree: 5412ab408634dfa1eda9cbd6535af705e2f6ec83
plan0_at: 2026-10-28T19:45:13Z
plan0_scope: []
verified: strong
---
# Backlog extras: good-first list, deferred swipe, learned priorities, spike rule, ticket planner
## Raw request
> Backlog extras: a good-first list, a swipe page, learned priorities, a spike rule, a pasted-ticket planner (from T-1548; waits: after the capture checks)
## Interpretation
Five backlog tools from T-1548's split, all reachable from Claude Code: a list of small ready items to start on, a way to sweep the deferred pile (revive, keep, drop), two-way 'which first?' choices that tilt the inbox order, a nudge to spike before an L feature, and a pasted ticket or error turned into one planned brief.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm inbox first lists ready S items with why; fm inbox swipe gives deferred items and --apply revives/drops; fm inbox pick gives close pairs, fm inbox prefer records a choice and rank_inbox learns from title words (bounded); an L FEATURE's first focus says spike first unless the brief has one; fm inbox ticket FILE|- makes one brief (type, title, criteria, repro step, scope from trace paths; redacted, defanged) — verify with `python3 plugin/tests/run.py test_backlog`
- [x] /foreman:backlog drives first, swipe, pick and ticket through AskUserQuestion like /foreman:looks — verify with `python3 plugin/tests/run.py test_backlog test_docs`
## Non-goals
## Approach (options → choice → why)
Options: A a new fm backlog verb; B fm inbox sources first/swipe/pick/prefer/ticket beside gh and spec; C an HTML swipe page served by fm settings serve; D fm queue --good-first plus fm intake --ticket. Chosen: B, where the backlog already lives (ticket mirrors spec FILE, reuses capture_once, LABEL_TYPES, _repro, defang, redact), with a /foreman:backlog command asking through AskUserQuestion like /foreman:looks. Learned priority: title-word weights from recorded choices, at most +-2 in rank_inbox's value, so it tilts ties and never beats urgency or type. Spike rule: a note on an L FEATURE's first focus, not a gate. Left out (captured): a TTY swipe loop, a served swipe page, Jira or Linear fetch.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests (test_backlog.py)
2. [x] fm inbox first, swipe, pick and prefer; the learned term in rank_inbox
3. [x] spike note on an L FEATURE's first focus; fm inbox ticket
4. [x] /foreman:backlog command; CHANGELOG, MASTER
## Resume here
<!-- auto -->
- 2026-10-28T19:59:46Z step 1/4: failing tests (test_backlog.py)
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmeco.py, plugin/tests/test_backlog.py, plugin/tests/test_cli.py, plugin/commands/backlog.md
- touched since last checkpoint: plugin/tests/test_cli.py, plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/tests/test_backlog.py
- failures met: assertionerror: '{gh,spec}' not found in 'usage: fm inbox [-h] [--json] [-p project] [--a…; ffmpeg-0
## Docs impact
MASTER.md backlog bullet + table row; CHANGELOG Unreleased; plugin/commands/backlog.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_backlog` → ✗ exit 1 · Ran 22 tests in 4.7s (4 classes, 16 at a time; slowest: Reverify 4s, Capture 3s, Extras 2s) / FAILED (1 classes) [ran] [tree d987cf4e940c] (2026-10-28T19:50:12Z)
- (step 2) `python3 plugin/tests/run.py test_backlog.Extras.test_first_lists_ready_small_items_with_why test_backlog.Extras.test_swipe_lists_deferred_and_apply_revives_drops_and_keeps_all_or_nothing test_backlog.Extras.test_pick_offers_close_pairs_and_prefer_tilts_the_order_within_a_bound` → exit 0 · Ran 3 tests in 2.7s (1 classes, 16 at a time; slowest: Extras 2s) / OK [ran] [tree 8cbf9b8bdac0] (2026-10-28T19:52:24Z)
- (step 3) `python3 plugin/tests/run.py test_backlog.Extras.test_ticket_makes_one_planned_brief_redacted_and_defanged test_backlog.Extras.test_an_l_feature_first_focus_says_spike_first_unless_the_brief_has_one` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Extras 1s) / OK [ran] [tree 8cbf9b8bdac0] (2026-10-28T19:52:26Z)
- (step 4) `python3 plugin/tests/run.py test_backlog test_plugin_parity 2>&1 | tail -3` → exit 0 · Ran 25 tests in 4.7s (5 classes, 16 at a time; slowest: Reverify 4s, Extras 4s, Capture 3s) / OK [ran] [tree aaae6c59d67a] (2026-10-28T19:53:02Z)
- (step 4) `python3 plugin/tests/run.py test_backlog test_docs test_plugin_parity` → exit 0 · Ran 99 tests in 11.7s (23 classes, 16 at a time; slowest: Fences 11s, Reverify 9s, Extras 7s) / OK [ran] [tree 5bee495afb6c] (2026-10-28T19:54:36Z)
- (audit intent) `reviewer read the brief and diff: all five extras built; ticket planner gaps fixed (title redacted+defanged, redact before the 4000 cut)` → pass after fixes [tree 2438c434ffb7] (2026-10-28T20:01:45Z)
- (audit adversary) `hostile ticket: ghp token and PEM key redacted in title and body, dot paths (.claude/.git/.env) never become scope, backticks turn to quotes, repro is a read-first step` → pass after fixes [tree 2438c434ffb7] (2026-10-28T20:01:46Z)
- (audit edge) `no-op prefer (no differing words) writes nothing and says so; keep keeps the defer reason shown; --limit honoured by first and pick` → pass after fixes [tree 2438c434ffb7] (2026-10-28T20:01:46Z)
- (audit operator) `every inbox flag a source does not read exits 1 naming the sources that do (T-1855 rule)` → pass [tree 2438c434ffb7] (2026-10-28T20:01:46Z)
- (audit maintainer) `unused test helper removed; --limit help names each default; prefer.json documented in MASTER` → pass [tree 2438c434ffb7] (2026-10-28T20:01:46Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 23 tests in 5.3s (4 classes, 16 at a time; slowest: Extras 5s, Reverify 5s, Capture 3s) / OK [ran] [tree 2438c434ffb7] (2026-10-28T20:06:14Z)
- (ac 2) `python3 plugin/tests/run.py test_backlog test_docs` → exit 0 · Ran 97 tests in 9.3s (22 classes, 16 at a time; slowest: Fences 9s, Extras 5s, Reverify 5s) / OK [ran] [tree 2438c434ffb7] (2026-10-28T20:06:14Z)
- (step 1) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 23 tests in 5.3s (4 classes, 16 at a time; slowest: Extras 5s, Reverify 5s, Capture 3s) / OK [ran] [tree 2438c434ffb7] (2026-10-28T20:06:14Z)
- (audit intent) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → all five extras built; ticket planner gaps fixed [tree 2438c434ffb7] (2026-10-28T20:06:14Z)
- (audit adversary) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → tokens/keys redacted in title and before the cut; dot paths never scope [tree 2438c434ffb7] (2026-10-28T20:06:14Z)
- (audit edge) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → no-op prefer writes nothing; keep keeps the defer reason; --limit read [tree 2438c434ffb7] (2026-10-28T20:06:14Z)
- (audit operator) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → unread inbox flags exit 1 naming their sources [tree 2438c434ffb7] (2026-10-28T20:06:14Z)
- (audit maintainer) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → unused helper gone; --limit help names defaults [tree 2438c434ffb7] (2026-10-28T20:06:14Z)
- (audit intent) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → all five extras built; ticket planner gaps fixed [tree 2cf379d31844] (2026-10-28T20:07:10Z)
- (audit adversary) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → tokens/keys redacted in title and before the cut; dot paths never scope [tree 2cf379d31844] (2026-10-28T20:07:10Z)
- (audit edge) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → no-op prefer writes nothing; keep keeps the defer reason; --limit read [tree 2cf379d31844] (2026-10-28T20:07:10Z)
- (audit operator) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → unread inbox flags exit 1 naming their sources [tree 2cf379d31844] (2026-10-28T20:07:10Z)
- (audit maintainer) `one fm-reviewer pass over the diff (intent lens required); its findings fixed test-first in test_review_fixes_…; fm check 4000 tests OK` → unused helper gone; --limit help names defaults [tree 2cf379d31844] (2026-10-28T20:07:10Z)
## Log
- 2026-10-22T20:59:06Z created
- 2026-10-28T19:45:01Z set tier=M, title=Backlog extras: good-first list, deferred swipe, learned priorities, spike rule, ticket planner
- 2026-10-28T19:45:03Z approach: A new fm backlog verb (more surface); B extend fm inbox's sources (gh, spec) with first/swipe/pick/prefer/ticket (chosen: where the backlog already lives, ticket mirrors spec FILE); C an HTML swipe page served by fm settings serve (needs write-back, worse CC parity); D spread over fm queue --good-first and fm intake --ticket (scattered). CC surface: a /foreman:backlog command using AskUserQuestion like /foreman:looks. Captured, not built: a TTY swipe loop, a served swipe page, Jira/Linear API fetch.
- 2026-10-28T19:45:13Z focused
- 2026-10-28T20:07:38Z done
- 2026-10-28T20:07:40Z committed 3e98fe17 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1548 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Backlog intelligence: cap new FEATURE captures against closed work, reje
- research mission-20261028-025205: Request: Recursive brainstorm/build rounds after the weekly reset: make Foreman insanely good, not just specific to usage; reason ahead…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- similar past tasks were L: consider --tier L
## Lessons
- a flag a sub-action doesn't read must refuse, not sit silently unread (T-1855 rule applies to every multi-action verb)
## Plan gaps
- failed first: step 1 failing tests (test_backlog.py)
## Files touched
- plugin/tests/test_backlog.py
- plugin/lib/fmcore.py
- plugin/lib/fmeco.py
- plugin/lib/fmcli.py
- plugin/commands/backlog.md
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_cli.py
