# Brainstorm round 2 — 2026-10-14: improvements on top of round 1 (T-0818)

437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run's ideas) in 29 capability clusters, each grounded in the code. Every idea is listed under its cluster. Marks: build (round 2), done, later (inbox), skip.

## [build] feature-usage-telemetry — Feature usage and lifecycle: fire counters, dormant-feature offers, lit/locked map, soft-launch, auto-toggles, unship, kill-switch
value 3 · effort S · risk low · which fm verbs and hooks are never used is the evidence the slim-down milestone (T-0794) lacks
Exists: state/events.jsonl logs every tool call with its command and every hook's ms (28k tool, 27.6k hook_ms events); no report of unused verbs
Premise: false in part: no new counter is needed, the event log already holds it
First slice: one-off analysis of events.jsonl (verbs and hooks used in 30 days vs registered) attached to T-0794; no new command
Ideas (25):
- Predict which shipped items the user will drop — near T-0435 (done): fm friction reads every project's friction, labelled by pro… (Round 1)
- Show a lit/locked feature map in `fm doctor` — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 1)
- Audit what round 1 shipped but nobody is using — near T-0031 (done): Fm audit prep: --note '<text>' adds round/slice-specific fo… (Round 1)
- Record proof-of-life per Claude Code integration — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 1)
- Offer one-yes opt-ins backed by the user's own telemetry — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 1)
- Generate FEATURES.md from the doctor manifest — near T-0785 (done): fm doctor names the Foreman features the installed Claude C… (Round 1)
- Ship each round-1 feature with a fire counter — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 1)
- Wild: Ablation switches for every round — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 1)
- Wild: a feature kill-switch that auto-trips on repeated silent failures (Round 1)
- Let toggles flip themselves from evidence and tell the user once (Round 1)
- Replace "known gaps" prose with a doctor probe — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- End every recursive round by deleting the least-used round-1 feature — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- Track feature escape rate: hotfixes within 24h of the feature — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 1)
- Convert deferred clusters into evidence-accruing promotions (Round 1)
- Give every shipped round-1 feature a fire counter — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 2)
- Light up dormant features with a one-line "ready when you are" offer — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 2)
- Add a round-1 fire counter and `fm doctor --alive` probe — near T-0672 (done): Milestone: Features — Guard and safety (Round 2)
- Add a doctor probe that names the one thing to fix, not a report — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 2)
- Wild: Make each feature a removable bundle with `fm unship <feature>` (Round 2)
- Build a feature manifest that runs Foreman's own plumbing — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Add a generic shadow mode that promotes a feature after N agreeing runs — near T-0682 (done): Milestone: Features — Verification and product checking (Round 2)
- Wild: Offer ablation week as a one-key toggle (Round 2)
- Wild: Make the idea pile queryable by `fm ideas ask "did we cover X"` so the user and children stop re-reading it — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 3)
- Wild: Fail any feature that can't be explained in one generated sentence — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 3)
- Soft-launch round features that expire to off unless ticked (Round 4)

## [build] compact-spill-store — Compact output spill store: recovery stubs, slice reads, lifetime, 0600/redaction/size cap
value 3 · effort S · risk low · an uncapped spill file can fill the disk on a runaway output
Exists: stub carries the path; 0700/0600 files; tidy prunes after 7 days; no size cap
Premise: false in part: recovery already works by Read with offset; unredacted text equals what transcripts already keep
First slice: cap the saved full text in plugin/hooks/compact (keep head and tail, mark the cut)
Ideas (7):
- Add `fm out` and put its exact command in every compact stub — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Round 1)
- Keep compact-output pointers alive as long as anything can cite them — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 1)
- Lock down the compact-output store (0600, redact on write, size cap) — near T-0672 (done): Milestone: Features — Guard and safety (Round 2)
- Redact and restrict the compact-output spill store (Round 2)
- Make compact-output stubs self-recoverable — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 2)
- Spill-store with slice reads for big outputs — near T-0783 (done): Big Bash outputs reach the model as head, tail and failure … (Round 3)
- Give each stub a one-line recovery command and keep the spill alive while cited — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Deepened: tokens)

## [build] metric-reader-roundtrip — Writer-owned shapes and reader round-trip tests, fuzzing, shared scenario builder, input normalisation
value 3 · effort S · risk low · a cheap test that catches real crashes when fm output is piped into head or a closed reader
Exists: BrokenPipe/isatty handled in only a few modules (fmwatch, fmbus, fmsession)
Premise: ok: a sweep of read-only verbs with closed stdin and a closed stdout pipe is missing
First slice: plugin/tests/test_verbs_nopipe.py: read-only verbs with stdin=DEVNULL and stdout closed early; assert no traceback
Ideas (12):
- Generate reader tests from real writer output — near T-0682 (done): Milestone: Features — Verification and product checking (Round 1)
- Canonicalise every path once, then property-test the spellings — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 2)
- Route every list and field input through one coercion function (Round 2)
- Pair every metric reader with a writer-output round-trip test — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Normalise every id, list and path argument in one place — near T-0707 (done): Frontier 07 — Knowledge graph (Round 2)
- Run a metric-reader round-trip suite against real writer output — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Make the writer own every persisted string shape — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Fuzz every state writer with hostile text — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 4)
- Test every verb under no-tty, closed-stdin, and BrokenPipe (Round 4)
- Make settings strict with did-you-mean — near T-0674 (done): Milestone: Features — Observability, replay and trust (Round 4)
- Build tests from one shared scenario builder — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 4)
- Pair every shipped hook with a counterexample the model must not trigger — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)

