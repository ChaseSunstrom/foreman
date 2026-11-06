# Brainstorm — lens: blind spots

Reading the pack through the blind-spot lens. The “What earlier brainstorms missed” list is the smoking gun: every one of those is a capability the *user* had to file by hand because no lens predicted it. Each is a class, not a one-off. I’ll name the question that would have caught it, ask it of the whole project, and surface what else in the class is still missing. I’ll also answer the earlier-left questions my lens can answer.

The recurring blind-spot class: **the user is the unmodeled actor.** Brainstorms modelled the agent, the model, the funnel, the Ward, the tower — but not the *user as a surface*. Kalevala-depth, headroom, fleet-claims, the mirror-name, “measure what the user feels,” “keep current with the field,” and “tonight’s lessons into prompts” are all the user reaching into Sampo and finding it only answers for the agent, not for the person.

- **Model the user as a first-class surface, not a config owner** — FEATURE — value 5 — effort M — risk low — category: user-surface
  Why: T-3312 (depth), T-3316 (headroom), T-3340 (measure what the user feels), T-3342 (mirror name) were all user-filed because no lens treated the *person* as a surface with its own grid cells. Every other capability has a user-facing receipt; the user’s own needs (what to stop doing, what to see) do not.
  Done when: `sampo status` has a “you” lane beside “agent,” listing what you no longer have to type, what I assumed about you (strikeable), and what I’m not doing because you went quiet.

- **Name the question a brainstorm should have asked: “Which surface did this ask hit?”** — FIX — value 4 — effort S — risk low — category: blind-spot
  Why: T-3339 (keep current), T-3321 (fleet), T-3352 (Rust) and T-3353 (lessons into prompts) each landed on a *different* surface (schedule, machine, perf, prompt). No brainstorm asked “which surface is this ask about, and what does that surface currently do for the user?” so each arrived as a surprise.
  Done when: every open brief carries a `surface:` tag (web UI / phone / machine / prompt / schedule / guard), and `sampo map` shows which surfaces have zero briefs — the empty ones are the next gap.

- **Make the “missed ask” a standing regression, not a one-time lesson** — FEATURE — value 5 — effort M — risk low — category: blind-spot
  Why: The “missed” list is a snapshot; the class keeps regenerating. The user had to file *nine* of these. The blind spot is that nothing converts a user’s late ask into a *standing* check that would have predicted the next one.
  Done when: `sampo doctor` runs “replay the last 30 days of user-filed asks that no open brief covered” and prints each as a named blind-spot class with a live check.

- **Cold-start the *user*, not just the project** — FEATURE — value 4 — effort M — risk med — category: cold-start
  Why: Earlier brainstorms seeded a new *project* from siblings (wild, listed). None seeded the *user’s* own habits — what they’ll ask next, what they’ll push back on. T-3340 (“measure what the user feels”) is exactly this: the user is a new “project” Sampo must model.
  Done when: on first `sampo` in a repo, Sampo writes a `taste.md` from the user’s 10 most recent corrections across their other repos, and `samo decide` cites it.

- **Model the *other machines and other people* as surfaces** — FEATURE — value 4 — effort M — risk med — category: fleet
  Why: T-3321 (fleet claims) and the steer “manage all of that across sessions… even without direct access… not only one machine” show the user thinks in a *fleet*, but every lens is single-machine. No brainstorm asked “who else, on which machine, sees this?”
  Done when: `sampo estate` lists machines and humans as claimants, and a lane can hold a claim another human renews.

- **Answer: “What does a project with <20 briefs get from a shared model?”** — FIX — value 4 — effort S — risk low — category: blind-spot
  Why: The earlier-left question was never answered by any lens because it’s a *user*-question, not a model-question. The honest answer the class needs: below the line the model says nothing and the *user* gets a “not enough data, here’s what I’d bet” card.
  Done when: `samo decide` on a thin project prints “N briefs, below floor; abstaining; nearest sibling is X” and the abstain is a receipt.

- **Answer: “What does a user who never read MASTER.md need to see?”** — FIX — value 4 — effort S — risk low — category: legibility
  Why: That earlier-left question was asked in a doc lens, not a *user* lens. The user is the one who never reads MASTER.md; the answer is the *one screen*, not a doc.
  Done when: a cold child given only `samo status` (one screen) names which slots are model-driven and the one key to turn each off.

