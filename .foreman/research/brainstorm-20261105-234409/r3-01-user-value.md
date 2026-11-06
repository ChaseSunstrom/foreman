# Brainstorm — lens: user value

- **Show "minutes given back" in the morning card, net of false alarms** — FEATURE — value 5 — effort S — risk low — category: value visibility
  Why: The user steers "I want it to still get done without burning a fuck ton of money, and quick" and keeps dropping work Sampo filed that it already knew. The pack's T-0795 and T-3340 ask "Measure what the user feels," but no idea yet prints a *net* number. Evidence: 80+ standing steers and a 2.4 GB state mean Sampo's value is invisible inside its own noise.
  Done when: `sampo doctor` and the web UI show one line: "Gave back X min this week (Y false alarms cost Z min), measured from closes you didn't re-ask."

- **Predict the user's pushback on the next close, before it ships** — FEATURE — value 5 — effort M — risk med — category: anticipation
  Why: The user's own words are dominated by pushbacks: "not a breakage," "stale," "absorbed by T-2893." They keep saying "I didn't ask for that" about Foreman-filed items (T-2450 class). The need behind this: Sampo files work, the user reverts or drops it, and the friction is the *surprise*. No idea drafts the user's *objection* in advance.
  Done when: at `fm task finish`, a one-line "you might say: ___" appears, derived from the user's last 30 drops/reverts; a "not a problem" key dismisses it and trains the model.

- **Make "I meant X, not Y" propagate in one keystroke** — FEATURE — value 5 — effort S — risk low — category: correction
  Why: The user repeatedly corrects interpretation: "not a breakage," "stale," "absorbed by T-2893," "the repo mirror is still named .foreman/." Each is a one-word fix that Sampo then has to re-learn. The pack has "Turn each pushback into a probe" but not a *live* propagation: fix the meaning once, watch it land in the pack, the grid and the next brainstorm.
  Done when: typing `fm meant X not Y` rewrites the open brief, the Mission grid cell and the injected steer, and the next `sampo decide` uses the corrected reading — verifiable in the diff.

- **Let the user's silence be a label, with a visible trust score** — FEATURE — value 4 — effort S — risk med — category: signal
  Why: The user steers "Treat the user's silence as a label" and "show the user's own undo rate as a trust score per capability." Drops in the pack ("not a breakage," "stale") are *silence with a reason*. No idea computes, per capability, "you ignored me N times; I'll stop proposing this class." This directly serves "don't burn money" by cutting low-trust noise.
  Done when: `sampo status` shows a per-slot trust bar (0–1) from silence/undo; a slot below 0.3 goes quiet until the user re-arms it.

- **Show "what Sampo stopped doing" after each model adoption** — CLEAN — value 4 — effort S — risk low — category: legibility
  Why: The user steers "Show the decider's 'I'd know it's done when…' as a struck line" and the standing rule that a capability must beat a free arm. When a model replaces a rule, the user has no receipt of what *disappeared*. Without it, "is it still earning its tokens?" (T-3340) can't be answered. Evidence: the rename itself (Foreman→Sampo) shows the user cares about visible deltas.
  Done when: each adoption card lists, in plain words, the exact rule or prompt the model supersedes, with a one-key "revert to rule" that actually reverts.

- **Pre-stage the "ship the landed commits" ask at idle, so the user never types it** — FEATURE — value 4 — effort S — risk low — category: friction
  Why: The user's words show they repeatedly end sessions with landed, unshipped work ("fm ship can't ship a branch that touched a file fm genesis live keeps publishing to main"). The standing push grant ("feel free to push to main") means this ask is *pre-approved* — yet Sampo waits. The need: stop asking for permission the user already gave.
  Done when: at Stop, if a branch is green and within the standing push grant, Sampo ships it and prints "Shipped T-NNNN under your standing grant; say 'hold' to stop this class."

