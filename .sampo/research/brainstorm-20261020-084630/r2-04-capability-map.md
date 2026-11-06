# Brainstorm — lens: capability map

- **Export the guard as native permission and sandbox rules** — FEATURE — value 4 — effort M — risk low — category: security
  Why: the Benchmarks result is that 20 of 24 dangerous commands are stopped and plain Claude Code runs all 24. That protection only applies when Foreman's hooks run. A generated `permissions.deny`/`ask` block and sandbox config reaches people who never use bypass mode, and it makes a cheap on-ramp (assumption: the rule shapes map from the guard's corpus).
  Done when: `fm guard export` writes a settings fragment, and a test feeds the known-24 and the 25 everyday commands to it, showing it blocks or asks on at least the 20 stopped commands and none of the everyday ones.

- **Audit the whole session context, not just Foreman's share** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: the user wants lower cost and a smaller "Foreman tax". Foreman's 15 skills are about 3,200 of 9,600 listing chars. The other 6,400 chars, MCP schemas and other plugins' hooks are invisible to Foreman and decide how fast compaction comes. Existing ideas meter only Foreman's own injections.
  Done when: `fm diet` prints bytes per source (skills, MCP tools, CLAUDE.md files, hook notes, other plugins) for a live session and names the three largest. A fixture session with a planted 5k-char MCP schema ranks it first.

- **Detect `foreman-ui` anchor drift against each new Claude Code release** — FIX — value 4 — effort S — risk low — category: compat
  Why: Foreman was adapted to 2.1.301 and 2.1.304 is out. T-0418 (the installed mod is stale) and T-1217 (pane background colour) show the mod patching a moving target. The existing compat ideas cover hooks and plugins, not the mod's patch anchors.
  Done when: a script takes a Claude Code version, applies each mod anchor to its bundle, and exits non-zero naming the anchors that no longer match. It is run in CI against a deliberately mutated bundle.

- **Fail loudly when another plugin's hooks fight Foreman's** — FEATURE — value 3 — effort S — risk low — category: doctor
  Why: the 2.1.304 note says at most 12 prompt/agent hooks run at once per event, and users run several plugins. Nothing in the pack lists neighbouring hooks per event or notices a competing Stop blocker.
  Done when: `fm doctor` lists every non-Foreman hook per event with its measured latency. A fixture second plugin that also blocks Stop is reported as a conflict.

- **Pin the Foreman version per repo** — FEATURE — value 3 — effort S — risk low — category: teams
  Why: Foreman releases fast (1.2.36 to 1.2.40 in a short span) and teammates' clones may have different versions. Assumption: the repo can carry a `.foreman/requires` line.
  Done when: with `requires >=1.2.40` committed and 1.2.38 installed, SessionStart prints one line with the update command, and the line disappears after the update.

- **Pull docs for the library version actually installed** — FEATURE — value 3 — effort M — risk med — category: knowledge
  Why: cards exist, and "warn when a library moved a major version" is already an idea, but nothing reads the installed package's own docstrings, types and changelog locally. That would keep the data on the user's machine and avoid stale-API edits. Assumption: stdlib introspection is enough for Python and `.d.ts` for JS.
  Done when: `fm lib docs requests.Session.send` prints the signature and docstring from the installed copy. A fixture with a pinned old version returns that version's signature, not the newest.

- **Add an integrity audit to every benchmark run** — SECURITY — value 4 — effort M — risk low — category: benchmarks
  Why: every site claim must be measured, and the duel already uses hidden tests. Nothing checks that a run didn't read the hidden tests, fetch a solution, or reuse another run's cache. One contaminated pass would undermine the +10%/+14% figures.
  Done when: `fm bench audit RUN` scans the transcripts and fails on a planted read of the hidden-tests path, and a clean run passes. The results file records the audit verdict per run.

- **Ship `--json` on every list verb, plus shell completions** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: assumption: verbs print only human text. The pack has JSON Schemas for files but none for verb output, and the web UI, pane and scripts all re-parse text. Completions can be generated from the per-verb metadata idea.
  Done when: `fm task ls --json | python3 -m json.tool` succeeds for every list verb, and `fm completion bash` completes `fm ta<TAB>` to `task` in a test shell.

- **Bind the Foreman plan to native plan mode** — FEATURE — value 3 — effort M — risk med — category: native integration
  Why: "plan before it edits" is the first promise, and the 2.1.304 `decider: "person"` check is a native approval path. Assumption: the plan is currently a Foreman artifact, not Claude Code's own plan approval.
  Done when: a task of size M or larger cannot be edited until the plan is approved through the native dialog. A headless run refuses with the unblock command.

- **Wild: Plant honeytoken credentials that prove the guard and catch other tools** — SECURITY — value 3 — effort S — risk low — category: tripwire
  Why: the credential-read guard just shipped. Fake `~/.aws/credentials` or `.env` bait files with unique tokens give a visible alarm whenever any agent, plugin or script reads or sends them, which is evidence the guard cannot produce on its own. Wild.
  Done when: `fm canary arm` writes bait files, and a scripted read through a non-Foreman path (guard bypassed) raises an alert naming the process. A read through the guard is blocked and logged.

- **Wild: Ship a booby-trapped demo repo** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: injection defenses are deferred (T-0791, 18 ideas) and the site's strongest result is safety. `fm demo trap` would open a repo with a README injection, a malicious Makefile target and poisoned test output, and show Foreman refusing each live. It doubles as the injection regression corpus and a site clip. Wild.
  Done when: running it against Foreman yields refusals for all planted traps with a printed reason each, and the same repo against bare `claude -p` in the harness is recorded as a comparison row.

- **Wild: Replay your own shell history against the guard before you trust it** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: the claim "0 of 25 everyday commands stopped" is on synthetic commands, and a first-time user's fear is false positives. Running `~/.bash_history` through the guard shows what would have been stopped on their own habits, locally and with nothing sent anywhere. Wild.
  Done when: `fm guard history` prints counts of allowed and stopped commands and lists the stopped ones with reasons. A fixture history with one `rm -rf /` line and 200 normal lines reports exactly 1 stopped.

- **Add a language-fixture matrix for gates and proofs** — FIX — value 3 — effort M — risk low — category: coverage
  Why: the only fixture repo shown is `app.py`, and 1,158 of 1,560 files are skills. Assumption: Go, Rust, TypeScript and Java projects hit untested paths in map, test-to-source mapping and the test sentinel.
  Done when: four tiny fixture repos run through the roundtrip e2e, with `fm map` finding the gates and `fm task prove` working in each. The test fails if any language's gate detection is empty.
