# Brainstorm catalogue: brainstorm-20261102-151147 (gen-3 Mission 6, #2)

398 ideas in 44 clusters, each grounded in the code: 54 built, 2 false-premise, 156 new, 186 partial. 24 clusters marked build.

Spot checks before any brief (T-2659, Mission 5's critique: every claim a brief rests on): fmideas.LENS_NOTES
(fmideas.py:28) has no grid lens — true. fmcore.stale_refs (fmcore.py:5432) checks a brief's named paths only when a
task is resumed, and only for ones gone since its start; nothing checks a plan's file:line citations when it is written —
true, partial. 22 of the 41 truncated `join(...[:N])` outputs in fmcli.py print no count of what was left out — true.
The brainstorm skill's grounding step (plugin/skills/brainstorm/SKILL.md step 4) runs no canary before accepting a
"not found" — true. The three recon passes spent 102 to 104 tool calls each this time (Mission 5: about 8).

## c01 Brainstorm completeness and stopping

Mark: **build** · value 4 · effort S · risk low — A grid lens forces coverage of the whole space and fits LENS_NOTES in a few lines; the rest is speculative.  
Slate: Add a 'grid' lens note to fmideas.LENS_NOTES that crosses the request's surfaces with its actors and failure modes and requires one idea per cell, and make --lens grid selectable.

- [partial] Fit a discovery curve to cluster labels and stop on estimated unseen mass — fmideas.py:877 stops a round adding < --dry new; no unseen-mass estimate
- [partial] Stop on estimated unseen idea mass, not on round count — fmideas.py:877 'if n > 1 and len(new) < args.dry: break' is yield-based
- [new] (wild) Seeded-gap recall test for brainstorms — grep -i 'seeded|recall test' fmideas/fmgenesis: only genesis planted defects (fmgenesis.py:1786); none for brainstorm
- [new] Brainstorm by morphological grid, one idea per cell — grep -i 'morpholog' repo: 0; LENS_NOTES (fmideas.py:28) has no grid lens
- [new] Make every unexplained ledger row owe an idea — grep -i 'unexplained' lib: 0; fm explain (fmrecall.py:1188) covers only blocks and drive decisions
- [built] Pre-register a kill probe with each idea — fm ideas --falsify FALSIFY prompt (fmideas.py:755), 'Kill it fast' in ideas.md (fmideas.py:921)
- [built] Score each lens by hindsight hit rate — fmideas.lens_rates (fmideas.py:376, T-0607), shown by fm taste
- [new] Chain lenses as an exquisite corpse — grep -i 'exquisite' repo: 0; lenses run parallel (fmideas.py:781); round 2 sees prior titles only
- [new] (wild) Have a child reconstruct the project's roadmap from only the closed-task titles, then diff — grep -i 'roadmap' fmideas/fmgenesis: none; fmideas.misses (fmideas.py:416) diffs asks vs ideas instead
- [new] (wild) Settle ideas in a market: each lens stakes a point budget, and use pays out — grep -i 'stake|market' fmideas.py: 0; yields tallied in lens_yield (fmideas.py:874)
- [partial] Calibrate brainstorm lenses to this user's accept history — lens_rates computed (fmideas.py:376) but DEFAULT_LENSES fixed (fmideas.py:50); not used to pick lenses

## c02 Brainstorm, grounding and slate pipeline

Mark: **build** · value 4 · effort S · risk low — A 'not found' that is never canary-checked is the exact T-2659 miss; a probe is the core of exhaustive grounding.  
Slate: Before the grounding step accepts any 'not found' for an idea, run a canary grep for a known-present term in the same scope and reject the result if the canary also returns empty.

- [new] (wild) Bisect the brainstorm pack until the top idea stops changing — grep -i 'bisect.*pack|pack.*bisect' lib: no hit
- [built] Gate each brief with a tiered claim resolver — near T-2269 (done) — T-2269 plan gate checks content by tier (CHANGELOG:270)
- [new] Run a grep canary before accepting any "not found" — grep -i 'grep canary|not found.*canary' lib: no hit; fmgenesis.py _grounded only checks quotes
- [partial] Verify every "Why:" quote against the pack — fmgenesis.py:3648 PRED_ROW parses Why:, :2569 _grounded quotes against charter; not pack
- [new] Score pack-ablation stability — grep -i ablat: fmcli.py:1227 hunk ablation, fmnight.py:37 rule ablation; none on packs
- [new] Add a "boring" lens — grep -i 'boring' lib: no hit
- [partial] Mine reverts and deleted files as retired-idea seeds — fmoutcomes graveyard (fmcli.py:6765), fmcost.reversals (fmcost.py:871)
- [new] Keep an idea funnel ledger with typed drop reasons — grep -i 'funnel|drop_reason' lib: no hit; fmideas.py exists for children
- [new] Add a grounding dial scaled by value — grep -i 'grounding dial' lib: no hit
- [built] Audit unslated work at each Mission close — near T-2393 (done) — T-2393 meaning proof per clause of user's request (CHANGELOG:1289-era)
- [new] Pick the final slate by diversity, with a greedy selector (MMR) — grep -i 'MMR|diversity' lib: no hit
- [new] Run a blind-reinvention probe on the verb table (wild) — grep -i 'reinvent' lib: no hit
- [new] Fork the same pack through the brainstorm skill and a plain prompt, then diff (wild) — grep -i 'plain prompt' lib: no hit; fm bench duel compares plugins
- [new] Time-box a quiet brainstorm: one lens per day, results waiting in the morning card (wild) — grep -i 'one lens per day' lib: no hit; fm night runs exist
- [built] Dedupe the pack against itself — near T-2487 (done) — T-2487 model exam arms per use incl. dedupe; fmsecond.py
- [new] Ask round 1 for titles only — near T-1992 (done) — T-1992 is intake @path scoping, unrelated; grep -i 'titles only' lib: no hit
- [partial] Generate the Genesis site from one data file and one template — near T-2474 (done) — T-2474 is genesis sweep coverage; grep -i 'site.*template' lib: no hit
- [partial] Name one primary consumer per brainstorm "Next question" — near T-2076 (done) — T-2076 brainstorms learn from misses; consumer not named (grep 'Next question' in lib)
- [new] (wild) Give each lens a random 25% slice of "ideas so far" — grep -i '25%|slice' fmgenesis/fmideas: no hit
- [new] (wild) Make children write each idea as "I want X so that Y" — near T-0684 (done) — T-0684 is a milestone; grep 'so that' brainstorm prompts: no hit
- [new] (wild) Let ideas decay by one value point per round unseen — grep -i 'decay' lib: no hit
- [new] (wild) Run a subtraction-only lens that may only say what to remove from the pack — grep -i 'subtraction' lib: no hit
- [partial] File tasks through a pre-flight hearing — fm intake plan gate (T-2269) and fm second (fmsecond.py) review items; no hearing
- [partial] (wild) Run a ghost reviewer that votes on every slate and plan — fm second (fmsecond.py), fmcritique.py review exist; not a voting ghost

## c03 Slate triage and exam items

Mark: **build** · value 4 · effort S · risk low — A Mission brief with no capped, checkable DONE-WHEN clause is the exhaustive-thinking gap that is still open  
Slate: Add a check to fm genesis check that every Mission brief is under 25 lines and names exactly one runnable Done-when command.

- [new] Rank the slate by days until the user first feels it — grep 'days until|first feel' MASTER.md/lib: none
- [partial] Draw the unlock graph between slate ideas — moonshot blocks carry Needs/Unblocks lines (MASTER.md:149); no graph drawn
- [partial] Treat unanswered slate lines as soft drops — asks expire after 24h, unanswered asks defer after ASK_DAYS=7 (fmcli.py:487); slate lines are not covered
- [new] Pin one omission-and-counterexample per accepted idea as an exam item — grep 'counterexample' fmexam.py/fmideas.py: none
- [partial] Mirror the slate to a shared offline file for other agents — fm export agents (MASTER.md:44) and genesis.json export (fmgenesis.py:1194); not the slate
- [partial] Slice every L task into a tracer that is useful alone — add('split') fmcli.py:6473 splits by step; no tracer rule
- [new] Cap each Mission brief at one screen and one Done-when command — CHANGELOG T-2391 is an unproven rollup, not a cap; grep 'one screen' lib: only digest help
- [partial] Chain backward from each DONE-WHEN clause to its falsifiers — fmrecall.bind(b) ties Raw-request clauses to criteria (MASTER.md:201); --assume add '--check CMD' (fmcli.py:6654) lists what would show it false
- [partial] Brainstorm omissions on a diff at finish — fm audit lenses (fmcli.py:6590) run on a diff; T-1510 is a config get/set change, not a finish brainstorm
- [built] Convert failed-spike notes into one "not yet" page — fmgenesis.py:18 SHAPE has not-yet.md; MASTER.md:146 'not-yet ledger'
- [partial] Compile friction events into capability candidates weekly — fm find --blindspots --capture 1 (MASTER.md:148) files a task a day; fm triggers reads friction
- [partial] Mine the model's own wishes from transcripts — T-1523 drafts playbooks from finished runs; fm recall --corrections mines the user's words; no model-wish miner

## c04 Truncated lists say what was left out

Mark: **build** · value 4 · effort S · risk low — Silent truncation hides part of the space; a shared helper makes omissions visible everywhere.  
Slate: Add one shared helper in fmcore that appends 'N left out: <flag>' to truncated lists and use it in every [:N] slice that prints to the user (start with fm todo, fm find, fm cost).

- [partial] Print "N left out" on every truncated list, with the flag that shows them — fmcli.py:4144 prints 'N more (fm todo --json)' for one list; grep 'left out|\+\d+ more|not shown' hits ~18 fmcli spots, not uniform

## c05 Brief grounding and pre-queue checks

Mark: **build** · value 4 · effort M · risk med — Briefs carrying false claims are the origin of wrong builds (T-2659); mechanical claim resolution closes the gap.  
Slate: At fm task new/capture time extract file paths, verbs and function names a brief asserts exist, grep them in the repo, and prefix the brief with a Claims section marking each found or missing.

- [partial] Lint every brief's factual claims against the repo before it files — fmcli.py:3711 reports files gone since start; grep 'brief_claims|lint brief' lib: no claim extraction at file time
- [partial] Extract each brief's load-bearing claims and resolve them mechanically — fmresearch.py:351 resolves web claims; briefs only get a stale-path note (fmcli.py:3711)
- [built] Refuse to file a brief that restates one already in the catalogue — T-2546 already-built at birth (fm capture/new); CHANGELOG
- [built] Run a built-check keyed to the drop class before any slate — T-2659 brainstorm skill grounding step; fmrecall.nearest_done (fmideas.py:907)
- [built] Backtest the grounding step on past drops — T-2471 cold read / grounding; fm backtest (fmcli.py:7084)
- [partial] (wild) Run an adversarial "already built" hunter with a grep tool and a bounty per hit — nearest_done word-overlap hint (fmideas.py:907) is built; a grep-armed hunter child is not (ideas children are tool-less)
- [partial] Kill each brief before it enters the queue — fm ideas --falsify (fmideas.py:755) kills ideas; fm queue --cost quotes (T-1878); no pre-queue kill pass
- [partial] Refuse to start a task whose p90 cost would breach a cap — fmcost.py:597 cost cap is checked mid-run; queue --cost is a quote only 'nothing is refused' (CHANGELOG:506)

## c06 Citation-checked answers

Mark: **build** · value 4 · effort M · risk low — Code answers cite file:line unverified; a mechanical existence and line check mirrors the web quote check.  
Slate: Check every file:line citation in an fm code --ask answer against the working tree and mark each found, moved or missing, as fm research ask does for web quotes.

- [partial] Make the answer to a question citation-checked — fm code --ask read-only (T-1770); fm research ask checks quotes (fmresearch.py:351) but only for web pages, not repo file:line
- [partial] (wild) Answer "how does X work here?" only with citations a checker has verified — grep 'file:line' fmcode.py: no verifier for code answers; fmresearch.py:351 checks web quotes only

## c07 Ledger integrity and concurrency

Mark: **build** · value 4 · effort M · risk med — A write that races (id allocation, hook replays) corrupts state, which is a consequence nobody has tested  
Slate: Add a test that starts N lanes at once with fm task new and asserts every T-id is unique, exercising fmcore.next_id under the project lock.

- [partial] Make recovery the only startup path — fm doctor --restore-state and --repair (MASTER.md:44); T-1280 tests hook timing; startup still has a cold path
- [new] Number every ledger record with a sequence beside the wall clock — grep '"seq"|sequence number' lib: none; fmcore.py:1067 has a 'prev' hash chain only
- [new] Shuffle and duplicate recorded hook events into the session readers — grep 'fuzz|shuffle' lib: only fmlong/fmexam/fmfind/fmwatch/fmdojo, not hook readers
- [false-premise] Differential-check any warm hook daemon against the cold path — grep 'daemon' fmhooks.py: only a scan thread (986); hooks run cold and no warm daemon exists
- [partial] Gate `fm genesis live` on a clean ledger read — T-2244 (fm log EVENT appends any name); fsck exists (fmcore.py:800); no genesis live gate found
- [partial] Prove task-id allocation is collision-free under concurrent lanes — fmcore.next_id:2149 runs under the project lock; no concurrent-lane test (grep 'next_id' tests: 1-3 per file, none concurrent)
- [new] Compare-and-swap Foreman's own writes into the user's tree — fmcore.write_atomic exists; grep 'compare-and-swap|CAS' lib: none; T-2539 is usage-burn advice
- [partial] Make tower files merge-safe when lanes land — fm lane merge refuses a dirty main (T-0403); no tower-file merge strategy found
- [new] Generate ledger writers, readers and validators from one schema file — grep 'schema' fmcore.py: no ledger schema; events are free-form (fm log EVENT)
- [partial] Event-source all state with a universal `--at` — fm at T -- CMD is scheduling (MASTER.md:541); fm replay replays prompts; no as-of reads
- [partial] Bind a guard verdict to the command's hash and check it afterwards — fmguard.py:4421 _DEPS keeps (path, sha256) for cached script verdicts; no post-run check

## c08 Repeat-correction and steer handling

Mark: **build** · value 4 · effort M · risk med — A repeated correction means a sibling was missed; wiring the existing cluster detector to a live sweep is a real coverage gain.  
Slate: When the UserPromptSubmit hook sees a second correction matching a fmideas.correction_clusters shape, run fm projects --sweep for the pattern and tell Claude to pause and list sibling sites.

- [partial] Break out when the user repeats themselves — fmideas.correction_clusters (fmideas.py:535) proposes rules after 2 repeats in fm taste; nothing interrupts the live session
- [partial] Detect repeat-correction language and trigger a sibling sweep and a pause — grep 'sibling sweep|repeat.*correction' lib: correction_clusters and fm projects --sweep exist, no hook linking them or pausing
- [new] Render steers whole when relevant and cut by relevance, not length — grep -i 'steer.{0,40}(max|cap|budget)' fmcore/fmcli/fmhooks: no hits; injection capped by doctor CTX_BUDGET (fmdoctor.py:196)
- [built] Run a steer interaction matrix in simulation — T-1063 steers compile to checkers (fmideas.compile_rule fmideas.py:485); fm backtest --rule
- [built] Preview a new steer against history before it is stored — fm backtest --rule REGEX (fmcli.py:7084, T-1058)
- [new] (wild) Hunt for loopholes in each steer's wording — grep -i 'loophole' plugin/lib: 0 hits; compile_rule demands 2 shape words (fmideas.py:488)
- [new] Mine the user's interrupts after Foreman output as the "felt cost" signal — grep -i interrupt plugin/lib: only KeyboardInterrupt/worktree; corrections are logged (event correction), not interrupts
- [built] (wild) Seal a prediction of the user's next steer and score it — T-2505 genesis sealed prediction (fmgenesis.py gen-N/prediction)
- [new] (wild) Write the user's reply before they do — grep 'proxy' : fm decide proxy answers repeats only (fmideas.py:571); no reply drafting
- [new] (wild) Ration the user's yes votes — grep 'ration' : none; fm ask tallies fatigue at 3 same-category asks (MASTER guard trust T-1606)
- [new] Rewind the user's decisions with a "what if I'd said no" fork — grep 'what if|fork' decisions code: none; fm rollback is file-level only

## c09 Unattended run stops and spend

Mark: **build** · value 4 · effort M · risk med — Unattended runs lose the cause of a stop; this closes the end-of-run consequence  
Slate: Make fm run record one stop_reason (done, max, max-usd, stall-usd, stall, usage-limit, killed) in its heartbeat and exit with a distinct code per reason, printed by fm status.

- [partial] Express stall and spend caps in the host's own usage units — fm run --max-usd/--stall-usd (fmcli.py:8169-8173) are dollars; fmbudget.py/fmcost.py read usage pace; grep found no unit-based cap
- [new] Attribute stall spend per lane — --stall-usd (T-2669) is run-wide; grep 'per.lane.*(spend|usd)' MASTER.md: none
- [new] Give each `fm run` stop reason its own exit code — grep 'stop_reason|EXIT_STALL' lib: only fmmodels.py:733; no per-reason exit codes
- [partial] Give every unattended stop a single plain-language reason line on the status surface — MASTER.md:631 fm night 'stopped says why'; heartbeat-run.json (T-0434); not one common status line
- [partial] Wrap every unattended entry in one run envelope — heartbeat files for fm run/night (MASTER.md:631); fm contract (T-1158); no shared envelope
- [partial] Remember the task a stall stopped on — T-2669 stops the run on spend; fm run resume keeps the journal (MASTER.md:713); stalled-lane recovery T-2354
- [new] Charge killed children from their transcript tail — grep 'transcript tail' fmcost.py/fmideas.py: none; fmideas._tail:80 reads tails only for display
- [new] Attribute a killed child to OOM, cgroup limit or signal — grep 'OOM|cgroup' lib: fmplaybooks.py:64 only; SIGKILL hits (fmideas.py:226, fmsession.py:443) just kill
- [partial] Replace the `fm run` stop flags with one `--until` expression — fm run has --max, --max-usd, --stall-usd, --stall (fmcli.py:8165-8174); fm contract --until HH:MM (7555) is separate

## c10 User-facing surfaces and comms

Mark: **build** · value 4 · effort M · risk low — Surfacing what blocks on the user, with their own words, completes the consequences of unattended work  
Slate: Extend fm status to list pending asks and blocked tasks ranked by how many other tasks each blocks, quoting each item's Raw request.

- [partial] Show a "what I need from you" desk, ranked by what each item blocks — fm ask list 'asks waiting' (fmcli.py:6403); fm desk (MASTER.md:439) is a glance card; no blocks-ranking
- [built] Print a "while you were away" card at session start with money, closes and stops — fmaway.py (T-1155) and help at fmcli.py:6749; money not included
- [partial] Quote the user's own words beside every "Foreman-filed" item — Raw request keeps the words (MASTER.md:150); not shown beside Foreman-filed items
- [partial] Warn when a new request contradicts a standing steer, before work starts — fm decide --cites warns on steer cites (MASTER.md:466); vetoes note on PreToolUse; no request-time contradiction check
- [partial] Mark the cost of each standing rule in injected tokens and blocked actions — fm doctor injection budget (fmdoctor.py:2600); MASTER.md:595 logs the rule that fired; no per-rule token cost
- [partial] (wild) Print a monthly "things I decided for you" ledger with a one-key veto — fm decide --digest and fm vetoes exist; no monthly ledger
- [new] Point at an element in the running app to file a task — grep 'picker|inspect element' lib: none; fmshot.py screenshots only
- [partial] Add a system-wide quick-capture with context — foreman-ui quick capture (T-0095) and fm capture; no OS-wide hotkey (MASTER.md grep 'hotkey|tray': tray in Genesis only)
- [new] Show steer violations as live editor squiggles — grep 'squiggle|language server' lib: none
- [new] Wild: Ship the read model as one offline HTML file with embedded Python readers — fmpage.py ships HTML with JS readers; grep 'embedded Python' lib: none
- [partial] Make the autonomy dial a replay-previewed slider — fm autonomy standard|full (MASTER.md:44) and fm replay exist; no preview of a setting
- [built] Assemble the one-card finish receipt from fields that already exist — add('receipt') fmcli.py:6528 (T-1518)
- [partial] Count the demand a duplicate capture shows — MASTER.md:96 describes duplicate-capture handling; no demand count surfaced
- [partial] Verify a pasted outside claim against the repo before it enters a brief — fm ask ignores pasted text (MASTER.md:511,744); fm task assume ID add --check CMD verifies; not for pasted claims

## c11 CLI ergonomics and registries

Mark: **build** · value 3 · effort S · risk low — Typed stop and error codes help diagnosis, but only the cheapest item is worth it  
Slate: Add `fm next --held` that lists every task fm next skips (blocked, deferred, waiting on an ask) with its release condition, read from the existing --until fields.

- [new] Make `fm go` run the last printed Next command — grep 'fm go|cmd_go' lib: none; T-2653 only prints one Next: line on nonzero exit
- [partial] Use one consent flag for every code-running verb — 15 --yes/--force flags in fmcli.py; T-2641 only adds tombstones (fmcli.py:6063)
- [new] Hard-code flags whose value never varied in 60 days — fm usage counts verbs (fmcli.py:6863); grep 'never varied' lib: none
- [new] Delete deciders that abstain almost always — grep 'abstain' lib: no hits
- [partial] Reduce all gate and doctor checks to one registry — fminfra.CLASSES:40 and fmrelease.GATES:31 are separate tables; fmdoctor has its own checks; T-1757 is a two-Foreman warning
- [new] Drive lint, doctor and help from one verb contract table — fmcli.add(...) tiers carry help text only; grep 'contract table' lib: none
- [new] Assign stable error codes and keep a failure census — grep 'error code|failure census' lib: only fmexam ERR_MODULE and fmcritique census (unrelated)
- [partial] Add `fm tail`, one chronological stream across all ledgers (read-only) — fm session tail --follow and fm watch; add('timeline') fmcli.py:6938 merges integrations; no all-ledger tail
- [partial] Show everything `fm next` withheld, with the release condition — defer/block --until conditions (fmcli.py:6664-6677); fm next lists unverified assumptions; no full withheld view
- [false-premise] Add `fm quiet 4h`, a tired-mode that mutes everything except blocking items — `fm quiet -- CMD` already means 'run a noisy command' (fmcli.py:6877); grep 'snooze|mute all' lib: none
- [new] Give every outward call an idempotency class — grep 'idempoten' lib: only prose in fmeco.py:201, fmcore.py:4972
- [partial] Store the coverage grid sparsely — fmgenesis.py:309,528 coverage grid (T-2093); no sparse storage
- [partial] Cap each Mission's file reach (wild) — T-2336 blast radius reaches plans; no per-Mission file cap

## c12 Lens health and scoring

Mark: **build** · value 3 · effort S · risk low — failed-vs-dry and per-lens rates are partly built, and a failed or dry lens skews every later score  
Slate: In fm ideas, record each lens child as failed, dry (zero ideas) or productive in ideas.json, and have lens_rates in fmideas.py count only productive and dry lenses.

- [partial] Separate a failed lens child from a dry one — fmideas.py:941 raises 'lens(es) failed' and names them; the --dry rounds (:805) are a different thing; scoring does not separate them
- [partial] Tell a dry lens from a failed child before scoring it — same as the line above (fmideas.py:941); duplicate of that idea
- [partial] Fertility-weighted lens budget from idea lineage — fmideas.lens_rates:376 gives per-lens keep rates in fm taste (MASTER.md:128); not used to size a budget
- [new] Re-run a lens only over what changed since its last run — grep 'since its last|if-changed' fmideas.py: 0 hits; --if-changed exists only on canary/landscape
- [new] Normalise value scores across lenses — grep 'normali[sz]e' fmideas.py: only line 573 (text normalisation)
- [new] Rank ideas by scorer disagreement, not mean score — grep 'disagree' fmideas.py/fmgenesis.py: none
- [partial] Back-test brainstorm configurations against the accept and drop ledger — fmideas.misses:416 and lens_rates read ideas.json outcomes; no config replay
- [partial] Run a time-boxed or constrained brainstorm — fm ideas --rounds/--dry/--deepen (MASTER.md:44); grep 'time.?box' fmideas.py: 0, so no wall-clock box
- [built] Load repo-local lens files — fmideas.py:910 'lens file'; plugin/skills/brainstorm/SKILL.md:14

## c13 Proof and test quality

Mark: **build** · value 3 · effort S · risk low — A rule's regex can hang the PreToolUse hook, and the add path only checks that it compiles  
Slate: In fmcore.add_rule, reject a user rule regex with nested open-ended repeats (the check fmexam.py:1464 already applies to child regexes) and test it with (a+)+.

- [new] Make proofs notebook-aware — grep 'ipynb' lib: none (NotebookEdit only appears in hook matchers, MASTER.md:561)
- [built] Keep a refuted-assumption bank — fm task hypo add|mark and Refuted hypotheses (T-1075; MASTER.md:513)
- [partial] Test for genericity: strip the project name — T-0054 lessons privacy filter strips paths and names; no strip-name test for generated output
- [partial] Run the suite under `-X dev -W error` once a night — T-1805 runs it before push or release; grep '-X dev' plugin: not in fm night
- [new] (wild) Double-fire canary — grep 'double-fire' lib: none
- [partial] (wild) Auto-stress and shrink every flaky test — fm check --repeat N and flaky reruns (MASTER.md:479; fmexam _flaky:152); no shrinking
- [built] Make proof verdicts flake-aware — a failure is rerun once and a pass then is a flake (MASTER.md:479); fm prove --same; T-0705
- [partial] Lint hook-path regexes for catastrophic backtracking — fmcore.add_rule:3346 only re.compile-checks; fmguard.py:4304 _LINE_CAP bounds scans; fmexam.py:1464 lints child regexes, not user rules
- [partial] (wild) File one planted-flaw brief a week — fmexam plants flaws for exams (MASTER.md:147); no weekly brief filing
- [partial] (wild) Swap units in mutants of the cost and time code — fmmutate.py exists (monotonic hits :174); no unit-swap mutants
- [partial] (wild) Mine the user's own correction words for gauge defects — fm recall --corrections and ideas.correction_clusters:535 cluster corrections; not tied to gauges
- [new] Mark a gauge fix as a break in the series — grep 'gauge|break in the series|rebaseline' lib: only fmdoctor.py:2055 re-baseline
- [new] Notice when the user re-runs a proof command by hand and treat it as distrust — grep 'distrust' MASTER.md/lib: none
- [built] Add a debugging hypothesis ledger (`fm hypo`) — fm task hypo ID add|mark (T-0207, MASTER.md:513)

## c14 Request intake: coverage of the whole ask

Mark: **build** · value 3 · effort S · risk low — Surfacing decisions made without asking is a real gap in request coverage; the rest is speculative or partly built.  
Slate: Record each question a task decided instead of asking (fm decide already logs asks) and list them in the close card and fm digest so the user can overrule.

- [partial] Confirm Foreman's model of the repo on first contact — fm adopt baseline (fmeco.py:195), fm tour; grep 'first contact|onboard|model of the repo' finds no user-confirmed repo model
- [new] Plan the queue backward from a deadline — grep -i 'deadline|backward from' plugin/lib/*.py: only fetch/loop timeouts, no queue deadline
- [partial] Save a finished task as a named recipe — fm lib / fm playbooks (fmplaybooks.py) are curated cards; grep 'recipe' finds no save-from-task verb
- [new] List the questions Foreman suppressed because of "never block on the user" — grep -i 'suppress|never block on the user|unasked' fmhooks/fmcore/fmcli: only argparse.SUPPRESS; fm decide records asks, not skipped ones

## c15 Single source for limits, metrics and gauges

Mark: **build** · value 3 · effort S · risk low — Caps are scattered constants with edge tests ad hoc; a boundary test per cap is cheap and catches off-by-one.  
Slate: Add one test module that lists every module-level hard cap (e.g. FLAKY_K, HUB_PAIRS, MAX_RUNS) and asserts behaviour at n-1, n and n+1 for each.

- [new] Ratchet the number of distinct lines the hook path executes — grep 'distinct lines|hook path.*lines|ratchet' in plugin/lib: only fmexam LEAN_METRICS hook_ms_per_call (fmexam.py:2765), no line count
- [partial] Compute each metric in one place — fmcost/fmoutcomes/fmexam each compute metrics; grep 'LIMITS\b' in plugin/lib found no table; no single registry
- [new] Hold every hard cap in one LIMITS table — grep 'LIMITS\b' in plugin/lib/*.py: no hit; caps are per-module constants (FLAKY_K fmprove.py:32, HUB_PAIRS fmcli.py:5535)
- [new] Make each new gauge name its one decision — grep 'gauge' fmgenesis.py and 'decision.*gauge' in lib: nothing enforcing a decision per gauge
- [partial] Keep a limit register with boundary tests at n−1, n and n+1 — near T-1992 (done) — T-1992 is intake @path scoping, not caps; grep 'n-1|n+1|boundary' only edge tests for clock (T-2645); no cap register
- [partial] Calibrate each hard cap from the user's own command history via `fm replay` — fmreplay.py replays guard verdicts (MASTER 'fmreplay'); fmbacktest.py counts rule firings; no cap calibration. grep 'calibrat' no cap hit
- [new] Declare a `valid_while` predicate on every gauge and check it on host upgrade — grep 'valid_while|hysteresis' plugin/lib: no hit; doctor has version skew in fmeco only
- [new] Find derived labels stored apart from their source — grep 'derived label|stored apart|denormal' plugin/lib: no hit
- [new] Make equivalent transcript encodings a test fixture for every counting gauge — grep 'encoding' near 'transcript' fixtures in plugin/tests: no shared fixture found; per-gauge only
- [partial] Snapshot gauges at each generation boundary and diff them mechanically — fmgenesis.py has drift/sweep vs gen-0 (T-2104) and fmexam LEAN_METRICS; grep 'snapshot' in fmgenesis.py no gauge diff
- [built] Make the by-source split the default `fm burden` output — near T-2667 (done) — CHANGELOG T-2667: fm burden counts SessionStart context as hook_success; by-source already shipped
- [partial] Calibrate characters-to-tokens in `fm burden` from transcript usage — grep 'chars/4' fmcode.py:306 uses fixed //4 'a tokenizer if it misfires'; no calibration from usage
- [new] Wild: Cap replay ("what would 0.5×, 1× and 2× have done") before any new limit ships — grep 'replay' fmreplay.py/fmbacktest.py: guard rules and fix sigs only, no scaling of caps

## c16 Stop reasons, stalls and unattended liveness

Mark: **build** · value 3 · effort S · risk low — A stall that names the hung step turns a vague stop into an actionable one.  
Slate: Make fm run's stall stop record in the run log which task and step (last transcript tool call) was running when the --stall minutes elapsed.

- [new] Resolve conflicting stop reasons by one precedence line — grep 'precedence' plugin/lib stop reasons: only MASTER §6 source precedence; no stop-reason ordering
- [partial] Make every stall and spend stop work when dollars read zero — near T-2669 (done) — T-2669 shipped --stall-usd (fmserve.py:901); grep 'zero|0.0' near stall_usd: behaviour with no cost data unchecked
- [new] Name the hung step when the ship gate hits its timeout (wild) — grep -i 'hung|which step' fmship/fmcli/fmcheck: only fmcli.py:4741 comment; no step name on timeout
- [partial] Name the stall precisely: `fm run` records why and which step hung — fmcli.py:8173 --stall minutes and fmmodels.py:580 stalled event; run log not recording step
- [built] Heartbeat for every unattended path with a "last alive" line in doctor — near T-2542 (done) — fmdoctor.py:1652 check_heartbeats; T-2542 timers known alive
- [partial] Fold `--stall-usd` into the existing budget cap — fmcli.py:8171 --stall-usd and --max-usd are separate flags; fmserve.py:901
- [new] Add a lowest-regret default when a decision window times out — grep -i 'lowest.regret|safe default|decision window' plugin/lib: no hit; pending asks expire (APPROVAL_TTL)
- [partial] Verdict hysteresis: a flaky proof is labelled, not flipped — fmprove.py:274 _flaky reruns FLAKY_K=6 and labels flaky; no memory across runs
- [partial] Rate-limit capture wakes and log the wakes that were undone — near T-2656 (done) — T-2656 refuses near-duplicate deferred capture; grep 'wake' no rate limit or undone-wake log

## c17 Guard reach across shells and callers

Mark: **build** · value 3 · effort M · risk med — Task-runner indirection (make, npm run) is an unmeasured guard surface; an exam arm shows the gap first.  
Slate: Add labelled guard-corpus cases for commands hidden behind make, npm run, just and non-bash shells (fish, powershell) and report which the guard misjudges.

- [new] Shim agent commands to be non-interactive — grep -i 'non-interactive|shim' plugin/lib: no hit in guard/hooks
- [partial] Teach the guard other shell dialects and task-runner indirection — grep -i 'powershell|fish|make -n|Makefile' fmguard.py 12 hits; fm dojo corpus; indirection coverage unmeasured
- [new] Emit forge-side enforcement matching the local guard — grep -i 'forge|CODEOWNERS|workflow' fmguard: none emitting CI rules
- [partial] Add dialect packs to the guard exam for non-bash shells — fmexam.py guard arms and fmreplay labelled corpus; no dialect axis (grep 'dialect' empty)
- [partial] Give unattended spawns a credential allowlist, tested with a canary grant — fmcore.py:5156 notes ambient credentials; fmeco 'fm canary'; grep 'allowlist|env -i' no spawn env scrub
- [new] Unify every unattended spawn under one capability token — grep 'capability token' plugin/lib: no hit
- [partial] Ship a guard proof ledger on every unattended receipt — fm guard try (MASTER:536), fmreplay verdicts; receipts do not carry guard proof
- [new] Ship the guard and prover as an Agent SDK permission-callback package — grep -i 'permission.callback|can_use_tool|Agent SDK' MASTER/README/lib: none

## c18 History and git-state signals

Mark: **build** · value 3 · effort M · risk med — Branch switch or rebase mid-task silently invalidates the task base; noting it is cheap.  
Slate: Have the PostToolUse/Stop hook compare HEAD's branch and merge-base with the task's recorded base and add one note when a branch switch or rebase happened under an open task.

- [built] Surface co-change and hotspot hints from git history — near T-2238 (done) — fm find hotspots T-2238; fmcli.py:5553 co-change pairs T-0952
- [partial] Carry an `Idea:` trailer from catalogue id to commit and answer "why does this exist" — Foreman-Task trailer fmcli.py:2169 read by fm why; no Idea: trailer (grep 'Idea:' empty)
- [partial] Detect the user's own edits during a task — near T-0696 (done) — fmcli.py:2076 dirty-before-focus is user's work (T-1169); T-0696 is a milestone; mid-task edits not detected
- [new] Note branch switches and rebases under an open task — grep -i 'branch switch|rebase' hooks/core/cli/resume: only rebase_snapshot fmcore.py:329 (pause rebase)
- [partial] Add a backport lane for release branches — near T-2598 (done) — T-2598 handles ship cherry-pick onto main (fmrelease.py:315); grep 'backport' empty
- [built] Fix once, fan out with per-repo proof — near T-0710 (done) — fm projects --sweep (fmcli.py:8221) and T-0710 merge train; fmsplit
- [partial] Add a verified "undo this landed task" verb — near T-2104 (done) — T-2104 is genesis drift; grep -i 'undo' lib: fm rollback restores snapshots (fmrollback); reverse of a landed task absent

## c19 Host portability and scheduling

Mark: **build** · value 3 · effort M · risk low — launchd/Windows scheduling is a real unattended-tick gap, though it widens the surface  
Slate: Make fm night --install also write a launchd plist on macOS (and print a schtasks line on Windows), next to its existing systemd and cron paths in fmnight.py.

- [partial] Give the unattended tick a launchd and Task Scheduler backend — grep 'launchd|schtasks|Task Scheduler' plugin: 0 hits in code. fmnight.py:120-196 does crontab and systemd timer only
- [partial] Hold a sleep inhibitor across critical sections — fmserve.py:807-816 re-execs under systemd-inhibit for fm run/serve; ledger writes and releases are not wrapped
- [new] Try the system-level proof on the user's own host: `fm host prove` — grep 'fm host|host prove|"host"' fmcli.py: only task_done_in host events (2597); no verb
- [partial] Diff the host's event and tool surface against what Foreman subscribes to — add('canary') fmcli.py:7396 diffs the Claude Code version; add('wiring') 6948 shows hooks wired; no event-surface diff

## c20 Hostile inputs and caps at the edges

Mark: **build** · value 3 · effort M · risk low — Numeric flags are an unexercised input surface; a table-driven hostile-value test is cheap.  
Slate: Add a test that walks every argparse numeric flag in fmcli.py and feeds 0, -1, nan, inf and 10**18, asserting a clean error rather than a traceback or hang.

- [partial] Bound the guard with a size gate in front of every regex — fmguard.py:218 'script too long to parse in time', :4183 cap on scanned part (T-1931), T-2668 nesting limit; not every regex
- [new] Fuzz every numeric flag with hostile values — grep 'fuzz' plugin/lib: only width fuzz test_code_tui.HostileWidth (MASTER:714); no flag fuzz of --stall-usd etc.
- [new] Audit caps that live only in process memory — grep 'in process memory|memory-only' plugin/lib: no hit
- [partial] Cap line and record size in every ledger and transcript reader — near T-2652 (done) — T-2652 is fm drill --restore, not size caps; grep 'MAX_LINE|max line' limited to fmguard/fmcore readers
- [new] Generalise the stall stop to disk, children and tool-call resources — grep 'stall' fmserve.py:901 only usd; fmcli.py:8173 --stall minutes; no disk/child count
- [partial] Make every guard-state read fail loudly, with a ledger record — near T-0272 (done) — T-0272 is flake ledger; grep 'except Exception' in fmguard state reads silent; no ledger record on read failure

## c21 Ledger integrity and forensics

Mark: **build** · value 3 · effort M · risk low — Start/terminal pairing is a concrete, cheap ledger invariant that surfaces silent loss.  
Slate: Add `fm doctor` check that pairs each task/lane/run start event with its terminal event in the ledger and lists orphans older than a day.

- [partial] Pair every start record with a terminal record, and list the orphans — grep 'orphan|no end record' hits fmideas.sweep_orphans (processes), fmgenesis start record; no ledger-wide start/end pairing
- [partial] Kill-point sweep across every ledger append — CHANGELOG:217 T-2332 relay race over 11 kill points (spike); no sweep of all appends
- [new] Make the ledger a content-addressed, machine-mergeable store — grep 'content-address|merge driver' plugin/lib: no hit; fmsync.py:13 keeps conflicts under sync-conflicts/
- [partial] Flag sync-folder conflict copies of ledgers — fmsync.py:154 stores its own conflicts; grep 'sync-conflict|Dropbox|Syncthing' finds no detection of foreign conflict copies
- [partial] Reconstruct a minimal reproduction from any ledger failure by delta-debugging records — fmdebug.py:168 _ddmin on source units for a red command; not on ledger records
- [partial] Mine invariants from the ledgers and enforce them as live tripwires — fmdataproof.py invariants are brief-declared SQL checks (fmdataproof.py:161); no mining
- [new] Model-check the task, grant and lane state machine, then check real ledgers against it — grep 'model.check|state machine' plugin/lib: no hit

## c22 Proof and test quality

Mark: **build** · value 3 · effort M · risk low — Flaky ranking by lower bound is a small pure function over data already in the flake ledger.  
Slate: Rank fm check's flaky-test report by Wilson lower bound on the failure rate using the existing flake ledger, so a 1-of-2 failure no longer outranks 5-of-50.

- [partial] Ship the do-less `fm prove` cache: skip only on an identical diff hash — grep 'diff.?hash' lib: fmsmoke.py:8 uses dirty-diff hash, fmmandate.py:311 caches check results; fm prove itself uncached
- [partial] Rank flaky tests by lower confidence bound, not raw fail rate — grep -i 'flaky|wilson' ~105 hits; fmprove.py:274 reruns only; no LCB ranking
- [partial] Re-run the closed task's proof when a capture near-duplicates it — near T-1662 (done) — T-1662 refuses near-duplicate capture naming the task; no proof re-run (grep 'near-dup' fmcli)
- [partial] Count the user's repeated corrections per class and promote a class to a standing check at three — fm digest --moves corrections metric (fmcli.py:7109); fmsteer corrections; no promote-at-three
- [built] Block test-weakening and suppression in every diff — fmmap.py:589 R3 weakened tests in the diff; fmcli.py:217 CHANGELOG skipped red tests
- [partial] Apply thresholds to changed lines only — fmfind.py:785 blindspots uses changed lines; fmcli.py:5709 'changed lines stay whole'; thresholds not diff-scoped
- [built] (wild) Prove the user's CI can go red — near T-2636 (done) — T-2636 fm prove --steer [check: CMD]; CHANGELOG
- [partial] Add a hotfix mode with a proof-debt clock — grep -i 'hotfix|proof.debt' hit only fmmap.py:197; 'Unproven:' trailer fmcli.py:2175 and unproven_cached fmcore.py:4828

## c23 Repo hygiene proofs

Mark: **build** · value 3 · effort M · risk low — Out-of-scope formatting churn is a consequence of a change nobody sees; a diff scan fits the close check.  
Slate: Add a close-time check to fm task finish that lists hunks in the task's files that only change whitespace or formatting outside the lines the plan named, offering a revert.

- [partial] Resolve merge and rebase conflicts with a proof from both sides — fmcli.py:2678 only flags conflict markers at close; fmlanes merge conflicts reported; no two-sided proof
- [partial] Turn review comments on the user's own PR into tasks, with replies that cite proof — fm pr threads (fmpr.py:1, T-1087) makes steps; fm pr --post posts the body (fmpr.py:88); no per-thread reply
- [new] Add `fm prove --api`: public API surface diff with semver verdict — grep -i 'semver|api surface' lib: only fmrelease version bump (fmrelease.py:33); fmprove.py has no api mode
- [new] Retire stale feature flags and dead config with a proof lane — grep -i 'feature flag|dead config|stale flag' lib: only fmsettings.py:788 dead pane flag
- [new] Revert formatting churn the agent introduced outside the lines it meant to change — grep -i 'formatting churn|reformat|whitespace.only' lib: churn only in fmpage git stats; fmcli.py:2929 scaffolding scan
- [partial] Check dependency licences and snippet provenance on every diff — fmdeps.py checks undeclared/new deps (fmdeps.py:23) but grep licen[cs]e fmdeps.py: 0; fmlib covers card licences only

## c24 Steer budgets, tests and ship-gate hygiene

Mark: **build** · value 3 · effort M · risk low — A hook-path parser that hangs blocks every tool call; generalising T-2668's latency test is cheap insurance.  
Slate: Add a test that feeds each hook-path parser (fmguard, fmhooks, fmdeps verbs) generated pathological inputs of growing size and fails when time grows faster than linear.

- [partial] Give steers a size and count budget at store time — VETOES_KEEP caps vetoes (fmideas.py:666); grep 'steer.{0,40}(max|cap)' fmcore/fmcli: no per-steer size cap
- [new] Test complexity growth, not just a fixed bar — grep -i 'pathological|latency' plugin/tests: fixed-bar hook latency only (test_doctor.py:157)
- [built] Name the hung test when the ship gate times out — T-1980 CHANGELOG:449 (fm ship marks scratch run, names why-not-caught)
- [partial] Run a pathological-input latency suite over every hook-path parser — T-2668 timed ten nested-$( commands for the guard (git log); other hook parsers untested (grep 'pathological' tests: no hits)
- [new] (wild) Run a timing-fuzzer child that is rewarded only for slowness — grep -i 'fuzz' fmexam/fmguard: none; bench_hooks.py fixed fixtures only

## c25 Brainstorm pack hygiene

Mark: **skip** · value 2 · effort S · risk low — the main hygiene is built; the integrity line is cosmetic and the shuffle is research-only

- [built] Reject fragment lines as idea titles — T-1056 in CHANGELOG; fmideas.py _TITLE/_is_new:725
- [built] Truncate pack lines at word boundaries — T-2249 (fm ideas adds the user's words once); fmideas.py PACK_WORDS:46 and c.fit
- [new] Print a pack integrity line — grep 'integrity' fmideas.py: 0 hits; fm ideas prints no pack-integrity line
- [partial] Keep a topic embargo list the pack always injects — fm vetoes (MASTER.md:558) keeps never-X words and lens notes quote them; no explicit embargo list in the pack
- [new] Shuffle pack section order to measure position bias — grep 'shuffle' fmideas.py: 0 hits

## c26 Brainstorm pack, slate and presentation

Mark: **skip** · value 2 · effort S · risk low — Mostly built or presentation-only; pack digest and numbering add little to coverage.

- [built] Make the brainstorm pack a diff, not a dump — fm ideas --seen/--seen-latest (fmideas.py:847-859, T-2559/T-1510)
- [partial] Replace the idea list in packs with a nearest-neighbour digest — later_round_pack lists all titles (fmideas.py:737); grep 'nearest.neighbo' lib: none
- [partial] Do less: freeze the pack at a clustered digest of at most 100 lines — PACK_WORDS=2000 warns only (fmideas.py:46,843); coverage() clusters by category (fmideas.py:744)
- [built] A/B the "ideas so far" list against a no-list pack — T-1150 forever loop round 2 compared; later_round_pack vs plain pack (fmideas.py:737)
- [new] Number every idea so round-2 ideas cite what they extend — grep -i 'extends|cite.*idea' fmideas.py: none; titles are unnumbered bullets (fmideas.py:908)
- [new] Show claimed value beside grounded value on every slate line — grep 'grounded value' lib: 0; slate lines carry only 'near T-' hint (fmideas.py:908)
- [partial] Preview exactly what a brainstorm pack sends out — manifest.json holds pack_sha256 (fmideas.py:927) after the fact; no --dry-run preview
- [built] Make the slate readable in one paste-able markdown file — ideas.md index written by cmd_ideas (fmideas.py:909)
- [new] Give each idea a first-screen sentence and lint for it — grep -i 'first-screen' lib: 0; _TITLE regex takes any bold title (fmideas.py:700)
- [built] Run the next lens in idle time while the user reads — T-1062 speculative next task; fm ideas children run in parallel (fmideas.py:781)
- [built] Stream ideas as each brainstorm child finishes — T-0696; status.json progress (fmideas.py:841), per-lens files written as they come
- [partial] Offer a local-only brainstorm for pack sections tagged private — fm sensitive marks projects; fm share off; ideas children are remote claude -p (fmideas.py:66); no local model
- [built] Triage the slate by swipe or keypress — fm inbox swipe (fmcli.py:7357, T-1664)
- [built] Show a mock of the output before asking for acceptance — T-0871 install.sh shows mock before bypass; fm design previews
- [built] Rank ideas by user-minutes, not build effort — T-0843; fm inbox first ready-S items (fmcli.py:7357)
- [new] (wild) Get a desk-lamp or tray colour for slate readiness — grep -i 'tray|lamp' MASTER.md/lib: statusline only (MASTER:91)
- [new] Let the hard hat live in the desktop tray as a posture lamp — grep -i 'tray|posture lamp' MASTER.md: statusline only; fm posture is lite/full (fmcli.py:7199)

## c27 Cost tallies and spend stops

Mark: **skip** · value 2 · effort S · risk low — Cost accounting, not coverage of the request.

- [new] Tally retries, hedges, fallbacks and skips with their dollars on every receipt — grep -i 'hedge' lib: only prompt text (fmcode.py:163); fmcost.py tally of retries: 0
- [new] Tally retries, fallbacks and hedges in the drive receipt — grep -i 'retries|tally' fmcost.py: none relevant; drive receipt lacks them
- [new] Price unknown model IDs at the highest known rate — grep -i 'MODEL_PRICES|unpriced|unknown model' fmcost/fmbudget: 0 hits (price table not located)
- [built] Reset the stall clock only on closes that landed something — fmserve.py:1041 resets since_close only when brief status == done
- [new] Default the stall limit from the user's own median task cost — fm run --stall-usd is explicit only (fmserve.py:901); queue --cost computes medians (CHANGELOG:506)
- [partial] Add a no-yield spend stop to model-spawning fan-out verbs — fm run --stall-usd (fmserve.py:925); fm ideas has only budget check (fmideas.py:834); no yield stop
- [built] (wild) Show dollars since the last close as a live meter — T-2669 --stall-usd prints since_close (fmserve.py:926)
- [new] Print the armed stops at the start of every `fm run` — grep -i 'armed|will stop' fmserve.py: 0 hits; stops announced only when hit (fmserve.py:922,926)
- [new] (wild) Report the energy and carbon cost of agent runs and CI re-runs — grep -i 'carbon|energy|kwh' lib: 0 hits

## c28 Dependency, credential and session awareness

Mark: **skip** · value 2 · effort M · risk low — session detection is built; docs caching and credential expiry are marginal here

- [partial] Cache dependency docs pinned to lockfile versions — fm deps --research (MASTER.md:583) leaves lockfiles out; grep 'docs cache|llms.txt' lib: only context7 mentions
- [partial] Warn before credentials expire — fmforesight.py warns of dated breakage (T-2408); grep 'credential.*expir' not matched as a check
- [built] Detect a second live session on the same repo — add('conductor') fmcli.py:6794 lists live sessions; claim --warn overlap (6793)

## c29 Docs, help and verb-surface hygiene

Mark: **skip** · value 2 · effort M · risk low — Hygiene and wild ideas; nightly README check is partly built via exam arms.

- [partial] Test every claim in the README against the code on one nightly pass — fmexam.py:1323,1392 README-claim planting arms; fmnight.py nightly; no pass over the real README
- [partial] Cut every verb's `--help` to one screen and enforce it — grep 'one screen' fmcli.py:6745,6948 and fmdoctor.py:2823 mention it for specific verbs; no enforcement test
- [new] (wild) Run a documentation-deletion exam — grep 'deletion exam|doc.*delet' plugin/lib: no hit
- [new] (wild) Read the repo as one scrolling page by blast radius — grep 'blast radius' plugin/lib: no hit; fm graph exists (MASTER)
- [new] Collapse alias spellings to one per verb and flag — grep 'alias' fmcli.py: no audit of duplicate spellings
- [new] Wild: Test whether every standing rule would survive its author's absence — grep 'author.s absence|bus factor' plugin/lib: no hit; fm evolve --drop ablates rules (fmnight.py:37)
- [partial] Wild: Hold a monthly "deleted by me" party — fmcli.py:2683 deletion honesty note; graveyard report fmcli.py:6765; no monthly ritual
- [new] Wild: Ask a cold child to guess each flag's meaning from its name alone — grep 'guess.*flag|cold child' fmexam/fmgenesis: cold readers exist for charter only
- [partial] Collapse `fm decide` kinds into one record with a "report" bit — near T-2342 (done) — T-2342 is stop-only-at-irreversible; fm decide kinds still separate in fmcli.py

## c30 Doctor, help and operator surface

Mark: **skip** · value 2 · effort M · risk low — Operator polish and tooling; `fm why-not` is the only item near coverage and is a thin wrapper of fm explain.

- [partial] Add `fm why-not` to explain why a nudge or guard rule did not fire — fm explain shows the newest block/drive decision (fmrecall.py:1188); grep 'why-not' : only fmcli why-not-caught text
- [new] Collapse `fm doctor` into one verdict line plus a red-only list — grep -i 'verdict line|red.only|--terse' fmdoctor.py: 0 hits
- [built] Print one "what to do now" line from bare `fm` — T-2641 fm --help everyday commands (fmcli.py:6161); fm next
- [built] Delete the verbs that have no session path, behind a tombstone — TOMBSTONES (fmcli.py:6064, T-2186/T-2641)
- [new] Fold the three ship-time gates into `fm gate` — fm gates/fm check/fm ship exist (verb list fmcli add()); no 'fm gate' verb; fm bench gate is separate (fmcli.py:7484)
- [partial] Cap injected session-start text to a fixed line budget with overflow behind `fm why` — fmdoctor.py:196 CTX_BUDGET chars FAIL; fm why is file blame (fmcli.py:7011), no overflow pointer
- [new] Generate man pages and `fm help --search` from the verb table — grep -i 'man page|help --search' lib: 0; fm which finds verbs by need (T-2371)
- [new] Count unrecognised transcript record types in every reader — grep -i 'unrecogni|unknown record' lib: only argparse messages; no per-reader counter
- [partial] Stamp the host CLI version on every hook ledger row — claude_version() (fmeco.py:1075) used by canary and bench (fmbench.py:732) only
- [new] Census protective flags that default off — grep -i 'default off|off by default' lib: 1 hit (fmfixes); no census verb
- [new] Stop the tower writing a new gauge unless a decision reads it — grep -i 'gauge' lib; no gauge-reader audit found
- [partial] Write hook stdout once, as a single JSON document — fmcli.py:3324 keeps --json to one document; hook dispatcher single-output rule not verified
- [built] Make every new capability pay a one-in, one-out toll — T-2097 fm exam scorecard per capability
- [partial] Run a diagnosability exam: a cold child names a planted fault from `fm` output alone (wild) — fm drill (fmdrill.py:192) and fm exam stranger newcomer (fmcli.py:7496); no planted-fault exam
- [partial] Let a cold child try to explain Foreman in five sentences, and fail the docs if it can't — fm exam stranger reads only README (fmcli.py:7496); fm docs drift (fmcli.py:8209)
- [new] Wild: Run a "one-page Foreman" week — grep -i 'one-page' repo: 0; fm posture lite exists (fmcli.py:7199)
- [new] Wild: Make deferred tasks expire into a single `someday.md` — grep -i 'someday' lib: 0; fmtidy expires decisions and asks only (fmtidy.py:301,328)
- [partial] Record a 30-second "first win" cast during install — demo/record.py makes a demo cast (README:647); install.sh records nothing
- [new] Route all dedupe through one similarity index — dedupe duplicated: _is_new (fmideas.py:725), nearest_done, playbook lint (fmplaybooks.py:4); no shared index
- [partial] Draw a "why not" ledger of what Foreman declined to build — decisions.md and dropped briefs with 'dropped:' reasons (fmideas.py:362); no single ledger view
- [built] Run lanes as multiplexer panes — T-1119 pane lane nodes; fm watch in tmux (MASTER:440)
- [built] Serve one local Foreman protocol that every surface reads — T-2371 fm which; fm serve (fmserve.py), fm mcp
- [partial] Compare held-rate anonymously against other users — fm exam steer held-rate (T-2625) local; fm share is opt-in lesson sharing, no anonymous benchmark
- [new] (wild) Record failing and flaky tests under `rr` and ship the replayable trace as evidence — grep -i 'rr record|flaky' lib: flaky rerun in fmeco.py:151; no rr

## c31 Objections, misreadings and reviewers

Mark: **skip** · value 2 · effort M · risk med — Plan objections and oracle misreadings already cover intake; finish-time forecast is marginal.

- [partial] Let Foreman object once, with evidence — fm second dissent (fmcli.py:6449) and T-0742 final run; no single evidence-bearing objection at intake
- [partial] Forecast the user's objections before the finish card — fmsecond.py:16 Objections section for the plan; fm oracle Misreadings (fmideas.py:955); not at finish
- [partial] (wild) Ghost reviewer: a tool-less child trained on the user's drops votes keep or drop on each slate first — taste() feeds dropped titles to packs (fmideas.py:356,330); tool-less children exist (NO_TOOLS); no keep/drop vote child

## c32 Catalogue shaping and grounding

Mark: **skip** · value 2 · effort L · risk med — mostly research; the one cheap item (re-ground on change) is covered by defer tags

- [partial] Select from the catalogue, don't generate — fmmoonshot.py catalogue and fmgenesis.py:1194 export it (T-2626); no select-only mode for brainstorm
- [partial] Re-ground catalogue entries when their files change — defer revisit_tag content hash (MASTER.md:577) exists; grep 'catalogue' fmmoonshot.py shows no re-ground-on-change
- [new] Collapse the catalogue into a subsumption tree — grep 'subsum' fmideas.py/fmmoonshot.py: none
- [new] Set-cover the catalogue to a build kernel — grep 'set.cover' lib: none
- [new] Zero-token candidate generator: operators × the verb table — grep 'operators' fmideas.py: none; Genesis A4/frontier (MASTER.md:146) uses model lenses
- [partial] Add a "Called by:" line to every idea — fmgenesis.py:778 (T-2184) requires each capability to be called by a real session path; ideas have no such line
- [partial] Add a local semantic code index — fm map/outline/sym/impact exist; grep 'embedding|tf-?idf' lib: only unrelated hits (fmrecall.py:51), no semantic index
- [partial] Run the same brainstorm blind, then subtract the catalogue mechanically — fmideas.seen_titles:713 and _is_new:725 dedupe against earlier titles; no blind run
- [partial] Union two model families and rank by single-finder novelty — Genesis tower finders carry a FLOOR and BAR (MASTER.md:148); fm ideas uses one family
- [new] Backtest recall on foreign repos' later issues — grep 'foreign|later issues' fmexam.py/fmfind.py: none; held-out exam covers own cases only
- [new] Grade grounding by acceptance sampling, not "spot checks" — grep 'acceptance sampling' lib: none
- [new] Mask the verbs and let a child reinvent them — grep 'reinvent|mask the verbs' lib: none

## c33 Delivery: monorepo, release, stacks

Mark: **skip** · value 2 · effort L · risk med — release is built; monorepo gates and stacks are large and speculative for this user's repos

- [partial] Make gates and tasks workspace-aware for monorepos — grep 'monorepo' lib: fmlib.py:466 scans nested manifests; fmdocs.py:157 'nested packages are not read'; gates are repo-root only
- [partial] Split a landed lane series into a stack of green, reviewable changes — fm lane + merge train exist (T-0710); add('split') fmcli.py:6473 splits tasks; no lane-to-stack splitter found
- [built] Add `fm release`: semver, tag, notes and artifact check in one gated verb — add('release') fmcli.py:7021; fmrelease.py (T-1188); T-2390 runs it in any repo
- [new] (wild) Maintain a patch queue over an upstream fork or PKGBUILD — grep 'PKGBUILD|patch queue' plugin: no hits
- [new] Run lanes in microVMs that restore from a snapshot — grep 'microVM|firecracker' lib: no hits. T-2652 is fm drill --restore (upgrade snapshot), not lane isolation

## c34 Guard degraded states and protection witnesses

Mark: **skip** · value 2 · effort L · risk high — Guard hardening is valuable but not exhaustive thinking about a request; canary grant needs design.

- [new] Plant a canary grant and prove no spawned process class can spend it — grep -i canary lib: fm canary tests host CLI version (fmeco.py:1049); no grant canary
- [partial] Break the guard's own state one file at a time and record what each unattended path does — fm drill (fmdrill.py), fm fsck; T-0706 is delta debugging; per-file state-break matrix not found
- [partial] Test the guard's degraded states, not only its rules — fm drill and fsck exist; hooks fail closed via fmpy child (MASTER fmpy); T-2661 was a rule fix
- [new] Witness protected paths across IDE terminals, cron and CI — grep -i 'IDE terminal|protected path' lib: cron only as night timer (fmnight.py:120)
- [partial] Give sub-agents a "blocked by policy" outcome with the one-line widening command — fmguard hint text on blocks; fm trust/standing widen; grep 'blocked by policy' lib: 0
- [new] Surface a sub-agent's allowlist block as its own outcome — grep -i 'blocked by policy|allowlist' lib: fmhome sync allowlist only; fm outcomes has no such class
- [partial] Fall back to the previous install generation on a hook import failure (wild) — fmpy re-exec child keeps guard from failing open (MASTER:121); fm rollback --list snapshots (fmdrill.py:300); no auto fallback
- [partial] Replay a museum of tasks that once hung or crashed the drive (wild) — fmreplay.py replays guard commands; fmlanes.py:335 detects hangs; no stored hung-task corpus
- [new] Port the hook path to a static binary, held to a recorded corpus — grep -i 'static binary' repo: 0; hooks are Python via fmpy
- [partial] Make every bypass session replayable as a sandboxed rehearsal — fm sandbox (fmcli.py:8192), fmreplay guard replay; bypass-session rehearsal not found
- [new] (wild) Inject a canary through every context channel — grep -i canary lib: only version canary (fmeco.py:1049); no context-channel injection
- [partial] Census every context channel against the gauges that read it — fmdoctor.py:196-218 budgets SessionStart/UserPromptSubmit; other channels (rules, skills) pooled fmdoctor.py:256
- [partial] Run a pathological-input latency suite over every hook-path parser — see test cluster; grep 'pathological' tests: none

## c35 Local models for fm code

Mark: **skip** · value 2 · effort L · risk med — bench and probing exist; the rest is speculative and needs hardware

- [partial] Probe local engines and pick a ceremony for `fm code` — fmmodels.py:71 LOCAL probes ollama/lmstudio/llamacpp/vllm; grep 'ceremony' lib: 0 hits, so no per-engine ceremony choice
- [partial] (wild) Run a local-model league on the user's own closed tasks — fm code bench (fmcodebench.py) grades a model on seeded tasks; add('bench') builds from finished tasks (fmcli.py:7403); no league ranking
- [partial] Run an offline parity score for `fm code` on a local model — fm code bench --variants (MASTER.md:132); grep 'parity' fmcli.py: 0 hits, so no score against a cloud baseline
- [partial] Run local-model brainstorm lenses on idle hardware — fmideas.py run_children uses claude -p children; fmmodels LOCAL profiles exist but no idle-hardware scheduling
- [new] Wild: Distil a small local model of the user's judgement overnight — grep 'distil|fine-tune' lib: none; fm taste (fmideas.py:356) is rule-based

## c36 Simulated worlds and wild drills

Mark: **skip** · value 2 · effort L · risk med — Mostly wild or already covered by drill, bench, backtest and exam arms.

- [new] Stamp lane records with a vector clock (wild) — grep 'vector.clock' plugin/lib: no hit
- [partial] Run a recovery theater in a scratch home (wild) — fm drill --restore (T-2652) and fm rollback (fmrollback) restore snapshots; no scripted theater
- [partial] Run a silence drill that times who notices (wild) — fmdoctor.py:1652 check_heartbeats warns on overdue run; fmexam stalled-lane arm fmexam.py:2640; no timed drill
- [partial] Run the whole product in a seeded simulated world — fmdojo --seed, fmbench soak shadow-user, fmdemo exist; grep 'simulat' no full world
- [partial] Stand up a standing Anti-Foreman adversary that is scored on lies it finds (wild) — CHANGELOG:217 Mission 4 adversary spike; fmexam 'plant one false sentence' arm fmexam.py:1323
- [partial] Wild: Dry-run the user's day on yesterday's ledger with a candidate steer applied — fmbacktest.py: fm backtest --rule replays recent sessions (MASTER:590); steers not applied as candidate
- [partial] Wild: Leave a replayable "morning after" bundle for each overnight run — fm night writes digest (fmnight.py:6); no replayable bundle
- [partial] (wild) Hand out a redacted capsule that reproduces a failing task for a friend — fmsplit 'fm task capsule' is a child return (MASTER:224); fmcore redact exists; no shareable repro
- [new] Wild: Distil a small local model of the user's judgement from their accepts and drops — grep 'distil' plugin/lib: no hit
- [new] Wild: Environment bingo, where a child invents a hostile first-day host — grep 'bingo|first-day host' plugin/lib: no hit; fmexam has host arms only

## c37 Steering rules and scoping

Mark: **skip** · value 2 · effort L · risk med — Path scoping of steers would help but needs steer-format changes; others are speculative.

- [partial] Delete the steer expander unless it beats verbatim — fmsteer.py:153 expander was reverted once, :181 judges compare expanders; no standing beat-verbatim gate
- [new] Compile a plain-words session charter into sandbox, guard rules and an after-session check — grep -i 'charter' lib: only genesis charter (fmgenesis.py:1484); no session charter
- [new] Scope steers to paths and stacks — near T-2600 (done) — T-2600 is fm lib dependency reader; grep -i 'scope|paths' fmsteer.py: no hit
- [partial] Choose injected-note wording per model family by exam — grep -i 'model famil' lib: none; fmexam model arms (T-2487) per use; fmmodels.py per model
- [partial] Run Foreman as a signed protocol server any agent can plug into — fmmcp.py exists (MCP server); no signing
- [new] Compile steers, lessons and guard rules into the other harnesses' native files — grep -i 'AGENTS.md|cursorrules|GEMINI' lib: no hit
- [built] Wild: A "stop-the-line" word the user can type in any pane — near T-0957 (done) — T-0957 hooks: user's stop recorded (CHANGELOG:1173); grep 'stop-the-line' empty
- [partial] Pre-flight a Mission's brief set for contradictions with standing steers — fmgenesis.py:105 _mission_grounded, :2494 BREAKS drift vs user-steers; briefs pre-read exists, not for all briefs

## c38 User-facing cards, cost and prediction

Mark: **skip** · value 2 · effort L · risk med — Mostly speculative or visual; the buildable parts are already covered by todo, forecast and backtest.

- [partial] Ship the do-less cost view: Pre-fund each task from its forecast and stop on overdraft (wild) — fmserve.py:901 --stall-usd and --max-usd cap spend; forecast fmbudget.forecast; no per-task prefund
- [new] Pre-answer the three likeliest follow-up asks on every finish card (wild) — grep -i 'follow-up' finish card code: no hit
- [partial] Show each task's cost against the user's review time on the finish card — near T-0913 (done) — T-0913 closing moment; cost shown; review time absent (grep 'review time' empty)
- [built] Report the share of generated work the user could not have predicted from gen-0 — near T-2505 (done) — fmgenesis.py:3648 PRED_ROW sealed prediction (T-2505)
- [partial] Keep a per-Mission spend envelope visible against the $200 cap — fm cost, --max-usd (fmcli.py:8171); no per-Mission envelope
- [new] (wild) Record which diff hunks the user actually read — grep -i 'hunks? (the user )?read' lib: no hit
- [partial] Make felt cost the tuning signal for everything Foreman says — fm burden counts context delivered; fmexam LEAN_METRICS inject_chars_per_turn (fmexam.py:2765)
- [new] Draft upstream host bug reports from host-blocked tasks — grep -i 'upstream.*bug|host.blocked' lib: no hit
- [built] Settle each costly self-made decision against later evidence — fm todo shows costly decisions unsettled by later reversal (MASTER:475); fmoutcomes.py:253 _regret
- [partial] Rerun settled bets with the data that arrived later, and report which lens was wrong (wild) — fmoutcomes.py settle/claims/regret reports (fmoutcomes.py:216); no lens attribution
- [partial] Seal the final-report forecast at generation 0 and score it at the end — fmgenesis.py:3648 seals a prediction of user steers at gen-0 (T-2505); not final report
- [partial] Mine `fm ask` timeouts to learn which questions were not worth asking — fm ask tally FATIGUE_ASKS (MASTER:544); pending asks expire APPROVAL_TTL; no mining
- [new] Schedule one shared quota across all registered repos by marginal yield per dollar — grep -i 'quota|marginal' fmbudget/fmeco/fmserve/fmcost: one eco hit, no scheduler
- [new] Expose state as a mountable filesystem, Plan 9 style (wild) — grep -i 'fuse|9p|plan 9' lib: no hit
- [partial] Build a policy lab: every decider registered, any change replayable — fmbacktest.py replays rule/fix/card changes; fmreplay --candidate guard; no decider registry

## c39 History search and catalogue-first answers

Mark: **skip** · value 1 · effort S · risk low — Search and precedent are built; the movie is visual-only.

- [built] Search your own history in your own words — fm recall / fm show other-words -> recall (fmcli.py:7017, fmrecall.py)
- [built] Search every past session and ledger with local full-text search (`fm recall --grep`) — fm recall searches sessions and ledgers (T-0694); only the flag name --grep is absent (fmcli.py:8224 --grep is fm projects --sweep)
- [built] Answer the ask by searching the catalogue first — fmideas.precedent (fmideas.py:571, T-1064): fm decide --ask answers from prior identical answers
- [partial] Replay the last 30 days of asks as a Monday-morning movie — grep 'movie|replay' : fm timeline/fm digest weekly (fmcost.py:860) exist; a movie is visual-only

## c40 Distribution, site and export

Mark: **skip** · value 1 · effort M · risk low — Packaging and showcase items do not widen request coverage.

- [new] Ship an Arch AUR package for Foreman — grep -i 'AUR|PKGBUILD' README.md plugin/*.sh: no hit
- [partial] Tag every Genesis generation and offer a one-command rollback — fm rollback (fmrollback) restores state snapshots (MASTER:263), not generation tags
- [new] Gate the site on accessibility, links and weight — grep -i 'accessib|broken link|page weight' lib: no hit
- [new] Export deferred tasks as contributor-ready issues — grep -i 'export.*issue' lib: fm inbox gh imports only
- [new] Run a hardened-kernel verb matrix — grep -i 'hardened' lib: no hit
- [partial] Harvest dated TODOs into the queue — near T-2374 (done) — T-2374 fm ask --later queue; fmnight.py:396 dates about to pass; grep TODO fmnight no harvest
- [built] (wild) Export closed tasks as SWE-bench-style instances — fmbench.py:5 fm bench build replays finished tasks as fail-to-pass cases
- [partial] (wild) Ask your history and get a cited answer, brag doc and notes vault — fm recall (fmrecall.py), fm why; no brag doc or vault export
- [new] Publish the forecast as a subscribable calendar feed (wild) — grep '\.ics|iCal|VEVENT' lib: no hit; fm cost --forecast exists (MASTER:613)
- [new] Wild: Foreman Wrapped — grep -i 'wrapped' lib: no hit; fm digest exists
- [new] Wild: Reply to the final report in advance — grep -i 'in advance' report code: no hit
- [new] Wild: Add a "things you'll ask me within a week" card at Mission close — grep -i 'within a week' lib: no hit

## c41 Fleet and cross-repo operations

Mark: **skip** · value 1 · effort M · risk med — Fleet writes cross-repo are outside exhaustive thinking about one request; the read half already exists.

- [built] Open one cross-repo inbox — fm inbox gh:OWNER/REPO#N (T-1869, CHANGELOG); fmeco.py inbox_gh; fm projects
- [built] Port a fix to the user's other repos — fm projects --sweep (fmeco.py:79, T-0443): asks sibling projects whether a fix applies; MASTER fmeco
- [partial] Apply one change across several registered repos with a rollup receipt — grep 'several repos|across all projects|--sweep' fmeco.py: sweep only reports; fm sub --apply is per-repo. No cross-repo apply or rollup
- [new] Export closed tasks as billable time entries — grep -i 'billable|time entr|timesheet|invoice' plugin/lib/*.py: 0 hits

## c42 Maintainer and user-facing writing

Mark: **skip** · value 1 · effort M · risk low — Outputs for other people, not coverage of the user's request.

- [new] Draft maintainer replies to incoming issues, with a repro attempt — grep -i 'maintainer|issue repl' lib: only review-lens names; fm inbox gh imports issues, fm repro exists, no reply
- [partial] Write the user a brag document — fm digest weekly (fmcost.py:860) lists finished work; grep brag: none
- [new] Export decisions and lessons as a linked notes vault — grep -i 'obsidian|wikilink|notes vault' lib *.py: 0; fm export exists (fmcli.py:7010) for other data
- [partial] Swap a redacted failing-task capsule with a friend — fm share (cross-project lessons) and fm task capsule (split child); grep 'friend|swap' none
- [new] (wild) Print a silence letter: what I considered saying and held back — grep -i 'silence|held back' lib: none; fm quiet is output compaction
- [partial] Quote a price and odds before taking a task — fm queue --cost quote (fmcli.py:7162, T-1878), fmcli.py:5362 gate odds; no per-task odds quote

## c43 Provocation lenses and wild ideation

Mark: **skip** · value 1 · effort M · risk low — speculative; the oblique and crossbreed lenses already cover the useful part

- [built] Deal Oblique-Strategies provocation cards to lenses (wild) — fmideas.py:25,33,820 'oblique provocation' lens from the project's own lessons (T-0628)
- [partial] Constraint roulette lens (wild) — grep 'roulette' lib: none; the 'oblique provocation' and 'flip assumptions' lenses (fmideas.py:25) are the nearest
- [new] Life-event deck: forty things that happen to the owner (wild) — grep 'life-event|deck' fmideas.py: none
- [partial] Hybrids that must shrink the catalogue (wild) — fmideas._crossbreed:766 (--crossbreed) exists; no shrink requirement
- [new] Run an idea séance with the ledger's last dissent (wild) — grep 'séance|seance|dissent' lib: none
- [new] Write the README for one year ahead and diff it (wild) — fmgenesis._prose reads README (MASTER.md:146); grep 'one year ahead' lib: none
- [new] Hardest-buyer FAQ as a doc-gap detector — grep 'FAQ|hardest-buyer' lib: none; fm docs --strict checks docs structure only
- [partial] Incubate every new idea for seven days — fm task defer --until DATE (fmcli.py:6677) could do it; no automatic incubation
- [partial] Wild: resurface one old deferred idea each morning with today's evidence — defer --until 'when PATH changes' (MASTER.md:577) resurfaces deferred work; no daily evidence-based pick
- [new] Wild: let a dormant-idea garden stand in for the idea list — grep 'garden|dormant' lib: none
- [partial] Wild: stage a felt-change bet at each Mission open and settle it at close — gen-N/prediction.md sealed and scored (MASTER.md:146, T-2505); not per Mission

## c44 Speculative wild ideas

Mark: **skip** · value 1 · effort L · risk med — wild and visual-only; no grounded value for exhaustive thinking

- [partial] (wild) Rehearse a week of silence — fmaway.py GAP = 2h silence logic; fm drill rehearses restore (fmdrill.py:289); no silence rehearsal
- [new] (wild) Map a macro pad or foot pedal to Foreman verbs — grep 'macro pad|foot pedal' lib: none
- [new] Wild: Turn state into a haptic grammar for phone and watch — grep 'haptic' lib: none
- [partial] (wild) Prognosis letter scored against what happens — sealed gen-N/prediction.md scored by T-2505 (MASTER.md:146); not a letter per task
- [new] Run a receipts-only week (wild) — grep 'receipts-only' lib: none
- [partial] Quarantine unreferenced skills behind a stub index (wild) — fm usage lists never-used skills (fmcli.py:6863); no quarantine
- [new] Type every string with its provenance — grep 'provenance' lib: no typed-string mechanism; plain() fences untrusted text
