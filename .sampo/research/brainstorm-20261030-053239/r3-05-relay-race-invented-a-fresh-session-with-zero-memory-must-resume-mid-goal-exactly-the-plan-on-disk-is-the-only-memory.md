# Brainstorm — lens: relay race (invented): a fresh session with zero memory must resume mid-goal exactly; the plan on disk is the only memory

- **Adopt the orphaned edits a killed leg left behind** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: assumption: a SIGKILL or usage-limit stop usually lands mid-edit, leaving a dirty tree no note explains. The pack's intent log only covers the ledger, not the working tree.
  Done when: a test kills a leg after 2 of 3 planned file edits. `fm goal step` then lists each dirty hunk as "belongs to step N / unattributed" and offers adopt or stash, with no hunk lost.

- **Give every plan step a postcondition probe** — FEATURE — value 5 — effort M — risk low — category: idempotence
  Why: the pack says the plan on disk is the only memory, and "Re-prove done items" is only about done items. A step with a probe command ("grep -q X file", "test -f Y") lets resume check the world instead of trusting the notes, whatever state the kill left.
  Done when: resuming a goal whose step 2 was half done runs step 2's probe, reports "not satisfied", and resumes at step 2. A step whose probe is already green is skipped.

- **Prefer a seam-aligned fresh relaunch over compacting** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: PreCompact today checkpoints and carries on in the same bloated session. When the session sits at a step boundary and the baton is current, a fresh session may beat a summary.
  Done when: PreCompact at a seam with a verified baton ends the leg with a `relaunch` verdict. The next leg starts clean, and the choice and its reason are in the ledger.

- **Keep a known-good commands ledger per goal** — FEATURE — value 4 — effort S — risk low — category: memory
  Why: assumption: each new session re-discovers how to run one test, build, or start the app, which is the costliest thing to relearn. The dead-ends idea records only negatives.
  Done when: a command that exited 0 in a leg is stored with its cwd and duration. The next leg's resume packet lists it, and a stale entry is re-verified before it is shown.

- **Record a recipe for the ephemeral state a leg depended on** — FEATURE — value 4 — effort M — risk low — category: environment
  Why: dev servers, watchers, venvs, env vars and ports die with the session and live nowhere on disk. A resume that doesn't know "needs the server on :8080" fails in confusing ways.
  Done when: a goal that started a background process stores a restart recipe. The next leg's resume detects the process is gone and prints the exact command, or restarts it if a grant allows.

- **Measure the handoff tax of every leg** — PERFORMANCE — value 4 — effort S — risk low — category: metrics
  Why: nothing measures how much a resume costs. "Cap the resume packet" has no number to cap against.
  Done when: each leg records tokens and seconds before its first productive edit. `fm goal` shows the median tax, and a bench gate fails if a packet change raises it more than 20% on the fixture goals.

- **Route a resume to the right goal when several are open** — FIX — value 4 — effort M — risk med — category: routing
  Why: assumption: the baton ideas all assume one goal. Epics and parked goals will make "which goal is this session?" ambiguous, and the user may never be asked mid-run.
  Done when: with two open goals, a session's cwd, branch and first prompt pick one through `fm decide`. The choice and its reason are logged, and a test with a wrong-goal prompt resumes the right one.

- **Chain the baton into the ledger so tampering shows** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: the plan file is the only memory, and anything with write access (a tool result, a repo script, a sub-agent) can silently rewrite it. The ledger is already hash-chained but the baton isn't.
  Done when: each baton write appends its hash to the ledger. Editing the baton outside `fm` makes the next resume say "baton changed outside fm", quote the diff as data, and fall back to the last chained version.

- **Keep per-leg baton snapshots and `fm goal blame`** — FEATURE — value 3 — effort M — risk low — category: history
  Why: when a resume goes wrong you can't see which leg wrote the bad plan line or what the baton looked like then. This is the debugging half of the relay.
  Done when: `fm goal blame <line>` prints the leg, time and cause that wrote or last changed a plan line. `fm goal as-of <leg>` prints that leg's baton.

- **Carry the baton as a local git ref** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: assumption: a goal that lives only under `state/projects` can't follow a clone to another machine or a Desktop session. A ref `refs/fm/goal/<id>` travels with the repo but is never pushed without a grant.
  Done when: a fresh clone with the ref present resumes the goal. `git push` includes no fm ref unless an explicit grant exists, and a test checks both.

- **Wild: Rehearse the resume with the weakest runner** — FEATURE — value 4 — effort M — risk low — category: baton quality
  Why: wild. After a leg, a tool-less Haiku-class child gets only the resume packet and must name the next action. If the weakest model can continue, the baton is good. Failures become lint rules for baton text.
  Done when: the rehearsal's named action matches `fm goal step` on the fixture goals. A deliberately vague baton fails the check and the report names the ambiguous line.

- **Wild: Make the successor restate the plan before touching anything** — FEATURE — value 3 — effort S — risk low — category: verification
  Why: wild. The first action of a leg is a 5-line "where we are and what I do next". It is diffed against the baton's own summary, and a disagreement means the baton misled or the model misread. Either way it is caught before the first edit.
  Done when: a seeded misleading baton produces a flagged diff in the ledger before any edit. A matching restatement passes silently.

- **Wild: Animate the baton pass on the pane** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A short motion on resume shows leg N handing to leg N+1 with a three-line card: done, in flight, next. Reduced-motion users get a static card. The user sees the relay working, which builds trust in an unattended multi-day goal.
  Done when: the pane shows the card within a second of a SessionStart resume. A reduced-motion test shows the static version.

Next question: What does a resume owe the user who returns after three days, as opposed to the next session of the same day — a changelog of the gap, or silence?
Next question: Which parts of the baton are facts that go stale (branch, versions, test counts) and which are intent that doesn't, and does the format separate them?
