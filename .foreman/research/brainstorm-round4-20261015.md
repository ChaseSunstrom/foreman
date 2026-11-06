# Brainstorm round 4 — 2026-10-15: make Foreman THE plugin (T-0843)

437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run) from new evidence: a clean-HOME newcomer install, a survey of rival Claude Code plugins, usage data and an over-engineering audit; 31 capability clusters, each grounded in the code. Every idea is listed under its cluster.

## [build] install-plan-consent — Install as a plan: itemised preview, receipt, questions, rehearsal, install by conversation
value 4 · effort S · risk low · a silent bypassPermissions default is a new user's biggest trust hit
Exists: fm install-user --dry-run (fmcli.py:4382); install.sh --no-bypass/--no-plugins (install.sh:10-11) but bypass is on by default with one line of notice (install.sh:131,139)
Premise: false in part: opt-outs exist; what's missing is asking before the biggest trust change
First slice: install.sh shows the wiring plan and asks y/N before bypass on a tty; --bypass opts in without asking; no tty keeps the current mode
Ideas (16):
- Show the full `~/.claude` diff at install and let the user decline each change — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Print an install receipt with per-item opt-out — near T-0003 (done): Phase 5: integration — install-user wiring, plugin decision… (Round 1)
- Show an itemised install plan before touching `~/.claude` — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Ask three install questions, with a `--plan` preview — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- Run the installer as a Foreman task that prints a receipt — near T-0678 (done): Milestone: Features — Releases and delivery (Round 1)
- Make the installer ask before it changes your setup — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Wild: Print an install "nutrition label" (Round 1)
- Generate a one-screen "what Foreman can see and send" statement — near T-0711 (done): Frontier 11 — Cockpit UI (Round 1)
- Make the install a receipt-first plan, with bypass off by default — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 3)
- Show the effect of each install change before applying it — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Make safe-by-default install: plan, show diff, bypass opt-in — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Make the installer's trust grants individually declinable and auto-expiring (wild) (Round 3)
- Install as a transaction: `fm install --plan`, then apply with a journal — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: trust)
- List the exact changes before applying them (`install.sh --plan`) — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: install)
- Wild: Rehearse an install in a throwaway HOME before touching the real one — near T-0691 (done): Milestone: Intelligence — Planning and decomposition (1) (Deepened: install)
- Wild: Install by conversation, so the first session asks three questions — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: install)

## [build] agent-install — Agent-executable INSTALL.md, tamper-proof download, pinned installer
value 4 · effort S · risk low · agent-led install is how many users try plugins now; the guide carries the consent steps
Exists: curl|bash from main (install.sh:3, README:12); no INSTALL.md
Premise: ok: 'tell Claude to install Foreman' has no guide
First slice: INSTALL.md: read install.sh, explain the defaults, ask consent, run it, run fm doctor; linked from README
Ideas (7):
- Pin and verify everything the installer downloads or self-updates — near T-0672 (done): Milestone: Features — Guard and safety (Round 1)
- Ship SBOM, build provenance and a vulnerability-report path (Round 1)
- Write an agent-readable install guide so the user can say "install Foreman" to Claude — near T-0729 (done): Friction: lane rm unlocks a finished builder's worktree; no… (Round 2)
- Make the install an agent-executable `INSTALL.md` — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Wild: Install by saying "install Foreman" to Claude through an agent-readable INSTALL.md — near T-0675 (done): Milestone: Features — Orchestration, lanes and fleets (Round 3)
- Wrap `install.sh` so a truncated download can't run, and pin the entry URL to a tag (Round 4)
- Wild: Install by telling Claude "install Foreman", via an agent-readable INSTALL.md that asks consent per step — near T-0009 (done): Autonomy: plain-chat approvals, Claude runs everything, mul… (Deepened: onboarding)

## [build] marketplace-install — Marketplace distribution: zero-wiring /plugin install, package channels, split micro-plugins
value 4 · effort M · risk med · the way every popular rival installs; verify it in a clean HOME, document it, and have the first session say how to finish wiring
Exists: marketplace.json lists foreman and foreman-ui (.claude-plugin/marketplace.json:10-22); README documents only the curl installer
Premise: unclear: whether a bare /plugin marketplace add + install gives a working Foreman without install-user is untested
First slice: clean-HOME test of claude plugin marketplace add <repo> + plugin install; README section; SessionStart note when not wired
Ideas (23):
- Ship a native plugin-marketplace install with zero config rewrite — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 1)
- Ship a zero-wiring marketplace install and make every `~/.claude` change a step of `fm wire` — near T-0004 (done): Phase 6: fm tidy and fm doctor (Round 1)
- Split the install into core and labs plugins — near T-0766 (done): Guard: a data heredoc that writes a Foreman source file isn… (Round 1)
- Add a one-file "Foreman Seed" for marketplace install — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- Wild: ship a `foreman` launcher that applies the discipline settings via `--settings`, so `~/.claude` stays untouched (Round 1)
- Ship Foreman as a marketplace plugin with a zero-wiring default — near T-0004 (done): Phase 6: fm tidy and fm doctor (Round 1)
- Ship the guard, resume and done-gate as standalone plugins — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 2)
- Wild: paste a zero-install "Foreman Lite" snippet (Round 2)
- Wild: Split Foreman into marketplace micro-plugins (guard, resume, evidence) (Round 2)
- Unbundle the three signature behaviours into single-job entry plugins (Round 2)
- Ship a three-rung install ladder with state-preserving upgrades (Round 2)
- Add `fm doctor --publish`, a marketplace-readiness lint — near T-0004 (done): Phase 6: fm tidy and fm doctor (Round 3)
- Move the installer's third-party plugins and bypass default out of the core install — near T-0009 (done): Autonomy: plain-chat approvals, Claude runs everything, mul… (Round 3)
- Ship a Foreman Seed marketplace plugin that wires nothing — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 3)
- Publish Foreman to uvx, pipx and Homebrew (Round 3)
- Install into a second CLAUDE_CONFIG_DIR profile — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 4)
- Ship one `fm.pyz` release asset that every channel consumes — near T-0678 (done): Milestone: Features — Releases and delivery (Round 4)
- Ship Foreman Core 2.0 as a zero-wiring marketplace plugin with a ten-verb front door (Round 4)
- Wire per project by default, not into `~/.claude` — near T-0003 (done): Phase 5: integration — install-user wiring, plugin decision… (Round 4)
- Install as a plain marketplace plugin first, with "full Foreman" as an opt-in upgrade — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Deepened: onboarding)
- Ship a marketplace-installable "Foreman Lite" that adds commands and hooks without rewriting `~/.claude` — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Deepened: trust)
- Publish a marketplace plugin with zero wiring and an `fm wire` ladder (Deepened: install)
- Wild: Add a `foreman` launcher that applies discipline through `--settings` (Deepened: install)

