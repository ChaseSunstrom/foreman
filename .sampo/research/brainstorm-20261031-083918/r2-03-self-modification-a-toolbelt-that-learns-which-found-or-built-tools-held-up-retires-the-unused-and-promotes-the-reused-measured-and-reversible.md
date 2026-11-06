# Brainstorm — lens: self-modification: a toolbelt that learns which found or built tools held up, retires the unused and promotes the reused, measured and reversible

- **Write a toolbelt ledger event per use, not per install** — FEATURE — value 5 — effort M — risk low — category: toolbelt telemetry
  Why: assumption: found or built tools (T-2278 scaffolds, `fm plugins find`) are recorded at creation, but nothing in the pack shows a record of each call. Without calls there is no "held up" or "unused" signal for any other idea.
  Done when: running a built tool from a session appends one event (tool id, task id, exit status, seconds) and `fm toolbelt show` lists a call count and last-used date for it.

- **Score each tool by outcome of the tasks it touched** — FEATURE — value 5 — effort M — risk med — category: toolbelt scoring
  Why: the pack's outcome survival signal (re-fixed, reverted, red after merge, used by T-2291's router) exists for lanes and models, not for tools. Presence of a tool in a task that later reopened is the held-up measure.
  Done when: `fm toolbelt show` prints held-up rate per tool, and a test with one tool used in a reverted task and one in a clean task ranks them correctly.

- **Propose retirement of tools unused for N sessions as a reversible card** — FEATURE — value 4 — effort S — risk low — category: retirement
  Why: the lean ratchet (T-2312-era work, Mission 8/#12) warns on footprint growth, yet a built skill or MCP server that is never called still counts against rules chars and descriptions chars.
  Done when: a tool with zero events in 10 sessions appears in `fm doctor` as a retire proposal, `fm toolbelt retire ID` moves it to a shelf directory, and `fm toolbelt restore ID` returns it byte-identical.

- **Promote a script reused in 3+ tasks to a project skill** — FEATURE — value 4 — effort M — risk med — category: promotion
  Why: T-2278 builds scripts and skills separately; nothing converts the first into the second when use proves it. Promotion needs the use ledger above.
  Done when: a script called in 3 distinct tasks produces a queued proposal that, when accepted, writes a SKILL.md in the listing format and passes the existing skill description check.

- **Promote a tool reused across 2 repos to a global library card** — FEATURE — value 3 — effort M — risk med — category: promotion
  Why: assumption: `fm lib` cards exist (cards: python, cc-skills …) and a second repo hitting the same capability miss (T-2270 trigger) is the evidence a tool generalises.
  Done when: the same miss signature in two projects offers a card draft, and `fm lib show NAME` displays it only after the user accepts.

- **Charge each tool its footprint against the lean ratchet at adoption** — PERFORMANCE — value 3 — effort S — risk low — category: footprint
  Why: the ratchet records always-on chars and hook p50 at ship; an adopted MCP server or skill adds to both, and the trade is invisible until ship time.
  Done when: `fm toolbelt add` prints the char and hook-ms delta, and refuses past the ratchet limit unless the user passes an explicit override recorded in the ledger.

- **Re-test a tool whenever its world changes** — FIX — value 4 — effort M — risk med — category: rot detection
  Why: built tools ship with a failing-first test (T-2278), but that test is run once. Interpreter, dependency or Claude Code version bumps are what silently break it.
  Done when: changing the pinned python or a plugin version causes `fm doctor` to rerun each shelf tool's test and list any now red as "rotted", verified with a planted breakage.

- **Make every toolbelt change one reversible journal entry** — FEATURE — value 4 — effort M — risk low — category: reversibility
  Why: the user's rules demand grants never be self-given; retire, promote and install all alter the project. A single `fm toolbelt undo` is the safety that lets self-modification run unattended.
  Done when: after retire, promote and install, three `fm toolbelt undo` calls restore the tree to a byte-identical state, checked by a diff test.

- **Remember retirement and refusal reasons so a tool isn't re-found** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: the capability-miss trigger (T-2270) fires on a missing command; without a tombstone it will suggest the same retired tool again.
  Done when: after retiring a tool for a reason, the same miss shows the tombstone and reason rather than a new find suggestion.

- **Wild: Run a tool bake-off when two shelf tools cover the same miss** — FEATURE — value 3 — effort L — risk med — category: selection
  Why: wild; assumption: find and build both can succeed for one miss. Running both on the miss's replay case and keeping the winner by held-up rate and footprint turns a hunch into a measurement.
  Done when: two tools registered against one miss signature run on its saved case, and the loser is shelved with the scores recorded.

- **Wild: Let a heavily used tool draft its own successor** — FEATURE — value 3 — effort L — risk high — category: self-improvement
  Why: wild; assumption: a built tool with logged failures (non-zero exits, edge inputs) holds the evidence for a better version. The draft goes through the same red-first test and a cold read before any swap.
  Done when: a tool with 5 logged failures yields a candidate v2 on a branch whose test includes those failures as cases, and v1 stays active until the user accepts.

- **Wild: Compost retired tools into lessons** — FEATURE — value 2 — effort M — risk low — category: learning
  Why: wild; assumption: lessons exist (T-0217 confidence idea). Retiring a tool should leave behind "why it failed or went unused" so the next find-or-build decision starts smarter.
  Done when: retiring a tool writes one lesson naming the miss, the tool, and the reason, and `fm lib search` or recall surfaces it on the next similar miss.

- **Wild: Publish a toolbelt report card on the genesis site** — FEATURE — value 2 — effort S — risk low — category: transparency
  Why: wild; the site already refreshes stats daily (T-2326), and the steers favour measures the user can inspect rather than claims.
  Done when: the next genesis publish includes tools found, built, promoted and retired with counts, and the numbers match `fm toolbelt show`.

Next question: Does anything today distinguish a tool the agent actually called from one that merely sat installed, and who else could check that count?
Next question: When a promoted or retired tool is wrong, which signal reaches the user first: a failed task, a doctor warning, or nothing?
