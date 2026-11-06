**Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in the acceptance criteria are untested. The Python core looks correct. All the findings are MEDIUM or LOW, and none is a blocker.

## intent: ok
- LOW — `CHANGELOG.md:36`, `fmcore.py:772` — The brief lists T-0074/76/80/81/83, but the changelog and `keep_ticks` also cite T-0075, and the diff adds the T-0084 mod, `install.sh`, `uninstall.sh` and the marketplace entry. Nothing is missing. Fix: say in the task log that T-0084 and T-0075 ride along.
- LOW — The acceptance criteria don't cover the mod (`mods/foreman-ui/tests` isn't in the full-suite command) or `install.sh`/`uninstall.sh`. Fix: add a criterion or a separate T-0084 brief.

## adversary: changes needed (MEDIUM)
- MEDIUM — `fmcore.py:806,815` — The string-literal stripper also hides code inside f-strings and template literals. `+x = f"{eval(user)}"` becomes `x = ""`, so `sensitive()` returns `[]` and the adversary lens isn't forced. The new `ponytail:` note only covers multi-line strings. Fix: skip stripping on lines whose literal has an `f`/`rf` prefix or `{`, or at least add a failing test and document the gap.
- LOW — `fmcore.py:775` — `keep_ticks` matches on text only. Reordering or inserting criteria moves a tick to a new number while the evidence stays keyed to the old number (`_EV_RE`, `fmcore.py:762`). `done_blockers` (`fmcore.py:881-883`) checks only the tick, so there is no new hole. Fix: none needed; optionally drop ticks when the number changes.

## edge: ok
- LOW — `fmwatch.py:898` — `watch` is `p.dir` and `p.dir/tasks`. A directory's mtime moves on `write_atomic` renames but not on ledger appends. `recent` and `health` can lag up to 30 s (`register.tsx:236`). Fix: add the ledger file to `watch`.
- No-project case: `cmd_ui` returns `{"v":1,"project":null}` without creating state, and `add()` supplies `--json` (`fmcli.py:1330`).

## operator: changes needed (MEDIUM)
- MEDIUM — `install.sh:71` — Every run of `install.sh` now installs a second user-scope plugin without asking. It does degrade gracefully, but this is opt-out. Fix: gate it behind a flag or prompt, or print clearly that it was installed.
- LOW — `marketplace.json` — `foreman` stays at 1.1.0 although `plugin/lib` changed. This is the pre-audit item, and it's fine only if versions are bumped at release.
- Pre-audit: the `fmhooks.py` companion edits for `fmcore.py` and `fmwatch.py` are not needed. These changes add no hook behaviour.

## maintainer: ok
- LOW — `fmwatch.py:889` — `view()` re-reads all briefs for `load_briefs` and `gather`, and the mod spawns it on every change. This is acceptable for now. Fix: only if latency shows up in `health.hook_p95_ms`.
- The tests assert behaviour and cover every change. `brief_detail` reuses `brief_summary`, and `recent_hook_errors` was extracted rather than duplicated.

## T-0084 (mods/foreman-ui)
- MEDIUM — `register.tsx:317-323` — A one-key `y` hotkey approves a plan after showing only its title, and Full auto (`:462-470`) is likewise one press. Plan approval is the user's consent gate. Fix: make Approve open the pane first, or require a second press.
- MEDIUM, unverified — `register.tsx:320,327,332` — The bare hotkeys `y`, `n` and `f` on a band above the prompt may fire while the user types. Fix: confirm the hotkeys need focus or a modifier in the Claude Code build, or add a modifier.
- LOW — `register.tsx:167-170` — `closed` is the newest 5 by `updated`. Editing an older closed task makes it reappear, and the mod fires a bogus "✔ T-x done" toast. Fix: toast only for ids that were not closed in the previous snapshot's full status.
- LOW — `register.tsx:181` — `guardReason` matches `Foreman:` in any `isError` tool text, so a file or output containing that string triggers a ⛔ toast. Fix: match only on `deny`, or anchor the pattern.
- LOW — `register.tsx:253` — `clock.every` is registered on every `session.start`. A repeat start would stack timers. Fix: keep the timer handle and clear it first.
- LOW — `register.tsx:355` — Titles are rendered raw. Whether control characters survive depends on the renderer, and `fm` runs `c.plain` only on the approvals text. Fix: apply `c.plain` to titles in `view()`.
- There are no rules or gates in the mod. The argv-array calls are shell-injection safe.

## Acceptance criteria
- Round I behaviours: not verifiable by running, but met by the code and `test_round_i.py`.
- `fm ui --json` and `task show --json`: met by the code and `test_ui.py`.
- Full suite green: not verifiable here.

## Not checked
- Test execution.
- The `claude-code` mod API semantics (hotkeys, `$.ui.*`).
- The `install.sh` and `uninstall.sh` round trip.
- The `fmdoctor` refactor beyond reading it.
