# Brainstorm — lens: grid

Cells covered: CLI, pane, Smith TUI and web UI as surfaces; user, agent, other lanes and unattended run as actors; missing, wrong, slow, unsafe and unclear as failure modes. Left empty: web UI × other lanes × slow (lane state is read from files, not rendered live) and TUI × unattended × unclear (nobody is watching, so the morning card covers it).

- **Predict the follow-up to the user's own hand commit** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Cell: CLI × user × missing.
  Why: assumption: most hand edits by the user are followed by a test, a CHANGELOG line or a ship ask. Sampo only learns from asks typed to it, not from commits the user made themselves.
  Done when: after a user-authored commit, `fm next` shows a drafted follow-up. A replay of the last 30 hand commits hits at least a stated rate against the ones that were followed up.

- **Resolve near-miss ids, paths and verbs in typed asks** — FIX — value 3 — effort S — risk low — category: intake
  Cell: CLI × user × wrong.
  Why: the pack shows the old Foreman and new Sampo spellings, stale `fm*.py` paths and renamed verbs in open items. Asks that cite them silently point at nothing.
  Done when: an ask naming `fmgenesis.py` or a dead task id is filed with the nearest live target and a one-line "I read X as Y".

- **Limit a speculative lane's writes to the draft's declared file set** — SECURITY — value 4 — effort M — risk med — category: lanes
  Cell: unattended × agent × unsafe.
  Why: overnight drafting with a 27B on the user's server means the weakest model gets the most unattended write access. Assumption: lanes currently write anywhere in their worktree.
  Done when: a planted draft that edits an undeclared file is blocked and logged, and the drive carries on with the next draft.

- **Pre-flight a predicted ask's grants before it is drafted** — FEATURE — value 3 — effort S — risk low — category: unattended
  Cell: unattended × other lanes × missing.
  Why: the "ship landed commits" ask needs a publish grant that is set on one task and spent on use. A draft that can't ship wastes the night.
  Done when: a predicted ask needing an unset grant is listed under "needs you" with the grant name, and no lane is spent on it.

- **Split the morning card into "done", "waiting on you" and "I'm unsure"** — FEATURE — value 4 — effort S — risk low — category: clarity
  Cell: web UI × user × unclear.
  Why: the user said "stop asking me for stuff" and wants progress by morning. A card that mixes the three costs them reading time.
  Done when: each card item carries exactly one of the three tags, and a cold child reading only the card can name what needs the user.

- **Time-box the local-model switch inside the predictor** — PERFORMANCE — value 3 — effort S — risk low — category: local models
  Cell: unattended × agent × slow.
  Why: a model switch on llama-swap costs about 3 minutes and can't be detected, because `/running` isn't relayed. A prediction pass that triggers a swap stalls the drive.
  Done when: the predictor uses only the resident model, or schedules a switch only in the night's batched window. A test shows no swap during the user's active hours.

- **Cross-check each draft against open and recently dropped tasks** — FIX — value 4 — effort M — risk low — category: duplicates
  Cell: other lanes × agent × wrong.
  Why: the user dropped several Foreman-filed items as "premise already met" or "absorbed by T-2893". Drafts built on a stale premise repeat that waste.
  Done when: a draft whose title is covered by a closed or absorbed task is suppressed, citing that task's id.

- **Keep the wildness score on the anticipation card** — FEATURE — value 3 — effort S — risk low — category: user model
  Cell: pane × user × wrong.
  Why: the user pushed back that "the moons aren't that wild". Assumption: the same class of miss (right topic, wrong intensity) will recur for other asks.
  Done when: a drafted brief for a moon-type ask shows its wildness 1–5 and is not shown below 4.

- **Wild: Make the user type their guess blind before the card shows** — FEATURE — value 3 — effort S — risk low — category: calibration
  Cell: CLI × user × unclear.
  Why: assumption: a hit rate counted from cards the user only skimmed is inflated. A blind guess in one line gives an honest comparison.
  Done when: `fm morning` takes an optional one-line guess, then shows the card, and the diff is logged as a hit or a miss.

- **Wild: Predict the user's next pushback on what was just built** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Cell: TUI × user × wrong.
  Why: recent pushbacks (not wild enough, wrong naming, asked too much) were all predictable from earlier steers. A local judge calibrated on those pushbacks reads a finished report before the user does.
  Done when: on a held-out set of past reports, the judge flags the ones that drew pushback, at a stated precision.

- **Wild: Keep a "would I have asked?" shelf of overnight work the user never wanted** — FEATURE — value 3 — effort M — risk low — category: waste
  Cell: web UI × unattended × unclear.
  Why: the user wants major progress by morning, but unattended output they discard is waste. Showing it, with its cause, teaches the predictor.
  Done when: discarded drafts show one reason each, and the next night's drafts exclude that class.

- **Stop and log when a draft loops** — FIX — value 3 — effort S — risk low — category: unattended
  Cell: unattended × other lanes × slow.
  Why: the drive kept re-pushing for each subagent shell, and counted agents that had already finished (T-2873, T-2901). Drafting lanes could repeat that churn.
  Done when: a draft that re-runs the same step three times is parked with its error fingerprint, and the night continues.

- **Tag every injected anticipation note with its surface** — CLEAN — value 2 — effort S — risk low — category: provenance
  Cell: agent × agent × unclear.
  Why: assumption: the same note reaches the agent through hooks, the pane and `fm next`. A tag lets the user see which surface it came from and whether it was read.
  Done when: each note carries a surface tag, and the doctor counts notes per surface.

Next question: which of the user's repeated asks (ship the landed commits, keep working the queue) are cheaper to automate than to predict?
Next question: when a prediction needs a grant only the user can give, should the draft wait, or ask once on the morning card?
