# Brainstorm — lens: bold bets

- **Run Foreman as a signed protocol server any agent can plug into** — FEATURE — value 5 — effort L — risk med — category: platform
  Why: the standing rule says Foreman isn't Claude-specific, and T-0335/36/37 stay blocked per-adapter because each harness needs bespoke wiring. One local MCP/ACP-style server exposing plan, prove, guard and task verbs would serve every harness at once. Assumption: Codex, Gemini and opencode all accept MCP tool servers.
  Done when: a fake non-Claude agent that speaks only MCP can open a task, get a guard refusal on a planted `rm -rf`, run `fm prove`, and close the task, all recorded in the ledger.

- **Replay a past commit overnight, Foreman vs plain, on the user's own repo** — FEATURE — value 5 — effort L — risk med — category: evidence
  Why: the long-horizon tier is deferred to the end of the run, and T-1231 ("beat Claude Code on the duel") needs real cases (T-0866 "needs cases"). The user's own history is a free, private case corpus. Assumption: the user will spend idle quota on it.
  Done when: `fm duel --repo . --commits 5` checks out each parent in a scratch worktree, runs both arms toward the real follow-up commit's goal, and prints pass, cost and time per arm.

- **Compile steers, lessons and guard rules into the other harnesses' native files** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: 40+ steers live only in Foreman's store; Codex, Gemini and opencode sessions never see them. Assumption: AGENTS.md, GEMINI.md and `.cursor/rules` are read at session start.
  Done when: `fm export-rules --agents` writes the three files, and a test confirms each steer's `[check: CMD]` appears or is explicitly marked "not enforceable here".

- **Fork a live or finished session at any step into a counterfactual branch** — FEATURE — value 4 — effort L — risk med — category: debugging
  Why: the user keeps asking "what if" (replay a session on a new model, run with one steer removed). The ledgers already record each step's commands. Assumption: tool calls are deterministic enough to replay from a snapshot.
  Done when: `fm fork T-#### --at STEP --steer-off N` produces a worktree at that step and a diff-of-outcomes report against the original.

- **Guard with a local small-model intent check for commands no rule matches** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard is regex-based; T-2668 shows its parser has limits, and the open question lists "unparseable" commands. The privacy lens favors local. Assumption: a small local model is installed, and the check is opt-in.
  Done when: a set of 30 obfuscated destructive commands the regex guard misses is blocked, with 0 false blocks on the replayed benign history, and the model call is off by default.

- **Make the ledger a content-addressed, machine-mergeable store** — FEATURE — value 4 — effort L — risk high — category: state
  Why: the ledger is hash-chained and `fm drill --restore` already exists, but two machines or lanes blur it. Assumption: user works from more than one machine.
  Done when: two copies diverge by independent appends, `fm merge-ledger` joins them, `fm verify-ledger` passes, and no record is lost or duplicated.

- **Add a verified "undo this landed task" verb** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: tasks land with receipts and a proof command, so reversal can be checked too. The dropped-ideas list shows the user doesn't want blind rewrites. Assumption: landed tasks map to revertable commits.
  Done when: `fm undo T-####` reverts the commits, reruns the suite, and refuses unless the task's own proof now fails as expected.

- **Spend idle quota on speculative drafts of the top queue items** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: the `--stall-usd` work and "spend receipt" asks show spend control matters. Drafts land only as unmerged branches, so the user pays in review, not risk. Assumption: pace data shows idle quota expiring.
  Done when: with idle quota and an empty urgent queue, the drive writes a draft branch for the top task, and `fm next` offers it as "draft ready" without merging.

- **Run a Foreman-as-oracle test of the whole product in a seeded simulated world (wild)** — FEATURE — value 4 — effort L — risk med — category: testing
  Why: assumption: a fake clock, fake agent and fake forge compose into a deterministic week; the user keeps asking for clock injection and crash points (T-2632 era).
  Done when: `fm sim --seed N` replays a week of edges and faults and prints identical ledger hashes across two runs.

- **Wild: Distil a small local model of the user's judgement from their accepts and drops** — FEATURE — value 4 — effort L — risk med — category: personalization
  Why: the pack holds hundreds of dropped and accepted ideas with reasons. Assumption: enough labelled pairs exist to rank better than chance.
  Done when: on held-out accept/drop history, the model's ranking beats the lens-value ordering by a stated margin, and it runs without network.

- **Wild: Hold a standing Anti-Foreman adversary scored on the lies it finds** — SECURITY — value 4 — effort M — risk low — category: verification
  Why: standing rules demand signals Foreman didn't author. A different-model child gets only the finish receipt and the diff and must find one false claim; a hit counts as a finding.
  Done when: against three planted false "proven" receipts the adversary finds at least two, and finds none on true ones.

- **Wild: Pre-answer the three likeliest follow-up asks on every finish card** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the pack shows follow-ups arriving within days (T-2656, T-2657 chains). Assumption: follow-ups cluster in predictable classes.
  Done when: on 20 past closed tasks, at least 8 of the real next asks match one of the three predictions.

- **Unify every unattended spawn under one capability token** — SECURITY — value 4 — effort M — risk med — category: authority
  Why: the left-over question asks which spawned processes inherit the push grant or signing key. Assumption: they currently inherit by default.
  Done when: a canary grant planted in the environment is unreadable by lanes, ticks, `fm code` tools and prover children, proven by a test per class.

Next question: Which of these needs the user's other machines or accounts, and how would Foreman know before filing it?
Next question: What fraction of the 525-idea catalogue has any measured evidence of user-felt value, versus self-generated rationale?
