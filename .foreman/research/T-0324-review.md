**Verdict: changes needed.** One fail-open path and two config-clobber paths are verified. I read the code but ran nothing, so each failing input below comes from tracing the code, not from execution.

**Findings**

1. **MEDIUM** — `plugin/hooks/hook:72` and `plugin/lib/fmagents.py:91-128`. This is a fail-open on Codex and Gemini.
   - `fmagents.hook()` and `_calls()` have no try/except, and the dispatcher doesn't wrap the call.
   - An exception becomes Python exit 1, which Codex and Gemini read as a non-blocking hook error, so the tool call runs. Only the opencode plugin (`foreman.ts:28`) blocks on any non-zero exit.
   - Failing input: `{"tool_name":"Write","tool_input":{"file_path":["/etc/x"]}}` raises `TypeError` in `os.path.isabs` (`fmagents.py:40`).
   - Claude's path avoids this: `fmhooks._pre_tool_use` returns 2 on any exception (`fmhooks.py:734-739`).
   - Fix: wrap the body of `hook()` and return `_deny(...)` when `tool` is true. Coerce `p` with `str()` in `_path`.
   - Confidence: high on the exception. Medium-high on the exit-1 semantics, which I took from Codex/Gemini conventions and did not check against their docs.

2. **MEDIUM** — `fmagents.py:29, 68`. Unmapped tool names pass the guard unseen.
   - `SHELL` lacks `shell_command`, and anything else falls through to `[(name, ti, cwd)]`. `fmhooks` returns 0 for that because the name isn't in `GUARDED` (`fmhooks.py:717`).
   - Example: `{"tool_name":"shell_command","tool_input":{"command":"rm -rf ~"}}` is allowed.
   - Fix: map any unrecognized tool whose input has a string `command` or `cmd` to Bash.
   - Confidence: medium. I can't confirm which names each agent actually emits.

3. **MEDIUM** — `fmagents.py:308`.
   - On gemini and opencode, install does `dict(servers, fm=entry)`. This silently replaces a user's own `mcpServers.fm` or `mcp.fm`.
   - Uninstall only removes `fm` when it equals Foreman's entry (`:309`), so the original is lost for good.
   - Codex handles this correctly: `:296-298` keeps the user's entry and adds a note.
   - Fix: keep an existing `fm` entry that isn't ours and add a note.

4. **MEDIUM** — `fmagents.py:316-317`.
   - Install overwrites `plugins/foreman.ts` without checking whether it exists. Uninstall deletes it via `_save("")`.
   - If the user already has their own `foreman.ts`, install replaces it and uninstall removes it.
   - Fix: put a marker line in the template. Refuse to install over an unmarked file, and only delete a marked one.

5. **LOW** — `fmagents.py:257`. `_block` strips `\n?` on both sides of the block, so it can join the user's lines.
   - Input: `a\n<START>…<END>\nb` becomes `ab`. This happens once the user has appended text after the block and then reinstalls or uninstalls.
   - Fix: consume only the trailing newline, or substitute a single `\n`.

6. **LOW** — `fmagents.py:321` and `fmcore.py:509-518`.
   - `json.dumps(val, indent=2)` uses `ensure_ascii`, so non-ASCII characters in the user's `settings.json` or `hooks.json` are escaped. Fix: pass `ensure_ascii=False`.
   - `write_atomic` writes via mkstemp and replaces the file. A symlinked dotfile (for example from stow) would likely become a regular file. I saw only part of that function, so confidence is low. Fix: resolve with `os.path.realpath` before writing.

**Acceptance criteria**
- *Refuses `rm -rf ~` and injects the next action in each agent's format:* not verifiable here (I ran no tests). The Bash mapping, `_deny` formats and `_answer` context paths look correct for the mapped names.
- *Install writes hooks, MCP and instructions idempotently, and uninstall removes them:* mostly met. Idempotency holds via strip-then-add (`:288-290`, `:318`). Findings 3, 4 and 5 are the exceptions.

**Pre-audit items**
- The `console.log` lines in `test_agents.py` are embedded JS test scripts, not debug leftovers. Dismissed.
- `test_doctor.py` needs no edit: `fmdoctor.py` is unchanged.
- `fmguard._shell_c` (diff lines 551-572) looked sound for `-lc`, `-ec` and `--rcfile`. I found no bypass.

**Not checked**
- Whether Codex and Gemini actually treat exit 1 as non-blocking.
- The real tool names each agent emits.
- Test execution, the docs and `CHANGELOG`, and the full `fmguard` diff beyond `_shell_c`.
