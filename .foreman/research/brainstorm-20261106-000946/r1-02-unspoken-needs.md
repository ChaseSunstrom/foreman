# Brainstorm — lens: unspoken needs

- **Show the "I had to type this twice" shelf as a permanent surface** — FEATURE — 5 — M — risk low — category: trust
  Why: "What earlier brainstorms missed" and the user's own "missed ask" tasks are a *class*, not an accident — the user keeps re-asking because Sampo didn't hold the pattern. A visible, growing shelf of "the thing you had to say, that I should have inferred" is the unspoken need: *stop making me repeat myself*.
  Done when: `sampo missed` lists every repeat-ask with the two messages side by side, and a new one appears without the user filing it.

- **Turn a one-off correction into a standing "you told me once" clause automatically** — FIX — 4 — M — risk low — category: trust
  Why: "Turn each repeated user correction into a one-line standing-rule candidate" exists but is buried. The unspoken need is that the *second* time a user says "no, X not Y" Sampo should say "noted for always" and ask one yes/no, then never re-ask.
  Done when: the user's second identical correction produces a `fm decide` line that, on the third, silently applies with a receipt.

- **Surface "Sampo stopped asking me" as a weekly number** — FEATURE — 4 — S — risk low — category: trust
  Why: The user's push grant + "never interrupt mid-run" steers mean their hidden goal is *less interruption, not more capability*. A per-week "questions I would have asked you, that I decided instead" tally (with the decision and its reason) is the proof they're after: *I'm earning my silence*.
  Done when: the morning card shows "7 decided, 0 asked" and each line links to the `fm decide` record.

- **Predict the user's "I didn't ask for that" before it is said** — FEATURE — 3 — L — risk med — category: trust
  Why: The user's drops and pushbacks are almost all *reactions to Sampo acting*. The unspoken need: Sampo should flag, at plan time, "this will surprise you, here's why, and you can veto before I do it."
  Done when: a brief that touches a public surface or spends budget shows a "would surprise you" line, and the user's veto is logged.

- **Give the user's silence a meaning per context, not one global label** — FEATURE — 3 — M — risk low — category: trust
  Why: "Let the user's silence be a label" exists but is coarse. The user's own words show silence means different things: quiet after a close = satisfied; quiet on a push = unimpressed; quiet for a week = gone. One global rule will be wrong somewhere.
  Done when: three silence contexts (post-close, post-push, week-quiet) each produce a different logged decision, and one is wrong for 7+ consecutive days and is re-tuned.

- **Show "what you no longer have to check" as a standing list, not a receipt** — FEATURE — 3 — M — risk low — category: trust
  Why: "Print what you can stop checking" is a one-off. The unspoken need is a *permanent, shrinking* list: every item Sampo now owns ("CI is green, I don't check", "deps are current") with the date it was earned. This is the trust ledger the user hasn't named.
  Done when: `sampo owes` lists each owned check, its origin task, and it shrinks only when the user re-asserts the check by hand.

- **Name the "I didn't know Sampo could do this" moment and file it** — FEATURE — 3 — S — risk low — category: discovery
  Why: The user's own words ("the user had to make" asks) are mostly *discovery gaps*: they asked for something Sampo already had. The unspoken need: Sampo should detect "you typed an ask that matches an existing verb" and say "you don't need to type that, `sampo X` does it," then learn from it.
  Done when: an ask matching an existing verb shows the verb inline, and the next week the same ask is typed 0 times.

- **Pre-draft the user's "what would break if I said no" for risky steers** — FEATURE — 2 — M — risk med — category: trust
  Why: The user asks "what would break if I said no to this steer?" — the unspoken need is that Sampo should *compute* the blast radius of a steer before the user gives it, so the decision is informed, not guessed.
  Done when: `fm steer draft` prints the files, gates and open tasks a new steer would touch, before it is stored.

