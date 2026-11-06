# Brainstorm — lens: user value

- **Print a behaviour changelog once after each Foreman update** — FEATURE — value 4 — effort S — risk low — category: upgrade trust
  Why: the user found `fm` not recognised after a symlink change (2026-10-20), and a defer that landed at midnight. Both changed behaviour they only noticed when something broke.
  Done when: after an upgrade, the first `fm` call prints the changed behaviours once, and `fm whatsnew` lists them until dismissed.

- **Preview the exact pack a paid run will send, and drop a section before it goes** — FEATURE — value 5 — effort S — risk low — category: token cost
  Why: the user had to ask for context-per-reply measurement and a 200k compact to cut burn. A preview lets them see what a run costs before it sends.
  Done when: `fm run --preview` prints bytes and estimated tokens per section, and removing one section lowers the sent total.

- **Turn a plain sentence into the fm command it means, echo it, and run on one key** — FEATURE — value 4 — effort M — risk low — category: plain requests
  Why: assumption: the user phrases work in prose ("defer till the reset", "press g during a run") while fm has many verbs and flags. Showing the mapping lets them catch a wrong reading before it runs.
  Done when: "defer this to the reset" shows `fm task defer <id> --until reset` before it runs, and an unmatched sentence returns the three closest verbs.

- **Park a stray thought mid-run without touching the queue** — FEATURE — value 3 — effort S — risk low — category: capture
  Why: the user asks for every idea, yet a new one arriving mid-run can derail the current task. A parking lot keeps the thought without changing the queue.
  Done when: `fm note "…"` during a run adds one line to the parking lot, and the queue, the run and its proof log are unchanged.

- **Answer "why did you do that" for any single edit from its recorded reasons** — FEATURE — value 4 — effort M — risk med — category: explain
  Why: the pack asks for run explanations (T-1373, `fm code why`), but the reason behind each edit is lost when the run ends. Per-edit answers would extend that.
  Done when: `fm why <step>` prints the reason and evidence recorded for that edit, or says "no reason recorded" rather than guessing.

- **Carry the user's standing choices in a profile they can copy to another machine** — FEATURE — value 3 — effort S — risk low — category: portability
  Why: assumption: choices such as "don't ask me" and builders on Sonnet live per machine and would be lost on a new box.
  Done when: `fm profile export` writes one file, and `fm profile import` on a clean install reproduces the same settings and lists any it could not apply.

- **Answer a side question during a run from a read-only fork, without pausing the work** — FEATURE — value 4 — effort M — risk low — category: interruption
  Why: the user pressed `g` mid-run and had to wait for it to finish (T-1779). A read-only fork lets a question get an answer while the run keeps going.
  Done when: a question asked mid-run gets an answer, and the run's journal shows no new edits from the fork.

- **Write a morning confession: one mistake Foreman made overnight and what it changed** (wild) — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild: the user said Foreman should have caught its own usage burn unprompted. A plain one-line account of each slip, with the fix, shows that it is paying attention.
  Done when: after any run with a retry or rollback, the morning note has one line naming the slip and the change made.

- **Count the hours of the user's typing each week that Foreman saved** (wild) — FEATURE — value 2 — effort S — risk low — category: value proof
  Why: wild: assumption: the user may measure value in their own time, not in budget. Per-task dollar and token figures are already planned, so an hours figure is a different lens.
  Done when: `fm week` prints an estimated hours-saved figure with its method (keystrokes avoided at a stated rate) and labels it an estimate.

- **Seal the one question a stuck run could not answer into a note to open later** (wild) — FEATURE — value 3 — effort S — risk low — category: unblock
  Why: wild: a stuck run currently ends in a status line, so the user has to read a log to find what it needs. One sealed question gives them a single thing to answer.
  Done when: a run that stops on an unanswerable question writes exactly one question to the note file, and `fm status` shows it once.
