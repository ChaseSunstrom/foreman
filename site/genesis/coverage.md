# Coverage — gen 1

Status: `fm genesis check` counts this file's cells (each `- stage × surface:` line is one) and lists the open ones. F names code that exists on that surface and how it's reached; Ideas aren't cells: an open cell is a gap until code fills it. Most cells are open, and gen 1 doesn't meet this grid: the open cells are its gaps and rank the next seed's Missions. Whether any F works is exam.jsonl's to say; no cell claims a pass.

## 1. Initiative
- find × MCP: F: plugin/lib/fmmcp.py — the `find` tool hands any MCP client fm find's ranked candidates, so other agents and Desktop read the same leads
- find × CLI: F: plugin/lib/fmfind.py — `fm find --rank` runs the ordered ladder over a repo with no request: its free finders, each stack's standard analyzer (the tool rung, T-2239), Foreman's tree-sitter rules (T-2240) and the git hotspots where fixes landed (--hotspots, T-2238), then ranks the candidates; the MCP find tool runs it
- verify × CLI: F: plugin/lib/fmprove.py — `fm prove` re-checks fm find leads on a throwaway copy (an untested function only in a tree you said yes to; docs, dep and secret findings found again cold); the other kinds stay leads
- build × Claude Code: F: plugin/lib/fmprove.py — `fm prove --capture` files each proven lead as a planned S task whose criterion is red until fixed, so the session's own fm next loop fixes it
- operate × Claude Code: F: plugin/lib/fmscout.py — when a full-autonomy queue drains and the quick probes find nothing, the Stop hook asks the session to run `fm scout --slow`, whose find probe files at most 3 proven leads a day on the user's own project
- plan × Claude Code: F: plugin/skills/initiative/SKILL.md — /foreman:initiative plans an unattended run: map the repo, find candidates, prove them, fix the proven ones test-first on lanes, stop at a receipt
- build × CLI: F: plugin/lib/fmdraft.py — a headless claude drafts the top queued S task in a throwaway worktree
- operate × CLI: F: plugin/lib/fmorders.py — standing orders capture a task on a schedule or when a file changes

## 2. Exhaustive thinking
- find × CLI: F: plugin/lib/fmideas.py — the brainstorm skill runs `fm ideas`, whose tool-less lens children return deduplicated ideas, each naming the finished task it may repeat
- understand × CLI: F: plugin/lib/fmmission.py — mission lenses and surfaces enumerate every reading of an open request
- plan × CLI: F: plugin/lib/fmsecond.py — cold second opinion, debate and dissent kept open in the brief
- verify × Claude Code: F: plugin/agents/fm-reviewer.md — one read-only reviewer per audit lens (intent, adversary, edge, operator, maintainer)
- verify × CLI: F: plugin/lib/fmauditrun.py — fm audit run starts one headless claude per lens with only Read, Grep and Glob allowed and merges what they return
- learn × CLI: F: plugin/lib/fmtaste.py — lens keep rates feed which lenses get more weight next brainstorm

## 3. Anticipation
- find × Claude Code: F: plugin/lib/fmforesight.py — the Stop hook's sweep caches a changed model, window or Claude Code version, and session start names it before it bites
- understand × MCP: F: plugin/lib/fmmcp.py — the impact and why tools answer blast radius and history read-only
- understand × CLI: F: plugin/lib/fmgraph.py — fm graph blast shows a change's blast radius from one local graph
- verify × CLI: F: plugin/lib/fmreverify.py — fm sentinel re-queues old passing criteria when a later commit touches their files
- operate × CLI: F: plugin/lib/fmrisk.py — the daily risk budget steps autonomy down after destructive blocks and reverts
- learn × CLI: F: plugin/lib/fmrecall.py — fm recall and fm dream keep failure memory so a repeat is foreseen

## 4. Goal to finish
- understand × MCP: F: plugin/lib/fmmcp.py — state and next tools show the one next required action
- plan × CLI: F: plugin/lib/fmcore.py — briefs with acceptance criteria and steps, each tied to a verify command
- build × Claude Code: F: plugin/lib/fmhooks.py — the Stop hook drives on while open work remains and refuses a premature done
- build × fm code: F: plugin/lib/fmcode.py — fm code runs Foreman's loop on the open task to the end of its plan
- build × other agents: F: plugin/lib/fmagents.py — Codex gets the Stop drive and done-gate; Gemini and opencode have no Stop
- verify × CLI: F: plugin/lib/fmcore.py — fm task finish closes only on fresh evidence for every criterion

