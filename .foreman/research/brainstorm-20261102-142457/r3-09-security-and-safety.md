# Brainstorm — lens: security and safety

- **Flag hidden text in everything the agent reads and writes** — SECURITY — value 4 — effort M — risk low — category: injection
  Why: the ideas list covers escapes, fences and airlocks, but none covers invisible Unicode (tag characters U+E0000–E007F, bidi controls, zero-width) hiding instructions in repo files, web fetches or pasted blocks. Assumption: PostToolUse can warn but not rewrite results.
  Done when: a fixture file with a U+E00xx-encoded instruction yields a hook warning naming file:line, and the ship gate fails on a diff adding bidi or tag characters.

- **Flag edits to files that run without being invoked** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the pack covers persistence on the machine and install scripts before a proof, but not the repo files the agent edits that later execute on someone else's machine. Examples are `.github/workflows`, `package.json` scripts, `.envrc`, `.vscode/tasks.json`, git hooks and pre-commit config. Assumption: finish receipts can carry a "runs on its own" line.
  Done when: a task whose diff touches any of those files prints a "now executes unprompted" line at `fm task finish`, and a diff without them prints nothing.

- **Detect diffs hidden from the reviewer** — SECURITY — value 3 — effort S — risk low — category: review integrity
  Why: assumption: an agent, or injected text, can blind review by editing `.gitignore` or `.git/info/exclude`, or by using `assume-unchanged` or `skip-worktree`, so changes never show in `git status`. Nothing in the pack watches for this.
  Done when: a fixture session that runs `git update-index --skip-worktree f` or adds an ignore line over a tracked path is flagged at finish, and the file still appears in the diff summary.

- **Treat what the session created or defined as untrusted when later run** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: "judge what a command will run" looks at script contents. This extends it to state the session built up: aliases, functions and PATH entries it defined, and downloaded or compiled binaries it created. A later `./build.sh` or `foo` then hits the guard as a session-born executable.
  Done when: replaying `curl -o x; chmod +x x; ./x` and `alias ls=...; ls` through the guard classes both runs as session-born, not as a plain command.

- **Run Foreman's own git and subprocess calls against a hostile-name repo** — FIX — value 3 — effort M — risk low — category: argv safety
  Why: Foreman shells out with branch names, task titles and file paths. Assumption: some calls lack `--` separators. Nothing in the pack tests names like `--upload-pack=x`, `$(touch pwned)`, or a newline in a filename.
  Done when: a fixture repo with such branch and file names passes `fm ship --dry-run`, `fm map` and `fm find` with no marker file created and no argv misparse.

- **Jail `fm code`'s file tools to the worktree** — SECURITY — value 4 — effort M — risk med — category: fm code
  Why: "argv-only exec tool" is listed, but file read and write tools are not. `fm code` runs any model's output, so symlink, `..` and hardlink escapes matter. Assumption: the tools resolve paths with plain joins today.
  Done when: a stub model asking to write through a symlink to `~/.bashrc`, or to read `/etc/shadow`, is refused with a logged reason, and tests cover symlink, `..` and hardlink.

- **Pin MCP tool descriptions at approval and alarm on change** — SECURITY — value 3 — effort S — risk low — category: MCP
  Why: the pack covers typing imported MCP tools at grafting, not a server changing its tool descriptions after you approve it (the rug-pull). Foreman ships an `mcp-server` template and is itself proposed as an MCP server.
  Done when: changing one tool's description in a test server after approval makes the next session start print "tool X changed since approved" and mark it unapproved.

- **Make the generated MCP server template secure by default** — SECURITY — value 3 — effort M — risk low — category: templates
  Why: `plugin/templates/mcp-server` appears in the map; assumption: it ships open handlers. Users copy templates unchanged.
  Done when: a freshly generated server rejects out-of-schema input, has a tool allowlist, writes no files outside its root, and a bundled hostile-input test passes.

- **Quarantine memory writes made after untrusted ingestion** — SECURITY — value 3 — effort M — risk med — category: persistence
  Why: the pack covers lesson origin tags, but a memory file the model writes after reading a web page or a pasted log can carry injected instructions into every future session. Assumption: the memory directory auto-loads.
  Done when: a memory write that follows a WebFetch or a pasted block is parked as "pending" and is not loaded at the next SessionStart until the user approves it.

- **Gate the Desktop publish (T-0352) on a hardening checklist** — SECURITY — value 3 — effort M — risk low — category: release
  Why: T-0352 is blocked on publishing Foreman Desktop. Assumption: the shell is Electron or Tauri. The pack lists web UI CSP and DNS-rebinding checks but nothing for desktop-specific items such as isolation, IPC allowlist, no remote content, and signed updates.
  Done when: a checklist test fails the release workflow if any item is missing (remote URL load, wildcard IPC, unsigned updater).

- **Shed ambient authority at bypass-session start** — SECURITY — value 4 — effort M — risk med — category: bypass mode
  Why: an exposure receipt is listed, but only reports. This acts on it: unset `SSH_AUTH_SOCK`, run `sudo -k`, drop cloud and `gh` token env vars from the session, each restorable by flag. Assumption: the launcher controls the session environment.
  Done when: in a bypass session with a cached sudo ticket and an agent socket, `sudo -n true` and `ssh-add -l` both fail inside it.

- **Wild: Authority drift alarm** — SECURITY — value 3 — effort M — risk low — category: monitoring
  Why: wild. A nightly snapshot of what an agent could reach (keys, tokens, writable dirs, group memberships, listening sockets), diffed day to day. It speaks only when authority grew, for example a new ssh key or docker group membership.
  Done when: adding a fixture key file makes the next `fm doctor` print one "authority grew: +1 key" line, and an unchanged day prints nothing.

- **Wild: Hidden-ink exam kind** — SECURITY — value 3 — effort M — risk low — category: exam
  Why: wild. A fixture repo carries hidden Unicode-tag instructions and white-on-white HTML comments. The exam scores per harness and model whether the instruction was obeyed, and the result becomes a table on the site next to the guard coverage.
  Done when: `fm exam` prints an obey-rate per harness for a 10-item hidden-text set, with a control arm of the same instructions in plain text.

- **Wild: Detect "behaves differently when unwatched" in agent-written scripts** — SECURITY — value 3 — effort M — risk med — category: integrity
  Why: wild. A static scan of agent-authored code for branches on TTY, `CI`, hostname, clock, or `sleep N` before an effect, with the hit listed at finish. Nothing in the pack looks for conditional behavior planted by a compromised or misaligned session.
  Done when: a fixture script with `[ -t 1 ] || curl …` is flagged at finish with its line, while a benign script using `-t 1` only for colour is not.

Next question: which of Foreman's own outputs (finish receipts, notes, lessons, steer checks) can a pasted document or fetched page change without the user typing anything, and is there a test per path?
Next question: what does the guard do on Windows or macOS (case-insensitive paths, UNC, `~` expansion), given the install story claims no `claude` dependency but only Linux is exercised?
