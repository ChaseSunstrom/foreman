# Brainstorm catalogue: brainstorm-20261102-142457 (gen-3 Mission 5, #12)

524 ideas in 46 clusters, each grounded in the code: 55 built, 1 false-premise, 289 new, 179 partial. 29 clusters marked build.

Spot checks before any build (T-2659): "fmrelproof.py:82 zip extraction is unfiltered" is false (lines 79-81 refuse
absolute and `..` names; the slate drops it). "_child_env is a denylist" is true (fmsession.py:289) but deliberate: child
sessions do the user's work with the user's environment, so an allowlist would break them; skip. "fm burden has no
per-source breakdown" is true (fmcost.burden sums injected_chars, fmcost.py:1561). "No guard timing test" is true (no
test_guard* file times g.check). "No no-progress spend stop" is true (fm run caps total spend with --max-usd only).
One idea of 525 was lost by chunk 0's recon pass (524 here).

## c01 Guard parity across tools, callers and spawn depth

Mark: **build** · value 4 · effort S · risk low — No depth cap exists, so a runaway nested spawn is a real cost and blast-radius risk.  
Slate: Set a FM_SPAWN_DEPTH env var in each Foreman child spawn and refuse a spawn at depth 2, with a test.

- [built] Check guard parity on non-Bash tool calls — near T-2370 (done): non-Bash tool-failure miss detection
- [partial] Parity-test the guard against every tool the harness exposes, subagents included — fmagents parity test (MASTER.md:233); subagent tools not enumerated
- [partial] Judge the expanded command, not the typed one — near T-2493 (done); fmguard expands scripts/substitutions, extent unverified
- [new] Make privileged fm verbs refuse lane and child callers — searched refuse lane/child callers; nothing; _NESTED env exists (fmsession.py:290)
- [partial] Cap spawn depth and debit child spend from the parent's budget — fm budget caps child spend (T-0227 done); no depth variable found
- [partial] Cap spawn depth for Foreman children — near T-0227 (done); grep spawn depth found no depth guard
- [partial] Hard-cap sub-agent depth at 1 and width at one constant — same grep: no depth cap in fm*.py
- [new] Give each sub-agent role a tool allowlist and test it — searched tool allowlist in plugin/agents; not confirmed
- [new] Wild: Monk mode, a profile with four tools and no shell — speculative profile
- [new] Make a revoke-only watchdog agent — speculative

## c02 Untrusted repos, git hardening and hidden text

Mark: **build** · value 4 · effort S · risk low — Zip extraction at fmrelproof.py:82 lacks a path filter and fm shot has no SSRF guard.  
Slate: Make fmrelproof.py:82 zip extraction reject absolute and parent-relative member names, and refuse fm shot and fm flow URLs to private addresses or file: schemes.

- [built] Audit repo-supplied agent config before it runs — near T-1263 (done); fmhooks.py:398 hashes repo hooks, MCP, allow rules
- [new] Mark a checkout untrusted by commit authorship and sandbox its proofs — searched untrusted checkout; authorship check absent
- [partial] Run every Foreman-initiated git call with a hardened config on untrusted repos — fsmonitor=false/hooksPath used in ~15 sites (fmfind.py:170, fmlib.py:561); no single wrapper
- [built] Run Foreman's own git and subprocess calls against a hostile-name repo — near T-0394 (done)
- [built] Fuzz every path-reading verb with hostile names — near T-2186 (done)
- [partial] Scan instruction files, skills, steers and pasted asks for hidden Unicode — fm doctor invisible text check (MASTER.md:440, T-0954); pasted asks and steers not covered
- [partial] Flag hidden text in everything the agent reads and writes — same doctor check covers config files only
- [partial] Flag edits to files that run without being invoked — fmguard git exec keys (fmguard.py:3812); no general autorun-file flag found
- [built] Detect diffs hidden from the reviewer — near T-0733 (done): smaller reviewer diffs; fmcli.py:5793 neutral diff
- [new] Treat what the session created or defined as untrusted when later run — searched session-created untrusted; nothing
- [built] Ship a safe extractor for every archive Foreman fetches — filter="data" at fmlanes.py:1035, fmrelproof.py:125, fmrollback.py:110; fmrelproof.py:82 zip extractall is unfiltered
- [new] Guard the browser behind `fm shot` and `fm flow` against SSRF and file reads — searched SSRF in fm*.py; nothing
- [partial] Jail `fm code`'s file tools to the worktree — fmcode.py:1025 protects git config and shell startup files; full jail not confirmed
- [new] Give `fm code` an argv-only exec tool with typed policy — searched argv exec in fmcode; not found
- [partial] Pin MCP tool descriptions at approval and alarm on change — near T-0672 (done); fmdoctor.py:2039 hashes MCP specs, not tool descriptions
- [partial] Make the generated MCP server template secure by default — fmcli.py:6919 scaffolds MCP servers; secure-by-default unverified

## c03 Bypass-mode authority and irreversible grants

Mark: **build** · value 4 · effort M · risk med — Bypass is the largest blast radius; a recoverability preflight reuses the built snapshot/restore drill.  
Slate: Make entering bypass mode (or granting an irreversible action) run a recoverability preflight that checks a fresh restore-verified snapshot exists and refuses with a Next line if not.

- [new] Shed ambient authority at bypass-session start — MASTER.md/fmcli grep: no bypass-start authority shed; guard grants exist in fmguard
- [new] Wild: Authority drift alarm — no drift alarm found in MASTER.md or fmcli help
- [new] Sound a seatbelt chime when a bypass session drifts — no bypass-drift cue found; only TUI waiting cues (T-1740)
- [partial] Run a recoverability preflight before bypass or irreversible grants — fm drill --restore and snapshots exist (T-2652); no preflight on grants
- [new] Wild: Cap irreversible grants with a monthly budget — no grant budget found in grep
- [partial] Gate bypass mode on a restore-verified backup — fm drill --restore verifies snapshots; no bypass gate found
- [partial] Let grants decay while the user is away — grants have expiry (T-2310); no away-decay found
- [partial] Keep grant expiry independent of the wall clock — T-2310 done for test deadlines only; grant expiry clock use unverified
- [partial] Make the unattended drive allowlist-shaped — fm night/fm drive budgets exist (MASTER.md); allowlist shape unverified
- [partial] Give unattended runs a stricter policy profile than interactive ones — fm night/drive exist; no separate guard profile found by grep
- [partial] Fail closed on an unknown permission mode or hook payload shape — T-0821 outward gate fails closed; unknown mode/payload handling unverified
- [new] Lock privileges to the stage rail — no stage-rail privilege lock found
- [partial] Make a Trust Gate that fails closed on unfamiliar repos and bypass mode — T-0821 gate fails closed for outward tools; no repo-familiarity gate found
- [partial] Snapshot-Before-Block Recovery — T-1339 run friction + upgrade snapshots; no per-block snapshot found
- [new] Wild: Add decoy off-switch verbs that only log — no decoy verbs; speculative

## c04 Capability retirement and lean pruning

Mark: **build** · value 4 · effort M · risk low — Unused-verb data exists but nothing acts on it; one retire step closes the loop.  
Slate: Add fm burden --retire-candidates, which lists verbs and skills unused for 60 days with their last-use date and prints the exact removal and codemod steps, changing nothing.

- [partial] Brown out unused verbs and skills for a shadow week — fm burden --by-verb lists unused verbs (fmcli.py:6861, T-0959); no brown-out
- [partial] Put removed things on a two-release deprecation clock — deprecation playbook + fm codemod (MASTER.md:173); no release clock
- [built] Find verbs that overlap — near T-2371 (done): fm which finds across shelves
- [partial] Archive a steer once its automatic check enforces it — near T-2327 (done) compiles steers to checks; no archival step
- [new] Wild: Run a "lean twin" every night with half the verbs hidden — speculative; fm burden is the measuring tool
- [partial] Wild: Stage a monthly "delete one thing" vote with the evidence attached — fm burden --by-verb unused list is the evidence; no vote
- [partial] Show a one-table "weight" page with a retire button per row — fm burden (fmcli.py:6858) reports weight; no retire action
- [new] Wild: use a weekly ejected-kit rehearsal as the lean oracle — searched eject/kit rehearsal; nothing
- [false-premise] Do less: compose verbs that already exist and add none — a design stance, not a capability
- [partial] Keep the roster of agent roles in one table — fm agents list (fmagents); roles spread across plugin/agents
- [new] Count tombstone hits before deleting the tombstone — searched tombstone in MASTER.md; not found as a counter
- [new] Score lean candidates from natural variation in the ledgers — speculative statistics; no ledger-variation scorer

