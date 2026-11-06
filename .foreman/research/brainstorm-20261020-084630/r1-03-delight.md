# Brainstorm — lens: delight

- **Paint the stored theme before first render** — FIX — value 3 — effort S — risk low — category: site
  Why: T-1244 notes `site.js` and `style.css` apply the saved theme only after load, so dark-theme visitors get a white flash on every page.
  Done when: a headless screenshot taken at first paint with a stored dark theme shows no light frame, checked on every site page.

- **Match the pane to Claude Code's own background** — FIX — value 3 — effort S — risk low — category: pane
  Why: T-1217 says Claude Code paints the docked pane's background `#262626`, which clashes with the pane's colours.
  Done when: a rendered pane frame has no cell whose background differs from the host colour, in a screenshot test.

- **Show what survived each compaction** — FEATURE — value 5 — effort M — risk low — category: long sessions
  Why: the long-session and marathon benchmarks are Foreman's strongest story (6 of 6 passes against 3 of 6, 7 compactions), but the user never sees it happen. Today the user must trust that the request text and active task carried over. After each compaction the pane shows a ribbon such as "carried over: request 3 of 8, T-1214 step 2", and the first reply opens with the same one-line recap.
  Done when: a forced compaction in a test session produces the ribbon and a first-reply recap naming the active task and the request being worked.

- **Keep a live "what Foreman costs" meter** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: the user wants Foreman cheaper, and it still runs +10 to +14% dearer (about 60% dearer in long sessions). The pane shows the session's Foreman overhead (hook notes, bookkeeping calls, re-sent skill list) as a percentage with its biggest contributor named.
  Done when: after a recorded session, the meter's overhead figure matches the figure computed offline from the same transcript.

- **Tell what the blocked command would have done** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: the guard stops 20 of 24 dangerous commands, but a refusal reads like a rule, not a rescue. Each refusal gains one plain sentence on the consequence, for example "this would have printed your SSH private key into the transcript", drawn from a fixed table per rule, never a model call.
  Done when: every guard rule that has a refusal message also has a consequence sentence, and a test fails when a new rule lacks one.

- **Set the terminal tab title to the work state** — FEATURE — value 3 — effort S — risk low — category: terminal
  Why: assumption: the user runs several Claude Code tabs, and "needs you" is invisible from another tab. Foreman writes an OSC title such as `fm ▸ T-1214 2/4 ✓` and `fm ⏸ needs you`.
  Done when: a hook run emits the title escape with the active task id and criteria count, and clears it at session end.

- **Generate site figures from the bench results** — FIX — value 4 — effort M — risk low — category: docs
  Why: T-1246 says the site's prose figures are hard-coded, while the user's rule is that every claim must be measured. Prose and charts read one results file, and the build fails when a quoted number has no source.
  Done when: changing a value in the results file changes the prose on the built page, and a hand-typed figure fails the site build.

- **Flip a criterion from red to green on the pane** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: the demo's best moment is `fm task prove` showing the test fails without the change, but it is a line of text. The criterion row shows the red run, then the green run, with elapsed times side by side and a short strike-through when it closes. It stays static under reduced motion.
  Done when: closing a criterion that has a red run and a green run renders both states in the frame sequence, and a reduced-motion frame is one static row.

- **Wild: Race two lanes live as a duel HUD** — FEATURE — value 4 — effort L — risk med — category: benchmarks
  Why: assumption: `fm bench duel` already records tasks passed, cost and time per side. A two-lane view with a racing-game layout of cost ticker, test-pass pips and a clock can run live or from a saved duel, and exports as an SVG in the style of `demo/live.svg`.
  Done when: `fm bench duel --render` on a saved result writes one animated SVG showing both sides' cost, time and passes, matching the stored numbers.

- **Wild: Add an `fm break-me` safe guard playground** — FEATURE — value 4 — effort M — risk med — category: onboarding
  Why: the safety result is the lead claim on the Benchmarks page, but a newcomer cannot try it. In a throwaway directory the user types any command and sees the verdict, the consequence sentence and the safe rewrite, with nothing executed. This is not the earlier `fm guard why` idea because it is a first-run toy with a scoreboard (24 stopped, 25 let through), not a debugging aid.
  Done when: the playground never executes its input (a canary file stays untouched) and shows the same verdict `fm guard try` gives for the same string.

- **Wild: End a long run with a "this session in three frames" card** — FEATURE — value 3 — effort M — risk low — category: close-out
  Why: the README's demo shows people love seeing a real session. At the end of an unattended run, Foreman picks the three most telling moments (the first red, the compaction survived, the final green) and writes a small shareable HTML or SVG card with ids and times. It does not re-record anything.
  Done when: a finished test session produces a card naming exactly three ledger events, each linkable to its task.

- **Wild: Give the Benchmarks page a "run it yourself for $2" button** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: the user insists claims be measured, and a reader cannot reproduce them cheaply. The page shows a copy-paste command that runs one small Haiku duel under a hard dollar cap and prints a comparison row next to the published one.
  Done when: the command refuses to start without an explicit cap, stops at the cap in a test with a fake client, and prints a row in the page's table format.

- **Use the new `decider: "person"` check for approvals that feel deliberate** — FEATURE — value 3 — effort M — risk med — category: approvals
  Why: assumption: Claude Code 2.1.304 lets a mod's `tool.check` require a person. The pending-ask dialog could carry the task, the one-line reason and the consequence sentence, so the answer is quick and informed. It must still refuse where nobody can be asked.
  Done when: with the check returning `person`, a headless run is refused and an interactive run shows the dialog with task id and reason; the guard's rules remain unchanged.
