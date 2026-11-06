# Brainstorm catalogue, half B: user value, unspoken needs, delight, bold bets, UI and motion

**Reading used.** I took all 250 bullets of rounds 1 to 4 in lenses 01, 02, 03, 08 and 09. Four titles occur twice (themes, ETA, gift task, trailer), plus a few near-duplicates. I counted every bullet, so the counts sum to 250.

**Earlier work I checked against.** The R and U clusters of `brainstorm-fm-code-catalogue.md`, and T-1328, T-1329, T-1330, T-1336, T-1343, T-1354. I could not map the T-1333..T-1361 ids to individual clusters, so I cite catalogue clusters (R7, U5 and so on) instead.

**Not read.** Neither research file (`claude-code-capabilities.md`, `anthropic-repos-integration.md`) was read, and I did not read the idea bodies (Why and Done when). Grounding rests on titles and the code. A title can hide a different premise.

Confidence is high where I cite `file:line`. Where I say "missing" it rests on a grep with no hit, so it is medium.

## Summary table

| id | capability | ideas | grounding | value | effort | risk | mark |
|---|---|---|---|---|---|---|---|
| B1 | Pin the six repos (lockfile, coverage, credit) | 10 | partial | 4 | M | med | build |
| B2 | Upstream change digest and arrivals | 8 | partial | 3 | S | low | build |
| B3 | Skills inside fm code (progressive load) | 9 | missing | 5 | L | med | build |
| B4 | Host Claude Code plugins on any runner | 3 | missing | 3 | L | high | skip (unsafe) |
| B5 | Drop-in `claude` flags and interop | 8 | partial | 4 | M | med | build (narrow) |
| B6 | Third-party asset gate (licence, quarantine, card) | 10 | partial | 4 | M | low | build (narrow) |
| B7 | SKILL.md spec lint, export, publish | 5 | partial | 3 | S | low | build (lint only) |
| B8 | Discovery, prior art, habit to skill | 12 | partial | 3 | M | low | skip (low value) |
| B9 | Cookbook patterns (`--pattern`, diagrams) | 10 | missing | 2 | L | med | skip (low value) |
| B10 | Prompt hardening and model exam | 11 | partial | 3 | M | low | build (narrow) |
| B11 | Small-model robustness (ladder, canary) | 8 | partial | 4 | M | low | build (ladder) |
| B12 | Finance vertical | 4 | missing | 2 | L | med | skip (out of scope) |
| B13 | Coverage and runner health | 7 | partial | 3 | S | low | build (narrow) |
| B14 | Cost, time and budget views | 8 | missing | 3 | M | low | skip (R11 covers) |
| B15 | Routing and multi-runner flow | 6 | partial | 3 | M | med | skip (R12, R22) |
| B16 | Standing mandate with bounds | 6 | partial | 5 | M | med | build |
| B17 | Overnight and ghost shift | 8 | partial | 4 | L | high | skip (U20 covers) |
| B18 | Steers, vetoes, intake honesty | 14 | partial | 4 | S | low | build (narrow) |
| B19 | Self-improvement measurement | 6 | partial | 3 | M | low | skip (done) |
| B20 | Site, README and demo honesty | 7 | partial | 3 | S | low | build (narrow) |
| B21 | Land, ship and close-out | 12 | partial | 4 | M | med | skip (U19, U8) |
| B22 | Home deck and guidance | 8 | partial | 4 | M | low | skip (U2, U3) |
| B23 | Request box | 6 | partial | 4 | M | low | skip (U4, U15) |
| B24 | Work with anything, edit safety | 10 | partial | 3 | S | low | build (narrow) |
| B25 | Liveness | 5 | done | 5 | S | low | skip (done) |
| B26 | Run-view discipline and motion | 9 | partial | 3 | M | low | skip (U6) |
| B27 | Run control (freeze, undo, ghost) | 5 | partial | 2 | M | med | skip (low value) |
| B28 | Render fidelity and evidence views | 9 | partial | 2 | M | low | skip (U12) |
| B29 | Power-user UI (menu, marks, chips) | 4 | missing | 2 | M | low | skip (low value) |
| B30 | Personality and delight | 9 | partial | 2 | S | low | skip (U13) |
| B31 | Run directory as the API | 5 | partial | 2 | M | low | skip (mostly done) |
| B32 | Reproducibility, sandbox and drills | 8 | partial | 2 | L | med | skip (low value) |

I have marked 13 clusters build and 19 skip.

## Clusters