## [build] demo-replay — fm demo: no-model recorded replay, playground, seeded-bug fixture kit
value 4 · effort M · risk low · twelve ideas converge on one no-model demo verb
Exists: nothing; fm tour means changed files in reading order (fmmap.py:305)
Premise: ok: no way to see Foreman work without spending model tokens
First slice: fm demo: a temp repo with a seeded bug, real fm task new / guard block / evidence / finish, no claude -p
Ideas (12):
- Wild: Turn the README into a self-running demo (`fm demo` plays a recorded session) (Round 1)
- Generate the README's first screen from a real recorded run — near T-0682 (done): Milestone: Features — Verification and product checking (Round 1)
- Add `fm demo`: a no-model replay of a seeded-bug fix — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 1)
- Add `fm demo`, a 60-second no-model walkthrough — near T-0776 (done): Foreman's claude -p children carry a hard --max-budget-usd (Round 1)
- Wild: Add a browser playground (Pyodide) that runs the real classifier and guard (Round 1)
- Wild: add `fm tour`, a scripted no-model walkthrough that also serves as demo and smoke test (Round 1)
- Ship `fm demo`, a 60-second scripted run with no model calls — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 1)
- Wild: `fm demo guard`, a 60-second safety demo with no model calls (Round 1)
- Wild: `fm demo` replays a recorded seeded-bug fix as a narrated terminal show (Round 3)
- Build one seeded-bug fixture kit for every showcase surface — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: Make the README a self-verifying transcript — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 3)
- Run a no-model hostile-repo drill at first install (wild) — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 3)

## [build] errors-teach — Every refusal, error and empty state names the next step; stable codes, docs, plain glossary
value 3 · effort S · risk low · cheap, visible cleanup
Exists: refusals lead with the fix (T-0440, T-0854); fm explain/why explain decisions; help strings still carry (T-NNNN) ids (fmcli.py:3799,3943,3965)
Premise: ok: ticket ids in help read as noise to a newcomer
First slice: strip (T-NNNN) from fm help strings and add a test that fails if any help string carries one
Ideas (18):
- Install a generated man page — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Strip internal ticket numbers from user-facing help and output — near T-0682 (done): Milestone: Features — Verification and product checking (Round 1)
- Gloss every unexplained field in `fm status` once — near T-0681 (done): Milestone: Features — UI and motion (Round 1)
- Replace jargon with a 10-word plain glossary surfaced in context — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Give every refusal a stable code and an `fm explain CODE` long form (Round 2)
- Print a personal cheat card — near T-0228 (done): foreman-ui catch-up: budget, bench and evolve, research ask… (Round 2)
- Generate a versioned offline docs site from the verb registry — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 2)
- Add `fm nope` to silence a message class for good — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 2)
- Ship offline `fm docs <query>` with stable codes that refusals link to — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 2)
- Translate refusals into a before/after command pair — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 3)
- Gloss `fm status` and drop ticket numbers from user-facing text (Round 3)
- Print a verified "try it yourself" line at every close — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Show a "what you can safely ignore" line per task — near T-0262 (done): Smarter nudges: already-covered requests, decision revisit … (Round 4)
- Teach the model the refused-then-retried pattern — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Round 4)
- Quote the user's own request back, side by side with Foreman's reading — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 4)
- Replace jargon in the first-session band with a swappable "plain" vocabulary (Round 4)
- Count which nudges and refusals users overrode per verb, and offer to quiet them — near T-0228 (done): foreman-ui catch-up: budget, bench and evolve, research ask… (Round 4)
- Give every refusal a "tell the user" plain sentence for the model to relay — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)

## [build] meta-process — Round process and project meta: roadmap, not-building, llms.txt, docs by audience, pitch
value 3 · effort S · risk low · honest expectations for newcomers
Exists: no 'when not to use' section in README
Premise: ok: small real gap
First slice: README: a short 'When not to use Foreman' section
Ideas (14):
- Add a "when not to use Foreman" section (Round 1)
- Switch the evidence source when a brainstorm round runs dry — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Round 2)
- Give reviewers a "done well" line — near T-0779 (done): Lane briefs pass a per-tier effort with the model (Round 2)
- Wild: Run an annual "defend or delete" report (Round 2)
- Run a domain-persona sweep (wild) — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 3)
- Pick one headline persona: the safe overnight queue — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Propose the kernel upstream as a concrete Claude Code feature request — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 3)
- Require external evidence before a recursive round starts — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Round 4)
- Wild: Hold a weekly "outside-only" day (Round 4)
- Own the search term and the one-line pitch — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Publish `llms.txt` and an AGENTS.md for Foreman itself (Round 4)
- Generate a public ROADMAP.md with a won't-do list — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Publish a "Not building" page answering the rival survey — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Split the docs by audience with enforced word budgets — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 4)

## [done] bypass-earned — Bypass mode earned/expiring, never default; ask-first posture, tighten when unattended
value 4 · effort S · risk med · folded into install-plan-consent: ask before bypass
Exists: bypass default (install.sh:131), guard, sensitive repos, /fm-trust
Premise: ok, but leases/expiry add machinery to an install-time choice
Ideas (15):
- Offer bypass only after Foreman has earned it — near T-0700 (done): Drive: the Stop hook re-offers 'fm second plan T-0672' afte… (Round 1)
- Wild: make Foreman safe enough that bypass mode is not needed (Round 1)
- Make install plan-then-apply, with bypass earned instead of defaulted — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Make bypass mode an explicit, explained opt-in (Round 1)
- Tighten the guard automatically when nobody is watching — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 1)
- Wild: Expire bypass mode on a lease (Round 1)
- Earn the allowlist instead of defaulting to bypass (Round 2)
- Count allows made by silence, not by proof — near T-0716 (done): Pipe-into-shell gaps (T-0715 review): option args read as s… (Round 2)
- Let learned approvals only narrow — near T-0671 (done): Milestone: Features — Autonomy and the user (Round 2)
- Earn bypass mode instead of defaulting to it (Round 3)
- Log what default mode would have asked, so bypass can be earned (Round 3)
- Keep bypass mode conditional on a live guard — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Wild: Add a cooling-off delay and a notification for every loosening of safety settings (Round 4)
- Default to a ask-first permission posture, with bypass as an explained opt-in (Deepened: trust)
- Wild: Let trust grants expire (bypass for 7 days, renewed by `fm trust`) (Deepened: install)

