# Brainstorm — lens: approaches

- **Mine the finish text's own caveats as predicted asks** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: the commit `Unproven:` trailer and the receipt's per-kind unproven list already exist, but the pack shows nothing that reads them as "what the user will ask about next". Zero tokens: match "not verified", "didn't", "you may want" at Stop and file each as a ghost candidate.
  Done when: a fixture finish message containing "I did not run the migration" yields one predicted-ask row naming it, and a message with no caveats yields none.

- **Capture a one-line "tomorrow:" note at session close** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: assumption: the user's own stated next step is the highest-precision predictor and nothing in the pack collects it. Optional, one line, skippable with Enter. It doubles as a labelled example for every other predictor.
  Done when: a `tomorrow:` line typed at Stop appears in the next SessionStart card, and an empty line writes nothing.

- **Settle predictions by the first thing touched next session** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: sealed predictions need a hit definition, and waiting for a typed ask is slow and needs text matching. The first file edited or the first `fm` verb run in the next session is an objective, zero-token label.
  Done when: a sealed prediction naming `plugin/lib/fmcost.py` scores a hit when that file is the first one edited, and a miss otherwise, in a fixture ledger.

- **Treat the user's own new TODO/FIXME lines and stashes as asks-in-waiting** — FEATURE — value 3 — effort S — risk low — category: intent signals
  Why: "Harvest dated TODOs" covers old markers, but a TODO the user typed this week is current intent. `git stash list` and WIP branches are the same kind of signal. A hand-written marker is not Foreman's own output, which matches the standing weakness-finding rule.
  Done when: a hand-added `# TODO: retry on 429` in the working diff shows up as a candidate with the line cited, and a Foreman-authored TODO does not.

- **Look up what followed the nearest past asks (local TF-IDF)** — FEATURE — value 3 — effort M — risk med — category: prediction
  Why: the task-kind follow-up table is coarse. Roughly 2,600 filed tasks give a stdlib-only kNN over ask text: "asks like this were followed by T-…". Trade-off: it finds repeats of past patterns only, never new ones.
  Done when: a leave-one-out run over the task ledger prints hit@3 for kNN beside the task-kind table, and the new method is kept only if it wins.

- **Ship a cold-start prior for fresh installs** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: assumption: every history-based predictor is empty on day one, and the standing rule says Foreman isn't just for this user. Distil a small follow-up table from the 30 foreign repos' histories and drop it as the user's own data grows.
  Done when: in an empty state dir the prior yields a non-empty prediction for `fix` tasks, and it fades to zero weight after N local closes.

- **Allocate the single anticipation slot with a bandit** — FEATURE — value 3 — effort M — risk med — category: prediction
  Why: dozens of predictor sources compete for one line, and the pack's mute is binary. Thompson sampling over per-source hit rates shows the best source most often and still explores. Trade-off: it needs hits to learn from, so the first-touch label comes first.
  Done when: in a simulated ledger where source A hits 60% and source B 5%, A holds over 80% of slots after 50 sessions and B is still sampled.

- **Show predicted tasks as dimmed ghost rows in `fm next`** — FEATURE — value 3 — effort M — risk low — category: queue
  Why: filing predictions as real tasks pollutes the inbox, and the standing round-first rule already limits Foreman-filed items. Unfiled ghost rows carry a one-key promote and decay unseen.
  Done when: a ghost row never appears in `fm list`, and promoting it files a task with the ghost's evidence quoted.

- **Hold non-urgent `fm ask` questions until the user's usual reply window** — FEATURE — value 2 — effort S — risk low — category: timing
  Why: assumption: reply latency by hour is already recoverable from `fm ask` timeouts and answers. Asking when the user historically answers quickly reduces blocked time without a new surface.
  Done when: a fixture where answers arrive only 18:00–22:00 defers a non-urgent ask to 18:00, and an urgent one fires immediately.

- **Tag each prediction with a horizon and score it against that horizon only** — CLEAN — value 2 — effort M — risk low — category: measurement
  Why: "next message", "next session" and "next week" predictions are currently one pool, so a weekly guess is scored as a miss on the next message. Horizon tags give honest per-horizon hit rates.
  Done when: `fm doctor` prints a hit rate per horizon, and a week-horizon prediction is not scored until the week closes.

- **Say what a close unblocked** — FEATURE — value 2 — effort S — risk low — category: queue
  Why: tasks have `depends`, and `fm next` already honours it, but the finish card doesn't tell the user what became ready. This is the cheapest "what's next" signal, and the graph supplies it.
  Done when: closing a task that two others depend on prints "unblocked: T-a, T-b", and closing one with no dependents prints no such line.

- **Dowse attention from the compositor and editor state (wild)** — FEATURE — value 3 — effort L — risk high — category: ambient context
  Why: assumption: focused window title, Neovim shada and VS Code recent files say what the user is looking at now, which no ledger records. Local-only and opt-in, since it is sensitive. Trade-off: the sources are compositor- and editor-specific.
  Done when: with the setting on and a fixture recent-files list, a file path from it is offered as a candidate, and with the setting off nothing is read.

- **Write tomorrow's morning note in the user's voice and learn from their edits (wild)** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: a first-person draft ("I stopped at the burden fix; I'll start with …") opens in `$EDITOR`, and the edit distance is a dense supervised label that costs the user nothing extra. Trade-off: the draft must stay short, or the user will skip it.
  Done when: an edited draft stores its diff, and the next draft reuses a phrase the user added.

- **Send a next-morning second-thoughts letter on yesterday's closes (wild)** — FEATURE — value 3 — effort M — risk med — category: re-verification
  Why: re-run each closed task's proof on today's main and have a cold child re-read the diff. Failures and drift become the likeliest next asks ("T-2668 now fails against X"), found before the user trips on them.
  Done when: a planted regression on main after a close appears in the next morning's letter naming that task, and a clean day prints one line.

Next question: which of these predictors can be scored without any text matching, so that a new one can be judged in a week and not a quarter?
Next question: what is the user's actual cost of a wrong anticipation (an ignored line, a filed junk task, an overnight spend), and does any current idea price it?