## c05 Grants, bypass, irreversible-step controls

Mark: **build** · value 4 · effort M · risk med — Bypass has no lease or exposure receipt; a one-board grant view plus bypass lease are bounded, real safety gains.  
Slate: Make bypass mode expire on a lease (default hours) after which the guard reverts to ask mode, and print an exposure receipt when a bypass session starts.

- [partial] Show every live grant on one board with an expiry — fm mcp grants lists queued install grants (MASTER.md:230); no board with expiry across kinds
- [new] Fuse bypass mode so it falls back to ask mode — grep bypass in fmhooks.py/fmguard.py: bypass default set in settings (MASTER.md:314), no fuse
- [new] Say "freeze" to make the session read-only mid-flight — grep freeze: only audit diff freeze (fmcli.py:5756)
- [partial] Ask for trust on first open of an unfamiliar repo — Claude Code itself asks workspace trust; fm trust verb (fmcli.py:6372) is different
- [partial] Offer a scoped one-shot allow after a guard block — fm trust/learned approvals exist; one-shot scope unverified
- [new] Print an exposure receipt before every bypass session — grep bypass receipt: none
- [new] Expire bypass mode with a lease — fm code leases are worker leases; none for bypass
- [new] Add a cooling-off period for irreversible commands, aware of presence — grep cooling-off: none
- [partial] Convert irreversible-class blocks into snapshots — fmrollback snapshots records (MASTER.md:263); not tied to guard blocks
- [new] Take a btrfs/snapper/ZFS snapshot at bypass start and offer one-command rollback — fm rollback is records-only; no fs snapshot
- [new] Require a FIDO2 key touch for the irreversible command class — grep FIDO/webauthn: none
- [new] Mint a one-use scoped push credential per `fm ship` grant — grep ship credential: ship uses user's git creds
- [new] Hold every publication for a grant bound to the content hash — fm ship grants exist but not hash-bound; grep content hash grant
- [partial] Add a cloud-spend command class with a dollar ceiling — fm budget caps child-run spend (fmcli.py:7583); no cloud-provider command class
- [new] Add `fm breach`, a one-command incident button — grep breach: none; fm rollback/doctor partial
- [new] Add a belt-rank trust ladder (wild) — speculative gamification
- [built] Add a phone kill switch (wild) — fm code app stalled-run card with k kill (T-1761)
- [partial] Renew the standing mandate monthly — fm mandate/goal verb exists (fmcli.py:7559); renewal cadence unverified
- [new] Wild: Run guest mode on a borrowed machine — speculative

## c06 Guard path protection and bypass of the guard

Mark: **build** · value 4 · effort M · risk med — Guard is the safety core; untested subagent/escape/ReDoS/obfuscation surfaces are real gaps.  
Slate: Add guard exam cases that run an obfuscation-transform set and a pathological-regex timing check against fmguard, and fail the exam on any allowed or slow line.

- [built] Protect named paths from every agent — guard protects state/plugin folders; T-2634 heredoc args; protect list in fmguard.py
- [partial] Compile guard rules into Claude Code's native deny rules — install-user writes deny rules into settings.json (MASTER.md:314); no full compile of rules
- [new] Strip terminal escapes from untrusted strings at render — grep ANSI/\x1b in render paths: only styling output, no sanitiser found
- [new] Time guard regexes on pathological input — grep fmguard.py timing/ReDoS: no timing test seen
- [partial] Add a guard lockout breaker — guard fails closed (T-0371); no lockout/escape breaker for self-lock
- [partial] Guard non-Bash tools by effect class — T-2370 was miss detection; guard hook scope is Bash-centred, verify fmhooks.py
- [new] Prove the guard holds inside subagents, background shells and worktrees — grep fmguard.py/fmexam for subagent guard test: none
- [built] Judge what a command will run, not what it says — guard oracle runs line in bwrap sandbox (fmoracle, MASTER.md:258; fm guard --oracle fmcli.py:7059)
- [new] Import GTFOBins and LOLBAS as a generated guard exam — grep GTFOBins/LOLBAS: none; fm guard --oracle cases exist
- [new] Make loosening a guard rule cool off for 24 hours — grep guard rule cooloff: none
- [new] Warn when a guard rule is allowed by the same session that edits it — grep guard allow self-edit: none
- [new] Detect hook collisions with other plugins — T-1744 was mv guard; no hook collision detector
- [partial] Add `fm distrust <shape>` to undo a learned approval — fm trust verb exists (fmcli.py:6372); check for revoke action
- [partial] Add `fm can-i "<command>"` as a no-run guard oracle — fm guard --oracle (fmcli.py:7059); fm guard verb at 7072 may already check a line
- [new] Run an obfuscation-transform exam against the guard — fm exam/drill cover other kinds; no obfuscation transform
- [new] Differential-parse the guard against a real shell parser — fmguard has own parser; no bash -n/shlex differential seen
- [partial] Resolve realpath before protected-path rules — T-0175 variable writes; grep fmguard.py realpath to confirm symlink resolution
- [new] Give the user a prove-it-before-I-trust-it quiz on the guard — visual/UX; fm exam exists but no user quiz
- [partial] Check imports against an allowlist across all of `plugin/lib` — T-2307 import-budget tests for hook modules only
- [built] Lint hook-path modules for heavy top-level imports — T-2307 import-budget tests in test_core

## c07 Lean accounting, retirement and subtraction

Mark: **build** · value 4 · effort M · risk low — Core of #12; lean ratchet exists, so closing the loop (expiry to decision, footprint-only credit) is the real gap.  
Slate: Make each lean-ratchet row expire after N ships into a keep/retire decision recorded with its footprint delta, and credit a subtraction only if fm doctor's footprint fell.

- [partial] Record every decision not taken, with a reason — T-2281 lean ratchet records always-on rows; rejected-decision log absent
- [partial] Show how much state a safe prune would reclaim — fm prune --dry-run likely (fmcli.py:7182); reclaim size unverified
- [new] Settle deletion and docs bets by non-resurrection — fm tombstone tests exist; no non-resurrection settlement
- [new] Count a subtraction only if total footprint fell — fm doctor --plugins footprint (fmcli.py:7311); no exchange rate
- [partial] Mute steer expansion for message shapes that never yield a method — T-2625 steer-expansion exam; per-shape mute absent
- [new] Link each costly decision to the decisions it rested on — T-2397 is research provenance, not decisions
- [new] Wild: Add a lone-sceptic child who may only argue a lean claim is false — speculative
- [partial] Wild: Give each retired capability a three-line obituary and a revival test — test_tombstones.py exists; obituary/revival test unverified
- [new] Require a detach test for every capability — no detach test found
- [partial] Make growth need a recorded waiver — T-2281/T-2342 lean ratchet per ship; waiver unverified
- [new] Run a cross-vendor deletion-only review each release — fm release exists (T-2390); no deletion-only review
- [partial] Drop the Haiku first-pass cold read if it never changes an outcome — T-2471 Haiku first; outcome data via fm outcomes
- [partial] Close T-0034 and T-0035 as covered by `fm exam` and `fm outcomes` — task housekeeping; needs fm task check
- [new] Start each Mission by trying to delete the previous Mission's largest addition — process rule; no code
- [new] Draw a simplicity constraint card at the start of each Mission — process rule; no code
- [new] Wild: Run a "one-file Foreman" week where main must pass the ship gate from a single directory listing under 100 files — speculative stunt
- [partial] Fold lean into one weighed footprint score — T-2281 lean rows; fm doctor --plugins footprint
- [partial] Make every lean row expire into a decision — T-2281 done: rows recorded each ship; expiry absent
- [new] Retire by joint evidence, not one signal — fm outcomes (T-1060) single signal
- [partial] Prove a deletion by running the suite with it removed — T-0679; fm bench guard --mutate pattern
- [partial] Keep a tombstone-and-revival record for each retirement — plugin/tests/test_tombstones.py; revival record unverified
- [new] Count only footprint-reducing subtractions in the exchange rate — no exchange rate found
- [partial] Rank context injection by whether it changed an outcome — fm outcomes (T-1060) survival grading; injection ranking absent

## c08 Lean ratchet, injected context and token budget

Mark: **build** · value 4 · effort M · risk low — Lean ratchet exists at ship; per-prompt injected-token trim menu and hook-time chip are cheap grounded gaps.  
Slate: Add `fm trim` that lists each context item Foreman injects at session start and per prompt with its token size and use count from fm usage.

