---
id: T-1244
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T21:06:16Z
updated: 2026-10-20T20:59:31Z
group: theme applied before first paint
lane_branch: worktree-agent-aba90c2714cbe183f
base: 4d9c6f529cc1544eb70f0cf2b43a44422bca4e0c
base_tree: 6fa0db589d6cd9de7de2c966d56566afe86be58a
plan0_at: 2026-10-20T20:55:27Z
plan0_scope: []
verified: strong
---
# The landing page applies the stored theme in its head, as the feature pages do, so a stored light choice on a dark OS doesn't flash dark
## Raw request
> site.js` and `style.css` apply the stored theme only after the page loads (the script sits at the end of body), so a stored "light" choice on a dark OS flashes dark first
> (noticed by an agent; research T-1220-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] every page the site build writes (the landing page and each feature page) sets the stored fm-theme on <html> from an inline script inside <head>, before <body> starts; a test builds the site and checks each page — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test over every built page's head
2. [x] Add the inline theme script to site/index.html's head (the feature pages already have it, site/build.py:188); one shared snippet if it's cheap
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- `python3 plugin/tests/run.py test_docs` → ✗ exit 1 · Ran 46 tests in 4.0s (12 classes, 16 at a time; slowest: TaskLifecycle 3s, TaskDocsDrift 1s, DocsDrift 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree e50a93e2ee3e] (2026-10-20T20:57:15Z)
- `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 46 tests in 4.8s (12 classes, 16 at a time; slowest: TaskLifecycle 4s, TaskDocsDrift 1s, DocsDrift 1s) / OK [ran] [tree e50a93e2ee3e] (2026-10-20T20:57:15Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 46 tests in 4.2s (12 classes, 16 at a time; slowest: TaskLifecycle 4s, TaskDocsDrift 1s, DocsDrift 1s) / OK [ran] [tree cf5e5fbaad4b] (2026-10-20T20:57:29Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 46 tests in 4.5s (12 classes, 16 at a time; slowest: TaskLifecycle 4s, TaskDocsDrift 1s, DocsDrift 1s) / OK [ran] [tree cf5e5fbaad4b] (2026-10-20T20:57:35Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 46 tests in 4.2s (12 classes, 16 at a time; slowest: TaskLifecycle 4s, TaskDocsDrift 1s, DocsDrift 1s) / OK [ran] [tree cf5e5fbaad4b] (2026-10-20T20:57:40Z)
- (audit intent) `self review of a two-part diff (an inline head script copied from site/build.py:188, a test over every built page); proved red on the start tree, green now` → every built page, the landing page included, sets data-theme from localStorage in <head> before <body> [tree cf5e5fbaad4b] (2026-10-20T20:57:40Z)
- (audit adversary) `self review of a two-part diff (an inline head script copied from site/build.py:188, a test over every built page); proved red on the start tree, green now` → the script reads one localStorage key inside try/catch and sets one attribute; nothing from the page or URL is used [tree cf5e5fbaad4b] (2026-10-20T20:57:40Z)
- (audit edge) `self review of a two-part diff (an inline head script copied from site/build.py:188, a test over every built page); proved red on the start tree, green now` → no stored theme leaves the attribute unset, so the OS preference applies as before; site.js still handles the toggle [tree cf5e5fbaad4b] (2026-10-20T20:57:40Z)
- (audit operator) `self review of a two-part diff (an inline head script copied from site/build.py:188, a test over every built page); proved red on the start tree, green now` → no build change; the static landing page carries the same line the feature pages get from the template [tree cf5e5fbaad4b] (2026-10-20T20:57:40Z)
- (audit maintainer) `self review of a two-part diff (an inline head script copied from site/build.py:188, a test over every built page); proved red on the start tree, green now` → the snippet exists twice (index.html and build.py); sharing it would mean templating the static landing page, not worth it for one line [tree cf5e5fbaad4b] (2026-10-20T20:57:40Z)
- (audit self) `self review of a two-part diff (an inline head script copied from site/build.py:188, a test over every built page); proved red on the start tree, green now` → no findings [tree cf5e5fbaad4b] (2026-10-20T20:57:40Z)
## Log
- 2026-10-16T21:06:16Z created
- 2026-10-20T20:53:34Z planned from capture
- 2026-10-20T20:55:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1244.builder.md
- 2026-10-20T20:55:27Z focused
- 2026-10-20T20:56:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aba90c2714cbe183f (branch worktree-agent-aba90c2714cbe183f kept: not merged)
- 2026-10-20T20:56:43Z focused
- 2026-10-20T20:56:44Z criterion 1 verify: `python3 plugin/tests/run.py test_site` → `python3 plugin/tests/run.py test_docs`
- 2026-10-20T20:56:51Z merged worktree-agent-aba90c2714cbe183f (2 file(s))
- 2026-10-20T20:57:05Z focused
- 2026-10-20T20:59:31Z done
- 2026-10-20T20:59:31Z committed f82a0818 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1220-review: Changes needed. Nothing is critical. Three MEDIUM defects are worth fixing before the next publish. I read the code and the data files and did no…
- T-1246 [CLEAN S, done, 1 steps] Site: prose figures computed from stats.json, and the saved theme applied before first paint
- T-1220 [FEATURE L, done, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history — lesson: A stdlib site g…
- decision 2026-10-20: T-1276 trims no fm verb: measured right, fm-only command output is 0.9% of what entered the context over three days (the 3.5% counted test runs chai…
- similar finished tasks took 1–3 steps
## Lessons
- A theme stored in localStorage must be applied by a blocking script in <head>; a script at the end of <body> paints the default first
## Files touched
- plugin/tests/test_docs.py
- site/index.html
- CHANGELOG.md
