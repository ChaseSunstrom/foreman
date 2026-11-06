# Brainstorm — lens: self-modification: a toolbelt that learns which found or built tools held up, retires the unused and promotes the reused, measured and reversible

- **Journal every toolbelt change as one reversible entry** — FEATURE — value 5 — effort M — risk low — category: toolbelt ledger
  Why: assumption: found/built tools are installed by separate verbs (`fm plugins find`, `fm mcp new`, `fm new tool`) with no common undo; "measured and reversible" is the lens's core need.
  Done when: `fm belt undo <entry>` after an install, build, promote or retire restores the prior files and config byte-for-byte, checked by a test that diffs the tree before and after.

- **Log a use event per tool call, tied to the task that used it** — FEATURE — value 5 — effort M — risk low — category: usage ledger
  Why: T-2270 fires on misses but nothing in the pack records whether the filled tool was ever called again; retirement and promotion both need this signal.
  Done when: after a session calls a built script, `fm belt show` lists the tool with a use count and the task ids, derived from the event log rather than typed by the tool.

- **Score each tool by whether the tasks it touched held up** — FEATURE — value 4 — effort M — risk med — category: outcome scoring
  Why: the pack already has outcome survival (re-fixed, reverted, red after merge) for lane routing (T-2291); the same signal can grade tools. Assumption: task-to-tool links exist once use events are logged.
  Done when: `fm belt score` prints a held-up rate per tool, and a fixture tool whose tasks were all reverted ranks last.

- **Propose retiring tools unused for N sessions, never retire silently** — FEATURE — value 4 — effort S — risk low — category: retirement
  Why: the lean ratchet (Mission 8/#12) warns when always-on footprint grows; unused tools are footprint with no benefit. Retirement lands as one card the user answers in a word.
  Done when: a fixture tool unused for N sessions appears in `fm doctor` as a retire proposal, and nothing is removed until the user runs the named command.

- **Promote a tool reused across two repos into a global library card** — FEATURE — value 4 — effort M — risk med — category: promotion
  Why: `fm lib` cards exist and the pack lists "Let a built tool graduate into a shared card" only as a wild idea. Assumption: reuse can be detected by a content hash recorded in the ledger.
  Done when: the same tool hash used in two repos yields a promote proposal, and approval creates a card that `fm lib show NAME` prints.

- **Remember retire and refuse reasons so a tool isn't re-found** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: the capability-miss trigger (T-2270) would otherwise re-suggest the same plugin the user already retired. Assumption: the find step can read a denylist.
  Done when: after retiring tool X with a reason, `fm plugins find` for the same miss shows X as "retired: <reason>" instead of a candidate.

- **Charge each tool its always-on footprint against the lean ratchet** — PERFORMANCE — value 3 — effort S — risk low — category: footprint
  Why: the ratchet records rules chars, descriptions chars and hook p50 per ship; a tool that adds a skill description costs context every session. Assumption: skills built by `fm new skill` add to that count.
  Done when: `fm belt show` lists footprint chars per tool, and a ship that adds a built skill moves the ratchet number.

- **Re-test shelf tools when their world changes** — FIX — value 4 — effort M — risk low — category: tool health
  Why: found plugins and MCP servers depend on host versions and binaries. Assumption: a changed Claude Code version or manifest hash is detectable.
  Done when: bumping a fixture dependency makes `fm doctor` re-run the tool's test and list it as broken, naming the failing check.

- **Replay the original miss against any changed tool before keeping the change** — FEATURE — value 4 — effort M — risk low — category: regression guard
  Why: T-2278 scaffolds a failing-first test per built tool; storing the miss as that test makes every later edit, promotion or successor replayable.
  Done when: editing a built tool to break the original miss makes the replay fail and blocks the promote.

- **Wild: Let a tool propose its own successor** — FEATURE — value 3 — effort L — risk high — category: self-improvement
  Why: wild. When the use ledger shows a tool failing on recurring inputs, a child drafts a revised version in a scratch lane, tested against the stored failures, and queues it as a diff for the user.
  Done when: a fixture tool with three logged failing inputs produces a candidate version that passes them, shown as a diff and never applied without a user command.

- **Wild: Run a tool bake-off when two shelf tools cover the same miss** — FEATURE — value 3 — effort M — risk med — category: selection
  Why: wild. Found and built tools can overlap; running both on the stored miss cases picks one by held-up rate and retires the loser to a reversible archive.
  Done when: two fixture tools with the same declared capability get a bake-off result, and the loser is archived with an undo.

- **Wild: Compost retired tools into lessons** — FEATURE — value 2 — effort S — risk low — category: learning
  Why: wild. Retirement writes a one-line lesson (what the tool was for, why it failed or went unused) into the existing lessons store, so recall of it can prevent the next rebuild.
  Done when: retiring a fixture tool adds a lesson that `fm lessons` returns when a similar miss is queried.

- **Show the belt's net effect as a single honest number** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: assumption: the user will ask whether this self-modification pays. Compare misses-filled and minutes saved against footprint and upkeep, with the denominator printed beside it.
  Done when: `fm belt report` prints misses filled, reuse count, retired count and footprint, and each figure traces to ledger events.

Next question: Which toolbelt change would the user refuse to see happen without asking, and does the journal's undo cover it?
Next question: How does Foreman tell a tool that wasn't used because it wasn't needed from one that wasn't used because the agent never found it?
