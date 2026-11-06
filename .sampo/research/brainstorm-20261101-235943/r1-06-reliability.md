# Brainstorm — lens: reliability

- **Gate every prediction heuristic on a walk-forward backtest** — FEATURE — value 5 — effort M — risk low — category: foresight
  Why: T-2546's word-overlap matcher met no bar, and Missions 3-5 lessons say a heuristic must name its backtest. `fm genesis put` already refuses ungrounded briefs (T-2547), so it can refuse an Anticipation brief with no replayable bar.
  Done when: `fm genesis put` rejects a Mission brief that adds a foresight heuristic with no `backtest:` line, and accepts it once the backtest command exits 0 on the closed-task history.

- **Resolve every prediction to hit, miss or expired** — FIX — value 5 — effort S — risk low — category: scoring
  Why: assumption: predictions that are never matched to a request silently leave the denominator, which inflates hit rates. The existing bets already settle per bucket, so the same rule should cover forecasts.
  Done when: a fixture with 10 predictions, 4 of them never matched, reports `hit 3 / miss 3 / expired 4`, never 3 of 6.

- **Make the forecaster say "abstained" or "failed", never an empty list** — FIX — value 5 — effort S — risk low — category: foresight
  Why: T-2532 and T-2542 showed hooks and timers going silently off, and the recurring blind spot is that nobody sees a dead component. A forecaster crash and a genuinely empty forecast look the same to the user.
  Done when: killing `fmforesight` mid-run makes the next SessionStart print `foresight: failed (reason)`, and a clean run with nothing to say prints `foresight: abstained`.

- **Stamp each speculative draft with its tree hash and steer set, and refuse adoption when either moved** — FEATURE — value 4 — effort M — risk low — category: drafts
  Why: assumption: a draft written overnight is adopted against a different tree. T-2334 and T-2507 were both stale-premise bugs, so this is the same class.
  Done when: a draft made at commit A is refused with a named reason after a commit that touches its blast radius, and is adopted after an unrelated commit.

- **Strip captured-by-mistake and dropped items from the user model's input** — FIX — value 4 — effort S — risk low — category: user model
  Why: the pack shows "The first brief" and "The second brief" as asks, later dropped as "captured by mistake: a sample line fed to fm intake while debugging T-2547's test". A predictor trained on the asked stream would learn them.
  Done when: a history containing those two dropped captures yields a user model identical to one without them, and a test pins it.

- **Cap problem flags per session and mute a signature after two dismissals** — FEATURE — value 4 — effort M — risk low — category: alerts
  Why: "flags problems before they happen" turns into noise fast, and noise teaches the user to ignore the one real flag. There is already a floor on speculative lanes, but nothing limits flag volume.
  Done when: a fixture session with 12 repeated-signature flags shows at most 3, and a signature dismissed twice stays silent until its inputs change.

- **Rebuild the user model from its append-only sources and prove it matches** — CLEAN — value 4 — effort M — risk med — category: state
  Why: the user model is state that sessions and lanes may write concurrently. Making it a disposable derived cache removes corruption as a failure mode.
  Done when: deleting the model file and running rebuild yields byte-identical output to the pre-delete file on a fixture history, and a half-written file triggers the rebuild instead of a crash.

- **Check that all four non-Claude harness formats yield the same asked records** — FIX — value 4 — effort M — risk med — category: harness parity
  Why: an earlier brainstorm asked what the web UI shows for a plan written by codex, gemini, opencode or `fm code`, and T-0335 to T-0337 show those paths are the least verified. A model fed only Claude transcripts is biased.
  Done when: one scripted session replayed in each harness's format produces the same normalised asked rows, and the test names any field a harness lacks.

- **Give each of the 58 cells a planted-history probe with a known next request** — FEATURE — value 5 — effort L — risk med — category: coverage
  Why: lessons say a cell counts only if it names a concrete capability grounded in a file or a real gap. A cell that cites `fmforesight` without a fixture that makes it predict something is only prose.
  Done when: each filled cell lists a fixture id, and `fm genesis check` fails any cell whose fixture does not reproduce its claimed prediction or flag.

- **Wild: run a shuffled-history control arm alongside the real forecaster** — FEATURE — value 4 — effort M — risk low — category: scoring (wild)
  Why: the standing rule says a free arm that beats the session arm is a top gap. The same logic applies to a null model: if a forecaster fed shuffled history scores about the same as the real one, the signal is fake.
  Done when: `fm outcomes` prints real versus shuffled hit rate with an interval, and flags any forecast kind where real does not beat shuffled.

- **Wild: add a time-machine mode that replays the forecaster at each past commit date** — PERFORMANCE — value 4 — effort L — risk med — category: backtest (wild)
  Why: the user has 2,500+ tasks of history, which is enough to ask what Foreman would have predicted on any past day and whether it was right, with no new data needed.
  Done when: `fm foresight timemachine --from DATE` prints a weekly hit-rate curve computed only from data that existed on each date, and a test shows a future task never leaks into an earlier week.

- **Wild: plant a fake habit and check the forecaster does not over-learn it** — SECURITY — value 3 — effort S — risk low — category: overfitting (wild)
  Why: assumption: with a low evidence threshold, two coincidental repeats become a "habit". A planted canary with 2 occurrences must stay below the draft threshold, while one with 6 consistent occurrences must cross it.
  Done when: the exam's tool-less child inserts both canaries and the test asserts only the 6-occurrence one yields a drafted lane.

- **Give the forecaster a no-network deterministic mode and diff its output** — CLEAN — value 3 — effort S — risk low — category: determinism
  Why: the run is cheap-model driven and unattended, and a prediction that changes between identical inputs cannot be backtested or audited.
  Done when: two runs on the same pinned inputs with the network cut produce identical forecasts, and any model-dependent field is labelled as such.

Next question: Which Anticipation outputs (forecast, flag, draft) does no session path read, so that a wrong one would never be seen by the user?
Next question: What is the smallest history size at which a forecast beats the shuffled control, and what should the forecaster say below that size?
