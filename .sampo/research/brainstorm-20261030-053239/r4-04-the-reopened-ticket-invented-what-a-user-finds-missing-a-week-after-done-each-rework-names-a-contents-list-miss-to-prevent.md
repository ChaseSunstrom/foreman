# Brainstorm — lens: the reopened ticket (invented): what a user finds missing a week after done; each rework names a contents-list miss to prevent

- **Mine the performance cliff at day 7** — FEATURE — value 4 — effort M — risk low — category: performance
  Why: assumption: the commonest week-later miss is a goal done on Foreman's small fixtures that is slow on the user's real repo (hooks over the bench gate, `fm map` on 50k files). Done-when only ran on toy state, so no row asked about scale.
  Done when: closing a goal that adds a hook or verb path runs it against a generated 10x state dir, and a goal with no scale row prints "scale row missing"; a test shows a 10x slowdown is caught.

- **Add a "second device" row to every contents list** — FEATURE — value 4 — effort S — risk low — category: devices
  Why: the pack's "thin so far" names devices; MUST says every surface, yet the user reopens for the phone, MCP or Desktop view. assumption: those are the commonest silent reopens.
  Done when: sealing a contents list without a row (or an explicit "n/a: reason") for each of CLI, Claude Code, fm code, MCP, other agents, Desktop, site fails `fm goal seal`.

- **Open a reopen ticket as a typed object with a miss class** — FEATURE — value 5 — effort M — risk low — category: reopen ledger
  Why: the user's asks T-2120..T-2127 were all repairs of earlier briefs that no brainstorm predicted; there is no record linking a rework to the contents row that would have prevented it.
  Done when: `fm goal reopen "<text>"` writes a ticket naming the goal, the missing row, and a class (surface, scale, day-2, docs, state-migration, cleanup); a test lists them per goal.

- **Name the missing row before fixing the reopen** — FEATURE — value 4 — effort S — risk low — category: reopen ledger
  Why: a rework fixed without adding its row repeats on the next goal. assumption: the fix is the only thing recorded today.
  Done when: `fm task finish` on a reopen-linked task fails until the goal's contents list gains the row or a "no row, because" line.

- **Run the day-2 persona before done** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: unit tests missed shapes the live run hit (a table-less seed). A scripted newcomer who runs the first five commands on a copy of the user's state finds what fixtures don't.
  Done when: a goal touching stored state runs an old-state fixture through `--help`, the new verb, and a lister; a missing lister entry fails the closing audit.

- **Budget the hook bytes per surface in the contents list** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: the ~10 KB hook preview cutoff and the bench_hooks gate are constraints that a goal-level card (re-injected each session) can silently break a week later.
  Done when: the goal card is capped by a test at a fixed byte size, and adding items sheds in a documented order instead of becoming a preview.

- **Cite the earlier reopens in the plan** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: Mission 3's eight satellites were each a separate user ask. Plan time can ask "what did the last three done goals need afterwards?"
  Done when: `fm goal plan` prints the miss classes of the last N reopens and each must be answered with a row or an explicit skip.

- **Hold done in a 14-day warranty with decay checks** — FEATURE — value 4 — effort M — risk med — category: lifecycle
  Why: assumption: "done" is final today; re-running done-when commands weekly would catch rot (a changed hook, a dependency) before the user does.
  Done when: a done goal's verify commands re-run on a schedule; a broken one reopens the goal with the failing criterion named, shown in a test with a mutated file.

- **Wild: Send a ghost newcomer in at day seven** — FEATURE — value 3 — effort L — risk med — category: exam
  Why: wild. A tool-less cold child reads only README and `--help` a week later, tries to use the finished capability, and every stumble becomes a candidate contents row.
  Done when: the ghost run on a finished fixture goal produces a list of at least one friction row, and none on a goal with complete docs.

- **Wild: Write the reopen the user will file before they do** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. At close, a cold model drafts three likely day-7 complaints in the user's own phrasing (drawn from their words above); each must be answered by a row or refuted by evidence.
  Done when: closing prints the three drafts with verdicts, and a seeded fixture goal missing a surface row gets that complaint predicted.

- **Wild: Keep a regret ledger of cut lines** — FEATURE — value 3 — effort S — risk low — category: reopen ledger
  Why: wild. A goal's cut list records scope dropped for time; when a reopen matches a cut line, it is marked regretted and raises that class's prior.
  Done when: a reopen matching a cut line links to it, and `fm goal regret` lists cut lines by later cost.

- **Add an output-for-scripts row to every new verb** — CLEAN — value 3 — effort S — risk low — category: devices
  Why: assumption: a week later users want `--json`, exit codes, and a pane line; the Mission 3 surface brief was a separate ask.
  Done when: a lint in `fm goal check` fails a new verb lacking `--json` and a documented exit code.

- **Measure the reopen rate per goal size** — PERFORMANCE — value 3 — effort S — risk low — category: metrics
  Why: without a rate, no one can tell whether the contents lists improve.
  Done when: the pane and site show reopens per finished goal, split by size, computed from the ledger in a test.

Next question: Which reopens are caused by the user changing their mind rather than by a missing row, and how does the ledger tell them apart?
Next question: Does a reopen's cost (tokens, user minutes) differ enough by class that the planner should spend its row budget unevenly?