- **Surface the *second-order* blind spot: the user files the *same class* twice** — FIX — value 3 — effort S — risk low — category: blind-spot
  Why: T-3339 (keep current) and T-3353 (lessons into prompts) are the *same* class — “ingest external change into what I use” — filed a month apart. The class is “Sampo doesn’t watch the outside world and fold it in.” No brainstorm predicted the recurrence.
  Done when: `samo doctor` flags “same class filed twice in 30 days” and opens one merged brief.

- **wild — Make the user’s *silence* a blind-spot detector** — FEATURE — value 4 — effort M — risk med — category: user-surface
  Why: The deepest missed ask is the one the user *didn’t* file because Sampo never surfaced the option. T-3340 (“measure what the user feels”) is the hint: felt, not said. No lens predicted that the gap is in the *absence* of an ask.
  Done when: Sampo tracks which capabilities the user has *stopped* using and files a “silence” brief: “you stopped asking me to X in 3 weeks — did I get it wrong?”

- **wild — Ship a “what I didn’t predict about you” confession per generation** — FEATURE — value 4 — effort S — risk low — category: blind-spot
  Why: The blind-spot class is the gap between Sampo’s model of the user and the real user. A per-generation confession makes the gap *visible and shrinkable* instead of a recurring list of surprises. This is the standing-rule answer to T-3312/3316/3340/3342 at once.
  Done when: each Rune generation ends with `samo confession`: three lines of what Sampo got wrong about the user, each tagged to the surface it hit.

- **wild — Run a “stranger with 15 briefs” drill every generation** — FEATURE — value 4 — effort M — risk med — category: blind-spot
  Why: The blind spots are all “the user had to do something Sampo should have.” A stranger holding only the user’s 15 most recent asks — with no code access — exposes which asks are *predictable from the user alone*. That’s the class every earlier lens (all code-side) structurally cannot see.
  Done when: the drill runs headless, scores “how many of the 15 could a user-only model have pre-drafted,” and files the misses as blind-spot classes.

- **wild — Give the user a “I’ll be annoyed if…” line at intake, compiled to a clause** — FEATURE — value 4 — effort S — risk low — category: user-surface
  Why: T-3340 and the “measure what the user feels” ask point at *felt* negatives the user can’t verbalise until asked. The blind spot is that Sampo only learns the user’s negatives from *after-the-fact* pushback. Asking up front for the one thing that would anger them collapses the class.
  Done when: `samo kickoff` asks for one “I’ll be annoyed if…” line, stores it as a clause, and the done-gate checks it.

- **wild — Let the model draft the user’s *next* “I didn’t ask for that” before it’s said** — FEATURE — value 3 — effort M — risk high — category: user-surface
  Why: The blind-spot class is negative space: the user’s pushbacks arrive *after* Sampo ships. The bold version pre-empts: from the user’s pushback history, draft the complaint Sampo is about to draw, so the user can correct *before* the close. This is the mirror of the listed “predict the next ask,” but for the negative, which is what the missed-asks actually are.
  Done when: at close, Sampo prints a one-line “you might say: …” and the user can strike it; a struck line becomes a standing rule.

- **Surface the *process* blind spot: the user files *blocked* work Sampo should have unblocked** — FIX — value 4 — effort S — risk low — category: blind-spot
  Why: T-3321, T-3335/3336/3337 (fm ask on other harnesses) are *blocked* items the user carried. The class: Sampo parks on “blocked by environment” instead of *trying* the other harness. No brainstorm asked “is this block real or just untested?”
  Done when: `samo doctor` runs the blocked-review hourly (as the user asked) and distinguishes “env truly missing” from “not yet tried,” escalating only the former.

- **Name what a fully-featured version still lacks: the *user model* has no surface** — CLEAN — value 5 — effort L — risk med — category: blind-spot
  Why: After every code-side capability (funnel, Ward, model, fleet, triggers) is built, the one surface with no grid cells is the *user themselves*. A best-in-class Sampo would have the user on the same coverage grid as the web UI and the phone: rows of user-states (quiet, in-rush, away, first-day), columns of what Sampo shows and does. That grid is empty.
  Done when: `coverage.md` has a “user” surface row with at least one grounded cell per user-state, and `samo map` renders it.

Next question: Which of the user’s own habits is Sampo *still* making the user do by hand that a “user-surface” grid would catch — and can we list it without reading any code, only the ledger?
Next question: When the user goes quiet for a week, does Sampo *know it should be quieter too*, and is that quietness a logged, reversible decision?
