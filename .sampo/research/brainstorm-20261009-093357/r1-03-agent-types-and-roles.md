# Brainstorm — lens: agent types and roles

- **Re-plan mid-flight when a surprise lands** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: the pack shows a plan made at intake and "3 failed attempts → block with diagnosis", but nothing in between revises the remaining steps when a step's assumption turns out false. Assumption: briefs already store steps and assumptions with confidence.
  Done when: falsifying a recorded assumption (`fm task assume` check fails) spawns a replanner that writes a plan diff against the remaining steps. A test shows it leaves done steps untouched and refuses a second re-plan within N steps unless new evidence exists.

- **Watch reasoning for known biases** — FEATURE — value 4 — effort M — risk med — category: metacognition
  Why: a supervisor for drift is already listed, but nothing names reasoning failures such as anchoring on the first hypothesis, premature closure, sunk-cost retries or confirmation-only probes. Assumption: the transcript and ledger show retried edits and probes.
  Done when: a replayed transcript of three same-hypothesis retries triggers a one-line nudge naming the bias and asking for a discriminating probe. A bench case shows fewer same-hypothesis retries with the monitor on.

- **Ask the historian before deleting or refactoring** — FEATURE — value 5 — effort M — risk low — category: agent roles
  Why: the user steered that cleanup requests "never got done", and the idea list has cleanup gates and deletion passes but no agent that knows why code exists. A read-only agent that reads git log, blame, briefs, decisions and vetoes can give a Chesterton's-fence verdict.
  Done when: for a CLEAN task naming a symbol, `fm history <path>` returns the originating task, the stated reason and a verdict of safe, unsafe or unknown, each with citations. The CLEAN plan cannot delete unknown symbols without recording an override.

- **Table-read the plan with a naive agent** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: M/L briefs carry steps and execution prompts, but only the author has read them. A cheap no-tools agent given only the brief narrates what it would do at each step and lists every point where it must guess. Assumption: fm-scout (Haiku) is good enough for this.
  Done when: a seeded brief with one ambiguous step makes `fm task tableread` output that step as a guess point. A clean brief yields none.

- **Run a simplifier against every L plan** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: briefs require 3+ approaches, but the choice is made by the same thread that wrote them. A role whose only charter is "the smallest thing that satisfies the criteria" proposes the less-code plan and names what it drops. This matches the user's recurring YAGNI and surface-cost concerns (the T-0278-style "see fm decide" drop).
  Done when: an L brief gets a simplifier section with a plan and a dropped-scope list. The main thread must accept or reject each dropped item in the brief before the plan is approved.

- **Define agent roles as data and bench each one** — FEATURE — value 4 — effort M — risk med — category: agent roles
  Why: five agent types exist as hand-written files, and the idea list wants new specialist roles. A role card holds charter, tools, model, stop rule and success metric. Each card gets its own bench slice, so a role can be tuned, merged or retired on evidence. Assumption: fm bench can filter by agent type.
  Done when: `fm agents roles` lists every role with its last bench score. A card with a score below the threshold for N runs is flagged for retirement.

- **Classify each mid-task fork as a one-way or two-way door** — FEATURE — value 4 — effort M — risk low — category: decisions
  Why: the user keeps tuning when Foreman asks versus acts ("budget limits shouldn't block until 75%"). A cheap agent labels each fork by reversibility and blast radius. It auto-decides and records two-way doors, and escalates only one-way doors. Assumption: `fm decide` can accept an automatic decision with a revisit trigger.
  Done when: a fork between two reversible edits is auto-decided with a recorded decision. A fork involving a schema migration or a push is escalated, and both cases are covered by tests.

- **Keep a working-memory scribe through long tasks** — FEATURE — value 4 — effort M — risk med — category: context
  Why: resume works after `/compact`, but the content is whatever the model summarised. A scribe agent maintains a small structured note (known facts, tried and failed, open questions, next step) after each step, and resume reads it.
  Done when: after a simulated compaction, the resumed thread's first answer cites an item that appears only in the scribe note. The note stays under a fixed size.

- **Preserve the minority report from agent panels** — FEATURE — value 3 — effort S — risk low — category: debate
  Why: fm second, reviewer panels and plan debates all end in a verdict and drop the lone dissent. A recorded dissent with a revisit trigger would let a later failure reopen the matching decision.
  Done when: a panel with one dissent writes it to the brief. If the task's gate later fails on the dissent's predicted point, `fm friction` surfaces it as "the dissent was right".

- **Wild: Wake a lateral-thinking squad when a task is stuck** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: wild. After the third failure the loop stops and diagnoses. Instead, a squad of agents with deliberately odd constraints (solve it by deleting code, work backwards from the desired output, solve a smaller instance first, assume the test is wrong) each returns a short attempt sketch. Assumption: forced-diverse retries are not yet tied to named strategies.
  Done when: on a replayed stuck task, at least three sketches with distinct strategy labels are produced, and a bench run records how often one unblocks the gate.

- **Wild: Give hot files a ghost owner** — FEATURE — value 3 — effort M — risk med — category: agent roles
  Why: wild. For files with long histories, distil a persona from their log: past bugs, conventions, reverted attempts and why-decisions. It comments on diffs touching that file with "last time this broke because…". Assumption: git history and briefs are rich enough.
  Done when: a diff reintroducing a previously reverted pattern in the test repo gets a ghost comment citing the reverting commit.

- **Wild: Hold a pre-mortem with a cast of the task's likely failures** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: wild. Before an L task starts, cheap agents each play one past failure mode taken from recall (flaky gate, scope creep, wrong file, missed edge). Each says how it would sink this plan. The surviving risks become brief risks with a detection step.
  Done when: an L brief gets at least two pre-mortem risks, each citing a past task id and carrying a verify command.
