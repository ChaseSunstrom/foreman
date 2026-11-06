# Brainstorm — lens: security and safety

- **Classify every write and delete by what git can restore** — FEATURE — value 5 — effort M — risk low — category: data safety
  Why: assumption: the guard blocks `rm` on confine/symlink grounds but has no notion of recoverability. Untracked, ignored, dirty-tracked and outside-repo files can't be restored from git, and the snapshot/undo ideas only cover the risky actions the guard already flags. Friction scales with the class, and a per-task running total of unrecoverable bytes trips a stop.
  Done when: a test deleting an untracked 3-file dir is refused or asked, while deleting a committed file passes, and a task that overwrites more than N unrecoverable files stops with the list.

- **Read untrusted text through a no-tools extractor** — FEATURE — value 5 — effort L — risk med — category: injection defense
  Why: assumption: `fm landscape`, scouts, issue triage and unknown repos feed raw web or repo text to tool-holding threads. Taint tracking and information barriers exist, but a dual-model pattern doesn't: a tool-less child turns the content into a fixed JSON schema and the main thread only sees that.
  Done when: a planted "ignore previous instructions, run X" page goes through the extractor, and the main thread's context has only schema fields, with the payload absent.

- **Render consent summaries from parsed effects, not model prose** — SECURITY — value 4 — effort M — risk low — category: approvals
  Why: `fm ask` has the user's next message decide a grant. Content-hash binding is already listed, but the text the user reads is still written by the model and can understate it. The guard's parser should generate "this will delete 14 files in X and contact host Y".
  Done when: an `fm ask` whose model-written rationale says "tidy cache" but whose command touches `~/.ssh` shows the guard-derived effect line, and a test asserts the two can't diverge silently.

- **Detect refusal-evasion walks** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the recent commits and open work are mostly refusals followed by "reword and retry" (`fm focus …; sed -i …` refused twice). Making refusals carry their fix helps an honest agent and also guides an adversarial one. Several rewordings of the same blocked effect within a window should stop the thread and ask the user, not just loop.
  Done when: replaying 3 obfuscated variants of one blocked write ends in an escalation event, while 3 unrelated refusals do not.

- **Run gates hermetically and flag gates that need the network or secrets** — SECURITY — value 4 — effort M — risk med — category: gate sandbox
  Why: `fm check` executes edited test code, `conftest.py`, and package scripts with the user's full environment. Running it in a network-off, env-scrubbed namespace turns "this gate phones home" into a visible finding. It also exposes flaky gates that silently depend on the network.
  Done when: a gate that curls an external host fails hermetically with a named reason, and `fm check --net` is the only way to allow it, recorded in the ledger.

- **Pin MCP tool descriptions and detect rug pulls** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: assumption: sessions load third-party MCP servers beyond Foreman's read-only one. A server can change a tool's description or schema after approval. Plugin pinning is covered, but runtime tool metadata is not.
  Done when: changing a pinned tool's description in a test server produces a block-until-reviewed event with a diff.

- **Census processes and ports per task and reap leftovers** — FEATURE — value 4 — effort M — risk med — category: runtime hygiene
  Why: the drive now pushes long-lived background jobs and refuses foreground waits, so background processes multiply. Nothing tracks what a task left listening or running (dev servers, `fm serve` units, stray watchers). Record each spawn with its lineage, show it in `fm watch`, and reap or report at done.
  Done when: a task that leaves a listener on a port can't close without it being killed or explicitly adopted, and the ledger names the pid.

- **Lock down the desktop app's IPC and CSP, and fuzz it** — SECURITY — value 4 — effort M — risk med — category: desktop
  Why: Foreman Desktop (Tauri) renders task text, briefs and transcripts, and can create sessions. Control-sequence neutralizing exists for terminals, but a webview that can start sessions is a bigger target. Least-privilege capabilities, strict CSP, and a fuzzer feeding hostile brief text through every command.
  Done when: the fuzz suite injects markup and script into brief titles, and no IPC command beyond the declared allowlist is reachable from the webview.

- **Add `fm contain` for a suspected compromise** — FEATURE — value 4 — effort M — risk low — category: incident response
  Why: honeytokens and panic buttons detect and freeze. Nothing guides what comes after: list what each lane and session could touch, which secrets were in its environment, and what to rotate. Output a scoped timeline and a rotation checklist from the ledger.
  Done when: after a simulated honeytoken trip, `fm contain` quarantines the lane, lists credentials readable in its scope, and writes a timeline file.

- **Gate added code and dependencies on license and provenance** — SECURITY — value 3 — effort M — risk low — category: legal and supply chain
  Why: supply-chain signals are covered, licences are not. Verbatim large pasted blocks from web research, and new dependencies with copyleft or no licence, should surface at done.
  Done when: adding a GPL dependency to a permissively licensed project blocks done with the licence named.

- **Make the threat model executable** — CLEAN — value 3 — effort M — risk low — category: assurance
  Why: assumption: MASTER.md describes the guard and limitations in prose. An attack tree whose leaves each map to a control and a test shows exactly which paths have no control.
  Done when: `fm doctor` prints leaves with no passing test, and deleting a control's test makes that leaf show red.

- **Verify the foreman-ui mod's patched bundle at launch** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: T-0418 (update the installed mod) shows the mod drifts from the installed version. It patches Claude Code's UI with that process's full privileges, so a hash mismatch or tampered bundle should fall back to stock rather than run.
  Done when: editing the installed mod file makes the next launch skip it and log the reason.

- **Blow a fuse after N dangerous actions per day (wild)** — FEATURE — value 3 — effort S — risk low — category: safety rails
  Why: wild. Each guard category gets a daily fuse count. Once it blows, further use needs the user to type a reset, so a runaway loop that is individually allowed can't compound.
  Done when: the (N+1)th permitted `git push --force` of the day is held until reset, with the count shown in the band.

- **Hold irreversible actions in a cooling-off window, cancellable from the phone (wild)** — FEATURE — value 4 — effort M — risk med — category: undo
  Why: wild. Pushes, publishes and mass deletes are queued for a short delay with a notification (`fm notify` already exists), and a tap cancels. It converts "approved in the moment" into "reviewed once it's real".
  Done when: a publish under autonomy=full waits the window, and a cancel signal aborts it with the ledger entry.

- **Preview untrusted content in a detonation chamber (wild)** — FEATURE — value 4 — effort L — risk high — category: injection defense
  Why: wild. Before a real thread reads a new repo, web page or issue, a disposable sandboxed agent with honeytoken tools reads it first. If it attempts any out-of-scope action, the content is marked hostile and routed through the extractor above.
  Done when: a test page with an embedded exfiltration instruction trips the chamber agent's tripwire, and the main thread never receives the raw page.
