# Brainstorm — lens: delight

- **Show the decider’s verdict as a forged rune in the pane** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: Sampo’s world is Kirjokansi + Ilmarinen’s forge; the request is a "decider." A tiny runic glyph that strikes on (green) or holds (amber) when the model decides, with the forge’s heat as the "running now" signal, fits the existing look (steer 2026-11-03) and makes a model slot legible at a glance.
  Done when: every model-backed decide() renders the glyph + a one-line plain reason in the Sampo pane, and `sampo status` shows it on the status line.

- **Sound the funnel as eight ember chimes on the web UI** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The site already converged on "eight stations as one night road with station lamps" (critique 7); a soft ember tick as a moon crosses a funnel stage (kill, tier, promote) turns a 3-minute batch into a perceptible pulse, honoring "more animated and fluid."
  Done when: enabling a toggle plays a distinct low-volume tick per stage crossing, respects reduced-motion/`prefers-reduced-motion`, and is silent by default.

- **A "model saved you X" receipt per session, struck in the forge** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: The user steered "I want it to still get done… without burning a fuck ton of money, and quick." A close-time receipt that names the concrete decision the model made and the cost/time it avoided (in the user’s words) is the tangible proof the model earns its tokens — the "what you no longer have to do" line made personal.
  Done when: `samo finish` prints one forged-stamp line per session naming the top model decision and its measured save, with a `--quiet` to suppress.

- **Strike the metal on the close (one chime, then quiet)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: Steer 2026-11-03 makes fire the "running now" signal and the forge the place generations are forged. A single, non-repeating "clink" when a task closes (and silence otherwise) gives the joy of completion without becoming notification noise — "chime once, then go quiet."
  Done when: a close plays one short sound (opt-out flag), and a closed task with no further model action stays silent.

- **Ghost-text the next ask on the prompt line** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: The user keeps re-asking (T-3340 "measure what the user feels"; repeated late asks in "What earlier brainstorms missed"). Typing the predicted follow-up as dimmed ghost text the user can Tab-accept turns anticipation into a tactile, low-commitment delight and makes a wrong guess instantly visible and dismissible.
  Done when: after a close, `sampo` offers one Tab-able ghost-text suggestion per session, sourced from the anticipation ledger, and pressing anything else clears it.

- **Let the model refuse the work, and show the refusal as a held rune** — FEATURE — value 3 — effort S — risk med — category: delight
  Why: "Give the decider an 'I don't know, here's why'" plus the user’s push for honest abstention. Rendering a refusal as an amber held rune with a one-line reason is a satisfying, dignified way to surface abstain rather than a silent fallback, and it teaches the user what the model will *not* do.
  Done when: an abstain renders the held-rune glyph + reason in the pane and `samo status`, and a follow-up `--retry` re-prompts.

- **The forge answers back: type a phrase once, confirm, and it’s a lesson** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: The user repeatedly corrects Sampo in plain words ("I meant X, not Y", "not a breakage:"). A delight loop where saying a correction once, pressing a confirm key, shows the phrase etched into a "taste rune" the user can strike through — makes teaching feel like forging, not editing config.
  Done when: a one-keystroke confirm after a correction files it into the taste file, shows the etched glyph, and `samo teach` lists them, strikethrough to delete.

- **A 60-second "season recap" you can scrub on the phone** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: Steer "manage all of that across sessions too" and the phone-surface gap (thin: devices). A swipeable 60s recap of the night — what closed, what held, what the model decided — as a small forge-log the user reads over coffee, with one tap to undo a landed change, is the delight that shows others.
  Done when: the morning card renders as a scrubbing recap on the phone surface, and a tap reverts one closed task.

- **Wild: Sonify the night as eight embers, and let you name the sound** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: The site is "one night road with station lamps." Turning the eight funnel/night stages into a low ambient 8-note ember sequence the user can rename per stage ("my kill stage sounds like rain") is playful, personal, and shows-off-able; it’s nobody’s ask but the user would love it.
  Done when: `samo night --sonify` plays the 8-note sequence and `samo ember name STAGE WORD` persists a per-stage label.

- **Wild: "What if I said no to this steer?" — rehearse a veto without committing** — FEATURE — value 4 — effort M — risk med — category: delight (wild)
  Why: The user steers a lot and pushes back often; the delight of *agency* is previewing the blast radius of a veto. A dry-run that shows, from the ledger, which open tasks a veto would stall or unblock, with a guaranteed rollback if they change their mind, makes governance feel tactile.
  Done when: `samo whatif VETO STEER-ID` prints the affected tasks and a rollback guarantee, and issuing the veto logs it with an auto-revert handle.

- **Wild: A "morning after" haiku for each overnight close** — FEATURE — value 3 — effort S — risk low — category: delight (wild)
  Why: "Give each trigger a 'morning after' haiku receipt" already appears for triggers; extending the same delight to model-driven overnight closes — one 17-syllable haiku naming what was done and held — is a small, shareable surprise that fits the runestone/poetic register (Kalevala, the user’s own lore).
  Done when: each overnight model close writes a haiku into the morning card, generated from the ledger (local, no frontier call).

- **Show the decider’s "I’d know it’s done when…" as a struck line** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The user’s own words repeatedly define success in their phrasing ("the tests went green and its closes held"). Surfacing the model’s stated done-condition as a struck-through line that lights up when the evidence satisfies it makes the decider’s confidence visible and the close feel earned.
  Done when: each model-backed close shows its done-condition line dim, struck solid when the bound evidence passes, in the pane and `samo status`.

- **Wild: A "silence is not consent" lamp that glows when you’ve gone quiet** — FEATURE — value 3 — effort S — risk low — category: delight (wild)
  Why: The user treats silence as a label ("no response in 48h = not wanted") and steered "let the user’s silence be a label." A gentle glowing lamp (not an alert) that rises as the user’s silence lengthens, with one tap to record "yes, not wanted," turns a passive signal into a small, dignified ritual.
  Done when: the lamp appears after the configured silence window on a pending model decision, and one tap files the "not wanted" label.

- **Ring the astrolabe on a first** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: Steer 2026-11-03: the astrolabe is the instrument and "more animated and fluid." A subtle astrolabe ring (a soft turn of the sky) when a capability lands its first-ever pass in a project — a "first" moment — rewards the user’s own history without constant noise.
  Done when: the first pass of a capability in a project triggers a single animated astrolabe ring on the web UI, once per capability per project, suppressible.

- **A "wrong calls" digest the model reads back, in your voice** — FEATURE — value 3 — effort M — risk med — category: delight
  Why: The user re-asks and corrects; a nightly one-line digest where the model, in the user’s compressed phrasing, names its own worst decision from yesterday and the fix it will try — "the forge answers back" — is a delight that also closes the improvement loop the request asks for.
  Done when: the morning card includes one model-authored line naming yesterday’s worst slot decision and its next attempt, drawn only from the regret ledger.

Next question: What does the user actually *hear* and *see* at the moment of a close and a veto, and which of those moments do they show to others — so I can put delight where the joy is real, not where I assume it is?
Next question: On which surfaces (web UI, phone, status line, terminal) does the user *actually* meet the decider, and which of those is where they’d want the rune, the chime, and the ghost-text to appear without becoming noise?