- [partial] Add `fm trim`, a menu of injected context with usage counts — fm usage lists skills/commands used and never used (fmcli.py:6862); no injected-context menu
- [built] Keep one footprint file that ship checks — T-2281 lean ratchet records always-on footprint per ship
- [partial] Print a lean receipt on every closed task — T-2655 drive receipt has yield per dollar; per-task receipt not
- [built] Add a Foreman overhead share to every drive receipt — T-2655 drive end-of-run receipt
- [partial] Ratchet injected tokens per session start and per prompt — T-2281 ratchets always-on footprint; per-prompt unverified
- [partial] Put a deadline on each pending-measurement lean row — T-2503 lean measures; deadline sweep idea near T-2503
- [partial] Run a lean-measurement deadline sweep — T-2503 done; sweep of overdue rows not seen
- [new] Cap the default install at 40 skills and load the rest by name — grep skills count cap: none
- [built] Load verbs on demand from a pinned local cache — fmcli.py lazy("fmx",...) loads verb modules lazily (fmcli.py:6848)
- [new] Put a verb catalog in every context pack — grep context pack verb list: fm which exists (MASTER.md:230)
- [new] Mark each lean claim with the evidence that earned it — grep lean claim evidence: none
- [built] Score each lean/safe change against a no-change twin — T-2363 exam kind lean: planted growth the gate must catch
- [new] Fail the ship gate when a fix adds a flag or env var — T-2086 is scratch-tree; grep ship flag-count gate: none
- [new] Ship a deletion-only release every fourth release — process rule; fm release has no cadence
- [new] Retire tests by their catch record — grep test catch record: none
- [built] Estimate the size of a change before filing it — Planning and decomposition S/M/L sizing (T-0691)
- [partial] Flag every number that is recorded but never decides — T-2496 ship chance bet; no generic audit
- [partial] Do less: make "lean" one sentence in `fm doctor` and nothing else — fm doctor exists (fmcli.py:7320); lean row unverified
- [new] Wild: Publish a lean ledger on the Genesis site — visual/publication; fm genesis live exists
- [new] Price the cold-read tax per filed item — grep cold-read tax: none; fm cost by task
- [partial] Show hook time spent this session on the status line — statusline budget <100ms noted (MASTER.md:91); no hook time total

## c09 Process confinement and host hardening

Mark: **build** · value 4 · effort M · risk med — Landlock module already exists; wrapping hooks plus rlimits shrinks blast radius cheaply.  
Slate: Apply fmlandlock's write confinement and a setrlimit CPU/memory/stdin cap to each Foreman hook entry point before it reads its input.

- [partial] Gate the Desktop publish (T-0352) on a hardening checklist — T-2344 surfaces work done; no publish checklist gate found
- [new] Flag precious paths that no backup covers — T-2175 is genesis coverage, unrelated; no backup coverage check
- [partial] Diff outbound hosts per release — T-0672 guard/safety milestone; per-release host diff unverified
- [new] Ratchet the list of user-owned paths Foreman reads — no read-path ratchet found
- [partial] Confine fm's own hook and verb processes with Landlock — fmlandlock.py confines fm code workers (T-1607); hooks not confined
- [new] Check that `fm`, `git` and `python3` resolve to trusted paths — T-0180 is grant scope; no PATH resolution check
- [new] Warn when the host CLI is older than its published security fixes — no host version advisory check found
- [new] Run every hook under rlimits and a bounded stdin read — grep setrlimit in plugin/lib: none for hooks
- [partial] Confine hooks with Landlock before they read input — fmlandlock.py exists for workers; hooks not wired
- [partial] Funnel every state write through one path-checked helper — T-0821 fixes; single helper coverage unverified
- [new] Score installed timer units with `systemd-analyze security` — grep systemd-analyze: 0 hits
- [new] Wild: ship hooks with proof-carrying effect certificates — speculative
- [new] Run agent sessions as a separate unix user — no separate-user support found
- [partial] Require a change certificate for protected-core edits — fmselfgate.py guards protected core; certificate absent
- [partial] Draw approval prompts on `/dev/tty` only — T-0009 plain-chat approvals; tty-only unverified
- [partial] Secure the upgrade snapshots at rest — fm drill --restore (T-2652) restores; encryption/permissions unverified
- [partial] Resolve `fm` and every hook command by absolute path — hooks install paths unverified; T-0175 unrelated

## c10 Secrets, outbound text and untrusted input

Mark: **build** · value 4 · effort M · risk med — Secrets and outbound leak paths are core to safe; redacted-read and outbound scan have partial coverage.  
Slate: Scan the text of every fm ship/PR/issue body for credential patterns with fmsecrets before it leaves the machine and refuse with the match named.

- [partial] Block reads of secret-bearing files and give a redacted view — fm secrets scans tree/config (fmcli.py:7050); guard credential-name refusal (T-2665); no redacted view
- [partial] Scan allowed outbound text for smuggled secrets — grep fmsecrets/outbound in MASTER.md Guard section; verify ship/PR text scan
- [built] Flag secrets in command arguments — guard credential-name/arg refusal (T-2665, T-2493 near); fmguard.py
- [partial] Scrub every child's environment to an allowlist — T-0361 AppImage children env; grep fmserve env allowlist for headless children
- [new] Stop Foreman verbs being triggered by untrusted text — grep fmhooks.py prompt injection into fm verbs: none
- [new] Accept a pasted verdict from another agent only as a claim to re-run — grep verdict pasted: none; fm prove re-runs commands generally
- [new] Fence security-testing tasks to an authorized scope file — grep authorized scope: none
- [partial] Keep lessons bound to their repo by default — verify lessons store scope in fmcli lessons verb
- [partial] Add `fm forget <repo|path|term>` — fm forget flags only on some verbs (fmcli.py:7024,7368,7836); no general forget
- [new] Scrub and cap child scratch directories — grep scratch dir cap: none
- [partial] Check state isolation on a shared machine — state marker in world-writable dir ignored (MASTER.md:441)

## c11 Untrusted input, prompt injection and package trust

Mark: **build** · value 4 · effort M · risk low — Slopsquatting check on install/add commands is a concrete new safe gap.  
Slate: Make the guard ask before pip/npm install of a package name that does not exist on the registry or was first published in the last 30 days.

- [new] Derive guard rules from files the user already wrote (ssh config, git remotes, branch protection) — no ssh config or remotes ingestion in fmguard grep
- [new] Diff the guard against the user's own settings.json permission rules — no settings.json permission comparison found
- [built] Unwrap interpreter one-liners and wrapper commands in the guard — fmguard wrapper/NAME=val expansion (T-0175, T-2665 sys.path literals)
- [new] Catch hallucinated package names (slopsquatting) — grep slopsquat: 0 hits in plugin/
- [partial] Lint prompt templates for unfenced untrusted fields — outside-text labelling exists (hooks notes); no template lint
- [partial] Refuse lane merges that carry dangerous file kinds — T-1818 requires review for CI/hook/install diffs; lane merge refusal unverified
- [built] Probe each model for injection susceptibility — fm code runners --probe (T-1403)
- [partial] Start unseen model IDs on probation — T-1395 runner flag lint/grade; no probation state
- [partial] Model-Aware Guard Probation — T-1395 grade; no probation on guard strictness
- [new] Import OWASP LLM/agentic and MITRE ATLAS technique lists as threat rows — grep OWASP/ATLAS in MASTER.md: none
- [partial] Secret-Aware Argument Scrubbing — T-1302 fm code app exports scrub secrets; process args scrub unverified

## c12 Context lean: reads, status deltas and child context

Mark: **build** · value 3 · effort S · risk low — Repeat-status output is paid every turn; a per-skill and hook context-weight line is cheap from burden data.  
Slate: Add a per-item context-token column (skills, agents, hook output) to fm burden, sorted by size.

- [partial] Cut each child's context to what changed its answer — near T-2358 (done) lean ratchet; no ablation of child context
- [partial] Dedupe repeated file reads inside a session — near T-2109 (done) only skips friction-detector events; reads not deduped
- [new] Print only the delta on repeat calls to status verbs — near T-1260 is bench noise; no repeat-call delta found
- [partial] Add a context-weight line for agents, skills and hooks, with dormant-by-default — fm burden bookkeeping cost (fmcli.py:6858); per-item context weight not confirmed
- [new] Cap the lessons store with recall-based eviction — searched lessons eviction; none found
- [new] Store lessons as typed facts, not prose — speculative schema change
- [new] Watch the host's release notes for features it now does natively — fm doctor model-name check only (T-2643)
- [built] Answer "can Foreman do X?" from MASTER.md without a model — near T-2643 (done); fm which across shelves (T-2371)

