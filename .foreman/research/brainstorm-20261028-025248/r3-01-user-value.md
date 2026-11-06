# Brainstorm — lens: user value

- **Strike a line from a request before it runs** — FEATURE — value 4 — effort S — risk low — category: request intake
  Why: the user's asks often bundle several steps, and they later drop one ("dropped the RETRY_WATCHDOG step"). Striking one clause before the run costs less than undoing it after.
  Done when: a multi-clause request shows one line per clause, and striking one removes it from the queued task's acceptance checks.

- **Re-ask an answer whose code has since changed** — FIX — value 4 — effort M — risk low — category: blocked questions
  Why: a dropped item shows criterion 2 was pinned to a commit that predates the test fix that moved `build`. Answers go stale the same way once the code they describe changes.
  Done when: an answer recorded before a commit that touches its file is marked stale in `fm status`, and Foreman asks again with that diff attached.

- **Let a steer note reach the next step** — FEATURE — value 4 — effort M — risk med — category: live steering
  Why: the user steers by correcting course ("step 2 becomes the budget", "dropped the RETRY_WATCHDOG step"), but today those steers land only after a run ends. Assumption: steers can be read at a step boundary, not mid-tool.
  Done when: a note typed during a run appears in the next step's pack, and the journal records which step read it.

- **Show the approach the run rejected, one key to take it** — FEATURE — value 3 — effort M — risk low — category: decisions
  Why: the drops show the user often wants a different approach ("recreated with interpretation and approach", "redo: work done but criterion 2 was pinned"). The rejected path is the fastest route to that.
  Done when: the close receipt lists each rejected approach in one line with its reason, and its key restarts the task on that approach.

- **Cap interruptions per hour and park the rest** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: "dont ask me for anything either, I want any and ALL ideas implemented... just go". The user wants few interruptions, and a per-hour cap enforces that where a preference only hopes for it.
  Done when: with a cap of 2, the third question in an hour goes to the morning list, and the glance line says how many were parked.

- **Import TODO and FIXME comments as tasks in one pass** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: assumption: a repo's TODO comments are the user's own backlog written in place. The pack's backlog and the code's comments are not linked, so that work is invisible to Foreman.
  Done when: `fm import todos` lists each comment with file:line, and only the ticked ones become queued tasks.

- **Un-defer an item from the morning list with one key** — FIX — value 3 — effort S — risk low — category: deferrals
  Why: `fm task defer --until` already had a midnight bug that delayed items by hours. When a deferral is wrong, the user should undo it without finding the task id.
  Done when: pressing one key on a deferred item in the morning list clears its deferral and re-queues it, and the journal records the reversal.

- **Post a dollar bounty on a stubborn bug** — FEATURE — value 2 — effort M — risk med — category: wild incentives
  Why: wild: the user already accepts spend against outcomes ("Quote a queue's cost before it starts"). A bounty turns a hard bug into a priced task that runs under a hard cap, with the first passing proof claiming it.
  Done when: a $2-capped bounty stops at the cap, posts the spend on the receipt, and leaves the bug open.

- **Pick between two passing fixes by taste** — FEATURE — value 3 — effort M — risk low — category: wild review
  Why: wild: the pack already runs racing fixes in worktrees and keeps the smallest proven one. Two passing fixes can differ in style, which only the user can judge, and each pick teaches a per-user preference.
  Done when: when two fixes both pass the gate, the user sees both diffs side by side, the choice is recorded, and the next race prefers that style.

- **Let a teammate steer one run through a link** — SECURITY — value 2 — effort L — risk high — category: wild collaboration
  Why: wild: the pack lists a "remote drive" idea and a "read-only" teammate view. A steer link that is read-only until the owner grants it lets a second person help without gaining write access.
  Done when: a link with no grant can read the run's state but cannot post a steer, and a grant expires on its own after one run.
