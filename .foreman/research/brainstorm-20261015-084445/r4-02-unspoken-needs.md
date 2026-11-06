# Brainstorm — lens: unspoken needs

Rounds 1-3 and the pile above cover most capabilities, so this round gives one gap and several combinations that are worth more as one thing. I'm assuming the 688 finished tasks are mostly Foreman working on Foreman, which the pack implies but doesn't state.

- **Show where Foreman's effort goes** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: assumption: most of the 688 tasks and 370 weekly closes are Foreman-on-Foreman, so "THE plugin" may be eating the time meant for the user's own products. No ledger view splits work by project.
  Done when: `fm stats --where` prints the share of tasks, tokens and wall time per project, with the Foreman repo's share on its own line. A fixture-ledger test pins the numbers.

- **Replace the install's 20 settings with three named postures** — FEATURE — value 5 — effort M — risk med — category: install
  Why: finding A2 says bypass, outputStyle, autocompact, the statusline wrapper and 20 deny rules arrive as one silent bundle. The pile has lite/standard/strict, earned bypass and observe-only as separate ideas. Together they are one choice for the user: Observe, Guided or Autonomous.
  Done when: `fm posture` shows and switches the active posture, `fm posture --explain` lists each setting it changes, and a clean-HOME install asks once and writes only that posture's settings.

- **Gate every release on a generated proof pack** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the bench has 1 case and no published evidence Foreman helps (C). Held-rate denominators, a repro kit, the newcomer walkthrough and the rival table are separate ideas that need one gate to make them real.
  Done when: the release script refuses to tag without a `proof/` folder. Every number in it must match a ledger query, and the clean-HOME walkthrough result is included.

- **Require external evidence before a recursive round starts** — CLEAN — value 3 — effort S — risk low — category: process
  Why: rounds 2-3 came back nearly dry because they only looked inward, and the user's steer was "recursively improve" from new evidence. The pile has a sweep round and a switch of evidence source, but no hard rule.
  Done when: `fm ideas` refuses a round unless the pack cites at least N external items (new Claude Code release notes, rival releases, the user's own friction). Otherwise it runs a sweep round and says why.

- **Attribute and license-check ported skills** — SECURITY — value 3 — effort S — risk low — category: provenance
  Why: the pack mentions ECC ports and installer-pulled Trail of Bits skills. Nothing records source or license, and the public push and rival survey make attribution matter.
  Done when: `fm doctor` fails if a ported or bundled skill has no source and license line, and a `NOTICE` file is generated from those lines.

- **Tag each verb for the human or the model** — CLEAN — value 3 — effort M — risk low — category: developer experience
  Why: `fm --help` is 231 lines and 16 KB (A4), and the model reads help too. The human needs the front door and the model needs exact flags, so one help surface serves neither.
  Done when: every verb in the registry carries an audience tag. `fm help` shows only human verbs, `fm help --model` prints a compact flag table, and a test fails on an untagged verb.

- **Teach the model the refused-then-retried pattern** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: finding A9 says `fm task done` refuses with 4 bullets and a newcomer, or the model, burns turns finding `fm task finish`. A prefilled retry command would save those turns.
  Done when: each refusal ends with one copy-ready command built from the current task, and a test checks that the command parses and succeeds on a fixture.

- **Get the ledger's folded tasks counted once in the weekly view** — FIX — value 3 — effort S — risk low — category: user value
  Why: 159 of 370 weekly closes show as "ungraded" because they were folded into other tasks. That undercounts how well Foreman is doing and weakens any proof claim.
  Done when: `fm digest` credits a folded task to its parent's grade and shows zero ungraded for a fixture with folds.

- **Wild: Certify third-party plugins with `fm conform`** — FEATURE — value 4 — effort M — risk med — category: ecosystem
  Why: wild. Rival plugins complain about hook conflicts (B). A conformance run would check a plugin's hooks against Foreman's guard and injection budget, plus its skill-name collisions, and give the author a badge. That makes Foreman the neutral referee rather than one more plugin.
  Done when: `fm conform <plugin-dir>` prints a pass/fail report on three checks (deny override, injected bytes, name collisions). It runs against a seeded hostile fixture plugin and reports the failures.

- **Wild: Write a maintainer handoff packet** — FEATURE — value 3 — effort M — risk low — category: continuity
  Why: wild. This is 28k lines with a single visible maintainer, and several open tasks wait on human-only chores (T-0325 sudo, T-0352 publish, T-0418, T-0431). A generated packet would hold the architecture postcard, load-bearing decisions, secrets and chores a successor needs, and the unfinished releases.
  Done when: `fm handoff` writes one markdown file that a cold child, given only that file, answers five seeded questions from correctly.

- **Wild: Hold a weekly "outside-only" day** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. Pair the effort ledger with a playful rule: one day a week, Foreman declines Foreman-on-Foreman tasks and works only on the user's other projects. The goal is to feel where it actually helps.
  Done when: with `fm outside-day on`, capturing a task in the Foreman repo is parked with a one-line reason, and the day's receipt lists what shipped elsewhere.

- **Say "nothing changed for you" when a round changes no behaviour** — FEATURE — value 2 — effort S — risk low — category: transparency
  Why: round 2-3 findings were mostly internal polish, and the user's "keep going" suggests they can't tell what each round changes.
  Done when: `fm round close` prints either three lines of user-visible changes or "nothing visible changed", decided by diffing `fm help` and the hook output on the fixture.
