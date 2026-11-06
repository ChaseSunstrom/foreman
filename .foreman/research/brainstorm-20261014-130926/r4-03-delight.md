# Brainstorm — lens: delight

- **Print an erratum when a fix changes a number Foreman already reported** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: your first two asks were readers that undercounted failures (track record, catch rates). Anything Foreman told you before those fixes was wrong, and nothing says so. Assumption: the old figure can be recomputed from stored results or the commit message.
  Done when: after a metric-reader fix lands, `fm task finish` prints "Erratum: track record was 0 failures, now 7" and the next session greeting repeats it once.

- **Give request prefixes a punctuation grammar: `!` jumps the queue, `?` plans without capturing, `~` parks** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: you already write `FIX!:` and `PERF:` by hand, and the `!` is currently ignored. Assumption: it means urgency.
  Done when: `fm` given `FIX!: x` queues it at the front, `FIX?: x` prints a plan sketch with no task created, and `FIX~: x` lands in deferred.

- **Hold each capture for a 10-second amend window** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: you send bursts of fragments (T-0790 intake folding) and often correct yourself mid-thought. A follow-up starting "no," or "actually" should edit the last capture instead of adding a second one. Assumption: that evidence is thin because T-0790 was deferred as unproven.
  Done when: capture "FIX: a", then within 10 seconds "actually b", leaves one task titled with b and the verbatim text of both messages.

- **Show a proof-freshness dot on the band** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: round 1 made close checks depend on real diffs, but nothing visible says whether the last verify ran on the current tree. Assumption: a tree hash is cheap to compute in the status path.
  Done when: the dot is green after verify, turns amber after any edit, and returns to green after the re-verify. A test covers all three.

- **Put the next command on the clipboard when Foreman tells you to run one** — FEATURE — value 3 — effort S — risk low — category: ergonomics
  Why: T-0325 and T-0418 are blocked on commands only you can run (`sudo pacman -S libappindicator-gtk3`, the foreman-ui update). Copying them by hand is friction. OSC 52 also works over ssh. Assumption: your terminal allows OSC 52 writes.
  Done when: a blocker line prints "copied", the clipboard holds exactly the command, and nothing is written when stdout isn't a tty.

- **Learn quiet hours from your own activity gaps** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: round 1 added push notifications with no schedule, and you rarely configure things ("etc. etc. etc."). Sleep and away patterns are in the session timestamps. Assumption: a week of history is enough to infer them.
  Done when: with a synthetic ledger showing no activity 00:00–07:00, a non-urgent push at 03:00 is held for the morning card, and an urgent ask still goes through.

- **Attach hindsight receipts to your own steers and drops** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: you drop ideas on measured premises (delta reads: 174 repeats cost about 109 tokens; Read hook: about 2 minutes a month). Foreman could report later "your call held" or "your call was wrong, here is the number." Assumption: the premise can be re-measured from logs.
  Done when: `fm research show` on a dropped idea prints its premise, a re-measured value, and a verdict line.

- **Wild: Tap state changes to any command you configure** — FEATURE — value 3 — effort S — risk low — category: ambient
  Why: assumption: a Hue light, tmux colour, or desk LED is a delight surface Foreman can't know about. A generic `on-state` command receiving `idle|working|needs-you|done` avoids building any of them. This is distinct from the existing tmux/starship segment.
  Done when: with `on_state = "echo $FM_STATE >> f"`, driving a task through its states appends the right lines, and a slow command never delays a hook.

- **Wild: Make a run audible with rising pitch** — FEATURE — value 2 — effort M — risk low — category: sound
  Why: a quiet tick per passing gate, with pitch rising through the plan steps and a low tone on red, lets you hear a run from another room. The existing sound ideas are completion and needs-you cues, not progress. Assumption: you have a local audio player, and it is off by default.
  Done when: the setting emits an ascending sequence over a 5-step fixture task and a distinct failure tone, and emits nothing without the setting.

- **Wild: Share skins: spinner verbs, palette and cues as one tiny file** — FEATURE — value 2 — effort M — risk med — category: personality
  Why: round 1 added sessionTitle and spinner-style touches. A skin file you can post as a gist makes those things shareable. Assumption: it is wanted; no evidence yet. Skins must be data only, never executable.
  Done when: `fm skin apply <file>` changes the verbs and colours, rejects any file with an unknown key, and `fm skin reset` restores defaults.

- **Wild: Give each round a one-page "what you'd notice" strip, built from before/after commands on throwaway fixtures** — FEATURE — value 3 — effort M — risk med — category: recursion
  Why: "recursively improve" means judging round 1, but you still can't see what it changed for you. Existing receipt ideas are prose; this runs each shipped feature's failure case on old and new code. Assumption: most round-1 items have a scriptable before state.
  Done when: `fm round show 1` renders at least five before/after pairs from real runs, with the exact commands, and each pair reproduces when re-run.
