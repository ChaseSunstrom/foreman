# Brainstorm — lens: subagents and delegation

- **Add an implementation subagent that works only in a lane worktree and returns a patch** — FEATURE — value 4 — effort M — risk med — category: subagents
  Why: the delegation policy bans implementation subagents, so every edit runs through the main thread's context. `fmlanes` already creates worktrees, and "Delegate mechanical edits under a patch contract" was proposed but not built. The agent works in a lane and the main thread merges after the gate.
  Done when: a mechanical S task, such as a rename across 6 files, is run by an `fm-builder` agent in a lane. Its diff merges only after `fm check` passes, and `fm cost` shows main-thread tokens for the task below a recorded baseline.

- **Add a research planner that splits a question into sub-questions before fm-recon runs** — FEATURE — value 4 — effort M — risk low — category: research
  Why: the pack says there is "no research plan/question decomposition". One recon call gets one brief and a 400-word cap. A plan file lists 2–4 disjoint sub-questions, each with a stop condition, so parallel recons (≤3) cover disjoint ground.
  Done when: `fm research plan "Q"` writes a plan with sub-questions, source types and stop rules. Each `fm-recon` brief is generated from one entry, and `fm research add` refuses a result whose sub-question id is missing.

- **Add a cross-check agent that re-fetches the cited URL for each load-bearing web claim** — FEATURE — value 4 — effort S — risk low — category: research
  Why: the main thread spot-checks only two claims, and "Cite-check research answers" was proposed only as an idea. A Haiku `fm-scout` variant with WebFetch only verifies that each quote or claim appears at its URL and returns pass/fail per claim.
  Done when: `fm research add --verify` marks each claim as confirmed, not found or unreachable in the saved note. An injected fake claim in a test fixture is flagged.

- **Give research notes freshness metadata and a source-quality tier** — FEATURE — value 3 — effort S — risk low — category: research
  Why: the pack says there is "no source-quality ranking... no notion of freshness". At `research add`, store the fetch date, a source tier (primary doc, vendor blog, forum) and an expiry by topic type. `fm recall` demotes expired or low-tier notes and tags them "stale".
  Done when: a fixture note older than its expiry appears in `fm recall` with a stale tag and ranks below a fresh note on the same query.

- **Cache fetched pages by URL and date, shared by all recon agents** — PERFORMANCE — value 3 — effort S — risk low — category: research
  Why: the pack says there is "no cache of fetched pages", and a usage-sensitive user pays for repeated fetches across briefs. Recon is told to go through `fm fetch URL`, which stores a trimmed text copy keyed by URL under state. It is searchable by `fm recall`.
  Done when: a second `fm fetch` of the same URL within its TTL makes no network call, and a recall query finds text from the cached page.

- **Record which playbooks and subagents were used and whether the task closed cleanly** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the pack says playbooks are "not measured" and the "46 never-read playbooks" idea has no data behind it. A PostToolUse note logs playbook Reads and agent calls per task. At finish, `fm friction` joins them to the gate retries and rework counts.
  Done when: `fm playbooks stats` lists each playbook with reads, tasks and the gate-retry rate of those tasks versus tasks that didn't read it.

- **Make a delegation router that chooses agent, model and scope from the step** — FEATURE — value 3 — effort M — risk med — category: delegation
  Why: the policy is "default none" and delegation is up to the model's judgement, which is why the "Brief and cap read-only subagents" idea exists. A table in `fm next` maps step kinds (a lookup of 3 files or fewer, an unfamiliar area, an audit) to scout, recon or reviewer, with a token cap and a prewritten brief skeleton.
  Done when: for a step that touches an area with no recall hits, `fm next` prints one `delegate: fm-recon <brief path>` line. A trivial step prints none.

- **Wild: Add a debate pair of reviewer agents who must disagree before a verdict counts** — FEATURE — value 3 — effort M — risk med — category: audit
  Why: assumption: one reviewer pass is cheap but rubber-stamps. One agent argues "ship" and the other "block", both over the same diff, run only for L and security tasks. Findings the two sides agree are real go into the verdict, and unresolved ones go to the user as yes/no.
  Done when: an L fixture with a planted bug yields a debate record in which the block side cites the bug line.

- **Wild: Let the main thread spawn a "future me" agent that writes the handoff and the outcome report from the transcript** — FEATURE — value 3 — effort M — risk low — category: delegation
  Why: the pack lists handoffs, outcome reports and lessons as separate main-thread writing, which costs tokens at the busiest time. A Haiku agent drafts them from the task's ledger and diff, and the main thread edits only the diff of that draft.
  Done when: `fm task finish` produces a draft report and lesson from the ledger with no main-thread composition tokens. The draft passes the existing lesson and docs checks.

- **Wild: Add a "skill scout" subagent that reads a newly installed plugin and drafts its stage mapping** — FEATURE — value 4 — effort M — risk med — category: plugin compat
  Why: the integrations table is static and `fm next` can't route to third-party skills. The scout reads the new plugin's skill frontmatter and proposes a stage, a conflict note and an always-on cost line. The user answers one yes/no and the mapping lands in the capability index.
  Done when: enabling a fixture plugin triggers a draft entry with stage, conflicts and cost. After a yes, `fm next` for a matching task type names its skill.

- **Wild: Run a recon "red herring" self-check where a second recon is told the first one's answer is wrong** — FEATURE — value 2 — effort S — risk low — category: research
  Why: assumption: recon output is single-source and confidence labels are self-assigned. The counter-agent looks for disconfirming evidence only. Its findings are appended as "challenges" in the saved research note.
  Done when: for a fixture question with a planted false premise, the saved note lists a challenge that cites the contradicting source.
