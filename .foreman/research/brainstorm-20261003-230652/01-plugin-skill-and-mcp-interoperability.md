# Brainstorm — lens: plugin, skill and MCP interoperability

- **Route stages to installed skills at `fm next`** — FEATURE — value 5 — effort M — risk low — category: interop
  Why: the pack says `next_action` names only Foreman's own procedure files; a SECURITY task doesn't surface `/security-review`, CLEAN doesn't surface `/ponytail-audit`, UI doesn't surface frontend-design. The MASTER.md §7 table is static prose. Compile it into a stage→skill map that `fm next` consults, filtered to what is actually installed and enabled (reusing fmplugins' local scan). One line, no new always-on context.
  Done when: with security-review installed, `fm next` on a SECURITY task in the audit stage names `/security-review`; with it uninstalled, the line is absent (test covers both).

- **Parse third-party skill frontmatter into a capability index** — FEATURE — value 4 — effort M — risk low — category: interop
  Why: `fm plugins find` keyword-searches marketplace indexes only, and `check` estimates cost at ~4 chars/token from descriptions. Reading each installed skill's `name`/`description`/`allowed-tools` into a cached index (keyed by plugin sha) lets routing, conflict checks and `find` share one source instead of three.
  Done when: `fm plugins index` lists every installed skill with description, token cost and owning plugin; the stage router and `check` read from it.

- **Derive KNOWN_CONFLICTS by overlap, not a hard-coded dict** — FEATURE — value 3 — effort M — risk med — category: interop
  Why: FOREMAN_OWNS and KNOWN_CONFLICTS are static; a new orchestrator-style plugin (hooks on Stop/UserPromptSubmit, "plan"/"brainstorm" descriptions) goes unnoticed until the user hits double-handling. Detect plugins that register the same hook events Foreman gates on, or whose descriptions claim an owned area, and warn once at install and `fm doctor`.
  Done when: a fixture plugin registering a Stop hook and a "planning" skill is flagged by `fm plugins check` without being in the dict.

- **Surface installed MCP servers and tools in GROUND and brainstorm packs** — FEATURE — value 4 — effort S — risk low — category: MCP
  Why: brainstorm children run with no MCP and the pack is built from repo data only; the intake skill mentions context7 once. Read `.mcp.json` and plugin-declared servers, add a compact "available tools" block (name + one-line purpose) to intake hints and packs so lenses can propose ideas that use them. Assumption: MCP config is readable from the usual locations.
  Done when: a pack built in a project with a configured MCP server contains its tool names, capped at a fixed size, and an absent config adds nothing.

- **Honor third-party hook outcomes in evidence** — FIX — value 3 — effort M — risk med — category: hooks
  Why: Foreman hooks gate edits and done, but other plugins' PostToolUse hooks (formatters, LSP diagnostics such as clangd/rust-analyzer) can fail or modify files silently, and edit attribution for Bash is mtime-based. Record a formatter-modified-file note so scope and "evidence fresh" checks do not misattribute or go stale. Assumption: such modifications currently appear as out-of-scope or stale evidence.
  Done when: a test where a stub PostToolUse hook rewrites an in-scope file does not trip the scope gate or invalidate cached evidence.

- **Export Foreman as an MCP server for other agents and clients** — FEATURE — value 3 — effort M — risk med — category: MCP
  Why: the mod idea of `$.tool.register` only covers the UI session; a stdlib stdio MCP server exposing read-only `state`, `next`, `recall`, `why` lets other plugins, subagents and `claude -p` children query Foreman state without shelling out through the guard. Writes stay behind the guard. Assumption: stdio JSON-RPC in stdlib is small.
  Done when: an MCP client can call `recall` and `state` and gets the same output as the CLI; no mutating tool is listed.

- **Wild: Let third-party skills declare Foreman stage hooks** — FEATURE — value 4 — effort L — risk med — category: interop
  Why: wild. A skill ships a tiny `foreman.json` ("stage: verify, command: …, lens: security") and Foreman adopts it as an audit lens or gate with its sunset and cost accounting, instead of only the author editing the table. Makes any plugin first-class without touching Foreman.
  Done when: a fixture skill with `foreman.json` appears as an audit lens in `fm next` and its command runs as a gate with the result recorded.

- **Measure each integration's real contribution** — PERFORMANCE — value 3 — effort M — risk low — category: interop
  Why: Foreman disabled ECC for 41k always-on tokens, but the enabled integrations (context7, code-review, ponytail) have no cost-vs-catch data. Join `fmcost` per-skill token use with whether the skill's findings changed a brief; list never-useful plugins in `fm plugins check` for the user's yes/no disable.
  Done when: `fm plugins check` prints per-plugin invocations, tokens and findings accepted over the last N tasks.

- **Wild: Import a skill's procedure as a playbook by yes/no** — FEATURE — value 3 — effort M — risk med — category: skills
  Why: wild. When the user installs a useful skill, Foreman offers to fold its steps into the playbooks (and the recall index) with attribution and sha pin, so it works with the stage machine and gates rather than as a free-floating prompt. Needs the guard's `plugin` category consent.
  Done when: accepting writes a playbook file marked with source plugin and sha, and `fm recall` finds it.

- **Wild: Skill-compat probe via `claude plugin eval` on every plugin update** — SECURITY — value 3 — effort M — risk low — category: interop
  Why: wild. When a pinned plugin's sha changes, run Foreman's 5 evals plus a hook-collision check in a temp HOME to see if the update broke gating or added conflicting hooks, and roll back to the last snapshot on failure. Evals already run in a temp HOME.
  Done when: bumping a fixture plugin to a version that blocks Foreman's Stop hook fails the probe and leaves the pinned sha unchanged.
