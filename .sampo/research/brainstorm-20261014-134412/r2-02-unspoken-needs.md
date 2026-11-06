# Brainstorm — lens: unspoken needs

Note: the pile is saturated and most angles already have an entry. These are narrow second-order or combined ideas, and I say where one sits close to an existing entry.

- **Flag regexes that never match real data** — FIX — value 4 — effort S — risk low — category: metrics
  Why: the track-record and give-up readers matched `exit N` against stored `✗ exit N`. A pattern that hits nothing on live rows looks identical to "nothing failed". "Reader round-trip tests" cover known readers. This covers every regex in `lib/` automatically.
  Done when: `fm doctor` lists each regex in the metrics/readers modules with zero matches over the last 30 days of real state, and the test replays the `✗ exit N` incident to show it would have been flagged.

- **Add `Measure:` and `Nearest existing:` lines to every brainstorm idea** — FEATURE — value 4 — effort S — risk low — category: brainstorm
  Why: round 2 had only 3 of 437 ideas survive grounding, and the user's drops are almost all "premise measured, doesn't hold" (Read hook saves ~2 min/month, delta reads add a hook process per Read). Making each child emit the one-line falsifying measurement and the closest already-shipped item turns grounding into a mechanical pass. This is a format change, not a new pass.
  Done when: a child output missing either line is rejected by the parser, and `fm ideas` shows both fields per idea.

- **Declare release targets once and close only when each one probes as landed** — FEATURE — value 4 — effort M — risk med — category: release
  Why: the user asked to release 1.2.27 "to GitHub main and JARVIS". Assumption: JARVIS is a second deploy target. The landing ladder exists, but nothing stores the per-target "is it live?" probe.
  Done when: a `targets` list holds a probe command per target, `fm release` fails when one probe disagrees about the version, and the failure names the target.

- **Redact the context pack before it goes to a child** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the pack carries paths, emails and usernames, and `claude -p` children send it to a cloud service. `fm page` already redacts, but the pack builder doesn't share that path.
  Done when: a seeded email, home path and token in the pack never appear in the child's stdin, and the pack header says how many were masked.

- **Make `fm doctor` name the first unreceipted claim from the last round** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: round 1 listed "mail monitor arming unverified" and "compact output not on" as prose, and the user later had to find real metric bugs themselves. This replaces prose gaps with a probe output of "claimed, not yet evidenced" items.
  Done when: each "known gap" line from a round close maps to a probe, and `fm doctor` prints the first unresolved one with its fix.

- **Rank unticked shipped items by what the user did next** — FEATURE — value 3 — effort M — risk med — category: feedback
  Why: nobody has ticked the board, so there is no signal. Assumption: transcripts show whether the user kept using, bypassed or complained about each shipped behaviour. This is close to "auto-tick the board".
  Done when: after a round, each shipped item gets keep/neutral/suspect from the next 50 transcript turns, and the evidence line cites a turn.

- **Give each deferred cluster a recurrence meter fed by captures** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: deferred clusters (supply chain, crash recovery, fleet) were deferred because there was "no incident". Intake can count new captures that match a cluster's keywords. Overlaps "reactivation trigger", but the mechanism here is intake-only and costs no model call.
  Done when: capturing a message that matches a deferred cluster increments its counter, and the queue view shows clusters at 3 or more hits.

- **Wild: Run a "blind rebuild" check on one metric per round** — FEATURE — value 3 — effort M — risk low — category: verification — wild
  Why: assumption: an independent implementation catches reader bugs that same-author tests share. A child gets only the stored data and the metric's name, with no code. It recomputes the number, and any gap is filed as a task.
  Done when: for the track record metric, a child's recomputation disagrees with the code on a seeded bug and the disagreement becomes a captured task.

- **Wild: Offer an "etc. mode" that spends a fixed budget on the user's plain-word mandate and stops itself** — FEATURE — value 4 — effort M — risk med — category: autonomy — wild
  Why: "etc. etc. etc." and "recursively improve" show a wish for unattended rounds. Assumption: a hard dollar and round cap, plus a morning summary, makes it safe.
  Done when: one command runs rounds until the cap, writes a single receipt, and halts when two rounds in a row yield fewer than 3 grounded ideas.

- **Wild: Feed children the user's last 20 pushbacks in place of the idea pile** — FEATURE — value 4 — effort S — risk med — category: ideation — wild
  Why: the pile is thousands of lines and it re-proposes things anyway, while the pushbacks carry the actual taste: measure first, don't duplicate built-ins. Compare yield per dollar against the pile-based pack.
  Done when: a paired run on the same lens shows grounded-idea counts for both packs, and the pack is under 5k tokens.

- **Wild: A "disbelief" trigger** — FIX — value 3 — effort S — risk low — category: trust — wild
  Why: the user's opening asks included "said the full suite never failed". Phrases like "never failed" or "that can't be right" could automatically open an audit task on the metric they doubted, quoting their sentence.
  Done when: a message containing a doubt phrase plus a known metric name creates a task titled with the metric and linking the quote.
