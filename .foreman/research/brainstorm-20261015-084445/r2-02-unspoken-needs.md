# Brainstorm — lens: unspoken needs

- **Say "coming from X": add `fm help --from <plugin>` cheat sheets** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: the survey says every rival teaches a one-command habit (superpowers skills, spec-kit's specify→plan, Task Master PRD→tasks). Someone leaving one needs a map from their habit to Foreman's. Importing their data isn't the same as translating the habit. Assumption: the commands to map to already exist.
  Done when: `fm help --from superpowers` prints ≤20 lines mapping each habit to an `fm` command, and a test fails if any named command doesn't resolve.

- **Give every refusal a stable code and an `fm explain CODE` long form** — FEATURE — value 4 — effort M — risk low — category: legibility
  Why: A9 says `fm task done` refuses with four bullets and the one-call shortcut is buried. A4/A11 say the output carries jargon and ticket numbers. Guard blocks may get reason codes in other ideas, but gates, doctor and `task done` refusals don't have them yet. This is the `rustc --explain` pattern.
  Done when: every refusal prints a code such as `FM-G014`, `fm explain FM-G014` prints cause, a worked fix and an example, and a test lists every code the source can emit and checks each has an entry.

- **Show a "what's new for you" card after an upgrade, filtered to verbs the user runs** — FEATURE — value 3 — effort S — risk low — category: upgrade
  Why: Foreman ships many tiny releases (T-0431 is "Release 1.2.16"), and 46 of 108 verbs are never run. A global changelog is noise, so the card should show only what touches this user's usage.
  Done when: the first session after a version bump shows ≤4 changelog lines, and a fixture with a usage log shows only entries for verbs in that log.

- **Close the task and write its CHANGELOG line in the same call** — CLEAN — value 3 — effort S — risk low — category: churn
  Why: the recent commits and asks include "CHANGELOG: T-0841 line" and "CHANGELOG: add round 2's late items" as separate tasks. Meanwhile 159 of 370 finished tasks last week were folded and show as ungraded. Bookkeeping is minting its own tasks.
  Done when: `fm task finish --changelog "…"` appends the Unreleased line, a bookkeeping-only follow-up task is no longer needed, and the changelog test passes.

- **Switch the evidence source when a brainstorm round runs dry** — FEATURE — value 3 — effort S — risk low — category: recursion
  Why: the steer says "recursive" means repeated rounds, and round 3's probe came back nearly dry. Rounds 2–3 only looked inward. A round should notice it is dry and swap to an outward source (rival release notes, clean-HOME run, usage data) instead of re-reading the same pile.
  Done when: a round with <3 grounded ideas records "dry" and the next pack is built from a different evidence source, shown by a test on the pack builder.

- **Publish a measured rival comparison table (install touches, always-on tokens, verbs)** — FEATURE — value 3 — effort M — risk med — category: credibility
  Why: the pack claims ~1.5k chars at SessionStart and 1k words of rules. The survey shows rivals have install paths and footprints Foreman has never measured side by side. A table of real numbers beats adjectives. Assumption: rivals can be installed in a clean HOME with no model calls. Risk is fairness, so each row is stamped with version and date.
  Done when: `fm landscape --table` installs each rival into a temp HOME and prints files touched, always-on bytes and verb count, each with a version and date.

- **Understand requests and refusals in the user's language** — FEATURE — value 3 — effort M — risk low — category: reach
  Why: assumption: Foreman's classifier and prefix grammar (`FIX:`) are English-only, and several of the rivals have large non-English followings. A terse non-English "arregla el timeout" shouldn't fall through to "unclassified".
  Done when: a fixture of 10 requests in 4 languages classifies to the same types as their English twins, with no change to existing English results.

- **Publish deferred briefs as contributor issues, dry-run by default** — FEATURE — value 3 — effort M — risk med — category: community
  Why: 30+ items sit deferred or blocked (T-0787–T-0799, T-0826–T-0832), each already a brief with a "Done when". That's a ready backlog nobody outside can see. Posting is outward-facing, so the verb confirms before it sends anything.
  Done when: `fm issues publish --dry-run` prints title, body and labels for each deferred brief with paths redacted, and nothing is sent without an explicit yes.

- **Add `fm stuck`, a redacted "where I got lost" bundle for the maintainer** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: A1–A11 were found only because someone ran a clean-HOME walkthrough. Real newcomers who stall will just leave. Bundling their last 5 `fm` commands and error as a prefilled issue draft would show the maintainer exactly where they stalled.
  Done when: `fm stuck` writes a local file and prints a prefilled issue URL, and a test shows the home path and username redacted. Nothing is sent without a yes.

- **Wild: paste a zero-install "Foreman Lite" snippet** — FEATURE — value 4 — effort M — risk med — category: funnel
  Why: the biggest newcomer barrier is a ~/.claude rewrite with bypass mode (A2). A generated 40-line CLAUDE.md block carrying the evidence-before-done and capture-don't-chase rules needs no install and no hooks. It is the on-ramp to the full plugin, and the bench can later check it beats bare Claude. Wild.
  Done when: `fm snippet` prints a block under 2 KB generated from the live rules, and a test fails if it names a command that doesn't exist.

- **Wild: unlock a seven-day tour, one seeded-bug lesson per day** — FEATURE — value 3 — effort M — risk low — category: retention
  Why: no rival drips learning over days. Day 1 is red→green, day 2 is evidence, day 3 is capture-don't-chase, day 4 is resume after `/compact`, and so on. Each runs on a throwaway fixture with no model calls and nudges once at SessionStart. Wild.
  Done when: `fm tour` runs lesson N on a seeded fixture and exits 0, and a second call the next day offers lesson N+1.

- **Wild: draft fixes for open good-first-issues in popular small repos, drafts only** — FEATURE — value 3 — effort L — risk high — category: proof
  Why: B shows rival popularity comes from visible community presence, and C says Foreman has no published evidence it helps. An unattended sandbox run on a real open issue produces a proof pack and a PR draft. Nothing is posted without an explicit yes. Wild.
  Done when: a run on a fixture repo yields a diff, a proof pack and an unsent PR draft, and the posting path is refused unless confirmed.
