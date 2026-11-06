# Foreman capability catalogue (brainstorm 2026-10-09)

835 ideas, 103 capabilities; every idea is listed under exactly one capability.

## C056 Taste model and user portrait [Autonomy and the user]
Learn the user's preferences from their answers, steers and edits and pre-answer asks in their style.
- mark: build — First version: fm taste proposes vetoes from repeated steers for one yes, and uses the record to default fm decide answers. Skip twin runs, interviews, arenas, field notes; pre-answering approvals must never touch guard categories.
- status: partial; value 4/5; effort M; risk med
- evidence: fm taste (T-0112), steering as data/vetoes (T-0264), standing yeses, memory files; no auto-veto or proxy answering
- ideas: #11 Build a taste twin that answers for the user (wild) (near T-0280); #20 Predict the user's approvals to ask less (near T-0119); #27 Auto-write standing vetoes from the user's repeated steers; #34 Generate a "taste portrait" the user can read and edit (near T-0264); #41 Offer a "what should I do next" card ranked by what the user would pick (near T-0228); #54 Train a taste proxy that pre-answers asks; #82 Wild: blind twin run for risky tasks; #107 Pre-answer questions from a taste model while the user sleeps; #158 Teach by taste: learn the user's preference model and apply it to autonomy decisions; #216 Wild: Interview the user daily to build a living product vision; #230 Wild: Keep a "second user" journal that argues for the user's absent preferences; #241 Wild: Hand the user a "field notes" page Foreman writes about their own habits; #361 Interview the user weekly where the taste model is unsure; #637 Wild: Stream a 24/7 dogfood arena; #662 Wild: Detect rubber-stamp approvals and raise the stakes display

## C057 Ask less, ask better [Autonomy and the user]
Batch asks into a deadline-defaulted digest, rehearse them, order them by information gain and treat attention as a budget.
- mark: build — First version: in standard autonomy, collect non-urgent asks into one deadline-defaulted digest (default applied at the deadline, logged via fm decide). Skip rehearsal, information-gain ordering, pre-building answers.
- status: partial; value 3/5; effort S; risk low
- evidence: Full autonomy decide + final review (fm decide --review), digest of asks at end, fm ask batching, T-0364 keep working during waits
- ideas: #164 Learn the cost shape of tasks and tune lane/model choice from it; #183 Ask the user only when sampled plans disagree (near T-0364); #215 Rehearse the "ask" before interrupting the user; #223 Batch everything that needs the user into one deadline-defaulted digest (near T-0364); #232 Wild: Hand each queued task a "who would be annoyed" check; #262 Spend the user's attention as a budget and batch asks (near T-0228); #370 Meter the user's attention cost (near T-0350); #386 Ask questions by information gain (near T-0313); #505 Coach the user's requests from rework statistics; #508 Wild: Pre-build both answers to a blocking ask; #746 Learn from every interrupt (near T-0205)

## C060 Capture from anywhere [Autonomy and the user]
Capture tasks from selected text, screenshots, voice, recordings and pasted transcripts.
- mark: build — First version: fm capture --from-file/stdin for pasted text, logs or transcripts (with excerpt attached) plus a clipboard/selection hook in the desktop app; screenshots as attached paths. Skip voice, recordings, tweet-close-outs.
- status: partial; value 3/5; effort M; risk low
- evidence: fm capture/intake, Ctrl+Shift+C desktop capture (T-0348), fm second session mines transcripts for requests (T-0307), fm pr
- ideas: #12 Write a bug brief from a screen recording (wild); #205 Wild: Let the user draw on a screenshot to file a task (near T-0141); #410 Capture TODOs from the user's own edits (near T-0224); #428 Wild: Walk-and-talk intake; #435 Capture from any selected text, with the excerpt attached; #443 Wild: Capture tasks by voice, transcribed locally; #604 Draft upstream bug reports from harness quirks (near T-0379); #611 Turn the ledger into client-ready progress reports (near T-0280); #627 Write commits and PRs in the user's own voice (near T-0377); #630 Catch bugs the user hits in their own dev tab; #689 Require a tweet-length close-out a cold reader can check (wild)

## C059 Earned autonomy [Autonomy and the user]
Scale autonomy by track record, per model and task type, from a signed mandate or a rigor dial.
- mark: skip — Scaling autonomy from a track record could weaken guard categories; user already runs full. Keep only per-model/tier routing from bench, which exists (stronger: model routing).
- status: partial; value 3/5; effort M; risk high
- evidence: fm autonomy standard/full, fm bench models routing per tier (T-0223), standing yes, budgets by pace
- ideas: #286 Add a single rigor dial (near T-0277); #308 Wild: Earn autonomy licences per model and task type; #309 Wild: Run a constitution interview (near T-0170); #656 Throttle autonomy by unreviewed-diff debt; #702 Wild: Scale autonomy from a signed mandate; #830 Tune strictness with the budget of trust: graduated, earned autonomy

## C058 Away and return experience [Autonomy and the user]
Show what happened while the user was away, check they can walk away and approve from the notification.
- mark: skip — Mostly shipped. Residuals (dead-man heartbeat, heads-down, notification approve) are thin; heartbeat folds into the observer-health item.
- status: exists; value 2/5; effort S; risk low
- evidence: While-you-were-away row (T-0117), fm digest, fm notify, bench stranger/walk-away checks (T-0298), foreman-ui Review tab (T-0348)
- ideas: #30 Show a "what Foreman did while you were away" return screen (near T-0117); #233 Open each session with a one-line "where we left off" greeting (near T-0276); #432 Run a walk-away check before the user leaves (near T-0298); #438 Approve asks from the notification itself (near T-0009); #439 Run a heads-down mode that goes silent while the user types; #475 Send an external dead-man heartbeat for unattended work

## C025 Red-team and fuzz the guard [Guard and safety]
Attack the guard unattended with adversary agents, fuzzers and leagues, and keep every escape as a regression case.
- mark: build — First version: a differential fuzzer in tests that generates shell snippets from a grammar of mutations on known-blocked fixtures, runs fmguard and asserts no known-dangerous effect passes (oracle: bash -n plus a dry effect list in a tmp dir); escapes are saved as test fixtures. Read-only against the guard, so it only tightens.
- status: missing; value 5/5; effort M; risk med
- evidence: no fuzz/red-team in lib or tests; only tests/test_guard*.py and fm replay (fmreplay.py) exist
- ideas: #21 Red-team the guard unattended (near T-0298); #62 Fuzz the guard against real bash, unattended (near T-0411); #106 Red-team the guard nightly with an adversary agent; #134 Run a red-team subagent against the guard (wild); #159 Wild: Foreman dreams: an overnight self-play fuzzer that attacks its own guard; #272 Let two lanes duel a risky guard change in public; #374 Guard playground with a differential against real bash (near T-0411); #534 Wild: Keep a red-team decoy repo that fights back against injections; #801 Treat the guard as a verified artifact: formal-ish differential fuzzing against real bash with property invariants; #818 Fuzz the guard continuously (wild); #823 Fuse the guard into a closed-loop "adversary–defender–judge" engine; #828 Run the guard as a cross-harness conformance suite; #832 Wild: Publish a guard "fuzz league" where models try to break it

## C035 Panic, containment and paranoia [Guard and safety]
A visible kill switch, freeze-everything button, paranoid-hour dial and compromise containment.
- mark: build — fm pause: one flag file that makes the Stop drive, fm run/serve/night and lane launches stop, and sets autonomy to standard; fm resume clears it. Only tightens; the user can toggle it.
- status: partial; value 4/5; effort S; risk low
- evidence: fm drive off, fm autonomy, fm trust, fm budget caps exist; no single pause/freeze or paranoid dial
- ideas: #288 Add `fm pause` as a visible kill switch; #334 Wild: Add a panic button that freezes everything; #526 Trip an anomaly dead-man's switch on unattended runs; #533 Wild: Let the user toggle a "paranoid hour" that raises every dial at once

## C024 Refusals that carry their fix [Guard and safety]
Every guard refusal says what is allowed instead, rewrites the command, and stops loops of repeated refusals.
- mark: build — Audit refusal messages so each names the allowed form (fixture test that every block reason has an 'instead/use' clause), and add a repeated-refusal counter in the hook that escalates to fm ask or task block after 3 identical blocks. Never rewrites and runs commands itself.
- status: partial; value 4/5; effort M; risk low
- evidence: fmguard.py refusals often name the way out (e.g. 'refusal names fm lane merge' L1935); fm ask on blocks; no repeat-loop detector
- ideas: #5 Turn guard refusals into self-fixing tasks (near T-0411); #31 Narrate the guard's refusals as a friendly teaching moment; #87 Make every refusal carry its fix (near T-0227); #91 Resume the one plausible task instead of refusing (near T-0080); #153 Turn every guard false-positive into a regression corpus automatically; #226 Spot repeated guard refusals and stop the loop (near T-0411); #234 Show each refusal as a before/after command pair (near T-0414); #616 Test refusal messages with a cold reader (near T-0164); #680 Rewrite a refused command into its allowed form (near T-0413); #826 Make refusals a conversation: refuse with a fix, not a wall (near T-0015); #827 Close the loop: turn each refusal into a labelled example automatically

## C031 Exfiltration and secrets [Guard and safety]
Scan outbound data, redact secrets at write time, plant honeytokens and label information flow between projects.
- mark: build — Extend fm secrets into a done-gate check on the task diff and outbound-looking commands (curl/scp of files matching secret patterns) already refused by guard; skip honeytokens. Strictly adds refusals.
- status: partial; value 4/5; effort M; risk med
- evidence: fm secrets scans tree, config and git history (fmsecrets.py); fmcore redaction patterns; guard refuses secret-named files; no honeytokens or outbound scan
- ideas: #130 Scan all outbound data: sync, share, eval capture, export; #329 Run a pre-push egress manifest (near T-0264); #331 Compartmentalize projects with information-flow labels; #332 Redact secrets at write time into ledger, briefs and evidence; #528 Scrub and expire Claude's own transcripts (near T-0328); #529 Audit Foreman's own file and socket permissions (near T-0205)

## C033 Harness parity of the guard [Guard and safety]
Enforce and test the guard identically on every harness shell form, with a PATH shim and a published enforcement matrix.
- mark: build — Generate an enforcement matrix from fmagents capability tables (which events block, which only warn) into fm doctor, and run the guard fixtures through each adapter's payload shape.
- status: partial; value 4/5; effort M; risk low
- evidence: fmagents.py installs guard for codex/gemini/opencode; hook fixtures in tests/fixtures/hook_payloads.json; no enforcement matrix
- ideas: #330 Check guard parity per harness shell form (near T-0421); #368 Publish a live-tested enforcement matrix per harness; #506 Wild: Run two independent guards and treat disagreement as a bug; #681 Enforce the guard with a PATH-shimmed shell on every harness (near T-0414); #719 Detect refusal-evasion walks; #758 Check read-before-edit coverage (near T-0264)

## C036 Cleanup as a done gate [Guard and safety]
Sweep leftovers after every task, treat cleanup as a done obligation and run a recurring janitor with deletion-safety proof.
- mark: build — In fm check/finish, list untracked files and stray tmp/worktrees the task created that are outside its scope and warn (block only with a flag). Reuse fmtidy lists.
- status: partial; value 3/5; effort S; risk low
- evidence: fm tidy (fmtidy.py) hygiene; CLEAN stage and audit.md; no per-task leftover sweep gate
- ideas: #3 Make cleanup a gate (near T-0291); #18 Enforce cleanup as a done-gate obligation (near T-0291); #84 Run a deletion pass as a first-class CLEAN gate (near T-0291); #100 Sweep leftovers after every task (near T-0364); #117 Make the cleanup agent a recurring janitor with proof of deletion safety

## C030 Snapshots, undo and irreversibility [Guard and safety]
Snapshot before risky actions, classify what git can restore, keep an effect ledger and budget irreversible steps.
- mark: build — First version: before a destructive-category grant is used, record git stash-create/HEAD sha in the task log and name restorable vs irreversible in the ask text. No effect ledger yet.
- status: partial; value 3/5; effort M; risk med
- evidence: lanes in worktrees, fm checkpoint, fmtidy/fmdoctor quarantine (never delete); no pre-action snapshot or effect ledger
- ideas: #132 Auto-snapshot before risky actions and add `fm undo` (near T-0004); #238 Offer "undo that" after any Foreman-initiated change; #305 Govern infrastructure and data changes with plan, apply, rollback; #328 Give autonomy=full an irreversibility budget (near T-0276); #335 Wild: Keep an effect ledger with compensating actions; #336 Wild: Require two-vendor concurrence for irreversible actions; #716 Classify every write and delete by what git can restore; #727 Blow a fuse after N dangerous actions per day (wild); #728 Hold irreversible actions in a cooling-off window, cancellable from the phone (wild)

