# Brainstorm — lens: user value

- **Answer "what did I get for the time I spent?" with a weekly outcome ledger** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: The user keeps asking for 10x and "full management" yet no idea ties effort to outcomes they can feel. Existing ideas cover cost, digests and receipts separately; none joins requests → closed-and-kept results → minutes saved in one number per project.
  Done when: `fm code report --week` prints per project: requests made, runs landed and kept (not reverted within 7 days), and one headline line, from the run journal alone, in a test with a seeded history.

- **Hold the user's "etc." as a standing, bounded mandate** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: Repeated phrases "etc. etc.", "super recursive", "don't stop until complete, full auto", "I shouldn't even need to ask" show the real need is delegation of open-ended scope. Ideas exist for round budgets and contracts, but none turns the user's own wording into a persisted mandate with a stop line.
  Done when: Saying "keep improving fm code, etc." creates a mandate with a dollar/time cap and a stop rule; `fm mandate show` lists it, and a run halts and reports when the cap or two dry rounds are reached.

- **Name what Foreman won't repeat: a "you already told me" register at intake** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: The user had to restate permission to release ("stop asking me", "feel free to release") and "don't stop". Dropped/steered items show Foreman misreading steers. Standing grants exist as ideas, but a visible register that is echoed back at intake and consulted before every ask is missing.
  Done when: After "stop asking me if you can release", `fm release --push` runs with no prompt on the next three releases, and `fm grants` lists the phrase, its date and its scope.

- **Finish the job for the user: one-key land of a proved run** — FEATURE — value 5 — effort M — risk med — category: completion
  Why: The user repeatedly asks for releases and "fully implemented"; a proved run still leaves merge, push, release steps. Assumption: the user wants the end state, not the diff.
  Done when: Pressing one key on a proved run in the app merges it, optionally cuts the release if the grant exists, and shows the landed commit; a test covers the grant-absent path refusing with the exact `fm task set ID --allow publish` line.

- **Rank "what needs me" across all projects on the home screen** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: The home screen exists (T-1330) but lists counts; the user manages many projects and wants "full management". Planned "home ranked by need" is unbuilt.
  Done when: Home shows a top-5 list ordered by blocked-on-user, stalled, failing, then queued age, from existing task state; a fixture with 4 projects renders the expected order.

- **Show "it's alive" evidence in the first 10 seconds of any run** — FIX — value 5 — effort S — risk low — category: trust
  Why: The user's complaint "it just isn't doing anything" triggered the stall work (T-1336), but stall detection fires after 120 s. A first-signal contract makes the opening wait visibly explained.
  Done when: A run started against a fake runner that stays silent displays a named wait ("starting claude, loading plugins… 8s") within 2 s and a classified diagnosis by 10 s, in a pty test.

- **Turn the user's pasted rival-plugin/skill idea into a trial before adoption** — FEATURE — value 4 — effort M — risk med — category: integration
  Why: The request is to integrate the six Anthropic repos "automatically". Existing ideas cover pinning and scoring; the user-facing step of "try it on my next run only and tell me if it helped" is missing.
  Done when: `fm code --try skill:NAME` runs one task with the skill enabled and one without on a seeded fixture, and prints pass/cost deltas without leaving the skill installed.

- **Close each recursive round with a three-line "what changed for you"** — FEATURE — value 4 — effort S — risk low — category: communication
  Why: Rounds ship many items (1.2.43–1.2.48), yet the user's own messages reveal they judge by what they can do ("why can't I launch fm code like claude"). Release notes are internal-ticket-shaped.
  Done when: `fm release` writes a notes section of at most 3 plain sentences, each naming a command the user can now run, linted to contain no T-ids.

- **Wild: Say a sentence, Foreman picks project, runner and ceremony** — FEATURE — value 4 — effort L — risk med — category: routing
  Why: assumption: with many projects and 8+ runners, choosing is the remaining friction; "work with anything" implies no choosing. wild
  Done when: Typing "fix the flaky login test in the shop app" on home shows resolved chips (project, runner, quick/full) before Enter, correct for 8 of 10 seeded phrases.

- **Wild: Adopt a stalled live Claude Code session into fm code with one command** — FEATURE — value 4 — effort L — risk high — category: rescue
  Why: The user's core frustration was Claude Code vs fm code parity and silent stalls; a rescue path converts failures into continuations. wild
  Done when: `fm code take-over` reads the newest session transcript in the cwd, builds a plan from its unfinished work, and continues it as a new run, verified on a recorded transcript fixture.

- **Wild: A morning-after page the user can tick, and Foreman acts on the ticks** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: The user wants unattended "full auto"; ideas cover digests but not a response channel that turns ticks into queued/landed/reverted actions. wild
  Done when: After an overnight run, `fm code morning` opens a checklist; ticking "keep" lands the run, "undo" reverts it, "more like this" queues a follow-up, confirmed by state changes in a test.

- **Make "10x better" measurable: a user-owned scorecard of their own axes** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: "10x" is stated twice without a metric; benchmark ideas are for Foreman vs Claude generally, not the user's own repos and complaints. Assumption: the user wants proof on their work.
  Done when: `fm code score` replays the user's last 10 closed requests on the current build and reports first-try pass rate, time to first signal, and cost versus the stored baseline.

- **Offer a "what should I do next?" answer on bare `fm code`** — FEATURE — value 4 — effort M — risk low — category: guidance
  Why: The user expects `fm code` to behave like `claude`; an empty prompt is the moment of greatest uncertainty. Open work lists 50+ deferred briefs they never triage.
  Done when: Bare `fm code` shows three suggested requests drawn from blocked tasks, red gates and deferred briefs with fresh evidence, each runnable with Enter, in a fixture project.
