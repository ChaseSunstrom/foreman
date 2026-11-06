# Brainstorm — lens: relay race (invented): a fresh session with zero memory must resume mid-goal exactly; the plan on disk is the only memory

- **Derive the baton from the ledger, not the model's goodbye** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: "Resume here" is written at PreCompact and Stop. A crash, kill or usage limit fires neither hook, which is the case the goal most needs to survive. The hash-chained ledger already records every step.
  Done when: after `kill -9` mid-step, a fresh `fm resume` prints the last step, last evidence and open criteria matching the ledger head, with no model-written text involved.

- **Add `fm goal step`, the next action from files** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: `fm genesis step` already does this for the tower, and the goal ledger gap has no equivalent. Assumption: a goal object exists, with contents → tasks → done-when.
  Done when: two cold invocations print the same action, and the output changes only after a new ledger event. The command writes nothing.

- **Gate the first edit on reading the baton** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: the PreToolUse guard already exists. A fresh session that starts editing before it has oriented is the commonest relay fumble. Assumption: the hook can see whether a baton exists for the session's goal.
  Done when: in a fresh session on a goal with a baton, an Edit is denied with a pointer to `fm resume`. After the ack, keyed to the baton hash, it is allowed. A changed baton re-arms the gate.

- **Journal every mid-goal steer at UserPromptSubmit** — FEATURE — value 5 — effort M — risk med — category: memory
  Why: the user's words are full of steers ("keep it read-only", "widened", "criterion 2 reads the last finished run"). A steer that lives only in chat dies at compaction, and the plan on disk never learns it. Untrusted text is stored quoted (`c.plain`).
  Done when: a prompt such as "also keep X out of scope" appears as a dated quoted steer on the goal after a compaction, and `fm resume` shows it.

- **Carry decisions with their reasons** — FEATURE — value 5 — effort M — risk low — category: continuity
  Why: every choice goes through `fm decide`. A cold session that can't see the rulings re-litigates them or re-asks, which the run's "never ask mid-run" rule forbids.
  Done when: `fm resume` lists the last N rulings tied to contents items. A test shows a repeated question returns the earlier ruling by fingerprint instead of opening a new decision.

- **Keep a dead-ends list in the baton** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: a fresh session can't know what the last one already tried. The ledger holds failed verify runs, so assumption: failed command plus error are recoverable from it.
  Done when: after two failed attempts at one criterion, a cold `fm resume` shows both commands and their error lines under "tried, failed". Retrying the identical command prints a warning.

- **Show what the world did during the gap** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: days pass between legs, and the user commits by hand, switches branches and edits briefs. Assumption: HEAD, branch and the dirty file list are recorded at each baton write.
  Done when: in a scenario where the user committed twice and edited one file between legs, resume prints "HEAD moved +2". It also lists the dirty files that fall outside any step's declared files.

- **Cap the resume packet with a fixed shed order** — PERFORMANCE — value 4 — effort S — risk low — category: hooks
  Why: hook context over ~10 KB becomes a preview, so a long goal could lose its next action to truncation.
  Done when: a goal with 200 items yields a packet of 8 KB or less. Next action, open criteria and steers are always present, and a test pins the order in which the rest is shed.

- **Lint plan text for context-dependent phrasing** — CLEAN — value 3 — effort S — risk low — category: plan quality
  Why: a brief step saying "as above" or "same as before" means something only to the session that wrote it. The plan on disk is the sole memory, so that phrasing is a latent resume bug.
  Done when: the lint flags fixture steps containing "as discussed", "the file" or "same as before". A self-contained brief passes. The check runs at task creation and at PreCompact.

- **Hand the baton to another agent** — FEATURE — value 4 — effort L — risk med — category: surfaces
  Why: shims exist for Codex, Gemini and opencode, and `fm code` is its own agent. When Claude Code hits a usage limit, a different engine could take the next leg, and a portable baton format would allow that.
  Done when: a baton written in a Claude Code session is read by `fm code`, which resumes at the same step in an exam scenario and cites the same criteria.

- **Add a goal lease with a logged takeover** — FIX — value 3 — effort M — risk med — category: concurrency
  Why: assumption: the user opens a second terminal on the same project mid-goal, and two runners then double-spend or collide.
  Done when: a second session sees "leg held, heartbeat 40s ago" and is read-only. After a stale heartbeat it can take over, and the takeover is a ledger event.

- **Wild: run an always-relay mode, with every step a fresh session** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: this measures the baton directly. One exam arm runs each task step in a new session fed only the on-disk plan, and a second arm runs the same goal continuously. The gap between them is the relay penalty, a score for how self-sufficient the plan is.
  Done when: `fm exam` reports a relay-penalty number per scenario, and a deliberately vague baton scores visibly worse than a good one.

- **Wild: fuzz the goal files with amnesia damage** — FIX — value 4 — effort M — risk low — category: reliability
  Why: a crash can leave a torn write, a truncated brief or a missing section. Assumption: `fm resume` now trusts what it reads.
  Done when: for each of N random truncations or deletions of goal files, resume ends in a named verdict (rebuilt from ledger, or degraded with the reason). It never crashes and never invents a next step.

- **Wild: carry the user's vocabulary into every leg** — FEATURE — value 3 — effort M — risk med — category: memory
  Why: the user's words use project-private terms such as "tower", "held-out", "brief", "Mission" and "lane". A cold session may read them as plain English and plan the wrong thing. Assumption: terms can be mined from the user's recorded words, with their defining quotes.
  Done when: the baton carries a glossary of terms the goal's words use, each with its defining quote as quoted data. A cold-resume scenario using one such term picks the project meaning.

Next question: When two legs disagree about what "done" means (a steer in leg 2 changes a criterion leg 1 already closed), which one wins, and where is that recorded?
Next question: How long may a goal sit idle before its baton should be re-grounded against the repo rather than trusted?
