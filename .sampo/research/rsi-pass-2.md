1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and the Python heredocs that only mention `import fmsecrets`/`import fmhooks` as text. The `.env` heredoc is only partly fixable, and the `state-direct` block can't be grounded from the code. The scope-reason refusal at `fmcli.py:240` gives no hint about ordering, and a one-line text change fixes that.

2. **Findings** (fixes ordered by value)
- **Fix 1, scope text (S, FIX).** `scope_reason_covers` (`plugin/lib/fmcore.py:1790-1794`) needs a `scope:` log timestamp at or after the latest edit of every outside file. The refusal at `plugin/lib/fmcli.py:239-241` doesn't say that.
  - Change: append "(log it after your last edit of <file>; an earlier note doesn't count)" to the message, naming the file with the latest `touches` entry.
  - Safe because it is text only. Confidence: high.
- **Fix 2, `secrets.txt` in scratch (S, FIX).** `_is_credential` (`plugin/lib/fmguard.py:165-166`) matches the stem `secrets` from its name alone. Scratch and `/tmp` are never consulted, and `ctx.scratch` is only used for the rm check (`fmguard.py:973`).
  - Change: skip only this fuzzy-name rule when the path is strictly under `ctx.scratch` or `/tmp`. Keep the `.env`, `.pem`, `id_rsa` and home-directory credential rules.
  - Safe because `classify_write` checks both the path and its realpath (`fmguard.py:254`, `_variants`). A symlink from scratch into `~/.ssh` or `~/secrets.txt` resolves outside scratch and is still caught. Confidence: medium-high. I haven't run it.
- **Fix 3, `import fm…` mentioned in text (M, FIX).** The "driving Foreman's modules" block fires at `fmguard.py:642` when `_FM_INTERNALS` (line 485) and `_FM_MUTATORS` (line 487) both match anywhere in the command text, so it can't tell code from a string.
  - Change: when the interpreter is Python and the heredoc or `-c` body parses with `ast`, test real `Import`/`ImportFrom` nodes and `__import__`/`import_module` calls with a constant `fm…` argument. Fall back to the current regex if parsing fails, or if the body calls `exec`, `eval`, `compile` or `getattr`.
  - Safe because the fallback keeps today's behaviour for anything the AST can't prove. Confidence: medium, since this is a design from reading, not a tested change.
- **Fix 4, `.env` in a test heredoc (S-M, partial).** `_QUOTED` (`fmguard.py:467`) turns a quoted `".env"` into a write target, and `_WRITE_API` (line 463) matches any write call. The gate at `fmguard.py:640` uses `_INTERP.search(_mask_fm(cmd, ctx))`, and `_mask_fm` returns the shell text plus the heredoc bodies (line 594), so an interpreter name in a body also triggers it.
  - Change: when the heredoc's command word is `cat` or `tee` (not an interpreter or shell), run the interpreter gate on the shell text only. The redirect-target check already covers where `cat >file` writes.
  - Safe because a real `python - <<EOF` or `bash <<EOF` still has its interpreter or shell in the shell text. Python heredocs that write test text containing `.env` stay blocked and still need a core yes. Confidence: medium.
- **Fix 5, `state-direct` from `open(D + "state.ts","w")` (not grounded).** `_QUOTED` requires a leading `./`, `~`, `/` or `dir/`, so a bare `"state.ts"` can't match. A block must have come from another quoted path in that script under `foreman/state`, `ctx.state_dir` or `<project>/.foreman` (`fmguard.py:255-258`).
  - Also, the digest has no `state-direct` line at all.
  - Needs the exact command text before any change.

3. **Risks / surprises**
  - The digest's `rm-outside` entry (recursive delete of `~`) and the `core` entries for `fmguard.py` and `fmsecrets.py` are probably genuine blocks, so don't loosen those.
  - The `plugin ?` entry is the claude-in-code check at `fmguard.py:647`. I didn't investigate it.
  - Fix 3's `ast` path must also look at `-c` bodies, which `_heredocs` doesn't return.

4. **Loop changes.** The digest shows only the block category, not the command. Logging a short redacted command for each guard block would make false positives groundable. It would also have covered the missing `state-direct` count.

   **FORMS to add** to `plugin/tests/test_guard_diff.py`. Whether the guard should allow each form is a decision for the main thread.
   - Must stay blocked: `python3 - <<E\nimport fmhooks\nfmhooks.save_brief(x)\nE`
   - Must stay blocked: `python3 -c 'open("~/.ssh/id_rsa","w")'`
   - Allowed after Fix 2: `echo x > <scratch>/secrets.txt`
   - Allowed after Fix 3: a Python heredoc with `s = "import fmsecrets; write_atomic(x)"` and no real import.
   - Must stay blocked: `python3 - <<E\nexec("import fmsecrets; write_atomic(1)")\nE`
   - Must stay blocked: `ln -s ~/.ssh <scratch>/l; echo x > <scratch>/l/secrets.txt`

5. **Not checked.** I didn't run the tests or the guard. I didn't read `test_guard_diff.py`, the hook latency data, or the earlier-pass items (the self-inbox section). I didn't trace the `plugin ?` block or the `fm quiet` and `sed` tool failures.
