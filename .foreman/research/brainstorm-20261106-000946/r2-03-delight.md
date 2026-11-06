# Brainstorm — lens: delight

- **Strike the verdict on the anvil** (imperative) — FEATURE — value 5 — effort M — risk low — category: delight
  Why: The user’s design language is the forge (T-2788, "struck metal", "heat as the running-now signal"). The decider’s verdict is the single most high-stakes moment in Sampo’s life. Making it a *physical* strike — a subtle hammer-down animation, a brief flash of heat, a single resonant tone that fades — turns a text output into a ritual. The user’s words ("the forge answers back", "strike the metal on the close") show they already value this.
  Done when: A decider verdict (close, abstain, block) triggers a distinct, sub-second forge-strike animation and a single audio tone in the web UI and CLI, and a user can mute it without disabling the decider.

- **Show the decider’s "I don’t know" as a held rune, not a grey failure** (imperative) — FEATURE — value 4 — effort S — risk low — category: delight
  Why: The pack shows "abstain" is a first-class concept, but the UI likely renders it as a silent error or a grey box. In the Kirjokansi world, an abstain is a *held* state — a rune carved but not yet lit. Rendering abstain as a dim, pulsing rune with a one-line "why I’m holding back" (e.g., "2 similar briefs disagreed") makes the model’s uncertainty feel like a deliberate, safe choice, not a bug.
  Done when: An abstain verdict displays a dim, pulsing rune glyph and a one-line reason in the web UI, and a user can click it to see the top-2 similar briefs that caused the disagreement.

- **Ring the astrolabe when the decider predicts the user’s next ask** (imperative) — FEATURE — value 5 — effort M — risk med — category: delight
  Why: The user’s own words ask for "predicting the user’s next ask" and "the forge answers back." When the decider successfully predicts a routine ask (e.g., "ship the landed commits") and the user types it anyway, the UI should *ring* — a soft astrolabe chime — and the morning card should note "predicted 3 of your last 5 asks." This turns a hidden capability into a felt, joyful surprise.
  Done when: When a user types a predicted ask, the web UI plays a soft astrolabe chime, and the morning card shows a "predicted X of Y recent asks" line, with a per-prediction confidence score.

- **Let the user "teach" a phrase by saying it once, with a forge-strike confirm** (imperative) — FEATURE — value 4 — effort S — risk low — category: delight
  Why: The user’s words include "Let the user teach Sampo a new phrase by saying it once, with a confirm." The decider can absorb a new user phrase (e.g., "I meant X, not Y") as a training signal. The "confirm" should be a forge-strike: the user types the phrase, hits Enter, and the UI strikes a small rune into the "taste file" with a satisfying sound and animation. This makes the model feel like it’s learning in real time.
  Done when: When a user types "I meant X, not Y" and hits Enter, the UI strikes a small rune animation, plays a short tone, and the decider’s "taste file" (local only) updates with the phrase, visible in `sampo doctor`.

- **A one-keystroke "ah" grade for the decider’s verdicts** (imperative) — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The user’s words mention "a one-keystroke 'ah' grade." After the decider strikes a verdict, the user can press `a` (ah) to signal "yes, that’s right," or `n` to signal "no, that’s wrong." This trains the decider’s regret model without a form. The "ah" should be a subtle, warm sound (like a hammer tapping stone) to make the feedback feel physical.
  Done when: After a decider verdict, pressing `a` or `n` in the CLI or web UI logs a one-bit feedback row to the training lake, and `sampo doctor` shows a running "ah-rate" per slot.

- **Show the "what I left out" as a torn-edge slip in the morning card** (imperative) — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The user’s words repeatedly ask for "what I left out" and "the one thing I’d ask you if I could." The morning card should end with a "torn-edge slip" — a visual element that looks like a piece of parchment with a rough edge — containing the decider’s top-1 "I left out" line. This makes the omission feel like a physical artifact the user can "keep" or "discard," not just a list item.
  Done when: The morning card renders a "torn-edge slip" visual with the decider’s top-1 "left out" line, and a user can click "keep" to file it as a task or "discard" to remove it.

- **Wild: Sonify the night as eight embers, and let the user name the sound** (imperative) — FEATURE — value 5 — effort L — risk med — category: delight
  Why: The user’s words include "sonify the funnel as eight ember chimes" and "the forge answers back." The night’s work (drives, lanes, decider calls) can be sonified as a sequence of eight short tones (embers), one per major event. The user can "name" the sound (e.g., "the night sounds like a forge") and the UI will remember the mapping. This turns the night’s activity into a *music* the user can listen to instead of reading logs.
  Done when: After a night run, the web UI shows a "night sonification" player with 8 tones, and a user can click "name" to assign a phrase (e.g., "a busy forge") that is stored locally and shown on the morning card.