## [done] gate-packs — Stack presets and gate packs, community recipes, task and example galleries, commons
value 4 · effort S · risk low · shipped in T-0855
Exists: fmmap._gates table: pytest (configured), unittest fallback, npm, cargo, go, make (T-0855)
Premise: false: the detector exists and fm check offers its first match
Ideas (9):
- Ship stack packs picked at `fm init` — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 2)
- Add `fm examples`, a searchable gallery of real terse requests (Round 2)
- Wild: add a Foreman Exchange of stack packs and lessons with bench receipts (Round 2)
- Ship a task-template gallery (Round 2)
- Publish ecosystem gate packs as data — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 2)
- Wild: Fetch a signed, read-only "Foreman Commons" feed — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 2)
- Add community gate recipes keyed by detected stack — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 2)
- Add stack presets with fixture repos for ten ecosystems — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 2)
- Rank gate-verifier packs from a registry with sandboxing and scorecards — near T-0707 (done): Frontier 07 — Knowledge graph (Round 2)

## [done] forgiving-task-new — fm task new / capture / add one forgiving path, valid values in help, whole-suite gates
value 2 · effort S · risk low · covered
Exists: short help, values, example, capture reuse, done leads with finish (T-0854)
Premise: false: shipped
Ideas (17):
- Detect the test runner and offer it as the gate on first `fm check` — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 1)
- Make `fm task new` smart about duplicates and self-describing (Round 1)
- Stop `fm repeats` suggesting single test modules as every-task gates — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 1)
- Make the `fm task done` refusal print a prefilled `fm task finish` call — near T-0682 (done): Milestone: Features — Verification and product checking (Round 1)
- Warn when `fm task new` duplicates an open capture, and offer to adopt it — near T-0821 (done): Round-1 review fixes (low): outward-tool gate fails closed,… (Round 1)
- End every `--help` with a worked example and the valid values (Round 1)
- Make `fm task new` pick up a matching capture and list valid values — near T-0004 (done): Phase 6: fm tidy and fm doctor (Round 1)
- Make `fm task new` forgiving (Round 1)
- Fix the newcomer dead ends in `fm task new` and `capture` — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 1)
- Make `fm repeats` suggest only whole-suite gates (Round 1)
- Stop `capture` then `task new` from duplicating, and list valid values in `task new --help` — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 1)
- Close the task and write its CHANGELOG line in the same call — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 2)
- Make `fm task new` adopt the matching capture — near T-0729 (done): Friction: lane rm unlocks a finished builder's worktree; no… (Round 2)
- Let `fm task new` adopt a matching capture and print valid values (Round 3)
- Replace capture, task new and batch with one `fm add` — near T-0729 (done): Friction: lane rm unlocks a finished builder's worktree; no… (Round 4)
- Let `fm task done` refuse with one prefilled, copy-ready `fm task finish` line — near T-0691 (done): Milestone: Intelligence — Planning and decomposition (1) (Deepened: onboarding)
- Make `fm task new` and `fm capture` one forgiving path with real help — near T-0682 (done): Milestone: Features — Verification and product checking (Deepened: onboarding)

## [done] shell-python-hygiene — Shell/Python hygiene and robust installs: PATH, no shadowing, offline, CI matrix, footprint gate
value 2 · effort M · risk low · fm in a plain shell and doctor-on-fresh-install shipped in T-0855
Exists: ~/.local/bin/fm link (T-0855); Python auto-install; first-run tests
Premise: false: shipped
Ideas (15):
- Put `fm` on the user's shell PATH at install — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 1)
- Put `fm` on the shell PATH, and never shadow another `fm` — near T-0286 (done): Self-improvement pass 4: guard heredoc precision, test lock… (Round 1)
- Make `fm` work in a normal shell (Round 1)
- Make installs work behind a proxy, mirror or no network (wild) (Round 3)
- Make a fresh install pass its own `fm doctor` and put `fm` on the shell PATH — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 3)
- Add a managed-install profile for company machines — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Ship an offline, resumable installer bundle (Round 3)
- Test install across shells and distros in CI and publish the matrix — near T-0442 (done): Guard parity across harnesses: same decision on codex, gemi… (Round 3)
- Make installer and first-run output safe for non-tty, NO_COLOR and screen readers (Round 3)
- Stop the installer's Python shadowing the system `python3` (Round 3)
- Give `fm` a shell front door with `eval "$(fm shellinit)"` (Round 4)
- Fail the release on install footprint — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 4)
- Make `fm` work in every shell and pass doctor on a fresh install — near T-0207 (done): Debugging ledger: hypotheses in the brief that fm next driv… (Deepened: install)
- Gate releases on a clean-HOME install test — near T-0678 (done): Milestone: Features — Releases and delivery (Deepened: install)
- Pin an isolated Python so Foreman never shadows the system `python3` — near T-0399 (done): Builder brief: edit files with the Edit/Write tools, never … (Deepened: install)

## [done] doctor-first-run — fm doctor first-run checklist/verdict, self-healing, hook cost and client matrix
value 2 · effort M · risk low · shipped
Exists: doctor warns on no backups, shows only problems unless -v (T-0855)
Premise: false: fixed
Ideas (12):
- Make a fresh install pass its own `fm doctor` and end with one line — near T-0207 (done): Debugging ledger: hypotheses in the brief that fm next driv… (Round 1)
- Make a fresh install pass its own `fm doctor` — near T-0207 (done): Debugging ledger: hypotheses in the brief that fm next driv… (Round 1)
- Stop a fresh install from failing its own `fm doctor` — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- Start `fm doctor` as a first-run checklist, not a failure — near T-0676 (done): Milestone: Features — Performance and cost (Round 1)
- Teach every error and empty state the next command — near T-0686 (done): Milestone: Intelligence — Debugging and diagnosis (Round 1)
- Replace the first-run `fm doctor` failure with a one-line verdict — near T-0704 (done): Frontier 04 — Zero-call bookkeeping and session lifecycle (Round 2)
- Check that every first-run message names its next command — near T-0440 (done): Every refusal names its fix; a third identical refusal esca… (Round 3)
- Make every empty state say what to do next, in plain words — near T-0207 (done): Debugging ledger: hypotheses in the brief that fm next driv… (Round 3)
- Add `fm doctor --one` that prints a single line — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 4)
- Rank every hot-path hook by cost against catches and show the table in `fm doctor` — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 4)
- Show a per-client capability matrix (CLI, IDE extensions, desktop, web) in `fm doctor` (Round 4)
- Replace `fm doctor`'s fresh-install failure with a first-run checklist that self-heals — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Deepened: onboarding)

