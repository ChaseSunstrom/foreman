# Brainstorm — lens: user value

Lens: user value. Ideas below go past the listed ones; each is aimed at something the user would notice in a week of use.

- **Show "model saved you X" receipts per session** — FEATURE — value 5 — effort S — risk low — category: user value
  Why: the pack shows many model slots (decide, intake, loop breaker, planner) but no way for the user to see what any of them earned. Without that, adoption looks like faith. Assumption: ledgers already log which slot answered.
  Done when: `sampo model receipt` prints, for the last 7 days, per slot: calls, abstains, overrides by the user, and the tasks where the model's answer was later reverted.

- **Pre-fill the brief's verify commands and criteria on `sampo task add`** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: 4,078 briefs hold criteria with verify commands and exit codes, so the pattern "request, stack, then the check that proved it" is learnable per stack. Writing criteria is the step users pay for most. Assumption: criteria text is clean enough to retrieve from.
  Done when: on 20 held-out briefs from a held-out project, the suggested verify command is accepted unchanged or with a one-token edit at least 50% of the time, shown on the bench card.

- **Warn at intake when a request resembles past reverted work** — FEATURE — value 4 — effort S — risk low — category: foresight
  Why: outcomes include reverted and "later fixes", and bge-m3 recall@1 is 0.85, so nearest-neighbour over reverted briefs needs no training. Distinct from predicting outcome: it names the specific earlier brief and what went wrong.
  Done when: creating a task close to a known reverted brief prints "like T-xxxx, reverted because …" with a link; false-warning rate is measured on held-out briefs.

- **Explain every model-made decision in one plain line** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: users steer constantly and push back, and a decision they can't read invites an override or a rule. Assumption: heads can return their nearest training neighbours as evidence.
  Done when: each `decide()` that used a model records "because: 3 similar closed briefs, all chose X" and `sampo why T-N` shows it.

- **Turn each repeated user correction into a one-line standing-rule candidate** — FEATURE — value 5 — effort M — risk med — category: learning
  Why: the steers list shows the user restating the same shapes (never block on me, keep working the queue, no installs). The model should notice the second restatement and propose the rule, not wait for the fifth. Assumption: the steer-expansion exam already exists as a base.
  Done when: replaying the ledger, a restated steer triggers a proposed rule at its second occurrence, and over the replay at least 60% of proposals match a rule the user later set.

- **Give a "time to finish" range on each queued task** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: there are ~40 open tasks and a drive that works the queue unattended. Closed briefs carry evidence timestamps, so size and duration are learnable per project. Assumption: timestamps are in the ledger.
  Done when: `sampo next` shows a range per task, and on held-out closed tasks the actual duration falls inside it about 80% of the time.

- **Offer a "no model" switch per project that really changes behaviour** — SECURITY — value 4 — effort S — risk low — category: control
  Why: sensitive projects and a user who vetoes software installs make it important that opting out be one flag, not a hunt. Assumption: slots are reachable through one config.
  Done when: with the flag on, a test shows no model call and no training row from that project, and `sampo doctor` reports it.

- **Wild: Morning digest written by the model, from the overnight ledger** — FEATURE — value 5 — effort M — risk low — category: delight
  Why: the user runs long unattended drives and is "away: no questions". What they need on return is what held, what didn't, and the three things only they can decide. Assumption: the ledger has enough structure to summarise.
  Done when: after an overnight drive, `sampo digest` prints at most 15 lines, and every claim in it links to a ledger line that backs it.

- **Wild: A "what would you ask me?" rehearsal before the user leaves** — FEATURE — value 4 — effort M — risk low — category: unspoken needs
  Why: the missed-asks list shows the user had to ask for the same classes of fixes (rename fallout, publish conflicts). Before an away window, the model predicts the likeliest blocking asks and gets them answered or pre-decided.
  Done when: on three replayed away windows, at least half of the asks the user actually had to make appear in the pre-departure list.

- **Wild: Hand a new project a "this is how you work" file the model wrote from your history** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the user wants it generic across projects, and 13 projects already carry the user's habits. Output is readable, editable text, not weights. Assumption: user-authored steers can be separated from repo text.
  Done when: on a fresh project, `sampo init` writes a draft of at most 20 lines, and the user accepts or edits instead of writing from scratch, as seen in the diff.

- **Show a per-project "model vs the user" agreement number** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the user wants a model only where it leads. One live agreement number per slot and project makes that visible and dull to check.
  Done when: `sampo status` prints agreement over the last 50 decisions per slot, from override and revert records.

- **Rank the open queue by what the user has actually picked first** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the queue holds 40+ deferred items with no guide to the user's real order, and the history shows which kinds the user pulls forward. Assumption: ledger records which task was started when.
  Done when: on a held-out period, the model's top 3 contains the user's next pick at least 60% of the time.

Next question: which asks does the user make at the moment of returning from an away window, and could a model have answered them before the user got back?

Next question: does the ledger distinguish a user's own words from text a tool pasted in, so that "learn the user's habits" never learns from injected or repo text?
