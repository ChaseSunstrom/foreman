# Brainstorm — lens: delight

- **Slide between before and after on every UI change** — FEATURE — value 4 — effort M — risk low — category: UI proof
  Why: `fm shot` and `fm flow` already capture screens, and the repo's own `demo/live.svg` shows the user likes showing work visually. Assumption: the shot pairs are stored per task.
  Done when: `fm task finish` on a UI task writes one self-contained HTML file with a draggable divider between the before and after shots, and opening it with no network shows both.

- **Let the user tap each changed region as "meant" or "not meant"** — FEATURE — value 4 — effort M — risk med — category: UI proof
  Why: a pixel diff can't say whether a change was intended, and "does it do what I meant" is a named gap in the request. Assumption: the diff regions can be grouped into boxes. Each tap is stored as a baseline note for the next shot.
  Done when: tapping "not meant" on a region adds a failing check to the task, and "meant" makes the same diff pass on the next `fm shot`.

- **Replay any `fm flow` as a captioned animated SVG** — FEATURE — value 4 — effort M — risk low — category: proof demos
  Why: `demo/live.svg` is already the project's showpiece, but it appears to be hand-built. Each flow step becomes a caption plus the assertion that passed or failed.
  Done when: `fm flow NAME --svg out.svg` writes an animation that plays in a browser with no scripts, with one caption per step.

- **Shade the diff by what a real run touched** — FEATURE — value 5 — effort L — risk med — category: proof coverage
  Why: "proof beyond unit tests" has no visible map of which changed lines any real command exercised. Assumption: line-level tracing can be added to the commands Foreman already runs. Lines are shaded green when a ran command reached them, amber when only read, and grey when untouched.
  Done when: `fm task prove --map` prints the diff with one of three shades per hunk, and a hunk no command reached is listed under "unproven".

- **Show a live proof counter on the status line** — FEATURE — value 3 — effort S — risk low — category: ambient status
  Why: the proof state lives in a finish card at the end, not while the user works. A line like `✔6 proven · ◐2 read-only · ○1 unproven` updates after each real command, and the unproven count turns amber if it is still above zero near finish.
  Done when: running a command that proves one criterion changes the counter on the next status refresh.

- **Pair every "not proven" with its cheapest proof** — FEATURE — value 4 — effort M — risk low — category: unproven labels
  Why: the request says unprovable things get labelled unproven, but a bare label doesn't tell the user what to do next. Entries read like "needs a real codex login, about 2 minutes: run X".
  Done when: every item under "not proven" on a finish card carries one runnable command or a named user action, and a card with a bare label fails the doctor check.

- **Draw data changes as a balance scale** — FEATURE — value 3 — effort M — risk low — category: data proof
  Why: data verification has no friendly form. After a migration or transform, show rows in and rows out, the changed cells highlighted in a small before and after table, and whether the totals balance.
  Done when: `fm verify data` on a fixture transform prints a scale line such as `1,204 in = 1,198 out + 6 dropped (named)`, and an unexplained row makes it unbalanced.

- **Make the README tick itself on the site** — FEATURE — value 3 — effort M — risk low — category: docs proof
  Why: docs-against-code is in the request, and the site already publishes from Genesis data. Each runnable code block gets a small badge showing when it last ran and its result.
  Done when: the site shows a dated pass badge beside every command block that a docs-check run executed, and a block that no longer runs shows a red badge.

- **Issue a shields-style proof badge** — FEATURE — value 3 — effort S — risk low — category: shareable proof
  Why: users show off a green CI badge, and a Foreman equivalent costs little. The badge reads like "proved 9/11 · 2 unproven · 14 Nov", generated from the latest finish record.
  Done when: `fm badge` writes an SVG that the README can embed, and its numbers match the newest finish card.

- **Add a one-line "meant-meter" to every finish** — FEATURE — value 4 — effort M — risk med — category: intent match
  Why: "does it do what the user meant" has no glanceable answer. Three short bars show how many of the user's words were demonstrated, how many were only claimed, and how much was added that they never said.
  Done when: the finish card prints three bars computed from the request's phrases, and a request phrase with no matching proof shows up as a named gap.

- **Wild: let a saboteur test the proof itself** — FEATURE — value 4 — effort L — risk med — category: proof strength
  Why: nothing shows whether a green proof could ever have been red. In a scratch copy, plant one harmless bug in the changed code and rerun the proof. A caught bug earns a "caught the saboteur" badge on the finish card, and a missed one downgrades the proof to "weak".
  Done when: on a fixture task with a deliberately weak check, the saboteur's bug is missed and the finish card says the proof is weak.

- **Wild: turn the infra check into a launch-control countdown** — FEATURE — value 3 — effort M — risk low — category: ops proof
  Why: infra and ops verification is dry output today. Each real probe (port open, health route, log line, timer fired) lights a row in turn, ends on "it's alive" with the real response quoted, and a dark row stays dark with its cause.
  Done when: `fm verify infra` on a fixture service lights rows in order from real responses, and a dead endpoint leaves its row dark with the actual error text.

- **Wild: print a "spot the difference" flicker for the user to judge** — FEATURE — value 3 — effort M — risk low — category: UI proof
  Why: a slider is static and a flicker between two frames catches changes the eye misses. Assumption: a terminal can't flicker reliably, so this is web-only. The page alternates the two shots at 2 Hz with circles around the changed areas.
  Done when: the HTML page flickers between the before and after shots, and the circled regions match the diff regions in the stored baseline.

- **Wild: end a proven task with a stamped proof card** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: finishing a proven task has no small moment of satisfaction. A short ink-stamp line appears in the terminal, `PROVED ▪ ran 7 commands ▪ 1 left unproven`, and the stamp is withheld whenever any claim is unproven, so it can't be faked.
  Done when: the stamp prints only when every criterion has a ran-command proof, and a task with one unproven criterion prints the dashed "partly proved" variant instead.

Next question: which of these proof views would the user open a week later, and what record of past opens (not Foreman's own guess) could settle that before building any?
Next question: when a finish card says "proved" and the user disagrees days later, what was the missing check, and could that miss rate size the saboteur arm?
