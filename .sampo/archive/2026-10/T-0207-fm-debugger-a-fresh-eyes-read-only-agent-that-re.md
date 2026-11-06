---
id: T-0207
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:10:46Z
updated: 2026-10-04T04:32:31Z
base: 1209d65c05002ece642f8af556f5690ccefa7995
base_tree: 5828bbd0cacafd8a110b99b2e09b61132277771a
verified: strong
---
# Debugging ledger: hypotheses in the brief that fm next drives, and a fresh-eyes fm-debugger agent
## Raw request
> FEATURE: fm-debugger, a fresh-eyes read-only agent that returns ranked root-cause hypotheses each with one cheap discriminating probe; the thrash hint and debugging.md offer it
> CONTEXT: STAGE_REFERENCE in plugin/lib/fmcore.py names only Foreman procedures; fmplugins.installed() and profile() already list enabled plugins' skills; next_action runs every turn, so the index must be cached (rebuild on installed_plugins.json/settings mtime)
> CONTEXT: plugin/agents/fm-recon.md and plugin/skills/intake/references/delegate.md; RESEARCH's STAGE_REFERENCE points at delegate.md
> CONTEXT: plugin/agents/, fmrecall.note_failure thrash hint, skills/intake/references/debugging.md and delegate.md (allowed delegations)
> CONTEXT: plugin/lib/fmideas.py writes ideas.md; fmrecall.recall(p, query) returns ranked hits with labels like "T-0039 [SECURITY S, done, …]"
> DONE-WHEN: a test with a fake enabled plugin carrying a matching skill shows it in next_action's executing line, and no line when none matches
> DONE-WHEN: fm-recon.md and delegate.md carry the protocol and test_docs (or a new check) keeps the agent's required output sections
> DONE-WHEN: the agent file exists with read-only tools and fm doctor passes; the thrash hint names it
> DONE-WHEN: a test shows an idea matching a done brief annotated with that brief's id in ideas.md
## Interpretation
Debugging state lives only in the model's context: after a compaction or a long hunt it forgets what it ruled out, retries variations, and the thrash hint can only say 'diagnose'. Make hypotheses first-class: recorded in the brief with their probe results, driven by fm next, and offer a fresh-context agent that proposes ranked hypotheses with discriminating probes.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task hypo records hypotheses and probe results in the brief, and fm next points at the first open one until one is confirmed — verify with `python3 plugin/tests/run.py -k test_debug`
- [x] the fm-debugger agent is read-only and the repeated-failure hint names it — verify with `python3 plugin/tests/run.py -k test_debug`
## Non-goals
## Approach (options → choice → why)
A) only an agent: fresh eyes, but its output evaporates. B) only a ledger: durable, but no second opinion. Choice: both, small — a Hypotheses section (H1 [open|ruled out|confirmed] claim — probe, with --run results recorded like evidence; the guard already checks every fm --run), next_action points at the first open hypothesis until one is confirmed, and a read-only fm-debugger agent whose output is hypothesis lines ready for fm task hypo add.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first
2. [x] Brief hypotheses + fm task hypo + next_action
3. [x] fm-debugger agent, thrash hint, debugging.md, docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/debugging.md, plugin/skills/intake/references/delegate.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 4 tests in 1.3s (2 classes, 16 at a time; slowest: Hypotheses 1s, Debugger 0s) / OK [ran] [tree 9490b38af25f] (2026-10-04T04:28:59Z)
- (step 2) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 4 tests in 1.2s (2 classes, 16 at a time; slowest: Hypotheses 1s, Debugger 0s) / OK [ran] [tree 9490b38af25f] (2026-10-04T04:29:01Z)
- (step 3) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 4 tests in 1.3s (2 classes, 16 at a time; slowest: Hypotheses 1s, Debugger 0s) / OK [ran] [tree 9490b38af25f] (2026-10-04T04:29:02Z)
- (step 1) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 5 tests in 2.8s (2 classes, 16 at a time; slowest: Hypotheses 3s, Debugger 1s) / OK [ran] [tree ecf115afa698] (2026-10-04T04:30:52Z)
- (step 2) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 5 tests in 2.9s (2 classes, 16 at a time; slowest: Hypotheses 3s, Debugger 1s) / OK [ran] [tree ecf115afa698] (2026-10-04T04:30:56Z)
- (step 3) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 5 tests in 2.8s (2 classes, 16 at a time; slowest: Hypotheses 3s, Debugger 1s) / OK [ran] [tree ecf115afa698] (2026-10-04T04:30:59Z)
- `python3 plugin/tests/run.py -k test_debug` → ✗ exit 1 · Ran 5 tests in 1.7s (2 classes, 16 at a time; slowest: Hypotheses 2s, Debugger 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree ecf115afa698] (2026-10-04T04:31:03Z)
- `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 5 tests in 2.7s (2 classes, 16 at a time; slowest: Hypotheses 3s, Debugger 1s) / OK [ran] [tree ecf115afa698] (2026-10-04T04:31:03Z)
- (ac 1) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 5 tests in 2.9s (2 classes, 16 at a time; slowest: Hypotheses 3s, Debugger 1s) / OK [ran] [tree ecf115afa698] (2026-10-04T04:32:30Z)
- (ac 2) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 5 tests in 2.9s (2 classes, 16 at a time; slowest: Hypotheses 3s, Debugger 1s) / OK [ran] [tree ecf115afa698] (2026-10-04T04:32:30Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge), findings verified and fixed test-first` → probes run only through --run, which the guard checks in every spelling (--run, --run=, --r: tested); fixed MEDIUMs: a newline in a claim forged a confirmed line and could add a section → ledger text is one line; probes and run commands were stored unredacted with raw backticks → redacted and backtick-free; claim text reached the model via fm next undefanged → defanged like evidence [tree ecf115afa698] (2026-10-04T04:32:30Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge), findings verified and fixed test-first` → re-marking replaced, not stacked (tested); numbering max+1 survives edits; the driver only acts in the executing stage and stops once one hypothesis is confirmed (tested) [tree ecf115afa698] (2026-10-04T04:32:30Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge), findings verified and fixed test-first` → hypotheses and their probe results survive a compaction in the brief, fm next keeps Claude on the open one, and the repeated-failure hint offers the ledger and the fresh-eyes fm-debugger [tree ecf115afa698] (2026-10-04T04:32:30Z)
## Log
- 2026-10-04T04:10:46Z created
- 2026-10-04T04:10:52Z set tier=S
- 2026-10-04T04:11:26Z steer: stateful — a Hypotheses section in the brief (open/ruled out/confirmed + probe evidence) that fm next drives, fed by fm-debugger
- 2026-10-04T04:11:27Z set tier=M
- 2026-10-04T04:27:28Z planned from capture
- 2026-10-04T04:27:28Z focused
- 2026-10-04T04:32:31Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0208 [FEATURE S, done, 1 steps] fm ideas marks each new idea with the finished task it most resembles
- T-0206 [FEATURE M, done, 3 steps] fm research ask: recall first, parallel web researchers per sub-question, every quoted claim re-fetched and checked, one note recorded …
- research brainstorm-20261003-round6: Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new ti…
- research brainstorm-20260926-super-slate: Built under T-0071, in rounds (inbox items folded in):
- similar finished tasks took 1–3 steps
## Lessons
- Any new free-text field written into a brief needs the same cleaning as evidence (one line, redact, defang, unmark); a shared helper per field kind beats re-deriving the list each time
## Files touched
- plugin/tests/test_debug.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/agents/fm-debugger.md
- plugin/lib/fmrecall.py
- plugin/skills/intake/references/debugging.md
- plugin/skills/intake/references/delegate.md
- CHANGELOG.md
- MASTER.md
