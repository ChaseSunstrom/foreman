# Brainstorm — lens: delight

- **Stamp CLOSED on the web card with a proof unroll** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: closes are the product's payoff, but the pack shows only text receipts (T-0795) and a terminal pane. Assumption: the web UI has task cards.
  Done when: a browser screenshot test shows a card's closed state with a stamp animation (disabled under reduced-motion) and a click-to-expand list of the proof commands that ran.

- **Compare each gate run with its usual time** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: gates and builds run constantly (fm doctor, roundtrip, bench), but the output doesn't say whether this run was normal. Assumption: per-gate durations are already in the ledger.
  Done when: a test with seeded history prints "41s, 6s faster than usual" and "ran slow: load 7.2" on a straining host. It prints nothing if there are fewer than 5 samples.

- **Rewrite task commit subjects into plain sentences** — FEATURE — value 3 — effort S — risk low — category: git readability
  Why: recent history reads "Merge T-1158: Add `fm contract --until HH:MM --usd N` so the drive, `fm run` and the loop stop at the ti…", which is cut off mid-sentence. Assumption: a first-sentence subject plus a "Why:" body line is allowed by the commit path.
  Done when: a test closes a task with a 200-character brief and gets a subject of 72 characters or fewer that ends on a word boundary. The body holds the full done-when.

- **Add a Focus view: one task, one sentence, one bar** — FEATURE — value 3 — effort M — risk low — category: pane
  Why: the pane is dense (work bar, rail, lanes, graph, charts), and the user keeps asking for "still cluttered" fixes (a measure-density idea is in the list). A zen mode is an escape hatch rather than another trim.
  Done when: a key or `fm ui --focus` renders only the current task title, the stage rail and a work bar. A narrow-terminal screenshot shows nothing clipped.

- **Fade the key hints once the keys have been used** — FEATURE — value 3 — effort S — risk low — category: progressive disclosure
  Why: assumption: the pane shows a key cheat strip. It stays forever, so experienced users see noise and new users get no nudge.
  Done when: after a key has been pressed 3 times its hint dims. A key never used keeps its hint. A test checks the stored counts.

- **Flash a card once when it changed while you weren't looking** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the away summary and the welcome-back receipt are text. In the pane and web UI the user still has to hunt for which card moved.
  Done when: a screenshot pair taken after a simulated gap shows only the changed cards highlighted. The highlight clears after one view or 3 seconds, and under reduced-motion it becomes a static dot.

- **Show "build weather" as a day-part palette** — FEATURE — value 2 — effort S — risk low — category: theme
  Why: the pack has colourblind-safe and reduced-motion ideas but no ambient time cue. The theme eases from day to dusk to night tones by local time, with an override setting.
  Done when: a test with a fake clock yields three distinct palettes, and contrast stays at or above AA in each.

- **Print plain-language failure explainers for the top 10 gate failures** — FEATURE — value 4 — effort M — risk low — category: error voice
  Why: weak or small local models and the user all meet raw red output. Assumption: failure fingerprints exist (fix ledger ideas) but no human-friendly sentence rides along. Gate output should say "This failed because X; the usual fix is Y" in two lines.
  Done when: a fixture of 10 recorded failures each prints a two-line explainer. Unknown failures print nothing extra.

- **Wild: Show lanes as a construction-site scene** — FEATURE — value 3 — effort L — risk med — category: pane (wild)
  Why: the brand is "Foreman". The Agents graph could have a toggle that draws each builder lane as a tiny crew figure carrying a block per commit, stalling visibly when idle (the stuck-lane signal), with a flag on the finished building. A joke that is also real status.
  Done when: `fm ui --site` renders N lane figures matching `fm lane list`. A stalled lane figure sits still, and a golden-frame test exists.

- **Wild: Render a git-history time-lapse at each release** — FEATURE — value 3 — effort L — risk med — category: release (wild)
  Why: the repo has 1,524 files and a demo-recorder habit. A short gource-style SVG or MP4 of files appearing and lanes merging (coloured by callsign) makes a shareable release artifact.
  Done when: `fm release` or a release script emits `timelapse.svg` under 2 MB for the version range, and the recorder uses the shared trust check.

- **Wild: Write a weekly yearbook page of superlatives** — FEATURE — value 3 — effort M — risk med — category: reports (wild)
  Why: lanes get callsigns and the ledger knows reworks, red streaks and conflicts. It would name "most-edited file", "longest red fixed", and "the review that caught the most" in one static HTML page. The risk is Goodhart gaming, so every superlative is shown as descriptive only and feeds no metric.
  Done when: `fm yearbook` on a fixture ledger writes one HTML file with 5 awards, each linking to its task. A grep test confirms no award value is read by routing or autonomy code.

- **Wild: Let the user pin a moment into a "good day" reel** — FEATURE — value 2 — effort M — risk low — category: keepsakes (wild)
  Why: it extends the last-frame keepsake and pin-this-moment ideas. A key bookmarks the pane state, and at day's end the pinned frames play back as a 10-second loop in the web UI. Local only, nothing is sent.
  Done when: pinning 3 states and opening the reel plays 3 frames in order. Deleting `.foreman/reel/` empties it.
