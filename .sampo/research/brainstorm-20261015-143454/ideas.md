# Ideas by round (deduplicated titles; details in the lens files; "near T-…" names a finished task that shares most of an idea's words)

## Round 1
- Sample hook latency from real turns, not only bench — near T-0805 (done): The hook benchmark judges by CPU time when the machine is b…
- Short-circuit every hook on a one-stat "is this a Foreman project" check before importing Python modules — near T-0713 (done): Frontier 13 — Intent, planning and change skills
- Budget `fm` verb cold-start with a per-verb import-time table in CI — near T-0677 (done): Milestone: Features — Planning, briefs and queue
- Make the test suite itself fast: affected-first with a content-hash result cache — near T-0680 (done): Milestone: Features — Self-improvement and learning
- Time-box and incrementalise `fm map` on large repos — near T-0707 (done): Frontier 07 — Knowledge graph
- Run recording-only hooks fire-and-forget — near T-0712 (done): Frontier 12 — Self-improvement flywheel
- Cap per-turn injected context by token count and print the bill — near T-0680 (done): Milestone: Features — Self-improvement and learning
- Speed up git calls with a single porcelain snapshot per hook turn — near T-0712 (done): Frontier 12 — Self-improvement flywheel
- Wild: Warm resident hook server with a thin shell shim, auto-fallback to cold Python
- Wild: Predict-and-prefetch the next gate while the model is still typing the edit — near T-0710 (done): Frontier 10 — Milestone work compiler and merge train
- Wild: Warm hot-spare headless child for brainstorm and review fan-out
- Make one Foreman install the only install — near T-0874 (done): Marketplace install works and is documented: /plugin market…
- Derive every version string from one tag — near T-0696 (done): Milestone: Intelligence — Understanding the request and the…
- Stop committing demo recordings and build them as release assets — near T-0677 (done): Milestone: Features — Planning, briefs and queue
- Generate test fixture repos from compact specs — near T-0713 (done): Frontier 13 — Intent, planning and change skills
- Write only non-default settings to the settings file — near T-0679 (done): Milestone: Features — Resilience, state and simplicity
- Move the root clutter under `docs/` and keep the root to README, install and license — near T-0701 (done): Frontier 01 — Zero-token instrument layer
- Give installer and `fm` prompts one non-interactive contract — near T-0697 (done): Milestone: Intelligence — Verification reasoning
- Mark unverified adapters unsupported and hide them from help and doctor
- Add a surface-delta trailer to every commit — near T-0707 (done): Frontier 07 — Knowledge graph
- Enforce a two-minute rule: every verb must appear in the scripted tour or be labelled labs — near T-0712 (done): Frontier 12 — Self-improvement flywheel
- Cap the generated product page at one printed page — near T-0712 (done): Frontier 12 — Self-improvement flywheel

## Round 2
- Bound the cost of work snapshots — near T-0703 (done): Frontier 03 — Model routing, effort and cache economics
- Make mutation proof stop at the first kill — near T-0708 (done): Frontier 08 — Orchestrator control plane
- Prove on a sparse worktree — near T-0898 (done): Fm at REF|ID -- CMD runs a command as of a commit or a task…
- Key the pyc cache by tree hash instead of deleting it
- Make tidy backups incremental — near T-0922 (done): fm tidy --apply keeps dated backups of the project's state …
- Cache per-project summaries for `fm projects --next` and `fm tour --since` — near T-0263 (done): Handoff: diff tour, proof sections in fm pr, AGENTS.md expo…
- Give bare `fm` and `fm complete` a latency budget
- Nudge whole-file Writes that change under 10% of a file — near T-0713 (done): Frontier 13 — Intent, planning and change skills
- Shape unbounded Grep and Glob calls — near T-0713 (done): Frontier 13 — Intent, planning and change skills
- Skip `fm doctor` checks whose inputs haven't changed — near T-0705 (done): Frontier 05 — Ambient verification and test intelligence
- Wild: add a tmpfs hot tier for volatile state
- Wild: bench hooks with a cold page cache — near T-0712 (done): Frontier 12 — Self-improvement flywheel
- Wild: pick the pane's motion level from measured frame lag
- Merge lessons, vetoes, decisions and preferences into one standing-rule store — near T-0696 (done): Milestone: Intelligence — Understanding the request and the…
- Collapse every escape-hatch flag into one `--because "<reason>"` waiver
- Fail CI when a tracked file holds local paths or a derived cache — near T-0677 (done): Milestone: Features — Planning, briefs and queue
- Toggle features by file existence under `.foreman/off/` — near T-0889 (done): Fm why FILE:LINE quotes the user's original request from th…
- Ratchet the lib file count and inline single-caller modules
- Make healthy turns add zero bytes, enforced by a golden test — near T-0712 (done): Frontier 12 — Self-improvement flywheel
- Raise a state-version floor and delete old readers
- Wild: have the Claude Code release differ open deletion tasks, not only integration tasks — near T-0709 (done): Frontier 09 — Orchestrators of orchestrators
- Wild: generate a 30-minute reading-order tour and treat unreachable files as delete candidates — near T-0885 (done): Rank a finished task's or a day's changes by review risk, w…
- Wild: distil a minimal verb path from the bench winners

## New ideas per lens
- performance: 24
- simplicity: 21

## Coverage (ideas per category)
- gate speed 4
- hook latency 2
- startup 2
- git speed 2
- config 2
- scale 1
- tokens 1
- stability 1
- install 1
- release 1
- repo weight 1
- test weight 1
- repo layout 1
- scripting 1
- scope 1
- storage 1
- fan-out verbs 1
- cli latency 1
- output tokens 1
- input tokens 1
- diagnostics 1
- state io 1
- cold start 1
- ui cost 1
- state 1
- cli surface 1
- repo hygiene 1
- codebase size 1
- silence 1
- migrations 1
- native overlap 1
- legibility 1
- surface 1
Thin (0-1 ideas): user value, reliability, performance, security, privacy, ui, devices, agents, simplicity, developer experience, observability, docs, delight
