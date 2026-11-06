All four call sites correctly updated to the 5-tuple. This confirms the pin plumbs through `_ask_prompt` (dialog) and `_grant_prompted` (actual grant), and is correctly ignored in `_record_asks`/`permission_request` where it isn't needed.

## Verdict: ok

## Findings

None that reach a severity threshold. I specifically re-traced the HIGH from the first adversary review (interpreter code, a prompt's `/plugin install`, and a marketplace add spending a pinned yes on an unnamed plugin) and confirmed it is closed:

- `plugin/lib/fmguard.py:414` (`_interpreter_writes`) and `:772-773` (`_check_claude_config`, slash-command path) now suffix their "plugin" findings with `[plugin ?]`.
- `plugin/lib/fmhooks.py:344-346` (`_pin_problem`) refuses `target == "?"` unconditionally, closing both routes regardless of whether a pin is in place.
- `claude plugin marketplace add` (`fmguard.py:780-781`) and any other plugin-category finding that carries no `[plugin id]` suffix at all (direct writes into `~/.claude/plugins`, `mcp add`, `config set`) hit `_pin_problem`'s `target is None` branch (`fmhooks.py:350-351`), which refuses whenever a pin is in place (`b.meta.get("plugin_pin")` set) and only falls through to allow when there is no pin — matching the documented "an unpinned yes still covers other plugin changes" behavior, unchanged from before this fix.
- Verified this end-to-end against the new regression test `test_a_pinned_yes_is_spent_on_nothing_else_and_evasive_spellings_on_no_yes` (`plugin/tests/test_hooks.py:665-675`), which exercises exactly the three bypasses the first review demonstrated and asserts `returncode == 2` and the grant stays unspent for all three, then confirms an unpinned yes also doesn't cover the slash-prompt route.

I also tried to break the target-extraction/regex myself:
- Injecting `] [plugin a@m]` into a plugin id argument: impossible, since `_one_plugin`'s `re.fullmatch(r"[\w.-]+(?:@[\w.-]+)?", ...)` rejects any token containing `[`, `]`, or whitespace, and multi-token injections fail the "exactly one word" check, falling back to `"?"` (always refused).
- `claude plugin install a@m --plugin-dir /evil` and `claude --plugin-dir /evil plugin install a@m`: both are caught by the `_SESSION_CONFIG` check (`fmguard.py:774-776`, includes `--plugin-dir`), which runs *before* target extraction and returns a suffix-less "plugin" finding — refused under a pin regardless of flag position.
- `claude plugin install a@m b@m` / bare `claude plugin install`: both correctly resolve to `"?"` via `_one_plugin`'s length check (tested at `test_guard.py:517-526`).

## Acceptance criteria (per the fix description)
- Interpreter code / slash-prompt findings marked `[plugin ?]`, always refused — met (`fmguard.py:414,772-773`; `fmhooks.py:344-346`).
- Any untargeted plugin change refused while a pin is in place — met (`fmhooks.py:350-351`; test at `test_hooks.py:610-616`).
- Malformed pin refused cleanly — met (`fmhooks.py:347-348`; test at `test_hooks.py:634-641`, no internal error).
- Pin re-checked under the lock at spend time — met (`fmhooks.py:251-260`, re-read `b` inside `c.lock`; test at `test_hooks.py:618-625`).
- Pinned yes for a vanished plugin grants nothing — met (`fmhooks.py:325-331`; test at `test_hooks.py:627-632`).
- Dialog flags remote-entry-only pins — met (`fmhooks.py:591-593`; `fmplugins.py:453-457`; test at `test_hooks.py:651-663`).

## Not checked
- `npx @anthropic-ai/claude-code plugin install`, `env`/`command`/`xargs`-wrapped `claude` invocations: pre-existing `_strip_wrappers`/name-matching logic, untouched by this diff; the first review already flagged this as out of scope and it remains so.
- Non-security correctness of `_tree_hash`/hashing performance, and `fm plugins` CLI implementations beyond what the guard/hook layer reference.
- The disclosed TOCTOU (marketplace refresh between check and install; remote-source entries pinning only the manifest, not fetched code) — accepted, documented limitation, not a silent regression.
