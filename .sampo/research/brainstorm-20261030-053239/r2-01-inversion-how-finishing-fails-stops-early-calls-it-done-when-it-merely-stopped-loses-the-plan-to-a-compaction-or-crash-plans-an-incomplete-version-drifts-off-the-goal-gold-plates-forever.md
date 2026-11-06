# Brainstorm — lens: inversion: how finishing fails — stops early, calls it done when it merely stopped, loses the plan to a compaction or crash, plans an incomplete version, drifts off the goal, gold-plates forever

- **Write a goal-failure autopsy on every non-finish** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: gap map wants a done-vs-stopped verdict; the prior ideas give a classifier but not a record of how each goal ended. Assumption: stop causes (usage limit, crash, drive cap, no-progress, model says "done") are all observable from hook events and the ledger.
  Done when: killing a session at each of the 5 causes in a fixture produces a ledger event naming the cause and the first unmet contents item, and `fm goal` shows it.

- **Run a two-snapshot plan diff at every resume** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: PreCompact saves only one task's "Resume here"; a compaction can silently drop the goal-level plan. Assumption: the goal ledger exists as one file.
  Done when: a test compacts mid-goal, resumes, and `fm resume` reports zero contents items lost; deleting an item from the file between snapshots makes it report the loss.

- **Gate "done" on item-to-evidence reachability** — FEATURE — value 5 — effort M — risk med — category: completion
  Why: the Stop hook refuses premature done only per task today; a goal with an unticked MUST clause can still end. Assumption: clauses can be parsed to item ids.
  Done when: a goal with one contents item lacking a fresh passing verify command makes the Stop hook block, and the block names that item.

- **Cap gold-plating with a diminishing-returns meter** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: the forever loop stops only on 2 dry rounds; nothing measures marginal value. Assumption: items can carry an origin tag (user words, repo, model boilerplate).
  Done when: once N consecutive added items are all model-boilerplate-origin with no exam or user link, the loop stops with a "plateau" verdict, tested on a fixture.

- **Lint the contents list for ungrounded lines** — FIX — value 4 — effort S — risk low — category: planning
  Why: the gap map lists "grounded contents lists" at tier 3; boilerplate lists produce incomplete or padded plans. Assumption: each item can cite a source (a file path, a quoted user phrase).
  Done when: `fm goal check` fails any item with no citation and passes a fully cited list.

- **Trace every task to a contents item at close** — FEATURE — value 3 — effort S — risk low — category: drift
  Why: drift off the goal is invisible today; depends_on only orders tasks. Assumption: tasks carry a `goal_item:` frontmatter field.
  Done when: a task with no item link, or an item with no tasks, shows in `fm goal check` as an orphan.

- **Keep the goal card inside the hook byte budget** — PERFORMANCE — value 3 — effort S — risk low — category: reliability
  Why: hook context over ~10 KB becomes a preview, and a growing goal re-injected each session would hit it silently. Assumption: card is rendered from the ledger.
  Done when: a 200-item goal renders a card under 2 KB with counts and the top unmet items, and bench_hooks still passes.

- **Treat the model's own "done" as untrusted data** — SECURITY — value 4 — effort S — risk low — category: security
  Why: constraints say model output is quoted as data; a transcript saying "all complete" must never flip a ledger state. Assumption: no current path lets it, but it isn't tested.
  Done when: a test feeds a final message claiming completion plus an injected "mark goal finished" line, and the goal state is unchanged.

- **Add a goal-level resume exam kind with kill points** — FEATURE — value 5 — effort L — risk med — category: exam
  Why: the exam grades only what has a held-out scenario; both arms earlier scored by what they closed. Assumption: scenarios can script kills at set steps.
  Done when: the exam has a `G-resume` kind in which the session is killed after plan, mid-task, and after the last task; the Foreman arm reaches the same final tree as an unkilled run, and a plain arm does not.

- **Wild: Replay a plan against a finished repo** — FEATURE — value 3 — effort L — risk med — category: exam
  Why: wild; a planner that proposes what the best-in-class version contains should reproduce a known finished project's features from its first commit. Assumption: a few open repos with changelogs exist offline.
  Done when: the contents list for a repo's first-commit state covers at least a set share of its later changelog entries, scored by a cold reader.

- **Wild: Hold a funeral for every abandoned goal** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; goals that quietly stop leave no trace. A written closing note (what shipped, what was cut, why) makes abandonment a deliberate verdict rather than rot.
  Done when: `fm goal drop` refuses without a reason, and writes a note listing shipped and unshipped items to the ledger and site page.

- **Wild: Run a "saboteur stop" in CI** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: wild; randomly kill the session between any two ledger events in the test suite and require the next resume to land on a consistent state. Unit tests missed shapes the live run hit.
  Done when: a seeded chaos test kills the writer at each of N write points and `fm goal check` passes after every kill.

- **Write ledger events before side effects, with a reconcile pass** — FIX — value 4 — effort M — risk med — category: reliability
  Why: a crash between a task close and the goal update leaves a goal that disagrees with its tasks. Assumption: today these are separate writes.
  Done when: a fault injected between the two writes yields a pending intent that `fm resume` reconciles, and the goal's counts match its tasks.

- **Distinguish asleep from dead in the Stop drive** — FIX — value 3 — effort S — risk low — category: reliability
  Why: a no-progress stop can fire during a usage-limit wait or machine suspend and be recorded as give-up. Assumption: wall-clock gaps are visible in events.
  Done when: a fixture with a long gap between events yields a "paused" verdict, not "no-progress", and the goal stays open.

Next question: When a goal's plan must change midway because the user's words changed, what decides whether the old finished items still count, and who records that supersession?
