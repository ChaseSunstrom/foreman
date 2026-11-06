# Brainstorm — lens: user value: what the user would notice and love

- **Lock out the real `claude` in test harnesses** — FIX — value 4 — effort S — risk low — category: safety
  Why: a stub `claude` lost its shebang, PATH fell through to the real one, and $0.42 of sessions ran unasked. Bench and test harnesses that shadow `claude` share the trap.
  Done when: with the harness env flag set, a child spawn that resolves outside the harness dir exits non-zero before any spend, and a test with a broken stub proves it.

- **Auto-run a security pass on ingest/network diffs** — FEATURE — value 5 — effort M — risk low — category: review
  Why: a background review of one just-committed feature found prompt injection, SSRF and terminal escape issues the in-loop reviewer rated MEDIUM/LOW. Every pass finds 3–8 issues, mostly in parsers and untrusted text.
  Done when: a diff that adds `urllib`, `subprocess` or a text parser makes `fm audit prep` require the adversary lens with a security checklist, and a diff that touches none of these doesn't.

- **Run `fm pass N` as a self-improvement loop with a convergence stop** — FEATURE — value 5 — effort L — risk med — category: recursion
  Why: the user asked for "numerous multiple passes" and recursive improvement, which today means manual re-invocation. The loop would chain brainstorm, shortlist, briefs, drive, review and friction.
  Done when: `fm pass 3 --dry-run` prints the planned stages and budget, and a real run stops early when a pass yields fewer than K accepted items.

- **Fold mid-run steers into the brief with a criteria diff** — FEATURE — value 4 — effort M — risk low — category: steering
  Why: the user steers mid-task ("do numerous multiple passes… mid T-0264") and the ledger records "criterion widened/corrected" after the fact.
  Done when: a user message during an active task adds or edits a criterion and prints a before/after diff, and the next `fm next` reflects it.

- **Give claims a half-life in the research store** — FEATURE — value 4 — effort M — risk low — category: research
  Why: the user wants better research. The page cache is per-day and `fm landscape` diffs scans, but no cited claim carries an age or a re-verify trigger.
  Done when: a claim cited in a brief older than its half-life is flagged stale and re-asked on the next `fm research ask`, with the old and new answers shown side by side.

- **Probe new plugins for conflicts at install** — FEATURE — value 4 — effort M — risk low — category: compat
  Why: the user asks for better plugin compat, and `fm bench duel` exists but only runs on request. Assumption: plugins can be diffed by hook events and tool matchers without spend.
  Done when: a SessionStart check finds a plugin new since the last run and prints a static overlap report (shared hook events, rival edit gates, competing routing). `fm bench duel` is suggested only when overlap exists.

- **Draft a skill from a habit the user repeats** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: assumption: the ledger holds repeated phrasings of the same multi-step request, such as the "FEATURE: … DONE-WHEN" shape. Foreman could package those as a skill with a bench case.
  Done when: three similar requests in the ledger make `fm next` offer a drafted skill, and accepting it installs the skill and a passing bench case.

- **Wild: Fuzz Foreman's hooks with synthetic rival plugins** — FEATURE — value 4 — effort L — risk med — category: compat
  Why: the user wants compat with "plugins/skills/whatever". A generated plugin that hooks the same events with conflicting outputs (reorder, double-block, mutate the payload) would find breakage before real ones do. wild.
  Done when: a generated rival set runs through the hook suite and any ordering or output-merge failure is reported with a minimal reproducing plugin.

- **Wild: Coach the user's phrasing with `fm coach`** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: the user's best requests carry a type, a DONE-WHEN and a CONTEXT, and the weakest ones need steers and re-intake. A weekly note comparing phrasings that closed first time with ones that needed rework would show which habits pay. wild.
  Done when: `fm coach` prints three phrasing patterns correlated with first-time close, each with an example from the user's own ledger.

- **Wild: Replay a task as a hindsight brief** — FEATURE — value 3 — effort L — risk med — category: learning
  Why: steered and dropped entries record what was wrong at intake (premise false, criterion widened). A child given only the original request and the final steers would write the brief it should have had, and the gap would train intake. wild.
  Done when: `fm hindsight ID` outputs the corrected brief and a diff against the original, and the missed clauses are recorded as an intake lesson.

- **Wild: Make an offline budget rehearsal** — FEATURE — value 3 — effort M — risk low — category: cost
  Why: the user wants speed and savings without losing quality. Each recorded task has measured token and time bills, so a queue's cost could be predicted from similar finished tasks before any child is spawned. wild.
  Done when: `fm budget rehearse` over a queue prints a predicted spend range, and a later run lands inside that range on a test fixture.
