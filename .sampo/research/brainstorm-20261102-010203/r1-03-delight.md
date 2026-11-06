# Brainstorm — lens: delight

Lens: delight, with the immune-system theme from Mission 8. Every idea ends with the Mission's three lines folded into one: Prior art, Better by, Novelty.

- **Graduate every new rule through a thymus exam** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: the brief-guard path false positives, and the 15+ approval-prompt complaint outside. A new guard rule, trigger or lesson must stay silent on the user's own last N accepted commands and diffs (negative selection) before it is released. It also prints a "born clean: 0 alarms on 4,212 of your commands" receipt.
  Prior art: the replay corpus (124 labelled cases) tests catches, not self-reactivity. Better by: "self" is the user's real unlabelled history. Novelty: 4.
  Done when: a rule that fires on a planted self command is refused at release with the offending command named.

- **Recognise a known failure in one line (memory cells)** — FEATURE — value 5 — effort M — risk low — category: recall
  Why: captured CI-red FIX tasks and per-file lessons exist, but recall is keyed on file, not failure signature. A repeat red shows "seen before: T-xxxx, fixed by <diff>" instantly and pre-briefs the lane.
  Prior art: error-search plugins only match text. Better by: the match is a normalised signature tied to the settled fix and its CI result. Novelty: 3.
  Done when: replaying a prior red CI log yields the earlier task id and fix within one tick, with no model call.

- **Warm the whole harness with a visible fever** — FEATURE — value 4 — effort M — risk med — category: status line
  Why: the risk budget steps autonomy down after harm but the user can't see it. After clustered failures, a temperature on the status line rises. At each level it turns on cold reads, narrows autonomy and mutes chatter. It cools with clean runs.
  Prior art: none found. Better by: one visible, self-resolving state replaces scattered thresholds. Novelty: 5.
  Done when: three injected failures raise the level, and five clean closes lower it, both shown in `fm status`.

- **Require two signals before a noisy detector speaks (costimulation)** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: trigger precision auto-demotes only after the noise has already happened. A lone signal is logged silently, and it surfaces only with an independent second one.
  Prior art: alert correlation in ops tools. Better by: it is pre-emptive, and each detector declares its partner. Novelty: 3.
  Done when: a detector firing alone adds a ledger row with no note, and firing with its partner adds a note.

- **Notice allergies: rules the user overrides by hand** — FIX — value 4 — effort M — risk low — category: guard
  Why: the user is repeatedly pulled into approvals. If the user runs a blocked command themselves within a minute, repeatedly, the rule is marked allergic and proposed for narrowing.
  Prior art: none found. Better by: false positives are detected from behaviour, with no survey. Novelty: 4.
  Done when: three planted manual re-runs after one block produce a narrowing proposal naming the rule.

- **Show the three lines a cold reader should check (antigen presentation)** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the Stack Overflow data shows 66% of developers cite near-miss output and review as the bottleneck. The finish card presents the 3 diff fragments most like past damage, and the cold reader sees only those.
  Prior art: PR summarisers describe the diff and don't rank it. Better by: ranking uses this repo's reopen and revert history. Novelty: 3.
  Done when: the finish card lists three file:line fragments, and a planted past-bug pattern is among them.

- **Calm Foreman's own overreactions (T-regs)** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: the user steers against nag volume. A session-wide governor mutes all non-critical notes when notes per turn spike, says "calming down" once, and resumes after a quiet stretch.
  Prior art: per-alert snooze only. Better by: one global rate regulator across every detector. Novelty: 3.
  Done when: a synthetic burst of 10 notes yields at most 3 shown, plus one calming line.

- **Issue a vaccination card (wild)** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: assumption: users trust what they can see. A weekly harmless planted exposure (a forbidden command, a poisoned issue text, a fake red CI) hits a scratch repo. The card lists each exposure, the outcome and the date, and is shareable as one SVG.
  Prior art: security canaries log to dashboards. Better by: it is a human-readable record with a story per line. Novelty: 4.
  Done when: `fm` writes a card with at least 5 exposures, each marked held or breached.

- **Light up local swelling on a file heat map (wild)** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: assumption: a spatial view beats a list. Files where guard hits, reverts and reds clustered glow in the web UI tree, and a lane's quarantine shows as a swollen region. Heat decays over days.
  Prior art: code-churn heat maps. Better by: the heat is damage, not edits. Novelty: 3.
  Done when: the tree view renders hit-count heat from the ledger, and a decayed file reads cooler after a simulated week.

- **Share learned bad signatures between my machines (wild)** — FEATURE — value 3 — effort M — risk med — category: local-first
  Why: Foreman's "keep a per-machine profile" ideas imply two machines. Guard and failure signatures sync over a private git ref, opt-in, with no content, only hashes and labels.
  Prior art: threat-intel feeds are vendor-wide. Better by: it is the user's own machines, private by default. Novelty: 4.
  Done when: a signature learned on host A blocks the same command on host B after sync, and it shows a "learned on A" tag.

- **Mutate a blocked command into its relatives overnight (wild, affinity maturation)** — FEATURE — value 3 — effort L — risk med — category: guard
  Why: the guard matches fixed rules, and shell rewordings evade them. A tool-less child makes variants of each blocked command. Variants the guard misses are proposed as rule patches, and the idea 1 exam checks them for self-reactivity.
  Prior art: grammar fuzzing. Better by: it seeds from real blocks and prunes by the self-corpus. Novelty: 4.
  Done when: a planted evasion variant of one rule appears as a patch proposal the next morning.

Next question: which of Foreman's detectors has no way to learn that it was wrong, other than the user saying so?
Next question: what would the user show another person about Foreman, and does any current output make that moment possible?
