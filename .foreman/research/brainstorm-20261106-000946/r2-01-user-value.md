# Brainstorm — lens: user value

- **Turn every "I had to type this twice" into a standing rule in one keystroke** — FEATURE — value 5 — effort M — risk low — category: unspoken needs
  Why: The user’s standing rule (2026-10-30) says "every user steer becomes a standing rule plus an automatic check in the same task." Yet the "blind spots" list shows the user had to *ask* for features like "blocked work never sits" and "the drive holds Foreman-filed items" that Sampo *should have inferred* from repeated corrections. The need is: Sampo should auto-detect when a phrase is a *class* (not a one-off) and propose the standing rule before the user files it. Evidence: T-0217 (lessons carry confidence) is deferred; the user keeps re-stating the same class of complaint.
  Done when: `samo teach "I don't want X"` files a standing-rule candidate with a confirm prompt; after 3 similar phrases across sessions, Sampo auto-files the rule with a "you told me once" receipt.

- **Show "what you no longer have to check" as a *living list*, not a receipt** — FEATURE — value 4 — effort S — risk low — category: unspoken needs
  Why: The user’s words: "I don't want to just cap the cost… I want it to still get done without burning a fuck ton of money, and quick." The morning card already promises "what you no longer have to do," but the "ideas so far" list shows it’s a one-time print. The user wants a *standing dashboard* of their own reduced cognitive load, so they can see the compound effect. This is the "cost of being interrupted" gauge made visible.
  Done when: `samo status` prints a "You no longer have to: [list]" line, updated as capabilities land, with a "since when" stamp per item.

- **Pre-draft the user’s *next* pushback on the pending close, and let them correct before Sampo ships** — FEATURE — value 5 — effort M — risk med — category: unspoken needs
  Why: The user’s words: "the forge answers back" and "pre-draft the user's pushback on the next close, so they can correct Sampo before Sampo ships." The "ideas so far" list has this, but it’s not wired. The need is: Sampo should *anticipate* the user’s objection from the user’s own phrasing history and present it as a draft *before* the user types it, so the user can strike or confirm with one key. This is the "answers in your voice" head made real.
  Done when: Before a close, `samo close` shows a "You might say: [draft]" line; the user presses `y` to confirm, `n` to edit, and the confirmed version becomes the close receipt.

- **Make "Sampo is earning its tokens?" a *live number* in `samo doctor`, updated per session** — FEATURE — value 4 — effort S — risk low — category: unspoken needs
  Why: The user’s standing rule: "Lean substance (T-2503): growth whose capability has no exam or outcome measurement yet waits." The user wants to see, in real time, whether Sampo’s overhead is justified. The "ideas so far" list has "one-line 'is Sampo still earning its tokens?' in `samo doctor`," but it’s not built. The evidence: T-1231 (Sampo beats Claude Code on the duel) is deferred; the user is paying for Sampo’s overhead without a clear ROI number.
  Done when: `samo doctor` prints "Sampo earned X minutes this session; spent Y tokens; net: +Z" computed from the ledger.

- **A "no-model" baseline that the decider must *beat* every Rune, or the slot retires** — FEATURE — value 5 — effort M — risk low — category: unspoken needs
  Why: The user’s standing rule: "a capability whose free arm beats the session arm on the same scenarios is a top gap." The decider is being trained, but there’s no *permanent* baseline to beat. The "ideas so far" list has "wild — run a 'no-model' zero-model mode as a permanent arm," but it’s not wired. The need: every decider slot must show its delta over plain retrieval (kNN) on every Rune generation, and if it doesn’t beat it, the slot is flagged for retirement.
  Done when: Every Rune generation’s scorecard includes a "decider vs. kNN" row per slot; a slot that underperforms for 3 consecutive generations is auto-filed for retirement.

- **Wild: The decider *dreams* the user’s next bad week and pre-stages the fix** — FEATURE — value 5 — effort L — risk high — category: unspoken needs (wild)
  Why: The user’s words: "Bet on predicting the user's next bad week and pre-stage the fix." The "ideas so far" list has "wild — dream the decider's mistakes overnight," but it’s about *Sampo’s* mistakes, not the *user’s* bad week. The user’s own words: "I don't want to just cap the cost… I want it to still get done without burning a fuck ton of money, and quick." The need: Sampo should predict *when* the user is likely to hit a wall (from their own rhythm, from the ledger) and pre-stage the *specific* fix (the card, the trigger, the task) *before* the user hits it.
  Done when: `samo dream` runs overnight and produces a "next bad week forecast" with 3 pre-staged fixes, each with a "why I think you’ll hit this" line, shown on the morning card.

- **Wild: Let the user’s *silence* be a first-class label, with a *visible trust score* per context** — FEATURE — value 4 — effort M — risk med — category: unspoken needs (wild)
  Why: The user’s words: "Let the user's silence be a label, with a visible trust score." The "ideas so far" list has this, but it’s not built. The user’s own words: "I don't want to just cap the cost… I want it to still get done without burning a fuck ton of money, and quick." The need: Sampo should interpret the user’s silence *per context* (e.g., "silence after a close" = satisfied, "silence after a steer" = Sampo should have acted), and show a *trust score* per context so the user can see where Sampo is over- or under-interpreting.
  Done when: `samo status` shows "Silence trust: close=92%, steer=64%, ask=81%" with a "what I assume" line per context; the user can veto an interpretation with one key.

