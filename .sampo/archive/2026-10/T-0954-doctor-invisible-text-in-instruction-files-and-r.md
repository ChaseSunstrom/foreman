---
id: T-0954
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:39Z
updated: 2026-10-15T21:43:35Z
base: b595b8924a0e85f5032f946390d81bd4332a7572
base_tree: e7e6473cc1ed1ec6ee8dc8ea7a082360a8dff841
verified: strong
---
# Doctor: invisible text in instruction files, and README verbs that don't exist
## Raw request
> Doctor: invisible text in instruction files, and README verbs that don't exist
## Interpretation
Board clusters security and r4-guard-hardening (invisible-text scan) and round5-skip #49 (doc claim checks). fm doctor gains check_invisible_text: Cf, bidi and tag characters (U+200B-U+200F, U+202A-U+202E, U+2066-U+2069, U+E0000-U+E007F) in CLAUDE.md, ~/.claude/rules/*.md, plugin skills/*/SKILL.md and agents/*.md, reported as file:line WARN; fmcore.plain already strips them for display. And a check that every `fm <verb>` in README.md names a real parser verb.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor WARNs with file:line when an instruction file holds zero-width, bidi or tag characters, and is quiet on clean files — verify with `python3 plugin/tests/run.py -k BoardDoctor`
- [x] fm doctor FAILs naming the verb when README.md mentions an fm verb the parser lacks — verify with `python3 plugin/tests/run.py -k BoardDoctor`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardDoctor class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
<!-- auto -->
- 2026-10-15T21:40:40Z steps 3/3 done
- git: foreman/build; 3 uncommitted: MASTER.md, plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py
- touched since last checkpoint: plugin/tests/test_doctor.py, plugin/lib/fmdoctor.py, MASTER.md
## Docs impact
MASTER (Health line), CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardDoctor` → exit 0 · Ran 3 tests in 0.2s (1 classes, 16 at a time; slowest: BoardDoctor 0s) / OK [ran] [tree 1cbff6f11593] (2026-10-15T21:40:03Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_docs` → exit 0 · Ran 71 tests in 21.1s (26 classes, 16 at a time; slowest: Command 21s, ViewsRepair 14s, TaskLifecycle 1s) / OK [ran] [tree 1cbff6f11593] (2026-10-15T21:40:24Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 31 tests in 1.1s (10 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree 1cbff6f11593] (2026-10-15T21:40:25Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_docs` → exit 0 · Ran 71 tests in 28.1s (26 classes, 16 at a time; slowest: Command 28s, ViewsRepair 15s, TaskLifecycle 1s) / OK [ran] [tree e20017fc78e8] (2026-10-15T21:43:16Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardDoctor` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: BoardDoctor 0s) / OK [ran] [tree ca06eac283d2] (2026-10-15T21:43:34Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardDoctor` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: BoardDoctor 0s) / OK [ran] [tree ca06eac283d2] (2026-10-15T21:43:34Z)
- (audit intent) `one fm-reviewer pass (sonnet): 5 findings, all fixed test-first` → hidden text in instruction files warns with file:line; README/MASTER/skills naming a missing fm verb fails, fences included [tree ca06eac283d2] (2026-10-15T21:43:34Z)
- (audit adversary) `one fm-reviewer pass (sonnet): 5 findings, all fixed test-first` → zero-width, bidi, tag, word-joiner, BOM mid-file, soft hyphen, variation selectors and ZWJ runs all warn; emoji glue after non-ASCII is allowed [tree ca06eac283d2] (2026-10-15T21:43:34Z)
- (audit edge) `one fm-reviewer pass (sonnet): 5 findings, all fixed test-first` → a leading BOM, emoji ZWJ sequences and VS16 hearts stay quiet; missing files are skipped [tree ca06eac283d2] (2026-10-15T21:43:34Z)
- (audit maintainer) `one fm-reviewer pass (sonnet): 5 findings, all fixed test-first` → one regex, one file list, one Result; the shipped-files test scans the plugin only [tree ca06eac283d2] (2026-10-15T21:43:34Z)
## Log
- 2026-10-15T21:12:39Z created
- 2026-10-15T21:29:56Z grounding: AC2 already exists: fmdoctor.check_self_docs (line ~671) FAILs on README/MASTER/rules/skills naming an fm command or subcommand the parser lacks; the BoardDoctor test only has to prove it. Remaining work: check_invisible_text (Cf/bidi/tag chars in CLAUDE.md, ~/.claude/rules/*.md, plugin skills/*/SKILL.md, agents/*.md; WARN file:line). Small: main thread after the lane merges.
- 2026-10-15T21:38:56Z focused
- 2026-10-15T21:40:41Z paused: focus moved to T-0957
- 2026-10-15T21:41:34Z focused
- 2026-10-15T21:43:34Z done
- 2026-10-15T21:43:35Z committed 1ac2efb (4 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize. [stale: plugin/lib/fmsetup.py, plugin/uninstall.sh changed since it…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
- similar past tasks were L: consider --tier L
## Lessons
- A ZWJ/VS exemption for emoji must still flag runs: a single allowed glue char repeated is a payload channel
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- MASTER.md
- CHANGELOG.md
