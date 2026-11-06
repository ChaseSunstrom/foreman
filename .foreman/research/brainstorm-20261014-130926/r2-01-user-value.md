# Brainstorm — lens: user value

- **Ask the user one question about round 1 at the end, with a default** — FEATURE — value 5 — effort S — risk low — category: feedback loop
  Why: the user's steer says "recursively improve" means review and re-brainstorm repeatedly, yet "nobody has ticked the board yet" and compact output waits on a yes. Round 2 has no input from the user on round 1. One end-of-round line, "Keep all 9 / revert X? default keep in 24h", lets rounds run unattended without blind drift.
  Done when: a finished round closes with one question that has a default and an expiry. An unanswered question resolves to the default and is logged.

- **Report round 1 in terms of what the user feels** — FEATURE — value 5 — effort S — risk low — category: close-out
  Why: the user's requests are phrased as "smarter, faster, better" but round 1's outputs are clusters and task ids. Show 3 lines: seconds saved per turn, asks avoided, failures caught, each from measured numbers (e.g. the ~1.04M tokens/30 days). Items that can't be measured say "unmeasured".
  Done when: `fm round report` prints at most 5 lines, each with a number and its source, and "unmeasured" where there is none.

- **Run compact output as a one-week shadow, then offer the yes with evidence** — FEATURE — value 5 — effort M — risk low — category: tokens
  Why: it is built and measured at ~1.04M tokens/30 days but off. The user said "etc. etc." about wanting more, so they would likely say yes if shown their own numbers. Shadow mode logs would-have-compacted outputs and whether the model later re-fetched them.
  Done when: with shadow on, no output changes, a log records bytes saved and re-fetch count, and `fm doctor` shows "enable? saves X, Y re-fetches".

- **Prove the mail monitor armed with a first-turn receipt** — FIX — value 4 — effort S — risk low — category: liveness
  Why: the pack says arming in a live interactive session is unverified, and the user's incident history is idle sessions. A silent failure here recreates that incident.
  Done when: a fresh session writes an "armed" heartbeat within N seconds, and `fm doctor` flags a session that has none.

- **Give every shipped round-1 feature a fire counter** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the board is unticked and some features (the push ask, session title, and the sensitive-repo outward refusal) have no usage evidence. Passive counters allow an auto-tick and a weekly "which features never fired" list, without asking the user.
  Done when: each feature increments a counter on firing, and `fm doctor` lists features with 0 fires after 7 days.

- **Make `fm page` accept ticks back through a pasted line** — FEATURE — value 4 — effort M — risk low — category: artifact
  Why: the page renders the board but is read-only. The user can paste a short code like `keep:1,3 drop:5` back into the session, which captures their taste with no new UI and no outbound channel. This respects the sensitive-repo egress refusal.
  Done when: pasting a tick string updates the board statuses and records dropped items as dropped, with a reason prompt optional.

- **Shorten and clean the idea pile before every brainstorm** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: this pack carries thousands of "ideas so far" lines, mostly duplicates, which costs tokens and causes repeats. Print cluster names with counts and the 20 most recent titles.
  Done when: the "ideas so far" section of a pack is under 3 KB, and a test shows a known duplicate is no longer proposed.

- **Add a doctor probe that replaces the "known gaps" prose** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: round 1 recorded its gaps as text, which nobody checks. Each gap (monitor armed, compact enabled, board ticked) becomes a one-line probe with the fix command.
  Done when: `fm doctor` prints each known gap as a pass or fail line and the prose list is deleted.

- **Salvage children that die on budget or turn limits** — FIX — value 3 — effort M — risk med — category: headless children
  Why: round 1 added hard `--max-budget-usd` caps. A child hitting the cap loses its partial output, which this brainstorm run itself would suffer. Keep partial text and mark it "partial".
  Done when: a child killed by the cap leaves a file with its output so far, and the caller reports "partial" rather than a failure.

- **Wild: Have the next round waiting at breakfast** — FEATURE — value 4 — effort L — risk med — category: unattended
  Why: the user wants repeated rounds ("recursively"). `fm night` could run a brainstorm, ground and queue pass within a budget, leaving a one-screen digest and the round-1-style default question.
  Done when: after an unattended night, the morning digest lists the new round's queued tasks and spend, and nothing risky shipped without a yes.

- **Wild: End every round by deleting the least-used feature from the last one** — CLEAN — value 3 — effort M — risk med — category: simplicity
  Why: the user's steers repeatedly drop things that duplicate built-ins (delta reads, Read-hook scoping), and "slim Foreman" is deferred. Fire counters make this decision data-driven, with a one-line veto window.
  Done when: each round close names one candidate for removal with its fire count, and removal needs no yes only if it fired 0 times.

- **Wild: Preview compact output on the user's own worst command** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: showing the user their largest Bash output, before and after, with the failure lines preserved, builds the trust that round 1 needs for the opt-in.
  Done when: `fm doctor --preview-compact` prints one real recent output's head, failure lines and tail next to its full size.

- **Wild: Auto-write a "by design" register from the user's drops** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: drops such as the heredoc guard, delta reads, and the Read hook were by design with measured reasons, yet brainstorms keep re-proposing similar ideas. A register that the brainstorm pack and intake consult would stop the repeats and show why.
  Done when: a dropped item with a reason is added to the register, and a later idea that matches it is filtered with a one-line citation.
