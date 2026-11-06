# Brainstorm — lens: bold bets

- **Share a substituter cache for agent work** — PERFORMANCE — value 4 — effort L — risk med — category: performance
  Why: assumption: the pack has gate-result caching by tree hash, but no cache for whole steps. Nix-style: key each step's result by (tree hash, step spec, runner manifest hash, model digest) and store it in a git ref or a shared folder. A clone, a lane or a second machine then pulls the finished diff and its proof instead of paying for the work again.
  Done when: rerunning an identical request on a fresh clone of the same tree makes zero model calls and yields a byte-identical diff, and any change to the tree or runner manifest misses the cache.

- **Compile each step's plan scope into a throwaway sandbox profile** — SECURITY — value 4 — effort M — risk med — category: containment
  Why: combines two separate ideas in the pack, declared file scope per plan and an OS sandbox for workers. Today the scope is checked after the fact. Generate a bwrap or sandbox-exec profile per step from its declared files and commands, so out-of-scope writes fail at the kernel and are logged as plan drift. This holds for any CLI runner, including ones with no hooks.
  Done when: a fake runner told to write outside its step's declared files gets EPERM, and the run log shows the denied path as a drift event.

- **Open a universal human port for every agent** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: the pack has many "needs you" inbox ideas, all fed only by Foreman's own runs. Expose one local `ask_human` MCP tool and CLI that Claude Code, Codex, Cursor and CI bots can all call. Answers land in the same decision inbox with defaults, deadlines and standing grants. The user answers in one place whichever agent is asking.
  Done when: two different agent CLIs each post a question, both appear in one `fm` inbox, and answering each unblocks the right process.

- **Make the run a plain file cockpit** — FEATURE — value 4 — effort M — risk low — category: devices
  Why: assumption: many surfaces are proposed (TUI, pane, web, Artifact, phone PWA), and each needs its own code. Instead, write `RUN.md` as a self-updating file with status, criteria checkboxes, an asks section and a steer section, and watch it for edits. Any editor, Obsidian, a synced phone notes app or `cat` becomes a working surface, and ticking a box or typing under "Steer" reaches the run.
  Done when: editing a checkbox and a steer line in `RUN.md` from a second process changes the live run within 2 s, and the file stays valid markdown across 1,000 updates.

- **Schedule runs as resumable quanta** — PERFORMANCE — value 4 — effort L — risk med — category: scheduler
  Why: the pack has a run journal, rate-limit pausing, cross-project fairness and laptop-lid survival as separate ideas. One cooperative scheduler covers them: chop each run into short quanta with yield points, checkpoint each, and interleave runs fairly over scarce runners and quota windows. Sleep, Ctrl-C and rate limits then lose at most one quantum.
  Done when: killing the process at 20 random points across three concurrent runs loses under one quantum of work each and every run finishes after restart.

- **Pin each runner's privileges to a promotion curve** — SECURITY — value 3 — effort M — risk low — category: trust
  Why: the pack has probation lanes and a guard grade per runner, but privileges are still set by hand. Let a new runner or model digest start with read-only plus diffs, and promote to edits, then shell, then unattended as its measured hold rate and clean closes cross published thresholds. A new model digest resets the curve.
  Done when: a scripted fake runner that cheats is never promoted past tier 1, and a clean one reaches tier 3 after N verified runs.

- **Run a daily brownout drill on Foreman itself** — FIX — value 3 — effort M — risk low — category: reliability
  Why: assumption: the user's repeated "it just isn't doing anything" complaints suggest silent degradation matters more than crashes. Each day, in a scratch HOME, run one real request while removing a dependency at random (network, `claude`, disk, the tray library, the ledger). Assert the harness names the loss in one line and continues in a reduced mode.
  Done when: all five fault injections end in a labeled degraded run and none in a hang or silent no-op.

- **Run a metered dollar auction among runners per step** — FEATURE — value 3 — effort L — risk med — category: routing
  Why: the pack has routing tables and cheapest-sufficient ideas but no live price discovery. Each step collects a quote (tokens, latency, prior pass rate) from every available runner. Pick the best expected cost per verified pass, and log how the quote compared with the actual cost. Over time this tunes itself from the user's own data.
  Done when: with a cheap and an expensive fake runner, the cheap one wins easy steps and loses to the expensive one after repeated verify failures.

- **Wild: Mirror every plan in a sabotaged universe** — FEATURE — value 3 — effort L — risk med — category: attribution
  Why: wild. The user wants the harness to be the strong part, and today nothing measures how much of a result the harness earned versus the model. Run sampled steps a second time with a known-wrong fact planted in the pack, and see whether the harness's checks catch it. The catch rate becomes a per-runner harness-value score shown beside each close.
  Done when: a planted false premise is caught by checks in at least X% of sampled runs with a strong runner, and the score appears in the run report.

- **Wild: Turn the user's idle hours into a speculative queue** — FEATURE — value 4 — effort L — risk med — category: unattended
  Why: wild; assumption: overnight and idle ideas exist, but none says "speculate on the user's likely next requests only with local models, never touch their tree, show one accept key." Predict the next three asks from the ledger. Pre-run them on a free local runner in a throwaway worktree. On return, one key lands any that match what was typed.
  Done when: on a replayed week of history, at least one typed request matches a staged result, and unmatched staged work is discarded with no changes to the user's tree.

- **Wild: Export a proof as a self-checking bundle** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. Today the proof lives in Foreman's ledger. Emit one folder with the diff, the exact commands, their recorded outputs, the tree hash and a stdlib `verify.py`. A stranger, or CI with no Foreman, re-runs it and sees pass or fail. It doubles as the artifact for the benchmark and for upstream bug reports.
  Done when: `python3 -I verify.py bundle/` on a clean machine reproduces the pass, and editing one byte of the diff makes it fail.

- **Collapse six nouns into one run table** — CLEAN — value 3 — effort L — risk med — category: simplicity
  Why: the pack repeats the complaint that captures, tasks, ideas, asks, runs and plans each have their own verbs and stores. One typed table with a state column replaces them, and every old verb becomes a forwarding alias that prints the new form once.
  Done when: all existing verbs still work via aliases, the CLI test suite passes unchanged, and the count of stores under state drops to one.
