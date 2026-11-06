# Ideas by round (deduplicated titles; details in the lens files)

## Round 1
- Route stages to installed skills at `fm next`
- Parse third-party skill frontmatter into a capability index
- Derive KNOWN_CONFLICTS by overlap, not a hard-coded dict
- Surface installed MCP servers and tools in GROUND and brainstorm packs
- Honor third-party hook outcomes in evidence
- Export Foreman as an MCP server for other agents and clients
- Wild: Let third-party skills declare Foreman stage hooks
- Measure each integration's real contribution
- Wild: Import a skill's procedure as a playbook by yes/no
- Wild: Skill-compat probe via `claude plugin eval` on every plugin update
- Route stages to installed skills from a capability registry
- Print a hypothesis ledger at each failed verify
- Classify the unknown before debugging: known-unknown vs. unknown-unknown
- Rank competing causes by cheap discriminating probes
- Quarantine pre-existing failures at focus
- Treat inconclusive evidence as a distinct state
- Wild: Keep a "surprise log" and mine it for model-of-the-code errors
- Wild: Run a "premortem fork" that argues the root cause is wrong
- Wild: Replay a failing session as a minimal repro by delta-debugging the transcript's commands
- Wild: Add a "rubber duck" mode that answers from the brief alone
- Record "assumed vs. verified" tags on every fact in the brief's evidence section
- Route each stage to the installed skill that fits it
- Import third-party review findings as audit evidence
- Pre-ground ideas mechanically before the main thread reads them
- Skip a brainstorm run when the evidence hasn't changed
- Generate lenses from friction clusters, not a fixed list
- Record why each idea died and feed reason codes back to children
- Generate the integrations table from fmplugins and re-map on plugin change
- Wild: Run a skill duel to retire duplicates
- Wild: Draft a new skill from repeated manual work
- Wild: Let ideas be falsifiable bets
- Wild: Make a scout fleet that grounds ideas with read-only tools
- Probe third-party skills for conflicts by behavior, not name
- Mine skill-call outcomes into a per-stage skill scorecard
- Make brainstorm lenses derive from the user's pushback clusters
- Stop a brainstorm early when the first round is mostly dupes
- Add `fm ground-ideas` to auto-prefilter ideas against code and done work
- Give "background wait" a first-class drive state
- Keep a "user preferences as checks" file the intake reads for every plan
- Wild: Let Foreman adopt a skill it finds useful by writing a thin wrapper
- Wild: Let a "skeptic of the queue" propose cutting tasks before the drive starts
- Wild: Publish Foreman's integrations as a self-describing manifest other plugins can opt into
- Treat installed skills as pluggable audit lenses
- Import foreign skills as Foreman playbooks with a cost note
- Auto-detect third-party conflicts at runtime from observed behavior
- Make brainstorm lenses learn from grounding outcomes per project
- Add a "stuck" consult that forks to a no-context solver
- Wild: Mine installed skills' own failure modes with a skill-vs-Foreman duel
- Wild: Let Foreman write new skills from its own repeated recipes
- Wild: Offer a "second project's lessons" lens in brainstorms
- Wild: Publish Foreman's integration map as a machine-readable manifest other plugins can target

## Deepened: plugin compat
- Add a stage-hint line to `fm next` from a cached capability index
- Rebuild the capability index on plugin change via a cheap mtime check
- Let a skill declare itself a lens via a `fm-lens` frontmatter key
- Warn on always-on cost delta at plugin enable time
- Detect runtime conflicts from hook-collision traces
- Publish `foreman-integration.json` that plugins can target (wild)
- Auto-port a foreign skill into a trimmed playbook (wild)
- Learn which routed skills actually helped, and prune the hints

## Deepened: interop
- Build a stage-to-skill capability index at plugin check
- Surface the indexed skill in `fm next` for the matching stage
- Record stage-skill use as evidence in the brief
- Measure integration yield from fmcost and evidence
- Derive conflicts from description overlap instead of the dict
- Tag installed-plugin hooks that touch the same events
- Wild: Let a skill declare a `foreman:` frontmatter block
- Wild: Run a probe eval when a plugin updates
- Wild: Export Foreman briefs as a skill other plugins can call
- Wild: Provide a "foreign-skill sandbox" lane

## Deepened: debugging
- Persist a hypothesis ledger in the brief, fed by failed verifies
- Auto-capture the failing verify's delta from its last pass
- Rank probes by cost and discrimination in `fm next`
- Seed the debugging lens from friction and past lessons automatically
- Stop-the-line detector for repeated identical failures
- Delta-debug a failing session into a minimal repro
- Rubber-duck from the brief alone
- Turn solved bugs into guard and replay regression cases
- Dashboard "debug state" strip showing ledger status

## New ideas per lens
- plugin, skill and MCP interoperability: 10
- problem solving and debugging under uncertainty: 11
- brainstorm and ideation quality: 11
- unspoken needs: 10
- bold bets: 9
