# Brainstorm — lens: user value

Reading the pack through "user value": the user’s words scream *speed, no waste, and proof it helped*. They cap cost as a backstop, not a brake; they hate re-asking; they push on “generic” (not just this repo); and they keep filing things Sampo should have predicted (T-3312, 3316, 3340). The decider’s worth is only real if it measurably *earns* those. Most prior ideas cover training/serving; what’s thin is the **value evidence loop** and the **user-facing value surfaces**.

Best first:

- **Show “earned this week” as one net number in `sampo doctor`** — FEATURE — 5 — M — risk low — value-evidence
  Why: steers: “I want it to still get done without burning a fuck ton of money, and quick.” T-0867 (held-rate scorecard) and T-1231 (duel) exist but are deferred; nothing ties the decider to minutes/cost returned. A number, not a dashboard.
  Done when: `sampo doctor` prints `decider: +114 min, −$2.30 (n=41 decisions)`, computed only from ledger outcomes, and fails the gate if it can’t be re-derived.

- **Gate every adopted slot on a per-week “does it earn?” review** — PERFORMANCE — 5 — M — risk med — value-loop
  Why: standing rule “growth with no measurement waits.” A slot that stops earning is exactly the drift nobody catches. Ties the improvement loop to the user’s felt value.
  Done when: a slot whose earned-value falls below its token-cost for 2 consecutive weeks is auto-mooted to shadow and a one-line “why” is filed.

- **One-line “here’s what I stopped making you do” at session close** — FEATURE — 5 — S — risk low — unspoken-needs
  Why: user keeps re-filing what Sampo should auto-handle; the value only lands if they *see* it. This is the receipt that makes the decider feel real.
  Done when: closing a session where the decider pre-empted ≥1 ask prints the ask’s words, not a count.

- **Pre-empt the re-ask by detecting a premise that already moved** — FIX — 4 — M — risk med — unspoken-needs
  Why: user’s own drops show repeated “this is already true” moments. A decider that flags “your request assumes X, which changed at commit Y” removes the round-trip that costs them most.
  Done when: a request citing a stale premise is flagged before a lane starts, and the user confirms it in one key.

- **Turn a one-off correction into a standing “you told me once” clause, automatically** — FEATURE — 4 — S — risk low — capability
  Why: standing rule: every steer becomes a standing rule + check. Doing that *for the decider* means the model’s corrections stop being one-shot.
  Done when: the user’s “I meant X, not Y” on a decider verdict is stored and the next similar verdict uses it, with the source line shown.

- **Expose the per-class veto as “I always veto *this kind*”** — FEATURE — 4 — M — risk low — unspoken-needs
  Why: user already wants to veto a *class* (in ideas-so-far) but nothing lets them. One setting that suppresses a whole decision class they’ve never wanted is high-leverage and low-risk.
  Done when: `samo decide mute <class>` stops that class’s prompts for 30 days and the morning card counts them muted.

- **Show the user’s “cost of being interrupted” as a live, settable gauge** — FEATURE — 4 — M — risk med — delight
  Why: reads their pushback (“never interrupt mid-run”). Letting them *set* the interruption threshold makes the decider behave to their stated tolerance, not a guess.
  Done when: the decider consults the gauge before a prompt; raising it reduces prompt count on the next ledger, visibly.

- **Print “what would break if I said no to this steer?” at store time** — FEATURE — 4 — M — risk med — capability
  Why: they literally ask this (wild in prior list) but it’s not wired. Computing the blast of a steer *before* it’s baked gives the user leverage to accept/reject informed.
  Done when: storing a steer prints the named files/verbs it would constrain, derived not asserted.

- **wild — “Sampo is gone” morning: disable the decider for one live session, log every hand-ask** — wild — FEATURE — 4 — L — risk low — blind-spots
  Why: the only honest value measure is the counterfactual. Standing rule already pauses exams; a weekly “decider off” run gives the user proof it earns its place and catches silent over-reliance.
  Done when: one session runs with the decider muted; the morning card lists each ask the user had to make that the decider would have pre-empted.

- **wild — Let the decider draft the user’s *next* pushback before it’s said** — wild — FEATURE — 3 — L — risk med — delight
  Why: reads “predict the user’s next ‘I didn’t ask for that’.” If the model can forecast the complaint, the user can correct *before* the ship, collapsing the whole review round.
  Done when: at close, the decider offers one “I think you’ll object to X” line, and 30 days later it scores against actual user edits.

- **wild — Sonify the decider’s abstain as a held rune in the web UI** — wild — FEATURE — 3 — S — risk low — delight
  Why: thin surfaces: ui, devices. An abstain is currently a grey failure; a held, quiet rune (vs. a struck one) makes “I don’t know” legible at a glance and on a phone, and it’s the emotional core of the forge.
  Done when: an abstain renders as a distinct held-rune glyph + low chime, and a verdict renders struck, across web UI and phone.

- **Prove “generic” by a canary project the user never built** — FEATURE — 5 — L — risk med — capability
  Why: the user’s exact phrase: “we don’t want it to just work on the sampo repo.” No prior idea gives a *shippable* proof of cross-project value. A redaction+leave-one-project-out run on a throwaway repo is the acceptance test they can trust.
  Done when: the decider pre-empts ≥1 ask on a canary project with zero Sampo-specific text in its training rows, shown in the scorecard.

- **Retire a slot that never earned, with an obituary** — CLEAN — 3 — S — risk low — lean
  Why: standing rule: only proven harm or duplication removes an idea, reason recorded. Applying it to the decider’s own slots prevents the model zoo from silently growing past its value.
  Done when: a zero-earn slot is removed and a one-line “why it died” is in the registry.

- **One “decider off” switch that really changes behaviour** — FEATURE — 4 — S — risk low — capability
  Why: they keep asking for control (veto, mute, silence). A single honest off-switch, with a “what you lose” line, makes the value claim falsifiable by the user’s own hand.
  Done when: `samo decide off` routes all slots to the rules arm and the next `doctor` prints the earned-value delta of turning it back on.

Next question: does the user consider a *count* (“pre-empted 4 asks”) or a *felt* number (“+114 min”) to be the real value proof — because that decides whether the earned-value metric counts interruptions-avoided or minutes-recovered first.
Next question: on the canary project, what is the *minimum* number of asks the decider must pre-empt for the user to call it “generic enough” — the acceptance threshold that’s currently undefined and gates whether any training is worth shipping.