## c13 Install drift and code-generation pinning

Mark: **build** · value 3 · effort S · risk low — Installed-versus-source drift is a real safety gap; the others are speculative or risky.  
Slate: Make fm doctor compare a hash of the installed plugin tree against the source checkout and WARN with the changed paths when they differ.

- [partial] Probe the installed copy against the source on a timer and flag drift — fm doctor checks hashes (fmdoctor.py:2039,2114); fm docs does doc drift; no timer
- [new] Pin the drive to one code generation and re-exec at task boundaries — searched re-exec/code generation in MASTER.md; nothing
- [new] Launch hooks with `python -I -S` and a frozen import set — searched python -I in fmhooks/hook launcher; not found. Risk: -S drops site-packages
- [new] Precompile bytecode into a writable cache prefix at install — only PYTHONDONTWRITEBYTECODE in fmmutate; no install-time precompile
- [new] Build the skill trigger index at install time — searched trigger index; nothing
- [new] Install by sparse checkout so unused skills never land on disk — searched sparse; none. Conflicts with plugin install model
- [partial] Offer a one-step revert after a config change followed by a red doctor — fm rollback exists (fmrollback.py:110); no doctor-triggered offer

## c14 Reliability, locks, doctor and degraded state

Mark: **build** · value 3 · effort S · risk low — A fail-open/closed declaration per hook is cheap and makes safe behaviour auditable.  
Slate: Add a fail-open or fail-closed field to each hook registration and a test that every hook declares one and the guard hooks are closed.

- [partial] Extend the flake registry to every nondeterministic check — T-0673 flake registry exists; extension unverified
- [new] Back off with jitter and a breaker on API overload — no jitter in plugin/lib; cards only
- [partial] Isolate every `fm doctor` check — fmdoctor.py exists; per-check isolation unverified
- [new] Explain who holds a lock and for how long — no lock-holder report found
- [new] Show a single persistent "running degraded" line — none
- [new] Record the nondeterminism of every hook call so any failure replays bit-exact (wild) — fmreplay replays inputs only
- [new] Record lock-wait time per state lock — none
- [partial] Pair each hook with a fail-open or fail-closed declaration — gates fail closed (T-0821); declaration table absent

## c15 Ship, CI and git hygiene

Mark: **build** · value 3 · effort S · risk low — Extend ship --dry-run with remote and branch blast radius; revert drafting is optional.  
Slate: Make fm ship --dry-run print the target remote, branch, commit count and files touched, and refuse when the push destination differs from the recorded grant.

- [partial] Draft a local revert when main goes red after a Foreman push — fm ship --watch / ci-watch (fmcli.py:7041); revert draft absent
- [new] Rehearse every ship push against a local bare remote — none
- [new] Stamp commits with a Guarded-by trailer and verify it later — T-1663 is re-verify queue; no trailer
- [built] Post-push watch: follow CI for the pushed sha and file a revert-or-fix task — fm ship --watch (fmcli.py:7041, T-1946)
- [new] Fast-forward single-commit tasks, drop the Merge commits — history shows Merge commits; none
- [partial] Batch Genesis site publishes into one daily commit — T-2326 publish refresh exists
- [partial] Run a dry-run `fm ship` that prints the push and its blast radius first — fm ship --dry-run prints the plan (fmcli.py:7029)
- [built] Pin the push destination to the grant — T-2390 fm release VERSION
- [partial] Run `fm lane --plan` as a dry-run that merges in a scratch worktree — fmcli.py:6477 --dry-run partition only

## c16 State footprint and config

Mark: **build** · value 3 · effort S · risk low — Unattended commits under the user's author hide who acted; the other items are speculative.  
Slate: Make unattended Foreman commits (drive, lanes, drafts) carry a distinct git author name so git log separates them from the user's.

- [new] Add `fm config --diff`, showing only non-default values — searched config --diff; not found
- [new] Ratchet the count of state files; a new one must merge or retire another — searched state file count; fm tidy exists, no ratchet
- [new] Prove state is readable with `cat` and `grep` alone — unchecked; state is JSON and JSONL files
- [new] Wild: Lazy state, with nothing created until the first write that matters — unchecked; state/ fallback logic at MASTER.md:441
- [partial] Wild: Keep a tripwire file in the state directory — fm doctor has tripwires (MASTER.md:560); no state-dir canary
- [partial] Add a per-session vanilla switch (`fm off --session`) — near T-2055 (done); fm off --now at fmcli.py:7207
- [partial] Include the guard and installed hooks in `fm drill --restore` — fm drill --restore at fmcli.py:7345; scope unverified
- [partial] Declare each agent adapter as data, behind one conformance fake — fmagents parity test exists
- [new] Give every multi-agent flow a tested single-agent path — searched; fmagents list only
- [built] Freeze the safety core by path — near T-2598 (done)
- [partial] Keep a threat register where every row names its test — near T-0701; guard corpus and mutation exist, no register file
- [new] Wild: Agents pay rent — speculative
- [new] Wild: Run a reputation auction among sub-agents — speculative
- [new] Make unattended commits carry their own git author — searched unattended author; nothing
- [partial] Wild: Quiz a cold child on picking the verb — fm which and exams exist; no cold-child quiz
- [new] Round-trip every mutating verb through apply and undo — fm tidy has apply; no generic undo
- [new] Random-walk the whole CLI against a state model — fmcli.py is huge; no model-based test found
- [built] Add a restraint exam kind — near T-2608 (done)
- [new] Wild: Run `fm doctor --as-of DATE` over the ledger — fm graph has --as-of only
- [new] Offer a one-step revert ...: Shadow-adopt step before a changed agent prompt goes live (wild) — Add a shadow-adopt step before a changed agent prompt goes live (wild); nothing found

## c17 Web UI and pane

Mark: **build** · value 3 · effort S · risk low — A zero-external-request check is cheap and guards the local-only promise.  
Slate: Add a ship-gate test that fails when any web UI asset contains an http(s):// URL to a non-localhost origin.

- [built] Poll the pane on ledger change, not on a timer — near T-1137 (done): stage_change ledger event
- [built] Stream ledger changes to the web UI — near T-1156 (done)
- [built] Show a live "waiting on" strip — near T-2062 (done)
- [new] Show the exact `fm` command beside every pane row and button — visual; not checked in fmweb
- [built] Show a Posture page in the web UI — near T-2626 (done)
- [partial] Fail the ship gate if the web UI fetches a remote origin — fm outbound logs requests; no ship-gate check on web assets
- [new] Render the web UI from `--json` only — architecture change, unchecked
- [partial] Ratchet the web UI to zero build and zero external requests — same as the remote-origin gate
- [new] Fit every web view in 80×24 without scrolling — visual only
- [new] Make the UI propose and the CLI dispose — design principle
- [new] Show agents' trust ranks in the UI as a roster strip — visual
- [new] Give each agent a résumé in the Agents graph (wild) — visual
- [new] Add an x-ray key that highlights every Foreman-injected line in the transcript (wild) — visual
- [built] Map agent-written lines nobody has read — near T-0701 (done); fm graph --cold (fmcli.py:6683)
- [built] Give each sub-agent a one-page dossier — near T-0689 (done)

## c18 Web UI, state-dir and publishing surface audits

Mark: **build** · value 3 · effort S · risk low — Hostile-string XSS test and state-dir perms check are small and guard real exposure.  
Slate: Add an fm doctor check that flags state-dir files not owned by the user or world-writable and symlinks escaping state/, and a test rendering hostile ledger strings in the web UI.

- [new] Check the web UI for XSS and CSP against hostile ledger strings — grep CSP/escape in fmweb/ui: verify; no hostile-string test found
- [partial] Audit state-dir permissions and symlink safety — world-writable marker ignored (MASTER.md:441); no perms/symlink audit in fm doctor
- [new] Ship a signed patch manifest for the foreman-ui mod — grep patch manifest signed: none

## c19 Cost runaway, performance and parallelism

Mark: **build** · value 3 · effort M · risk low — A no-progress spend stop on the drive protects cost directly with existing budget plumbing.  
Slate: Make the unattended drive stop and name why when it has spent a set dollar amount with no task closed, using fm budget's spend counters.

