# Brainstorm — lens: capability map

- **Bridge trackers and PR review comments into the queue** — FEATURE — value 4 — effort M — risk med — category: integrations
  Why: assumption: the pack shows `fm intake` and `fm capture` and a "pr" command that writes descriptions, but no inbound path from GitHub Issues, Linear, or PR review threads. Reviewer comments on a Foreman PR are the most natural next requests.
  Done when: a review comment on a PR from a finished task becomes a captured brief linked to that task. Closing the task replies on the thread with its evidence.

- **Snapshot the public surface and gate breaking changes** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: the done-gate checks tests and lenses, but nothing compares the CLI help, HTTP routes, config schema, DB schema, or exports before and after. JARVIS and other consumers keep reporting breakage from Foreman changes (the 1.2.x release stream).
  Done when: changing a flag name in a fixture project makes `fm task done` refuse until the brief declares a breaking change. An unchanged surface passes silently.

- **Review other people's PRs with Foreman's lenses in CI** — FEATURE — value 4 — effort M — risk med — category: review
  Why: assumption: the review lenses, `fm audit` and `fm second` already exist for Foreman's own diffs. A GitHub Action that runs them headless on any inbound PR would extend them to teams and open-source maintainers. T-0034 (`fm audit run`) is deferred but is the same machinery.
  Done when: opening a PR on a fixture repo posts a structured findings comment with file and line anchors. Findings the user dismisses are recorded as taste.

- **Compact at step boundaries with a curated handoff** — FEATURE — value 4 — effort M — risk med — category: context
  Why: the pack shows resume after `/compact` via a PreCompact checkpoint, which fires wherever Claude Code chooses. Foreman could watch context fill and trigger compaction between steps, after writing a handoff of only the facts the next step needs.
  Done when: in a long fixture task, compaction fires only at a step boundary. The next step's first action matches what an uncompacted run does.

- **Land changes across several repos as one atomic set** — FEATURE — value 4 — effort L — risk high — category: orchestration
  Why: the pack shows JARVIS and Foreman changing in tandem (briefs shipped "to GitHub main and JARVIS"). Lanes and merges are single-repo, and "let projects request changes" covers asking, not coordinated landing.
  Done when: a two-repo change set merges in dependency order. If the second repo's gate fails, the first is reverted or held, with the reason recorded.

- **Pin gate environments to tell drift from regression** — FEATURE — value 3 — effort L — risk med — category: reproducibility
  Why: assumption: `fm sentinel` re-runs old checks, and a failure could be a toolchain or dependency change rather than a code regression. Recording tool versions and a lockfile hash per evidence entry (or running gates in a devcontainer or Nix shell) would classify each sentinel failure.
  Done when: a sentinel failure caused by bumping a tool version in a fixture is reported as environment drift, not regression.

- **Trace every criterion to its test and code** — FEATURE — value 3 — effort M — risk low — category: traceability
  Why: `fm why` goes from code to commits, and `fm map` links tests to sources. There is no matrix from acceptance criterion to verify command to covered lines, so uncovered intent is invisible.
  Done when: `fm trace T-xxxx` lists each criterion with its verify command and the changed lines it exercises. A criterion exercising none is flagged.

- **Add an incident mode for hotfixes** — FEATURE — value 3 — effort M — risk med — category: workflow
  Why: assumption: tiers scale the gates, but there is no fast path that trades ceremony for a mandatory after-the-fact audit. Production fires are where discipline layers get bypassed.
  Done when: `fm incident` shrinks the pre-merge gates to a named minimum. It auto-opens a follow-up audit task and a timeline entry that blocks the next release until closed.

- **Automate dependency upgrades from `fm deps`** — FEATURE — value 3 — effort M — risk med — category: maintenance
  Why: `fm deps` already reports major-version lag with a migration question, but nothing acts on it. A lane per bump could read the changelog, apply the change, and run the gates.
  Done when: one outdated dependency in a fixture becomes a lane with a migration note and gate evidence, and merges or reports blocked.

- **Add team claims for multiple humans** — FEATURE — value 3 — effort L — risk med — category: collaboration
  Why: assumption: `fm sync` mirrors briefs into the repo, but the queue assumes one user. Two people running Foreman on one repo would collide on focus and merges.
  Done when: two clones claiming the same task see a conflict before work starts. Review requests route to the other person by name.

- **Wild: Rebuild Foreman from its spec and diff the behaviour** — FEATURE — value 4 — effort L — risk low — category: spec fidelity
  Why: wild. `--build` and `BUILD_PROMPT.md` already exist. Building in a scratch dir and replaying the e2e suite plus the guard replay corpus against the result would show which behaviours live only in code and not in MASTER.md or the prompt.
  Done when: a report lists behaviours that differ between the rebuild and the live plugin, each filed as a doc or spec task.

- **Wild: Give decisions revisit triggers** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: wild. `fm decide` records decisions like "YAGNI: loosening the brief gate adds guard surface", but nothing says when to reconsider them. A trigger such as "revisit when two refusals of this kind recur" or "when Claude Code adds feature X" would let decisions expire on a condition instead of silently going stale.
  Done when: a decision with a trigger auto-captures a review brief when the condition fires, quoting the original reasoning.

- **Wild: Pin current behaviour with characterization tests before touching an unfamiliar repo** — FEATURE — value 4 — effort L — risk med — category: onboarding
  Why: wild. `fm init` registers a project, but nothing makes legacy code safe to change. An `fm adopt` pass could discover the gates by trying them, then generate tests that lock in today's observable behaviour.
  Done when: on a fixture repo without tests, `fm adopt` produces gate commands that pass on the untouched tree. A deliberate behaviour change then fails one of them.

- **Wild: Run an LSP-backed impact analysis and safe rename** — FEATURE — value 3 — effort M — risk med — category: code intelligence
  Why: wild. `fm impact` and `fm outline` are file- and test-link based. Asking the language server for references would give exact dependents, so `fm impact` could report symbol-level blast radius and `fm lane` could refuse overlapping symbol edits.
  Done when: renaming a function in a fixture reports every caller across files, and `fm impact` on that symbol matches the language server's reference list.
