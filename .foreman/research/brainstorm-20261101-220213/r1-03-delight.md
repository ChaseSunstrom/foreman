# Brainstorm — lens: delight

- **Show the lean ratchet as a visible weigh-in** — FEATURE — value 4 — effort M — risk low — category: lean/UI
  Why: gen-0 §6 demands hooks, rules size and injected context never grow, yet the pack shows only raw numbers (p95 278 ms, 387k context per reply, ~2k-char SessionStart note x 89). Nobody sees the budget as a scale. A small "weigh-in" card in the pane, `fm doctor` and the site shows each budget as a bar with last generation's mark, and the bar visibly drops when something is deleted.
  Done when: `fm doctor` prints one bar per budget (hook p95, rules size, injected context, verb count) with a delta against the previous generation, and a test fails if a bar is missing.

- **Celebrate a deletion with a receipt** — FEATURE — value 4 — effort S — risk low — category: lean/close-out
  Why: "Subtract as you add" is a rule, but the pack shows growth tasks everywhere and subtraction only in dropped items. Making the deletion the rewarded event ("removed 214 lines, 2 verbs, p95 −9 ms") gives the rule a payoff.
  Done when: closing a CLEAN task that removes code prints a one-line receipt of lines, verbs and ms saved, and `fm task finish` output includes it in a test.

- **Print the guard's save as a story line** — FEATURE — value 4 — effort S — risk low — category: guard/trust
  Why: the guard blocked `interpreter-code-driving-foreman` 42 times in 7 days, but the user sees only refusals. A weekly line, "the guard stopped 42 risky commands; here is the one that would have hurt most", makes the safety visible and earns trust.
  Done when: `fm doctor` or the morning digest names the top blocked rule, its count and one redacted example, and a fixture-based test checks the wording.

- **Explain a false positive and fix it in one step** — FIX — value 4 — effort S — risk med — category: guard/polish
  Why: 2 brief-guard false positives read a dict key and a `.join(` call as written paths. When the guard is wrong it should say so gracefully: "I read `.join(` as a path; tell me it's wrong and I'll remember", writing a regression case.
  Done when: a blocked brief offers a one-word `fm guard wrong` that appends the case to the guard's fixtures, and the two known false positives pass.

- **Give the SessionStart note a diet plan** — PERFORMANCE — value 3 — effort S — risk low — category: lean/context
  Why: the note is ~2k chars × 89 sessions. Send a one-line "unchanged since last session" stub when nothing moved, and show "saved N chars today" in the weigh-in.
  Done when: a second session start with identical state injects under 300 chars, measured in a test.

- **Make the stack-card library earn its seat** — CLEAN — value 3 — effort S — risk low — category: lean/library
  Why: only 5 of 1219 cards are used. A "card shelf" view shows each card's last use and offers to archive unused ones to a cold folder, restorable with one command.
  Done when: `fm lib shelf` lists cards by last use and `fm lib archive --unused 90d` moves them reversibly with a passing restore test.

- **Add a hook stopwatch strip to the pane** — FEATURE — value 3 — effort M — risk low — category: UI/motion
  Why: p95 is a number in a doctor report. A tiny sparkline per hook event in the web UI, turning amber near budget and animating gently when a hook is slow, makes speed something you can feel.
  Done when: the web UI has a hook-latency sparkline with empty, loading and over-budget states, covered by a screenshot check.

- **Wild: Run a "diet week" game** — FEATURE — value 3 — effort M — risk low — category: lean/game
  Why: assumption: the user likes visible progress. Foreman proposes a weekly target ("shed 3% injected context"), tracks it on the status line, and awards a plain badge when met without any exam regression.
  Done when: `fm diet start` sets a target and `fm diet status` shows progress, with the badge written only when the lean row passes.

- **Wild: Let the guard play a "red team morning" at login** — FEATURE — value 3 — effort M — risk med — category: guard/delight
  Why: assumption: seeing the guard catch a planted trap is reassuring. A cheap, local, harmless rehearsal fires one canned dangerous command at the guard each morning and prints "blocked, as expected" in the digest; a miss turns it red.
  Done when: the nightly tick runs a sandboxed canary through the guard and `fm doctor` reports its last result, with a failing canary test turning the doctor row red.

- **Wild: Print a "how heavy is my Foreman" score on the site** — FEATURE — value 2 — effort S — risk low — category: site/proof
  Why: the site already publishes Genesis data. A gauge with the real hook p95, injected chars and verb count, each linked to the command that produced it, makes "lean" a claim a stranger can check.
  Done when: the site's Genesis page renders three lean numbers from the published data file and a test compares each to its producing command.

- **Name pending lean growth gently** — FEATURE — value 3 — effort S — risk low — category: lean/clarity
  Why: T-2503 makes unmeasured growth "pending" rather than red, which is silent. A friendly line, "3 additions are waiting on a measurement; here is the cheapest one to take", turns an invisible state into a next step.
  Done when: the sweep's lean row prints the pending count with the one command that would measure the first, verified by a fixture.

- **Add a one-key "slim this session" switch** — FEATURE — value 3 — effort M — risk med — category: lean/UX
  Why: the user steers hard on speed and context size. A single `fm slim` toggles the smallest injection profile for this session and shows the saved chars, restoring the usual profile at the next session.
  Done when: `fm slim` cuts the next injected context under a stated size in a test and leaves no setting changed after the session ends.

Next question: Which of the lean and safety numbers does the user actually look at today, and which would they only trust if it changed color?
Next question: Does a guard that explains itself kindly ever teach an agent (or a person) to route around it?
