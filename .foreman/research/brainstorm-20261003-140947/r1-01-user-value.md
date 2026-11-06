# Brainstorm — lens: user value

- **Replay real command corpus against the guard on every change** — FIX — value 5 — effort M — risk low — category: guard
  Why: Most recent friction is guard false positives on Claude's own edit/probe commands, and each fix has exposed a new bypass (heredoc quoting, backticks, `$'…'`, keywords, fake `--run`). Fix-by-fix is whack-a-mole.
  Done when: `fm check` replays a recorded corpus of allowed and blocked commands from the ledger, and a guard change that flips any expected verdict fails the gate with the command named.

- **Record guard false positives with one-line rewrite hints** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: Each block costs Claude a rewrite turn, which the user feels as slowness ("agents using foreman feel slow"). Blocks currently say what's wrong, not the allowed form.
  Done when: every guard block message includes a concrete safe alternative, and a test asserts each category has a non-empty hint.

- **Add a render-conformance snapshot test for every panel kind** — CLEAN — value 4 — effort M — risk low — category: mod UI
  Why: The user has complained about mismatched panels, duplicated dashboard, unpanelled messages, and animation inconsistencies across at least five rounds. The 58 mod tests likely don't pin the visual contract.
  Done when: golden-file tests cover reply, command, edit, diff, prompt, dashboard and band at two widths, and the test fails if any row lacks the border, if the dashboard renders twice, or if an escape sequence leaks.

- **Pre-flight the parallel lane budget before `fm run --parallel`** — PERFORMANCE — value 4 — effort M — risk med — category: parallel
  Why: The user asked that parallel work not cause context, speed, quality or usage problems. Nothing in the pack shows the lane count is checked against estimated tokens or file overlap beyond "disjoint".
  Done when: `fm run --parallel N` prints a lane plan (files, estimated cost, serial fallback reason) and refuses or lowers N when overlap or the budget is exceeded, with a test for each.

- **Mine git history for credential leaks in Foreman-tracked repos** — SECURITY — value 4 — effort M — risk low — category: credentials
  Why: The user asked for credential finding and auditing in repositories and Claude config. `fmsecrets` exists, but the pack doesn't show history or `~/.claude` scanning.
  Done when: `fm secrets audit --history` scans commits plus `~/.claude` files, reports hits as path, commit and rule without echoing the secret, and a seeded fake key in a test repo is found.

- **Make self-improvement passes cite the user's complaint they came from** — FEATURE — value 3 — effort S — risk low — category: RSI
  Why: The user wants real recursive self-improvement, and the last pass found a real bug. Passes mine friction events but there's no link back to what the user actually objected to.
  Done when: each friction digest item carries a source (event, ledger entry or user quote), and items with none are dropped.

- **Show a "what I changed in your repo" ledger on session return** — FEATURE — value 3 — effort S — risk low — category: git tracking
  Why: The user asked for better tracking of Foreman work in git repos. The branch is ahead of main and merging is theirs, but the pack shows no single view of what's unmerged.
  Done when: session start shows commits per task ahead of main with a merge-readiness line, and says nothing if clean.

- **Wild: Run a "user pushback fuzzer" that regenerates past complaints as tests** — FEATURE — value 4 — effort L — risk med — category: regression
  Why: wild. The same complaints recur (panel mismatch, duplicates, bad contrast, unanimated `$`). Turn each verbatim complaint into an assertion that runs in `fm check`.
  Done when: a `complaints/` file maps each quote to a runnable check, and removing a fix makes exactly its check fail.

- **Wild: Add a "second terminal" visual diff bot that screenshots the mod via its own tmux** — FEATURE — value 4 — effort L — risk med — category: mod UI
  Why: wild. A snapshot tool with its own tmux already exists, and the user judges by sight. Capture frames and have Haiku flag misalignment, duplicates and unpanelled text before the user sees them.
  Done when: after a mod change, a frame set is captured and a report lists any detected panel-rule violations, with a seeded defect caught.

- **Wild: Keep a "speed truth" trace showing where agent wall time goes** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: wild. The user said it feels slow but not the hooks (p95 ≈ 30 ms). Time per turn is likely guard rewrites, drive restarts and reloads. Attribute each minute to its cause.
  Done when: `fm speed` outputs a breakdown per task of model time, hook time, guard-rewrite turns, reload turns and gate time, summing to within 5% of wall time.

- **Raise confidence in the standing-yes coverage with a decision-table test** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: The last self-improvement pass found a standing-yes coverage bug, and the pack records two real bypasses found only incidentally.
  Done when: a table of grant × command-shape cases is tested, and every cell where a yes covers more than the plain path it was given fails.
