## Verdict: ok

The implementation matches its documented contract and is well tested. Findings below are minor.

## Findings

**LOW** — `~/.claude/foreman/plugin/lib/fmhooks.py:552` (`_grant`) — Any later `fm ask ID plugin` grant for the same task (even unpinned, e.g. for a marketplace add) unconditionally pops `plugin_pin` (`b.meta.pop("plugin_pin", None)` runs whenever `"plugin" in cats`, regardless of whether the new grant is for the same plugin). Scenario: agent gets a pinned yes for `fm ask T plugin --pin a@m`, then before spending it asks `fm ask T plugin --why "add marketplace"` for an unrelated change and the user says yes again; the first pin silently vanishes even though `allow` still lists `plugin`. A subsequent `fm plugins install a@m` is then blocked with "the user's plugin yes names no plugin, not a@m; ask again" (`_pin_problem`, fmhooks.py:234-235), forcing a needless re-ask. Fails closed (no install proceeds without a fresh yes), so not a security hole, and the comment ("a new plugin yes replaces an earlier pin") shows it's deliberate — but it isn't mentioned in MASTER.md/CHANGELOG's user-facing description of pin lifetime. Fix (optional): only pop `plugin_pin` when the new grant is itself pinned, or document the replace-on-any-plugin-ask behavior. Confidence: high (verified by reading `_grant` and `_pin_problem` together; not covered by an existing test).

**LOW (pre-existing, not introduced by this diff)** — `~/.claude/foreman/setup-plugins.sh:67` (`install()` → `claude plugin install "$id" --scope user`) — the guard's plugin-category detection is textual (`fmguard.py:508-511`, `:757-783`) and only recognizes `claude plugin install|enable` or `fm plugins install|enable` appearing directly in the Bash command string. If an agent runs `bash setup-plugins.sh --build-tools` via the Bash tool, the guard never sees the `claude plugin install` text (it's inside the script), so no `plugin` category is raised and no yes/pin is required at all. This predates T-0036 and isn't a regression from this diff, but it means the new pin protection doesn't apply to this install path; worth a follow-up if agents are ever expected to run this script through Claude Code rather than the user running it directly in a terminal.

## Acceptance criteria
- `--pin PID` binds the yes to the plugin + content hash — met (`fmplugins.content_hash`, `fmhooks.py:545-558`, `fmcli.py:564-568`).
- PreToolUse spends the yes only for that install/enable, unchanged, within 24h — met (`_pin_problem`, `fmhooks.py:219-241`; TTL check against `c.APPROVAL_TTL` = 24h, `fmcore.py:79`).
- Changes the guard can't tie to one plugin (interpreter code, prompt `/plugin`) spend no yes — met (`_pin_problem` target `"?"` case, `fmguard.py:141`/`162` tag `[plugin ?]`; tested in `test_a_pinned_yes_is_spent_on_nothing_else...`).
- Pins never sync — met (`fmsync.py:22` `LOCAL_ONLY` now includes `"plugin_pin"`; tested in `test_sync.py:758-767`).
- Docs (CHANGELOG, MASTER.md, rules/foreman.md, all 5 eval prompts, skills) updated consistently, no stale `fm ask ID plugin` → install without pin instructions — met, verified by grep across the repo.
- Blocked messages give the exact next command — met, verified in code and tests (e.g. `"--pin a@m"` in stderr).

## Not checked
- `plugin/uninstall.sh` and `fmsetup.py` in depth (grepped, no plugin-install code paths found in `fmsetup.py`).
- Runtime behavior on a live Claude Code session (only static/code-path review).
- Non-diff files/tests not shown above beyond what was read.
- Performance of `_tree_hash`/`content_hash` on very large plugin directories.
