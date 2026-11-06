# Brainstorm — lens: delight

- **Draw the plan as a fork map** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: the pack's mission is exhaustive thinking (readings, approaches, race), but the user only meets it as text in a plan gate; the web UI (`plugin/templates/web/index.html`) is the only surface and has no deliberation view. Assumption: readings and options are stored as files the page can read.
  Done when: opening the web UI on a task with a plan shows readings as branches, each approach as a node, the chosen one highlighted, with the rejected ones still visible.

- **Name the save** — FEATURE — value 3 — effort S — risk low — category: receipts
  Why: "Print the guard's save as a story line" and the decision-receipt ideas recur; deliberation that changed an outcome is invisible. Assumption: a close can compare first-instinct approach vs chosen one.
  Done when: `fm task finish` prints one line such as "First instinct was X; the race showed Y fails on Z; went with W", or "deliberation changed nothing" when true.

- **Write the "why this one" sentence** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: the choice by evidence is gen-0 #2's core, yet receipts show the pick, not the reason in plain words. Assumption: the race and the plan already hold the evidence.
  Done when: every plan with 2+ options carries a one-sentence reason in the user's vocabulary, and the gate refuses plans where the sentence only restates the option's title.

- **Pulse the blast radius as ripples** — FEATURE — value 3 — effort M — risk low — category: web UI motion
  Why: `fm graph blast` output is a list; motion that explains state is a pillar-4 requirement. Assumption: blast results can be exported as nodes with distance.
  Done when: the web UI animates ripples from the changed file outward, nodes labelled "unknown" shown dashed, honouring reduced-motion settings.

- **Hover a plan step to light up the user's words** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: the user's steers repeatedly concern the letter defeating the intent; showing which of their words each step serves makes drift visible. Assumption: plan steps can be matched to quoted request phrases.
  Done when: hovering a step highlights the request phrases it cites, and a step citing none is flagged "no ask behind this".

- **Show a depth gauge that says why** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: "scale depth to risk" is in gen-0 #2 but a S task and an L task look the same to the user. Assumption: tier, blast radius and reversibility are available at plan time.
  Done when: the status line and web UI show a gauge such as "depth 2/5: S task, 3 files, reversible" and it changes when the tier does.

- **Give every coverage cell a "try it" line** — FEATURE — value 4 — effort M — risk low — category: coverage grid
  Why: the 58 empty cells must name concrete capabilities (steer: coverage must be real); a runnable command makes each cell a small demo and defeats templated phrasing. Assumption: most cells map to a verb.
  Done when: each filled cell carries a command that exits 0 and prints something specific to that cell, and the sweep runs them.

- **Fill the Genesis grid as a live heatmap** — FEATURE — value 3 — effort M — risk low — category: site
  Why: the standing rule says the site follows Genesis (`site/genesis`); a grid emptying in colour makes progress felt. Assumption: coverage.md parses into rows by surfaces and stages.
  Done when: `site/genesis` shows the grid with empty, existing, gap and n/a cells distinct, updated by `fm genesis live`, and cells link to their citations.

- **Make "do less" a first-class chip** — FEATURE — value 3 — effort S — risk low — category: plan UI
  Why: the gen-0 text names "use what exists" and "do less" as required approaches, but they're easy to hide in prose. Assumption: option labels can be typed.
  Done when: options render with chips (existing, do less, new build), and a plan without both of the first two is flagged with a one-line nudge.

- **Turn edge cases into a swipeable deck** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: edge-case lists are long and skimmed; the user could one-word keep, drop or "already handled" each card, feeding a regression probe. Assumption: edge cases are stored as structured rows.
  Done when: the web UI shows one card at a time, keyboard navigable, and each answer is written to the task's file and shows in the finish receipt.

- **Wild: Collect caught edge cases in a bestiary** — FEATURE — value 2 — effort M — risk low — category: delight — wild
  Why: assumption: an edge case that really prevented a reopen deserves a name and a sketch, and seeing them accumulate rewards thinking.
  Done when: a page lists each caught edge case with the task that caught it, a one-line name, and a count of times it recurred.

- **Wild: Argue with the road not taken** — FEATURE — value 3 — effort M — risk med — category: deliberation — wild
  Why: assumption: users doubt a runner-up when it loses; a button that replays that branch cheaply builds trust.
  Done when: `fm plan argue` spawns a capped lane for the rejected option and returns its verify result beside the winner's, within a stated cost.

- **Wild: Print each plan as a haiku on the status line** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: assumption: a three-line summary is what someone remembers and shows to others; it forces the plan's essence into words.
  Done when: the status line shows a 5-7-5 summary of the current plan, tested to fit the width and fall back to plain text when it can't.

- **Show a "what I did not think about" list from a blind child** — FEATURE — value 3 — effort M — risk med — category: deliberation
  Why: the user's asks that no earlier brainstorm predicted show real blind spots; a tool-less child reading only the request can name the gaps cheaply. Assumption: a Haiku child suffices.
  Done when: L plans include a section from a blind child's list, and the finish receipt says how many items later proved relevant.

Next question: Which of the 58 empty cells would the user be annoyed to find still empty, judged by what they've actually asked for rather than by the grid's shape?
Next question: Does any deliberation view need to work with no web UI running, such as the terminal pane or a hookless harness?
