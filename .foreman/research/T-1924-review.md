**Verdict: changes needed.** One adversary finding is real and new. The relative-`cd` change lets a line pass that was refused before. I ran nothing, so every reproducer below is traced from the code.

## lens: adversary
- MEDIUM — plugin/lib/fmguard.py:3342-3367 — The walk takes a `cd` run through an exec wrapper as a shell `cd`. `_strip_wrappers` (1426-1457) drops `sudo`, `env`, `timeout`, `nohup`, `nice`, `xargs`, `flock` and similar before `name == "cd"` is tested. Those wrappers run `cd` in a child, so the shell does not move. A relative `cd` into an existing folder is now certain, so `_moved(sure=True)` replaces `cwds` with the new folder. Trigger: cwd is Foreman, then `nice cd ../<existing sibling the guard doesn't protect>; tar xf -`. Before, a relative `cd` always counted as "may fail", so `cwds` kept Foreman and the line was blocked as core. After, `cwds` is only the sibling, so it passes, while the real shell stays in Foreman. The absolute form (`nice cd /tmp; tar xf -`) already had this hole. This diff extends it to relative `cd`, the common spelling. — Fix: set `certain=False` when `_strip_wrappers` removed anything other than `command`, `builtin`, `time`, `noglob` or a keyword. — confidence medium-high; I haven't run it.
- MEDIUM — plugin/lib/fmguard.py:3361-3364 — `lands` trusts that the folder exists at guard time, but an earlier command in the same line can remove or rename it. Trigger: cwd is Foreman, `mv ../d ../e; cd ../d; tar xf -`, with `../d` existing now. `isdir` is true, so the `cd` is certain and the guard thinks the shell is in `../d`. In bash the `cd` fails and the shell stays in Foreman. Before, the relative `cd` always kept the old folder in `cwds`. The absolute branch had the same weakness through `made` and `isdir`. — Fix: count the `cd` as can-fail when any earlier command on the line is `mv`, `rm`, `rmdir`, `ln` or `chmod`, or computes its target. — confidence medium.
- LOW — plugin/lib/fmguard.py:3302 — `clean` rests on `_moves_text(plain)`. The comment at 3292-3293 says the same test misses `A=1 $C` and `c$(…)`, and the T-1921 head check adds extra tests for them. `clean` leaves those out. I could not build an input where the dropped tail was the only catch, so this is a lead, not a finding. — Fix: reuse the extra `_MOVERS` and `word()` tests from 3292-3293.

## lens: intent
- MEDIUM — plugin/tests/test_guard.py:2587-2618 — The acceptance criteria name "a 20-folder for loop under 1 s each". The test has no 20-folder loop, and its time limit is 2 s for the whole table. The request also asked to cap sets at about 64 and collapse to unknown. What shipped is a 1024 cap that refuses (fmguard.py:3386). The refusal is safer, but long legitimate scripts with many conditional `cd`s will now be refused. — Fix: add a 20-folder `for d in …; do cd $d && echo $(…); cd ..; done` case with `< 1` s, and say in the brief that the cap is 1024 and refuses.

## lens: maintainer
- LOW — plugin/lib/fmguard.py:3299-3302 — This duplicates the `$S` masking loop at 3289-3290. Pull out a helper. The tail-index bookkeeping in `_subst_bodies` (`tail`, `top[3]`, `None` entries filtered at the end) is also fragile.
- LOW — plugin/lib/fmguard.py:3388 — The refusal uses category `rm-outside` for a line with no `rm`. A grant of that category silently lifts the cap. — Fix: use a dedicated category.

## Acceptance criteria
- 20 `cd` blocks in a `;` line under 1 s: partly met. The test covers it, but its limit is 2 s total and I did not run it.
- 20-folder for loop under 1 s: not met. No test covers it.
- A tree write after a `cd` into Foreman still blocks: met for the cases in the table (the `test_repeated_cds_in_a_line_are_judged_fast` rows). The two adversary findings above are not covered.
- CHANGELOG: updated (line 4), no edit needed.

## Implicit decisions
- The cap is 1024 entries and refuses; it does not collapse to unknown.
- Heredoc `live` text uses the `clean` flag computed from `shell` only.
- The expected category in `test_guard_pipes.py:10` changed from `system` to `pipe-shell`. It still blocks.
- A `#`, backtick, backslash, `<<`, `((` or `case` anywhere in a body keeps the tail, even where it is harmless (for example `$#`).

## Not checked
I did not run the tests or time them. I did not trace how the main walk handles a computed command word. I did not review the other files that call `_subst_bodies`.

**Noticed:**
- The existing absolute `cd` hole (wrapper-run `cd`, or a folder removed earlier in the line) deserves its own task.
- `_DCWD` is still a module global that is reset only in `findings`. fmmcp.py:288 calls `check_bash` directly, so stale entries can build up (an earlier nit).
