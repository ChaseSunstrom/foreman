# Brainstorm — lens: user value

- **Screen a new repo at birth (newborn screening)** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: assumption: the install-time demo and guard assume a repo already has tests, CI and a protected main. Missing basics are never named.
  Prior art: repo health checkers (OpenSSF Scorecard). Better by: gives a one-yes fix per gap, tied to the guard. Novelty: 3.
  Done when: `fm doctor --newborn` on a fixture repo with no CI or lockfile lists both and offers one fix for each.

- **Trace contagion after a bad merge** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: the pack has gated revert and sibling-site tagging, but nothing says which later tasks built on the bad commit.
  Prior art: none found in coding harnesses; `git bisect` finds the origin only. Better by: lists downstream commits and tasks to re-verify. Novelty: 4.
  Done when: reverting a planted bad commit lists the two later tasks that touched its files.

- **Print a reactogenicity report for every new rule** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the pack has a thymus exam and rule probation, but the user never sees the "sore arm" of a new rule.
  Prior art: none found. Better by: reports blocks, overrides and prompts added in the first week, with a one-word keep or retire. Novelty: 4.
  Done when: seven days after a rule ships, `fm next` shows its counts and a keep/retire choice.

- **Declare immunocompromise when defences degrade** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the risk budget steps down only after harm. Nothing steps down when the guard hook failed to import, the usage window is nearly gone, or the corpus replay is stale.
  Prior art: none found. Better by: acts before harm and states why. Novelty: 4.
  Done when: with the hook import broken in a fixture, unattended lanes refuse irreversible steps and say "defences down: hook import".

- **Probation for panic-born rules (keloid audit)** — FEATURE — value 3 — effort S — risk low — category: rule quality
  Why: assumption: rules written right after a harm spike are over-broad, and the pack has no check for that.
  Prior art: none found. Better by: tags rules by birth context and forces a review after cool-down. Novelty: 4.
  Done when: a rule created within a fever window carries a `born:fever` tag and is queued for review after 14 days.

- **Clock time to containment per incident** — FEATURE — value 3 — effort S — risk low — category: metrics
  Why: assumption: the ledger holds harm and fix timestamps, but no gauge says how fast Foreman contained damage.
  Prior art: MTTR in ops tooling, not in harnesses. Better by: per-incident timeline of detect, block, contain, with a trend. Novelty: 3.
  Done when: `fm outcomes` prints median detect-to-contain minutes per harm class.

- **Turn a pasted postmortem into a tested rule (serum from a stranger)** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: the frontier section shows users hitting sandbox and permission incidents elsewhere. Only the user's own history feeds rules today.
  Prior art: none found. Better by: drafts a rule plus a replay case, thymus-tests it on the user's history, and installs only on one yes. Novelty: 4.
  Done when: pasting a postmortem yields a draft rule, a labelled replay case, and a false-positive count on the 124-case corpus.

- **Hand child lanes decaying maternal antibodies** — FEATURE — value 3 — effort S — risk low — category: agents
  Why: assumption: tool-less and builder children start without the parent's recent hard-won lessons.
  Prior art: none found. Better by: passes a signed short list that expires after N tasks. Novelty: 3.
  Done when: a child's context lists three inherited lessons and drops them after N tasks.

- **Wild: Desensitise muted nudges** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: the pack mutes a signature after two dismissals, permanently. wild
  Prior art: none found. Better by: re-offers a muted nudge at one-line strength after weeks and ramps up only if accepted. Novelty: 5.
  Done when: a nudge muted 30 days ago reappears once at minimal strength and stays muted if dismissed.

- **Wild: Regenerate rules from incident sources (stem-cell rules)** — CLEAN — value 3 — effort M — risk med — category: maintenance
  Why: guard rules are fixed text, so a host CLI change can quietly break them. wild
  Prior art: none found. Better by: each rule stores its incident and replay cases and can be re-derived and re-tested. Novelty: 5.
  Done when: `fm guard regen <rule>` rebuilds the rule and passes its replay cases.

- **Wild: Hunt one bug species with a phage lane** — FEATURE — value 4 — effort M — risk med — category: eradication
  Why: assumption: after a FIX the user wants every instance of that pattern gone, not just siblings.
  Prior art: codemods and semgrep autofix, which don't self-limit. Better by: one targeted lane makes gated micro-commits until a scan finds none, then retires. Novelty: 4.
  Done when: `fm phage "<pattern>"` leaves zero scan hits and one reviewable commit per site.

- **Wild: Turn public incidents into draft rules (antivenom feed)** — SECURITY — value 3 — effort L — risk med — category: threat intel
  Why: the frontier shows sandbox-escape and prompt-injection reports. Foreman learns of them only when the user pastes one. wild
  Prior art: advisory feeds for packages, none for harness behaviour. Better by: drafts rules locally and stages them behind a yes. Novelty: 4.
  Done when: a fixture frontier item produces a staged draft rule with a replay case and no auto-install.

Next question: Which of Foreman's rules or lessons has the user overridden by hand, and what did they know that the rule didn't?
Next question: What would a new user need to see in the first ten minutes to believe the defences are working?
