# Brainstorm — lens: approaches

- **List the co-changers that did not change** — FEATURE — value 4 — effort S — risk low — category: left-out
  Why: assumption: git history already says which files move together, and nothing in the pack uses it to say what a Mission left out. A diff that touches A but not B, when B changed with A in most past commits, is a cheap and checkable gap.
  Done when: on a fixture repo where B changed with A in 8 of the last 10 commits, a change to A alone makes the left-out slip name B. A change to both files names nothing.

- **Score request coverage with the steer-expansion judge** — FEATURE — value 4 — effort M — risk low — category: reuse
  Why: `fm exam steer` (T-2625) already does the same job for steers. It expands the raw words, a judge one rank up counts only quoted clauses, and a third of the cases are held out. Pointing it at a Mission's request means "exhaustive" gets scored by a tool that is already built and not by the planner's own list.
  Done when: a request with one clause removed from its Mission page reports that clause as uncovered, quoting the request. The unmodified page reports none.

- **Check the three carried gaps in `fm genesis check`, with no new verb** — CLEAN — value 4 — effort S — risk low — category: do less
  Why: the checker already has mix, kill-result and measure rows. A row that parses each brief's Exam for an outcome line and a live-state line is the least machinery that closes the gap. Fewer new surfaces means less to maintain.
  Done when: a brief file with the Exam missing either line fails `fm genesis check` naming the file and the missing line. A brief with both passes.

- **Hold a dissent as "pending measurement" until its outcome exists** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: the lean-substance rule (T-2503) already has a state that is neither red nor a task, used when no measurement exists yet. A dissent whose outcome has not been observed needs exactly that, so it is neither scored nor dropped. The trade-off is that dissents can sit pending forever unless a deadline is added.
  Done when: a dissent filed today shows pending in the sweep, creates no task, and flips to scored when its brief's outcome line returns a value.

- **Join the diff to the tests→src map to name untested blast radius** — FEATURE — value 3 — effort S — risk low — category: grounding
  Why: `fm map` already carries tests→src, and a Mission's briefs name the files they change. Source modules in that set with no mapped test are left-out cells that need no model to find. Assumption: the map is fresh. The pack says it was taken at an older HEAD.
  Done when: a fixture brief touching a module with no mapped test lists it on the slip. A fully mapped module lists nothing.

- **Record thinking spent per grid cell** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: assumption: child transcripts carry usage, as `fm burden` already reads. A cell that received a tenth of the median thinking is "touched" but not covered, and a filled cell cannot show that today.
  Done when: the slip shows tokens per cell and flags any cell under 10% of the median as thin, on a recorded run.

- **Ablate each brief and read the Exam** — FEATURE — value 3 — effort M — risk med — category: grounding
  Why: a brief whose removal leaves every Exam reading unchanged either does nothing or is unmeasured. This is the brief-level counterpart of the clause-ablation idea for requests. The cost is one scratch worktree per brief.
  Done when: reverting a planted do-nothing brief in a scratch worktree reports "no reading moved", and reverting a real brief reports which reading moved.

- **Build the dissent as an unapplied shadow patch** — FEATURE — value 3 — effort L — risk med — category: dissent
  Why: scoring words after the fact is vague. If the dissent becomes a patch plus its own Exam reading, the comparison is two numbers on the same measure. The trade-off is real build effort for every dissent.
  Done when: one dissent filed with a shadow patch shows two Exam readings side by side, the applied one and the shadow one, with the reading command identical.

- **Send the left-out slip as a mail reply the user answers one word per cell** — FEATURE — value 2 — effort M — risk med — category: devices
  Why: assumption: the mail intake path from T-0827 exists, and the phone is where a user triages away from the terminal. It is outward-facing, so it needs an explicit setting and a local-only default.
  Done when: with the setting on, a slip with three cells is delivered to a local test mailbox. A reply of "1 yes 2 no 3 later" files one task and drops one cell. With the setting off, nothing is sent.

- **Run a hidden twin Mission on the left-out list (wild)** — FEATURE — value 4 — effort L — risk med — category: unattended
  Why: wild: each Mission's left-out list becomes the request of a second Mission, run on idle quota at a tenth of the budget. The twin's briefs are shown only if the user's next ask lands in one of its cells. Measuring whether left-out items turn out to matter is the same work as measuring exhaustiveness.
  Done when: a closed Mission spawns a twin whose briefs stay hidden in a file. The next typed ask is matched against them and a hit or miss is recorded.

- **Round-trip the request through a paraphrase to find its ambiguity (wild)** — FEATURE — value 3 — effort M — risk low — category: ambiguity
  Why: wild: a tool-less child restates the request in a different form, such as a formal predicate or a plain-words sentence. A second child restates that back. Where the meaning drifts is where scope is ambiguous, and the drift costs two small calls.
  Done when: a request with a planted ambiguous word, such as "exhaustive", yields a drift report naming that word, and an unambiguous request yields none.

- **Draft the next Mission's request in the user's own voice (wild)** — FEATURE — value 3 — effort M — risk low — category: unspoken needs
  Why: wild: the user already types near-identical Mission requests ("Mission N (gen G, #K): brainstorm, ground and file…"). The highest-sting left-out cell can be phrased that way and filed as a draft they accept with one word.
  Done when: at Mission close a draft request in the repeated phrasing appears, quoting the cell, and accepting it files exactly one task.

Next question: which of the three carried gaps would the user notice missing first, given that dissent scoring has no observed outcome yet while the Exam lines are checkable today?
Next question: of the briefs already filed under gen 3, how many have a live-state reading that runs cold, meaning a read-only `--json` verb over ledgers, and how many need session state?