## [done] cli-front-door — Shrink CLI to a ten-verb front door, forwarding aliases, noun-verb, net-surface budget
value 2 · effort L · risk high · the new-user problem is solved; merging verbs is churn
Exists: START_HERE 12-command help (fmcli.py:3487), fm help --all
Premise: false: shipped in T-0854
Ideas (18):
- Hide the 108-verb surface behind a ten-verb `fm help` and a pointed `--help` (Round 1)
- Keep removed verbs as one-line forwards — near T-0686 (done): Milestone: Intelligence — Debugging and diagnosis (Round 1)
- Fold the diagnostic verbs into `fm inspect`, with aliases that teach (Round 1)
- Make `fm --help` the 8-verb front door (Round 1)
- Give the CLI a noun-verb grammar with a forwarding table (Round 2)
- Wild: Add `fm one` as the whole interface for week one — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 2)
- Attribute every `fm` verb call to its caller (Claude, human or hook) — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 2)
- Make `fm help` the front door: 10 verbs, one example each (Round 3)
- Refuse to grow: a net-surface budget that fails the release — near T-0672 (done): Milestone: Features — Guard and safety (Round 3)
- Collapse the CLI to a "core 8" help and a forwarding table for the rest (Round 3)
- Collapse the CLI to ten front-door verbs, with forwarding aliases (Round 3)
- Tag each verb for the human or the model — near T-0690 (done): Milestone: Intelligence — Metacognition and calibration (Round 4)
- Show the `fm` verbs used per caller (Claude, human, hook) to find what to hide (Round 4)
- Retire a verb or setting before adding one, tracked in a net-surface ledger — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 4)
- Collapse six task types into "change" and "question" — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 4)
- Add an `fm x` namespace where new verbs live until they earn promotion — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 4)
- Move the 46 unused verbs into one lazily imported `labs` module (Round 4)
- Hide the 108-verb surface behind progressive disclosure (`fm help` tiers) (Deepened: onboarding)

## [later] postures-lite — Named postures and Lite/observe-only first week, project-fit recommendation
value 4 · effort L · risk med · ship the bypass question first and see how many choose off
Exists: no posture concept; only --no-bypass/--no-plugins and fm autonomy
Premise: unclear: an observe-only mode needs hook-by-hook semantics
Ideas (12):
- Offer a Foreman "lite" posture chosen at install: ask, don't assume bypass (Round 1)
- Offer a week of observe-only mode beside the user's current plugin — near T-0280 (done): Bench family: judged cases, plugin duels, version replays, … (Round 1)
- Wild: "Foreman Lite" first week — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 1)
- Show the 20 deny rules as three named presets — near T-0004 (done): Phase 6: fm tidy and fm doctor (Round 2)
- Wild: Start new projects in observe-only mode (Round 2)
- (wild) Race lean, standard and strict profiles on your own idle tasks (Round 2)
- Score project fit at init and recommend a posture per repo (Round 2)
- Scope the discipline to Foreman projects only — near T-0708 (done): Frontier 08 — Orchestrator control plane (Round 3)
- Wild: Offer a "Foreman Lite first week" that quietly runs observe-only beside the user's habits (Round 3)
- Wild: Add a "Foreman Lite" first week with observe-only mode — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Replace the install's 20 settings with three named postures — near T-0765 (done): A verify that can't run at all (python3 -m <missing module>… (Round 4)
- Ship three named postures (Observe, Guide, Enforce) instead of 20 settings (Deepened: install)

## [later] newcomer-gates — Newcomer-path CI gates: clean-HOME, cold-agent, stuck-ladder, release-check
value 3 · effort S · risk low · the suite has never run without claude installed; a CI workflow could go red on the public repo: try it on a scratch runner first
Exists: test_firstrun*.py, test_setup; no .github CI
Premise: ok: nothing runs the newcomer tests outside this machine
Ideas (13):
- Keep the clean-HOME newcomer walkthrough as a permanent no-model gate — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 1)
- Wild: A/B the README with cold agents — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 2)
- Audit launch hygiene before the public push — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 3)
- Close this round with a five-item "Newcomer" release gate — near T-0678 (done): Milestone: Features — Releases and delivery (Round 3)
- Rank the pile by "what a newcomer would feel", then freeze it (Round 4)
- Test one "stuck newcomer" ladder per dead end A1–A11 (Round 4)
- Add `fm first-hour`: score the install against a cold agent playing newcomer (Round 4)
- Run a "rival-installed" newcomer path as a permanent no-model test — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 4)
- Show which verbs a cold agent can't discover — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Round 4)
- Make `fm release-check` one command that runs every newcomer and fault gate — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 4)
- Ratchet newcomer-path cost in CI — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 4)
- Wild: publish a nightly "time to first task" badge from the clean-HOME run — near T-0685 (done): Milestone: Intelligence — Cognitive architecture and wild b… (Round 4)
- Wild: Make a stranger test the CI gate: a scripted persona runs the install and first task, and the build fails if friction grows (Deepened: onboarding)

## [later] tour-learn — Guided tutorials: tour, learn, quest, spar, git-repo lesson, 7-day course
value 3 · effort M · risk low · see whether fm demo plus the new first-run guidance are enough
Exists: fm tour (different meaning), fm adopt, fm bench stranger
Premise: false: no tutorial exists, but the need is unproven after the first-run fixes
Ideas (14):
- Add `fm hello`, a 60-second guided first task on a throwaway fixture — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 1)
- Wild: Offer a "first real task" tour on the newcomer's own repo — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Wild: Give a first-scan gift at install — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 1)
- Wild: Add `fm learn`, a rustlings-style tutorial — near T-0684 (done): Milestone: Intelligence — Brainstorming and ideation (Round 1)
- Wild: unlock a seven-day tour, one seeded-bug lesson per day (Round 2)
- Wild: play a toy while a long gate runs — near T-0364 (done): Foreman keeps working while background jobs run, plans and … (Round 2)
- Add a "first win in 5 minutes" path: `fm hello` fixes a seeded bug in a throwaway fixture (Round 3)
- Wild: Add `fm hello`, a guided first real task on the user's own repo — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: add `fm spar`, a seeded-bug drill on a throwaway copy of the user's own repo (Round 3)
- Wild: Play a Foreman quest with `fm quest`, a text adventure through the verbs (Round 4)
- Wild: Keep a weekly queue bingo card — near T-0146 (done): Dashboard: no duplicates between band and pane, nothing sta… (Round 4)
- Wild: make the tutorial a git repo whose history is the lesson — near T-0692 (done): Milestone: Intelligence — Planning and decomposition (2) (Round 4)
- Wild: Turn the tutorial into a git repo whose history is the lesson, graded by Foreman itself — near T-0706 (done): Frontier 06 — Debugging intuition engine (Deepened: onboarding)
- Walk a newcomer through a 60-second `fm tour` in a scratch repo (Deepened: install)

