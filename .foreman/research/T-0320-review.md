## Verdict
Approve with nits. Nothing blocks. One MEDIUM and two LOW findings, all in snapshot parsing. I did not run the tests.

## Findings
- **MEDIUM** — `plugin/lib/fmbudget.py:103` — `week_gone` is clamped to 0 when `resets_at` is more than 7 days away.
  - The clamp is `max(0.0, 1 - (resets - now)/(7*86400))`. Any such `resets_at` makes the pause threshold `100*0 + 10`, so subagents pause at 10% weekly usage.
  - Failing input: `{"seven_day":{"used_percentage":15,"resets_at":1.8e12}}`, a millisecond epoch. The result is "weekly usage 15% with 0% of the week gone".
  - The same happens with a `resets_at` more than 7 days out from clock skew or a changed window length.
  - Fix: set `week_gone` only when `0 < resets-now <= 7*86400`. Otherwise treat it as unknown, which falls back to the 80% threshold.
  - Confidence: medium. It depends on the statusline ever emitting such a value, but the code trusts any number.

- **LOW** — `plugin/lib/fmbudget.py:98` — `isinstance(True, (int, float))` is true, so `used_percentage: true` reads as 1. It is harmless, but a bool is accepted as a percentage. Fix: add `and not isinstance(used, bool)`. Confidence: high.

- **LOW** — `plugin/lib/fmbudget.py:100-101` — a window with no `resets_at` never reads as reset.
  - Failing input: an old snapshot `{"five_hour":{"used_percentage":95}}`. It pauses subagents until a newer snapshot is written. The old code behaved the same way, so this is not a regression.
  - Fix: use the snapshot file's mtime as a staleness cap, for example ignore it after 5 hours.
  - Confidence: medium.

## Cases I checked that hold
- String percentages such as `"95"` are skipped, which means unknown, so no pause.
- NaN used or NaN `resets_at` never pauses.
- A non-dict window raises `AttributeError`, which is caught.
- A reset weekly window reads 0, so the economy halving in `usage_high` also ends. That is the intended change.
- Week end: `gone`→1 gives `min(90, 110)` = 90, which matches the "never past 90%" rule.
- Week start: `gone`≈0 pauses at 10% weekly usage. This is by design and documented.
- A stored `budget.json` that still has `subagent_tokens` is ignored on read. `set_caps` drops the key on the next write.

## Acceptance criteria
1. Pause only at 5-hour ≥90% or weekly ahead of pace: met by `subagent_pause` (`fmbudget.py:194-203`). The new `test_subagents_follow_the_weeks_pace` covers on-pace, ahead of pace, over 90%, a reset window and unknown usage. It has no test for malformed `resets_at`, which is where the MEDIUM sits. I did not run it.
2. `fm budget`, `fm ui` and the pane show subagent tokens without a cap: met by the `cmd_budget` lines, the `fmwatch._budget` payload and the `register.tsx:1298` header. The `test_ui.py:69` assertion on `subagent_tokens` still matches the payload. Not run.

## Operator
- `fm budget set --subagent-tokens N` is now an argparse error. Any script or user habit that uses it breaks. The CHANGELOG says so, so I count this as acceptable.
- The foreman-ui version bump to 0.6.1 appears in both `plugin.json` and `marketplace.json`. No further edit is needed there.
- `fmhooks.py` only changed a comment, so it needs no test edit.

## Not checked
- I did not run the test suites.
- I did not check what format the statusline actually writes for `resets_at`.
- I did not check whether `fmwatch._budget` wraps `subagent_pause` in a try/except.
- I did not do the maintainer or adversary lenses in depth.
