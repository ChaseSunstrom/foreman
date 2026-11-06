# Brainstorm — lens: delight

- **Show a lean weigh-in receipt on every task close** — FEATURE — value 4 — effort S — risk low — category: lean delight
  Why: pack measures hook p95 278 ms, 387k context per reply, and the lean ratchet exists, but the user only sees it in `fm doctor`. A one-line "this task cost +0 ms hook, −3 verbs" at close makes leanness felt. Assumption: the finish receipt already has a place for a footer line.
  Done when: `fm task finish` prints a line with hook p95 delta, injected-bytes delta and verbs added/removed, and a test pins its format.

- **Make every guard block teach the safe command** — FEATURE — value 5 — effort M — risk low — category: guard UX
  Why: "core:interpreter-code-driving-foreman blocked 42x in 7 days" shows a repeated block. A refusal that ends in one runnable alternative turns a stop into a nudge.
  Done when: the top 10 block reasons by count each print a "run this instead:" line, and a test fails if a block reason lacks one.

- **Give the guard a one-keystroke false-positive report** — FIX — value 4 — effort S — risk low — category: guard UX
  Why: 2 brief-guard false positives (a dict key and a `.join(` call read as written paths) are known. A `fm guard wrong` that saves the last blocked input into a corpus fixes them and prevents the next.
  Done when: `fm guard wrong` appends the last block's input to a corpus file, and both known false positives are fixtures that pass after a fix.

- **Fix the brief-guard path false positives with a real shell tokenizer** — FIX — value 4 — effort M — risk med — category: guard accuracy
  Why: the pack names the two misreads directly.
  Done when: the dict-key and `.join(` fixtures no longer block, and the existing deny corpus still blocks.

- **Add a weight-class gauge to the pane and status line** — FEATURE — value 3 — effort M — risk low — category: motion/UI
  Why: lean is invisible; a small gauge (hook ms, bytes injected, against budget) that eases on change makes the budget a thing people watch. Assumption: the foreman-ui pane can take one more row.
  Done when: the pane shows a gauge row reading from fm doctor data, and a screenshot test shows it at under and over budget.

- **Give the SessionStart note a diet: hash first, delta after** — PERFORMANCE — value 4 — effort M — risk med — category: context size
  Why: "SessionStart note ~2k chars x 89" is repeated cost. Injecting a hash plus only what changed since the last session cuts it.
  Done when: a second session start in an unchanged repo injects under 300 chars, and the first still injects the full note.

- **Print the guard's weekly save in plain words** — FEATURE — value 3 — effort S — risk low — category: guard story
  Why: block counts exist in `fm friction`, but "stopped 42 interpreter-driven Foreman calls, 0 you overrode" is the line people show others.
  Done when: `fm doctor --week` prints a sentence per top block class, fed from the real block log.

- **Celebrate a deletion with a receipt** — FEATURE — value 3 — effort S — risk low — category: lean ratchet
  Why: gen-0 §6 demands subtracting as you add, yet nothing rewards it. A "removed 4 verbs, 1,200 lines" receipt makes subtraction visible.
  Done when: a task whose diff nets negative lines prints a deletion receipt at finish, and a test covers the threshold.

- **Shelve stack cards nobody loaded** — CLEAN — value 3 — effort M — risk low — category: library diet
  Why: "5 of 1219 stack cards used". A cold shelf with on-demand load keeps the library without the weight.
  Done when: cards unused for 90 days move to a cold index, `fm lib show NAME` still finds them, and the shipped file count drops.

- **Run a diet week mode** — FEATURE — value 3 — effort M — risk med — category: lean experiment — wild
  Why: assumption: disabling one optional hook per day and reporting what nobody noticed gives evidence for the "capability pays for itself or gets cut" rule. wild.
  Done when: `fm diet start` disables one optional hook daily for 7 days and the end report lists correction counts per day.

- **Publish a guard playground on the site** — FEATURE — value 3 — effort L — risk med — category: site — wild
  Why: assumption: a visitor pasting a command and seeing allow/deny with the rule that fired is the most shareable proof the guard is real. Runs client-side on a compiled rule table. wild.
  Done when: the Genesis site page returns the same verdict as `fm guard check` on 20 corpus commands.

- **Run a lean twin on the same task** — FEATURE — value 4 — effort L — risk med — category: proof of weight — wild
  Why: assumption: showing the same small task with hooks on and off, with time and tokens side by side, answers "is Foreman worth its weight" in one screen. wild.
  Done when: `fm twin TASK` produces a two-column cost and time table from two real runs.

- **Add a "how heavy is my Foreman" card to the Genesis page** — FEATURE — value 3 — effort S — risk low — category: site
  Why: the standing rule publishes Genesis data to main; a lean card fed by `fm doctor` JSON keeps claims tied to the command that made them.
  Done when: the page shows hook p95, context per reply and verb count with the producing command beside each, matching `fm doctor`.

- **Add a "since you left" lean line on resume** — FEATURE — value 2 — effort S — risk low — category: resume
  Why: assumption: a one-line note ("hooks +12 ms since Tuesday, 2 blocks") makes drift felt early.
  Done when: first prompt after 24 h idle includes the line and it stays under 120 chars.

Next question: Which of the lean and safe signals does the user actually look at today, and does any of them change what they do next?
Next question: Where does the guard feel hostile rather than protective, and can the 42 repeated blocks be traced to one missing habit or verb?
