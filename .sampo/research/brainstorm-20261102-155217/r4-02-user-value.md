# Brainstorm — lens: user value

Round 4 is saturated, so these are second-order moves and combinations; I dropped anything the "ideas so far" list already contains. Every idea is built on an assumption, since the pack shows no per-idea use data.

- **Gate every brief on a 90-day incident count** — FEATURE — value 4 — effort S — risk low — category: grounding
  Why: the drops (c16, c17, c21) were mostly "already built" or low value after re-grounding. assumption: the ledgers can count how often each brief's pain actually occurred (a ledger row, a doctor warning, a user correction).
  Done when: `fm` refuses to file a brief with no cited incident rows and sends it to a "no evidence yet" shelf, and a test shows a zero-incident brief is shelved while a three-incident brief files.

- **Run the unattended tick on an always-on host** — FEATURE — value 4 — effort L — risk med — category: unattended
  Why: the pack asks which unattended paths have never run on a real clock while the machine slept, and `fm-children` lives under `/run/user` (tmpfs). assumption: the user has a Pi, NAS or home server.
  Done when: a second machine runs `fm tick` against a git remote, lands only on a branch, and `fm doctor` shows its last-alive time.

- **Add a one-word cost-of-delay field to tasks** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: the 30-plus "Later from" deferrals look the same in the queue, so urgency has no input except effort and value. assumption: the user can state urgency in one word at filing.
  Done when: `fm file --delay now|week|never` changes `fm next` order and idle-quota selection, and a test shows a "now" S task beating a "never" M task of equal value.

- **End every finish card with a verdict and its flip condition** — FEATURE — value 4 — effort S — risk low — category: finish
  Why: the finish card reports state but never says "ship, hold or revert" or what evidence would change that. assumption: a card line built from the proof grade and unproven list is enough.
  Done when: the card ends with "Recommend: ship. Would flip if: <named check> fails", and a test with an unproven row shows "hold" with that row named.

- **Let the user strike an idea mid-brainstorm and re-aim the remaining lenses** — FEATURE — value 3 — effort M — risk med — category: brainstorm
  Why: dropped ideas cost a full round before the lenses learn from them. assumption: the skill can pass a strike list to children that haven't started.
  Done when: striking idea N in a running `fm ideas` adds it to the pack of lenses not yet launched, and a test shows none of them repeat it.

- **Turn a read-later list into a repo impact digest** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: the pack covers verifying one pasted claim but not links the user saves to apply later. assumption: the user pastes links or articles regularly.
  Done when: `fm read <url…>` returns at most 5 lines per link saying "affects T-#### / file / nothing", with claims checked against the repo, and an irrelevant link says "nothing here".

- **Add `fm bye <capability>` for per-capability removal** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: the user wants fewer decisions and Lite mode is deferred (T-0794). Eject and the session-wide vanilla switch remove too much or too little. assumption: capabilities are enumerable (hooks, skills, state files).
  Done when: `fm bye X` removes X's hooks, skills, injected text and state, prints the bytes freed, and `fm doctor` stays green on the remainder.

- **Prototype both options of a stalled user decision overnight (wild)** — FEATURE — value 4 — effort L — risk med — category: unblock
  Why: blocked and "needs the user" items (T-0335, T-0352) sit for weeks, and a decision is easier made by looking at two cheap throwaways than by reading prose. assumption: many stalls are a choice between two buildable paths.
  Done when: for a decision pending over 7 days, `fm` builds two throwaway branches, each with a 3-line summary and a screenshot or test output, and the morning card asks "A or B".

- **Watch a manual debugging session and write the regression test afterwards (wild)** — FEATURE — value 4 — effort L — risk high — category: learning
  Why: the user's hand work is where Foreman learns least, and the hand-edit steers keep asking for it. assumption: an opt-in `fm watch` can read the shell and edit stream without sending it out.
  Done when: after a watched fix, `fm` proposes one failing-before, passing-after test and one lesson drafted from the commands, and a test with a recorded session proves the test fails on the parent commit.

- **Propose aliases and git hooks from the user's repeated commands (wild)** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: assumption: shell history shows repeated multi-step habits, such as the same four-command proof sequence.
  Done when: after a command sequence repeats 5 times, `fm tips` offers a one-line alias or hook with a diff preview, and declining it is remembered.

- **Rescore dropped ideas only when new incidents appear** — FEATURE — value 3 — effort S — risk low — category: catalogue
  Why: drops are final today, while the Genesis rule says nothing is killed for ambition and a failed idea goes to not-yet with its blocker. assumption: drop reasons are stored with a probe that could later turn true.
  Done when: a dropped idea carries a probe, and a test shows it re-enters the slate only after its incident count rises.

- **Test the first minute after install with the user's own settings** — FIX — value 4 — effort M — risk low — category: trust
  Why: the pack asks what the user sees in the first minute after a silent fail-open and whether that moment is ever tested. assumption: the user's real `settings.json` differs from the fixtures.
  Done when: CI runs the fail-open card test against a copy of a real-shaped config with unusual hooks and permissions, and fails if the card does not appear.

Next question: Which of the 525 catalogue entries did the user ever see a result from, and what is the accept rate per lens, so the next brainstorm spends its budget where the user's attention actually goes?
Next question: When a standing steer and a hand edit disagree in the same file, which one does each reader obey, and is that written down once?
