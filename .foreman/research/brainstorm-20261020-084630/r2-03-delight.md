# Brainstorm — lens: delight

- **Show the tax receipt as a one-line sign-off** — FEATURE — value 4 — effort S — risk low — category: delight/cost
  Why: Foreman costs +10–14% and ~60% on long sessions; the user keeps pushing on cost, but nothing shows it per session. A closing line like "Foreman added 11% (4.2k tokens); it stopped 1 command, proved 3 criteria" makes the price visible and earns trust.
  Done when: ending a session whose ledger holds a close prints one line with the token share and the count of guard stops and proofs, and `fm doctor` confirms the numbers match the ledger.

- **Paint the stored theme before first render** — FIX — value 3 — effort S — risk low — category: site polish
  Why: T-1244: `site.js` and `style.css` apply the theme only after load, so dark-mode readers see a white flash on every Pages visit. Cheap and visible to everyone who opens the demo.
  Done when: an inline head script sets the theme attribute, and a headless screenshot at first paint with dark stored shows no light frame.

- **Match the pane to Claude Code's own background** — FIX — value 3 — effort S — risk low — category: pane polish
  Why: T-1217: Claude Code paints the docked pane #262626 and Foreman's colours seam against it. Fixing this makes the hero demo look native.
  Done when: a screenshot test of the pane shows no colour seam against the 48;2;38;38;38 background, and the cell colours come from one constant.

- **Close with a three-frame keepsake** — FEATURE — value 3 — effort M — risk low — category: close-out
  Why: The README's strongest asset is the live SVG demo, which is hand-made. Each closed task could emit a tiny SVG of the before/after proof (failing run, passing run, diff stat) saved beside the brief, so users have something to show.
  Done when: closing a task writes `.foreman/keepsakes/T-xxxx.svg`, and it renders in a browser with the task id, the red→green proofs and the diff stat.

- **Name the release after its most annoying fix** — FEATURE — value 2 — effort S — risk low — category: release notes
  Why: 40 releases in a row are listed as "Foreman 1.2.40" with the real content in the subject lines below. A headline, such as "the Benchmarks page stops overflowing", makes the changelog readable by someone who never opens the commits.
  Done when: the release step writes a one-sentence plain headline taken from the task titles, and the Pages changelog shows it above the version.

- **Celebrate a hard-won green in plain words** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: Unattended runs end with ids and counts. A close that took 3 retries or a once-red gate should say so in one human sentence ("Took three tries; the flaky timing bound was the culprit"), since people remember the story, not the id.
  Done when: closing a task with retries ≥ 2 prints one sentence naming the failing check and the fix, drawn from the ledger, and a test pins the wording.

- **Draw the Benchmarks page from the results files** — FIX — value 4 — effort M — risk low — category: site trust
  Why: T-1246: prose figures are hard-coded, and the user has already reported overflow bugs on this page. Every claim must be measured, so generating the sentences from the JSON removes drift and makes each rerun a delight to publish.
  Done when: the build fails if any number in the Benchmarks prose differs from the results file, and a rerun updates the page with no hand edits.

- **Fade quiet pane cards by recency** — FEATURE — value 2 — effort M — risk low — category: pane motion
  Why: The pane has many lanes (Activity, Agents, History, Today). Static cards compete for attention. A slow brightness decay says what is live without needing more rows, and honours reduced motion by stepping instead of fading.
  Done when: a card untouched for 10 minutes renders one step dimmer, a ledger event restores it, and the reduced-motion setting disables the decay in the pane test.

- **Wild: Show a ghost bill of plain Claude Code beside the real one** — FEATURE — value 4 — effort L — risk med — category: honesty/cost
  Why: wild. The user wants Foreman cheaper than Claude Code and every claim measured. Estimating what the same prompts would have cost without Foreman's injected notes (from token counts of the session's own turns) gives a live, honest comparison, labelled as an estimate with its error range.
  Done when: the pane shows "you $0.31 · plain ≈$0.27 (±8%)", and a replayed recording lands within the stated error of a real plain run.

- **Wild: Hum build weather in the statusline** — FEATURE — value 2 — effort S — risk low — category: statusline
  Why: wild. One glyph for load, green/red streak and queue depth gives ambient awareness for people who never open the pane, and it works as the fallback when the mod UI isn't installed.
  Done when: the statusline prints one glyph plus a number that changes when the queue length or the gate state changes, within one refresh.

- **Wild: Cut a thirty-second director's cut replay at each release** — FEATURE — value 3 — effort L — risk med — category: demo
  Why: wild. The hero demo is a hand-recorded session, and the README says it was sped up where the model thinks. Recording the pane during the release's own round and trimming the idle time automatically keeps the demo current without manual effort.
  Done when: tagging a release produces `demo/release.svg` from the recorded pane frames, under 2 MB, and the README embeds it.

- **Wild: Leave a decaying sticky note on files a builder was nervous about** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: wild. Builders already record "noticed, didn't touch" style findings in ideas above, but they vanish. A one-line note keyed by file and blob hash, shown when the next agent opens it and expiring when the file changes, is a small touch that makes the next session feel remembered.
  Done when: a note written on a file appears in the pre-edit hint for that file, and disappears after the file's contents change.

- **Flash a card once when it changed while you were away** — FEATURE — value 2 — effort S — risk low — category: pane motion
  Why: The pane is watched from the corner of the eye during unattended runs. A single pulse on a card whose state moved since the last keypress tells the user where to look.
  Done when: a state change in a card during idle triggers one highlight cycle, which stops on any keypress, and is off under reduced motion.

- **Print a last-frame keepsake when the pane exits** — FEATURE — value 2 — effort S — risk low — category: pane polish
  Why: The pane clears on quit, so the day's work vanishes from the terminal. Printing the final frame to scrollback leaves a record of the queue, the bar and the counts.
  Done when: quitting the pane leaves a static frame in the terminal scrollback matching the last render, and `--no-keepsake` suppresses it.
