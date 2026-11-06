# Brainstorm — lens: bold bets

- **Compile each task's verify commands into a pre-edit "tripwire" suite** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: 32 evidence runs vs 13 finishes suggests verify commands are run late. Running them red at focus and green at done turns every brief into an executable spec; failures at focus prove the check can fail.
  Done when: `fm task focus` records a red/green baseline per criterion and `fm task finish` refuses a criterion whose check was never red (unless marked "already true").

- **Make the drive loop a state machine with a stop-reason taxonomy** — FIX — value 4 — effort M — risk med — category: drive
  Why: pack shows drive stops for mod reloads (5) and background waits (7) in one window, and a dropped "reload resume lost in a race" task. Enumerate legal stop reasons (user question, budget, real block) and treat any other stop as a bug that auto-resumes and logs itself.
  Done when: a replay of the last session's stops shows zero unclassified stops, and a test injects a reload and a background completion in the same second and the drive resumes.

- **Detect "pushback echoes" and turn them into render fixtures automatically** — FEATURE — value 5 — effort M — risk low — category: user-feedback
  Why: the user's words repeat one complaint across rounds (unpanelled rows, duplicated dashboard, diff contrast, unanimated `$`). Each was fixed ad hoc and then re-raised. A capture that tags a complaint with the row kind it names and writes a golden-frame fixture stops the same class from returning.
  Done when: capturing "my messages aren't panelled" creates a failing fixture for that row type, and the fix commit turns it green.

- **Add a single `fm status --since-away` return card with cost, changes and asks** — FEATURE — value 4 — effort S — risk low — category: return-UX
  Why: usage-sensitive user, unattended drive runs, and "don't stop until complete" imply long absences. assumption: no one-screen summary of spend, repo changes and pending yeses exists.
  Done when: after a simulated 2 h gap, the first reply shows one panel listing tokens spent, commits made and open questions, in under 12 lines.

- **Pin a per-session token ceiling that downshifts ceremony and subagent fan-out** — FEATURE — value 5 — effort M — risk med — category: budget
  Why: one session burned 20% of weekly quota. Budget ideas exist as ledgers and warnings, but none acts. A ceiling that automatically drops audit lenses, parallel lanes and brainstorm rounds, and says so in one line, converts awareness into protection.
  Done when: with a ceiling set low in a test fixture, `fm run --parallel 4` refuses to exceed it and the audit uses one lens, each logged.

- **Auto-bisect the guard when `fm replay` flags a verdict change** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: replay reports verdict changes but leaves attribution manual. Reapplying the guard commit by commit names the one that flipped it.
  Done when: a seeded regression yields "verdict changed at commit X for command Y" without manual steps.

- **Wild: Run a nightly "shadow user" that replays the user's past complaints as prompts against the candidate build** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: wild. The recursive self-improvement ask lacks ground truth. Real complaints are the best held-out test set, scored by a read-only judge subagent on the transcript.
  Done when: a candidate build gets a pass/fail score per past complaint, and a release is blocked when a previously fixed one regresses.

- **Wild: Let Foreman hold a "demo day" that renders each finished task as a 10-second animated panel strip** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The user cares about animation and panel polish. A replay of brief → evidence → green gate in the mod's own style makes progress visible without reading text.
  Done when: `fm demo T-NNNN` plays the strip in the pane and exits cleanly on any key.

- **Wild: Have the self-improvement loop propose deleting one feature per pass, graded by usage** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: wild. Usage shows skills never invoked and 46 of 46 playbooks unread, while the ideas list keeps adding. A forced one-in-one-out budget keeps Foreman from growing past its token-efficiency goal.
  Done when: each friction pass emits a deletion candidate with its 30-day usage count, and the queue accepts it as a CLEAN brief.

- **Wild: Make Claude's own idle waits productive by pre-running the next step's read-only exploration in a cheap scout** — PERFORMANCE — value 3 — effort L — risk med — category: speed
  Why: wild. Time split shows model 55% and shell 45%, with Read filling 59% of context. A scout that outlines likely files while gates run could cut first-action latency, if its output is discarded unless used.
  Done when: on a replayed task, time-to-first-edit drops measurably versus baseline with no added context when the scout output goes unused.
