# Brainstorm — lens: docs against code

- **Compile spec examples into runnable criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the request names this directly, and "meaning" is the largest unproven class (599). Each `input → output` or "e.g. `fm x` prints Y" block in a spec or MASTER section would become a table-driven check filed with the task.
  Done when: a spec with 3 example lines yields 3 generated checks at `fm plan`. A block the parser can't read is listed as `unproven: <line>` and never silently dropped.

- **Give every absolute doc claim an id and a proof status** — FEATURE — value 5 — effort L — risk med — category: claim ledger
  Why: 421 docs flag claims no run has checked. Sentences with "always, never, every, default, only" would get a stable id (content hash) and a status of proven (command and sha), unproven, or stale. They would be indexed in one `fm claims` listing, not scattered across the docs.
  Done when: `fm claims --json` lists each absolute sentence in README and MASTER with a status. Editing the sentence resets it to unproven.

- **Fail the ship gate on machine or vendor names in public surfaces** — SECURITY — value 4 — effort S — risk low — category: public surface
  Why: the user was pushed back twice ("don't show jarvis", "any orchestrator"). The scan would cover site HTML, README, SVG text and `<title>`/alt text, the generated Genesis JSON, and demo captions. It would match a deny-list of hostnames, home paths, endpoint profile names and "Claude as the orchestrator" phrasing.
  Done when: planting `jarvis` in a site SVG `<text>` makes the gate fail, naming the file and line. The allowlist is only the role vocabulary (planner, judge, router, embedder).

- **Render model roles from one role table, not hand-typed names** — CLEAN — value 4 — effort M — risk low — category: docs/code single source
  Why: scene copy, README and site text each name models themselves, which is how "jarvis" and "Claude plans" leaked. Docs would write `{role:judge}` and the build would fill it from one table that maps roles to any agent.
  Done when: grepping the built site for a model or vendor name outside the table's "examples" page finds nothing. Changing a role label in the table changes every page.

- **Template every number in docs from the command that produces it** — FIX — value 3 — effort M — risk low — category: doc drift
  Why: the README quotes counts (2358 files, 1396 skills, "Claude Code 2.1.301") that rot. Literals would become `{{fm map --count}}` fill-ins, and a lint would reject bare digits next to counted nouns.
  Done when: adding a file changes the rendered README count without a doc edit. A literal "2358 files" fails the lint.

- **Flag code surface that no doc mentions** — FEATURE — value 4 — effort M — risk low — category: reverse drift
  Why: other ideas check doc→code. This runs code→doc over argparse flags, env vars (`SAMPO_*`), exit codes and hook names, listing the ones absent from MASTER.md and `--help` prose. A missing doc line means the behaviour is unproven by definition.
  Done when: the report lists every flag with no doc hit. Adding its doc line removes it, and a flag marked internal is exempt.

- **Resolve renamed-path residue in docs** — FIX — value 3 — effort S — risk low — category: rename hygiene
  Why: the dropped cold-read item shows docs still naming `fm*.py` paths that became shims in `plugin/lib/sampo/` (T-2748). Every path and module in docs must resolve, and a path that resolves only to a shim is reported with its canonical target.
  Done when: running it over MASTER.md returns zero unresolved paths, and the shim-pointing ones are listed with canonical replacements.

- **Pin host-behaviour claims to a host version and recheck on upgrade** — FEATURE — value 4 — effort M — risk med — category: host drift
  Why: T-0335, T-0336 and T-0337 are blocked on unverified Codex, Gemini and opencode behaviour. A doc line about what a host does would carry `host: codex@x.y`, and `fm doctor` would mark it unproven after the host version changes.
  Done when: bumping a faked host version string turns the pinned claims to `stale: host changed`. Claims that were never verified on that host show `unproven`.

- **Verify CHANGELOG entries against their commits** — FIX — value 3 — effort S — risk low — category: changelog truth
  Why: the user asks to ship the batch with the CHANGELOG. Each "FIX:" line must point to a commit that adds a test failing on its parent, which is the revert-replay idea applied per entry. Entries failing that are labelled `unproven fix`.
  Done when: a FIX entry with no red-first test shows `unproven` in the shipped changelog.

- **Mutate doc claims to find ones nothing guards** — FEATURE — value 4 — effort M — risk low — category: doc mutation (wild)
  Why: assumption: flipping a default or count in a copy of a doc, then running the suite and `fm doctor`, exposes claims with no check behind them. Surviving mutants are the true unproven set, and no model is needed.
  Done when: the tool mutates 20 numeric or default claims, reports which mutants survived, and each survivor becomes a claim-ledger entry.

- **Make MASTER.md sections runnable with captured output** — FEATURE — value 4 — effort L — risk med — category: living docs (wild)
  Why: `fm doc run MASTER.md#section` would execute the fenced commands in a scratch home and write the captured output beside the text as a sha-stamped block. A diff against the last capture is a doc-drift finding.
  Done when: one section runs end to end offline, its stored output matches, and breaking a command makes the next run show a diff.

- **Have a docs-only child run the quickstart and score what it had to guess** — FEATURE — value 3 — effort M — risk low — category: cold-read verification (wild)
  Why: assumption: a tool-less child that sees only README and MASTER writes the exact commands it would run. Each command that fails in a scratch home, or that needs a fact the docs lack, becomes a doc bug filed with its quoted line.
  Done when: the run files each divergence as a task, and a command it invented that doesn't exist counts as a doc gap.

- **Resolve reach claims through the call graph** — FIX — value 3 — effort M — risk med — category: capability reach
  Why: the steer says every built capability must be called by a real session path. A doc line saying "the drive does X at session start" should resolve to a path through hook, drive or skill code, or be labelled `unproven reach`.
  Done when: a claim naming a verb that only the CLI calls fails the reach check, and a claim whose path is a hook or `fm next` passes.

Next question: which doc claims has the user corrected by hand after a session, and do those corrections cluster in a doc section no check covers?
Next question: can the public-surface scan tell a user-authored endpoint name from a product word, or does it need a learned allowlist per install?
