# Brainstorm — lens: user value

- **Ship the guard, resume and done-gate as standalone plugins** — FEATURE — value 5 — effort M — risk med — category: distribution
  Why: the survey says every popular rival installs in one marketplace command and adds commands without rewriting `~/.claude`, while Foreman's full install asks for a large trust leap (bypass mode, 20 deny rules, third-party plugins). Blocking dangerous commands in bypass mode and resuming after `/compact` are the parts nobody else has. Each can stand alone as an install with no wiring, built from the same code. Run a marketplace-readiness lint (manifest, size, no global writes, license) before each submission.
  Done when: `/plugin install foreman-guard@…` in a clean HOME blocks a seeded `rm -rf` in bypass mode, leaves `~/.claude/settings.json` byte-identical, and the readiness lint passes.

- **Ship stack packs picked at `fm init`** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: a newcomer's `fm check` finds no test runner and `fm repeats` suggests bad gates. A pack for each common stack (pytest, npm/vitest, cargo, go, Django, Rails, Next, Zig) would set the whole-suite gate, risky paths, ask-versus-allow commands (`terraform apply` asks, `npm run build` doesn't) and 5 starter lessons. Assumption: roughly 8 stacks cover most users.
  Done when: `fm init` in a fixture Next.js repo and a fixture cargo repo each configures a passing gate and a stack-specific guard rule without any editing.

- **Add `fm new` for empty directories** — FEATURE — value 4 — effort L — risk med — category: greenfield
  Why: spec-kit and BMAD win on starting from nothing. Foreman is built around an existing tree. One sentence in an empty directory would produce a one-page spec to approve, a stack pack, a scaffold with a failing first test, and a queued first task.
  Done when: `fm new "CLI that dedupes files"` in an empty directory ends with a committed spec, a green scaffold gate and one queued task.

- **Turn a labelled GitHub issue into a verified PR in CI** — FEATURE — value 4 — effort L — risk med — category: ci
  Why: CCPM turns issues into parallel agents and PRs, and the survey lists GitHub/Linear sync as a gap. Existing ideas cover importing issues as briefs and reviewing PRs, but not the full loop. A `foreman` label would run a headless task, attach the evidence pack as a PR comment, and ask the human only at merge.
  Done when: labelling a fixture issue opens a PR whose body lists criteria with recorded evidence, and an unmet criterion leaves the PR as a draft.

- **Add `fm where-is-my-work`** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: lanes, worktrees, stashes, deferred tasks and unmerged branches are spread across projects, and the recent commits keep fixing lane leftovers. A user who walks away needs one answer to "is anything of mine stranded or unmerged?", with one command per item to finish or discard it.
  Done when: with a seeded orphan lane, an unmerged task branch and a stash in two fixture projects, one command lists all three with a safe next command each.

- **Alias rival command names to Foreman procedures** — FEATURE — value 3 — effort S — risk low — category: adoption
  Why: superpowers users already type `/brainstorm`, `/write-plan` and `/execute-plan`, and spec-kit users type `/specify`, `/plan` and `/tasks`. Thin aliases onto Foreman's own flow remove relearning. Assumption: the alias names don't collide with installed plugins; the conflict probe would check this.
  Done when: each alias runs the matching Foreman skill in a clean HOME, and a collision with an installed plugin is skipped with a one-line note.

- **Write release notes from the user's own usage** — FEATURE — value 3 — effort S — risk low — category: upgrades
  Why: Foreman ships many changes a day and 46 of its 108 verbs were never run by Claude in 11 days. Users only care about the ones that touch what they use. Filter the changelog by the user's verb, hook and setting history and print "3 changes affect you, 40 don't" on the first session after an upgrade.
  Done when: upgrading between two fixture versions prints only the entries whose verbs or settings appear in the fixture usage log, with a count of the rest.

- **Add `fm examples`, a searchable gallery of real terse requests** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: the README's first screen is abstract and the jargon is unexplained. Redacted cases from the 688 finished tasks would show each request, the type and tier Foreman chose, and the evidence that closed it, filtered by type. Assumption: the existing redactor is enough to make cases publishable.
  Done when: `fm examples FIX` prints at least 5 cases from the bundled corpus, and a scan for secrets and home paths finds none.

- **Bridge Telegram, Slack and ntfy both ways, outbound-only** — FEATURE — value 3 — effort M — risk med — category: chat-ops
  Why: the push ideas so far are one-way. A terse request sent from a phone, and a yes or no from a notification, is what makes unattended runs usable. The bridge would poll outbound with no inbound port and tag messages as untrusted input.
  Done when: a message to a test bot arrives in the capture inbox verbatim, and a "yes" resolves one pending `fm ask`.

- **Wild: add a Foreman Exchange of stack packs and lessons with bench receipts** — FEATURE — value 4 — effort L — risk high — category: ecosystem
  Why: wild. ECC's 311 skills and agent-os's standards show people want shareable procedure packs, but nothing proves they help. Each Foreman pack would ship with the replayed-case delta it earned, such as "+8 points first-pass on 40 Django cases", and refuse to publish without one. This depends on the bench growing past its current 1 case, so it turns the proof gap into a pipeline.
  Done when: a pack installs only if it carries a bench receipt that re-verifies locally on a fixture repo.

- **Wild: credit every external bug report that becomes a bench case** — FEATURE — value 3 — effort S — risk low — category: community
  Why: wild. Foreman has no published evidence and few outside users. A reproducing report would become a named case in the public bench and a credited changelog line, so every reporter adds to the proof and has a reason to return.
  Done when: running the report command on a fixture failure produces a redacted case file, and the changelog generator credits the reporter handle.

- **Wild: put quality debt on a visible ledger** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. 18 of 688 closes were fixed later (2.6%), and folded tasks show as "ungraded". When a closed task is reopened, its original cost would go on a "debt" line shown at session start and at zero when clear. Reopened work would jump the queue. Seeing the number is what would make the 97.4% believable.
  Done when: reopening a fixture task adds its original cost to the debt line and puts it first in `fm next`, and clearing it returns the line to zero.

- **Accept requests in any language** — FEATURE — value 2 — effort M — risk low — category: reach
  Why: assumption: some users type requests in their own language. Ticket ids, commands and prefixes like `FIX:` stay literal, while status text follows the request language. The rival survey doesn't show anyone doing this, so it is cheap to lead on.
  Done when: a German fixture request is classified as the same type and tier as its English equivalent, and the close-out summary comes back in German.
