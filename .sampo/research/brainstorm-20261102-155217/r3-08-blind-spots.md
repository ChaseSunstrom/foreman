# Brainstorm — lens: blind spots

**Blind-spot ideas (round 3)**

I'm asking one question of the whole project: where does Foreman state something confidently that nothing re-checks? The listed asks (T-2659, 2667, 2668, 2669 and the steered 7-vs-8-characters one) are all of that kind. The earlier rounds already cover gauges, channels, caps and latency, so these ideas sit beside them or build on them.

- **Run the `fm` commands quoted in skills against a scratch home** — CLEAN — value 3 — effort M — risk low — category: doc drift
  Why: assumption: `plugin/skills/` holds 1388 files, and the pack shows README and MASTER fenced blocks being checked but not skill bodies. Skills are what sessions actually read, so a renamed flag silently misleads the model.
  Done when: a test extracts every `fm …` line from skill files, runs each with `--help` or `--dry-run` in a temp home, and fails on any unknown verb or flag. A planted dead flag in one skill proves it.

- **Lint a new brief against the other open briefs for contradictions** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: the pack's own ideas conflict. "Print one next command on every nonzero exit" and "Print N left out" both add output, while another idea caps default output at ten lines. Only briefs against steers are checked today.
  Done when: filing a brief that says "cap output at 10 lines" while an open brief adds a per-list overflow line prints the conflicting task id and exits nonzero unless `--ack`.

- **Fold co-filed same-file briefs into one task with a checklist** — CLEAN — value 3 — effort S — risk low — category: queue shape
  Why: c13–c24 arrived as 12 separate M-sized asks. Four were dropped or re-scored after re-grounding, and several touch fmcli, doctor or drill.
  Done when: when two or more new briefs from one catalogue touch the same file, `fm next` offers one parent task whose checklist lines map to the original ids.

- **Revert-replay every FIX commit's test** — FEATURE — value 4 — effort M — risk med — category: test honesty
  Why: the burden fix (T-2667) and the criterion-arithmetic fix show that tests can pass while checking the wrong thing. Only a revert tells you the test bites.
  Done when: `fm audit-fixes` takes the last N FIX commits, reverts only their non-test hunks in a temp worktree, and lists any commit whose new test stays green.

- **Keep a durable blind-spot question bank that every lens must answer** — FEATURE — value 4 — effort M — risk low — category: brainstorm
  Why: each miss (T-2659 to T-2677) produced a one-off question, and there is no file that keeps them. The "Next question" lines get lost between rounds.
  Done when: `fm ideas` loads `blind-questions.md`, each lens output ends with a yes/no line per question, and a missing line fails the lens as incomplete.

- **Tag every filed item with which brainstorm question would have caught it** — CLEAN — value 2 — effort S — risk low — category: provenance
  Why: assumption: the pack separates "asked" from "slate-origin" only by hand. Without the tag you cannot tell whether the question bank above shrinks the miss rate.
  Done when: `fm task add --missed-by <question-id>` stores the tag, and `fm digest` prints the miss count per question id for the week.

- **Quarantine "dropped with a noted remainder" into a visible one-line shelf** — FIX — value 3 — effort S — risk low — category: dropped work
  Why: the drops for c16, c17 and c21 each name a real remainder (decide() not booking a None answer, a 60-day window under `fm tidy`). That text sits in a steer line and no queue holds it.
  Done when: `fm next --remainders` lists each noted remainder with its source task, and closing or re-dropping one removes it.

- **Check at close that a gauge's own test would fail on the unit it replaced** — FEATURE — value 3 — effort M — risk med — category: measurement
  Why: the 8+/7-character slip and the burden channel miss are both an instrument and its example disagreeing. This is a stricter, test-time form of the criteria lint.
  Done when: a gauge task cannot close until a test feeds the old definition's output and asserts the new reader differs; a planted unchanged reader fails the close.

- **Wild: pay a different-vendor model to find gaps from `fm --help` alone** — FEATURE — value 3 — effort M — risk med — category: outside view — wild
  Why: the standing rule asks for signals Foreman didn't author, and `--help` is the product's first impression. The child sees no code, only help text and a goal sentence.
  Done when: the child lists 10 things a user would expect, and `fm exam` scores how many have a verb or are filed. The run prints the score per round.

- **Wild: audit the user's 90 days of asks for needs no slate item ever mentioned** — FEATURE — value 4 — effort M — risk low — category: unspoken needs — wild
  Why: it measures the real blind-spot rate: the share of asks whose nearest prior idea is weak. It also answers the left question about how much of the catalogue the user actually felt.
  Done when: a tool-less child clusters the asks, and `fm ideas --orphans` prints the fraction with no related earlier idea plus three examples.

- **Wild: plant a wrong fact in a skill each week and time its discovery** — SECURITY — value 3 — effort S — risk low — category: tripwire — wild
  Why: skills and steers are read confidently by sessions and by Genesis cold reads. Nothing shows whether a false line there would ever be caught.
  Done when: a weekly job inserts a labelled falsehood in one scratch-copy skill and records whether a cold read, a session or `fm doctor` flags it within seven days, with the result in `fm digest`.

- **Check which side wins when hand edits and Foreman edits meet, per file class** — FIX — value 4 — effort M — risk med — category: precedence
  Why: this is an open left question ("which side does each reader trust?") and no listed idea defines the rule for the task queue file, tower files and ledgers one by one.
  Done when: a precedence table in MASTER.md names the winner per file class, and a test edits each class by hand and by `fm` then asserts the documented winner.

Next question: which of the ideas the user accepted have since been touched by the user's own hand (edited, reverted, or re-run manually), and what would that say about which gaps were real?
Next question: what do the 12-item batch accepts (c13–c24) say about how the user triages, and does the slate format fit that?