### B1. Pin the six repos (10) — partial — build
- Ideas:
  - Adopt the six Anthropic repos into one pinned local catalog
  - Pin the six repos as an offline knowledge pack
  - Pin the six repos in an upstream lockfile that files its own work
  - Run the whole six-repo upstream as one `upstreams.lock` with a coverage ledger
  - Close the upstream loop with a kill-switched autopilot
  - Keep an adopt/skip/later register for upstream features
  - Fill a capability bingo card from the six repos
  - Wild: Print a licence-aware collectible sticker per source repo
  - Report which adopted upstream capability changed an outcome
  - Credit the upstream on every run that used it
- Evidence:
  - `plugin/lib/fmlib.py:482-487` DEFAULT_SOURCES has only `anthropics/skills` of the six.
  - `plugin/lib/fmlib.py:472-475` sources are shallow, markdown-only checkouts, indexed once per commit.
  - `plugin/lib/fmlib.py:531-539` `_license` reads the first line of the LICENSE file.
  - `plugin/lib/fmplugins.py:163-170` has a content-hash pin for plugins.
  - `plugin/THIRD_PARTY_LICENSES.md:5` says sources are indexed, not copied.
  - No lockfile and no coverage ledger exist.
- Build: add the other five repos as `fm lib source` entries, with a lockfile recording sha and licence per repo and a one-line coverage view. Skip the autopilot, bingo, sticker and outcome attribution; they are speculative.
- Done when: `fm lib source list --json` lists six sources, each with a sha and a licence, and `python3 -m unittest discover -s plugin/tests -p test_library.py` passes with a new lockfile test.

### B2. Upstream change digest and arrivals (8) — partial — build
- Ideas:
  - Show a personal "what changed upstream" digest
  - Wild: Run a nightly reading lane over upstream changelog entries
  - Render the upstream feed as a changelog stream with a pulse
  - Show new arrivals and renames on the home screen
  - Show the upstream as a "new arrivals" shelf
  - Wild: Open a "patch notes trailer" when Claude Code ships
  - Offer one weekly "adopt this?" decision card
  - Wild: Print a one-line "what you'd feel" delta at every release
- Evidence:
  - `plugin/lib/fmscout.py:153-154,172` probes the newest Claude Code release.
  - The same probe list has a `library gaps` probe (`fmscout.py:67`).
  - Scout captures into the inbox, bounded (`fmscout.py:1-6`).
  - Nothing diffs the pinned repos.
- Build: when B1's lockfile moves, a scout probe captures one brief listing new and renamed skills and agents. Skip the visual treatments.
- Done when: a test moves a fixture lockfile sha and `fm scout --json` returns one finding with a key of its own, captured once.

### B3. Skills inside fm code (9) — missing — build
- Ideas:
  - Run Agent Skills inside fm code on any model
  - Execute Agent Skills on any runner through a progressive-disclosure host
  - Load skills progressively for any runner
  - Show a context loadout screen for skills
  - Add a fitting room: try a skill on this run only
  - Wild: Run a skill straight from a URL and sha
  - Turn adopted upstream skills into a searchable index on the home screen
  - Map skill trigger overlap as a constellation
  - Unbox every adopted skill with a receipt card
- Evidence:
  - `grep skill` finds nothing in `fmcode.py`, `fmmodels.py` or `fmcodetui.py`.
  - Skill selection exists only for Claude Code sessions: `fmplugins.py:270-305` (`_skill_index`, `stage_skills`).
  - `fmlib.py` can search and show a skill's path as data.
  - The model's actions are fixed (`fmcode.py:12-24`, read, edit, write, run_cmd).
- Build: give the planner prompt a list of skill names and descriptions, and add a `skill` action that returns one SKILL.md body from `fm lib`. This is progressive disclosure with the guard unchanged, and the `fm lib` path stays read-only and treated as data. Skip the URL and sha form (unsafe), the constellation, the receipts and the fitting room.
- Done when: a unit test with a fake model that calls `{"action":"skill","name":"x"}` receives the body, the journal records the load, and an unknown name returns an error string.

### B4. Host Claude Code plugins on any runner (3) — missing — skip (unsafe)
- Ideas:
  - Run Claude Code plugins on any runner
  - Host Claude Code plugins inside fm code for any runner
  - Draw a hook pipeline rail with travelling signals
- Evidence: fm code applies Foreman's own guard in-process (`fmcode.py:447` `self.guard`). Running third-party hooks and MCP servers would run foreign code on the user's machine.
- Why skip: effort L, risk high. B3 covers the useful part (skill text). Revisit after B6 ships.

### B5. Drop-in `claude` flags and interop (8) — partial — build (narrow)
- Ideas:
  - Make `fm code` a drop-in for `claude` flags
  - Make `fm code` a drop-in `claude` binary
  - Make `fm code` a drop-in `claude` binary for the Agent SDK and IDEs
  - Wild: ship a fake `claude` binary so other tools run on any model
  - Let `fm code` read the user's existing Claude keybindings and slash commands
  - Wild: Hand a Claude Code session to `fm code` by saying "take this over"
  - Wild: Adopt a stalled live Claude Code session into fm code with one command
  - Show the feature-parity wall as a tile grid