## [done] vetoes-and-by-design — User vetoes and by-design register fed to guard, intake and briefs
value 2 · effort M · risk low · covered by vetoes
Exists: fm vetoes (fmcli.py:369), recorded from 'never X' (fmhooks.py:510), checked at capture and edit; fmideas proposes vetoes
Premise: false: the by-design register exists as vetoes
Ideas (11):
- Write a by-design register the guard and intake consult — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 1)
- Wild: Auto-write a "by design" register from the user's drops — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 2)
- Wild: Let the user say "keep it like this" about a behaviour — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: Keep a hot "second opinion" session that reads only the user's words — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 3)
- Put the user's vetoes into every agent and lane brief — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 3)
- Check the user's factual claims against the ledger at intake — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 4)
- Attach hindsight receipts to your own steers and drops (Round 4)
- Gate every self-edit on "would this have changed a real past decision?" — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Wild: Let the user hold one "veto token" per day that reverts any Foreman-initiated change, no questions — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 4)
- Inject the user's vetoes and steers into every brief with a "contradicts" check — near T-0680 (done): Milestone: Features — Self-improvement and learning (Deepened: agents)
- Run a user-voice shadow that reads only the user's words and grades the close — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Deepened: agents)

## [later] brainstorm-pack — Brainstorm pack: cluster summaries instead of idea pile, lens slicing, saturation scaling, delta-only, reproducibility
value 3 · effort S · risk low · scaling lenses needs lens_rates data on which lenses go dry
Exists: shared-prefix pack (fmideas.py:126), lens_rates (:172), --seen
Premise: ok: pile bloat is real; pruning exists
Ideas (21):
- Shrink "ideas so far" to cluster summaries for each brainstorm — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 1)
- Wild: A pre-round "interview the transcript" pass — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 1)
- Prune the brainstorm pack: archive unseen ideas and print clusters, not lines — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 1)
- Lint context packs for duplicated blocks before any child sees them — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Shorten and clean the idea pile before every brainstorm — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 2)
- Hedge slow read-only children with a second cheaper attempt — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 2)
- Give each lens a filtered slice of the pack — near T-0707 (done): Frontier 07 — Knowledge graph (Round 3)
- Brainstorm only the delta: feed children round N's shipped diff plus open friction, not the full idea pile — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 3)
- Wild: Hedge each slow read-only child with a second cheaper attempt and keep the first answer back — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 3)
- Send the filter, not the pile (Round 3)
- Scale lens count down as the pile saturates — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 3)
- Drop the don't-repeat list from child prompts and dedupe afterwards — near T-0708 (done): Frontier 08 — Orchestrator control plane (Round 3)
- Prune the "ideas so far" list to cluster summaries — near T-0780 (done): Audit findings reach the host's review UI: fm audit prep as… (Round 3)
- Fix the pack builder's own bloat — near T-0710 (done): Frontier 10 — Milestone work compiler and merge train (Round 4)
- Rebuild the context pack builder so it stops polluting its own input — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 4)
- Write a reproducibility manifest for each brainstorm — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Run an amnesiac round and count independent rediscoveries (Round 4)
- Build the brainstorm pack from a budgeted, prefix-stable template — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Deepened: tokens)
- Send each lens only the slice of the pack it needs — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Deepened: tokens)
- Replace the "ideas so far" list with cluster summaries plus a nearest-neighbour check afterwards — near T-0682 (done): Milestone: Features — Verification and product checking (Deepened: tokens)
- Scale the number of lenses to the saturation of the pile (Deepened: tokens)

## [later] round-loop-automation — Round loop automation: fm recurse, fm round ledger/close/revert, round briefs, names, tags, standing 'etc.' mandates
value 3 · effort M · risk low · needs evidence rounds are a stable unit; mission/ideas loop works without a ledger
Exists: no fm round/recurse verb; fm mission + fm ideas --rounds/--seen run the loop (fmcli.py:4201,4216)
Premise: unclear: 'near done' tags are word overlap; a round is a brainstorm pass plus its tasks
Ideas (21):
- Run `fm recurse` for open-ended "keep improving" mandates — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 1)
- Generate the "Round N shipped" brief from the ledger — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Revert a whole round with `fm round revert N` — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Wild: Have Round 3 waiting at breakfast — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Wild: queue the next round automatically from what the user said "etc." about — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 1)
- Add `fm round`, a recursive-improvement ledger with a scorecard and revert — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 1)
- Wild: Turn "etc. etc. etc." into a standing, budgeted mandate (Round 2)
- Wild: Wake to a finished Round 3 on the breakfast page — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Round 2)
- Wild: Add an ambition dial for rounds (`fm ambition 1-5`) — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 2)
- Wild: Mark round boundaries as git tags and build the brief from `git log round-N..` — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 2)
- Close each round automatically with `fm round close` — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Wild: Report the "pit-stop" lap time between rounds — near T-0167 (done): fm run --parallel N: independent queued tasks at once, each… (Round 3)
- Wild: Echo what "etc." means, then proceed unless vetoed (Round 3)
- Name each round, and put the name on the title and tag (Round 3)
- Hold a round-close checklist as data, so "recursive" is a procedure — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: Let a night lane write the next round's brief from what the user said "etc." about — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 3)
- Add a stage-pipelined queue: plan N+1 and review N−1 while N builds — near T-0710 (done): Frontier 10 — Milestone work compiler and merge train (Round 3)
- Offer a hands-off weekly slot for the "etc." mandate (Round 4)
- Run a sweep round before any new brainstorm — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Make every recursive round net-zero in surface (wild) — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Wild: Run a "Foreman Sabbath" that deletes before it builds — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 4)

