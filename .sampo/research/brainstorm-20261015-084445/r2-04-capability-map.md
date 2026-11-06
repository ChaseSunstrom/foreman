# Brainstorm — lens: capability map

- **Honor `<private>` spans and `.foremanignore` everywhere** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: claude-mem's `<private>` tag is its trust feature and Foreman has no user-controlled equivalent (assumption: redaction today is pattern-based and automatic only). Newcomers already balk at how much Foreman writes and wires.
  Done when: text inside `<private>…</private>` in a prompt, and files matching `.foremanignore`, never appear in the ledger, briefs, recall index, evidence, `fm page` or exports. A test greps all state for a planted marker.

- **Ship a task-template gallery** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: newcomer item 6: `fm task new --help` lists no valid types or tiers and no example. Task Master and spec-kit both start from templates. Templates would be bug fix, add endpoint, bump dependency, fix flaky test and rename symbol, each with prefilled criteria, gates and a verify hint.
  Done when: `fm task new --template` lists the templates, and `--template bugfix "login timeout"` creates a briefed task whose criteria and verify command are non-empty.

- **Read a committed `.foreman/project.toml` for team-shared gates** — FEATURE — value 4 — effort M — risk med — category: teams
  Why: assumption: everything today lives in per-user central state, so a teammate who clones the repo gets none of the project's gates, vetoes or tier defaults. CCPM and spec-kit win teams through files in the repo. The risk is that a cloned repo can specify commands to run, so config must be hash-approved on first use and re-approved on change.
  Done when: a fresh clone prompts once to trust the config, then applies its gates. Editing the file re-prompts, and an unapproved file runs nothing.

- **Publish ecosystem gate packs as data** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: newcomer item 7: `fm check` doesn't detect the test runner. Foreman is Python-centric (its own gates are unittest and pytest). Packs (Rust, Go, JS/TS, Java, .NET, notebooks) would each be a small TOML file giving the detector, test, lint and affected-test commands, so adding an ecosystem needs no code.
  Done when: in fixture repos for five ecosystems, the first `fm check` proposes the right gate. A contributor adds a sixth pack with no Python change.

- **Add a forge adapter layer (GitHub, GitLab, Gitea/Forgejo)** — FEATURE — value 3 — effort L — risk med — category: integrations
  Why: the survey lists GitHub Issues sync as a gap, and the pack only mentions `gh`. Assumption: PR drafting, CI-result reading and issue import are GitHub-only today. One interface would let all three work against GitLab and Forgejo.
  Done when: issue import and PR draft pass the same contract tests against a recorded GitHub fixture and a recorded GitLab fixture.

- **Generate a versioned offline docs site from the verb registry** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: MASTER.md is 18k words, `fm --help` is 231 lines, and the README's first screen is abstract. A static site with one page per verb (examples, valid values, exit codes) plus a search box and a "start here" path replaces reading the monolith.
  Done when: `fm docs build` writes a site that opens from `file://`. Every registered verb has a page, and a test fails if one is missing.

- **Generate a contributor onboarding pack for humans (`fm onboard`)** — FEATURE — value 3 — effort M — risk low — category: teams
  Why: agent-os and BMAD extract conventions for the agent, but nothing hands a new human teammate the repo's map, gates, decisions, vetoes and lessons. Foreman already holds all of these.
  Done when: `fm onboard` writes one Markdown page with sections for layout, how to run gates, standing decisions and "don't do this" lessons. A cold reader can locate the test command from it.

- **Show usage-aware "what's new" on upgrade** — FEATURE — value 3 — effort S — risk low — category: discoverability
  Why: 46 of 108 verbs are never run by Claude, and a user can't know what's new or relevant. After an upgrade, list only changes touching verbs or features this user's history actually used, plus one "you haven't tried" suggestion.
  Done when: upgrading from a fixture version prints at most 5 lines, each tied to a verb in the local history. It prints nothing on the second run.

- **Support non-English intake and output** — FEATURE — value 2 — effort M — risk low — category: reach
  Why: assumption: classifier keywords such as FIX and "fix the…" and the jargon-heavy output are English-only. Rivals with tens of thousands of stars have international users. Classification and status prose should follow the user's language.
  Done when: a Spanish and a Japanese request classify to the same type and tier as their English originals in a table test. `fm status` honors a `language` setting for its prose.

- **Wild: Add chat-ops with two-person approval for one-way doors** — FEATURE — value 3 — effort L — risk med — category: surfaces
  Why: wild. The pack covers the phone and ntfy but not Slack or Discord, where teams live. A bot posts "needs you" cards and can require two distinct humans to approve irreversible actions.
  Done when: in a local test with a fake chat server, a push-to-main ask stays blocked after one approval and clears after a second, different approver.

- **Wild: Split Foreman into marketplace micro-plugins (guard, resume, evidence)** — FEATURE — value 4 — effort L — risk med — category: distribution
  Why: wild. Every popular rival is found through a one-command marketplace install, and Foreman's single large plugin rewrites `~/.claude`. Single-purpose plugins such as `foreman-guard` would be a zero-wiring funnel, and the full Foreman would layer on top.
  Done when: each micro-plugin installs alone in a clean HOME and passes `fm doctor` with no changes to `defaultMode`. The full plugin detects and adopts them.

- **Wild: Fetch a signed, read-only "Foreman Commons" feed** — FEATURE — value 3 — effort L — risk med — category: ecosystem
  Why: wild. One signed, versioned index delivers guard-rule updates, gate packs and templates between releases, so a new bypass pattern can be fixed in hours. It is pull-only and sends nothing from the user's machine.
  Done when: `fm commons update` verifies the signature and applies new gate packs. A tampered feed is rejected, and with the setting off there are zero network calls.
