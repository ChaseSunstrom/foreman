# Brainstorm catalogue: brainstorm-20261102-121128

552 ideas in 59 clusters, each grounded in the code: 104 built, 197 new, 249 partial, 2 premise-false. 24 clusters marked build.

## c01 First-class 'unproven' receipt state

Mark: **build** · value 4 · effort M · risk low — Claims already tri-state; carry that into the finish receipt and make overrides unable to upgrade it. Skip the visual-only items.  
Slate: Finish receipt gets a third state, unproven, that an override cannot flip to proven

- [partial] Mark a check that couldn't run as UNPROVEN, never as pass — fmprove.py:542,653,709 claims verdict unproven; finish receipt not confirmed
- [partial] Label UI checks that couldn't run as "unproven (no display)" — T-2394 exam kinds; T-2391 unproven rollup by domain
- [partial] Mark unrunnable checks "unproven" in every receipt — fmprove.py:709 only; fmrelproof.py has 7 hits
- [partial] Mark every overridden or unrun proof as "unproven" in a third state — T-2391; fmprove.py:708 three verdicts for claims
- [partial] Make "unproven" a first-class receipt state — fmprove.py:708; fmcli.py 22 unproven hits
- [partial] Give every receipt exactly three states: proven, unproven, overridden — fmprove.py:708 has proven/failed/unproven; no overridden
- [partial] Add an "unproven" receipt state that overrides can't turn into "proven" — T-2398 records the world; no override lock found
- [built] Give every check a third state, "could not run", with a reason — fmprove.py:653 verdict unproven with why
- [partial] Prove the headless case: UI checks that say why they didn't run — T-2394; mods/foreman-ui/tools/shot.py
- [new] Draw "unproven" as hatched, never green — site/ and mods hatch grep: only style.css hits, no unproven art
- [new] Give every receipt one visual verdict grammar — grep found no shared verdict style; fmprove.py:709 text marks only
- [new] Mark override and unproven rows with a persistent badge — grep of mods/foreman-ui for badge on override rows found nothing

## c02 Guard hardening and security

Mark: **build** · value 4 · effort M · risk med — DONE-WHEN mutation closes the vacuous-pass hole in the finish gate; rest overlaps built guard work  
Slate: Mutate each task's DONE-WHEN command to flag proofs that still pass on a broken tree

- [partial] Taint untrusted content in the guard — T-1327 nested sessions; fm audit data-labelling MASTER.md:739
- [partial] Run bypass-mode sessions in a bwrap/Landlock sandbox — fmlandlock T-1607 and fm sandbox fmcli.py:8135 cover fm code workers
- [partial] Enforce the guard at the OS, not the hook — fmlandlock.py confines writes; fm oracle bwrap fmoracle
- [partial] Scrub a pasted secret from every stored copy and say to rotate it — fmcore.secret_kinds + redact (MASTER.md:544); no sweep of stored copies
- [new] Replay the credential-redaction path against a public secret-format corpus — fmcore.secret_kinds tested on hand cases only; no corpus found
- [partial] Publish-time leak scan for auto-published data — fm share/fm sync redact; publish-time scan unconfirmed
- [built] Unit-test the guard rules with examples — fmreplay labelled cases + test_guard.py; fmmutate T-1066
- [partial] Wild: Compare a second implementation of the guard — fm oracle fmoracle.py runs lines in bwrap as a second opinion
- [partial] Install the guard and the task-id check as git hooks — T-1107 guards .git/config edits; git hook installer not found
- [built] Offer the safe alternative when the guard blocks — T-0185 block messages name one safe rewrite
- [partial] Show a "close call" shelf for the guard — fm guard fmcli.py:7024; fm replay --coverage
- [partial] Wild: Adversarial twin agent that tries to get a false "done" past the finish gate — fm exam fault kinds fmexam.py; T-2377
- [partial] Mutate each DONE-WHEN to find vacuous passes — fmmutate is guard-only; T-2453 outside authors
- [partial] Wild: Run a task's proof in a throwaway container as the arbiter — fm prove --release builds in temp; fm sandbox

## c03 Proof quality: mutation, cold re-run, adversary, second opinion, jury

Mark: **build** · value 4 · effort M · risk med — Vacuous-steer-check and mutate-the-fix both address proofs that cannot fail; cross-vendor judge conflicts with the no-model-in-fm rule.  
Slate: fm prove --mutate: revert a finished task's change and confirm its proof fails; flag vacuous [check:] steers

- [partial] Validate "test fails without the change" with mutation testing — T-0224 fm evolve mutation; fmmutate.py guard only
- [new] Mutate each finished task's fix to see whether its proof notices (wild) — fmmutate.py targets fmguard.py only
- [new] Add mutation proof: break the fix, watch the test fail — same
- [partial] Reproduce a sample of proofs cold (wild) — T-2606 replay from recorded commands
- [partial] Spot-check proofs cold on a schedule — fmnight.py nightly; T-2606
- [built] Replay a finished task from its recorded commands — T-2606
- [new] Run a proof court: an adversary tries to refute each "proven" (wild) — fmsecond.py is one-shot second read
- [partial] Wild: A "second opinion" button that has a different model re-judge any green receipt — fmsecond.py:1 independent second read
- [partial] Wild: let two agents on different models cross-check each other's proof — fmsecond.py
- [partial] Convene a cross-harness jury on disputed "proven" rows (wild) — fmsecond.py, T-0442 harness parity
- [partial] Add a cross-vendor judge to the finish gate — fmsecond.py; MASTER mandates no model import in fm (T-2486)
- [built] Quarantine proofs by independent author — T-2453 outside authors
- [partial] Tie every MASTER.md clause to a proof row — fm prove --docs, T-2616 docs proof kind
- [new] Hand out a proof "warranty" that expires (wild) — no hit
- [new] Calibration court (wild) — no hit
- [new] Check that stored steer checks aren't vacuous — fmsteer.py grep stale/vacuous: 0; T-2167 [check:] tags exist
- [new] Warn when a steer's automatic check has gone stale — same
- [partial] Lint the criteria in a task against their own examples — T-2606 criterion matching no test; fm oracle
- [new] Give exam items stable IDs and versions — fmexam.py grep ids not confirmed

## c04 Reversed 'proven' labels and proof-kind reversal rates

Mark: **build** · value 4 · effort M · risk low — Reversal machinery exists for decisions; extending it to proof kinds gives a measured trust score. Five ideas are one feature.  
Slate: fm outcomes: per proof kind, how often a proven task was later reverted or corrected

- [partial] Audit "proven" labels that were later reversed — fmoutcomes.py:245-252 reversals by decision kind, not proof labels
- [partial] Audit past "proven" labels against later reversals — fmoutcomes.py:251 fmcost.reversals
- [partial] Audit past "proven" labels read-only — fmoutcomes.py:285 reversal authors
- [partial] Track reversed "proven" labels — fmoutcomes.py:285
- [partial] Reversal ledger for "proven" labels — fmcost.reversals covers decisions
- [partial] Rank proof kinds by their measured reversal rate — T-2391 proof-kinds rollup; no reversal rate per kind found
- [new] Predict-then-run proof commands — grep predict near fmprove found nothing

## c05 Review aids and proof kinds for diffs

Mark: **build** · value 4 · effort M · risk med — hunk-level proof coverage is the one real gap in the proof story  
Slate: fm prove --coverage: report which changed hunks the proof command actually executed

- [built] Order the diff for a one-minute human review — fm tour reading order and risk verdict (MASTER.md:467-468)
- [partial] Show the ask the diff actually answered — Frontier 13 intent skills T-0713; fm explain fmrecall.py:1258
- [partial] Quiz the user on a big diff (wild) — fm dojo --quiz fmdojo (guard drill only)
- [new] Show which diff hunks the proof command exercised — grep hunk/coverage in fmprove.py: 0 hits
- [new] Add a diff-coverage proof kind — no coverage kind in fm prove; T-2288 is migration
- [new] Render proof coverage as a repo treemap — no coverage data to draw; depends on hunk coverage
- [partial] Check the diff against the plan's scope — T-2497 plan percent vs base rate; scope-diff check unconfirmed
- [partial] Gate diffs for secrets and new dependencies — fm find finders T-2121; fm secrets fmcli.py:7002
- [built] Gate package installs — install grants fm mcp grants; guard install checks (MASTER.md:409)
- [partial] Review someone else's PR with the proof discipline — fm pr fmcost.py:1128; fm audit fmcli.py:7239
- [new] Wild: Apprentice mode for the user's own commits — grep apprentice found nothing
- [partial] Show the red-to-green flipbook — fm incident T-2388; fm whyred fmdebug
- [partial] Slide before/after on UI receipts — fm shot / fm stories fmstories.py capture states
- [new] Read a fixed bug's gravestone — grep gravestone found nothing
- [partial] Replay a mistake as a kind post-mortem card — fm friction/fm repeats fmcli.py:7204-7225
- [partial] Rehearse a steer's check against the diff that would break it (wild) — T-2167 steer check; fm exam steer T-2625

