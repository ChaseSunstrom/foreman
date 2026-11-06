**Verdict: changes needed.** The Stop-hook change and the exam re-ask look sound. The user's stated goal is not met, and the re-ask trigger is weaker than the criterion it implements.

## lens: intent
- MEDIUM — plugin/lib/fmhooks.py:928 — The user asked for the session to find "at least what the finders find". The changelog reports 15/18 against the finders' 16/18, and the question whether 8 leads per scenario was the cap that cost them is not answered in the diff. `LEADS = 8` is unchanged and no per-scenario leads-vs-findings analysis is in the diff. — Either state which scenario still misses and why the cap is not the cause, or raise `LEADS` and re-smoke. Do not call the gap closed at 15/18. — 70%

## lens: edge
- MEDIUM — plugin/lib/fmexam.py:853 — The re-ask fires on `not re.search(r'"findings"\s*:', said)`, but the criterion is "no findings object". Two replies slip past it and are graded as empty with no re-ask:
  - A truncated or invalid JSON object, such as an unescaped quote in `says`, still contains `"findings":`.
  - A prose mention such as "I'll end with {"findings": …}" does too.
  - `_reply` (fmexam.py:819) parses the reply and returns empty for both. Re-ask when no parsed dict has a `findings` key, sharing the parser with `_reply`. — 85%
- LOW — plugin/tests/test_exam.py:254 — Only the happy re-ask path is tested. Nothing covers the three cases that skip the re-ask (first turn errors, no `session_id`, JSON already present with a bad parse) or a second turn that errors. Add a stub mode for each. — 70%

## lens: operator
- LOW — plugin/lib/fmexam.py:851 — `keep=True` now applies to every session arm, so every scenario leaves a persisted transcript in `~/.claude/projects/` keyed to a temp dir. Before this change they ran with `--no-session-persistence`. — Remove the transcript after the arm, or accept the 30-day cleanup and say so. — 60%
- LOW — plugin/lib/fmexam.py:885 and plugin/lib/fmbench.py:369 — `--max-budget-usd` applies per invocation, so a scenario can now spend up to 2× `budget`. `fmbudget.estimate` still assumes one turn per scenario. The reply-with-no-JSON rate is unknown, and it was probably high on Rust. — Estimate at 1.5× or document it. — 60%
- LOW — plugin/rules/foreman.md:3 and 5 eval prompts — The hint "(long: `fm outline` it or Read with an offset)" is removed. No step, test or changelog line mentions it. MASTER.md is 315 KB, so sessions now lack the cue not to read it whole. — Restore it, or log why it was cut (rules size?). — 65%

## lens: adversary
Ok. The new strings are constants. `said` is redacted, capped at 400 characters, and has no consumer that feeds it to a model. Lead rows stay JSON-quoted.

## lens: maintainer
- LOW — plugin/lib/fmhooks.py:3281 — This repeats the `sdk-cli` environment check that `_headless()` (3426) and `_oneoff()` (3449) already do. A drive run (`FOREMAN_DRIVE_TASK`) is covered only if the entrypoint is also set. — Use or extend one helper. — 50%
- LOW — The mail hold at fmhooks.py:3296 gets the suffix, but no test covers it. The tests cover the drive and test-failure holds, and assert interactive gets none.

## Acceptance criteria
- Re-ask resumes once, counts both turns' cost, and keeps the reply tail and the `reasked` flag: **met** (fmexam.py:851-860; test_exam.py:254). The trigger is weak (see edge).
- Haiku smoke on s31-006: **not verifiable** from the code. The changelog says 15/18 found. The recorded per-scenario leads-vs-findings diff is not in the diff.
- Every `claude -p` Stop hold ends with the whole answer, and interactive holds don't: **met** (fmhooks.py:3277-3283; tests at test_hooks.py:1020, 1033, 2289).

## Implicit decisions
- The re-ask applies to every session arm, not only the foreman arm.
- A single re-ask, with `AGAIN` as a fixed prompt.
- Print mode is detected only by `CLAUDE_CODE_ENTRYPOINT=sdk-cli`.
- The leads text now directs sessions to write tests for untested leads.
- `LEADS` stays at 8.

## Not checked
MASTER.md (the diff left it out as generated), the live Haiku smoke numbers, and whether the claude `total_cost_usd` on a resumed turn is per invocation. It is summed that way in `soak_case` (fmbench.py:665).

**Noticed:** `fm exam` scorecard does not show `reasked` or `said`, so the lost-answer rate is not visible without opening the answer files.
