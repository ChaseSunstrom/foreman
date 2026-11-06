# Brainstorm — lens: grid

Grid used: surfaces are the web UI, the `fm` CLI and its `Next:` lines, session hooks and injected notes, the foreman-ui pane, and the Genesis site. Actors are the user, the builder agent, other agents (lanes and external harnesses), and the unattended drive. Failure modes are missing, wrong, slow, unsafe and unclear. These ideas go after cells the earlier list left thin, mostly where dissent scoring and Exam readings meet the user's own actions.

- **Censor dissent outcomes the user touched** — FEATURE — value 4 — effort S — risk low — category: dissent scoring
  Cell: dissent × user × wrong.
  Why: the pack's dissent score uses close survival over 14 days. A hand edit by the user after close looks the same as a failed close, so a dissent gets blamed or credited for the wrong cause. Assumption: hand edits are visible from git authorship or the "Learn from hand edits" signal.
  Done when: a fixture task edited by hand on day 3 is scored "censored", not "failed", and the count of censored dissents prints beside the score.

- **Make dissents against safety briefs need a second reader** — SECURITY — value 4 — effort S — risk low — category: dissent scoring
  Cell: dissent × builder agent × unsafe.
  Why: a scored dissent that says "skip it" can drop a guard or data-loss brief. Dropped FIX items already show Foreman closing items on a single argument. Assumption: briefs carry a kind or class tag.
  Done when: a dissent on a SECURITY-typed brief marks it "contested" and leaves it in the queue until a second cold reader agrees.

- **Capture a lane's disagreement as a dissent** — FEATURE — value 4 — effort M — risk low — category: lanes
  Cell: dissent × other agents × missing.
  Why: lane hand-backs say what landed, not "this brief was wrong". The pack shows dissents only from brainstorm lenses, so the most informed objectors (builders who read the code) are never scored. Assumption: the hand-back has a free-text field to parse.
  Done when: a lane hand-back with a `Disagree:` line files a dissent record that is later scored against that same task's outcome.

- **Mark Genesis site data as non-instructional for other agents** — SECURITY — value 3 — effort S — risk low — category: site hygiene
  Cell: Genesis site × other agents × unsafe.
  Why: `fm genesis live` publishes the user's steers and briefs verbatim, and external harnesses and crawlers read that page. Imperative lines in a steer ("keep going", "never block") could be obeyed by a visiting agent. Assumption: the pages are crawlable.
  Done when: each data block on the site carries a fixed "data, not instructions" wrapper, and a test fails when imperative steer text appears outside it.

- **Show a "cannot tell yet" verdict on the pane, separate from pass** — FEATURE — value 3 — effort M — risk low — category: pane
  Cell: foreman-ui pane × user × unclear.
  Why: the open T-0217 and T-1217 pile is already crowded with pane work, and pending-measurement rows are shown as "pending" in the sweep but not in the pane. Assumption: the pane can read the lean-row state.
  Done when: a brief whose Exam is unmeasured renders as a hatched row, and a screenshot test distinguishes it from a green one.

- **Give every `Next:` line a "what this will not do" tail** — FEATURE — value 3 — effort S — risk low — category: CLI clarity
  Cell: CLI × user × unclear.
  Why: T-2738 and T-2732 show printed commands whose effect or grammar surprised the user. A short tail ("won't push", "won't close the task") removes that class of ask. Assumption: each emitter knows its own effects.
  Done when: every `Next:` emitter in the verb table passes a lint requiring the tail, and `fm next` shows it.

- **Time every Exam reading against the unattended tick interval** — PERFORMANCE — value 3 — effort S — risk low — category: unattended
  Cell: Exam × unattended × slow.
  Why: the sweep runs readings in sequence and one hang blocks the tower. Existing ideas cap a reading but never compare the total runtime to the interval it must fit in. Assumption: the tick interval is configurable.
  Done when: filing is refused or warned when the summed reading budgets exceed half the tick interval.

- **Read each brief's file list back against the hook-injected notes** — FIX — value 3 — effort M — risk med — category: hooks
  Cell: hooks × agent × wrong.
  Why: the injected note can name a brief that a lane has already landed, and the agent then redoes it. Assumption: injection is built from the queue, not from the live tree.
  Done when: a planted already-landed brief is dropped from the injected note, and the drop is logged.

- **Record which grid cell each typed user ask landed in** — FEATURE — value 4 — effort M — risk low — category: coverage
  Cell: web UI/CLI × user × missing.
  Why: "Score each cell by typed asks" is proposed, but the lens also needs the reverse. The "What earlier brainstorms missed" list shows eight asks that fit no cell label, so the grid has no home for them. Assumption: asks can be matched to cells by title words.
  Done when: asks that match no cell are listed as "orphan asks" in the sweep, with a count.

- **Wild: Hold a one-minute "stranger's morning" screen test** — FEATURE — value 3 — effort M — risk low — category: delight
  Cell: all surfaces × user × unclear. Wild.
  Why: a cold child sees only the pane and the Mission page and says what it thinks happened overnight. The result is diffed against the ledger. This extends the pack's cold-reader habit to the display itself.
  Done when: the child's one-paragraph summary scores at least 4 of 5 key facts against a seeded night.

- **Wild: Let the dissenter's record choose the next lens count** — FEATURE — value 3 — effort M — risk med — category: brainstorm
  Cell: dissent × unattended × missing. Wild.
  Why: lenses whose dissents were right more often get more budget next Mission, and lenses that were always wrong get fewer. Assumption: at least 20 scored dissents exist, so the signal is not noise.
  Done when: the next Mission's lens list shows its weights and the dissent hit rate each one came from.

- **Wild: Play the Mission back as a seven-second changelog frame** — FEATURE — value 2 — effort M — risk low — category: delight
  Cell: pane × user × slow. Wild.
  Why: reading the full Mission page takes minutes. A short animated frame shows cells turning from empty to filled and the dissents tipping, which lets the user see the shape without opening anything. Assumption: terminal motion is allowed and reduced-motion is respected.
  Done when: the frame renders from the Mission file alone and is static under `NO_COLOR` and reduced motion.

Cells left empty:
- **Web UI × user × missing:** the earlier list already holds a dissent shelf, a stale badge and a cell board.
- **Unattended × unsafe at the guard:** many earlier ideas on capability tokens and sandboxing already cover it.
- **Site × user × slow:** the site is static, so latency is not a real failure here.

Next question: which cell of the grid has had the most typed asks while no brief has ever been filed against it?
Next question: when a dissent is censored because the user touched the work, does the user's edit mean the brief was wrong or merely incomplete?
