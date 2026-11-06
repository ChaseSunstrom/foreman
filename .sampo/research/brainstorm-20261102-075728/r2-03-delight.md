# Brainstorm — lens: delight

- **Show a "safe to stop" light** — FEATURE — value 4 — effort S — risk low — category: reassurance
  Why: the request is about carrying a plan across crashes and compactions, yet nothing tells the user when closing the laptop is safe. Assumption: the baton and ledger can be checked for "nothing unsaved" cheaply.
  Done when: the status line shows a green mark after a checkpoint and amber while a row is mid-write. A test that kills the session in the amber window shows the resume lost something, and one in the green window shows it lost nothing.

- **Leave a replayable cast on every closed row** — FEATURE — value 4 — effort M — risk low — category: proof you can watch
  Why: the finish card says "you can now…" in prose, and the user's steers insist on proof from commands that really ran. A short text recording of the proving command makes "done" something you can watch. Assumption: the proof command's output can be captured as a plain asciicast-style file under the goal's state dir.
  Done when: closing a row with a verify command writes a cast file of 100 KB or less. `fm goal cast ROW` replays it in the terminal, and a row closed without a command says "no cast".

- **Narrate a review tour in the order of the user's own sentence** — FEATURE — value 4 — effort M — risk med — category: finish experience
  Why: assumption: at finish the user faces a big diff and has to work out which hunk answers which phrase of their goal. A tour that walks the diff phrase by phrase, quoting the user's words, makes review feel guided.
  Done when: on a fixture goal of 3 phrases, `fm goal tour` prints 3 stops. Each stop quotes a phrase and the hunks that serve it, and any hunk matching no phrase is listed under "unrequested".

- **Hang a "days since a false done" safety sign** — FEATURE — value 3 — effort S — risk low — category: site charm
  Why: the pack's recurring worry is false dones, such as the long-tier false dones, and the hard-hat theme invites the classic site sign. It also turns an honesty metric into something the user glances at. Assumption: reopened tasks are in the ledger with dates.
  Done when: the web UI header and `fm status` show "N days since a done was reopened". Reopening a closed task resets it to 0, and a fresh install shows "no history" instead of 0.

- **Give each goal a generated emblem** — FEATURE — value 2 — effort S — risk low — category: identity
  Why: assumption: with several goals live, text codenames blur together. A small emblem generated from the goal's hash shows up on the status line, the web UI, the finish card and commit trailers.
  Done when: the same goal id always yields the same emblem, two different goals differ, and a snapshot test covers the SVG output.

- **Scale the welcome-back to the length of the gap** — FEATURE — value 3 — effort S — risk low — category: tone
  Why: the pack proposes many resume cards, but a lunch break and a two-week absence need different weight. Assumption: gap length is readable from the last ledger timestamp.
  Done when: a gap under 1h prints one line, a gap of 1h–2d prints the three-line story, and a gap over 2d also names what changed in the repo. A table test covers the three bands.

- **Add a voice dial for Foreman's own text** — FEATURE — value 3 — effort S — risk med — category: personality
  Why: assumption: some users want terse output and others a warm site-foreman voice. The risk is a flavour that alters facts, so the dial may change wording but never numbers, ids or commands.
  Done when: `fm voice terse|plain|foreman` changes the finish card and refusal text. A test diffs the ids, numbers and commands between voices and finds them identical.

- **Add earcons that explain state (off by default)** — FEATURE — value 2 — effort S — risk low — category: motion and sound
  Why: assumption: a user in another window misses state changes. A distinct terminal bell pattern for "plan locked", "row proved", "crash recovered" and "needs you" tells them which without looking.
  Done when: with `earcons on`, each of the 4 events emits its own bell and OSC notification sequence. With the setting off, nothing is emitted, and a test asserts that.

- **Race your own best goal as a ghost line (wild)** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: the user bets on finish dates and the ledger holds estimate-versus-actual per row. Drawing the current goal's progress curve against the user's own fastest past goal, like a time-trial ghost, makes pace feel playful and not like a burn-down warning. Assumption: at least 2 closed goals exist, otherwise it says so.
  Done when: the goal page draws two curves normalised by row count. With fewer than 2 closed goals it shows "no ghost yet", and a fixture with two goals draws both.

- **Award hat stickers for rare real events (wild)** — FEATURE — value 2 — effort M — risk low — category: collectibles
  Why: the logo is a hard hat, and laptop-sticker culture fits it. Stickers go only to events the ledger can prove: "survived a kill -9 with zero lost rows", "first red-first prove", "closed a goal with no reopens". They are not points for activity.
  Done when: each sticker has a ledger query. A fixture ledger earns exactly the stickers it should, a sticker is never awarded twice, and the web UI shows them on the hat.

- **Draw the finish as a four-panel comic (wild)** — FEATURE — value 2 — effort M — risk med — category: shareable
  Why: assumption: the user likes to show others what the tool did, and a day-end postcard is text-only. Four panels (the vague ask, the plan, the crash or compaction survived, the finish) built from ledger events give a screenshot-friendly SVG. Captions come from recorded facts, not generated claims.
  Done when: `fm goal comic` writes an SVG with 4 panels. Each caption cites a ledger line id, and a goal with no crash uses the "no incidents" variant.

- **Build a live construction-site view (wild)** — FEATURE — value 3 — effort L — risk med — category: motion that explains state
  Why: assumption: lanes, rows and crashes are abstract in text. An isometric site where rows are floors, a running lane is a worker or crane, a blocked row is taped off and a crash is a barrier lets motion carry state. It would need reduced-motion and keyboard parity.
  Done when: the page animates a fixture goal. Each lane state maps to one visual state, reduced-motion shows a static version, and every element has a text alternative listing its state.

- **Turn a pencil sketch into plan rows (wild)** — FEATURE — value 3 — effort L — risk high — category: intake
  Why: assumption: some vague goals are visual ("a dashboard like this") and the user finds a canvas easier than a paragraph. A sketch pad in the web UI could feed the goal intake as rows the user can strike out. Any local vision model use would need an explicit setting.
  Done when: a sketch with 3 boxes labelled "chart", "list", "filter" yields 3 draft rows marked "from sketch", each strikeable, and nothing is sent off-machine without the setting on.

Next question: which of these delights would the user keep if each cost one more verb, and which should replace an existing ceremony instead?
Next question: does the user ever open the web UI during a goal, or only the terminal, so that motion and sound ideas reach the surface they use?
