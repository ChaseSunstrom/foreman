# Brainstorm — lens: unspoken needs

- **Name the silent "I didn't know Sampo could do this" asks in the next pack** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: The user's own words show a pattern: they keep asking for things that *exist as a verb or a mechanism* but aren't surfaced in the context pack (e.g., `fm ask` on Codex/Gemini, lane brief --ready, sampo kickoff ID). The need behind: "I trust Sampo to tell me what it already does so I stop re-asking." Assumption: the user's repeated asks correlate with existing-but-unseen capabilities.
  Done when: every "already built" drop in the last 30 ledger entries maps to a named verb, and the next context pack includes a "things you could have asked Sampo instead" line.

- **Stop the drive from parking Foreman-filed items I already knew about** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: T-2450, T-2444, T-2428, T-2441 wait under `--round-first` because Foreman filed them. The user's unspoken need: "if *you* filed it, you should own the waiting, not me." The current rule (steer 2026-11-01 #2) holds them, but the user has to manually notice they're stuck.
  Done when: `fm next` prints a one-line "held by round-first: N items, oldest Xh" and the drive auto-escalates after 24h with a `fm decide` record.

- **Surface which model saw which bytes, per session, in the morning card** — FEATURE — value 5 — effort M — risk low — category: privacy
  Why: The user steered: "manage all of that across sessions too… even without direct access." Unspoken need: auditability without a dashboard. The ledger exists (T-2625, T-2868), but the user never *reads* it. The need: "I want to know, in plain words, what the local model was shown overnight and what it couldn't reach."
  Done when: the morning card has a ≤3-line "data flow" section: "local 4B read: 12 briefs, 3 ledger lines; sent nowhere; blocked 2 private paths."

- **Let the user veto a *class* of Sampo behaviour, not just a single item** — FEATURE — value 4 — effort M — risk med — category: control
  Why: The user's pushes are always about specific incidents ("don't push to main," "don't run Haiku for cards"), but the unspoken need is a *preference dial*: "I don't want Sampo to ever do X in *any* repo." Currently each steer is a one-shot rule. The user will want a `sampo prefs` file with per-repo, per-verb, per-model toggles that the drive *must* read before acting.
  Done when: `sampo prefs list` shows a per-verb allow/deny/ask table, and the drive's `fm next` refuses a verb that's set to "deny" without the user re-enabling it.

- **Warn when a request names a capability Sampo will only ship in the *next* model, not this one** — FEATURE — value 4 — effort S — risk low — category: expectation
  Why: The user's asks repeatedly hit the "not-yet local model" boundary (T-0035, T-1366, the entire uplift part 1). Unspoken need: "before you start, tell me this is a 27B-only task and the 4B will fail." The context pack doesn't tag briefs by model tier.
  Done when: every brief carries a `model-tier: 4B|12B|27B|frontier` field, and `fm next` flags a tier mismatch with a one-line "this needs 27B; local 4B will likely loop."

- **Make the "I'll re-ask this later" wish list visible and auto-referenced** — FEATURE — value 5 — effort M — risk low — category: continuity
  Why: The user drops items ("Source rea moved," "Breakage ahead: bced376… not a breakage") with the implicit expectation Sampo *remembers* the dismissal reason. Unspoken need: "when I ask again in 3 days, don't re-explain why it was dismissed — just cite the old drop." The ledger has the drops, but no retrieval path at intake.
  Done when: `fm task add` with a title matching a dropped item within 90 days prints "dropped 2026-11-04: <reason>; re-raise?" as a one-line prompt before filing.

- **Show the user's *own* undo rate as a trust score per capability** — FEATURE — value 4 — effort S — risk med — category: accountability
  Why: The user steered: "measure what the user feels." Unspoken need: "if I keep reverting Sampo's work, I want to see that, per verb, before Sampo does it again." The close-holds verifier (T-2868) tracks outcomes, but not the user's *reverts*.
  Done when: `fm doctor` prints a per-verb "user revert rate (30d)" line, and the drive's `fm next` skips a verb whose rate exceeds 50% unless the user overrides.

