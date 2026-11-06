# Brainstorm — lens: bold bets

Past round three the remaining ideas are mostly marginal. These six are the ones I think would still change outcomes, best first.

- **Build a private benchmark from the repo's own fix commits** — FEATURE — value 5 — effort L — risk med
  Why: A/B tests, `fm whatif` and verdict taps all depend on the user's opinions or on the model's own claims. Git history holds ground truth: a fix commit plus its test. Foreman could check out the parent, hide the fix, and replay the request under a candidate rule set or model. Tokens, turns and pass/fail would then be objective. Assumption: the repo has at least ~20 fix commits with tests.
  Done when: `fm bench --build` produces ≥5 replayable cases from git history, and `fm bench run` scores a rule change with pass rate and tokens per case.

- **Track taint from untrusted content and gate egress** — SECURITY — value 5 — effort M — risk med
  Why: instruction-like text is currently only marked as data. Nothing stops a command run after a WebFetch or an unfamiliar file read from sending local files out. PostToolUse would set a taint flag. For N turns afterwards, PreToolUse would ask yes/no before any network-capable command (`curl -d`, `git push` to a non-project remote, `pip install` from a URL). The remote allowlist would be learned from `.git/config`.
  Done when: a test replays "read tainted file → `curl -d @.env`" and gets a denial, while a normal `git push origin` is unaffected.

- **Run variant analysis after each FIX** — FEATURE — value 4 — effort M — risk low
  Why: the loop records a lesson and a red→green proof, but never asks where else the same bug pattern lives. It would derive a regex or `ast` pattern from the fixed hunk, scan the repo, and queue each hit as a scoped brief. Assumption: most fixes have a matchable shape.
  Done when: after a fix such as an unchecked `dict[key]`, `fm task done` lists N other matches as queued briefs, or says "none found".

- **Fuzz old against new for changed pure functions** — FEATURE — value 4 — effort M — risk med
  Why: the CLEAN behaviour lock relies on existing tests or snapshots. Where a changed Python function has type annotations, a stdlib generator can feed random inputs to both the HEAD and working versions and compare outputs. That catches behaviour drift that no test covers. It is limited to functions with no I/O.
  Done when: a seeded refactor that changes edge-case behaviour is caught with a minimal counterexample, and a true refactor passes silently.

- **Add `fm climb` for metric-ratchet optimization** — FEATURE — value 4 — effort M — risk med
  Why: "make it faster/smaller" requests currently get one attempt plus before/after numbers. A loop would propose a change, measure it, keep it if the metric improved and the gates pass, and revert otherwise. It would stop at a spend cap or after K dry rounds. Applies to PERF, bundle size, flake rate and gate time.
  Done when: a fixture with a slow function reaches a lower measured time in ≤N iterations, and every rejected candidate is reverted byte-for-byte.

- **Compile lessons and corrections into executable checks** — CLEAN — value 3 — effort M — risk med
  Why: tripwires only emit notes on edits, and notes get ignored or pruned. A lesson that has fired ≥2 times could be promoted into a mechanical `fm check` rule (pattern plus path scope) that fails instead of nagging. It would be retired if it produces false positives. Assumption: about a third of lessons are patternable.
  Done when: a promoted rule fails `fm check` on a seeded violation, and `fm doctor` lists rules with their hit and false-positive counts.
