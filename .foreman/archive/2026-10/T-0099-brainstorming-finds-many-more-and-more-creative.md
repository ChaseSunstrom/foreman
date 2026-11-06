---
id: T-0099
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T20:09:43Z
updated: 2026-10-02T22:59:42Z
base: d0d52978372bbb7f713859193410e5390f616a20
verified: ok
---
# Brainstorms find more, wilder and unspoken ideas and build off categories
## Raw request
> FEATURE: brainstorming finds many more and more creative ideas, including what the user wants but can't put into words, and builds off categories of ideas
> CONTEXT: user report from a long-running Volt session; Foreman should keep driving the queue unattended
## Interpretation
User: brainstorming doesn't come up with many ideas, creative ones, or things they want but can't say, and doesn't build off categories of ideas.
## Assumptions (confidence)
## Acceptance criteria
- [x] default lenses include unspoken needs and delight; packs carry the user's own words; --deepen runs a yes-and round per top category — verify with `python3 -m unittest discover -s plugin/tests -p test_ideas.py -q`
## Non-goals
## Approach (options → choice → why)
Options: (a) new lenses (unspoken needs, delight), the user's own words auto-added to every pack, category tags and a --deepen round per top category, 8–12 ideas with wild ones; (b) only raise the idea count. Choice: (a). Why: count alone repeats; the user's words and category deepening are what surface unsaid wants and build on ideas.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] lenses, user voice, categories, --deepen, prompt
3. [x] skill + docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md, plugin/skills/brainstorm/SKILL.md, plugin/skills/brainstorm/references/ideas-prompt.md
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_ideas.py -q` → 11 OK (2026-10-02T22:59:27Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_ideas.py -q` → 11 OK (2026-10-02T22:59:27Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -p test_ideas.py -q` → 11 OK (2026-10-02T22:59:27Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -p test_ideas.py -q` → exit 0 · Ran 11 tests in 2.397s / OK [ran] [tree 3141b1944f46] (2026-10-02T22:59:36Z)
- (audit intent) `self-review of the diff and a stubbed run of every new path` → more ideas (8-12, 3 wild), unsaid wants (unspoken needs lens + the user's own words in every pack), building off categories (--deepen yes-and per top category) — each part of the ask is covered and tested [tree 3141b1944f46] (2026-10-02T22:59:36Z)
- (audit edge) `self-review of the diff and a stubbed run of every new path` → no captures or corrections → no user-words section; ideas without a category tag are just not deepened; deepen children go through the same failure/format checks; user words are marked as data [tree 3141b1944f46] (2026-10-02T22:59:36Z)
- (audit intent) `self-review of the diff and a stubbed run of every new path` → more ideas (8-12, 3 wild), unsaid wants (unspoken needs lens + the user's own words), building off categories (--deepen) — covered and tested [tree 3141b1944f46] (2026-10-02T22:59:41Z)
- (audit edge) `self-review of the diff and a stubbed run of every new path` → no captures/corrections → no user-words section; untagged ideas aren't deepened; deepen children share the failure/format checks; user words marked as data [tree 3141b1944f46] (2026-10-02T22:59:41Z)
## Log
- 2026-10-02T20:09:43Z created
- 2026-10-02T22:16:39Z planned from capture
- 2026-10-02T22:16:39Z focused
- 2026-10-02T22:56:00Z user approved core in Claude Code's permission prompt
- 2026-10-02T22:59:42Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- T-0097 [PERFORMANCE M, done, 3 steps] Find and cut where Foreman's time goes — lesson: Measure from the ledgers before cutting: the bookkeeping round-trips, not the tool…
- playbook Verification Loop Skill (skills/playbooks/references/verify/verification-loop.md)
- research t0041-slate-review: HIGH — INTENT — slate item 9 (`brainstorm-20260926-smarter-slate.md:16`)** "Sensitive-path audits: a diff touching auth/crypto/secrets/exec/…
- similar finished tasks took 3–3 steps
## Lessons
- Feed brainstormers the user's own words and a yes-and pass on categories; more lenses alone repeat.
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmideas.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/brainstorm/references/ideas-prompt.md
- plugin/tests/test_ideas.py
