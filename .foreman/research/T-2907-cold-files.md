# Cold files: what each does (T-2907, 2026-11-05)

Notes from one read-only scout pass over `sampo map --cold`, so later sessions can skip the cold read.

## plugin/lib/fmgenesis.py
Alias for plugin/lib/sampo/rune.py: Genesis tower (`fm genesis`, T-2078), where gen-0 is kept byte for byte.
Entry points: `cmd_genesis` (rune.py:3943).
Size: 5 lines (target 4144).

## plugin/lib/fmexam.py
Alias for plugin/lib/sampo/louhi.py: the seeded exam (`fm exam`, T-2079) of throwaway repos in six languages, each planting one defect.
Entry points: `cmd_exam` (louhi.py:4303).
Size: 5 lines (target 4482).

## plugin/lib/fmcode.py
Alias for plugin/lib/sampo/smith.py: `fm code` (T-1212), Smith's loop run by the harness with a model filling small slots.
Entry points: `cmd_code` (smith.py:2774), `class Run` (:598), `class Blocked` (:1488), `class ConfineError` (:1573), `class CodeError` (:246).
Size: 5 lines (target 3979).

## plugin/lib/fmdoctor.py
Alias for plugin/lib/sampo/doctor.py: `fm doctor`, the Sampo self-check (BUILD_PROMPT §12), where a FAIL exits 1.
Entry points: `cmd_doctor` (doctor.py:2845), `cmd_fsck` (:2610), `cmd_wiring` (:2915), `class Result` (:35).
Size: 5 lines (target 2950).

## plugin/lib/fmlanes.py
Alias for plugin/lib/sampo/lanes.py: `fm lane` (T-0134), a linked git worktree of a project's repo with its own active task.
Entry points: `cmd_lane` (lanes.py:169).
Size: 5 lines (target 2152).

## plugin/lib/fmcost.py
Alias for plugin/lib/sampo/cost.py: `fm cost` / `fm usage` (T-0064, T-0056), where tokens went per session, task and tool, read from Claude's logs.
Entry points: `cmd_cost` (cost.py:663), `cmd_digest` (:894), `cmd_evals` (:1032), `cmd_pr` (:1130), `cmd_export` (:1273), `cmd_usage` (:1409), `cmd_burden` (:1592).
Size: 5 lines (target 1622).

## plugin/lib/fmcodetui.py
Alias for plugin/lib/sampo/smithtui.py: the terminal UI for `fm code tui` (T-1283). It runs fm code as a child with `--json` and draws only from that output.
Entry points: `class State` (smithtui.py:151), `class Canvas` (:407), `_theme` (:78), `class NewerStream` (:147). My grep found no `main` or `cmd_` function.
Size: 5 lines (target 5005).

## plugin/lib/fmrecall.py
Alias for plugin/lib/sampo/recall.py: `fm recall` (T-0043), related past work for a request or task, with outcome and lesson.
Entry points: `cmd_recall` (recall.py:933), `cmd_clauses` (:737), `cmd_share` (:1135), `cmd_explain` (:1267), `cmd_dream` (:1460).
Size: 5 lines (target 1475).

## MASTER.md
Sampo system map (666 lines). Not loaded each session; `sampo doctor` checks its file map against disk.
Top-level sections: 1 What Sampo is (:12), 2 How to prompt it (:20), 3 File map (:51), 4 Interaction diagram (:301), 5 Lifecycle walkthrough (:321), 6 Source of truth and precedence (:333), 7 Integrations (:354), 8 Relationship to BUILD_PROMPT.md (:377), 9 Operations (:381), 10 Known limitations (:624), 11 Deviations from BUILD_PROMPT.md (:647).

## site/genesis/genesis.json
Genesis data file (22138 lines). Top level has `updated` (2026-11-02), `rev` ("1494cb5f") and `capabilities`, a list of `{n, name, text}` entries such as "Initiative", "Exhaustive thinking" and "Anticipation" (from the first lines only).
Size: 22138 lines.

## .claude-plugin/marketplace.json
Marketplace manifest (30 lines), version 1.2.51, listing three plugins: `foreman` (./plugin), `foreman-ui` (./mods/foreman-ui) and `foreman-design` (./plugins/foreman-design).
Size: 30 lines.

## plugin/tests/test_cli.py
Tests for the `fm` CLI (1717 lines). Test classes: HelpRegistrations (:18), OutJson (:42), Init (:57), CaptureAndIntake (:164), TaskLifecycle (:439), StateViews (:782), Checks (:899), AuditPrep (:1095), RoundFiveWorkflow (:1270), DecisionsResearchSelf (:1365), Completion (:1583), SelfRunningLine (:1702), plus about 20 more.

## plugin/tests/test_docs.py
Doc-consistency tests (1153 lines). Test classes: Rules (:88), Skills (:95), PluginParity (:271), SampoFrontDoor (:327), Site (:490), Fences (:793), ReadmeShape (:1032), MasterShape (:1074), MapShards (:1106).

## plugin/tests/test_doctor.py
Tests for `fm doctor` (1383 lines). Test classes: Checks (:18), Briefs (:507), HookErrors (:637), CoreIntegrity (:740), FootprintRatchet (:809), ScanCache (:949), BoardDoctor (:1133), ModelBackends (:1263), SelfFixWeek (:1306), ProofWorlds (:1335), ReleaseAge (:1361).

## plugin/tests/test_lanes.py
Tests for `fm lane` (2223 lines). Test classes: Lanes (:20), LoadGates (:689), LaneRecovery (:875), PlanRace (:1300), RaceEvidence (:1391), DesignRace (:1529), SelfChangeGate (:1717), ProbeDown (:1976), ProbeProvisional (:2039), LaneReexec (:2109).

**Noticed:** test_docs.py `MapShards` says MASTER.md's File map and Operations moved into shards, but MASTER.md still holds both sections at :51 and :381, so the test may be checking a stale layout.
**Noticed:** The alias files (fm*.py) say they are kept for two releases (T-2742); nothing I read records when they can be removed.