## c06 State durability, integrity and recovery

Mark: **build** · value 4 · effort M · risk med — State-location audit plus a ledger cross-check catches silent loss; one doctor check covers both.  
Slate: fm doctor: audit durable state on volatile paths and cross-check ledger conservation

- [new] Spool child output off tmpfs before the session ends — no hit
- [new] Audit where durable state lives against tmpfs and logout — no hit
- [new] Audit Foreman state kept on volatile paths — duplicate of previous; no hit
- [partial] Chain ledger records with hashes and scrub them nightly — T-1065 fm verify-ledger; nightly scrub not confirmed
- [new] Fence ledger writes across concurrent writers — grep flock/fence on ledger found none
- [new] Classify every state file as source or derived, then rebuild derived ones nightly — no hit
- [new] Check conservation laws across the ledgers — no hit
- [partial] Wild: Rewind Foreman state to before a bad write — fmrollback.snapshot_upgrade fmrollback.py:75; fm snapshots
- [built] Take shadow checkpoints before each edit batch — refs/foreman/snapshots fmcore.py:339; undo_point fmhooks.py:2524
- [new] Ship a POSIX-sh rescue doctor for when `fm` won't start — grep rescue: none

## c07 Steers as standing rules

Mark: **build** · value 4 · effort M · risk med — steers pile up forever; scope, expiry and conflict detection are missing  
Slate: Give each standing steer a scope and release condition, retire one-shots at close, and flag conflicts

- [partial] Answer a re-pasted steer with the task that already did it — fm recall fmrecall; T-2409 checks new requests; no answer step
- [built] Pick standing rules per task instead of injecting all of them — T-1290 rules live once in fm-builder.md; fm rule fmcli.py:7051
- [built] Draft the standing rule and its check from a user correction — T-2167 every steer is a rule plus automatic check
- [new] Retire one-shot steers when their task closes — fm standing fmcli.py:6329 has no scope/expiry; grep found nothing
- [new] Give conditional steers a machine-readable release condition — grep release condition steers found nothing
- [partial] Store steers and criteria verbatim, and flag truncated ones — fm.fit truncation used widely; T-2322 pins literals
- [built] Check new requests against standing rules — T-2409 next-request/standing-rule check
- [new] Make the steers a compiled policy with a conflict detector — grep conflict detector steers found nothing
- [partial] Alert when a user correction repeats a class a prior ask fixed — fm repeats fmcli.py:7225; fm friction
- [partial] Replay last month's tasks with one steer removed (wild) — fm backtest fmcli.py:7035 replays rules
- [partial] Wild: Hold a constitution court — fm genesis drift gen-0 MUST/NEVER T-2104
- [partial] Wild: Stage a "lessons passport" shared across repos — fm share fmcli.py:6693; fm projects --sweep fmeco

## c08 CLI ergonomics and doctor

Mark: **build** · value 3 · effort S · risk low — tombstone for removed flags and doctor --calm are tiny; the rest already built  
Slate: Removed flags print a one-line tombstone (replacement and version) instead of an argparse error

- [new] Give removed flags a tombstone instead of an error — grep tombstone in plugin/lib found nothing
- [partial] Offer a `fm doctor --calm` view that prints one line when all is well — fm quiet fmcli.py:3692; fm doctor fmcli.py:7272; no --calm flag
- [partial] Collapse `fm doctor` to red items only — T-2104; doctor WARN/FAIL levels exist
- [built] Let `fm doctor --fix` apply the safe repairs — T-1184 fm doctor --fix
- [built] Offer a single-file `fm doctor` fix-it mode that applies safe repairs — T-1184 duplicate
- [built] Make doctor repair its own warnings — T-1184 and T-2257 doctor repairs
- [partial] Ship a single-file `fm doctor --explain` that turns each warning into one command — findings with fix commands (T-1184); fm explain fmrecall.py:1258
- [partial] Show only the day's next move on bare `fm` — fm next / fm glance exist; bare fm output unchecked
- [built] Route plain sentences to verbs — fm which fmcli.py:6681 T-1699; fm find
- [built] Complete `fm` in bash, zsh and fish, including task ids and verbs — fm complete fmcli.py:6146 T-0924
- [partial] Complete verbs with a reason and a next guess — fm complete verbs+ids; no reasons
- [built] Generate shell completion and did-you-mean from the verb table — cmd_complete fmcli.py:6146; difflib did-you-mean in fmcli (10 hits)
- [built] Cap default output at ten lines — T-1276 fm output trimmed; fm compact-output fmcli.py:8179
- [partial] Replace flags and env vars with three presets — fm autonomy fmcli.py:7256 and fm posture presets exist
- [partial] Knob census — fm settings fmsettings.py:1997 lists settings with sources
- [new] Put inline sparklines in CLI status lines — grep sparkline found nothing
- [partial] Wild: Say it in one sentence — fm glance; fm quiet

## c09 Self-change rollout, bisect and benchmarks

Mark: **build** · value 3 · effort S · risk low — checking the pushed tree equals the tested tree is a cheap gap in ship  
Slate: fm ship asserts the pushed tree hash equals the tree its tests ran against

- [built] Calibrate the noise floor for the self-change gate — T-2605 median wall-time comparison; fmselfgate.py
- [partial] Bisect Foreman's own regressions automatically (wild) — fm bisect fmcli.py:6767; fm night sentinel T-0888
- [partial] Auto-bisect an exam regression to a commit — T-0686; fm bisect; exam hookup unchecked
- [partial] Roll self-changes out to one lane first, with auto-rollback — T-2352 self-change gate at lane merge; fm rollback
- [new] Verify the pushed tree equals the tested tree — grep found no tree comparison in fm ship
- [new] Run a public benchmark slice as the outside referee — fm bench is own cases (fmbench); no public slice
- [partial] Predict file overlap before spawning parallel lanes — T-2407 predictions; fm lane fmlanes.py
- [partial] Predict file overlap between queued tasks and schedule lanes around it — duplicate; fm impact fmcli.py:6691

## c10 Self-check of the runtime and upstream

Mark: **build** · value 3 · effort S · risk low — Model-ID liveness probe is a few lines in fmscout and catches a silent break.  
Slate: Probe daily that every pinned model ID still answers

- [partial] Probe the upstream CLI contract daily — fmscout.probe_claude_code fmscout.py:57, probe_cc_changelog:335
- [new] Probe that every pinned model ID still answers — no hit for model ID liveness probe
- [partial] Stamp each result with a model fingerprint and canary it — fm canary in fmeco.py (MASTER.md:209)
- [new] Tell a sleeping machine from a dead timer — no hit
- [partial] Count the commands the guard couldn't parse — T-2342 and T-2068 name the guard clause that fired
- [new] Refresh test fixtures from real captures and flag drift — no hit
- [partial] Soak the drive with a scripted fake agent — fmbench.soak_case fmbench.py:649
- [partial] Wild: Replay each release against its own past inputs before it installs — fm backtest T-1058; fmreplay guard cases
- [new] Wild: Run a bare-minimum shell tripwire in a second language — no hit
- [partial] Keep test fixtures out of the live ledger — T-0207 debugging ledger

## c11 Speed: caching, warm daemon, impacted tests

Mark: **build** · value 3 · effort S · risk low — proof cache by tree hash saves repeated runs at ship and sentinel  
Slate: Cache fm prove results keyed by tree hash plus command so unchanged trees skip the rerun