## C032 Supply-chain and install trust [Guard and safety]
Gate dependency changes, quarantine unknown repos, pin and diff plugins and MCP descriptions, and sign releases.
- mark: build — Record a content hash of each enabled plugin and MCP tool description in doctor and warn on change between runs. Detection only.
- status: partial; value 3/5; effort M; risk low
- evidence: fm plugins find/install behind fm ask plugin --pin (fmplugins.py); guard gates installs; no diff of plugin/MCP descriptions
- ideas: #131 Gate dependency changes on supply-chain signals (near T-0261); #325 Quarantine unknown repos before trusting their config; #337 Sign Foreman's own releases and updates (near T-0013); #531 Pin and diff plugins, skills and hooks on update (near T-0366); #721 Pin MCP tool descriptions and detect rug pulls; #726 Verify the foreman-ui mod's patched bundle at launch

## C034 Hardening Foreman's own surfaces [Guard and safety]
Neutralise control sequences, audit symlinks and permissions, lock down the desktop IPC, fuzz the approval parser and keep an executable threat model.
- mark: build — First version: one sanitizer for rendered strings (strip ESC/OSC) applied to statusline and task output, plus a fuzz test of the approval-phrase parser in fmcore. Skip desktop IPC lockdown here.
- status: partial; value 3/5; effort M; risk med
- evidence: control-sequence handling in fmguard/fmclaude/fmmission; fm doctor checks; threat model only as fm outline flags (fmcli.py:2507); symlink handling in fmcore/fmsync
- ideas: #338 Fuzz the approval and grant parser with adversarial user messages; #522 Neutralize control sequences in every rendered string (near T-0144); #523 Watch the persistence surface at the done gate (near T-0318); #621 Audit lane writes that pass through symlinks (near T-0286); #694 Keep a living threat model and data-flow map for the user's product; #723 Lock down the desktop app's IPC and CSP, and fuzz it; #724 Add `fm contain` for a suspected compromise; #725 Make the threat model executable (near T-0276)

## C026 Guard as policy data and verified artifact [Guard and safety]
Express guard rules as data with origins and fire records, compile them to an effect IR, and prove a rule change can't loosen the guard.
- mark: build — Cheap first step only: log a rule id per block into the event log and report fire counts in fm friction/replay (decision ledger). Defer the data-table rewrite and IR; a rewrite risks loosening the guard, so gate it on the monotonicity check via fm replay.
- status: partial; value 3/5; effort L; risk high
- evidence: fmguard.py is 2.5k lines of code rules; fm replay compares decisions (fmreplay.py); no rule origins or fire counts
- ideas: #170 Show a guard decision ledger with false-positive tracking (near T-0269); #182 Abstract-interpret shell for effects in the guard (near T-0345); #210 Turn plain-language policy statements into tested settings; #268 Express guard rules as data in a policy engine; #290 Make the guard a declarative policy table (near T-0162); #465 Promote guard rules from warn to enforce on replay evidence; #527 Prove a safety non-regression before evolve promotes; #564 Score the guard's decisions against later outcomes (near T-0187); #585 Wild: Synthesise guard rules by counterexample-guided search; #757 Detect guard circumvention (near T-0153); #764 Give guard rules an origin and a fire record (near T-0169); #824 Compile the guard into an effect IR with a verified interpreter (near T-0170); #834 Prove guard monotonicity: a rule change can't silently loosen

## C027 Sandbox and preview risky commands [Guard and safety]
Judge or run risky commands in an OS sandbox or shadow filesystem before touching the real one.
- mark: skip — Running judged commands changes the guard's trust model and can loosen it for the 'unknown' cases; Claude Code's own sandbox already exists. Near-duplicate value is better served by the fuzz differential (Red-team and fuzz the guard).
- status: partial; value 3/5; effort L; risk high
- evidence: fmguard.py:5 says it is a speed bump, not a sandbox; sandbox mentions in fmevolve/fmsession only
- ideas: #89 Replace guard heuristics with an OS sandbox for the unknown cases (near T-0355); #105 Judge risky commands by running them in a sandbox (near T-0019); #124 Run guarded commands inside an OS sandbox as a second layer (near T-0190); #135 Preview risky commands in a shadow filesystem (wild); #524 Execute exactly what was judged (near T-0414); #729 Preview untrusted content in a detonation chamber (wild); #831 Wild: Let the guard run a shadow universe and diff reality

## C028 Taint and provenance of untrusted content [Guard and safety]
Track untrusted text through a session and gate actions it triggers, reading it only through tool-less extractors.
- mark: skip — Hard to do at the hook level without session semantics and the premise needs model cooperation; value-per-effort low. Revisit via scoped capability limits for lanes instead.
- status: missing; value 3/5; effort L; risk med
- evidence: no taint tracking; fmoutside.py handles outside-project content only
- ideas: #127 Taint-track untrusted content and gate actions it triggers (near T-0012); #128 Track write-then-execute provenance (near T-0370); #133 Plant honeytokens to catch exfiltration (wild); #333 Wild: Run prompt-injection drills on the live agent (near T-0148); #525 Quarantine lessons that came from untrusted input; #530 Tag message provenance between sessions and lanes (near T-0167); #717 Read untrusted text through a no-tools extractor (near T-0328); #829 Keep a taint ledger across the whole session, not per command (near T-0097)

## C029 Capability scopes and bound approvals [Guard and safety]
Give each lane least privilege, broker credentials, bind approvals to content hashes and signed capabilities, and audit grants.
- mark: skip — Core grant system already binds approvals to category and task; signed/hash-bound capabilities add crypto surface and touch approval logic where mistakes loosen the guard. Skip until a concrete grant-replay bug appears.
- status: partial; value 3/5; effort L; risk high
- evidence: fm ask categories and standing grants (fmcore.py), lane scope in fmlanes.py, trust lock via fm trust
- ideas: #129 Give each lane a least-privilege capability scope; #136 Require signed approvals for `fm ask` from other devices (near T-0318); #326 Broker credentials so sessions never hold real ones; #327 Bind approvals to content hashes (near T-0036); #371 Audit grants with expiry and usage (near T-0216); #718 Render consent summaries from parsed effects, not model prose; #825 Give every approval a signed, content-bound capability (near T-0234)

## C037 Guard anomaly learning [Guard and safety]
A guard that learns the project's normal and flags anomalies, with graduated strictness.
- mark: skip — A learned guard can loosen what is refused by treating the normal as safe; value is low versus replay-based evidence. Better served by Guard as policy data (fire records) and Red-team and fuzz the guard.
- status: partial; value 2/5; effort L; risk high; wild
- evidence: fm replay shows newly blocked/allowed per real command (fmreplay.py); fm friction; no learned baselines
- ideas: #79 Wild: self-healing guard patches; #396 Show the guard's reasoning as an interactive parse tree (near T-0180); #767 Run a trust-fall drill on the human reviewer (near T-0327); #833 Wild: Guard that learns the project's normal and flags anomalies; #835 Wild: A guard "explain" mode that narrates verdicts as a trace

## C078 Cross-project requests, sweeps and friction [Multi-machine, multi-project and ecosystem]
Let projects ask each other for changes and sweep or transplant a fix across all projects.
- mark: build — First version: `fm sweep "<fix>"` that, for each registered project, runs fm recall/grep for the sibling pattern and captures a brief in that project's inbox (source cross-project); plus consumer friction into briefs via fm friction. No auto-edit of other repos.
- status: partial; value 4/5; effort M; risk low
- evidence: fm projects lists all projects (fmwatch.py:502); fm share recalls lessons across projects (fmrecall.py:406); no cross-project capture/sweep
- ideas: #23 Let projects request changes from each other (near T-0375); #64 Coordinate a fleet across projects (near T-0041); #227 Show which fixes each downstream project is missing (near T-0318); #250 Land changes across several repos as one atomic set; #408 Sweep a fix across all my projects (near T-0375); #451 Run codemod campaigns; #502 Transplant a fix to sibling code across projects (near T-0328); #615 Sweep a fix across its sibling sites; #623 Wild: Give each consumer project an ambassador; #624 Wild: Collect a candid state of the union from each consumer; #814 Turn downstream friction into briefs (near T-0224)

## C082 Adopting an existing repo [Multi-machine, multi-project and ecosystem]
Adopt a legacy repo with a baseline scan, safety crawl, characterization and a practice run.
- mark: build — First version: `fm adopt` that runs map, gates, secrets, deps and a flake pass once, records a baseline brief with failing gates and untested hot files, and queues CLEAN/RESEARCH tasks. Great for new projects like JARVIS siblings.
- status: partial; value 4/5; effort M; risk low
- evidence: fm init, fm map, fm check discovery, fm bench build --commits (T-0222), fm secrets exist; no baseline health scan or characterization
- ideas: #213 Adopt an existing repo with a baseline health scan; #287 Infer the whole init from the repo and history; #306 Onboard a legacy repo with a safety crawl; #355 Examine Foreman on any repo's git history (near T-0394); #413 Generate a hermetic dev environment from what the gates need; #479 Contract-test the JSON surfaces that consumers read (near T-0322); #501 Score and improve how legible a repo is to agents; #753 Wild: Practice on a new repo before touching it (near T-0222)

## C084 Version skew and upstream drift [Multi-machine, multi-project and ecosystem]
Alert when a project runs an old Foreman and show which fixes each project lacks.
- mark: build — First version: in fm projects/doctor, show per project the Foreman version it last ran and which CHANGELOG T-ids it lacks; extends T-0391. Skip auto-upgrades and upstream PRs.
- status: partial; value 3/5; effort S; risk low
- evidence: check_running_code flags the Foreman code a project's last session ran vs installed (T-0391, fmdoctor.py:334); fm deps lists outdated dependencies (T-0278)
- ideas: #254 Automate dependency upgrades from `fm deps` (near T-0278); #372 Track version skew across projects; #472 Pin each session to a Foreman version during upgrades; #571 Alert on drift between installed Foreman and the repo's HEAD per project (near T-0296); #697 Watch upstream contracts and turn drift into briefs; #700 Wild: Send upstream fixes for bugs that bite the user's dependencies

## C081 Trackers and CI [Multi-machine, multi-project and ecosystem]
Bridge issues, PR comments and CI, triage public issues and review others' PRs with Foreman's lenses.
- mark: build — First version: `fm inbox gh` that reads open issues of the repo via gh (read-only) and captures each as a brief with repro command; PR review comments later. Treat issue text as untrusted data.
- status: missing; value 3/5; effort M; risk med
- evidence: no gh issue/PR bridge in plugin/lib; fm pr only writes a description (T-0417 smoke covers product, not trackers)
- ideas: #53 Turn production signals into briefs (near T-0417); #208 Tell the user's edits from the agent's (near T-0120); #214 Triage public GitHub issues into reproduced briefs; #246 Bridge trackers and PR review comments into the queue; #248 Review other people's PRs with Foreman's lenses in CI (near T-0286); #269 Triage the public repo's issues into briefs (near T-0134); #414 Review the user's own commits in the background (near T-0116); #452 Gate human commits with git hooks (near T-0291); #650 Adopt the user's manual commits into the ledger (near T-0220)

## C083 Harness and Claude Code compatibility [Multi-machine, multi-project and ecosystem]
Contract-test Foreman against Claude Code and plugin surfaces, turn releases into adaptation tasks and run on other harnesses.
- mark: build — First version: a canary that records `claude --version` per session and, on change, runs the guard fixtures, fm replay and a hook smoke; failure captures a brief. Skip the single binary and portable kernel.
- status: partial; value 3/5; effort M; risk low
- evidence: fm landscape (T-0278), fmdoctor check_hook_events/check_settings_json, check_running_code (T-0391), fm agents for codex/gemini/opencode
- ideas: #75 Canary new Claude Code versions (near T-0406); #279 Contract-test Foreman against Claude Code's hook and settings surface (near T-0216); #291 Ship Foreman as one self-contained binary; #292 Extract a tiny portable kernel for the adapters; #412 Turn Claude Code releases into adaptation tasks (near T-0145); #478 Test Foreman beside popular plugins at runtime (near T-0280); #483 Verify tool versions at startup, not just at install (near T-0379)