- [partial] Stop a drive burning money without progress — fm contract and fm budget cap time/spend (fmcli.py:7583); no no-progress stop
- [new] Share one prompt-cache prefix across a brainstorm fan-out — grep cache prefix: none
- [new] Balance test shards by recorded durations across lanes — grep shard durations: none
- [new] Admit lanes by machine pressure, not a fixed count — grep lane count / loadavg in fmlanes.py
- [new] Flag serial tool calls that could have run in parallel — grep parallel tool calls: none
- [new] Give web UI views a render budget at 10k tasks — no perf budget found
- [new] Cap git calls per verb and cache by index mtime — grep git call counter: none
- [partial] Wild: Give every verb a `--deadline` that degrades to a labelled partial answer — deadline exists in ablate/bisect (fmcli.py:1237,2314); not universal
- [new] Wild: Report a "battery tax" for Foreman's idle wakeups — speculative
- [new] Wild: Precompute the next likely proof while the model is still typing — speculative
- [built] Print the end-of-run receipt on every exit path, from one renderer — T-2655 drive receipt
- [partial] Check that every printed "Next:" command parses and resolves — T-2653 prints Next: on nonzero exits; parse check not seen

## c20 Footprint ledger, install and uninstall

Mark: **build** · value 3 · effort M · risk low — A recorded footprint baseline feeds every lean ratchet and uninstall check.  
Slate: Record a footprint ledger (files, state bytes, hooks, timers) at install and ship and have fm doctor fail when uninstall leaves anything not in the ledger.

- [new] Tree-shake the install from field coverage, with lazy restore — none
- [partial] Wild: Make Foreman uninstall itself in a sandbox every release — fm demo smoke test (T-0870); uninstall rehearsal unverified
- [partial] Ship a Footprint Ledger that install, uninstall and ship all check — fm doctor --plugins footprint (fmcli.py:7311); no ledger

## c21 Footprint, install manifest and uninstall proof

Mark: **build** · value 3 · effort M · risk low — Install manifest exists; a single footprint verb that diffs it against disk and proves uninstall is the real gap.  
Slate: Add `fm footprint` that diffs state/install-manifest.json against what is on disk (settings, rules dirs, state) and fails if uninstall would leave anything unlisted.

- [partial] Print a footprint of everything Foreman put on this machine — state/install-manifest.json lists outside-repo changes (MASTER.md:298); no single footprint verb; fm doctor --plugins
- [partial] Diff what a session changed outside the repo — install-manifest covers install only; fm rollback snapshots records (MASTER.md:263); no per-session outside-repo diff
- [partial] Prove the uninstall leaves nothing behind — uninstall reads manifest (MASTER.md:298); T-0851 cleaned dirs; no leave-nothing proof/exam
- [built] Write an install manifest and uninstall from it — state/install-manifest.json, used by uninstall (MASTER.md:298)
- [partial] Prove the zero-config install is safe — fm doctor and install checks exist; no safe-by-default proof; grep install-manifest
- [new] Safe-by-default install profile with no unattended outward effect — grep fmcli.py help= for profile/unattended found no install profile switch
- [new] Audit and bound Foreman's footprint in the user's repo — grep MASTER.md/fmcli.py footprint: only plugin footprint in doctor (fmcli.py:7311)
- [built] Verify the install works with a read-only plugin directory — state falls back to XDG when ~/.claude read-only (MASTER.md:441)
- [new] Run the owner's first-ever install in a fresh container nightly — grep fmcli.py/MASTER.md container nightly: nothing; fm night exists for other jobs
- [new] Measure install-to-first-value — grep install-to-first / first-value in plugin/lib: no metric
- [partial] Swap installs atomically and pin running sessions — setup-plugins.sh refuses a real run inside a session (T-0039); no atomic swap/pin
- [new] Take a persistence census at every session close — grep persistence census / session close hooks: none
- [new] Wild: "What runs on your machine" one-pager — no such doc found in MASTER.md; docs only
- [partial] Budget the repo's weight: bytes, files and largest blobs — supply check flags a plugin file over 4 MB (T-1446); no per-repo budget report
- [new] Show the repo as a weight treemap by bytes, blast radius and last-used date — visual; fm usage lists never-used files (fmcost.py:1476) but no treemap

## c22 Guard rule measurement and corpus health

Mark: **build** · value 3 · effort M · risk low — Mutation and labelled corpus exist; pricing blocks by loss avoided adds the missing lean/safe signal.  
Slate: Add a one-line cost estimate to each guard refusal in fm bench guard output (what the blocked command would have deleted or sent) using the labelled corpus.

- [new] Price each guard block by what it would have lost — no block-cost field found; fm bench guard exists
- [partial] Add a one-key "was that block right?" label — guard corpus labels exist (T-1291); no in-the-moment label key
- [partial] Query the guard as of a past date — fmreplay.verdicts replays current rules; no as-of-date query
- [new] Test block messages for comprehension, not only a Next: line — Next: line lint exists (T-1334); no comprehension test
- [built] Mutation-census the guard's rules — fm bench guard --mutate (fmcli.py:7416)
- [built] Label guard cases by running them — T-1291 guard corpus plus fmreplay.verdicts
- [partial] Prove guard invariants with a solver — fm prove exists (T-2387 data proof); no solver on guard rules
- [new] Wild: three blind guard implementations vote in shadow — speculative; no shadow guard found
- [new] Wild: preview a command's effects with a symbolic shell — speculative; no symbolic shell
- [partial] Rule Health Dashboard (lint + mutation + shadow) — mutate bench and guard lint exist; no combined dashboard
- [new] Guard Exam Generator from Binaries (wild) — fm dojo uses labelled corpus; no binary-derived generator
- [partial] Parse-Expand-Judge Pipeline — fmguard parses and expands wrappers; pipeline naming only
- [built] Guard Parity Across Surfaces — T-0442 guard parity across harnesses
- [new] Guard Effect Ledger (allowed-then-undone) — no allowed-then-undone ledger found
- [new] Wild: Tune guard block wording by how often the model routes around it — no route-around metric found
- [new] Guard Pack Hot-Swap by Context — no context-keyed rule packs found
- [partial] Guard Self-Edit Tripwire — fmselfgate.py and T-1818 protect hook configs; tripwire named after T-2663
- [new] Wild: Dual-Interpreter Guard Vote — speculative; single interpreter
- [new] Run the guard under two Python versions and block when they disagree (wild) — speculative
- [new] Wild: estimate the guard's unseen bypasses by capture–recapture — speculative statistics

## c23 Guard self-testing and rule hygiene

Mark: **build** · value 3 · effort M · risk low — The guard is the safety core; a rule-shadow lint is cheap and the mutation harness exists.  
Slate: Add fm bench guard --lint, which reports guard rules that no corpus case reaches first or that another rule fully shadows.

- [built] Plant backdoors to test the self-change reviewer — near T-2363 (done): lean exam kind; fm bench seed-review (fmcli.py:7405)
- [partial] Lint the guard rule set for shadowed, unreachable and contradictory rules — fm bench guard --mutate finds untested rules (MASTER.md:547); no shadow lint
- [built] Wild: drill the guard with an approve-everything stand-in for the user — near T-1063 (done); fm drill faults
- [new] Wild: keep the guard small by making the red-team lane minimise its own fix — speculative
- [new] Run a janitor and a defender as an adversarial pair — speculative
- [new] Wild: Mine installed binaries' man pages for destructive flags and diff them against guard coverage — searched man-page mining; nothing (fmreplay covers commands run)
- [new] Run a told-versus-untold A/B on guard awareness — searched A/B guard awareness; not found; costs model runs
- [partial] Mine git reflog and the trash for allowed commands the user undid — fm replay (fmcli.py:7053) uses session logs, not reflog

## c24 Ledger integrity and crash tolerance

Mark: **build** · value 3 · effort M · risk low — Torn-tail and swallowed-exception proofs harden recorded state, which safe depends on.  
Slate: Add a drill fault that kills each ledger writer mid-write and asserts every reader (fm fsck, verify-ledger) reports a torn tail instead of crashing.

- [partial] Anchor the ledger tail outside the state dir — fm verify-ledger hash chain and finish-receipt head (MASTER.md:200); no external anchor
- [new] Bracket every hook with start and end records — grep hook start/end ledger: none
- [partial] Surface accepted ledger damage until it is re-anchored — T-2664 verify-ledger --accept-damage (fmcli.py:6768); persistent surfacing unverified
- [new] Declare lock order and assert it under test — grep lock order: none
- [new] Wild: Keep a write-set manifest per verb — speculative
- [new] Wild: Tag every written file with its writer in an xattr — speculative
- [new] Wild: Make each unattended capability earn a reliability deposit — speculative
- [new] Detect swallowed exceptions with an AST census — grep except: pass census: none
- [partial] Fail-closed census of swallowed exceptions in hooks — T-0371 guard fails closed; no census
- [new] Scan writers for swallowed errors and list the ledgers each can lose — grep ledger writers audit: none
- [partial] Make every ledger writer torn-tail tolerant and prove it by killing at each write — fm fsck flags torn journals (fmcli.py:7336); no kill-at-each-write proof
- [new] Seal the ledgers at the OS level — grep chattr: none
- [partial] Hold a canary-reader drill each week — fm drill plants faults (fmcli.py:7340)
- [partial] Make each drill fault declare which reader should report first — T-2648 drill fault; declare-first not seen
- [partial] Show a "last green" restore receipt in fm doctor — T-2365 doctor self-fix line; fm rollback (fmcli.py:7313)
- [partial] Treat "could not run" as a third result in every gate — T-0280 bench family only
- [new] Make ledger readers incremental with a verified-up-to cursor — verify-ledger walks whole chain