- [partial] Keep one warm hook daemon — hook dispatcher in plugin/hooks/hook; T-0676; no resident daemon
- [partial] Run hooks through a warm daemon — duplicate; hooks p95 budgets MASTER.md:91
- [partial] Keep a warm hook daemon instead of cold Python starts — duplicate of warm daemon
- [built] One hook dispatcher process — plugin/hooks/hook single entry -> fmhooks
- [new] Cache hook verdicts per input hash to cut hook p95 — no verdict cache found in fmguard/fmhooks
- [new] Cache prove results by tree hash — grep write-tree/tree hash in fmprove.py found nothing
- [partial] Cache cold-read verdicts by content hash — T-2471 cold read; cache not confirmed
- [built] Run only impacted tests in the ship gate, full suite nightly — T-2323 fm ship runs affected tests over its range
- [built] Run affected tests first at ship, full suite as the backstop — T-2323
- [partial] Select tests by impact during a task, run the full suite at ship — T-2323 at ship; in-task selection fm impact fmcli.py:6691
- [built] Run only the tests a diff can affect — T-2323; fm impact
- [new] Rebuild `fm map` incrementally — fmmap rebuilds; no incremental grep hit
- [partial] Budget each verb's cold-start time and import cost — lazy() imports fmcli.py:6962; fm check timings MASTER.md:517
- [partial] Keep the injected prefix byte-stable to hit the prompt cache — T-0703 cache economics; stability test unconfirmed
- [new] Ship Foreman as a single zipapp — grep zipapp in plugin/lib found nothing

## c12 Crash, fault injection and reader robustness

Mark: **build** · value 3 · effort M · risk low — clock injection plus ledger-fixture replay catch real silent drift; rest overlaps fm drill  
Slate: Route every windowed reader through one injectable clock and boundary-test the metrics

- [built] Sweep crash points on the drive — fm drill plants faults mid-day (MASTER.md:135); T-0679
- [partial] Pull the plug on a whole session — fm drill torn ledger/stale lock faults (MASTER.md:135); no kill -9 session
- [new] Hold a suspend-and-resume test for the whole day — grep suspend in plugin/lib found nothing
- [new] Emit a repro bundle on any hook or verb crash — grep repro bundle in plugin/lib found nothing; fm record is for red runs
- [partial] Degrade to notes when the disk is full or read-only — read-only ~/.claude fallback to XDG state (MASTER.md:441); no ENOSPC path
- [partial] Add a stale-safe claim heartbeat to tasks — fm fsck stale locks T-1667; session heartbeat MASTER.md:341; flock locks
- [built] Check repo hazards before a finish or ship — T-1980 gates; fm ship gates fmcli.py:6985
- [partial] Check cross-ledger references with `fm fsck` — fm fsck fmcli.py:7286 covers locks/worktrees/journals; cross-ledger refs T-2339 unread
- [partial] Replay real poison inputs through every hook — fm drill + fm replay corpora; hook-wide poison replay not found
- [partial] Run a hook × failure-mode matrix — fm drill faults across SessionStart..Stop (MASTER.md:135); T-2344
- [new] Wild: Fossil mode: boot Foreman against a six-month-old ledger snapshot — grep fossil found nothing; fm rollback snapshots exist T-1085
- [new] Replay old ledger fixtures through the current readers — grep ledger fixtures replay found nothing
- [partial] Time ledger readers against 10× ledger size — T-2339 race at plan time; no scale benchmark found
- [new] Generate task histories to test state-machine readers — grep history generator found nothing
- [partial] Inject a fake clock into every windowed reader — fake clock only in fm night --tick (MASTER.md:147); readers use c.now()
- [new] Boundary-test every windowed metric against clock changes — no DST/clock-jump tests found in grep
- [partial] Schema-validate and retry every headless child's output — fmserve/fmcode headless claude paths; per-child schema not confirmed

## c13 Guard: ledger, replay, red team, packs, shadow

Mark: **build** · value 3 · effort M · risk med — Core is built; the real gap is a dry-run 'what would the guard have blocked' preview for the user's own history.  
Slate: fm guard --dry-run: replay the user's recent bash history through the guard and list would-be blocks

- [partial] Keep one guard ledger of every verdict — T-1910; fmreplay.verdicts
- [built] Replay the ledger against every guard change — T-2352 guard replay at lane merge
- [partial] Run an unattended red-team loop — fmdojo.py is human drill; fmmutate.py guard mutation
- [partial] Fail closed on the unparseable, in tiers — T-2068 names clause for unparsable code
- [new] Preview what a block would have done — no dry-run grep hit in fmguard
- [built] Turn repeated workarounds into rule proposals — T-1042 corrections become proposed rules
- [partial] Probe guard liveness from outside — T-0883 guard tests; hook circuit breaker T-0087
- [built] Test guard parity across harnesses — T-0442
- [partial] Subtract guard rules by evidence — fmmutate --weaken; T-2486
- [new] Wild: run blocked commands in a throwaway overlay — no hit
- [built] Wild: a Guard Dojo to try to sneak past it — fmdojo.py T-1608
- [new] Wild: a 100-line shadow guard that must agree — no hit
- [new] Share guard packs as tested, signed bundles — no hit
- [new] Export the guard as shareable policy packs — no hit
- [new] Wild: turn the guard into an on-device "what would have been blocked" dry-run for any shell — fmreplay.verdicts exists internally
- [partial] Fuzz the guard with an adversarial agent — T-0411 corpus; fmmutate.py
- [partial] Wild: Chaos-month for the guard — replay your own near-misses — T-2352 replay of ledger
- [new] Wild: a 100-line guard a person can audit in five minutes — fmguard.py is large
- [new] Wild: Show the guard as a visible tripwire — no UI hit
- [new] Make the hard hat wink when the guard saves you — mascot T-0108; no guard event hook found

## c14 Learning from the user's hand edits, reverts and regrets

Mark: **build** · value 3 · effort M · risk med — One real gap: diff landed lines against later user edits and file lessons; reverts are already learned.  
Slate: Mine post-landing user edits to Foreman-landed lines into lessons

- [partial] Learn from hand edits after landing — T-0705 ambient verification; no hand-edit-after-land miner found in grep
- [partial] Mine the user's hand edits after a landing — duplicate of previous; T-1537 taste ledger covers reverts only
- [partial] Harvest the user's rewrites of landed Foreman lines into lessons — same gap; MASTER.md:129 taste ledger reads reverts, not rewrites
- [built] Learn the user's review taste from reverted commits — T-1537 fm looks taste ledger, MASTER.md:129
- [partial] Add a one-key regret button on landed work — undo_point fmhooks.py:2524, fmsettings.undo; no per-landing key
- [built] Watch for regret after every subtraction — T-1946 fm ship --watch
- [built] Rank capabilities by correction regret — T-2482 genesis seed ranking
- [new] Show the three hunks you'd reject — no grep hit for a hunk-rejection predictor

## c15 Ledger resilience: record-class deletion, mutation, torn writes, authorship

Mark: **build** · value 3 · effort M · risk low — Five duplicate ideas; one drill fault kind in fmdrill (drop a record class, expect doctor to name it) covers it.  
Slate: fm drill gains a drop-one-ledger-class fault the readers must name, not crash on

- [new] Let each ledger reader declare the record classes it needs — grep found no reader declaration in fmledger.py
- [new] Check each ledger reader against a missing record class — T-2505 is a prediction exam, not this
- [new] Delete one ledger record class at a time and watch the readers (wild) — fmdrill plants other faults
- [new] Delete-a-record-class drill — same
- [new] Run a drill that deletes one ledger record class at a time — same
- [partial] Torn-write fuzz for ledgers — T-2337 calibration ledger; fmdrill plants faults
- [new] Run a mutation test on every ledger — fmmutate.py mutates guard only
- [partial] Tag every record with its author and filter readers by it — fmoutcomes.py:285 author notion; T-2453 outside authors
- [new] Merge Foreman's ledgers into one append-only record with a class field — many ledgers; fmledger.py exists, not merged
- [partial] Make every decider report its coverage — T-2347 final report; fmreplay --coverage for guard

## c16 Measurement integrity and calibration

Mark: **build** · value 3 · effort M · risk low — sample-size and abstain-rate scan finds silent dead deciders cheaply  
Slate: fm doctor row: list deciders with no sample size or an abstain rate near 100%

