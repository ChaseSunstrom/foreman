# Brainstorm — lens: deepen: supply chain

- **Adoption ledger with provenance receipts** — FEATURE — value 5 — effort M — risk low — category: supply chain
  Why: the seed row has an "install-grant queue" and ideas already cover pinning and hashing; none records why a tool was adopted. Assumption: grants are currently bare yes/no cards.
  Done when: `fm tools ledger` lists every adopted tool with source URL, content hash, the capability-miss that triggered it, the task, the grant time and the tests that proved it. A tool with no row fails `fm doctor`.

- **One-card grant bundle** — FEATURE — value 4 — effort M — risk low — category: grant queue
  Why: pack ideas (vet, injection scan, sandbox trial, diff review) would each add a separate step. Assumption: separate steps would bury the user in cards.
  Done when: a queued grant shows one card with the vet verdict, scan result, sandbox trial output, pinned hash and requested permissions. Approving it takes one answer, and a test checks that no grant card is created without all five fields.

- **Permission manifest diff for every tool** — SECURITY — value 5 — effort M — risk med — category: permissions
  Why: assumption: found MCP servers and plugins declare hooks, network use, env access and file paths. The user decides on those, not on the name.
  Done when: the grant card lists the declared and *observed* capabilities (network hosts, env vars read, paths written) from the sandbox trial. A tool that uses something it didn't declare is refused by a test fixture.

- **Typosquat and lookalike check on search results** — SECURITY — value 3 — effort S — risk low — category: vetting
  Why: `fm plugins find` and `fm lib search` return names from outside. The pack's vet idea covers behavior but not name confusion. Assumption: results are matched on text.
  Done when: a fixture search returning `fm-lib-serach` next to a known `fm-lib-search` flags the lookalike and lowers its rank, and the flag shows on the card.

- **Author-writes, different-model-reviews for built tools** — SECURITY — value 4 — effort M — risk low — category: built tools
  Why: the pack asks which verbs have a model on both sides with no user check. `fm new tool` and `fm mcp new` have the writer's own tests as the only judge. Standing rule: weakness-finding uses signals Foreman didn't author.
  Done when: a built tool gets a cold read by a different model against its stated purpose (does it do anything beyond it: network, writes outside scope, exec). A fixture tool with a hidden `curl` fails the read and is not offered for use.

- **Trust tiers that expire** — FEATURE — value 4 — effort M — risk low — category: grants
  Why: a grant "spent on use" matches the push-grant pattern in the steers. Assumption: today an adopted tool stays trusted forever.
  Done when: each tool has a tier (trial, project, global). A grant moves it up only by user answer, and unused tools drop back after N days. A test shows an expired tool asks again.

- **Update watch with diff-only re-grant** — SECURITY — value 4 — effort M — risk med — category: updates
  Why: extends "review the diff when a found tool updates". Combined with the ledger, a changed hash is the trigger. A changed permission manifest forces a new grant, while a doc-only change doesn't.
  Done when: a fixture tool update that adds a network call blocks use and queues a card showing only the diff. A comment-only update passes silently.

- **Tool recall: revoke and sweep** — FEATURE — value 3 — effort S — risk low — category: revocation
  Why: assumption: there is no way to pull a tool back once it's adopted and tasks used it.
  Done when: `fm tools revoke NAME` removes it, lists the done tasks whose proof rested on it, and files them into the Unproven rollup (Mission 7).

- **Prefer building over installing when the need is small** — FEATURE — value 3 — effort S — risk low — category: find-or-build
  Why: the user's rules favor a lean always-on footprint (Lean ratchet) and a stdlib script is a smaller trust surface than a third-party server. Assumption: the miss trigger currently ranks "find" first.
  Done when: for a miss the vet scores as "under 50 lines of stdlib", the trigger names the build path first. A test covers both branches.

- **Reproducible build of any tool Foreman adopts (wild)** — SECURITY — value 3 — effort L — risk med — category: provenance
  Why: wild. Instead of trusting a packaged artifact, Foreman fetches the source at a pinned commit, builds it in the sandbox and checks the output hash matches what the registry serves.
  Done when: for a fixture package whose published artifact differs from its source build, the grant card says "artifact does not match source" and blocks.

- **Canary tool: a fake secret honeypot in the trial sandbox (wild)** — SECURITY — value 4 — effort M — risk low — category: sandbox
  Why: wild. The trial sandbox holds decoy credentials (fake `~/.aws`, `.env`, SSH key). A found tool that reads or sends them is caught in the act, which beats static scanning.
  Done when: a fixture tool that reads the decoy `.env` is marked "touched secrets" with the access trace, and the card shows it red.

- **Shared tool reputation from the user's own history (wild)** — FEATURE — value 3 — effort M — risk low — category: reputation
  Why: wild. Reuse the trigger-precision idea from Mission 8. Each tool gets a held-rate (tasks that used it and stayed done, versus reverted or re-fixed). A low-scoring tool is flagged for removal on the next doctor run.
  Done when: `fm tools score` prints per-tool held-rate from task outcomes, and a fixture with 3 reverts after use appears in `fm doctor` as a removal candidate.

- **Offline vendor mode: adopt by copying, never by reference** — SECURITY — value 3 — effort M — risk low — category: local-first
  Why: assumption: found tools are referenced by an install command that fetches at run time. Vendoring the reviewed files into the project makes the reviewed bytes the run bytes.
  Done when: an adopted tool runs with the network blocked and its files match the ledger hash. Editing the vendored copy trips the re-check.

- **Dependency tail check for built tools** — SECURITY — value 3 — effort S — risk low — category: dependencies
  Why: `fm mcp new` could pull packages. Assumption: the scaffold template lists dependencies without limits, though the stdlib script path avoids this.
  Done when: a scaffolded tool importing a non-stdlib package must list it in the manifest with a hash. A test shows an unlisted import fails `fm check`.

Next question: Which grants has the user already given by hand, and can their answers reveal the real vetting criteria they apply, so the card shows those and not generic ones?
Next question: When a found tool is unavailable or revoked mid-task, what does the task fall back to, and does the user see that the proof changed?
