# Brainstorm — lens: self-modification: a toolbelt that learns which found or built tools held up, retires the unused and promotes the reused, measured and reversible

- **Fold a tool's outcome into its held-up score at task close** — FEATURE — value 5 — effort M — risk low — category: toolbelt ledger
  Why: earlier ideas log use events and "score each tool by held-up rate," but none names the join. assumption: `fm task finish` already records re-fixed/reverted/red-after-merge (T-2291's router uses them per lane), so the same signals can be attributed to every tool the task touched.
  Done when: after a task using tool X closes and is later reverted, `fm toolbelt show X` lists held-up 0/1 with the task id, and a task that stayed green shows 1/1.

- **Make retirement a soft move to a trash shelf with a one-command restore** — FEATURE — value 4 — effort S — risk low — category: reversibility
  Why: the steer on measured and reversible self-change; the pack's "Make every install and retirement reversible" idea has no mechanism. assumption: tools live as files plus a registry row.
  Done when: `fm toolbelt retire X` moves its files and registry row to `.fm/toolbelt/trash/`, X no longer resolves, and `fm toolbelt restore X` returns a byte-identical tree.

- **Propose retirement only after N sessions of fit-but-unused, not plain disuse** — FEATURE — value 4 — effort M — risk med — category: retirement
  Why: unused is ambiguous: no relevant work happened vs. the agent ignored it. The capability-miss trigger (T-2270) already fires on misses, so "a miss of X's kind occurred and X wasn't called" is detectable. assumption: miss records carry a kind.
  Done when: a fixture with 5 sessions that had matching misses and no calls proposes retirement; 5 sessions with no matching misses propose nothing.

- **Promote on reuse across tasks, not calls** — FEATURE — value 4 — effort M — risk low — category: promotion
  Why: one task calling a script 40 times is one reuse. The scaffolds from T-2278 make script→skill promotion cheap. assumption: use events carry task ids.
  Done when: a script used by 3 distinct closed tasks gets a promotion proposal (`fm new skill` draft prefilled), and one used 40 times by one task does not.

- **Hold every self-change behind a before/after replay of the miss that caused the tool** — FEATURE — value 5 — effort M — risk med — category: safety
  Why: a promote, retire or update could silently drop the capability it was built for. assumption: each tool stores its originating miss (command + stderr) as a replay case.
  Done when: `fm toolbelt promote X` refuses and prints the failing replay if the original miss no longer passes after the change.

- **Journal every belt change as one revertable entry** — FEATURE — value 4 — effort S — risk low — category: reversibility
  Why: install, build, promote, retire and update each need undo; one journal beats five. assumption: no belt journal exists yet.
  Done when: `fm toolbelt undo` reverts the last N changes in reverse order and `fm doctor` shows an empty diff afterward.

- **Charge decayed footprint to the lean ratchet per shelf tool** — PERFORMANCE — value 3 — effort S — risk low — category: lean
  Why: T-2290-era ratchet tracks rules/descriptions chars, but a shelf of promoted skills grows both. assumption: skill descriptions are always-on.
  Done when: promoting a skill that pushes descriptions chars past the last shipped value warns in `fm doctor` and names the least-held-up shelf tool as the retirement candidate.

- **Detect a tool that holds up only for one model** — FEATURE — value 3 — effort M — risk low — category: scoring
  Why: T-2291 already stores outcomes per model; a tool that fails under the cheap model but passes under the strong one is a description problem, not a bad tool. assumption: use events record the model.
  Done when: the toolbelt report flags a tool with ≥3 uses per model and a held-up gap above 50 points, and suggests rewriting its `--describe`.

- **Self-edit a tool only through a failing-first test from its own failure** — FIX — value 4 — effort M — risk med — category: self-repair
  Why: the standing rule is red-first for every task; a tool that fails in use should file a FIX task seeded with the failing input rather than being patched in place. assumption: the failure is capturable from the tool's exit and stderr.
  Done when: a built tool exiting nonzero creates a task whose first criterion is a test reproducing that input, and the tool file is unchanged until that test is red.

- **Wild: Let two tools covering the same miss run a monthly bake-off on replayed misses** — FEATURE — value 3 — effort L — risk med — category: selection
  Why: wild. Found-vs-built duplicates accumulate; replay cases make a fair score possible. assumption: replays are deterministic enough to compare.
  Done when: for two shelf tools sharing a miss kind, `fm toolbelt bakeoff` prints pass rate, time and footprint per tool and proposes retiring the loser.

- **Wild: Compost a retired tool into a lesson and a replay test** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: wild. Retiring discards what was learned; the pack's lessons system (T-0217) can hold why it died and the miss it served. assumption: lessons accept generated entries.
  Done when: retiring a tool writes a lesson naming its miss, held-up rate and retirement reason, plus its replay case into the exam fixtures.

- **Wild: Run a "belt autopsy" that deletes the whole shelf in a scratch copy and measures what breaks** — PERFORMANCE — value 4 — effort L — risk low — category: ablation
  Why: wild. The only honest evidence a tool matters is that tasks get worse without it; the exam can ablate (earlier idea, "Ablate the shelf in the exam") but not per-tool. assumption: held-out scenarios can run with a tool hidden.
  Done when: `fm toolbelt autopsy` reports, per tool, the scenarios whose outcome changed with it removed, and tools with zero change are flagged as retirement candidates.

- **Show promote/retire proposals as a single weekly card, never auto-applied** — FEATURE — value 3 — effort S — risk low — category: user control
  Why: standing rules keep grants user-owned; self-modification should follow the same line. assumption: the grant queue can carry non-install item types.
  Done when: the card lists each proposal with its evidence line and one-word accept/decline, and declined items are not re-proposed for 30 days.

Next question: Which signals about a tool's success come from something other than the agent that used it (outcome survival, a cold reader, a different model's rerun), so the held-up score can't be gamed by the tool's own author?
Next question: When a built tool is promoted into a shared card, what stops one project's quirks from becoming another project's silent default?
