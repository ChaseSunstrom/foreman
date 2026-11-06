# Brainstorm — lens: unspoken needs

- **Mine Foreman's own follow-up fixes as missed anticipation** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: pack evidence: T-2667 (`fm burden` missing SessionStart context) and T-2645's later doctor warning both look like second commits to a capability that had just landed. No idea in the list mines Foreman's own quick re-touches, only the user's hand edits. A follow-up task or commit that touches the same files within N days of a close gets labelled a "missed sibling" with its class, and the counts feed the intake checklist below.
  Done when: `fm outcomes --followups` lists at least the T-2645/T-2667 pairs from the repo history, each with a class label and the original task id.

- **Attach a generated implied-siblings checklist to every new verb, flag or gauge brief** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: many catalogue items exist as separate fragments: a MASTER.md anchor lint, an exit-code `Next:` line, a `--json` twin, a planted-defect test, a decider with a stated decision. None is composed into the brief at filing time. Assumption: the class lists come from the follow-up miner above.
  Done when: filing a task that adds a flag appends a checklist whose items each map to a runnable check, and `fm task finish` lists unticked items.

- **Book every anticipation as a sealed prediction with a recency baseline and a mute** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: the "Ideas so far" list has a dozen separate predictor ideas (n-grams, task-kind tables, pre-drafts, forecast bets). They lack one shared ledger, and Mission 7 is about anticipation. Each prediction gets an id, an expiry and a settle-by evidence query. `fm anticipate` reports hit rate against "the user repeats their last ask kind", and a kind that doesn't beat that baseline is muted.
  Done when: a muted kind produces no new predictions, and a test with a planted always-wrong predictor shows it muted after N settled misses.

- **Reopen an unattended decision when its premise changes** — FEATURE — value 4 — effort M — risk med — category: decisions
  Why: the steers say never block on the user and record the choice with `fm decide --kind costly`. Each such choice rests on a number, file, model ID or measurement that can later change, and nothing watches it. A `--premise` clause, such as a command whose output was true then, is rechecked at session start, and a flip files a reopen item.
  Done when: a test decision with `--premise "test -f X"` reopens after X is deleted, and the reopen names the original decision.

- **Diff host facts per session and probe on change** — FEATURE — value 3 — effort S — risk low — category: environment
  Why: the platform is Arch on a hardened kernel with a tmpfs working directory, and T-0325 needs a pacman package. A rolling distro changes python, git or the `claude` CLI between sessions without warning. Snapshot kernel, interpreter paths and versions, CLI version, tmpfs free space and mounts, then print only the diff at session start and run the hook smoke test when an interpreter or CLI changed. An optional pacman hook is a one-time user step. Assumption: Arch with pacman.
  Done when: faking a changed `python3 --version` makes the next session start print one "since last session" line and run the hook smoke test.

- **Forecast the date each hard cap will bind** — FEATURE — value 3 — effort S — risk low — category: capacity
  Why: the pack mentions a $200 budget, a 100-line pack digest, a 40-skill cap, ledger growth, tmpfs size, and the lean rule's caps. Existing ideas register the limits and test their edges, but none projects when each will be hit. Fit the slope from the ledgers and warn when the projected date falls within 14 days.
  Done when: `fm doctor` prints "cap X hits in ~N days" for a seeded fast-growing ledger and stays silent for a flat one.

- **Turn each left-over "Next question" into a zero-token probe or a filed experiment** — FEATURE — value 3 — effort M — risk low — category: brainstorm
  Why: the pack carries eight unanswered questions, and several are scriptable, such as which numeric defaults were never run against the user's history, or which unattended paths ran on a real clock. Each question gets a probe command, a filed experiment, or an explicit "unanswerable here" tag before the next round.
  Done when: the next pack's "Questions earlier brainstorms left" section shows each question with a status of answered, probe filed, or unanswerable, and none are silently carried.

- **Learn predictor rules from the asks that surprised the ledger** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: the "What earlier brainstorms missed" section has eight asks no idea predicted. When a user message arrives that the ledger could have predicted, write the smallest rule that would have fired and replay it on the past 60 days to count false alarms. Ship the rule only if it fires less than it hits. Assumption: enough past asks exist to replay.
  Done when: for one T-2659-class miss, a rule is generated and its replay shows hits and false alarms before it is accepted.

- **Wild: Add a frustration key that captures the state it was pressed in** — FEATURE — value 3 — effort S — risk low — category: felt cost
  Why: wild; the user's drops and steers show friction only after the fact, in prose. One keypress in the pane or web UI, or one `fm ugh` command, timestamps the screen state, the last three verbs and the last injected note, with no questions asked. Unspoken need: report the annoyance without having to articulate it. It feeds the felt-cost signals the catalogue already imagines.
  Done when: `fm ugh` writes a record containing the last three verbs, the active task and a ledger offset, and `fm friction` lists it.

- **Wild: Track asks that went quiet and check whether they were solved or abandoned** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: wild; the user's drops show some asks were re-grounded away, but an ask that was repeated three times and then never again is invisible. List such asks with the last task that touched them. Mark each as quietly solved, superseded or silently abandoned. Offer the abandoned ones once, in a single line.
  Done when: seeding a ledger with a repeated-then-silent ask makes `fm next --quiet-asks` list it with its classification.

- **Wild: Forecast the user's complaint a month ahead and score it** — FEATURE — value 2 — effort M — risk low — category: anticipation
  Why: wild; an existing pre-mortem idea covers the run, but nothing writes the user's own voice. A tool-less child sees only the closed-task titles and steers and writes a one-sentence complaint in the user's phrasing. Seal it, then settle it against the steers that actually arrive. Unspoken need: Foreman should hit the pain before the user has to name it.
  Done when: a sealed complaint is stored with an expiry, and `fm anticipate` reports whether any later steer matches it.

- **Stamp each filed item with the first-screen question it expects the user to ask** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: the user opens a slate line and wants one answer first. This is cheaper than a full pre-answer feature. Each item gets one predicted "so what does that change for me?" line, the answer drawn from the Done-when, and it's checked by a lint that the answer is not a restatement of the title.
  Done when: every filed item shows the line, and the lint rejects an item whose answer repeats the title.

Next question: Of the asks the user actually made in the last 30 days, how many were predictable from the preceding ledger by a simple recency or follow-up rule, and which ones were not?
Next question: Which silent behaviours of Foreman has the user never had to ask about, and would they notice if one broke?