- **Wild: A "Sampo is gone" morning — weekly, disable *every* Sampo capability for one live session and log what the user had to do by hand** — FEATURE — value 5 — effort M — risk med — category: unspoken needs (wild)
  Why: The user’s words: "a 'Sampo is gone' morning: weekly, disable every Sampo capability for one live session and log what the user had to do by hand." The "ideas so far" list has this as wild, but it’s not built. The need: the user wants to *feel* the cost of Sampo’s absence, not just see it in a dashboard. This is the "cost of being interrupted" gauge made *experiential*. The user’s standing rule: "no idea is killed for ambition." This is the "Sampo’s last day" drill, made routine.
  Done when: `samo gone` runs a 30-minute session with all Sampo capabilities off; the ledger records every manual action the user took; the morning card shows "Last week, without Sampo, you spent X minutes on Y."

- **Show "what I left out" as a *permanent shelf*, not a one-time receipt** — FEATURE — value 4 — effort S — risk low — category: unspoken needs
  Why: The user’s words: "a 'what I left out' line on the morning card, not just every Mission." The "ideas so far" list has this, but it’s not built. The user’s own words: "I don't want to just cap the cost… I want it to still get done without burning a fuck ton of money, and quick." The need: the "left out" list should be a *standing* surface, so the user can see what Sampo *chose not to do* and why, and can promote any item with one key.
  Done when: `samo status` shows a "Left out: [list]" section with a "why" per item and a "promote" key; the list persists across sessions.

- **Turn a one-off correction into a standing "you told me once" clause *automatically*, with a confirm prompt** — FEATURE — value 4 — effort M — risk low — category: unspoken needs
  Why: The user’s standing rule: "every user steer becomes a standing rule plus an automatic check in the same task." The "ideas so far" list has "turn every pushback into a 'you told me once' receipt," but it’s not built. The user’s own words: "I don't want to just cap the cost… I want it to still get done without burning a fuck ton of money, and quick." The need: Sampo should detect when a correction is *repeated* (same class, different phrasing) and auto-file the standing rule with a "you told me once" receipt, so the user doesn’t have to re-type it.
  Done when: After 3 similar corrections across sessions, `samo teach` auto-files a standing rule with a "you told me once: [original phrase]" receipt and a confirm prompt.

- **Wild: The forge *sighs* when you let it sleep — a one-line "morning after" haiku for each overnight close** — FEATURE — value 3 — effort S — risk low — category: delight (wild)
  Why: The user’s words: "the forge keeps a 'museum' chime" and "a 'morning after' haiku for each overnight close." The "ideas so far" list has this, but it’s not built. The need: the user wants *emotional* feedback from Sampo, not just a dashboard. The "sigh" is a small, playful touch that makes Sampo feel *alive* and *aware* of the user’s absence. It’s the "strike on the phone too" idea, but for the *user’s* return.
  Done when: On session start after an overnight run, `samo status` prints a one-line haiku summarizing the night’s work, with a "sigh" sound (opt-in) that plays once, then goes quiet.

- **Let the user *rehearse* a decision without committing it, with a *rollback guarantee*** — FEATURE — value 4 — effort M — risk low — category: unspoken needs
  Why: The user’s words: "let the user *rehearse* a decision without committing it, with a rollback guarantee." The "ideas so far" list has this, but it’s not built. The need: the user wants to *try* a decision (e.g., "what if I said no to this steer?") and see the *consequences* before committing. This is the "what would break if I said no?" idea, made *interactive*.
  Done when: `samo what-if` lets the user draft a decision, shows a "what would break" line, and a "rollback" key that reverts the draft without touching the ledger.

- **Wild: A "cost of being interrupted" gauge that is *visible*, not inferred — with a "since when" stamp** — FEATURE — value 4 — effort S — risk low — category: unspoken needs (wild)
  Why: The user’s words: "a 'cost of being interrupted' gauge that is visible, not inferred." The "ideas so far" list has this, but it’s not built. The need: the user wants to see *exactly* how many times Sampo interrupted them *this week*, and *what* the cost was (in minutes, in lost focus). This is the "Sampo is earning its tokens?" number, but from the *user’s* side, not Sampo’s.
  Done when: `samo status` shows "Interrupted you: 4 times this week; cost: ~12 min (est.); since: [date of last interruption]".

- **Show the *user’s own* undo rate as a *trust score* per capability, updated per session** — FEATURE — value 4 — effort S — risk low — category: unspoken needs
  Why: The user’s words: "show the user's own undo rate as a trust score per capability." The "ideas so far" list has this, but it’s not built. The need: the user wants to see *their own* pattern of undos, so they can calibrate how much trust to give Sampo per capability. This is the "silence is not consent" label, but for *undo* behavior.
  Done when: `samo status` shows "Your undo rate: close=12%, steer=5%, ask=3% (this session)" with a "what I assume" line per capability.

- **Wild: A "Sampo’s last day" drill that the user can trigger on *any* capability, with a *one-key* revert** — FEATURE — value 5 — effort M — risk med — category: unspoken needs (wild)
  Why: The user’s words: "a 'Sampo’s last day' drill that the user can trigger on any capability." The "ideas so far" list has this, but it’s not built. The need: the user wants to *test* whether a capability is *really* earning its place, by *removing* it for one session and seeing what breaks. This is the "Sampo is gone" morning, but for *one* capability, not all.
  Done when: `samo retire --capability X` disables capability X for one session; the ledger logs what the user had to do by hand; the next session shows "Without X, you spent Y minutes on Z; keep or retire?"