## C079 Machines, identity and shared lessons [Multi-machine, multi-project and ecosystem]
Run the queue and gates across machines with leases, logical clocks, durable state in git refs and one identity everywhere.
- mark: skip — Leases, logical clocks and DP lessons are a distributed-systems build for a single-user setup; fm sync plus git already covers cross-machine state. Cheap piece (restore rehearsal of backups/*.tgz) belongs under Crash-safe state.
- status: partial; value 3/5; effort L; risk med
- evidence: install.sh one-liner and git pull move Foreman between machines (MASTER.md:241); doctor check_backup (fmdoctor.py:247); fm sync on mirrors state into repo .foreman/; no leases/clocks
- ideas: #8 Fleet across machines; #24 Run the queue across machines (near T-0318); #56 Share bench-proven lessons between teams; #68 Federate Foremen across machines; #108 Dispatch lanes across machines with queue leases; #147 Wild: Shard gates across machines; #185 Run lanes across machines; #477 Back up central state and rehearse the restore; #605 Carry the user's identity to any machine or project (near T-0280); #655 Keep durable state in git refs so sync and multi-machine come free; #673 Order events with logical clocks for multi-machine work; #682 Keep central state in a git ref instead of a private store; #777 Share lessons with differential privacy (near T-0295)

## C080 Extensions and delegation to others [Multi-machine, multi-project and ecosystem]
Offer an SDK, project-owned gates and lenses, a typed MCP surface and an LSP, and act as a delegate for other orchestrators.
- mark: skip — SDK, LSP and delegate mode have no consumer beyond the user; MCP and adapters exist. Project-owned gates already exist as fm check commands.
- status: partial; value 2/5; effort L; risk med
- evidence: fm mcp read-only tools (T-0245, fmmcp.py); fm export agents AGENTS.md; fm agents installs guard into codex/gemini/opencode
- ideas: #319 Offer Foreman as a delegate to other orchestrators (near T-0207); #445 Add a Foreman extension SDK; #464 Open extension points for project-owned gates and lenses (near T-0215); #485 Make the fm CLI an implementation detail behind typed MCP tools; #648 Serve Foreman's knowledge to any editor as an LSP (near T-0016)

## C066 Observer health [Observability, replay and trust]
Prove the hooks and observers are alive with heartbeats, canaries, witnesses and swallowed-error counts.
- mark: build — First version: count swallowed exceptions in hooks into a log, doctor and fm friction read it, plus a canary fixture the Stop hook checks per session so a blind observer is flagged. Skip randomized drills and witness sessions.
- status: partial; value 4/5; effort S; risk low
- evidence: Hook circuit breaker (T-0087), SessionStart heartbeat (fmhooks.py:356), fm doctor hook latency and fixtures, fm replay, fm sentinel
- ideas: #283 Wild: Keep a black-box flight recorder for the last 200 hook events (near T-0115); #377 Wild: Keep a witness that only observes; #378 Wild: Fire randomized trust drills at the observers themselves; #444 Wild: Open a "near-miss reel" of saves; #561 Run a trust-regression suite on Foreman's own observers; #562 Show a hook-coverage heartbeat per session (near T-0318); #567 Detect the observer being blind: silent-failure canaries; #568 Wild: Keep a witness session that re-derives STATE from raw transcripts (near T-0212); #667 Count every swallowed exception in the hooks (near T-0087); #759 Probe cross-surface state parity

## C064 Explain why [Observability, replay and trust]
Answer why did you do that with causal traces, wall-clock critical paths and budget causality.
- mark: build — First version: fm explain on a guard block or a drive/Stop decision prints the rule, inputs and ledger events behind it from existing logs (breaker, ledger). Skip per-action keystroke UI and round-trip counts.
- status: partial; value 3/5; effort S; risk low
- evidence: fm why FILE (commits and tasks), fm cost says where time went (T-0188), guard block messages, ledger events
- ideas: #172 Explain idleness live; #178 Show budget causality (near T-0318); #219 Hold a one-keystroke "why did you do that?" on any action; #339 Profile where a task's wall-clock went (near T-0188); #356 Profile where each task's time and tokens went (near T-0188); #536 Count wasted round trips per task (near T-0245); #563 Explain every state change with a causal trace (near T-0318)

## C061 Task replay as a scrubbable story [Observability, replay and trust]
Replay a finished task or day as a scrubbable timeline, time-lapse or receipt.
- mark: build — First version: fm task show ID --story prints the ledger as chapters (plan, steps, evidence, reviews, close) with times, rendered in the desktop Review tab. Skip time-lapse and shareable receipts (see trust passports).
- status: partial; value 3/5; effort M; risk low
- evidence: fm tour (T-0263), ledger events, fm watch, fm pr proof sections, fm bench replay
- ideas: #13 Replay a task as a scrubbable story; #29 Replay a finished task as a scrubbable timeline (near T-0280); #38 Wild: Turn each finished task into a one-screen shareable "receipt"; #171 Scrub a task like a flight recording (near T-0338); #196 Scrub through a task like a video (near T-0286); #442 Wild: Render a day as a 20-second time-lapse; #592 Fold the ledger into collapsible chapters

## C065 Ask the project's memory [Observability, replay and trust]
Search and question the ledger, history and code by meaning, locally.
- mark: build — First version: fm recall --ask QUESTION over briefs, ledger, decisions, research using keyword/BM25 ranking in stdlib (sqlite3 FTS5 is stdlib) with cited task ids. Skip embeddings and OTel export.
- status: partial; value 3/5; effort M; risk low
- evidence: fm recall (T-0043, T-0343), fm mcp read-only tools, fm research ask, fm why, fm usage; no embeddings, no sqlite
- ideas: #143 Index briefs, ledger and recall in SQLite (near T-0276); #409 Search code and history by meaning, locally (near T-0116); #434 Interrogate the project's memory in plain language; #453 Ask the ledger in plain language; #454 Export traces over OpenTelemetry (near T-0263); #466 Recall by meaning with a local index (near T-0276); #467 Answer questions about Foreman's own history; #665 Give every event stream a cursor and replay (near T-0376); #732 Roll up transcripts and the ledger incrementally (near T-0276)

## C062 Replay under other plans and models [Observability, replay and trust]
Deterministically replay a session against a candidate plan, model or plugin and fork it from any point.
- mark: skip — Core need is met by fm bench with --models and version replays; deterministic fork/time-travel needs ledger-level determinism the model can't give. Near-duplicate of fm bench.
- status: partial; value 3/5; effort L; risk med
- evidence: fm bench run replays finished tasks under candidate plugin/model (T-0212, T-0223), fm second plan (another model), fm replay for guard
- ideas: #26 Replay a task under a different plan or model (near T-0276); #67 Replay a whole session against a candidate plugin (near T-0296); #104 Replay whole task runs deterministically and fork them; #160 Wild: Time-travel debugging of Foreman's own decisions; #188 Replay sessions deterministically to find the first wrong step (wild)

## C063 Tamper-evident evidence [Observability, replay and trust]
Hash-chain the ledger, bind evidence to the tree, tag who acted and anchor the head outside the machine.
- mark: skip — The agent and ledger live on the same user machine; a hash chain adds little against the real threat (the model), and anchoring externally is outside scope. Tree-bound evidence already covers false-done.
- status: missing; value 2/5; effort M; risk low
- evidence: No prev-hash chain in ledger; evidence bound to tree already (T-0261), approvals bound to session (hardening)
- ideas: #81 Wild: tamper-evident evidence ledger (near T-0276); #126 Hash-chain the ledger and evidence, and run gates out of the model's reach (near T-0220); #167 Chain the ledger with hashes; #307 Make Foreman's own evidence reproducible years later (near T-0165); #366 Bind evidence to the tree it proved (near T-0261); #367 Attest that the guard was in the loop (near T-0411); #572 Record a tamper-visible "who acted" tag on every ledger event; #763 Stamp model and build on every event (near T-0224); #766 Anchor the ledger head outside the machine (near T-0280); #807 Make evidence tamper-evident with a hash-chained ledger and a signed done receipt

## C067 Trust passports and attestations [Observability, replay and trust]
Publish signed receipts, run records, redacted spectator links and trust passports for outsiders.
- mark: skip — Outsider-facing attestations have little value for a solo autonomous user; fm pr already carries proof. Redacted publishing risks leaking data.
- status: partial; value 2/5; effort M; risk med
- evidence: fm pr proof sections (T-0263), fm export agents, fm sentinel; no signing or public views
- ideas: #176 Attach a signed attestation to every release or PR; #303 Verify evidence in CI for any agent's PR (near T-0379); #375 Wild: Publish a trust passport for each project; #566 Publish a verifiable run record for outside review; #570 Wild: Let the user ask "show me the least-verified thing you shipped this week"; #631 Share a read-only live view of a run (near T-0328); #768 Open a redacted spectator link

## C068 Wild observability bets [Observability, replay and trust]
Prediction markets, time capsules, near-miss reels, behaviour time machines and a monthly yearbook.
- mark: skip — Prediction markets, yearbooks and time capsules are novelty with low value for this user; the useful core (predicting gate outcomes) is covered by estimates item.
- status: missing; value 1/5; effort M; risk low; wild
- evidence: Nothing similar; fm digest and fm taste are the closest
- ideas: #310 Wild: Keep a behaviour time machine; #441 Wild: Publish a monthly project yearbook; #584 Wild: Open a prediction market on gates; #636 Wild: Seal time capsules for predictions

## C014 Dependency-aware lane dispatch [Orchestration, lanes and fleets]
Dispatch the queue as a dependency graph across builder lanes, scheduled by predicted cost, risk and file footprint, with a durable scheduler.
- mark: build — Make --parallel pick lanes from the fm relate graph plus a predicted file footprint (scope plus fm impact/co-change), and have drive offer the same set; skip solver/cost-prediction extras.
- status: partial; value 4/5; effort M; risk low
- evidence: fm run --parallel N (T-0167) picks disjoint-scope S/M tasks; fm relate (fmrelate.py) infers task deps; fm lane brief
- ideas: #46 Run the queue as a dependency graph across lanes; #111 Dispatch the queue as a dependency DAG across parallel builder lanes (near T-0257); #140 Dispatch lanes from the queue automatically (near T-0375); #186 Schedule the queue from predicted cost and risk; #499 Forecast file footprints to catch queue conflicts (near T-0277); #500 Mine a hidden-coupling graph from surprises and co-change; #545 Wild: pack lanes by predicted file overlap (near T-0403); #660 Schedule the queue with a constraint solver and explain infeasibility; #709 Choose the orchestration shape per task, learned from bench; #809 Build a durable lane scheduler (near T-0429); #817 Tune scheduling policy with bench (near T-0264)

## C015 Merge train and conflict resolution [Orchestration, lanes and fleets]
Land lane output through a speculative merge train, resolving conflicts from both briefs' intent and proving a merge before it lands.
- mark: build — On a conflicting lane merge, keep the lane and spawn a resolver session given both briefs plus the conflict hunks, re-gated before landing; no speculative train yet.
- status: partial; value 4/5; effort M; risk med
- evidence: fm lane merge (fmlanes.py:166) rebases, gates, refuses dirty main, aborts conflicts (T-0403); CHANGELOG left to main (T-0428)
- ideas: #1 Run a merge-train lane fleet (near T-0428); #73 Prove a merge before it lands (near T-0280); #515 Add an integrator agent that owns the seams between lanes; #640 Stack a task's diff into independently green commits (near T-0234); #641 Resolve lane merge conflicts using both briefs' intent; #690 Merge by re-deriving, not by diffing (near T-0382); #734 Rebase lanes continuously so merges are fast-forwards (near T-0167); #810 Test a speculative merge train; #822 Reconcile lane intent at merge time

## C020 Failover, preemption and rescue [Orchestration, lanes and fleets]
Continue a task on another agent or harness when quota runs out or a session dies, and park and resume lanes at the exact step.
- mark: build — First step: fm run/drive detect a session with no progress for N minutes (ledger/transcript mtime), kill and resume it from the checkpoint, and on a usage limit hand the task to another installed agent via fm session.
- status: partial; value 4/5; effort M; risk low
- evidence: fm run --wait waits out usage limits (Round 8); fm session starts codex/gemini/opencode (fmsession.py); fm resume; no wedged-session detector
- ideas: #207 Continue a task on another agent when usage runs out (near T-0125); #221 Fail over a task to another harness when quota runs out; #277 Detect and recover a wedged or dead session; #284 Wild: Hold a keep-alive twin that takes over when the main drive dies; #373 Bundle an incident on any stuck or confused session; #429 Wild: Dead-man's-switch succession; #509 Wild: Let Foreman interview a dead session; #705 Park lanes on preemption and resume them at the exact step

## C017 Lane isolation and host health [Orchestration, lanes and fleets]
Give each lane its own runtime, copy-on-write tree, file leases and sandbox, and admit lanes by machine load.
- mark: build — First step: fm run --parallel and drive lane offers check os.getloadavg/free memory and cut lane count; fm lane rm reaps leftover processes. Skip microVMs and CoW trees.
- status: partial; value 3/5; effort S; risk low
- evidence: git worktree lanes (fmlanes.py); fm budget caps spend; no load or process census (grep loadavg none)
- ideas: #55 Run tasks in disposable microVM sandboxes; #224 Lease files between lanes and the main thread (near T-0428); #345 Make lane creation instant with copy-on-write dependency trees; #646 Add a host health governor for lanes and gates; #664 Journal every spawned resource and reap the orphans; #698 Admit lanes by machine load (near T-0367); #722 Census processes and ports per task and reap leftovers; #733 Tune lane concurrency like TCP

## C021 Unblock blocked tasks and hand off [Orchestration, lanes and fleets]
Park a blocked task and keep going, using scouts, unblock probes and scoped privileged steps.
- mark: build — fm task packet ID: one markdown with brief, evidence, blocker, tried steps and next probe, for a human or another machine; plus drive running a scout on blocked tasks. Skip team claims.
- status: partial; value 3/5; effort S; risk low
- evidence: fm task block, drive names a task to block (T-0401), fm ask, fm second; no handoff packet or bundle
- ideas: #255 Add team claims for multiple humans (near T-0228); #311 Hand a task to a human with a packet; #315 Unblock blocked tasks with scouts (near T-0341); #340 Park a blocked task and keep going (near T-0423); #647 Broker scoped privileged steps for blocked tasks (near T-0296); #657 Export a live task as a portable bundle another machine or person resumes

## C022 Speculative and idle-time work [Orchestration, lanes and fleets]
Use idle and overnight time to pre-plan, rehearse and dream over old failures so the next task starts faster.
- mark: build — Extend fm night with a friction pass over the log plus a read-only pre-plan of queued L tasks written into the brief; no speculative edits or hot spares.
- status: partial; value 3/5; effort M; risk med; wild
- evidence: fm night runs second read, landscape, research debt, court, evolve (fmnight.py); drive fills idle with queued work (T-0401, T-0415)
- ideas: #10 Dream mode (wild); #57 Dream overnight on old failures; #66 Run speculative overnight lanes ("dream queue"); #121 Run a swarm of agents on Foreman's own friction log overnight (wild); #145 Wild: Start verification of task N in a side lane while N+1 begins; #146 Wild: Pre-plan queued tasks at idle in the background (near T-0401); #189 Dream at night over the day's work (wild); #349 Wild: Prepare the task while the user is still typing (near T-0258); #351 Wild: Keep a hot spare of the main thread's next step (near T-0216); #547 Wild: let idle drive time shorten the next task's critical path; #819 Rehearse the next task while idle (wild)

## C016 Racing attempts and tournaments [Orchestration, lanes and fleets]
Race competing approaches, models or planner/critic pairs on hard tasks and keep the gate winner or the best hunks.
- mark: skip — Doubles spend per hard task with a run-away cost risk; fm second plan and a single lane already give a cheaper independent read. Revisit only after cost caps in fm budget cover lanes.
- status: partial; value 3/5; effort L; risk high
- evidence: fm second plan (another model), fm bench plugin duels (T-0280), fm lane + run --models
- ideas: #45 Race competing attempts on a hard task; #58 Race competing approaches per task; #99 Race competing builder lanes on L tasks (near T-0429); #114 Spawn a planner/critic/executor tournament for L-sized plans (near T-0276); #116 Fork-and-race hard tasks across models and keep the gate winner (near T-0224); #416 Wild: Fork a UI feature into three prototypes and pick by screenshot; #752 Mine the loser–winner delta of a race

## C018 Live lane messaging and shared facts [Orchestration, lanes and fleets]
Steer running lanes, share a blackboard of retractable facts, route messages, answer side questions and pool human interrupts.
- mark: skip — Lanes are short S/M tasks with disjoint scopes; live steering and blackboards add machinery for little gain. A brief note appended before start covers most of it.
- status: missing; value 2/5; effort L; risk med
- evidence: lanes are fresh claude -p sessions with no inbound channel (fm run, fmlanes.py)
- ideas: #228 Steer running lanes with live messages (near T-0143); #601 Answer side questions from a read-only lane (near T-0277); #602 Route one message to the right lane (near T-0179); #625 Answer side questions without touching the task; #654 Run a live blackboard that lanes publish to and subscribe from; #703 Broadcast antibodies to running lanes (near T-0401); #706 Share a blackboard of retractable facts across live agents; #711 Add breakpoints to a live fleet; #712 Run lanes against mock neighbours until the real one arrives; #816 Pool human interrupts across lanes

## C019 Delegation governance [Orchestration, lanes and fleets]
Govern sub-agents with lineage trees, cascaded budgets, typed handoffs, information barriers, confidence scores, librarians and supervisors.
- mark: skip — Subagent use is shallow (scout/recon/reviewer/builder), so lineage trees, barriers and chiefs of staff are overbuilt; fm budget plus fm second already cover the useful parts.
- status: partial; value 2/5; effort L; risk low
- evidence: fm budget caps child spend (T-0227); fm second audit/debate (T-0276); fm audit prep; agents are read-only by design
- ideas: #115 Run a supervisor agent that watches live sessions and intervenes on drift (near T-0002); #123 Give agents persistent role memory (reviewer, builder, scout) distilled from past verdicts; #261 Test the adapters with a scripted fake model and cassettes; #312 Fake the agents to test the orchestrator (near T-0375); #313 Cascade budgets through a delegation tree (near T-0234); #314 Make handoffs typed receipts; #320 Enforce information barriers between roles; #510 Govern recursive delegation with a lineage tree; #511 Coalesce identical questions across the agent tree; #516 Make every sub-agent state a confidence and score it (near T-0370); #517 Run a librarian agent that builds per-lane context packs (near T-0234); #521 Run a standing "chief of staff" that answers sub-agents' blockers by escalation tier; #707 Audit what each child's summary dropped (near T-0276); #708 Grade the briefs the orchestrator writes for children (near T-0276); #710 Brief children with commander's intent and log their deviations (near T-0414)

## C023 Orchestration wild bets [Orchestration, lanes and fleets]
Auctions, forks at decision points, work stealing, fractal child Foremen, and peers consulted over a rate-limited line.
- mark: skip — Speculative with no grounded first step that beats existing fm bench and fm lane; budget auctions and fractal scopes risk runaway spend.
- status: missing; value 2/5; effort L; risk high; wild
- evidence: no auctions, forks or child Foremen; fm evolve is the nearest self-tuning loop (T-0224)
- ideas: #118 Let agents negotiate a shared contract before parallel lanes start (wild) (near T-0167); #321 Wild: Shadow every expensive agent with a cheap predictor; #322 Wild: Discover new specialist roles from failure clusters; #390 Wild: Auction the budget among lanes; #518 Wild: Fork a lane at a decision point; #520 Wild: Hold an orchestration policy tournament on replayed queues; #704 Let idle lanes steal work from slow ones; #713 Wild: Fractal Foremen — a task can own a child Foreman scope (near T-0224); #714 Wild: Drill handoff fidelity by swapping the model mid-task; #715 Wild: Consult peers by asking agents on a rate-limited line; #790 Wipe-compare lanes; #820 Fork lanes from transcript checkpoints (wild); #821 Auction budget to lanes by expected value (wild)

## C091 Context economy [Performance and cost]
Compact at step boundaries, rotate sessions, serve reads as deltas and share prompt-cache prefixes.
- mark: build — Add step-boundary compaction with a curated handoff (extend T-0098's task-boundary rule to M/L steps) and a session rotate when context slope turns bad; reuse checkpoint/resume.
- status: partial; value 4/5; effort M; risk low
- evidence: Compact at task boundary with freshAt (T-0098), checkpoint at 85%, per-turn state note only on change, shared brainstorm cache prefix, compaction at 70%
- ideas: #249 Compact at step boundaries with a curated handoff (near T-0098); #295 Wild: Run a "silent unless needed" mode with a measured output budget; #316 Share recon across agents by tree hash; #324 Interview the main thread before compaction (near T-0208); #342 Share one prompt-cache prefix across reviewer fan-out; #343 Serve repeat reads as ranges or deltas; #344 Compact at a step boundary, not when the window fills (near T-0228); #731 Schedule around the prompt-cache TTL; #739 Learn output digesters from what the model reuses (near T-0276); #740 Rotate the session when the context slope turns bad (near T-0212); #743 Compress briefs with a learned abbreviation dialect

## C093 Budgets and usage [Performance and cost]
Forecast cost, degrade gracefully near limits, enforce latency and cost budgets and use expiring quota.
- mark: build — First version: when pace is over, degrade (drop optional second reads/brainstorms, keep required gates) instead of blocking, and let fm night spend expiring weekly quota on queued low-priority tasks under hard caps. Spend guard must stay conservative.
- status: partial; value 4/5; effort M; risk high
- evidence: Pace-based subagent budget (T-0320), fm budget, fm cost, fm night budgeted work, usage meter (T-0346); no graceful degrade or expiring-quota harvesting
- ideas: #150 Enforce a latency and cost budget in the done-gate; #346 Record project performance as evidence, and block on regressions (near T-0280); #348 Degrade gracefully near the usage limit instead of blocking (near T-0320); #350 Wild: Schedule heavy work around the user's presence; #609 Wild: Borrow usage from tomorrow's pace; #663 Wild: Harvest expiring usage quota on low-priority backlog; #780 Wild: Schedule night work by grid carbon intensity

## C092 Gate scheduling and warm starts [Performance and cost]
Order and shard gates by failure odds, duration and return on time, cancelling reviewers on the first blocker.
- mark: build — Order gates in fm check by (recent failure rate / median runtime) from stored run times, keeping fail-fast; cancel remaining reviewer work on first blocker later.
- status: partial; value 3/5; effort S; risk low
- evidence: fm check --fail-fast, gate timing and slow-gate detection (T-0424), process-group timeouts; no ordering by failure odds, no warm pool
- ideas: #148 Keep a pool of warm headless sessions for `fm run` (near T-0014); #149 Shard gates by measured duration (near T-0257); #341 Order gates by failure odds per second; #539 Cancel reviewer fan-out on the first blocker (near T-0327); #542 Build a precomputed session image (near T-0001); #737 Prefetch reads one plan step ahead (near T-0414); #738 Rank gates by return on time (near T-0364)

## C089 Fast hooks [Performance and cost]
Keep hooks fast with a resident daemon, lazy imports, fork servers and latency SLOs.
- mark: build — First version: record per-hook import time and an SLO burn counter in the ledger, and have fm doctor/friction flag regressions with the offending commit range. Skip daemon (adds a long-lived process near the guard).
- status: partial; value 3/5; effort M; risk med
- evidence: Hooks p50 ~29 ms (round 6); fm doctor checks hook latency p95 vs fixtures (fmdoctor.py:109); no daemon or auto-bisect
- ideas: #137 Run hooks through a resident daemon (near T-0318); #144 Bisect hook-latency regressions automatically; #352 Wild: Hold a latency "race day" between plugin versions; #476 Track hook SLOs and auto-degrade on burn (near T-0012); #535 Budget every hook's import time and lazy-load the rest (near T-0367); #546 Wild: compile Foreman's hot path to a stripped self-checking "fast kernel"; #741 Run test workers from a pre-imported fork server

## C090 Route work to the cheapest model [Performance and cost]
Route each step to the cheapest model and effort that passes and draft cheap then verify strong.
- mark: build — Let fm run/lane pick model and effort from task type and tier using fm bench history, defaulting to current behaviour; start by logging model and pass/fail per task to feed it.
- status: partial; value 3/5; effort M; risk med
- evidence: Subagents are already tiered (fm-scout Haiku, fm-reviewer, fm-builder); fm budget; no per-step routing in fm run
- ideas: #122 Add an agent budget broker that schedules by pace, not caps (near T-0228); #141 Route each step to the cheapest model that passes (near T-0224); #385 Draft cheap, then verify strong (near T-0222); #543 Set reasoning effort per step type (near T-0415)

## C088 Run only affected gates and cache results [Performance and cost]
Pick gates by what the diff touches, cache by tree hash and test input, and reuse results.
- mark: skip — Already built. Remaining per-test-file input-hash cache is marginal over tree-hash reuse.
- status: exists; value 2/5; effort S; risk low
- evidence: fm check reuses pass on identical tree, --affected runs linked tests (CHANGELOG round 5, T-0136); passes keyed to environment, 12h expiry
- ideas: #138 Run only the gates a diff can affect (near T-0280); #139 Reuse gate results by tree hash; #538 Cache gate results per test file by input hash (near T-0224); #540 Index the project map incrementally from git object hashes; #541 Cache guard verdicts by parsed command shape (near T-0189)

## C049 Intake quality [Planning, briefs and queue]
Catch contradictions, XY problems, duplicates and re-asks at intake, split big briefs and gate briefs by readiness.
- mark: build — First version: at capture, compare the new text to dropped/done briefs and open inbox (fmrecall) and note a likely re-ask or contradiction with the veto list; add a Definition-of-Ready lint (AC has verify cmd, scope named) on fm task new.
- status: partial; value 4/5; effort S; risk low
- evidence: fm capture notes existing-command overlap (T-0262), recall at focus (T-0043), fm intake parser; no contradiction, dup-vs-dropped or XY check
- ideas: #264 Detect re-asks of things already dropped (near T-0016); #299 Capture contradictions at intake (near T-0383); #411 Split oversized briefs into a dependency chain at intake; #420 Learn the user's request dialect (near T-0375); #426 Cross-check each request against the whole inbox (near T-0079); #552 Learn the user's vocabulary into a project glossary (near T-0041); #617 Detect the XY problem at intake; #638 Gate briefs with a Definition-of-Ready lint

## C048 Queue grooming and lifecycle [Planning, briefs and queue]
Groom the queue, expire deferrals, stack and park tasks and unify inbox, queue and tasks into one lifecycle.
- mark: build — First version: deferrals carry a revisit date/condition and fm next/tidy resurface expired ones; add fm task revert ID that lists dependents (fm relate) before undoing. Skip objectives layer and lifecycle table.
- status: partial; value 4/5; effort M; risk low
- evidence: fm task defer/block/drop (fmcli.py:428), fm relate (T-0383), fm tidy flags stale inbox; no expiry, stack or revert-with-dependents
- ideas: #19 Groom the queue and expire deferrals; #263 Add an objectives layer above tasks; #266 Park and resume tasks with a task stack; #406 Revert a task along with its dependents; #419 Converge the brainstorm into epics; #460 Distil the idea pile into a ranked epic roadmap; #468 Idea futures: bet on which ideas the user will keep (near T-0205); #503 Add discipline packs for non-code deliverables; #599 Run metric-climbing campaigns; #678 Unify inbox, queue, batch and task into one item lifecycle (near T-0383); #679 Define the task lifecycle as one transition table with property tests; #692 Optimise a metric with a lane-per-experiment loop (`fm tune`); #742 Report flow metrics and recommend a WIP limit

## C051 Estimates, pace and time budgets [Planning, briefs and queue]
Predict cost and duration of tasks, plan the day against pace and work backwards from dates.
- mark: build — First version: fm next / plan shows predicted cost and minutes from finished tasks of the same type and tier (fm cost data), and fm run orders the queue to fit the remaining budget. Skip demo-date backwards planning.
- status: partial; value 4/5; effort M; risk low
- evidence: Usage pace in fm projects (T-0346), fm budget (T-0227), size words typical time (T-0116), fm cost, fm night --dry-run estimates
- ideas: #9 Make estimates and pace predictive; #51 Forecast cost and fit work to the budget (near T-0276); #103 Plan the day against usage pace and learned task cost; #211 Attribute wall-clock time and show the critical path; #347 Fit a task to a time budget (near T-0367); #417 Wild: Work backwards from a demo date

## C055 Triggers and standing orders [Planning, briefs and queue]
Run standing orders on schedules or external conditions and wake sessions on events.
- mark: build — First version: a standing-orders file (cron-like or file/CI/git-change condition -> captured brief or fm command) evaluated by fm night and drive; spend capped by fm budget. Skip event-push infrastructure.
- status: partial; value 4/5; effort M; risk med
- evidence: fm night jobs, fm run, fm serve, drive Stop hook, background_tasks wake (T-0115), fm notify; no user-defined schedules or conditions
- ideas: #220 Wake sessions on events, not polling (near T-0391); #405 Run standing orders on a schedule or condition; #421 Arm tasks on external conditions; #446 Run triggers and flows (`fm flow`); #696 Run long-lived investigations that probe on a schedule

## C050 Scope and intent drift [Planning, briefs and queue]
Detect drift between brief, diff and vetoes, derive tier from the diff and keep sessions on intent.
- mark: build — Derive tier from the diff at done (files, lines, core paths) and flag a mismatch with the declared tier; reuse the existing scope check. Skip the effort ledger.
- status: partial; value 3/5; effort M; risk low
- evidence: Scope refusal with scope: reason (T-0055/T-0168), security audit judges task's own diff (T-0078/79), fm vetoes pre-action check
- ideas: #102 Detect scope drift against the brief (near T-0366); #192 Radar for intent drift against briefs and vetoes; #289 Derive task tier from the diff, not the declaration (near T-0216); #622 Keep an effort ledger by origin (near T-0376)

## C052 Decisions, assumptions and promises [Planning, briefs and queue]
Keep tripwires, revisit triggers, assumption registers and promise ledgers that reopen work when they stop holding.
- mark: build — First version: fm task assume gets a re-check command; sentinel/night reruns them and reopens or inboxes the task when one fails. Skip regret review, spaced repetition, release/rollback briefs, sunset contracts.
- status: partial; value 3/5; effort M; risk low
- evidence: fm decide, fm task assume, stale-fact tripwire (T-0113), decision revisit nudges (T-0262)
- ideas: #231 Wild: Let a brief be "released" like software, with a rollback; #422 Keep a promise ledger from the agent's own words (near T-0116); #425 Keep an assumption register that reopens work (near T-0134); #431 Wild: Hold a weekly regret review; #486 Require a sunset contract on every FEATURE brief (near T-0328); #701 Wild: Resurface forgotten decisions by spaced repetition

## C053 Plan-time rigour [Planning, briefs and queue]
Require build-vs-reuse records, pre-mortems, spike tasks, demo transcripts and previews before building.
- mark: build — First version: for FEATURE L plans require a short build-vs-reuse line (existing fm command or module found by recall) and one pre-mortem line from fm second plan; add SPIKE as a discarded-lane task. Skip council, rubber-duck, demo transcripts.
- status: partial; value 3/5; effort M; risk low
- evidence: fm second plan (T-0276), fm oracle (T-0226), fm recall at focus, bench judged; no pre-mortem, spike type or reuse record (TYPES in fmcore.py:22)
- ideas: #323 Wild: Run a pre-mortem with a council of past users; #415 Wild: Hold a rubber-duck mode; #418 Wild: Hand the user a "pre-mortem" before any L task starts (near T-0047); #437 Add a rubber-duck shaping mode for vague ideas; #456 Run spike lanes for what-if questions (wild); #461 Add a SPIKE task type with a discard guarantee; #462 Gate FEATURE L plans on a build-vs-reuse record (near T-0280); #487 Show a surface-cost estimate in every plan (near T-0353); #578 Give builders the program slice, not the files (near T-0234); #606 Show a demo transcript before building a FEATURE (near T-0280); #628 Preview a brief before it exists (near T-0384); #651 Compile plans into programs with per-step pre/postconditions; #754 Wild: Reverse-derive the brief from the diff (near T-0271)

## C054 Living handbook and docs [Planning, briefs and queue]
Keep a self-writing handbook, MASTER.md and docs that track reality and pass a cold-start test.
- mark: build — First version: fm docs also checks MASTER.md module/command table against lib/*.py and fm help and offers the diff. Cold-start test already exists as bench stranger; skip editor why-lines (fm why exists).
- status: partial; value 3/5; effort M; risk low
- evidence: fm docs reports drifted markdown (T-0323), docs impact stage, fm export agents, fm bench stranger cold-start (T-0298), fm map
- ideas: #28 Keep a self-writing project handbook that tracks reality (near T-0291); #229 Test the handbook with a cold-start agent (near T-0379); #297 Generate MASTER.md sections from code (near T-0276); #626 Show why a line exists, in the editor (near T-0262)

## C085 Canary releases with consumer replay [Releases and delivery]
Replay consumer projects against a release candidate and close a release only after consumers ran it.
- mark: build — Before a release, run fm replay, fm bench and fm sentinel across every project from fm projects and print per-project deltas; skip channels and synthetic fixtures.
- status: partial; value 3/5; effort M; risk low
- evidence: fm replay (guard on real commands), fm bench version replays (T-0280), fm sentinel re-runs finished checks; single-user, one install
- ideas: #2 Close the downstream loop with a canary release; #16 Canary-gate releases with consumer replay (near T-0280); #80 Wild: canary ring across the user's own projects (near T-0041); #427 Explain the release delta per consumer; #613 Run projects on release channels (near T-0326); #619 Close a release only when consumers have run it; #620 Distil consumer repo shapes into synthetic fixtures; #812 Canary releases on downstream projects (near T-0326)

## C086 One-command releases and self-test [Releases and delivery]
Cut releases from a clean throwaway worktree with clean-install and upgrade tests.
- mark: build — scripts/release: clean git worktree, run tests, install-user into a temp HOME, then uninstall and diff the tree for a round trip, bump versions and changelog; skip blue/green.
- status: partial; value 3/5; effort M; risk low
- evidence: install.sh/uninstall manifest (fmsetup.py), fm doctor, tests/run.py; no release or clean-install script
- ideas: #15 Ship releases with one command (near T-0414); #83 Gate releases on clean-install and upgrade tests; #281 Ship a self-test that runs on the user's machine after every install or upgrade (near T-0350); #491 Prove install and uninstall are a byte-identical round trip; #618 Cut releases from a clean throwaway worktree; #669 Install blue/green with automatic rollback; #685 Add `fm try`: a session that leaves no trace (near T-0338)

## C087 Release flow, gates and rituals [Releases and delivery]
Release by flow, publish contracts first and mark releases with a ritual or film.
- mark: skip — Single-developer plugin; rituals, films and flow releases are low value. The public-surface snapshot idea is folded into the one-command release item.
- status: partial; value 2/5; effort S; risk low
- evidence: fm doctor, docs drift, Release playbook (T-0101); no public-surface snapshot
- ideas: #86 Ratchet complexity in the release gate (near T-0280); #247 Snapshot the public surface and gate breaking changes (near T-0262); #253 Add an incident mode for hotfixes; #507 Wild: Film a release; #683 Ship a feature as a thin slice and unlock the rest only on use; #811 Publish contracts before building (near T-0428); #813 Release by flow, not by request

## C102 Wild codebase and rebuild bets [Research frontier and wild bets]
Regenerate Foreman or a module from a tiny spec and diff behaviour.
- mark: skip — Rebuild-from-spec diff is costly and its signal is weak versus fm bench; court and appeals ideas duplicate fm second debate. Safe rename belongs to LSP, not Foreman.
- status: partial; value 2/5; effort L; risk med; wild
- evidence: fm bench replays finished tasks (T-0212); fm impact and fm why exist; LSP tool available to agents; no spec rebuild
- ideas: #37 Wild: Hold a post-mortem court where past mistakes argue the plan; #218 Wild: Open a regression shop where users bet against the gates (near T-0280); #256 Wild: Rebuild Foreman from its spec and diff the behaviour; #259 Wild: Run an LSP-backed impact analysis and safe rename; #270 Rebuild Foreman from its own prompt and diff the result (near T-0212); #296 Wild: Make Foreman a ~200-line spec a fresh model can rebuild (near T-0207); #389 Wild: Regenerate a module clean-room and diff it; #635 Wild: Hold an appeals court for refusals; #649 Conform diffs to the repo's own style fingerprint (near T-0134); #699 Wild: Run an architecture flex test; #779 Wild: Learn a repo digital twin that predicts blast radius

## C103 Wild research and incubation bets [Research frontier and wild bets]
Incubate a whole project overnight, resurrect dormant ones and walk-and-talk.
- mark: skip — Overnight incubation from one line is what fm mission plus fm run already do; ghost edits and tree search add runaway spend risk for little gain. Resurrecting dormant projects is a small fm projects digest, covered by fm status.
- status: partial; value 2/5; effort L; risk high; wild
- evidence: fm mission and fm night/run exist for overnight work (T-0375); no resurrect, ghost edits or game-tree search
- ideas: #430 Wild: Resurrect a dormant project; #557 Wild: Write a changelog from the future as a steering device (near T-0308); #608 Wild: Incubate a whole project from one line overnight (near T-0296); #610 Wild: Suggest ghost edits while the user types by hand; #661 Wild: Search over steps like a game tree, using partial gate scores as the value; #687 Make a markdown project page the database (wild)

## C099 Heartbeat for unattended work [Resilience, state and simplicity]
Circuit breakers, retry classes, an external dead-man heartbeat and anomaly switches for headless runs.
- mark: build — First version: fm run/night write a heartbeat file each loop and a preflight (guard fixture replay + fm doctor) before starting; a stale heartbeat triggers the fm notify command. Add a consecutive-failure breaker that stops the run.
- status: partial; value 5/5; effort M; risk low
- evidence: fm run backoff on usage limit (MASTER.md:250); drive supervises long jobs (T-0415); fm serve systemd unit with Restart; check_serve; fm night budgets; no dead-man ping or preflight canary
- ideas: #376 Wild: Run a pre-flight and canary task before every night run; #424 Supervise long-lived processes (near T-0415); #474 Put circuit breakers and retry classes on headless runs; #532 Wild: Run a canary that bites the agent's own guard before every night run

## C096 Chaos and drills [Resilience, state and simplicity]
Chaos-test resume, lifecycle and state with fire drills, hostile environments and fault injection.
- mark: build — First version: a stdlib test that fuzzes random task-lifecycle sequences with a kill at random fs write points in a temp state dir and asserts fm doctor/briefs stay consistent and resume restores; later a compaction-resume check in fm bench.
- status: partial; value 4/5; effort M; risk low
- evidence: check_integrity (T-0268), fm sentinel (fmcli.py:1685), fm bench stranger (T-0298), fm resume skill; no kill-and-resume or lifecycle fuzz
- ideas: #50 Test that resume survives compaction (near T-0148); #72 Chaos-test resume; #282 Wild: Run a chaos monkey inside the real session (near T-0039); #473 Fault-inject the environment in CI; #481 Wild: Hold a monthly fire drill that destroys state on purpose; #482 Wild: Fuzz random lifecycle sequences with crash points; #668 Run a hostile-environment matrix in CI

## C097 Subtract and slim the surface [Resilience, state and simplicity]
Run deletion passes, prune unused surface from usage data, deprecate with a pipeline and keep a graveyard.
- mark: build — First version: `fm usage --prune` joining usage data with help to list commands unused in 60 days and proposing CLEAN briefs (never deletes). Skip graveyard and deprecation pipeline.
- status: partial; value 3/5; effort S; risk low
- evidence: fm usage lists commands and skills used and never used (fmcli.py:2345); fm help tiers commands; fm tidy; fm repeats
- ideas: #85 Prune unused surface from usage data; #88 Collapse the command tree to about 25 verbs; #92 Run a nightly subtraction job; #181 Track replacement debt to closure (near T-0298); #293 Add `fm less` to remove the thing that bothers you most (near T-0125); #457 Map comprehension debt (wild); #470 Keep a graveyard of removed capabilities with resurrection tests (near T-0125); #488 Run a deprecation pipeline for commands and settings (near T-0414); #493 Wild: Reveal commands by use, so `fm help` shows only what you'd touch (near T-0262); #494 Wild: Ablate whole subsystems against the user's own live work (near T-0224); #495 Wild: Give Foreman a "monastery mode" that runs only guard, resume and done-gate; #642 Price technical debt by how often agents tripped on it; #684 Generate the skills from the CLI definitions (near T-0296); #686 Fold the separate toggles into one settings file (near T-0216); #688 Hold weekly delete-golf (wild)

## C100 X-ray and honest self-metrics [Resilience, state and simplicity]
Show what is wired and active right now and which settings nobody changes.
- mark: build — First version: `fm wiring` printing registered hooks, enabled plugins, autonomy/drive/sensitive/sync flags, standing yeses, running code version and non-default settings in one screen, from existing doctor helpers.
- status: partial; value 3/5; effort S; risk low
- evidence: fm doctor, fm usage, fm ui --json, fm watch show pieces; no single view of active wiring
- ideas: #298 Report settings that nobody changes (near T-0428); #492 Add `fm wiring`, an X-ray of what is active right now; #676 Spend an error budget on Foreman's own misbehaviour

## C094 Crash-safe state [Resilience, state and simplicity]
Version, migrate and write state transactionally with locks, repair commands and a git-ref backup.
- mark: build — First version: `fm doctor --repair` for briefs vs STATE vs ledger mismatches and torn-file recovery, with a torn-write unit test; skip the single append-only log rewrite and git-ref store.
- status: partial; value 3/5; effort M; risk low
- evidence: atomic writes + project lock (fmcore.py:1,35), STATE_SCHEMA in meta.json (fmcore.py:408), doctor integrity (T-0268), backups/*.tgz, fm sync
- ideas: #77 Make state crash-safe, with a repair command (near T-0268); #95 Fold briefs, STATE, ledger and decisions into one append-only log (near T-0004); #274 Version and migrate all on-disk state (near T-0004); #275 Make state writes transactional across files (near T-0291); #276 Lock and fence concurrent writers; #278 Run a continuous invariant checker over live state (near T-0245); #670 Declare each command's network needs and degrade offline (near T-0045); #674 Simulate torn writes and reordered renames

## C098 Lifecycle as one machine [Resilience, state and simplicity]
Define the task lifecycle as a transition table with property tests and compound operations as resumable sagas.
- mark: build — First version: one transition table in fmcore plus a property test that random fm task commands only make legal transitions; later a drive idleness model check. Skip the unified scheduler.
- status: partial; value 3/5; effort M; risk low
- evidence: status sets OPEN/RUNNABLE in fmcore.py:25; drive/run/serve/night each have own loops; no transition table or property tests
- ideas: #74 Model-check the drive for idleness (near T-0207); #471 Run compound operations as resumable sagas; #484 Run drive, run, serve, night and session on one scheduler (near T-0014); #490 Gate module layering with an import graph

## C101 Test the test suite [Resilience, state and simplicity]
Randomise, isolate, mutation-test and scale-test Foreman's own tests and prove guard and done-gate source quality.
- mark: build — First version: a stdlib mutation script that flips operators/constants in fmguard.py's deny paths and reports which survive the guard tests; plus random test order in fm check. Skip the five-year synthetic history.
- status: partial; value 3/5; effort M; risk low
- evidence: plugin/tests exists; T-0338 added guard regressions; fm check records flakes.json (T-0274); no mutation or randomised ordering
- ideas: #666 Mutation-test Foreman's own guard and done-gate source (near T-0338); #671 Scale-test against a synthetic five-year history; #672 Randomize and isolate Foreman's own test suite (near T-0134)

## C095 Fail-safe hooks [Resilience, state and simplicity]
Hooks that fail closed with a degraded mode, watchdog and last-known-good fallback, with the UI quarantined.
- mark: skip — Fails closed and has a breaker already (T-0371, T-0087); remaining ideas (last-known-good copies) add risk of stale guard.
- status: exists; value 2/5; effort S; risk med
- evidence: hooks.json onFailure block on guard (T-0371, hooks.json:43); hook circuit breaker (T-0087); doctor check_hook_errors/latency/exit_codes
- ideas: #78 Fail-safe hooks with a watchdog (near T-0371); #273 Fail closed on hook crashes with a degraded-mode contract (near T-0087); #280 Quarantine the mod and UI from the core on failure; #677 Keep a last-known-good fallback for each hook (near T-0115)

## C040 Friction capture and self-improvement loop [Self-improvement and learning]
Collect friction from the user, downstream projects and Foreman's own runs and turn it into improvement tasks with proof it helped.
- mark: build — Let fm friction read other registered projects' ledgers (guard blocks, user corrections, taste) read-only and file self-inbox items; postmortem line on each correction. Skip mood detection and weather report.
- status: partial; value 5/5; effort M; risk low
- evidence: fm friction digest of Foreman's own runs (T-0125, T-0187); fm night; fm bench stranger (T-0298); no downstream-project friction intake
- ideas: #17 Capture consumer-project friction as Foreman tasks automatically (near T-0276); #154 Mine the user's relayed complaints before they relay them (friction from downstream projects) (near T-0280); #177 Write a postmortem for every correction (near T-0373); #222 Treat user frustration as a trigger for process root-cause; #301 Analyse escapes and propose the missing gate; #504 Watch model quality with a weather report; #583 Wild: Run Foreman as a scientist on itself

## C038 Lesson lifecycle [Self-improvement and learning]
Store lessons with confidence, evidence and expiry, quiz them, resolve contradictions and prune or retire the stale ones.
- mark: build — Add a lesson ledger sidecar: count when a tripwire-surfaced lesson preceded a clean pass vs a repeat block; fm tidy flags lessons whose pinned file changed or that never helped. Skip quizzes and truth-maintenance graph.
- status: partial; value 4/5; effort M; risk low
- evidence: Lessons per brief + file tripwires fmrecall.py:327; shared lessons :352; fm tidy archives (T-0004); no confidence/expiry/outcome score
- ideas: #6 Learn lessons with confidence and prune them; #69 Do less: derive lessons from the ledger instead of a store (near T-0276); #109 Score lessons by whether recall preceded a clean pass; #151 Close the loop on lessons: measure whether a lesson actually changes outcomes; #152 Auto-retire and merge stale lessons, rules and briefs (near T-0004); #359 Pin lessons to code and expire them when it changes (near T-0226); #556 Wild: Let rival lessons compete and keep the survivor; #576 Keep a truth-maintenance graph of lessons and decisions; #745 Embargo born-from lessons during replay; #751 Quiz each lesson with a cold agent (near T-0263); #755 Wild: Stage lessons in probation, then promote in sleep

## C039 Evals from failures and steers [Self-improvement and learning]
Capture an eval automatically from every block, steer or guard false positive and gate releases on them.
- mark: build — Auto-run fm evals when a task is blocked and log guard false positives (user steer after a block) into an eval inbox; gate releases on fm bench gate plus these cases. Skip predictive failure and randomized trials.
- status: partial; value 4/5; effort M; risk low
- evidence: fm evals turns a blocked/failed task into a plugin eval case (fm help Reports); fm replay on guard commands; no auto-capture of steers/false positives
- ideas: #63 Capture evals from real failures automatically; #119 Grow a self-writing eval from every user steer (wild) (near T-0224); #155 Predict a task's failure before running it, from past similar tasks (near T-0174); #156 Write evals from every blocked task by default, and gate releases on them (T-0035 made real) (near T-0170); #157 Self-improvement pass that proves it helped: A/B each friction fix in a lane (near T-0350); #388 Detect stuck trajectories mid-run from ledger signatures; #549 Pre-register self-experiments before changing Foreman (near T-0278); #553 Schedule self-improvement passes by marginal yield (near T-0125); #644 Predict gate outcomes before running them (near T-0174); #653 Estimate an instruction change's effect from old logs before running it; #748 Tune Foreman's own dials as a bandit (near T-0125); #749 Track whether friction fixes stay fixed (near T-0370); #750 Plan from solved look-alikes; #773 Run sequential randomized trials of instruction variants

## C043 Benchmarks of Foreman itself [Self-improvement and learning]
Hold secret bench sets, grow them when saturated, track a release scorecard, measure time horizon and report outside scores.
- mark: build — Add a holdout split to fm bench so evolve gates on train cases and a release check runs the held-out ones; keep a scorecard line per release. Skip outside benchmarks and publishing.
- status: partial; value 4/5; effort M; risk low
- evidence: fm bench build/run/gate/duel/stranger/judged (T-0212, T-0221, T-0280); no holdout, scorecard or saturation growth
- ideas: #25 Dogfood arena: seeded-bug projects scored by the discipline; #353 Hold out a secret bench set evolve never sees (near T-0413); #354 Track a release scorecard and make it evolve's objective (near T-0280); #579 Report an outside score on public agent benchmarks (near T-0280); #735 Memoize bench and evolve by case reach (near T-0223); #744 Grow the bench harder when it saturates; #776 Measure Foreman's time horizon (near T-0367); #781 Wild: Publish an open discipline benchmark from redacted ledgers

## C045 Rule lifecycle [Self-improvement and learning]
Give rules a half-life, promote repeatedly broken prose rules to enforcement and detect contradictions.
- mark: build — From fm friction counts, flag a prose rule that was nudged or corrected 3+ times as a candidate for a guard check; add reaffirm date to rules in fm tidy. Decision tripwires already exist, skip those.
- status: partial; value 3/5; effort S; risk low
- evidence: fm decide --revisit after DATE or when PATH changes (T-0262); fm tidy reports contradictions (fmtidy.py:5); no rule half-life or promotion to enforcement
- ideas: #209 Give decisions tripwires that reopen them; #225 Detect contradictions among vetoes, lessons, decisions and rules; #257 Wild: Give decisions revisit triggers (near T-0262); #271 Give rules a half-life and require reaffirmation; #548 Promote repeatedly broken rules from prose to enforcement

## C046 Self-experiment discipline [Self-improvement and learning]
Pre-register experiments, raise Goodhart alarms, test sequentially and keep dead-end registries.
- mark: build — Dead-end registry: store rejected evolve and friction candidates with reason, and have fm evolve and fm friction skip or cite them. Skip Goodhart alarm and sequential trials.
- status: partial; value 3/5; effort S; risk low
- evidence: fm surprise logs expected-to-observed (help Finding your way); fm friction rechecks fixes (T-0187); evolve gated by bench; no dead-end registry or pre-registration
- ideas: #294 Wild: Add a "was it Foreman?" differential rerun; #458 Keep a dead-end atlas (wild); #551 Keep a dead-end registry checked at plan time (near T-0115); #581 Drive idle exploration from the surprise log; #659 Raise a Goodhart alarm on Foreman's own metrics; #760 Log surprises from stated predictions (near T-0261); #772 Turn landscape findings into bench-gated experiments (near T-0298)

## C041 Mining lessons from attempts [Self-improvement and learning]
Learn from paired attempts, reverted work, races and hard tasks, and write teaching notes for cheaper models.
- mark: build — Extend fm repeats to propose a playbook draft from repeated successful step sequences, and scan git reverts linked to T-ids for a lesson line. Skip contrastive pairs and teaching notes until bench pairs exist.
- status: partial; value 3/5; effort M; risk low
- evidence: fm repeats suggests tools (fmrepeats.py); fm bench keeps attempts (T-0221); reverted/paired mining absent
- ideas: #304 Compile repeated procedures into tested playbook skills; #318 Turn repeats into tested project tools (near T-0280); #519 Wild: Leave teaching notes from hard tasks for cheaper models; #559 Mine abandoned and reverted work for lessons; #643 Learn a playbook from one demonstration (near T-0263); #770 Mine contrastive lessons from paired attempts; #774 Distil the minimal sufficient trajectory into a playbook

## C042 Instruction tuning across models [Self-improvement and learning]
Tune, shrink and ablate instructions per model, delete crutches on new models and test instruction variants in shadow.
- mark: build — Run fm evolve --drop over rules/skills on each new model id via bench models, report files that earn no tokens. Skip fuzzing, shadow runs and bake-off as duplicates of evolve+bench.
- status: partial; value 3/5; effort M; risk med
- evidence: fm evolve with --drop ablation (T-0224, fmevolve.py:116); fm bench models (T-0223); no per-model instruction variants
- ideas: #94 Compile all rules into a one-page contract and load the rest on demand (near T-0277); #357 Delete instruction crutches when a new model arrives (near T-0224); #358 Tune instructions per harness and model (near T-0318); #360 Run candidate instructions in shadow on live tasks (near T-0224); #383 Attribute outcomes to injected context by ablation; #384 Fuzz Foreman's instructions and classifier with paraphrases; #554 Run a model-upgrade exam from the failure museum; #756 Wild: Hold a yearly "fresh model, old tasks" bake-off

## C044 Context injection quality [Self-improvement and learning]
Keep injected context small, cache-stable and delivered at the action, and measure what was used.
- mark: build — Log injected note kinds and sizes per turn in the ledger and show a per-session total in fm friction, with a cap that drops the lowest-yield notes. Skip live rule-retention probes.
- status: partial; value 3/5; effort M; risk low
- evidence: Injection in fmhooks.py (prompt notes, tripwires, recall); budgets of skill descriptions in fm doctor (T-round 7); no per-session cap or used-vs-injected measure
- ideas: #90 Cap the instruction tokens injected per session; #142 Keep the injected context cache-stable and measured (near T-0277); #480 Wild: Probe rule retention inside live sessions; #565 Diff what was injected into context against what was used (near T-0278); #747 Teach running sessions new lessons mid-flight (near T-0174); #762 Score each rule's compliance from transcripts (near T-0364); #769 Inject lessons at the action, not the session (near T-0013)

## C047 Self-evolution wild bets [Self-improvement and learning]
Breed Foreman variants, apprentice instances, distil the discipline into a local model and run adversarial curricula.
- mark: skip — Breeding, apprentice shadowing and local-model distillation need volume and compute beyond value; evolve plus bench already covers the grounded step. Letter to next week's Foreman is covered by digest and resume.
- status: missing; value 2/5; effort L; risk high; wild
- evidence: fm evolve is single-lineage (T-0224); no population, apprentice or distillation
- ideas: #161 Wild: Skill genome — breed instruction variants and keep the winners (near T-0224); #162 Wild: Apprentice mode — a second Foreman instance that shadows the user's manual fixes and learns from the diff; #190 Train Foreman against synthetic failures (wild); #217 Wild: Distil the discipline into a cheap local model's training set; #362 Wild: Hold an adversarial curriculum between a teacher and Foreman; #363 Wild: Let Foreman write its own letter to next week's Foreman; #364 Wild: Breed rival Foremen and let the user pick the survivor; #555 Wild: Hold a mirror session where Foreman interviews its own transcripts (near T-0176); #558 Wild: Keep a learning journal of questions the model couldn't answer without asking (near T-0277); #778 Wild: Keep a quality-diversity archive of Foreman variants

## C070 Band and statusline signals [UI and motion]
A quiet band and statusline with the next action, mood glyph, sparklines, pace mood and pulse strip.
- mark: build — Add a quiet pace/health glyph to the band and statusline from existing data (usage pace vs share of week, failing gates, blocked count) shown only when amber/red; reuse fm ui --json fields.
- status: partial; value 3/5; effort S; risk low
- evidence: Hook-latency sparkline (mods/foreman-ui/hooks/kit.ts:195), usual-time-for-type, context meter, usage-pace meter (T-0346), statusline Foreman line
- ideas: #32 Give the band a sense of progress with a live "pace" mood; #42 Draw a small cost-and-pace gauge that stays quiet until it matters; #93 Show only the next action in the statusline (near T-0245); #198 Add a budget and pace gauge that stays quiet until 75%; #237 Let the statusline carry a tiny "mood" glyph of the run's health; #240 Wild: Let the band breathe with the pulse of the work; #402 Wild: Float a pill that expands only when you're needed; #436 Show a ghost pace marker on every progress bar; #569 Wild: Give each task a "confidence weather" forecast on the band; #593 Draw sparklines in the terminal band (near T-0328); #595 Publish a live status badge as animated SVG (wild); #791 Turn token burn into ambient light; #792 Keep a pulse strip of session heartbeat (near T-0338)

## C071 Proof and close-out cards [UI and motion]
A proof card, close-out story and small-win motion when a task finishes.
- mark: build — Render the existing done-time grade and lens verdicts as a one-card close-out in fm ui --json and the pane toast; no new data, closes the loop for unattended runs.
- status: partial; value 3/5; effort S; risk low
- evidence: fm pr prints proof (red-green, lens verdicts); band tallies 'since your last message' (T-0117); verification grade at done (round B)
- ideas: #40 Celebrate small wins in the pane with a clear checkmark motion; #200 Show a proof card when a task finishes (near T-0406); #235 Add a "close-out card" at task done that reads like a good commit story; #242 Wild: Name the session's "unsung fix" at the end of a long run (near T-0401); #243 Wild: Let the user pin a "lucky charm" rule that Foreman greets when it saves them

## C075 Diff and review reading [UI and motion]
Evidence-anchored diff reader, review-lens heatmap, risk-ranked packets and explaining a line in the editor.
- mark: build — First version: make guard blocks show the offending command segment with the rule that matched (fmguard.py), and rank fm audit prep packets by risk. Skip editor/LSP and heatmaps.
- status: partial; value 3/5; effort M; risk low
- evidence: fm tour (reading order), fm second, fm audit prep, fm why; guard block messages exist
- ideas: #175 Colour the codebase by trust; #197 Make guard blocks legible with a visual diff of the offending command; #206 Add a live review-lens heatmap on diffs (near T-0276); #267 Rank review packets by risk and the reader's time (near T-0158); #594 Make the diff reader evidence-anchored (near T-0276); #658 Show open criteria as editor diagnostics over LSP; #782 Follow the agent's cursor (near T-0263)

## C072 Navigation and palette [UI and motion]
A keyboard command palette, deep links, saved layouts, id completion and state-aware help.
- mark: skip — Palette exists. State-aware 'you probably want' is already what fm next does each turn. Not worth a separate build.
- status: partial; value 2/5; effort S; risk low
- evidence: Desktop Ctrl+K palette (T-0328); fm help tiers; no state-aware help row, no id+title completion
- ideas: #201 Add a keyboard-first command palette with live previews (near T-0143); #239 Give `fm help` a "you probably want this" row based on the current state; #395 Dispatch by dragging queue cards onto sessions; #399 Swipe through pending asks and decisions as a deck; #634 Complete task ids with their titles (near T-0280); #786 Deep-link every view with `foreman://` (near T-0364); #788 Save and restore workspace layouts

## C077 Needs-you moments and delight [UI and motion]
Single choreographed ask moments, stale-work patina, naming lanes and whimsical rewards.
- mark: skip — Needs-you toast and empty-queue reasons already exist; voice, parties and patina are whimsy.
- status: partial; value 2/5; effort S; risk low
- evidence: fm ask via prompts, toasts with chime for needed yeses (T-0095), mascot cheer; Stop drive says why idle (T-0415)
- ideas: #33 Hold a "ship party" release ritual; #36 Wild: Give Foreman a voice that reports at the end of a long run; #236 Name each lane after what it is doing, not its id (near T-0414); #244 Make the first run feel guided: an interactive `fm hello` that does a real tiny task; #245 Say "nothing to do" with a reason and a suggestion, never silence (near T-0415); #597 Show a stale-work patina that ages briefs and deferrals (wild); #598 Choreograph a single "needs you" moment

## C069 Living task and project views [UI and motion]
Animated pipelines, constellations, flow boards, a codebase city or pixel workshop that show where work is.
- mark: skip — UI already animated and the desktop has project dashboards; cities/constellations/gravity are decoration. If any, a dependency-aware flow board from fm relate (T-0383) is the only useful bit but value is low.
- status: partial; value 2/5; effort M; risk low
- evidence: Band/pane animate step bars, queue rows, subagent minis (CHANGELOG T-0095, T-0109, T-0328); no dependency/flow board
- ideas: #35 Draw the project as a living map that lights up where work is happening; #193 Animate the task as a living pipeline; #194 Add a session constellation view (near T-0351); #195 Show the queue as a dependency-aware flow board (near T-0146); #203 Wild: Render the codebase as a city and let tasks walk through it; #403 Wild: Make the queue a physical gravity field; #596 Run lanes as characters in a tiny pixel workshop (wild); #785 Morph the queue between groupings (near T-0383)

## C074 Desktop app and ambient surfaces [UI and motion]
Tray orb, file plaques, wall display, offline shell and live theme preview.
- mark: skip — Tray orb and wall display are in the separate desktop repo and are cosmetic; sounds and watch already cover ambient status.
- status: partial; value 2/5; effort M; risk low
- evidence: Desktop app exists in separate repo (README:77); chimes in mod (T-0095); fm watch dashboard
- ideas: #202 Make the tray icon a reactive status orb; #204 Wild: Add an ambient soundscape and haptics for long unattended runs; #433 Hang plaques on files in the desktop tree; #440 Put a wall-display mode on a spare screen; #736 Stream delta patches to the UI; #793 Build an offline-first shell that never blanks (near T-0318); #794 Preview a theme change live across surfaces

## C076 Terminal rendering [UI and motion]
Inline smoke screenshots, structured transcript cards and pty snapshot tests of the band.
- mark: skip — Rows/cards exist. Pty snapshot test is a nice-to-have regression net but value is low versus other work.
- status: partial; value 2/5; effort M; risk low
- evidence: Structured rows and cards in mod (T-0137, T-0228); fm smoke screenshots; band tests exist; no pty snapshot test
- ideas: #401 Wild: Stream a builder lane's edits as a live code morph; #629 Show smoke screenshots inline in the terminal (near T-0137); #783 Render transcripts as structured cards (near T-0228); #787 Snapshot-test the terminal band through a real pty (near T-0286); #789 Show a ghost cursor in smoke recordings

## C073 Design system and motion grammar [UI and motion]
One design spec for every surface, a motion grammar with lint and frame budgets, glyph alphabet, reduced motion and fixture galleries.
- mark: skip — Large cross-surface infrastructure for a single-user tool; value does not justify cost. Freshness/changed-since marks could ride on existing --follow streams later.
- status: missing; value 2/5; effort L; risk low
- evidence: No design spec/lint found; reduced-motion only in eval report html
- ideas: #199 Design a unified empty, loading and error language across band, pane, web and desktop; #392 Compile one design spec to every surface (near T-0322); #393 Gate the UI with screenshot-and-motion diffs (near T-0318); #394 Render every UI state from a fixture gallery (near T-0130); #398 Mark data freshness in the UI; #400 Give each project a generated identity across all surfaces (near T-0375); #404 Honor reduced motion and screen readers everywhere; #586 Define a motion grammar and lint it; #587 Add semantic zoom to every session view (near T-0328); #588 Encode state in a glyph alphabet that never relies on color; #589 Make every number in the UI explain itself (near T-0417); #590 Give optimistic actions an honest rollback animation; #591 Gate motion on a frame budget in `fm smoke` (near T-0318); #633 Mark what changed since each surface last looked (near T-0278)

## C001 Reject vacuous proof [Verification and product checking]
Refuse a done claim whose verify command can't fail, by mutating the code or reverting the fix and checking the check goes red.
- mark: build — Make fm task done refuse a criterion whose verify command also passes on the start tree (or with the diff's hunks reverted), reusing the prove --hunks machinery; today the user must run prove by hand.
- status: partial; value 4/5; effort M; risk low
- evidence: fm task prove --hunks (T-0271, CHANGELOG), evidence --inconclusive (T-0261)
- ideas: #43 Mutate the proof of a finished task (near T-0406); #44 Reject empty verifications; #59 Run mutation checks on the proof behind "done" (near T-0271); #71 Reject gates that can't fail (near T-0338); #97 Verify the verifier with mutation proof (near T-0271); #113 Audit the verifiers: a meta-agent checks that each criterion's verify command can actually fail (near T-0379); #125 Detect weakened verification at the done gate (near T-0364); #165 Reject vacuous proof; #166 Prove the proof by reverting the fix (near T-0297); #169 Calibrate Foreman's own "done"; #179 Catch vacuous verifies with mutation probes; #285 Prove the done-gate itself against a corpus of known-bad closures; #652 Grade every proof on an evidence-strength ladder; #784 Edit criteria live with a "can this fail?" button (near T-0342); #795 Build a proof-strength ledger that fuses mutation, coverage and red-first into one score; #796 Replay the verifier against the pre-fix commit automatically (near T-0224)

## C003 Edit-time sentinel and regression bisect [Verification and product checking]
Run the affected tests as the code is edited, like a shadow CI, with mutation proof of what the sentinel covers.
- mark: build — First version: fm sentinel --bisect runs git bisect in a throwaway worktree on a sentinel-failing check and captures the culprit commit/task as a FIX item; edit-time shadow CI deferred.
- status: partial; value 4/5; effort M; risk med
- evidence: fm sentinel re-runs finished tasks' checks (T-0071); fm impact maps tests; no edit-time run or bisect
- ideas: #4 Run an edit-time test sentinel with mutation proof (near T-0286); #47 Bisect the regression a sentinel finds; #60 Run the edit-time test sentinel (near T-0286); #101 Run a shadow CI daemon on every edit (near T-0318); #173 Bisect regressions found by the night sentinel; #407 Shrink every FIX repro to a minimal failing case (near T-0369); #489 Minimize the guard by replay delta-debugging; #537 Learn the file-to-test map from coverage (near T-0262); #575 Minimise a failing diff by hunks (ddmin) (near T-0271); #632 Record the docs from real runs (near T-0280); #805 Wild: Time-travel bisect for every regression the sentinel finds

## C004 Product journeys from criteria [Verification and product checking]
Generate real user journeys from acceptance criteria, replay them for every task and diff the results.
- mark: build — Allow a criterion to carry a smoke journey (URL plus click/expect steps in Playwright) that fm smoke runs for that task and keeps the screenshots; no LLM generation first.
- status: partial; value 4/5; effort M; risk low
- evidence: fm smoke crawls tabs at two widths (T-0417); no per-criterion journeys
- ideas: #14 Check the product against real journeys (near T-0189); #22 Generate product journeys from acceptance criteria; #49 Replay the product journey and diff it per task (near T-0280); #459 Run a user-defined rehearsal of the product (wild)

## C006 Check non-web products and services [Verification and product checking]
Check APIs, CLIs and services with record/replay, differential, property, fuzz, metamorphic and LLM-rubric tests in a throwaway stack.
- mark: build — Add fm smoke set cmd/http: recorded commands or API calls with expected status/JSON shape run as a gate (JARVIS API/voice endpoints); record/replay and fuzz later.
- status: partial; value 4/5; effort M; risk low
- evidence: fm smoke is web only (fm help); T-0417 targeted web UIs
- ideas: #387 Perturb the environment inside smoke; #423 Isolate each lane's runtime (near T-0379); #447 Check products that aren't web UIs (near T-0417); #448 Record and replay external services in product checks (near T-0417); #449 Differential-test against a reference implementation (near T-0276); #450 Synthesize property and fuzz tests for the diff; #497 Provision a throwaway product stack for smoke; #498 Fuzz what the diff touched (near T-0278); #544 Wild: keep a warm browser daemon for `fm smoke`; #574 Check the product with metamorphic relations (near T-0417); #600 Gate LLM-powered products with rubric evals

## C007 Audit done claims against the diff [Verification and product checking]
Check that every sentence of a done summary is backed by evidence the gates actually ran on this diff, and list what was not verified.
- mark: build — At fm task finish print a 'not verified' list: changed files/hunks no evidence run touched (from recorded touched files and prove --hunks), written into the brief.
- status: partial; value 3/5; effort S; risk low
- evidence: verification grade and unverified assumptions at close (T-0261); fm audit prep (T-0216)
- ideas: #61 Detect drift between the brief and the diff (near T-0280); #76 Check that a closed task did what it said (near T-0117); #163 Detect "asked-for but never done" requests across the inbox history (near T-0364); #168 Audit claims against the diff (near T-0216); #252 Trace every criterion to its test and code (near T-0076); #365 Reconcile two independent ledgers at done (near T-0280); #369 List what was not verified on every done (near T-0379); #379 Measure how much of the diff the evidence ran (near T-0276); #455 Research with provenance; #463 Verify RESEARCH tasks by checking their claims (near T-0277); #469 Re-derive a finished task from its brief alone (near T-0366); #513 Shard "done" into context-blind claim checkers (near T-0277); #550 Detect rework to grade past "done" claims; #560 Diff every "done" against what the gates actually exercised; #580 Bound the error rate of "done" with conformal escalation; #771 Cross-examine the builder before done (near T-0384); #797 Maintain a claim graph linking every sentence of a done summary to its evidence; #800 Verify by independent re-derivation: a second agent solves the spec without seeing the diff, then the two are compared behaviourally; #802 Prove step evidence belongs to the step with causal tracing

## C011 FIX debugging helpers [Verification and product checking]
Help fix bugs with ranked suspect lines, hypothesis ledgers, runtime traces, statistical and deterministic reproduction of flaky bugs.
- mark: build — fm check --repeat N to run a failing gate N times and report pass rate for intermittent bugs; suspect-line ranking later.
- status: partial; value 3/5; effort S; risk low
- evidence: fm task hypo ledger, fm-debugger agent, fm check flake ledger (T-0274)
- ideas: #317 Force diverse retries when a gate fails repeatedly (near T-0280); #380 Verify intermittent bugs statistically; #381 Seed FIX plans with ranked suspect lines; #603 Ground FIX evidence in runtime traces (near T-0178); #612 Give every blocked task an unblock probe (near T-0259); #614 Make intake read pasted transcripts and reproduce first (near T-0291); #693 Reproduce time- and race-dependent bugs in a deterministic simulator

## C013 Gate hygiene [Verification and product checking]
Quarantine flaky gates, pin gate environments, record known-red baselines and flag gates that need network or secrets.
- mark: build — Add quarantine: a gate flagged flaky twice is run but non-blocking with a loud note, plus a recorded known-red baseline list; network/secrets flag later.
- status: partial; value 3/5; effort S; risk low
- evidence: flake ledger and 'predates the task' labels in fm check (T-0047, T-0274)
- ideas: #52 Quarantine flaky gates (near T-0274); #251 Pin gate environments to tell drift from regression; #260 Record a baseline of known-red gates; #720 Run gates hermetically and flag gates that need the network or secrets (near T-0280); #730 Infer each gate's true inputs from the files it reads (near T-0291)

## C010 Behaviour preservation for CLEAN work [Verification and product checking]
Prove a refactor changes no behaviour using characterization tests, before/after capture and AST-level review.
- mark: build — fm task prove variant for CLEAN: record test output/exit before and after and require identical; characterization tests for untested code later.
- status: partial; value 3/5; effort M; risk low
- evidence: CLEAN requires a test run before first edit (T-0071)
- ideas: #96 Delete redundant tests found by replay (near T-0224); #180 Prove behaviour preservation for CLEAN tasks; #258 Wild: Pin current behaviour with characterization tests before touching an unfamiliar repo; #302 Capture behaviour before and after each task (near T-0276); #577 Review at the AST level and certify behaviour-neutral changes

## C002 Hidden checks and planted bugs [Verification and product checking]
Test the verifiers themselves with held-out check variants, planted canary bugs and reward-hacking traps, and score what each gate alone catches.
- mark: skip — Near-duplicate of Reject vacuous proof (mutation/revert already built); canary and honeypot variants add spend for little over prove --hunks.
- status: partial; value 2/5; effort M; risk low
- evidence: fm bench hides commit tests (T-0212); prove --hunks covers mutation
- ideas: #174 Plant canary bugs to test the reviewers; #573 Hold out hidden variants of each task's checks (near T-0207); #582 Wild: Plant reward-hacking honeypots in gates; #645 Compose the final change from the best hunks of racing attempts; #765 Score each gate by what it alone catches (near T-0228); #798 Run a verification canary: plant known bugs and check the gates catch them; #799 Learn a per-project verification policy from escapes (near T-0041); #808 Score verification debt per area and steer the queue toward it

## C008 Adversarial reviewers and red team on done [Verification and product checking]
Have attacker, saboteur and reviewer-panel agents try to break each change before it closes, and settle their disagreements by experiment.
- mark: skip — Adversary lens, debate and split reviewers already exist; more panels mostly add spend.
- status: exists; value 2/5; effort M; risk med
- evidence: adversary lens in fm audit prep/fm-reviewer; fm second debate (T-0276)
- ideas: #7 Run structured adversarial audits (near T-0286); #48 Make the red team break the diff before done; #65 Run an adversarial red-team on "done" claims; #110 Run a standing agent court for every finished task (near T-0375); #112 Add an adversarial tester agent that tries to break each change; #184 Weight reviewers by measured precision (near T-0286); #391 Wild: Hold a "reviewer's duel" with hidden ground truth; #512 Settle reviewer disagreements with an experiment agent; #514 Staff reviewer panels for decorrelated errors; #803 Wild: Run a verification tournament where agents bid on how to break the change, and paid-out bugs fund the budget; #815 Pair every builder with a saboteur (near T-0401)

## C009 Criteria become executable contracts [Verification and product checking]
Turn acceptance criteria into red-first executable checks and a red-to-green board, and edit them live.
- mark: skip — Criteria already carry executable verify commands and red-first proof; a compiler adds little.
- status: exists; value 2/5; effort M; risk low
- evidence: ac 'criterion :: verify', fm task prove red-first (T-0059), fm oracle (T-0226)
- ideas: #70 Write a test-first contract compiler from the brief (near T-0383); #98 Compile criteria into red-first executable checks (near T-0338); #191 Compile acceptance criteria into executable contracts (near T-0276); #300 Record a hypothesis ledger for FIX tasks (near T-0228); #397 Give acceptance criteria a red-to-green board (near T-0263); #496 Record a failing run before fixing it (near T-0280)

## C012 Invariants and cross-task checks [Verification and product checking]
Mine invariants from the repo and gate runs, and turn decisions, vetoes and MASTER.md claims into checks run on every diff.
- mark: skip — Vetoes and doc drift checks exist; mined invariants are speculative with false-positive risk.
- status: partial; value 2/5; effort M; risk med
- evidence: fm vetoes checked against commands/edits; fm docs reports MASTER drift (T-0296)
- ideas: #212 Turn the claims in MASTER.md into executable checks (near T-0206); #265 Mine invariants from the repo and propose them as gates (near T-0224); #382 Mine invariants from gate runs and check each diff (near T-0134); #607 Gate license and provenance on added code and deps (near T-0296); #639 Detect hallucinated APIs at edit time; #691 Resolve every symbol in a diff against reality (near T-0175); #695 Check diffs for licence and provenance contamination (near T-0271); #761 Store absence claims as re-runnable queries; #775 Compile decisions into executable constraints (near T-0170); #806 Assert cross-task invariants: decisions and vetoes become executable checks

## C005 Simulated users of the product [Verification and product checking]
Send a learned or ghost user through the product to explore it, record clips and report what felt wrong.
- mark: skip — Wild and costly; smoke plus the drained-queue product pass and journeys cover the real need.
- status: partial; value 2/5; effort L; risk med; wild
- evidence: fm smoke exploration only (T-0417); drive asks for a product pass when drained
- ideas: #39 Wild: Run a "ghost user" that tries the product like a first-time visitor and posts a clip; #120 Run a user-simulator agent that uses the product like the user (wild); #187 Explore the product as a learned user (wild); #675 Run a time-warped soak with a synthetic user; #804 Wild: Verify against a digital twin of the user, replaying their own session habits on the product



Checklist page: https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW (choices in its db collection "choices": {choice: add|veto, note})