- [partial] Detect circular evidence in Foreman's own scores — T-0680 self-improvement; exam held-out rate T-2625
- [partial] Scan for deciders that carry no sample size — denominator checks T-1271; fmoutcomes bins; no scanner
- [new] Detect dead deciders by their abstain rate — grep abstain in plugin/lib: no rate tracking
- [new] Scaffold deciders with the blind-spot checks built in — no decider registry found
- [new] Wild: Run the placebo shuffle to expose circular readers — grep placebo found nothing
- [new] Measure blind-spot latency per bug class (wild) — grep blind-spot latency found nothing
- [new] Plant canaries to detect exam contamination (wild) — fm canary is install canary, not exam
- [new] Wild: Validate brainstorm questions against past misses — fm ideas fmideas.py:803 has no miss backtest
- [new] Add an adaptive-difficulty exam so plain stays near 50% — fmexam.py arms fixed; no adaptive difficulty
- [partial] Judge cold reads with a local model — T-2341/T-2471 Haiku then Sonnet; local profile in fm code only
- [built] Measure cold-read agreement between Haiku and Sonnet — T-2471 cold read made reliable, Haiku first Sonnet decides
- [built] Bind task-text numbers to the code constants — T-2322 long goals state every literal their checks pin
- [partial] Give every receipt a hatched third state with a reason code — fminfra verdict pass|fail|unproven with why (fminfra.py:208)
- [partial] Draw calibration as a reliability diagram with live bet dots — T-2498 reliability bins; fm outcomes; no diagram
- [partial] Fade values as they go stale — T-0697 verification reasoning; no age fade in UI
- [partial] Probe every blocked task against today's world — fm sentinel; fm todo checks block reasons
- [partial] Print the denominator on every "nothing found" — T-1271 worker verify; not universal

## c17 Outside-signal checks on Foreman's own gauges

Mark: **build** · value 3 · effort M · risk med — Six brainstormers converged on it and nothing exists. Start with one gauge (statusline tokens vs transcript usage).  
Slate: fm doctor cross-checks one self-written gauge against transcript usage and flags disagreement

- [new] Add an outside tripwire for ops gauges Foreman wrote itself — grep outside signal in doctor/watch/infra: 0 hits
- [new] Cross-check every ops gauge against a signal Foreman didn't write — same grep, 0 hits
- [new] Check ops gauges against an outside signal — same
- [new] Cross-check each ops gauge against a second source — same
- [new] Cross-check self-written gauges against outside signals — same
- [new] Add an outside witness for ops gauges — same
- [new] Add a ledger-health strip with outside-signal ticks — no ledger-health strip in mods/foreman-ui
- [new] Run a fuzzer that tries to make the gauges lie — fmdrill plants faults in a day, not gauges
- [new] Outside-signal contradiction check — same grep
- [partial] Calibration drift alarm — T-2498 interim calibration reads; no alarm found
- [new] Add a negative-space map of what Foreman never observes — no hit; fmmap is a test-to-code map

## c18 Proof kinds and verification

Mark: **build** · value 3 · effort M · risk med — Perf proof kind fills a real hole in the proof family.  
Slate: Add fm prove --perf: a benchmark threshold proof kind

- [new] Add a performance proof kind — T-2616 docs/T-2387 data proofs only; no perf kind
- [built] Verify host changes with commands, not hope — T-0943 lint_verify
- [built] Run the user's examples as red-first tests — T-2266 ship red
- [new] Write the acceptance test blind — no hit
- [partial] Run proofs in remote CI as an arbiter — fmci ci-watch polls CI after push; not proof arbiter
- [partial] Add a codemod mode with a repo-wide proof — fmcodemod.py:59 cmd_codemod exists
- [built] Watch dependencies with a proof lane — T-0751 runtime milestone
- [built] Verify every quoted line in a cold-read FAIL exists — T-2471
- [new] Ratchet function length and nesting, starting with `register.tsx` — grep ratchet: nothing
- [partial] Table-drive near-duplicate tests — T-1834 playbook use

## c19 Restore drill / host wipe rehearsal

Mark: **build** · value 3 · effort M · risk low — fmdrill's temp home plus fmrollback snapshots make a restore-then-doctor drill cheap.  
Slate: fm drill --restore: restore a snapshot into a temp home and run fm doctor on it

- [partial] Drill a host wipe: restore Foreman state on a scratch directory — fmrollback T-1085 restores project record; fmdrill.py is a fault drill, not restore
- [partial] Rehearse a host wipe with `fm restore --drill` — MASTER.md:263 fm rollback; no restore verb
- [partial] Run a restore drill — T-1085
- [partial] Restore drill for a replaced host — T-0679 resilience milestone; fm machine in fmeco
- [partial] Prove a restore drill on a clean home directory — fmdrill.py:1 uses a temp home
- [new] Restore drill: prove the proofs survive a wiped host — no hit
- [new] Restore drill with calibration carried over (wild) — no hit

## c20 Self-audit of session behaviour and dead code

Mark: **build** · value 3 · effort M · risk low — A uniform next command on nonzero exit is cheap and helps every verb.  
Slate: Print one next command on every nonzero fm exit

- [partial] Earn autonomy per task kind — T-2338 confidence routes next step; per-kind trust not found
- [partial] Audit your plain sessions for what Foreman would have caught — T-1624 session review (inbox); not a replay against guard rules
- [partial] Record guard blocks the user worked around — T-0298 bench stranger; fm doctor --wrong stores cases (MASTER.md:544)
- [built] Find modules no session path reaches — T-2270; fm map --cold
- [partial] Measure real-session code coverage of Foreman itself and file deletion candidates — fm map --cold covers repos, not Foreman's own lib
- [new] Print one next command on every nonzero exit — no hit for uniform next-command on nonzero exit
- [built] Test answerability of the status verbs — T-0959

## c21 Slimming and lifecycle

Mark: **build** · value 3 · effort M · risk med — verb count keeps growing; a death-certificate and expiry audit gives a pruning loop  
Slate: fm tidy --verbs: list verbs with no use in 60 days and a one-line retire proposal

- [partial] Give every new capability an expiry date — T-0680 self-improvement; fm trial due dates fmtrials.py
- [partial] Auto-close stale Foreman-filed items — fmscout stale handling (8 hits); fm tidy fmcli.py:7259
- [new] Move Genesis out of the core install — fmgenesis.py in plugin/lib core; T-2078 tower home
- [partial] Unload skills that haven't triggered in 60 days — fm triggers fmcli.py:7214 tracks skill triggers
- [partial] Swap rule: a new verb must retire one — T-0712 flywheel; ~190 verbs in fmcli add() list
- [new] Delete-a-module drill — grep found nothing
- [built] Pack the 1,388 skill files into on-demand bundles — fm lib on-demand cards T-0933
- [new] Verb death certificates — no verb-removal record found
- [new] Collapse the calibration readers into one module — fmoutcomes/fmtrials/fmforesight separate; refactor
- [new] Collapse the exam arms into "with" and "without" in the scorecard — fmexam.py arms; presentation only
- [built] Bound ledger growth with verified compaction — T-0676 performance; fm verify-ledger fmcli.py:6720
- [partial] Wild: Compact ledgers into signed summaries — fm verify-ledger hash chain; compaction exists
- [premise-false] Wild: A 100-line kernel that boots everything else — fmcli.py alone is 8000+ lines; kernel idea runs against design

## c22 Spend planning, quota and idle-yield

Mark: **build** · value 3 · effort M · risk med — A per-run spend receipt with yield is cheap and the cost ledger already exists.  
Slate: Print a spend receipt with yield per dollar after each drive run

- [built] Spend the expiring quota first — T-0676 performance and cost
- [new] Lint the spend plan against the steers — grep found no spend-plan lint
- [partial] Yield to the user: idle work preempts itself — fmlong/fmserve idle handling; preempt on user activity not confirmed
- [new] Print a spend receipt with yield per dollar — grep 'spend receipt|yield per': nothing
- [new] Offer three spend plans with a timed default — no hit; fmcost forecast exists
- [partial] Make zero spend the default with a named payoff — zero-token instruments T-0701; default is not zero
- [new] Schedule heavy runs around the user's own rhythm — no hit for rhythm scheduling
- [new] Freeze feature work when a verb burns its error budget — grep 'error budget': nothing

## c23 Triage and wake-up of deferred and inbox work

Mark: **build** · value 3 · effort M · risk low — Evidence-triggered wake of deferred tasks fits existing fm todo and fm find.  
Slate: Wake a deferred task when new evidence matches its brief

- [partial] Triage the deferred pile in five minutes — fm todo T-1157 and fm drive offer inbox items
- [new] Wake deferred tasks when matching evidence arrives — grep wake/deferred in lib: no evidence trigger
- [partial] Offer a plan menu on L tasks — T-2464 drive offers; L-task menu not found
- [new] Allow one check per task — no hit
- [new] Wild: Plant a honeypot in the inbox — grep honeypot: nothing
- [partial] Wild: Ask the user the question the user model is least sure of — T-2554 user model; fm ask exists; no uncertainty-ranked question
- [built] Score intake precision from the user's own drops — T-2554 user model reads user asks
- [built] Dedupe the idea ledger and count re-proposals — T-0689 intelligence milestone
- [partial] Stop brainstorming when it starts repeating itself — T-1388/T-0959 brainstorm partial answers; repeat-stop not confirmed