## [later] mail-monitor-arming — Mail monitor arming proof and wake delivery receipts: canary, echo, idempotency, degrade ladder
value 3 · effort M · risk med · a receipt signal needs a Claude Code event; the manual live check stands
Exists: fmbus watch/record_pid/wake/heartbeat; live arming verified once in this session (fresh interactive session in tmux started fm bus watch and resolved its id)
Premise: ok, but no hook shows Claude Code delivering a monitor line
Ideas (20):
- Probe whether the mail monitor really armed in this session (Round 1)
- Run a live arming canary for the mail monitor (Round 1)
- Confirm the mail monitor armed, with a tiny dot and a first-delivery line (Round 1)
- Verify the mail monitor in a real interactive session — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 1)
- Prove the mail monitor armed with a first-turn echo receipt (Round 1)
- Require a delivery ack on every monitor wake, or escalate — near T-0708 (done): Frontier 08 — Orchestrator control plane (Round 1)
- Merge wake, push and title into one attention emitter (Round 1)
- Arm the mail monitor by resume, and prove it (Round 1)
- Make `fm bus watch` event-driven and reap orphaned watchers — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 1)
- Wild: Replace wake-up polling with a compare-and-save "nothing changed" heartbeat (Round 1)
- Greet the monitor's first delivery — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 2)
- Stream mail to the monitor as a pointer, not the body — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 2)
- Give every wake path a delivery receipt, then stop trusting unreceipted ones — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 2)
- Test the arming of every plugin monitor against the real CLI at install time — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 3)
- Give every wake path a delivery receipt — near T-0708 (done): Frontier 08 — Orchestrator control plane (Round 3)
- Prove the mail monitor armed, once, loudly (Round 4)
- Split mail into wake and piggyback lanes (Round 4)
- Unify arming proof into one liveness ledger — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: liveness)
- Degrade wakes along a ladder, automatically (Deepened: liveness)
- Stamp each wake with an idempotency key (Deepened: liveness)

## [later] compact-output-rollout — Compact output rollout: shadow mode, fetch-back gating, per-command-family opt-in, preview on worst output, digesters
value 3 · effort M · risk med · wait for real use after the user's yes
Exists: opt-in hook + fm compact-output on/off/status (fmsetup.py:207); tidy prune
Premise: unclear: shadow mode and per-family gating need fetch-back data that doesn't exist yet
Ideas (23):
- Run compact output in shadow mode before asking for a yes (Round 1)
- Report which of the user's own commands produce the biggest outputs — near T-0682 (done): Milestone: Features — Verification and product checking (Round 1)
- Re-fetch tripwire for compact output — near T-0811 (done): Fm tidy prunes state/outputs/<session>/ (compact-output's f… (Round 1)
- Shadow-mode compact output with a one-line ask — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Preview compact output on your own worst output before asking for a yes — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Coach shorter forms from the user's own `fm` history — near T-0781 (done): Sessions are named after their task: SessionStart and UserP… (Round 1)
- Make compact output expandable, and gate enabling it on measured re-fetches (Round 1)
- Run compact output in shadow first, then ask once — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Make compact output provably lossless for failures — near T-0783 (done): Big Bash outputs reach the model as head, tail and failure … (Round 1)
- Shadow-run compact output, then switch it on from the measurements — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 1)
- Run compact output in shadow first and enable it per command family from measured fetch-backs — near T-0682 (done): Milestone: Features — Verification and product checking (Round 1)
- Ship runner-specific failure digesters with golden tests — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 1)
- Run compact output as a one-week shadow, then offer the yes with evidence — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 2)
- Wild: Preview compact output on the user's own worst command — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Turn compact output on for a named noisy-command list and remove the global question — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 2)
- Shadow-mode compact output with a measured fetch-back rate — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 3)
- Offer compact output on the user's own worst real output — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Run compact output inside lanes first — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 4)
- Let a cheap child digest big outputs and whisper only anomalies — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 4)
- Run compact output in shadow mode and log what it would have cut — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Deepened: tokens)
- Gate the compact-output switch on measured fetch-backs, per command family (Deepened: tokens)
- Wild: Let the model ask for a command's output ahead of time ("output contracts") — near T-0672 (done): Milestone: Features — Guard and safety (Deepened: tokens)
- Wild: Grow a per-project "noisy command" dictionary from the ledger and ship it as a shareable file (Deepened: tokens)

## [later] sensitive-and-redaction — Sensitive repo inference, fail-closed native tools, page redaction and zero-network proof
value 3 · effort M · risk med · auto-inference could guess wrong; first learn which repo signals match the user's flags
Exists: fm sensitive on|off (fmcli.py:2194); outward gate fails closed (T-0821); fm page redaction
Premise: ok: no inference of sensitivity
Ideas (6):
- Infer repo sensitivity and say why (Round 1)
- Fail closed on unclassified native tools in sensitive repos — near T-0784 (done): In a sensitive repo, Claude Code's outward tools (Artifact,… (Round 1)
- Property-test `fm page` redaction — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 1)
- Prove `fm page` makes zero network requests — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 2)
- Key project identity by repo identity, not path — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 4)
- Budget the `fm page` catalogue — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 4)

## [later] child-salvage — Child failure handling: typed partial results, salvage, continue, preflight, stalled kill
value 3 · effort M · risk med · needs a count of children hitting the cap first
Exists: fm run stall resume (fmserve.py:707); --max-budget-usd and maxTurns; no partial-result salvage
Premise: unclear: no count of capped children yet
Ideas (10):
- Salvage children that die on budget or turn limits — near T-0676 (done): Milestone: Features — Performance and cost (Round 1)
- Hand back a typed partial result when a child hits `--max-budget-usd` — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 1)
- Return a typed partial result when a child hits its budget or turn cap — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 2)
- Continue a turn-limited agent instead of respawning it — near T-0019 (done): Drive lets the turn end while background agents or commands… (Round 3)
- Give every sub-agent a delegation slip — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 3)
- Hold a lane huddle before parallel launch — near T-0174 (done): Parallel runs clean up after a failure, re-check main befor… (Round 3)
- Preflight an agent's required tools before spawning it — near T-0208 (done): fm ideas marks each new idea with the finished task it most… (Round 3)
- Kill and salvage stalled subagents — near T-0693 (done): Milestone: Intelligence — Reasoning and thought process (Round 3)
- Salvage and resume capped children from their own transcript — near T-0693 (done): Milestone: Intelligence — Reasoning and thought process (Deepened: agents)
- Preflight a child's tools, budget and cwd before spawning — near T-0276 (done): fm second: one primitive for independent second reads — riv… (Deepened: agents)

