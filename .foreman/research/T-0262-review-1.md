## adversary: ok (one low item)

- **LOW** — `plugin/lib/fmcore.py:230-239`: the creation-time check is sound. `realpath` plus the `top + os.sep` prefix rejects `../`, absolute paths and symlinks that point outside the project. `test_a_bad_trigger_is_refused` covers `../../etc/passwd`.
- **LOW** — `plugin/lib/fmcore.py:174,252,263`: the check is not repeated when the trigger fires. `_REVISIT_TAG` is searched over the whole row, including the why and rejected cells. The path is joined with `os.path.join(p.root, m.group(2))`, so a hand-edited or forged tag such as `[revisit: when /etc/shadow changes @abc]` is hashed. The only leak is a "changed" or "is gone" line, so it is a small side channel and nothing worse. Fix: search only `cells[2]`, and `realpath`-contain the path in `fired_decisions`.

## edge: changes needed

- **MEDIUM** — `plugin/lib/fmcore.py:252-258`: tag parsing in `fired_decisions` is loose.
  - `settled` is built from `"".join(rows[i+1:])`, so a `[revisited: …]` or `[reverses: …]` anywhere in any later cell settles an earlier decision. That includes the free text of the decision, why and rejected cells, which `cmd_decide` does not sanitise.
  - Matching is by substring, so `--revisited "a"` settles every fired decision containing "a".
  - A decision or why text that contains `[revisit: after 2020-01-01]` fires without a real trigger.
  - Fix: parse tags only from the leading tag run of `cells[2]`, and require the settle words to be at least 4 characters or a whole-word match.
- **LOW** — `plugin/lib/fmcore.py:253`: the escaped-pipe split fails when a cell ends in a backslash. `cell()` turns `x\` plus the `|` delimiter into `x\|`, and the lookbehind then merges two cells. This is cosmetic: the displayed decision picks up the why text.
- **MEDIUM** — `plugin/lib/fmcli.py:589` (`cmd_batch`) and `:1376` (`cmd_check`): `hint_used` and `hints_reset` call `write_atomic` with no try/except.
  - The hooks wrap their calls, but these two do not. An `OSError` on `hints.json` (read-only or full state dir) aborts `fm batch` outright.
  - In `fm check` it aborts after the gates have run but before `log_event`, so the check result is lost.
  - Fix: wrap both in `try/except OSError`, or make `_save_hints` swallow `OSError`.
- **LOW** — `plugin/lib/fmcore.py:195-203`: hook latency and race.
  - `hints_shown` does a read, then a write with `fsync` (`fmcore.py:516`), on every prompt where the injected state changed. This stays within budget, but it writes even when `shown` is already `[]` and `ignored` is unchanged. Fix: skip the save when nothing changed.
  - Two sessions in one project share `hints.json` unlocked. One session's first injection counts the other's `shown` as ignored. This is acknowledged in the `ponytail:` comment and only speeds up quieting.
- **LOW** — `plugin/lib/fmcore.py:1745-1756`: "ignored" really means "the Next line changed again". Any step change re-injects Next and counts the earlier hint as ignored. After six step changes the skills hint is quiet even if it was never relevant. This follows the brief's wording but is cruder than the request.

## intent: ok with notes

- **MEDIUM** — `plugin/lib/fmrecall.py:360`: `covered` can give false positives. `task_new` passes `title + raw`, and the raw text can be a long pasted request. After stopword removal and 5-letter stems, a long `q` shares at least 3 words with, and at least 60% of, any help of 5 or fewer stems. The note is advisory and says "If it is…", so the harm is noise. Fix: also require `shared / len(q) ≥ ~0.25` for long requests, or cap `q` to the title.
- **LOW** — `plugin/lib/fmrecall.py:355-357`: only top-level subcommands are scanned. `fm task evidence`, `fm task assume` and `fm audit …` are never matched.
- **LOW** — `plugin/lib/fmcore.py:1745` (T-0250): "restored when its absence correlates with a failed gate" is implemented as any failing `fm check` resetting every hint. In a TDD red phase this undoes quieting constantly. This is acceptable as a proxy but is not correlation.

## maintainer: ok

- Tests cover all three features, the hook path (`test_the_hooks_count_shown_hints…`) and the bad triggers. `plugin/tests/test_hooks.py` needs no edit, because the new hook behaviour is exercised in `plugin/tests/test_nudges.py`.
- **LOW** — `plugin/lib/fmcore.py:1686,1693`: `next_for` hashes every path-trigger file and re-reads `decisions.md` on each call. It runs per prompt, in the pane view and in Stop. This is O(rows²) in `"".join(rows[i+1:])`. Cache or limit it if decisions grow.
- No test exercises `fm decide … --revisit` together with `--revisited` on the same row (re-arming).

## Acceptance criteria

- T-0256 (covered note on capture and task new): met by code and test. I did not run it.
- T-0247 (path trigger shows in `fm next`, `--revisited` settles it): met, with the parsing caveats above.
- T-0250 (quiet after `QUIET_AFTER`; use or a failed gate restores): met.
- Pane shows a fired trigger: met by `plugin/lib/fmwatch.py:384` and `register.tsx`. The mod test was not run.

## Not checked

I ran no tests. I did not review the full `fmcli` argument flow, `fmplugins.stage_skills`, or the UI rendering beyond the diff.
