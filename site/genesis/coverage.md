# Coverage — gen 1

Status, as `fm genesis check` counts this file (each `- stage × surface:` line is one cell): 161 of the 1408 cells hold a concrete cell; the other 1247 are open (T-2159 emptied the templated ones and T-2166's cold read emptied cells that repeated another row's feature), listed by `fm genesis check`. Open is not done: no row here counts as covered until its cells are filled.

## 1. Initiative
- find × fm code: I: run the scout finders on fm code's idle turn (plugin/lib/fmcode.py)
- find × other agents: I: run idle scouts from the Codex Stop event and capture findings (plugin/lib/fmagents.py)
- find × MCP: I: let an MCP client read what the scouts found (plugin/lib/fmmcp.py)
- find × Desktop: I: list scout findings in the Desktop inbox for one-click accept (plugin/lib/fmwatch.py)
- find × CLI: F: plugin/lib/fmfind.py — `fm find` runs deterministic, language-agnostic finders over a repo with no request
- find × headless/server: F: plugin/lib/fmnight.py — fm night spends a --max-usd budget while the user is away on the sentinel, a landscape scan and one research-debt question, and the morning digest says what it found
- plan × Claude Code: F: plugin/skills/brainstorm/SKILL.md — grounded, scored ideas turned into queued tasks
- build × CLI: F: plugin/lib/fmdraft.py — a headless claude drafts the top queued S task in a throwaway worktree
- operate × CLI: F: plugin/lib/fmorders.py — standing orders capture a task on a schedule or when a file changes

## 2. Exhaustive thinking
- find × CLI: F: plugin/lib/fmideas.py — lens children read the code and return ideas marked new, partial or built
- understand × CLI: F: plugin/lib/fmmission.py — mission lenses and surfaces enumerate every reading of an open request
- plan × CLI: F: plugin/lib/fmsecond.py — cold second opinion, debate and dissent kept open in the brief
- verify × Claude Code: F: plugin/agents/fm-reviewer.md — one read-only reviewer per audit lens (intent, adversary, edge, operator, maintainer)
- verify × CLI: F: plugin/lib/fmauditrun.py — fm audit run runs the audit lenses as headless read-only reviewers
- learn × CLI: F: plugin/lib/fmtaste.py — lens keep rates feed which lenses get more weight next brainstorm

## 3. Anticipation
- find × Claude Code: F: plugin/lib/fmforesight.py — session-start sweep notes a changed model, window or Claude Code version before it bites
- understand × MCP: F: plugin/lib/fmmcp.py — the impact and why tools answer blast radius and history read-only
- understand × CLI: F: plugin/lib/fmgraph.py — fm graph blast shows a change's blast radius from one local graph
- plan × Claude Code: I: inject a pre-mortem of likely failures from fm recall into each new brief (plugin/lib/fmhooks.py)
- plan × fm code: I: have fm code list foreseeable failures from failure memory before its PLAN slot (plugin/lib/fmcode.py)
- verify × CLI: F: plugin/lib/fmreverify.py — fm sentinel re-queues old passing criteria when a later commit touches their files
- operate × CLI: F: plugin/lib/fmrisk.py — the daily risk budget steps autonomy down after destructive blocks and reverts
- learn × CLI: F: plugin/lib/fmrecall.py — fm recall and fm dream keep failure memory so a repeat is foreseen

## 4. Goal to finish
- understand × MCP: F: plugin/lib/fmmcp.py — state and next tools show the one next required action
- plan × CLI: F: plugin/lib/fmcore.py — briefs with acceptance criteria and steps, each tied to a verify command
- build × Claude Code: F: plugin/lib/fmhooks.py — the Stop hook drives on while open work remains and refuses a premature done
- build × fm code: F: plugin/lib/fmcode.py — fm code runs Foreman's loop on the open task to the end of its plan
- build × other agents: F: plugin/lib/fmagents.py — Codex gets the Stop drive and done-gate; Gemini and opencode have no Stop
- build × Desktop: I: show open criteria and the next required action for every project in Desktop (plugin/lib/fmwatch.py)
- verify × CLI: F: plugin/lib/fmcore.py — fm task finish closes only on fresh evidence for every criterion