## [later] hook-latency — Hook latency: shell prefilters, async recording, lazy startup, hook-time ledger, single emitter
value 2 · effort M · risk med · needs a bench result naming a hook as a top cost
Exists: doctor latency/SLO probes (fmdoctor.py:110-154), bench_hooks
Premise: ok: measured and gated
Ideas (17):
- Shed optional hooks under load — near T-0805 (done): The hook benchmark judges by CPU time when the machine is b… (Round 1)
- Replace Python spawns on size-gated PostToolUse hooks with a shell prefilter (Round 1)
- Wild: Add a shell-level guard fast-path for provably read-only commands — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 1)
- Make the edit-time test sentinel out of `fm check --affected` — near T-0682 (done): Milestone: Features — Verification and product checking (Round 2)
- Bench the whole hook chain per tool event — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 3)
- Mark hooks that run inside Foreman's own children — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 3)
- Gate bench on a replayed concurrent hook trace — near T-0805 (done): The hook benchmark judges by CPU time when the machine is b… (Round 3)
- Wild: Run a hook "diet week" shadow where each hook is disabled in turn on a throwaway lane (Round 3)
- Measure the real hook tax per turn from CC's own timing — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 3)
- Short-circuit non-Foreman projects in one stat call — near T-0708 (done): Frontier 08 — Orchestrator control plane (Round 3)
- Run non-gating recording hooks as async — near T-0671 (done): Milestone: Features — Autonomy and the user (Round 3)
- Make `fm` startup lazy: import only the verb's module — near T-0676 (done): Milestone: Features — Performance and cost (Round 3)
- Wild: Warm hot-spare headless child per project (Round 3)
- Route all hook stdout through one validating emitter (Round 4)
- Emit every hook result through one helper — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 4)
- Hibernate idle projects to guard-only (wild) — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 4)
- Add a hook-time ledger that outlives bench — near T-0676 (done): Milestone: Features — Performance and cost (Round 4)

## [skip] round-user-summary — User-facing round summaries: what changed for you, what to ignore, one-question closes, strips and celebrations
value 2 · effort S · risk low · a 'what changed for you' line belongs in the final reply, not a command; no evidence of need
Exists: fm digest; fm page board
Premise: unclear: mostly celebration/novelty items
Ideas (21):
- Wild: Celebrate subtraction with a net-lines-deleted flourish (Round 1)
- Wild: Turn a round into a one-minute "what got better" strip — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 1)
- Wild: show a round-delta arrow in the band (Round 1)
- Offer a one-line "what changed for me" on every round close — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 1)
- Ask the user one question about round 1 at the end, with a default — near T-0364 (done): Foreman keeps working while background jobs run, plans and … (Round 2)
- Report round 1 in terms of what the user feels — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 2)
- Wild: Hold a "stranger's first ten minutes" replay with a cold child — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 2)
- Celebrate subtraction (Round 2)
- Wild: A quiet "queue zero" moment (Round 2)
- Wild: Let a round close with five yes/no toggles and nothing else (Round 2)
- Wild: Launch a first-ten-minutes stranger test for installs (Round 2)
- Hand over a single-screen "decide these 3 things" at round start (Round 3)
- Wild: Say "nothing changed for you" when nothing did (Round 3)
- Wild: Hold a "stranger test" for each round's user-visible surface — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Say what round 1 changed for you in three lines — near T-0262 (done): Smarter nudges: already-covered requests, decision revisit … (Round 4)
- Wild: Preview a round as a one-minute before/after strip — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 4)
- Pause a round for a one-line question with a default — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 4)
- Have a stranger read the round's commits and describe the product — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 4)
- Report "what you can now ignore" at round close — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 4)
- Wild: Give each round a one-page "what you'd notice" strip, built from before/after commands on throwaway fixtures — near T-0678 (done): Milestone: Features — Releases and delivery (Round 4)
- Show a "needs from you" manifest at plan time — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)

## [skip] attention-channels — Attention emitters: push, sessionTitle, return cards, sensitive-repo no-cloud path, quiet hours, ntfy
value 2 · effort S · risk low · remaining items are polish with no measured need
Exists: sessionTitle, Stop-hook PushNotification ask (fmhooks.py:1696), outward gate, statusline
Premise: ok: core exists
Ideas (19):
- Make sessionTitle a return card on resume — near T-0781 (done): Sessions are named after their task: SessionStart and UserP… (Round 1)
- Show the longest unattended stretch in the greeting (Round 1)
- Keep session titles and push bodies in sensitive repos to T-ids — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- Log whether each push got a response (Round 1)
- Show a returning-session card that states the first failing check — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 1)
- Add a one-file status segment for tmux and starship — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 2)
- Return card on resume in the session title — near T-0781 (done): Sessions are named after their task: SessionStart and UserP… (Round 2)
- Keep push bodies human and one-line — near T-0691 (done): Milestone: Intelligence — Planning and decomposition (1) (Round 2)
- Print a stable `fm status --porcelain` and ship tmux and starship segments — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 2)
- Offer a self-hosted ntfy channel for local-first push — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 2)
- Give sensitive repos a no-cloud attention path — near T-0784 (done): In a sensitive repo, Claude Code's outward tools (Artifact,… (Round 2)
- Leave a manual `/rename` alone — near T-0784 (done): In a sensitive repo, Claude Code's outward tools (Artifact,… (Round 2)
- Quiet-hours acknowledgement for hands-off stretches (Round 3)
- Wild: Offer a three-line `fm status --haiku` as the default status (Round 3)
- Put the next command on the clipboard when Foreman tells you to run one (Round 4)
- Learn quiet hours from your own activity gaps (Round 4)
- Wild: Make a run audible with rising pitch (Round 4)
- Wild: Share skins: spinner verbs, palette and cues as one tiny file (Round 4)
- Wild: Gate risky approvals on fatigue signals — near T-0685 (done): Milestone: Intelligence — Cognitive architecture and wild b… (Round 4)

