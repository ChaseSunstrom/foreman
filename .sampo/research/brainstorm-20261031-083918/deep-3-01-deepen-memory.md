# Brainstorm — lens: deepen: memory

**Answers to the earlier questions my lens can reach**
- **Baton, ledger and repo disagree after a kill:** the repo should win for what exists, the ledger for what was decided, and the baton last. Assumption: no rule exists today. The user should see a one-line "ledger says X, repo shows Y" instead of a silent pick.
- **Resume reading:** a content hash of the baton, ledger and tree makes "nothing changed, continue T-NNNN" cheap to prove. A digest is only needed when the hash differs.

**Ideas**

- **Build one verdict ledger for every tool no** — FEATURE — value 5 — effort M — risk low — category: memory
  Why: T-2270's capability-miss trigger and `fm plugins find` / `fm lib search` have no record of past retirements, refused grants or dropped finds, so the same tool can be re-found and re-queued. The existing ideas (graveyard, retire reasons, refuse reasons, "record every no") are one store.
  Done when: after refusing a grant with a reason, the same capability miss prints "refused <date>: <reason>" and queues nothing.

- **Require a reason and a re-open condition on every no** — FEATURE — value 4 — effort S — risk low — category: memory
  Why: the steer "no idea is killed for ambition" means a no must go to not-yet.md with its blocker. A verdict needs a reason and a checkable condition, such as "needs libappindicator" or "license GPL", as T-0325 already shows.
  Done when: `fm tools retire X` without a reason and condition exits non-zero, and a test covers it.

- **Block reinstall after two retirements, with an automatic reopen** — SECURITY — value 4 — effort S — risk low — category: guardrail
  Why: a hard block would break the "retry what a new capability may unblock" Seed rule. The block should lift when the tool's version or the re-open condition changes.
  Done when: a third install request for a twice-retired tool is refused with the reasons. After the condition flips, it is allowed once.

- **Check re-open conditions at every Seed** — FEATURE — value 4 — effort M — risk med — category: memory
  Why: the Seed row already retries blocked items. Conditions are free to test (binary on PATH, version, grant state), so the ledger can announce "unblocked: X" once, with no tokens spent.
  Done when: installing a missing binary makes the next `fm genesis` Seed list the matching tool as unblocked.

- **Cache the solution to each capability miss** — FEATURE — value 5 — effort M — risk med — category: memory
  Why: assumption: misses repeat across sessions (the trigger already counts "missing in 2+ sessions"). Store signature → what worked (plugin, MCP server, script) in the library. The second miss then skips the search.
  Done when: a repeat miss resolves from the cache with zero `fm plugins find` calls and says where the answer came from.

- **Give every built tool a provenance manifest and flag self-judged ones** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: `fm new tool` writes a tool and its failing-first test, but a model wrote both. That is the "model on both sides with no user-owned check" question. The manifest records the miss, the test, the run output and whether any non-model check exists.
  Done when: `fm doctor` lists built tools with no user-owned check, and a fixture with a model-only test is flagged.

- **Let steers supersede ledger entries and cite them** — FIX — value 3 — effort S — risk low — category: consistency
  Why: earlier intake answers were later contradicted by steers. A ledger "no" that a newer steer overrides should show as superseded, not as live truth.
  Done when: setting a steer that names a tool marks its verdict "superseded by steer <date>" in `fm tools history`.

- **Have a different model re-read each verdict's reason against its evidence** — SECURITY — value 3 — effort S — risk low — category: trust
  Why: the standing rule requires a cold Haiku read of tower files. Verdict reasons the writer could have invented fall in the same class.
  Done when: a verdict whose reason cites a failure the logs don't show is marked "unverified" by the cold read.

- **Propose retirement of tools that go unused** — CLEAN — value 3 — effort M — risk low — category: lean
  Why: the Lean ratchet warns when the always-on footprint grows, but nothing names which built tools never fire. Use usage counts since the build to propose, never self-retire.
  Done when: a tool with zero calls in N sessions appears in a retire proposal with its call count.

- **Rank the grant queue from past approvals without ever deciding** — FEATURE — value 3 — effort M — risk med — category: grants
  Why: grants stay the user's. Ledger history can sort, batch and pre-explain requests ("you refused two like this") but must not approve.
  Done when: a test shows the queue sorted by similarity to past approvals, and no code path grants without a user command.

- **Compost a retired tool into a lesson and a replay test** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: the miss that caused the build becomes a regression scenario, and the retirement reason becomes a lesson with confidence (T-0217). A later session can then show the same miss is still solvable without the tool.
  Done when: retiring a tool writes a lesson and a replay test that fails if the miss is no longer handled.

- **Rebuild old misses on a schedule to see if they are solvable now** — FEATURE — value 4 — effort M — risk med — category: memory — wild
  Why: assumption: ecosystem tools change faster than ledgers. Each no gets a time-capsule retry in a throwaway lane, using only free arms. A pass turns "no" into "now possible" for the user to decide.
  Done when: a stored no whose scenario now passes is surfaced once as "retry candidate", with the run log.

- **Have a retiring tool write a will naming its heir** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: a retirement record names the replacement tool, what carried over (tests, config) and what was lost. This turns the graveyard into a lineage, not just a list.
  Done when: `fm tools show X` on a retired tool prints its heir and the test it left behind.

- **Share verdicts across projects, opt-in and local-first** — FEATURE — value 3 — effort L — risk med — category: privacy — wild
  Why: assumption: the same tool is refused in many repos. A signed export of verdicts (tool, reason class, no paths) lets a second project start with "refused elsewhere". Nothing leaves the machine unless a setting is turned on.
  Done when: with the setting off, a network-denied run produces no calls. With it on, an exported verdict appears in a second repo's `fm plugins find` output.

- **Publish the graveyard as a Genesis page** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: the site already publishes Genesis data daily. Epitaphs ("retired: duplicated fm map") show the project's judgement.
  Done when: `site/genesis` renders retired tools with reasons after `fm genesis publish`.

Next question: Which no in the ledger is most often overturned by the user later, and would that class of reason have been predictable?
Next question: When two ledger verdicts conflict for the same capability, such as one project refused it and another approved it, which should a new project inherit?
