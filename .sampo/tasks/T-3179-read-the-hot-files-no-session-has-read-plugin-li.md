---
id: T-3179
type: RESEARCH
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: cold
created: 2026-11-05T08:31:00Z
updated: 2026-11-06T02:11:26Z
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: d70900bfa82901f6780427aa09383c4a4171679f
plan0_at: 2026-11-06T02:11:01Z
plan0_scope: []
verified: strong
unproven: [meaning, research-uncited]
---
# Read the hot files no session has read: plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_cli.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py
## Raw request
> Research debt (fm map --cold, T-0660): read and note what each does — plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_cli.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py. Local reading only.
## Interpretation
Reading 1 (chosen): map --cold lists files no session has read; read each and record what it does so later sessions can route by it. Reading 2: review them for defects; ruled out, the request says read and note, local reading only.
## Assumptions (confidence)
## Acceptance criteria
- [x] each of the six files has a one-line note of what it does and what it covers — verify with `sampo task show T-3179`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] read the six files and note each
## Resume here
## Docs impact
## Verification evidence
- (step 1) `wc -l plugin/lib/fmcli.py plugin/lib/fmhooks.py plugin/lib/fmcore.py plugin/tests/test_cli.py plugin/tests/test_docs.py plugin/tests/test_doctor.py` → exit 0 · 1415 plugin/tests/test_doctor.py / 4407 total [ran] [tree d70900bfa829] [world 2f1906870a] (2026-11-06T02:11:12Z)
- (ac 1) `sampo task show T-3179` → exit 0 · - plugin/tests/test_docs.py (1,179 lines, 20 classes): static checks on the prose: rules and lite rules within budget, skills and agents frontmatter (read-only agents), plugin parity, the UI mod's tes [ran] [tree d70900bfa829] [world 2f1906870a] (2026-11-06T02:11:14Z)
- (audit intent) `self: read each file's head, class list and docstrings` → six notes, one per file, in Findings [tree d70900bfa829] (2026-11-06T02:11:14Z)
- (audit self) `self: read each file's head, class list and docstrings` → no findings [tree d70900bfa829] (2026-11-06T02:11:14Z)
- (audit intent) `self: read each file's head, class list and docstrings` → six notes, one per file, in Findings [tree d70900bfa829] (2026-11-06T02:11:24Z)
- (audit self) `self: read each file's head, class list and docstrings` → no findings [tree d70900bfa829] (2026-11-06T02:11:24Z)
## Log
- 2026-11-05T08:31:00Z created
- 2026-11-06T02:10:59Z planned: it has criteria and steps
- 2026-11-06T02:11:00Z focused
- 2026-11-06T02:11:16Z paused: focus moved to T-3252
- 2026-11-06T02:11:21Z focused
- 2026-11-06T02:11:26Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2907 [RESEARCH S, done, 1 steps] Read the hot files no session has read: MASTER.md, plugin/lib/fmgenesis.py, site/genesis/genesis.json, plugin/lib/fmdoctor.py, plugin/…
- T-2801 [RESEARCH S, dropped, 0 steps] Read the hot files no session has read: MASTER.md, README.md, plugin/lib/fmgenesis.py, site/genesis/genesis.json, plugin/tests/test…
- T-2374 [FEATURE M, done, 4 steps] Install-grant queue (Mission 6, #5): fm ask --later queues a user-only grant that never expires, with the miss, the alternatives and th…
- decision 2026-11-05: Recommendation: keep the notes as the cold read for these files; the fm*.py aliases point at plugin/lib/sampo, so a session reading them should open…
## Findings
- plugin/lib/fmcli.py, fmhooks.py, fmcore.py (4 lines each): old import paths kept for two releases after the rename (T-2742); each imports sampo.cli / sampo.hooks / sampo.core and aliases itself in sys.modules, so old 'import fmcli' code keeps working. Nothing else lives there; the real code is plugin/lib/sampo/.
- plugin/tests/test_cli.py (1,801 lines, 32 classes): the CLI run as a subprocess against an isolated FOREMAN_HOME: help and registrations, --json output, init, capture and intake, the task lifecycle, state views, decide rows, criteria edits, checks, audit prep, next action, autonomy, research list/show, ask, redo, list fields, bare fm, shell completion, the inbox, affected pairs.
- plugin/tests/test_docs.py (1,179 lines, 20 classes): static checks on the prose: rules and lite rules within budget, skills and agents frontmatter (read-only agents), plugin parity, the UI mod's test command, runnable code examples, the README's shape and front door, MASTER.md's shape and map shards (lines under 2,000 chars), fences, help answers, card dates, the logo.
- plugin/tests/test_doctor.py (1,415 lines, 21 classes): sampo doctor's checks on good and bad fixtures and the command end to end: briefs, state restore, timing, hook errors, core integrity, the footprint ratchet, state size, scan cache, dual installs, the board, headless, rule conflicts, night timers, model backends, local embedders, served context, the self-fix week, proof worlds, release age.
## Decision
Recommendation: none to act on; route to plugin/lib/sampo/ rather than the fm*.py aliases, and drop the aliases when their two releases end (T-2742). Would change if: something still imports fmcli/fmhooks/fmcore after that.
## Lessons
- The fm*.py files in plugin/lib are 4-line import aliases since T-2742: route to plugin/lib/sampo/ instead