## 5. Getting the tools it lacks
- find × fm code: F: plugin/lib/fmcode.py — fm code offers one matching indexed skill at a run's start
- find × CLI: F: plugin/lib/fmplugins.py — fm plugins find searches for a plugin that covers a missing need
- understand × Claude Code: F: plugin/skills/library/SKILL.md — stack cards with verify commands before coding in a framework
- understand × MCP: F: plugin/lib/fmmcp.py — lib_suggest, lib_search and lib_show serve stack cards read-only
- plan × CLI: F: plugin/lib/fmwhich.py — fm which names the skill, playbook or command that fits a task
- build × CLI: F: plugin/lib/fmplugins.py — fm plugins install adds a pinned plugin only after the user's yes to fm ask ID plugin
- learn × CLI: F: plugin/lib/fmrepeats.py — fm tidy's repeats finding points a session at fm repeats, which drafts a playbook, script or check from repeated manual step sequences

## 6. Verifying anything
- understand × CLI: F: plugin/lib/fmdebug.py — fm whyred ranks suspects and minimal failing hunks for a red run
- verify × fm code: F: plugin/lib/fmcode.py — fm code's steps close through the same evidence runs
- verify × CLI: F: plugin/lib/fmcore.py — fm task evidence --run runs the command itself and stores its exit and output, so a pass is never typed in
- verify × headless/server: F: plugin/lib/fmserve.py — fm run sessions close tasks through the same gates
- ship × CLI: F: plugin/lib/fmledger.py — fm verify-ledger proves the hash-chained record line by line
- operate × CLI: F: plugin/lib/fmsmoke.py — fm smoke crawls the web UI at desktop and phone width
- learn × CLI: F: plugin/lib/fmoutcomes.py — each finished task's fate (reverted, fixed later, held) scores its verification

## 7. Self-repair and self-improvement
- find × CLI: F: plugin/lib/fmfriction.py — fm friction mines stage paths, weak closes and give-up points
- understand × CLI: F: plugin/lib/fmdoctor.py — fm doctor and fm wiring show what is wired and what is broken
- plan × CLI: F: plugin/lib/fmevolve.py — fm evolve revises one instruction file on its own branch from bench and friction
- build × Claude Code: F: plugin/skills/improve/SKILL.md — eval-gated changes to Foreman itself in a worktree
- ship × CLI: F: plugin/lib/fmrollback.py — a snapshot before each new version and fm rollback to restore it
- operate × CLI: F: plugin/lib/fmtidy.py — fm tidy repairs drift and dead state
- learn × CLI: F: plugin/lib/fmtrials.py — a self-change is a pre-registered trial graded on ledger event rates

