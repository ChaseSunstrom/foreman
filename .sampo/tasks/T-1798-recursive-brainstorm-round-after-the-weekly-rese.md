---
id: T-1798
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-27T22:34:00Z
updated: 2026-10-28T08:15:06Z
revisit: 2026-10-28T02:00
inferred_deps: [T-1797]
inferred_why: T-1797: measures per-reply context using fm cost added there
base: 5919745d4ff2ea773dcdd754f9e463b54bebf82c
base_tree: e804d2882be8bbcdb54b294047f7f2067f52281a
plan0_at: 2026-10-28T08:14:38Z
plan0_scope: []
verified: strong
---
# Recursive brainstorm round after the weekly reset (user: 'super recursive brainstorm impro
## Raw request
> Recursive brainstorm round after the weekly reset (user: 'super recursive brainstorm improvement'): first measure T-1796 with fm cost (context per reply should be under ~140k), then /foreman:brainstorm with a usage-efficiency lens (per-reply context, parallel sessions each driving, reviewer/builder spend) beside the usual lenses; build round, review, brainstorm on top, until dry
## Interpretation
Check that T-1796's 200k compact window brought per-reply context under ~140k (fm cost --sessions), then run a super brainstorm with a usage-efficiency lens (per-reply context, parallel sessions each driving, reviewer and builder spend) beside the usual lenses, past the 2026-10-27 ideas; capture the best grounded ideas as tasks, build them, review what shipped, brainstorm on top; repeat until a round adds little.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1796 measured: per-reply context of sessions since it is under 140k — verify with `fm cost --sessions --days 1`
- [x] a brainstorm with a usage-efficiency lens, past the 2026-10-27 ideas, saved with its ideas list — verify with `ls state/projects/foreman-4a056f/research/brainstorm-2026102[89]*/ideas.md`
- [x] its top usage-efficiency ideas captured as tasks and queued — verify with `fm queue`
## Non-goals
## Approach (options → choice → why)
Options: (A) fm ideas on Haiku, 15 lenses, rounds until dry, --seen the last ideas.md, then fm ideas' ranked list to tasks; (B) fm-recon agents per lens on Sonnet (grounded, costlier); (C) skip brainstorming and mine the 1160 unbuilt ideas from 2026-10-27. Choice: A with C folded in: --seen makes the run go past the last list, Haiku keeps it cheap (≈60 child calls), and the build round draws from both lists' top usage-efficiency ideas. B only if A's ideas come back ungrounded.
## Risks and rollback
## Execution prompt
## Steps
1. [x] measure T-1796 with fm cost --sessions (target under ~140k a reply)
2. [x] fm ideas: 15 lenses with usage efficiency, rounds until dry, --seen the 2026-10-27 ideas.md
3. [x] rank; capture the top grounded ideas as tasks; queue them for the build round
## Resume here
## Docs impact
none: research note and decision only
## Verification evidence
- (step 1) `fm cost --sessions --days 1` → exit 0 · Sessions, last 1 day(s), costliest first, main thread only (the context a turn re-reads is most of the cost): / 70f2d724-d84: 761 turns, 96k context per turn, ≈ 10.7M input-equivalent (cache read 67%, [ran] [tree e804d2882be8] (2026-10-28T08:14:39Z)
- (step 2) `ls state/projects/foreman-4a056f/research/brainstorm-2026102[89]*/ideas.md` → exit 0 · state/projects/foreman-4a056f/research/brainstorm-20261028-025248/ideas.md [ran] [tree e804d2882be8] (2026-10-28T08:15:02Z)
- (step 3) `fm queue` → exit 0 · 7. T-1824 FEATURE M [planned] — FEATURE: fm cost shows the retry tax per task: tokens spent on failed attempts (a step's g / 8. T-1825 FEATURE M [planned] — FEATURE: fm run (headless) skips a model ca [ran] [tree e804d2882be8] (2026-10-28T08:15:03Z)
- (ac 1) `fm cost --sessions --days 1` → exit 0 · Sessions, last 1 day(s), costliest first, main thread only (the context a turn re-reads is most of the cost): / 70f2d724-d84: 766 turns, 96k context per turn, ≈ 10.8M input-equivalent (cache read 67%, [ran] [tree e804d2882be8] (2026-10-28T08:15:04Z)
- (ac 2) `ls state/projects/foreman-4a056f/research/brainstorm-2026102[89]*/ideas.md` → exit 0 · state/projects/foreman-4a056f/research/brainstorm-20261028-025248/ideas.md [ran] [tree e804d2882be8] (2026-10-28T08:15:04Z)
- (ac 3) `fm queue` → exit 0 · 7. T-1824 FEATURE M [planned] — FEATURE: fm cost shows the retry tax per task: tokens spent on failed attempts (a step's g / 8. T-1825 FEATURE M [planned] — FEATURE: fm run (headless) skips a model ca [ran] [tree e804d2882be8] (2026-10-28T08:15:04Z)
- (audit intent) `self: measured with fm cost, 4-round brainstorm (626 ideas), 32 value-5 ideas grounded by two scouts, triage saved as research T-1798-triage` → per-reply context 96k (under 140k); usage-efficiency ideas T-1820, T-1824, T-1825 queued with the others [tree e804d2882be8] (2026-10-28T08:15:04Z)
- (audit maintainer) `self: measured with fm cost, 4-round brainstorm (626 ideas), 32 value-5 ideas grounded by two scouts, triage saved as research T-1798-triage` → cost at scale — the brainstorm is one-off; captured tasks are each sized M and grounded first [tree e804d2882be8] (2026-10-28T08:15:04Z)
## Log
- 2026-10-27T22:34:00Z created
- 2026-10-27T22:34:03Z deferred: weekly usage at 95%; resumes after the 02:00 reset (revisit 2026-10-28)
- 2026-10-28T00:53:10Z deferred: waits for the weekly usage reset (95% used) (revisit 2026-10-28T02:00)
- 2026-10-28T00:55:52Z steer (user, 2026-10-27): 'super super recursive brainstorm … builds on top of the finished product a few times … super -> super -> super, each improving from the last … don't cut yourself off with running out of usage'. PLAN, run after T-1800 and T-1799 (CI green first, baseline before building): (0) fm mission --request with the user's words; T-1796 measured with fm cost (context per reply < ~140k). (1) Round 0 = audit: every idea in research/brainstorm-*.md plus the 53 open follow-ups (11 captured, 29 deferred, 11 blocked, 2 active) marked built / partial / missing with file:line evidence (fm ideas marks it); done-but-not-built goes first. (2) Rounds 1..N, each on the shipped product of the last: fm ideas --rounds 4 --deepen --falsify --crossbreed --seen <every earlier catalogue> → scored slate → build test-first (Sonnet builders, worktrees) → one review of what shipped → merge to foreman/build → fm loop round --next with its yield → the next round brainstorms on top. Fold T-1797 into round 1. (3) Stop: a round adds fewer than 3 new grounded ideas (dry), or the pace guard trips. PACE GUARD (usage math): the week is 100%, other sessions need room, so the loop takes at most ~60% of the week and about 15% a day; before each round and each fan-out, fm cost --forecast: weekly projected-at-reset <= 85% and five_hour < 70%, else finish the current build, checkpoint, and wait for the window (Cron or ScheduleWakeup at the reset) instead of starting a new fan-out; never past 90% weekly. Every round's catalogue goes in research/brainstorm-recursive-rN-<date>.md.
- 2026-10-28T00:56:55Z steer (user, 2026-10-27): 'super super wild/niche/groundbreaking ideas, and thousands of them, all implemented … fast, secure, performant, no token burn, anything and everything'. ADD: lenses wild, niche, groundbreaking/10x, cross-domain steal, the opposite of the obvious, plus the defaults; --crossbreed and --falsify every round; ideas from cheap tool-less children (Haiku), so thousands of ideas cost little. Every idea is deduped against all earlier catalogues and scored. Building is the expensive part: measured 386 tasks closed in the 7 days to 2026-10-27, a week that burned all its usage, so thousands of builds take several weeks. Build in score order each day inside the pace guard, keep fm loop on so it carries on week after week, and never skip the tests to go faster. Each round also checks speed (bench_hooks), security (an adversary lens on every exec/auth/secrets diff) and tokens (fm cost: context per reply, tokens per task) and fixes anything that got worse before starting new ideas.
- 2026-10-28T00:58:27Z steer (user, 2026-10-27): 'everything done this week, not pushed out over 2 months'. REPLACES the 60%/8-week pacing: (1) the loop may use up to ~90% of the week (10% kept for the user's own sessions), spread ~13%/day so no day locks out; (2) cut cost per idea: batch related ideas into one task (fm batch: one gate run, one review per batch, not per idea), Haiku for idea generation and playbook drafts, Sonnet builders, Opus only to plan and judge, fm check --affected while iterating; (3) run around the clock: builders in parallel worktrees, wake at each 5-hour window reset (ScheduleWakeup/Cron; fm run headless if no session is open); (4) day-1 check: after the first ~5% of usage, measure ideas built per 1% and project the week; if it falls short, say so once with the number and build in score order so whatever is left is the lowest value; extra usage on the user's plan is the only lever beyond that, and only the user can choose it.
- 2026-10-28T01:06:36Z catalogue: 650 new distinct ideas over 4 rounds in state/projects/foreman-4a056f/research/brainstorm-20261027-200146 (ideas.md index); round 0 turns them into batched tasks
- 2026-10-28T07:48:36Z set status=planned
- 2026-10-28T08:14:37Z focused
- 2026-10-28T08:15:06Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1029 [RESEARCH L, done, 5 steps] Super recursive brainstorm: anything on the table to make Foreman super good; build, revie — lesson: Show the whole catalogue, not a s…
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- T-0071 [FEATURE L, done, 5 steps] Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve…
- decision 2026-10-20: The recursive brainstorm loop is dry after round 1: a two-lens probe past the 368 earlier ideas gave 51 titles, 2 of real value after grounding (rep…
## Why not caught
none: a planning task
## Lessons
- fm cost already counts cache busts and their cause: check what a lens calls new against the code before capturing it
