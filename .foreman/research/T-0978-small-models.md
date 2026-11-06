# T-0978: small and local models on Foreman — what they trip on

Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one
`fm bench stranger --model haiku` run, and one headless Haiku session (`claude -p --model haiku`, bypassPermissions,
$3 cap, 25-minute timeout) working a real FIX in a scratch clone with its own Foreman state: "fm next's due-back line
for a 'when PATH changes' deferral suggests --until <date>; it should name the file trigger". No local model or
harness is installed here (no ollama, opencode, aider, codex or gemini), so Haiku stands in for "small": the fixes are
all in Foreman, so they help any model.

## Outcome

- Haiku read `fm next`, made a correct brief in one `fm task new` call (type, tier, `--ac` with a `::` verify, a
  step), wrote the failing test beside the existing one, saw it red, wrote a correct 3-line fix, saw it green, and
  recorded the green run. Then it ran the whole suite serially (`python3 -m unittest discover`, 1,537 tests: ~20
  minutes this way, 110 s through the repo's parallel runner) and timed out before closing. Not committed.
- Its fix was right; harvested as T-0986 (committed).
- `fm bench stranger --model haiku`: 0 findings at $0.0086. Uninformative: the stranger pass is too short to stumble.

## Stumbles, causes, fixes

| # | Stumble (who) | Cause in Foreman | Fix | Status |
|---|---|---|---|---|
| 1 | Dropped and redid T-0001 after a criterion's verify path was wrong (both Sonnet sessions) | a criterion whose check never ran was locked like one that ran and failed | never-ran checks stay editable with `fm task ac edit` | done T-0985 |
| 2 | Used a task id from the main repo inside the clone (Sonnet) | ids are per-project; the refusal said only "no task T-0983" | the refusal names the active and newest open ids here | done T-0987 |
| 3 | Saw red in raw output but never recorded the failing run, so a FIX can't prove red→green at close (Haiku) | nothing at edit time said "record the failing run" | test-first note on the first source edit (the clone predates it) | done T-0969 |
| 4 | Ran `unittest discover` (serial; import errors from the repo root) instead of the repo's runner `plugin/tests/run.py` (Haiku) | fresh state, no checks; `fm check`'s first-run hint came from fmmap gate detection, which didn't know a repo's own runner script | gates offer `tests/run.py` / `run_tests.py` first | done T-0987 |
| 5 | The serial suite in the foreground hit its own `timeout 550` (9 min lost) | no hint that the suite is long | covered by #4 (the runner is parallel, ~2 min) and the existing affected-tests path; a duration note needs a recorded gate time a fresh project doesn't have | skip (covered) |
| 6 | Polled with `for i in $(seq 1 110); do …; sleep 5; done` for 9 minutes (Haiku) | the wait-loop refusal matched `until`/`while`, not `for` | `for` polls are refused the same way | done T-0987 |
| 7 | `git stash` while its own background suite ran in the tree, then `pkill -f` to restart it (Haiku) | the guard doesn't know a background test run reads the tree | none: rare and self-inflicted; the stash was restored | skip |
| 8 | Monitor called with string-typed params, `(…) &` exit 144, a blocked `sleep 500` (Haiku) | Claude Code's tool surface, not Foreman | none | skip |

## Bottom line

A small model follows Foreman's loop when each next step is one exact command. It stumbles where Foreman leaves a gap
it fills from general knowledge: which test command, how long it takes, when to record a run, which ids exist. Closing
those gaps with exact commands in the refusal or note is cheaper than more instructions, and it helps every model.

Next probe (when worth the spend): re-run the same task with Haiku on the current tree and compare time-to-close.