## 8. Calibrated judgment
- understand × CLI: F: plugin/lib/fmexam.py — the exam grades agents on held-out scenarios that outside (child) authors write, kept apart from any Foreman wrote itself (T-2204)
- learn × Claude Code: F: plugin/lib/fmhooks.py — the track record by type and tier is injected at focus
- find × Claude Code: I: fm find --rank states each lead's chance of being real beside its rank, booked so a proven or dropped lead scores the number (plugin/lib/fmfind.py)
- find × fm code: I: fm code's planner states a percent per hotspot before it reads one, settled when that hotspot yields a fix or nothing (plugin/lib/fmcode.py)
- find × other agents: I: the AGENTS.md block asks another harness to put a percent beside each bug it claims, so fm outcomes can score that harness's claims (plugin/lib/fmagents.py)
- find × MCP: I: the MCP find tool returns each lead's stated chance with the lead ledger's real hit rate for that 10-point bucket (plugin/lib/fmmcp.py)
- find × Desktop: N/A: the desktop app lists projects and their next action; no lead is found or scored there
- find × site: I: the Judgment page shows lead calibration: of the leads stated at 70–80%, the share that proved real (site/pages.py)
- find × CLI: F: plugin/lib/fmoutcomes.py — fm outcomes --judgment lists stated-confidence buckets per kind beside what held, which finds the kinds whose numbers are off (T-2344)
- find × headless/server: I: the nightly digest names the bet kind whose Brier trails its base rate most this week as the next calibration target (plugin/lib/fmnight.py)
- understand × Claude Code: I: fm next says when the active plan's Choice percent sits 20+ points above the held rate for its type and tier, with that rate (plugin/lib/fmhooks.py)
- understand × fm code: I: the fm code TUI shows the run's stated Choice percent beside the type and tier base rate before the build station starts (plugin/lib/fmcodetui.py)
- understand × other agents: I: a bet records which harness stated it, so fm outcomes --judgment can show one harness's record apart from the others (plugin/lib/fmoutcomes.py)
- understand × MCP: F: plugin/lib/fmmcp.py — the calibration tool returns the buckets, the stated Brier beside the base rate's, the bars, races and parked doors, and writes nothing (T-2344)
- understand × Desktop: I: each project row in Foreman Desktop carries its stated Brier against its base rate, read from fm projects --json (plugin/lib/fmwatch.py)
- understand × site: F: site/pages.py — the Judgment page renders confidences scored, the stated Brier against the base rate's, races lost and the race bar from fm outcomes --judgment --json (T-2344)
- understand × headless/server: I: fm serve's status reply carries the calibration snapshot, so a remote viewer reads the record with no session open (plugin/lib/fmserve.py)
- plan × Claude Code: F: plugin/lib/fmcli.py — the M/L plan gate needs two readings, 3+ fails-if options and Choice N (NN%); a choice under 80% needs fm second rival and each dissent resolved (T-2344)
- plan × fm code: F: plugin/lib/fmcode.py — the PLAN slot asks for a choice and a whole-percent confidence, writes Choice N (NN%): why, and refuses a number outside 0–100
- plan × other agents: F: plugin/lib/fmagents.py — the AGENTS.md plan line asks other harnesses for 2 readings, 3+ fails-if options and Choice N (NN%) (T-2344)
- plan × MCP: I: a plan_check MCP tool scores a draft's Choice percent against the type and tier base rate before the plan is filed (plugin/lib/fmmcp.py)
- plan × Desktop: N/A: plans are written in sessions and briefs; the desktop shows project state, not plan text
- plan × site: I: the Planning page quotes a real plan's Choice line next to how often plans stated in that bucket held (site/pages.py)
- plan × CLI: I: fm task set --section Approach warns when the Choice percent is 20+ points above the pair's base rate and names that rate (plugin/lib/fmcli.py)
- plan × headless/server: I: fm run's headless sessions meet the same stated-percent plan gate, so queue work feeds the ledger like session work (plugin/lib/fmserve.py)
- build × Claude Code: F: plugin/lib/fmlanes.py — fm lane race runs rival builders when the plan's percent is under the race bar; the race_pick row records whether the first choice lost (T-2344)
- build × fm code: I: fm code books the build station's retries against the plan's percent, so a plan that needed three tries scores as an over-bet (plugin/lib/fmcode.py)
- build × other agents: I: a lane built by another harness (codex, gemini) meets the same race bar, so its Choice percent decides whether a rival runs (plugin/lib/fmagents.py)
- build × MCP: I: an MCP bet tool records an outside agent's stated percent on a task, write-once like the judgment ledger's rows (plugin/lib/fmoutcomes.py)
- build × Desktop: N/A: building happens in sessions and lanes; the desktop app starts none
- build × site: N/A: the site is a static report of the record; nothing is built or bet from it
- build × CLI: F: plugin/lib/fmoutcomes.py — a decision bet is missed when a later fm decide row reverses it and held after SURVIVE_DAYS (30) unreversed; its own signal, so it never moves a bar (T-2344)
- build × headless/server: I: each night lane states its percent at launch, and its merge or block settles the bet (plugin/lib/fmnight.py)
- verify × Claude Code: I: fm task finish asks an S task with no plan percent for the chance the close holds, so small work enters the ledger too (plugin/lib/fmcli.py)
- verify × fm code: I: fm code's verify station books its first-run result against the plan's percent, so each run scores its own planner (plugin/lib/fmcode.py)
- verify × other agents: I: the exam scores a plain harness's stated confidences with the same Brier as Foreman's arm, so the two records compare (plugin/lib/fmexam.py)
- verify × MCP: I: the calibration tool adds reliability bins (stated bucket against held share) so a client can draw the curve itself (plugin/lib/fmmcp.py)
- verify × Desktop: N/A: scoring runs where the ledger lives; the desktop reads only its summary through fm projects
- verify × site: I: the Judgment page draws a reliability curve, stated bucket against held share, beside the Brier pair (site/pages.py)
- verify × CLI: F: plugin/lib/fmoutcomes.py — settle() grades each write-once bet once its signal speaks, and the Brier is read against the type and tier base rate (T-2344)
- verify × headless/server: F: plugin/lib/fmexam.py — the foresight arm scores stated confidences by Brier, an unstated one counted at 50 (T-2366)
- ship × Claude Code: F: plugin/lib/fmcli.py — a plan's one-way steps are each undone or parked at a door, and fm decide --review prices each parked door by its wait (T-2346, T-2347)
- ship × fm code: I: fm code's close states the chance the change survives seven days, settled by fm outcomes' survival check (plugin/lib/fmcode.py)
- ship × other agents: I: another harness's commit hook records its stated chance the change holds, so its ships join the same ledger (plugin/lib/fmagents.py)
- ship × MCP: N/A: the MCP server pushes nothing; shipping belongs to fm ship and a session
- ship × Desktop: N/A: the desktop app pushes nothing; it shows what a push left behind
- ship × site: I: each release on the site shows the risk stated at ship beside whether a revert or hotfix followed (site/pages.py)
- ship × CLI: I: fm ship states the chance CI's blocking jobs pass on the pushed commit, and fm ci-watch settles it (plugin/lib/fmrelease.py)
- ship × headless/server: I: a release cut by fm release states the chance it needs a hotfix within a week, settled from the revert log (plugin/lib/fmrelease.py)
- operate × Claude Code: F: plugin/lib/fmoutcomes.py — the research and race bars live in project meta and are read by every plan, a hand-set bar above BAR_MAX kept (T-2344)
- operate × fm code: I: fm code reads the same research bar to decide whether a run researches before it plans (plugin/lib/fmcode.py)
- operate × other agents: I: other harnesses' hooks read the bars from fm state --json, so they race and research at Foreman's thresholds (plugin/lib/fmagents.py)
- operate × MCP: I: the MCP state tool includes the bars, so an outside agent knows when Foreman would research or race (plugin/lib/fmmcp.py)
- operate × Desktop: I: Foreman Desktop shows a project's bars and resets one through fm, with a decision row saying why (plugin/lib/fmwatch.py)
- operate × site: N/A: the site reports the bars (understand × site); it runs nothing against them
- operate × CLI: I: fm outcomes --judgment --set-bar research=N sets a bar by hand and writes the decision row that says why (plugin/lib/fmoutcomes.py)
- operate × headless/server: I: fm run's worker checks the research bar before each queued task, as a session's plan gate does (plugin/lib/fmserve.py)
- learn × fm code: I: fm code writes each closed run's stated percent and outcome into the judgment ledger, so its planner's misses move the bars too (plugin/lib/fmcode.py)
- learn × other agents: I: a harness whose Brier trails the base rate over 20 bets has its stated percents shrunk toward that rate before they gate a race (plugin/lib/fmoutcomes.py)
- learn × MCP: I: the model layer's decide answers, MCP ones included, are scored in the same per-kind Brier table as stated confidences (plugin/lib/fmmodels.py)
- learn × Desktop: N/A: the bars move from the project's ledger; the desktop only reads the result
- learn × site: I: the Judgment page plots each bar's moves over time with the bucket that moved it (site/pages.py)
- learn × CLI: F: plugin/lib/fmoutcomes.py — adjust_bars() raises the research bar when a kind is 15+ points overconfident over 20+ scored closes, registers the raise as a trial and writes its decision row
- learn × headless/server: I: the nightly digest settles the day's bets and adjusts the bars, so a project with no sessions still learns (plugin/lib/fmnight.py)

