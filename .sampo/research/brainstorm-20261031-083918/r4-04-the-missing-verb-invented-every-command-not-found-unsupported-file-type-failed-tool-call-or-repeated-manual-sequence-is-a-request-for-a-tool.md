# Brainstorm — lens: the missing verb (invented): every 'command not found', unsupported file type, failed tool call or repeated manual sequence is a request for a tool

- **Classify every failed call into a miss taxonomy** — FEATURE — value 5 — effort M — risk low — category: miss triage
  Why: T-2270 fires on "missing command or module" only; unsupported file types, wrong-flag invocations, permission denials and timeouts are also tool requests but are unnamed. Assumption: the event log already records failed Bash/tool results.
  Done when: a fixture log with one of each of 6 failure kinds (not-found, bad-flag, unsupported-type, denied, timeout, wrong-output) yields 6 distinct miss records with kind, and `fm triggers` counts them per kind.

- **Cluster hand-typed sequences into a proposed verb** — FEATURE — value 5 — effort M — risk med — category: sequence mining
  Why: the pack's repeated-manual-sequence signal (e.g. the same fm task evidence / prove / ship steps users retype) has no consumer; T-2270 sees only single commands. Assumption: Bash events keep full command text.
  Done when: a log where a 3-command sequence repeats in 3 sessions produces one proposal naming the sequence, its count and a draft `fm new tool` name; a sequence seen twice produces none.

- **Add `fm peek FILE` for any file type** — FEATURE — value 4 — effort M — risk low — category: file types
  Why: unsupported file types are a miss class in this lens, and the pack's intake and exam paths read only text. Assumption: PDFs, images, xlsx and archives currently stop agents.
  Done when: `fm peek` on a PDF, a PNG, an xlsx and a zip each prints bounded fenced text or a stated "no converter" line plus a miss record, and a second call reads the cache.

- **Treat an unknown fm verb or flag as a vote** — FEATURE — value 4 — effort S — risk low — category: verb demand
  Why: the user's own habit is to invent verbs in asks (fm mandate, fm round, fm exam --jobs); agents guess verbs the same way and the typo is thrown away. Assumption: argparse errors are not logged.
  Done when: `fm bogus` and `fm task new --nope` append a vote; `fm triggers` lists the top 5 with counts, and a near-match gets a "did you mean" line.

- **Make a miss carry its replay command** — FEATURE — value 5 — effort S — risk low — category: replay
  Why: the build-test-use loop (seed row 3) needs a test that fails on the original miss; today the miss note names a path, not a reproducible case. Assumption: the failed command and cwd are recorded.
  Done when: each miss record stores a replay line, and `fm new tool` writes it as the first failing test so the test is red before the code exists.

- **Rank misses by cost of the workaround** — FEATURE — value 4 — effort M — risk low — category: prioritisation
  Why: "a tool missing in 2+ sessions" is a count rule; the user's perf and cost steers suggest minutes and tokens matter more. Assumption: event timestamps let us sum the time between the failed call and the next success.
  Done when: `fm triggers` sorts misses by estimated minutes lost, and a miss with 2 cheap hits ranks below one with 1 expensive hit in a fixture.

- **Shim "command not found" from the user's own shell** — FEATURE — value 3 — effort M — risk med — category: shell hook
  Why: misses outside agent sessions (the user's terminal) are invisible, so the repeated-miss count undercounts. Assumption: the user opts in; nothing is sent anywhere.
  Done when: with the opt-in `command_not_found_handle` snippet installed, a typo-free missing binary appends a local miss and the snippet is removable with one command.

- **Offer a safe replacement verb for every guard block** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: a guard refusal is a failed call that today ends in a stop; the user's push, mandate and consent steers show blocked actions are routine. Assumption: blocks are logged with the rule id.
  Done when: each guard rule has a mapped alternative (or an explicit "user-only" tag), and a blocked command prints it; a rule without either fails `fm doctor`.

- **Generate a verb from `--help` of an installed binary** — FEATURE — value 3 — effort M — risk med — category: wrapping
  Why: many misses are "I know a CLI does this but not how". Assumption: `--help` is parseable enough for a thin wrapper plus smoke test.
  Done when: `fm wrap jq` writes a wrapper with a test that runs it on a sample and passes, and refuses a binary whose help yields no flags.

- **Wild: Turn a recorded manual session into a tool** — FEATURE — value 4 — effort L — risk med — category: record-to-tool
  Why: wild; assumption: the user would rather do a task once by hand than describe it. `fm record` captures commands and their outputs, then drafts a script plus a test that replays the outputs.
  Done when: recording a 4-step shell session produces a script that reproduces the final output on the recorded input, in a throwaway directory.

- **Wild: Have a cold child invent the verbs fm will be asked for next** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: wild; assumption: a tool-less child given only the verb list and a project description names plausible missing verbs. This mirrors the exam rule that scenarios come from a child that never sees the code.
  Done when: a run produces a ranked list of 20 invented verbs, and `fm triggers` later shows how many of them real misses matched (precision reported).

- **Wild: Cross-check misses against peer tools' changelogs** — FEATURE — value 2 — effort M — risk low — category: ecosystem
  Why: wild; assumption: a verb that Claude Code, Codex or Gemini CLI recently added is probably something Foreman users will try to type.
  Done when: a dated list of peer verbs not covered by any fm verb or skill appears in `fm lib search`'s output for a given miss.

- **Wild: Let a failing shelf tool file its own repair task** — FIX — value 4 — effort M — risk med — category: self-repair
  Why: wild; assumption: tools built by T-2278 will rot. On a nonzero exit with a recognised signature, it files one FIX task carrying the failing input as a fixture.
  Done when: a built tool run on a deliberately bad input creates exactly one FIX task with that input attached, and a repeat of the same failure adds no second task.

- **Verify a "nothing found" search is still true** — FIX — value 3 — effort S — risk low — category: search memory
  Why: `fm plugins find` and `fm lib search` returning nothing leads to building, but a later session repeats the search or never revisits it. Assumption: results aren't cached with an age.
  Done when: a stored empty result carries a date, is reused for 7 days without a new search, then is re-run once.

Next question: When a session works around a missing capability silently (no error, just a longer way round), what trace does Foreman have to even know?
Next question: Which built tools would the user still trust a month later, and what evidence of use would they want to see before saying so?
