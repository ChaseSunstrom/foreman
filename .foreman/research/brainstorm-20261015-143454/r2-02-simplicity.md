# Brainstorm — lens: simplicity

- **Merge lessons, vetoes, decisions and preferences into one standing-rule store** — CLEAN — value 4 — effort L — risk med — category: state
  Why: the pack shows separate stores (lessons, vetoes, decisions.md, preferences) and many open ideas to detect contradictions, rank precedence and retire stale ones. One store with `kind` and `origin_quote` fields removes that reconciliation work. Assumption: the stores overlap enough that a shared schema fits.
  Done when: one `fm rules` file holds all four kinds, old files migrate losslessly, and recall, injection and the guard read only it (test greps for the old readers and finds none).

- **Collapse every escape-hatch flag into one `--because "<reason>"` waiver** — CLEAN — value 3 — effort M — risk med — category: cli surface
  Why: assumption: gates, close warnings and the guard each grew their own skip flag or env var. The pack proposes audited waivers and flag-usage logs but never merges the flags. One waiver form is easier to teach, log and count.
  Done when: `fm doctor` lists exactly one bypass syntax, and every former flag forwards to it and writes a waiver line to the ledger.

- **Fail CI when a tracked file holds local paths or a derived cache** — FIX — value 3 — effort S — risk low — category: repo hygiene
  Why: T-0836 found `skill-index.json` tracked with home paths. Nothing stops the next one, and the repo is public.
  Done when: a test fails on any tracked file that contains `/home/<user>` or a path under the state dir, or that matches the derived-file list, and passes on the current tree.

- **Toggle features by file existence under `.foreman/off/`** — FEATURE — value 3 — effort S — risk low — category: config
  Why: assumption: toggles now live in settings keys, env vars and `fm` verbs. `touch .foreman/off/nudges` can be found with `ls`, committed for a team and reverted with `rm`. It adds no key schema and nothing to explain.
  Done when: creating or removing a file flips that feature in the next hook call, and `fm doctor` lists the active off-files.

- **Ratchet the lib file count and inline single-caller modules** — CLEAN — value 3 — effort M — risk med — category: codebase size
  Why: the map shows 50 lib modules, and the audit suggested ~8k removable lines. A fan-in report is concrete and mechanical, and the ratchet stops regrowth.
  Done when: `fm doctor` prints modules with one importer, a CI test fails if the lib file count rises without a ledger note, and at least three such modules are inlined with the suite green.

- **Make healthy turns add zero bytes, enforced by a golden test** — CLEAN — value 4 — effort M — risk low — category: silence
  Why: the pack proposes "boring mode" and "quiet because" lines, but no test pins the baseline. Replay about 50 recorded ordinary turns (no gate, no ask, no stall) and assert that Foreman's hooks emit nothing.
  Done when: the replay test passes on the current tree and fails when any hook adds a note to a healthy turn.

- **Raise a state-version floor and delete old readers** — CLEAN — value 3 — effort M — risk med — category: migrations
  Why: assumption: migration and compat readers accumulate across versions, and the pack already has version stamps, an upgrade replay and a version-skew doctor check. A floor of "two minors back, upgrade first" lets old code paths go.
  Done when: `fm doctor` offers an in-place upgrade for state below the floor, reader code for versions below it is deleted, and the old-fixture replay still passes for versions at or above the floor.

- **Wild: have the Claude Code release differ open deletion tasks, not only integration tasks** — FEATURE — value 4 — effort M — risk med — category: native overlap
  Why: wild. Many ideas say "adopt the native feature". Their counterpart, "retire the Foreman mechanism it replaces", has no trigger. Each new native tool or hook diffed against Foreman's mechanisms produces a CLEAN task with a bench-parity check.
  Done when: running the differ on two Claude Code versions queues at least one "retire X, native Y covers it" task whose Done-when includes a shadow comparison.

- **Wild: generate a 30-minute reading-order tour and treat unreachable files as delete candidates** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: wild. The repo has 350 files, 73 skills and 50 lib modules. A tour built from the entry points down, ordered by what a contributor needs first, doubles as reachability analysis. Anything the tour can't justify gets listed.
  Done when: `fm tour --source` prints an ordered list that covers the core path in under 30 minutes of reading, plus a separate "not reached" list a human reviews.

- **Wild: distil a minimal verb path from the bench winners** — FEATURE — value 3 — effort L — risk med — category: surface
  Why: wild. Among passing bench runs, find the cheapest ones by distinct `fm` verbs used. Verbs that never appear in any winning run move to labs or hidden help. The user's own words ("super improve", "THE plugin") favour a surface that wins on evidence rather than a feeling of less.
  Done when: a report lists each verb's appearances in winning runs, and at least one verb with zero appearances and zero real-use calls is moved behind `fm help --all`.
