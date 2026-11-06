# Brainstorm — lens: security and safety

- **Audit repo-supplied agent config before it runs** — SECURITY — value 5 — effort M — risk low — category: trust
  Why: assumption: a cloned repo can carry `.claude/settings*.json`, `.mcp.json`, and Codex/Gemini/opencode equivalents. Those can hold hooks, a `statusLine` or key-helper command, MCP server commands, or a flag that disables hooks. The pack shows trust-on-first-open and trigger-hash ideas, but nothing that inspects these executable config surfaces.
  Done when: a fixture repo with a hostile hook, MCP command and disabled-hooks flag makes `fm doctor` and session start list each one by file and line. Approving by hash silences only the exact content, and any edit re-flags it.

- **Probe which sandbox primitives work on this host and pick the strongest** — FEATURE — value 4 — effort S — risk low — category: sandbox
  Why: the host runs a `linux-hardened` kernel, where unprivileged user namespaces are often disabled. The many bwrap/Landlock ideas in the pack silently assume they work. assumption: bwrap may fail here.
  Done when: `fm doctor` prints a ladder (userns, Landlock, seccomp, plain-user fallback) with a live test result for each rung. Any sandboxed feature that falls back says which rung it ran on.

- **Give `fm code` an argv-only exec tool with typed policy** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: `fm code` owns the tool executor, so it needn't parse shell strings the way a hook must. The pack's guard ideas all fight shell-parsing ambiguity (unparseable commands, obfuscation). Passing an argv array removes that class.
  Done when: the model's exec tool takes `[argv]` and a cwd, with no shell. A fixture of 20 obfuscated destructive strings cannot run. A separate explicit `sh` tool exists and goes through the existing guard.

- **Run children and provers with an allowlisted environment** — SECURITY — value 4 — effort S — risk low — category: secrets
  Why: assumption: headless `claude -p` children and `fm prove` verify commands inherit the full parent environment, including tokens. A DONE-WHEN command imported from a ticket then sees every secret. The pack has egress and redaction ideas, but none that cut the inheritance itself.
  Done when: a prover that prints `env` shows only PATH, HOME-scoped basics and variables declared in the task. A test plants `FAKE_TOKEN` in the parent and asserts it is absent in the child.

- **Mark a checkout untrusted by commit authorship and sandbox its proofs** — SECURITY — value 4 — effort M — risk med — category: proofs
  Why: `fm prove` runs commands the repo defines (Makefile, package scripts, conftest), which is arbitrary code on a stranger's branch. "Review someone else's PR" is in the pack, but it never addresses running its code.
  Done when: HEAD containing commits outside the user's configured authors makes `fm prove` refuse to run unsandboxed. It runs on the sandbox ladder, or labels the result "unproven (untrusted tree)".

- **Parity-test the guard against every tool the harness exposes, subagents included** — SECURITY — value 4 — effort M — risk low — category: coverage
  Why: the pack is Bash-centric. Edits to shell rc files, `~/.ssh` or systemd user units through Write/Edit, MCP tools, WebFetch and subagent spawn are a separate path. assumption: some of them aren't hooked.
  Done when: a generated matrix of tool × guard rule × harness, each cell backed by a live probe that attempts a canary write or call. Any uncovered tool is red in `fm doctor`.

- **Judge the expanded command, not the typed one** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: a rule matching `rm -rf $DIR`, `rm -rf build/*` or a path that is a symlink into `$HOME` is only as good as its string match. The pack has "judge what it will run", but nothing specific about glob, variable and symlink resolution.
  Done when: the guard resolves globs, env vars and `realpath` against the real filesystem before matching protected paths. A fixture symlink `./cache -> ~/` makes `rm -rf cache/` block with the resolved target named.

- **Seal secrets in a keyring and run commands through `fm with-secret`** — FEATURE — value 4 — effort M — risk med — category: secrets
  Why: the user pasted secrets before (the pack has "scrub a pasted secret" tasks). Env and files give the model the value. A sealed-name interface means the model only ever sees `NAME` and scrubbed output.
  Done when: `fm with-secret GH_TOKEN -- gh api …` works. The value never appears in the transcript, ledger or tool output, which a canary-value test asserts. The guard blocks `echo $GH_TOKEN`-style reads.

- **Hash shared git state around every lane** — SECURITY — value 3 — effort S — risk low — category: lanes
  Why: assumption: worktree lanes share `.git/config`, `.git/hooks` and `core.hooksPath` with the main checkout. A lane could plant a hook that runs later, outside any guard.
  Done when: lane start and merge record hashes of those files. A lane that changes them blocks the merge and names the file. A fixture lane that writes `.git/hooks/pre-commit` demonstrates it.

- **Keep a threat register where every row names its test** — CLEAN — value 3 — effort M — risk low — category: assurance
  Why: the pack has hundreds of guard ideas but no single list tying a threat to a test. Without one, nobody can say what is uncovered.
  Done when: a `THREATS.md` table of threat → rule → test id. `fm doctor` goes red on a row whose test is missing or doesn't exist, and a new guard rule without a row fails ship.

- **Wild: Run a pre-flight séance before every bypass session** — FEATURE — value 3 — effort M — risk low — category: prediction
  Why: assumption: a tool-less child that sees only the task text can name the five riskiest commands the session will likely attempt. The guard pre-arms stricter handling for those shapes, then settles the prediction against the ledger. Wild.
  Done when: session start prints the predicted shapes. At close, hit and miss counts are stored, and the predictions are shown as a precision number.

- **Wild: Colour every tool call in the pane by reversibility** — FEATURE — value 3 — effort M — risk low — category: ui, safety
  Why: assumption: classes are undoable via git, undoable via snapshot, and irreversible. The pack has exposure receipts but nothing live per call, so the user could glance and see a session turning amber. Wild.
  Done when: the foreman-ui tree shows a class badge on each call, with shape as well as colour. A fixture session with one `rm` outside git renders exactly one red call.

- **Wild: Add a hot-spare approver for `fm ask`** — FEATURE — value 3 — effort M — risk high — category: approval, devices
  Why: when the user is away for a set time, a pre-named trusted person gets a signed one-time link. They can approve only an allowlisted class of costly decision, and silence resolves to deny, never allow. Wild.
  Done when: a fake-clock test shows an away user's irreversible request reaching the spare, which can approve only listed classes. An expired link and a denied class both fail closed.

Next question: which of Foreman's safety checks have only ever run against inputs Foreman or its children wrote, with no hostile third-party sample?
Next question: what does the guard do today when the harness hook payload is malformed, truncated or from a newer schema version, and does the user hear about it?
