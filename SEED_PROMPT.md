super improve Foreman into the harness that can do anything on its own, and seed yourself to get there. After this message I'm not going to say anything else.

RESEARCH!: Genesis. Build Foreman into a self-directing agentic harness: it finds, thinks through, and does anything on its own
CONTEXT: The goal is Foreman's own abilities, not work in other people's repos. In any repo, on any task, or with no task at all, Foreman should: find what needs doing without being asked; think through every interpretation, approach, outcome, failure mode and fix before choosing; get or build whatever tool it's missing; do the work end to end; prove it; and know when it's truly done. Section 2 is the spec. The run builds all of it, completely.
CONTEXT: This message is Generation 0. It writes a Seed. The Seed writes one Mission per capability gap. Missions write and build the briefs, then critique and rewrite the Seed for the next generation. I never write another prompt.
CONTEXT: Foreman already has most of the parts: fm mission, fm ideas, fm research ask, fm scout, fm orders, fm night, fm run, fm graph blast, fm second, fm lane (--spike, race), fm evolve, fm bench, fm backtest, fm trials, fm mcp new, fm plugins find, fm shot/flow, fm loop, fm mandate. Extend them and build what's missing. Don't rebuild what exists.
CONTEXT: Recent rounds mostly shaved hook milliseconds and followed up the last ship. This run works from the capability spec, not from the last diff.
MUST: full autonomy. Every decision through fm decide. Never ask me anything mid-run.
MUST: no spend cap on building and proving. Tokens go into Foreman's code and its tests, not into sweeping the outside world. Waiting out a usage limit is fine.
MUST: everything finishes completely. A capability is done only when it has its tests, its exam scenarios passing (§4), docs (MASTER.md, README where it belongs, CHANGELOG), a site page if it's user-facing, a pane/status surface if it has state, and it works on every surface it belongs on (Claude Code, fm code, other agents, Desktop).
MUST: unprompted actions stay local and reversible (a lane, a branch, a spike, a throwaway folder). Anything that leaves the machine needs its grant, so it goes into the final report.
NEVER: clone or sweep outside repos to brainstorm or to benchmark. Outside material is only allowed in the targeted form in §5.
NEVER: grant yourself anything or lower your own guard. Protected core gets a built, evaluated candidate in a worktree plus `fm ask ID core` at the end. Merging Foreman changes stays my call.
DONE-WHEN: every capability in §2 passes its held-out exam (including #13: Foreman can run this kind of Genesis by itself from no prompt), the completeness sweep (§7) is clean, and two generations in a row find no remaining tier 3–4 gap. It ends with one report.

---

## 0. Set up

```
fm autonomy full
fm drive on
fm loop on
fm contract off
fm lane max 6
fm mandate set "Genesis: build Foreman into a self-directing harness per research/genesis/gen-0.md §2" --until <YYYY-MM-DD>
```
Capture this message as the Genesis task, save it verbatim as `research/genesis/gen-0.md` (never edited), and record the setup with `fm decide`.

## 1. Gap map first (generation 1 only, no brainstorm yet)

For each capability in §2, map what Foreman already has with file and verb evidence, what's partial, and what's missing, using `foreman:fm-recon` per capability in parallel. Save it as `research/genesis/gap-map.md`. Every later idea is checked against it. Nothing gets built twice.

## 2. The capability spec: what "can do anything on its own" means

Each item has a test. A capability counts only when its exam scenarios pass (§4).

1. **Initiative.** In any repo with no request: map it, find the real bugs, security holes, missing or failing tests, slow paths, rotten deps, docs drift, CI flakes, open issues and missing features, rank them by value, prove each one (repro or failing test), and fix them on lanes. Language-agnostic. Grows `fm scout` from watching Foreman into watching any project.
2. **Exhaustive thinking.** Before acting on anything non-trivial: list the readings of the request, every approach (including "use what exists" and "do less"), the likely outcomes and failure modes of each, edge cases, and blast radius (`fm graph blast`). Then generate several candidate fixes or designs, test them in parallel lanes, and choose by evidence, not first instinct. Scale the depth to the risk, so an S task doesn't pay an L task's cost.
3. **Anticipation.** A model of me, my projects and my machines (requests, corrections, habits, what breaks). It predicts the next request and drafts it on spec in a lane, and flags problems before they happen (grow `fmforesight`).
4. **Goal to finish.** Turn a vague goal into a complete plan: what a finished, best-in-class version contains, decomposed and ordered. It carries the plan over days, across crashes and compactions, and knows when it's actually done rather than merely stopped.
5. **Getting the tools it lacks.** When it hits something it can't do, it finds an existing plugin, skill or MCP server (`fm plugins find`, `fm lib search`) or builds one (`fm mcp new`, a script, a project skill), tests it, and uses it. Install grants are queued for me, never self-granted.
6. **Verifying anything.** Proof beyond unit tests: UI (`fm shot`, `fm flow`), data, docs against code, infra and ops, performance, and "does it do what the user meant". Whatever can't be proven gets labelled as unproven.
7. **Self-repair and self-improvement.** Its own failures, friction, misses and my corrections become fixes, gated by bench and trials, without being asked.
8. **Calibrated judgment.** It knows what it doesn't know: it states confidence, researches when unsure, and stops for me only when something is irreversible and ambiguous. Everything else it decides and records.
9. **Orchestration.** It spawns, briefs, checks and merges its own subagents and lanes, picks the cheapest model that can do each part, and recovers stopped ones.
10. **Beyond code.** Research, docs, ops and incidents, infra, data, design and releases, done to the same standard of proof.
11. **Self-triggering.** Schedules, file and event triggers, CI and issue watchers, so work starts without me. Installs (timers, units) get queued for one yes.
12. **Staying lean and safe.** Each of the above keeps the hooks fast, keeps context small and keeps the guard intact (see §6).
13. **Genesis as a feature.** Turn this whole tower into something Foreman ships and runs on its own, so nobody ever has to hand-write a prompt like this again. That means:
    - **One entry point** (a verb such as `fm genesis` plus a skill) that writes its own gen-0. It writes it from whatever it's given: one line like "make this great", a sweeping request, or nothing at all. It draws on the project, my history and corrections, and the gap map, then runs the tower (Seed → Missions → briefs → critique → selection → drift check → completeness sweep) in any project, not just Foreman.
    - **It starts by itself.** Routing sends open-ended or sweeping requests to it. The forever loop and `fm scout` start it when a project's queue runs dry or its gap map shows big gaps. The routing change to rules/foreman.md is protected core, so it gets queued for my yes.
    - **It gets a spec of its own.** For any project it writes that project's version of §2: what "complete and best-in-class" means for that kind of project, with the same held-out exam approach.
    - **It carries over.** What this run learned (the winning Seed and mission templates, the lenses that paid off, the lineage) becomes its starting defaults.
    - **Exam:** given only "make this great", or no request at all, on held-out generated projects, its self-written gen-0 has to cover at least everything this hand-written one does (every MUST, NEVER and section). The tower it runs has to close the planted gaps. From generation 2 on, this run's own Seed is written by the feature, not by this message.

## 3. The tower (each generation)

| Level | Written by | File |
|---|---|---|
| L0 Genesis | me | `gen-0.md` (fixed) |
| L1 Seed | gen 1: Genesis plus the gap map; later: the last generation's critiques | `gen-N/seed.md`: which gaps this generation closes, lenses, order |
| L2 Missions | the Seed, ≤ 8, one per gap | `gen-N/mission-<capability>.md`: a self-contained prompt a fresh `fm run` session can execute |
| L3 Briefs | each Mission | `fm intake` blocks, grounded, tiered, built |

1. The Seed picks the biggest open gaps from the gap map and the exam results. Capability #13 goes in generation 1 (a first working version), so the rest of the run uses it on itself.
2. Each Mission runs `fm mission` and `fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen <earlier ideas.md>`, with lenses fitted to its capability, plus **inversion** (how this capability fails or gets abused), **sci-fi** (the 2030 version, worked back to a slice buildable today) and **self-modification**. It invents at least 2 lenses of its own and puts their definitions in the pack.
3. It grounds every idea against the code (brainstorm step 4: nothing dropped silently) and tags it with an **ambition tier**: 1 tweak, 2 feature, 3 capability, 4 paradigm. At least 70% of what gets built is tier 3–4. Tier 1 goes to the inbox.
4. It builds (§6) until its capability's exam passes.
5. It writes `gen-N/critique-<capability>.md`: what in its mission or the Seed was wrong or too timid, and a proposed rewrite of each.
6. **Selection:** the next Seed is written from the critiques. A rewrite stays only if its generation closed more exam scenarios than its parent did; otherwise the parent text comes back. Lineage goes in `lineage.md`. Every 3rd generation, the Seed and mission templates and `ideas-prompt.md` go through `fm evolve --runs 3`.
7. **Drift check:** an `fm second` read compares each new Seed to gen-0's goals, MUSTs and NEVERs, and undoes anything that drifted.
8. **Structure caps:** at most 4 levels, at most 8 Missions per generation, one generation at a time, each finished before the next starts.

## 4. The exam: local, cheap, held out

There are no outside repos. Build the exam in gen 1, as a permanent suite like `fm code bench` or `bench/spec-suite`:

- **Generated scenarios:** throwaway repos made locally from scripts, in at least 6 languages, with planted defects (bugs, vulnerabilities, missing tests, slow paths, docs drift, a flaky test, a broken dep), plus vague goals ("make this production-ready"), ambiguous requests, and a task that needs a tool Foreman doesn't have. Every scenario has a hidden answer key. "No request at all" scenarios test initiative.
- **My own history:** `fm bench build` cases from finished tasks, `fm backtest` on real sessions, and `fm bench court` on my past corrections, so taste is measured too.
- **Held out:** a third of the scenarios are never shown to any Mission or used for selection. They're only used to grade a capability as done, so the tower can't overfit to the exam.
- **Scored:** what it found or did against the answer key, false alarms, how many readings and approaches it considered against the key's list, fixes that pass with a failing-test-first proof, tokens per verified result. Results go to `research/genesis/exam.jsonl`.

## 5. Outside ideas: targeted only

When a Mission is stuck on a specific gap, it may do one `fm research ask` on how others solve exactly that, and search the already indexed sources (`fm lib search`, `fm lib source defaults`, which are markdown-only and cheap). At most a couple of web pages or one README per gap, never a clone-and-read sweep. Distill the result into the mission's critique.

## 6. Building rules

- Tier 4 or uncertain → `fm lane new ID --spike` first, then promote it or kill it with the reason. "Too ambitious" is never a reason on its own.
- Two credible designs → `fm lane race`, then `fm lane pick`.
- A normal brief: red-first test, M/L approaches listed first, `fm task finish` with its audits.
- Changes to Foreman's instruction files go through `fm evolve`, kept only past `fm bench gate` and `fm bench court`. Protected core goes through an `/foreman:improve` worktree and is queued for my yes.
- Every self-change is a registered trial with the metric it should move.
- **Subtract as you add:** each generation removes, merges or slims at least as much as it adds (`fm burden --by-verb`, unused verbs and cards). Hook p95 (`fm doctor`), rules size and injected context may not grow. A new capability pays for itself or gets cut.
- **Retry limit:** a blocked task gets two genuinely new approaches. If both fail, record the diagnosis with `fm decide` and move on. It doesn't loop.

## 7. Completeness sweep (the end of every generation)

Run `fm state`, `fm queue`, `fm lane list`, `fm docs`, `fm doctor` and the full gates. Every task is closed, or blocked with a diagnosis after its two retries. Every spike has a verdict. Every finished lane is merged (or queued for me if it's core). Docs drift is zero, gates are green, and the exam is re-run. The next generation doesn't start until this is clean.

## 8. Final report (one, at the end)

- The capability scorecard: each §2 item with its held-out exam score per generation, what was built for it, and a short real example of it working
- The catalogue checklist page: every idea with its capability, tier, outcome and reason
- The prompt lineage, and which rewrites won
- What was removed to stay lean, with the hook latency and context numbers before and after
- What's waiting on me: core candidates with their eval deltas, installs and timers, outward actions, merges, `fm decide --review` items
- The last completeness sweep's output, and `fm cost` for the record
