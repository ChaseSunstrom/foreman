# Brainstorm — lens: user value: what the user would notice and love

- **Park the reviewer instead of waiting on it** — FIX — value 5 — effort M — risk med — category: drive speed
  Why: 31 drive turns ended only to wait on a background reviewer, about a minute idle per task. The user's PERF steer asked for speed without losing quality. Prior ideas covered the wait as a state; this goes further: the drive starts the next independent queue item in a lane while the review runs, and folds findings back into the earlier task when they land.
  Done when: a two-task queue test shows task 2's first edit timestamp is before task 1's review verdict, and a finding on task 1 reopens it with its criteria intact.

- **Teach the guard to read python heredocs as text edits** — FIX — value 4 — effort M — risk med — category: guard precision
  Why: 4 false blocks on python heredocs that edit plugin/lib files, where a replacement string mentioned `import fmX`. The constraint is that the guard is only made more precise. Parse the heredoc (AST) and block only real imports or exec, not string literals.
  Done when: replay cases for the 4 blocked commands are allowed, and a heredoc that really imports and runs fmguard is still blocked.

- **Auto-run a security pass on diffs that ingest text** — SECURITY — value 5 — effort M — risk low — category: review
  Why: a background review of a just-committed feature found prompt injection, SSRF and terminal escape issues that the in-loop reviewer graded MEDIUM/LOW. Most review findings were untrusted text reaching prompts or the terminal. Route to the security lens when the diff touches network, subprocess, or prompt-building code. Assumption: this is distinct from the "trigger from what the diff touches" idea, in that it also re-grades severity upward.
  Done when: a fixture diff adding an unsanitised fetch triggers the security lens and the finding is graded at least HIGH.

- **Make the stub-`claude` trap impossible** — FIX — value 4 — effort S — risk low — category: test safety
  Why: a stub without a shebang fell through PATH to the real `claude` and spent $0.42. Give test and bench helpers one `fake_claude()` that writes a validated stub and sets an env tripwire the real binary path refuses, with spend counted as a failure.
  Done when: a test that shadows `claude` with a broken stub fails loudly and records $0 spend.

- **Show "what you can stop worrying about" at session start** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user keeps asking for savings without lost quality and for fewer small fixes. Each session opens with three lines: gates that passed untouched, risks stopped last time, and what needs the user. Assumption: the existing "since you left" card idea does not cover reassurance and risk.
  Done when: the card renders from a fixture ledger with all three lines, and stays silent when there is nothing to say.

- **Let the user rate a pass in one word, and carry it forward** — FEATURE — value 3 — effort S — risk low — category: feedback loop
  Why: the user asks for numerous recursive passes. A cheap grade per pass (kept, noisy, wrong direction) tells the next pass what to skip. Assumption: the grade is stored as data and feeds the shortlist's dedup.
  Done when: `fm pass grade noisy` changes the next pass's context pack to name the downweighted categories.

- **Wild: Ship a "two-hour autopilot" proposal** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: wild; the open inbox has "night shift" unscoped. The user wants things done while they are away. Foreman reads the queue and the budget, then offers a signed plan listing tasks, a cost ceiling, and what it will refuse, and the user approves once. Everything stays inside the existing guard.
  Done when: approving a plan runs the queue within the ceiling, stops at the first unapproved category, and leaves a one-page report.

- **Wild: Let Foreman answer "what's the best thing I could ask next?"** — FEATURE — value 4 — effort M — risk low — category: initiative
  Why: wild; the user's words push toward ideas they haven't had. Combine friction, landscape diff, open inbox and recent drops into three ranked suggestions, each with a one-line expected payoff and a prefilled brief.
  Done when: `fm suggest` prints three suggestions with prefilled `fm task new` commands that run without edits.

- **Wild: Give each pass a changelog the user can skim in 30 seconds** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: wild; many features shipped daily, and the user can't hold them all in mind. A generated page lists "now you can…" lines with the one command to try each, and flags anything unused for a week as a candidate for cutting.
  Done when: the page lists every task closed in the pass with a runnable example, and a verbatim command from it executes cleanly in a test.

- **Wild: Run a blind taste test between Foreman builds** — FEATURE — value 3 — effort M — risk low — category: self-improvement
  Why: wild; the user wants Foreman to improve itself recursively and prefers evidence. Present two anonymised outputs for the same task, one from the old build and one from the new, for the user to pick between. Their picks feed the preference rubric in bench court.
  Done when: `fm bench taste` shows an unlabelled pair, records the pick, and the judge's agreement rate with the user's picks is reported.

- **Cut or merge inbox items into pipelines** — CLEAN — value 3 — effort S — risk low — category: scope
  Why: the pack asks whether any open items should be cut. Suggest merging "lesson confidence" into reviewer memory, and folding "stranger test" with "Foreman MCP server" into one external-use check. Hunk proof for untracked files stays standalone.
  Done when: the inbox lists four items instead of six, each merge or cut with a recorded reason.
