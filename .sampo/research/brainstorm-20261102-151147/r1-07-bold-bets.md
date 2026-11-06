# Brainstorm — lens: bold bets

- **Port the hook path to a static binary, held to a recorded corpus** — PERFORMANCE — value 4 — effort L — risk med — category: performance
  Why: assumption: hook latency is the cost the user feels most, and the pack shows `bench_hooks.py`, a "warm daemon" idea and cold-start ratchets. A native guard-and-dispatch binary, gated by `fm replay` over real recorded hook payloads, removes Python start-up without a daemon.
  Done when: `bench_hooks.py --runs 20` shows p95 at or below a third of the Python path, and 10k replayed payloads give identical verdicts on both implementations.

- **Run lanes as multiplexer panes** — FEATURE — value 4 — effort M — risk low — category: devices
  Why: lanes and the Agents graph exist, but the pack shows no way to attach to a live lane from a terminal. `fm lane --attach` would open each lane as a tmux/zellij pane and tear it down on merge.
  Done when: three lanes started in a scratch repo appear as three attachable panes, and closing the lane removes its pane.

- **Serve one local Foreman protocol that every surface reads** — FEATURE — value 5 — effort L — risk med — category: dev experience
  Why: the pack lists a web UI, the foreman-ui pane, Desktop, status bars, a phone page and editor hovers, and each re-reads the ledgers. A single JSON-RPC socket with versioned schemas (like LSP) would let new surfaces be thin clients. Assumption: surface drift is a recurring cost, given the T-0166 split and the "test that every receipt field appears on every surface" idea.
  Done when: the web UI and one other surface run with no direct ledger reads, and a conformance test checks both against the same protocol fixtures.

- **Kill each brief before it enters the queue** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: the pack shows T-2666's "ground the 525-idea brainstorm" and dropped items such as `fm guard --dry-run` that turned out to be "mostly built". A cheap falsifier lane would spend a few minutes trying to show a brief is duplicate, already built or vacuous before it is filed, and would log the result.
  Done when: seeded with the dropped `fm guard --dry-run` brief, the lane returns "mostly built: fmreplay.py" with a path, and the finding is recorded on the intake record.

- **Compare held-rate anonymously against other users** — FEATURE — value 3 — effort L — risk high — category: privacy
  Why: assumption: a solo user can't tell whether their 4% lost-work rate is good. An opt-in exchange of k-anonymised aggregates (rates only, no text, no paths, fixed buckets, local-first) gives context without sending content. The default is off, and `fm` previews the exact bytes before any send.
  Done when: `fm bench --share --preview` prints the payload, it contains no strings outside a fixed numeric schema, and nothing is sent without the setting. (wild)

- **Make every bypass session replayable as a sandboxed rehearsal** — SECURITY — value 4 — effort L — risk med — category: security
  Why: assumption: users run bypass mode because asking is slow, and the pack's open questions ask what unguarded surfaces do. The idea is to re-run the session's commands against a copy-on-write snapshot afterwards and show the effect diff, so the user can accept or reverse what actually happened.
  Done when: after a scratch bypass session that edits `$HOME`, the replay lists every changed path and one command restores them.

- **Draw a "why not" ledger of what Foreman declined to build** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: dropped ideas carry reasons in the pack but live only in conversation. A `fm nope` page (reason, evidence, revival condition) would stop the same ideas being re-proposed, which the "re-proposals" count already hints at.
  Done when: each of the five dropped items above appears with its reason, and a re-proposed duplicate brief is flagged at filing with a link to its entry.

- **Calibrate brainstorm lenses to this user's accept history** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the pack's "Ideas so far" holds thousands of ideas and the user accepted a small fraction (a few dozen asks). Weighting future lenses by accepted and dropped categories (guard, proofs, lean) lets `fm ideas` spend its budget where the user actually acts. T-0829 defers a related lens-rate cut.
  Done when: on the last 100 filed ideas, the weighted ordering puts at least 60% of the accepted ones in the top third.

- **Replace the idea list in packs with a nearest-neighbour digest** — PERFORMANCE — value 4 — effort M — risk low — category: simplicity
  Why: this pack is dominated by a long "ideas so far" list with many near-restatements (many "wild" proof and tick variants). A local lexical index that returns the 20 nearest prior ideas per candidate cuts pack tokens and the repeat rate.
  Done when: pack size falls by at least 70% and a rerun on a fixed lens yields no more near-duplicates than before.

- **Rewind the user's decisions with a "what if I'd said no" fork** — FEATURE — value 3 — effort L — risk med — category: observability
  Why: there are 40+ standing steers, and the user can't tell which ones cost time. `fm fork --without STEER` replays a closed task's ledger slice under the alternative to price it. (wild)
  Done when: forking one steer on a closed task prints the delta in steps, spend and checks run, and leaves live state untouched.

- **Let the hard hat live in the desktop tray as a posture lamp** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: T-0325 is blocked on libappindicator. A lamp (green, amber, red) fed from the drive state, via a status-notifier D-Bus item, needs no GTK appindicator.
  Done when: the item appears under a stock KDE or sway-bar and changes colour when a scratch drive stalls. (wild)

- **Record a 30-second "first win" cast during install** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: T-0862/0863 defer newcomer tours until there's evidence. A scripted cast of a planted bug being fixed in a throwaway repo, with the hard-hat receipt at the end, gives that evidence cheaply (fraction who run a second verb within a day).
  Done when: `install.sh` ends by offering the demo, and one run shows the red-to-green flip on a planted bug.

Next question: which surface, other than the terminal, does the user actually open in a normal week, and would they miss the rest?
Next question: what do the 40+ steers cost in latency and tokens per session, and which have never changed an outcome?
