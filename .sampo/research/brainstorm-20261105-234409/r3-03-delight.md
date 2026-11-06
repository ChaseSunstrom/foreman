# Brainstorm — lens: delight

Lens: delight. The pack’s own design language is a fuse: Kirjokansi’s brass astrolabe under a turning sky, Ilmarinen’s forge (heat = “running now”), the living machine (blueprint linework). And “Work in progress is published, not held.” The delight here is not a sticker on top of a decider; it’s making the *model* feel like an instrument you trust — its verdicts as struck metal, its learning as a forge you can watch, its doubt as a held rune. Best first.

- **Strike the verdict on the close, then let it ring** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: “Sampo’s look” says heat is the “running now” signal and the hammer’s motion trail is a signature element (T-2964). Every close already carries a three-valued verdict. A tiny hammer strike on the close glyph, one soft ring that fades as the run cools to “settled,” makes a model-backed decision feel forged, not printed.
  Done when: a close animates the strike once and the glyph dims to settled state; `prefers-reduced-motion` shows a static tint instead.

- **Show the forge answer, in your words, at the block** — FEATURE — value 5 — effort M — risk low — category: delight
  Why: the decider’s whole point is “a better decider.” A Ward block or a model abstain is the worst moment. Render the *reason* as one line in the user’s own compression — the phrase they keep reusing — beside a plain “here’s the safe equivalent.” The forge answers back when you’re about to hit the anvil wrong.
  Done when: a refused decision prints one user-phrased line plus a safe-equivalent command, sourced from the decider’s nearest-verified run, not a static string.

- **The morning card is a forge log, read like a night road** — FEATURE — value 4 — effort M — risk med — category: narrative
  Why: “Re-sync site to the converged illustrated forge: the redrawn eight stations as one night road with station lamps.” The overnight unattended work already exists; render it as the eight stations lighting in order, each lamp = a capability that earned its tokens. A dead-lamp = a capability that went silent (the “what I stopped doing” diff).
  Done when: the morning card lays out eight stations, lit/unlit by overnight outcome, and a cold reader can name one lit and one unlit capability from the image alone.

- **Abstain as a held rune, not a grey failure** — FEATURE — value 5 — effort S — risk low — category: state
  Why: the standing rule demands every model abstain with a measured coverage-vs-accuracy curve; “assumption: the abstain currently renders as a neutral error.” A held rune — brass, unstruck, with the abstain reason engraved — makes “I don’t know” feel like deliberate craft, and invites the one-key veto.
  Done when: an abstain renders the held-rune state with its reason in ≤12 words and a single “veto this class” key, distinct from the error state.

- **One-keystroke “ah” on every moon, trained across generations** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the site/tower lead with the wildest moons; “a one-keystroke ‘ah’ grade” was already a delight note. Grade the top three moons per generation with one key; the taste file feeds the funnel’s wildness floor.
  Done when: pressing one key on a moon records a taste row that the next funnel run reads, and a cold reader sees the taste count on the moon.

- **Teach the forge a phrase by saying it once** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: “Let the user teach Sampo a new phrase by saying it once, with a confirm.” Type a correction, confirm, and it becomes a struck line in the lesson ring — visibly added to the ring, not a hidden config edit.
  Done when: a confirmed phrase appears as a new struck line in the lesson ring within one session and is cited by the next model decision that matches it.

- **Sonify the funnel as eight ember chimes** — FEATURE — value 3 — effort M — risk low — category: audio
  Why: “Sound the funnel as ambient audio” is already in the design. One soft chime per funnel stage that advances, eight total, off by default — the instrument’s ambient hum, not a notification storm.
  Done when: advancing through eight stages produces eight distinct chimes, and a mute switch silences them with a visible lamp.

- **Scrub a week as a 60-second “season recap”** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: “A 60-second ‘season recap’ you can scrub on the phone.” Compress a week of closes into a scrubbable strip, one frame per close, colour by outcome. Delight = the user seeing their whole week as a film they can skip through.
  Done when: a week renders as a scrubbable strip on the phone; scrubbing to any frame shows that close’s one-line verdict.

- **Rehearse the veto without committing** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: “Let the user rehearse a decision without committing it, with a rollback guarantee” and “What if I said no to this steer?” Pressing “no” on a steer shows what would break (blast radius) without changing it. Delight = power with a safety catch.
  Done when: a “rehearse no” on any open steer shows the blast-radius list and leaves the steer unchanged on release.

- **wild — The decider keeps a “museum” chime** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: a frozen first-generation model re-runs on every close forever (the museum tripwire). When the live and museum deciders *disagree*, play one distinct bronze chime and pin a “the old forge disagrees” rune. Delight from the machine noticing its own drift, audibly.
  Done when: a live/museum verdict disagreement triggers the bronze chime once and shows the museum’s verdict on the close card.

- **wild — A “morning after” haiku for each overnight close** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: unattended work already lands un-witnessed. The local model writes a three-line haiku from the close’s own ledger line, stamped “unwitnessed until you read it.” Small, surprising, and a human-shaped receipt for machine work.
  Done when: each overnight close carries a haiku generated from its ledger, marked unwitnessed, and it appears on the morning card.

- **wild — The forge answers back in *your* voice** — FEATURE — value 5 — effort L — risk high — category: delight
  Why: the user’s own compression is the highest-value data in the pack; the standing intent is to work in their compression. A tiny head that, at the block and at close, drafts the decider’s one-line verdict *in the user’s recurring phrasing* (their repeated words), confirmed by a diff against their actual words. The machine stops sounding like a machine.
  Done when: the decider’s one-line verdict uses at least one of the user’s recurring phrases, and a “this is how I’d have said it” diff matches their actual close text within edit distance on a held-out set.

- **wild — Ring the astrolabe on a first** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: “Ring the astrolabe on a first.” The first time any model slot beats the rules arm on a held-out case in a generation, the astrolabe in the sky turns once and rings. A rare, earned moment — delight from the instrument marking a genuine advance, not a routine pass.
  Done when: a slot’s first measured beat-over-rules in a generation triggers one astrolabe turn + ring, and it does not re-trigger for the rest of that generation.

- **A “silence is not consent” lamp that glows when you’ve gone quiet** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: the user treats silence as a label. A soft lamp that glows when the user has gone quiet past their learned window — not a nagger, a held rune in the sky saying “I’ll keep working; ping me if you’ve changed your mind.”
  Done when: silence beyond the learned window lights the lamp and the next action waits rather than assuming consent.

Next question: What single moment in the decider’s life feels most like *craft* to this user right now — the block, the close, or the abstain — so the strike/forge motion goes where they’ll feel it first?
Next question: Is the user’s actual phrase-frequency high enough to make the “answers in your voice” head honest, or do I need a minimum-vocabulary floor before that slot can claim delight rather than parody?
