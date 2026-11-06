---
id: T-0205
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:10:46Z
updated: 2026-10-04T04:35:42Z
base: e28d4d3499c878038982af1317b98b413f2aac18
base_tree: 7af4d9ffe6c18e1c6b4982c9b60b764b5faa07f4
verified: strong
---
# fm next names the installed third-party skills that fit a task's stage
## Raw request
> FEATURE: fm next names the installed third-party skills that fit a task's stage (e.g. CLEAN → /ponytail:ponytail-audit, SECURITY → a security skill, UI scope → frontend-design), from a cached index of enabled plugins' and user skills
> CONTEXT: STAGE_REFERENCE in plugin/lib/fmcore.py names only Foreman procedures; fmplugins.installed() and profile() already list enabled plugins' skills; next_action runs every turn, so the index must be cached (rebuild on installed_plugins.json/settings mtime)
> CONTEXT: plugin/agents/fm-recon.md and plugin/skills/intake/references/delegate.md; RESEARCH's STAGE_REFERENCE points at delegate.md
> CONTEXT: plugin/agents/, fmrecall.note_failure thrash hint, skills/intake/references/debugging.md and delegate.md (allowed delegations)
> CONTEXT: plugin/lib/fmideas.py writes ideas.md; fmrecall.recall(p, query) returns ranked hits with labels like "T-0039 [SECURITY S, done, …]"
> DONE-WHEN: a test with a fake enabled plugin carrying a matching skill shows it in next_action's executing line, and no line when none matches
> DONE-WHEN: fm-recon.md and delegate.md carry the protocol and test_docs (or a new check) keeps the agent's required output sections
> DONE-WHEN: the agent file exists with read-only tools and fm doctor passes; the thrash hint names it
> DONE-WHEN: a test shows an idea matching a done brief annotated with that brief's id in ideas.md
## Interpretation
Foreman knows other plugins only from a static table in MASTER.md; fm next names Foreman's own procedure for a stage and nothing else, so an installed /ponytail-audit or frontend-design is forgotten at the moment it fits. Route each stage to the installed skills that fit it, cheaply, and learn from which ones get used.
## Assumptions (confidence)
## Acceptance criteria
- [x] an enabled plugin's skill matching the active task's stage is named in fm next; none when nothing matches; skills used before in tasks of that type rank first — verify with `python3 plugin/tests/run.py -k test_skillroute`
## Non-goals
## Approach (options → choice → why)
A) a static map stage→skill names: breaks when plugins change. B) an index built from enabled plugins' skill/command frontmatter (fmplugins.profile) plus user and project skills, matched by per-stage keywords on name+description, cached in state keyed by the mtimes of the plugin registry, settings and skills folders and the day; ranked by how often each was invoked (Skill tool events) in past tasks. Choice: B — adapts to whatever is installed and costs one JSON read per prompt.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first (fake plugin dir, user skill)
2. [x] Cached capability index in fmplugins + next_for hint
3. [x] Docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_skillroute` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: SkillRoute 1s) / OK [ran] [tree 482640a938fd] (2026-10-04T04:34:47Z)
- (step 2) `python3 plugin/tests/run.py -k test_skillroute` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: SkillRoute 1s) / OK [ran] [tree 482640a938fd] (2026-10-04T04:34:48Z)
- (step 3) `python3 plugin/tests/run.py -k test_skillroute` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: SkillRoute 1s) / OK [ran] [tree 482640a938fd] (2026-10-04T04:34:50Z)
- `python3 plugin/tests/run.py -k test_skillroute` → ✗ exit 1 · Ran 4 tests in 1.3s (1 classes, 16 at a time; slowest: SkillRoute 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 482640a938fd] (2026-10-04T04:34:52Z)
- `python3 plugin/tests/run.py -k test_skillroute` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: SkillRoute 1s) / OK [ran] [tree 482640a938fd] (2026-10-04T04:34:52Z)
- (ac 1) `python3 plugin/tests/run.py -k test_skillroute` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: SkillRoute 1s) / OK [ran] [tree 482640a938fd] (2026-10-04T04:35:42Z)
- (audit intent) `self review (read-only hint, no exec or trust boundary; independent pass skipped for usage)` → the stage's fitting skills from whatever is installed reach Claude at the moment they fit; on this machine CLEAN → ponytail-audit/review + /simplify, SECURITY → /security-review, UI → frontend-design, nothing spurious for FIX/RESEARCH/PERF (checked live after cutting two false hits) [tree 482640a938fd] (2026-10-04T04:35:42Z)
- (audit edge) `self review (read-only hint, no exec or trust boundary; independent pass skipped for usage)` → a broken registry or unreadable plugin is swallowed in next_for (the next action never fails); disabled plugins and Foreman-duplicating or extension-authoring skills are left out (tested); the cache key carries an index version, the day and six mtimes so a code change or install rebuilds it; usage counts are per project [tree 482640a938fd] (2026-10-04T04:35:42Z)
## Log
- 2026-10-04T04:10:46Z created
- 2026-10-04T04:10:52Z set tier=M
- 2026-10-04T04:11:27Z steer: learn — record which routed skills were used and whether the task closed first time; demote hints that never help
- 2026-10-04T04:32:49Z planned from capture
- 2026-10-04T04:32:49Z focused
- 2026-10-04T04:35:42Z done
- 2026-10-04T04:35:42Z committed 72aa696 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0208 [FEATURE S, done, 1 steps] fm ideas marks each new idea with the finished task it most resembles
- T-0207 [FEATURE M, done, 3 steps] Debugging ledger: hypotheses in the brief that fm next drives, and a fresh-eyes fm-debugger agent — lesson: Any new free-text field wri…
- T-0206 [FEATURE M, done, 3 steps] fm research ask: recall first, parallel web researchers per sub-question, every quoted claim re-fetched and checked, one note recorded …
- research brainstorm-20261003-round6: Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new ti…
- similar finished tasks took 1–3 steps
## Lessons
- Keyword routing over skill descriptions needs the first sentence only: later sentences list side uses (a skill creator 'benchmarks skill performance'), which made two of three PERF hits false
## Files touched
- plugin/tests/test_skillroute.py
- plugin/lib/fmcore.py
- plugin/lib/fmplugins.py
- CHANGELOG.md
- MASTER.md