## c25 Memory quarantine and hostile-source unwinding

Mark: **build** · value 3 · effort M · risk med — Lib unwind exists; extending it to memory writes closes a real taint path.  
Slate: Mark memory and lesson writes made in a session that ingested outside text as quarantined until the user confirms them.

- [new] Quarantine memory writes made after untrusted ingestion — no post-ingestion write quarantine found
- [new] Flag steers the user's recent words quietly contradict — no steer-contradiction check found
- [partial] Unwind everything descended from a hostile source — fm lib re-index of hostile source (T-1396/T-1415); descendants unwind incomplete

## c26 Quota, cost and shedding

Mark: **build** · value 3 · effort M · risk low — Quota pressure shedding is real lean value; one pre-registered order covers three ideas.  
Slate: Add a shed order in config that fm night and fm drive follow in sequence when quota pressure is detected, logging each shed step.

- [new] Report yield per quota window as well as per dollar — cost reports per dollar; no window yield
- [new] Pre-register and rehearse a shedding order for quota pressure — none
- [new] Wild: Forecast the date the footprint hits a user-set ceiling — none
- [new] Shed in a pre-registered order under quota pressure — same as above, none
- [new] Lean twin that runs on the free arms — none
- [partial] Fall back along a ranked model chain, with a daily pin probe feeding it — runner probes exist (T-1403); chain absent

## c27 Sandbox and environment isolation

Mark: **build** · value 3 · effort M · risk med — Children inherit most of the environment by denylist; an allowlist reduces secret exposure.  
Slate: Switch fmsession._child_env and fmideas._child_env from a nested-variable denylist to an allowlist of PATH, HOME, locale and Foreman variables, with a test that a planted secret variable is dropped.

- [partial] Probe which sandbox primitives work on this host and pick the strongest — bwrap oracle (fmoracle, MASTER.md:258); no probe-and-pick
- [partial] Run children and provers with an allowlisted environment — near T-2394 (done); _child_env is a denylist (fmsession.py:289-290)
- [new] Run lanes under a `systemd-run --user` sandbox and print its exposure score — fmguard.py:5306 only blocks systemd-run; no lane sandbox
- [new] Wild: run self-changes under a time-shifted, network-off sandbox — bwrap exists for the oracle only
- [new] Wild: run the unattended drive in a disposable clone and receive patches by mailbox — lanes use worktrees; no mailbox
- [new] Give lanes an outbox remote instead of a push regex — searched outbox; nothing
- [new] Run learned fixers and rules in a WASM sandbox — speculative; no WASM runtime
- [new] Reuse the test suite under strace as an effect-manifest check — searched strace; nothing
- [new] Declare an effect class in each skill's frontmatter — searched effect class; nothing
- [new] Wild: run self-changes under hostile conditions: Run a hostile-lane drill that tries to exceed its lane's declared reach (wild) — fm drill faults exist; no reach-exceeding fault found

## c28 Static lean analysis: dead code, duplication, dependencies

Mark: **build** · value 3 · effort M · risk low — Runtime lesions exist but no zero-token static dead-code pass; one cheap AST census is worthwhile.  
Slate: Add an fm check lean step that runs a stdlib-ast pass over plugin/lib listing functions defined but never referenced, and files each as a removal candidate.

- [new] Add a static security lint pass over Foreman's own Python — grep bandit/ast lint in plugin/tests: none
- [partial] Lint workflows and shell: pinned actions, least-privilege tokens, shellcheck — T-1245 pages workflow read-only token; no general lint
- [new] Inventory the node and Desktop dependency tree with an offline advisory check — grep advisory/npm audit: none
- [new] Tag every module with its blast radius and budget the high-blast lines — no blast tag; lean measures code/test lines per module (T-2503)
- [new] Flag import cycles and layer violations with a layering file — grep import cycle in plugin/lib: none
- [new] Detect dead Python statically and file removal tasks — fm usage covers runtime never-used (fmcost.py:1476); no static pass
- [new] Detect near-duplicate source functions across `plugin/lib` — grep duplicate functions: none
- [new] Draft a 3-line stdlib replacement for each dependency — plugin is stdlib Python; few deps; speculative
- [new] Use off-the-shelf dead-code finders as a zero-token lean pass — grep vulture: none
- [partial] Find near-duplicate skill files by content similarity — T-1834 reports unused playbooks; no content similarity
- [partial] Move candidate-dead code to an attic before deleting it — fm evolve --drop lesions a file (fmcost.py:1317); no attic
- [partial] Delta-debug the product to find what's safe to delete — fm evolve lesions + fm ablate (fmcli.py:1395); not delta-debugging
- [partial] Compute the kernel by greedy removal — fm evolve --drop lesions one file at a time (fmcost.py:1317)
- [partial] Turn unused verbs into a pre-proven deletion patch — fm usage names never-used verbs (fmcli.py:6862); no patch
- [new] Plant a dead-weight canary verb (wild) — speculative
- [new] Hold a nightly code-golf match against each verb (wild) — speculative
- [partial] Run a mass-extinction rehearsal in a scratch home (wild) — fm drill plants faults in scratch home (fmcli.py:7340); not deletions
- [partial] Wild: Nightly deletion race on the costliest 20% of code — fm evolve lesions exist; no nightly race
- [new] Wild: a minimiser child with an oracle — fm oracle is spec-only (T-0226); no minimiser
- [partial] Wild: random weekly disable of one verb or hook in the drive's own lanes — fm evolve lesion is the manual form
- [new] Lean lockfile reviewed like a dependency lock — grep lean lockfile: T-2281 footprint file is nearest
- [new] Pay-down ledger for additions — grep pay-down: none; T-2363 twin exam is nearby
- [new] Shell-equivalence audit for each verb — fm complete lists verbs only
- [new] Publish a SECURITY.md and a private-report path, scored against OpenSSF Scorecard — grep SECURITY.md repo root: check; docs only

## c29 Verb contract and CLI consistency

Mark: **build** · value 3 · effort M · risk low — Effect class in help is lean for the model's context and also a safety cue.  
Slate: Add an effect-class tag (read, write-state, outward) to every verb's argparse help in fmcli.py with a test that fails when a verb lacks one.

- [new] Audit every verb's help promise against its exit code — no help-vs-exit audit; T-1334 only covers Next lines
- [new] Build a flag-parity matrix across sibling verbs — fmcli.py help strings only; no matrix
- [new] Add `--fail-if EXPR` to every number-printing reader — grep --fail-if in fmcli.py: 0
- [partial] Put the Next command in `--json` error output — Next: line in text errors (T-1334); json errors unverified
- [partial] Run every verb with a closed stdout, a SIGPIPE and a full disk — T-0825 covers read-only verbs on closed stdout
- [new] Test that every receipt field appears on every surface — no receipt-field parity test
- [new] Generate a default web view from any verb's `--json` schema — speculative; no schema
- [new] Wild: mine the user's own words for verbs that don't exist — no unknown-verb mining found
- [new] Print the effect class in every verb's help line — fmcli help strings lack effect class
- [new] Run a pipe-flood and slow-reader fake agent — no slow-reader test found
- [partial] Lint that every raised exception maps to an exit code and a Next line — T-1334 Next-line ratchet for fm code only
- [new] Turn verbs under 40 lines into rows of a recipe table — fmcli.py is argparse per verb; no recipe table
- [built] Hide every verb that has no session path from default `fm help` — T-2186 wired verbs to a session path

## c30 Usage telemetry and tracking

Mark: **skip** · value 2 · effort S · risk low — Small bookkeeping; no clear lean or safety payoff.

