# Brainstorm — lens: capability map

- **Re-run proven tasks nightly and bisect the break** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: closed tasks store verify commands and start commits, but nothing re-checks them once closed. Assumption: verify commands are replayable from the ledger.
  Done when: break a function a closed task proved, run the tick, and the digest names that task and the first bad commit.

- **Taint untrusted content in the guard** — SECURITY — value 5 — effort L — risk med — category: injection
  Why: T-0791 holds 18 deferred injection ideas and none is built. Assumption: PostToolUse sees web and file-read results.
  Done when: a command whose text was copied from a fetched page is held for confirmation, and the same command typed by the user is not.

- **Run bypass-mode sessions in a bwrap/Landlock sandbox** — SECURITY — value 5 — effort L — risk med — category: sandbox
  Why: the guard blocks by pattern, so anything it misses runs with full access. A per-task profile (write only to the worktree, network allowlist) limits the damage. Assumption: Linux-first.
  Done when: `fm sandbox run` fails to write outside the repo or reach a non-allowlisted host, and the receipt lists the profile.

- **Gate diffs for secrets and new dependencies** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: a pasted credential already reached the inbox (T-2624), and nothing scans agent-written diffs. Add typosquat, age and license checks on newly added packages.
  Done when: a diff adding a fake key or a one-day-old package name blocks `fm ship` with the line named.

- **Add a diff-coverage proof kind** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: red-first tests prove a test fails without the change, but not that every changed line is exercised. Assumption: stack cards know each language's coverage tool.
  Done when: a task whose new branch no test reaches finishes with "unproven: 3 changed lines uncovered", not as passed.

- **Hand a task between harnesses** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: Foreman targets Claude, Codex, Gemini and opencode, but a session started in one can't resume in another. Pass the plan, task state, proof so far and lessons.
  Done when: `fm handoff T-x --to codex` starts a Codex session that names the plan and the remaining proof steps without re-asking.

- **Review someone else's PR with the proof discipline** — FEATURE — value 4 — effort M — risk low — category: review
  Why: Foreman verifies its own work but never a human's. `fm review <PR>` would run the PR's claimed tests and check each claim in its description against the diff.
  Done when: on a PR whose description claims a fix the tests don't cover, the output lists that claim as unproven.

- **Unit-test the guard rules with examples** — CLEAN — value 4 — effort S — risk low — category: guard
  Why: the standing rules say every steer gets an automatic check, but the guard's block rules have no should-block and should-allow corpus. Assumption: rules live in one data file.
  Done when: `fm guard test` fails when a rule edit lets a listed dangerous command through or blocks a listed safe one.

- **Add an event bus with notification sinks** — FEATURE — value 3 — effort M — risk low — category: notifications
  Why: tick failures, pending `fm ask` prompts, a finished queue and a tripped guard are only visible inside a session. Sinks would be ntfy, webhook, Matrix and desktop. Nothing is sent without an explicit setting.
  Done when: with `sink ntfy` configured, a failed night tick sends one message naming the cause, and with none configured nothing leaves the host.

- **Generate release notes from closed tasks and their receipts** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: there are 2,600+ tasks and the commit log is the only story. Group by FEATURE/FIX, show each proof line, and leave out unproven tasks.
  Done when: `fm release-notes v1..v2` produces a markdown file where every entry links a task id and its proof status.

- **Sync the queue with GitHub Issues or Linear in both directions** — FEATURE — value 3 — effort M — risk med — category: integration
  Why: a watch exam kind for issues exists, but task state doesn't flow back to the tracker. Assumption: teams expect statuses to match.
  Done when: closing T-x comments the receipt on its linked issue and closes it; reopening the issue reopens the task.

- **Wild: Make Foreman an MCP server for any agent** — FEATURE — value 4 — effort L — risk med — category: platform
  Why: `plugin/templates/mcp-server` is a template. If `fm_plan`, `fm_prove` and `fm_guard_check` were exposed as tools, an agent with no hook support (Cursor, Zed, Aider via a bridge) would get the discipline. Wild.
  Done when: a stock MCP client lists the three tools and `fm_guard_check "rm -rf ~"` returns a block.

- **Wild: Replay a session against a new model before upgrading** — PERFORMANCE — value 4 — effort L — risk low — category: model change
  Why: model IDs change often, and the duel measures Foreman against plain, not model against model. Replay the last 10 finished tasks' goals from their start commits and compare pass, cost and time. Wild.
  Done when: `fm bench swap --to claude-opus-5-5` prints a table by task kind and refuses to change the default if pass rate drops.

- **Wild: Stage a "lessons passport" shared across repos** — FEATURE — value 3 — effort M — risk med — category: knowledge
  Why: lessons and stack cards are per project; the same mistake in a second repo is learned again. Export redacted lessons by stack tag; import is opt-in and read by the cold-read check. Wild.
  Done when: a lesson from repo A that matched a tag shows up at planning in repo B with its source labelled, and a lesson with a redacted credential is refused on export.

Next question: Which Foreman checks assume the project has tests, and what proof does a repo with none (infra, docs, data pipelines) get?
Next question: Who besides this user could run Foreman (a teammate, CI), and which ledgers and steers would then conflict?