## [skip] state-integrity — State integrity: lane base, merge journal, git refs, topology matrix, writer stamps, derived status, merge driver, idempotency
value 2 · effort S · risk low · the window is one function call and no incident has hit it
Exists: pre-merge base written right after the merge (fmlanes.py:230-241); undo refs
Premise: ok in theory: a crash between merge and the meta write loses the start point
Ideas (23):
- Journal the lane merge so a crash cannot lose the pre-merge start point (Round 1)
- Wild: stamp every state write with its writer — near T-0817 (done): Guard refusals read better: /dev/null on a data-only python… (Round 1)
- Keep task titles short and move CONTEXT to a linked field (Round 1)
- Derive task status from facts instead of storing it (Round 1)
- Merge Foreman's state files with a custom git merge driver — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 2)
- Give every mutating `fm` verb `--dry-run` that prints the state diff — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 2)
- Add `fm config explain KEY` showing which layer set each value (Round 2)
- Check a lane's base before it forks from `head` — near T-0804 (done): A merged lane's task is measured from the main checkout's c… (Round 2)
- Collapse task statuses to now, next and later, with a reason field — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 2)
- Replay old incidents as drills against every release — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 2)
- Drill each round-1 feature's failure path — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 3)
- Stamp each state write with its writer and version — near T-0686 (done): Milestone: Intelligence — Debugging and diagnosis (Round 3)
- Make one 10-line NOW file the only thing resume reads — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 3)
- Wild: Configure Foreman by deleting lines from `fm.lock` — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 3)
- Wild: Mint a paste-in resume token (Round 3)
- Give every fm verb a documented exit-code and error-class contract (Round 4)
- Pin every task's start point as a git ref — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Run a git-topology matrix over every git-reading verb — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 4)
- Give `fm` typed exit codes with a retry class — near T-0750 (done): Catch rates and give-up mining miss real failures: stored r… (Round 4)
- Add idempotency keys to mutating verbs (Round 4)
- Wild: Check multi-session histories Jepsen-style — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 4)
- Wild: Torture the calendar (Round 4)
- Wild: Mine Claude Code's issue tracker for hook-crash fixtures — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 4)

## [skip] exports-and-policy — Exports and policy: SARIF, Mermaid, todo.txt, Perfetto, evidence pack, policy calendar, saved queue views
value 2 · effort S · risk low · no consumer
Exists: fm ui --json, fm queue, fm page
Premise: unclear: no consumer named
Ideas (9):
- Export audit findings and evidence failures as SARIF — near T-0276 (done): fm second: one primitive for independent second reads — riv… (Round 2)
- Export the queue as Mermaid and Gantt (Round 3)
- Wild: Tap state changes to any command you configure — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Make one policy calendar drive everything time-shaped — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 4)
- Query and save views over the queue (Round 4)
- Export the queue as todo.txt and iCalendar (Round 4)
- Write a signed Autopilot Charter per unattended stretch (Round 4)
- Export the ledger as a change-management evidence pack — near T-0710 (done): Frontier 10 — Milestone work compiler and merge train (Round 4)
- Export any session as a Perfetto trace — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 4)

## [skip] round-scorecard — Round metrics and receipts: per-round snapshots, claimed-vs-measured, spend per verified task, errata, raw rows beside numbers
value 2 · effort M · risk low · duplicates fm digest
Exists: fm digest (fmcost.py:309), fm outcomes (fmoutcomes.py:108), bench scorecard (fmbench.py:499)
Premise: false: a round receipt is a digest over a date range; 'round' has no stored state
Ideas (15):
- Replay every metric reader against real stored result strings — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Snapshot metrics per round and judge the round by them — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Stamp each round's catalogue with a closing receipt in `fm research` — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 1)
- Add a claimed-vs-measured receipt for each round — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 1)
- Audit each round's own diff before calling it shipped — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Show a "round receipt" when a recursive round closes — near T-0674 (done): Milestone: Features — Observability, replay and trust (Round 2)
- Show a before/after of each fixed metric on the real data that exposed it — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Add a spend-per-verified-task line to every round receipt — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Replay your own round to prove it helped before keeping it — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: Print "seconds Foreman added" at every close-out — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Print three raw source rows beside every number Foreman reports (Round 4)
- Print an erratum when a fix changes a number Foreman already reported — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 4)
- Run a ceremony holdout on every tenth S task (wild) (Round 4)
- Make `fm round close` produce a one-screen decision card — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 4)
- Add a "Foreman-off" differential on every close — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 4)

## [skip] board-ticking — Tick the board/catalogue: click, paste-back, editor checklist, inferred ticks from user behaviour
value 2 · effort M · risk low · the user hasn't ticked the board; chat replies and fm decide cover choices
Exists: fm page renders queue/catalogue with a picks collection (fmpage.py:99); no tick read-back
Premise: unclear: no picks recorded yet on the round-1 board
Ideas (12):
- Tick the board in one pass at round end — near T-0088 (done): Round I core: fm ui --json view model + section aliases/tic… (Round 1)
- Tick the board: a keep/tune/revert review of shipped items — near T-0691 (done): Milestone: Intelligence — Planning and decomposition (1) (Round 1)
- Auto-tick the board from observed use (Round 1)
- Wild: Draw the task page like a clipboard that ticks itself (Round 1)
- Let the user tick the catalogue page and paste the result back — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 1)
- Infer idea ticks from what the user does next — near T-0778 (done): Phone push when the user is needed or the queue drains: the… (Round 1)
- Make the `fm page` board answer back through a local tick file — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 1)
- Make `fm page` accept ticks back through a pasted line — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 2)
- Tick the catalogue page by clicking — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 2)
- Auto-tick the board from the user's next move — near T-0406 (done): Evidence for a step should move the UI's current step there… (Round 2)
- Tick the board in `$EDITOR` as a plain checklist (Round 4)
- Collect the human-only chores into one copy-paste page (Round 4)

