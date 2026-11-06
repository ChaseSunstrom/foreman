**Verdict: changes needed.** I found one regression: a command the old code refused and the new code lets through. I read the code and did not run anything.

## lens: adversary

- HIGH — plugin/lib/fmguard.py:683,719-720 — A real `$IFS` that arrives through eval text is no longer seen by the IFS rule. `_IFS_PLAIN` now skips `\$IFS`, and `live` strips `\$`. Eval strips that backslash at run time, so the expansion is real. The IFS rule is meant to refuse exactly this: a second eval reads `$IFS`, and the first eval set IFS where the guard can't see it. — Fix: add a case for it. Where the text is not masked and `_RUNS_HERE` found an eval or source (`hidden` is true), read `\$` as a possible expansion again. Concretely, set `live = text` when `hidden`, instead of stripping `\\.`. Eval text is the one place `\$` is not literal. — confidence: medium-high.

  The command is `eval 'IFS=n'; eval "\"shutdow\$IFS\" now"`.
  - Bash runs the first eval, so IFS is `n`. The second eval receives `"shutdow$IFS" now`, which is `shutdown now`.
  - Old code: `_IFS_PLAIN` matched `$IFS` inside `\$IFS`, so `plain and hidden` were both true and line 712 returned the "IFS may be changed…" refusal.
  - New code (the walk-through is in the next paragraph):
    - `_IFS_PLAIN` finds no match, so `plain` is False.
    - `hidden` is truthy because `; eval ` matches `_RUNS_HERE`.
    - Line 718 finds the `IFS` name inside `'IFS=n'`, because `text` is unmasked when `hidden`.
    - `live` becomes `eval 'IFS=n'; eval "shutdowIFS now"`. It has no `$` and no backtick, so `split` is False and line 725 returns None.
  - Nothing else refuses it, as far as I can read:
    - `_line_literals` ignores the quoted `IFS=n`, so `_readings` never substitutes `n`.
    - The nested text `"shutdow$IFS" now` has a computed command word, and line 2878 checks it only as `_COMPUTED_AS` (rm, git, claude, dd, systemctl, cryptsetup, direnv, init and the publish tools).
    - `shutdown` is not in that list. The comment at 4350-4352 says a bare `$X` that is shutdown stays unread.
  - Don't use `IFS=n eval "…"` as the reproducer. `_LIT_ASSIGN` records the prefix assignment, `_readings` substitutes it, and that reads as `"shutdown" now`.

  The same hole applies to any destructive command outside `_COMPUTED_AS` whose name is built from `$IFS`. An unquoted heredoc is a second route to the same result: `. /dev/stdin <<EOF` with `\$IFS` in the body.

  The rm form, `eval 'IFS=m'; eval "\"r\$IFS\" -rf ~"`, is still refused. The computed-name path checks the nested `"r$IFS"` as rm and returns `rm-outside`.

  Add a test to `SeparatorProse` for `eval 'IFS=n'; eval "\"shutdow\$IFS\" now"` that expects a refusal.

No problems found in the cases below:
- **Odd and even backslash runs:** `\$IFS` is literal and `\\$IFS` is a real expansion. I checked runs of 1, 2, 3 and 4, and the regex gets all of them right.
- **Backslash in single quotes:** `'\'$IFS` has a `'` before the `$`, so it matches as an expansion and the guard stays strict. A literal backslash can't sit directly before a real `$`, because a quote must come between them.
- **`\$` inside backticks:** the backtick is still in `live`, so `split` stays True.
- **Line continuations:** `_join_continued` joins them before this code runs.
- **`$'` in `_mask_quotes`:** `_decode_ansi_c` has already rewritten real `$'…'` at line 2632. The change loses nothing there, apart from the unreviewed heredoc-body case below.

## Acceptance criteria
Not verifiable from the code, and I could not run the tests. The criteria say a quoted argument naming eval, IFS and `$` passes, and that `"eval" 'X=…'` and the existing IFS cases still block. The finding above is a case those tests don't cover.

## Implicit decisions
- An escaped `\$` counts as literal everywhere, including in unmasked eval and source text.
- `live` strips every `\\.` pair, whatever quote state the pair was in.

## Not checked
- The playbook checklists. I reviewed through the adversary lens only.
- The interaction.md hunk.
- Heredoc bodies that contain `$'` or an apostrophe, now that `_mask_quotes` no longer fails closed on them. I only saw that `_ifs_unreadable` strips heredocs first.
- Whether other checks refuse commands outside `_COMPUTED_AS`, apart from shutdown.

Noticed: the `eval 'IFS=…'; eval "…\$IFS…"` form has no test in test_guard.py or test_guard_pipes.py. Lines 960-961 cover only the unescaped forms.
