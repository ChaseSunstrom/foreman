# Brainstorm — lens: user value

- **Make hooks and `fm` survive a broken fmcore (self-lockout #2)** — FIX — value 5 — effort M — risk med
  Why: T-0037. A fmcore bug stopped the hook loading the active task, core grants vanished, the fix was refused, and the user had to run `git checkout`. That breaks "I don't have to run the commands". The committed fallback covers only fmguard.
  Done when: a test injects a syntax error into the working fmcore. The hooks then load the active task and its grants from the committed copy, `fm` still runs with a visible warning, and the fix can be applied without user shell commands.

- **Add `fm audit run` for headless read-only lens reviewers** — FEATURE — value 5 — effort L — risk med
  Why: T-0034. Reviewers run in the background, so the agent idle-waits, and their output is huge and saved by hand at the tail.
  Done when: one command runs the five lenses read-only and writes a structured findings file per lens. `fm task done` reads it, and no manual tail-saving is needed.

- **Store audit findings as a compact digest with severity and open/resolved status** — FEATURE — value 4 — effort M — risk low
  Why: reviewer files are huge and the agent copies the tail by hand. Every round also produced real bugs that needed re-review.
  Done when: ingesting a 50 KB reviewer report stores only the verdict and a findings list with severity. Open high-severity findings block done, and resolving one records the commit or evidence.

- **Seed lens briefs with past findings for the touched area** — FEATURE — value 4 — effort M — risk low
  Why: each round's reviewers found security bugs after the agent thought it was done, and the fixes needed re-audits. Assumption: findings cluster by area, such as guard heuristics and sync import.
  Done when: `fm audit prep` on a diff touching fmguard includes the prior findings for that file as a checklist. A test asserts the checklist appears.

- **Add `fm guard why` to explain the last block and suggest a safe alternative** — FEATURE — value 4 — effort S — risk low
  Why: the guard's text heuristics blocked the agent's own legitimate edits (quoted paths, "claude plugin" strings), and the agent worked around them with heredocs.
  Done when: after a block, `fm guard why` prints the matched rule, the category, and either an allowed way to make the change or "needs `fm ask`". A test covers a quoted-path false positive.

- **Generate the rules copies and eval copies from one source** — CLEAN — value 3 — effort M — risk low
  Why: every behaviour change touches MASTER.md, CHANGELOG, the 60-line rules file and the eval copies of the rules. Drift is a known risk.
  Done when: the rules copies are generated from one file. `fm docs` or `fm doctor` fails on any hand-edited divergence, and a rules edit is a one-file change.

- **Pin plugin approvals to source and content hash** — SECURITY — value 3 — effort M — risk med
  Why: T-0036. An approval currently trusts the plugin name, so a changed upstream could be installed under the old yes.
  Done when: changing the source or content hash after approval forces a new `fm ask`. A test covers a swapped source.