## c24 Flaky test quarantine

Mark: **build** · value 2 · effort S · risk low — Ledger exists; adding a per-test fail rate is small.  
Slate: flakes.json records a fail rate per test and fm doctor lists the worst

- [partial] Quarantine and track flaky tests — fmcli.py:1582 flakes.json _known_flaky; rerun once at :4859
- [partial] Flake quarantine with rates — flakes.json keeps names, rates not confirmed

## c25 Away and morning surfaces

Mark: **skip** · value 2 · effort S · risk low — Away card built; remaining items are decoration.

- [built] Print a "while you were away" card — T-0117, fmaway.py (MASTER.md:474)
- [partial] Add a "morning on the site" strip from last night's tick — fm away/digest exist; site strip not found
- [new] Add a "since you looked" ribbon at the top of every surface — grep 'since you looked': nothing
- [new] Typeset the daily report as a printable one-page broadsheet — grep broadsheet: nothing; fm digest exists
- [new] Wild: Print an anti-changelog each morning — no hit
- [new] Sign an absence contract before leaving — no hit; fm away is after the fact
- [partial] Wild: Hold a weekly one-key "Delete Tuesday" — fm tidy, subtraction watch T-1946

## c26 Decision inbox and interruption load

Mark: **skip** · value 2 · effort S · risk low — todo, vetoes, inbox prefer, ask fatigue already cover this

- [partial] Batch the user's decisions with timed safe defaults — fm decide --ask default fmcli.py:4346; fm ask batching nudge MASTER.md:544
- [built] Learn queue order from what the user actually picks — fm inbox prefer --why T-1872 learned priority
- [built] Add a veto window to costly decisions Foreman made for you — fm vetoes fmcli.py:603; fm todo lists costly decisions fmcli.py:4063
- [partial] Age every pending decision and escalate stale ones — pending approvals expire APPROVAL_TTL (MASTER.md:475); no escalation
- [partial] Cap interruptions per day — fm ask fatigue FATIGUE_ASKS fmcli ask_tally; T-2498
- [built] Surface open tasks that only the user's hardware or credentials unblock, on their own screen — fm todo T-1157 fmcli.py:4063
- [partial] Print how many minutes of review today's work asks of you — fm burden fmcli.py:6810 / fm tour review risk (MASTER.md:467)
- [new] Pre-answer every `fm ask` from the user model and score the guess (wild) — grep user model ask prediction found nothing; T-2409 predicts next request
- [new] Wild: Interview the user for five minutes a week — grep interview found nothing

## c27 Dream passes and cold re-derivation

Mark: **skip** · value 2 · effort S · risk low — fm dream already does this; check its nightly wiring instead

- [partial] Wild: Run a "dream" pass that picks random old closed tasks and re-derives them from the current repo — fm dream fmrecall.py:1451
- [partial] Wild: Run a nightly dream pass that re-derives one old fix cold — fm dream + fm night; duplicate
- [partial] Run a cold-start apprentice that re-derives each closed task from its ask alone — fm dream; T-2341 cold rival reads; paid per task

## c28 Forecast, cost and honest progress

Mark: **skip** · value 2 · effort S · risk low — forecast, cost, router and budget exist; remaining gains small

- [built] Forecast duration and cost before starting, then score the forecast — fm queue --cost T-1878; fm outcomes fmcli.py:6702
- [partial] Forecast the end of a long run — T-2327; fmforesight; fm code --max-usd cap fmcode
- [partial] Print the cost of each finished task in plain money and minutes — fm cost fmcli.py:6800; fm pr fmcost.py:1128
- [partial] Print a progress bar that is honest about uncertainty — status line step N/M (MASTER.md:91); no range
- [partial] Draw the forecast as a range on the work bar — depends on forecast bands in fmoutcomes; UI bar unchecked
- [new] Meter the ceremony tax per task — grep ceremony in plugin/lib: 0 hits
- [built] Route each task to the cheapest model that historically passes — T-2291 history-based model router; fmcode route
- [built] Plan the idle spend as a budget, not a loop — T-0703; fm budget fmcli.py:7531
- [partial] Add a spend-the-idle-budget planner that queues only measurement runs — fm night jobs fmnight.py:483; measurement-only filter not found
- [new] Wild: Let Foreman bet its own budget on whether a deferred task is worth doing — grep found nothing

## c29 Hooks and tower liveness, version skew, approvals

Mark: **skip** · value 2 · effort S · risk low — Mostly built.

- [built] Hook circuit breaker: fail open on slow, fail closed on guard — T-0087 hook circuit breaker
- [built] Version-skew check across installed parts — fmeco.py version skew T-0673
- [partial] Flight recorder for hook decisions (wild) — T-2281; hook logs, fmhooks.py
- [partial] Wild: Dead-man's switch for the whole tower — T-2542 unattended liveness
- [built] Chaos run (wild) — fmdrill.py T-1669 faults in a temp home
- [new] Approve `fm ask` prompts from a phone push (wild) — T-1226 approvals are local; no push grep hit
- [partial] Sweep a whole class of siblings after every user correction — T-1042 corrections become rules; sibling sweep unverified

## c30 Interop and export

Mark: **skip** · value 2 · effort S · risk low — Export exists; a support bundle is small but rarely needed.

- [built] Emit the user's way of working for other harnesses — fmcost.py:1197 EXPORTS; fmcli.py:6957 AGENTS.md/GEMINI.md/cursor
- [partial] Compile steers, lessons and guard rules into AGENTS.md, GEMINI.md and .cursor/rules — fmcost.py:1202 has rules, lessons, corrections; guard rules not confirmed
- [new] Produce a redacted support bundle — no bundle hit; redact exists in fmcore

## c31 Overrides recorded as overrides, not proof

Mark: **skip** · value 2 · effort S · risk low — Mostly duplicate of the unproven-state cluster; T-1137 and T-2398 cover the record.

- [partial] Record hand overrides as overrides, not proof — T-2398 proof run records the world; T-1137 stage_change event
- [partial] Record every override of an unproven row as "not proof" — T-2391/T-2398
- [partial] Record human overrides as an override ledger — T-1137 stage_change on the ledger
- [partial] Record overrides as overrides — T-1137, T-2398
- [partial] Make an override record that it is not proof — T-2398
- [new] Record overrides as not-proof, with an expiry — grep for override expiry in fmguard/fmcore found nothing
- [new] Show "what I almost did" on the override — no grep hit on override preview in fmhooks

## c32 Periodic digests, recaps, receipts to the user

Mark: **skip** · value 2 · effort S · risk low — fm digest and fm todo cover it.

- [partial] Send a weekly "what Foreman did for you" receipt — fm digest; fmnight.py morning digest
- [partial] Wild: A weekly "what I would have told you" letter from the user model — T-1800 reasons ahead unasked
- [partial] Add a "Friday recap" that tells the week as a story — fm digest
- [new] Wild: a weekly "diet" digest with a negative-growth goal — T-2281 lean ratchet is per ship
- [new] Stage a self-writing "cheat sheet of unopened proofs" (wild) — no hit
- [new] Record which proof artifacts get opened after a finish receipt — no hit
- [built] List what blocks only the user, with one action each — fm todo T-1157, MASTER.md:475

## c33 Release notes, changelog and receipts as prose

Mark: **skip** · value 2 · effort S · risk low — release notes and PR text built; rest is polish

- [built] Draft release notes and PR text from closed tasks — fm release fmcli.py:5239 / fmrelease.py; fm pr
- [built] Generate release notes from closed tasks and their receipts — fmrelease.py (16 changelog hits); duplicate of line above
- [built] Write release notes from receipts — fmrelease.py; duplicate
- [partial] Wild: Write the weekly changelog as the project's own release notes in the project's voice — fm digest fmcli.py:6697; no voice learning
- [partial] Generate the README feature list from MASTER.md clauses — fm clauses fmcli.py:7102; fm docs fmcli.py:8152
- [partial] Give every task a one-line headline written at close — task title exists; CHANGELOG Highlights T-2591; no close-time headline field
- [partial] Name each settled bet in the feed with a tiny result line — fm outcomes / fm trial grade bets (fmtrials.py:137)
- [built] Name the ship — T-2611 fm ship --chance names the ship record
- [partial] Wild: Keep a changelog of the user's changing mind — fm vetoes/decide reversals; fm standing steers; no timeline
- [partial] Keep a graveyard page of removed features and rejected ideas (wild) — deadends in meta fmfriction.py:398; no page
- [partial] Make the demo SVG regenerate from the latest real session — T-0979 re-recorded once; fm demo fmcli.py:7721

