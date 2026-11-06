# Brainstorm — lens: delight

- **Publish a live Artifact run board** — FEATURE — value 5 — effort M — risk low — category: artifacts
  Why: Artifact is in the tool list with 0 references; the user keeps asking for a cockpit (Frontier 11) but only has a local pane and web UI. A private claude.ai page works from phone or any browser, with no server to run.
  Done when: `fm board publish` creates an Artifact showing queue, current step, evidence and blocked asks, and the page updates after the next `fm task` state change.

- **Answer asks from the Artifact page** — FEATURE — value 5 — effort M — risk med — category: artifacts, asks
  Why: ArtifactData and ArtifactComments flow back to the CLI. The user is never handed commands and asks pile up while they're away (the digest and deadline-default ideas). Approve and Defer buttons, plus a comment box that becomes a captured task, would resolve them.
  Done when: pressing Approve on a pending `fm ask` card on the page resolves that ask in the ledger within one poll, and a comment on a task becomes a T-id with the comment as brief.

- **Push a one-line "done" to the phone** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: `fm notify` only runs a user shell command, which needs setup. PushNotification is built in. The messages could be small and human, e.g. "T-0760 closed: 3 checks green, 1 thing needs you".
  Done when: finishing a task or hitting a block while the session is idle sends one PushNotification, and a setting turns it off.

- **Stream the long run with Monitor** — FEATURE — value 4 — effort S — risk low — category: live feedback
  Why: gates, `fm night` and smoke are long silent runs, and the user complained about it "sitting idle". Monitor turns their output into live notifications ("suite 412/1900… 2 failures so far") instead of silence.
  Done when: a verify taking over 30s emits at least three progress notifications, and the failing test name appears before the run ends.

- **Name the work on the band by lane** — FEATURE — value 3 — effort S — risk low — category: statusline
  Why: the user noticed it "will start working on different steps without updating the step". A statusline that shows the actual step title, with a gentle tick animation when evidence is recorded, makes drift visible and gives a small reward.
  Done when: recording evidence for step N changes the statusline step text within one render, and starting an edit under a different step shows a visible mismatch marker.

- **Sing a morning "while you were away" Artifact** — FEATURE — value 4 — effort M — risk low — category: return screen
  Why: unattended night runs end with a wall of ledger text. A generated one-page recap (what shipped, what was refused, what needs a decision, the one thing it's least sure about) is what the user would show people.
  Done when: after `fm night`, an Artifact titled with the date exists and contains shipped, blocked and needs-you sections, each linked to T-ids.

- **Tint model choice with a visible "cheap hands" badge** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: T-0755 asks whether Foreman can spawn lower-model agents. Per-call `model` and `effort` exist in Agent. Showing "scout·haiku" and "builder·sonnet·low" next to each lane in the pane makes the savings feel real.
  Done when: the fleet pane shows model and effort per live lane, and an S-tier lane passes `effort: low` on spawn.

- **Wild: Let the page talk back with "ask Claude" on any task card** — FEATURE — value 4 — effort M — risk med — category: artifacts, wild
  Why: the Artifact runtime can send "ask Claude" from the page. A button on each task card ("why is this blocked?", "split this") answers in place from the ledger, so the user never opens a terminal. Assumption: the CLI side can receive those calls while a session is live.
  Done when: clicking "why blocked?" on a blocked card returns a one-paragraph answer citing the ledger entry, and the exchange is stored on the task.

- **Wild: Turn the task into a trading-card receipt** — FEATURE — value 3 — effort S — risk low — category: delight, wild
  Why: the user shares Foreman results ("Release 1.2.27 to GitHub"). A one-screen Artifact card per finished task (title, tier, evidence count, the check that nearly failed, time saved) is something people screenshot.
  Done when: `fm task finish` offers a card URL, and the card renders without the ledger present.

- **Wild: Wake on a schedule with a bedtime story** — FEATURE — value 3 — effort M — risk med — category: scheduling, wild
  Why: CronCreate and RemoteTrigger exist unused. A cloud routine at 7am could review the repo's overnight CI and open issues, then push a one-line "good morning, 2 things look off" to the phone.
  Done when: a registered routine fires on schedule and produces a PushNotification with at least one real finding, or "all quiet" with a reason.

- **Wild: Give each subagent a nickname and a running joke** — FEATURE — value 2 — effort S — risk low — category: personality, wild
  Why: six subagents show up as ids in the pane. Stable, readable names ("Scout", "Nit" for the reviewer) that carry through ledger lines and the board make the fleet feel like a crew. Assumption: personality stays out of evidence text.
  Done when: every fleet line shows the agent's name, and the closed-out summary credits them, with a setting that reverts to plain roles.

- **Show findings in the host's own review UI** — FEATURE — value 3 — effort S — risk low — category: review
  Why: ReportFindings renders typed findings natively, and Foreman's reviewers currently write them as text. Native rendering makes the review step look first-class and clickable.
  Done when: a reviewer lane's findings appear through ReportFindings with file:line locations, and the ledger stores the same list.

- **Greet the session with a one-line resume that moves** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: after `/compact` or a new session the user wants to know exactly where it stopped. A SessionStart line like "T-0760 step 3/7 · last green: gate A · next: edit fmbus.py" replaces re-reading state.
  Done when: a new session in a project with an active task shows its step number, last evidence and next action in the first message, under 200 characters.
