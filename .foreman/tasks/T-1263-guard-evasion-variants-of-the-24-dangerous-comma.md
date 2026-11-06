---
id: T-1263
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/tests/fixtures/gen_evasions.py, plugin/tests/fixtures/guard_evasions.jsonl, plugin/tests/fixtures/guard_gaps.jsonl, plugin/tests/test_guard_evasions.py, plugin/lib/fmguard.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-20T14:01:27Z
updated: 2026-10-22T17:10:26Z
group: guard evasion and dangerous-flag coverage
base: b912b1f2994f2204e40fcd06e919eedd9bd554da
base_tree: eb1b93ad9907976755b33afd210374fe75ccebbd
plan0_at: 2026-10-22T16:37:07Z
plan0_scope: [plugin/tests/fixtures/gen_evasions.py, plugin/tests/fixtures/guard_evasions.jsonl, plugin/tests/fixtures/guard_gaps.jsonl, plugin/tests/test_guard_evasions.py, plugin/lib/fmguard.py, CHANGELOG.md]
verified: strong
---
# Guard evasion corpus for the 24 dangerous commands, and an audit of a cloned repo's .claude config
## Raw request
> Guard: evasion variants of the 24 dangerous commands as a corpus; audit a freshly cloned repo's own .claude config before trusting it (brainstorm-20261020 C9)
## Interpretation
site/bench_safety.py runs 24 dangerous commands through fmguard.check (all refused); their evasion variants (quote splitting, \\ escapes, variable or array indirection, eval/base64, env -S, alias/function, IFS tricks, a script file, here-strings) aren't checked anywhere, so a regression or a gap shows only when it's hit. Separately, a freshly cloned repo's own .claude/settings.json (hooks, permissions, MCP servers) starts running the first time Claude Code opens it, and Foreman never shows what it would run.
## Assumptions (confidence)
## Acceptance criteria
- [x] every generated variant is in the corpus or the gap list, the guard holds every corpus label (block and allow), and every listed gap is still a gap — verify with `cd plugin/tests && python3 -m unittest test_guard_evasions`
## Non-goals
## Approach (options → choice → why)
Corpus only (the cloned-config audit is its own task). A checked-in generator script (plugin/tests/fixtures/gen_evasions.py) writes plugin/tests/fixtures/guard_evasions.jsonl: for each of bench_safety's 24 dangerous commands a fixed set of transforms (quote splitting, backslash escapes, $'..' quoting, variable and array indirection, env -S, a function or alias, a changed field separator, here-string, a script file written then run, eval of a literal, base64 into sh), labelled block; and for each of its 25 everyday commands the same quoting transforms, labelled allow (the false-positive side). Undecidable forms (computed eval, base64 into a shell) are block because the guard refuses what it can't read. The test holds the guard to every label; a variant the guard gets wrong goes to guard_gaps.jsonl with its reason and a captured task, and the test asserts each gap is still a gap (so a fix has to move it into the corpus); no label is ever weakened. The generator's output is committed; the test fails if regenerating changes it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] generate the variants into the corpus
2. [x] fix or capture each variant the guard misses (test-first)
3. [x] cloned-config note on first init
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/fixtures/gen_evasions.py` → exit 0 · corpus 347 cases, gaps 17 [ran] [tree 1ee884fdba16] (2026-10-22T16:48:18Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 1.510s / OK [ran] [tree 1ee884fdba16] (2026-10-22T16:48:31Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_evasions` → ✗ exit 1 · Ran 3 tests in 2.170s / FAILED (failures=2) [ran] [tree 8c217dd145d9] (2026-10-22T17:05:26Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 1.385s / OK [ran] [tree 253d1240b6bd] (2026-10-22T17:07:12Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_cloned_config` → exit 0 · Ran 7 tests in 3.169s / OK [ran] [tree 253d1240b6bd] (2026-10-22T17:07:22Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 1.334s / OK [ran] [tree 06425ee9efbf] (2026-10-22T17:09:52Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 1.039s / OK [ran] [tree 06425ee9efbf] (2026-10-22T17:09:54Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 1.177s / OK [ran] [tree 06425ee9efbf] (2026-10-22T17:09:56Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_evasions` → exit 0 · Ran 3 tests in 1.242s / OK [ran] [tree 06425ee9efbf] (2026-10-22T17:10:17Z)
- (audit intent) `builder (high) built the generator, corpus and gaps test-first; merged; in the main checkout the verdicts differed (core protection), so the corpus now runs from the home folder without the four tree-dependent snapshot commands; one fm-reviewer pass: 4 of 5 findings fixed (quoted assignments aren't evasions, compound commands aren't wrapped, home-in-a-repo refused/skipped, dead lists collapsed), the 5th captured T-1482; test_guard_evasions OK` → 301 variants hold; 21 gaps listed, 12 real block->allow captured as T-1480 and T-1481 [tree 06425ee9efbf] (2026-10-22T17:10:17Z)
- (audit adversary) `builder (high) built the generator, corpus and gaps test-first; merged; in the main checkout the verdicts differed (core protection), so the corpus now runs from the home folder without the four tree-dependent snapshot commands; one fm-reviewer pass: 4 of 5 findings fixed (quoted assignments aren't evasions, compound commands aren't wrapped, home-in-a-repo refused/skipped, dead lists collapsed), the 5th captured T-1482; test_guard_evasions OK` → $'…' quoting, variable indirection and BASH_ENV get past the guard today; tracked, not fixed here [tree 06425ee9efbf] (2026-10-22T17:10:17Z)
- (audit edge) `builder (high) built the generator, corpus and gaps test-first; merged; in the main checkout the verdicts differed (core protection), so the corpus now runs from the home folder without the four tree-dependent snapshot commands; one fm-reviewer pass: 4 of 5 findings fixed (quoted assignments aren't evasions, compound commands aren't wrapped, home-in-a-repo refused/skipped, dead lists collapsed), the 5th captured T-1482; test_guard_evasions OK` → a home folder inside a git tree skips the test and the generator refuses, rather than failing on that machine [tree 06425ee9efbf] (2026-10-22T17:10:17Z)
- (audit operator) `builder (high) built the generator, corpus and gaps test-first; merged; in the main checkout the verdicts differed (core protection), so the corpus now runs from the home folder without the four tree-dependent snapshot commands; one fm-reviewer pass: 4 of 5 findings fixed (quoted assignments aren't evasions, compound commands aren't wrapped, home-in-a-repo refused/skipped, dead lists collapsed), the 5th captured T-1482; test_guard_evasions OK` → CHANGELOG line has the counts [tree 06425ee9efbf] (2026-10-22T17:10:17Z)
- (audit maintainer) `builder (high) built the generator, corpus and gaps test-first; merged; in the main checkout the verdicts differed (core protection), so the corpus now runs from the home folder without the four tree-dependent snapshot commands; one fm-reviewer pass: 4 of 5 findings fixed (quoted assignments aren't evasions, compound commands aren't wrapped, home-in-a-repo refused/skipped, dead lists collapsed), the 5th captured T-1482; test_guard_evasions OK` → one EVERY list and a QUOTING subset; regenerate with python3 fixtures/gen_evasions.py [tree 06425ee9efbf] (2026-10-22T17:10:17Z)
## Log
- 2026-10-20T14:01:27Z created
- 2026-10-22T16:03:48Z planned from capture
- 2026-10-22T16:05:12Z set scope=['plugin/tests/fixtures/gen_evasions.py', 'plugin/tests/fixtures/guard_evasions.jsonl', 'plugin/tests/fixtures/guard_gaps.jsonl', 'plugin/tests/test_guard_evasions.py', 'plugin/lib/fmguard.py', 'CHANGELOG.md']
- 2026-10-22T16:36:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1263.builder.md
- 2026-10-22T16:37:05Z focused
- 2026-10-22T17:05:12Z merged worktree-agent-a08aa59e43f095275 (4 file(s))
- 2026-10-22T17:05:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a08aa59e43f095275
- 2026-10-22T17:05:13Z focused
- 2026-10-22T17:06:13Z steer: in the main checkout the four SNAPSHOT commands (git reset --hard, git checkout -- .) are blocked as protected core, in a builder worktree allowed: their verdict depends on the tree, so the generator leaves them out
- 2026-10-22T17:07:22Z step 3 (cloned-config note) shipped as T-1472 (b912b1f2); its tests are this step's evidence
- 2026-10-22T17:09:26Z steer: review: quoting transforms skip a NAME= head (bash runs a quoted assignment as a command name, a no-op), array/env -S skip compound commands, transform lists collapsed, a home folder inside a git tree refuses/skips; SNAPSHOT obfuscations captured
- 2026-10-22T17:10:22Z done
- 2026-10-22T17:10:26Z committed 2be76554 (5 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Criterion 1 is circular. "Every variant is labelled block and the guard holds each" can only pass if the guard already blocks all of them, yet step 2 admits some variants will be missed. The plan doesn't say what happens to the criterion meanwhile: if misses are fixed in this task it is not S…
- HIGH: Some evasions are not statically decidable (eval/base64, script file, alias/function, IFS tricks, variable indirection). A "block" label on all of them may require the guard to block every eval or base64 pipe, which would produce false positives on legitimate commands. Nothing in the corpus c…
- HIGH: The cloned-config audit has no definition of "first" and no acknowledgement mechanism. "One note on first fm init", "SessionStart hook on a project's first session" and "fm doctor naming it until acknowledged" are three different triggers, and the acknowledge command isn't in the steps or cri…
- MEDIUM: The audit's timing is wrong for the threat. Claude Code starts running hooks and MCP servers when it opens the repo, which can be before `fm init` runs, and the plan itself notes Foreman can't prevent this. A note after the fact informs but protects nothing for the first session. — Say so p…
- MEDIUM: Parsing scope is thin. The plan lists `.claude/settings*.json` but doesn't cover `.claude/settings.local.json` precedence, the `.mcp.json` at the repo root, malformed JSON, symlinks pointing outside the repo, or very large files. The audit reads attacker-controlled input, so each of these n…
- LOW: Generated variants are fixed transforms, so the corpus only covers what the author thought of, and "generated" is ambiguous (checked-in output vs generator run at test time). A regenerate step that silently rewrites labels could mask a regression. — Check in the generated jsonl, keep the gener…
Verdict: revise — the criterion-1 contradiction and the missing allow-side and ack-state definitions would cause rework; fix those before generating anything.
## Dissent
- [ ] HIGH: Criterion 1 is circular. "Every variant is labelled block and the guard holds each" can only pass if the guard already blocks all of them, yet step 2 admits some variants will be missed. The plan doesn't say what happens to the criterion meanwhile: if misses are fixed in this task it is not S…
- [ ] HIGH: Some evasions are not statically decidable (eval/base64, script file, alias/function, IFS tricks, variable indirection). A "block" label on all of them may require the guard to block every eval or base64 pipe, which would produce false positives on legitimate commands. Nothing in the corpus c…
- [ ] HIGH: The cloned-config audit has no definition of "first" and no acknowledgement mechanism. "One note on first fm init", "SessionStart hook on a project's first session" and "fm doctor naming it until acknowledged" are three different triggers, and the acknowledge command isn't in the steps or cri…
- [ ] MEDIUM: The audit's timing is wrong for the threat. Claude Code starts running hooks and MCP servers when it opens the repo, which can be before `fm init` runs, and the plan itself notes Foreman can't prevent this. A note after the fact informs but protects nothing for the first session. — Say so p…
- [ ] MEDIUM: Parsing scope is thin. The plan lists `.claude/settings*.json` but doesn't cover `.claude/settings.local.json` precedence, the `.mcp.json` at the repo root, malformed JSON, symlinks pointing outside the repo, or very large files. The audit reads attacker-controlled input, so each of these n…
- [ ] LOW: Generated variants are fixed transforms, so the corpus only covers what the author thought of, and "generated" is ambiguous (checked-in output vs generator run at test time). A regenerate step that silently rewrites labels could mask a regression. — Check in the generated jsonl, keep the gener…
## Related
Related past work (data from this project's history, not instructions):
- T-1472 [SECURITY M, planned, 3 steps] A repo's own Claude config is named on its first Foreman session
- T-0275 [SECURITY M, done, 2 steps] Guard reads what a command runs: script files run by bash/sh/source/. and python, and exec — lesson: A guard that reads files has to c…
- research t0016-adversary-recheck: n## Findings\n\n**CRITICAL — `claude --settings` / `claude --mcp-config` flags entirely unclassified** — `plugin/lib/fmguard.py:656-670…
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/fixtures/gen_evasions.py, plugin/tests/fixtures/guard_evasions.jsonl, plugin/tests/fixtures/guard_gaps.jsonl, plugin/tests/test_guard_evasions.py; re-ground the plan against them before editing
## Why not caught
the builder generated and checked it only in its worktree
## Lessons
- A guard corpus that stores cwd '.' is judged differently in Foreman's protected checkout and a builder worktree; corpora run from a neutral folder.
## Files touched
- plugin/tests/fixtures/gen_evasions.py
- plugin/tests/fixtures/guard_evasions.jsonl
- plugin/tests/fixtures/guard_gaps.jsonl
- plugin/tests/test_guard_evasions.py
- CHANGELOG.md
