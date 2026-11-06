# Brainstorm 2026-10-03 (round 6): compat, problem solving, research, subagents, playbooks, recursion — grounded

Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new titles), both past every earlier ideas.md. Pack: the user's three requests verbatim, grounded notes on plugins, research, subagents, playbooks.

## Slate (grounded, scored value/effort/risk)
1. fm next names installed third-party skills that fit the task's stage (plugin compat lens; deepened ×3) — STAGE_REFERENCE (fmcore.py:1398) names only Foreman's own procedures; fmplugins.installed()/profile() already enumerate enabled plugins' skills. V4 · M · low.
2. Research protocol: fm-recon plans sub-questions, ranks sources by tier, anchors each web claim with a short verbatim quote + URL + fetch date, adds a disconfirming pass; recall-first before the web (research lens; deepened) — fm-recon.md has citations + confidence but none of these; delegate.md has no recall-first rung. V4 · S · low.
3. fm-debugger: fresh-eyes read-only agent that returns ranked root-cause hypotheses, each with one cheap discriminating probe (debugging lens: hypothesis ledger, discriminating probes, stuck consult, rubber duck) — the thrash hint (fmrecall.py:200) says "diagnose" but offers no second opinion. V4 · S · low.
4. fm ideas pre-grounds: each new idea in ideas.md carries its nearest finished task from fm recall (brainstorm-quality lens: pre-ground mechanically, stop early on dupes) — the last probe lost 39/40 titles at grounding, mostly already done. V3 · S · low.
5–8. Friction pass (fm-recon on the rsi brief, spot-checked fmguard.py:63/1573, fmhooks.py:1416, fmreplay.py:18): T-0201 one plugin change for marketplace update + plugin update; T-0202 ghost background waits; T-0203 mod reload only for runtime files; T-0204 fm replay skips unchanged logs.

## Already done (dropped)
- Stop-the-line on repeated identical failures: fmrecall.note_failure thrash hint (REPEATS).
- Quarantine pre-existing failures: fm check notes "pre-existing: it also failed before this task" (fmcli.py:1176).
- Measure skill/playbook use, retire unread playbooks: fm cost counts Skill calls and playbook reads and lists unused ones (fmcost.py:345).
- Draft a skill/playbook from repeated manual work: fm repeats proposes project skills.
- Friction items auto-close when fixed: fm friction reports "done since" and rechecks blocks.
- Replay old work against a candidate: fm replay (guard).
- Stamp research and decay it: fm recall halves weight by age (HALF_LIFE).

## Premise false / low value now (dropped)
- Export Foreman as an MCP server; foreign-skill sandbox lane; skill duels; two-model quorum; research tournaments; debate pairs — cost over value for a usage-sensitive user.
- Page cache / fm fetch: WebFetch is Claude Code's own tool; a parallel fetcher adds a network path the guard must police. Low value.
- Implementation subagents in lane worktrees: fm run/lanes cover parallel work; breaks the main-thread-edits contract. Inbox.
- Derive KNOWN_CONFLICTS by overlap: fmplugins._own_findings already matches FOREMAN_OWNS names. Low.
- Hypothesis ledger as a new brief section: the thrash hint already asks to log what is ruled out; folded into item 3.

## Inbox (follow-ups)
- Paired, repeated evals with a variance floor for /foreman:improve; grow eval cases from finished tasks.
- Research notes tied to the files they influenced (expire when those files change).
- Auto-suggest research on unknown-library errors (context7 first).
