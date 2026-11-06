# Brainstorm — lens: user value

- **Offer a counter-proposal when a request can't be done** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the user's complaints are "why can't I…" and "it just isn't doing anything"; today a refusal or a stalled run ends in a dead end. Assumption: the nearest doable variant can be derived from the plan slots and runner capability cards.
  Done when: a seeded impossible request (e.g. a runner without write access) ends with up to 3 labelled alternatives, each with a price and a one-key run, and a test asserts that no failed request ends without at least one.

- **Run a trial slice first, then ask go or no-go** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: "10x better" and "fully implemented" requests are large and expensive. Assumption: users would rather judge a thin real slice than a plan. Distinct from a walking skeleton because the slice is shown to the user with the full run's price and time before they commit.
  Done when: `fm code --slice "<big request>"` runs about 10% of the plan in a lane, shows its diff and proof plus a projected full cost, and the full run starts only after one key.

- **Verify advice pasted from other chatbots** — FEATURE — value 4 — effort M — risk med — category: capability
  Why: assumption: users bring snippets and "just do X" advice from other tools. Pasting a bare block of text into the request box is a common input that today is treated as a normal request.
  Done when: pasting a fenced answer plus "check this" runs each claimed step in a throwaway lane and returns a per-claim verdict (holds, fails with output, or untestable), and a seeded wrong answer is marked as failing.

- **Land everything proved, across all projects, in one pass** — FEATURE — value 4 — effort M — risk med — category: management
  Why: the app already has a home over every project and per-run proof grades. The "fully management" ask implies one gesture that clears the finished pile. Assumption: a grade threshold plus per-project policy is safe enough to merge on.
  Done when: `fm code land --all --min-grade strong` merges only runs at or above the threshold, skips the rest with reasons, and a fixture with one weak run leaves it unmerged.

- **Give each finished run a live preview until accepted** — FEATURE — value 4 — effort M — risk med — category: review
  Why: the user asks for visible examples ("show better examples"). Reading a diff is the slowest way to judge a UI or CLI change. Assumption: the project map already knows how to start the app.
  Done when: a finished run in a worktree can be started with one key on a free port and printed as a URL or terminal transcript, and it stops cleanly on accept or discard with no leftover process.

- **Show a plan wallet across subscriptions and keys** — FEATURE — value 3 — effort M — risk low — category: cost
  Why: runners include claude, codex, gemini and keyed endpoints, but nothing shows what each seat has left. The user says "work with anything", which means several seats. The wallet is the visible input that routing and quota pausing can read.
  Done when: `fm code wallet` lists each runner's known limit, usage, reset time and last error, and a seeded rate-limit failure shows as "empty until <time>" and moves the default route elsewhere.

- **Report attention minutes against a manual estimate** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: the user pushes hard for "10x" but has no number that says so. Assumption: the estimate comes from the user's own past manual commit sizes and times. It should also say when a run was not worth it.
  Done when: a run's close line shows attention minutes (time the user actually spent answering or reviewing) beside an estimated manual time, and a trivial task is flagged as "faster by hand".

- **Explain unfamiliar stacks by analogy to the user's own** — FEATURE — value 3 — effort S — risk low — category: understanding
  Why: assumption: the user works across many stacks. They said "I should be able to do anything with it", and that includes areas they don't know. The explanation uses their own repos' idioms.
  Done when: `fm code explain <file>` with a language setting of "known stacks" produces a gloss that cites at least one concept from a named project of theirs, and a test checks that the citation resolves to a real file.

- **Schedule around presence and calendar** (wild) — FEATURE — value 3 — effort M — risk low — category: attention
  Why: wild; assumption: a local `.ics` file and mic/camera-in-use status are readable without network. Heavy gates and pings pause during a call, and the day's free gaps size what an unattended run attempts.
  Done when: with a fixture calendar containing a meeting now, a queued heavy run waits and notifications are held, and the held items arrive as one digest when the meeting ends.

- **Port a feature from any repo, clean-room, with a licence gate** (wild) — FEATURE — value 4 — effort L — risk high — category: capability
  Why: wild; extends the requested six-repo integration to "give me the thing that repo does". It reuses the licence-class ledger so ideas-only sources produce a spec, not copied code.
  Done when: pointing at a fixture repo with an MIT licence yields an attributed port plan, a restricted-licence fixture yields a behaviour-only spec with a verbatim-overlap check passing, and an unlicensed fixture is refused.

- **Mine exported chat history for abandoned plans** (wild) — FEATURE — value 3 — effort M — risk med — category: privacy-safe intake
  Why: wild; assumption: the user has chat exports (JSON) from other assistants. Intake is currently only what they type to Foreman. A local, opt-in scan turns "we never finished that" into queue candidates.
  Done when: `fm code import-chats FILE` runs fully offline, lists candidate tasks with a quoted source line each, queues none without a key, and a network-denied test passes.