- Evidence:
  - T-1343 already makes `fm code "<request>"` open the app on a terminal (`fmcli.py:5728`).
  - Flags are Foreman's own (`fmcli.py:5729-5760`); there is no `-p`, `-c` or `--output-format` alias.
  - Session handoff is catalogue U18, already briefed.
- Build: accept `-p/--print`, `-c/--continue` and `--output-format json` as aliases, mapped to `--plain`, `--resume` and `--json`. Skip the fake binary, keybinding import and parity wall.
- Done when: `fm code -p "x" --dry-plan` behaves like `fm code --plain "x" --dry-plan` (a test in `plugin/tests/test_cli.py`).

### B6. Third-party asset gate (10) — partial — build (narrow)
- Ideas:
  - Gate upstream imports by licence class
  - Trace a third-party plugin install in a throwaway HOME
  - Wild: Install official plugins in a trial lane first
  - Gate every imported asset with a quarantine stage and capability card
  - Unpack plugins on a quarantine stage before trust
  - Give every imported asset a licence and provenance glyph
  - Show a requirements card on every adopted plugin
  - Explain every denial from a third-party skill in the user's terms
  - Replay the whole plugin ecosystem through the guard and parsers
  - Turn the user's pasted rival-plugin/skill idea into a trial before adoption
- Evidence:
  - Quarantine already exists in effect. `fmlib.py:477-479` turns off hooks, LFS, symlinks and submodules.
  - Plugin install needs the user's yes under guard category `plugin` (`fmplugins.py:1-3`; `fmguard.py:4093`; `plugin/tests/test_guard.py:1431-1503`).
  - The pin hashes the code (`fmplugins.py:163`).
  - Licence is a free-text first line (`fmlib.py:531-539`), not a class.
  - `fm doctor --accept-supply` exists (`fmcli.py` flags) for supply drift.
- Build: classify each source's licence (permissive, copyleft, none, other) in `fm lib source list`, and show the requirements (hooks, MCP, commands) on `fm plugins find`. Skip the throwaway-HOME trace and the trial lane; the yes plus the pin already gate installs, and a trace is L.
- Done when: `fm lib source list --json` carries `license_class`, and `fm plugins find --json` shows `needs: [hooks, mcp]` for a fixture plugin.

### B7. SKILL.md spec lint, export, publish (5) — partial — build (lint only)
- Ideas:
  - Lint Foreman's own skills against the Agent Skills spec
  - Lint every SKILL.md against the Agent Skills spec at adopt time
  - Export Foreman's discipline as a spec-valid Agent Skills bundle (wild)
  - Wild: Publish Foreman's skills as a pinned, marketplace-schema-valid feed
  - Wild: Publish Foreman as a PR-ready plugin entry
  - Show a live spec meter while drafting a skill from a run
- Evidence:
  - `plugin/lib/fmdoctor.py:252-275` checks only name and description presence.
  - `fmdoctor.py:21` caps the SKILL.md body at 10000 chars.
  - The first two ideas are near-identical; the rest need an external spec I did not read.
- Build: tighten the doctor's frontmatter check (name pattern and length, description length), and reuse it in the `fm lib` index. Skip export, publish and the live meter.
- Done when: `fm doctor` fails a fixture skill with an over-long name and passes the shipped ones (`plugin/tests/test_doctor.py`).

### B8. Discovery, prior art, habit to skill (12) — partial — skip (low value)
- Ideas:
  - Recommend plugins from marketplace.json by the project's own stack
  - Wild: Recommend plugins from the user's own friction
  - Open a marketplace shelf for all six repos
  - Preview marketplace entries as real replays
  - Adopt before authoring when a habit repeats (wild)
  - Adopt before authoring: search the six repos when a habit repeats
  - Wild: hatch a draft skill from a repeated habit
  - Hatch a draft skill from a repeated habit (wild)
  - Wild: Offer "next to try" from the user's own history
  - Gate diffs on clean-room similarity to restricted sources
  - Wild: Port a feature from any repo, clean-room, with a licence gate
  - Look up prior art at intake before planning
- Evidence:
  - `fmplugins.py:197` `find` searches marketplaces.
  - `fmscout.py:67-79` is a stack-gap probe.
  - `fmrepeats.py:1-7` already proposes a project skill from repeated work (report-only).
  - `fmrecall.py` does BM25 prior art.
- Why skip: most of it exists, and the clean-room ideas are high-risk and unmeasured. Follow-up: `fm repeats` could print the top `fm lib` hit per candidate (S).

