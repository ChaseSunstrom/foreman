# Brainstorm — lens: deepen: guard

- **Build a guard verdict corpus that every surface replays** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: the list repeats "replay logged decisions" and "deny-class matrix" as separate ideas. Merge them: one file of (input, surface, expected verdict) rows drawn from the 42 `interpreter-code-driving-foreman` blocks, the 2 brief-guard false positives, and child-written evasions. Claude Code, fm code, Codex, Gemini, opencode and MCP all run it.
  Done when: `fm guard corpus --surface all` prints a per-surface pass table, and deleting any one rule in a copy turns at least one row red.

- **Replace the brief guard's path regex with a shell tokenizer, pinned by the false-positive pair** — FIX — value 5 — effort S — risk low — category: guard
  Why: the pack's measured section says two brief-guard false positives read a dict key and a `.join(` call as written paths. Almost every earlier idea starts here.
  Done when: both false positives become corpus rows that allow, a mirrored evasion row for each still blocks, and a differential test against a real `bash` parse shows no disagreement on 500 generated commands.

- **Make every block a three-part receipt: rule, why, safe command** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: 42 blocks in 7 days on one rule means the model keeps retrying the same thing. A block that names the safe alternative should cut repeats. The same text can quote the user steer that created the rule.
  Done when: each deny rule has a non-empty `safe_alternative`, and `fm outcomes` shows the repeat-block rate falling over 7 days.

- **Turn the top repeated block into a pre-emptive hint** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: assumption: the 42 blocks are mostly one habit. A one-line note in the SessionStart text (which is already ~2k chars) would replace a block and a retry. Pay for it by trimming other lines, since injected context may not grow.
  Done when: the net SessionStart size is not larger, and that rule's 7-day block count drops.

- **Measure each rule's precision from what follows a block** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: today the false positives are found by hand. After a block, check whether the user approved the same action, whether the agent worked around it, and whether the task later failed. Rank the rules by likely false-positive rate.
  Done when: `fm guard rules` lists each rule with fired/overridden/evaded counts and a precision estimate.

- **Add a scoped, expiring release valve that the guard itself mints** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: bypass mode plus a hard "no" pushes users toward disabling the guard whole. A one-shot allow for one exact command, minted via `fm ask`, expiring in 10 minutes and logged, keeps the guard on. The model cannot mint it.
  Done when: an allow works once for the exact command only, expires, appears in the final report, and an attempt by the agent to create it is itself blocked.

- **Print a guard parity matrix at session start and in `fm doctor`** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: Gemini's Stop hook isn't wired (T-0337) and grants on Codex, Gemini and opencode are blocked (T-0335), so coverage differs by harness. The user should see "unguarded: X" instead of assuming.
  Done when: `fm doctor` shows rule × harness as enforced, advisory or none, and a test fails if a harness's entry disagrees with its corpus result.

- **Fuzz and mutate the guard on a schedule, inside `fm night`** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the tick already runs unattended. Each night, delete one rule in a copy (a surviving mutant means a gap) and feed the parser pathological and Unicode input (a crash must fail closed).
  Done when: the nightly digest lists mutants that survived and any fuzz input that crashed or allowed, each filed as a task.

- **Lint the permission and guard rules for shadowing, conflicts and typo'd keys** — CLEAN — value 3 — effort S — risk low — category: guard
  Why: several ideas point at settings typos and rule overlap. A static pass is cheap and needs no model.
  Done when: `fm doctor` reports an unknown key or a rule that can never fire, and a seeded typo in a test fixture is caught.

- **Wild: Run an N-version shadow guard written by a cold child** — SECURITY — value 3 — effort L — risk med — category: guard
  Why: wild. A tool-less child writes its own deny rules from gen-0 alone, never seeing the real ones. The two run side by side and any disagreement is logged. It follows the steer that signals must come from something Foreman didn't author.
  Done when: a week of real hook inputs yields a disagreement report, and each disagreement is classified as a real gap or a false positive.

- **Wild: Plant a harmless forbidden command weekly as a liveness canary** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: wild. A hook that has silently stopped, for example after a host CLI update, looks identical to a quiet week. A canary like `echo` wrapped in a known deny pattern should be blocked every time.
  Done when: the canary runs at session start and weekly, and a disabled hook turns `fm doctor` red within one run.

- **Wild: Hostile-session replay with a red-team child** — SECURITY — value 4 — effort L — risk med — category: guard
  Why: wild. After each block, a child that sees only the block message tries to reach the same effect by other means: base64, an `env` prefix, a script file. Every success becomes a corpus row and a rule task. This is "detect evasion" turned into a producer of tests.
  Done when: one run adds at least one evasion row, or reports zero across N attempts.

- **Wild: Make the guard's "no" quote the user's own steer** — FEATURE — value 2 — effort S — risk low — category: guard
  Why: wild. Blocks tied to a dated user steer, such as the 2026-10-30 push grant, read as the user's rule rather than the tool's. It also shows which rules have no steer and may be stale.
  Done when: each block names its steer date or "built-in", and `fm guard rules` lists rules with no source.

- **Track untrusted text into the guard's decisions** — SECURITY — value 4 — effort L — risk high — category: guard
  Why: T-0791 (injection and supply-chain defenses) is deferred. Mark commands that follow fetched web or file content and apply a stricter tier, tying into "flag the lethal trifecta at session start".
  Done when: a command whose argument came from a fetched page gets the stricter verdict in a test, and the same command typed by the user does not.

Next question: Which guard rules are advisory rather than enforced on Codex, Gemini and opencode today, and does the user know?
Next question: Is a guard that never fires in a week alive and well, or silent, and what would tell the two apart without a planted command?
