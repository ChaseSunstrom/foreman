# Brainstorm — lens: bold bets

- **Plant backdoors to test the self-change reviewer** — SECURITY — value 4 — effort M — risk low — category: self-change safety
  Why: The cold reads check Foreman's own diffs against the gen-0 MUSTs and for metric-gaming. Nothing in the pack measures whether they would catch a trojan hidden in a plausible refactor, such as a date-gated hook, a silent network call or a widened allow-list. Assumption: no such corpus exists today.
  Done when: `fm exam` has a "trojan" kind with 20 or more planted diffs, and it prints per-diff recall for Haiku and Sonnet with the misses named.

- **Lint the guard rule set for shadowed, unreachable and contradictory rules** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: Rules arrive from packs, learned rules, steers and hand edits. Assumption: the set is only tested by example, never analysed as a whole.
  Done when: `fm guard lint` flags a fixture rule hidden by an earlier deny and a pair of allow/deny rules that overlap. It runs clean on the shipped set, or each finding is listed with the rule ids.

- **Block by measured blast size, not command shape** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: Pattern rules miss `find -delete`, `git clean -fdx` and globbed `rm`. Assumption: the guard works by pattern today. Expanding the glob or running the tool's own dry-run (`git clean -n`, `rsync -n`) yields a file count and byte total that can be gated.
  Done when: a fixture command that would delete 500 files is blocked with "would touch 500 files, 40 MB", and the same command on 3 files passes.

- **Check guard parity on non-Bash tool calls** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: The README describes the guard as stopping commands. Writes to `~/.bashrc` or `~/.ssh`, MCP shell tools and WebFetch URLs carrying a secret reach the same harm by other tools. Assumption: coverage there is thinner.
  Done when: a table lists each tool class against the guard's verdict for ten equivalent harms, and each "allowed" cell is either blocked or recorded as a deliberate allow.

- **Random-walk the whole CLI against a state model** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: Recent commits (T-2664 torn lines, T-2648 dropped ledger classes, T-2653 exit paths) show bugs found one fault at a time. A stdlib random walk over all verbs, with invariants (ledger chain intact, no traceback, a `Next:` on every nonzero exit) and shrinking, would find the combinations.
  Done when: `fm drill --walk SEED` runs 500 steps in a temp home, fails on a planted invariant break, and prints the shrunk repro sequence.

- **Cut each child's context to what changed its answer** — PERFORMANCE — value 4 — effort L — risk med — category: privacy
  Why: Every brainstorm and cold-read child gets a full pack, which costs tokens and sends more of the project out than needed. Dropping one section at a time and keeping only those whose removal changes the verdict gives a per-kind minimal profile. Assumption: sections are separable.
  Done when: a profile file lists the pack sections each child kind needs, the replayed verdict agreement is 90% or better, and the median pack size is smaller.

- **Run a told-versus-untold A/B on guard awareness** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: An earlier brainstorm asked whether a model's behaviour changes when it knows it is guarded. The guard's own ledger can't see that.
  Done when: the same 20 scenarios run with and without a guard note in the prompt, and the report shows the unsafe-attempt rate for each arm.

- **Round-trip every mutating verb through apply and undo** — FEATURE — value 3 — effort M — risk low — category: safety
  Why: Assumption: verbs like `fm task`, `fm ship` and the tidy verbs have no machine-checked undo. A drill that runs apply, then undo, then diffs the state dir would show which are not reversible.
  Done when: `fm drill --undo` lists every mutating verb as reversible, irreversible-by-design or untested, and fails on a planted verb that leaves residue.

- **Answer "can Foreman do X?" from MASTER.md without a model** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: The pack has 1,388 skill files and 30+ "later" tasks, and docs are on the thin list. A BM25 `fm can "..."` over MASTER.md and verb help would answer with a citation or "not built". Searches that find nothing would be logged as doc gaps.
  Done when: `fm can "rewind a task"` returns the matching clause, `fm can "order a pizza"` prints "not built", and the miss is logged.

- **Mine git reflog and the trash for allowed commands the user undid** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: An earlier brainstorm left this question open: which allowed commands did the user later undo by hand? Reflog resets, restored files and re-created directories are evidence that needs no shell history, which the dropped `--dry-run` idea ruled out on privacy grounds.
  Done when: `fm doctor` lists allowed calls followed within an hour by a reflog reset or file restore, with a count and the denominator.

- **Wild: run self-changes under a time-shifted, network-off sandbox** — SECURITY — value 4 — effort M — risk med — category: self-change safety
  Why: Sleeper behaviour is triggered by date, host or network. Running the suite and hooks with `faketime` at +1 and +10 years, a different TZ and no network, and diffing the syscall and file-write logs against a baseline run, exposes it dynamically. Assumption: faketime and strace are available, or a stdlib shim can stand in.
  Done when: a planted date-gated write is flagged by the diff, and a clean change shows no divergence.

- **Wild: quote the price of bypass mode before it starts** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The risk budget exists but isn't framed as a price. From past block, incident and restore counts, show "this session: about 1 in 40 chance of a restore, about 7 minutes expected cost", then settle the quote afterwards.
  Done when: enabling bypass prints a one-line quote with its sample size, and session close prints actual against quoted.

- **Wild: dry-run pasted shell commands from the clipboard (opt-in)** — FEATURE — value 2 — effort M — risk med — category: devices
  Why: People paste "curl | sh" lines into their own terminal. A `wl-paste --watch` opt-in could run the guard's dry-run and show a desktop toast. It stays local and records nothing.
  Done when: copying `curl x | sudo sh` raises a toast naming the rule, copying `ls` raises nothing, and it is off by default.

Next question: Which of Foreman's own verbs, hooks or skills would have to be audited first if the self-change reviewer itself were compromised, and does anything outside the reviewer check them?
Next question: If a user installed only the guard and nothing else, which measured claims in the README would still hold?
