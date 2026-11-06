---
id: T-1399
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T19:10:13Z
base: 61ba3b091091b27329600cd0e970651b5ca9eda5
base_tree: bf186f5b9bafd6b7d41b2966065d877337d4a2eb
plan0_at: 2026-10-21T17:33:14Z
plan0_scope: []
verified: strong
---
# fm code takes claude's own flags: -p/--print, -c/--continue and --output-format json mean --plain, --resume and --json
## Raw request
> FEATURE: claude-compatible flags for fm code: -p/--print, -c/--continue and --output-format json map to --plain, --resume and --json (S12, B5)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: fm code -p "x" --dry-plan behaves as fm code --plain "x" --dry-plan, and -c resumes the newest unfinished run
## Interpretation
People type claude's flags out of habit; fm code should accept them where the meaning matches.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code --print "x" --dry-plan behaves as fm code --plain "x" --dry-plan; fm code -c resumes the newest unfinished run; --output-format json gives --json's events — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
Options: (A) argparse aliases on the code parser (-p clashes with fm's global -p/--project, so --print and -p only after the code verb, resolved in the code subparser) (chosen); (B) a shim command named claude (rejected: shadows the real claude); (C) document only. --output-format stream-json is refused with a hint (fm code's --json is its own schema).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests for --print, -c and --output-format json
2. [x] Aliases in the code parser; help text; docs
## Resume here
## Docs impact
CHANGELOG line; README fm code section; MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code` → ✗ exit 1 · Ran 212 tests in 173.3s (30 classes, 16 at a time; slowest: Worker 171s, Bench 56s, Fuzz 45s) / FAILED (2 classes) [ran] [tree 8b5dfcdc7c89] (2026-10-21T17:38:37Z)
- (step 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 212 tests in 222.5s (30 classes, 16 at a time; slowest: Worker 222s, Bench 35s, Review 23s) / OK [ran] [tree e773aaf1f527] (2026-10-21T17:43:46Z)
- (step 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 212 tests in 140.6s (30 classes, 16 at a time; slowest: Worker 140s, Bench 34s, Review 23s) / OK [ran] [tree c91e26bd60c0] (2026-10-21T19:04:28Z)
- (ac 1) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 212 tests in 139.4s (30 classes, 16 at a time; slowest: Worker 139s, Bench 34s, Review 23s) / OK [ran] [tree c91e26bd60c0] (2026-10-21T19:06:48Z)
- (audit intent) `self: read the diff — the code subparser uses conflict_handler=resolve so -p after the verb is --print (plain) and fm's own -p before the verb still picks the project; -c/--continue sets --resume with no id; _OutputFormat maps json to --json and refuses text/stream-json with a hint` → --print x --dry-plan plans like --plain, -c resumes the newest unfinished run to done, --output-format json gives --json events (test_code ClaudeFlags and Resume) [tree c91e26bd60c0] (2026-10-21T19:06:48Z)
- (audit edge) `self: read the diff — the code subparser uses conflict_handler=resolve so -p after the verb is --print (plain) and fm's own -p before the verb still picks the project; -c/--continue sets --resume with no id; _OutputFormat maps json to --json and refuses text/stream-json with a hint` → fm -p SLUG code -p 'x' from outside the repo picks SLUG and runs plain; --output-format text and stream-json exit 2 with a hint; an old 'fm code -p SLUG req' now runs 'SLUG req' plainly (nothing in the repo uses it; documented form is fm -p SLUG code) [tree c91e26bd60c0] (2026-10-21T19:06:48Z)
- (audit self) `self: read the diff — the code subparser uses conflict_handler=resolve so -p after the verb is --print (plain) and fm's own -p before the verb still picks the project; -c/--continue sets --resume with no id; _OutputFormat maps json to --json and refuses text/stream-json with a hint` → no findings [tree c91e26bd60c0] (2026-10-21T19:06:48Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T17:32:36Z planned from capture
- 2026-10-21T17:32:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1399.builder.md
- 2026-10-21T17:33:13Z focused
- 2026-10-21T18:29:14Z merged worktree-agent-a3aa79e42a4569674 (4 file(s))
- 2026-10-21T18:29:14Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3aa79e42a4569674
- 2026-10-21T19:02:06Z focused
- 2026-10-21T19:10:13Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1410 [FEATURE S, active, 2 steps] fm vetoes prints the command that retracts each veto, and that command removes exactly it
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- similar past tasks were M: consider --tier M
## Why not caught
none: new flags
## Lessons
- A CLI that copies another's flags must decide each shared short flag's meaning per position and test both positions
## Plan gaps
- failed first: step 1 Failing tests for --print, -c and --output-format json
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcli.py
- README.md
- MASTER.md
- CHANGELOG.md
- plugin/tests/test_doctor.py