- **Wild: The forge keeps a "museum" of retired decider slots** (imperative) — FEATURE — value 4 — effort M — risk low — category: delight
  Why: The user’s words include "commit a 'museum' model" and "the forge keeps a museum." When a decider slot is retired (e.g., because the rules beat the model), the UI should move its "rune" to a "museum" section — a dim, read-only gallery of past slots with their final "ah-rate" and the reason for retirement. This makes the decider’s evolution feel like a living, curated collection, not a black box that disappears.
  Done when: Retired decider slots appear in a "museum" tab in the web UI with their final performance, retirement reason, and a "replay" button that runs the slot on a recent close for comparison.

- **Wild: A "morning after" haiku for each overnight close** (imperative) — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The user’s words include "a 'morning after' haiku for each overnight close." When a decider closes a task overnight, the morning card can include a one-line haiku (5-7-5) written by a local model, summarizing the close in poetic terms (e.g., "The loop breaks at three; the test goes green; the close holds its breath"). This makes the night’s work feel *human* and *complete*, not just a list of checks.
  Done when: The morning card includes a haiku for each overnight close, generated by a local model from the close’s diff and test results, and a user can mute it with a per-feature toggle.

- **Strike a "season recap" scrub for the decider’s 30-day history** (imperative) — FEATURE — value 4 — effort M — risk low — category: delight
  Why: The user’s words include "a 60-second 'season recap' scrub." The web UI should show a "decider season" view: a 30-day timeline of decider verdicts, colored by outcome (green for "ah," red for "n," grey for abstain). The user can "scrub" a 60-second window (like a video) to see a dense summary of what the decider did, with the forge-strike sounds playing as they scrub. This makes the decider’s learning visible and *fun* to review.
  Done when: The web UI has a "decider season" tab with a 30-day timeline, a scrub bar, and audio playback of forge-strikes for each verdict, and a user can export a 60-second "season recap" as an audio file.

- **Let the user "rehearse" a veto with a "what would break?" preview** (imperative) — FEATURE — value 5 — effort M — risk med — category: delight
  Why: The user’s words include "warn when a request names a capability Sampo will only ship in the next model" and "rehearse a veto without committing." When the decider predicts a decision the user might veto, the UI should show a "rehearsal" mode: a dim, ghosted version of the verdict with a "what would break?" line (e.g., "if you veto this, 3 open tasks stall"). This lets the user *feel* the consequence before acting, making the veto a deliberate, informed choice.
  Done when: When a user hovers over a decider verdict in the web UI, a "rehearsal" tooltip shows the "what would break?" line, and clicking "veto" strikes a rune with a different sound than an "ah."

- **Wild: A "silence is not consent" lamp that glows when the user has gone quiet** (imperative) — FEATURE — value 4 — effort S — risk low — category: delight
  Why: The user’s words include "a 'silence is not consent' lamp that glows when you’ve gone quiet." The decider should detect when the user has not interacted with Sampo for a set time (e.g., 48 hours) and glow a soft, amber lamp in the status bar. This signals "I’m here, but I’m not pushing" — a respectful, visible acknowledgment of the user’s absence. The lamp dims when the user returns.
  Done when: When a user has not interacted with Sampo for 48 hours, a soft amber lamp glows in the web UI status bar, and it dims when the user sends any message, with the threshold configurable in `sampo doctor`.

- **Show the decider’s "cost of being interrupted" as a live gauge** (imperative) — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The user’s words include "a 'cost of being interrupted' gauge." The decider can estimate the "cost" of a decision (e.g., how many tasks it unblocks, how much time it saves) and display it as a live gauge in the web UI. This makes the decider’s value *visible* and *tangible*, not just a list of checkmarks. The gauge should be a small, animated forge-stone that fills as the decider’s value accumulates.
  Done when: The web UI shows a "decider cost" gauge that fills as the decider’s decisions unblock tasks, and `sampo doctor` shows the "cost of being interrupted" as a number (e.g., "3.2 hours saved this week").

- **Wild: The forge "sighs" when the user lets it sleep** (imperative) — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The user’s words include "the forge sighs when you let it sleep." When a user pauses or stops the decider (e.g., `sampo stop`), the UI should play a soft, fading "sigh" sound (like a forge going cold) and dim the forge animation. This makes the decider feel like a *living* thing that is being put to rest, not just a process that is killed. The "sigh" should be subtle and warm, not sad.
  Done when: When a user runs `sampo stop`, the web UI plays a soft "sigh" sound and dims the forge animation, and the sound is muted by the same toggle that mutes the forge-strike sounds.

- **Let the user "strike a test" on the anvil before the decider runs** (imperative) — FEATURE — value 4 — effort S — risk low — category: delight
  Why: The user’s words include "let the user strike a test on the anvil." Before the decider runs a close, the user can "strike" the test suite with a single keystroke (e.g., `t`), which runs the tests and shows a forge-strike animation for each passing test. This makes the decider’s "prove its work" step feel like a *ritual* the user participates in, not a background process. The "strike" should be a quick, satisfying tap, not a long wait.
  Done when: Before a decider close, pressing `t` in the CLI or web UI runs the test suite and shows a forge-strike animation for each passing test, with a "all tests struck" line when done.
