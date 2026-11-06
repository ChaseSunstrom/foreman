# Brainstorm — lens: approaches

- **Write an agent-readable install guide so the user can say "install Foreman" to Claude** — FEATURE — value 4 — effort S — risk low — category: install
  Why: Every popular rival installs in one command or one pasted sentence. Foreman's install rewrites `~/.claude` and only says "Claude Code asks you to confirm once" (evidence A2). Assumption: agents follow a published `INSTALL.md`/llms-install-style file.
  Done when: a cold Claude session given only the repo URL and "install this" reaches a passing `fm doctor`, narrating each change and asking before each `~/.claude` edit (tested with a scripted fake model).

- **Carry adoption in the repo so teammates get prompted to install** — FEATURE — value 4 — effort M — risk med — category: distribution
  Why: Rivals spread by marketplace entry. Foreman has no Anthropic-marketplace path and no repo-carried one (B). Assumption: project `.claude/settings.json` can declare `extraKnownMarketplaces` and `enabledPlugins` so a clone triggers a trust prompt.
  Done when: `fm share` shows a diff of the settings and gate files it would add, writes them only after a yes, and a clean-HOME clone of that repo offers the Foreman install.

- **Ship cold-start priors distilled from the 688-task ledger** — FEATURE — value 4 — effort M — risk low — category: cold start
  Why: The pack's "learn per-user estimates from history" ideas all start empty for a newcomer, while Foreman's own ledger has real numbers (C). Assumption: an aggregate table of cost by type and tier, gate yield and rework rate can be shipped as a data file with no private content.
  Done when: in a clean HOME, `fm task new` shows a time/cost range for a task type, labelled "shipped prior", and the label disappears once 5 local tasks exist.

- **Unbundle the three signature behaviours into single-job entry plugins** — FEATURE — value 4 — effort M — risk med — category: distribution
  Why: Rivals win with one-line promises; Foreman's first screen is abstract (A1). Its distinct strengths (the guard, resume after compact, done needs evidence) could each be a one-sentence listing. Earlier "core/labs" ideas split by size, not by job.
  Done when: `foreman-guard`, `foreman-resume` and `foreman-done` each install alone in a clean HOME, work without the others, and the full plugin upgrades them with no duplicate hooks.

- **Make the `~/.claude` wiring a git-backed journal so uninstall is a revert** — CLEAN — value 3 — effort M — risk med — category: trust
  Why: Uninstall leaves residue and prints "defaultMode = None" (A10). Reversal by construction beats a round-trip test that checks it afterwards.
  Done when: after install and `fm uninstall`, `git -C <journal> diff <pre-install-commit>` is empty and `fm wiring log` lists each change with its reason.

- **Add community gate recipes keyed by detected stack** — FEATURE — value 4 — effort M — risk low — category: gates
  Why: `fm check` detects no test runner (A7) and `fm repeats` suggests single test modules as gates (C). A data-file registry of Django, Next, Cargo, Go and Rails recipes (test, lint, typecheck, affected-test pattern) lets others contribute by PR.
  Done when: in fixture repos for 5 stacks, the first `fm check` proposes the right whole-suite gate and the one-yes accept stores it.

- **Import claude-mem and auto-memory observations into `fm recall`** — FEATURE — value 3 — effort M — risk low — category: switching cost
  Why: claude-mem (~101k stars) is the cross-session memory rival, and Foreman lacks automatic searchable memory (B). Importing removes the reason not to switch. Existing import ideas cover Task Master, spec-kit and CCPM, not memory.
  Done when: a fixture claude-mem database imports into recall, a search returns those items labelled with their source, and re-importing is idempotent.

- **Add `fm report-miss`: a redacted, preview-first bundle for a GitHub issue** — FEATURE — value 3 — effort M — risk low — category: feedback
  Why: There is no published evidence (C) and the bench has 1 case, so real misses from users are the cheapest source. Assumption: nothing leaves the machine until the user opens the prefilled issue link themselves.
  Done when: the command writes a local redacted bundle, prints exactly what it contains, makes no network call, and the bundle loads as a bench case with `fm bench add`.

- **Route user-facing strings through one catalogue so output can be translated** — FEATURE — value 2 — effort L — risk med — category: reach
  Why: assumption: "THE plugin" implies non-English users. Output text is scattered, and the jargon in A11 shows it is hard to audit. A catalogue also enables a plain-words lint.
  Done when: every `fm status` and `fm doctor` string comes from the catalogue, and a test fails on any bare literal added outside it.

- **Wild: Issue-comment `/foreman` Action that returns a PR with a proof pack** — FEATURE — value 4 — effort L — risk high — category: reach
  Why: wild. It reaches people who never open a terminal, and it matches the CCPM (issues-as-audit-trail) pattern. Needs explicit repo opt-in and a spend cap, since it runs unattended.
  Done when: on a test repo, a maintainer's `/foreman fix` comment produces a PR whose body links the evidence ledger, and an unauthorised commenter is ignored.

- **Wild: Day-30 time capsule that scores the user's own annoyance** — FEATURE — value 4 — effort M — risk low — category: proof of value
  Why: wild. The install asks "what annoys you most about Claude Code?", and the user's own baseline sentence is the only metric no rival offers. Day 30 reports which of those complaints the ledger shows reduced, or says it can't tell.
  Done when: in a fixture history, a complaint "it says done when tests fail" turns into a before/after count of evidence-less closes, and the report says "can't tell" when data is thin.

- **Wild: Volunteer-compute bench with opt-in leftover quota** — FEATURE — value 2 — effort L — risk high — category: proof of value
  Why: wild. The public benchmark needs many runs, and users' unused weekly quota is idle. Strictly opt-in, runs only public fixture cases, and sends back only pass/fail counts.
  Done when: with the setting off, nothing runs and nothing is sent. With it on, a run uses only the public fixtures and stops at the user's set quota share.
