# Brainstorm — lens: delight

Reading the pack: Sampo is a discipline layer with a strong identity (runestone logo, Kirjokansi brass-astrolabe/forge theme, "Sampo the forge"). The user keeps asking for craft and motion (T-2964 hammer trail clipped; M2 smear), delight moments (strike on close, forge answers back), and legibility of state. The "user's own words" show a love of *feel* and *narrative* ("season recap," "what you no longer have to do," silence as label). Prior ideas already cover strike-on-close, held-rune abstain, sonification, morning haiku, forge-answers-in-your-voice. I go past those.

- **Let the user *feel* a verdict before reading it** — FEATURE — value 5 — effort M — risk low — category: delight
  Why: T-2964 shows the team already polishes the hammer trail; the user wants *felt* feedback, not just a glyph. A verdict (pass/block/abstain) should land as a haptic tick + a 120ms brass-astrolabe needle settle, distinct per outcome, on any surface that supports haptics.
  Done when: a closed task and a Ward-block each produce a different, measurable haptic + motion event, and `sampo doctor` confirms the two are distinguishable.

- **Make the forge *remember the user's hand*** — FEATURE — value 5 — effort M — risk med — category: delight
  Why: "Turn every pushback into a receipt" and "teach a phrase by saying it once" are already proposed; the delight is that the *forge itself* reacts to *this* user — a small etched sigil per user, drawn from their most-repeated phrasing, shown on the logo plate.
  Done when: `sampo sigil` renders a distinct rune per account from their top 5 recurring phrases, and it appears on the runestone logo plate and morning card.

- **A "forge glow" that tells you the night is safe at a glance** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: User asked for "a sleeping-lamp status that tells you at a glance if the night is safe." A single warm ember that brightens as unattended work lands cleanly and dims on a block is the lowest-effort, highest-feel signal.
  Done when: the ember's brightness maps to the count of clean overnight closes, and it dims on any Ward refusal, visible from across a room.

- **Turn the 2.4 GB state into a visible "weight" you can set down** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: The user cares about Sampo "not eating the whole CPU" and about *cost of being interrupted.* A tiny "luggage tag" on the status bar showing injected characters and total state weight, with a one-keystroke "set it down" that prunes cold state and *physically shrinks* the number, gives a tactile reward.
  Done when: `samo set-down` prunes a measurable byte amount and the status tag visibly drops, with a soft "clunk" motion.

- **Wild: Give the forge a *season* you can scrub** — FEATURE — value 5 — effort L — risk med — category: delight
  Why: "A 60-second season recap you can scrub on the phone" was proposed but only as a report. Make it *playable*: drag the astrolabe's sky forward/back a day, and the forge plays that day's closes as a time-lapse of hammer strikes and flame flares, with a one-line caption per close. Delight = *reliving* your own work.
  Done when: scrubbing the sky to last Tuesday replays that day's closes as distinct flame flares with a caption, and it runs on a phone without audio.

- **Wild: The forge *sighs* when you let it sleep** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: "Let the user's silence be a label" is a label idea; the delight twin is that the forge *responds* to your stillness — when the user goes quiet for a set window, the forge exhales: the flame steadies, the astrolabe slows, and a one-word word ("resting") appears. It makes the tool feel *alive to you*, not just busy.
  Done when: after a user-configured quiet period, the UI transitions to a slower, dimmer "resting" state with a single word, and returns to working state on the next keystroke.

- **A "what I stopped doing" scroll that *peels*** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: "Show what Sampo stopped doing after a rename" is a list idea; the craft is that it *peels* away like a forge's scale — each item lifts and falls off as the new behaviour lands. Small, show-able, and it turns a chore (migration) into a small spectacle.
  Done when: after `samo migrate`, a "what I stopped doing" panel peels off items one by one as their successor capability first fires.

