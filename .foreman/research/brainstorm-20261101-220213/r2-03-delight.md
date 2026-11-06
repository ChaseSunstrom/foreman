# Brainstorm — lens: delight

- **Show the lean weigh-in as a receipt on every task close** — FEATURE — value 4 — effort S — risk low — category: lean/receipts
  Why: pack measures hook p95 278 ms, 387k context per reply, SessionStart note ~2k chars x 89, but the user only sees these in `fm doctor`. A one-line "this task cost X ms of hooks, Y bytes of injection, net lines +N/-M" on the finish receipt makes leanness felt.
  Done when: `fm task finish` output ends with a weigh-in line whose three numbers match `fm friction`, `fm cost` and `git diff --stat` for that task, tested on a fixture task.

- **Celebrate a deletion with a deletion receipt** — FEATURE — value 3 — effort S — risk low — category: lean/motion
  Why: gen-0 §6 says "subtract as you add", and T-2503 only files subtraction tasks as penalties. Nothing rewards removal. assumption: positive framing makes the ratchet something the user shows others.
  Done when: closing a task whose net code lines are negative prints a "freed N lines, M verbs, K cards" receipt and appends it to a ledger that `fm burden` lists.

- **Turn each guard block into a one-line story with the safe alternative** — FEATURE — value 5 — effort M — risk low — category: guard/UX
  Why: `core:interpreter-code-driving-foreman` blocked 42x in 7 days and two brief-guard false positives mis-read a dict key and `.join(` as paths. A block that says "I stopped X because Y; do Z instead" teaches the model and calms the user.
  Done when: every guard deny reason in the corpus carries a "try instead" command, and a test asserts none of the 42 recorded blocks renders without one.

- **Make false positives one-keystroke fixable** — FIX — value 4 — effort M — risk med — category: guard/trust
  Why: the pack names two brief-guard false positives. Today fixing means editing code. `fm guard why LAST` plus `fm guard allow-once` (user-only channel) with an auto-filed regression test removes the friction without weakening the guard.
  Done when: the two named false positives become fixtures that pass, and `fm guard why` prints the matched rule and span for the last block.

- **Add a weight-class gauge to the pane and status line** — FEATURE — value 3 — effort M — risk low — category: UI/motion
  Why: hook p95, context share and injected bytes are numbers nobody watches. A small gauge that settles (eases) to the current value, amber near budget, makes the ratchet visible. assumption: foreman-ui can draw a compact gauge in the existing band.
  Done when: the pane renders a gauge with an accessible text equivalent, and a screenshot test shows it amber when p95 exceeds the stored budget.

- **Give the SessionStart note a diet: hash first, delta after** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: ~2k chars injected 89 times is about 178k chars of repetition. Injecting only "unchanged since <hash>" plus a delta saves context and feels lighter.
  Done when: a second session start with no state change injects under 300 chars, and a test proves any changed standing rule still appears in full.

- **Add a "how heavy is my Foreman" card on the site's Genesis page** — FEATURE — value 3 — effort M — risk med — category: site/trust
  Why: steer says public claims must match exam lines and `fm outcomes`; the site follows Genesis automatically. A card showing hook p95, context bytes, verbs and cards with their producing command invites verification.
  Done when: the card renders from site/genesis data, each number shows its producing command, and the claims-vs-measurement sweep goes red if one drifts.

- **Warm the stack library by use, shelve the rest** — CLEAN — value 4 — effort M — risk low — category: lean/library
  Why: 5 of 1219 cards used, and a dropped task already says unmeasured growth waits. Moving the cold ones to an archive index that loads on demand shrinks install and map weight.
  Done when: cards unused for 90 days sit in a cold index, `fm lib show NAME` still finds them, and the install size drops measurably in a test.

- **Wild: Run a "diet week" mode that disables one optional hook per day and reports what nobody noticed** — FEATURE — value 3 — effort M — risk med — category: lean/game
  Why: wild. Pairs with the withhold-one-block idea; delight comes from a weekly "you didn't miss these three hooks" digest. The user can veto with one word.
  Done when: `fm diet start` withholds a different non-guard hook daily, never the guard, and `fm diet report` lists outcomes with a keep/drop recommendation.

- **Wild: Plant a harmless forbidden command weekly and show the guard catching it** — SECURITY — value 4 — effort S — risk low — category: guard/proof
  Why: wild. The guard is only felt when it blocks something. A visible weekly canary, "Guard alive: stopped a planted `rm -rf` at 09:02 in 3 ms", gives confidence on every surface including non-Claude hosts.
  Done when: a scheduled canary per host writes a ledger row, `fm doctor` flags a host whose canary was not blocked, and the canary command is inert.

- **Wild: Show a "since you left" lean line on resume** — FEATURE — value 2 — effort S — risk low — category: resume
  Why: wild. When a goal resumes, one line such as "hooks stayed under budget, context shrank 4%, guard blocked 3, 1 false positive filed" turns invisible discipline into a small daily reward.
  Done when: first prompt of a resumed goal includes the line, sourced from ledger rows, and it is absent when nothing changed.

- **Print the guard's weekly save as plain words** — FEATURE — value 4 — effort S — risk low — category: guard/digest
  Why: 42 blocks in 7 days are only a counter. A Friday note, "stopped 42 attempts to drive Foreman from inline Python; here's the top 3 and the safe commands", shows what bypass mode would have cost.
  Done when: `fm night` digest includes a guard section with counts, top rules, and one example each, with no secrets or raw commands beyond the redacted rule name.

- **Lint the 61 coverage cells as they are written, with a friendly nudge** — FIX — value 3 — effort S — risk low — category: coverage
  Why: the mission fills 61 cells under a rule against templated phrasing; rejecting a cell with "this reads like cell X in row Y; name the file or the real gap" saves cold-read round trips.
  Done when: writing a cell that reuses a phrase from another row fails with the matching row cited, and a grounded cell passes.

Next question: Which of these weigh-ins and receipts does the user actually read, and would the guard story or the deletion receipt be skipped like the proofs the earlier questions worried about?
Next question: What is the smallest visible sign, on a host with no pane and no hooks, that Foreman's guard and lean budget are still in force?
