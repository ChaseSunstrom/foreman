## Verdict
Changes needed. The three caps are now unliftable and `check()` ordering is sound. One refusal in the same class is still liftable, and the `unanalysed()` substring match is fragile.

## lens: adversary
- MEDIUM — plugin/lib/fmguard.py:3451 — "eval of computed text" is `("rm-outside", …)` and its text is never read, so an rm-outside grant still lifts it and the unread text runs. Input with the grant: `eval "$(echo -e 'tar xf - -C ~/.claude/foreman')"`. `_PRINTED_SUBST` matches, `w[:1]` starts with `-`, the `else` at 3450 fires, and `_readings` never reads inside `$(…)`. Fix: make `unanalysed()` true for it, for example by changing the detail to "eval of computed text it is too tangled to analyse". Confidence: high, from reading the code (nothing was run).
- MEDIUM — plugin/lib/fmguard.py:218 — `"to analyse" in detail` is a substring test on free text that also holds user paths and script lines. `rm -rf ~/"to analyse"` makes `_rm_target_violation` return `~/to analyse`, so the detail is "recursive delete of ~/to analyse" (4790). An rm-outside grant can no longer lift it. The message then says "split the command; no grant lifts this", which is wrong because splitting changes nothing. The same happens for a system refusal that quotes `line[:80]` of a script (4381). A core path under a folder named "to analyse" gets this text instead of the `fm ask … core` instructions, because the new branch at fmguard.py:256 runs before the USER_ONLY branch. These fail closed but cannot be recovered from. Fix: match exactly. Use one frozenset of the three constants, or, as the request asked, a category added to NOT_AUTHORIZABLE. Confidence: high.
- LOW — plugin/lib/fmhooks.py:1783 — `guard.unanalysed` is an attribute the committed fallback guard may lack. fmhooks.py:2076 already guards the same case with `hasattr(guard, "discards_work")`, and 1793 notes "committed fallback may lack it". If the working fmguard fails to import before this change is committed, the 3rd repeat of any authorizable refusal raises AttributeError in PreToolUse. Fix: `getattr(guard, "unanalysed", lambda d: False)(block.detail)`. Confidence: medium.

## lens: intent
- LOW — plugin/lib/fmguard.py:136 — The request said "give them a category no grant lifts". The change keeps `rm-outside` and filters on message text. This is the root of the substring finding above, and `fm risk` and the guard_block events still count these under rm-outside. Fix: as above, or record the choice in the brief.

## lens: maintainer
- LOW — plugin/lib/fmhooks.py:1784 — The 3rd-repeat hint for an unanalysed refusal now drops `fm ask`. It says "record why the task can't go on (fm task block)" and never says splitting the command is the way through. Fix: for `unanalysed`, say "split the command, or ".
- LOW — plugin/tests/test_guard.py:2630-2640 — The nesting cap (depth > 4) is never run end to end under a grant. `test_nesting_too_deep` has no allow, and the new test feeds hand-written details to `check`. Rewording the cap text would break the real caps while the synthetic loop still passes. Fix: in `test_nesting_too_deep`, assert `self.bash(deep, allow=("rm-outside",))` is still blocked.

## Checked and fine
- `check()` is the only place a grant lifts a finding. Callers: fmcli.py:995, fmlanes.py:720, fmsettings.py:634, fmedit.py:81, fmoracle.py:131, fmhooks.py:1652.
- Any unliftable finding blocks whatever its CATEGORIES position. Order only picks which message is shown, and a cap finding sits in `rm-outside`, never in `core`, so `core` standing or trust cannot lift it.
- The 3418 cap returns `found + [cap]`, so nothing beside it passes.

## Acceptance criteria
- An rm-outside grant leaves both folder caps and the nesting cap refused, and a plain rm-outside is still lifted: met. The new test covers it, and the CHANGELOG entry exists at line 4. I did not run the suite (read-only).

## Implicit decisions
- The change uses a substring marker, "to analyse", not a category.
- Splitting the command is named as the way through.
- The unliftable test covers `rm-outside` details only.

## Not checked
- I did not run the tests.
- I did not check the guard fallback import path beyond fmhooks.

**Noticed:**
- plugin/lib/fmguard.py:4016-4020 — `_check_script` drops "too deep" findings unless 3 scripts are chained (`len(_IN_SCRIPT) < 3`). Content nested past depth 4 inside a script file is then never read and not refused. This was deliberate (5 of 330 scripts), so it is worth its own task.
- plugin/lib/fmguard.py:254 — system "can't read" refusals (a pipe into a shell, IFS, a script too long to parse) are still lifted by `--allow system`, though the message says they are not.
