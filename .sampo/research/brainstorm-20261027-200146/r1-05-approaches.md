# Brainstorm — lens: approaches

- **Route playbooks through a prebuilt inverted index** — FEATURE — value 5 — effort M — risk low — category: playbook routing
  Why: The user wants tens of thousands of playbooks routed fast and accurately, with none loaded up front. An index from trigger terms to playbook IDs loads only the matches. Assumption: today's `fm playbooks route` scans the full set.
  Done when: With 10,000 synthetic playbooks, routing returns the expected playbook for each query in a held-out set, at a fixed latency budget the bench enforces.

- **Make the long tail user-only slash commands** — FEATURE — value 4 — effort S — risk low — category: skill listing
  Why: The user asked that skills the model never loads itself (the hook already prints the fm command) become user-only slash commands. That frees the model's listing room for the skills it actually uses.
  Done when: A skill the model never loads appears as a slash command and is absent from the model-facing listing, and the listing's size drops.

- **Two-tier catalog: one-line descriptions in context, bodies on demand** — PERFORMANCE — value 5 — effort M — risk med — category: token budget
  Why: At this scale the context cannot hold every playbook, so only name and one-line description should be visible, with the body fetched by a single call. Assumption: the model can reliably choose from one-line descriptions.
  Done when: Per-reply context stays under the 140k target from the user's last request, measured with `fm cost`, with the routed playbook's body fetched in one call.

- **Prune by measured use, not by guess** — CLEAN — value 4 — effort M — risk low — category: library hygiene
  Why: The user wants playbooks "actually used". A local count of which playbooks are invoked, and which are routed but never followed, shows what to demote to cold storage or delete.
  Done when: A report lists playbooks with zero invocations over a window, and the cold-storage move leaves routing hit-rate unchanged on the bench.

- **Shell prefilter in front of size-gated hooks** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: The PreToolUse:Bash:script hook's p95 sat around 310 ms against a 300 ms budget (T-0832 already names this approach). A cheap grep decides whether the heavy hook runs at all.
  Done when: `bench_hooks --runs 20` reports PreToolUse:Bash:script p95 under 300 ms at load 0.6 per core.

- **Per-project gate lock for affected and evidence runs** — FIX — value 4 — effort S — risk med — category: concurrency
  Why: `fm check --affected` and `--evidence` take the machine-wide gate lock, so every builder waits behind the others. A per-project lock removes that wait while the full check keeps its shared lock.
  Done when: Two builders in different projects run `fm check --affected` at the same time with no wait, and a full `fm check` still serialises against both.

- **Move the rules file's reference text into skills instead of trimming** — CLEAN — value 3 — effort S — risk low — category: rules budget
  Why: The rules file is 6,416 characters, over the doctor's 6,400 budget since T-1520. Moving reference material into on-demand skills gets it under budget without losing content, where trimming would lose content.
  Done when: `fm doctor` reports the rules file under 6,400 characters, and every moved passage is still reachable through a skill.

- **Hard token ceiling per run, enforced by a hook** — SECURITY — value 4 — effort M — risk med — category: usage control
  Why: The user has asked for no token burn, and earlier fixes (compact at 200k, Sonnet builders) rely on the agent behaving well. A hook that stops a run at its ceiling makes the limit a fact, not a hope.
  Done when: A run past its ceiling is stopped by the hook, with a journal entry naming the ceiling and the tokens used, and a run under the ceiling is untouched.

- **Adapt brainstorm lens count to lens yield** — PERFORMANCE — value 3 — effort S — risk low — category: brainstorm cost
  Why: T-0829 proposes dropping lenses that go dry, using lens_rates. Assumption: a lens that yields no new idea across recent rounds adds cost without value.
  Done when: A round with a dried-up lens spawns one fewer child, and the round's idea count is no lower than the prior round's.

- **Evolve playbooks by tournament, archive the losers** — FEATURE — value 3 — effort L — risk high — category: playbook evolution — wild
  Why: The duel bench already scores runs. Finished tasks could propose playbook variants, the bench would pick survivors, and losers would be archived out of routing. Assumption: the duel score tracks real quality, which is unverified.
  Done when: A round of 50 generated variants produces a ranked top set on the bench, and the archived losers never appear in routing results.

- **Compile deterministic playbooks to scripts that run with zero tokens** — PERFORMANCE — value 4 — effort L — risk med — category: token-free execution — wild
  Why: A playbook whose steps are fixed could run as a script, with the model seeing only the verdict. That turns many playbooks into zero-token work. Assumption: a meaningful share of playbooks are deterministic.
  Done when: A playbook marked compilable produces the same pass or fail result as its prompted form on the bench cases, and the run uses zero model tokens.

- **Overnight library consolidation as a scheduled routine** — FEATURE — value 3 — effort M — risk med — category: library upkeep — wild
  Why: T-0793 already moves overnight and periodic work to cloud routines. A nightly pass could merge duplicate playbooks, tighten their trigger terms and rebuild the index, using off-peak usage. Assumption: consolidation can be verified by routing hit-rate, not by reading.
  Done when: After a consolidation pass, the routing bench's hit-rate is at least as high as before, and no playbook is deleted without a logged merge target.