## 5. Getting the tools it lacks
- find × fm code: F: plugin/lib/fmcode.py — fm code offers one matching indexed skill at a run's start
- find × CLI: F: plugin/lib/fmplugins.py — fm plugins find searches for a plugin that covers a missing need
- understand × Claude Code: F: plugin/skills/library/SKILL.md — stack cards with verify commands before coding in a framework
- understand × MCP: F: plugin/lib/fmmcp.py — lib_suggest, lib_search and lib_show serve stack cards read-only
- plan × CLI: F: plugin/lib/fmwhich.py — fm which names the skill, playbook or command that fits a task
- build × fm code: I: let fm code build a missing stdlib-only tool as a local task in a lane and register it, nothing fetched from outside (plugin/lib/fmcode.py)
- build × CLI: F: plugin/lib/fmplugins.py — fm plugins install adds a pinned plugin only after the user's yes to fm ask ID plugin
- verify × CLI: F: plugin/lib/fmdeps.py — fm deps checks installed versions and import sites locally
- learn × CLI: F: plugin/lib/fmrepeats.py — fm repeats drafts a playbook from repeated manual step sequences

## 6. Verifying anything
- understand × CLI: F: plugin/lib/fmdebug.py — fm whyred ranks suspects and minimal failing hunks for a red run
- verify × fm code: F: plugin/lib/fmcode.py — fm code's steps close through the same evidence runs
- verify × MCP: F: plugin/lib/fmmcp.py — the checks tool returns the project's last fm check gate run, each command with its exit and time
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
- verify × CLI: F: plugin/lib/fmbench.py — fm bench replays finished tasks and gates a candidate plugin
- ship × CLI: F: plugin/lib/fmrollback.py — a snapshot before each new version and fm rollback to restore it
- operate × CLI: F: plugin/lib/fmtidy.py — fm tidy repairs drift and dead state
- learn × CLI: F: plugin/lib/fmtrials.py — a self-change is a pre-registered trial graded on ledger event rates

## 8. Calibrated judgment
- understand × CLI: F: plugin/lib/fmexam.py — the generated exam grades agents on held-out tasks
- plan × MCP: I: an MCP tool that returns past finish rates for a task's type and tier, so any agent can size its estimate (plugin/lib/fmmcp.py)
- verify × site: F: site/pages.py — bench pages publish pass rates and where Foreman loses
- verify × CLI: F: plugin/lib/fmoutcomes.py — stated confidence scored per bucket with a Brier score, shown at focus
- learn × Claude Code: F: plugin/lib/fmhooks.py — the track record by type and tier is injected at focus

## 9. Orchestration
- find × Claude Code: F: plugin/agents/fm-debugger.md — fresh-eyes debugger returns ranked hypotheses with a probe each
- understand × Claude Code: F: plugin/agents/fm-recon.md — read-only recon subagent with a bounded, cited summary
- plan × CLI: F: plugin/lib/fmsplit.py — fm task split partitions a task's files into child tasks
- build × Claude Code: F: plugin/agents/fm-builder.md — one S/M task built test-first in a worktree on its own branch
- build × fm code: I: let fm code fan a task out to fm lane worktrees and merge the children (plugin/lib/fmcode.py)
- build × other agents: F: plugin/lib/fmsession.py — fm session runs detached claude, codex, gemini and opencode sessions
- build × CLI: F: plugin/lib/fmlanes.py — fm lane runs git worktrees as lanes with their own active task
- verify × CLI: F: plugin/lib/fmstack.py — stacked commits each checked alone in a scratch worktree
- ship × CLI: F: plugin/lib/fmpr.py — fm pr train merges approved green PRs in order
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
- build × CLI: F: plugin/lib/fmloop.py — fm loop on starts an improvement round when the queue empties
- build × headless/server: F: plugin/lib/fmserve.py — fm run works the queue in fresh headless sessions, one task each
- verify × Claude Code: F: plugin/lib/fmambient.py — tests run detached after each edit with no prompt
- learn × CLI: F: plugin/lib/fmfriction.py — fm friction --every N triggers a self-improvement digest

