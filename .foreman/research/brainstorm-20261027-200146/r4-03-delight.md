# Brainstorm — lens: delight

- **Guess the gate before it runs** — FEATURE — value 3 — effort S — risk low — category: play
  Why: Assumption: the T-1556 extras already turn the wait during checks into play (Breakout), so a one-key pass/fail guess before a full check adds a calibration score to that wait. The guess is optional and never delays the run.
  Done when: pressing a guess key before `fm check` records the guess, and the closing line shows whether it matched the verdict.

- **Draw each fix as a three-panel comic** — FEATURE — value 3 — effort M — risk low — category: explain
  Why: Assumption: a closed task already holds the failing test, the diff and the passing run. Three panels (what failed, the change, what passes) can render as one SVG through the same path as the zine export (T-1556), so a finished fix is something you can show someone.
  Done when: closing a proven task writes one SVG with three panels whose text matches the test name and the diff's first hunk.

- **Open a museum of retired code** — FEATURE — value 3 — effort M — risk low — category: history — wild
  Why: Wild: code removed in recent commits becomes an exhibit. `fm museum` lists each deleted function with the commit that removed it, the tests that last touched it and a short plaque. Assumption: git history already holds this, so no new storage is needed.
  Done when: `fm museum` on a repo where a function was deleted prints an exhibit that names the removing commit.

- **Turn spend into cups of tea** — FEATURE — value 2 — effort S — risk low — category: budget — wild
  Why: Wild: the user's complaints about usage burn are about a number they can't feel. Assumption: a unit they recognise (a cup of tea, a phone charge) makes the same dollars land faster. This sits beside the dollars-and-days view rather than replacing it.
  Done when: `fm cost` prints one everyday-unit equivalent next to the dollar figure, with its conversion held in a single constant.

- **Greet a new project with its own first sentence** — FEATURE — value 2 — effort S — risk low — category: onboarding
  Why: Assumption: the first `fm` run in a repo is a moment of attention. Quoting the README's first sentence back shows Foreman has read the project, not just its config.
  Done when: the first `fm` run in a repo with a README prints that README's first sentence, cut to 80 characters or fewer.

- **Give a run one stamp key** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: Assumption: the user already expresses approval and disapproval in plain words, and the duel and playbook scores need explicit signals. One key stamps a run "gladly" or "meh", a gesture that feeds those scores without a form.
  Done when: pressing the stamp key on a closed run writes one stamp to its journal and shows it on the run's receipt.

- **Break for a stretch when a run has been idle a long time** — FEATURE — value 2 — effort S — risk low — category: wellbeing
  Why: Evidence: the gate lock can hold a full check for up to 15 minutes, and the user has reported long holds. Assumption: those idle stretches are the natural moment for one gentle line that suggests standing up.
  Done when: a run idle for 15 minutes shows one stretch line, and the same line does not repeat within the hour.

- **Keep a streak for lines deleted** — FEATURE — value 2 — effort S — risk low — category: celebration
  Why: Assumption: the user values efficiency, and lines removed without losing behaviour are a visible kind of progress that the current receipts don't count. The streak counts consecutive closed tasks whose diff nets out negative, and the count resets on a positive task.
  Done when: `fm status` shows a streak count that rises after a net-negative closed task and resets after a net-positive one.

- **Draw the pane's accent from the project's own colours** — FEATURE — value 2 — effort M — risk low — category: theme
  Why: Assumption: the pane looks identical in every repo, so it can't tell projects apart. Reading the dominant colours from the project's logo or CSS gives each project its own accent, which earns a glance.
  Done when: a repo whose CSS defines a brand colour gets a pane accent within a small distance of it, and a repo without one keeps the default.

- **Give the queue a seasonal coat** — FEATURE — value 1 — effort S — risk low — category: mood — wild
  Why: Wild: the pane's palette shifts with the local season and time of day, and each queue states its mood in one word. Assumption: a quiet change of light helps long sessions feel less like a grind.
  Done when: the pane palette changes between two set times of day, and a test checks both palettes meet the contrast floor.

- **Play a tiny tune for each gate colour** — FEATURE — value 1 — effort S — risk low — category: sound — wild
  Why: Wild: each gate's verdict plays a two-note cue that the user can mute with one switch. Assumption: a short, consistent cue helps a user who has looked away learn the result by ear. This is kept to two notes so it stays clear of the existing sonic recipes.
  Done when: each verdict plays its own cue, and the mute switch silences all of them with no other side effects.
