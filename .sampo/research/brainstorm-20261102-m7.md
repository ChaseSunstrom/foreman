# Brainstorm catalogue: brainstorm-20261102-155217 (gen-3 Mission 7, #3)

393 ideas in 64 clusters, each grounded in the code: 34 built, 13 false-premise, 170 new, 176 partial. 16 clusters marked build.

Mission 6's measures, counted from this catalogue: 169 of the 170 "new" verdicts carry a canary result (T-2674's rule);
41 ideas came from grid-lens cells (T-2672), and 27 of them grounded as new or partial, that is, as real gaps.
Spot checks before any brief: fmforesight.lines (fmforesight.py:197) shows setup changes and red CI only, never the
booked next-request prediction — true (found by two passes independently). No hook names landed, unshipped work —
true. fmforesight.pile_lines (fmforesight.py:184) gives the blocked count, the oldest and "→ fm tidy", never the action
that frees the most — true. fmserve._notify (fmserve.py:741) ignores the notify command's exit code and swallows every
error — true.

## c01 Blocked and stalled work: the one action that frees it

Mark: **build** · value 4 · effort S · risk low — the pile line exists and says only how many; naming the unblocking action is direct anticipation  
Slate: Extend fmforesight.pile_lines to name, for the blocked pile, the user action that frees the most tasks (answer an fm ask, grant a request, resolve a dependency) with its count, ranked.

- [partial] Mark each blocked task with the single user action that frees it, ranked by count freed — pile_lines (fmforesight.py:184-194) shows the blocked count and oldest age with → fm tidy; no per-task action or ranking
- [partial] Rank stalled work by days since the user last mentioned it — pile ages by 'updated' (fmforesight.py:188-190); STALE_DAYS=14; not by last user mention

## c02 Prediction delivery and surfaces

