## adversary: ok

No bypass found.
- `--run` on `fm task assume ID verify` goes through the guard's generic `--run` scan at `plugin/lib/fmguard.py:1297-1300`, so those commands get the same checks as typed ones.
- `[inconclusive]` can't be forged through typed text. `_unmarked` now blocks it at `plugin/lib/fmcore.py:659`, and `_ledger` applies it to assumption text and "how".
- Dismissed: the `_NO_TESTS` substring match from past findings is not touched by this diff.

## intent: ok (one gap)

- LOW — `plugin/lib/fmcli.py:548-551` and `plugin/lib/fmserve.py:243`. `b.evidence()` now hides inconclusive lines, so a task whose only evidence is inconclusive looks "never started" to `fm batch` and `drop --done-in`, which is arguably right. `fmserve.py:243` counts raw "\n- " lines in the section, so it counts inconclusive runs as evidence. This is inconsistent with the new "never counts" rule. Fix: use `len(b.evidence())` there. Confidence medium.
- Criteria check:
  - T-0253 (surprise in friction and recall): met. See `fmfriction.py:125` and `fmrecall.py:76`, plus the test `Surprise`.
  - T-0254 (assume/verify tags, done warns in M/L): met. `fmcli.py:352` limits the warning to M and L, and it is a warning, not a gate, as asked.
  - T-0255 (inconclusive leaves the step open, done refuses, `fm next` asks for a sharper check): met. See `fmcore.py:837-848` and `:1589`.
  - UI criterion: card lines added in `register.tsx` and the `_ledger_lines` view. I did not run the UI tests.

## edge: changes needed (minor)

- LOW — `plugin/lib/fmcli.py:102-110`. The "assumption N exists" check runs outside the lock, then `mark_assumption` runs inside `mutate`. Its `False` return is ignored (`fmcore.py:267-276`). If a concurrent edit removes the bullet, the CLI still prints "assumption N verified" and nothing was written. Fix: check the return value inside the lambda and raise `UsageError` if it is false. Confidence medium.
- LOW — `plugin/lib/fmcli.py:279-282`. `fm task evidence --run false --inconclusive` exits 1 after recording, because `code` is the run's exit code. That is arguably fine, but it is undocumented and the test passes `check=False` to hide it. Decide on one behaviour and document it. Confidence low.
- LOW — `plugin/lib/fmcli.py:123`. `fm surprise --task X` doesn't check that X exists, so a typo writes an orphan record. Fix: call `need_brief` when `--task` is given. Confidence high.
- The `surprises.jsonl` append runs under `c.lock`. Recall reads only the last 500 lines, so a large file is not a problem.
- Corrupt state: I did not verify `tail_jsonl`'s behaviour on corrupt lines.

## operator: ok

- `MASTER.md` and `CHANGELOG.md` describe the new commands. `surprise` is added to `HELP_TIERS`, which `test_help` requires.
- Always-on rules file: not touched, so there is no startup-cost growth.
- Nothing is installed or enabled.
- Pre-audit items:
  - `fmfriction.py` changed. No test lists its section names (grep found none), so `test_friction.py` needs no edit. The new `Surprise` test covers the new section.
  - `test_ui.py` was edited in this diff. `kit.ts` is not needed, since the changes are in `register.tsx` and `types/index.d.ts`.

## maintainer: ok with nits

- LOW — `plugin/lib/fmcore.py:227` and `:260`. `_ASSUME_RE` is used by `assumptions()` and `mark_assumption()`. In `mark_assumption`, `.match(x).group(3)` would raise `AttributeError` if the regex ever failed to match. It can't today, because `(.*)$` always matches a line starting with "- ". Low risk.
- Tests assert behaviour through the CLI, and each criterion has a test. Gaps:
  - No test covers `--evidence` containing `]`, which `mark_assumption` rewrites to `)` (`fmcore.py:273`).
  - No test covers the "done on an S task doesn't warn" branch.

## Not checked
I did not run any tests or the UI test suite. I also did not check `fmrecall` scoring, which decides whether a surprise ranks for a related query.