## c34 Subtraction and simplification

Mark: **skip** · value 2 · effort S · risk low — Housekeeping; steer supersession worth a later look only.

- [new] Fold the 30+ deferred "Later from" tasks into a few catalog files — archive housekeeping, no tool found
- [new] Collapse the steers into a superseding rule set — fmsteer.py; no supersede grep confirmed
- [partial] Cap Foreman-filed inbox items at 5 in `fm next` — T-0125 friction digest; cap not confirmed
- [new] Hide verbs the user hasn't used in 30 days from `fm help` — fm help is query-based, MASTER.md:445
- [new] Close or tier the long-blocked adapter tasks (T-0335, T-0336, T-0337) — user triage, not code
- [built] Subtraction (T-2534/35/36): — theme header, tasks T-2534..2536 already filed
- [new] Wild: a weekly "diet" digest with negative-growth goal duplicate — see digest cluster

## c35 Dashboards, timelines and alternative views

Mark: **skip** · value 2 · effort M · risk low — fm page, timeline and serve cover the substance; the rest is cosmetic

- [partial] Wild: Run a read-only status page that works over a local network and nothing else — fm serve fmserve.py; fm ui fmcli.py:8156
- [partial] Wild: Hand the whole queue to a phone-sized "pocket foreman" read model — fm serve Remote Control (MASTER.md:722); fm desk fmintegrations.py:262
- [partial] Open the whole queue as one offline HTML file (wild) — fm page fmpage.py; fm export fmcli.py:6956
- [partial] Wild: Play a finished day back as a scrubbable timeline — fm timeline fmintegrations.py:126 (not scrubbable)
- [partial] Show the morning as a map of the repo — fm map / fm tour / fm digest; T-2341
- [partial] Show the night's work as a sunrise strip — fm night/fm away summary text; no strip
- [new] Print the daily report on a thermal-receipt stylesheet — grep thermal found nothing
- [new] Profile a session's time as a flame bar — grep flame found nothing

## c36 Duel scoreboard, claims page, honest benchmarks

Mark: **skip** · value 2 · effort M · risk low — Benchmarks page already built; trial mode listed under onboarding too.

- [partial] Publish an honest duel scorecard, losses included — T-1222 Benchmarks page exists
- [partial] Publish a signed duel scoreboard against plain Claude — T-1222; signing absent
- [partial] Wild: publish a claims-versus-evidence page that rebuilds itself nightly — site/build.py, site/genesis/coverage.md; nightly rebuild unverified
- [new] Ship a trial mode with an eject command (wild) — grep eject: 0 hits in lib

## c37 Explain and provenance

Mark: **skip** · value 2 · effort M · risk low — fm why, explain, inbox prefer --why cover it

- [built] Show why a line exists — fm why FILE[:LINE] fmcli.py:6962 (fmmap.cmd_why)
- [partial] Add `fm why` for any verdict, hook note or refusal — fm why is file-based; refusals via fm gates/fm explain fmrecall.py:1258
- [built] Explain any line with `fm why file:line` — fm why fmcli.py:6962
- [partial] Explain what each waiting task is waiting on — fm todo fmcli.py:4063 lists blocked by user; fm queue block reasons
- [partial] Open a number's provenance on click — T-2591 highlights; fm explain; no UI click
- [partial] Wild: Show the user which of their own words each rule came from — fm standing fmcli.py:6329 keeps steer text; fm rule fmcli.py:7051
- [built] Resolve `fm config` values with their source — fm code config source column T-1359; fm settings
- [new] Wild: Let the user "adopt" a lesson by naming it — grep adopt lesson found nothing; fm adopt is for repos
- [partial] Fingerprint Foreman's own output so echoes can't pass as user input — redacted/pasted text never counts as approval (MASTER.md:742)
- [built] Add a "why this one next" whisper to fm next — T-1969 Stop drive and fm next reason

## c38 Install, timers and nightly hygiene

Mark: **skip** · value 2 · effort M · risk low — duplicate of fm night/sentinel/pause/canary and fm prove --release

- [partial] Hostile environment matrix nightly (run the suite) — fm drill temp-home faults; fm smoke fmcli.py:7725; no matrix
- [new] Run the nightly on awkward repo shapes — grep found no worktree/submodule/bare repo shape matrix
- [partial] Run a synthetic task through the installed copy hourly — fm sentinel/fm canary fmeco.py:1143; hourly cadence unchecked
- [partial] Check installed units still execute after an OS upgrade — fmdoctor.check_night_timers (MASTER.md:213) checks last run, not post-upgrade
- [built] Report alive-but-idle timers — T-2542 timers known alive via last trigger
- [built] Test install on clean distros with no `claude` on PATH — fm prove --release T-2389
- [partial] Run the fenced command blocks in README and MASTER nightly — T-2395 proof surfaces; nightly docs run not confirmed
- [new] Wild: Canary a rolling-distro upgrade before pacman runs it — grep pacman found nothing
- [built] Probe the guard from the timer's environment — T-1224; fm night timers run guard probe
- [new] Shadow twin on the last good release (wild) — grep shadow twin found nothing
- [built] Re-run proven tasks nightly and bisect the break — fm night runs fm sentinel T-0888; fm bisect fmcli.py:6767
- [partial] Cap unattended side effects per hour — daily risk budget fmrisk (MASTER.md:261); not hourly
- [built] Add a HALT file every unattended path checks — fm pause writes state/PANIC (MASTER.md:723)

## c39 Log the user's hand-typed verification commands

Mark: **skip** · value 2 · effort M · risk med — Privacy surface and unclear payoff; transcript format dependency.

- [new] Log the commands the user types to check verdicts via an opt-in `fm run` wrapper — grep bash-input in lib: 0 hits
- [new] Log the commands the user types to check Foreman, via a `fm verify` alias — T-1639 is fm flow, unrelated
- [new] Log the user's own verification commands (wild) — same
- [new] Log hand-typed verification commands from the Claude Code bash-input channel — same
- [new] Log the commands the user types by hand to check verdicts — T-2416 is goal verdict, other thing
- [new] Mine the transcript's bash-input records for the user's hand checks — same
- [new] Log the user's hand-checks as proof evidence — T-0701 is zero-token instruments

## c40 Mining closed bugs into finder and lint rules

Mark: **skip** · value 2 · effort M · risk low — Mostly built; bisecting a metric jump is a niche remainder.

- [built] Mine closed FIX tasks into finder rules — T-2241 fm find blind spots
- [built] Turn each fixed bug into a lint rule — T-1628 afterglow lint; T-2241
- [partial] Route bugs to the commit that introduced them — fm find hotspots T-2238 uses fix history; no introducing-commit routing
- [built] Map churn hotspots from task history — T-2238 fm find hotspots
- [partial] Bisect an abstain-rate jump to the commit behind it — fm backtest T-1058 replays history; no metric bisect
- [built] Turn an error report into a task with a repro — T-2297; T-0701 file repro tasks
- [built] File repro tasks from the user's own runtime failures — T-0701 zero-token instruments

## c41 Newcomer onboarding and docs honesty

Mark: **skip** · value 2 · effort M · risk low — model-priced and noisy; clause matcher was already removed as failing

- [partial] Teach a newcomer the repo from its task history — fm tour fmcli.py:6952; fm bench build --commits T-0222
- [new] Run a cold newcomer persona against the README — grep newcomer persona found nothing
- [new] Simulate a newcomer from README alone (wild) — duplicate of cold newcomer persona; no matches
- [partial] Map every MASTER.md clause to a test or exam line — fm clauses fmcli.py:7102; matcher removed T-2587

## c42 Onboarding, Lite mode, trial and eject

Mark: **skip** · value 2 · effort M · risk med — Tour built; Lite and eject are product decisions with no evidenced demand.

- [built] Give the first run a 90-second guided win — T-1309 fm code tui --tour
- [partial] Add a "gap-only" first-hour check instead of a tutorial — fm doctor; T-1309 tour
- [partial] Ship Lite mode: guard, plan, prove only — settings disable switch; no lite profile found
- [new] Wild: `fm eject` leaves a standalone guard and removes Foreman — grep eject: 0 hits
- [partial] Wild: a one-command home screen where plain `fm` shows only what to do now — fm next, fm todo exist