## 9. Orchestration
- find × Claude Code: F: plugin/agents/fm-debugger.md — fresh-eyes debugger returns ranked hypotheses with a probe each
- understand × Claude Code: F: plugin/agents/fm-recon.md — read-only recon subagent with a bounded, cited summary
- plan × CLI: I: fm next offers fm task split when an L task's files fall into independent groups, so lanes can take the children (plugin/lib/fmsplit.py)
- build × Claude Code: F: plugin/agents/fm-builder.md — one S/M task built test-first in a worktree on its own branch
- build × other agents: F: plugin/lib/fmsession.py — fm session runs detached claude, codex, gemini and opencode sessions
- build × CLI: F: plugin/lib/fmlanes.py — fm lane runs git worktrees as lanes with their own active task
- ship × CLI: F: plugin/lib/fmpr.py — fm pr train merges approved green PRs in order, each spending its task's publish grant (fm ask ID publish, the user's yes) before it posts
- operate × CLI: F: plugin/lib/fmbus.py — fm bus passes messages and leases between sessions on a machine

## 10. Beyond code
- find × Claude Code: F: plugin/skills/research/SKILL.md — cited research before building, saved as one note
- find × MCP: F: plugin/lib/fmmcp.py — research_list and research_read serve saved notes
- understand × CLI: F: plugin/lib/fmresearch.py — fm research stores and finds cited notes
- plan × Claude Code: F: plugin/skills/directions/SKILL.md — six style directions, the pick saved as DESIGN.md
- build × Claude Code: F: plugin/skills/ui-design/SKILL.md — direction, tokens, motion and QA for pages and scenes
- verify × CLI: F: plugin/lib/fmoffice.py — fm check office asserts spreadsheet and Word deliverables
- operate × CLI: F: plugin/lib/fmdocs.py — fm docs reports doc drift against the code
- learn × CLI: F: plugin/lib/fmtaste.py — the taste ledger learns which looks the user kept or reverted