- [partial] Tag verb use by caller, so the usage census sees only hands that count — fm burden --by-verb (fmcli.py:6861) counts session calls; no caller tag
- [new] Log whether the user ran the printed `Next:` command — searched Next: follow-through; nothing
- [new] Count which pane tabs and web views the user opens, then fold the untouched ones — no pane view telemetry found
- [new] Label each brainstorm-accepted ask in the pack as slate-origin, not user-origin — fmideas.py is the brainstorm module; no origin label checked
- [new] Turn "dropped with a noted remainder" into a tracked S task or an expiring note — searched noted remainder; nothing
- [built] Record a safety-wins tiebreak as a standing decision — near T-2403 (done)

## c31 Brainstorm and steer hygiene

Mark: **skip** · value 2 · effort M · risk low — Process polish not tied to lean or safe outcomes.

- [new] Compress "ideas so far" into a clustered digest with saturation counts — brainstorm skill; no digest compress found
- [partial] Require every "already built" drop to cite a command run — T-2659 grounding step asks MASTER.md first
- [new] Classify each user ask by blind-spot class and chart recurrence — grep blind-spot class: none
- [built] Auto-run the re-grounding pass before a slate reaches the user — T-2659 brainstorm skill grounding step
- [new] Wild: a tool-less child predicts the user's next ten asks from the README and recent diffs, then is scored — fm oracle is spec-only
- [partial] Wild: a child writes the DONE-WHEN from the title alone, and the diff to the real one measures ambiguity — fm oracle finds ambiguities from spec (fmcli.py:7643)
- [new] Wild: an anti-pack of the last 30 dropped ideas, each with its drop reason, handed to every brainstormer — grep anti-pack: none
- [new] Detect two steers that conflict, and say which one wins — steer ledger exists (fmcli.py:4290); no conflict detect

## c32 Dead-man and external liveness

Mark: **skip** · value 2 · effort M · risk med — Speculative; needs off-box infrastructure.

- [partial] Wild: Pull-the-plug day for the drive — fm drill (fmcli.py:7343) plants faults and --restore; no power-cut day
- [new] Wild: Dead-man's switch that tells the user the tower stopped — searched dead-man/heartbeat in MASTER.md; none (T-2664 covers crash-cut ledger lines only)
- [new] Wild: Give Foreman a dead-man's twin on another machine — same search; also outbound-only, speculative
- [new] Tie pane motion to a real heartbeat — visual; no heartbeat source found for fm watch

## c33 Hook and verb crash handling

Mark: **skip** · value 2 · effort M · risk low — Resilience polish; no evidence of a crash class it fixes, and the near item is done.

- [new] Add a hook crash card with fail-open or fail-closed declared per hook — grep fail-open/fail_open in MASTER.md and fmhooks: no per-hook declaration found (not read in depth)
- [partial] Quarantine a verb that crashes repeatedly — near T-1405 (done) crash hygiene; fmcli.py:7324 quarantines git objects only; no per-verb quarantine found
- [new] Wild: Ship a misbehaving fake host for every child-spawning test — searched fake host/misbehaving in MASTER.md; nothing matched
- [new] Wild: a hostile-slow host simulator — same search as fake host; nothing; only timeouts in fmlong/fmbench
- [partial] Fall back along a ranked model chain when a pinned ID stops answering — near T-2643: fm doctor checks model names daily; no runtime fallback chain found
- [new] Render the web UI from a last-good snapshot with a visible stale banner — searched stale snapshot in MASTER.md; only fm watch/pane sources found

## c34 Hook and verb latency

Mark: **skip** · value 2 · effort M · risk med — No measured latency problem cited; the gate and bench are already ratcheted.

- [partial] Benchmark hooks against recorded real payloads — near T-1222 (done) Benchmarks page; fm bench and T-2358 hook p95 ratchet
- [new] Wild: Compile the guard to a native binary that hooks prefer — speculative; second implementation to keep in step
- [new] Show a header within 100 ms for slow verbs — searched header latency; nothing
- [new] Run doctor checks in parallel and print a timing table — searched doctor parallel/timing; not found
- [built] Count doctor checks run against checks registered — near T-2657 (done)
- [new] Memoize every pure verb by input tree hash — speculative; cache invalidation risk
- [new] Run the ship gate as a dependency graph with a critical-path report — fm ship gates run in sequence; no DAG found
- [new] Wild: let a content-addressed memo follow the user across their machines — speculative
- [built] Ratchet the bench threshold from passing runs — near T-2651 (done): fm task evidence --bench CMD --under MS
- [built] Run a shrink pass on every diff at ship — near T-2086 (done); fm ship scratch-tree
- [new] Wild: Complexity advocate, a child that reads each diff and scores new nouns — costs a model call per ship; speculative

## c35 Lane scheduling, spawn cost and merge safety

Mark: **skip** · value 2 · effort M · risk med — Most are built or speculative; hash-around-lane is the one safety item and unproven.

- [new] Keep a warm pool of lane worktrees — fmlanes.py creates worktrees on demand; no pool
- [new] Wild: pre-warm lanes from queue prediction — speculative
- [new] Hedge straggler lanes — duplicates spend; against lean
- [new] Send non-urgent model children through a batch tier — searched batch tier; fm batch (fmcli.py:7544) batches tasks, not API tier
- [partial] Choose reasoning effort per step, separately from model — near T-0688 (done); fm judge --model only (fmcli.py:6899)
- [new] Reflink-clone test fixture worlds — searched reflink; nothing
- [partial] Merge lanes in a scratch worktree before touching the live tree — fm ship uses a scratch tree (T-2086); lane merge path in fmlanes.py:1876 unverified
- [built] Time-bound lanes by progress, not wall clock — near T-2310 (done)
- [built] Throttle lanes while the user is active — near T-1841 (done)
- [built] Preview a lane before spawning it (`fm lane --plan`) — near T-2340 (done); fm run --dry-plan (fmcli.py:8012)
- [new] Hash shared git state around every lane — searched; fmlanes.py:28 only resolves the common dir
- [built] Cap what a lane can hand back to its planner — near T-0629 (done)
- [partial] Add pause, resume and shrink-budget controls per lane in the pane — fm budget caps exist; pane controls unverified

## c36 Lean metrics, charts and cost reporting

Mark: **skip** · value 2 · effort M · risk low — Mostly reporting on top of built cost and burden verbs; the cache ratio is built.

- [partial] Chart lean metrics across history — fm burden per version (fmcli.py:6858) and T-2358 lean ratchet; no chart
- [new] Wild: Hold a budget market for the footprint — speculative
- [new] Wild: Show remaining life in every verb's help line — depends on a deprecation clock; none built
- [partial] Print a capability bill of materials — fm doctor and MASTER.md list features; no BOM verb
- [built] Gauge the prompt-cache hit ratio per session — fm cost --sessions: cache read/write split and busts (fmcli.py:6856-6857)
- [new] Print the exchange rate on every Mission close — searched exchange rate; nothing
- [new] Weight yield per dollar by effort and flag task splitting — fm cost by task exists; no yield weighting
- [partial] Wild: Give every hook and verb a millisecond line in a shared budget — hook p95 ratchet (T-2358) exists; no per-verb shared budget
- [new] Ratchet peak memory and open file descriptors per verb — searched rss/fd ratchet; only time ratchets
- [new] Wild: Declare a worst case for every verb — speculative

## c37 Ledger and verify performance

Mark: **skip** · value 2 · effort M · risk med — Mostly built; the new items add state files against the lean goal.

- [built] Seek windowed readers to the window start — near T-1810 (done)
- [partial] Verify the hash chain from the last checkpoint — near T-2664 (done) verify-ledger; checkpointing unverified
- [new] Count fsyncs per hook and group-commit ledger appends — searched fsync; only write_atomic in fmlib
- [new] Dedupe hook-decision ledger writes by event key — searched dedupe ledger writes; nothing
- [new] Wild: Keep a derived columnar sidecar of the ledgers for instant aggregates — speculative; an extra state file
- [built] Wild: drop one whole day from a ledger and make windowed readers report the gap — near T-2648 (done): fm drill drops one ledger event class
- [built] Make each drill fault list the readers it must exercise — near T-2648 (done)
- [built] Scan ledger fields for write-only data — near T-0689 (done)
- [new] Wild: plant a deliberately wrong number in the receipt and see whether anything flags it — searched wrong-number plant in fm drill faults; none
- [new] Wild: show a blind-spot index per class in the pane header — visual

## c38 Test suite speed and determinism

Mark: **skip** · value 2 · effort M · risk low — Speed items are not lean/safe for #12; seed-shuffle alone is small, defer.

