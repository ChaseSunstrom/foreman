# Brainstorm — lens: done-vs-stopped auditor (invented): an adversary that tries to prove the work merely stopped — usage limit, drive cap, no-progress stop, crash, the model saying done

- **Gate the Stop verdict on a stop-cause enum, not on the model's words** — FEATURE — value 5 — effort M — risk med — category: stop verdict
  Why: the pack's "done-vs-stopped verdict" gap lists five distinct stops (usage limit, crash, drive cap, no-progress stop, model says "done"). The Stop hook already knows the drive cap and no-progress cases first-hand, so it can record them with no inference. Only the usage-limit and crash cases need transcript evidence.
  Done when: a fixture session that ends at DRIVE_MAX with 2 open criteria yields `stopped:drive_cap`. `fm goal verdict` prints it, and a forced "all done" message in the same fixture does not change it.

- **Require a completion sentinel on every piece of acceptance evidence** — FIX — value 5 — effort S — risk low — category: evidence integrity
  Why: assumption: a verify command killed by a usage limit, a timeout or output truncation can leave partial green output that `fm task finish` reads as fresh evidence. A sentinel written after the exit code is recorded closes that gap.
  Done when: a test kills a verify command mid-run, and its criterion stays unmet with the reason `evidence incomplete`.

- **Cache the audit by (ledger head, tree hash) and read it in O(1) from the Stop hook** — PERFORMANCE — value 4 — effort M — risk low — category: hook speed
  Why: the pack says hooks must pass the bench_hooks gate. A charge sheet that grows with the goal would run on every Stop in a drive loop, so the audit should be computed on ledger append and only read at Stop.
  Done when: bench_hooks shows the Stop hook p95 unchanged with a 200-item goal ledger. The cache is invalidated by one new event.

- **Size DRIVE_MAX per goal from measured cost per closed criterion** — PERFORMANCE — value 4 — effort M — risk med — category: drive cap
  Why: a constant drive cap ends a large goal early as "stopped" and over-runs a small one. The ledger already has the per-criterion close history needed to estimate the cost.
  Done when: a goal with 40 open criteria gets a larger cap than one with 3, and the cap is shown with its basis in `fm goal`. Replaying a recorded 10-item goal produces zero cap stops.

- **Measure progress by criterion transitions, not by diff size** — FIX — value 4 — effort M — risk med — category: no-progress stop
  Why: the no-progress stop can misfire either way. A long diagnosis changes no files yet is progress, while a churn loop changes many files and is not. Counting red→green transitions, new reproductions and new decisions in the ledger is a better signal.
  Done when: a fixture of 30 turns of reading and one test run does not trip the stop. A fixture of 30 edits with no criterion change does.

- **Keep a per-model false-done rate and set drive strictness from it** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the model's "done" is untrusted data in this project. Each audited done that is later reopened gives a per-model count, so a model with a high false-done rate gets the cold audit every time and a reliable one gets a lighter check.
  Done when: `fm goal stats` shows the false-done rate for each model id. A test shows that a model with 3 of 5 reopened dones always triggers the cold audit.

- **Label real session ends from the user's own transcripts as the stop-classifier exam set** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: the exam is planted-defect repos, which have no stop shapes. Locally, a session that is followed within 48h by the same goal's work was really "stopped", and one that is followed by silence is probably "done". That gives free labels. assumption: transcripts are readable on the owner's machine. Nothing leaves it.
  Done when: `fm exam` has a `stop-tail` kind built from at least 30 locally labelled tails, and the classifier's agreement with the labels is reported per cause.

- **Score other agents' exits: label a Codex, Gemini or opencode session ended-open** — FEATURE — value 3 — effort M — risk low — category: surfaces
  Why: the shims in fmagents.py already see the agent's exit. At exit, diffing the ledger and the git state against the goal's open criteria gives a "quit with 4 open" verdict even where there is no Stop hook.
  Done when: each shim run ends with a verdict line, and one fixture per agent covers a premature exit.

- **Show the verdict as a glyph on every glance surface (terminal status line, tmux, pane, ntfy push)** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: assumption: the user mostly learns a session died by returning to it. `○ stopped:usage_limit +1 open` with a reset time, sent as a push if the user has configured ntfy, avoids that. It is an outward send, so it needs an explicit setting.
  Done when: the status line shows ●/○/◐ for done, stopped and unknown. The push is sent only when `push` is on, and a test checks that the default sends nothing.

- **Fail closed on a verdict that cannot be read** — SECURITY — value 3 — effort S — risk low — category: stop verdict
  Why: a corrupt or missing goal ledger must never read as "nothing open, so done". Absence of items needs the same strictness as an unmet item.
  Done when: deleting or truncating the goal file makes the verdict `unknown` and blocks done in the Stop hook.

- **Wild: Hold a parole hearing for goals stopped more than 7 days** — FEATURE — value 3 — effort M — risk low — category: lifecycle
  Why: wild. Abandoned goals stay open forever and keep re-injecting into sessions as noise. A cheap cold read of the ledger and the repo decides between revive, shelve and cut-with-reasons, and the user can veto in one line.
  Done when: a goal with 8 days of silence gets a hearing record with one of the three outcomes. A shelved goal no longer appears in the session card.

- **Wild: Ask "is it done?" aloud and get the strongest charge back** — FEATURE — value 2 — effort M — risk low — category: voice
  Why: wild. A local text-to-speech call, or a printed line if there is none, answers in one sentence: "Stopped. Drive cap hit; criterion 3 unmet." Nothing leaves the machine.
  Done when: `fm goal say` prints the same sentence a spoken version would read. A test checks it is under 25 words.

- **Wild: Publish mortality tables of how goals of each size end** — FEATURE — value 3 — effort M — risk low — category: forecasting
  Why: wild. From the goal ledger, count how goals of each size ended (done, drive cap, usage limit, abandoned). A new goal can then show "goals this size finish in a single session 18% of the time", which sets the user's expectations.
  Done when: `fm goal odds` prints a table from at least 10 closed goals and says "too few goals" below that.

Answers to earlier questions: the proof-failure cost question is about recording the cause. A proof killed by a limit is a stopped proof, not a failed one. The finding's record should be unchanged by it.

Next question: What does the Stop hook do when two goals are open and the session closes one, and which goal's ledger owns the verdict?
Next question: Which stop causes does Foreman never see because the process was killed before any hook ran, and what is the cheapest external witness?
