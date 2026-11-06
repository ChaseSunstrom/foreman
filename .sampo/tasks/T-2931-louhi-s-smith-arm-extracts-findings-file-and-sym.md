---
id: T-2931
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T08:23:08Z
updated: 2026-11-04T10:15:02Z
base_note: Calibration: this plan states Choice 60% where FEATURE M closes (607) held on the first finish 98% of the time: 38 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T08:49:12Z
rival_split: true
builder_model: haiku
base: 28bd5155a44d7449c34a0be42524a1bde749c77c
base_tree: 1832fb900b22a76ec0ef09dffa8813b053bdf88d
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T09:18:58Z
plan0_scope: []
lane_stop: merged 2026-11-04T09:32:46Z
verified: strong
---
# Louhi's smith arm extracts findings (file and symbol) from Smith's final summary, so…
## Raw request
> FEATURE: Louhi's smith arm extracts findings (file and symbol) from Smith's final summary, so 'found' counts for local models as it does for the agent arms; gemma4:12b named vuln-js's SQL injection in find_user_sql correctly and got no credit because the arm writes no findings
## Interpretation
Reading 1 (chosen): louhi._smith_arm returns "findings": [] by design (its docstring: Smith reports a summary, the grade reads the tree), and the grade (louhi.grade) credits "found" only from ans["findings"] matched to the key's defects by file and symbol. So gemma4:12b naming vuln-js's SQL injection in find_user_sql in its summary got no credit. After fm code ends, ask the same local profile once for the findings from the end text and use the answer as the arm's findings.
Reading 2 (ruled out): matching the summary against the key, or against defect names. The arm must never see the key; credit and false alarms stay the grader's job, so a wrong or invented finding costs a false alarm like any agent arm's.
## Assumptions (confidence)
## Acceptance criteria
- [x] given an end text and a stubbed models.complete, the smith arm's answer holds the findings (file, symbol, says) parsed from the reply, and the arm's grade can credit them — verify with `python3 plugin/tests/run.py test_exam_smith_findings`
- [x] a finding naming a file not in the repo is dropped; with no end text (timeout, crash) no extra call is made and findings stay empty — verify with `python3 plugin/tests/run.py test_exam_smith_findings`
- [x] the existing smith-arm tests pass — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) One tool-less call after fm code ends: models.complete on the arm's profile with the end event's text (the closed or answer event, up to a few thousand characters) and the repo's file list, asking for the {"findings": [{"file","symbol","says"}]} object the session arms use (louhi.ASK/AGAIN wording), parsed by the existing _reply/_answer; findings whose file is not in the repo's tree are dropped; the call goes in the events log. Likely outcome: gemma4:12b's find_user_sql finding is credited, 'found' becomes a real number for local models, and false alarms show up where they are earned. Fails if: the model restates the task's request as findings the summary did not make, raising false alarms; the grader's own false-alarm count then shows it, and no key is involved.
2) use what exists: a regex over the end text for repo file paths and def/function names in the tree. Likely outcome: no second call, deterministic. Fails if: it lists every file the summary mentions, so false alarms swamp found.
3) do less: leave findings empty (today). Likely outcome: 'found' stays 0 for every local model, so the exam cannot rank them. Fails if: the exam's purpose (comparing local models by what they find) matters, which is why this task exists.
Choice 1 (60%): the only option that credits what the model actually reported without reading the key; the file-exists filter is the only guard on invention.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: test_exam_smith_findings.py patching models.complete
2. [x] After fm code ends in _smith_arm, call the arm's profile once with the end text and the file list, parse with _reply, filter by files that exist
3. [x] Log the call in the events file; update the _smith_arm docstring
4. [x] Run the new test and test_exam
## Resume here
## Docs impact
CHANGELOG line (T-2931); _smith_arm's docstring names the findings call
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam_smith_findings` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: SmithFindings 0s) / OK [ran] [tree 4176494c6595] [world 2f1906870a] (2026-11-04T09:23:38Z)
- (step 2) `python3 plugin/tests/run.py test_exam.SmithArm 2>&1 | tail -5` → exit 0 · Ran 3 tests in 9.3s (1 classes, 16 at a time; slowest: SmithArm 9s) / OK [ran] [tree 14a9bff99561] [world 2f1906870a] (2026-11-04T09:24:21Z)
- (step 4) `python3 plugin/tests/run.py test_exam.SmithArm` → exit 0 · Ran 3 tests in 10.5s (1 classes, 16 at a time; slowest: SmithArm 10s) / OK [ran] [tree 14a9bff99561] [world 2f1906870a] (2026-11-04T09:24:35Z)
- (step 3) `python3 plugin/tests/run.py test_exam_smith_findings` → exit 0 · Ran 4 tests in 0.5s (1 classes, 16 at a time; slowest: SmithFindings 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:11:30Z)
- `python3 plugin/tests/run.py test_exam_smith_findings` → ✗ exit 1 · Ran 4 tests in 1.5s (1 classes, 16 at a time; slowest: SmithFindings 0s) / FAILED (1 classes: test_exam_smith_findings.SmithFindings) (start tree + this task's tests) [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:11:40Z)
- `python3 plugin/tests/run.py test_exam_smith_findings` → exit 0 · Ran 4 tests in 0.5s (1 classes, 16 at a time; slowest: SmithFindings 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:11:40Z)
- (ac 1) `python3 plugin/tests/run.py test_exam_smith_findings` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T10:11:40Z [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:13:14Z)
- (ac 2) `python3 plugin/tests/run.py test_exam_smith_findings` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T10:11:40Z [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:13:14Z)
- (ac 3) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 109 tests in 92.8s (27 classes, 16 at a time; slowest: LeanKind 93s, ExamAuthors 78s, JudgmentKinds 74s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:13:14Z)
- (audit intent) `one fm-reviewer pass over the uplift batch (T-2931's diff)` → _smith_findings asks the arm's local model once for findings from Smith's end text and the repo's paths; the grade credits a finding naming the planted file [tree c6d95c6236bb] (2026-11-04T10:13:14Z)
- (audit adversary) `one fm-reviewer pass over the uplift batch (T-2931's diff)` → end text is redacted before it is sent; a finding naming a file outside the repo is dropped; an invented finding in a real file costs a false alarm, as with the agent arms [tree c6d95c6236bb] (2026-11-04T10:13:14Z)
- (audit edge) `one fm-reviewer pass over the uplift batch (T-2931's diff)` → a timeout counts as no end, so no call; a ModelError or OSError leaves findings empty and is logged [tree c6d95c6236bb] (2026-11-04T10:13:14Z)
## Log
- 2026-11-04T08:23:08Z created
- 2026-11-04T08:44:57Z set tier=M
- 2026-11-04T08:46:20Z planned: it has criteria and steps
- 2026-11-04T08:46:25Z set approved=True
- 2026-11-04T09:18:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2931.builder.md
- 2026-11-04T09:18:57Z focused
- 2026-11-04T09:18:58Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T09:32:46Z merged worktree-agent-abc967b423c75b97c (3 file(s))
- 2026-11-04T09:44:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abc967b423c75b97c
- 2026-11-04T10:11:29Z focused
- 2026-11-04T10:15:02Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: in the Louhi bench harness's "smith" arm (the local-model arm, likely under `bench/` or a `plugin/lib/` louhi module), parse Smith's final summary text into structured findings `{file, symbol}` and write them in the same format/location the agent arms write, so the existing scorer's "fou…
- Scoring-side reading: the arm already emits something, but the scorer only reads a findings artifact (e.g. `findings.json`) that the smith arm never produces. The fix is to make the scorer fall back to summary text for this arm instead of changing the arm.
- Model-side reading: ask Smith to emit a structured findings block (JSON) in its final summary through the prompt, then parse it, rather than extracting free-form prose after the fact.
- Narrow reading: only the vuln-js case is broken (e.g. symbol matching is case/format-sensitive such as `find_user_sql` vs `findUserSql`), and the real bug is in matching, not extraction.
Approaches:
- Add an extractor function in the smith arm that runs after Smith finishes: regex/heuristics over the summary for path-like tokens (`\S+\.(js|py|ts)`) and identifier-like tokens near them, validated against files that actually exist in the target repo, then write findings in the agent arms' schema. …
- Constrain the output: append a prompt instruction requiring a fenced `FINDINGS` JSON block, parse that first, and use the heuristic extractor only as a fallback when the block is missing or malformed (small local models often ignore format instructions).
- Ground extraction in the repo: take candidate symbols by grepping the summary for names that appear as definitions in the files mentioned (via ctags/ast or simple `def`/`function` regex), so hallucinated symbols are dropped rather than counted.
- Do it in the scorer with a per-arm adapter: leave the arm untouched and convert summary to findings at scoring time. It's less invasive but the arm still "writes no findings", which contradicts the request.
Failure modes:
- Over-extraction inflates "found": the summary mentions files or symbols it merely read or ruled out ("`find_user_sql` is parameterized, fine"), or lists several functions, so false positives get credited and local models look better than agent arms. Negation and context around the mention must matt…
- Schema drift: findings written with different keys, path form (absolute vs repo-relative), or symbol form than the agent arms use, so the scorer's match silently fails and gemma4:12b still gets no credit. Verify against the scorer's matching code, not just against the file's existence.
- Extraction run on the wrong text: Smith's final message can be empty or truncated, or tool-call chatter and a reasoning/thinking block can be mixed in, so the parser sees the wrong content. Gate on the true final assistant message only.
- Test coverage gap: a fixture built from a clean, idealized summary passes while real gemma4:12b output (markdown bullets, backticks, `file:line` suffixes, `Class.method` forms) does not match. The test must use the actual captured gemma4:12b summary for vuln-js.
## Dissent
- [x] rival reading: Likeliest: in the Louhi bench harness's "smith" arm (the local-model arm, likely under `bench/` or a `plugin/lib/` louhi module), parse Smith's final summary text into structured findings `{file, symbol}` and write them in the same format/location the agent arms write, so the existing scorer's "fou… — answered: taken: this is option 1, in _smith_arm after fm code ends
- [x] rival reading: Scoring-side reading: the arm already emits something, but the scorer only reads a findings artifact (e.g. `findings.json`) that the smith arm never produces. The fix is to make the scorer fall back to summary text for this arm instead of changing the arm. — answered: ruled out: grade reads only the arm's answer file and has no end text; the arm is where the text is
- [x] rival reading: Model-side reading: ask Smith to emit a structured findings block (JSON) in its final summary through the prompt, then parse it, rather than extracting free-form prose after the fact. — answered: ruled out: changing Smith's own prompt changes the run being measured; a call after it leaves the run untouched
- [x] rival reading: Narrow reading: only the vuln-js case is broken (e.g. symbol matching is case/format-sensitive such as `find_user_sql` vs `findUserSql`), and the real bug is in matching, not extraction. — answered: ruled out: the arm writes an empty findings list, so matching is never reached for local models
- [x] rival approach: Add an extractor function in the smith arm that runs after Smith finishes: regex/heuristics over the summary for path-like tokens (`\S+\.(js|py|ts)`) and identifier-like tokens near them, validated against files that actually exist in the target repo, then write findings in the agent arms' schema. … — answered: taken in part: the file-must-exist filter is taken; the regex extractor is option 2, ruled out for the false alarms it makes
- [x] rival approach: Constrain the output: append a prompt instruction requiring a fenced `FINDINGS` JSON block, parse that first, and use the heuristic extractor only as a fallback when the block is missing or malformed (small local models often ignore format instructions). — answered: ruled out: same as 3, and a small model ignores a format instruction it was given mid-task
- [x] rival approach: Ground extraction in the repo: take candidate symbols by grepping the summary for names that appear as definitions in the files mentioned (via ctags/ast or simple `def`/`function` regex), so hallucinated symbols are dropped rather than counted. — answered: taken in part: the file must exist in the tree; the symbol is left to the grader's own match, since a filter stricter than the grader would drop near-misses it would credit
- [x] rival approach: Do it in the scorer with a per-arm adapter: leave the arm untouched and convert summary to findings at scoring time. It's less invasive but the arm still "writes no findings", which contradicts the request. — answered: ruled out: same as 2; the scorer has no end text, and the arm would still write no findings
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- decision 2026-10-30: Recommendation: keep the free finders arm as the zero-token per-generation check for the find capabilities; on s0-001 it found 90/108 (held out 30/3…
## Lessons
- An arm graded on findings must be asked for findings: Smith's arm scored found 0 because nothing asked
## Files touched
- plugin/tests/test_exam_smith_findings.py
- plugin/lib/sampo/louhi.py
- plugin/tests/test_exam.py