### B9. Cookbook patterns (10) — missing — skip (low value)
- Ideas:
  - Offer cookbook agent patterns as `fm code --pattern`
  - Offer cookbook agent shapes as `fm code --shape`
  - Draw the run as its named cookbook pattern
  - Draw each cookbook pattern as a live diagram of the run
  - Play a cookbook pattern as a named diagram of the run
  - Wild: swap cookbook patterns mid-run like cartridges
  - Swap cookbook patterns mid-run, like cartridges (wild)
  - Wild: Offer a cookbook recipe of the day as a guided run
  - Wild: Generate a cookbook-style notebook from any finished `fm code` run
  - Flip through a goal loop like a flipbook
- Evidence: no pattern flag (`fmcli.py:5729-5760`). The harness is one fixed plan, act, verify loop (`fmcode.py:1-24`). The premise that cookbook patterns map onto it is unverified (I did not read the research).
- Why skip: effort L with no demonstrated need. The harness's fixed loop is the product.

### B10. Prompt hardening and model exam (11) — partial — build (narrow)
- Ideas:
  - Harden slot prompts with the tutorial's techniques, measured
  - Add an unknown escape and evidence quote to every slot prompt
  - Run a prompt-sensitivity exam on each runner
  - Lint Foreman's own prompts against the tutorial's rules
  - Turn cookbook notebooks and the prompt tutorial into a model exam that tunes slot prompts
  - Import cookbook eval patterns as bench cases
  - Mine the cookbook's eval notebooks into bench cases
  - Grade models on a prompt-engineering dojo
  - Wild: Give local models cookbook homework while idle
  - Wild: Grade the user's own prompts with a prompt dojo
  - Tint the request box by prompt-craft
- Evidence:
  - Slot prompts are `fmcode.py:140-175`.
  - `fm code bench` grades on seeded tasks in throwaway repos (`fmcodebench.py:1-6`).
  - `fm bench` also exists (`fmbench.py`).
  - Nothing measures prompt variants.
- Build: put a prompt variant (the "unknown" escape and an evidence quote) behind a flag, and measure it with `fm code bench` on the existing seeds. Keep it only if closed seeds do not drop. Skip the dojos, homework and tinting.
- Done when: `fm code bench --model <fake> --seeds a,b --json` reports closed counts for both prompt variants, and a unit test pins the variant text.

### B11. Small-model robustness (8) — partial — build (ladder)
- Ideas:
  - Climb a slot-format ladder when a model fails a slot
  - Escalate slots on logprob entropy
  - Wild: make weak models explain themselves in smaller questions
  - Wild: Slip a known-answer canary slot at the start of each run to detect a swapped or degraded model
  - Rerun a red canary after the machine goes quiet before showing it
  - Pin each runner's privileges to a promotion curve
  - Wild: Make weak models earn privilege through a promotion curve and an injection exam
  - Wild: shade model prose by token confidence
- Evidence:
  - Slots repair by quoting the error back, at most REPAIRS times (`fmcode.py:212-232`).
  - A model with tools gets tool calls, otherwise a JSON object in its text (`fmcode.py:12`).
  - There is no logprob handling in `fmmodels.py`.
  - `fm canary` (`fmeco.py:1-4`) checks Foreman against a new Claude Code, not a model.
  - The bench's canary file is a safety seed (`fmcodebench.py:4`).
- Build: when repairs fail, try the next format step (tool call, then JSON in text, then one field per question) before escalating. Skip the logprob, canary, promotion-curve and confidence-shading ideas; they need provider support or are speculative. The "red canary" idea concerns `fm canary` and is a separate S fix.
- Done when: a fake model that fails JSON twice but answers single-field questions closes a test run (`plugin/tests/test_code.py`, or the equivalent that holds the fmcode tests).

### B12. Finance vertical (4) — missing — skip (out of scope)
- Ideas:
  - Wild: Add a numeric tie-out evidence kind for finance-style work
  - Wild: Pick up the finance vertical when the repo isn't code
  - Greet finance projects with a vertical ribbon
  - Adopt a vertical pack as a themed workspace skin
- Evidence: nothing in `plugin/lib` is domain-specific. Brainstormers rated the finance one value 2.
- Why skip: B3 makes finance skills loadable if they are indexed.

### B13. Coverage and runner health (7) — partial — build (narrow)
- Ideas:
  - Measure "work with anything" with a request-kind coverage matrix
  - Wild: dry-run the "anything" sampler on stranger-domain requests invented by a child
  - Watch for retired model IDs in `models.json` and propose the swap
  - Record each runner's automation terms and warn before parallel overnight work
  - Draw the runner wiring diagram with a preflight pulse
  - Wild: Run a weekly "guest runner" low-risk task
  - Show the model's slot, not just the step
