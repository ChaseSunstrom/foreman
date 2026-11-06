---
id: T-0208
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:10:46Z
updated: 2026-10-04T04:20:05Z
base: 329d1810f2fca16c034db6940e3eaac8851d3b0a
base_tree: 6a4be9d1760ad116dfbb7295e95b74ff86b487ce
verified: strong
---
# fm ideas marks each new idea with the finished task it most resembles
## Raw request
> FEATURE: fm ideas pre-grounds each new idea with its nearest finished task from fm recall, so dupes of done work are marked before the main thread grounds them
> CONTEXT: STAGE_REFERENCE in plugin/lib/fmcore.py names only Foreman procedures; fmplugins.installed() and profile() already list enabled plugins' skills; next_action runs every turn, so the index must be cached (rebuild on installed_plugins.json/settings mtime)
> CONTEXT: plugin/agents/fm-recon.md and plugin/skills/intake/references/delegate.md; RESEARCH's STAGE_REFERENCE points at delegate.md
> CONTEXT: plugin/agents/, fmrecall.note_failure thrash hint, skills/intake/references/debugging.md and delegate.md (allowed delegations)
> CONTEXT: plugin/lib/fmideas.py writes ideas.md; fmrecall.recall(p, query) returns ranked hits with labels like "T-0039 [SECURITY S, done, …]"
> DONE-WHEN: a test with a fake enabled plugin carrying a matching skill shows it in next_action's executing line, and no line when none matches
> DONE-WHEN: fm-recon.md and delegate.md carry the protocol and test_docs (or a new check) keeps the agent's required output sections
> DONE-WHEN: the agent file exists with read-only tools and fm doctor passes; the thrash hint names it
> DONE-WHEN: a test shows an idea matching a done brief annotated with that brief's id in ideas.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an idea matching a done brief is annotated with that brief's id in ideas.md, and --seen strips the note — verify with `python3 plugin/tests/run.py -k test_ideas`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then a one-index nearest-done helper in fmrecall used by fm ideas
## Resume here
## Docs impact
plugin/skills/brainstorm/SKILL.md
## Verification evidence
- `python3 plugin/tests/run.py -k test_ideas` → ✗ exit 1 · Ran 12 tests in 3.1s (1 classes, 16 at a time; slowest: Ideas 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ab7b461ca74d] (2026-10-04T04:19:06Z)
- `python3 plugin/tests/run.py -k test_ideas` → exit 0 · Ran 12 tests in 3.0s (1 classes, 16 at a time; slowest: Ideas 3s) / OK [ran] [tree ab7b461ca74d] (2026-10-04T04:19:06Z)
- (step 1) `python3 plugin/tests/run.py -k test_ideas` → exit 0 · Ran 12 tests in 3.0s (1 classes, 16 at a time; slowest: Ideas 3s) / OK [ran] [tree ab7b461ca74d] (2026-10-04T04:19:09Z)
- (ac 1) `python3 plugin/tests/run.py -k test_ideas` → exit 0 · Ran 12 tests in 3.0s (1 classes, 16 at a time; slowest: Ideas 3s) / OK [ran] [tree f4d9a3e7e8e6] (2026-10-04T04:20:05Z)
- (audit self) `self checklist: threshold (half the words, ≥2) keeps unrelated ideas unmarked (bold-bets case); --seen strips the note so dedupe and packs see bare titles; one brief pass for all titles` → pass [tree f4d9a3e7e8e6] (2026-10-04T04:20:05Z)
## Log
- 2026-10-04T04:10:46Z created
- 2026-10-04T04:10:52Z set tier=S
- 2026-10-04T04:18:03Z planned from capture
- 2026-10-04T04:18:03Z focused
- 2026-10-04T04:20:05Z done
- 2026-10-04T04:20:05Z committed 22bb0d1 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261003-round6: Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new ti…
- research brainstorm-20260926-super-slate: Built under T-0071, in rounds (inbox items folded in):
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- research t0016-edge: 901a8c8-aa34-4df7-8164-6500197eb1c7","version":"2.1.280","gitBranch":"foreman/build","slug":"starry-petting-quasar"}
## Files touched
- plugin/tests/test_ideas.py
- plugin/lib/fmrecall.py
- plugin/lib/fmideas.py
- plugin/skills/brainstorm/SKILL.md