## 11. Self-triggering
- find × Claude Code: F: plugin/lib/fmscout.py — the idle-turn hook runs scouts and captures findings
- build × CLI: F: plugin/lib/fmloop.py — with fm loop on, the Stop hook's drive starts the next improvement round each time the queue drains (T-1057)
- build × headless/server: F: plugin/lib/fmserve.py — fm run works the queue in fresh headless sessions, one task each
- verify × Claude Code: F: plugin/lib/fmambient.py — tests run detached after each edit with no prompt
- learn × CLI: F: plugin/lib/fmfriction.py — once fm friction --every N is set, fm next offers the self-improvement pass every N closes

## 12. Staying lean and safe
- plan × CLI: F: plugin/lib/fmbudget.py — subagents wait at 90% of the 5-hour window, or when weekly usage reaches 90% or, past 75%, runs 10+ points ahead of the week's pace
- build × CLI: F: plugin/lib/fmreplay.py — fm replay scores the guard on real past commands
- operate × CLI: F: plugin/lib/fmcost.py — fm cost and fm burden account tokens per task, session and version

## 13. Genesis as a feature
- find × Claude Code: F: plugin/lib/fmscout.py — the idle scout offers "Start Genesis here?" once, when the queue is drained, 10+ briefs are done and no gen-0 exists
- find × site: F: site/genesis/gap-map.md — the gap map is published on the Genesis page
- find × CLI: F: plugin/lib/fmgenesis.py — fm genesis check enforces the tower's gap-map shape
- understand × CLI: F: plugin/lib/fmgenesis.py — fm genesis draft writes a whole gen-0 from one line or none, carrying open briefs' MUST/NEVER lines over and marking any not from the user unconfirmed
- plan × Claude Code: F: plugin/skills/genesis/SKILL.md — /foreman:genesis runs every stage in order, spec and seed through the Missions, critiques, select, drift and the sweep to the next seed, each named by fm genesis step
- plan × site: F: site/genesis/gen-1/seed.md — generation 1's seed is published
- plan × CLI: F: plugin/lib/fmgenesis.py — fm genesis put stores a self-written seed for the next generation
- verify × site: F: site/genesis/genesis.js — each generation's drift and sweep verdicts on the Genesis page
- ship × site: F: plugin/lib/fmgenesis.py — fm genesis export writes the live tower page
- operate × CLI: F: plugin/lib/fmgenesis.py — fm genesis live on republishes after each tower change
- learn × site: F: site/genesis/gen-0.md — the previous generation is published beside the next

## Onboarding
- understand × CLI: F: plugin/lib/fmdemo.py — fm demo fixes a seeded bug in a throwaway repo with no model calls
- plan × CLI: F: plugin/lib/fmsetup.py — fm setup configures a project
- build × CLI: F: install.sh — one-line install, with --desktop for the app
- verify × Claude Code: F: plugin/skills/doctor/SKILL.md — the doctor skill checks the install
- operate × CLI: F: plugin/lib/fmaway.py — fm away summarises on return after a long gap

