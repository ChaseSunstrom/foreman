# fm and fm code brainstorm, round 2: the six anthropics repos, Claude Code parity, "work with anything", full management (T-1382)

Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 new distinct ideas). Inputs: research/claude-code-capabilities.md, research/anthropic-repos-integration.md. Grounded against plugin/lib by two agents in halves, every idea placed in exactly one cluster:
- research/brainstorm-fm-anthropic-half-a.md: capability map, approaches, reliability, simplicity, security, and the three deepened categories (runners, integration, skills): 286 titles in clusters A1–A35.
- research/brainstorm-fm-anthropic-half-b.md: user value, unspoken needs, delight, bold bets, UI and motion: 250 titles in clusters B1–B32.
(Some titles appear in both halves' lens files; each half placed its own. The half files hold every idea title, its grounding with file:line, score and mark.)

## Merged slate (build marks, security first, then value for effort)

| # | capability (clusters) | value | effort | risk |
|---|---|---|---|---|
| S1 | A worker CLI can't change Foreman's grants or state, and a lean claude child whose init event lists a tool or MCP server outside the lean set is killed (A9) | 5 | M | med |
| S2 | The six anthropics repos as pinned fm lib sources with a depth and a licence class (open / source-available / ideas-only), marketplace.json fetched, copy refused past the class (A13, A5, B1) | 5 | M | low |
| S3 | Agent Skills in fm code for any runner: names and descriptions in the planner prompt, a `skill` action loads one body, scripts/ only through the guard (A16, A1, B3) | 5 | L | med |
| S4 | Upstream watch: a source whose sha moved captures one finding (added, removed, renamed, licence class); ls-remote skips unchanged; Claude Code's CHANGELOG lines without a Foreman match become captures (A14, A34, B2) | 4 | S | low |
| S5 | Plugin capability-delta gate: an update adding a hook event, MCP server or script waits for --accept-supply; fm plugins find shows each entry's needs (A2, B6) | 4 | M | low |
| S6 | fm code's judge holds shell rc files and agent settings outside the tree, and an edit step with no effect is reported (A8) | 4 | S | low |
| S7 | Nonce-tagged data envelopes in fm code's slot prompts; metadata fenced (A7) | 4 | S | low |
| S8 | Runner flag lint (--yolo, --dangerously-skip-permissions, danger-full-access acknowledged per template hash), a guard-coverage grade in fm code runners, link-local endpoint deny (A10) | 4 | S | low |
| S9 | Hostile-asset corpus through the indexer, SKILL.md spec lint (name pattern, lengths), over-broad description lint, tolerant marketplace read (a bad entry skipped, renames read as new) (A6, A4, B7) | 4 | S | low |
| S10 | Intake offer: fm code prints one line when a skill matches the request (name, licence class, token cost), never installing; fm plugins suggest lists three with reasons (A18) | 4 | M | low |
| S11 | Slot integrity: elided-code output rejected, unique near-miss edit anchors applied, verify output digested to file:line items; a slot-format ladder (tool call → JSON in text → one field per question) before escalating (A23, B11) | 4 | M | low |
| S12 | claude-compatible flags: -p/--print, -c/--continue, --output-format json map to --plain, --resume, --json (B5) | 4 | S | low |
| S13 | A standing mandate record (text, clauses, contract bounds, expiry) that night and scout read; expiry becomes one decision (B16) | 5 | M | med |
| S14 | Stale safety stack gate: unattended runs and release --push refuse when the last canary or guard-corpus replay is red or old (A12) | 3 | M | low |
| S15 | Containment label in fm code's start event (guard only, or the primitive found) (A11) | 3 | S | low |
| S16 | Model literacy probe (ten graded prompts, 0–10) in fm code runners --probe; a prompt variant ('unknown' escape, evidence quote) measured on the bench (A22, B10) | 3 | M | low |
| S17 | Prompt truncation check: prompt_tokens far under the estimate fails the slot with its cause (A24) | 3 | S | low |
| S18 | Crash hygiene: faulthandler in long verbs, a stale .git/index.lock removed only by owner proof, a doctor filesystem probe (A28) | 3 | S | low |
| S19 | fm check office: a stdlib OOXML asserter for xlsx/docx deliverables (A21) | 3 | M | low |
| S20 | Toolchain activation (.tool-versions and the like, trusted tools only) before workers and gates (A30) | 3 | M | med |
| S21 | Write hygiene: fm code's write keeps a file's line endings and refuses a non-UTF-8 target; option-shaped values fuzzed through path options (B24) | 3 | S | low |
| S22 | Retired model ids flagged by fm code runners --check (B13) | 3 | S | low |
| S23 | fm vetoes prints the retract command for each veto (B18) | 4 | S | low |
| S24 | The site loads nothing third-party: fonts self-hosted, the build fails on an outside host (B20) | 3 | S | low |
| S25 | source_add killed at each step leaves the previous index intact (A15) | 3 | S | low |

Folded into existing briefs: A25 resume validity stamp → T-1338; A26 park on an expired login → T-1356; A27 the plan header names the routing rule → T-1358; A29 → T-1335 and T-1361; A31 → T-1359; liveness (B25) done by T-1329/T-1336; B14 → T-1357; B15 → T-1358/T-1341; B17 → T-1342; B21–B23 → round-1 U8/U19/U2/U3/U4/U15 briefs; B26 → T-1347.

## Skipped, with reasons
A3 detonation sandbox (no OS sandbox: unsafe to promise); A17 and B4 hosting Claude Code plugins on any runner (foreign hooks and MCP run unguarded; revisit after S3 and S5); A19 adoption trials (after S3; the bench has 4 seeds, too few); A20 and B9 cookbook patterns as plan shapes (fm code's loop already is plan-act-verify with fix rounds); A32 architecture refactors; A33 scope process (queue policy, the user's call); A35 new verbs (speculative; the git-conflict resolver is the strongest if one is wanted); B8 discovery and habit-to-skill (mostly exists: fm plugins find, fm lib suggest, fm repeats); B12 finance vertical (S3 makes its skills loadable); B19 self-improvement measurement (exists); B27 run freeze; B28 render fidelity; B29 power-user UI; B30 personality; B31 run directory API (mostly true); B32 reproducibility drills.

Every cluster above with its ideas, grounding (file:line) and done-when is in the two half files.