## 12. Staying lean and safe
- plan × CLI: F: plugin/lib/fmbudget.py — subagents wait at 90% of the 5-hour window, or when weekly usage past 75% runs 10+ points ahead of the week's pace
- build × CLI: F: plugin/lib/fmreplay.py — fm replay scores the guard on real past commands
- verify × Claude Code: F: plugin/tests/bench_hooks.py — times each Claude Code hook over its fixture payloads and exits 1 when a p95 runs past its budget, so a hook that slows every turn fails before it ships
- verify × CLI: F: plugin/lib/fmmutate.py — guard mutation tests prove each rule bites
- operate × CLI: F: plugin/lib/fmcost.py — fm cost and fm burden account tokens per task, session and version
- learn × CLI: F: plugin/lib/fmbacktest.py — fm backtest shows where a changed rule would have fired

## 13. Genesis as a feature
- find × Claude Code: F: plugin/lib/fmscout.py — the idle scout offers "Start Genesis here?" once, when the queue is drained, 10+ briefs are done and no gen-0 exists
- find × site: F: site/genesis/gap-map.md — the gap map is published on the Genesis page
- find × CLI: F: plugin/lib/fmgenesis.py — fm genesis check enforces the tower's gap-map shape
- understand × Claude Code: F: plugin/skills/genesis/SKILL.md (the /foreman:genesis skill) — See it: fm genesis status prints the tower
- understand × CLI: F: plugin/lib/fmgenesis.py — fm genesis draft writes a whole gen-0 from one line or none, carrying open briefs' MUST/NEVER lines over and marking any not from the user unconfirmed
- plan × Claude Code: F: plugin/skills/genesis/SKILL.md (the /foreman:genesis skill) — draft, init, spec and the seed stage, driven by fm genesis step
- plan × site: F: site/genesis/gen-1/seed.md — generation 1's seed is published
- plan × CLI: F: plugin/lib/fmgenesis.py — fm genesis put stores a self-written seed for the next generation
- build × Claude Code: F: plugin/skills/genesis/SKILL.md (the /foreman:genesis skill) — the mission, intake and build stages, each brief closed with fm task finish
- build × CLI: F: plugin/lib/fmexam.py — fm exam gen renders throwaway projects in six languages with planted defects and the keys kept outside each; `--author child` has a tool-less model write the planted defects of the kinds it can author
- verify × Claude Code: F: plugin/skills/genesis/SKILL.md (the /foreman:genesis skill) — drift, sweep and fm genesis exam on the held-out third
- verify × site: F: site/genesis/genesis.js — each generation's drift and sweep verdicts on the Genesis page
- verify × CLI: F: plugin/lib/fmgenesis.py — fm genesis drift (seal + cold read), sweep (§7 + privilege diff) and exam score each generation (T-2104, T-2112, T-2113)
- ship × Claude Code: F: plugin/skills/genesis/SKILL.md (the /foreman:genesis skill) — the next seed waits on a clean sweep
- ship × site: F: plugin/lib/fmgenesis.py — fm genesis export writes the live tower page
- operate × CLI: F: plugin/lib/fmgenesis.py — fm genesis live on republishes after each tower change
- learn × Claude Code: F: plugin/skills/genesis/SKILL.md (the /foreman:genesis skill) — select writes lineage.md; a stopped tower reads lineage and critiques before the next seed
- learn × site: F: site/genesis/gen-0.md — the previous generation is published beside the next

## Onboarding
- understand × site: F: site/index.html — the home page explains the loop
- understand × CLI: F: plugin/lib/fmdemo.py — fm demo fixes a seeded bug in a throwaway repo with no model calls
- plan × CLI: F: plugin/lib/fmsetup.py — fm setup configures a project
- build × CLI: F: install.sh — one-line install, with --desktop for the app
- verify × Claude Code: F: plugin/skills/doctor/SKILL.md — the doctor skill checks the install
- operate × CLI: F: plugin/lib/fmaway.py — fm away summarises on return after a long gap
- learn × CLI: F: plugin/lib/fmdojo.py — fm dojo drills the guard's rules

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
- operate × headless/server: F: plugin/lib/fmsettingsserve.py — the control room serves settings as a page