## [later] start-ladder — One resumable fm start ladder and first-session guidance (strips, fading wheels, starter tasks)
value 3 · effort M · risk low · needs evidence the first-run guidance falls short
Exists: init/status guidance, 12-command --help, task new example (T-0854)
Premise: ok but mostly covered by the first-command fixes
Ideas (18):
- Fade out training wheels over the first three tasks — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 1)
- Order and label the slash menu as a journey (start, work, finish, recover) (Round 2)
- Wild: add a stuck-newcomer rescue ladder (Round 2)
- Run a newcomer's first three tasks in probation lanes — near T-0440 (done): Every refusal names its fix; a third identical refusal esca… (Round 2)
- Open with a one-line "first win" receipt after the first finished task — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 3)
- Print a quiet "queue zero" moment when the last task closes — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 3)
- Greet a resumed session with a "last time" line that names the exact step — near T-0781 (done): Sessions are named after their task: SessionStart and UserP… (Round 3)
- Wild: Let the guard's first save become a keepsake line — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 3)
- Track install-day milestones and nudge the next missing one once — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 3)
- Surface the first-session path as a single conversational `/foreman:start` skill — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 3)
- Hand the newcomer a "you're here" strip after every command until three tasks close — near T-0672 (done): Milestone: Features — Guard and safety (Round 3)
- Make the first-run experience one command and one line of output — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 3)
- Propose three starter tasks from the repo's own signals at `fm init` — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 3)
- Show a setup ladder in the statusline — near T-0681 (done): Milestone: Features — UI and motion (Round 3)
- Wild: Offer a "foreman walk-through" card on new repos' first session — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 4)
- Wild: Add "On this day" to the greeting — near T-0685 (done): Milestone: Intelligence — Cognitive architecture and wild b… (Round 4)
- Merge the proposed onboarding verbs into one resumable `fm start` ladder — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Make one resumable `fm start` ladder that owns the whole first hour — near T-0436 (done): fm pause: one flag stops everything Foreman runs unattended (Deepened: onboarding)

## [later] keep-or-leave — Day-7 earned-its-place card, once-offer, self-uninstall, re-engagement, graduation
value 3 · effort M · risk med · one user and one bench case: nothing to measure yet
Exists: escape events in the ledger (fmfriction.py:187)
Premise: unclear: nudging users unprompted needs a safe channel and a signal
Ideas (14):
- Wild: add a once-a-quarter "hide it for a week" for unused verbs (Round 1)
- Wild: Day-30 time capsule that scores the user's own annoyance — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 2)
- Add a day-7 keep / lite / remove card seeded by a one-line wish — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 2)
- Re-engage an installed-but-unused Foreman once, with the exit offered beside it (Round 2)
- Count the user's escapes from Foreman as the honest satisfaction signal — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 3)
- Add a "Foreman earned this" card at day 7 with keep / lite / remove (Round 3)
- Wild: Print a shareable postcard when a milestone closes — near T-0692 (done): Milestone: Intelligence — Planning and decomposition (2) (Round 3)
- Graduate the user: bake the learned rules into the repo and let Foreman retire — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 3)
- Run one task under Foreman, then offer keep or drop with `fm once` — near T-0676 (done): Milestone: Features — Performance and cost (Round 3)
- Wild: let Foreman offer to uninstall itself at day 14 if it can't show lift (Round 3)
- Put a "was it worth it?" one-key rating on close, feeding the held-rate evidence (Round 4)
- Use day-7 keep rate as the round's north-star metric (Round 4)
- Wild: a day-7 "did Foreman earn its place" card with keep / lite / remove (Deepened: trust)
- Wild: let Foreman recommend its own uninstall when the bench shows no lift — near T-0685 (done): Milestone: Intelligence — Cognitive architecture and wild b… (Deepened: trust)

## [later] data-safety — Protect user work and secrets; undo/rescue; auditable guard core
value 3 · effort M · risk med · needs a decision on what the guard protects and evidence of loss
Exists: fm secrets (fmsecrets.py:205), fm sensitive, fm adopt; no snapshot of uncommitted work
Premise: ok in part
Ideas (17):
- Add `fm shield`, a scan of the user's whole Claude config — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 1)
- Wild: Detect first-week confusion and file it as a task against Foreman — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Wild: Run the guard over commands the user pastes into the prompt — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 1)
- Add `fm new` for empty directories (Round 2)
- Add `fm where-is-my-work` (Round 2)
- Honor `<private>` spans and `.foremanignore` everywhere (Round 2)
- Keep a shadow-repo safety net for what git can't restore — near T-0672 (done): Milestone: Features — Guard and safety (Round 2)
- Make `<private>` spans invisible to Foreman's stores (Round 2)
- Run Foreman in directories with no git — near T-0413 (done): Audit diffs leave out secrets (Round 3)
- Write a session blast-radius receipt — near T-0707 (done): Frontier 07 — Knowledge graph (Round 3)
- Protect the user's own uncommitted work from the agent — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Add `fm rescue` for a half-finished human branch (Round 4)
- Wild: Disclose Foreman's competence per stack at plan time — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Add `fm oops`, a one-word "that was wrong" — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 4)
- Keep the guard core to one auditable page — near T-0752 (done): Milestone: Learning, paid half — evals on block, bench hold… (Round 4)
- Make the guard core one auditable page with a published threat model — near T-0672 (done): Milestone: Features — Guard and safety (Deepened: trust)
- Add `fm oops`: one word for "that was wrong", which reverts and teaches — near T-0689 (done): Milestone: Intelligence — Learning from outcomes (Deepened: trust)

## [later] rival-coexist — Coexist with rivals: import specs, aliases, cheat sheets, peace treaty, conform tests
value 3 · effort M · risk low · needs evidence of which rivals users arrive from
Exists: fmplugins search/scoring; no import from Task Master/spec-kit/CCPM
Premise: unclear: no evidence users migrate from them
Ideas (10):
- Import work from Task Master, spec-kit and CCPM (Round 1)
- Alias rival command names to Foreman procedures — near T-0327 (done): Foreman Desktop: private ssh control socket, confirmed host… (Round 2)
- Say "coming from X": add `fm help --from <plugin>` cheat sheets (Round 2)
- Make a peace-treaty card for coexisting plugins (Round 2)
- Add `fm coexist <plugin>`: stage ownership plus a translation cheat sheet — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 2)
- Turn rivals' loudest complaints into "Foreman must not" tests (Round 3)
- Spend a "rival swap day" to find the felt gaps (wild) (Round 3)
- Keep rival task files and the Foreman queue in sync in both directions — near T-0277 (done): Research rigor: page cache and --file batches, cross-checks… (Round 3)
- Wild: Certify third-party plugins with `fm conform` — near T-0280 (done): Bench family: judged cases, plugin duels, version replays, … (Round 4)
- Offer a polite handoff line when a rival skill takes the wheel (Round 4)