## UX
- understand × Claude Code: F: plugin/hooks/statusline — statusline shows task, progress and cost
- understand × fm code: F: plugin/lib/fmcodetui.py — fm code tui draws the run from its event stream
- understand × Desktop: F: plugin/lib/fmwatch.py — fm projects feeds Foreman Desktop's project list
- understand × site: F: site/style.css — the site's shared palette and type
- understand × CLI: F: plugin/lib/fmwatch.py — fm watch and fm ui show live task state
- plan × CLI: F: plugin/lib/fmsettings.py — one schema for every setting the TUI and mod read
- build × Claude Code: F: plugin/output-styles/foreman.md — the Foreman output style keeps replies short
- build × fm code: F: plugin/lib/fmcodeterm.py — an ANSI terminal without curses, changed cells only
- build × CLI: F: plugin/lib/fmdesign.py — fm design sprint checks brief, look and tokens in order

## Docs
- understand × Claude Code: F: MASTER.md — the system map lists every module
- understand × site: F: site/pages.py — builds site pages from Foreman's own code, such as fm code tui's key poster from its key map (T-2061)
- plan × CLI: F: plugin/lib/fmplaybooks.py — the playbook library's lint: index, budget, duplicates
- build × Claude Code: F: plugin/skills/playbooks/SKILL.md — stage playbooks for refactor, ADR, TDD and the like
- learn × CLI: F: plugin/lib/fmplaybooks.py — fm playbooks draft turns a done task into a playbook

## Ecosystem
- understand × other agents: F: plugin/lib/fmagents.py — fm agents list prints what each harness enforces
- understand × MCP: F: plugin/lib/fmmcp.py — fm mcp serves Foreman read-only over stdio
- understand × Desktop: F: plugin/lib/fmclaude.py — the desktop app's session view reads `fm claude --json`, locally or over ssh: each session on the device with its conversation, subagents and scratchpad
- plan × Claude Code: F: plugin/lib/fmlib.py — stack cards for languages and frameworks
- build × Claude Code: F: mods/foreman-ui — the foreman-ui mod for Claude Code
- build × other agents: F: plugin/lib/fmagents.py — fm agents install wires Codex, Gemini and opencode
- verify × CLI: F: plugin/lib/fmci.py — fm ci-watch polls GitHub Actions after a push
- operate × CLI: F: plugin/lib/fmintegrations.py — fm timeline exports Perfetto and OTLP JSON

## Multi-user
- understand × CLI: F: plugin/lib/fmsync.py — fm sync keeps tasks and fixes with the repo so clones and teammates see them
- build × Claude Code: F: plugin/lib/fmbus.py — hooks deliver bus mail between sessions on a machine
- operate × CLI: F: plugin/lib/fmeco.py — fm machine and version skew checks across machines

## Observability
- understand × MCP: F: plugin/lib/fmmcp.py — logs, trace and fail tools read run data
- understand × CLI: F: plugin/lib/fminstr.py — zero-token instruments: sym, fail, logs, data, trace

## Security
- understand × MCP: F: plugin/lib/fmmcp.py — read-only tools, argument caps and a sensitive-repo off switch
- plan × CLI: F: plugin/lib/fmdeps.py — typosquat, registry and age look on a new package
- build × Claude Code: F: plugin/lib/fmguard.py — the guard blocks destructive categories in Claude Code, and test_guard_decision_matches_across_harnesses checks the same decision through fmagents' dispatcher
- verify × CLI: F: plugin/lib/fmoracle.py — the guard's oracle runs a line in a bwrap sandbox
- ship × CLI: F: plugin/lib/fmsecrets.py — secret scan before commit; credential audit

## Performance
- understand × CLI: F: plugin/lib/fmgraph.py — fm graph pack ranks a task's read-set
- build × Claude Code: F: plugin/lib/fmambient.py — affected-only tests keep the loop fast

## Portability
- build × fm code: F: plugin/lib/fmmodels.py — fm code runs on any OpenAI-compatible or Anthropic profile
- build × other agents: F: plugin/lib/fmagents.py — one hook dispatcher maps each harness's tool events onto Foreman's hooks
- build × CLI: F: plugin/lib/fmpy.py — re-exec under a supported interpreter