## c43 Replay, backtest and overnight measurement runs

Mark: **skip** · value 2 · effort M · risk low — backtest and night runs exist; remainder is chores.

- [partial] Replay a past commit overnight, Foreman vs plain, on the user's own repo (wild) — T-1058 fm backtest; fmnight.py
- [built] Wild: replay a past session against a new model or Foreman version — T-1058 fm backtest
- [partial] Spend idle usage on a whitelist of measurement-only runs — fmnight.py --tick model-free pass, fmbudget.py
- [partial] Run blind-language scenario generation overnight — fm oracle in fmideas.py; fmnight
- [partial] Turn ablation results into removal tasks — T-0224 fm evolve bench-gated
- [new] Split foreman-ui `register.tsx` while the budget is idle — register.tsx exists in mods/foreman-ui/hooks
- [partial] Add cost and token budgets per task, not just per account — T-1824 fm cost per task; fmbudget.py

## c44 Self-change experiments and duels

Mark: **skip** · value 2 · effort M · risk low — Experiment machinery largely built; remainder is speculative.

- [built] Duel Foreman against its past self — T-1058 fm backtest
- [partial] Build a rival from the README, then duel it — fm bench duel T-2536; README-rival not built
- [built] Run a prose-only arm in the duel — T-2536 fm bench duel --ablate
- [new] Write the smallest-diff retrospective — no hit
- [built] Keep a pre-registered prediction on every self-change and settle it from data — T-1059 pre-registered trial
- [built] Bet on whether each idea will ship and be used — T-2496 fm ship --chance
- [partial] Predict each proof command's result before running it — T-2387 data proof; predict-before-run not confirmed
- [built] Quarantine a lesson that preceded a failure — T-0680 self-improvement
- [built] Measure how often injected lines get used — T-0051
- [partial] Distill repeated winning trajectories into skills, kept only if they cut cost — T-1834 playbook use; fmplaybooks; cost gate not confirmed

## c45 UI design system and accessibility

Mark: **skip** · value 2 · effort M · risk low — UI mod not read; gallery and colour degradation exist, rest is polish

- [partial] Define one design-token sheet for every surface — fm design fmcli.py:7739; fm looks fmcli.py:8033
- [new] Make clickable task ids and verdicts one component — mods/foreman-ui not read; grep not run
- [partial] Fix the docked pane background and add a contrast test — T-1002 pane readability; contrast test unchecked
- [new] Let the web UI theme follow the host terminal palette — fmcodetui has colour_depth only (MASTER.md:708)
- [built] Build a UI gallery with golden screenshots — fm page looks gallery T-1649; fm shot
- [partial] Make every motion map to a state-machine edge — fm motion fmcli.py:7847 exists
- [new] Allow one pulsing element per screen — no motion budget found
- [built] Degrade colour for NO_COLOR, 16-colour and non-truecolor terminals — colour_depth 24/256/8/0 on NO_COLOR (MASTER.md:708); T-0962
- [partial] Encode verdicts with shape, not colour alone, and respect reduced motion — reduced motion honoured (MASTER.md:162,188); shape coding unconfirmed
- [partial] Reflow the pane across narrow, medium and wide terminals — Term.frame handles resize; breakpoints unchecked
- [new] Give every lane a name and colour that follow it everywhere — fmlanes names only; no colour binding found
- [new] Wild: Hatched "unproven" rendered as a visible fog over unrun checks — unproven is text verdict (fminfra.py:208)
- [new] Wild: Let the hard hat carry the mood of the calibration — hard hat mascot not grepped; likely UI mod

## c46 Undo, park, resume and partial landing

Mark: **skip** · value 2 · effort M · risk med — mostly built (revert, oops, resume, failover); remainder is speculative

- [built] Undo a landed task in one command — fm task revert fmcli.py:6439 (T-0732); fm oops fmcli.py:5184; T-2342
- [partial] Park and resume cards for interrupted work — fm resume/checkpoint fmcli.py:7098-7107; no card UI found
- [new] Land the best verified partial when a task runs out of time — grep for partial landing in fmcode/fmlanes found nothing
- [built] Schedule work to resume when a usage limit lifts — fm code limits and failover T-1356; fm at fmcli.py:6820
- [partial] Journal multi-step verbs before running them — fm code journal code/<task>.jsonl (MASTER.md:704); other verbs not journaled
- [partial] Mark sessions that ended without a clean close — fmcode.unfinished lists open journals (MASTER.md:711); no session-level mark
- [partial] Reap orphaned children on a drive kill — fm pause --now panic_stop kills what runs (MASTER.md:723); drive kill unchecked

## c47 Vocabulary, glossary and doc-size lints

Mark: **skip** · value 2 · effort M · risk low — Vocabulary drift is real but glossary lint is speculative; reader-divergence is covered by cold read.

- [new] Define-on-first-use lint plus `fm glossary` — grep glossary in plugin/lib: no hits
- [new] Cap the vocabulary with a glossary lint — same grep, no hits
- [partial] Set a reading budget per doc — fmcost AGENTS_CAP 32KiB; T-2266 6,400-char always-on cap
- [built] Wild: Probe legibility with a cold reader — T-2471 cold read (Haiku then Sonnet)
- [partial] Make two cold readers interpret each DONE-WHEN independently — T-2471 cold read exists; no two-reader divergence on criteria
- [new] Wild: Keep a one-page napkin contract — grep napkin: no hits
- [partial] Wild: Fold the Genesis files into one readable page — T-2626 catalogue on the Genesis page
- [new] Stamp every pack section with its age — no hit for pack section age stamps

## c48 Web UI quality gates and designed states

Mark: **skip** · value 2 · effort M · risk low — Empty-state and accessibility work is nice but not core; contrast already handled.

- [partial] Ship a motion budget linter for the web UI — fmscene.soak_problems fmscene.py:1089 budget_ms
- [new] Render every receipt state from one verdict component with a state table — no hit
- [new] Design the "nothing here yet" screen per web view, each with the one command that fills it — no hit
- [new] Show a diff-of-state scrubber on the stage rail — no hit
- [partial] Ship a contrast and colour-depth gate for all themes — T-1736 one WCAG contrast function; fm design roll fmroll.py
- [new] Make every chart keyboard- and screen-reader-navigable with a data-table twin — no hit
- [partial] Give the guard block a designed "stop" card with the safe alternative — T-0394 names the guard's save; T-2068 clause hint
- [new] Wild: Make the guard a visible tripwire that snaps in the pane — no hit
- [built] Name the guard's save in plain words — T-0394
- [partial] Make foreman-ui disarm itself on a version mismatch — fmeco version skew (MASTER.md:209)

## c49 Ceremony per task kind and A/B

Mark: **skip** · value 2 · effort L · risk med — needs a ceremony profile model that does not exist; protocols.json tiers already approximate it

- [new] Fetch a ceremony-per-task-kind table from a Haiku-vs-Sonnet replay of finished tasks — ceremony has 0 hits in plugin/lib; protocols.json has S/M/L only
- [new] Replay the ledgers under other ceremony profiles with zero tokens — no ceremony profile concept found
- [new] Wild: A/B the user's own queue by randomizing ceremony per task — no ceremony profile concept found

## c50 Foreign repos, teams and remote machines

Mark: **skip** · value 2 · effort L · risk high — Team and remote modes are large and off the single-user core.

- [partial] Run Foreman on thirty foreign repos, zero tokens — fmeco projects --sweep, fm adopt, fm map --cold
- [partial] Fill missing stack cards from the corpus — fmmap stack cards, MASTER.md:193
- [new] Promote steers across repos only when they recur — no hit
- [new] Make a team ledger with author-tagged steers — no hit
- [new] Git-native team mode: the queue, claims and receipts in `refs/foreman/*` — refs/foreman only for snapshots/undo/shipped
- [partial] Run lanes on the user's other machines over ssh — T-0711 cockpit; fm machine in fmeco
- [new] Let a pocket CLI reply to `fm ask` over a webhook — grep webhook: nothing

## c51 Harness portability and integrations

Mark: **skip** · value 2 · effort L · risk med — bus, MCP, agents exist; ACP and editor work is large for a niche

