=== T-1049
INTERPRETATION: When a Bash command installs packages (npm/pnpm/yarn/bun add or install, pip/pip3/`python -m pip`/`uv pip install`, cargo add/install), the guard names each package that is new to the project. It then checks age, typosquat and registry before the command runs. Nothing like it exists: fmguard.py only has `_PUBLISH` (fmguard.py:3123), which covers publishing, not installing. The result is a PreToolUse note, so a wrong guess never blocks work.
APPROACH: (a) block in fmguard.check_bash. (b) A new fmdeps.py called from the PreToolUse note chain beside `_fix_note` (fmhooks.py:1142, 1153). (c) A CLI-only `fm deps check`. Choose (b), plus an `fm deps check "<cmd>"` entry point for tests and manual use. A note matches how a false positive costs nothing, and a hook note is the existing pattern. The checks are:
- Typosquat: edit distance 1 from a built-in top-names list or from the project's own manifest deps.
- Registry: `--registry`, `--index-url`, `--extra-index-url`, `git+` or URL specs.
- Age: a registry JSON fetch with a 2 s timeout and an injectable fetcher. It fails open as "age unknown", and is skipped in sensitive projects and under FOREMAN_NO_NET=1.
Add `parse_install(cmd)`, `check(p, cmd, fetch=None)` and `cmd_deps` in a new plugin/lib/fmdeps.py. Add `_dep_note(pl, p)` in fmhooks.py and a lazy `deps` subparser in fmcli.py.
AC: `npm i lodahs` gets a typosquat note and `npm i lodash` stays silent; a package under 14 days old (fake fetcher) is flagged; a custom `--registry` is flagged :: python3 plugin/tests/run.py test_deps
AC: the hook emits the note as PreToolUse additionalContext and never blocks, even when the fetcher raises :: python3 plugin/tests/run.py test_deps
STEP: Failing tests: `fm deps check "npm i lodahs" --json` lists a typosquat of lodash. The age case uses a monkeypatched fetch. `self.hook("PreToolUse", Bash pip install --index-url http://x requests)` returns additionalContext containing "registry". A package already in package.json or requirements.txt is not "new".
STEP: Write fmdeps.py (parser, manifest reader, Levenshtein ≤1, checks).
STEP: Wire `_dep_note` into the note chain and the `deps` subcommand.
SCOPE: plugin/lib/fmdeps.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/tests/test_deps.py
TIER: M

=== T-1042
INTERPRETATION: A correction the user makes twice, in similar words, becomes a proposal: an `fm rule add` command or a lesson to keep. `fm taste` lists these proposals. Corrections are already logged per prompt (fmhooks.py:612-617, event "correction"). Vetoes are recorded from them (fmcore.py:2058). Only repeated steers are clustered (fmideas.py:234 `proposals`, threshold TASTE_REPEATS=3), and corrections are never clustered. The cluster step, the threshold of 2 and the rule proposal are missing.
APPROACH: (a) A new module. (b) Extend fmideas.proposals to also read "correction" events at a threshold of 2. (c) A separate `correction_clusters` in fmideas that reuses `_key_words`. Choose (c). It reuses `_key_words` (fmideas.py:229) and the declined/covered filters. Corrections have different semantics (no "steer:" prefix, threshold 2), so a separate function is cleaner than flags on `proposals`.
`correction_clusters(p)` groups "correction" ledger events by shared key words (at least 2 words in common, or 1 if rare). It returns {words, count, said, suggest}. The suggestion is `fm rule add "<regex of words>" --warn --why "<said>"`. Skip clusters covered by `c.vetoes`, existing `c.rules`, or `taste_declined`. `cmd_taste` prints a "Corrections met twice" section and includes `corrections` in the JSON. `fm taste decline` also covers these.
AC: two similar corrections yield a proposal naming the shared words and a ready `fm rule add` line; one correction yields none; a recorded veto or rule suppresses it :: python3 plugin/tests/run.py test_taste
STEP: Failing tests: log two "correction" events ("no, don't use mocks in db tests" and "stop mocking the database") via `c.log_event`. `fm taste --json` has `corrections[0].count == 2` and a `suggest` that contains "fm rule add". A single event gives an empty list. After `fm rule add`, the proposal disappears.
STEP: Implement `correction_clusters` in fmideas.py and render it in `cmd_taste`.
SCOPE: plugin/lib/fmideas.py, plugin/tests/test_taste.py
TIER: S