## [later] bench-vs-plain — Prove lift vs plain Claude and rivals: bench, duel, n-of-1, own-history replay, referee
value 3 · effort L · risk med · needs a real case corpus before any lift claim
Exists: fm bench duel/versions/court/soak (fmbench.py:703); fm replay; outcomes
Premise: false: the verbs exist; the bench has 1 case
Ideas (25):
- Ship a published proof page: Foreman vs. bare Claude Code on a public task set — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 1)
- Wild: Give Foreman a "tell me what you'd have done differently" receipt vs. plain Claude (Round 1)
- Add `fm preview`, a read-only audit of the user's past Claude sessions — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 1)
- Replay the user's own history through Foreman at install — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Measure Foreman's lift from the user's own pre- and post-install transcripts — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Wild: Proof page for newcomers — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Wild: Volunteer-compute bench with opt-in leftover quota (Round 2)
- Turn the 18 "fixed later" tasks into the first real bench — near T-0783 (done): Big Bash outputs reach the model as head, tail and failure … (Round 2)
- (wild) Run a public "forge a done" challenge that feeds the bench (Round 2)
- Wild: run `fm duel --vs <plugin>` on the same real task — near T-0669 (done): Guard hardening: fuzzer escape classes 2-5 and 7-9, one clo… (Round 2)
- Show a before/after proof strip from Foreman's own ledger — near T-0672 (done): Milestone: Features — Guard and safety (Round 3)
- Publish a convergence certificate so "keep going" can end (wild) (Round 3)
- Print a "ceremony tax" line comparing a Foreman task with a bare-Claude baseline — near T-0695 (done): Milestone: Intelligence — Steps and execution craft (Round 3)
- Measure Foreman's marginal lift on top of each rival (Round 3)
- Run a randomized n-of-1 trial in the user's own repo — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 3)
- Turn the bench into a neutral plugin referee — near T-0224 (done): Fm evolve — a bench-gated self-improvement loop: a mutation… (Round 3)
- Publish a proof page that compares Foreman with bare Claude Code — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: Ship `fm duel --vs <plugin>` to run one real task both ways on throwaway lanes (Round 3)
- Ship `fm repro-bench`, a skeptic's kit that reruns the headline claim locally (Round 3)
- Bench the user's own CLAUDE.md lines against their ledger — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Treat every "Foreman off for this task" escape as a free control group — near T-0690 (done): Milestone: Intelligence — Metacognition and calibration (Round 4)
- Wild: add Referee mode, a read-only live grader for any Claude Code session — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Wild: add `fm autopsy-me`, naming the user's three costliest habits from their own transcripts — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Produce a public, reproducible "with vs. without Foreman" proof from `fm demo` — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Deepened: onboarding)
- Preview on the user's own history: `fm preview` replays past sessions to show what Foreman would have caught — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Deepened: onboarding)

## [later] published-metrics — Honest published held-rate, scorecards, evidence pages, rival tables, README lint
value 2 · effort M · risk med · needs bench cases and real denominators first
Exists: bench scorecard (fmbench.py:767); no published held-rate
Premise: false: 1 bench case makes any published rate noise
Ideas (18):
- Publish the real held-rate with its denominators (Round 1)
- Wild: Give repos a "Foreman-verified" badge backed by a proof pack — near T-0707 (done): Frontier 07 — Knowledge graph (Round 1)
- Wild: Collect an opt-in, verb-only usage census across users (Round 1)
- Wild: Generate the README proof strip from the ledger at release — near T-0672 (done): Milestone: Features — Guard and safety (Round 1)
- Rewrite the README's first screen from the ledger — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 1)
- Publish the held-rate as a self-updating evidence page — near T-0786 (done): fm page: the queue (and optionally a brainstorm catalogue) … (Round 1)
- Put a 60-second before/after on the README's first screen — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 1)
- Wild: Publish a live "held rate" badge computed from the ledger — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 1)
- Publish a safety scorecard against bare bypass mode (Round 1)
- Publish a measured rival comparison table (install touches, always-on tokens, verbs) (Round 2)
- Wild: Print a diff of the user's own verb habits — near T-0682 (done): Milestone: Features — Verification and product checking (Round 2)
- Lint the README so every number cites a results file — near T-0691 (done): Milestone: Intelligence — Planning and decomposition (1) (Round 2)
- Publish an open evidence-receipt schema with a validator — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Wild: publish a browsable, redacted replay of the author's real ledger — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Publish what the guard cannot stop, generated from xfail tests (wild) — near T-0442 (done): Guard parity across harnesses: same decision on codex, gemi… (Round 3)
- Gate every release on a generated proof pack — near T-0710 (done): Frontier 10 — Milestone work compiler and merge train (Round 4)
- Add a lifetime "guard and gate saves" counter in the statusline — near T-0681 (done): Milestone: Features — UI and motion (Round 4)
- Make the held rate honest: a ledger-derived scorecard with ungraded work shown as ungraded (Deepened: trust)

## [skip] reversible-install — Reversible install journal, byte-clean uninstall/eject, preserve user settings and decisions
value 2 · effort M · risk med · covered by the manifest and backups
Exists: install manifest + settings backups; uninstall-user reverses exactly (fmsetup.py:1-5,241); T-0851 removes empty leftovers
Premise: false: journal and exact undo exist
Ideas (15):
- Make uninstall leave nothing behind and restore prior settings exactly (Round 1)
- Wild: Hold an uninstall exit interview that leaves nothing behind — near T-0174 (done): Parallel runs clean up after a failure, re-check main befor… (Round 1)
- Wild: Uninstall that leaves byte-identical `~/.claude` — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 1)
- Make the `~/.claude` wiring a git-backed journal so uninstall is a revert — near T-0682 (done): Milestone: Features — Verification and product checking (Round 2)
- Keep every setting the user already chose — near T-0783 (done): Big Bash outputs reach the model as head, tail and failure … (Round 2)
- Remember the user's reversals and never re-apply them on update — near T-0680 (done): Milestone: Features — Self-improvement and learning (Round 2)
- Resume a partly failed install from where it stopped — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 3)
- Wild: Add `fm eject`, leaving plain markdown and no Foreman (Round 3)
- Snapshot all of `~/.claude` at session start and add `fm claude-undo` — near T-0677 (done): Milestone: Features — Planning, briefs and queue (Round 4)
- Wild: Let the uninstall be a graceful goodbye that proves it left nothing (Round 4)
- Prove Claude still starts after wiring, and ship a file-based off switch (Round 4)
- Make an upgrade unable to widen permissions without consent (Round 4)
- Ship a trust ledger: show every change install made, with a one-line undo each — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Deepened: onboarding)
- Record every install change in a reversible journal — near T-0682 (done): Milestone: Features — Verification and product checking (Deepened: install)
- Keep a decision ledger that updates never override — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Deepened: install)