- Evidence:
  - `fm code runners` and `--check` exist (T-1328; `fmcode.py:1620-1680`; `fmcli.py:5745-5748`).
  - Preflight is catalogue R5.
  - Nothing checks model IDs against a retired list.
- Build: `fm code runners --check` flags a configured model ID that is on a small, dated retired list. Skip the coverage matrix and the child-invented sampler (L, unverifiable), and the diagrams.
- Done when: a test with a `models.json` fixture naming a retired id makes `fm code runners --check --json` report `retired: true`.

### B14. Cost, time and budget views (8) — missing — skip (R11 covers)
- Ideas:
  - Show a plan wallet across subscriptions and keys
  - Report attention minutes against a manual estimate
  - Run a metered dollar auction among runners per step
  - Wild: Show the time and money box as a sundial
  - Wild: add pressure mode for deadline and spend boxes
  - Show an ETA by analogy
  - Show an ETA by analogy
  - Wild: Fuzzy money units for budgets
- Evidence: there are no cost or budget references in `fmcode.py`. `fm run` has `--max-usd` (`fmserve.py:772`) and `fm budget` and `fm cost` exist (`fmbudget.py`, `fmcost.py`).
- Why skip: this is catalogue R11 (slate #12), already briefed. Do not re-brief.

### B15. Routing and multi-runner flow (6) — partial — skip (R12, R22)
- Ideas:
  - Retry a rejected run on a different runner with the rejection as a hard constraint
  - Draw handoffs and fallbacks as a baton path
  - Show one process table across every runner
  - Collapse six nouns into one run table
  - Wild: Say a sentence, Foreman picks project, runner and ceremony
  - Run a duel only where it shows a loss, then adopt
- Evidence: `fm run --failover` (`fmserve.py:302-316,869`); runner default resolution (`fmcode.py:891-911`); `fm lane race` exists (`fmlanes.py:351`).
- Why skip: R10, R12 and R22 already cover these.

### B16. Standing mandate with bounds (6) — partial — build
- Ideas:
  - Close sweeping mandates with a per-clause ledger
  - Write one `mandate.toml` per sweeping request
  - Hold the user's "etc." as a standing, bounded mandate
  - Close the loop on "super recursive" with a bounded mandate file and convergence stop
  - Wild: Make mandates expire into a decision card, not silence
  - Lint workflow graphs for termination and budget bounds
- Evidence:
  - The per-clause ledger is done: `fmrecall.py:387-426` (`fm clauses`) and `fmcli.py:4487-4489`.
  - Bounds exist: `fmcontract.py:1-3` (time and spend limits).
  - Autonomy and standing yeses exist (`fmcli.py:2994-3010`).
  - `fmnight.py:149` runs standing orders.
  - A file that ties one sweeping request to its bounds, expiry and convergence stop is missing.
- Build: a project mandate record (text, clauses from `fm clauses`, `fm contract` bounds, expiry date). `fm night` and `fm scout` read it, and on expiry the mandate becomes one decision in the inbox. Reuse the contract and clause code; no new engine.
- Done when: a test creates a mandate with a past expiry, and `fm night --dry` (or `fm scout --json`) emits one decision card and stops capturing.

### B17. Overnight and ghost shift (8) — partial — skip (U20 covers)
- Ideas:
  - Wild: Add "ghost shift" `fm code --tonight`
  - Wild: Ship a "ghost shift" that spends idle hours on a speculative queue
  - Wild: Turn the user's idle hours into a speculative queue
  - Schedule runs as resumable quanta
  - Schedule around presence and calendar (wild)
  - Sample-audit the unattended output
  - A morning-after page the user can tick, and Foreman acts on the ticks
  - Wild: Hand the user a morning quiz of three things Foreman built while they slept
- Evidence: `fmnight.py`, `fmdraft.py:1-4` (drafts the top S task on a branch, never merged), `fmaway.py` (return summary), `fmcontract.py`.
- Why skip: catalogue U20 and R17 cover unattended fm code. Rated risk high.

### B18. Steers, vetoes, intake honesty (14) — partial — build (narrow)
- Ideas:
  - Show a "your words, my reading" diff when a recorded steer changes behaviour
  - Echo every recorded veto with a one-key retract
  - Answer rhetorical complaints, then queue the fix
  - Keep a polarity corpus of the user's own phrasings
  - Name what Foreman won't repeat: a "you already told me" register at intake
  - Tag every user message by why it was needed
  - Tag a fix with "because you said" the first time you hit it
  - Thread the request's words to the criteria they became
  - Wild: print the user's own rules as marginalia next to the thing they constrain
  - Offer a counter-proposal when a request can't be done
  - Run a trial slice first, then ask go or no-go
  - Send brainstorm children only the user's last 30 steers plus a capability gap list
  - Mirror the user's typing register
  - Wild: write the future README first and let its failing fences be the queue
- Evidence:
  - The "already told me" register is mostly done: `fmcli.py:280` (T-0438, a dropped or vetoed request is said at capture).
  - `cmd_vetoes` and `fm taste` exist (`fmideas.py`).
  - Standing steers become rule candidates (`fmcli.py:1818-1821`).
  - `fm second` gives a second read.
  - `fmcode.py` has `--dry-plan`.
- Build: `fm vetoes` prints the retract command for each veto it records (verify the current output first). Skip tagging, the polarity corpus, marginalia, trial slice and typing mirror; they are speculative and cost model calls.
- Done when: `fm vetoes --json` lists each veto with a `retract` command that removes it, and a test round-trips it.

### B19. Self-improvement measurement (6) — partial — skip (done)
- Ideas:
  - Back-test the auto-notice trigger on whether its rounds were wanted
  - Rank each shipped round-1 slate item by what the user did next
  - Make "10x better" measurable: a user-owned scorecard of their own axes
  - Answer "what did I get for the time I spent?" with a weekly outcome ledger
  - Close each recursive round with a three-line "what changed for you"
  - Close each round with a decision card, not a report
- Evidence: `fmoutcomes.py:1-3`, `fmtrials.py:1-3` (a pre-registered metric per self-change), `fmfriction.py:1-4`, `fmbacktest.py`, a `scorecard` command (`fmcli.py`), `fm digest` (`fmcost.py`).
- Why skip: the machinery exists. The user-owned axes are an opinion call, not code.

### B20. Site, README and demo honesty (7) — partial — build (narrow)
- Ideas:
  - A feature without a runnable demo doesn't close
  - Bind each claim in the site and README to a rerunnable check with an expiry
  - Fail the site build on any third-party request
  - Wild: Run a nightly "new user, old repo" rehearsal of the headline demo
  - Wild: Reverse demo from a typescript of the user's own claude session
  - Stage the landing hero as a scroll-scrubbed replay
  - Make recorded SVG casts re-skin with CSS variables
- Evidence:
  - The premise holds, and it is a live defect: `site/build.py:196-198` loads Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`) from the built page.
  - `fmdemo.py:1-4` is a model-free demo.
  - Stats are in `site/stats.py`.
- Build: `site/build.py` fails on any third-party host except the repo's own links. This means self-hosting the fonts (or dropping them) first.
- Done when: `python3 site/build.py` exits non-zero on a fixture page with `https://fonts.googleapis.com`, and zero on the real build.

### B21. Land, ship and close-out (12) — partial — skip (U19, U8)
- Ideas:
  - Land everything proved, across all projects, in one pass
  - Finish the job for the user: one-key land of a proved run
  - Give each finished run a live preview until accepted
  - Close deploy tasks only when the live URL answers
  - Add a pre-receive git remote that only accepts proved pushes
  - Wild: Mirror the repo to a user-owned second remote with a divergence alarm
  - Turn the 11 externally blocked briefs into one page of paste-ready steps
  - Wild: Let the user's accepted wording stand as the spec for the next release notes
  - Pre-fill the release sentence in the user's style
  - Close every run with a "what you can say to a friend" line
  - Show "the line that fixed it" on FIX receipts
  - End failed runs with a fail-forward card
- Evidence: `fmlanes.py:77-89` (`lane merge`), `fmpr.py:1-4` (`pr train`), `fmrelease.py:1-6`, and fm code's `--no-commit` (`fmcode.py:3`). Catalogue U8 and U19 cover close-out and proved-to-shipped.
- Why skip: the earlier round already briefed it. Follow-up (S): the "11 blocked briefs on one page" idea uses `fm queue` and is separate.

### B22. Home deck and guidance (8) — partial — skip (U2, U3)
- Ideas:
  - Rank "what needs me" across all projects on the home screen
  - Offer a "what should I do next?" answer on bare `fm code`
  - Replace the home screen with a project deck that morphs into the run
  - Wild: sweep a lighthouse beam across the home deck
  - Wild: make the home deck an orrery
  - Leave an afterimage on the last-touched element when switching views
  - Small-multiples run history on one time axis
  - Build one data-grid component for every table
- Evidence: `fmcodetui.py:1459-1485` (home sorted by missing-folder-last then newest first; the project view lists active, queue, inbox, blocked and past runs; T-1330). Ranking by need and the visual treatments are U2 and U3.
- Why skip: already briefed.

### B23. Request box (6) — partial — skip (U4, U15)
- Ideas:
  - Tab-complete the request from repo signals
  - Paste anything into the request box
  - Keep a draft shelf for half-typed requests
  - Remember half-typed requests in a draft shelf
  - Never lock the request box: type to steer
  - Warm the runner on the first keystroke
- Evidence:
  - `fmcodetui.py:1371-1386` is a plain text line. There are no drafts, and Esc discards the text.
  - `fmcodetui.py:1396-1400` blocks "new" during a run ("a run is going: s stops it").
  - U4 and U15 are briefed.
- Why skip: already briefed.

### B24. Work with anything, edit safety (10) — partial — build (narrow)
- Ideas:
  - Verify advice pasted from other chatbots
  - Mine exported chat history for abandoned plans
  - Explain unfamiliar stacks by analogy to the user's own
  - Localize the user's own project
  - Keep a living architecture diagram for any project
  - Wild: Offer a "rubber-duck runner" that only asks questions
  - Preserve bytes the model didn't mean to change
  - Edit JSON, TOML and YAML by key without reformatting the file
  - Fuzz every path-taking option with option-shaped values
  - Block close on stray top-level paths the plan never named
- Evidence:
  - `fmedit.py:94,109` keeps CRLF as CRLF in `fm edit`.
  - fm code's `write()` rewrites whole files as UTF-8 text (`fmcode.py:456-466`) and reads through text paths.
  - `fmmap.py` has `map` and `tour`.
  - The rest are new ideas.
- Build: one hygiene brief. (1) `write()` preserves the existing line-ending style, and refuses a non-UTF-8 target instead of rewriting it. (2) A test feeds option-shaped values (`--x`, `-`) to path options in `fmcli.py`. Skip the new-capability ideas.
- Done when: a test where the model writes LF text over a CRLF file leaves it CRLF, and one over a binary file returns a refusal.

### B25. Liveness (5) — done — skip
- Ideas:
  - Show "it's alive" evidence in the first 10 seconds of any run
  - Fire a "first sign of life" within 10 seconds, with a named wait
  - Add `fm code why` as a one-screen answer, then make it the stall card
  - Add an intermission screen on rate limits
  - Show an intermission screen on a rate limit
- Evidence:
  - T-1329 (live progress) and T-1336 (stall): `fmcode.py:107` (event `stalled` with cause launch|prompt|limit|silent), `fmcode.py:578-593`, `fmcodetui.py:115,259,796`.
  - `fmcode.py:732` has a `_LIMITED` regex for rate limits.
  - Not done: a first sign inside 10 seconds for a model-run (not CLI) turn, and a separate intermission screen. The stall card covers most of it.
- Why skip: catalogue R6, R7 and U5.

### B26. Run-view discipline and motion (9) — partial — skip (U6)
- Ideas:
  - Subtitle every moving thing on demand
  - Say why the look is degraded
  - Add minimum-dwell and hysteresis to status changes
  - Encode progress certainty in texture
  - Define a three-level interruption ladder
  - Give relative times a tick-stable grammar
  - Wild: add a tape-counter footer
  - Virtualise long transcripts with scroll anchoring
  - Gate key-to-paint feel against claude
- Evidence: motion modes full, reduced and off (`fmcodetui.py:97,1309-1318`). NO_COLOR drops to the mono theme (`fmcodetui.py:1997`). Scrolling is by line slice (`fmcodetui.py:992,1091`).
- Why skip: U6 is briefed, and these are polish. The key-to-paint gate is M with risk; defer it until a user reports lag.

### B27. Run control (5) — partial — skip (low value)
- Ideas:
  - Freeze the run with one key
  - Replay the last 15 seconds on demand
  - Play undo backwards
  - Make one-way doors feel heavy
  - Wild: show a ghost of the next action with a one-second veto
- Evidence:
  - `fmcodetui.py:1427-1433` `stop` sends SIGTERM and `r` resumes from the journal.
  - Replay of whole runs exists (`fmcodetui.py:1550`, T-1283).
  - There is no SIGSTOP freeze. Freezing a process that holds model sockets is fragile.
- Why skip: stop and resume already give the same control.

### B28. Render fidelity and evidence views (9) — partial — skip (U12)
- Ideas:
  - Remap worker ANSI colours onto theme roles
  - Fold stack traces by ownership
  - Highlight diff syntax with a stdlib-only lexer table
  - Make Foreman's own chrome unforgeable
  - Draw a files × judges verdict matrix
  - Map read versus write footprint
  - Show a keyring of live grants with expiring rings
  - Wild: Render a run as sheet music
  - Wild: Blur the transcript by what the harness never verified
- Evidence: four theme presets (`fmcodetui.py:72-73`), control characters stripped (`fmcodetui.py:1989`), a diff view (`fmcodetui.py:1441-1446`).
- Why skip: catalogue U12 was already skipped as low value. One real item: unforgeable chrome has a security angle, since worker output could paint fake status; the control-character strip may cover it.

### B29. Power-user UI (4) — missing — skip (low value)
- Ideas:
  - Open an action menu on any object
  - Mark several items and act as a batch
  - Pin any value as a watch chip
  - Run the docs inside the TUI
- Evidence: the keys are a flat map (`fmcodetui.py:84-87`), with a help view (`fmcodetui.py:1071`). There is no menu, marking or pinning.
- Why skip: the app has few objects, and U7 covers key discoverability.

### B30. Personality and delight (9) — partial — skip (U13)
- Ideas:
  - Unlock themes from real milestones
  - Unlock themes from real milestones
  - Coach on friction, not on a timer
  - Wild: Pay back Foreman's mistakes with a gift task
  - Wild: a "gift task" after Foreman's own mistakes
  - Wild: Let a failed check show a replay of its own near-miss
  - Play a trailer in an empty project
  - Wild: print a trailer in an empty project
  - Mirror the user's typing register (dedupe note: this title also sits in B18's list; it counts once there, so ignore it here)