- [partial] Generate a per-harness parity table from a conformance run — fm agents list prints enforcement; parity test in fmagents (MASTER.md:233)
- [partial] Add a cross-harness conformance run that fills T-0335/36/37 with evidence — parity test exists; needs real harness run
- [new] Hand a task between harnesses — fm agents installs hooks; no task handoff; fm tour ID is human handoff
- [built] Add an event bus with notification sinks — fmbus.py cmd_bus:569; fm notify fmserve.py:790
- [partial] Sync the queue with GitHub Issues or Linear in both directions — fm inbox gh fmeco (one-way in); no Linear
- [new] Queue publishes and retry them idempotently offline — grep offline publish retry found nothing
- [built] Wild: Make Foreman an MCP server for any agent — fm mcp fmmcp.py (which, grants) T-2378
- [built] Expose discipline as an MCP server — fm mcp T-2378; T-2371
- [new] Speak Agent Client Protocol so editors can host `fm code` — grep ACP found nothing
- [partial] Show Foreman in the editor status bar — statusline hook is Claude Code only (MASTER.md:91)
- [partial] Ship a status-bar module instead of a tray icon — statusline status.json could feed one; no module
- [new] Wild: Hover any `T-####` in the editor to see its receipt — no editor extension found
- [partial] Wild: Make ledgers merge cleanly across machines — fm sync fmsync.py; fm machine id fmeco.py:1192; merge rules unknown
- [partial] Stamp records with a host id so two machines can't blur ledgers — fm machine hashed machine id (MASTER.md:479); log events unstamped
- [partial] Wild: Replay a session against a new model before upgrading — fm bench build --commits T-0222; fm replay

## c52 Receipt export and distribution (PR bot, SARIF, in-toto, signed bundle)

Mark: **skip** · value 2 · effort L · risk med — No evidenced user need; signing adds key management.

- [new] Sign proof receipts as in-toto attestations — grep in-toto: 0 hits
- [partial] Add a PR bot that posts the proof receipt as a comment — fmpr.py exists, unproven mention; comment posting unchecked
- [new] Export Foreman data as SARIF and OpenTelemetry — grep sarif/otlp: 0 hits
- [new] Make the receipt a signed, hash-chained bundle — no hash chain grep hit
- [partial] Show the receipt as a one-glance "proof card" — fmprove.py:709 text summary; no card
- [partial] Show the calibration as a reliability diagram — T-2498 reliability bins in text

## c53 Sandboxing and session forking

Mark: **skip** · value 2 · effort L · risk high — Large and risky; the bwrap oracle already covers the common case.

- [partial] Run bypass sessions on a copy-on-write overlay of $HOME with a side-effect diff — fmoracle bwrap sandbox (MASTER.md:546) for lines only
- [new] Fork a finished or live session at any step into a counterfactual branch — no hit for session fork
- [new] Guard with a local small-model intent check for commands no rule matches — guard is rule-based; no local model hit
- [new] Seed bugs into the user's repo as a skill drill — no hit

## c54 Speculative idle work and parallel framings

Mark: **skip** · value 2 · effort L · risk med — draft, race and rival plans cover it; costs real money for unclear gain

- [built] Spend idle usage on speculative drafts of the top queue items (wild) — fm draft fmdraft.py T-1062 (MASTER.md:590)
- [partial] Run the same ask on two models and show a diff of diffs (wild) — fm second / fm lane race (T-2339); no diff-of-diffs view
- [partial] Wild: Adopt-an-issue, spending idle quota on local draft PRs — fm draft + fm inbox gh fmeco; not issue-driven
- [new] Spike deferred tasks under a cap to learn their real effort — fm draft only takes top unblocked S; no deferred spike
- [partial] Spike two approaches in parallel lanes and keep the smaller proof — T-2339 race at plan time chosen by evidence; fm lane
- [partial] Race three framings of an L task, keep the proven smallest — T-2339/T-2341 rival plans; not three framings
- [partial] Rehearse tonight's plan before the user leaves — fm night --plan listing jobs fmnight.py:483
- [partial] Wild: Pre-mortem every long run — fm second plan on L; no explicit pre-mortem prompt
- [partial] Wild: Dead-reckoning twin that predicts the next session's first hour — T-2409 next-request prediction; fmforesight
- [partial] Wild: Let the proof ask a stranger model to break it first — T-2453 outside authors for proofs

## c55 Predictions, bets, calibration surfaces

Mark: **skip** · value 1 · effort S · risk low — Mostly built; remainder is cosmetic.

- [built] Show a sealed-prediction hit rate (wild) — T-2505 sealed predictions; T-2406 prediction book
- [partial] Let the user bet against Foreman — T-2406 prediction book, no user bet verb found
- [new] Name a settled bet in the feed as a small celebration — no hit
- [new] Settled-bet one-liners in the feed (wild) — no hit
- [partial] Confidence-gated ceremony — T-2337 calibration ledger; ceremony tiers
- [partial] Pick ceremony by nightly ablation — T-0224 fm evolve; fmnight.py
- [built] Forecast the whole queue (wild) — T-0108 whole-queue progress, size words
- [built] Calibration card in the session start — T-2589 session-start note
- [new] Wild: Let the hard hat have moods from the calibration data — mascot exists T-0108; mood no hit
- [new] Wild: Give the hard hat a mood — same

## c56 Task-close delight and UI flourishes

Mark: **skip** · value 1 · effort S · risk low — Cosmetic, low value.

- [built] Show the red-to-green moment as a one-line "flip" on close — T-0913 closing moment
- [built] Greet a clean `fm doctor` with one calm line — T-1736 cleanups
- [new] Give the hard hat a mood from today's record — no hit
- [new] Chime softly when a long run lands a pass — no hit
- [new] Let a task finish with a tiny "first of its kind" badge — no hit
- [built] Add a "settle" transition when a number changes — T-2594 gen-2 review
- [new] Wild: Print a tiny sparkline "heartbeat" of the drive in the terminal prompt — grep sparkline: nothing
- [partial] Wild: Let the web UI become an ambient dashboard on a spare monitor — fmserve web UI exists; ambient mode not found

## c57 Theme headers from earlier rounds

Mark: **skip** · value 1 · effort S · risk low — Headings, not ideas; already filed tasks.

- [built] Unattended liveness (T-2542): — filed as T-2542
- [built] Duplicates and grounding (T-2546/47): — filed as T-2546/47
- [built] Input authorship (T-2554): — filed as T-2554
- [built] Silent abstention (T-2566): — filed as T-2566

## c58 Delight, voice and novelty

Mark: **skip** · value 1 · effort M · risk low — novelty with no stated user need

- [new] Dictate asks and hear the morning brief from your phone (wild) — grep voice/tts found nothing
- [new] Wild: Brief the day by voice — duplicate of voice idea
- [new] Wild: Turn a bug report into a task from a screen recording — fm img/fm shot read images; no video intake
- [new] Wild: Install an andon light — grep andon found nothing; fm notify fmserve.py:790
- [partial] Play a soft chime or terminal bell when a long run finishes with a pass — fm code TUI bell_due on block/refusal (MASTER.md:708); not on pass
- [new] Collect earned stickers for firsts — grep stickers found nothing
- [new] Ask the duck — grep duck found nothing
- [new] Hear the factory — no sonification found
- [partial] Wild: Offer an end-of-day "tool belt" screen that shows only the three verbs you used — fm triggers/fm log fmcli.py usage tallies

## c59 UI polish, animation, empty states, command palette

Mark: **skip** · value 1 · effort M · risk low — Cosmetic; premise false for web screens and palette.

- [new] Animate the stage rail so state is felt, not read — no hit in foreman-ui
- [new] Animate the stage rail to explain state — same
- [new] Clickable task ids everywhere — terminal UI; no link grep
- [new] Play the queue as a train timetable — T-0243 is shadow-user soak, unrelated
- [new] Wild: Turn a finished day into a 20-second replay clip — no hit
- [new] Wild: A "ghost pair" that argues the other side in the pane — no hit
- [new] Quiet the doctor with a "all clear" moment — no hit
- [new] Ship designed empty, loading and error states for every web screen — no web app; site is static
- [partial] Make the Today charts one shared chart kit — mods/foreman-ui/hooks/kit.ts
- [partial] Fix the pane background mismatch — T-1012 pane work; bug not reproduced
- [new] Wild: Play the session back as a scrubbable timeline — no hit
- [new] Wild: Turn the tower into a living map — fmmap is test map
- [premise-false] Add a keyboard command palette to the web UI — foreman-ui is a Claude Code terminal mod; no web UI