## [skip] session-liveness — Stall and liveness detection: idle canary, outside stall detector, handoff, orphan reaping, liveness verdict, gates
value 2 · effort M · risk med · headless covered; canary/chaos ideas speculative
Exists: fm run/serve stall detector (fmserve.py:434-451); bus heartbeat; Stop-hook drive
Premise: ok for interactive sessions only
Ideas (15):
- Turn the 2026-10-14 headless-drive incident into a permanent drill — near T-0775 (done): One-off headless claude -p sessions answer their prompt and… (Round 1)
- Detect Stop-hook overload and split the verdict — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 1)
- Add a stop-reason and idle canary for the drive loop — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 2)
- Wild: Add a nightly canary that wedges a throwaway session on purpose (Round 2)
- Detect a stalled session from the outside — near T-0680 (done): Milestone: Features — Self-improvement and learning (Deepened: liveness)
- Make the stall threshold learn from history — near T-0706 (done): Frontier 06 — Debugging intuition engine (Deepened: liveness)
- Handoff a wedged session to a fresh one with the step pointer — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Deepened: liveness)
- Reap orphans on every session start — near T-0675 (done): Milestone: Features — Orchestration, lanes and fleets (Deepened: liveness)
- Add a one-line liveness verdict to the SessionStart greeting — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Deepened: liveness)
- Replay the liveness ledger in a time-travel view — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Deepened: liveness)
- Wild: Run a chaos monkey for liveness in CI (Deepened: liveness)
- Wild: Let sessions heartbeat to each other as a peer mesh (Deepened: liveness)
- Wild: Turn the queue's idle time into a spoken or haptic heartbeat — near T-0415 (done): Drive: long-lived jobs and an empty queue never leave a ses… (Deepened: liveness)
- Gate the push on liveness confidence — near T-0775 (done): One-off headless claude -p sessions answer their prompt and… (Deepened: liveness)
- Check liveness in the install and release gate — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Deepened: liveness)

## [skip] deferral-triggers — Deferred work: unlock triggers, premise ledger, recurrence counters, owners, nightly reconcile, leftover-budget tasks
value 2 · effort M · risk low · revisit dates cover the common case
Exists: fm task defer --until (fmcli.py:585; fmcore.py:2222)
Premise: ok but thin evidence
Ideas (15):
- Give each deferred cluster a reactivation trigger (Round 1)
- Re-measure the premise behind every dropped idea on a schedule — near T-0691 (done): Milestone: Intelligence — Planning and decomposition (1) (Round 1)
- Turn deferral reasons into unlock triggers — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 1)
- Spend leftover round budget on small deferred tasks — near T-0751 (done): Milestone: Runtime — usage-limit failover, revert with depe… (Round 1)
- Add passive recurrence counters for the deferred clusters — near T-0672 (done): Milestone: Features — Guard and safety (Round 1)
- Shelve catalogue clusters as one file, not thirteen tasks — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 1)
- Wild: Spend leftover quota on a "gift" task (Round 3)
- Surprise me: a gift diff from the deferred pile (Round 3)
- Throw back requests that just became cheap — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 3)
- Retire tasks whose premise has expired using a premise ledger — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 3)
- Give each blocked task a machine-checkable unblock predicate — near T-0675 (done): Milestone: Features — Orchestration, lanes and fleets (Round 4)
- Keep a decision-owner column on every deferred cluster — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 4)
- Wild: Leave one small task for the user, with a hint ladder — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Wild: Declare amnesty windows for spike weeks (Round 4)
- Reconcile deferrals nightly against what the user actually did — near T-0682 (done): Milestone: Features — Verification and product checking (Round 4)

## [skip] close-warning-quality — Close warning precision: track overrides, auto-demote, one verdict line, what-would-user-do check
value 2 · effort M · risk low · revisit if warning kinds grow
Exists: _close_warnings_of has two kinds (secret, left-behind) plus drift/not-verified notes (fmcli.py:1248)
Premise: false: too small a surface to learn overrides from
Ideas (7):
- Learn which close warnings the user overrides, and quiet them — near T-0711 (done): Frontier 11 — Cockpit UI (Round 1)
- Track warning precision at close — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- Auto-demote close warnings the user never acts on — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 1)
- Wild: Add a per-hook "would the user notice" probe — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 2)
- Pin every close warning to a "what would the user do about it" check — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 4)
- Fold close warnings into one verdict line — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 4)
- Print a "quiet because" line when Foreman says nothing (wild) (Round 4)

## [skip] resource-footprint — Resource and disk footprint: fsync, git snapshots, retention, quotas, doctor timing, background census, throttling
value 2 · effort M · risk med · no measured footprint problem
Exists: tidy retention, state fallbacks (fmcore.py:84-172), fsync in write_atomic, ENOSPC as stall
Premise: false: mostly covered
Ideas (17):
- Wild: run a disk-full and read-only-home drill in `fm doctor --drill` — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 1)
- Turn on git fsmonitor and untracked cache, and take one porcelain snapshot per hook turn (Round 1)
- Defer fsync in the ledger to stage transitions — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 1)
- Parallelise and time-box `fm doctor` and the installer's plugin fetches — near T-0206 (done): fm research ask: recall first, parallel web researchers per… (Round 1)
- Wild: Defer heavy gates while on battery or thermally throttled (Round 1)
- Bound Foreman's disk footprint with a budget and LRU eviction — near T-0004 (done): Phase 6: fm tidy and fm doctor (Round 2)
- Run the bench under a throttled-CPU profile — near T-0805 (done): The hook benchmark judges by CPU time when the machine is b… (Round 2)
- Wild: Mount a slow-disk and read-only-home drill (Round 2)
- Add a state quota with hot/cold tiering (Round 2)
- Give every on-disk store one retention table — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 2)
- Census Foreman's own background footprint — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Round 3)
- Tie scratch artifacts to a round's lifetime (Round 3)
- Time-box `fm map` and `check --affected` on huge repos — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 4)
- Memoize version probes and single-flight shared derived work (Round 4)
- Run housekeeping and gates in a low-priority class — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 4)
- Bound every regex over tool output — near T-0227 (done): fm budget: one spend ledger and caps for every child run an… (Round 4)
- Suspend UI polling when Desktop is hidden — near T-0322 (done): fm projects --json and fm ui --follow: a device-wide read s… (Round 4)

