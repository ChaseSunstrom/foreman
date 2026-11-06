# T-2879 probe: how a plugin rename moves an existing install (2026-11-05, Claude Code 2.1.317)

Run: `bash scripts/probe-plugin-rename.sh MODE` (toy marketplace "foreman" with plugin "foreman": a command, a skill, a hook; installed into a throwaway CLAUDE_CONFIG_DIR; nothing of the user's touched).

| Mode | After `claude plugin marketplace update` | After a session start (logged out) |
|---|---|---|
| plugin renamed to "sampo" in the same marketplace, `"renames": {"foreman": "sampo"}` | enabledPlugins moves to `sampo@foreman: true`; the old install record clears; `plugin update foreman@foreman` fails ("not found") | `sampo@foreman` is installed and enabled by itself; no stale entry |
| shim: "foreman" kept, depends on "sampo" | foreman@foreman 1.1.0 **fails to load**: "Dependency sampo@foreman is not installed" | (not needed: broken) |
| marketplace renamed to "sampo" too | the configured marketplace keeps its add-time name "foreman"; only the plugin rename applies (same as row 1) | same as row 1 |

Findings:
- The renames map inside the existing marketplace moves every install with no user action: the next session after the marketplace updates installs and enables `sampo@foreman`.
- Shims with a dependency break the install (dependencies are not auto-installed): ruled out.
- A marketplace's configured name comes from when it was added, so renaming marketplace.json's name does not reach existing installs; `sampo@sampo` would need every user to re-add the marketplace. The marketplace stays "foreman" (an id part, kept like any alias); filed as not-yet with this blocker.
- Gap: between the marketplace update and the next session start, the running session keeps the old plugin loaded; nothing breaks mid-session.
