# Brainstorm — lens: blind spots

**Answers to earlier questions, through this lens**
- *Which repeated follow-ups have no trigger?* The satellite asks. Every genesis capability (T-2093 to T-2113) produced the same follow-ups: a check, a step, an exam, a seal, a site page and a skill. Idea 1 makes that a trigger.
- *Who audits the hidden keys?* Idea 3 pre-registers the pass rule, and idea 9 guards the keys against leakage.

**Ideas**

- **Scaffold a capability's satellite tasks when it is filed** — FEATURE — value 5 — effort M — risk low — category: process
  Why: the pack's misses are one pattern asked eight times: `check` (T-2093), `step` (T-2095), `draft/spec` (T-2099), `select/seed` (T-2102), `drift/sweep` (T-2104), `propose` + skill (T-2105), `exam` (T-2112) and `seal` (T-2113). Mission 3 will draw the same follow-ups.
  Done when: filing "fm find" queues stubs for check, step, exam, seal, site page, skill and doctor probe, each with a dedupe key, and the `fm find` fixture shows 7 stubs once, not twice.

- **Reflow every text parser's fixtures before trusting it** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2114 shows a seed quote across a wrapped bullet scored "didn't count" because the matcher read physical lines. Other Foreman matchers likely share the assumption. Line-wrap sensitivity is also a bug class to hunt in user repos.
  Done when: a test rewraps each parser fixture at widths 40, 72 and 120, with CRLF and tabs, and fails on any changed result. The parser it first breaks gets fixed.

- **Run the suite under hostile ambient values** — FIX — value 4 — effort M — risk low — category: flake finder
  Why: the first ask in the pack is `test_ship` failing when a commit hash ends in "add" (substring match on "add a"). Hashes, temp paths with spaces, PIDs, TZ and usernames are all unpinned inputs.
  Done when: a flake mode forces a commit hash containing "add" and "fix", a path with a space, and TZ=Pacific/Kiritimati. It reproduces the `test_ship` failure on the old code and passes after the fix.

- **Pre-register the exam's pass rule in a sealed file** — SECURITY — value 4 — effort S — risk low — category: exam integrity
  Why: T-2113 sealed gen-0, but nothing seals the metric. A rule picked after seeing `none` and `bug` scores can be tuned. The Mission 3 grade names `none` and `bug` in never-seen repos.
  Done when: `fm exam` refuses to score unless `rule.sha256` was written before the run's first arm started, and editing the rule afterwards makes `fm genesis drift` fail.

- **Record what each head-to-head arm was given and refuse unequal pairs** — FIX — value 4 — effort S — risk low — category: fairness
  Why: T-2112 had to be re-asked to score "on what each arm was given". The critique says plain Claude matches Foreman's score at about 0.17 USD, so any hidden advantage skews the comparison.
  Done when: each arm's prompt, tool list and file view are hashed into `exam.jsonl`, and a pair whose manifests differ beyond the declared delta is marked invalid.

- **List every unasked actor and give one off switch** — SECURITY — value 4 — effort M — risk low — category: consent
  Why: the night queue job, scout, adopt, genesis live publish (a standing grant pushing to main) and the proposed initiative all act unasked. The pack's open question asks what a never-typed-`fm genesis` user does when a proposal appears.
  Done when: `fm autonomy` lists each trigger with its grant source, last fire and next fire. `fm autonomy off --all` disables them, and a test confirms nothing fires afterwards.

- **Grid the stack × defect kind and validate it like coverage.md** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the exam spans 6 languages and 11 kinds, and the genesis `check` pattern (a grid plus a not-yet ledger) already worked. Foreman found 0 of 108 planted defects with no map of which cells it covers.
  Done when: `fm find check` exits non-zero for any cell that has neither exam evidence nor a not-yet entry with a reason.

- **Route each stack and kind to the cheapest arm that held score** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: plain Claude gets 3/3 on held-out bugs at about 0.17 USD, and Foreman's session costs more for the same score. The data to choose is already in `exam.jsonl`.
  Done when: given a fixture `exam.jsonl`, the router picks the plain arm for a cell where plain tied at lower cost, and the finder-led arm only where it scored strictly higher.

- **Fence the bug class with a generated lint rule beside every fix** — FEATURE — value 3 — effort M — risk med — category: prevention
  Why: assumption: a proven finding teaches a pattern that a sibling edit can bring back. A cheap regex or ast-grep rule stops that without another model call.
  Done when: a fix lane ends with a rule file that matches the pre-fix code, does not match the post-fix tree, and runs in gates.

- **Bootstrap a missing toolchain in a throwaway prefix** — FEATURE — value 3 — effort M — risk med — category: missing-tool
  Why: `missing-tool` is an exam kind, and "cannot prove here" is the only current answer. Assumption: many never-seen repos only lack pytest, cargo or similar.
  Done when: with the tool absent, Foreman prints the exact install plan, asks, installs under a temp prefix only, runs the proof, and leaves no change to system paths.

- **Hibernate a repo that has proven clean and wake it on outside events** — PERFORMANCE — value 3 — effort M — risk low — category: dry vs finished
  Why: the pack asks what separates "finished" from "queue dry" besides the gap map. Assumption: a clean verdict plus canary recall above a floor is the evidence for finished.
  Done when: after a clean verdict the scan interval backs off. A new advisory on a locked dependency, or a push by someone else, schedules a scan within one cycle.

- **Wild: Watch the shell for the third identical failing command and offer to take it** — FEATURE — value 3 — effort M — risk med — category: unspoken needs
  Why: wild. The user's need is "someone fix the thing I keep re-running". It stays local, offers instead of acting, and shows a failing-test proof first.
  Done when: running the same failing command three times prints one offer line, and `n` suppresses it for that command for a week.

- **Wild: Find tests that can't tell equivalent rewrites apart** — FEATURE — value 3 — effort L — risk med — category: finder
  Why: wild. In idle time it rewrites a hot function three behaviour-changing-but-plausible ways and reports the rewrites the suite cannot detect. Each one is an untested behaviour with a ready failing test.
  Done when: on a planted fixture, the report names the one mutation that survives and emits a test that is red on that mutant and green on the original.

- **Wild: Defect weather in the status line** — FEATURE — value 2 — effort M — risk low — category: ui
  Why: wild. Churn × untested × past findings per module gives a one-glyph forecast ("tests thin near `fmeco.py`"), without spending a model call.
  Done when: the glance line shows the top module's glyph, and the value is reproducible from the journal alone.

- **Scan finder code for exam literals and alarm on own-repo overfit** — SECURITY — value 4 — effort S — risk low — category: leakage
  Why: Mission 3 is graded off Foreman's own repo, where the dev loop runs. Assumption: literals and paths from scenarios drift into probe code.
  Done when: a gate fails if any finder source contains a held-out scenario's identifiers. The exam report flags own-repo vs held-out score gaps above a set margin.

Next question: Which of the eight satellite asks does each new capability need, and can the scaffold list be learned from the journal instead of written by hand?
Next question: What does a wrong "none" cost the user, and does the exam price a missed bug against a false alarm the same way?