Mark: **build** · value 4 · effort S · risk low — The predictor is booked and scored but never shown at session start. The user cannot see it, and it must respect mute.  
Slate: Show the newest unscored, unmuted next-request prediction as one session-start line from fmforesight.lines (type and top paths, with its hit rate beside the baseline's), and cover it with a test.

- [partial] Turn every "Next question" into a scored forecast — fmideas.py carries a 'Next question:' per lens into the next pack (T-2076). Not booked in predictions.jsonl
- [partial] Precompute the anticipation card at Stop, read it at SessionStart — Stop spawns the sweep (fmforesight.py:1-4) and lines() reads caches at SessionStart. The next-request prediction is not in lines()
- [partial] Bind each prediction to the ledger epoch and HEAD, and drop it when the user's first message contradicts it — Rows are bound to the 'after' task id (fmforesight.py:343), not HEAD. No contradiction drop
- [new] Show a predicted-asks shelf in the web UI with evidence and a never button — No web UI for predictions. fm outcomes --predictions --unmute is CLI only. canary: def main found (fmcli.py:8473)
- [new] Turn each left-over "Next question" into a zero-token probe or a filed experiment — grep 'Next question' fmideas.py: 1 file, only carried forward. canary: def main found (fmcli.py:8473)

## c03 Say the next-request guess to the user

Mark: **build** · value 4 · effort S · risk low — the predictor already beats its baseline and gates itself, but its guess is shown nowhere; one gated line is the cheapest anticipation payoff  
Slate: At SessionStart and in fm next print one line naming the newest unscored next-request prediction (type and top paths) only while fmforesight.prediction_kinds shows it beating its naive baseline and not muted, and book that it was shown.

- [partial] Do less: print one "you usually ask X next" line at finish — fmforesight.prediction_tick (:311) books next-request type+paths; only the hit rate prints (fmtriggers.py:298), never the guess
- [partial] Wild: let `fm ?` answer with the one thing Foreman expects you to ask — grep 'fm \?' in fmcli.py: no verb; the guess exists in predictions.jsonl (fmforesight.py:342) but has no reader verb
- [partial] Suggest the next ask as ghost text on the prompt line — near T-0095 (done) — grep 'ghost text' lib: 0 hits; the guess is booked (fmforesight.py:342) but no surface renders it
- [partial] Show predicted tasks as dimmed ghost rows in `fm next` — fmcli.py:6009 fm next only notes 3x overrun; the next-request row (fmforesight.py:342) is never listed
- [partial] Wild: Draft the follow-up as a task title with a one-word veto — fmdraft.ahead (:139) drafts a plan (DRAFTED-AHEAD.md) for the predicted request; no title or veto word
- [new] Print a one-line repo hello on `cd` — grep 'hello|on cd' lib: 0 hits; canary: def main found in fmcli.py:8473

## c04 Visible degraded state

Mark: **build** · value 4 · effort S · risk low — A hook failing silently is something the user will hit and not understand. The error data and the session-start reader already exist.  
Slate: Add a hook-error line to fmforesight.lines so a session start names any hooks.log traceback from the last day, with the fm doctor command that clears it, and test it by planting a traceback.

- [partial] Let hooks degrade visibly when the user can't tell they're off — fmfriction.py:209-219 and fmdoctor.py:1138 read hooks.log. fmhooks.py:3 fails open silently at the prompt
- [partial] Print a first-minute card after any fail-open, and test it — grep 'first.minute|degraded' fmhooks: only fmbudget.degrade. Hook errors show in fm doctor and friction, not at session start
- [partial] Print a one-line "running degraded" status that survives every fail-open — fmdoctor.recent_hook_errors (fmdoctor.py:1138) has the data. No status-line surface
- [new] Show the user a harmless fail-open on install day — grep 'install day|first run' fmsetup/fmhooks: nothing. canary: def main found (fmcli.py:8473)
- [partial] Show the first-minute "Foreman is degraded" card from the same file the anticipation card uses — fmforesight.lines (fmforesight.py:197) is the session-start cache reader. A hook-error line could join it

## c05 Alert delivery, liveness and hook reliability

Mark: **build** · value 4 · effort M · risk low — A swallowed notify failure means the user never hears the warning Foreman foresaw.  
Slate: Make fmserve._notify record a delivery result per channel and fall back to the next channel when one fails, with a doctor line when all failed.

- [partial] Time-box the unattended drive's own startup on a slow disk and cold cache — bench_hooks.py ratchets hook time; grep 'cold cache' fmnight.py: none
- [partial] Wild: Add a "heard nothing" lamp to the status line for each unattended path — fmcore.py:3835 stall; grep 'heard nothing' lib: none
- [new] Run the unattended tick on an always-on host — grep 'always-on|remote host' plugin/lib: none; canary: def main found
- [new] Wild: prove the first minute after a silent fail-open by deliberately triggering one on install day — grep 'fail-open' fmhooks.py drill: no install-day trigger; canary: def main found
- [partial] Prove every alert channel delivers, and fall back when it doesn't — fmserve.py:741 _notify swallows errors silently; grep 'fallback' fmserve.py: none
- [built] Make each hook time itself out before the host kills it — fmhooks.py:958 hook deadlines
- [partial] Single-flight every scheduled job and record overlaps — fmnight.py:372,525 flock 'already running'; overlaps not recorded. grep 'overlap' fmnight.py: none
- [new] Harvest a slow-input corpus from real hook timings — grep 'slow-input|corpus' plugin/lib: none; canary: def main found

## c06 Anticipation card surface, delivery and what-changed

Mark: **build** · value 4 · effort M · risk low — Cards exist but delivery and surface are unrecorded, so a hit cannot be told from a never-read card.  
Slate: Write a delivery receipt (surface, injected yes or no) for each anticipation card and drop a card when the user's first message contradicts it.

- [new] Park `fm ask` for the user's learned present window — grep 'present window|learned window' plugin/lib: none; canary: def main found
- [partial] Make anticipation cards declare which surface they were rendered on — fmforesight.py lines()/pile_lines() feed SessionStart only; grep 'rendered_on|surface=' lib: none
- [partial] Show a "what changed since you last looked" diff in the pane header — SessionStart summary exists (fmforesight.lines); grep 'since you last' lib: no pane diff
- [partial] End every finish card with a verdict and its flip condition — fmcli.py:8500 Next: lines (T-2653); grep 'flip condition' lib: none
- [new] Wild: Keep a "things you've stopped asking about" shelf — grep 'stopped asking|shelf' plugin/lib: none; canary: def main found

## c07 Capacity forecasts

Mark: **build** · value 3 · effort S · risk low — The disk filled once on 2026-10-22 with no warning first. A growth projection adds a warning in time, on top of check_disk.  
Slate: Extend fmdoctor.check_disk to project state-dir growth from the last 7 days of ledger size and warn when the low-disk threshold would be crossed within 7 days.

- [partial] Warn when the state directory or ledger growth will cross a ceiling inside a week — fmdoctor.py:1591 check_disk warns at LOW_DISK_BYTES now. No growth-rate projection
- [partial] Make the ledger size and age visible to the user's disk — fmforesight._state_bytes (fmforesight.py:412) exists for breakage. fm doctor shows disk, not ledger size
- [partial] Forecast the date each hard cap will bind — fm cost --forecast (MASTER.md:613) projects usage windows. Other hard caps not forecast
- [built] Diff host facts per session and probe on change — fmforesight.setup_change (fmforesight.py:42): model, window and CC version diffed per sweep and named at session start

## c08 Doctor extensions and install checks

Mark: **build** · value 3 · effort S · risk low — Doctor already finds sandbox doubt; toolchain and override lines forestall silent unattended failures.  
Slate: Add toolchain-manager (mise, asdf, nvm, pyenv) and ambient FOREMAN_* override lines to fm doctor, each with the command that clears it.

- [built] Make `fm doctor` print one cause line per red, with the command that clears it — fmcli.py:8500 Next: lines (T-2653) on every nonzero exit
- [partial] Test the first minute after install with the user's own settings — near T-2357 installs queued for one yes; no first-minute test. grep 'first minute' lib: none
- [partial] Extend `fm doctor` with a toolchain-manager check (mise, asdf, nvm, pyenv) — grep -w 'mise|asdf|pyenv' lib: only fmcode.py:1278 for runs, none in fmdoctor.py
- [partial] List ambient override variables at every unattended entry — FOREMAN_NOW at fmcore.py:109 read; grep 'FOREMAN_' fmdoctor.py: no entry listing
- [partial] Make `fm doctor` run in each sandbox and list what it didn't check — fmdoctor.py:2412 doubts the PID namespace; grep 'sandbox' fmdoctor.py: no per-harness run

## c09 Draft-ahead legibility and staleness

Mark: **build** · value 3 · effort S · risk low — a draft-ahead exists and is adopted blind; a file-set stamp and a drafted/adopted/expired line make it safe and visible  
Slate: Stamp each draft-ahead doc with a hash of the files it names at draft time, drop it as stale in fmdraft.adopt when they changed, and list waiting, adopted and expired drafts in fm away and the digest.

- [partial] Name overnight drafts as drafted, landed or discarded on the morning card — drafts scored adopted/expired (fmdraft.py:124-137); fm away line (fmaway.py:89) never names drafts
- [partial] Stamp speculative drafts with their file-set hash — draft doc keeps id, keys, plan, cut from HEAD (fmdraft.py:182); no file-set hash, so no stale check against later edits
- [partial] Reserve a "who was I predicting for" tag on lane hand-backs — draft rows carry id and made (fmdraft.py:187) and adopt logs for (:203); ordinary lanes carry no prediction id
- [partial] Wild: Hold an 02:00 "tomorrow rehearsal" that dry-runs the top queue item to a scratch worktree — fmdraft.sweep/cmd_draft (:40, :56) drafts the top queued S task in a throwaway worktree; no clock-time schedule

## c10 Intake quality and prior art

Mark: **build** · value 3 · effort S · risk low — Surfacing the closest existing task at filing prevents duplicate work, and the dropped-task lookup already exists.  
Slate: Make fm capture also print the closest open or done task (by shared words) beside its 'Dropped before' line, so the user sees it when filing.

- [new] Write every task title in plain words and lint for jargon at filing — grep -i 'jargon' plugin/lib: nothing. canary: def main found (fmcli.py:8473)
- [partial] Declare `needs:` when filing and check a host profile — grep 'needs:' in fmcli.py/fmcore.py: 1 hit each, not a host-profile check
- [partial] Recheck a brief's claims when it is picked up, not just when it is filed — fmreverify.py exists (reverifies at close). Pickup-time claim recheck not found
- [new] Replay the same ask in three phrasings and require intake to file one task — grep 'phrasing' in fmexam/fmcli: nothing. canary: def main found (fmcli.py:8473)
- [partial] Show a "closest existing thing" line when a user ask is filed — fm capture prints 'Dropped before: T-0260' (T-0726, CHANGELOG.md:1465). Only drops, not open or done tasks
- [built] Tell questions from requests at intake — T-2554: the user model reads only the user's own asks (fmforesight._requests)
- [new] Attach a generated implied-siblings checklist to every new verb, flag or gauge brief — grep 'sibling' in fmcli.py/fmideas.py: no checklist generator. canary: def main found (fmcli.py:8473)

## c11 Lane hand-backs and attribution

Mark: **build** · value 3 · effort S · risk low — The trailer records only the task; lane and model make later predictions about lane quality possible.  
Slate: Add lane id and model to the Foreman-Task commit trailer written at fmcli.py:2177 and show them in fm outcomes.

- [partial] Give lanes a "blocked by policy" hand-back with the widening command — fmcli.py:8500 Next: lines on exit; grep 'blocked by policy' lib: none for lanes
- [partial] Stamp each lane's landed commit with lane id and model — fmcli.py:2177 Foreman-Task trailer carries task only; grep 'Foreman-Lane' lib: none
- [new] Attach a debugger-evidence lane (DAP) — grep 'DAP|debugger' plugin/lib: none; canary: def main found
- [new] Wild: Offer a pair-programming handback with "I'll watch" — grep 'pair-programming|I.ll watch' plugin/lib: none; canary: def main found
- [new] Let peer Foremen negotiate cross-repo contracts — grep 'peer|cross-repo contract' plugin/lib: none; canary: def main found

## c12 Ledger integrity, stamps and identity

Mark: **build** · value 3 · effort S · risk low — Stamping simulated rows keeps replay and forecast scoring honest.  
Slate: Add a simulated flag to every ledger row written while FOREMAN_NOW is pinned, and have the prediction book skip those rows.

- [new] Redact ledger records in place with chain-preserving tombstones — grep 'tombstone|redact' plugin/lib: none; canary: def main found
- [partial] Stamp records written under a pinned clock as simulated — fmcore.py:109 FOREMAN_NOW pins the clock; grep 'simulated' fmcore.py: none
- [partial] Key project state by repo identity and offer re-attach on move — fmcore.py:285 slug_for keys by path slug; grep 'repo identity|re-attach' lib: none
- [new] Wild: rebuild the task index from git history alone — grep 'rebuild.*index|from git history' plugin/lib: none; canary: def main found
- [new] Emit one typed Verdict record from guard, prove, finish gate and doctor — grep 'class Verdict|Verdict record' plugin/lib: none; canary: def main found
- [built] Write the injection ledger at emit time — fmlib.py:1214 card_injected ledger (near T-0691)

## c13 Proactive digests and nudges

Mark: **build** · value 3 · effort S · risk low — Landed work that was never shipped is a likely next question, and nothing offers it at session end.  
Slate: At session end (Stop hook), when tasks have landed on the work branch but not shipped, print one line naming them with the ship command, silent when nothing is waiting.

- [new] Send a try-it card the moment a capability lands — grep 'try it|try-it' in fm*.py: nothing. canary: def main found (fmcli.py:8473)
- [new] Declare a plateau and go quiet — grep 'plateau' in fmloop/fmgenesis: only loop stop rules, not a declare-and-quiet mode
- [new] Show a standing-intent drift gauge per generation — grep 'drift gauge' in fmgenesis: nothing. canary: def main found (fmcli.py:8473)
- [partial] Digest what reached main under the push grant — fm digest (T-1084) lists decisions made without the user. Pushes under grant not listed. fmgrants.py
- [new] Wild: let the user scrub a week of the tower as a short "season recap" — grep 'recap' in fm*.py: nothing. canary: def main found (fmcli.py:8473)
- [new] Gate generation growth on the user's read receipt — grep 'read receipt' in fmgenesis: nothing. canary: def main found (fmcli.py:8473)
- [new] Offer to ship when a session ends with landed, unshipped work — grep -i 'unshipped|offer to ship' in plugin/lib: none. canary: def main found (fmcli.py:8473)
- [partial] Hold a Sunday-night "week ahead" draft built only from the user's own history — fmforesight prediction_tick predicts one next request. fm digest is weekly. No week-ahead draft

## c14 Ask-pattern mining: series, vocabulary, repeats, ask-debt

Mark: **build** · value 3 · effort M · risk med — Repeats exist; series and new-vocabulary detection foresee the next ask but need a quiet false-positive rate.  
Slate: Extend fm repeats with numbered-series extrapolation and a new-vocabulary check against fm verb names and MASTER.md anchors, shown only above a hit-rate floor.

- [partial] Wild: audit the user's 90 days of asks for needs no slate item ever mentioned — fmrepeats.py:1 mines briefs for repeated hand work; no coverage-gap audit. grep 'never mentioned' lib: none
- [partial] Turn a read-later list into a repo impact digest — near T-2151 recorded list persists; no impact digest. grep 'impact digest' lib: none
- [partial] Propose aliases and git hooks from the user's repeated commands (wild) — fmrepeats.py:1 proposes from repeated briefs; no alias/git-hook output. grep 'alias' fmrepeats.py: none
- [new] Pre-brief each Mission on which user-owned inputs it will need — grep 'user-owned inputs|pre-brief' plugin/lib: none; canary: def main found
- [partial] Wild: let the user say "I keep…" and have Foreman count it — fmrepeats.py:65 repeats_dismissed counts repeats from briefs; no say-it capture. grep 'I keep' lib: none
- [new] Extrapolate numbered series in the user's asks — grep 'numbered series|extrapolat' plugin/lib: none; canary: def main found
- [new] Detect new vocabulary in the user's recent messages that no verb or MASTER.md clause covers — grep 'new vocabulary|unknown term' plugin/lib: none; canary: def main found
- [partial] Collapse the repeated Mission request into one command — fmgenesis.py publish/live (:1219) automates Mission steps; no one-shot Mission request. grep 'mission request' lib: none
- [new] Report ask-debt: asks Foreman now handles unprompted — grep 'ask.debt|unprompted' plugin/lib: none; canary: def main found
- [partial] Wild: Hold a monthly "what did the user have to say twice" report — fmrepeats.py:1 repeated-work report; no say-twice report. grep 'say twice|said twice' lib: none

## c15 Conditional reminders and snooze

Mark: **build** · value 3 · effort M · risk low — defer plus a wake-on-capture exists; a wake predicate is the missing anticipation piece  
Slate: Add fm task defer --until PREDICATE (a date, a task closing, or a CI result) with a reason, and surface the deferred task at fm next and SessionStart when it holds.

- [new] Add conditional reminders: `fm remind when <predicate> "<note>"` — near T-2290 (done) — grep 'remind' in fmcli.py: 0 hits (T-2290 is effort prediction); canary: def main found
- [partial] Snooze with a reason and a wake condition — fm task defer + capture wakes a matching deferred task (fmcli.py:328-336, :1044); no reason field or wake predicate
- [new] Hold non-urgent `fm ask` questions until the user's usual reply window — grep 'reply window|quiet hours' lib: 0 hits; ASK_DAYS=7 is the only timer (fmcli.py:488); canary: def main found
- [partial] Detect expected events that did not happen — fmnight.liveness (:329) names timers with no trigger in three intervals; no general expected-event model
- [partial] Pause on hesitation at an `fm ask` card — near T-0591 (done) — fm pause gaps verbs exist (T-0591); no hesitation timing; not grepped further

## c16 Prediction scoring and shadow predictors

Mark: **build** · value 3 · effort M · risk low — The prediction book exists; logging show-probability and replaying early asks sharpens it cheaply.  
Slate: Record the show-probability on every prediction row and add an fm exam replay of the earliest 100 asks that reports the pre-emption rate.

- [partial] Wild: Turing-test the predictor on the user — fmforesight.py:296 predict scored vs naive baseline; no user-blind test. grep 'turing|blind test' lib: none
- [partial] Count anticipation hits only if the user did not have to be told — fmforesight.py:311 prediction_tick books hits; no told-vs-unprompted split. grep 'unprompted' lib: none
- [partial] Wild: write a letter from the Foreman of a year ago and score what it got wrong — predictions.jsonl write-once rows scored later (fmforesight.py:311); no letter form. grep 'year ago' lib: none
- [partial] Log the show-probability of every anticipation for offline evaluation — grep 'show_prob|probability' fmforesight.py: none; rows log kind and score only (:311)
- [partial] Fit every anticipation window and half-life by backtest on the user's own history — fmexam.py:3253 replay_forecast backtests; windows fixed (AHEAD_DAYS=3). grep 'half.life' lib: none
- [new] Show a prediction only when a conformal set has size one — grep 'conformal|prediction set' plugin/lib: none; canary: def main found
- [partial] Make `fm anticipate` a stateless pure function over the ledgers — fmforesight.predict:296 reads ledgers; grep 'anticipate' fmcli.py help=: no verb
- [new] Use zlib compression distance as the nearest-neighbour finder for asks — grep 'zlib|compression distance|ncd' plugin/lib: none; canary: def main found
- [partial] Replay the first 100 historical asks through today's Foreman to measure the pre-emption rate — fmexam.py:3253 replay_forecast replays history; grep 'first 100|pre-emption' lib: none
- [partial] Write a prospective receipt for each filed task and score it at close — next-request predictions scored (fmforesight.py:311), not per filed task. grep 'prospective' lib: none
- [new] Write tomorrow's expected ledger in the real schema and diff it against the actual one — grep 'expected ledger|tomorrow' fmforesight.py fmexam.py: none; canary: def main found
- [new] Run a weekly tournament of three shadow predictors and let the held-out week choose the live one — grep 'shadow predictor|tournament' plugin/lib: none; canary: def main found

## c17 Ask batching and blocked-list ranking

Mark: **skip** · value 3 · effort M · risk low — fm todo, fm digest and the proxy already cover most of it. The ranking tweak is minor.

- [partial] Coalesce simultaneous `fm ask` questions into one card — fmgrants.py:70-80 dedupes an identical queued ask. Near-identical text from different lanes is not merged
- [new] Reply to Foreman by editing a file — grep 'ask' answer paths: only fm decide --answer. canary: def main found (fmcli.py:8473)
- [partial] Batch every question into one dated decision sheet with a default and a deadline — fm todo (fmcli.py:6399) and fm digest (T-1084) list pending items. No default or deadline
- [partial] Rank the blocked list by what one user action would free — fm todo (T-1157, fmcli.py:6399) lists user-only items. Ranking by unblocked count not verified
- [built] Reuse past answers to process questions — User proxy for repeated asks, T-1064 (CHANGELOG.md:1086)
- [built] Guard the user's own typing (wild) — User proxy T-1064 plus guard asks (CHANGELOG.md:1086); fm decide --answer is user-only

## c18 Mining the user's pending intent

Mark: **skip** · value 3 · effort M · risk med — plausible but speculative; text mining of user words risks noise and privacy

- [partial] Wild: Track asks that went quiet and check whether they were solved or abandoned — fm second ask defers after ASK_DAYS (fmcli.py:488); no solved/abandoned check
- [new] Extract a promise ledger from the user's deferral words — grep 'promise ledger' lib: 0 hits (fmtidy/fmcore 'deferral' is task status); canary: def main found
- [new] Treat the user's own new TODO/FIXME lines and stashes as asks-in-waiting — grep 'TODO|FIXME|git stash' lib: only fmmap scan and guard stash checks; canary: def main found
- [new] Mine the finish text's own caveats as predicted asks — grep 'caveat' fmhooks.py not run; canary: def main found
- [partial] Look up what followed the nearest past asks (local TF-IDF) — fmdraft._keys word/path overlap (fmdraft.py:110) picks the closest past request's plan; no TF-IDF or follow-up lookup
- [new] Mine editable event→ask rules — fmnight/fmtriggers have fixed triggers; grep 'event.*ask' unrun; canary: def main found

## c19 Per-model pre-warning

Mark: **skip** · value 3 · effort M · risk med — Routing already picks the model by rework rate. A warning adds injected text, against the burden steer (T-2667).

- [partial] Inject a per-model, per-task-kind pre-warning only where that model has failed three or more times — fmlanes.py:1440,1492 route probes by rework rate per tier. A pre-warning injection was not found in fmmodels.py

## c20 Pre-answering what the user will ask on reading

Mark: **skip** · value 3 · effort M · risk low — each item is small and uncertain; none is proven wanted

- [new] Stamp each filed item with the first-screen question it expects the user to ask — grep 'first.screen' fmcli.py: 0 hits; canary: def main found
- [partial] Pre-answer "did it do what I meant" with their own sentence beside the evidence — fm task prove and criteria quote the request (fmcli.py:2381); no verbatim-sentence-beside-evidence line
- [new] Say what a close unblocked — near T-2648 (done) — grep 'unblocked' fmcli.py not found in close path; canary: def main found
- [new] Estimate review minutes a day's work asks of the user — grep 'review minutes' lib: 0 hits; canary: def main found
- [new] Wild: name an "ask under the ask" at intake — fm intake exists (fmcli.py:300); no hidden-ask step; canary: def main found
- [partial] Explain every cost outlier on its receipt — fm cost --task shows spent, cap and forecast (fmcli.py:6874); no per-outlier explanation

## c21 Privacy and outbound hygiene

Mark: **skip** · value 3 · effort M · risk med — valid hygiene but off the anticipation mission

- [new] Learn per-path sensitivity from the user's own redactions and overrides — meta 'sensitive' is a manual flag (fmforesight.py:317); canary: def predict found
- [new] Wild: Add a local sensitivity red team that guesses what private facts each new pack section reveals — grep 'red team' lib not found; canary: def main found
- [new] Build outbound packs from a field allowlist — grep 'allowlist' fm{pack,cli,serve}*.py inconclusive; canary: def main found
- [new] Pseudonymise identifiers in every outbound model prompt — grep 'pseudonym' lib: 0 hits (c.redact only, fmdraft.py:168); canary: def main found
- [partial] Give every verbatim-user-text store a retention clock — fmtidy rotates hooks.log by size (fmtidy.py:688); no per-store retention for user text

## c22 User-model and steer learning

Mark: **skip** · value 3 · effort M · risk med — Mostly partial or speculative, and many are wild. No single grounded item beats the other builds.

- [new] Wild: let the user veto a past Foreman decision and replay the run without it — grep 'veto' in fmcli.py: only a correction veto (T-0251). No replay. canary: def main found (fmcli.py:8473)
- [partial] Wild: grade Foreman's work by a stand-in for the user's taste, trained on their drops — fmtaste.py taste ledger (T-1520, T-1537) learns from kept and dropped work
- [built] Learn what "simplify" means for this user — T-1537 taste ledger, fmtaste.py
- [partial] Give each steer a review-by date and an evidence query (wild) — fm decide --sunset (T-1084, CHANGELOG.md:1098) gives decisions an expiry. No evidence query
- [new] Keep a "what I assumed about you" file the user can strike through (wild) — grep -i 'assumed about' plugin: nothing. canary: def main found (fmcli.py:8473)
- [partial] Fold repeat user corrections into the next pack's "do not repeat" slice — fmrepeats.py exists. Whether it feeds the next pack's slice not verified
- [partial] Keep a promise ledger — The taste ledger (T-1537) keeps what the user kept. A ledger of promises Foreman made was not found
- [partial] Detect a bad stretch and go quiet — fm drive --stall-usd (MASTER.md:185, T-2669) stops after spend with no close. Not a quiet mode
- [partial] Ratify costly decisions the user never vetoed — fm digest lists costly decisions once under review (CHANGELOG.md:1098). No ratify step
- [new] Log the waits the user feels — grep -i 'wait' fmdoctor/fmcost: hook SLO misses only, not user-felt waits. canary: def main found (fmcli.py:8473)
- [new] Pre-run the user's habitual first commands — grep -i 'prefetch|habitual' plugin/lib: nothing. canary: def main found (fmcli.py:8473)
- [new] Whisper when the user opens a file a deferred task covers — grep -i 'deferred' in fmhooks: nothing. canary: def main found (fmcli.py:8473)
- [partial] Reopen an unattended decision when its premise changes — fm decide --revisited/--reverses and sunset (fmcli.py:4248). Premise-change trigger absent

## c23 Work ahead of the ask

Mark: **skip** · value 3 · effort M · risk med — Draft-ahead scores adopted or expired already; extras are speculative.

- [partial] Pre-merge the futures — fmdraft.py:106 draft-ahead branch; never merges (expires day 3). grep 'pre-merge' lib: none
- [partial] Prototype both options of a stalled user decision overnight (wild) — fmdraft.py:140 drafts one predicted task; grep 'both options' fmdraft.py: none
- [new] Land unattended work on a probation ref — grep 'probation' plugin/lib: none; canary: def main found
- [new] Finish the safe tail of an interrupted session — grep 'safe tail|interrupted session' plugin/lib: none; canary: def main found

## c24 Upstream and request-versus-repo checks

Mark: **skip** · value 3 · effort L · risk med — network and per-ecosystem parsing; the request-names-missing-things check is the only cheap piece

- [partial] Fetch upstream on every tick and flag queued tasks it just invalidated — tick fetches CI/issues only when watched (fmnight.py:6, fmforesight.refresh); no upstream-vs-queue check
- [new] Warn when a request names things the current repo doesn't have — grep 'names things|not in this repo' fmhooks.py: 0 hits; canary: def main found
- [partial] Wild: Brief the user once a month on upstream deprecations and end-of-life dates for their own dependencies, runtimes and CI actions — fmmodels.py:75-85 tracks model retirements only; fmtidy.py:301 sunset is for Foreman's own; no dependency/runtime EOL

## c25 Brief hygiene and decision intake

Mark: **skip** · value 2 · effort S · risk low — Mostly covered by capture checks and the deadline field.

- [built] Lint a new brief against the other open briefs for contradictions — near T-0438: capture flags a re-ask of dropped work and a veto contradiction
- [partial] Fold co-filed same-file briefs into one task with a checklist — capture flags overlap (T-0438); grep 'fold|co-filed' fmcli.py: none
- [new] Quarantine "dropped with a noted remainder" into a visible one-line shelf — grep 'noted remainder' plugin/lib: none; canary: def main found
- [partial] Gate every brief on a 90-day incident count — near T-2610 calibration reads compare like with like; no brief gate. grep 'incident count' lib: none
- [partial] Add a one-word cost-of-delay field to tasks — fmcore.py deadline: field exists; grep 'cost.of.delay' lib: none
- [new] Answer one dated decision sheet by editing a file — grep 'decision sheet' plugin/lib: none; canary: def main found

## c26 Genesis site and tower publish

Mark: **skip** · value 2 · effort S · risk low — Cold read is built; quarantine guards publish, not foresight.

- [partial] Quarantine the site's data publish when a user-authored ask is in the diff — fm genesis live (fmgenesis.py:1219) has a leak scan; grep 'user-authored' fmgenesis.py: none
- [built] Hold tower files in a pending state until their cold read lands — fmgenesis.py:281 cold read for tower writes
- [new] Wild: run a release radar from drift hashes — grep 'release radar|drift hash' plugin/lib: none; canary: def main found

## c27 Hand versus Foreman precedence

Mark: **skip** · value 2 · effort S · risk low — A documentation and test task. It is not anticipatory.

- [partial] Make a hand edit win, and say so — T-0400 builder briefs say edit with Edit/Write. fmlandlock.py exists. Hand-vs-Foreman conflict rule not read
- [new] Check which side wins when the user's hand and Foreman both change tree, queue or ledger — grep -i 'precedence' in fmcore/fmlanes: nothing. canary: def main found (fmcli.py:8473)
- [new] Settle hand-vs-Foreman precedence in one table — grep 'who wins' MASTER.md: nothing. canary: def main found (fmcli.py:8473)

## c28 Lane hand-back fields

Mark: **skip** · value 2 · effort S · risk low — Follow-ups are already recorded via --followups. Extra mandatory fields add friction.

- [partial] Require a "not checked" field in every lane hand-back — grep 'not checked' fm*.py: fmauditrun, fmcritique, fmdoctor have it, and fm-reviewer.md/fm-recon.md agents do too. No merge-time rejection seen
- [partial] Require a lane to hand back "what the user will ask about this" in two lines — fmcli.py:6624 --followups 'Q => A' (T-0639) gives likely follow-ups for tasks; not required of lanes

## c29 Prediction book and hygiene (built)

Mark: **skip** · value 2 · effort S · risk low — mostly built; the remainder is marginal

- [built] Retire the predictor when it loses to the baseline — near T-2449 (done) — mute at MUTE_MIN when hit < baseline, fm outcomes --predictions/--unmute (fmforesight.py:371, fmcli.py:6777-6779)
- [built] Record every anticipation as its own ledger class with an outcome — write-once rows kind next-request/score/draft in predictions.jsonl (fmforesight.py:230, :342, fmdraft.py:135)
- [built] Score the Genesis site's hit rate on user-authored asks only — near T-2505 (done) — _requests(clean=True) drops tower and non-user briefs (fmforesight.py:254-261, T-2554); fmgenesis.py:3674 scores user steers
- [partial] Settle predictions by the first thing touched next session — scored against the next user request incl. its touched files (fmforesight.py:325-336); not session-start touches
- [partial] Keep the predictor local-only and show what it read — near T-0871 (done) — reads only this project's briefs and ledger, sensitive skips (fmforesight.py:312-319); nothing shows what it read
- [new] Tag each prediction with a horizon and score it against that horizon only — near T-0690 (done) — grep 'horizon' fmforesight.py: 0 hits (one fixed horizon: next request); canary: def predict found

## c30 Prediction book, baseline and mute

Mark: **skip** · value 2 · effort S · risk low — The core book, baseline, mute and doctor line are built (T-2406, T-2409). What is missing is delivery.

- [built] Score a recency baseline first — fmforesight.py:343 books 'base' (the last request) beside each prediction; fmforesight.py:352 prediction_kinds
- [built] Predict by task-kind follow-up table — fmforesight.predict (fmforesight.py:296) uses the user's type transitions (T-2409)
- [partial] Treat drops as negative evidence — _SLIP (fmforesight.py:234) excludes tasks dropped by mistake. Other drops are not used as negative evidence
- [built] Wild: let the predictor retire itself — MUTE_MIN (fmforesight.py:231); a kind that trails its baseline is muted
- [partial] Wild: let the predictor retire itself once it stops beating its baseline for 30 days — Muting is by count (MUTE_MIN=20 scored rows), not a 30-day window. fmforesight.py:231
- [built] Put a hit-rate line in `fm doctor` and mute any predictor below its baseline — fmdoctor.check_predictions (fmdoctor.py:582); mute in fmforesight.py:371
- [partial] Book every anticipation as a sealed prediction with a recency baseline and a mute — next-request and draft-ahead kinds are booked (fmforesight.py:387). Other anticipations (CI, setup changes) are not
- [new] Wild: sell the prediction back as a bet — grep -i 'bet' predictions code: nothing. canary: def main found (fmcli.py:8473)
- [partial] Wild: keep a trust-the-prediction dial the user can see and set — fm outcomes --predictions --unmute KIND (fmdoctor.py:595) is a mute switch. No visible dial
- [built] Learn predictor rules from the asks that surprised the ledger — T-2076 blind spots (CHANGELOG.md:401) turn missed asks into questions for the next brainstorm

## c31 Self-describing docs and help

Mark: **skip** · value 2 · effort S · risk low — Docs hygiene. Not anticipation.

- [new] Rebuild a module from MASTER.md alone — grep 'rebuild' in fmcli.py/fmdocs.py: nothing. canary: def main found (fmcli.py:8473)
- [new] Mine `--help` examples from real invocations — grep 'help examples' in fmdocs/fmcli: nothing. canary: def main found (fmcli.py:8473)
- [partial] Lint that every verb has a MASTER.md anchor with a "use when" line — fmdoctor.py:553-554 'file map' check ties files to the map. T-2659 grounding step. Verb anchor lint not found

## c32 Stuck-loop and retry detection

Mark: **skip** · value 2 · effort S · risk low — Error-fingerprint stop is built; n-grams add little.

- [partial] Detect stuck loops from tool-call n-grams — fmcore.py:3835 stall exists; grep 'n-gram' fmcore.py: none
- [built] Stop a retry loop by its error fingerprint — fmserve.py:976 fingerprint and _repeat_key

## c33 Anticipation delivery, arbitration and export

Mark: **skip** · value 2 · effort M · risk med — premise is a card that is not injected anywhere; the useful part is built in the first cluster

- [false-premise] Record whether the anticipation card reached the agent — no anticipation card is injected: grep 'anticipat' lib hits only fmgenesis/fmcli steer scoring; fmforesight.lines (:197) has no prediction
- [false-premise] Gauge card age at the user's first keystroke — no card exists; predictions are written by the tick (fmforesight.py:311) and read by nothing at prompt time
- [partial] Test the anticipation card across ledger gaps and a clock jump — test_foresight.py covers the book; prediction_tick orders by request ids not time (fmforesight.py:324), so a clock jump barely applies
- [partial] Precompute forecasts in the tick and read a file at session start — near T-2356 (done) — tick precomputes (fmnight.py:388, fmforesight.refresh) but session start (fmforesight.lines :197) reads no prediction
- [partial] Show an honest "I can't read you this week" state — sensitive project predicts nothing silently (fmforesight.py:317); no stated reason or sparse-history state
- [new] Arbitrate every anticipation through one slot per surface — grep 'slot|arbitrat' fmforesight, fmtriggers, fmhooks: none for anticipation; canary: def main found
- [partial] Run one anticipation governor — fmtriggers.row(p,'draft-ahead')['route'] mute route (fmdraft.py:152) and MUTE_MIN (fmforesight.py:371) are per-kind governors
- [new] Allocate the single anticipation slot with a bandit — grep 'bandit' lib: 0 hits; canary: def main found
- [false-premise] Export the anticipation card into AGENTS.md and GEMINI.md — no card; fmagents.py:205-214 only names rules files for codex/gemini installs
- [false-premise] Prime other harnesses with the anticipation card — no card to prime with (see fmforesight.lines :197); fmagents carries rules and hooks only

## c34 Blind-spot question bank and brainstorm steering

Mark: **skip** · value 2 · effort M · risk low — Bank is built; remaining items improve brainstorm quality, not foreseeing the user's next need.

- [built] Keep a durable blind-spot question bank that every lens must answer — fmgenesis.py:915 blind-spots.md act; fmideas.py:44 blind spots lens
- [partial] Tag every filed item with which brainstorm question would have caught it — fmgenesis.py:915 keeps questions; grep 'would have caught' lib: none
- [new] Wild: pay a different-vendor model to find gaps from `fm --help` alone — grep 'vendor|--help alone' fmgenesis.py fmideas.py: none; canary: def main found
- [partial] Mark the pack's sections with the question each one answers for the lens — fmideas.py:44 lens notes exist; grep 'answers for' fmideas.py: none
- [partial] Replace "ideas so far" with a verb-and-idea coverage grid — grid lens in fmideas.LENS_NOTES (T-2672) covers cells; grep 'ideas so far' lib: still listed
- [new] Let the user strike an idea mid-brainstorm and re-aim the remaining lenses — grep 'strike|re-aim' fmideas.py skills/brainstorm: none; canary: def main found
- [new] Mine other agent trackers for bug classes Foreman hasn't asked about — grep 'agent tracker|bug class' plugin/lib: none; canary: def main found
- [partial] Wild: Name the blind-spot class on every user-filed FIX at intake — fmgenesis.py:915 bank exists; no intake tagging. grep 'blind.spot' fmcli.py capture: none

## c35 Cold start and cross-repo transfer

Mark: **skip** · value 2 · effort M · risk high — cross-repo pooling mixes private data; one user's history rarely warrants it

- [new] Seed predictors with stack-card priors for repos with no history — near T-0706 (done) — stack card exists (fmscout.py:2, fmwhich.py:100) but predict (fmforesight.py:296) takes no prior; canary: def predict found
- [new] Ship a cold-start prior for fresh installs — prediction_tick returns None without requests (fmforesight.py:320); canary: def predict found
- [new] Transfer habit predictions across the user's repos — predictions are per project; prediction_tick reads only this project (fmforesight.py:316); canary: def predict found
- [new] Pool follow-up tables across the user's registered repos — fmforesight._requests is per-project (:253); canary: def predict found
- [partial] Sync forecast tables, never ledgers, between the user's machines — fmsync.py mirrors state across machines; no forecast-table-only mode; not read further
- [partial] Predict from coverage-grid neighbours — near T-2093 (done) — fmforesight.py:316 notes 'no co-change neighbours yet'; foresight-cochange warning exists (:390)

## c36 Cost of ownership of rules and catalogue

Mark: **skip** · value 2 · effort M · risk low — Meta-accounting. It does not help the user next.

- [partial] Report the cost of ownership of Foreman's own standing rules — fm cost and the burden fix (T-2667) count injected text. Per-rule ownership cost not found
- [partial] Write a behaviour changelog of what the model is told — fm audit prep --note (T-0031) records round notes. Not a changelog of injected text
- [partial] Make a catalogue entry carry its use evidence (wild) — T-1084 sunset clauses. fm outcomes tracks use. Per-entry evidence not found
- [partial] Hold a lesson-trial court that sentences rules to expire (wild) — fm decide --sunset (CHANGELOG.md:1098) expires decisions. Rules as trials not found
- [partial] Count hours given back, net of false alarms — fmtriggers.py:285-299 reports predictions beside baselines. Hours and false alarms not counted
- [new] Record effort before and after grounding, per lens — grep -i 'before and after grounding' plugin: nothing. canary: def main found (fmcli.py:8473)
- [partial] Mine Foreman's own follow-up fixes as missed anticipation — T-2076 blind spots list the user's asks that no idea predicted (CHANGELOG.md:401). Foreman's own follow-ups not mined

## c37 Doctor reach and hermetic runs

Mark: **skip** · value 2 · effort M · risk med — Harness-parity and test hygiene. Little anticipation value.

- [new] Run `fm doctor` from inside each harness's own sandbox — grep sandbox/harness in fmdoctor.py: no per-harness reach table. canary: def main found (fmcli.py:8473)
- [new] Show a headless-safe line for a missing Desktop tray dependency — grep 'appindicator' in plugin/lib: nothing found. canary: def main found (fmcli.py:8473)
- [built] Run a zero-token self-explaining doctor (wild) — fmdoctor.py has 2600+ lines of local checks, with the fix command named in each result
- [partial] Run the suite and hooks under a different uid, an unset HOME and a path with spaces — grep 'HOME' in fmdrill/fmsmoke: fake-home scratch exists. Different uid and spaced paths unverified
- [partial] Fire every never-fired hook, verb and guard rule once in a scratch home — fm bench guard --coverage (MASTER.md:547) and fmsmoke cover guard rules. Verbs and hooks not seen

## c38 Drift and hand-edit conflicts

Mark: **skip** · value 2 · effort M · risk med — Quality checks, not foresight of the user's next need.

- [new] Hand-wins precedence table with a surfaced conflict — grep 'hand-wins|precedence table' plugin/lib: none; canary: def main found
- [partial] Run the `fm` commands quoted in skills against a scratch home — near T-1458 guard reads quoted names; no scratch-home run. grep 'scratch home' lib: none
- [new] Check which side wins when hand edits and Foreman edits meet, per file class — grep 'hand edit|file class' plugin/lib: none; canary: def main found
- [partial] Check `.env.example`, config reads and docs for drift — fmdoctor.py has drift checks for hooks/docs; grep '\.env\.example' lib: none
- [new] Lint the user project's UI strings for terminology and tone — grep 'terminology|ui strings' plugin/lib: none; canary: def main found

## c39 Drills, replay and fault days

Mark: **skip** · value 2 · effort M · risk low — Drill machinery is built; extras test resilience, not foresight.

- [partial] Replay the user's worst day on every release — fm drill (fmdrill.py, T-1669) runs fault days; grep 'worst day' lib: none
- [new] Wild: plant a wrong fact in a skill each week and time its discovery — grep 'plant|canary fact' plugin/lib skills: none; canary: def main found
- [built] Run compound-fault drills in pairs — near T-1669: fm drill compound fault days in a temp home
- [new] Diff every cache against its uncached twin nightly — grep 'uncached' plugin/lib: none; canary: def main found
- [new] Wild: Run the user's project under network and clock chaos during a proof — grep 'chaos' plugin/lib: none; canary: def main found
- [partial] Wild: have a Murphy child write the 3am sequences from MASTER.md — fmdrill.py compound faults hand-written; grep 'murphy' lib: none
- [partial] Wild: run a monthly fire drill for the human — fm drill exists (fmdrill.py); grep 'monthly' fmdrill.py: none
- [new] Wild: Run a "stranger's first PR" drill against the guard's timing — grep 'stranger' plugin/lib: none; canary: def main found
- [partial] Replay the worst-day ledger, and let the user veto a decision and replay — fmexam.py:3253 replay_forecast; no veto-and-replay. grep 'veto' fmexam.py: none

## c40 Effort and attention signals

Mark: **skip** · value 2 · effort M · risk med — the 3x alarm exists; the rest needs new sensors

- [partial] Raise a mid-flight overrun alarm at a fraction of the median cost — fm next notes once at 3x the prediction (fmcli.py:6009-6016, T-2290); no earlier fraction
- [new] Offer time-boxed work bundles — grep 'time.?box' lib: only regex budget; canary: def main found
- [new] Split-offer oversized forecasts at pick time — grep 'oversized' lib: 0 hits; fmcli.py:3688 sets prediction at focus; canary: def main found
- [new] Add a frustration key that captures the state it was pressed in — grep 'frustration' lib not found; canary: def main found
- [new] Dowse attention from the compositor and editor state (wild) — grep 'compositor' lib: 0 hits; canary: def main found
- [new] Show the user's open editor buffers as a next-ask hint, opt-in and local — grep 'editor buffer' lib: 0 hits; canary: def main found

## c41 Failure atlas and worst-day replay

Mark: **skip** · value 2 · effort M · risk low — Test and visual machinery. Does not act ahead of the user.

- [new] Wild: Mint a grid cell from "this surprised me" — grep 'grid cell|coverage.md' in fm*.py: nothing. canary: def main found (fmcli.py:8473)
- [new] Wild: Open a failure atlas as the web UI's home — grep 'atlas' in fm*.py: nothing. canary: def main found (fmcli.py:8473)
- [partial] Wild: Replay a recorded worst-day ledger through every surface on each release — fmdrill.py:73,272 drills a day with crash and hooks.log counts. fm replay (MASTER.md:228) replays the guard only
- [partial] (wild) Hold a weekly "what surprised me" interview with a cold child that has only the last week's ledger — fmexam.py cold-child exams, T-2341 rival. No weekly interview
- [new] (wild) Keep a "nobody asked, nobody noticed" shelf of Foreman's own silent behaviours, each with a check that someone would notice if it broke — grep -i 'nobody noticed' plugin: nothing. canary: def main found (fmcli.py:8473)
- [built] (wild) Play the user's recent asks back as a test the harness must pass — fmexam forecast replays the user's own request stream (fmexam.py:781)

## c42 Faults, locks and landing hardening

Mark: **skip** · value 2 · effort M · risk med — reliability work with no anticipation angle

- [new] Detect refile livelock in the self-advancing tower — grep 'livelock|refile' lib: 0 hits in fm{core,tower,land,lanes}; canary: def main found
- [partial] Open a landing breaker with a cooldown after a red main — fmhooks.py:75-96 has a hook breaker, not a landing one; not read further
- [partial] Clear provably stale lockfiles — fm doctor detects stale locks (fmdoctor.py:2253-2534; fmdrill KINDS 'stale lock'); clearing not confirmed
- [partial] Mirror ledgers continuously to a second filesystem — fmsync.py mirrors state (fmsync.py:1-307); continuous mode not checked
- [partial] Share one retry budget and jitter across all lanes — jitter in fmpage.py:331, fmdoctor.py:214; no shared lane-wide budget
- [new] Drill a split-brain with two Foremen on one repo (wild) — fmdrill.KINDS (:17) lacks it; canary: def main found
- [partial] Run a ledger kill-point sweep on the real writers — fm drill plants torn ledger/journal (fmdrill.py:17); no per-writer kill sweep
- [new] Make grant spending two-phase — fmbudget.reserve exists for exam spend (MASTER T-2292); grants not checked; canary: def main found
- [new] Generate a runbook line per drill fault — near T-2648 (done) — fmdrill.KINDS (:17-18) incl. 'dropped class' present; no runbook generation; canary: def main found

## c43 Gauge claim-consumer sealing and reader forecast

Mark: **skip** · value 2 · effort M · risk low — Process rule for builders; state-growth forecast already built.

- [partial] Seal the claim–consumer pair on every new gauge — gauge is Mission vocabulary; grep 'gauge' plugin/lib: none; claims checked per task by fm evidence
- [partial] Ledger-gap anticipation: forecast the day each reader goes wrong — fmforesight.breakage_tick:531 warns on state growth; no per-reader forecast. grep 'reader goes wrong' lib: none
- [partial] Check at close that a gauge's own test would fail on the unit it replaced — near T-0679; fm ship replays builder lanes (fmcli ship); no unit-swap check. grep 'unit it replaced' lib: none
- [new] Wild: Fail a gauge's tests unless it knows its own zero — grep 'own zero|knows its zero' plugin/lib plugin/tests: none; canary: def main found

## c44 Grounding lexicon and canary measurement

Mark: **skip** · value 2 · effort M · risk low — Serves brainstorm tooling; no user-facing foresight.

- [partial] Learn phrasing aliases from every "already built" drop — near T-2659 three phrasings in skills/brainstorm/SKILL.md:15; no alias store. grep 'alias' SKILL.md: none
- [partial] Log every grounding canary result to measure the search's own recall — T-2674 canary rule in SKILL.md:15; results kept in output, no log. grep 'canary' lib: none
- [partial] Build a grounding lexicon from help strings and MASTER anchors — near T-2659 asks for MASTER.md files; no lexicon file. grep 'lexicon' plugin/lib: none
- [partial] Feed every "already built" drop back into the lexicon — near T-0684; no lexicon to feed. grep 'lexicon' plugin/lib: none
- [new] Rescore dropped ideas only when new incidents appear — grep 'rescore|dropped ideas' plugin/lib: none; canary: def main found
- [partial] Look back at the last Mission's use counts when the next one opens — Mission 6 use counts are reported by hand in T-2677 brief; no auto lookback. grep 'use counts' lib: none
- [partial] Carry follow-up measurements into the next Mission's brief automatically — near T-2392 carried a reply check; no Mission-to-Mission carry. grep 'follow-up measure' lib: none

## c45 Learned preferences and ceremony

Mark: **skip** · value 2 · effort M · risk med — broad and weakly tied to foreseeing the next ask

- [new] Ask what "simplify" means once, then store it as a measurable preference — grep 'simplify' lib not found as a preference; canary: def main found
- [partial] Learn ceremony per task kind from the user's turns-to-close — near T-0680 (done) — fmoutcomes closes keep per type/tier stats (fmcli.py:941); no ceremony tuning
- [new] Gate ceremony on a learned regret score — grep 'regret' fmforesight.py: 0 hits; canary: def predict found
- [new] Compute lesson confidence with zero tokens (unblock T-0217) — not grepped (task-specific); canary: def main found
- [new] Cross every verb and hook with the four recurring blind-spot questions — not grepped; a fmexam blind-spot kind exists in Genesis; canary: def main found
- [new] Reset the stall clock only on closes whose diff survives 24 hours — STALE_DAYS counts 'updated' (fmforesight.py:188); no survival check; canary: def predict found
- [partial] Make every Done-when carry a one-line vacuous-pass sentence — near T-2636 (done) — fm task prove --vacuous exists (fmcli.py:2381-2497); not a required sentence per Done-when
- [new] Keep the catalogue's use evidence next to each entry — near T-0775 (done) — not grepped in depth; canary: def main found
- [new] Collapse the catalogue into a "what I'd actually do Monday" list of five — grep 'Monday' lib: 0 hits; canary: def main found
- [new] Precedence table for hand vs Foreman edits — near T-1652 (done) — not grepped in depth; canary: def main found
- [new] Wild: reverse-engineer the pack from the slate — not grepped; canary: def main found
- [partial] Wild: file one "what I suspect I'm wrong about" item per day — fm surprise logs where the model was wrong (fmcli.py:662); no daily self-suspicion item
- [false-premise] Show a minutes-saved estimate before enabling anticipation — no anticipation switch to enable (grep 'anticipat' lib hits Genesis scoring only)

## c46 Predictor evaluation extras

Mark: **skip** · value 2 · effort M · risk low — measurement polish on a predictor whose output is not yet shown

- [partial] Build a leave-one-out backtest for any predictor — fm exam forecast_replay holds out the last third (fmexam.py:2645-2658); fmbacktest.py is a rule/card backtest, not a predictor one
- [new] Rank forecasts by regret, not likelihood — grep 'regret' fmforesight.py: 0 hits; canary: def predict found
- [new] Hold out anticipation to measure induced demand — grep 'induced|holdout' fmforesight.py, fmdraft.py: 0 hits; canary: def predict found
- [new] Show a forecast only when two independent predictors agree — fmforesight.predict is the only next-request predictor (:296); canary: def predict found
- [new] Test the forecaster for memorising secrets — grep 'secret' fmforesight.py: 0 hits; fmdraft uses c.redact (:168); canary: def predict found
- [new] Wild: write a "why I was wrong" line when a confident prediction misses — score rows hold hits and overlap only (fmforesight.py:333); no confidence or miss cause; canary: def predict found
- [partial] Score Foreman's surprise to the user before any costly decision — fm surprise logs expected→observed (fmcli.py:662); no pre-decision score
- [partial] Wild: Publish a "surprise index" for each week: how much of what the user asked wasn't predictable from the ledger — per-steer hit and miss scoring exists (fmgenesis.py:3674, fmcli.py:4318); no weekly index
- [new] Open 90-day project predictions and settle them on the date — grep '90.day' lib: 0 hits; canary: def main found
- [new] Wild: Forecast the user's complaint a month ahead and score it — grep 'complaint' lib: 0 hits; canary: def main found

## c47 Predictor inputs

Mark: **skip** · value 2 · effort M · risk low — The bigram predictor works. Richer inputs have no evidence they would beat the baseline.

- [partial] Mine ask-sequence n-grams from the ledgers — fmforesight.predict uses bigram type transitions. No longer n-grams (fmforesight.py:303-306)
- [partial] Fire anticipation from external events, not history — fmforesight.ci_main (fmforesight.py:70) flags red CI from the network. Other events not wired
- [built] Reuse the host's own history — T-2321: long goals replayed from Foreman's own history (CHANGELOG.md:228)
- [partial] Wild: replay the user's week and predict only the gaps — fmexam.py:781 holds out the last third of the stream and predicts it. Gap-only scoring not seen
- [new] Count what the user types after Foreman's last output — grep -i 'types after|after.*last output' fmforesight/fmhooks: nothing. canary: def main found (fmcli.py:8473)
- [partial] Keep only normalised n-grams and task ids, not raw asks — predictions.jsonl rows hold type and paths only (fmforesight.py:342-343). The brief text is not stored there
- [built] Run a cold child that tries to be surprised — T-2341 cold rival reads the request (Mission 5, #2); fmexam.py

## c48 Prefetch and read caching

Mark: **skip** · value 2 · effort M · risk med — nothing is prefetched today and the premise (predicted commands) is false; speculative latency work

- [new] Prefetch read-only verb output from verb-transition counts — near T-0276 (done) — grep 'prefetch|verb.transition' lib: 0 hits; canary: def main found
- [false-premise] Prove a prefetched verb is read-only — near T-2461 (done) — no prefetch exists (grep 'prefetch' lib: 0 hits), so there is nothing to prove read-only
- [partial] Serve hash-keyed digests of big files in place of repeat full reads — MASTER.md names read memos (Cost, usage and performance section); not hash-keyed digests; not checked further
- [new] Prime session-start caches from the previous session's first reads — grep 'prime|first reads' fmhooks.py, fmforesight.py: none relevant; canary: def main found
- [new] Cache claim-resolution results by tree hash — grep 'claim.resolution|tree hash' lib not run in depth; canary: def main found
- [new] Bench hook start on a cold page cache — grep 'page cache' in fm{guard,hooks,bench}*.py: 0 hits; canary: def main found
- [new] Normalise timing-test bars by a same-process reference loop — grep 'reference loop' lib: 0 hits; canary: def main found
- [false-premise] Tag each predicted next command with the guard's verdict — near T-1289 (done) — predictions are request type+paths (fmforesight.py:342), never shell commands, so no command reaches fmguard.check

## c49 Recurring rituals and periodic asks

Mark: **skip** · value 2 · effort M · risk med — needs a long history of repeats; Foreman has no scheduling of user asks

- [new] Detect the user's recurring rituals and propose them as scheduled tasks — grep 'ritual|periodic' lib: only fmincident/fmrelease (release ritual); canary: def main found
- [new] Detect periodic asks and schedule them — grep 'periodic|recurring ask' lib: 0 hits; fm night stages timers (fmnight.py:136) but not from asks; canary: def main found
- [new] Wild: alert on a missing ritual — grep 'missing ritual' lib: 0 hits; canary: def main found

## c50 Repo chores learned from the project

Mark: **skip** · value 2 · effort M · risk low — Co-change learning is built; the rest is housekeeping.

- [partial] Janitor lane worktrees, branches and stashes — near T-0803 lanes start from the working branch; grep 'janitor|stash' lib: no sweep
- [built] Learn a repo's change-completeness conventions — fmforesight.py:449 _cochange warns of co-change files
- [new] Wild: Map bus factor and queue the docs tasks — grep 'bus factor' plugin/lib: none; canary: def main found

## c51 Speculative pre-work and scheduling

Mark: **skip** · value 2 · effort M · risk med — Pre-drafting and branch expiry are built. A calendar needs the user to give access, and the rest is speculative.

- [built] Pre-draft the top predicted ask during idle quota — fmdraft.py:141-168 plans the top prediction ahead as DRAFTED-AHEAD.md while the kind beats its baseline (T-2407)
- [built] Confine speculative overnight work to a branch that expires in 3 days — fmdraft.py:106 AHEAD_DAYS=3; draft/ahead-ID branch, never pushed or merged (fmdraft.py:142-149)
- [new] Wild: read a local calendar file to plan unattended work around the user's day — grep -i 'calendar' plugin/lib: only a systemd OnCalendar line in fmnight.py:136. canary: def main found (fmcli.py:8473)
- [partial] Wild: seal tomorrow's three likely asks at day close and show only the hits — The book seals one next-request prediction (fmforesight.py:342). No top-three or day-close reveal

## c52 Surface robustness and degraded-state visibility

Mark: **skip** · value 2 · effort M · risk low — hardening, not anticipation

- [new] Run readers under shuffled determinism inputs — not grepped in depth; canary: def main found
- [new] Snapshot `--json` schemas and gate breaking changes — near T-1790 (done) — grep 'json.?schema' fm{cli,serve,exam}*.py: 0 relevant; canary: def main found
- [new] Run hooks and verbs from a deleted, unreadable or symlinked cwd — not grepped in depth (fmdrill has an 'unreadable' fault); canary: def main found
- [new] Soak the long-lived web server — grep 'soak' fmserve.py: 0 hits; canary: def main found
- [new] Fuzz the verbs with an impatient user in a pty (wild) — grep 'pty' lib: no fuzz; canary: def main found
- [partial] Replace guard regexes with a linear-time matcher — rule matching is time-boxed by RULE_BUDGET with SIGALRM (fmcore.py:3378); not linear-time
- [partial] Gauge Foreman's tmpfs footprint and daily write volume — fmforesight._state_bytes/_state_days (:412-477) forecast state growth; tmpfs and write volume not covered
- [partial] Print a degraded line after any fail-open — fail-open logs to hooks.log (fmhooks.py:3, :184), surfaced by fmfriction (fmfriction.py:209-219); no inline line
- [new] Test the first minute after a silent fail-open — fmdrill checks hooks.log tracebacks (fmdrill.py:272), not the first-minute user view; canary: def main found

## c53 Test-quality and evidence lanes

Mark: **skip** · value 2 · effort M · risk low — Verification built; not about foreseeing the user.

- [built] Revert-replay every FIX commit's test — near T-2054: fm ship replays merged builder lanes at the branch's first commit
- [new] Watch a manual debugging session and write the regression test afterwards (wild) — grep 'debugging session|watch.*regression' plugin/lib: none; canary: def main found
- [built] Pin legacy behaviour with characterization tests before editing — near T-1503 engineering playbooks include characterization tests
- [partial] Write tests for surviving mutants — near T-1953 fm ship remembers --test; grep 'mutant' plugin/lib: none
- [partial] Run task start, finish and ship through a git-state matrix — plugin/tests has git-state cases; grep 'git-state matrix' tests: none as one matrix

## c54 Unattended window planning and morning notes

Mark: **skip** · value 2 · effort M · risk med — mostly speculative or privacy-sensitive (calendar, power); little grounded demand

- [partial] Hold a quota floor for the user's habitual first hour — fmhooks.py:4323 calls fmbudget.degrade before side work; no floor reserved for the first hour
- [new] Pick unattended windows from power and idle state — grep 'battery|suspend|idle' fmnight.py: 1 incidental hit; canary: def main found
- [new] Read a local calendar file to switch to lean mode in crunch weeks — grep 'calendar|crunch|lean mode' lib: only systemd OnCalendar and calendar.timegm; canary: def main found
- [new] Print an "expected to need you at" line when an unattended run starts — grep 'need you' fmnight.py: 0 hits; canary: def main found
- [partial] Hold the unattended drive on provider incidents and model sunset dates — fmmodels.py:75-85 retiring/retired model rows feed a note; the drive does not hold on them
- [new] Score a "clean morning" forecast before each unattended night (wild) — grep 'clean morning' lib: 0 hits; canary: def main found
- [new] Wild: reboot rehearsal in a throwaway VM — grep 'reboot' lib not run; fm drill is temp-home only (fmdrill.py:1); canary: def main found
- [new] Write tomorrow's morning note in the user's voice and learn from their edits (wild) — fmaway.py:89 is a template line, no voice or edit learning; canary: def main found
- [new] Send a next-morning second-thoughts letter on yesterday's closes (wild) — grep 'second.thoughts' lib: 0 hits; canary: def main found
- [new] Wild: have a cold child read only the morning card and say what happened overnight, then diff it against the ledger — fmideas.run_child exists (fmexam.py), no morning-card check; canary: def main found
- [new] Keep a change-freeze calendar the guard honours — near T-0935 (done) — grep 'change.freeze|code freeze' fm{hooks,guard,cli,core}.py: 0 hits; canary: def main found
- [partial] Checkpoint before a predicted compaction — near T-2504 (done) — PreCompact hook checkpoints at compaction (fmhooks.py:3501); nothing predicts it in advance
- [new] Capture a one-line "tomorrow:" note at session close — near T-0729 (done) — grep 'tomorrow' fmhooks.py, fmcli.py not found; canary: def main found
- [new] Wild: preview a month of silence on request — grep 'silence' lib: no feature; canary: def main found

## c55 Web action safety and render consistency

Mark: **skip** · value 2 · effort M · risk med — Safety for web actions that do not exist yet. It does not anticipate what the user needs.

- [partial] Reject web actions fired from a stale tab — fmsettingsserve (MASTER.md:187) has a one-use token, cookie, Host/Origin checks, but no tab-age check. grep 'stale tab' in fmweb*.py: no file
- [partial] Retype the task id to confirm irreversible web actions — grep 'csrf|Origin|token' found only fmsettingsserve; it serves settings, not ship/publish grants, so no retype step exists
- [new] Serve every page render from one ledger epoch — grep 'epoch' over fm*.py found no read-consistency code. canary: def main found (fmcli.py:8473)

## c56 Autonomy policy and unattended scheduling

Mark: **skip** · value 2 · effort L · risk high — Large policy changes, speculative; risk budget already built.

- [partial] Measure the judges against themselves — near T-2632 steer expander returns Rule and Proposals; no judge-vs-judge score. grep 'judges' lib: none
- [new] Run an N-version hunk consensus on risky tasks — grep 'consensus|N-version' plugin/lib: none; canary: def main found
- [built] Set autonomy by value-at-risk — near T-1080: fmrisk.py daily risk budget slows autonomy
- [new] Govern chatter with a churn-hazard score — grep 'churn|hazard' plugin/lib: none; canary: def main found
- [new] Solve the night's schedule as one constraint problem — grep 'constraint|schedule solver' fmnight.py: none; canary: def main found
- [partial] Run every capability through a lifecycle ladder with auto-demotion — fmtriggers.py:4 route/muted ladder and MUTE_MIN=20; only for triggers
- [new] Declare a plateau from drift and taste, then wait for a read receipt — grep 'plateau|read receipt' plugin/lib: none; canary: def main found

## c57 Cold-start onboarding and repo integration

Mark: **skip** · value 2 · effort L · risk med — Mostly broad product features, not user-next-step anticipation.

- [partial] Bootstrap any clone to first green — fmsetup.py, fm new (fmnew.py) and fm doctor give first-run checks. A one-command first-green not verified
- [partial] Adopt existing agent-rule files on first contact — AGENTS.md/GEMINI.md grep: fmagents.py (3), fmcli.py (2). Auto-adopt on first contact not verified
- [new] Print upgrade notes filtered to the verbs you use — grep -i "what's new|upgrade notes" fmcli.py: only the scan. canary: def main found (fmcli.py:8473)
- [new] Bootstrap taste from the user's merged PR reviews — grep -i 'merged PR' in fmtaste.py/fmpr.py: nothing. canary: def main found (fmcli.py:8473)
- [partial] Classify repo sensitivity from its contents on first contact — meta 'sensitive' flag read at fmforesight.py:317. Auto-classification not found
- [new] Mine the forge's past review comments into repo-scoped lessons — grep -i 'review comments' fmpr.py/fmci.py: nothing. canary: def main found (fmcli.py:8473)
- [new] Route CODEOWNERS-sensitive changes to a sign-off row — grep CODEOWNERS plugin *.py: no matches. canary: def main found (fmcli.py:8473)
- [partial] Run downstream consumers' proofs on a library change — fmdeps.py, fmrelproof.py, fmchange.py exist. Cross-repo consumer proofs not verified
- [partial] Write an ADR for each costly decision into docs/adr — grep 'docs/adr' fmcli.py: 3 hits. Per-decision ADR writing not verified
- [partial] Plan a git-history secret purge, rotation first — fmsecrets.py scans for secrets. grep purge: no history-purge planner
- [new] Sign unattended commits with a dedicated, revocable key — grep -i 'gpgsign|ssh-keygen' plugin/lib: nothing relevant. canary: def main found (fmcli.py:8473)
- [partial] Tokenise identifiers reversibly before any cloud send — c.redact (fmdraft.py:168) redacts. Reversible tokenising not found

## c58 Resilience and kill-safety

Mark: **skip** · value 2 · effort L · risk med — Hardening of the unattended drive. It reacts to failures and does not foresee user needs.

- [partial] Stage a nightly fake-clock month for unattended timers — fmexam breakage runs a fake clock (fmexam.py:728). No full month soak
- [partial] Run the unattended drive through a real suspend/resume and network-loss soak — grep 'suspend|resume' in plugin/lib: hits in fmnight/fmclaude/fmscout/fmexam. No soak
- [partial] Make every ledger writer kill-safe, proven by a kill-point sweep — T-0679 chaos tests for resilience (CHANGELOG.md). Per-writer sweep not found
- [new] Add a two-phase grant spend so a crash cannot double-push or lose a grant — grep -i 'two-phase' fmgrants.py: nothing. canary: def main found (fmcli.py:8473)
- [partial] Wild: Pull-the-plug day, a seeded random SIGKILL of the real drive on a scratch repo — fmdrill.py runs a simulated day with crashes. Seeded SIGKILL not seen
- [new] Wild: Run the guard in two independent implementations and block on disagreement — fm bench guard --mutate (MASTER.md:547) tests one guard. No second implementation. canary: def main found (fmcli.py:8473)
- [new] Wild: Fall back to the last good install generation when a hook fails to import — grep 'generation' in fmhooks/fmsetup: nothing relevant. canary: def main found (fmcli.py:8473)
- [partial] Fuzz the readers with a fake clock and ledgers at 10× size — T-2645 c.clock() for windowed readers. Fuzz at 10× size not found
- [new] Suspend a real microVM mid-drive — grep 'microVM' plugin: nothing. canary: def main found (fmcli.py:8473)
- [partial] Give new guard and gauge tests a mandatory "fails on the planted defect" twin — fmmutate.py (T-1066) mutates the guard. No rule that every gauge test needs a planted-defect twin

## c59 Grid cells dismissed in the lens file

Mark: **skip** · value 1 · effort S · risk low — these are dismissal notes, not ideas

- [built] Web UI × any × slow: — lens file r3-01-grid.md:58 says an existing render-budget idea covers it
- [false-premise] Site × agent: — near T-2395 (done) — r3-01-grid.md:59: agents do not read the Genesis site
- [built] Other lanes × unsafe: — r3-01-grid.md:60: covered by capability-token and file-intent ideas
- [built] All "missing" cells for the user on the CLI: — near T-2493 (done) — r3-01-grid.md:61: covered by the honest 'can't read you this week' idea

## c60 Genesis site provenance

Mark: **skip** · value 1 · effort M · risk low — Outward-facing and visual. Not anticipation.

- [partial] Record the Genesis site's published commit on every page — fm genesis live (CHANGELOG.md:396) shows the last push in the CLI. Page-footer sha not verified
- [new] Publish DisciplineBench for any harness (wild) — grep -i 'DisciplineBench' plugin/lib: nothing. canary: def main found (fmcli.py:8473)

## c61 Net-new verbs and surfaces

Mark: **skip** · value 1 · effort L · risk med — Speculative new surfaces with no foresight benefit.

- [new] Add `fm bye <capability>` for per-capability removal — grep 'fm bye|bye' fmcli.py help=: none; canary: def main found
- [new] Run tasks from `fm:` comments in source — grep 'fm:' comment scan in plugin/lib: none; canary: def main found
- [new] Stand up a local offline forge for review — grep 'forge|offline review' plugin/lib: none; canary: def main found

## c62 Packaging and distribution

Mark: **skip** · value 1 · effort L · risk med — Distribution work. Not anticipation.

- [new] Ship `fm top`, a standalone live view for non-Claude harnesses — fmcli.py has no 'top' verb (fm watch/fmwatch.py exists as a related live view). canary: def main found (fmcli.py:8473)
- [new] Package Foreman for Nix, Homebrew and pipx — grep -i 'homebrew|pipx|flake' MASTER.md and pyproject: 5 hits, none a package. canary: def main found (fmcli.py:8473)
- [new] (wild) Map receipts to SOC 2 and ISO change-management controls — grep -i 'SOC 2' plugin: nothing. canary: def main found (fmcli.py:8473)
- [partial] (wild) Bridge `fm ask` and status to Matrix, Slack or Discord — fmintegrations.py, fmbus.py exist. Specific bridges not verified
- [new] (wild) Teach the user one thing a week from the agent's own diffs — grep -i 'teach' plugin/lib: nothing relevant. canary: def main found (fmcli.py:8473)
- [partial] (wild) Open a third-party extension registry with a lean budget — fmplugins.py, fmextras.py exist. A registry was not found
- [new] Open one intake socket for mail, Matrix and share-sheet — grep -i 'share-sheet|intake socket' plugin: nothing. canary: def main found (fmcli.py:8473)
- [new] Ship a hermetic Nix flake for Foreman — grep 'flake.nix' MASTER.md: no flake file. canary: def main found (fmcli.py:8473)

## c63 Visual and speculative wilds

Mark: **skip** · value 1 · effort L · risk high — Visual-only or speculative.

- [new] Wild: Render an architecture diagram diff on every finish card — grep 'architecture diagram' plugin/lib: none; canary: def main found
- [new] Wild: pool expiring quota across the user's accounts and machines — grep 'pool.*quota|accounts' plugin/lib: none; canary: def main found
- [new] Wild: run a bet-to-ship contract that the user can cancel in advance — grep 'bet-to-ship' plugin/lib: none; canary: def main found
- [new] Wild: audit by an oracle that carries the user's disbelief — grep 'oracle|disbelief' plugin/lib: none; canary: def main found

## c64 Web UI surfaces

Mark: **skip** · value 1 · effort L · risk med — The premise is wrong: there is no task web UI, and it is visual.

- [false-premise] Require a human-input witness for web UI approvals — only web UI is the settings page, fmsettingsserve.py:1; no approvals there
- [false-premise] Show a stale-data badge with age on every web UI card — fmsettingsserve.py:1 serves settings only; no cards
- [false-premise] Wild: Let the web UI replay a recorded worst day against each release — no web UI beyond settings (fmsettingsserve.py:1)
- [false-premise] Wild: Have a cold child guess each surface's next click from a screenshot and score it — no web UI surfaces to click (fmsettingsserve.py:1)
- [false-premise] Bind each web action to the epoch and task it was rendered from — web UI has no task actions; fmsettingsserve.py:1 is settings only
- [partial] Make the home page a season recap, atlas and try-it feed — Genesis site publishes pages (fmgenesis.py:1219); grep 'season recap' lib: none
