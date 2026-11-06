# Brainstorm — lens: simplicity

- **Replace HELP_TIERS hand-edits with per-verb self-registration** — CLEAN — value 4 — effort S — risk low — category: structure
  Why: Review says nearly every second parallel merge conflicted on the one HELP_TIERS line in fmcli.py (T-1059, T-1062 twice), each needing a re-merge builder.
  Done when: Adding a verb touches only its own file, two builders each adding a verb merge with no conflict, and `fm help` output is unchanged (golden test).

- **Add `fm guard why "<cmd>"`** — FEATURE — value 5 — effort S — risk low — category: debuggability
  Why: Guard false positives cost the most debugging time; the main thread wrote scratch replay scripts twice (T-1125, T-1141). Nothing answers "would the guard allow this here, and why".
  Done when: `fm guard why "cmd"` run in a given cwd prints allow/deny, the matching rule and the parsed segments, and matches the real hook's decision on 20 recorded commands.

- **Lint verify commands when they are added** — FIX — value 4 — effort S — risk low — category: correctness
  Why: Verify commands naming nonexistent test modules or `npm test` without npm are caught only when they run (T-1128/T-1133 made runs editable, nothing checks at add time).
  Done when: `fm verify add` with a missing module path or absent runner is refused with the reason and a suggested command.

- **Collapse the escape-hatch flags into one `--because`** — CLEAN — value 3 — effort M — risk med — category: surface
  Why: The pack's earlier ideas list this, but nothing shipped; each bypass flag is a separate thing to learn and audit. Assumption: several `--force`/`--skip-*` style flags exist.
  Done when: Every bypass flag is accepted only through `--because "<reason>"`, the reason lands in the ledger, and the old flags print a one-line migration.

- **Cache a parsed brief index so no command parses 1,069 briefs** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: T-1140 fixed hooks only; `fm state --json` took over 120 s under load and other commands still parse every brief.
  Done when: `fm state --json` on a 1,000-brief repo under load 30 completes under 3 s, and the index rebuilds itself after a brief edit (test).

- **Archive closed briefs out of the hot directory** — CLEAN — value 3 — effort S — risk low — category: scale
  Why: 1,069 briefs make every scan slow; closed ones are rarely read. Simpler than an index for the common case.
  Done when: Briefs closed over 30 days move to `archive/` by `fm tidy`, `fm show T-id` still finds them, and active scans read only the live set.

- **Make builders self-attack before returning "done"** — FEATURE — value 5 — effort M — risk low — category: quality
  Why: Reviewers found real defects in nearly every builder branch (deny-bypass, false green, unbounded time, writes outside a folder).
  Done when: A builder's done report must include a filled checklist (deny paths, time bounds, write scope, empty input), and `fm lane close` refuses without it.

- **Resolve cwd to the worktree root for every path argument** — FIX — value 3 — effort S — risk low — category: correctness
  Why: Builders cd into subdirectories and lease paths doubled (`mods/foreman-ui/mods/foreman-ui/...`).
  Done when: Running `fm lease` from a subdirectory with a relative path records the repo-root-relative path once, and a doubled path is rejected.

- **Delete the deferred "Later from T-…" tail** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: About 30 deferred items (T-0787…T-0866) each say "later: needs evidence"; they are never triaged and dilute `fm next`.
  Done when: Each is closed as dropped or reopened with a concrete trigger, and the open list shrinks by at least 20 with no information lost (ids kept in the ledger).

- **Wild: Run Foreman in a "one verb" mode** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: assumption: 1,158 skills files and a long verb list overwhelm newcomers (T-0861 Lite mode was deferred). Only `fm` exists, and it answers "what now?", acting on the one obvious next thing.
  Done when: A fresh user types only `fm` for a full task from request to close, and the transcript shows no other verb needed. (wild)

- **Wild: Generate the README from the code and delete the hand-written parts** — CLEAN — value 3 — effort M — risk med — category: docs
  Why: Version strings, verb lists and claims drift (pane 0.7.0 installed vs 0.17.0 in the repo).
  Done when: CI regenerates verbs, versions and gate lists into the README and fails on any diff; hand-written prose is under one screen. (wild)

- **Wild: Prune by usage: auto-open deletion tasks for verbs unused in 60 days** — CLEAN — value 4 — effort M — risk med — category: deletion
  Why: Many features shipped this round; the pack asks "report which features are never used" but nothing deletes them. The ledger has the call data.
  Done when: A weekly job lists verbs with zero ledger calls in 60 days and opens a deletion task for each with its callers and tests listed. (wild)

- **Make shared registries append-only directories** — CLEAN — value 3 — effort M — risk low — category: structure
  Why: HELP_TIERS is one instance; any list every feature edits conflicts the same way. Assumption: other registries exist (cards, doctor checks, hook lists).
  Done when: Each such registry is a directory of one-file entries discovered at load, and a two-builder merge test adding to each passes with no conflict.
