# Brainstorm — lens: unspoken needs

- **Flag reflex approvals** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the frontier reports 15+ approval prompts in one session, and the user keeps asking for gauges checked against ground truth. Habituation is the unspoken need: after enough prompts the user stops reading them. Record time-to-approve and prompt shape; a string of sub-second approvals of the same shape counts as reflex.
  Done when: a replay with 10 identical prompts approved in under 1s, then one destructive prompt, shows that prompt in full detail with "last 10 were reflex".
  Prior art: none found (rivals reduce prompts, none watch the user's attention). Better by: guards the human side of the loop. Novelty: 4.

- **Check lessons for prion support** — SECURITY — value 4 — effort M — risk low — category: learners
  Why: the open question is which learner was never fed poison. A lesson that is recalled, shapes a transcript, and is then re-learned from that transcript supports itself. Flag any lesson whose supporting events all post-date its first recall.
  Done when: a fixture lesson supported only by sessions that recalled it is flagged circular and excluded from recall; an independent one is not.
  Prior art: none found. Better by: catches self-amplified errors that provenance tags miss. Novelty: 4.

- **Watch for serum sickness after self-started changes** — FEATURE — value 4 — effort M — risk low — category: unattended
  Why: night work and auto-fixes land with no user present. The harm shows up days later as reverts, red CI or reopens on the same files. Keep a watch window per Foreman-originated change and charge late harm to the risk budget with attribution.
  Done when: a night-merged change reverted on day 3 lowers that trigger's autonomy and the digest names the commit.
  Prior art: revert-watch only for single triggers. Better by: covers every Foreman-originated change over a delayed window. Novelty: 3.

- **Let learned detectors tag but never act** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: learned and replayed rules sit beside the fixed guard. Following antibody-dependent killing, adaptive learners only write tags, and one small fixed effector turns tags into prompts or blocks under thresholds the learners cannot edit. A poisoned learner can then raise noise but never open a door.
  Done when: a test that injects a "allow everything" tag from a learner changes no verdict.
  Prior art: none found in harnesses. Better by: removes the learner-to-authority path. Novelty: 4.

- **Tighten the guard by observed presence** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: steers assume a live session, yet triggers run unattended. Presence is read from recent prompts or hook events; with no human for N minutes the guard moves to the strict profile and unattended asks take their safe default.
  Done when: the same command is allowed with a recent prompt and held after 30 idle minutes, and the card names the reason.
  Prior art: none found. Better by: setpoint follows who can intervene. Novelty: 3.

- **Route failures by novelty distance** — FEATURE — value 3 — effort M — risk med — category: memory
  Why: known failures should take the one-step memory path, and unfamiliar ones should go to a blind "naive" reviewer. Embed failure signatures by cheap features; near past cases replay the old fix, far ones route cold.
  Done when: a repeat signature takes the fast path in a replay, and a never-seen one is sent to the cold reader.
  Prior art: bug triage by dedupe only. Better by: also drives review depth. Novelty: 3.

- **Fit a dose-response curve per nudge** — FEATURE — value 3 — effort M — risk low — category: attention
  Why: earlier ideas cap flags at a fixed number. Measure act-versus-ignore against how often a signature fires, then emit at the peak of the curve rather than at a guessed cap.
  Done when: a noisy signature's emission rate falls to the fitted peak and the acted-on rate does not drop.
  Prior art: fixed mute-after-two. Better by: learned per signature. Novelty: 3.

- **Detect the user's avoidance of a region** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: assumption: after repeated blocks or nudges in one area, the user quietly stops working there. Compare edit density per path before and after block clusters and surface it as "you've stopped touching X since Y".
  Done when: a fixture with 5 blocks in a path followed by 30 days without edits yields one avoidance line.
  Prior art: none found. Better by: surfaces silent harm that nobody reports. Novelty: 4.

- **Ship day-one checks that retire themselves** — CLEAN — value 3 — effort M — risk low — category: lean
  Why: the history-trained detectors need data a new repo lacks. Born-with, broad checks cover day one, and each retires once a learned rule matches it on the replay corpus, which fits subtract-by-evidence.
  Done when: a retired check shows its covering learned rule and the lean count drops.
  Prior art: static defaults. Better by: scaffolding that removes itself. Novelty: 3.

- **Attach an exposure record to every merge** — FEATURE — value 3 — effort S — risk low — category: proof
  Why: the user wants claims proven. Per merge, record which defences saw the change (guard events, cold read, flake reruns) and which could not.
  Done when: `fm ship` writes a git note listing seen and unseen defences.
  Prior art: CI badges. Better by: includes blind spots. Novelty: 2.

- **Wild: Run a prion drill** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild. Plant a false lesson that only self-reinforces and score whether the circularity check catches it before the exam arm degrades.
  Done when: the planted lesson is flagged within 5 sessions.
  Prior art: none. Better by: tests the new check. Novelty: 5.

- **Wild: Hold a parabiosis day** — FEATURE — value 2 — effort M — risk med — category: cross-project
  Why: wild. Two of the user's repos share lessons for 24 hours; a diff report shows what transferred, what each repo rejected, and which lessons were repo-specific.
  Done when: the report lists accepted and rejected transfers.
  Prior art: none. Better by: measures lesson portability. Novelty: 5.

- **Wild: Draw blood for other harnesses** — FEATURE — value 3 — effort S — risk low — category: portability
  Why: wild. The frontier names cross-tool memory drift as a pain. `fm draw` writes one plain page of the user's hard nevers, overrides and allergies that Codex or Cursor rules can paste.
  Done when: the page contains no secrets and round-trips into an AGENTS.md block.
  Prior art: hand-copied rules files. Better by: generated from observed behaviour. Novelty: 4.

Next question: which Foreman outputs does the user act on versus merely approve, measured by time-to-response?
Next question: which learner's inputs include text produced under that learner's own influence?