- **Pre-draft the user's *pushback* on the next close, so they can correct Sampo before Sampo ships** — FEATURE — value 5 — effort L — risk med — category: anticipation (wild)
  Why: The user's "the user's own words" section is dominated by corrections ("not a breakage," "absorbed by T-2893," "stale"). Unspoken need: "if you're about to close something I'm going to complain about, *draft my complaint first* so I can just edit it." This inverts the model: instead of predicting the ask, predict the *objection*.
  Done when: at `fm task finish`, the local model drafts a one-line "I think you'll say: <objection>" on the finish card; the user's actual next message is diffed against it, and the hit rate is logged.

- **Give the user a "Sampo is thinking" *reason* line, not just a spinner** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: The user's steers show frustration with *silent* waits ("Stopped on spend and disk, not only on usage limits"). Unspoken need: "when Sampo is idle or slow, tell me *why* in words I can act on." The drive's typed stops exist, but the CLI pane doesn't surface them.
  Done when: the pane's work bar shows a one-line "waiting: <reason>" (e.g., "waiting: local 4B busy with moons funnel, ETA 12m") instead of a generic spinner.

- **Let the user *teach* Sampo a new phrase by saying it once, with a confirm** — FEATURE — value 4 — effort M — risk low — category: personalization
  Why: The user's vocabulary is very specific ("rune," "forge," "moons," "tower," "kalevala"). Unspoken need: "when I introduce a new term, Sampo should adopt it in *all* future surfaces without me repeating it." Currently each steer is a one-shot; there's no "add to vocabulary" path.
  Done when: a user message containing a novel noun (not in MASTER.md or the role table) triggers a one-line "adopt '<noun>' as Sampo vocabulary? [y/n]"; on yes, it's added to the role table and the next Mission pack includes it.

- **Show a "what Sampo *stopped* doing" diff after each rename or migration** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: The Foreman→Sampo rename touched 36 code sites (T-3342), and the user's drops show confusion about what changed ("Source rea moved to 4b961e37"). Unspoken need: "after a big change, show me what *stopped working* or was *removed*, not just what was added."
  Done when: `fm ship` includes a "retired/renamed" section in the commit message, listing every verb, path or alias that no longer resolves, with its replacement.

- **Make the *user's* calendar file the "don't touch the GPU now" signal, with a fallback** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: The user's steers show the GPU is shared with the moons funnel, exams, and training. Unspoken need: "when I have a meeting, Sampo should *pause* heavy local work, not just wait out the usage limit." The context pack mentions "schedule heavy local work into the user's calendar busy blocks" as an idea, but it's not built.
  Done when: `sampo drive` reads a local iCal or a `.sampo/calendar.ics` and pauses local-model lanes during marked busy blocks, logging the pause in the ledger.

- **Let the user *rehearse* a decision without committing it, with a rollback guarantee** — FEATURE — value 4 — effort M — risk med — category: safety
  Why: The user's steers show they push back on irreversible actions ("irreversible… only outward actions, protected core, merges"). Unspoken need: "before you *do* something, show me the *exact* diff and let me say 'no' without it being logged as a steer." The current `fm decide --kind costly` requires a user prompt.
  Done when: `fm decide --dry-run` prints the full diff, the ledger entry it would write, and the rollback command; nothing is applied unless the user types the commit hash.

- **Predict the *user's frustration* from their *silence*, not just their words** — FEATURE — value 5 — effort L — risk high — category: anticipation (wild)
  Why: The user's most damaging corrections come *after* a delay ("stale," "absorbed by," "not a breakage"). Unspoken need: "if I don't respond to a close within 30 minutes, Sampo should *assume* I'm unhappy and re-check before proceeding." The "treat the user's silence as a label" idea exists in the ideas-so-far, but it's not wired to the drive.
  Done when: the drive tracks time since the user's last message per task; if a task closed and the user is silent for 30 minutes, the next `fm next` leads with "you haven't confirmed T-XXXX; proceeding as if accepted?" with a one-key "reject and re-open."

- **Show the *user's own* hand-edits as a "taste file" Sampo reads before drafting** — FEATURE — value 5 — effort M — risk low — category: personalization (wild)
  Why: The user's steers are full of taste judgments ("wild," "simple," "like X"). Unspoken need: "when I edit Sampo's output by hand, that edit *is* my preference data. Use it." The "mine the user's hand edits" idea exists, but it's not a *file the user can read or edit*.
  Done when: every user hand-edit of Sampo-written prose is appended to `~/.sampo/taste.md` with a timestamp and the original Sampo text; the next drafting model loads this file as a few-shot preference set, and the user can read or prune it directly.