- **A "Sampo is thinking" reason line, not just a spinner, that survives a session restart** — FIX — 3 — S — risk low — category: trust
  Why: "Give the user a 'Sampo is thinking' reason line" exists but is per-session. The unspoken need: when a session dies and restarts, the *reason* for the current state should survive, not just the work. The user shouldn't have to re-derive "why is this running."
  Done when: a restarted session's first output names the current task, its stage, and the last reason for that stage, from the ledger not the model.

- **wild — A "cost of being interrupted" gauge that is visible, not inferred** — FEATURE — 3 — M — risk low — category: trust
  Why: "Show the user's cost of being interrupted as a live gauge" exists but is hidden. The unspoken need: the user wants to *see* Sampo respecting the rule it keeps re-stating. A gauge that goes up when Sampo fires an `fm ask` and down when it doesn't, visible in the status line, is the proof the user is asking for without saying it.
  Done when: the status line shows a number that decreases over a week with zero user complaints.

- **wild — A "what I'll be annoyed if" line at intake, compiled to a clause** — FEATURE — 3 — M — risk med — category: trust
  Why: "Give the user an 'I'll be annoyed if…' line at intake" exists. The unspoken need: the user can't always articulate their annoyance in advance, so Sampo should *offer* the line at the moment the task is filed, with a sensible default ("I'll be annoyed if you ship this without running the full suite") that the user can edit or strike.
  Done when: every `fm task add` shows a default annoyance line, and striking it is one keystroke, logged.

- **wild — A "Sampo's last day" drill that the user can trigger on any capability** — FEATURE — 2 — L — risk high — category: trust
  Why: "Hold a 'Sampo's last day' drill" exists but is monthly. The unspoken need: the user wants to *test* whether a capability is earning its keep *right now*, not on a schedule. `sampo retire <capability> --dry-run` should show what breaks if it disappeared today, from the ledger, not a model.
  Done when: `sampo retire <verb> --dry-run` prints the tasks, gates and user asks that would be affected, computed from the last 30 days of ledger data.

- **wild — A "what I left out" line on every morning card, not just every Mission** — FEATURE — 4 — S — risk low — category: trust
  Why: "Print 'the one thing I'd ask you if I could' at session close" and "Left out" receipts exist per-Mission. The unspoken need: the morning card is the *daily* trust surface, and it should carry the same honesty as the Mission close — "here's what I didn't do and why I didn't."
  Done when: every morning card ends with a "Left out:" line (or "Left out: nothing, here's the receipt"), and the line is computed from the overnight ledger, not a model.

- **wild — A "silence is not consent" lamp that glows when the user has gone quiet, and dims when Sampo decides to be quieter** — FEATURE — 2 — M — risk med — category: trust
  Why: "A 'silence is not consent' lamp that glows when you've gone quiet" exists. The unspoken need: the lamp should *dim* when Sampo makes the reversible decision to reduce its own output in response to silence, so the user can see Sampo is *responding* to the quiet, not ignoring it.
  Done when: the lamp has two states (glowing = user quiet, Sampo active; dim = user quiet, Sampo quieted) and the transition is logged with a reason.

- **Answer earlier question: what single moment feels most like craft — the block, the close, or the abstain?** — CLEAN — 1 — S — risk low — category: trust
  Why: The user's own words ("never interrupt mid-run", "keep working the rest of the queue") point to the *abstain* as the craft moment: the hardest thing is knowing when *not* to act. The block is mechanical; the close is visible; the abstain is invisible and trusted.
  Done when: the status line's grammar treats "chose not to act" as a first-class state, distinct from "stalled" or "done."

Next question: Does the user ever *want* Sampo to be wrong on purpose (to test a hypothesis) and have no surface for it — or is "never act without evidence" absolute?
Next question: Which of the user's own hand-edits to Sampo-written prose are *taste* (style, word choice) vs *correction* (fact, logic), and does Sampo treat them differently?