## Docs
- understand × Claude Code: F: MASTER.md — the system map lists every module
- understand × site: F: site/pages.py — site pages are generated from the real data
- plan × CLI: F: plugin/lib/fmplaybooks.py — the playbook library's lint: index, budget, duplicates
- build × Claude Code: F: plugin/skills/playbooks/SKILL.md — stage playbooks for refactor, ADR, TDD and the like
- learn × CLI: F: plugin/lib/fmplaybooks.py — fm playbooks draft turns a done task into a playbook

## Ecosystem
- understand × other agents: F: plugin/lib/fmagents.py — fm agents list prints what each harness enforces
- understand × MCP: F: plugin/lib/fmmcp.py — fm mcp serves Foreman read-only over stdio
- understand × Desktop: F: plugin/lib/fmclaude.py — fm claude lists every Claude Code session for the desktop app
- plan × Claude Code: F: plugin/lib/fmlib.py — stack cards for languages and frameworks
- build × Claude Code: F: mods/foreman-ui — the foreman-ui mod for Claude Code
- build × other agents: F: plugin/lib/fmagents.py — fm agents install wires Codex, Gemini and opencode
- verify × CLI: F: plugin/lib/fmci.py — fm ci-watch polls GitHub Actions after a push
- operate × CLI: F: plugin/lib/fmintegrations.py — fm timeline exports Perfetto and OTLP JSON

## Multi-user
- find × Desktop: I: show teammates' open tasks from synced repos in Desktop (plugin/lib/fmwatch.py)
- find × CLI: F: plugin/lib/fmeco.py — fm inbox gh reads a repo's open issues as work
- understand × CLI: F: plugin/lib/fmsync.py — fm sync keeps tasks and fixes with the repo so clones and teammates see them
- plan × CLI: I: add per-user attribution and an approval handoff to the brief so a teammate can pick up a task (plugin/lib/fmcli.py)
- build × Claude Code: F: plugin/lib/fmbus.py — hooks deliver bus mail between sessions on a machine
- operate × CLI: F: plugin/lib/fmeco.py — fm machine and version skew checks across machines
- operate × headless/server: F: plugin/lib/fmserve.py — fm serve runs Remote Control for a repo on a server
- learn × CLI: I: share the taste and fixes ledgers between teammates through fm sync (plugin/lib/fmcli.py)

## Observability
- understand × MCP: F: plugin/lib/fmmcp.py — logs, trace and fail tools read run data
- understand × CLI: F: plugin/lib/fminstr.py — zero-token instruments: sym, fail, logs, data, trace
- operate × headless/server: F: plugin/lib/fmserve.py — fm run keeps a rotating run log

## Security
- understand × MCP: F: plugin/lib/fmmcp.py — read-only tools, argument caps and a sensitive-repo off switch
- plan × CLI: F: plugin/lib/fmdeps.py — typosquat, registry and age look on a new package
- build × Claude Code: F: plugin/lib/fmguard.py — guard blocks destructive categories on every harness
- verify × fm code: I: run the guard mutation tests against fm code's own tool path (plugin/lib/fmcode.py)
- verify × CLI: F: plugin/lib/fmoracle.py — the guard's oracle runs a line in a bwrap sandbox
- ship × CLI: F: plugin/lib/fmsecrets.py — secret scan before commit; credential audit

## Performance
- understand × CLI: F: plugin/lib/fmgraph.py — fm graph pack ranks a task's read-set
- build × Claude Code: F: plugin/lib/fmambient.py — affected-only tests keep the loop fast
- learn × CLI: F: plugin/lib/fmcodebench.py — fm code bench grades a model on seeded tasks

## Portability
- build × fm code: F: plugin/lib/fmmodels.py — fm code runs on any OpenAI-compatible or Anthropic profile
- build × other agents: F: plugin/lib/fmagents.py — one hook dispatcher for Codex, Gemini and opencode
- build × Desktop: I: ship a Windows build of Foreman Desktop and a Windows path for fm and the hooks (plugin/lib/fmwatch.py)
- build × CLI: F: plugin/lib/fmpy.py — re-exec under a supported interpreter
