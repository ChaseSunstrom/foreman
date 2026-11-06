---
id: T-1031
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, README.md, CHANGELOG.md, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json]
depends_on: []
source: user
created: 2026-10-16T02:25:06Z
updated: 2026-10-16T02:46:56Z
base: 1a0d99629f5d580b818623dd55f7d7d7be5fd4f4
base_tree: 9ea07aab91d77b26547a9ede2ad862dd809eddcc
verified: strong
---
# Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for
## Raw request
> Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for tool rows and replies, better diffs, and no plain rows left (ReportFindings/code review, other tools render plainly)
## Interpretation
Every row in the chat reads like a pane section: a mark, a bold label in the row's colour, its subject, a rule fading out in that colour, muted facts on the right, and the body under it without a box. Your prompts, replies, commands, edits, agents and every other tool (review findings, skills, artifacts, MCP calls …) get one, none left in the engine's plain style. Diffs show a line of context, separate hunks, and highlight the changed words in a changed line.
## Assumptions (confidence)
## Acceptance criteria
- [x] Prompt, reply, shell, edit, agent, generic tool and ReportFindings rows draw a section header with a fading rule and no border — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
- [x] Edit diffs show context lines, hunk breaks and a highlight on the changed words of a changed line — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Options: (a) keep the rounded boxes and recolour them: still boxes, not the pane's look; (b) a shared section header (mark, bold label, subject, fading Raster rule, muted meta) for every chat row, bodies indented under it; (c) text rules in one colour: no fade. Choice (b) on the terminal with (c) as the off-terminal twin, the pane's own rule(). Diffs: changedLines grows context and hunk breaks; paired -/+ lines get a common prefix/suffix split so only the changed middle is washed. Generic finished tools get a section with their result's first lines; ReportFindings lists each finding with severity and outcome. Errors still draw the engine's.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: section header on each row kind; diff context, hunks, word highlight; generic tool and ReportFindings rows
2. [x] kit: diffRows (context, hunks, word spans); rows: section header helper; restyle shell, edit, agent, running tool, prompt, reply, turn line
3. [x] Generic finished-tool row and the ReportFindings row; ToolResult blanks under them
4. [x] Live look in the harness; README, CHANGELOG, foreman-ui 0.14.0
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 1 test across 1 file. [0.19s] [ran] [tree f31e9500006f] (2026-10-16T02:31:42Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 104 tests across 1 file. [8.78s] [ran] [tree ea3730a7f54d] (2026-10-16T02:35:15Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 104 tests across 1 file. [8.66s] [ran] [tree ea3730a7f54d] (2026-10-16T02:35:34Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 104 tests across 1 file. [8.78s] [ran] [tree ea3730a7f54d] (2026-10-16T02:35:44Z)
- (step 4) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 104 tests across 1 file. [8.59s] [ran] [tree 3d85acf5fc25] (2026-10-16T02:40:55Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 104 tests across 1 file. [8.72s] [ran] [tree 039605847f31] (2026-10-16T02:46:55Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 104 tests across 1 file. [8.72s] [ran] [tree 039605847f31] (2026-10-16T02:46:55Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); all findings fixed, plus a line-joining bug the new MCP test caught; live look in the 200x55 harness (chat2.png, chat3.png)` → prompt, reply, shell, edit, skill and review rows seen live as pane-style sections with fading rules and spacing; diff washed only 'hello'→'hi there' [tree 039605847f31] (2026-10-16T02:46:55Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); all findings fixed, plus a line-joining bug the new MCP test caught; live look in the 200x55 harness (chat2.png, chat3.png)` → long or empty results keep the engine's expandable block; images too; prototype-key and null findings render; a spent diff budget shows no stray context [tree 039605847f31] (2026-10-16T02:46:55Z)
## Log
- 2026-10-16T02:25:06Z created
- 2026-10-16T02:29:47Z set scope=['mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'README.md', 'CHANGELOG.md', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']
- 2026-10-16T02:29:47Z focused
- 2026-10-16T02:46:55Z done
- 2026-10-16T02:46:56Z committed 587c941 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-0179 [FEATURE M, done, 3 steps] Each reply is a panel: a round-bordered box per message, the closing report accented — lesson: Check a layout change in the live render…
- T-1002 [FEATURE M, done, 3 steps] Pane readability: zones with dividers, breathing room between sections, aligned label/picture/value rows, fewer facts per line; still f…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Lessons
- clean() drops newlines: split a tool's text into lines before cleaning it, or every multi-line result reads as one line.
## Plan gaps
- failed first: step 1 Failing tests: section header on each row kind; diff context, hunks, word highlight; generic tool a…
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/rows.tsx
- mods/foreman-ui/hooks/register.tsx
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
