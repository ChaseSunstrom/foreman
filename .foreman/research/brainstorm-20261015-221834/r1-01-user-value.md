# Brainstorm — lens: user value

- **Resume any stopped agent from one verb** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: The user asked for worktree agents to resume easily after a session stops; T-1028 is only "planned". Assumption: builders leave a worktree, branch, task id and brief that can be rejoined.
  Done when: after killing a builder mid-task, `fm resume` lists it with its task, branch and last step, and resuming it continues from that step with the brief intact (tested with a fake killed session).

- **Write a handoff note on every stop** — FEATURE — value 5 — effort S — risk low — category: continuity
  Why: Users complain that instructions don't survive compaction or new sessions; the user said "session was stopped or something". Assumption: Stop and SessionEnd hooks can write a small file.
  Done when: a killed or compacted session leaves `.foreman/handoff/<id>.md` (done, next step, open questions, uncommitted files), and the next SessionStart injects it in under 400 tokens.

- **Share fixes through git as reviewable hints** — FEATURE — value 5 — effort M — risk med — category: portability
  Why: The user steered that fixes must travel with git, per-project in the repo and machine-wide in Foreman state. T-1032 shipped the learning. Gap (assumption): trust and merging across clones.
  Done when: a hint file committed on one clone is offered on a fresh clone for a matching obstacle, with provenance (task id, date) shown, and `fm hints prune` drops entries that stopped matching.

- **Score each hint by outcome and retire the ones that don't help** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: The user asked "why have you not really improved" and wants genuine self-improvement. T-0217 (lesson confidence) is deferred. Assumption: offering a hint and the next pass/fail are both recorded.
  Done when: `fm hints` shows offered/helped/ignored counts per hint, and a hint that failed three offers in a row is demoted and reported.

- **Report what Foreman learned this week** — FEATURE — value 4 — effort S — risk low — category: visibility
  Why: The user can't see the improvement they ask about. Assumption: the ledger holds the data to answer it.
  Done when: `fm learned --since 7d` and a pane section list new hints, repeat obstacles avoided, and time or tokens saved with the evidence for each.

- **Detect repeat obstacles before they cost a turn** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: The user's example was a harness stalling at the folder-trust prompt on every recording. Assumption: failure signatures (command, exit code, output tail) can be normalized and matched.
  Done when: a second occurrence of a recorded failure signature is intercepted by PostToolUse with the known fix attached, shown by a test that replays the failure twice.

- **Ship a one-line start ritual** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: The user said they shouldn't need to ask for any of it. T-0861 to T-0863 ask for a newcomer path but are deferred. Assumption: the first-run guide is too long.
  Done when: opening Claude Code in a repo shows one line ("3 queued, 1 stopped builder, 2 hints ready: `fm go`"), and `fm go` does the sensible next thing.

- **Triage the deferred backlog into drop, do or ask** — CLEAN — value 4 — effort M — risk low — category: backlog
  Why: Over 25 open items are deferred, many "Later from T-0760/0818/0843". They are stale cost and noise. Assumption: some are dead.
  Done when: `fm triage` proposes a verdict with a reason for each deferred item, and applying it shrinks the open list, with every drop kept in the ledger.

- **Run the brainstorm-build-review loop unattended until dry** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: The user asked for a "super recursive brainstorm: build, review, brainstorm on top, repeat until dry". Assumption: a budget and a stop rule exist.
  Done when: `fm loop --budget $N` runs rounds, stops when a round yields no new accepted ideas or the budget is spent, and writes a per-round scorecard (T-0826).

- **Explain each blocked item with its unblock command** — FIX — value 3 — effort S — risk low — category: clarity
  Why: Several tasks sit blocked (T-0325, T-0335, T-0336, T-0352) on things the user can do, such as installing a package. Assumption: users forget these.
  Done when: `fm next` lists each blocked task with the exact command or step that unblocks it, and re-checks the block when that is done.

- **Wild: Let a teammate's clone inherit the whole learned brain by a single `git pull`** — FEATURE — value 4 — effort L — risk med — category: portability
  Why: wild; extends the steer about transferable fixes. Assumption: hints, vetoes and lessons can sit in one committed directory that merges cleanly.
  Done when: a fresh clone with no Foreman state shows the same hints, lessons and gates as the original in `fm doctor`.

- **Wild: Replay last week's failures against today's Foreman and report which it now prevents** — FEATURE — value 4 — effort L — risk med — category: proof of progress
  Why: wild; answers "why have you not improved" with evidence, and builds on T-0035 (eval capture). Assumption: failures can be captured with enough context to replay.
  Done when: `fm replay --week` prints N failures, M now caught or fixed by a hint or gate, with a diff against the previous week.

- **Wild: Let Foreman write its own "letter to the next session" as the pane's idle screen** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; the pane is empty when quiet and the user dislikes empty areas. Assumption: the handoff note exists.
  Done when: with no active task, the pane shows the last handoff, the stopped agents and the next suggested step in place of blank space.

- **Wild: Offer to turn a repeated manual request into a standing rule after the third time** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: wild; the user keeps re-asking for similar things (UI density, fills the dock, no gaps). Assumption: repeated phrasing can be clustered.
  Done when: after three similar user requests, Foreman proposes one rule with the evidence, and accepting it adds it to the standing-rule store.