## Model layer
- find × Claude Code: I: a decision call ranks fm find's leads by how likely each is a real bug before the session proves any (plugin/lib/fmfind.py)
- find × fm code: I: fm code's planner asks a local model which hotspots to read first, shadow-logged beside its current order (plugin/lib/fmcode.py)
- find × other agents: I: AGENTS.md tells other harnesses to call fm find --rank, whose order comes from the decision interface once its exam beats the plain sort (plugin/lib/fmagents.py)
- find × MCP: I: the MCP find tool returns each lead's model score and calibrated confidence beside the deterministic rank (plugin/lib/fmmcp.py)
- find × Desktop: N/A: the desktop list shows projects and their next action, not leads; lead triage happens in sessions
- find × site: I: the leads page shows model-scored against rule-ranked precision from the exam, so a reader sees whether the model earns its place (site/pages.py)
- find × CLI: I: fm find --rank scores leads with selfjev-4b behind the Jev-compatible API when TYPESAFE_BASE_URL is set, and with rules alone otherwise (plugin/lib/fmmodels.py)
- find × headless/server: I: the hourly tick dedupes open leads by embedding similarity, so one defect found twice files once (plugin/lib/fmnight.py)
- understand × Claude Code: I: recall answers a session's question by embedding search over lessons and briefs, kept only if its hit rate beats keyword overlap (plugin/lib/fmrecall.py)
- understand × fm code: I: the worker gets a reranked file list from a local reranker and spends its context on the top files (plugin/lib/fmcode.py)
- understand × other agents: N/A: other harnesses read the repo themselves; Foreman's recall reaches them through MCP, counted on that row
- understand × MCP: I: an MCP recall tool backed by the embedding index names the backend in each answer, so a client sees which model spoke (plugin/lib/fmmcp.py)
- understand × Desktop: N/A: no code is read in the desktop app; it lists projects and starts sessions
- understand × site: I: a Model layer page explains each backend, what it decides, its accuracy against the path it replaced and its cost (site/pages.py)
- understand × CLI: I: fm which matches a need to shelves by embedding similarity, falling back to word overlap when no backend answers (plugin/lib/fmwhich.py)
- understand × headless/server: I: fm serve offers the decision interface to a remote session and refuses sensitive projects at that boundary (plugin/lib/fmserve.py)
- plan × Claude Code: I: intake asks the decision interface for type and tier with a probability; a low-confidence answer routes to research as fm next does today (plugin/lib/fmcli.py)
- plan × fm code: I: Von routes short requests by intent to the planner slot, the cloud model takes the rest, and each choice is logged (plugin/lib/fmcode.py)
- plan × other agents: I: the AGENTS.md block gives the tier suggestion as advice an agent may override, never as a gate (plugin/lib/fmagents.py)
- plan × MCP: I: an MCP intake tool returns the suggested type, tier and confidence, so a client plans with the numbers a session sees (plugin/lib/fmmcp.py)
- plan × Desktop: N/A: plans are made in sessions; the desktop app shows the next action a plan produced
- plan × site: I: the judgment page plots stated against scored confidence for model-made tier guesses beside the session's own bets (site/pages.py)
- plan × CLI: I: fm second rival asks a local model for the cold reading first and spends a cloud read only when the local one is unsure (plugin/lib/fmsecond.py)
- plan × headless/server: I: fm run picks each task's model by the router's cheapest-that-holds rule, extended to the local backends in the registry (plugin/lib/fmlanes.py)
- build × Claude Code: F: plugin/lib/fmmodels.py resolves a configured local or cloud profile: the base each backend in the cascade registers on
- build × fm code: F: plugin/lib/fmcode.py runs Foreman's loop on any fmmodels profile, so a local code model behind vLLM or llama-swap can already work
- build × other agents: I: one registry entry per backend with cost, latency and a sensitive_ok flag, so no caller hardcodes a model (plugin/lib/fmmodels.py)
- build × MCP: I: an MCP decide tool takes a kind and an input and returns choice, score and probability from the cheapest backend that clears the bar (plugin/lib/fmmcp.py)
- build × Desktop: N/A: nothing is built from the desktop app; it starts the sessions that build
- build × site: I: the site build reads the registry and the exam lines to chart each backend's accuracy, cost and latency (site/pages.py)
- build × CLI: I: fm models lists the registry, probes each backend once and queues missing ones as install requests, never downloading (plugin/lib/fmgrants.py)
- build × headless/server: I: Jevlike trains a task-specific classifier from Foreman's closed tasks on the night run, staged as a candidate until its exam arm wins (plugin/lib/fmnight.py)
- verify × Claude Code: I: a test fails if the guard or an evidence gate imports the model layer: models advise, proof decides (plugin/lib/fmguard.py)
- verify × fm code: I: a vision model reads fm shot's screenshot as a second signal on a UI done claim, never in place of the run (plugin/lib/fmshot.py)
- verify × other agents: N/A: other harnesses' claims face the same fm gates, and by the rule that proof decides no model is added there
- verify × MCP: I: each MCP decide answer goes into the prediction book with its probability, so its calibration is scored against what happened (plugin/lib/fmforesight.py)
- verify × Desktop: N/A: verification runs in the session and fm check; the desktop app only shows the result
- verify × site: I: the exam page adds a model-against-path column per use; a use stays only while its column beats the path it replaced (site/pages.py)
- verify × CLI: I: fm exam gains one model arm per use (intake tier, lead triage, dedupe) run on held-out scenarios against the path it would replace (plugin/lib/fmexam.py)
- verify × headless/server: I: the night run replays the week's decisions through each candidate backend in shadow mode and scores them before any switch (plugin/lib/fmnight.py)
- ship × Claude Code: I: a use moves from shadow to live only by an fm decide row citing its exam numbers, so the final report lists every switch (plugin/lib/fmoutcomes.py)
- ship × fm code: N/A: fm code ships through fm ship like a session does; the model layer changes no step of it
- ship × other agents: N/A: another harness ships through fm ship, and nothing a model makes touches the publish grant
- ship × MCP: N/A: the MCP server ships with the plugin; no model decides a release or a push
- ship × Desktop: N/A: the desktop app never ships code; releases go through fm release in a session
- ship × site: I: CHANGELOG and the site name each model use when it goes live, with the accuracy and cost it beat (site/pages.py)
- ship × CLI: I: fm release refuses a build whose registry names a backend the user never approved through the install queue (plugin/lib/fmgrants.py)
- ship × headless/server: N/A: headless runs never publish; fm ship needs a per-task grant the night run doesn't take
- operate × Claude Code: I: a sensitive repo's sessions resolve only local backends, and a cloud call from one is refused with its reason (plugin/lib/fmmodels.py)
- operate × fm code: I: the worker falls back to the cloud model when the local server is down and logs the outage to the trigger table (plugin/lib/fmtriggers.py)
- operate × other agents: I: decision calls are metered against fm budget, so an outside harness can't spend Foreman's cap through MCP (plugin/lib/fmbudget.py)
- operate × MCP: I: the MCP server reports each backend's health and last latency, so a client sees which model will answer (plugin/lib/fmmcp.py)
- operate × Desktop: I: the desktop list shows each project's active backend, local or cloud, beside its next action (plugin/lib/fmwatch.py)
- operate × site: N/A: the site is static; it shows measured results, not live backend state
- operate × CLI: I: fm doctor checks every registered backend answers within its latency budget and fails loud on a silent fallback (plugin/lib/fmdoctor.py)
- operate × headless/server: I: the hourly tick probes the user's vLLM and llama-swap servers and marks a backend down before a run leans on it (plugin/lib/fmnight.py)
- learn × Claude Code: I: each closed task's decisions (tier, lead, dedupe) become labelled rows Jevlike trains on, so the local model learns this repo (plugin/lib/fmoutcomes.py)
- learn × fm code: I: fm code records which backend held on which task kind, feeding the router's cheapest-that-holds table (plugin/lib/fmcode.py)
- learn × other agents: N/A: other harnesses' sessions aren't Foreman's to learn from; only work closed through fm counts
- learn × MCP: I: decide answers the session overrode are kept as disagreement rows, the signal the next candidate model is scored on (plugin/lib/fmmcp.py)
- learn × Desktop: N/A: the desktop app records nothing a model could learn from
- learn × site: I: the site shows each backend's calibration curve over time, so drift in a local model shows before it is trusted more (site/pages.py)
- learn × CLI: I: fm outcomes --judgment scores model-made probabilities beside the session's own bets in one Brier ledger (plugin/lib/fmoutcomes.py)
- learn × headless/server: I: the night run retrains Jevlike's candidates from the week's labelled rows and stages the winner for its exam, never swapping it live (plugin/lib/fmnight.py)
