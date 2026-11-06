---
id: T-2049
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T20:27:27Z
updated: 2026-10-30T00:43:16Z
base: 4c6b3dee82af39a40a8df083e7ed8bd444d5e65a
base_tree: 5cad1dc37ea1939ec6761aa625d7a4804b271411
plan0_at: 2026-10-30T00:23:34Z
plan0_scope: []
verified: strong
---
# Library cards: flag npx names not on a reviewed list; fix the two that don't exist and stylelint's invalid --rule
## Raw request
> _card_problems` cannot check that a Verify `npx` package or flag exists. A small allowlist or a "your script" lint would have caught the `axe-core-cli`, `scripts/*.mjs` and `stylelint --rule` cases. …
> (noticed by an agent; research T-2039-review)
## Interpretation
A card's Verify may run npx NAME, which downloads whatever package holds that name. Two shipped cards name packages that don't exist (electronegativity is @doyensec/electronegativity; bullmq-cli is 404 on npm), and design-systems.md runs stylelint with an invalid --rule. The lint should catch a new unknown name at the time it's written.
## Assumptions (confidence)
## Acceptance criteria
- [x] an unknown npx name in a card is a card problem naming npx-known.txt — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library`
- [x] every shipped card passes — verify with `fm lib check`
## Non-goals
## Approach (options → choice → why)
Options: (1) query the npm registry at lint time: network in a lint, slow and flaky, no. (2) a reviewed allowlist file, plugin/skills/library/npx-known.txt, one name per line; the lint flags a backticked npx [-y|--yes] [--package|-p] NAME that isn't on it, and the message names the file: chosen, offline, cheap, and a new name gets a deliberate review. (3) only flag names that look invented: no rule exists for that. Flags aren't checked (skip until a second invented flag ships). Names were checked against registry.npmjs.org on 2026-10-29; local bins (tsc, ng, cdk) count as known because npx runs a project's own bin first.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a card whose Verify runs an unknown npx name is flagged; --yes/--package forms parse
2. [x] npx-known.txt (reviewed names) + _card_problems check
3. [x] fix electron.md (@doyensec/electronegativity), background-jobs.md (no bullmq-cli), design-systems.md:15 stylelint --rule
4. [x] fm lib check over all cards
## Resume here
<!-- auto -->
- 2026-10-30T00:35:35Z steps 4/4 done
- git: foreman/build; 2 uncommitted: CHANGELOG.md, plugin/tests/test_library.py
- touched since last checkpoint: .claude/worktrees/agent-a96fd6d76f53844ed/plugin/tests/test_library.py, .claude/worktrees/agent-a96fd6d76f53844ed/plugin/skills/library/npx-known.txt, .claude/worktrees/agent-a96fd6d76f53844ed/plugin/skills/library/cards/web/electron.md, .claude/worktrees/agent-a96fd6d76f53844ed/plugin/skills/library/cards/design/background-jobs.md, .claude/worktrees/agent-a96fd6d76f53844ed/plugin/skills/library/cards/frontend/design-systems.md, .claude/worktrees/agent-a96fd6d76f53844ed/plugin/lib/fmlib.py, CHANGELOG.md, plugin/tests/test_library.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library` → exit 0 · Ran 45 tests in 6.7s (9 classes, 16 at a time; slowest: LibSources 6s, LibraryAdmit 2s, LibraryCards 1s) / OK [ran] [tree 5382f0fcb394] (2026-10-30T00:24:49Z)
- (step 4) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 5382f0fcb394] (2026-10-30T00:24:50Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_edit_cards test_lib_hostile test_library` → exit 0 · Ran 76 tests in 15.5s (17 classes, 16 at a time; slowest: ImportCards 14s, LibSources 10s, EditCards 10s) / OK [ran] [tree 5382f0fcb394] (2026-10-30T00:25:06Z)
- (step 2) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 5382f0fcb394] (2026-10-30T00:25:10Z)
- (step 3) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 5382f0fcb394] (2026-10-30T00:25:11Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library` → ✗ exit 1 · Ran 45 tests in 12.8s (9 classes, 16 at a time; slowest: LibSources 12s, LibraryAdmit 4s, LibrarySuggest 3s) / FAILED (1 classes) [ran] [tree d00b617459ee] (2026-10-30T00:32:37Z)
- (step 4) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree d00b617459ee] (2026-10-30T00:32:38Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library 2>&1 | grep -E "^(FAIL|ERROR|AssertionError| File.*test_library)" -A3 | head -25` → ✗ exit 1 · Ran 45 tests in 12.5s (9 classes, 16 at a time; slowest: LibSources 12s, LibraryAdmit 4s, LibrarySuggest 3s) / FAILED (1 classes) [ran] [tree d00b617459ee] (2026-10-30T00:32:56Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library` → exit 0 · Ran 45 tests in 12.8s (9 classes, 16 at a time; slowest: LibSources 12s, LibraryAdmit 5s, LibrarySuggest 4s) / OK [ran] [tree 8a32d73ecd91] (2026-10-30T00:33:23Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library` → exit 0 · Ran 45 tests in 6.6s (9 classes, 16 at a time; slowest: LibSources 6s, LibraryAdmit 2s, LibrarySearch 1s) / OK [ran] [tree 8024f5d2fd14] (2026-10-30T00:37:44Z)
- (ac 2) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 8024f5d2fd14] (2026-10-30T00:37:44Z)
- (audit intent) `one fm-reviewer pass over the diff; 1 medium (admit read /tmp/npx-known.txt) and 3 low findings, all fixed and tested` → whole-card scan kept (a card's Do line can run npx too); changelog reworded to say so [tree 8024f5d2fd14] (2026-10-30T00:37:44Z)
- (audit adversary) `one fm-reviewer pass over the diff; 1 medium (admit read /tmp/npx-known.txt) and 3 low findings, all fixed and tested` → admit lints in a temp dir; the list beside it is read only when the root folder is named cards, so /tmp/npx-known.txt is never read; tested [tree 8024f5d2fd14] (2026-10-30T00:37:44Z)
- (audit edge) `one fm-reviewer pass over the diff; 1 medium (admit read /tmp/npx-known.txt) and 3 low findings, all fixed and tested` → trailing ;|&\ stripped from names; a non-UTF-8 list falls back to the shipped one [tree 8024f5d2fd14] (2026-10-30T00:37:44Z)
- (audit operator) `one fm-reviewer pass over the diff; 1 medium (admit read /tmp/npx-known.txt) and 3 low findings, all fixed and tested` → fm lib check stays clean on 1219 cards; an unknown name says to add it to npx-known.txt [tree 8024f5d2fd14] (2026-10-30T00:37:44Z)
- (audit maintainer) `one fm-reviewer pass over the diff; 1 medium (admit read /tmp/npx-known.txt) and 3 low findings, all fixed and tested` → the list is read once per process (functools.cache); tests clear it [tree 8024f5d2fd14] (2026-10-30T00:37:44Z)
## Log
- 2026-10-29T20:27:27Z created
- 2026-10-29T20:27:27Z noticed by an agent (research T-2042-review): _card_problems` cannot check that a Verify `npx` package or flag exists. A small allowlist or a "your script" lint would have caught the `axe-core-cli`, `scripts/*.mjs` and `stylelint --rule` cases. …
- 2026-10-29T20:27:27Z noticed by an agent (research T-2043-review): _card_problems` cannot check that a Verify `npx` package or flag exists. A small allowlist or a "your script" lint would have caught the `axe-core-cli`, `scripts/*.mjs` and `stylelint --rule` cases. …
- 2026-10-29T20:27:27Z noticed by an agent (research T-2044-review): _card_problems` cannot check that a Verify `npx` package or flag exists. A small allowlist or a "your script" lint would have caught the `axe-core-cli`, `scripts/*.mjs` and `stylelint --rule` cases. …
- 2026-10-30T00:22:31Z planned from capture
- 2026-10-30T00:22:45Z criterion 1 verify: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_lib` → `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library`
- 2026-10-30T00:23:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2049.builder.md
- 2026-10-30T00:23:33Z focused
- 2026-10-30T00:31:44Z merged worktree-agent-a96fd6d76f53844ed (6 file(s))
- 2026-10-30T00:31:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a96fd6d76f53844ed
- 2026-10-30T00:31:49Z focused
- 2026-10-30T00:33:51Z scope: CHANGELOG.md and plugin/skills/library/npx-known.txt are this lint rule's own changelog line and data file
- 2026-10-30T00:38:00Z done
- 2026-10-30T00:38:02Z committed 9e762557 (3 files)
- 2026-10-30T00:38:23Z guard authorization added: publish
- 2026-10-30T00:43:16Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2044-review: Not checked:** I read about 25 cards in full and ran grep across the rest. I had no network and could not run any command, so package and flag cl…
- research T-2043-review: Not checked:** I read about 25 cards in full and ran grep across the rest. I had no network and could not run any command, so package and flag cl…
- research T-2042-review: Not checked:** I read about 25 cards in full and ran grep across the rest. I had no network and could not run any command, so package and flag cl…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
## Lessons
- A lookup beside a path the caller controls must say which paths qualify: a temp dir's parent is /tmp
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmlib.py
- plugin/skills/library/npx-known.txt
- plugin/skills/library/cards/web/electron.md
- plugin/skills/library/cards/design/background-jobs.md
- plugin/skills/library/cards/frontend/design-systems.md
- CHANGELOG.md
