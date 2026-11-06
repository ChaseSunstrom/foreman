# Catalogue: capability map, approaches, reliability, simplicity, security, and the three deepen files (A1..A35)

Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).

**Reading notes**
- Idea titles are shortened to their key phrase, with the same wording as the files.
- (x2) or (x3) means the same idea appears in two or three rounds or files and is counted once.
- Confidence is high unless noted.
- Task state (from the task files' `status:` lines): T-1328, T-1329, T-1330, T-1336, T-1343, T-1354 are done. T-1333..T-1361 are mostly still `captured` (briefed, unbuilt). Done exceptions: T-1327, T-1332, T-1363.
- Premises checked against the code:
  - `fm code` has zero skill or plugin awareness (no matches for `skill`, `fmlib` or `fmplugins` in fmcode.py, fmcodetui.py or fmcodebench.py).
  - `fm lib source` is a read-only, markdown-only index of `anthropics/skills` and five other repos (`fmlib.py:472-487`).
  - Foreman has no OS sandbox. There is no bwrap or landlock code (`fmbench.py:967` only mentions bwrap in a comment).

## Summary table (security first)

| id | capability | ideas | grounding | value | effort | risk | mark |
|---|---|---|---|---|---|---|---|
| A9 | Control plane, grants, secrets, config lattice | 10 | partial, unverified | 5 | M | med | build (probe test first) |
| A2 | Capability-delta gate on adopt and update | 7 | partial | 4 | M | low | build |
| A8 | Worker judge extensions (out-of-tree, zero-diff) | 10 | mostly done, 2 gaps | 4 | S | low | build (gaps only) |
| A7 | Prompt fencing and provenance | 8 | partial | 4 | S | low | build (envelope) |
| A10 | Runner trust grades, flag lint, model identity | 10 | partial | 4 | S | low | build (lint, grade, canary) |
| A1 | Exec broker for third-party code | 7 | premise: nothing runs yet | 4 | M | med | fold into A16 |
| A6 | Hostile-input corpus and parsers | 9 | partial | 4 | S | low | build |
| A4 | Marketplace identity and tolerant read | 6 | partial | 3 | S | low | build |
| A5 | Licence class | 5 | partial | 3 | S | low | build (with A13) |
| A12 | Guard assurance, safety case, odds and ends | 10 | mostly exists | 3 | M | low | build (stale-stack gate only) |
| A11 | Containment honesty and OS cage | 12 | missing | 3 | M | med | build label only; skip cage |
| A3 | Detonation and sandbox trial | 7 | missing | 2 | L | high | skip (unsafe, L) |
| A13 | Upstream register (lock, depth, one verb) | 12 | partial | 5 | M | low | build |
| A14 | Watch, weekly diff, schedule | 10 | partial | 4 | S | low | build |
| A15 | Sync integrity and rollback | 5 | partial | 3 | S | low | build (one slice) |
| A16 | Skill host for any runner | 7 | missing | 5 | L | med | build |
| A17 | Plugin host and claude facade | 5 | missing | 3 | L | high | skip |
| A18 | Discovery, recommendation, search | 12 | partial | 4 | M | low | build |
| A19 | Adoption trial and skill hygiene | 11 | missing | 3 | L | med | skip until A16 |
| A20 | Cookbook patterns and upstream corpora | 9 | premise partly false | 2 | M | low | skip |
| A21 | Office documents and data | 3 | missing | 3 | M | low | build (asserter) |
| A22 | Per-model technique profile and learning | 8 | missing | 3 | M | med | build literacy probe only |
| A23 | Slot output integrity and mechanical tools | 9 | partial | 4 | M | low | build |
| A24 | Prompt budget, local servers, roster, cost | 12 | partial | 3 | M | med | build prompt check only |
| A25 | Resume and durability | 9 | partial, T-1338 | 3 | S | low | planned T-1338 plus stamp |
| A26 | Park, limits, failover | 9 | partial, T-1356 | 4 | M | med | planned T-1356 plus auth park |
| A27 | Routing, league, handoff | 10 | partial, T-1358, T-1341 | 3 | M | med | planned; skip extras |
| A28 | Crash hygiene | 7 | partial | 3 | S | low | build |
| A29 | Runner probe, preflight, conformance | 8 | partial, T-1335, T-1361 | 4 | M | low | planned T-1335, T-1361 |
| A30 | Toolchain fidelity, LSP, language adapter | 4 | missing | 3 | M | med | build activation only |
| A31 | Config and run-state consolidation | 20 | partial, T-1359 | 3 | M | med | skip, fold T-1359 |
| A32 | Architecture and UI refactors | 15 | mixed | 2 | L | med | skip |
| A33 | Scope process and self-improvement loops | 15 | process | 2 | S | low | skip |
| A34 | Claude Code feature-gap tracking | 7 | partial | 3 | S | low | build (changelog board) |
| A35 | New verbs and input kinds, git workflow | 33 | missing | 2 | M | med | skip, except A35g |

Cluster counts add up to 286 titles.

---

## Security findings first

### A9. Control plane, grants, secrets and the config lattice (10 ideas)

- **Ideas**
  - Make Foreman's state and grants unwritable from inside a run
  - Enforce a tighten-only config lattice (x2: r2-10 and r4-10)
  - Keep secrets off argv (x2: r2-10 and r4-10, the second also "out of env behind run-scoped keys")
  - Make connector credentials unreachable from runners, read-only finance mode
  - Mint a run-scoped, spend-capped API key
  - Attest each child's capabilities from its own init event
- **Grounding: partial.**
  - Worker env drops forge, cloud and registry credentials and secret-named vars (`fmcode.py:82-118`).
  - Model keys are read only from the env var a profile names, never put on argv (`fmmodels.py:36`, `:479-486`). Runner `{prompt}` templates carry only the prompt.
  - Foreman state is the guard category `state-direct` (`fmguard.py:575`). A CLI worker's writes there are reverted and refused by the judge (`fmcode.py:634-640`).
  - Open question (medium confidence): whether a codex or gemini worker's shell can run `fm task set T --allow publish`. The built-in codex and gemini presets run shell without Foreman's command guard (`fmcode.py:57-60`).
  - Lattice: `code.toml` is read from `$FOREMAN_HOME` only (`fmcode.py:844-850`). No per-project config exists yet, so the lattice premise is future work.
  - Init-event attestation: missing. T-1354's lean flags are applied (`fmcode.py:72-73`, `:873-880`), but nothing checks the init event.
- **Mark: build (value 5, effort M, risk med).** One probe test first.
  - Deliver: a test that spawns a fake worker running `fm task set T --allow publish` and `fm ask` grant verbs under `FOREMAN_WORKER_OF`. Close whatever it finds, then kill a stream-json child whose init event lists a tool or MCP server outside the lean set.
  - Done when: `python3 -m unittest plugin.tests.test_code_worker_grants` is green, with a worker-run grant mutation refused and an unexpected init-event tool killed.
  - Skip lattice, run-scoped keys and the connector broker for now (no project config, no connectors).

### A2. Capability-delta gate on adopt and update (7 ideas)

- **Ideas**
  - Gate adopted packs behind cooldown, ring and capability delta
  - Bind adopted assets to a capability manifest, re-diffed on update
  - Show a skill's diff before an upstream update is adopted
  - Pin and verify a hash for every file in an adopted pack
  - Install plugins through the native installer in a scratch config dir
  - Run adopted third-party code only under the guard with a declared-capability manifest
  - Observe what a third-party hook does against its card (moved to A3)
- **Grounding: partial.**
  - `profile()` already lists a plugin's hook events, MCP servers, skills and token cost (`fmplugins.py:65-92`).
  - A yes to install approves a content hash (`fmplugins.py:163-175`). Install is gated by guard category `plugin`, granted via `fm ask` (`fmplugins.py:1-4`, `:378-391`).
  - `fm doctor` has a supply-chain baseline: it warns once on changed, new or gone plugins and MCP servers (`fmdoctor.py:1132-1157`).
  - Missing: a delta of capabilities (new hook event, MCP server, script) that blocks an update. No cooldown. Nothing installs into a scratch `CLAUDE_CONFIG_DIR`.
- **Mark: build (value 4, effort M, risk low).**
  - Deliver: record `profile()` as a capability card at approval. `fm doctor` and `fm plugins check` then refuse an update that adds a hook event, MCP server or script path until `fm doctor --accept-supply`.
  - Done when: `python3 -m unittest plugin.tests.test_plugins_delta` shows a fixture plugin gaining a `PreToolUse` hook flagged with that exact delta, and a SKILL.md body-only edit passing.

### A8. Worker judge extensions (10 ideas)

- **Ideas**
  - Derive the changed-file set two independent ways, fail closed
  - Tripwire the out-of-tree files a worker can reach
  - Verify the changed-file set two ways and tripwire reachable paths (r4-10 dup)
  - Watch every runner's control surfaces, not just git
  - Zero-diff success is a failed step
  - Replay the final verdict from saved evidence in a clean process
  - Cross-check the judge with a second one in POSIX sh
  - Make path identity agree across case-folding and Unicode
  - Detect a runner binary replaced mid-run
  - Pin binaries and detect swaps in one trust ledger
- **Grounding: mostly done.**
  - The set is already derived two ways. `_dirty` uses `git status --porcelain -z -uall` (`fmcode.py:938-941`). A stat walk finds ignored, hidden and mode or ctime changes (`:1102-1114`, `:631-633`). The index-flag walk is at `:1117-1120`.
  - Control surfaces are covered through `_strict` and `classify_write`: Claude settings, plugins, credentials, `~/.codex/config.toml`, `.gemini` and opencode (`fmguard.py:520-534`, `fmcode.py:1123-1133`).
  - Gaps:
    - Only `.git` config, hooks and `~/.gitconfig` are held outside the tree (`fmcode.py:1080-1084`), so a CLI worker's append to `~/.bashrc` is never re-read.
    - A worker that exits 0 with an empty diff is marked done (`fmcode.py:563`). Verify is the only judge.
    - Binary swap is not detected.
    - Path folding is untested (not checked).
- **Mark: build the two gaps (value 4, effort S, risk low).**
  - Deliver: add `~/.bashrc`, `~/.profile`, `~/.zshrc` and `~/.codex`, `~/.gemini` and `~/.claude` settings to the `own` set so they are restored and reported. Mark an edit step with a no-effect diff as `no-effect`.
  - Done when: `python3 -m unittest plugin.tests.test_code_judge` shows a fake worker appending to `$HOME/.bashrc` reverted and named in a `revert` event, and an empty-diff edit step reported.
  - Skip the sh judge (L, common-mode risk is already low) and the binary ledger (see A29).

### A7. Prompt fencing and provenance (8 ideas)

- **Ideas**
  - Wrap untrusted text in per-session nonce-tagged envelopes
  - Fence prompt-borne metadata channels (r3-10: branch, commit, issue text)
  - Fence prompt-borne metadata: terminal escapes, bidi, tool descriptions (r4-10)
  - Rebuild handoff packets from ledger facts, not transcripts
  - Mark every byte entering a slot prompt with a provenance tag (r4-10)
  - Track prompt provenance per byte and fail closed (r3-10)
  - Lint Foreman's injected strings against eight prompt-tutorial rules
  - Turn the prompt-tutorial lessons into a lint on Foreman's own prompts
- **Grounding: partial.**
  - `c.plain` strips control, bidi and zero-width characters (`fmcore.py:2229`). Imported skill text passes through it (`fmlib.py:467-468`, `:526-527`). `_printable` cleans task text (`fmcode.py:1435`).
  - `fm doctor` flags invisible characters in instruction files (`fmdoctor.py:811-821`).
  - No nonce or data envelope was found in fmcode.py, fmmodels.py or fmcore.py (one `untrusted` mention at `fmcore.py:3285` is a comment).
  - Slot prompts mix repo text and instructions without tags (`fmcode.py:211-233`, medium confidence).
- **Mark: build the envelope and metadata fence only (value 4, effort S, risk low).** Skip per-byte provenance (L), the tutorial-rule lint (low value) and handoff packets (T-1341 is unbuilt).
  - Deliver: wrap repo text, tool results and metadata in `<data-NONCE>` blocks in `fm code` slot prompts, stripping lookalike tags.
  - Done when: `python3 -m unittest plugin.tests.test_code_envelope` shows a README containing `</data-...>` plus "ignore previous" rendering inside the envelope.

### A10. Runner trust grades, flag lint, model identity (10 ideas)

- **Ideas**
  - Lint user-defined runners for dangerous flags
  - Grade each runner by guard coverage; the grade gates privilege
  - Gate repos on a per-runner data-handling card
  - Give each runner a measured gullibility and privilege grade (r4-10)
  - Give each model a gullibility score from a planted-injection exam (r2-10)
  - Pin model identity (digest) to grades and privilege
  - Slip a known-answer canary slot at run start (r2-06)
  - Honeytoken credentials plus a canary slot (r4-10)
  - Refuse non-inert local model artifacts (premise false: Foreman never loads weights; no weight loader found in `plugin/lib`)
  - Harden the model-endpoint client (mostly done)
- **Grounding: partial.**
  - Endpoint client: no redirects (`fmmodels.py:84-90`), key never over plain http except loopback (`:300-301`), no userinfo in base_url (`:298-299`), key scrubbed from errors (`:93`).
  - Missing: link-local or `169.254.169.254` deny, and DNS rebinding.
  - `code.toml` runners are only checked for `{prompt}` (`fmcode.py:857-870`). No flag lint. The built-in codex preset is `--full-auto` (`:74`).
  - A sensitive repo already refuses cloud models and any worker CLI (`fmcode.py:290-301`, `:1206-1208`). That is the coarse data-handling card.
  - No grading by guard coverage is shown.
  - `fm code bench` seeds a canary file (`fmcodebench.py:105-111`).
- **Mark: build (value 4, effort S, risk low).**
  - Deliver: a dangerous-flag table (`--yolo`, `--dangerously-skip-permissions`, `danger-full-access`) acknowledged per runner by template hash. `fm code runners` shows a guard-coverage grade (A guard in the command path, B sandbox, C post-hoc). The grade is also shown on the home runner list.
  - Done when: `python3 -m unittest plugin.tests.test_code_runners_lint` shows a `code.toml` runner containing `--yolo` refused until acknowledged, and editing the template voiding the acknowledgement.
  - Also add the link-local deny (S).
  - Skip the gullibility exams, digest and honeytoken canary (low value).

### A1. Exec broker for third-party code (7 ideas)

- **Ideas**
  - Execute imported scripts only through one exec broker (r1-06)
  - Run every imported script through one exec broker with the guard as its only door (r4-10)
  - Run every skill script under the guard (deep-3)
  - Make the guard's verdict the only thing a third-party asset can set
  - Use adopted skills and plugins in place, never vendored
  - Tag imported scripts with an idempotence class
  - Run adopted third-party code only under the guard with a manifest (deep-2)
- **Grounding: premise false today.**
  - Nothing imported runs. Sources are a read-only checkout (`fmlib.py:472-475`) with hooks off (`_SAFE_GIT`, `:477-479`).
  - Plugins run via `claude plugin install` gated by a grant (`fmplugins.py:378-391`).
  - Needed the moment A16 executes a `scripts/` path.
- **Mark: fold into A16** (value 4, effort M, risk med). Do not build separately. The A16 brief must route script runs through `fmguard`, as `Run.act`/`guard` does for Bash (`fmcode.py:470-472`).

### A6. Hostile-input corpus and parsers (9 ideas)

- **Ideas**
  - Ship a hostile-skill and schema-drift zoo
  - Run a poison-asset corpus through the indexer
  - Detect over-broad and hijacking skill descriptions
  - Treat cookbook notebooks as inert data until converted
  - Parse registry.yaml with a stdlib YAML-subset reader, fuzzed
  - Freeze a mini-corpus of each repo's shape plus a live drift canary
  - Harvest documented examples as parser and guard fixtures
  - Share only hashes of rejected assets (immune feed)
  - Run an adversary trial for routing hijack on each candidate pack
- **Grounding: partial.**
  - The indexer is already defensive: symlinks skipped and resolved under the repo root (`fmlib.py:507-515`), name sanitised and capped at 64 (`:526`), description cleaned and capped at 400 (`:527`), frontmatter read from the first 4000 chars (`fmplugins.py:48-62`).
  - Missing: a hostile corpus test (not checked for fmlib tests), a description-hijack lint, and any YAML or notebook reader (none needed today).
- **Mark: build zoo, poison corpus, hijack lint and notebook-inert rule (value 4, effort S, risk low).** Skip registry.yaml, immune feed and adversary trial.
  - Deliver: a checked-in corpus of at least 25 bad assets run through `_index_source`, plus a breadth lint that holds "use for every task" descriptions out of `fm lib search` (shown in `fm doctor`).
  - Done when: `python3 -m unittest plugin.tests.test_lib_hostile` is green and every item is quarantined with a reason.

### A4. Marketplace identity and tolerant reads (6 ideas)

- **Ideas**
  - Keep a local transparency log of marketplace entries
  - Treat a marketplace rename or source change as a new install (x2: r2-10, r4-10)
  - Follow marketplace renames and yanks on installed plugins
  - Read marketplace.json tolerantly and reconcile renames
  - Search marketplace.json locally with a stat-keyed cache
- **Grounding: partial.**
  - `index()` reads every `marketplace.json` entry as a dict. A non-dict entry would crash it. `renames` is never read (`fmplugins.py:113-126`).
  - `entry_hash` covers the entry and local copy (`:125`, `:163-170`).
  - Install is by id only, so a rename silently repoints.
  - Search is lexical and uncached, but fast enough (`:197-211`).
- **Mark: build (value 3, effort S, risk low).**
  - Deliver: a tolerant per-entry read (skip bad entries with a reason). Trust keyed to (name, source, sha), so a rename or source change reads as new.
  - Done when: `python3 -m unittest plugin.tests.test_plugins_market` shows a fixture with one non-dict entry still loading the rest, and a renamed plugin shown as untrusted.
  - Skip the log and the cache.

### A5. Licence class (5 ideas)

- **Ideas**
  - Keep a license ledger that fails closed
  - Enforce a three-value licence class at the single copy chokepoint
  - Enforce "ideas only" with a verbatim-overlap check
  - Mark licence provenance on every adopted asset
  - Give each skill a cost and licence label everywhere
- **Grounding: partial.**
  - `_license()` stores the first line of the LICENSE file or "no license file" (`fmlib.py:531-539`). `source.json` keeps it (`:564-566`) and `fm lib source list` prints it (`:648`).
  - No class, and nothing refuses to copy. Nothing copies today. Search output marks text as third-party data (`:993`).
- **Mark: build with A13 (value 3, effort S, risk low).**
  - Deliver: classify into open, source-available and ideas-only in `source.json`, and refuse any copy path for the last two.
  - Done when: `python3 -m unittest plugin.tests.test_lib_licence` shows the no-licence tutorial fixture classed `ideas-only` and a copy attempt refused naming the class.
  - Skip the n-gram overlap check.

### A12. Guard assurance, safety case and odds and ends (10 ideas)

- **Ideas**
  - Require a differential soundness oracle for every fast path
  - Hold a bounty board for the guard's blind spots
  - Run a rival-hook arena on the claude-code hook examples
  - Hold a nightly adversarial maintainer review of Foreman's claims
  - Generate a safety case with a live check per claim
  - Refuse unattended modes when the safety stack is stale (x2: r3-10 and r4-10, the latter plus a safety case)
  - Add a harness-level misuse screen
  - Make suggested commands paste-safe (premise false: no clipboard code in `plugin/lib`)
  - Cross-check... (moved to A8)
- **Grounding: mostly exists.**
  - Differential and corpus tests exist: `test_guard_diff.py`, `test_guard_cases.py`, `test_guard_mine.py`.
  - A canary exists (`fm canary`, `fmcli.py:5518`; `fmhooks.py:369-371`; `fm release --canary-status`, `:5240`).
  - No "refuse unattended when stale" gate (not found).
- **Mark: build the stale-stack gate only (value 3, effort M, risk low).** Skip the rest (low value, or premise false).
  - Deliver: `fm code --unattended` and `fm release --push` refuse when the last canary or guard-corpus replay is red or older than N days.
  - Done when: `python3 -m unittest plugin.tests.test_unattended_gate` shows a stubbed failing replay refusing both and naming the check.

### A11. Containment honesty and OS cage (12 ideas)

- **Ideas**
  - State what containment is real, from probed primitives
  - Mark every run's outer edge with a canary the worker can't see
  - Show the run's excess power as one number
  - Run the worker as a separate OS user with an ACL
  - Track descendants with a subreaper or cgroup (partly done)
  - Enforce the run envelope from a separate process
  - Open network only for the declared dependency step
  - Burn-after-reading mode (x2: r3-10, r4-10)
  - Leave a last-will sidecar that outlives `fm`
  - Wild canary and honeytoken (moved to A10)
  - Classify spawn exhaustion (moved to A28)
- **Grounding: missing, except one piece.**
  - Linux subreaper is done: `prctl PR_SET_CHILD_SUBREAPER` (`fmcode.py:754-805`), orphan kill at `:808`.
  - No bwrap, landlock or unshare use was found. The `bwrap` mention is a comment (`fmbench.py:967`).
  - Closing T-1337 (process registry) covers survivors after a hard kill.
- **Mark: build the containment label only (value 3, effort S, risk low).** Skip the cage, OS user, separate enforcer, network window and burn-after-reading (sudo or user-namespace dependent on a hardened kernel; unsafe to promise).
  - Deliver: probe at start and print `contained by: guard only` (or the primitive) in the start event.
  - Done when: `python3 -m unittest plugin.tests.test_code_containment_label` shows a stubbed probe-off producing the weaker label.

### A3. Detonation and sandbox trial (7 ideas)

- **Ideas**
  - Observe what a third-party hook does, diff against its card
  - Compare a skill's declared behaviour with its detonated behaviour (r1-10)
  - Detonation chamber (r4-10)
  - Keep a pre-adoption "quarantine ward"
  - Run a skill from a URL and sha in a throwaway sandbox
  - Soak newly synced content in shadow
  - Bisect imports to find the asset causing a failure
- **Grounding: missing.** Needs an OS sandbox that does not exist (see A11).
- **Mark: skip** (value 2, effort L, risk high; unsafe without a real sandbox). A2's static delta covers the cheap part.

---

## Integration and upstream capabilities

### A13. Upstream register: lock, depth, one manifest, one verb (12 ideas)

- **Ideas**
  - Pin the six upstreams in a licence-aware lockfile with a coverage ledger
  - Pin the six repos in one `sources.lock`
  - Keep the six repos in one `upstreams.toml`
  - Build one `fm upstream` engine that owns lock, diff and ledger
  - Give each upstream a depth dial (reference, index, host, emulate)
  - Point `fm plugins` and `fm scout` at all six repos
  - Add one `fm add <thing>` verb for every upstream capability
  - Sniff repo shape for a generic `fm adopt URL` (note: `fm adopt` already means "take in an existing repo", `fmcli.py:5494`)
  - Adopt upstream assets as merges on an orphan branch
  - Land each adoption as a branch with its bench result
  - Serve a curated private marketplace
  - Publish Foreman's adopted-and-trialled set as a marketplace.json
- **Grounding: partial, and the base exists.**
  - `fm lib source` records url, commit sha and licence (`fmlib.py:564-566`).
  - The clone is sparse and `*.md`-only, with an atomic swap (`:542-579`).
  - `DEFAULT_SOURCES` holds six repos, but only `anthropics/skills` is among the user's six (`:482-487`). The other five are not registered.
  - `*.md`-only means `marketplace.json`, `registry.yaml` and notebooks are never fetched (`:561`).
  - Scout refreshes sources weekly (`fmscout.py:133-150`).
  - No depth, no change-review gate: `update` just moves the pin and prints names (`fmlib.py:629-640`).
- **Mark: build (value 5, effort M, risk low).** Skip the branch-merge, private marketplace and publish ideas.
  - Deliver: register `claude-code`, `claude-cookbooks`, `claude-plugins-official`, `financial-services` and `prompt-eng-interactive-tutorial` as sources. Add a per-repo `depth` and `licence class` (A5). Add `marketplace.json` to the sparse set, and `fm lib source list` shows pin, depth and class. No new top-level verb.
  - Done when: `fm lib source defaults --dry` lists all six repos with a depth, `python3 -m unittest plugin.tests.test_lib_sources` passes, and a `reference`-depth repo yields no installable entry.

### A14. Watch, weekly diff, schedule (10 ideas)

- **Ideas**
  - Watch upstreams with `git ls-remote` and sparse fetch
  - Fetch upstream offline-first with conditional requests and a circuit breaker
  - Make "automatically" a weekly diff, never a silent install
  - Offer follow-up adoption as a single weekly decision card
  - Radar for open upstream pull requests
  - Adopt skills from the six repos on a schedule
  - Adopt at most three upstream capabilities per release
  - Predict the next upstream feature and pre-build its adapter
  - Rank upstream changes by what your own failures needed
  - Fetch each upstream by two independent paths (moved to A15)
- **Grounding: partial.**
  - `probe_sources` refreshes stale sources weekly inside the slow scout run (`fmscout.py:133-150`). It prints nothing and does not capture a finding.
  - Scout captures one task per new Claude Code release (`:53-64`).
  - Offline failures are swallowed (`:148-149`).
  - Network is only in the slow probes, so no hook blocks.
- **Mark: build (value 4, effort S, risk low).**
  - Deliver: when a refresh changes a source's commit, capture one finding naming added, removed and renamed items and the licence class (nothing installs). Use `ls-remote` to skip clones when the sha is unchanged.
  - Done when: `python3 -m unittest plugin.tests.test_scout_sources` shows a changed fixture sha creating exactly one capture and an unchanged sha making no fetch.
  - Skip the PR radar, predictor, quota and decision card.

### A15. Sync integrity and rollback (5 ideas)

- **Ideas**
  - Sync upstream assets transactionally with a last-good snapshot
  - Roll back a single adopted asset when its probe fails after an update
  - Fetch each upstream by two independent paths
  - Hold an upstream-outage game day
  - Freeze... (in A6)
- **Grounding: partial.**
  - `source_add` clones into a temp dir, indexes, then swaps (`fmlib.py:556-579`), and `finally` removes the temp dir. A failed add leaves nothing behind, and the old copy stays until the swap.
  - Not covered: a per-asset rollback.
- **Mark: build the injected-kill test only (value 3, effort S, risk low).**
  - Done when: `python3 -m unittest plugin.tests.test_lib_source_kill` kills `source_add` at each step of a fixture and the previous index is intact.
  - Skip two-path hashing and the game day.

### A16. Skill host for any runner (7 ideas)

- **Ideas**
  - Run Agent Skills with progressive disclosure on any model
  - Serve skills to any runner via `fm skill index|load|run`
  - Build a skill host every runner shares
  - Translate upstream shapes into fm code runner capabilities
  - Accept one upstream shape: a folder with a markdown file
  - Make SKILL.md the one format for playbooks and cards
  - Gate imported-skill context on measured load
- **Grounding: missing in `fm code`.**
  - Zero skill references in fmcode.py, fmcodetui.py or fmcodebench.py.
  - The pieces exist elsewhere: indexed skills (`fmlib.py:597-602`) and an `fm lib search` (`:656-668`). `profile()` estimates tokens at about 4 characters each (`fmplugins.py:65-92`).
  - `fmdoctor.check_frontmatter` (`fmdoctor.py:250`) already lints Foreman's own skill frontmatter, so the one-format idea is partly done.
- **Mark: build (value 5, effort L, risk med). Slice first.**
  - Deliver: `fm code --skill NAME` (or a plan slot naming one) loads the body into the step prompt. Only metadata (about 100 tokens) is in the prompt until then. `scripts/` runs only through `fmguard`'s Bash verdict (absorbs A1), with a per-model token budget.
  - Done when: `python3 -m unittest plugin.tests.test_code_skill` runs a seeded skill with a `scripts/` helper under a fake non-Claude runner. The prompt holds metadata until activation, and a planted `curl` in the script is refused.

### A17. Plugin host and claude facade (5 ideas)

- **Ideas**
  - Host Claude Code plugins on any runner
  - Phase-compile slash commands into harness state graphs
  - Differential-test the plugin host against recorded hook traces
  - Emulate only the gap with a runner x capability matrix
  - Make `fm code` a `claude`-compatible facade
- **Grounding: missing.**
  - `fm agents` already runs Foreman's own hook in codex, gemini and opencode (`fmagents.py:1-4`, `:23-28`).
  - `fm code` has its own `--json` schema (`fmcode.py:89-109`), not stream-json.
- **Mark: skip** (value 3, effort L, risk high). Host-in-harness needs a loader for hooks, commands and MCP with no demand evidence, and the guard cannot confine non-Claude shells. Revisit after A16.

### A18. Discovery, recommendation and search (12 ideas)

- **Ideas**
  - Recommend marketplace plugins from repo signals, trial before adopting
  - Recommend the top three plugins per project, never auto-install
  - Rank plugin recommendations by backtest against the user's ledger
  - Diff the user's enabled plugins against upstream's catalog
  - Resolve `@skill:`, `@plugin:`, `@pattern:` references in requests
  - Let a request pull the matching upstream capability on demand
  - Offer the matching upstream skill in one line at intake
  - Bundle skills into role packs that pick themselves
  - Resolve requests like dependencies, with a lockfile
  - Index all sources in local SQLite FTS5 as `fm sources find`
  - Use grep as the index for the pinned upstream trees
  - Ask a pinned repo, citation or "unknown"
- **Grounding: partial.**
  - `fm plugins find` is lexical over marketplace entries (`fmplugins.py:197-211`).
  - `fm lib suggest` matches card detect signals to a project (`fmlib.py:440-451`).
  - `fm lib search` covers plugin and source skills (`:656-668`).
  - Not present: repo-signal plugin suggestion, intake offer, `@` handles, or an index beyond SKILL.md and agents.
- **Mark: build the intake offer plus a suggest verb (value 4, effort M, risk low).** Reuse `find` and `fm lib search`. Skip FTS5, resolver and backtest.
  - Deliver: `fm code "<request>"` prints one offer line when `fm lib search` has a strong match (name, licence class, token cost), never installing. `fm plugins suggest` lists three with reasons.
  - Done when: `python3 -m unittest plugin.tests.test_code_offer` shows "extract tables from this pdf" printing exactly one offer and a no-match request printing none.

### A19. Adoption trial and skill hygiene (11 ideas)

- **Ideas**
  - Adopt only where a duel shows a loss
  - Gate every adoption through a trial that must beat baseline
  - Score skills by whether they changed the outcome
  - Show one unified catalog in the fm code app
  - Draw the skill loadout and overlap as a live pane
  - Retire skills that go unused or never helped
  - Unload adopted packs unused for 30 days (atrophy)
  - Write the skill from the run, spec meter live
  - Rank... (see A18)
  - Rank upstream changes by failures (A14)
  - Hold... (n/a)
- **Grounding: missing.** It depends on A16, `fm code bench` (`fmcodebench.py:168`) and a noise-band method.
- **Mark: skip until A16 ships** (value 3, effort L, risk med). The bench has 4 seeds (`fmcodebench.py:22-44`), too few to detect a skill's effect.

### A20. Cookbook patterns and upstream corpora (9 ideas)

- **Ideas**
  - Harvest the cookbook patterns as `fm code` plan templates
  - Turn the cookbook patterns into skills the harness can invoke
  - Reduce orchestration to the five cookbook loop shapes
  - Make plans cite the loop pattern they follow
  - Synthesize "strategy cards" from cookbook patterns
  - Turn cookbook notebooks into `fm code bench` cases
  - Mine the financial-services marketplace as a live workload corpus
  - Run one financial-services skill end to end per release
  - Generate a cookbook-style notebook from any run
- **Grounding: premise partly false.** `fm code` already is a plan, small steps, verify and fix-rounds loop (`fmcode.py:51` `ROUNDS=3`, `:174-203`). Verify is the evaluator, so evaluator-optimizer exists in effect. There is no notebook parser.
- **Mark: skip** (value 2, effort M, risk low): done in effect or low value. Revisit the finance smoke after A16.

---

## Models and output quality

### A21. Office documents and data (3 ideas)

- **Ideas**
  - Lint xlsx and docx deliverables with stdlib zip and XML
  - Verify office deliverables with a stdlib OOXML asserter
  - Read office documents and read-only data through stdlib tools
- **Grounding: missing.** Verify commands are arbitrary shell checked by the guard (`fmcode.py:689-693`), so an asserter script fits unchanged.
- **Mark: build the asserter (value 3, effort M, risk low).**
  - Deliver: `fm check office FILE --cell Sheet1!B7=42 | --sheets N | --no-errors`, stdlib only.
  - Done when: `python3 -m unittest plugin.tests.test_check_office` shows a workbook with `#REF!` failing and a clean one passing.
  - Skip the read tool.

### A22. Per-model technique profile and learning (8 ideas)

- **Ideas**
  - Probe which prompting techniques move a given model
  - Grade every model with a technique exam from the tutorial's list
  - Ten-exercise literacy probe replaces the capability profile
  - Remember each model's repair pairs as its own few-shot
  - Train a free apprentice by shadowing the strong runner
  - Oracle tree-diff teacher
  - Let skills teach the model with the tutorial's techniques
  - Close the complaint to bench to patch loop (see A33)
- **Grounding: missing.** `bench` grades closing rate on 4 seeds only (`fmcodebench.py:66-137`).
- **Mark: build the literacy probe only (value 3, effort S, risk low).** Skip the rest (noise, spend, cost about $25 for the oracle).
  - Deliver: ten small graded prompts (tagged data, JSON only, refuse to invent) scoring a model 0-10 in `fm code runners --probe`.
  - Done when: a fake runner that ignores the format scores below 3 in a unit test.

### A23. Slot output integrity and mechanical tools (9 ideas)

- **Ideas**
  - Require a verbatim quote or "unknown" in every fact slot
  - Reject elided-code output and track per-model laziness and refusals
  - Match edit anchors tolerantly before spending a repair call
  - Continue and stitch truncated model output
  - Digest compiler and test output into ranked diagnostics
  - Offer a deterministic compute tool for exact answers
  - Cluster log lines into templates before showing them to a model
  - Search installed `--help` and man pages offline for flag grounding
  - Wild: write edits as a three-way merge (moved to A35)
- **Grounding: partial.**
  - Edit is exact and must occur once (`fmcode.py:128`, `:444-450`).
  - A `length` stop re-asks, but there is no stitching (`:504-508`).
  - `slot` repairs a bad JSON answer twice (`:211-233`).
  - Verify output is cut to `CAP` characters (`:712`, `:698`), not parsed.
  - No elision check.
- **Mark: build elision rejection, tolerant unique anchors and a verify-output digest (value 4, effort M, risk low).** Skip quote slots, the compute tool, log clustering and help search.
  - Done when: `python3 -m unittest plugin.tests.test_code_edit_rules` shows `# ...rest unchanged` rejected and re-asked. Of 20 near-miss anchors, the unique ones apply and the ambiguous ones are refused. A failing pytest hands the next slot at most five `file:line: message` items.

### A24. Prompt budget, local servers, roster and cost (12 ideas)

- **Ideas**
  - Detect silent prompt truncation (reported vs expected prompt tokens)
  - Shed an overflowing prompt in a fixed priority order
  - Use local servers' KV cache and keep-alive
  - Apply chat templates for raw completion endpoints
  - Manage the local model server's lifecycle
  - Downshift local models on OOM or swap
  - Watch the model roster for drift
  - Pretend a model is gone
  - Audit a new model overnight when it appears
  - Reconcile the cost ledger against provider bills
  - Rewrite an app's Claude model calls for a new model
  - Heat-map diffs by self-consistency (moved to A35)
- **Grounding: partial.**
  - Local context is a fixed default: `LOCAL_CONTEXT = 8192` (`fmmodels.py:69`, `:111`, `:159`). T-1360 (real server context) is captured.
  - `prompt_tokens` is read from replies (`:519`) but not compared with the estimate.
  - Small-context models get half the output cap (`fmcode.py:1218`).
  - `models.json` is hand-written, with no roster check in `fm doctor`.
  - `fm cost` reads Claude transcripts only. T-1357 prices fm code calls.
- **Mark: build the prompt-token check only (value 3, effort S, risk low).** Skip the rest (user-managed servers, or no demand).
  - Done when: `python3 -m unittest plugin.tests.test_models_trunc` shows a stub reporting `prompt_tokens` under 70% of the estimate failing the slot with a "truncated at N tokens" cause.

---

## Reliability and runs

### A25. Resume and durability (9 ideas)

- **Ideas**
  - Cache accepted slot answers in the run journal
  - Snapshot the run journal so resume cost stays flat
  - Resume validity stamp
  - Run a nightly resume drill on the user's finished runs
  - Rehearse a kill-and-resume before every unattended run
  - Make quitting a crash
  - Adapt checkpoint density to the repo's failure rate
  - Lint that every exit path writes a typed terminal record
  - Land a run by compare-and-swap ref update from the recorded base
- **Grounding: partial, covered by T-1338.**
  - Every phase message is journaled (`fmcode.py:668-671`). Resume skips done phases and answers lost tool calls (`:479-495`). `--resume` exists (`:1285-1331` per the earlier catalogue).
  - T-1338 (captured) owns "names unfinished runs" and the kill-at-every-station tests.
  - Sweeps and CAS landing: `fm code` does not land on a user branch yet (T-1352 undo and PR is captured).
- **Mark: planned T-1338, plus the validity stamp (value 3, effort S, risk low).**
  - Deliver: a journal-header hash of (base ref, resolved config, runner card). A resume with a changed part prints a three-line diff and needs `--accept-drift`.
  - Done when: `python3 -m unittest plugin.tests.test_code_resume_stamp` shows a changed `code.toml` between kill and resume prompting.
  - Skip the drills, snapshots and CAS.

### A26. Park, limits, failover (9 ideas)

- **Ideas**
  - Park on expired login, don't fail
  - Park runs on expired login or rate limit, then resume them
  - Pass a deadline tree through every run
  - Share one retry-token pool down the deadline tree
  - Put a cross-process rate limiter per endpoint and key
  - Add hysteresis to runner breakers and fallback
  - Pause globally on correlated failures
  - Classify spawn exhaustion
  - Downshift local models on OOM or swap (see A24, skipped)
- **Grounding: partial.**
  - Stall events classify `launch|prompt|limit|silent` (`fmcode.py:736-751`, `:587-593`). A `limit` cause is detected but nothing parks.
  - Calls retry 429 and 5xx three times, waiting at most 20 s (`fmmodels.py:35`, `:320-326`).
  - No whole-run deadline; a worker has `WORKER_TIMEOUT=1200` (`fmcode.py:56`).
  - T-1356 (limits and failover) is captured.
- **Mark: planned T-1356.** Add one criterion: an auth-expiry line (`please log in`) parks the run, consuming no retries, with the login command in the event (value 4, effort S, risk low).
  - Skip the retry pool, global pause and rate limiter (no multi-run load evidence).

### A27. Routing, league and handoff (10 ideas)

- **Ideas**
  - Route steps to runners by their recorded results
  - Race two runners on a step, keep the first that passes
  - Keep a runner league table that ranks and promotes
  - Pay in tokens: a runner budget market
  - Record a fallback chain and replay a run on another runner
  - Hand a stuck run to a live CLI and take it back
  - Freeze default routing to a three-line rule
  - Show per-endpoint reliability weather before choosing a runner
  - Keep a heat strip of the user's own dependencies
  - Hysteresis (A26)
- **Grounding: partial.**
  - Premise already true for "freeze routing". `pick_runner` is exactly the project's choice, then `code.toml`'s, then the first verified installed runner (`fmcode.py:890-913`).
  - T-1358 (routing by record) and T-1341 (hand to a live CLI) are captured.
  - Races and league need spend and a noise band.
- **Mark: planned T-1358, T-1341; skip the rest** (value 3, effort M, risk med). Add one criterion to T-1358: the plan header names which of the three rules chose the runner.

### A28. Crash hygiene (7 ideas)

- **Ideas**
  - Recover stale git locks by owner proof
  - Arm `faulthandler` in every long-running verb
  - Probe filesystem semantics before trusting locks
  - Heal by quarantine, never by deletion
  - Assert resource flatness in the soak
  - Claim tasks by atomic rename, not leases
  - Leave a last-will sidecar (A11)
- **Grounding: partial.**
  - Locks use flock (`fmcore.py:824-837`). The ledger tolerates no flock and leaves a gap (`:894`).
  - `fm repair` already quarantines crash-truncated objects (`fmcli.py:5482`).
  - No faulthandler (not found). No `index.lock` handling in fmcode.
- **Mark: build `faulthandler`, stale `index.lock` and the doctor fs probe (value 3, effort S, risk low).**
  - Done when: `python3 -m unittest plugin.tests.test_code_crash` shows a hung verb writing a stack dump, and `index.lock` removed only when no live process has the repo as cwd.
  - Skip rename-claims and the soak.

### A29. Runner probe record, preflight, conformance, adapters (8 ideas)

- **Ideas**
  - Build one runner probe record, the only source of truth
  - Feed every runner consumer from one probe result
  - Add preflight lamps that block a run before it burns tokens
  - Use one runner address string everywhere
  - Show detected-only runners as one line
  - Add misbehaving fake runners as a conformance suite
  - Acquire a missing runner CLI into a private prefix
  - Let the runner write its own adapter, then check it
- **Grounding: partial.**
  - Registry done (T-1328): `RUNNERS`, `all_runners`, `pick_runner` (`fmcode.py:65-80`, `:857-913`).
  - `runners --check` only runs `--version` (`:1623-1628`).
  - Detected-only runners (opencode, qwen, cursor-agent, goose, amp) are listed with "no preset" (`:77`, `:1632`).
  - T-1335 (preflight and lamps) and T-1361 (misbehaving fakes) are captured.
- **Mark: planned T-1335 and T-1361.** Skip acquisition and the self-written adapter (installs software or lets a model draft a shell template; unsafe). Cluster value 4, effort M, risk low.

### A30. Toolchain fidelity, LSP, language adapter (4 ideas)

- **Ideas**
  - Activate the project's own toolchain before every worker and gate
  - Provision and health-check language servers
  - Let the harness write its own language adapter
  - (Search `--help`: see A23)
- **Grounding: missing.** No `.tool-versions`, mise, asdf or nvm handling in fmcode (not found). Gates run with `worker_env()` as is (`fmcode.py:113-118`).
- **Mark: build the activation only (value 3, effort M, risk med).** Skip LSP and the self-written adapter. Caution: activating `.envrc` or mise runs repo code, and the guard already treats `direnv allow` as a system action (`fmguard.py:4160`). Activate only trusted tools.
  - Done when: `python3 -m unittest plugin.tests.test_code_toolchain` shows a fixture with `.tool-versions` having its gate's recorded interpreter equal the pinned one.

---

## Process, consolidation and new surfaces

### A31. Config and run-state consolidation (20 ideas)

- **Ideas**
  - Merge `models.json` and `code.toml` into one config file
  - Replace the split with one rule: a runner is a command line
  - Ship `code.toml` as a commented template
  - Reveal settings only after a run needs them
  - Reconcile a desired-state file with `fm plan` and `fm apply`
  - Manage everything Claude Code reads from one panel
  - Make a run a directory of three files
  - Make the run directory the whole API
  - Make the run branch the only run state
  - Store each run as a section of its task brief
  - Emit one run report that every other output reads
  - Emit `replay.sh` from every run
  - Plan-only time machine
  - Run heavy proofs on the user's own CI
  - Git remote as the request surface
  - Land multi-project sweeps as a saga
  - Wild: Treat "etc." as one bounded round (r3-07)
  - Wild: Treat "etc." as a counted budget (r4-07)
  - Hold approvals to a quiet window per device (moved to A35)
  - Build the home as a plain directory listing (moved to A32)
- **Grounding: partial.** `code.toml` is read by `code_config` (`fmcode.py:844-854`) and `models.json` by `_config` (`fmmodels.py:126-136`). T-1359 (config view) is captured.
- **Mark: skip, fold into T-1359.** These are L rewrites or conflict with captured briefs (T-1338, T-1352, T-1330).

### A32. Architecture and UI refactors (15 ideas)

- **Ideas**
  - Give endpoint models the same worker path as CLIs
  - Give every runner the same worker contract through an adapter shim
  - Route every feature through three seams
  - Run `fm code bench` as an ordinary project
  - Make the loop card the executable spec
  - Ship the whole harness as a one-file `fm.pyz`
  - Remove Python TUI extensions
  - Run a delete-and-see pass nightly
  - Cut the four line-mode switches to one `--format`
  - Share one stall classifier between TUI, events and doctor
  - Show one status line that reuses the stall classifier
  - Give the home screen a mail-style inbox of runs
  - Build the home screen as a plain directory listing
  - Add an `fm code shell` REPL
  - Make the guard... (A1)
- **Grounding: mixed.**
  - Two execution paths exist by design: `Run.phase` for endpoint models and `Run.work` for CLIs (`fmcode.py:477`, `:530`).
  - One classifier already exists: `stall_cause` (`fmcode.py:736`).
  - `fm code why` does not exist (see Noticed).
  - T-1365 (extensions outside the guard) was dropped.
- **Mark: skip** (value 2, effort L, risk med). Refactors with no user-visible win; UI belongs to the other half.

### A33. Scope process and self-improvement loops (15 ideas)

- **Ideas**
  - Hold one open FEATURE per area
  - Finish the half-built before starting anything new
  - Hold an exit-gate census per round
  - Replace the 29 round-1 briefs with three story scripts
  - Close the complaint to bench to patch loop end to end
  - Adopt... (A14)
  - Run the claude-code repo's maintainer automation on Foreman's own issues
  - Hold a nightly adversarial maintainer review (A12)
  - Score the test suite's real strength overnight
  - (the rest are listed under their capability)
- **Grounding: process.** Self-start rounds are T-1332 (done), friction from runs is T-1339 (captured).
- **Mark: skip** (value 2). Queue policy for the user to set, not product code.

### A34. Claude Code feature-gap tracking (7 ideas)

- **Ideas**
  - Ingest the Claude Code CHANGELOG into a feature-gap board
  - Mine feature gaps from tool-call sequences, not docs
  - Run the maintainer automation (A33)
  - Predict the next upstream feature (A14)
  - Radar for open upstream pull requests (A14)
  - Hold... (A12)
  - Oracle... (A22)
- **Grounding: partial.** `probe_claude_code` captures one task per release (`fmscout.py:53-64`). `fmeco.changelog` and `check_cc_features` read release notes (`fmdoctor.py:505`, `:545`).
- **Mark: build the changelog board (value 3, effort S, risk low).**
  - Deliver: scout parses new changelog lines into candidate capabilities and captures one task per unmatched line.
  - Done when: `python3 -m unittest plugin.tests.test_scout_changelog` shows a fixture changelog creating one capture per unmatched feature and none for matched ones.
  - Skip the tool-sequence miner (needs `claude -p` spend).

### A35. New verbs and input kinds, git workflow (33 ideas)

- **Ideas**
  - Compile machine-readable specs into conformance checks
  - Check design tokens against code
  - Generate synthetic fixture data from schemas
  - Queue the decisions from a meeting transcript
  - Add hardware-in-the-loop evidence
  - Bind physical controls to verbs
  - Hold approvals to a quiet window per device
  - Map one request over a list of inputs
  - Protect regions inside a file with inline markers
  - Answer in-source `fm:` comment markers
  - Resolve the user's merge and rebase conflicts
  - Write edits as a three-way merge against what the model read
  - Build evidence-backed deterministic twins of the official git plugins
  - Answer read-only questions by runner quorum
  - Explain which rules apply at a path
  - Open a slot workbench in the app
  - Heat-map diffs by self-consistency
  - Wild: Hold a bounty board (A12)
  - (and the remaining speculative verbs from r1..r4 capability-map)
- **Grounding: missing.** There is no `fm commit`, `fm spec check` or `fm rules` verb in `fmcli.py`. `fm pr` exists (`fmpr.py`).
- **Mark: skip all** (value 2, effort M, risk med): speculative, no user ask. If one is wanted first, the git-conflict resolver (value 3 to 4) is the strongest.

---

## Risks and surprises

- **Priority order.** Briefs should start with A9's probe test, since it may expose a live privilege gap. Then A13, A14 and A5 (one upstream-register brief), A2, A8 and A10. A16 is the largest build and should come after those.
- **`fm adopt` clash.** A13's "generic `fm adopt URL`" collides with the existing `fm adopt`, which takes in an existing repo (`fmcli.py:5494`).
- **`probe_sources` is unattended.** It refreshes pins weekly without review (`fmscout.py:133-150`). That is safe only because the index is read-only. It must not be reused once A16 runs scripts.
- **Counts.** 286 is my count of titles across the 17 files. The clusters were not re-counted line by line, so one or two borderline duplicates could be off.

## Not checked

- `plugin/tests` coverage of `fmlib` sources (no test file located).
- Whether T-1333..T-1361 changed any of the grounding since HEAD (the working tree has uncommitted edits to `fmcli.py` and `test_cli.py`).
- fmcodetui.py internals, fmserve.py, fmhooks.py hook payloads, and the website.
- The research files `claude-code-capabilities.md` and `anthropic-repos-integration.md`, which I did not open. Licence classes for the six repos come from the idea files only.

**Noticed:**
- `fm code why` is in the earlier catalogue brief (R7) but is not a subcommand. The `fm code` subcommands are `runners`, `models`, `bench` and `tui`. Worth a task or a note in T-1336's follow-up.
- `fm code runners --check` only runs `--version` (`fmcode.py:1623`), while the help text and T-1335 imply a real probe.
- `fmplugins.index()` crashes on a non-dict marketplace entry (`fmplugins.py:119-125`), a latent bug for a 166-entry official catalogue.
- `DEFAULT_SOURCES` still carries "vetted 2026-10-15" repos but lacks five of the user's six repos (`fmlib.py:482-487`).
- `fmcode.py:57-60` says codex and gemini shell commands are not confined by Foreman's guard. Worth a doc line or a test that makes the unconfined state visible in `fm code runners`.
