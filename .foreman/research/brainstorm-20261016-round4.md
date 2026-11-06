# Round 4 catalogue

195 ideas, 46 clusters, each grounded against plugin/lib, hooks, skills, workflows, mods/foreman-ui and CHANGELOG.md. Paths are relative to ~/.claude/foreman.

## C1. Auto-record reviewer findings
Ideas: Auto-record reviewer findings from the review workflow; Record reviewer findings automatically at reviewer stop; Record reviewer findings from the reviewer's own output; Parse reviewer output into findings automatically; Prove the reviewer loop closes: auto-record findings and show defect-class survival
- Grounding: Manual today: `fm task finding` (plugin/lib/fmcli.py:480, T-0743). SubagentStop (plugin/lib/fmhooks.py:2936-2962) logs only summary_chars; the payload's last_assistant_message is never parsed. Reviewer output format is fixed (fmcli.py:4076 `## <lens>: ok | changes needed`, findings ranked HIGH/MEDIUM/LOW with file:line); plugin/workflows/review.js returns a structured findings schema. Defect classes already feed builder briefs (T-1164).
- Status: partial: the reading side (defect classes, past findings per lens, fmcli.py:4089) exists; recording is manual; no survival view.
- Score: value 4, effort M, risk low
- Decision: build

## C2. Guessed verbs and flags just work
Ideas: Alias the common guessed verbs; Make guessed verbs and flags work, using the unknown-command log; Make common guessed commands just work, with a quiet "(ran `fm task ls`)" note; Learn verb aliases from the unknown-command ledger; Let the common guessed verbs just work; Alias common guessed command names; Make the commonly guessed commands work; Add a verb-alias table fed by the unknown-command ledger; Alias guessed verbs from the unknown-command log and say so quietly
- Grounding: Only nearest-match hints exist: ArgumentParser.error (plugin/lib/fmcli.py:4448-4462, T-0273/T-1170). Verified here: `fm task list` and `fm task ls` fail with "unknown ... (fm help lists them)" and `fm task list` adds 'did you mean split?'. No alias table, no unknown-command ledger (grep finds none).
- Status: partial: wrong guesses are named, never run; no aliases; no log to learn from.
- Score: value 4, effort S, risk low
- Decision: build

