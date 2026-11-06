# Brainstorm — lens: bold bets

- **Enforce the guard at the OS, not the hook** — SECURITY — value 5 — effort L — risk med — category: security
  Why: T-0335/T-0336/T-0337 are blocked because Codex, Gemini and opencode have no usable hook events. A hook-only guard only works where the harness cooperates. An `fm sandbox -- <agent>` wrapper (bwrap or Landlock plus a PATH shim for rm, git push and curl) makes the same rules hold on any agent, including `fm code`. Assumption: bwrap or Landlock is available on the user's Linux hosts.
  Done when: under `fm sandbox -- sh -c 'git push --force'` the push is refused and logged, with no Claude hooks loaded.

- **Expose discipline as an MCP server** — FEATURE — value 4 — effort M — risk low — category: adapters
  Why: the adapter tasks are stuck on per-harness hook gaps, but all four CLIs speak MCP. Tools such as `fm_plan`, `fm_prove`, `fm_next` and `fm_finish` would give them the plan and prove loop even without hooks. Assumption: the agents call MCP tools reliably when the prompt tells them to.
  Done when: a Codex session with only the MCP server configured completes a task whose receipt has a plan and a prove record.

- **Explain any line with `fm why file:line`** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: commits are prefixed with task ids (T-2624, T-2616). Blame to task id to request, plan, proof, decisions and bets can be joined, and nothing today answers "why does this code exist". An editor hover or web-UI link could reuse it.
  Done when: `fm why plugin/lib/x.py:40` prints the task's request, its proof commands and the decisions that touched it.

- **Route each task to the cheapest model that historically passes** — PERFORMANCE — value 5 — effort L — risk med — category: cost
  Why: T-1266 (ceremony per model) and T-1231 (beat Claude Code on cost and time) both depend on duel data, and `fm code` already runs on any model. A router that chooses model and ceremony per task kind from outcome survival and cost per proven task turns that data into savings. Assumption: there are enough settled tasks per kind to estimate pass rates.
  Done when: `fm code --auto-model` picks a model, shows the pass rate and cost estimate behind the choice, and a replay on 20 past tasks costs less at the same pass rate.

- **Gate package installs** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: T-0791 (injection and supply-chain defenses, 18 ideas) is deferred, and the guard stops destructive commands but not `npm i typo-pkg`. Intercept pip, npm, cargo and go installs and check package age, typosquat distance to popular names and install scripts. Quarantine anything suspicious until the user approves it through `fm ask`.
  Done when: a seeded install of a package with a typosquat name and a postinstall script is blocked with the reason named, and a normal install passes in under a second.

- **Hand a session between harnesses** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: Foreman claims to be harness-neutral, and the stage, plan, proofs and queue all live in its own files. `fm handoff --to codex` would write a bundle the next agent loads, so a usage limit on one vendor doesn't stall the queue. Assumption: the receiving CLI can read the bundle as its first prompt.
  Done when: a task started in Claude Code, handed to `fm code`, finishes with one continuous receipt whose steps name both harnesses.

- **Check the diff against the plan's scope** — FEATURE — value 4 — effort M — risk low — category: discipline
  Why: Foreman plans before it edits and keeps to one task at a time, but nothing compares what was edited with what the plan declared. At finish, files or symbols outside the plan are flagged as scope creep, which needs an explicit reason or a split into a new task.
  Done when: a test task that touches an undeclared file fails `fm task finish` until the file is justified or split out.

- **Write release notes from receipts** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: docs are a thin area, and every commit already carries a task id with a request and a proof. `fm release-notes v1..v2` would group closed tasks by kind, put the user's own words first, and link each line to its proof. Unproven or reversed tasks are marked.
  Done when: running it between two tags produces a changelog where each entry has a task id and a proof status, and a reversed task shows as such.

- **Judge cold reads with a local model** — FEATURE — value 3 — effort M — risk med — category: privacy/cost
  Why: the standing rules require a cold read on every tower file and every Mission, with Haiku first and Sonnet deciding, and that costs usage and sends code out. A local engine such as Ollama could take the first pass. The rules already say Sonnet's verdict stands on any non-pass, so the local read only filters. Assumption: a local model can catch the obvious gen-0 violations.
  Done when: with `--local-first`, at least 60% of passing cold reads finish with no API call, and the escalated ones match Sonnet's verdict on a labelled set.

- **Wild: Apprentice mode for the user's own commits** — FEATURE — value 4 — effort L — risk med — category: user value — wild
  Why: assumption: the user also edits by hand, and those commits get no plan or proof. A watcher notices non-agent commits, drafts the task, infers which tests cover the change, runs them, and files a receipt marked "after the fact". Human work then shows up in the same ledgers, bets and `fm why`.
  Done when: a hand commit in a test repo gets a drafted receipt within a minute, labelled "after the fact", with the tests it ran.

- **Wild: Turn a bug report into a task from a screen recording** — FEATURE — value 3 — effort L — risk high — category: intake — wild
  Why: assumption: the user's UI bugs are hard to put in words, and `fm intake` takes only text. Frames from a clip or screenshot sequence go to a vision model, which writes a repro, a failing check and a DONE-WHEN. The receipt labels the check "unproven (no display)" if it can't run.
  Done when: a recorded 10-second clip of a seeded UI bug yields a task whose repro steps reproduce the bug on the fixture app.

- **Wild: Install an andon light** — FEATURE — value 2 — effort S — risk low — category: devices — wild
  Why: assumption: the user runs Foreman unattended overnight and in the drive. A local webhook sets a smart bulb, a USB light or a terminal-bell colour from queue state: green when proven and idle, amber when it waits on a usage limit, red when it needs the user (`fm ask`, a tripped guard, a dead timer).
  Done when: forcing a pending `fm ask` in a test changes the configured webhook's payload to red within 5 seconds.

- **Wild: Brief the day by voice** — FEATURE — value 2 — effort M — risk low — category: devices — wild
  Why: the night tick already writes a digest (T-2607 and the nightly bet-Brier line). A local text-to-speech pass turns it into a 60-second clip: what finished, what is unproven, what blocks only the user. It can play from the web UI or as a phone notification. Assumption: a local TTS engine such as piper is installable.
  Done when: `fm brief --audio` writes a file under 90 seconds whose transcript matches the digest's three sections.

Next question: Which of Foreman's guarantees hold only because the harness cooperates (hooks, transcripts, `fm` being on PATH), and what does each one become when the agent is hostile, buggy or not Claude?
Next question: What would the user have to give up to run only the 20% of Foreman they've actually used in the last 30 days, and can Foreman measure that without asking?
