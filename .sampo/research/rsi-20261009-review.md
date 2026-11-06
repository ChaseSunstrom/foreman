1. **Answer.** Two guard-related frictions are grounded in code: the guard misreads remote interpreter code run over `ssh` as local Foreman tampering, and `fm lane merge` is not what the contract tells builders or the main thread to use. Two other digest items are not defects. I could ground only 2 improvements of the 8 allowed, so the list is short. The remaining digest lines either match intended behaviour or lack the output needed to ground them.

**Findings, ranked**

1. **FIX, S: `ssh ... python3.12 -` is blocked as "core: interpreter code driving Foreman's modules" (digest line 11, 2×).**
   - `_python_units` (`plugin/lib/fmguard.py:792-793`) only recognises a line that starts with `python … - <<`. An `ssh host '… python3.12 - …'` line fails that match, so its body goes to `rest`.
   - `_drives_fm` (`fmguard.py:950-953`) then runs the plain text match of `_FM_INTERNALS` and `_FM_MUTATORS` (`fmguard.py:637-643`) over everything, and returns True.
   - The fix is to drop the remote command string from that text match when the segment's word is `ssh`. Remote file writes are a separate matter, and the existing `remote` category (`fmguard.py:15`) is the place to keep them guarded.
   - Verify: add an `ssh host 'python3 - <<EOF\nimport fmcore; save_brief(1)\nEOF'` form to the "allowed" side of `plugin/tests/test_guard_diff.py`, and keep a local `python3 - <<…` form on the "blocked" side. Both must pass.
   - Confidence: medium. I did not read the full ssh command from the log, so I am inferring that the python was inside the ssh quote.

2. **CLEAN, S: builders and the main thread run into a Foreman-repo `git merge` block (digest line 15, "still blocks"; digest line 10, `fm lane rm` over `__pycache__`).**
   - The block is correct by design. `fm lane merge` was added in 1.2.3 for this case (`CHANGELOG.md:23`).
   - The `git merge --no-ff worktree-agent-…` command was typed by hand instead of using `fm lane merge`. Nothing in `fmlanes.py:87-100` (the builder contract) or the main-thread rules points the main thread at `fm lane merge` when the plain merge is refused.
   - The change is to add the line "On Foreman's own repo use `fm lane merge ID`" to the guard's `core` refusal message when the command is a `git merge` in the Foreman tree. Look near `fmguard.py:95-120`, the hint function.
   - Verify: a test that asserts the refusal text for `git merge x` in `~/.claude/foreman` contains `fm lane merge`.
   - Confidence: medium. The hint text is inferred; I did not read the exact function.

**Earlier self-inbox items**
- T-0369 and T-0370 are done. The trend line (guard blocks 0.8 → 1.7 per 100 tool calls) shows no block count falling. Digest lines 10 and 13 are marked "today's guard allows it", so I left them out.
- T-0275 (guard reads script files) and T-0317 are still open. I did not check whether they relate to line 12.

**Loop change.** The window is short: 905 hook runs and a handful of events. Run the pass at most daily, or only when the guard-block count is at least 3. Fewer passes would mean fewer reports built on thin data.

**Risks / surprises**
- The digest line 12 `state-direct` block (`echo hi > $S/t247.volt` with `S` set in a nested `$(ls …)` earlier on the line) looks like the T-0370 area, which `CHANGELOG.md:29` says is fixed. It is not marked "today's guard allows it". Re-run that exact line in `fmguard` before dropping it.
- Digest line 14 (`rm -rf $NOPE_UNSET/`) is the intended refusal (`fmguard.py:2113-2114`), not friction.
- The 4× `ssh … sd(){ echo root | sudo -S …}` exit 1 and the `fm task set` exit 2 are ungrounded. I could not tell what failed: `task set` takes `assignments` as `nargs="*"` (`fmcli.py:2224`), so an exit 2 is probably the `scope=` value, but I did not find the cause.
- The 4× "isolated in the worktree" failures are already described in the builder contract (`fmlanes.py:97-99`). They look like harness behaviour, not a Foreman defect.

**Not checked**
- The ledgers and event logs themselves. I read only the digest, and the brief gave no log paths.
- `plugin/tests/test_guard_diff.py` `FORMS` contents beyond a grep for `rm -rf`.
- The `Read` token-limit overflow (digest line 20). It is a Claude Code limit, not Foreman code.
- Hook latency (p95 50 ms). Nothing to act on.
