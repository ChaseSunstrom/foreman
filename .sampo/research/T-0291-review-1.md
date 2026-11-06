## Verdict
Changes needed. Fix 2 (the `confirm` flag) can be bypassed by the working session itself, and fix 3 has one gap that runs a planted driver.

## Findings (adversary lens first)

**1. HIGH. `plugin/lib/fmcli.py:14,910` bypasses the `confirm` flag in `plugin/lib/fmcore.py:1507`.**
- `needs_approval` returns False whenever `meta["approved"]` is set.
- `approved` is in `EDITABLE`, and `fm task set ID approved=true` has no guard category. `USER_ONLY` in `fmguard.py:17` covers only core, remote and plugin.
- Trigger: in full autonomy, with a `fm second session` capture T-9, run `fm task set T-9 approved=true`. The item is then ready for `fm focus`, `fm run` and drive, with no user yes.
- The fix needs the user's yes to be what grants it. Either make `confirm` clear only through `fm ask`, or refuse `approved=true` from `fm task set` when `confirm` is set. The test sets `approved` in memory (`test_session_fixes.py:54`), so it never exercises this path.
- Confidence: high.

**2. MEDIUM. `fmcli.py:784` (batch) and `fmcore.py:1910` (`fm next`).**
- Batch refuses members only on `meta["explore"]`, not on `confirm`.
- `fm task set T-9 explore=false` is allowed (`explore` is in `EDITABLE`), and `fm batch T-9 T-10` then succeeds. The host brief is new and carries no `confirm`, so its members get worked.
- Fix: refuse in batch on `needs_approval(b, "full")`, or on `confirm`.
- Acceptance criterion 2 says `fm next` skips such an item, but it does not. `_next_for` takes `rank_inbox` and `order_queue` with no approval filter, and stage "captured" yields "expand it into a planned brief". Once planned, it shows "approval (explore item, standard autonomy)" (`fmcore.py:1544`), which is mislabelled in full autonomy.
- Confidence: high for batch, medium on the `fm next` wording.

**3. MEDIUM. `plugin/lib/fmbench.py:38`: drivers in global scope are never neutralised.**
- Only `local` and `worktree` scopes are emptied. The replay runs under the real HOME, and `_env` does not reset it.
- A bypass-mode session that writes `~/.gitconfig` or `~/.config/git/config` with `filter.evil.clean=…` and commits a `.gitattributes` line `* filter=evil` gets the driver run by the judge's `git add -A` (`fmbench.py:273`).
- The "git-lfs still runs" exemption leaves this open. Fix: neutralise every driver except an allowlist (`lfs`), or run the bench git with `GIT_CONFIG_GLOBAL` pointed at a copy that has only the lfs filter.
- Confidence: medium. It depends on whether the replay guard blocks writes to `~/.gitconfig`.

**4. LOW. `fmbench.py:36-38`: the discovery fails open.**
- The `--show-scope` flag needs git 2.26 or later. An older git prints no scope column, the regex never matches, and nothing is neutralised, with no error.
- Fix: check the return code and fall back to neutralising every `filter.*` driver.
- Confidence: medium.

**5. LOW. `plugin/lib/fmcost.py:441` and `plugin/lib/fmcore.py:512`.**
- The temp file is `.AGENTS.md.<pid>.tmp` in the unresolved parent, opened with `"w"`. That follows a symlink planted at that name (the pid is guessable), and the write lands outside the project. The parent check also runs before the write, so it is subject to a swap race.
- `--out` still reaches in-project sensitive files such as `.git/config`, `.claude/settings.json` and `CLAUDE.md`, because `--force` overwrites them. The content quotes lessons, which can be model-written.
- Fix: open the temp file with `O_EXCL|O_NOFOLLOW`. Refuse `.git/` and `.claude/` targets.
- Confidence: low.

**Checked and held:**
- Export: a final-component symlink is replaced, not followed, by `os.replace`.
- `..` is collapsed by `abspath` before `realpath`, and the same path is used for the write.
- A symlinked project root is handled, because both sides go through `realpath`.
- Bench: the judge diff already passes `--no-ext-diff --no-textconv` (`fmbench.py:274`). Hooks and fsmonitor are neutralised. An empty `clean=` means no filter.

## Acceptance criteria
- **T-0288:** met for the tested cases (outside path, symlink out, in-project path). Residuals are in finding 5.
- **T-0289:** not met. The flag is honoured by `needs_approval`, `waits_on_user` (so `fm run` and drive), `plan_gaps` (so `fm focus`) and fmserve. `approved=true` and `explore=false` plus batch defeat it, and `fm next` does not skip the item.
- **T-0290:** partly met for local and worktree scopes, which the test covers. Global scope and old git are not covered.

## Not checked
The other four lenses (intent, edge, operator, maintainer), fmserve internals, the MASTER and CHANGELOG lines, and a live run of the tests.