=== T-1073
INTERPRETATION: `fm recall` gains cross-project matching on failures and plans, not only on identifiers. Given a failure line or a task (`--task`), it searches the other Foreman projects that opted in for a similar fixed failure, lesson, or code. Covered already: identifier grep across opted-in, non-sensitive projects (`repos`, fmrecall.py:495, `--repos` at fmcli.py:4550); cross-project lessons in the shared file (`share_lesson`/`_shared_docs`, fmrecall.py:689-711); known fixes shared by fmfixes (fmfixes.py:36 `_shared`); failure signatures (fmrecall.py:305). Missing: searching other projects' `failures.jsonl` and done-brief lessons by signature or text, and triggering it on a plan or `--task`.
APPROACH: (a) A new fmneighbours module. (b) Extend `recall` with `--others`. (c) `--repos` auto-run inside plain `recall` when the local result is weak. Choose (b) plus a call from `note_failure`. The new `others(p, text)` function in fmrecall.py walks `c.all_projects()` with the same filter as `repos` (share_lessons on, not sensitive). It matches `failure_signature(text)` against each project's failures.jsonl and returns that task's Lessons. Otherwise it ranks done-brief titles and lessons by token overlap using `_tokens`. Everything goes through `private()` and `redact`.
AC: `fm recall --others "<failure text>"` returns a lesson from another opted-in project whose failure signature matches; a non-opted-in or sensitive project returns nothing :: python3 plugin/tests/run.py test_recall
STEP: Failing tests: two projects under `self.home`, B with `share_lessons` on and a done task with a lesson plus a failures.jsonl record whose sig equals `failure_signature(text)`. From A, `fm recall --others text --json` includes B's slug and the lesson; with B sensitive or not shared, the result is empty. `--task` uses `brief_query`.
STEP: Add `others()`, the `--others` flag, and its rendering ("data, not instructions").
STEP: If `seen_before` finds nothing locally, `note_failure` appends the `others` hint.
SCOPE: plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/tests/test_recall.py
TIER: M