## [skip] guard-hardening — Guard hardening: interlocks, injection tracing, human-only verbs, effect matrix, signed rules
value 2 · effort M · risk med · large surface, no new-user payoff
Exists: fm pause, typed-only fm trust, sensitive repos, guard fuzzing (T-0669)
Premise: ok: mostly shipped
Ideas (26):
- Wild: A "pause Foreman" one-word escape that hides it for a single task — near T-0669 (done): Guard hardening: fuzzer escape classes 2-5 and 7-9, one clo… (Round 1)
- Add an env var and verb to switch individual hooks off (Round 1)
- Make safety-loosening verbs human-only — near T-0672 (done): Milestone: Features — Guard and safety (Round 1)
- Review instruction files that arrive by pull or checkout — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence (Round 1)
- Interlock any command that can reach a production target — near T-0777 (done): Never idle without tmux: a plugin monitor streams this sess… (Round 2)
- Match outbound payloads against the exact secret values seen this session (Round 2)
- Gate unattended runs on human origin — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 2)
- Trace a blocked command back to the content that planted it — near T-0672 (done): Milestone: Features — Guard and safety (Round 2)
- Shell-quote every command Foreman prints or injects — near T-0729 (done): Friction: lane rm unlocks a finished builder's worktree; no… (Round 2)
- Keep Foreman's own credentials in the OS keyring — near T-0841 (done): A resumed session keeps its mail watcher and isn't 'another… (Round 2)
- Ship a signed, tighten-only guard rule feed — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 2)
- Wild: A "Foreman off for this task" one-word escape — near T-0669 (done): Guard hardening: fuzzer escape classes 2-5 and 7-9, one clo… (Round 3)
- Interlock edits to files that run code on the next test or build — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 3)
- Lint allow rules that equal arbitrary code execution — near T-0691 (done): Milestone: Intelligence — Planning and decomposition (1) (Round 3)
- Demote the session after a dangerous-command strike (wild) (Round 3)
- Seed the guard corpus from public agent-incident postmortems (Round 3)
- Probe whether a rival plugin's hook can override Foreman's deny (Round 3)
- Tag each verify command with where it came from, and ask once before running a new source — near T-0706 (done): Frontier 06 — Debugging intuition engine (Round 4)
- Give every `fm` verb an effect class and enforce a caller-by-effect matrix (Round 4)
- Don't let hook profiles or env vars switch off the guard (Round 4)
- List the files the self-improvement loop can never edit — near T-0286 (done): Self-improvement pass 4: guard heredoc precision, test lock… (Round 4)
- Only act on public issues and PRs from trusted authors — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 4)
- Cap CPU, memory and process counts for children and gates — near T-0693 (done): Milestone: Intelligence — Reasoning and thought process (Round 4)
- Treat guard and hook messages as an injection surface — near T-0679 (done): Milestone: Features — Resilience, state and simplicity (Round 4)
- Wild: Run Foreman's own hooks under a Landlock or seccomp filter (Round 4)
- Wild: Add `fm attack-me`, a bounded red-team run against the user's real config — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 4)

## [skip] memory-knowledge — Cross-session memory, cold-start priors, runbooks, incident names, repo tour
value 2 · effort M · risk med · speculative
Exists: fm recall, fm adopt, tidy lints MEMORY.md
Premise: unclear: a new user has no memory to import
Ideas (9):
- Import an existing repo's conventions into injected standards (`fm adopt` standards) — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Wild: put quality debt on a visible ledger — near T-0696 (done): Milestone: Intelligence — Understanding the request and the… (Round 2)
- Tour an unfamiliar repo from the map — near T-0807 (done): A lane's edits recorded under .claude/worktrees/<lane>/ cou… (Round 2)
- Keep a shelf of firsts — near T-0817 (done): Guard refusals read better: /dev/null on a data-only python… (Round 2)
- Ship cold-start priors distilled from the 688-task ledger — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 2)
- Import claude-mem and auto-memory observations into `fm recall` — near T-0674 (done): Milestone: Features — Observability, replay and trust (Round 2)
- Wild: Give each repo a "Foreman scar map" built from its own fixed-later tasks — near T-0707 (done): Frontier 07 — Knowledge graph (Round 3)
- Learn the project's runbook from commands that worked — near T-0808 (done): fm check --affected works in Foreman's own project; lane br… (Round 4)
- Name each major incident and use the name in recall — near T-0707 (done): Frontier 07 — Knowledge graph (Round 4)

## [skip] away-queue — Safe overnight/away queue: fm away/leave, sleep inhibitor, remote notify, chat-ops
value 2 · effort M · risk med · chat bridges clash with the sensitive-repo posture
Exists: fm night, fm notify, PushNotification asks, mail watcher, fm pause, OSC progress
Premise: false: largely covered
Ideas (13):
- Bridge Telegram, Slack and ntfy both ways, outbound-only (Round 2)
- Wild: Add chat-ops with two-person approval for one-way doors (Round 2)
- (wild) Approve a yes/no by replying to an SMS or email — near T-0015 (done): Foreman-aware conversation view: output style, richer badge… (Round 2)
- Add `fm away <until>`, one verb for "I'm gone" (Round 4)
- Hold a sleep inhibitor while an unattended run is live (Round 4)
- Wild: React to the user's red test run before they read it — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Stamp each queued brief with "needs a human?" up front (Round 4)
- Show true repo trivia instead of a spinner on gates over 20 s — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Alert through the terminal itself (OSC 9/777 plus bell) — near T-0778 (done): Phone push when the user is needed or the queue drains: the… (Round 4)
- Add `fm tail --why`, one live stream that names the cause — near T-0207 (done): Debugging ledger: hypotheses in the brief that fm next driv… (Round 4)
- Wild: Serve a 1-bit status image for an e-ink or old-tablet desk display (Round 4)
- Add `fm leave 8h`, one verb for the safe overnight queue — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Wild: add a commute briefing with spoken return card and voice yes/no — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 4)

