**Verdict: changes needed.** One MEDIUM bypass of the guard (in code from T-1496, which the new command calls through) and one MEDIUM test gap. I could only read code, not run tests or the engine.

## lens: adversary
- MEDIUM — plugin/lib/fmsettings.py:357,433 — `/foreman:settings set` can write settings.json without the guard's check. `in_claude_code()` reads only `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT`, and `set_plugin` skips `_guard_block` when both are empty. fmguard.py has no rule on `fm settings set` or on blanking those variables. A Bash call like `CLAUDECODE= CLAUDE_CODE_ENTRYPOINT= fm settings set motion off --surface plugin` therefore goes through `_write_plugin` (:443-451) and rewrites the whole settings.json. The damage is bounded because the key must be a foreman-ui option and the value is schema-checked. The new settings.md:13 ("the guard decides writes") is only true while that env is set. The lane did not touch fmsettings.py. Fix: fail closed (guard unless a positive interactive-terminal signal such as `sys.stdin.isatty()`), or add a guard rule for `fm settings set` when `CLAUDECODE` is blanked. Confidence: high on the code path, not run.

## lens: edge
- LOW — mods/foreman-ui/hooks/register.tsx:292-295 — `$.config.list()` is called bare. A rejection is caught, but if `$.config` is absent on an older engine it throws a TypeError. The throw happens inside `void tick($)` before the shell, agent and watch-path work (:311 onward), so that work stops on every poll. Fix: run the options block in its own `try/catch`, or in a helper with `.catch(() => undefined)`. Confidence: plausible. I couldn't find `config.list` in the mod's local types (types/index.d.ts), so engine support isn't confirmed here.
- LOW — register.tsx:303-308 — the first tick only records the baseline and never applies. A change made between `register` and the first poll (up to 2 s) is silently adopted without being applied. Fix: seed `seenOptions` from `startOptions` at register, or apply on the first tick.
- LOW — register.tsx:450 with :478-487 — lowering motion mid-work cancels `motionClock` on its next fire (≤33 ms), which is correct. The 8 fps `clock` keeps redrawing for as long as `starts.size` is non-zero, because `advance` refreshes `lastActive` on every frame. `moving` is false, so the frames are static, but the "off = no clocks" comment at :570 doesn't hold until the tool call ends. Fix: in `tick`, call `sleep()` when `cfg.motion` has become `'off'`.

Not a finding: the poll is one timer, cancelled before it is re-created (:596-597), so it doesn't leak. Re-apply happens only when the JSON string changes (:303).

## lens: maintainer
- MEDIUM — mods/foreman-ui/tests/foreman-ui.test.tsx:1568-1580 — the new test can't catch the new `|| cfg.motion !== 'full'` check at register.tsx:450. Motion is already `'off'` before any work starts, so `motionClock` is never created. Reverting that line leaves the test green. Fix: start work with motion `'full'` and assert blits occur, then flip to `'off'` and assert no more blits arrive.
- LOW — plugin/tests/test_settings.py:150-157 — `test_the_pane_applies_changed_options_on_its_poll` only checks that source strings exist, including the test's own title. The acceptance command (`python3 -m unittest test_settings.PluginSurface`) passes even if the tsx behaviour test is broken or never run. Fix: say so in the criterion, or have the unittest run the mod's test runner.
- LOW — plugin/lib/fmsettings.py:108,509,545 — fm still prints "next Claude Code session reads it" and "next session" for pane options. settings.md:15 now says "within a few seconds". Fix: update the effect text.

## Acceptance criteria
- Command file exists and runs `fm settings list`: met (plugin/commands/settings.md:10; frontmatter matches the build.md convention).
- Pane picks up a changed motion or palette on the next poll in the mod's tests: partly met. The tsx test fails if the `tick` block is removed (palette colour changes after one 2 s advance), but the motion half doesn't cover the mid-work case, and the Python command doesn't run the tsx test.
- Whether a real Claude Code `config.list` reflects an `fm`-written settings.json: not verifiable. The test mocks `config.list` directly.

## Implicit decisions
- Options are re-read from `config.list` at a fixed 2 s cadence, with keys matched by `foreman-ui(@x)?.name`.
- `startOptions` stays as the base layer under whatever `config.list` returns.
- A removed row falls back to the starting value, not to the default.
- The command was made user-only with `disable-model-invocation: true`.

## Not checked
tsc types, running either test suite, the engine's `config.list` semantics, the CHANGELOG hunk, and the three hunks you said to ignore.

Noticed: fmsettings.py `in_claude_code` is detectable-by-env only, so it deserves its own guard task (see the adversary finding).
