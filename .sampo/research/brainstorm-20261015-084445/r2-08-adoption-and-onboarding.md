# Brainstorm — lens: adoption and onboarding

- **Keep every setting the user already chose** — FIX — value 5 — effort M — risk low — category: install
  Why: A2 says the default install silently sets bypassPermissions, outputStyle, autocompact and a statusline wrapper, while every rival "adds commands, doesn't rewrite ~/.claude". Assumption: the installer currently overwrites rather than detects.
  Done when: with a pre-seeded settings.json (own defaultMode, outputStyle, statusline), install leaves those values byte-identical and prints one "kept your X" line for each.

- **Remember the user's reversals and never re-apply them on update** — FEATURE — value 4 — effort S — risk low — category: install
  Why: assumption: updates re-run the wiring. A newcomer who flips bypass back to default would see it silently reset, which is the fastest way to lose trust.
  Done when: after the user changes a Foreman-set key and runs the updater, the key keeps their value and `fm wire` lists it as "yours".

- **Make the install an agent-executable `INSTALL.md`** — FEATURE — value 4 — effort S — risk med — category: install
  Why: B shows newcomers already sit inside Claude Code, and the README's first step is a curl-pipe-bash. A pinned, step-by-step file Claude follows (showing each change and asking before settings edits) fits that context.
  Done when: pasting the one-line prompt into a clean-HOME session installs Foreman, stops for consent before each `~/.claude` change, and ends with a passing `fm doctor`.

- **Invite a teammate with one file (`fm invite` / `fm join`)** — FEATURE — value 4 — effort M — risk low — category: team adoption
  Why: B notes rivals spread through repos and teams. Assumption: Claude Code project settings can name a marketplace and enable a plugin. The invite would carry that stanza, the gate presets, the vetoes and a 3-task starter queue, with state kept out of git.
  Done when: in a fresh clone with a clean HOME, `fm join invite.json` yields a working project with no personal state committed.

- **Add `fm coexist <plugin>`: stage ownership plus a translation cheat sheet** — FEATURE — value 4 — effort M — risk med — category: interop
  Why: B lists superpowers (~300k stars) and ECC (~280k). People who already use them need "your /brainstorm is `fm ideas`" and a way to let one plugin own planning while Foreman keeps the guard, evidence and resume.
  Done when: with superpowers installed, `fm coexist superpowers` disables Foreman's duplicate stages, prints the mapping, and `fm doctor` reports no hook conflict.

- **Ship offline `fm docs <query>` with stable codes that refusals link to** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: MASTER.md is 18k words, and A9 says the `fm task done` refusal gives four bullets with no pointer. A stdlib keyword search over MASTER.md returning the top 3 sections would fill that gap. Each guard or gate refusal would carry a code that `fm docs E-xx` resolves.
  Done when: every refusal message includes a code, and `fm docs <code>` prints its section in under 100 ms offline.

- **Score project fit at init and recommend a posture per repo** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: C says 46 of 108 verbs are never used, and an over-engineering audit found heavy ceremony. A one-off script repo shouldn't get the full ceremony. Assumption: signals like tests present, size and commit cadence are cheap to read.
  Done when: `fm init` prints a fit line ("full / lite / guard-only, because …") for three fixture repos and picks differently for each.

- **Add a day-7 keep / lite / remove card seeded by a one-line wish** — FEATURE — value 4 — effort M — risk low — category: retention
  Why: C shows there's no published proof, but a user's own numbers can stand in. At install Foreman asks "what do you hope this fixes?" and on day 7 shows matching counts from the ledger (for example compactions survived, unverified "done" blocked) with one-key keep, lite or remove.
  Done when: a fixture ledger yields a card quoting the wish and at least two matching measured counts, and each key makes the matching change.

- **Lint the README so every number cites a results file** — CLEAN — value 3 — effort S — risk low — category: trust
  Why: C says the bench has 1 case and 0/3 court cases. Over-claiming in the first screen is a risk when a skeptic checks. Unbacked figures should fail CI.
  Done when: a README with a number lacking a `results/` reference fails the lint, and the current README passes.

- **Order and label the slash menu as a journey (start, work, finish, recover)** — CLEAN — value 3 — effort S — risk low — category: discoverability
  Why: A11 flags jargon, and the plugin ships dozens of skills. Assumption: descriptions are internal-flavoured and unordered.
  Done when: a test checks every user-invocable skill description is verb-first, ≤80 characters, and tagged with exactly one of the four stages.

- **Re-engage an installed-but-unused Foreman once, with the exit offered beside it** — FEATURE — value 2 — effort S — risk low — category: retention
  Why: assumption: a new user who installed and never finished a task is the commonest silent drop-off. One SessionStart line shows the smallest next step and the one-line uninstall.
  Done when: after 3 days with zero finished tasks the line appears exactly once, then never again.

- **Wild: run `fm duel --vs <plugin>` on the same real task** — FEATURE — value 3 — effort L — risk med — category: proof
  Why: wild. B shows adoption is a head-to-head against installed rivals. The same brief would run in two worktrees (one with the rival, one with Foreman) and produce a side-by-side of diff, evidence and tokens. The user judges on their own repo.
  Done when: on a fixture task both lanes run and a comparison report lists diff size, verification evidence and spend for each.

- **Wild: add a stuck-newcomer rescue ladder** — FEATURE — value 3 — effort M — risk med — category: support
  Why: wild. After the same `fm` error or refusal appears 3 times, offer in order: the docs section, a matching known issue, then a redacted draft discussion post shown for approval, since sending is outward-facing.
  Done when: three identical failures trigger the ladder, nothing leaves the machine without an explicit yes, and the draft contains no paths or username.

- **Wild: A/B the README with cold agents** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: wild. Evidence A1 says the first screen is abstract. Variants of the first screen would be scored by cold agents attempting install plus first task from only that text, and the best variant is kept by measured completion.
  Done when: a script runs N variants × M cold runs, reports completion rate and steps to first finished task, and the chosen README beats the current one.
