# Brainstorm — lens: approaches

Round 4 is close to saturated: nearly every newcomer, safety, proof and simplification angle is already in the pile. These are the gaps I could still find for "make it THE plugin". They are approaches to adoption and to keeping the project maintainable, and none repeats a listed idea. Assumptions are marked.

- **Own the search term and the one-line pitch** — FEATURE — value 4 — effort S — risk low — category: discoverability
  Why: assumption: "foreman" collides with the Red Hat sysadmin tool and the Ruby process manager, so a newcomer searching the name finds the wrong thing. The README's first screen is also abstract (evidence A1). Fix the tagline, the marketplace and `plugin.json` keywords, and the repo topics, then draft submissions to the awesome-claude-code lists.
  Done when: the README's first line and `plugin.json` carry a disambiguating tagline ("evidence-gated task discipline for Claude Code"), and a lint in `fm doctor --publish` fails if either is missing.

- **Ship one `fm.pyz` release asset that every channel consumes** — FEATURE — value 4 — effort M — risk med — category: distribution
  Why: install currently needs a clone, git and Python 3.12.7+ (README). The installer, a devcontainer feature, CI and a future GitHub Action could all fetch one checksummed zipapp instead.
  Done when: `python3 fm.pyz doctor` runs in a clean container with no clone, and the installer's `--desktop` and CI paths use the same asset by checksum.

- **Add `fm scaffold verb|hook|skill`** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: 28k lines in 48 modules, with seven copies of `_git` and three child launchers, shows that new code is copied by hand. A generator would create the module, registry entry, test stub and help line from one template, so contributors start from the shared helpers.
  Done when: `fm scaffold verb demo` produces a passing test and a registry entry, and the "every command reference resolves" check stays green.

- **Publish `llms.txt` and an AGENTS.md for Foreman itself** — FEATURE — value 3 — effort S — risk low — category: agents
  Why: users can ask Claude "how do I use Foreman?", and MASTER.md at 18k words is too large for that to work. Generate a short agent-facing guide from the verb registry that states what is core, what is internal, and the one-call `fm task finish` path.
  Done when: a cold child given only `llms.txt` completes init → capture → finish on a fixture without a wrong verb.

- **Fail the release on install footprint** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: the install silently changes permissions, output style, the statusline and 20 deny rules (A2). Record in CI the install wall time, the number of `~/.claude` files touched, the always-on token count and the number of settings keys changed, and fail the release if any budget is exceeded.
  Done when: `install.sh` in a clean HOME emits a footprint JSON and CI fails when a key count or token total exceeds the stored budget.

- **Use day-7 keep rate as the round's north-star metric** — FEATURE — value 5 — effort M — risk med — category: user value
  Why: rounds 2-3 came back dry because nothing measures whether newcomers stay. A day-7 keep / lite / remove answer, logged locally, would let each round be judged by it. Assumption: the user will opt in to one local-only counter.
  Done when: `fm doctor --north-star` prints the keep rate over the local installs it can see, and `fm round close` refuses a round that has no before/after value for it.

- **Add a "reachability" tag to every MASTER.md section** — CLEAN — value 3 — effort M — risk low — category: simplicity — wild
  Why: MASTER.md is 18k words and the rules are loaded every session. Tag each section with its consumer (a hook, a skill, a verb, or human-only) and let CI flag sections nothing reads or injects. This applies the dead-code idea to docs.
  Done when: CI lists unconsumed sections, and deleting one removes it from the generated site with no broken reference.

- **Generate a public ROADMAP.md with a won't-do list** — FEATURE — value 3 — effort S — risk low — category: positioning — wild
  Why: the 13 deferred T-079x clusters, the by-design drops and the over-engineering audit already hold the reasons. Render them as "now / later / deliberately not", which tells evaluators what Foreman will not become and why.
  Done when: `fm roadmap` builds the file from the queue and the drops, and every won't-do line cites a recorded reason.

- **Add `fm first-hour`: score the install against a cold agent playing newcomer** — FEATURE — value 4 — effort M — risk med — category: onboarding — wild
  Why: the newcomer findings (A1–A11) were gathered once by hand. A cheap child with only the README would attempt the first hour on a clean HOME, record each stall and refusal, and open a ticket per stall. Run it at each release.
  Done when: the command writes a stall list with step numbers, and the release gate lists the open stalls from the last run.

- **Retire a verb or setting before adding one, tracked in a net-surface ledger** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: 108 verbs, 46 never run by Claude in 11 days, and a verb-surface target of about 70. Record each round's verb, setting and hook counts and show the delta in the round receipt. This is a ledger, not a block.
  Done when: `fm round close` prints verbs, settings and hooks added versus removed since the previous round.

- **Run a "rival-installed" newcomer path as a permanent no-model test** — FEATURE — value 3 — effort M — risk med — category: interop
  Why: users will already have superpowers or ECC (survey B). Install Foreman beside a fixture plugin that registers the same events, and check that the first-run output and doctor verdict stay clean.
  Done when: CI installs both into a clean HOME and `fm doctor` ends in one line with no conflict warning that has no stated fix.