## C3. Headless review and ideas for the unattended drive
Ideas: Let the autonomous drive run review and ideas workflows; Make the drive able to run review and ideas headless; Report which shipped verbs the unattended drive can reach; Make the plugin workflows thin wrappers over `fm` verbs; Let the autonomous drive invoke review and ideas as headless verbs; Gate the drive on a review-then-fix loop per lane
- Grounding: plugin/workflows/review.js and ideas.js (T-0787) are Claude Code workflows the user types (CHANGELOG Unreleased; the T-1174 brief: a workflow 'needs the user's opt-in'). Headless pieces exist: `fm ideas` (plugin/lib/fmideas.py, tool-less children), `fm draft` (T-1062), `fm run` (plugin/lib/fmserve.py cmd_run), `fm audit prep` (fmcli.py:4196, prints a reviewer brief for a subagent), `fm contract` bounds spend (T-1158). No verb runs the audit lenses through `claude -p`.
- Status: partial: ideas headless is done; review is not; 'drive runs workflows' is a false premise (a hook cannot start a workflow), the lever is a verb.
- Score: value 4, effort M, risk med
- Decision: build

## C4. Lane builders run their worktree's own fm
Ideas: Make bare `fm` inside a lane resolve to the lane's own copy; Give each lane its own `fm` on PATH; Resolve bare `fm` to the worktree's own copy; Make lane builders see their own `fm` flags when testing guard changes; Let lanes run `fm` from their own worktree
- Grounding: Verified: `readlink -f $(which fm)` is ~/.claude/foreman/plugin/bin/fm, the main checkout; plugin/bin/fm only prepends its own sibling lib dir (bin/fm:6). A builder in a linked worktree running bare `fm` exercises the main checkout's code, not its edited copy. The builder contract (plugin/lib/fmlanes.py:137-160, plugin/agents/fm-builder.md) says `fm focus` and never names a worktree-local binary.
- Status: new
- Score: value 3, effort M, risk med
- Decision: build

## C5. Release as one resumable verb
Ideas: Add `fm release` that does the eight-step ritual; Make the release ritual a resumable, checkpointed run; Make `fm release` one transactional verb; Cut a release with one verb, `fm release`; Collapse the release ritual into one resumable `fm release`; Cut a release with `fm release`, resumable at every step; Release as a drive-run pipeline
- Grounding: release.py (T-0678) bumps plugin.json and both marketplace.json, heads the changelog, runs gates, commits, optionally pushes from a scratch clone, and has --canary (fm sentinel per project); `fm release-check` (plugin/lib/fmdemo.py:152, T-0960) runs doctor and demo in a temp HOME; `fm round close` (fmcli.py:3737) tags round-N; plugin/tests/test_release.py exists. Not an fm verb, no checkpoint or resume, and release-check, round close and the machine update are separate manual calls.
- Status: partial: bump, gate, commit and push are one script; the whole chain is not, and nothing resumes after a failure.
- Score: value 3, effort M, risk med
- Decision: build

## C6. Release story pages and overnight skeptic
Ideas: Wild: Self-diff the release against round 2 as a "what got better" page; Wild: Prove each release candidate by building a task with itself; Wild: Auto-cut a 30-second "director's cut" replay when a release is tagged; Wild: Run a night "bounty hunt" where a skeptic agent attacks the last release; Wild: Publish Foreman's own receipts as a static "state of the product" page; Wild: Pick one showcase moment per round for the user to show someone; Wild: Hold a "regret test" before pushing to main; Wild: Render a git-history time-lapse at each release; Wild: Mode where a skeptic child tries to break the last release overnight
- Grounding: Nothing equivalent: `fm release-check` and sentinel are checks, not stories; `fm pr` renders per-task descriptions (T-1167); `fm night` runs jobs (plugin/lib/fmnight.py).
- Status: new
- Score: value 2, effort L, risk low
- Decision: skip (Pages and replays are presentation; the overnight skeptic needs model spend and has no deterministic test; sentinel and release-check already catch regressions.)

## C7. One `fm round` verb
Ideas: Fold `fm ideas`, `fm review` and the plugin workflows into one `fm round`; Make the round itself a verb: `fm round` runs review, brainstorm, triage, build, and release; Run a shadow round on a throwaway clone (wild)
- Grounding: `fm round close` tags and lists (fmcli.py:3737). The forever loop already sequences a round: `fm loop round` and `fm loop round --next` (CHANGELOG Unreleased, T-1057); /foreman:review and /foreman:ideas exist (T-0787).
- Status: partial: round sequencing exists as `fm loop round`; folding workflows overlaps the headless-review cluster.
- Score: value 2, effort L, risk med
- Decision: skip (Overlaps `fm loop round` and the headless-review cluster; adds no capability.)

## C8. Refused commands in the friction digest
Ideas: Show refusal commands in the friction digest; Put the refused command and its replay verdict in the friction digest; Mine guard refusals into a digest that shows the commands; Mine guard refusals with their full commands into the friction digest
- Grounding: plugin/lib/fmfriction.py:128-140 shows each guard block with its newest command (T-0172), the replay verdict "today's guard allows it / still blocks" (fmfriction.py:61-68, T-0187), and rules by fire count (T-0672); CHANGELOG T-0698 friction batch.
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (Already shipped (fmfriction.py:128).)

## C9. Guard refusal workbench (`fm guard mine`)
Ideas: Build a guard refusal workbench (`fm guard mine`); Auto-label mined refusals as right or wrong from what followed; Wild: Publish a daily "what Foreman refused and why" page for the user to skim; Wild: Guard "court" that replays the day's refusals to the user as a one-minute verdict page
- Grounding: `fm guard` has only try and wrong (plugin/lib/fmhooks.py:1041-1045, T-1146/T-1162); `fm replay` (plugin/lib/fmreplay.py) replays transcript commands; guard_block events carry cmd (fmfriction.py:128). No verb lists recent refusals for review, and nothing labels one from what followed (retry, rewrite, override).
- Status: partial: data and replay verdict exist; the mining verb and the auto-label are new.
- Score: value 3, effort M, risk low
- Decision: build

## C10. Guard drift nightly and per-rule cost
Ideas: Run guard drift as a night job with a verdict diff; Track guard cost per rule in the friction digest
- Grounding: `fm replay --cases --capture` files one FIX per drifted labelled case and `fm night` runs it (fmreplay.py:292-351, T-1162); per-rule fire counts exist (fmfriction.py:138-140). Milliseconds per rule are absent.
- Status: partial: drift job exists; verdict diff and ms per rule missing.
- Score: value 2, effort S, risk low
- Decision: skip (Drift capture already runs nightly; the remaining gap is small.)

## C11. Premise check before guard tasks
Ideas: Wild: Premise-check sandwich — run a mined replay before any guard task is accepted; Replay mined refusals as a standing premise check before any guard task; Gate guard tasks on a standing replay premise check
- Grounding: `fm replay --candidate REF|FILE` scores a changed guard against the working one (plugin/lib/fmcli.py:5112-5114, T-0712) and `--cases` replays labelled cases; nothing requires either when a task edits plugin/lib/fmguard.py (close gates, fmcli.py:570-596, never mention replay).
- Status: partial: the tool exists; nothing makes it a standing gate.
- Score: value 3, effort S, risk low
- Decision: build

## C12. Guard 'it could be' path guess
Ideas: Fix the guard's "it could be" path guess; Show real paths in the guard's "it could be …" guess; Drop the guard's "it could be …" guess unless the path exists; Make the "it could be …" guess print only existing, whole paths
- Grounding: plugin/lib/fmguard.py:2156 prints 'not known before it runs: it could be PATH' for each guessed write target; `_possible` (fmguard.py:1881) already drops paths under an existing file. The guess exists so a target not yet created (a guarded file) is still judged (T-0374, T-0183).
- Status: false premise for 'print only existing paths': that would let a command write a not-yet-existing guarded file; only the wording is odd.
- Score: value 2, effort S, risk med
- Decision: skip (Filtering to existing paths opens a bypass; a rewording is cosmetic.)

## C13. Refusal message shape and safe rewrite
Ideas: Give every refusal one three-part shape: what, why, do; Show the refusal message with a one-line safe rewrite; Show the guard's exact passing rewrite beside each refusal; Wild: Dry-run sandbox preview for blocked commands
- Grounding: Messages are written per rule; some carry the rewrite (CHANGELOG Unreleased heredoc case: write it in one command, run it in the next). `fm guard try` prints the decision without running (plugin/lib/fmhooks.py:1041). No shared what/why/do shape.
- Status: partial
- Score: value 2, effort M, risk low
- Decision: skip (Cosmetic across many rules; no failing behaviour to test; worst messages get fixed one by one from friction.)

## C14. Replace guard regexes with a shell tokenizer
Ideas: Cross-check the guard against a real shell parser; Replace guard regexes with a small shell tokenizer; Replace regex scanning with a shell tokenizer shared by every guard rule
- Grounding: plugin/lib/fmguard.py is hand-tokenized (shlex plus word regexes, about 2000 lines, T-0158, T-0161, T-0370-T-0374); fuzzer escapes were closed in T-0669 and `fm bench --mutate` mutates the guard (fmcli.py:5396). T-1140 was about speed, not parsing.
- Status: partial: a rewrite is not a new capability.
- Score: value 2, effort L, risk high
- Decision: skip (L effort and high risk on the safety layer with thousands of fixtures; fuzz and mutate gates already find escapes.)

## C15. Guard fuzzer
Ideas: Wild: Guard fuzzer that mutates allowed commands to find bypasses
- Grounding: Seeded fuzz tests exist (CHANGELOG T-0669, fuzzer class 6); `fm bench --mutate --module fmguard.py` (fmcli.py:5396).
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (Already shipped.)

## C16. Recheck trigger for blocked and parked briefs
Ideas: Park the 11 externally blocked briefs with a recheck trigger; Give deferred briefs a revisit-by date that expires them
- Grounding: `fm task defer ID --until YYYY-MM-DD | "when PATH changes"` (plugin/lib/fmcli.py:4835-4840, T-0450/T-0958) re-offers a brief. State has 28 deferred briefs (23 with a revisit) and 6 blocked (T-0325, T-0335, T-0336, T-0337, T-0352, one more). `fm task block` takes no --until (fmcli.py:4828-4830).
- Status: partial: date and file-change triggers exist for defer; external needs (a binary installed, a login) have no trigger, and blocked tasks have none at all.
- Score: value 3, effort S, risk low
- Decision: build

## C17. Return receipts, welcome back, morning digest
Ideas: Wild: "Ask me nothing" ledger the user can audit on return; Show a one-line "welcome back" receipt at the first prompt after a gap; Say the day's end in one line: closes, near-misses, minutes saved; Wild: Turn the user's AFK stretch into a self-verifying "return receipt"; Draft the user's status update from closes (wild); Lead the return receipt with surprises, not successes; Make a morning digest the end of every contract
- Grounding: `fm away` and a session-start "Away" line after a 2 h gap (plugin/lib/fmaway.py, T-1155); `fm contract receipt` lists what closed, cost and more (T-1158); `fm todo` (T-1157); `fm digest`.
- Status: done: only ordering by surprise (103) is missing.
- Score: value 2, effort S, risk low
- Decision: skip (Shipped in T-1155, T-1157, T-1158; ordering is polish.)

## C18. Tick-box 'only you' page that executes ticks
Ideas: Wild: Make the final report answerable by ticking boxes; Run the user-only steps from one reviewed script; Wild: A tick-box "what only you can do" page that executes the ticks; Wild: Make the final report a tickable "only you" page that executes the ticks
- Grounding: `fm todo` lists user-only items with what to type (plugin/lib/fmcli.py:2863, T-1157). Grants (guard categories, logins, secrets) can only come from the user's own answer (rules/foreman.md).
- Status: false premise: executing ticks would grant what only the user may grant.
- Score: value 2, effort M, risk high
- Decision: skip (Cannot execute user-only steps without breaking the consent model; the list itself exists.)

## C19. Steer or kill a running contract by phrase
Ideas: Add a mid-run steer file the loop reads at each boundary; Let the user type a phrase to widen or narrow a running contract (wild); Wild: Steer a running contract with a plain phrase; Wild: Give the queue a "kill switch phrase" the user can type from a phone
- Grounding: User messages already steer: logged, typed and compiled to rules (fmcli.py:1761, T-1063, T-1042); `fm contract --until/--usd/--tokens` bounds a run (plugin/lib/fmcontract.py); `fm pause` stops everything (fmcli.py:5243); NOW: and TAG!: intake (fmcore.py:1943). A phone kill switch needs a remote surface.
- Status: partial: steering exists; a steer file is new; the phone path needs a device or login this machine lacks.
- Score: value 2, effort M, risk med
- Decision: skip (Existing steers and `fm pause` cover it; the phone part needs something this machine lacks.)

## C20. Small-model and local-model smoke
Ideas: Wild: Run a small-model smoke test of the whole discipline; Wild: Run the scripted tour on a small local model and map where it derails; Wild: Add a "cold small model" smoke path; Wild: Test the final report on a cold small model; Run fm children against a local OpenAI-compatible endpoint; Wild: Route all model traffic through a local proxy that Foreman owns; Run a no-network lane smoke on a stub model; Prove offline behaviour for every network verb
- Grounding: `fm demo` stubs claude itself and `fm release-check` runs it in a temp HOME (plugin/lib/fmdemo.py:152); `fm smoke` (plugin/lib/fmsmoke.py). No ollama or llama-server is installed (which finds none), so a real small-model run is impossible here.
- Status: partial: the stub no-network path is done; real-model variants need a model this machine lacks.
- Score: value 3, effort L, risk med
- Decision: skip (Needs a local model server that is not installed; the stub path already ships.)

## C21. Review measurement and history
Ideas: Measure the builder self-review and defect classes; Count review rounds per lane and show them; Wild: Run a replay of every past red review finding against each new lane diff; Gate measured claims on before/after numbers
- Grounding: Builders self-review as an adversary and say so (CHANGELOG Unreleased); defect classes confirmed in 30 days go into builder briefs (T-1164); past findings per lens go into reviewer briefs (plugin/lib/fmcli.py:4089, T-0743); close prints a Not-verified block. No count of review rounds per lane, no replay of old red findings against a new diff, no before/after gate for measured claims.
- Status: partial: the feedback exists; the counters depend on automatic finding records (C1).
- Score: value 2, effort M, risk low
- Decision: skip (Counters are only meaningful once findings are recorded automatically; revisit after C1.)

## C22. Real-path probe per surface
Ideas: Register a real-path probe per surface
- Grounding: `fm smoke` checks the product the way its user uses it, by kind (plugin/lib/fmsmoke.py:75-92: http, cmd, and more; T-0417, T-0460).
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (Already shipped.)

## C23. Fire-drill with a planted bad brief
Ideas: Wild: Fire-drill the discipline with a planted bad brief
- Grounding: Closest: `fm bench` replays finished tasks (fmcli.py:5375) and the guard fuzzers; no planted-brief drill.
- Status: new
- Score: value 2, effort M, risk low
- Decision: skip (Needs model runs to judge; no deterministic test.)

## C24. Drive resilience and the autonomy dial
Ideas: Wild: Bound the loop with a no-new-value stop; Break repeated-action loops on the main thread; Add one autonomy dial; Stop on graceful signals at safe points only; Run Foreman's drive as a headless daemon that works the queue between sessions; Resume the drive after a crash or limit hit
- Grounding: Loop stop and yield: `fm loop` (T-1057); repeated-action breaker (T-1150, plugin/tests/test_breaker.py); usage-limit waits, failover and restart (plugin/lib/fmserve.py:6, :29-31, :315); graceful SIGTERM and SIGHUP exits (plugin/lib/fmbus.py:548, T-0819); systemd units for a headless queue (fmserve.py:190); `fm autonomy` (fmcli.py:4402, T-0436).
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (All five exist.)

## C25. Git-state preflight and topology matrix
Ideas: Fence edit-time writes to files dirty before the drive started; Preflight the user's git state before any loop commit, merge or push; Fix a git topology matrix for commits and lane merges
- Grounding: `fm task finish --commit` commits only the task's files and leaves out files dirty at focus (CHANGELOG Unreleased, T-1177); staged-leak scan (fmcli.py:1315). No check for a rebase or merge in progress, a detached HEAD in the main checkout, or a dirty index before a loop commit or lane merge (fmlanes.py handles detached only at lane rm, :279).
- Status: partial
- Score: value 2, effort M, risk low
- Decision: skip (No observed incident; each case is hypothetical until a friction event names one.)

## C26. Context pack hygiene
Ideas: Stamp the map's age in every pack and refresh it first; Label every pack section by origin and fence the untrusted ones; Dedupe the context pack; Cut pack text at sentence boundaries and always keep DONE-WHEN; Tag each brief's origin and quote only the user's real words as the user's
- Grounding: The brainstorm pack is a text file the main session writes and `fm ideas --pack` reads (plugin/lib/fmideas.py:680); code does not build it, so stamps, dedupe and cuts would be a lint on prose. One map line goes into session context (T-0215, CHANGELOG:724); inbox text is fenced as untrusted (T-1165).
- Status: partial
- Score: value 2, effort M, risk low
- Decision: skip (The pack is model-authored; a lint adds little.)

## C27. Pane delight and visual polish
Ideas: Celebrate a hard-won green with a plain-words close line; Give every lane a stable callsign shown in pane, ledger and commit trailer; Print a last-frame keepsake when the pane exits; Add a first-time capability toast, once per feature; Fade quiet pane cards by recency instead of collapsing them; Wild: Hum a "build weather" glyph in the statusline; Add a Focus view: one task, one sentence, one bar; Fade the key hints once the keys have been used; Flash a card once when it changed while you weren't looking; Show "build weather" as a day-part palette; Wild: Show lanes as a construction-site scene; Wild: Write a weekly yearbook page of superlatives; Wild: Let the user pin a moment into a "good day" reel
- Grounding: mods/foreman-ui (hooks/rows.tsx, register.tsx, tests/*.test.tsx, tools/shot.py): colourblind palette and history scrubber (T-1081), step band (T-1154), stage rail (T-0909); fade and flash exist in part (T-0938, T-0706).
- Status: partial
- Score: value 2, effort M, risk low
- Decision: skip (Taste items with no failing behaviour; each needs a visual review loop (shot.py plus Spectacle).)

## C28. Web UI features
Ideas: Add inline diff comments in the web UI that become lane steers; Add a command palette and deep links to the web UI; Wild: Show a repo map page with hotspot, ownership and task overlays; Stamp CLOSED on the web card with a proof unroll; Add a plan editor to the web UI; Make the web UI survive restarts and version skew
- Grounding: The `fm serve` page is plugin/lib/page.html (213 lines) with plugin/lib/smoke_web.cjs; the Ctrl+K palette lives in the separate Desktop app (CHANGELOG:677, T-0328).
- Status: partial: the palette exists in the Desktop app, not this repo's page.
- Score: value 2, effort L, risk med
- Decision: skip (L effort, needs a browser to verify, no failing behaviour.)

## C29. Plain-language messages and commit subjects
Ideas: Write error messages in the user's recent vocabulary; Rewrite task commit subjects into plain sentences; Print plain-language failure explainers for the top 10 gate failures
- Grounding: Gate failure explainers exist in part (T-0855, plugin/tests/test_gate_friction.py); every close prints a Not-verified block (plugin/tests/test_not_verified.py); commit subjects come from `fm task finish --commit`.
- Status: partial
- Score: value 2, effort M, risk low
- Decision: skip (Subjective, no testable contract; no user-vocabulary data source.)

## C30. `fm doctor --fix`
Ideas: Add `fm doctor --fix` for the safe findings
- Grounding: plugin/lib/fmcli.py:5331-5337: doctor has --repair (crash-truncated objects, T-0268), --restore-state, --accept-supply, -v; the /foreman:doctor skill fixes by hand. No single safe-fix flag.
- Status: partial
- Score: value 3, effort S, risk low
- Decision: build

## C31. New close gates and stack packs
Ideas: Gate public API breaks at close; Ship migration and infra guard packs; Gate UI projects on visual regression; Add an accessibility gate for web projects; Run framework upgrade runbooks; Write tests for uncovered changed lines; Prove dead code before deleting it; Generate a devcontainer and bootstrap script from the map; Turn ADRs into executable checks
- Grounding: Gates come from `fm map` and CI files (plugin/lib/fmmap.py:113-119); `fm deps --capture` queues major-version upgrades (T-1166); `fm lib` stack cards (plugin/lib/fmlib.py). No coverage, API-break, a11y or visual gate (grep finds none).
- Status: new
- Score: value 2, effort L, risk med
- Decision: skip (Each needs a per-stack tool this machine may lack and has no demonstrated need; stack cards carry the advice.)

## C32. Gates derived from CI, gate timing
Ideas: Derive gates from CI and pre-commit config; Wild: Keep a flaky-host mode that fingerprints load at each gate failure; Compare each gate run with its usual time
- Grounding: CI commands mirrored into gates (plugin/lib/fmmap.py:113-119); a flaky first failure is rerun (fmcli.py:3477); a gate far over its median time is flagged (fmcli.py:3826); fail-fast order by failure odds (fmcli.py:3842).
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (All three exist.)

## C33. State durability and process identity tests
Ideas: Enumerate crash points in every state write; Count subprocesses per hook, not milliseconds; Preserve unknown fields on read-modify-write; Detect lock re-entry and ordering in tests; Identify live processes by pid, start time and boot id; Test hook stdout purity under hostile conditions
- Grounding: write_atomic (plugin/lib/fmcore.py:609); lock re-entry tests (T-1099); pid plus /proc start time (plugin/lib/fmideas.py:100-111, T-1003); hook stdout purity (T-0783, plugin/tests/test_hooks.py:181); brief meta keeps unknown fields.
- Status: done: only a crash-point enumerator and a subprocess count per hook are missing.
- Score: value 2, effort M, risk low
- Decision: skip (Mostly shipped; the two gaps have no observed failure.)

## C34. Subdirectory and environment matrix tests
Ideas: Run the whole suite from a subdirectory and a symlinked path; Replay archived real state from every release; Run the suite under a time-warped clock; Wild: Run the whole gate suite once with all state deleted
- Grounding: Real bug class: `fm lease take` with a relative path from a subdirectory (CHANGELOG Unreleased, T-1148). `fm release-check` already runs doctor and demo in a temp HOME (plugin/lib/fmdemo.py:152); tests/test_core.py and test_agents.py touch symlinks.
- Status: partial: fresh state is covered; subdirectory and symlinked-path runs of the verbs are not.
- Score: value 3, effort S, risk low
- Decision: build

## C35. Verb, flag and skill pruning by usage
Ideas: Do less: freeze round 4 to deletions and wiring only; Leave a tombstone when a verb is deleted; Give every new flag an expiry release; Wild: Run a weekly "one thing less" report; Rank skill descriptions by use and trim the unused from the session listing; Shrink the skills tree by injection receipts; Prune flags by usage, not just verbs; Count concepts in the README and cap them at a fixed number; Delete a verb's tests, docs and help entry as one unit
- Grounding: `fm tidy` prunes state (plugin/lib/fmtidy.py); `fm repeats` finds repeated work (plugin/lib/fmrepeats.py); help tiers are tested one command each (T-1144, tests/test_help.py); skill routing is plugin/skills/routing.json; verb pruning by usage came with the T-0679 and T-0680 milestones.
- Status: partial: flags and skill descriptions are not tracked by use.
- Score: value 2, effort M, risk low
- Decision: skip (No usage ledger for flags; deletions without a defect are churn.)

## C36. Retire never-failing tests
Ideas: Retire tests that have never failed and cover nothing unique
- Grounding: `fm bench --mutate` mutates the guard (fmcli.py:5396); 196 test files in plugin/tests; test_suite_hygiene.py exists.
- Status: partial
- Score: value 2, effort M, risk low
- Decision: skip (Needs mutation runs per test; slow, and deleting tests is risky.)

## C37. Off switch and what-now
Ideas: Keep a single "Foreman is off" switch that proves it is off; Wild: Make `fm` print only the next one command when asked "what now"
- Grounding: `fm pause` (fmcli.py:5243), plugin disable (fmhooks.py:1116), `fm next` prints the one next action (fmcli.py:5246, T-1157).
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (Already shipped.)

## C38. One SQLite file for all state
Ideas: Wild: Store all machine state in one SQLite file
- Grounding: Only the graph is sqlite (state/projects/*/graph.sqlite, T-0707). Briefs, ledger and meta are files by design: git-syncable (`fm sync`) and hand-recoverable (`fm doctor --repair`).
- Status: false premise: the file format is the recovery and sync story.
- Score: value 1, effort L, risk high
- Decision: skip (Would break `fm sync` and crash repair.)

## C39. Intent compiler and question-answering `fm`
Ideas: Wild: Make `fm` answer a question, not a verb; Make `fm do` a closed-loop intent compiler
- Grounding: /foreman:intake and `fm intake` parse tags and plain requests (plugin/lib/fmcore.py); `fm recall --ask` answers questions over project history (plugin/lib/fmrecall.py).
- Status: partial
- Score: value 2, effort L, risk med
- Decision: skip (Needs model parsing in the CLI; intake and recall cover it.)

## C40. Cost, model choice and budget edge
Ideas: Step down to cheaper capacity at the budget edge; Pick the cheapest model per lane with a measured fallback
- Grounding: `fm budget` caps spend (plugin/lib/fmbudget.py, T-0227); `fm lane brief` accepts a model (fmlanes.py:574); `fm cost`.
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (Shipped.)

## C41. Queue hygiene and why-not
Ideas: Preview a contract against the queue; Score the mission's pillars at the end; Merge overlapping open briefs; Demote stale "active" tasks at session start; Answer "was this already considered?" with `fm why-not "<idea>"`
- Grounding: Queue preview (plugin/tests/test_queue_preview.py), mission pillars (plugin/lib/fmmission.py), related-brief detection (plugin/lib/fmrelate.py), stale active demotion (test_stale.py), near-dropped warning at capture (fmcli.py:283, fmrecall.nearest_dropped), `fm recall`.
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (Shipped.)

## C42. Round retros and adoption probes
Ideas: Attach a post-ship adoption probe to each shipped feature; Write a three-line round retro that seeds the next pack; Wild: Pick the next lens by neglect, not by list; Wild: Replay the whole round's ideas against a "taste twin" built from the steers
- Grounding: `fm loop yield` records a round (T-1057); thin categories are reported in the ideas tally; `fm taste` and the court contest (fmcli.py:5450, T-0242); `fm repeats`.
- Status: partial
- Score: value 2, effort M, risk low
- Decision: skip (Reports on reports; no testable defect.)

## C43. Builder notes, lane preflight and spikes
Ideas: Wild: Leave a decaying sticky note on files a builder was nervous about; Add a "lane env doctor" run at lane creation; Keep a "noticed, didn't touch" margin file for builders; Run a time-boxed spike lane that self-discards; Pre-flight every brief by dry-building it in a throwaway lane
- Grounding: `fm lane brief` warns on conflict-prone scope (T-1161) and lists defect classes (T-1164); `fm draft` drafts on a throwaway branch (T-1062); lane race (T-1137).
- Status: partial
- Score: value 2, effort M, risk low
- Decision: skip (The real builder problem is the own-fm issue, a separate cluster.)

## C44. Racing builders
Ideas: Wild: Race two cheap builders on a hard task and keep the one whose proof passes
- Grounding: `fm lane race T`, `--score`, `fm lane pick W` (CHANGELOG 1.2.32).
- Status: done
- Score: value 1, effort S, risk low
- Decision: skip (Shipped.)

## C45. Code intelligence at edit time
Ideas: Resolve a symbol rename across the repo through LSP; Show a live blast-radius preview before each edit
- Grounding: `fm graph blast PATH` gives dependents, co-change and linked tests (CHANGELOG:389, T-0707); no edit-time preview and no LSP use in plugin/lib.
- Status: partial
- Score: value 2, effort L, risk med
- Decision: skip (An edit-time preview would sit on the hot hook path (72 ms median).)

## C46. PR and branch readability
Ideas: Wild: Offer GitButler-style virtual branches for the user's own dirty tree; Walk through a PR in narrated reading order
- Grounding: `fm pr ID --post` renders and posts the description (T-1167).
- Status: partial
- Score: value 2, effort L, risk low
- Decision: skip (Large and subjective.)

## Tally
- Clusters: 46; ideas: 195 (all placed).
- done: 11
- false premise: 2
- false premise for 'print only existing paths': 1
- new: 4
- partial: 28
- Decision: build 10, skip 36
- Build: Auto-record reviewer findings; Guessed verbs and flags just work; Headless review and ideas for the unattended drive; Lane builders run their worktree's own fm; Release as one resumable verb; Guard refusal workbench (`fm guard mine`); Premise check before guard tasks; Recheck trigger for blocked and parked briefs; `fm doctor --fix`; Subdirectory and environment matrix tests

## Intake
FEATURE: A small static alias table (task list/ls/all to the queue view, task get/view/info to task show, and similar common guesses) runs the real command and prints one quiet "(ran `fm ...`)" line; unknown guesses still get the nearest-match error.
DONE-WHEN: a new test in plugin/tests/test_cli.py runs `fm task ls` and `fm task list` and sees exit 0 with the "(ran" note, and `fm task nonsense` still exits non-zero with its error.
FEATURE: At SubagentStop for an fm-reviewer, parse its `## lens: ...` sections and ranked findings out of last_assistant_message and log one `finding` event per finding for the active task, so reviewer findings are recorded without a hand-typed `fm task finding`.
DONE-WHEN: a new test in plugin/tests (python3 plugin/tests/run.py -k reviewer_findings) feeds subagent_stop a sample reviewer message and sees one finding event per finding with the right lens and severity, and none for a non-reviewer agent.
FEATURE: `fm task finish` on a task whose diff touches plugin/lib/fmguard.py requires a recorded `fm replay --cases` run on that tree with no drifted case, else it names the command to run.
DONE-WHEN: a new test in plugin/tests/test_close_gates.py sees finish refused for a guard-file diff without the recorded run and accepted with it.
FEATURE: `fm task block` and `fm task defer` accept `--until "when CMD succeeds"` (for example `command -v codex`), and `fm next` names the task again once that command exits 0.
DONE-WHEN: a new test in plugin/tests/test_stale.py blocks a task with `--until "when true"` and sees `fm next` re-offer it, while `--until "when false"` stays quiet.
FEATURE: `fm doctor --fix` applies only the findings that already have a safe repair (regenerate status views, the --repair and --restore-state moves) and lists every finding it left for a person.
DONE-WHEN: a new test in plugin/tests/test_doctor.py seeds a stale status view and a truncated brief, runs `fm doctor --fix`, and sees the view regenerated and the second finding listed as unfixed.
FEATURE: A test runs the path-taking verbs (lease, edit, evidence, check, focus) from a subdirectory and through a symlinked checkout and holds each to the same result as from the repo root.
DONE-WHEN: `python3 plugin/tests/run.py -k subdir_matrix` passes with each verb run from root, a subdirectory and a symlink.
FEATURE: `fm audit run ID` runs the audit lenses as headless `claude -p` reviewers over the frozen diff brief of `fm audit prep`, bounded by `fm budget` and `fm contract`, and records the lens verdicts and findings.
DONE-WHEN: a new test (python3 plugin/tests/run.py -k audit_run) with a stub claude shows `fm audit run T-x` records one verdict per lens, refuses when the budget is spent, and does not run once `fm contract` has expired.
FEATURE: `fm guard mine` lists the last N days of guard refusals with their full command, today's replay verdict, and a label (rewritten and passed, retried unchanged, or abandoned) taken from the next events of the same session.
DONE-WHEN: a new test in plugin/tests/test_guard_cases.py seeds guard_block events plus follow-up events and sees `fm guard mine --json` return each refusal with the right label.
FEATURE: When `fm` is run from inside a linked git worktree whose own plugin/bin/fm exists, bare `fm` re-executes that copy (one cheap `.git`-file check, skipped outside worktrees), so a builder tests its own flag and guard changes.
DONE-WHEN: a new test in plugin/tests/test_lanes.py makes a worktree of a temp repo with a marker verb in its plugin copy, runs the main `fm` from inside it and sees the marker verb work, while the same command from the main checkout is unchanged.
FEATURE: `fm release VERSION` chains release-check, canary, the release.py steps and `fm round close` as named steps, writes a checkpoint after each, and `--resume` continues from the first unfinished step; `--dry-run` only prints the plan.
DONE-WHEN: plugin/tests/test_release.py runs `fm release 9.9.9 --dry-run` in a temp repo and lists every step, and a run stopped after step 2 continues from step 3 with `--resume`.
