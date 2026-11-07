---
id: T-2022
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T17:37:00Z
updated: 2026-10-29T18:01:53Z
base: 23bbf7357af7b5d89940ef1aa1c1137e71da29f2
base_tree: 9334b345704ec6afb1c805aa5dd5094e694d84af
plan0_at: 2026-10-29T17:45:24Z
plan0_scope: []
verified: strong
---
# load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs
## Raw request
> PERF: load_briefs costs ~90 ms per hook on 1199 briefs: frontmatter parse by partition not regex, no _orig dict copy per Brief (render compares against the raw line), no memo copy in one-shot processes
## Interpretation
Every hook and fm command loads all 1199 briefs (state_dict: ~31 ms of a Notification hook; active_brief_fast opens all of them for PreToolUse: ~12 ms). 1149 are done or dropped and never change. Read those from a validated index instead.
## Assumptions (confidence)
## Acceptance criteria
- [x] a closed brief older than 2 s loads from the index without opening its file, equal to a full parse (meta, title, render), and an edit re-parses it — verify with `python3 plugin/tests/run.py test_core -k brief_index`
- [x] state_dict and active_brief_fast get faster on the 1199-brief copy (ld_t.py before/after) — verify with `python3 plugin/tests/run.py test_core test_hooks test_cli`
## Non-goals
## Approach (options → choice → why)
Index file briefs-index.json in the project dir: {v:1, e:{basename:[ino, mtime_ns, size, meta, preamble]}} for tasks/ briefs older than 2 s. load_briefs stats each path; a key match yields a stub Brief (meta+preamble, body parsed lazily on first render/sections). active_brief_fast skips opening indexed non-active briefs. Bad index → ignored; written atomically only when entries change. Alternatives: pickle cache (refused: never pickle-load from state), sqlite (heavier), archiving closed briefs (most are <14 days old, no gain).
## Risks and rollback
A stale entry would show old meta: entries are keyed by inode+mtime_ns+size and only for files older than 2 s. A corrupt or foreign index is ignored (full parse). A stub's body loads on first use; a file changed in between gets the new body (same race the old code had). Rollback: git revert; deleting briefs-index.json is always safe.
## Execution prompt
## Steps
1. [x] test: index hit skips the file, edit/corrupt index/new file fall back (red)
2. [x] index in load_briefs and active_brief_fast; lazy body for stubs; render compares to raw lines; measure
## Resume here
<!-- auto -->
- 2026-10-29T17:53:01Z step 2/2: index in load_briefs and active_brief_fast; lazy body for stubs; render compares to raw lines; measure
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmcore.py, plugin/tests/test_core.py
- touched since last checkpoint: plugin/tests/test_core.py, plugin/lib/fmcore.py, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/exp/plugin/lib/fmcore.py
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core -k brief_index` → ✗ exit 1 · Ran 5 tests in 1.9s (1 classes, 16 at a time; slowest: BriefIndex 2s) / FAILED (1 classes) [ran] [tree ca64b488e76b] (2026-10-29T17:47:33Z)
- (step 1) `python3 plugin/tests/run.py test_core -k brief_index` → exit 0 · Ran 5 tests in 2.0s (1 classes, 16 at a time; slowest: BriefIndex 2s) / OK [ran] [tree 74d7b4bddd90] (2026-10-29T17:50:51Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.1    34.1     150  [0] / SessionEnd                  27.1    28.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree 74d7b4bddd90] (2026-10-29T17:54:25Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.5    33.7     150  [0] / SessionEnd                  27.1    28.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree 12d8c446769c] (2026-10-29T17:58:31Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k brief_index` → exit 0 · Ran 5 tests in 1.9s (1 classes, 16 at a time; slowest: BriefIndex 2s) / OK [ran] [tree 12d8c446769c] (2026-10-29T17:59:28Z)
- (ac 2) `python3 plugin/tests/run.py test_core test_hooks test_cli` → exit 0 · Ran 429 tests in 36.6s (86 classes, 16 at a time; slowest: Stop 36s, NoTaskGate 29s, PreToolUse 24s) / OK [ran] [tree 12d8c446769c] (2026-10-29T17:59:28Z)
- (audit intent) `self-review: diff re-read; stubs carry meta+preamble only and read their file lazily for fm lines or sections; render compares against the file's own lines; index rewritten only when its entries change; 4231 tests and bench green` → hooks stop opening ~1150 closed briefs; Notification 87 -> 51 ms measured on the 1199-brief copy [tree 12d8c446769c] (2026-10-29T17:59:28Z)
- (audit edge) `self-review: diff re-read; stubs carry meta+preamble only and read their file lazily for fm lines or sections; render compares against the file's own lines; index rewritten only when its entries change; 4231 tests and bench green` → stub body read lazily; a file moved before its body is read raises OSError (tidy reads only meta after moving); corrupt or malformed index ignored; briefs written under 2 s ago are not indexed; same-tick rewrite covered by inode+mtime_ns+size [tree 12d8c446769c] (2026-10-29T17:59:28Z)
- (audit adversary) `self-review: diff re-read; stubs carry meta+preamble only and read their file lazily for fm lines or sections; render compares against the file's own lines; index rewritten only when its entries change; 4231 tests and bench green` → the index is a cache in Foreman's own state folder, JSON only (never pickle), every entry stat-checked and shape-checked before use; a forged entry can only change what a closed brief's meta reads as, which writing the brief file itself already allows [tree 12d8c446769c] (2026-10-29T17:59:28Z)
## Log
- 2026-10-29T17:37:00Z created
- 2026-10-29T17:40:55Z planned from capture
- 2026-10-29T17:41:06Z approaches: (1) JSON index in the project dir of closed briefs' meta+preamble, each entry checked by (inode, mtime_ns, size) on a stat, body read only when used — chosen: ~1150 opens and parses become one json load, wrong entries are impossible without a same-key rewrite (2 s rule as the memo); (2) partition-based frontmatter parse + bytes read — ~25% of parse, kept as fallback idea; (3) archive closed briefs sooner — changes what fm task show finds; (4) a status-only index for active_brief_fast — helps PreToolUse only. Pickle rejected (never load a pickle from a state dir).
- 2026-10-29T17:45:24Z focused
- 2026-10-29T17:59:32Z done
- 2026-10-29T17:59:33Z committed d8dabdee (3 files)
- 2026-10-29T17:59:39Z guard authorization added: publish
- 2026-10-29T18:01:53Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- research T-1434-1417-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** T-1438 approve. T-1434 changes needed. T-1417 change…
- research T-1879-review: Verdict:** changes needed (two small gaps against the acceptance criterion). I read the diff and the surrounding code but did not run `plugin/tes…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
## Measurements
load_briefs cold 31.6 -> 7.8 ms; state_dict 36.4 -> 12.8 ms; Notification hook 87 -> 51 ms; PreToolUse 45 -> 41 ms; warm load_briefs 6.6 -> 6.8 ms (unchanged)
## Lessons
- A stat-checked JSON index of closed records beats parsing them; prefer a cheap stub over copying a memoized object
## Plan gaps
- failed first: step 1 test: index hit skips the file, edit/corrupt index/new file fall back (red)
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- CHANGELOG.md