## [skip] verify-command-hygiene — Verify commands and gate reuse: lint expiring refs, derive from test map, affected tests, tree-hash caching, self-gates
value 2 · effort M · risk low · leftovers have no demonstrated need
Exists: fm check --affected, tree-hash reuse, verify linting (T-0698), unrunnable refusal (T-0765), fmcore.judged (T-0820)
Premise: ok: nearly all done
Ideas (17):
- Lint verify commands for self-expiring references — near T-0698 (done): Friction batch 2026-10-09: IFS false block from heredoc dat… (Round 1)
- Re-verify "done" in a clean checkout of the staged diff — near T-0710 (done): Frontier 10 — Milestone work compiler and merge train (Round 1)
- Reject verify commands that read Foreman's own queue — near T-0710 (done): Frontier 10 — Milestone work compiler and merge train (Round 1)
- Record `--affected` misses and widen the selection on its own — near T-0808 (done): fm check --affected works in Foreman's own project; lane br… (Round 2)
- Test that every verify command can still run after its target leaves the queue — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 2)
- Run one command for all three self-gates — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 2)
- Default `verify` from the test map instead of hand-written commands — near T-0682 (done): Milestone: Features — Verification and product checking (Round 2)
- Derive gates from the repo's own CI config — near T-0686 (done): Milestone: Intelligence — Debugging and diagnosis (Round 3)
- Respect monorepo workspaces (Round 3)
- Share one build cache across lanes — near T-0445 (done): Lane dispatch respects relate groups and co-change footprin… (Round 3)
- Run last-failed tests first on every runner — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 3)
- Route changes by CODEOWNERS — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 3)
- Cache gate and verify results by tree hash plus command — near T-0682 (done): Milestone: Features — Verification and product checking (Round 3)
- Classify path classes once: generated, vendored, frozen, hot (Round 4)
- Add cross-task evidence reuse with a staleness proof — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Run a local-only dry run of every new idea's "Done when" — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 4)
- Reuse the lane's verify when the merged tree is identical — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 4)

## [skip] install-and-platform — Install and platform reach: Python floor, Windows/WSL, devcontainer, daemon units, host probe, optional packs
value 2 · effort M · risk low · launchd is the only remnant, niche here
Exists: install.sh refuses native Windows (:47); Python floor auto-installed; systemd units
Premise: false: done or out of scope
Ideas (15):
- Fail loudly and minimally-safe when `python3` is missing or too old — near T-0368 (done): fm and the hooks re-run under a supported Python when pytho… (Round 1)
- Lower the Python floor so the installer never installs Python — near T-0765 (done): A verify that can't run at all (python3 -m <missing module>… (Round 1)
- Give the guard bounded script-file reading — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 2)
- Fall back to window-only mode when the tray library is missing (Round 2)
- Bootstrap Windows through WSL from one PowerShell line (Round 2)
- Add `fm daemon install` for systemd user and launchd units — near T-0298 (done): Unattended checks: fm bench stranger (a newcomer session fr… (Round 2)
- Ship a devcontainer feature and Codespaces install (Round 2)
- Wild: Give each machine a restricted SSH forced-command Foreman shell (Round 2)
- Wild: Add a Foreman Lens browser extension for GitHub PR pages — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 2)
- Wild: Run Pocket Foreman in Termux on a phone (Round 2)
- Fail loudly when `python3` is missing or older than the floor — near T-0368 (done): fm and the hooks re-run under a supported Python when pytho… (Round 2)
- Install optional skill packs on first need, not by flag — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Run Foreman natively on Windows — near T-0319 (done): install.sh installs a Python Foreman supports on each platf… (Round 2)
- Fail safe when the project map is stale — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 3)
- Probe the host once and let every feature declare what it requires — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 4)

## [skip] cli-ergonomics — CLI ergonomics: terse verbs, default to active task, one-line answers, show-anything, nouns, question shapes, request grammar
value 2 · effort M · risk med · duplicates the intake grammar
Exists: active-task defaults, fm explain/why/recall
Premise: false: punctuation grammar clashes with intake tags
Ideas (13):
- Wild: capture from a forwarded email (Round 1)
- Make `fm` answer "what is Foreman doing this turn" in one line — near T-0778 (done): Phone push when the user is needed or the queue drains: the… (Round 1)
- Echo every capture in under 100 ms — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 3)
- Print the answer line first, details after — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 3)
- Default every task verb to the active task — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 3)
- Make successful `fm` verbs silent (Round 3)
- Give request prefixes a punctuation grammar: `!` jumps the queue, `?` plans without capturing, `~` parks (Round 4)
- Hold each capture for a 10-second amend window — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 4)
- Show live work by default and count the rest — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Cut Foreman's nouns to ten and lint for the rest (Round 4)
- Resolve any id with one verb, `fm show <anything>` — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Give every question one of three shapes — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Make successful `fm` verbs print one line — near T-0802 (done): fm research list and fm research show NAME (Deepened: tokens)

## [skip] token-ledger — Token ledger and spend envelopes: count tokens, per-task budgets, savings, yield per dollar, usage-window sleep, wire gateway
value 2 · effort L · risk high · exists; gateway out of scope
Exists: fmcost (cost/digest), fmbudget rate limits (:86-127), usage-window wait/failover (fmserve.py:295), --max-budget-usd
Premise: false: ledger and budgets exist; a wire gateway is large and risky
Ideas (19):
- Reinvest measured savings as review effort (wild) — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 1)
- Run a Foreman wire: a local API gateway for true token truth and wire-level compaction (wild) (Round 1)
- Wild: Run overnight brainstorms and audits through the Batch API at half price — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 1)
- Show a savings strip beside spend (Round 2)
- Set one spend envelope for a recursive mandate — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 3)
- Gate children's spend with a per-lens payoff history — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Retune `maxTurns` and effort from observed turn use (Round 3)
- Compile each idea's "Done when" into a runnable verify at queue time — near T-0672 (done): Milestone: Features — Guard and safety (Round 3)
- Sleep until the usage window resets, and say so (Round 3)
- Make child contracts: declare an estimate, enforce twice that, learn the error (Round 3)
- Count tokens, not characters, for every budget — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 3)
- Measure child yield per dollar by model and lens — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 4)
- Set a savings floor that auto-drops PERF tasks (Round 4)
- Build a token ledger that every Foreman surface writes to — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: tokens)
- Let the ledger set a per-task token budget, and warn when a task is on track to exceed its tier (Deepened: tokens)
- Wild: Add a "token weather" line in the status bar that turns red when a runaway loop is burning budget (Deepened: tokens)
- Wild: Replay a finished task offline with and without each optimisation to prove what it saved — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Deepened: tokens)
- Build one agent-run ledger that every child writes to — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: agents)
- Learn caps from the ledger and propose changes as a diff — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Deepened: agents)

