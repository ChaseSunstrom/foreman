---
name: capability-mapping
title: Capability mapping
area: practice
tags: [planning, capabilities, inventory, gaps, reuse]
detect: []
related: [grounding-ideas, approach-comparison, brainstorming-lenses, ideation-to-briefs]
---
Before building, list what the system can already do, what it almost can, and what is missing, with a file or command as proof for each row.

## Verify
- `fm lib search WORDS`: existing cards and plugin skills for the need were looked up first.
- `grep -rn "<verb or symbol>" --include='*' . | head`: each "already exists" row has a hit you can cite.
- `fm research list`: the map is saved where the next session finds it.

## Test first
Write the map's claims as checkable rows before reading code.
```markdown
| capability | status (have/partial/missing) | proof (path:line or command) |
|------------|-------------------------------|------------------------------|
| export CSV | partial | `grep -n "def export" src/` |
Falsifier: if any "have" row has no proof, it is "unknown", not "have".
Pass = every row is have/partial/missing with proof, zero unknown.
```

## Do
- Start from the user outcome, break it into 5-10 verbs ("import", "dedupe", "notify"), one row each.
- For each verb, search the repo, the installed tools and the standard library; record the hit or the empty search.
- Mark partial rows with the exact gap ("works for one file, not a directory").
- Order the missing rows by how many outcomes they unblock.
- Note the cheapest way to close each gap: reuse, configure, extend, write.
- Re-run the searches after the work; the gap count should drop.

## Avoid
- "We have X" from memory: run the search and paste the path, or mark unknown.
- Mapping the whole system: stop at the verbs the outcome needs.
- Treating a library's mention in docs as capability: check the code path is wired.
- Listing gaps with no size: add a rough cost word (line, file, module) each.
- Building a new thing for a "missing" row without a second search under another name; synonyms hide existing helpers.

## Review
- [ ] Every row has proof or is marked unknown.
- [ ] Partial rows name their precise gap.
- [ ] Gaps are ordered by what they unblock.
- [ ] A reuse option was considered for each gap.
- [ ] The map was saved and linked from the brief.
