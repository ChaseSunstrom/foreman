---
id: T-2907
type: RESEARCH
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: cold
created: 2026-11-04T06:33:53Z
updated: 2026-11-05T02:08:02Z
base: b3ac10ff49295f54456dfa8a6c32f2b8fa9b9888
base_tree: ab0d245b6375d38111d3d00152230ace0565424a
plan0_at: 2026-11-05T02:03:47Z
plan0_scope: []
verified: strong
unproven: [meaning, research-uncited]
---
# Read the hot files no session has read: MASTER.md, plugin/lib/fmgenesis.py, site/genesis/genesis.json, plugin/lib/fmdoctor.py, plugin/tests/test_cli.py, plugin/lib/fmexam.py, plugin/lib/fmlanes.py, p…
## Raw request
> Research debt (fm map --cold, T-0660): read and note what each does — MASTER.md, plugin/lib/fmgenesis.py, site/genesis/genesis.json, plugin/lib/fmdoctor.py, plugin/tests/test_cli.py, plugin/lib/fmexam.py, plugin/lib/fmlanes.py, plugin/lib/fmcost.py, 11 left out. Local reading only.
## Interpretation
Reading 1 (taken): the map's cold list names files with many commits that no session has read; a short note per file (what it does, its new home after the Sampo rename, its main entry points) filed as research so later sessions skip the cold read. Reading 2 (ruled out): change the files: local reading only.
## Assumptions (confidence)
## Acceptance criteria
- [x] A note per cold file (what it does, where it lives after the rename, its main entry points) is filed as research and the map's cold list shrinks — verify with `sampo research show T-2907-cold-files`
## Non-goals
## Approach (options → choice → why)
1) use what exists: one fm-scout pass over the cold list, notes filed with sampo research add: likely outcome: one page, cheap. 2) read them in the main thread: fails if: spends main-thread context for notes. 3) do less: nothing: fails if: the map keeps flagging them. Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] scout notes per cold file; file them
## Resume here
## Docs impact
## Verification evidence
- (step 1) `sampo research show T-2907-cold-files | grep -c '^## '` → exit 0 · 15 [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:07:47Z)
- (ac 1) `sampo research show T-2907-cold-files` → exit 0 · **Noticed:** test_docs.py `MapShards` says MASTER.md's File map and Operations moved into shards, but MASTER.md still holds both sections at :51 and :381, so the test may be checking a stale layout. / [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:07:54Z)
- (audit intent) `self: read the scout's notes against the files' own headers for three of them (fmgenesis.py, fmcost.py, marketplace.json); the alias targets and entry points match` → one note per cold file, filed as research T-2907-cold-files; its two noticed items captured (T-3094, T-3095) [tree ab0d245b6375] (2026-11-05T02:07:54Z)
- (audit self) `self: read the scout's notes against the files' own headers for three of them (fmgenesis.py, fmcost.py, marketplace.json); the alias targets and entry points match` → no findings [tree ab0d245b6375] (2026-11-05T02:07:54Z)
- (audit intent) `self: read the scout's notes against the files' own headers for three of them (fmgenesis.py, fmcost.py, marketplace.json); the alias targets and entry points match` → one note per cold file, filed as research T-2907-cold-files; its two noticed items captured (T-3094, T-3095) [tree ab0d245b6375] (2026-11-05T02:08:01Z)
- (audit self) `self: read the scout's notes against the files' own headers for three of them (fmgenesis.py, fmcost.py, marketplace.json); the alias targets and entry points match` → no findings [tree ab0d245b6375] (2026-11-05T02:08:01Z)
## Log
- 2026-11-04T06:33:53Z created
- 2026-11-05T02:03:45Z planned: it has criteria and steps
- 2026-11-05T02:03:46Z set approved=True
- 2026-11-05T02:03:46Z focused
- 2026-11-05T02:08:02Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2801 [RESEARCH S, dropped, 0 steps] Read the hot files no session has read: MASTER.md, README.md, plugin/lib/fmgenesis.py, site/genesis/genesis.json, plugin/tests/test…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-05: [cites: research T-2879-probe] T-2879: rename the plugins inside the existing 'foreman' marketplace with a renames map (foreman→sampo, foreman-ui→sa…
## Decision
Recommendation: keep the notes as the cold read for these files; the fm*.py aliases point at plugin/lib/sampo, so a session reading them should open the sampo module named in the note; would change if: the aliases are removed (T-3095) or a file's entry points move, then the map's cold list flags it again.
## Lessons
- A cold-file list after a rename is mostly aliases; the note's job is to point at the new module, not to restate it