- **Name the single user action that frees each blocked task, ranked** — FEATURE — value 4 — effort M — risk low — category: unblocking
  Why: The pack's open work is full of "blocked" (T-0325, T-0335, T-0862…) and the user steers "Blocked work never sits." But the user can't unblock what they don't know they're blocking. T-3340 ("Measure what the user feels") and T-0863 ("Start ladder") both point here. No idea ranks blocked items by *what one user click frees*.
  Done when: `fm next` leads with "To unblock: (1) install libappindicator — unblocks T-0325; (2) grant X — unblocks 3 tasks." Each is one action, not a task.

- **Print "the one thing I'd ask you if I could" at session close** — FEATURE — value 3 — effort S — risk low — category: intent
  Why: The user's own words are a stream of *unasked* follow-ups (the "Missed asks" class, T-3339). They keep saying "we will want it to be a generic model" and "maybe brainstorm on features the model should have" — ideas they haven't formally asked for. A single line at close surfaces the latent ask *without* a dashboard.
  Done when: at close, one line: "If I could ask one thing, it'd be: ___" derived from the session's near-misses; the user can answer with one word or ignore.

- **wild — Show the cost of *being interrupted* as a live gauge** — FEATURE — value 4 — effort M — risk med — category: friction
  Why: The user's standing rule "Never interrupt the user mid-run" exists *because* interruptions cost them. But no idea measures it. The user drops work when Sampo interrupts ("dropped: CI failed on main"), then Sampo re-files it. The need: a gauge that prices each interruption in re-focus minutes, so Sampo can self-suppress low-value noise.
  Done when: the pane header shows "Interruptions this week: N (≈ M min re-focus)"; Sampo routes below-threshold events to the morning card instead of the live session, and the user can watch the gauge drop.

- **wild — Let the user "rehearse" a decision without committing it** — FEATURE — value 4 — effort L — risk med — category: safety
  Why: The user steers "Let the user *rehearse* a decision without committing it, with a rollback guarantee" and "Never block on the user… pick the option most consistent with gen-0." The tension: Sampo must act *and* the user must feel safe. The need behind "feel free to push": they want *reversibility*, not more permission. A dry-run that shows the diff *and* its blast radius before the verb fires.
  Done when: `sampo <verb> --rehearse` prints the exact diff, the files touched, the Ward verdict and the one-key undo; the user types the verb bare to commit. No state changes on rehearse.

- **wild — A "Sampo is earning it?" one-line verdict in `sampo doctor`** — FEATURE — value 5 — effort M — risk low — category: value visibility
  Why: The user's words keep circling "Measure what the user feels" (T-3340) and "is Sampo still earning its tokens?" (T-3340). The 2.4 GB state, 80+ steers and 20+ blocked tasks mean the user *suspects* Sampo is overhead. The single number they'd trust: a weekly, net-of-false-alarms verdict in plain words. This is the *summary* of every value idea above, and it's the one they'd actually read.
  Done when: `sampo doctor` ends with "Earning it: YES — gave back 42 min, 3 false alarms, cost $1.20" or "Earning it: NO — net −6 min; quiet the 2 lowest-trust slots?" with a one-key fix.

- **wild — "I'll be annoyed if…" — let the user name their frustration in one line at intake** — FEATURE — value 4 — effort S — risk med — category: intent
  Why: The user's pushbacks are *emotional* ("without burning a fuck ton of money," "I don't want to just cap the cost"). The pack has "Ask for an 'I'll be annoyed if…' line at intake" (goal lens) but never wires it to the decider. The need: capture the *feeling* behind a task, not just the spec, so Sampo optimizes for the thing that actually irritates.
  Done when: at `sampo task add`, an optional "I'll be annoyed if ___" line is stored on the brief; the decider uses it as a tie-breaker and the morning card reports "T-NNNN: your annoyance condition was met/avoided."

Next question: Which of the user's last 30 drops was the *most* surprising to them, and does any current capability predict it — if not, that's the first slot to build.
Next question: When the user says "feel free to push to main," do they *actually* want Sampo to push unshipped-but-green branches at Stop, or only branches they explicitly named — and what's the one action that would make that safe?
