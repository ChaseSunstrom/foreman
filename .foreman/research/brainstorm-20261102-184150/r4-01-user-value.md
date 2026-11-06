# Brainstorm — lens: user value

- **Print the `fm next` before and after at Mission close** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: assumption: `fm next` is the screen the user reads most, so a Mission that doesn't change it is invisible to them. Pack evidence: T-2722 and T-2738 were filed because `fm next` printed the wrong thing.
  Done when: closing a Mission prints two captured `fm next` outputs from a fixed fixture state, or the line "fm next unchanged".

- **Count asks removed per capability for 14 days after it lands** — FEATURE — value 4 — effort M — risk low — category: outcomes
  Why: the user typed "Ship N commit(s)" about eight times in the pack. Each time they typed an ask a capability should have made unnecessary, that is the real outcome measure for the Exam.
  Done when: a settled brief shows "typed asks of kind K: before N, after M", computed from the ledger, and says "no baseline" when it has none.

- **Add a "walk-away" line to every Mission page** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: assumption: the user wants to leave an unattended Mission and know what would make them come back. The pack's "stop and show me" and "walk-away condition" ideas cover the key, but not a stated stop condition.
  Done when: the Mission file has a parsed `Walk-away:` line, and `fm genesis check` fails if it is missing.

- **Show the dissent's cost to reverse** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: the user dropped #23, #24 and #25 as "by design" or "gap" after reading them. Each overruled dissent should say how many files and minutes it would take to reverse the call, so they can overrule it cheaply.
  Done when: every dissent record carries a `reverse:` line with a file count, and `fm genesis check` rejects a dissent without one.

- **Pre-write the "why did you build this?" answer in the user's words** — FEATURE — value 3 — effort M — risk low — category: provenance
  Why: the pack's most common user message is a short, specific correction, and the gap is that nothing quotes the user's sentence beside the thing it caused. This idea attaches the user's verbatim request sentence to each brief, commit and verb help line.
  Done when: `fm why T-id` prints the user's verbatim sentence, and an item with none prints "self-filed".

- **Hold a brief whose Exam the user could not re-run by hand** — FIX — value 4 — effort S — risk low — category: Exam
  Why: the user re-ran or redid several results by hand (T-2720, the M-02 rerun, the volatile-path audit). Each Exam should print one copy-paste line that works from a fresh shell.
  Done when: `fm exam brief T-id --print-cmd` outputs one command, and a test runs it in an empty home and gets the recorded reading.

- **Give each steer a "last enforced" date** — FEATURE — value 3 — effort S — risk low — category: steers
  Why: the pack lists dozens of standing steers. The user can't tell which ones still bite, and the cost of owning them grows quietly.
  Done when: `fm decide --list` shows "last enforced N days ago" per steer, and steers never enforced in 60 days are marked dormant.

- **Reorder the Mission page so each section answers one question the user asks** — CLEAN — value 3 — effort S — risk low — category: legibility
  Why: assumption: the user opens the sting cell first. Open work shows no evidence about reading order, and an earlier brainstorm question asked about it directly.
  Done when: local, opt-in open counts for the page's sections exist for two Missions, and the section order matches them.

- **Wild: Hold a "regret postcard" the user can tear up** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A cold child writes the user's likeliest complaint about the Mission as a two-line postcard, sealed before building. If the user later types something close to it, the postcard is shown as a hit.
  Done when: sealed postcards exist at Mission open, and the Mission report prints "hit" or "miss" against the user's next three typed asks.

- **Wild: Offer a "boring Mission" that only deletes** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: wild. Every fourth Mission may only remove things (steers, verbs, gauges, tower files), and the user sees a net-negative diff as the headline.
  Done when: a deletion-only Mission passes the full suite, and its report shows lines removed greater than lines added.

- **Wild: Read the Mission aloud as a 60-second script** — FEATURE — value 2 — effort M — risk low — category: surfaces
  Why: wild, assumption: the user glances at their phone or a terminal, not at a long page. Plain text-to-speech from a five-line twin works with zero tokens.
  Done when: `fm genesis say` writes a script under 150 words from fixed fields only, and a cold child can state the interpretation, the outcome and the left-out count from it.

- **Settle a Mission's left-out list against the user's next fortnight of asks** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the pack records asks that no idea predicted (T-2691 to T-2738). It doesn't yet say whether a given Mission's own "left out" items were later asked for, which is the cheapest score of exhaustiveness.
  Done when: 14 days after a Mission, `fm outcomes` prints "left out X, later asked Y" with the matching ask ids, or "none matched".

- **Show what the user can stop checking** — FEATURE — value 4 — effort M — risk med — category: attention
  Why: assumption: value to this user is mostly attention saved. Each closed brief should name the manual check it replaces, such as re-running a script or comparing a tree, and which verb now does it.
  Done when: a closed brief with a `replaces:` line is listed on a "you can stop doing" shelf, and entries expire if the user keeps doing the check.

Next question: which of the user's repeated messages in the last 30 days name a manual check, and does any Exam reading replace one?
Next question: if the user never opens a Mission page, which single line of it would they most want pushed to them?
