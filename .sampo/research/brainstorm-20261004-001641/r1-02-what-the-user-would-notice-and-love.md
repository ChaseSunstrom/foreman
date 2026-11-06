# Brainstorm — lens: what the user would notice and love

- **Fork interpretations to measure ambiguity before planning** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the user's recurring corrections and "steered" edits suggest misread intent is a main source of rework; nothing in the list measures ambiguity. Idea: at capture, two no-tool `claude -p` children each write a 3-line interpretation of the request plus the repo map. If the key nouns or files diverge past a threshold, ask the one disambiguating yes/no and otherwise proceed silently. Assumption: a divergence signal beats asking every time.
  Done when: replaying 5 bench cases whose original request was later corrected flags ≥3 as ambiguous, while the 8 clean cases flag ≤1.

- **Neutralize foreign orchestration so conflicting skills become usable** — FEATURE — value 5 — effort M — risk med — category: compat
  Why: ECC, superpowers, feature-dev and ralph-loop are disabled for conflicts (the pack lists this in MASTER.md §7). Existing ideas only route, port or detect conflicts. Idea: when a skill from KNOWN_CONFLICTS is invoked, a PostToolUse(Skill) hook scans its body for orchestration verbs (todo lists, "write plan file", "commit now", "brainstorm first") and injects one mapping line, e.g. "plan → fm task plan; commit → task done". Assumption: the Skill tool call is visible to hooks.
  Done when: with superpowers' TDD skill enabled, a bench case completes with no second plan file and no direct commit, and the mapping note appears once.

- **Give decisions machine-checkable revisit triggers** — FEATURE — value 3 — effort M — risk low — category: memory — wild
  Why: `fm decide` records exist, and the idea list has only "turn decisions into invariants", not decisions that expire. A decision gets `revisit-when:` conditions (dependency ≥ version, file > N lines, test count, date). SessionStart surfaces a decision only when its trigger fires.
  Done when: a decision with `revisit-when: lines(fmcli.py) > 1900` surfaces at the next session start and not before.

- **Tour the diff in dependency order for the user's review** — FEATURE — value 4 — effort M — risk low — category: review UX
  Why: the user reviews unattended queue work, and the dashboard shows lists rather than reading order. Idea: at done, a panel orders hunks from definitions to callers to tests (using the `fm map` links), gives each a one-line why, and lets the user tick them off. Skipped hunks remain visible.
  Done when: for a 5-file diff, the `fm review tour --json` order places every definition before its callers, and the panel shows the check state.

- **Re-run affected tests when the user hand-edits a file** — FEATURE — value 3 — effort S — risk low — category: sentinel
  Why: the edit-time test sentinel exists but covers only Claude's edits. `fm watch` plus the mtime-based attribution already detects outside edits. Report a failure only for edits made outside Claude, with a one-line "this broke X".
  Done when: touching a source file by hand in a fixture repo produces one note naming the newly failing test within 10 s.

- **Compile example inputs and outputs in a request into the test** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: users paste "given X it should print Y" with the request, and today the acceptance criteria are re-typed by the model. Idea: extract code-fenced example pairs at capture and emit them as a literal table test in criterion 1, red before the code and green after. Assumption: this is common in the user's requests.
  Done when: a request containing an I/O example yields a failing test at plan time that passes after the fix.

- **Prove the gates' value with a bench ablation card** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: the user is usage-sensitive and will ask whether the ceremony is worth it. Replay bench cases with each gate disabled (leave-one-out) and show "gate X would have let N of 8 bad results through, at the cost of Y tokens". The card is built from existing `fm bench` runs.
  Done when: `fm bench ablate --gates` prints a per-gate catches-versus-cost table from stored runs without a new live run.

- **Watch the live transcript with a cheap observer that whispers** — FEATURE — value 4 — effort L — risk high — category: guidance — wild
  Why: `fm next` hints can be ignored, and the 21 drive stops show waiting patterns the main thread doesn't notice. A Haiku child reads the last N tool events every few turns and emits at most one line, only when it sees repeated failure, a ruled-out approach, or a lesson that applies. Silent otherwise.
  Done when: replaying a recorded thrash session yields exactly one whisper before the third failure, and a clean session yields none.

- **Bundle a re-runnable proof pack with each PR** — FEATURE — value 3 — effort M — risk med — category: trust — wild
  Why: evidence currently lives only in Foreman state. Export the criteria, verify commands, the pinned commit and the red-to-green logs as one `proof.md` plus a script a reviewer can run. This sits behind the existing outward-facing yes.
  Done when: running the script in a fresh checkout reproduces the recorded pass or fail for every criterion.

- **Watch dependency releases and pre-research the migration** — FEATURE — value 3 — effort M — risk low — category: research — wild
  Why: `fm research ask` and the stale-note marking exist, but nothing is proactive about libraries. On a manifest version bump or an upstream release, run research ask for breaking changes and file one queued brief with quoted claims. Assumption: only public registries are fetched, per the public-https rule.
  Done when: bumping a pinned dependency in a fixture produces one research note with ✓-marked quotes and one queued brief.
