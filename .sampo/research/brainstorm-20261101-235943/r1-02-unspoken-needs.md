# Brainstorm — lens: unspoken needs

**Earlier questions my lens can answer**
- *Which cells are one capability counted under several stages?* Assumption: Anticipation has three mechanisms (predict, draft in a lane, flag before it breaks). Most of the 58 cells are probably those three read at different stages, so about three probes cover them.
- *What does the user get if they never open the UI?* The pack gives no evidence of a non-UI delivery path. Idea 4 makes foresight change actions instead of adding text.

- **Tag every line in the model-of-me stream by origin** — FIX — value 5 — effort M — risk low — category: user model
  Why: "The user's own words" mixes real asks with Foreman-filed `FEATURE!:` items, its own `steered:` decisions and test debris, so a predictor trained on it learns Foreman's voice. Assumption: fmforesight reads this stream untagged.
  Done when: every stream line carries user, tower, decision or test, and a backtest of next-request prediction uses only user-origin lines.

- **Quarantine captures fed from tests and debugging** — FIX — value 3 — effort S — risk low — category: intake
  Why: the dropped lines "The first brief" and "The second brief" were sample text fed to `fm intake` while debugging T-2547, and both became queue items.
  Done when: `fm intake` called under a test or debug run lands in a quarantine list, never the queue, and a test proves it.

- **Forecast the ship before running the suite** — FEATURE — value 4 — effort S — risk low — category: ship
  Why: pushes are allowed but need a per-task publish grant that is spent on use, and the full suite takes minutes. Assumption: a missing grant or stale baseline currently surfaces late.
  Done when: `fm ship` prints grant state, baseline age and affected-test count before it starts, and refuses at once if the grant is missing.

- **Make foresight act instead of announce** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: the lean steers (injected chars, silence ratio, "pay by deletion") say the user doesn't want more text. A flag that only prints a note adds weight.
  Done when: each foresight flag type maps to a concrete action (reorder, add a step, run a test twice) or is logged silently, and a test shows zero added injected chars for a flag that changed an action.

- **Lift a steer when its own end condition is observed** — FEATURE — value 4 — effort M — risk med — category: steers
  Why: steers like "no new maintenance tasks until round 1 is done" and "T-2462 waits with T-2441 until round 1" carry end conditions, and nothing watches for them being met. Held items could sit past their release.
  Done when: when a steer's stated condition holds, the next session names the steer and the items it releases, and a fixture steer demonstrates it.

- **Tie machine quirks to pre-flight checks** — FEATURE — value 3 — effort M — risk low — category: machine model
  Why: the pack shows machine-specific failures: ETXTBSY (T-2543), setuptools missing (T-2529), libappindicator missing on Arch (T-0325), a hardened kernel, and children dir on tmpfs. Assumption: these aren't linked to checks yet.
  Done when: each recorded machine-caused failure has a pre-flight probe that runs when a task touches the related area, and one is shown firing on a fixture.

- **Predict which self-filed tasks the user will drop, before filing** — FEATURE — value 4 — effort M — risk med — category: filing
  Why: the dropped lines give reasons like "already built", "measured: 1 of 22" and "captured by mistake". All are things Foreman could have checked before filing. Assumption: a drop-rate base rate by task source can be computed.
  Done when: the filer reports drop-rate by source over the last 50 filings and withholds a filing whose predicted drop probability beats a backtested bar.

- **Count a cell only if a past incident could have used it** — CLEAN — value 3 — effort M — risk low — category: coverage
  Why: the standing rule says a cell counts only if grounded and not templated. Anticipation cells are the easiest to fill with plausible prose.
  Done when: each of the 58 cells cites a file or ledger/decision id, and `fm genesis check` rejects any cell without one.

- **Show a per-path correction density map that sets foresight depth** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: assumption: reopens and `steered:` lines cluster in particular files (fmdoors, fmexam, the hooks), and uniform foresight spends effort evenly.
  Done when: `fm foresight` prints a ranked path list from reopens and steers, and a task touching a top-5 path gets the extra check.

- **Wild: Run a bandit draft that sometimes drafts the second most likely request** — FEATURE — value 3 — effort M — risk med — category: speculation
  Why: assumption: always drafting the top guess never reveals when the runner-up was right, so precision can't be calibrated.
  Done when: 1 in N speculative lanes drafts the runner-up, labelled, and the report shows both hit rates.

- **Wild: Keep a hindsight court of the last 20 closed asks** — FEATURE — value 3 — effort L — risk low — category: backtest
  Why: the T-2546 lesson (a matcher with no backtest bar). Assumption: no replay of past asks through fmforesight exists as a gate.
  Done when: a stored replay of 20 past asks scores next-request hit rate and runs at every `fm ship` that touches fmforesight.

- **Wild: Open each session with the one thing the user is most likely to type first** — FEATURE — value 3 — effort S — risk med — category: session start
  Why: assumption: the SessionStart note is passive. A single predicted first move, shown only above a confidence bar, gives the user something to accept in one word.
  Done when: session start prints at most one predicted first request when its backtested precision is above the bar, and prints nothing otherwise.

Next question: Which of the 58 cells has no past user ask, correction or incident behind it, so that it is tower-originated demand?
Next question: What would a foresight flag have to change in the user's next action for the user to notice it?
