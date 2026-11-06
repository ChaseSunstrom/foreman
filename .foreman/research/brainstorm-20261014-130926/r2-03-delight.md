# Brainstorm — lens: delight

- **Show a "round receipt" when a recursive round closes** — FEATURE — value 4 — effort M — risk low — category: round close-out
  Why: the user defined "recursively improve" as finish, review, brainstorm again, repeat, yet nothing marks a round ending. Round 1's gaps (monitor unverified, compact off, board unticked) sit in prose. assumption: the ledger can list tasks per round.
  Done when: closing a round prints ≤8 lines (shipped N, deleted M, still-unlit features, one next step) and the same text lands in the ledger.

- **Light up dormant features with a one-line "ready when you are" offer** — FEATURE — value 4 — effort S — risk low — category: opt-in nudges
  Why: compact output saves ~1.04M tokens/30 days but is off until the user says yes. Offer it once, with their own numbers, at the moment a big output happens.
  Done when: the first Bash output over 6,000 chars in a session adds one line naming the measured saving and the exact command to enable it, and it never repeats after a yes or no.

- **Greet the monitor's first delivery** — FEATURE — value 3 — effort S — risk low — category: liveness feedback
  Why: "arming in a live interactive session is unverified". A tiny confirmation, "mail monitor armed ●", on the first heartbeat turns an invisible mechanism into trust. Silence when armed would otherwise look identical to broken.
  Done when: a new session shows the armed marker within one turn of the monitor's first heartbeat, and shows "not armed (restart to enable)" when absent.

- **Tick the catalogue page by clicking** — FEATURE — value 4 — effort M — risk med — category: artifact board
  Why: nobody has ticked the board. `fm page` output is static HTML. Checkboxes with keep/drop/later that produce one paste-back line remove the friction of replying by prose.
  Done when: the page has per-idea three-state controls and a "copy my picks" button whose output `fm research` ingests and records.

- **Return card on resume in the session title** — FEATURE — value 3 — effort S — risk low — category: session greeting
  Why: sessionTitle already follows the active task. On resume, extend it into "T-0818 · step 3/5 · 2 asks waiting" so the resume picker and tab read as a status line.
  Done when: resuming shows step progress and ask count in the title, and the title stays ≤60 chars and uses T-ids only in sensitive repos.

- **Celebrate subtraction** — FEATURE — value 2 — effort S — risk low — category: close-out delight
  Why: the user keeps steering toward less ceremony (drops, "do less" ideas). A close-out line "net −212 lines, 1 hook retired" makes deletion feel like a win, nudging more of it.
  Done when: finish prints net lines removed and retired surfaces when the diff is net-negative, and prints nothing otherwise.

- **Keep push bodies human and one-line** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: Stop now asks for PushNotification. A body like "Needs you: pick A or B (default A in 10m)" reads on a lock screen; a generic "Foreman needs input" does not.
  Done when: every push body names the decision and its default, ≤90 chars, and contains no paths in sensitive repos.

- **Show a savings strip beside spend** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: round 1 measured tokens saved but the user never sees it per session. A statusline fragment "saved ~38k tok today" makes the work feel earned.
  Done when: with compact output on, the statusline shows cumulative tokens saved this session, and it hides at zero.

- **Wild: Wake to a finished Round 3 on the breakfast page** — FEATURE — value 4 — effort L — risk med — category: unattended rounds
  Why: wild. The user said "etc. etc. etc." about improving, and wants repetition. Spend leftover budget overnight on the deferred small tasks, then publish one Artifact "what got better" with a net-delta and a keep/revert button per item. assumption: a safe overnight budget cap exists.
  Done when: a night run executes only tasks tagged S from deferred clusters and produces a page listing each with a revert command that works.

- **Wild: Draw the task as a clipboard that ticks itself** — FEATURE — value 2 — effort M — risk low — category: band motion
  Why: wild. Criteria turning green with a brief tick as evidence lands makes verification visible rather than a final claim.
  Done when: the band shows each criterion and flips its mark within one render of its verify passing, with reduced-motion rendering a static mark.

- **Wild: One-minute "what got better" strip per round** — FEATURE — value 3 — effort L — risk med — category: shareable recap
  Why: wild. Round 1 shipped ~20 changes across hooks, guard and tokens; the user receives prose lists. A scrollable HTML strip with before/after numbers (hook ms, tokens, idle minutes) is something to show others.
  Done when: `fm page --round N` emits a self-contained page with at least three measured before/after pairs, each sourced from recorded metrics, and no home paths.

- **Offer a "why did it do that" key on any guard block** — FEATURE — value 3 — effort M — risk low — category: guard legibility
  Why: round 1 changed several guard messages (state-direct refusals point to `fm research add`). A single follow-up showing the matched rule, one safe rewrite, and the command that allows it once cuts the frustration of an opaque refusal.
  Done when: a blocked command's message ends with a `fm guard why` hint, and running it prints rule id, rewrite, and the allow-once command.

- **Wild: A quiet "queue zero" moment** — FEATURE — value 2 — effort S — risk low — category: micro-delight
  Why: wild. When the queue drains the Stop hook already fires a push; locally, show a single-line summary (tasks closed, first-time passes, time) once, with no animation unless motion is allowed.
  Done when: draining the queue prints exactly one summary block, suppressed on subsequent turns until new work arrives.
