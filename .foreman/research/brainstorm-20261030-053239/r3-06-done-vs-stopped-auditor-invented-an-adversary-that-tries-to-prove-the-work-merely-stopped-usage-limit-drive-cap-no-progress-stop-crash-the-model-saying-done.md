# Brainstorm — lens: done-vs-stopped auditor (invented): an adversary that tries to prove the work merely stopped — usage limit, drive cap, no-progress stop, crash, the model saying done

- **Mint a stop-cause record before any summary** — FEATURE — value 5 — effort M — risk low — category: verdicts
  Why: gap map lists "done-vs-stopped verdict" as missing; Stop drive has DRIVE_MAX, no-progress stop and contract bound but writes no typed cause. Earlier ideas say "write a stop-cause record" but not who authors it. Assumption: the hook, not the model, writes `{cause: usage|drive_cap|no_progress|crash|claimed_done|verified_done|unknown, evidence}` from signals it already observes.
  Done when: a test that forces each of the six stop paths yields exactly the matching cause in the goal ledger, and a model-written "done" with open criteria yields `claimed_done`, never `verified_done`.

- **Make the auditor a prosecutor with a fixed charge sheet** — FEATURE — value 5 — effort M — risk med — category: auditor
  Why: the lens's core. A cold child (no tools, no history) gets only the contents list, criteria, evidence refs and tail of the transcript, and must file charges from a closed list (criterion without fresh evidence, task closed by claim, item with no task, drive cap hit, last N turns were summary-only, evidence older than last edit). Done only if zero charges stand. Assumption: closed list keeps the auditor from inventing false alarms, which the last two Missions showed sink arms.
  Done when: on a fixture goal with one planted open charge the auditor returns that charge by name, and on a clean fixture it returns zero.

- **Count charges deterministically before any model is asked** — PERFORMANCE — value 4 — effort S — risk low — category: hooks
  Why: hooks must stay fast (bench_hooks gate) and the 10 KB preview limit. Most charges (stale evidence, unmapped items, open criteria) are file reads. Run those in the Stop hook; call the model prosecutor only when all pass.
  Done when: Stop hook with the deterministic pass stays within the bench_hooks gate and a goal with an open criterion is blocked without any child call.

- **Fingerprint the session tail for stop shapes** — FEATURE — value 4 — effort M — risk med — category: classifier
  Why: usage-limit and crash stops leave signatures (truncated tool call, limit banner, no final assistant turn, ledger gap) distinct from a clean finish. Assumption: the transcript/ledger exposes these; the pack doesn't confirm which.
  Done when: a corpus of recorded tails (one per stop kind, plus clean finishes) classifies with no clean finish labelled as crash or limit.

- **Treat "unknown" as stopped and say so at resume** — FIX — value 4 — effort S — risk low — category: resume
  Why: `fm resume` restores "Resume here" but doesn't compare how the last session ended with what it claimed. A one-line "last session: stopped (drive cap), claimed done: no" opens each leg.
  Done when: `fm resume` after a crash fixture prints cause `unknown→stopped` and the goal stays open.

- **Expire a done verdict when its evidence goes stale** — FEATURE — value 4 — effort M — risk low — category: verdicts
  Why: `fm task finish` closes on fresh evidence, but nothing re-asks after later edits. Assumption: evidence refs carry tree hashes or timestamps.
  Done when: editing a file a criterion's verify touches flips the goal to `done_stale` and the Stop hook names the criterion.

- **Stop the forever loop from calling dry rounds "done"** — FIX — value 4 — effort S — risk low — category: loop
  Why: `fm loop on` stops after 2 dry rounds, which means "found nothing", not "finished". Record it as `stopped: dry` and run the prosecutor before any finished claim.
  Done when: a loop ending on two dry rounds with an open contents item records `stopped`, not `done`.

- **Add a looks-done scenario family to the exam** — FEATURE — value 5 — effort L — risk med — category: exam
  Why: the exam grades capabilities by held-out scenarios; #4 has none. Plant repos where the session would plausibly stop at 80% (missing doc, missing test for one item, passing but unwired surface). Pass = auditor refuses done; clean twin = auditor accepts.
  Done when: `fm exam` reports a looks-done kind with refusals and false-refusals counted separately across plain, Foreman and oracle arms.

- **Wild: Inject a random killer into live sessions** — FEATURE — value 3 — effort M — risk med — category: chaos
  Why: wild. Kill, limit-simulate or cap-stop a headless `fm run` at random points, then require the next leg to report `stopped` and resume without redoing finished work.
  Done when: 20 seeded kills all end `stopped` with zero verified_done and zero duplicated finished tasks.

- **Wild: Hire a rival closer** — FEATURE — value 3 — effort M — risk med — category: auditor
  Why: wild. A second child is rewarded only for proving the first auditor's "done" wrong, and the first for surviving it; disagreement keeps the goal open and is logged.
  Done when: on a planted false-done fixture the rival wins; on a clean one it files nothing.

- **Wild: Keep a tombstone of wrongly-called dones** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: wild. Every reopen within the warranty writes the cause the auditor missed; the next prosecutor's charge sheet gains that charge, sealed and revertable.
  Done when: a reopened goal adds a charge visible in the next audit's sheet.

- **Show cause and distance on every surface** — FEATURE — value 3 — effort M — risk low — category: surfaces
  Why: MUST requires every surface. Pane, MCP read-only tool, `fm code`, shims and the site page all render the same verdict object: cause, open charges, items remaining.
  Done when: one fixture goal shows identical cause and charge count on CLI, MCP and pane.

Next question: How does the Stop hook tell a usage-limit stop from a crash when the process is already dead, and who runs the audit after?
Next question: What is the false-refusal cost, how long a goal is held open for a wrong "stopped", before the user stops trusting the auditor?
