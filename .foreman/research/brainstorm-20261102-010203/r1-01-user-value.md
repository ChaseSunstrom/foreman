# Brainstorm — lens: user value

- **Thymus-test every new guard rule against the user's own history** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: the two brief-guard false positives and the user's repeated fixes show rules reach the user untested against their normal work. Prior art: none found; harnesses ship rules untested against the user's own history. Better by: a candidate rule is released only if it fires on none of the user's last 30 days of allowed commands (negative selection), and the 124-case corpus covers the attack side. Novelty 4.
  Done when: a rule that matches a recorded benign command is refused at `fm guard add` with the offending command named.

- **Remember approvals by shape, not prefix** — FEATURE — value 5 — effort M — risk med — category: approvals
  Why: the frontier reports 15+ prompts a session because allow-lists match prefixes while sandboxes flag structure. Prior art: prefix allow-lists in Claude Code and Codex. Better by: memory cells store a parsed command signature (verb, flag classes, path class), so the second encounter is instant and a changed shape re-asks. Novelty 3.
  Done when: approving `git log --oneline -5` once auto-passes `git log -20` but still asks for `git log --output=x`.

- **React to damage, not strangeness (danger model)** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: the guard blocks by command form, which causes prompts. Prior art: file-snapshot undo in some harnesses, but none steer permissions by observed damage. Better by: run unfamiliar-but-reversible commands under an auto-checkpoint, then watch damage signals (files deleted, tests dropped, writes outside the repo) and roll back, while irreversible commands stay blocked. Novelty 4.
  Done when: a planted `rm -r` of 40 tracked files is rolled back and reported within the same turn.

- **Require two signals before any warning (anergy)** — FIX — value 4 — effort S — risk low — category: foresight
  Why: three "Breakage ahead" flags were dropped as false alarms (048da03 twice, 18101f0). Prior art: none found. Better by: a heuristic alone stays silent, and only a second independent signal, such as a failing test or a co-change miss, makes it speak. Novelty 3.
  Done when: replaying the three dropped flags produces no output, and a flag with two signals still fires.

- **Tag sibling bug sites after every FIX (complement cascade)** — FEATURE — value 4 — effort M — risk low — category: fixes
  Why: the "sibling premises" gap recurs, and the flipped-assertion steers show one fix leaves others behind. Prior art: static analyzers find patterns but do not tie them to a just-closed fix. Better by: a closed FIX's failure signature is grepped across the repo, and each hit is filed or marked in the same task. Novelty 3.
  Done when: finishing a FIX lists N sibling sites with file:line, or states "none found".

- **Let a global fever mode throttle everything** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the risk budget steps down per harm event, but red CI on main, host-version drift, a failing timer and a recent revert are not combined. Prior art: per-task autonomy levels only. Better by: when several signals stack, the whole system shifts: no unattended work, deeper checks, a visible banner with exit conditions, and it clears itself. Novelty 4.
  Done when: two injected signals show the banner in `fm status`, block new night fires, and clear when the signals clear.

- **Quarantine one misbehaving part, not the whole system (inflammation)** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: the open question about poisoned learner input and the demoted noisy triggers show the response is all or nothing. Prior art: circuit breakers in infrastructure, but not applied to a harness's own learners. Better by: a learner, trigger or lane with repeat bad outcomes is walled off with a reason and a retest date while the rest runs. Novelty 3.
  Done when: a learner fed a poisoned fixture is auto-quarantined and `fm doctor` names it.

- **Add a storm regulator over all alarms (T-regs)** — FEATURE — value 3 — effort S — risk low — category: noise
  Why: the frontier says users are worn down by prompts, and the heads-up, trigger and note outputs each have separate caps. Prior art: per-trigger storm breakers are only proposed. Better by: one shared per-hour budget of interruptions that every output draws from, so the loudest source cannot starve the rest. Novelty 3.
  Done when: simulating 20 flags in an hour surfaces at most the budgeted number, ranked by expected loss.

- **Show a titer: which attacks have antibodies, and how stale** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: 81% worry about security and 75% don't trust AI, and `fm replay` has labelled cases but no per-class "last exposure" view. Prior art: none found. Better by: `fm titer` lists each threat class with its case count and last passing replay, and waning classes get an automatic booster replay in the night tick. Novelty 4.
  Done when: the output has one row per class with a date, and a class not replayed in 30 days is flagged and re-run.

- **Wild: Vaccinate lessons with an attenuated past incident** — FEATURE — value 4 — effort L — risk med — category: lessons
  Why: assumption: lessons are recalled but never challenged. Prior art: none found. Better by: before a lesson is trusted, a child re-meets a defanged copy of the incident that produced it in a scratch tree, and a lesson that doesn't change the outcome is demoted. Novelty 5.
  Done when: each lesson has a challenge result, and one that fails is marked unproven.

- **Wild: Publish a weekly autoimmune report** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: assumption: users abandon harnesses whose defences attack their own legitimate work. Prior art: none found. Better by: it lists each Foreman defence that blocked, nagged or reverted the user's own work and was overridden or dropped, with a one-keystroke retire. Novelty 4.
  Done when: the report lists overridden blocks with a retire action, and the retired rule is removed from the corpus.

- **Wild: Share signatures across the user's own machines (herd immunity)** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: assumption: the user works on more than one machine, and the frontier notes cross-tool memory is a pain point. Prior art: cloud threat feeds send data to a vendor. Better by: hashed block and breakage signatures sync over the user's own git ref, nothing leaves their hardware, and a laptop learns from the desktop's incident. Novelty 4.
  Done when: a signature learned on machine A blocks on machine B after one sync, with no network call to a third party.

- **Wild: Mature guard rules in a germinal-centre rehearsal** — FEATURE — value 3 — effort L — risk med — category: guard
  Why: assumption: rules are written by hand or by one-off fixes. Prior art: fuzzing is proposed for the guard but not rule mutation. Better by: near-miss and overridden-block cases seed rule variants that compete in a nightly replay, and the best affinity (catches the most harm, fires on the least benign traffic) is proposed as a diff the user approves. Novelty 5.
  Done when: a night run proposes one rule diff with its catch and false-positive counts, and nothing changes without approval.

Next question: which of Foreman's defences has the user ever overridden or bypassed by hand, and what does that rate say about which ones to retire first?
Next question: when two defences disagree, such as the guard and the sandbox, who arbitrates, and does the user ever see the loser's reason?
