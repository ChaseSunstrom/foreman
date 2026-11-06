# Brainstorm — lens: deepen: guard

- **Keep one guard ledger of every verdict** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: assumption: blocks, allows, unparsed commands and overrides live in separate places. Earlier questions ask which reader gives a wrong answer if a record class is missing. This is the base for most ideas below.
  Done when: every guard call appends one row (harness, command hash, rule id, verdict, parsed yes/no, override yes/no), and `fm doctor` reads counts from it.

- **Replay the ledger against every guard change** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: grows "chaos-month" and "unit-test the rules" into a regression gate. Recent commits show `fm ship` gating on a full suite and a bench, but no verdict-diff gate. Assumption: the ledger above exists.
  Done when: `fm ship` on a guard edit prints each old verdict that flipped and refuses on an unexplained allow-to-block or block-to-allow.

- **Run an unattended red-team loop** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: grows "fuzz with an adversarial agent". Per the standing rule, signals Foreman didn't author come from a tool-less child that never sees the guard code. It tries evasions (quoting, `$IFS`, base64, heredocs, `env -S`, aliases). Each bypass becomes a red-first test.
  Done when: one run files at least N candidate bypasses as failing tests, or reports "0 found" with the attempt count and technique classes tried.

- **Fail closed on the unparseable, in tiers** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: grows "count the commands the guard couldn't parse". Silent allow on a parse failure is the classic hole. Classify each failure (heredoc, process substitution, nested quoting) and show the parse-gap rate in `fm doctor`.
  Done when: an unparseable command in bypass mode gets a named tier (ask, block or allow-with-note), and the doctor line lists the top three gap classes.

- **Preview what a block would have done** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: merges "safe alternative", "plain words" and "what I almost did". On a block or override, show the effect (`rm -rf` lists the files, `git push --force` shows the commits lost) and offer the safer equivalent in one line. Assumption: the common blocked commands are few enough to hand-write previews.
  Done when: the 10 most-hit rules each print a one-line effect and a safer alternative, and a test pins the text.

- **Record overrides as not-proof, with an expiry** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: answers the open question about who records that an override isn't proof. An override row carries the user's reason, expires after the session or N days, and marks the task's receipt "guard overridden".
  Done when: a finish receipt for a task with an override says so, and an expired override blocks again.

- **Turn repeated workarounds into rule proposals** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: grows "record blocks the user worked around". If the same rule is overridden three times for a similar command, file a task to narrow the rule, with the examples attached. Fewer false blocks keep users from turning the guard off.
  Done when: three similar overrides produce one filed proposal task that quotes them.

- **Probe guard liveness from outside** — FIX — value 4 — effort S — risk low — category: guard
  Why: grows "probe from the timer's environment". Earlier questions ask which gauges Foreman trusts only because it wrote them. A canary harmless-but-blocked command, run hourly from the timer's environment and from each harness, must come back blocked.
  Done when: removing the hook from one harness's config makes `fm doctor` WARN within one probe interval.

- **Test guard parity across harnesses** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: T-0335, T-0336 and T-0337 are blocked, and the standing rule says Foreman isn't Claude-specific. One shared corpus runs through each harness adapter and `fm code`.
  Done when: a matrix of corpus rows against harnesses prints, and a row with different verdicts fails the test.

- **Subtract guard rules by evidence** — CLEAN — value 3 — effort S — risk low — category: guard
  Why: the lean ratchet and the subtract-by-evidence asks already exist. Rule hit counts and override rates would show rules that never fire, or that are mostly overridden.
  Done when: `fm doctor` lists rules with zero hits in 30 days or an override rate above 50%, each with a retire-or-tune suggestion.

- **Wild: run blocked commands in a throwaway overlay** — FEATURE — value 5 — effort L — risk high — category: guard
  Why: wild. Instead of a flat refusal, run the blocked command on a copy-on-write copy of the repo (bwrap or overlayfs), show the real diff, and let the user apply or discard. Assumption: the sandbox tools exist on the user's Arch box.
  Done when: a blocked `rm -rf build/..` reports exactly which files it would remove, and the real tree is byte-identical afterwards.

- **Wild: a Guard Dojo to try to sneak past it** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: wild. A playful local `fm guard dojo` shows a goal ("delete the repo") and lets the user, or a model, craft commands. Wins feed the fuzz corpus and the red-team tests. It also makes the guard something people show others.
  Done when: a dojo bypass attempt that succeeds is saved as a failing test, and one that fails scores a point.

- **Wild: a 100-line shadow guard that must agree** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: wild. This merges "100-line auditable guard" and "second implementation". A tiny deny-list core runs in shadow on every call, and each disagreement with the full guard is logged. Disagreements are free finders of bugs on both sides.
  Done when: the shadow runs on the replay corpus and prints its disagreement list, and the core is at most 100 lines.

- **Share guard packs as tested, signed bundles** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: grows "export policy packs". A pack carries its rules, its example commands and expected verdicts, and installs only if its own examples pass.
  Done when: `fm guard pack install` refuses a pack whose bundled examples fail, and shows a diff of rule changes before accepting.

Next question: Which commands has the guard allowed that the user later undid by hand (git reflog, restored files), and can Foreman find them without reading shell history?
Next question: If a model is told it is being guarded, does its behavior change in ways the guard's own ledger can't see?
