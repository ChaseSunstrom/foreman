# Brainstorm — lens: bold bets

- **Split sensing from acting** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the pack shows many learners (lessons, triggers, nudges) and a standing worry that a poisoned input could steer one. This answers the question about which learner was never tested with poison.
  Prior art: Codex "Guardian" is a reviewer that retrieves context, and SELinux separates roles, but no harness splits a learned sensor from a fixed actor. Better by: ADCC, where an antibody only tags and a separate killer cell acts. Learned detectors may only write tags to the evidence log. A tiny fixed effector (quarantine, revert, park) holds the only power to act. Novelty: 4.
  Done when: a test feeds a poisoned lesson to every learner and none of them can write a block, delete or run anything.

- **Block benign steps that compose into harm** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard checks single calls, and the frontier notes compound-command bugs (deny rules missed on nested parts, fixed in v2.1.289).
  Prior art: taint research exists, and no harness ships it. Better by: a hapten is harmless alone and immunogenic when bound to a carrier. The guard keeps a short window of earlier calls, and pairs such as read secret then network send match a sequence signature. It is deterministic and needs no model. Novelty: 3.
  Done when: replaying `cat ~/.ssh/id_*` then `curl -d @-` in one window is blocked, and each call alone still passes.

- **Promote learning from somatic to germline** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: the Genesis generations ship fixed rules, while the learned state stays on one machine. Nothing sets a bar for what graduates.
  Prior art: none found. Better by: a learned rule becomes a release candidate only after it fires correctly across at least 3 repos or sessions, passes the 124-case corpus, and the user approves an export. Nothing leaves the machine without that explicit step. Novelty: 4.
  Done when: `fm doctor` lists promotable somatic rules with their evidence counts, and a rule seen in one repo is never listed.

- **Draw a family tree of failures** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: CI-red tasks, reopens and lessons are separate records, and "sibling bug sites" and "cross-reactivity" were only proposed as single ideas.
  Prior art: Sentry-style stack clustering has no lineage. Better by: phylogeny links each failure to its ancestor and flags a "variant of concern" that evades its family's rule, naming the rule to widen. Novelty: 4.
  Done when: a new failure sharing 2 or more features with a known family but missing its rule is reported with the ancestor task id.

- **Strip the workaround biofilm** — FEATURE — value 3 — effort M — risk med — category: debt — **wild**
  Why: flaky reruns and quarantines are Foreman's own band-aids. A hotspot that keeps failing can sit under accreted retries, sleeps, broad excepts and skips.
  Prior art: none found; mutation testing and flaky quarantine tools differ. Better by: a dispersal lane removes the layers one by one in a scratch tree and reports what breaks, so Foreman audits its own band-aids. Novelty: 4.
  Done when: on a fixture with three stacked workarounds, the report lists all three and the failure each hid.

- **Run a vaccination drill for the user** — FEATURE — value 4 — effort S — risk low — category: trust — **wild**
  Why: the frontier reports that users don't know the sandbox escape hatch exists (coygeek), and 15+ prompts per session cause blind approval.
  Prior art: phishing-simulation tools exist for email, and none exist in coding harnesses. Better by: it trains the human, not the tool. Foreman stages a harmless near-miss in a scratch repo so the user sees a block, an unsandboxed call and the override. Novelty: 4.
  Done when: `fm drill` runs offline in under 2 minutes and logs which prompts the user answered correctly.

- **Compute a herd-immunity threshold for tests** — FEATURE — value 3 — effort L — risk med — category: risk — **wild**
  Why: `fm graph blast` exists, but a bad change's spread is shown as a list, not as a threshold.
  Prior art: change-impact analysis and predictive test selection. Better by: treat the co-change graph as a contact network, estimate R0, and name the fewest hub files whose tests push it below 1. Novelty: 4.
  Done when: for a fixture graph, the command names the hubs and the computed R0 drops under 1 after tests are added there.

- **Store incidents as a capped signature array** — PERFORMANCE — value 3 — effort M — risk med — category: memory
  Why: assumption: lessons are recalled as prose per file, which costs injected context.
  Prior art: none. Better by: CRISPR style, with a newest-first array of short signatures, each needing an adjacent context motif (PAM) so it can never match Foreman's own files. The hook matches in microseconds and injects nothing until a match. Novelty: 3.
  Done when: hook p95 is unchanged at 500 signatures, and a signature that matches Foreman's own source is refused on insert.

- **Add the incident's cost to each lesson** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: the pack's trust complaints say lessons go stale or get ignored.
  Prior art: none. Better by: an adjuvant makes a vaccine stick. A recalled lesson carries its measured cost (minutes, tokens, files), so ranking and wording follow real pain. Novelty: 3.
  Done when: a recalled lesson shows "cost 41 min" and ranks above a zero-cost one.

- **Shift spend toward cheap sentinels after harm** — FEATURE — value 3 — effort M — risk med — category: budget
  Why: the risk budget steps autonomy down but leaves the lane mix unchanged.
  Prior art: none. Better by: emergency myelopoiesis. After harm, a burst of short-lived cheap reviewers replaces some builder spend for N hours, then decays. Novelty: 3.
  Done when: after a recorded harm event the next 3 sessions run more cheap reviewers, and the mix returns to baseline in N hours.

- **Derive guard rules from the repo's own scripts** — SECURITY — value 3 — effort M — risk low — category: guard
  Why: the replay corpus has only 124 cases, and every rule so far came from an incident.
  Prior art: none. Better by: reverse vaccinology reads the genome, not the pathogen. It scans Makefile, deploy and CI scripts for irreversible call sites and drafts rules before anything breaks, each checked against the corpus. Novelty: 3.
  Done when: a fixture repo with `deploy.sh --force` gets a drafted rule that passes the corpus.

Next question: which of these ideas needs a second signal that the pack never records, and where is that data kept?
Next question: what would a user need to see to believe the guard is alive on a quiet day?
