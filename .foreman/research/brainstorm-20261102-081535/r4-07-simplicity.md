# Brainstorm — lens: simplicity

Reading "simplicity" as subtraction: fewer proof kinds, fewer files, fewer things the user must read, with every idea paid for by something it removes. Most of the catalogue is already filled, so these are second-order moves and combinations.

- **Adopt the CI workflow's `run:` steps as the default verify set** — FEATURE — value 4 — effort S — risk low — category: discovery
  Why: assumption: most target repos already encode "what proves this" in `.github/workflows`. No model call and no per-language prover is needed, and it fits the "never hand-write per language" steer.
  Done when: in a fixture repo with a workflow, `fm prove` with no arguments lists and runs those steps. It prints "none found" when there is no workflow.

- **Promote repeated post-finish manual commands into a prover** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: the pack has "log post-finish touches" but no step that turns them into action. If the user runs the same command after three finishes, that is their real definition of "works".
  Done when: a replayed history with a command typed after three finishes yields a proposed prover, accepted with one keystroke. A command typed once yields none.

- **Prove only claims the user would act on** — FEATURE — value 3 — effort S — risk low — category: claim triage
  Why: assumption: much verification spend goes to claims nobody would change a decision over. Each candidate claim gets one test: "if this were false, what would the user do differently?".
  Done when: a finish with six candidate claims proves at most three. The rest print as "not checked: wouldn't change your next move".

- **Use text as the default evidence in `fm shot`; make pixels opt-in** — CLEAN — value 3 — effort S — risk low — category: UI evidence
  Why: a text dump (visible text plus roles) is greppable, diffable and cheap for a cold reader. Pixel diffs add flake and artifact weight.
  Done when: `fm shot` with no flags writes a `.txt` and no `.png`. `--pixels` restores the image, and the text dump stays stable across two runs on the same fixture page.

- **Write flows as plain scripts over three verbs** — CLEAN — value 3 — effort M — risk med — category: flows
  Why: assumption: `fm flow` carries format-specific machinery. A flow that is a shell file calling `open`, `do` and `expect` can be read, diffed and run without Foreman.
  Done when: an existing flow converts to a script of 20 lines or fewer, produces the same verdict, and `bash flow.sh` runs it with Foreman absent.

- **Expire proofs by a 14-day lease first, and add file-hash expiry only if it beats the lease** — CLEAN — value 3 — effort S — risk low — category: proof lifecycle
  Why: the pack proposes hash-bound expiry, rename re-binding and re-verify samplers. A plain time lease is the do-less baseline, and nobody has measured the gap.
  Done when: the backtest over closed tasks prints how many stale proofs each rule catches. The hash machinery is built only if it catches more.

- **Name each task's evidence folder after the user's sentence and keep one self-contained `evidence.html` in it** — FEATURE — value 3 — effort S — risk low — category: evidence
  Why: scattered artifacts are hard to find and hard to show to someone else. A folder like `login-button-works/` holding a single double-clickable page also opens on a phone.
  Done when: finishing a task with a shot and a flow produces one folder with one HTML file that opens offline. The page includes the text dump, the command lines and the exit codes.

- **Show only the proof delta since the last finish card** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: the same "7 proven" boilerplate gets reread every card. Print "+2 proven, 1 expired, 0 new unproven" and nothing else when nothing moved.
  Done when: two consecutive finishes on unchanged claims print a card of 2 lines or fewer, and one changed claim appears alone.

- **Accept one bring-your-own command as the entire proof** — FEATURE — value 3 — effort S — risk low — category: do-less
  Why: this is the cheapest fallback for stacks Foreman has no prover for. The user supplies `--cmd`, and Foreman only records it, labels it, and checks it goes red against the parent commit.
  Done when: `fm prove --cmd 'make smoke'` writes a proof line with the command, the exit code, a red-on-parent result, and an expiry. It runs no other prover.

- **Echo test: the user types what they think shipped, and a cold child diffs that against the ledger** — FEATURE — value 4 — effort S — risk low — category: meaning check
  Why: wild. "Does it do what the user meant" is the hardest item in the request. One user sentence compared with the record surfaces the gap without any new prover.
  Done when: given a planted mismatch (the user claims "also works on mobile" and no such proof exists), the child lists it as unproven. A matching sentence gets a clean result.

- **Hold out a proof-free lottery: 1 in 10 low-risk tasks gets only the smoke floor** — PERFORMANCE — value 3 — effort M — risk med — category: measurement
  Why: wild. Nothing in the pack shows whether the extra provers lower reopen rates. If the lottery arm reopens no more, that prover class can be dropped. It is labelled unproven until enough tasks exist.
  Done when: `fm doctor` prints reopen rate per arm with counts, and says "insufficient" under 20 tasks per arm.

- **Run a one-claim week: each task may make exactly one claim** — FEATURE — value 2 — effort S — risk low — category: experiment
  Why: wild. A hard cap makes the user and Foreman pick the sentence that matters. Compare the reopen and "not quite" rates with the usual weeks.
  Done when: with `FM_ONE_CLAIM=1`, a second claim is refused with the first one named, and the week's numbers print beside the baseline.

- **Cap the finish card at the length of an index card** — CLEAN — value 3 — effort S — risk low — category: reporting
  Why: wild. It is 8 lines of 72 columns, with everything else behind a path. Anything that can't fit is, by construction, not what the user needed first.
  Done when: a finish with 20 proofs renders in 8 lines or fewer, with the unproven items listed first.

Answers to earlier questions, through this lens:
- **Which surfaces would the user open in a week?** Likely only the terminal finish card. Add no web proof page until `fm` logs show the existing pages being opened.
- **What should private goals do when they need a remote model?** Fail closed with one `fm ask` line that offers the weaker local model as the default, rather than silently degrading.

Next question: Which proof kinds has this user's reopen history shown never to matter, so they can be cut before anything new is added?
Next question: What is the shortest command the user types by hand to check that Foreman's work is real, and does any prover already cover it?