## [skip] prompt-cache — Prompt-cache efficiency: prefix-stable child packs, cache affinity, miss attribution, cold-cache compaction
value 2 · effort L · risk med · little control; cost visibility exists
Exists: fmcost weights cache read/write tokens (fmcost.py:12,210)
Premise: unclear: Claude Code assembles the prompt prefix, not Foreman
Ideas (6):
- Cap every injected-context block with a CI-enforced byte budget per event — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 2)
- Route agents by cache affinity, not only by tier — near T-0676 (done): Milestone: Features — Performance and cost (Round 3)
- Make child-spawning prefix-stable and measure the cache hit (Round 3)
- Prefix-stable child packs for prompt-cache hits — near T-0269 (done): Pass 1 quick wins: read-only git stash, S-tier outgrowth tr… (Round 3)
- Attribute every prompt-cache miss to a cause — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 4)
- Compact the context when the prompt cache is already cold — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Round 4)

## [skip] agent-role-table — Agent roster: one role table, fewer roles, canary evals, typed findings, auto-split, hunter pairing, traces
value 2 · effort L · risk med · churn without a failure to fix
Exists: agents/*.md frontmatter with model/effort/maxTurns (T-0768); fmagents.py
Premise: unclear: no stated failure
Ideas (16):
- Wild: Split an agent role automatically when it keeps hitting its cap — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Run a crew roll call in the agents' own voices — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Show a per-agent trace timeline — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: pair an optimizer agent with a regression hunter on PERF tasks (Round 3)
- Wild: attach agent traces to commits as git notes — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 3)
- Wild: export a time sheet from the ledger — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Reuse native agent memory instead of injecting lessons into briefs — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 3)
- Collapse the fm-* specialists into one agent with a role argument, and let bench decide — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 3)
- Collapse agents to a builder and a checker — near T-0807 (done): A lane's edits recorded under .claude/worktrees/<lane>/ cou… (Round 3)
- Generate every agent file from one role table — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: Fork a hunch lane that races the plan on every FIX — near T-0676 (done): Milestone: Features — Performance and cost (Round 3)
- Generate all agent files and lane briefs from one role table — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: agents)
- Pair a regression hunter with every PERF builder — near T-0805 (done): The hook benchmark judges by CPU time when the machine is b… (Deepened: agents)
- Run per-role canary evals when Claude Code or a model changes — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: agents)
- Hand findings between agents as typed records, not prose — near T-0780 (done): Audit findings reach the host's review UI: fm audit prep as… (Deepened: agents)
- Auto-split roles that repeatedly hit their cap, with a bench gate — near T-0680 (done): Milestone: Features — Self-improvement and learning (Deepened: agents)

## [skip] diff-and-release-gates — Diff-level and release gates: undo detection, hygiene, risk agent, artifact inspection, clean-container install, release freeze
value 2 · effort L · risk med · add only if a regression slips past
Exists: bench hygiene, undo points, fm check, audit prep, reviewer
Premise: false: duplicates existing gates
Ideas (14):
- Smoke-test a cold session end to end — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- Flag diffs that undo recent closed work — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 3)
- Run a cheap diff-risk agent before the full done-tail — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 3)
- Run a post-install claim check — near T-0675 (done): Milestone: Features — Orchestration, lanes and fleets (Round 3)
- Turn gate waits into a review tour — near T-0751 (done): Milestone: Runtime — usage-limit failover, revert with depe… (Round 3)
- Wild: reproduce a failing CI run from its URL — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Close tasks with a provisional done that finalizes or reopens — near T-0690 (done): Milestone: Intelligence — Metacognition and calibration (Round 3)
- Freeze merges and self-edits to hooks while a release is in flight — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Gate pushes to main on a clean-container install of that exact sha — near T-0672 (done): Milestone: Features — Guard and safety (Round 4)
- Add a diff-hygiene gate to close — near T-0682 (done): Milestone: Features — Verification and product checking (Round 4)
- Inspect the built artifact before a release closes — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 4)
- Support a patch-stack mode for forks and patched bundles (Round 4)
- Park L tasks on a user-fired ultra review and ingest the result (Round 4)
- Close FEATURE tasks by ramping a flag, not by merging — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)

## [skip] misc — Unclustered one-offs
value 1 · effort S · risk low · speculative leftovers
Exists: fm whatif, prove, friction, ideas --seen
Premise: ok: mostly covered or wild
Ideas (11):
- Test discoverability with a cold agent — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 1)
- Hardening-debt futures: predict the next hotfix (wild) (Round 1)
- Wild: Put a "why is this here" link on every injected line, with a delete button — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 2)
- Run `fm whatif <setting>` against 30 days of real transcripts — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 2)
- Keep a time-debt ledger of Foreman's own mistakes — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Wild: Treat the queue as a build graph (`fm make`) — near T-0710 (done): Frontier 10 — Milestone work compiler and merge train (Round 3)
- Record an adjacent-possible note on each shipped capability (Round 4)
- Add `fm prove-it <claim>` that prints a one-command disproof — near T-0682 (done): Milestone: Features — Verification and product checking (Round 4)
- Show a proof-freshness dot on the band — near T-0681 (done): Milestone: Features — UI and motion (Round 4)
- Wild: Hand the queue to a rival harness overnight and diff the results — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 4)
- Wild: Offer a "premortem tape" the user can scrub before approving an L plan (Round 4)