- **Let the user *strike a test* on the anvil** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: The discipline layer proves work with "commands it really ran." The delight: when a test goes green, the user can *physically* strike the onscreen anvil (a tap or a key) and the test's pass is stamped into it as a small mark. Turning verification into a tactile ritual.
  Done when: a green test can be "struck" by the user, leaving a permanent small mark on the anvil view tied to that test's hash, viewable in the museum.

- **Wild: A "morning after" that smells of the forge** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: "A 60-second morning after haiku" was proposed as text. Push to *synesthesia*: the morning card opens with a single 8-second ambient sound (a low forge hum that rises and settles) plus the haiku, tuned to the night's outcome — clean night = calm hum; a block occurred = a faint clank.
  Done when: the morning card emits a distinct 8s ambient per outcome class (clean/block/stall), and the sound is skippable and respects the user's reduced-motion setting.

- **Turn the "unproven" shelf into a *glass case* you can open** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: "Unproven shelf grouped by reason" is a list. The delight: it's a small glass case on the web UI; clicking a claim *slides the glass open* and shows the exact command, output, and the age of its proof (or the reason it's unproven). A tiny "show me" ritual that builds trust.
  Done when: clicking any unproven claim slides open a panel showing the checking command, output, and staleness date, and closing it slides the glass shut.

- **Wild: The forge keeps a *museum* you can walk** — FEATURE — value 5 — effort L — risk med — category: delight
  Why: "The forge keeps a museum chime" and "frozen museum model" are proposed. Make it *walkable*: a side pane (or a URL) where every past strike, abstain, and block is a small artefact on a shelf — a pass is a forged ingot, an abstain a held rune, a block a cold mark. You can *walk the shelves* of your project's history.
  Done when: the web UI exposes a "museum" view listing each historical verdict as a distinct artefact, and it grows one entry per close/block/abstain.

- **Make the *block* feel like the Ward, not an error** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: A Ward refusal currently reads as a failure. The delight: when the Ward blocks, the screen *cools* — the forge's flame dims to a blue ember, the astrolabe's needle locks, and a single engraved line appears ("held by the Ward"). It reads as *protection*, not punishment, reinforcing the safety story the user keeps selling.
  Done when: a Ward block transitions the UI to a cooled "held" state with one engraved line naming the rule, and returns to working state when the user retries.

- **A one-line "what the forge is *smelling*" in the status bar** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: "Give the user a Sampo-is-thinking reason line" is a spinner idea. The craft: a single rotating word that names the current internal state in forge-idiom ("kindling," "striking," "quenching," "resting"), so the user *feels* the phase without a dashboard.
  Done when: the status bar shows one of a fixed small set of forge-idiom phase words that changes with the drive's state and is stable within a phase.

- **Wild: Let the user *name a sound* for a verdict, once** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: "Sonify the night as eight embers, and let you name the sound" was proposed. The personal touch: the *first* time each verdict type (pass/block/abstain) fires, the forge offers a one-line prompt to assign it a name ("the clank," "the ring"), stored per user. The tool then *uses your word*, making the sonification theirs.
  Done when: on first fire of each verdict class, a one-line prompt appears to assign a name, and subsequent plays of that verdict use the stored name in the morning card.

- **Make the *first run* a small ritual, not a tutorial** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: T-0862/0863 (newcomer tour, start ladder) are deferred and evidence is thin. The delight: instead of a tour, the first `samo` command strikes the anvil once and forges a single rune that becomes the project's mark — a "birth" moment that ties the identity (runestone logo) to the user's first act.
  Done when: the first ever `samo` command in a fresh project forges a unique rune tied to that project's id, and it appears on the logo plate and morning card thereafter.

Next question: does the user actually *hear* and *feel* the UI (do they run it with audio/haptics on), or is the delight purely visual — because several of these bet on sound and haptics, and I can't tell from the pack whether a screen-reader or muted context is the norm.
Next question: which single surface does the user *live* in most (the terminal pane, the web UI, or the phone) — the pack lists all three but never which one they look at when they say "the forge," so the strike/season/museum ideas should land on the right one first.
