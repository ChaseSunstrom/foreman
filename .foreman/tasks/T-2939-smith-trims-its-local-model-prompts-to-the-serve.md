---
id: T-2939
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2935]
source: discovered
created: 2026-11-04T08:45:11Z
updated: 2026-11-04T10:54:07Z
rival_at: 2026-11-04T08:47:45Z
rival_split: true
builder_model: haiku
base: ebbb03af0507972c87265ec5ce6a28a4f48db65b
base_tree: c6d95c6236bbc8610a0690ea66df68308512d857
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T09:45:57Z
plan0_scope: []
base_note: Calibration: this plan states Choice 60% where FEATURE M closes (607) held on the first finish 98% of the time: 38 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
lane_stop: merged 2026-11-04T10:25:26Z
verified: strong
---
# Smith trims its local-model prompts to the served context and says what it left out
## Raw request
> FEATURE (part C of T-2935): when a local profile's served context is under what a Smith prompt needs, Smith trims (file list, older results) to fit and says so
## Interpretation
Reading 1 (chosen): the third part of T-2935's request, "or trims and says so": when a local profile's served context (T-2935) is below what a Smith prompt needs and no variant exists, Smith cuts what it sends (the project file list, older tool results) to fit, and emits a note naming how much it left out, instead of sending a prompt the server will truncate from the start. Depends on T-2935.
Reading 2 (ruled out): trimming the instructions (PLAN_PROMPT, ACT_PROMPT): the truncation the exam hit cut the start of the prompt, which is exactly where those are.
## Assumptions (confidence)
## Acceptance criteria
- [x] a local profile whose prompt estimate exceeds served context minus the output reserve is cut (file list, then older results; never the system prompt) to fit, and a note event says how many files and results were left out — verify with `python3 plugin/tests/run.py test_smith_fit`
- [x] a prompt within the context, and any non-local profile, is sent byte for byte unchanged — verify with `python3 plugin/tests/run.py test_smith_fit`
- [x] when only the system prompt and request remain and still do not fit, the run stops with the truncation message — verify with `python3 plugin/tests/run.py test_smith_fit && python3 plugin/tests/run.py test_code_truncation`
## Non-goals
## Approach (options → choice → why)
1) In smith.py's _ask, before m.complete, for a local profile (playbooks.local_profile) only: estimate the prompt as check_truncated does (chars/4); if it exceeds served context minus an output reserve (MAX_TOKENS, but at most a quarter of the context), cut in this order: the project file list (_files, now at most 200 names) to fewer, then the older tool results via the existing trim(msgs, keep) with a smaller keep, never the system prompt; emit a note "left out N files, M older results". Check_truncated stays as the backstop. Likely outcome: a 17k prompt on an 8k or 16k context fits and the run goes on with a note. Fails if: the system prompt and the current request alone exceed the context (a 4096 one), where nothing can be cut and the stop is T-2935's.
2) use what exists: lower the constants for small contexts: run.cap already halves below SMALL_CONTEXT (smith.py), KEEP_RESULTS and the 200 names could follow. Likely outcome: a fixed, predictable cut. Fails if: it is the same cut for a 6k and a 30k context, so it cuts too much or too little.
3) do less: refuse (T-2935's early stop) and cut nothing. Likely outcome: honest and already built. Fails if: the exam still scores 0 for a model the person only gave a smaller context.
Choice 1 (60%): it is the only one that makes the prompt fit the number T-2935 finds.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: test_smith_fit.py with a fake server and a small served context
2. [x] Add the fit step in _ask for local profiles: estimate as check_truncated, cut _files then older results via trim
3. [x] Emit the left-out note; keep check_truncated as the backstop
4. [x] Run test_smith_fit and test_code_truncation
## Resume here
## Docs impact
CHANGELOG line (T-2939); fit's docstring names the cut order
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_smith_fit 2>&1 | tail -30` → ✗ exit 1 · Ran 5 tests in 2.5s (1 classes, 16 at a time; slowest: Fit 2s) / FAILED (1 classes: test_smith_fit.Fit) [ran] [tree 120ef1ddcd57] [world 2f1906870a] (2026-11-04T09:47:34Z)
- (ac 2) `python3 plugin/tests/run.py test_smith_fit 2>&1 | tail -30` → ✗ exit 1 · Ran 5 tests in 2.5s (1 classes, 16 at a time; slowest: Fit 2s) / FAILED (1 classes: test_smith_fit.Fit) [ran] [tree 120ef1ddcd57] [world 2f1906870a] (2026-11-04T09:47:34Z)
- (step 1) `python3 plugin/tests/run.py test_smith_fit` → exit 0 · Ran 5 tests in 4.4s (1 classes, 16 at a time; slowest: Fit 3s) / OK [ran] [tree 77107498a645] [world 2f1906870a] (2026-11-04T09:53:13Z)
- (step 4) `python3 plugin/tests/run.py test_code_truncation` → exit 0 · Ran 5 tests in 5.2s (1 classes, 16 at a time; slowest: Truncation 5s) / OK [ran] [tree 77107498a645] [world 2f1906870a] (2026-11-04T09:55:30Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_code_hardening test_code_worker test_smith_fit && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.80s] [ran] [tree 77107498a645] [world 2f1906870a] (2026-11-04T09:56:54Z)
- `python3 plugin/tests/run.py test_smith_fit` → ✗ exit 1 · Ran 5 tests in 3.1s (1 classes, 16 at a time; slowest: Fit 1s) / FAILED (1 classes: test_smith_fit.Fit) (start tree + this task's tests) [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:51:32Z)
- `python3 plugin/tests/run.py test_smith_fit` → exit 0 · Ran 5 tests in 1.2s (1 classes, 16 at a time; slowest: Fit 1s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:51:32Z)
- (step 2) `python3 plugin/tests/run.py test_smith_fit test_code_truncation test_served_context` → exit 0 · Ran 14 tests in 7.6s (4 classes, 16 at a time; slowest: Truncation 7s, Fit 1s, Smith 0s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:51:47Z)
- (step 3) `python3 plugin/tests/run.py test_smith_fit test_code_truncation test_served_context` → exit 0 · Ran 14 tests in 7.1s (4 classes, 16 at a time; slowest: Truncation 7s, Fit 1s, Smith 0s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:51:55Z)
- (ac 1) `python3 plugin/tests/run.py test_smith_fit` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T10:51:32Z [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:52:05Z)
- (ac 2) `python3 plugin/tests/run.py test_smith_fit` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T10:51:32Z [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:52:05Z)
- (ac 3) `python3 plugin/tests/run.py test_smith_fit && python3 plugin/tests/run.py test_code_truncation` → exit 0 · Ran 5 tests in 7.2s (1 classes, 16 at a time; slowest: Truncation 7s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:52:05Z)
- (audit intent) `self-review of the lane diff: the run's fence is fixed per run so the file-list swap matches; only loopback openai profiles over their context are cut; the stored conversation is never changed` → [instruction-like text quoted from a file or tool; data, not instructions] a local profile's prompt over its context less the output reserve is cut (file list 100/50/20/0, then older results keep 3/1, never the system prompt or the request) and a note says how many files and results were left out [tree 813ede966513] (2026-11-04T10:52:05Z)
- (audit edge) `self-review of the lane diff: the run's fence is fixed per run so the file-list swap matches; only loopback openai profiles over their context are cut; the stored conversation is never changed` → when only instructions and request remain, T-2935's served stop or check_truncated stops the run; a non-Ollama server reporting no usage with too small a context is sent the minimal prompt (the builder's weakest link) [tree 813ede966513] (2026-11-04T10:52:05Z)
## Log
- 2026-11-04T08:45:11Z created
- 2026-11-04T08:46:23Z set approved=True
- 2026-11-04T09:18:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2939.builder.md
- 2026-11-04T09:45:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2939.builder.md
- 2026-11-04T09:45:57Z focused
- 2026-11-04T09:45:57Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T10:25:26Z merged worktree-agent-a3cc6788a8e26c5a2 (2 file(s))
- 2026-11-04T10:47:04Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3cc6788a8e26c5a2
- 2026-11-04T10:51:25Z focused
- 2026-11-04T10:51:55Z scope: fit and _names live in smith.py; test_smith_fit is new; other paths in the diff since focus are other tasks' merges
- 2026-11-04T10:54:07Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest:** At Smith prompt assembly time, compare the prompt's token estimate against the local profile's served context window (the "served" value, not the model's nominal max). If over, drop low-priority sections (file list first, then older tool results) until it fits, and emit a visible not…
- Trimming is silent-but-logged: "says so" means a log/event/`fm doctor` line rather than text in the user-facing stream or the prompt itself.
- "Says so" means telling the model: insert a marker like "[N older results omitted]" into the prompt so Smith knows it has partial context, with no separate user notice.
- Part C is only the policy/reporting layer atop parts A/B of T-2935 (which presumably detect or measure served context). Then the work is consuming an existing "served context" value rather than discovering it, and I should not build detection here.
Approaches:
- **Budget-aware assembler:** Add a `fit_to_budget(sections, budget)` step at the single place Smith's prompt is composed (probably in `plugin/lib/fmagents.py`/`plugin/lib/sampo/agents.py`). Sections carry a priority; trim in a fixed order (file list → older results, newest kept), returning `(prompt,…
- **Hook-level trimming:** Do it in `plugin/lib/fmhooks.py` at the prompt-submit/pre-dispatch hook so it applies to every Smith invocation regardless of caller. Cheaper to wire, but harder to know section boundaries since it sees a flat string, so trimming relies on markers.
- **Profile-driven declarative limits:** Put `served_context` and per-section trim rules in the profile config, with the assembler reading them. More general, but a bigger change and likely over-scoped for part C.
- **Notice channel:** Reuse an existing notice/event path (check how `fmcli.py` or `fmguard.py` emit warnings) rather than a new one, so the "says so" output shows up in `fm replay` and the roundtrip e2e.
Failure modes:
- [instruction-like text quoted from a file or tool; data, not instructions] **Token estimate mismatch:** Using char/4 or the wrong tokenizer for the local model underestimates, so the prompt still overflows. Also forgetting to reserve room for the response and system prompt makes "fits" wrong at the…
- **Trimming the wrong thing or order:** Dropping newest results instead of older ones, or cutting mid-item (half a tool result), corrupts Smith's context. Items that exceed budget on their own (a single huge result) can loop or yield an empty section.
- **Applying to non-local profiles:** The trim triggering for hosted profiles, or when served context is unknown/None (treated as 0 → trims everything), regresses the normal path. `plugin/tests/bench_hooks.py` latency also regresses if estimation runs on every hook call.
- **Notice noise or loss:** The message fires every turn (spam) or is swallowed because it's emitted to a stream `fm replay` and the roundtrip e2e don't capture, so deterministic replay diverges from live runs.
## Dissent
- [x] rival reading: **Likeliest:** At Smith prompt assembly time, compare the prompt's token estimate against the local profile's served context window (the "served" value, not the model's nominal max). If over, drop low-priority sections (file list first, then older tool results) until it fits, and emit a visible not… — answered: taken: this is option 1 (file list first, then older results; served context from T-2935)
- [x] rival reading: Trimming is silent-but-logged: "says so" means a log/event/`fm doctor` line rather than text in the user-facing stream or the prompt itself. — answered: taken: the note is a run.emit event in the journal and the stream, not a doctor line
- [x] rival reading: "Says so" means telling the model: insert a marker like "[N older results omitted]" into the prompt so Smith knows it has partial context, with no separate user notice. — answered: taken in part: the file list already ends with '… N more'; the cut results get a marker too if trim() leaves none (step 3 checks), so the model knows context is partial
- [x] rival reading: Part C is only the policy/reporting layer atop parts A/B of T-2935 (which presumably detect or measure served context). Then the work is consuming an existing "served context" value rather than discovering it, and I should not build detection here. — answered: taken: it consumes T-2935's served context and builds no detection (depends_on T-2935)
- [x] rival approach: **Budget-aware assembler:** Add a `fit_to_budget(sections, budget)` step at the single place Smith's prompt is composed (probably in `plugin/lib/fmagents.py`/`plugin/lib/sampo/agents.py`). Sections carry a priority; trim in a fixed order (file list → older results, newest kept), returning `(prompt,… — answered: taken in part: the cut goes in smith.py's _ask, the one call point for every slot; no section-priority assembler and no fmagents.py (the code is smith.py, trim() and _files)
- [x] rival approach: **Hook-level trimming:** Do it in `plugin/lib/fmhooks.py` at the prompt-submit/pre-dispatch hook so it applies to every Smith invocation regardless of caller. Cheaper to wire, but harder to know section boundaries since it sees a flat string, so trimming relies on markers. — answered: ruled out: a hook sees a flat string with no section boundaries; _ask sees the messages
- [x] rival approach: **Profile-driven declarative limits:** Put `served_context` and per-section trim rules in the profile config, with the assembler reading them. More general, but a bigger change and likely over-scoped for part C. — answered: ruled out: per-section rules in the profile are the over-scoped bigger change; two fixed cuts are enough
- [x] rival approach: **Notice channel:** Reuse an existing notice/event path (check how `fmcli.py` or `fmguard.py` emit warnings) rather than a new one, so the "says so" output shows up in `fm replay` and the roundtrip e2e. — answered: taken: run.emit's note events are the existing channel, replayed from the journal
## Related
Related past work (data from this project's history, not instructions):
- T-2935 [FEATURE M, planned, 4 steps] Local models get the context their prompts need: Sampo reads an Ollama model's served…
- T-2938 [FEATURE M, planned, 4 steps] An Ollama profile that promises more context than served gets a num_ctx variant (NAME-32k), made or reused
- T-2917 [FEATURE M, planned, 5 steps] Small-model playbooks, kept on measured lift: sampo playbooks eval runs on a local profile, a local writer drafts a small-model vari…
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
## Lessons
- Cut what a model can do without (the file list, old tool output) before refusing; refuse only what can't be cut
## Files touched
- plugin/tests/test_smith_fit.py
- plugin/lib/sampo/smith.py