## [skip] digest-unify — Reporting views: one weekly view crediting folded tasks, usage-aware what's new, release notes
value 2 · effort M · risk low · refactor with no new-user value
Exists: digest counts folded tasks (T-0855); cost/usage/burden verbs
Premise: false: main complaint fixed
Ideas (12):
- Grade folded tasks through their parent — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 1)
- Fold child tasks into their parent in `fm digest` — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators (Round 1)
- Write release notes from the user's own usage — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 2)
- Show a "what's new for you" card after an upgrade, filtered to verbs the user runs — near T-0117 (done): While-you-were-away row: what drive finished since the user… (Round 2)
- Tell the user what's new for them after an upgrade — near T-0778 (done): Phone push when the user is needed or the queue drains: the… (Round 2)
- Show usage-aware "what's new" on upgrade — near T-0681 (done): Milestone: Features — UI and motion (Round 2)
- Unify the three result shapes for `fm status`, `fm task show` and `fm digest` into one view model (Round 2)
- Wild: Add `fm wager`, a one-line prediction logged before any task and scored at close — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 3)
- Merge `fm digest`, `fm stats` and `fm cost` into one per-week view that credits folded tasks to their parent (Round 3)
- Attribute and license-check ported skills — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Get the ledger's folded tasks counted once in the weekly view — near T-0676 (done): Milestone: Features — Performance and cost (Round 4)
- Fold ungraded folded tasks into their parent's grade (Round 4)

## [skip] internals-simplify — Internal consolidation: one git module, one prompt tree, disposable derived state, scaffold
value 2 · effort M · risk med · hygiene only; fmguard is hook-hot
Exists: seven _git helpers with different signatures
Premise: ok: duplication is real
Ideas (9):
- Merge the seven `_git` helpers into one module — near T-0280 (done): Bench family: judged cases, plugin duels, version replays, … (Round 1)
- Replace the seven `_git` copies with one tested module — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 1)
- Compile one prompt tree into every injected surface — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 2)
- Require a 12-word purpose sentence per module (Round 2)
- Merge the seven `_git` helpers and three child launchers into one tested module each — near T-0280 (done): Bench family: judged cases, plugin duels, version replays, … (Round 3)
- Add `fm scaffold verb|hook|skill` — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Add a "reachability" tag to every MASTER.md section — near T-0205 (done): fm next names the installed third-party skills that fit a t… (Round 4)
- Prove derived state is disposable — near T-0686 (done): Milestone: Intelligence — Debugging and diagnosis (Round 4)
- Let doc sections expire unless re-verified — near T-0691 (done): Milestone: Intelligence — Planning and decomposition (1) (Round 4)

## [skip] forge-issue-sync — Issue-tracker/forge sync and CI: GitHub issues both ways, Action, required check, adapters
value 2 · effort L · risk med · outward-facing work with no user base yet
Exists: fm inbox gh imports open issues (fmeco.py:216-235)
Premise: unclear: inbound half exists
Ideas (10):
- Turn a labelled GitHub issue into a verified PR in CI (Round 2)
- Wild: credit every external bug report that becomes a bench case — near T-0685 (done): Milestone: Intelligence — Cognitive architecture and wild b… (Round 2)
- Publish deferred briefs as contributor issues, dry-run by default — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 2)
- Wild: draft fixes for open good-first-issues in popular small repos, drafts only (Round 2)
- Add a forge adapter layer (GitHub, GitLab, Gitea/Forgejo) (Round 2)
- Add `fm report-miss`: a redacted, preview-first bundle for a GitHub issue (Round 2)
- Wild: Issue-comment `/foreman` Action that returns a PR with a proof pack (Round 2)
- Mirror tasks with GitHub Issues, posting evidence as comments (Round 2)
- Bridge tasks and GitHub Issues both ways, with evidence as comments (Round 3)
- Publish `foreman/evidence` as a GitHub required status check — near T-0682 (done): Milestone: Features — Verification and product checking (Round 4)

## [skip] team-share — Teams and contributors: invite/join, committed project config, onboard pack, guest, passport
value 2 · effort L · risk med · revisit when a second user asks
Exists: fm export agents, fm share; no committed project config
Premise: ok but no team evidence
Ideas (10):
- Add `fm stuck`, a redacted "where I got lost" bundle for the maintainer (Round 2)
- Wild: lend Foreman to a friend with `fm guest` (Round 2)
- Read a committed `.foreman/project.toml` for team-shared gates — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos… (Round 2)
- Generate a contributor onboarding pack for humans (`fm onboard`) (Round 2)
- Carry adoption in the repo so teammates get prompted to install (Round 2)
- Invite a teammate with one file (`fm invite` / `fm join`) — near T-0707 (done): Frontier 07 — Knowledge graph (Round 2)
- Wild: Write a maintainer handoff packet (Round 4)
- Wild: Diff the same task across two machines' ledgers — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Offer `fm init` automatically in the user's second repo with the same posture — near T-0694 (done): Milestone: Intelligence — Research and knowledge (Round 4)
- Wild: a portable "Foreman passport" file for dotfiles (Round 4)

## [skip] i18n-voice — Localization and voice: any-language intake/output, string catalogue, voice picks
value 2 · effort L · risk low · no evidence of demand
Exists: intake language handling (fmcore.py:1516); Claude answers in any language
Premise: false: no demand
Ideas (9):
- Accept requests in any language — near T-0688 (done): Milestone: Intelligence — Judgment, taste and decisions (Round 2)
- Understand requests and refusals in the user's language — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 2)
- Pick a voice at install — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Configure by saying it (Round 2)
- Speak the user's language — near T-0701 (done): Frontier 01 — Zero-token instrument layer (Round 2)
- Wild: write the dev diary into the user's notes vault (Round 2)
- Support non-English intake and output (Round 2)
- Route user-facing strings through one catalogue so output can be translated — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 2)
- Compose with the user's statusline and output style instead of replacing them — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)

## [skip] editor-ui-surfaces — Editor, web and protocol surfaces: IDE sidebars, web wizard, A2A/MCP, status
value 1 · effort L · risk med · off-strategy for a Claude Code plugin
Exists: fm page, statusline, sessionTitle
Premise: false: IDE sidebars and web wizards are other products
Ideas (7):
- Show where Foreman's effort goes — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics (Round 4)
- Show Foreman state in VS Code and JetBrains — near T-0713 (done): Frontier 13 — Intent, planning and change skills (Round 4)
- Run notebooks and data pipelines as evidence — near T-0414 (done): Guard: a data-reading python -c is judged by what runs befo… (Round 4)
- Wild: Draft the milestone write-up in the user's voice (ghostwriter) — near T-0697 (done): Milestone: Intelligence — Verification reasoning (Round 4)
- Ship a first-run wizard in the web UI — near T-0712 (done): Frontier 12 — Self-improvement flywheel (Round 4)
- Expose verify-as-a-service over A2A and MCP (Round 4)
- Add a thin editor sidebar for VS Code, Cursor and Windsurf (Round 4)
