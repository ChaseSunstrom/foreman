## Verdict: changes needed

## Findings

**MEDIUM** — `~/.claude/foreman/plugin/lib/fmhooks.py:341-364` (`_pin_problem`) and `~/.claude/foreman/plugin/lib/fmguard.py:773,783-793` (`_check_claude_config`, `check_bash`, `_one_plugin`, `_claude_plugin_target`) — the plugin target is carried as a suffix baked into the free-text finding `detail` string (`f"... [plugin {target}]"` / `"[plugin ?]"`), and `_pin_problem` parses it back out with `re.search(r"\[plugin (\S+)\]$", str(detail))`. This is exactly the failure mode the brief's own past-finding list names ("a protocol carried in free-text detail strings … parsed back by regex in the hook"). A future wording tweak to any of the four producer strings in fmguard.py (e.g. rewrapping the message, adding a trailing period, or truncating it for a user-facing note) silently breaks pin enforcement — either fail-open (regex stops matching, `target` becomes `None`, and an install with no target check falls through to the "unpinned covers it" branch) or fail-closed with a confusing message. Only the exact end-of-string anchor keeps this alive today. Fix: pass the plugin target as a structured value (e.g. `found` tuples become `(category, detail, target)`, or a small `PluginFinding` namedtuple) instead of embedding it in the human-readable string, so producer and consumer can't drift independently. Confidence: high (verified both sides read/write the identical literal format, no shared constant).

**LOW** — `~/.claude/foreman/plugin/lib/fmguard.py:793` and `~/.claude/foreman/plugin/lib/fmhooks.py:585` — the plugin-id format regex `r"[\w.-]+(?:@[\w.-]+)?"` is copy-pasted in both files rather than defined once. This is the second past-finding class the brief flags by name ("plugin-id validation regexes in fmguard and fmhooks that drift"). Currently identical, but nothing enforces that. Fix: hoist to one constant (e.g. `fmplugins.PLUGIN_ID_RE`) and import it in both call sites.

**LOW** — `~/.claude/foreman/plugin/lib/fmplugins.py:149-153` (`pin_covers_code`) re-implements the same "is there an installed dir, else a local marketplace copy" check that `content_hash` (lines 136-147) already does, with separate logic (`installed().get(pid)`, `index()` lookup) rather than sharing a helper. If `content_hash`'s notion of "has local code" changes (e.g. a new local-source form), `pin_covers_code`'s dialog wording can silently go stale. Fix: have `content_hash` return/expose whether it hashed real code, or derive `pin_covers_code` from the same lookup `content_hash` performs.

**MEDIUM** — `~/.claude/foreman/plugin/lib/fmhooks.py:370` (`_use_plugin_grant`, `with c.lock(p.dir, timeout=LOCK_QUICK)`) and `:545` (`_grant`, invoked under `LOCK_SLOW`/`LOCK_WORDS` from `_grant_prompted`/`_resolve_approvals`) — `fmplugins.content_hash` (which does a full recursive `os.walk` + per-file SHA-256 read, `fmplugins.py:107-127`) is called while holding the project's single exclusive `flock` (`fmcore.py:402`), the same lock every other fm state write and hook (`SessionStart` heartbeat, `Stop` drive counters, task edits) contends for. `LOCK_QUICK`'s own comment says callers expect sub-second turnover ("losing one is harmless"); a plugin with a non-trivial file tree turns a "quick" lock into a slow one and can make unrelated concurrent fm operations time out. Fix: compute `content_hash(target)`/`content_hash(pin)` before acquiring the lock (the target/pin values are already known at that point) and only do the brief read/compare inside the critical section.

## Acceptance criteria (from CHANGELOG entry, diff line 9)
- Pin binds yes to plugin + content hash: met — `fmhooks.py` `_grant` stores `plugin_pin: [id, hash, epoch]`.
- Install/enable spend it only for that plugin, unchanged, within 24h: met — `_pin_problem` checks target match, TTL, hash match; covered by `PluginPins` tests.
- Says which `fm ask` to run again on mismatch: met — `_pin_problem`'s `ask` string.
- Dialog names the plugin (and flags remote-only pins): met — `_ask_prompt`, tested by `test_the_dialog_says_when_a_pin_covers_only_a_remote_entry`.
- Pins never sync: met — `fmsync.LOCAL_ONLY` includes `"plugin_pin"`, tested in `test_sync.py`.

## Not checked
- Non-lens concerns (correctness of guard regexes beyond the plugin-pin feature, security review of the sandbox/trust model, performance beyond the lock-contention point above).
- Whether `installed()`/`index()` themselves are correct (pre-existing code, unchanged by this diff).
- Actual test execution (read-only review; did not run the suite).
