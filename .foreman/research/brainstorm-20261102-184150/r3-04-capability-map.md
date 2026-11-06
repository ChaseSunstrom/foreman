# Brainstorm — lens: capability map

- **Rank canary hits by file class** — FIX — value 3 — effort S — risk low — category: grounding
  Why: the map shows `plugin/skills/` holds 1,388 of 2,176 files, so a "near the idea" canary probably returns mostly skill text. Assumption: the canary doesn't weight by directory today.
  Done when: on a fixture where a term appears in 30 skill files and 1 `plugin/lib` file, the canary prints the lib hit first, with per-class counts.

- **Add a prior-art line naming an outside tool to every brief** — FEATURE — value 4 — effort M — risk low — category: approaches
  Why: the canaries and the existing "three nearest things" idea only search inside the repo. The deferred T-0869 (rival plugins) and the approaches lens both ask "does a tool already do this?". Assumption: stack cards can supply an offline list of tool names such as semgrep, hypothesis and tree-sitter.
  Done when: filing a brief without `prior-art:` (a tool name, or "none found, searched <cards>") is refused, and a test covers the refusal.

- **Slot-fill every request in EARS templates** — FEATURE — value 4 — effort M — risk low — category: exhaustive thinking
  Why: this Mission is about saying what was left out. The EARS slots (always / on event / while state / unwanted behaviour / optional) give mechanical empty cells that need no lens. The unwanted-behaviour slot is the one requests usually skip. Assumption: the existing grid columns don't already force that slot.
  Done when: `fm spec` on a three-clause request prints five slots per clause, marks the empty ones, and the empties land in the Mission's left-out list.

- **Fit carried-gap expiry to the lag before the user re-asked** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: the expiry is fixed at two generations. The pack already has dropped and re-asked items (e.g. T-2738 follows T-2683), so the real time from "left out" to "user asked" can be measured. Assumption: ledgers hold enough pairs to compute a median.
  Done when: `fm outcomes` prints median days from a left-out cell to the user's matching ask, and the expiry reads that value, falling back to 2 generations when there are fewer than 5 pairs.

- **Diff declared effects against observed effects during each Exam** — SECURITY — value 4 — effort M — risk med — category: security
  Why: a brief's live reading is code Foreman runs unattended. Each brief would declare `touches:` (state paths written, hosts contacted), and the Exam run would compare that to what it actually did. A strace/inotify wrapper is the only tooling assumed.
  Done when: an Exam that writes an undeclared file or opens an undeclared socket fails with the offending path or host named.

- **Rehearse a Mission offline under a network namespace** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: the local-first rule says nothing is sent without an explicit setting, but nothing shows which Mission steps send. The host runs a hardened kernel, which often disables unprivileged user namespaces. So the rehearsal must say plainly when it can't isolate.
  Done when: `fm genesis rehearse --offline` lists every step that needs the network and the pack sections it would send. On a kernel without namespaces it prints "isolation unavailable" and exits non-zero rather than reporting zero sends.

- **Add a four-way unsafe-action table to briefs that add a verb or hook** — FEATURE — value 3 — effort M — risk low — category: security
  Why: the usual failure-mode columns describe what breaks. The STPA question is different: when does the action itself go wrong (not given, given wrongly, too early or late, stopped too soon). Assumption: no current brief template asks this.
  Done when: `fm genesis check` rejects a brief that adds a verb or hook without those four rows, and a test covers the rejection.

- **Encrypt stored verbatim asks at rest** — SECURITY — value 2 — effort M — risk med — category: privacy
  Why: the user's own words (steers, intake, pasted text) are kept verbatim, and pasted text can hold secrets. Scrub and retention ideas exist, but none covers at-rest protection. Assumption: a keyring or `age` is available and the state dir isn't already encrypted.
  Done when: grepping the state dir for a planted marker string finds nothing, while `fm next` and `fm recall` still show the text.

- **Publish an Atom feed from the Genesis site** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: `fm genesis live` already publishes static data to `site/genesis`. A feed adds phone, watch and reader-app delivery of Mission closes and left-out slips with no new server. Assumption: the feed fits the static-site constraint.
  Done when: `site/genesis/feed.xml` validates and lists the last 20 Mission events, and it changes after a `fm genesis live` publish.

- **(wild) Show a terminal QR that opens one cell on the phone** — FEATURE — value 3 — effort M — risk high — category: devices
  Why: the pack proposes a phone triage board and pocket approval, but not the step that gets you there from the terminal. A LAN-only, single-use token URL for one grid cell would close that gap. The risk is exposing the web UI to the network, so it needs an expiring token and a bind check.
  Done when: `fm qr <cell>` prints a QR code whose URL opens that cell once from a second device, then returns 410 on reuse and after expiry.

- **(wild) Draw a fingerprint of each Mission's grid** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the "grid delta between Missions" idea needs reading. A small identicon from the filled, empty and n/a pattern lets the user see at a glance when a Mission's shape is unusually hollow. Assumption: a stable cell ordering across Missions.
  Done when: two Missions with identical grids render identical SVGs, and moving one cell from filled to empty changes the image.

- **(wild) Write a seventeen-syllable left-out line for the status bar** — FEATURE — value 1 — effort S — risk low — category: delight
  Why: the left-out receipt is long. A one-line poem-shaped summary is the version people might actually show others. Assumption: it only ever sits beside the real receipt and never replaces it.
  Done when: the status line shows a single line under 60 characters whose count of left-out items matches the receipt.

Next question: which brief fields do the user or the cold readers actually act on at close, so a new field such as `prior-art:` or `touches:` can be paid for by retiring a field they never look at?
Next question: on this machine, which of the kernel-level isolation primitives (user namespaces, Landlock, seccomp) work under the hardened kernel, and which proposed Exam sandboxes depend on one that is switched off?
