# Brainstorm — lens: unspoken needs

- **Draft upstream host bug reports from host-blocked tasks** — FEATURE — value 3 — effort S — risk low — category: host
  Why: T-1217 (pane background colour), T-0337 (Gemini AfterAgent discards the answer) and T-0335/36 are blocked on host behaviour. Nobody writes the bug report, so the block stays forever. Assumption: the user would file these if the text were ready.
  Done when: `fm upstream draft T-1217` writes a local markdown file with the version, repro steps, expected and actual behaviour, and sends nothing.

- **Settle each costly self-made decision against later evidence** — FEATURE — value 4 — effort M — risk low — category: decisions
  Why: the standing rule says never block on the user and record the choice with `fm decide --kind costly`. Nothing ever says whether those choices went well. The user will eventually ask whether Foreman's picks were right.
  Done when: `fm decide --settle` pairs a decision older than 14 days with a later outcome or reversal, and the final report lists the three worst-settled first.

- **Snapshot gauges at each generation boundary and diff them mechanically** — FEATURE — value 4 — effort M — risk low — category: genesis
  Why: the cross-cutting cold review reads a diff, exam lines and outcomes by judgement. A zero-token before/after of doctor rows, hook p95, injected characters, verb count and file count would make "what got worse" a fact first.
  Done when: `fm genesis diff gen-2 gen-3` prints per-gauge deltas and flags any that worsened without a matching measured gain.

- **Carry an `Idea:` trailer from catalogue id to commit and answer "why does this exist"** — FEATURE — value 3 — effort S — risk low — category: provenance
  Why: briefs cite ids like c13 and T-2631, but nothing links a shipped commit back to its idea. Later subtraction and lean decisions have no lineage to weigh against.
  Done when: `fm why <commit|verb>` prints the originating idea id, Mission and brainstorm date, or says "no recorded origin".

- **Pre-flight a Mission's brief set for contradictions with standing steers** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the user has already corrected criteria, such as T-2583's 8+ versus 7 characters, and keeps adding steers. A Mission filed in parallel lanes can silently break an older one. Assumption: a keyword and numeric check catches most cases.
  Done when: filing a brief that names a flag or number conflicting with a stored steer prints the steer and refuses until the brief is amended.

- **Report the share of generated work the user could not have predicted from gen-0** — FEATURE — value 2 — effort M — risk med — category: genesis
  Why: the moonshot rule requires novelty, but nothing measures whether ordinary Missions drift outside gen-0 §2. Assumption: gen-0's capability list is text a cold child can match against.
  Done when: each generation report lists every closed task mapped to a §2 capability or tagged "unmapped", with counts.

- **Keep a per-Mission spend envelope visible against the $200 cap** — FEATURE — value 4 — effort S — risk low — category: budget
  Why: the environment shows a hard $200 budget, and `--stall-usd` (T-2669) only watches dollars since the last close. The user will want to see what each remaining Mission may spend before one eats the rest.
  Done when: `fm run` start prints remaining dollars divided over unstarted Missions, and a Mission that passes 150% of its share files a note.

- **Add a lowest-regret default when a decision window times out** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: "never block on the user" means Foreman picks. The pick should be the most reversible option, not simply the most gen-0-consistent. Assumption: options can be ranked by undo cost.
  Done when: a decision card records each option's undo cost, and the chosen default is the cheapest to reverse unless a steer overrides it.

- **Wild: Reply to the final report in advance** — FEATURE — value 3 — effort M — risk low — category: reporting
  Why: wild. A tool-less child reads only the user's steers and drops and predicts the five questions they will ask on reading the end-of-run report. The report must answer them or flag the gaps.
  Done when: the report has a "questions you'll likely ask" section, and later user questions are scored against it.

- **Wild: Hold a monthly "deleted by me" party** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Many ideas are dropped with a recorded reason. A once-a-month card shows the three dropped ideas the user would most likely now regret, with the evidence that has changed since the drop.
  Done when: `fm digest` includes a "revisit?" card with each drop reason and new evidence, or says nothing new.

- **Wild: Leave a replayable "morning after" bundle for each overnight run** — FEATURE — value 3 — effort L — risk med — category: unattended
  Why: wild. The user will review hours of unattended work. One file with the ordered closes, each proof command's output, the stops with reasons and the dollar curve lets them replay the night in five minutes.
  Done when: `fm run` writes `night-<date>.html` that opens offline and lists every task with its proof output.

- **Count the user's repeated corrections per class and promote a class to a standing check at three** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: the user's drops and steers show repeat classes: arithmetic in criteria, "already built" claims, a gauge counted from the wrong source. The sibling sweep is a one-off. A counter that auto-proposes the check ends the repeats.
  Done when: the third correction in one class files a standing rule plus a check, and `fm doctor` lists classes with counts.

Next question: which of Foreman's self-made decisions has the user quietly reversed by hand, and does anything notice?
Next question: when the unattended run ends, what is the first question the user asks that today's final report cannot answer?
