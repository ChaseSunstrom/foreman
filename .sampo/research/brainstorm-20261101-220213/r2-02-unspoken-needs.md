# Brainstorm — lens: unspoken needs

- **Backfill the lean baseline over git history** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: T-2503 says growth waits as "pending" until a measurement exists, and the pack gives no baseline for code lines per module, hook p95 or injected bytes. Replaying `fm burden` and the size counts over past commits would give the ratchet a real previous generation on day one.
  Done when: `fm lean --history` prints per-generation code lines, test lines and verb count for the last 20 commits, and the sweep's lean row reads "measured" instead of "pending".

- **Name the commit that made it heavier** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: the pack shows hook p95 at 278 ms and 387k context per reply, but nothing says which change added them. assumption: weight rises in small steps no one notices.
  Done when: `fm lean blame` bisects a seeded hook slowdown or context growth to the task id that caused it, in a test.

- **Make "n/a" cells expire** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the steers say every Seed retries items a new capability may unblock, and an n/a is the easiest way to fill a cell. assumption: some of the 61 empty cells will be filled with n/a.
  Done when: each n/a cell stores a re-open condition, the sweep re-asks it after any capability is added, and a test shows an n/a turning red once its condition is met.

- **Turn rotted coverage cells red** — FIX — value 4 — effort S — risk low — category: coverage
  Why: the steer says a cell counts only if it names a concrete file or a real gap. A cell can stay green after its file is renamed or deleted. The pack's map is already "as of an older HEAD".
  Done when: deleting or renaming a file or test named by a cell makes `fm genesis sweep` flag that cell as stale, in a test.

- **Budget the tail, not only p95** — PERFORMANCE — value 4 — effort M — risk low — category: hooks
  Why: the pack reports p95 278 ms over 13533 runs, but a person feels the slow session start, not the median. assumption: p99 and cold-cache starts are much worse than p95.
  Done when: `fm doctor` prints p99 and cold-start time per hook event, and `bench_hooks.py` fails above a stated tail budget under a loaded-CPU run.

- **Quiet the injection when the session is plain chat** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: the SessionStart note is about 2k characters across 89 sessions, and context averages 387k per reply. assumption: many sessions never touch tasks or code.
  Done when: a session whose first prompts touch no repo or task gets only the guard line, and a test shows the injected bytes drop with the guard still firing.

- **Publish the guard's known gaps, each with a test** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: `core:interpreter-code-driving-foreman` blocked 42 times in a week, so the guard is the headline claim. A gap list the user can read tells them what bypass mode still lets through.
  Done when: a `guard-gaps` doc lists each uncovered case, and each entry has a test asserting the case is still uncovered or now blocked, so the list cannot go stale.

- **Run `fm doctor` in hostile environments** — SECURITY — value 3 — effort M — risk low — category: headless/server
  Why: the machine is a hardened-kernel Linux with a tmpfs home path. assumption: read-only HOME, noexec tmp and no network are where hooks and the guard silently degrade.
  Done when: a test runs doctor with a read-only state directory and a noexec temp directory, and the guard either works or says plainly that it cannot.

- **Budget idle cost and page weight on the web surfaces** — PERFORMANCE — value 3 — effort S — risk low — category: site, server
  Why: the surfaces list includes the web UI, the site and headless/server, but only hooks have a budget. assumption: an idle web UI process polls, and the site loads unneeded assets.
  Done when: a test fails above a set idle CPU and memory for the web UI, and above a set page bytes and a zero-third-party-request rule for `site/genesis`.

- **Show what the cold reads cost against what they caught** — PERFORMANCE — value 3 — effort M — risk low — category: lean
  Why: the steers require a Haiku read and a Sonnet fallback on every tower file, but no ratio of spend to defects is shown, and they are not measured as part of the lean cost.
  Done when: `fm cost --by-feature` lists tokens spent on cold reads and the FAILs that held up afterwards, per generation.

- **Give every capability a sunset clock at birth (wild)** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: wild. The steers say a capability must pay for itself or be cut, and only 5 of 1219 cards are used. Each new capability would register a review date and the measure that keeps it. The sweep would then queue the subtraction task itself.
  Done when: a capability added without a review date fails the sweep, and a test shows an expired one filing a keep-or-cut task.

- **Grow the coverage rows from what the user actually does (wild)** — FEATURE — value 4 — effort L — risk med — category: coverage
  Why: wild. The grid is built from the capabilities Foreman already knows, and the pack lists blind-spot asks the user had to make that nothing predicted. Mining the user's transcripts and shell history for actions with no row would catch the next one.
  Done when: `fm genesis grow --from-usage` lists actions that map to no row, each with an example from the user's own history, and filing one adds an empty cell.

- **Let a guard block quote the user's own steer (wild)** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: wild. The pack holds dated user steers behind the rules. A block that says "you set this rule on 2026-10-30, because…" and offers the safe command is easier to accept than one citing an internal rule id.
  Done when: a block message for a rule backed by a steer prints its date, the steer text and one safe alternative, checked by a golden test.

Next question: Which of the 61 empty cells cannot be measured by any existing signal, and what small instrument would each need before it can be filled without a template?
Next question: What does the user do in the first minute after a guard block, and does any surface make that minute shorter?
