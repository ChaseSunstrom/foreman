# Brainstorm — lens: user value

- **Diff the capability surface of every change** — FEATURE — value 5 — effort M — risk low — category: security
  Why: assumption: tests prove behaviour, not what new power the change grants. Nothing in the pack lists new network calls, subprocesses, file writes outside the repo, env reads or deps as a checked surface.
  Done when: a fixture change that adds one `subprocess` call and one outbound `requests.get` makes `fm prove caps` print both lines as "new capability, unreviewed".

- **Audit narrated actions against real tool calls** — FEATURE — value 5 — effort M — risk med — category: agents
  Why: the project premise is "commands it really ran", but a finish message can still say "I ran the migration" with no such call in the transcript. Assumption: the transcript is parseable on all harnesses.
  Done when: a recorded session whose final message says "ran the tests" with no test command makes `fm check` flag that sentence as "narrated, never executed".

- **Explain every red proof by its last-green delta** — FEATURE — value 5 — effort M — risk low — category: developer experience
  Why: assumption: a red proof today names what failed but not what changed since it was last green. The delta is commits, dependency versions, env fingerprint and files, ranked, with an optional bisect to the first bad commit.
  Done when: a planted regression three commits back is named by commit in the red output, in under 60 seconds on the fixture repo.

- **Re-check premises at lane handoff** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: parallel lanes merge in mission order, and a downstream lane builds on upstream "done" claims. Assumption: nothing re-runs an upstream proof before the next lane relies on it.
  Done when: a lane whose upstream proof was broken by an earlier merge stops with "premise T-x no longer holds" instead of building on it.

- **Verify the user's LLM features, not only the user's code** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: assumption: many users' projects call a model. "Does it do what the user meant" for those has no prover. The kit is a pinned prompt-regression set, an injection-payload corpus, and an N-run variance report that labels non-deterministic answers "unproven", not "passed".
  Done when: a fixture app with a deliberately injectable prompt fails the injection corpus, and the same app passes after the fix.

- **Report whether each vulnerable dependency is reachable** — FEATURE — value 4 — effort M — risk med — category: security
  Why: assumption: an advisory scan gives noise the user ignores. A call-graph check for the vulnerable symbol turns it into reachable, unreachable or unknown, and unknown is labelled unproven.
  Done when: on a fixture with one advisory whose symbol is called and one whose symbol isn't, the output differs between the two.

- **Scan built artifacts, not just source** — FEATURE — value 4 — effort S — risk low — category: security
  Why: the pack covers scrubbing ledgers and screenshots but not wheels, bundles, source maps, docker layers or the built `site/` output. Those are where secrets and absolute home paths leak.
  Done when: a fixture build that embeds a planted token in a source map fails `fm prove artifact`, naming the file inside the artifact.

- **Promote passing flows to a post-ship production canary** — FEATURE — value 4 — effort M — risk med — category: ops
  Why: `fm flow` proves the thing once, before ship. Assumption: the user learns of the next regression from a customer. The canary replays the flows read-only on a timer and writes the first red to the morning note.
  Done when: breaking the fixture server after the canary is armed produces a red entry within one interval, with the flow's name.

- **Run watch mode for proofs** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: assumption: proofs run at finish, so feedback comes late. `fm prove --watch` re-runs only the proofs whose covered files hashed differently and prints a single status line.
  Done when: editing one file re-runs exactly the proofs that cover it, and an unrelated edit re-runs none.

- **Prune proofs and provers by unique catch** — CLEAN — value 3 — effort M — risk med — category: simplicity
  Why: Foreman adds many provers and almost nothing is removed. Assumption: some provers never fail where another doesn't also fail. Plant faults, record which prover alone catches each, and list the ones that catch nothing unique for deletion.
  Done when: a report names at least one prover with zero unique catches over the planted set, or states that none exist.

- **Render a proof table in the PR description** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: reviewers don't have Foreman. One row per claim carries the proof kind, a verdict from the fixed vocabulary, and the single command to re-run it.
  Done when: `fm ship --pr-body` outputs a markdown table where every row's command runs standalone in a fresh clone.

- **Wild: stream a live claim ledger beside the agent's work** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: wild. Claims are extracted from the agent's messages as it writes them and flip from "claimed" to "proven" or "unproven" as provers return. The user watches the gap close, or doesn't, before the finish.
  Done when: in the web UI, a sentence like "all endpoints validated" appears within 5 seconds of being written, with a status that changes when a prover reports.

- **Wild: calibrate the human verifier** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: wild. Assumption: a human "looks fine" is Foreman's weakest proof and is never graded. Occasionally slip a planted-bad item into the user's hand-check queue and measure their false-accept rate. That rate then sets how much hand proof Foreman trusts.
  Done when: after 10 queued hand-checks including 2 planted faults, `fm doctor` shows the user's catch rate and the trust weight derived from it.

- **Wild: build a synthetic data twin from production statistics** — FEATURE — value 4 — effort L — risk high — category: data privacy
  Why: wild. Data proofs on a copy of real rows are risky for private users. Generate a staging set from the schema's statistics, with no real rows, and run migrations and invariants on it.
  Done when: a migration is verified on a generated set whose per-column distributions match within a stated tolerance, and a scan finds zero real values from the source.

- **Mine the repo's own proof idiom** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: assumption: each FIX commit in the repo already shows how this team proves a fix (test shape, fixture style, assertion habit). Propose the same shape for the next fix instead of a generic one.
  Done when: for a fixture repo with three prior fix commits using one fixture helper, the suggested proof for a new fix uses that helper.

Next question: Which of Foreman's own "proven" verdicts has the user ever overruled by hand, and what did the prover not see in those cases?
Next question: What does a user without Foreman see when a reviewer or CI re-runs the claim, and which proof kinds cannot be re-run outside the original machine?