- [new] Shuffle the test order and print the seed on failure — no shuffle in plugin/tests grep
- [partial] Virtualize `time.sleep` across the test suite — T-2310 CPU-time bars in tests; sleep virtualization unverified
- [new] Run likely-to-fail tests first — no ordering found
- [new] Cache test results per file by measured dependency hash — no test cache found
- [partial] Call `fm` in-process from tests instead of spawning it — some tests call main; T-1337 unrelated
- [new] Fork-server for tests — none
- [partial] Replay hook inputs under a shrinking environment — T-1258 context-tax ratchet replays sessions
- [new] Flag redundant reruns on an unchanged tree — none
- [new] Bench hooks under contention and run background work at idle priority — no nice/ionice found
- [new] Memoize the Genesis sweep per cited-file hash — none
- [partial] Batch small cold reads into one child call — T-0694 milestone; batching unverified
- [new] Keep a warm pool of cold-read children — none
- [new] Tune install settings with a 5-second host microbench — none
- [partial] Start the cold read when a tower file is saved — T-2243 fm genesis put judges sections

## c39 Deletion safety, trash and plan/apply

Mark: **skip** · value 2 · effort L · risk med — Git and fm rollback already cover most recoverability; a generic trash is wide and speculative.

- [new] Split destructive verbs into plan and apply — grep plan/apply on destructive verbs: none generic
- [new] Send every deletion through a TTL trash — grep trash in plugin/lib: none
- [new] Move deletions to a session trash — same; T-1350 unrelated

## c40 Guard console and session receipt

Mark: **skip** · value 2 · effort L · risk med — Visual or large; outside-repo diff may spin out later.

- [partial] Build a Guard Console: grants, protected paths and freeze on one board — fm guard verbs and fm code TUI exist; single board absent
- [partial] Run a Session Receipt that diffs outside-repo changes and writes the "held back" letter — receipts exist (task receipts); outside-repo diff absent
- [new] Learn a sandbox profile from observed runs, then show it as a treemap you can trim — none; fmlandlock static sets
- [new] Add a Hostile-Input Test Bench that every static check runs against — none

## c41 Multi-agent roster, capability tokens and lanes

Mark: **skip** · value 2 · effort L · risk med — Large, speculative surface; capability token idea belongs to later slate.

- [new] Fold the agent roster, allowlists and depth caps into one signed `agents.toml` — no agents.toml
- [new] Pass a capability token down every spawn, never a shared grant — none
- [partial] Record every agent abstention and skip as a ledger event with a reason — T-0689 learning from outcomes; abstention events unverified
- [new] Give each role a "who checks the checker" pairing, enforced — none
- [partial] Replay a changed agent prompt against frozen cases before it goes live — T-0712 flywheel; fm exam
- [new] Throttle and hedge lanes by progress signals, not the clock — none
- [partial] Show the agents as a live "who's holding what" board — T-1000 pane; fm code TUI exists
- [new] Wild: Hold a nightly "mutiny drill" where a red-team agent tries to make a sub-agent break its own allowlist — speculative
- [new] Wild: Let agents bid for a task with a cheap probe run, and let the cheapest passing bid win — speculative
- [new] Wild: Pre-warm a lane's context (map, lessons, dossier) from queue prediction, as a local cache — speculative; map cache exists (T-0215)
- [partial] Make every multi-agent flow run single-agent in CI on a fake adapter — fm code bench uses seeded repos; fake adapter unverified

## c42 Red-team and adversarial probing

Mark: **skip** · value 2 · effort L · risk med — Mostly speculative; existing probe and mutate cover the groundable part.

- [partial] Wild: Hidden-ink exam kind — fm exam kinds exist (T-2394); no hidden-ink kind found
- [new] Wild: Detect "behaves differently when unwatched" in agent-written scripts — no such detector found
- [partial] Wild: mutate exit codes and see whether any test notices — fm bench guard --mutate does rules, not exit codes; T-0697
- [new] Wild: a red-team agent hunts for exit paths that break a verb's promise — no verb-promise red team found
- [new] Fuzz one-keystroke neighbours of your habitual commands — no typo fuzzing found
- [partial] Wild: Trend the model's own recklessness with a weekly bait suite — fm code runners --probe (T-1403) scores injection; no weekly trend
- [new] Wild: red-team from the user's own command distribution — T-0697 milestone only; no command-distribution red team
- [new] Wild: Adversary Lane That Minimises Its Own Fix — speculative

## c43 Sandbox, exec surface and OS isolation

Mark: **skip** · value 2 · effort L · risk high — Sandbox exists; remaining items are large OS-level builds with speculative payoff.

- [partial] Learn a sandbox profile from observed runs and enforce it — fm sandbox verb (fmcli.py:8187), --sandbox flag at 8177; fixed profile, not learned
- [new] Keep an exec manifest of every binary Foreman may spawn — grep subprocess manifest: none
- [new] Keep a list of the external programs Foreman may run — same as exec manifest
- [partial] Probe which sandbox primitives this kernel allows — fm sandbox/oracle use bwrap; a primitives probe not seen
- [new] Run the unattended drive as a separate low-privilege unix user — grep drive uid: none
- [new] Run Foreman's unattended processes under OS resource limits — grep RLIMIT/ulimit: none; fm contract bounds time/spend
- [new] Emit a devcontainer or rootless-podman profile from the sandbox profile — grep devcontainer: none
- [partial] Ship a typed safe-ops tool server in place of raw bash for risky verbs — fm mcp read-only tools (MASTER.md:230); none for write ops
- [new] Ship the guard as one file that protects a remote server (wild) — speculative
- [new] Intercept effects at a customs checkpoint — grep chokepoint: none
- [new] Lint every outward effect to one chokepoint — grep outward effect lint: none
- [new] Run Foreman's own suite under the guard in bypass mode — grep tests guard bypass: none
- [new] Wild: hostile-fake-agent footprint golden — speculative; fm exam uses throwaway repos

## c44 Secrets, bypass-mode and approval UX

Mark: **skip** · value 2 · effort L · risk high — Large new surface, speculative or visual; the built guard already refuses sudo and shims.

- [new] Seal secrets in a keyring and run commands through `fm with-secret` — searched with-secret/keyring; nothing
- [new] Wild: Release secrets only while the human is present, and give unattended lanes decoys — speculative
- [new] Wild: Tie the ledger signing key to the machine with TPM or `systemd-creds` — no hardware-bound key found
- [new] Wild: quote the price of bypass mode before it starts — searched bypass price; nothing
- [new] Wild: Run a pre-flight séance before every bypass session — speculative
- [new] Census listeners, tunnels and background services after bypass sessions — fm outbound lists requests only (fmcli.py:6773)
- [new] Pin ambient infrastructure context and block on mismatch — searched kube context pin; nothing
- [partial] Show an annotated approval card for guard blocks and `fm ask` grants — guard blocks print reasons; card format unverified
- [new] Wild: Add a hot-spare approver for `fm ask` — speculative
- [partial] Wild: dry-run pasted shell commands from the clipboard (opt-in) — oracle sandbox runs a line (fm replay --oracle, fmcli.py:7059)
- [new] Hold an intent-class jury for irreversible commands — speculative; costs model calls
- [new] Block by measured blast size, not command shape — fm graph blast is for code changes only
- [new] Put a blast-radius thermometer on the pane and status line — visual; no radius metric
- [built] Shim the destructive binaries on PATH — near T-2377 (done)
- [built] Refuse any script step that needs sudo or pipes a download to a shell — near T-1932 (done); fmguard system refusals (fmguard.py:5306)
- [new] Wild: Colour every tool call in the pane by reversibility — visual only

## c45 Safety presentation and threat modelling

Mark: **skip** · value 1 · effort M · risk low — Visual or speculative framing with no measurable lean or safe outcome.

- [partial] Render a live safety case — fm exam steer T-2625 builds an exam; no live case page
- [new] Compute a defence-depth meter — visual/speculative
- [new] Bind each threat-model row to a test — grep threat model in docs: none bound to tests
- [new] Price the user's disasters once, then report guard saves in hours — speculative
- [new] Wild: Print a monthly "things I held back from doing" letter — speculative; guard refusals logged only
- [new] Wild: five-minute "tour of what can hurt you" — visual/docs
- [new] Offer a "tripwire home" decoy — speculative

## c46 Speculative and stunt ideas

Mark: **skip** · value 1 · effort L · risk high — Speculative or product-direction, no grounded lean/safe value.

- [new] Wild: publish the ledger formats as an open spec with a 300-line reference reader — none
- [new] Wild: run a "heavy sleeper" week where one capability is secretly off per day — none
- [new] Pull a cable on a random subsystem during a real idle drive, with a kill switch (wild) — none
- [partial] Drop Foreman Desktop and open the web UI in browser app-mode — Desktop exists (T-0352); app-mode unverified