- Evidence: themes are in `fmcodetui.py:31-74`. `fm demo` is the existing trailer (`fmdemo.py:1-4`).
- Why skip: low value and speculative. U13 covers delight.

*Correction for the main thread:* "Mirror the user's typing register" belongs to B18 only. B30 is therefore 8 ideas and B18 stays 14, so the total is still 250 (the table's B30 count of 9 includes it; subtract 1 and the sum is 249). I could not reconcile the last bullet. Please recount the three counts that are my likeliest slips: B5 (8), B26 (9), B11 (8).

### B31. Run directory as the API (5) — partial — skip (mostly done)
- Ideas:
  - Make the run a plain file cockpit
  - Make the run directory the entire API
  - Open a universal human port for every agent
  - Let workers call back into Foreman mid-step
  - Record a context manifest per call
- Evidence: the journal is `code/<task>.jsonl`, the events are `code/<task>.events.jsonl`, and the stream schema is versioned (`fmcode.py:24,89,255-261`). Agent sessions are logged as `events.jsonl` (`fmsession.py:7`).
- Why skip: the premise is largely true already. Worker callbacks would loosen the guard; skip.

### B32. Reproducibility, sandbox and drills (8) — partial — skip (low value)
- Ideas:
  - Share a substituter cache for agent work
  - Compile each step's plan scope into a throwaway sandbox profile
  - Run a daily brownout drill on Foreman itself
  - Wild: Mirror every plan in a sabotaged universe
  - Wild: Export a proof as a self-checking bundle
  - Reproduce a run bit for bit from a one-file bundle
  - Run the whole harness under a deterministic simulator
  - Version behaviour bundles like packages and upgrade them only on a replay win
- Evidence: `fm sandbox` exists (`fmserve.py`, `cmd_sandbox`). `fmledger.py:1-4` has the hash chain and `fm verify-ledger`. `fmreplay.py` and `fmbacktest.py` replay sessions. Catalogue R25 covers the harness simulator.
- Why skip: L effort with little user-visible gain.

## Risks / surprises
- **Count mismatch.** My cluster counts sum to 249, not 250, by my recount. The B30 note above flags one miss. Please re-run the exactly-once check against `ideas.md`. I could not run a script (read-only tools).
- **Site loads Google Fonts** (`site/build.py:196-198`). This contradicts a privacy-first, nothing-leaves-the-machine stance and is a real defect behind B20.
- **fm code has no cost or budget path at all** (no hit in `fmcode.py`). That is catalogue R11 and is not yet built.
- **Only `anthropics/skills` of the six repos is a source.** The claude-code repo, cookbooks, plugins-official, financial-services and the tutorial are not indexed; the indexer takes only SKILL.md and agent markdown (`fmlib.py:504-528`).

## Not checked
- Both research files, and the idea bodies.
- fm code's test files (names of the real fmcode tests are a guess in B11).
- The exact subcommands of `fm lib source`, and whether `fm vetoes` already prints a retract.
- `plugin/commands`, `skills` and `hooks` content.
- Which T-13xx id covers which earlier cluster.

Noticed: `plugin/lib/fmcode.py:456-466` `write()` opens with text mode and no line-ending handling, unlike `fmedit.py:94,109` (B24 covers it).
Noticed: `site/build.py:196-198` pulls Google Fonts, against the project's stance that nothing leaves the machine (B20 covers it).
Noticed: `plugin/lib/fmlib.py:531-539` reports a licence as the file's first line, not a class (B6 covers it).
Noticed: `plugin/lib/fmcodetui.py:1396-1400` refuses a new request mid-run, which blocks any type-ahead (U15 already covers it).
