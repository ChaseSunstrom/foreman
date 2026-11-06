---
id: T-1434
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T20:57:58Z
updated: 2026-10-21T22:52:06Z
base: e66d90397e3fe038d7097f423f79136753aa41ef
base_tree: 2fbc14f1d97940afd5eb3e8b000cb04fbed3c147
plan0_at: 2026-10-21T22:23:09Z
plan0_scope: []
verified: strong
---
# fm doctor's supply check reads the rest of what a plugin runs: hooks in skill and agent frontmatter, LSP servers, linked and large files, and a hooks module
## Raw request
> fm doctor supply: hooks declared in skill/agent/command frontmatter, .lsp.json servers and hooks inlined in a marketplace entry aren't read; the tree hash skips symlinks and files over 4 MB (could hash target or size); fmdoctor._frontmatter has no regular-file check (a FIFO could hang it); the foreman-ui mod's hooks/hooks.json reads as a hook event named 'modules' (T-1392 builder)
## Interpretation
T-1392's capability reader covers hooks.json, .mcp.json and bin/ scripts, but Claude Code also runs hooks declared in skill and agent frontmatter, starts LSP servers from .lsp.json, and loads a mod's TypeScript hooks module (foreman-ui's hooks.json is {modules: [...]}, misread today as a hook event). The tree hash skips symlinks and files over 4 MB, so changes there only show through capabilities. fmdoctor's own frontmatter reader would block on a FIFO.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fixture plugin update that adds a hooks: block to a SKILL.md or agent's frontmatter, an .lsp.json server, a symlinked or over-4 MB script, or a new hooks module entry is held naming it; foreman-ui's hooks.json reads as 'runs hooks module register.tsx', not a hook event named modules; a FIFO in a plugin folder never hangs fmdoctor's frontmatter reader — verify with `python3 plugin/tests/run.py test_supply_delta`
## Non-goals
## Approach (options → choice → why)
Options: (A) extend capabilities() with the three missing sources and make the tree hash cover links and large files by cheap stand-ins (chosen: closes the named gaps with the existing delta and accept flow); (B) hash every byte of large files (slow on big plugins; the doctor has a time budget); (C) document the gaps only (leaves known holes in a security check). Marketplace-inline hooks stay out of scope: they apply only at install time, where fm plugins find already shows needs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_supply_delta.py for each case
2. [x] fmplugins.capabilities: frontmatter hooks of skills/agents/commands (event names), .lsp.json server names with a spec digest, a 'modules' list in hooks.json as 'module X'; fmdoctor._tree_hash hashes a symlink's target path and a large file's size and mtime instead of leaving them out; fmdoctor._frontmatter reads regular files only
3. [x] fix the review (research T-1434-1417-review, T-1434 part) test-first: the hooks key matches quoted and spaced forms; a frontmatter with no closing --- in the read window, or one that mentions hooks but doesn't parse, records event '?'; column-0 comments don't end the hooks block; hook digests compare as sets, so a second component reusing a name is still held; read plugin.json's custom skills/agents/commands paths and nested command folders; glob.escape the root; non-string modules entries record '?'
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_supply_delta` → ✗ exit 1 · Ran 25 tests in 5.4s (2 classes, 16 at a time; slowest: SupplyDelta 5s, FindNeeds 1s) / FAILED (1 classes) [ran] [tree e6b521786472] (2026-10-21T22:27:12Z)
- (step 1) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 25 tests in 2.3s (2 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 1s) / OK [ran] [tree f022b6ac3d95] (2026-10-21T22:30:15Z)
- (step 2) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 25 tests in 2.1s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 1s) / OK [ran] [tree f022b6ac3d95] (2026-10-21T22:30:24Z)
- (step 1) `python3 plugin/tests/run.py test_supply_delta test_doctor test_plugins` → exit 0 · Ran 100 tests in 5.4s (24 classes, 16 at a time; slowest: Install 5s, Command 4s, ViewsRepair 3s) / OK [ran] [tree fdc6e3feec54] (2026-10-21T22:39:27Z)
- (step 2) `python3 plugin/tests/run.py test_supply_delta test_doctor test_plugins` → exit 0 · Ran 100 tests in 4.6s (24 classes, 16 at a time; slowest: Install 4s, Command 4s, ViewsRepair 3s) / OK [ran] [tree fdc6e3feec54] (2026-10-21T22:41:15Z)
- (step 3) `python3 plugin/tests/run.py test_supply_delta` → ✗ exit 1 · Ran 33 tests in 1.9s (2 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 1s) / FAILED (1 classes) [ran] [tree 64f6600455e4] (2026-10-21T22:47:31Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | grep -E "^(FAIL|ERROR):|Error|\?|Ran|OK|FAILED" | head` → exit 0 · Ran 34 tests in 3.5s (2 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 1s) / OK [ran] [tree 4752c916c654] (2026-10-21T22:49:11Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | grep -E "^(FAIL|ERROR):|Error:|Ran|OK|FAILED|^ : " | head` → ✗ exit 1 · Ran 35 tests in 3.8s (2 classes, 16 at a time; slowest: SupplyDelta 3s, FindNeeds 1s) / FAILED (1 classes) [ran] [tree 039794d80948] (2026-10-21T22:49:45Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | grep -E "^(FAIL|ERROR):|Error:|Ran|OK|FAILED|^ : " | head` → exit 0 · Ran 35 tests in 2.2s (2 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 1s) / OK [ran] [tree 4a89eadf3d8a] (2026-10-21T22:49:55Z)
- (step 3) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 35 tests in 2.0s (2 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 1s) / OK [ran] [tree 6b1374025188] (2026-10-21T22:50:14Z)
- (step 3) `python3 plugin/tests/run.py test_supply_delta test_doctor test_plugins` → exit 0 · Ran 110 tests in 5.0s (24 classes, 16 at a time; slowest: Install 5s, Command 5s, ViewsRepair 4s) / OK [ran] [tree 4cca2bdb78be] (2026-10-21T22:51:48Z)
- (audit adversary) `fm-reviewer` → 4 HIGH/MEDIUM ways to read hooks as 'no hooks' (quoted key, frontmatter past 256 KB, column-0 comment, shared name digest) plus custom paths, glob characters and non-string modules — all fixed failing-first (test_supply_delta 35 tests); the rule now: unreadable for sure means event '?' [tree 22a92920fda3] (2026-10-21T22:51:59Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 35 tests in 1.9s (2 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 1s) / OK [ran] [tree 22a92920fda3] (2026-10-21T22:52:02Z)
- (audit intent) `fm-reviewer (research T-1434-1417-review): 7 findings fixed failing-first in step 3; real machine re-checked: supply PASS, Foreman's own plugin and mods read without unknowns (test)` → frontmatter hooks, LSP servers, a hooks module, symlink retargets and large-file changes are held naming them (test_supply_delta) [tree 22a92920fda3] (2026-10-21T22:52:02Z)
- (audit edge) `fm-reviewer (research T-1434-1417-review): 7 findings fixed failing-first in step 3; real machine re-checked: supply PASS, Foreman's own plugin and mods read without unknowns (test)` → a description containing 'hooks:' gives a '?' accepted once (safe failure); an unreadable file costs only a WARN via the tree hash (captured) [tree 22a92920fda3] (2026-10-21T22:52:02Z)
## Log
- 2026-10-21T20:57:58Z created
- 2026-10-21T22:22:51Z planned from capture
- 2026-10-21T22:22:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1434.builder.md
- 2026-10-21T22:23:08Z focused
- 2026-10-21T22:32:20Z merged worktree-agent-a6ca217630e49a35e (3 file(s))
- 2026-10-21T22:32:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6ca217630e49a35e
- 2026-10-21T22:44:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1434.builder.md
- 2026-10-21T22:45:10Z focused
- 2026-10-21T22:51:29Z merged worktree-agent-ad0319b3015aa31d7 (3 file(s))
- 2026-10-21T22:51:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad0319b3015aa31d7
- 2026-10-21T22:51:41Z focused
- 2026-10-21T22:52:03Z affected tests waived: UI mod JS tests don't read fmplugins or fmdoctor output; Python suites linked ran green
- 2026-10-21T22:52:06Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1392-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** The FAIL only fires for a narrow set of u…
- T-1392 [SECURITY M, done, 3 steps] A plugin update that adds a hook event, MCP server or script is held with that exact delta until fm doctor --accept-supply; fm plugins…
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- the similar finished task took 3 steps
## Why not caught
the first build tested well-formed YAML only; the reviewer's adversary lens tried quoting, padding and comments
## Lessons
- A security parser must fail closed: when it can't read a thing for sure, hold it as unknown rather than reading it as empty
## Plan gaps
- added late: fix the review (research T-1434-1417-review, T-1434 part) test-first: the hooks key matches quoted and spaced forms; a …
- failed first: step 1 failing tests in plugin/tests/test_supply_delta.py for each case
- failed first: step 3 fix the review (research T-1434-1417-review, T-1434 part) test-first: the hooks key matches quoted …
## Files touched
- plugin/tests/test_supply_delta.py
- plugin/lib/fmplugins.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
