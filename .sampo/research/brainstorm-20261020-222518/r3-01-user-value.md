# Brainstorm — lens: user value

- **Finish the job for the user: land a proved run as a merged PR or local merge in one key** — FEATURE — value 5 — effort M — risk med — category: outcome
  Why: the pack's ideas stop at "closes with a commit" and "open a PR from a proved run" (one line). The user's real goal is work shipped, not a green receipt. Assumption: they still merge by hand today.
  Done when: `fm code --land` on a closed task in a scratch repo fast-forwards or opens a PR with the proof-built description, and refuses (with the reason) if any criterion is unproved.

- **Make the first request after install succeed or explain in under 60 seconds** — FIX — value 5 — effort M — risk low — category: first-run
  Why: the nixie run "just isn't doing anything" for minutes at 66k–133k tokens per call. A hard first-call time budget with a named fallback (leaner profile, other runner) removes the worst experience. The pack covers diagnosing silence, but not a budget that acts by itself.
  Done when: a fake runner that stays silent 20 s triggers a visible "switching to lean profile" within the budget and the request then completes; the test asserts both events.

- **Keep the user's own phrase-to-action vocabulary: learn "do the usual"** — FEATURE — value 4 — effort M — risk low — category: personalization
  Why: the user repeatedly types the same shapes ("release X and push", "keep going", "full auto"). Assumption: these repeat per project. Per-project saved standing orders (release permission, no-ask, full-auto) are applied without re-asking.
  Done when: after the user says "full permission to release" once, a later run in that project does not prompt for publish, and `fm code standing` lists and revokes it.

- **Show a weekly "what Foreman did for you" report across projects** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: the user can't see value beyond individual runs, and the benchmark/scorecard tasks are deferred for lack of cases. Local history already holds tasks closed, guard blocks, cost, and time. Assumption: that data is queryable from run logs.
  Done when: `fm code report --week` prints tasks proved, commands refused, spend per project and runner, and matches a seeded fixture's counts exactly.

- **Resolve a request that spans projects into linked tasks** — FEATURE — value 4 — effort L — risk med — category: multi-project
  Why: the user asked for "multiple projects"; ideas so far run one request in one project. Real changes ("rename the API, then update the client in nixie") cross repos.
  Done when: one request touching two fixture repos yields two tasks, the second blocked on the first's proof, and both close in order.

- **Make user complaints into standing regression checks automatically** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: "it just isn't doing anything" and "why can't I…" are already captured as friction, but nothing in the pack turns each into a test that stays. Assumption: friction phrases are reliably detected by the existing intake hook.
  Done when: replaying the nixie silent-run transcript through the intake creates a task whose verify command fails today and a fixture test that is then kept in the suite.

- **Offer "explain this repo to me" as the zero-risk first run** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: questions already get answers from files without a task. A first-run suggestion on a new project builds trust before any edit happens. Assumption: new users hesitate to let it edit.
  Done when: bare `fm code` in an unseen project offers that question first and answers it with file citations without creating a task.

- **Price every runner by real outcome: cost per proved task, per kind** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: `fm code bench` exists and routing by evidence is proposed, but the user-facing figure that matters is dollars and minutes per closed, proved task from their own history.
  Done when: `fm code runners` lists each runner's median cost and time per proved task by request kind from seeded history, and the router's pick matches the cheapest passing one.

- **Wild: Let the user text a request from their phone and get the receipt back** — FEATURE — value 4 — effort L — risk high — category: remote
  Why: assumption: the user runs unattended and wants to start or approve work away from the desk. Needs a self-hosted channel, off by default, with guard rules unchanged.
  Done when: a signed local-network message creates a queued task, and the receipt is delivered back; an unsigned message is refused and logged.

- **Wild: Run a "second opinion" from a different runner only when the first one's proof is thin** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: a model can pass weak checks. Triggering a cross-check only on low-strength criteria (no failing-first proof) spends tokens where doubt actually is.
  Done when: a task closed with a criterion that never failed first gets a reviewer-runner verdict attached; a strong-proof task does not.

- **Wild: Take over a project the user abandoned: "what was I doing here?"** — FEATURE — value 3 — effort M — risk low — category: resume
  Why: with many projects, the user returns after weeks. Rebuild the thread from git, open tasks, and the last runs into a three-line brief with a suggested next request.
  Done when: in a fixture repo idle 30 days with one blocked task, `fm code resume` names that task, its blocker, and the last commit.

- **Wild: Say "stop being annoying" and have Foreman trim its own prompts and notes** — FEATURE — value 3 — effort M — risk med — category: noise
  Why: the user has pushed back on being asked about releases and wants silence when things are fine. Map such phrases to a measured reduction in questions and notes, with the guard untouched.
  Done when: after the phrase, a replay of a standard session emits fewer user-facing prompts than before, and every guard verdict is identical.