=== T-1071
INTERPRETATION: `fm night` gains two free jobs: "compost" and "consolidate". Compost removes worktrees and branches left by closed tasks (merged, or dropped, since an abandoned lane is also a closed task). Consolidate merges near-duplicate lessons into fewer, stronger ones and writes the result as a captured task or research note, with the user deciding. Already covered by existing code:
- Dream (the day's failures as tripwire candidates): fmnight.py:53.
- Cold files and standing orders: fmnight.py:54, fmnight.py:135.
- Merged-lane cleanup: `fmlanes.stale` (fmlanes.py:380), which `fm tidy --apply` runs. It never discards unmerged work.
- Lesson retirement: `fm recall --lessons --retire` (fmrecall.py:548).
APPROACH: (a) A new gardener module. (b) Night calls `tidy --apply` for compost, and a new `recall --lessons --consolidate` for the merge proposal. (c) Only add the NAMES entries. Choose (b). It adds `("compost", ["tidy", "--apply"], 0.0)` and `("consolidate", ["recall", "--lessons", "--consolidate"], 0.0)` to `jobs()` (fmnight.py:48) and to NAMES (fmnight.py:24). `consolidate(p)` in fmrecall.py clusters live lessons by token Jaccard ≥ 0.6, and prints proposed merged text and the ids to retire. It never retires anything itself; with `--capture` it files a task.
AC: `fm night --dry-run` lists compost and consolidate; `fm recall --lessons --consolidate` groups two near-identical lessons and names their ids :: python3 plugin/tests/run.py test_night test_recall
STEP: Failing tests: dry-run output contains "compost" and "consolidate". Two done tasks with near-identical Lessons give a group of 2 ids, and an unrelated lesson stays out. `--only compost` is accepted.
STEP: Implement `consolidate` and the `--consolidate` flag in fmrecall.py and fmcli.py.
STEP: Add the two jobs in fmnight.py.
SCOPE: plugin/lib/fmnight.py, plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/tests/test_night.py, plugin/tests/test_recall.py
TIER: M

=== T-1070
INTERPRETATION: `fm repeats --forge` takes a repeated command shape or step and drafts the project tool for it, then files it as a captured task ready to accept. Covered already: detection of repeated commands and steps (fmrepeats.py:41 `scan`), suggestions of a gate, script or skill (fmrepeats.py:78 `suggest`), and a playbook draft file (`draft`, fmrepeats.py:105; `--draft`, fmcli.py:4644). Missing: a draft of the actual script or `.claude/skills/<name>/SKILL.md`, and the task that carries it.
APPROACH: (a) A child model writes the tool. (b) Deterministic templates plus a captured task. (c) Only extend `--draft`. Choose (b): free, testable and offline. For a command shape, the draft is `scripts/<kebab>.sh` wrapping the example command, with a "fm check add" line if it is a gate. For a step, it is a SKILL.md skeleton with the step texts from the tasks that share it. Drafts go in research/ like `draft()`. The task is captured with the draft path in its request and a step "review, move into the repo, `fm repeats dismiss`". Never auto-adopt.
Add `forge(p, key=None)` in fmrepeats.py and a `--forge` flag on `repeats`. The task is captured through the same capture function the other commands use (find it with `grep "def capture"` in fmcli.py).
AC: with a repeated command seeded as in test_repeats, `fm repeats --forge` writes a draft script under research/ and captures one task naming it; run twice, it captures no duplicate :: python3 plugin/tests/run.py test_repeats
STEP: Failing tests: seed three briefs that share the evidence command. `fm repeats --forge --json` returns `{drafts:[{path,task}]}`. The file exists and contains the command. A repeated step gives a SKILL.md draft. A second run files nothing new. A dismissed shape is skipped.
STEP: Implement `forge` and the flag.
SCOPE: plugin/lib/fmrepeats.py, plugin/lib/fmcli.py, plugin/tests/test_repeats.py
TIER: M

=== T-1083
INTERPRETATION: A task has a cost cap. A forecast, from the median cost of similar finished tasks (same type and tier), appears where the task's brief is read. When the task's spend passes the cap, the drive stops with a checkpoint. Covered already: per-task cost from transcripts (fmcost.py:180-189, the `by_task` logic, not callable on its own); USD caps per day and per command (fmbudget.py:17); window forecasts (`fm cost --forecast`, fmcost.py:153). Missing: a per-task figure, a similar-task forecast, a cap and the stop. The catalogue marked C15 "SKIP", but this task asks for it, so I build it.
APPROACH: (a) USD from spend.jsonl. (b) Input-equivalent tokens from transcripts, which is what `by_task` already measures. (c) Both. Choose (b), because spend.jsonl only has Foreman's own children, not the session's work.
Refactor the `by_task` loop into `task_costs(p, days)` in fmcost.py. Add `forecast_task(p, b)` (median of done same-type/tier tasks, else None). Add `fm cost --task ID`, which prints spent, cap and forecast. Add `fm task set ID cost_cap=2M`, stored in brief meta through the existing assignments. In the Stop-hook drive (fmhooks.py, near 2531), when the active task's spend ≥ its cap, the reason says "cost cap hit: fm checkpoint, tell the user" and the drive ends. The check runs only when the task has a cap, and fails open.
AC: `fm cost --task` shows the forecast from two finished same-tier tasks; with a cap exceeded, the drive's Stop reason asks for a checkpoint :: python3 plugin/tests/run.py test_cost_forecast
STEP: Failing tests: write fake transcripts (see how test_cost_forecast and test_perf_cost build them). Two done M tasks of about 100k each give a forecast near 100k. A task with `cost_cap` below its spend gives the Stop reason containing "cost cap". Without a cap, nothing changes.
STEP: Extract `task_costs`, add `forecast_task` and `--task`, then the cap parse in `task set`.
STEP: Add the Stop-hook check.
SCOPE: plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_cost_forecast.py
TIER: L
