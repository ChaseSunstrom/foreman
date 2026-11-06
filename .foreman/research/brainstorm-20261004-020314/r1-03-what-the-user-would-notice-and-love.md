# Brainstorm — lens: what the user would notice and love

- **Lint every verify command when the brief is written** — FIX — value 5 — effort S — risk low — category: intake
  Why: the log shows two steered corrections, "fm research has no list verb" and "run.py takes -k, not a positional". Bad verify commands get found only after a step has been spent on them.
  Done when: a criterion whose verify names a nonexistent fm verb, flag, or test path is flagged at `fm task new` with the nearest valid form.

- **Suggest the nearest command on any fm typo or wrong flag** — FEATURE — value 4 — effort S — risk low — category: CLI ergonomics
  Why: the stranger-test item is queued because newcomers stall on wrong commands, and argparse errors are terse.
  Done when: `fm tsk new` and `fm research list` each print "did you mean …" plus the one-line usage, and exit non-zero.

- **Ping me only when you need me** — FEATURE — value 5 — effort M — risk low — category: notifications
  Why: the drive runs long, and the user steps away (night shift and morning report are both on the list). Today they have to watch for the moment it needs a real decision or an approval. Assumption: the platform has a desktop notification path (notify-send or a terminal bell).
  Done when: a drive that hits an approval or a decision rings or notifies once, with the question text, and stays silent on routine progress.

- **Park questions with a default and a timeout** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the drive stalls on questions when the user is away. Full autonomy exists but is all-or-nothing.
  Done when: a non-risky question is queued with a recommended default. If unanswered after N minutes the default is applied and recorded via `fm decide`, and `fm next` lists what was auto-chosen.

- **Learn standing answers from repeated replies** — FEATURE — value 4 — effort M — risk low — category: preferences
  Why: the user's corrections and steers repeat, such as "never X" and re-tiering. Foreman already turns "never" into a veto but doesn't notice "you've said yes to this 4 times".
  Done when: after the same question kind gets the same answer three times, Foreman offers "make this standing?", and on yes it stops asking and cites the rule.

- **Show task progress in the Claude Code status line** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: the pane needs the UI mod. Assumption: the status line is a script hook that other clients can use too. A compact `fm statusline` would reach everyone.
  Done when: `fm statusline` prints something like `T-0264 M step 3/5 · 2/4 criteria green · $1.20` in under 50 ms and updates as evidence lands.

- **Add tab completion with live task IDs and verbs** — FEATURE — value 3 — effort S — risk low — category: CLI ergonomics
  Why: IDs like T-0248 and T-0259 are typed constantly, and the verb tree is large.
  Done when: `fm tour T-02<TAB>` completes from real briefs in bash and zsh, and a test checks the generated script.

- **Wild: Shrink a failing gate to its smallest repro automatically** — FEATURE — value 4 — effort L — risk med — category: debugging
  Why: gate failures, flaky tests, and "passed for the wrong reason" guard tests all cost the user reading time. Delta-debugging the failing test or input down to the minimum, then attaching it to the hypothesis ledger, would feel like magic.
  Done when: a seeded failing test with a 40-line input is reduced to at most 5 lines, and the reduced case is recorded as evidence on the task.

- **Wild: Let the user pick Foreman's voice** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: nobody asked, but the pane, nudges, and receipts are read all day. A setting for terse, deadpan foreman, or chatty would be something people screenshot. Done reports must stay factual in every voice.
  Done when: `fm config voice deadpan` changes the phrasing of nudges and the close message in the pane and CLI, and a test confirms the evidence lines are byte-identical across voices.

- **Wild: Attach a replayable terminal cast of red to green to the proof pack** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: `fm proof` and `fm pr` list the criteria runs as text. A recorded cast of the verify commands failing, then passing, makes a PR reviewer believe it in 10 seconds. Redact secrets and paths, since exports are a known privacy gap.
  Done when: `fm proof ID --cast` writes a small cast file or self-contained HTML replaying the first red run and the final green run, with paths redacted.

- **Wild: Offer a "show me" mode that replays any finished task as a 60-second narrated walkthrough** — FEATURE — value 3 — effort L — risk med — category: handoff
  Why: `fm tour` gives the reading order and `fm proof` gives the evidence. Neither plays the story of what was tried, what surprised Foreman, and what was decided, which is what a returning user wants.
  Done when: `fm show ID` prints a chronological digest of at most 40 lines that is assembled only from ledger entries (hypotheses, surprises, decisions, evidence), with each line citing its entry.
