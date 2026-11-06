# Mission 5 — staying lean and safe (gen 4, #12): a map a session can read

Task: T-2915 (brief 1).

Parent: gen-4/seed.md row 5 → gen-0.md #12: "Staying lean and safe. Each of the above keeps the hooks fast, keeps
context small and keeps the guard intact (see §6)." gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply
here unchanged.

## Capability
Context small enough to use. The gen-3 cross-cutting review's demanding-user complaint: "a user who asks the agent to
consult MASTER.md watches Read fail on size, and this generation lengthens the file instead of splitting it (75758
tokens)". Read on the machine first, as the lean critique asks ("a Mission's baseline step reads the code path behind
each number before trusting it"):
- MASTER.md is now 462,922 bytes in 779 lines (`wc`), about 115,000 tokens, half again what the review saw. The File
  map body is 226,556 bytes and Operations 200,814. Single module bullets run to 32,592 characters on one line, and
  the Read tool cuts any line past 2,000 characters, so even a ranged Read shows a fraction of a module's entry.
- Use: in state/events.jsonl's window, Read on MASTER.md failed 7 times and worked once, while 83 Bash calls grepped
  or sed-cut it instead. Every session is pointed at it: the global rules' "System map: ~/.claude/foreman/MASTER.md"
  line is written by plugin/lib/sampo/setup.py:36.
- The other two numbers in the seed, checked: "SessionStart injects 2,733 characters twice" was not confirmed. There
  is one SessionStart registration (plugin/hooks/hooks.json:4) and none in ~/.claude/settings.json; `sampo burden`
  reads 77 characters a turn on the working copy against 40 on released versions, a lead for the next #12 Mission. The
  project state is 3.2 GB (`du`), 2.9 GB of it under exam/, the prediction's third steer. It goes to Hands below
  rather than this brief, because pruning exam state touches the held-out runs the end-of-run exam reads.

## Grounding (each read in the code on 2026-11-04)
- Every reader of MASTER.md, found by grep (the shared-read rule): plugin/lib/sampo/doctor.py:537 (file-map section
  present), doctor.py:1415-1456 (`check_self_docs`: every verb, skill and module named), doctor.py:1477
  (`missing_modules`), plugin/lib/sampo/cli.py:1955-1969 (a close that adds a plugin entry without a File map row is
  refused), plugin/lib/sampo/demo.py:152 (release-check runs its ```bash runnable fences), plugin/lib/sampo/map.py:216
  (a hub-file note), plugin/lib/sampo/scout.py:323 (a doc glob), plugin/lib/sampo/mandate.py:486 (a standard goal
  item), setup.py:36 (the pointer). 14 test files under plugin/tests read it.
- `## 3. File map` runs from MASTER.md:50 to :324 in five subsections. `## 9. Operations` runs from :405 to :740 in 16.
  The other sections (1, 2, 4-8, 10, 11) total about 35,000 bytes.

## Gaps this Mission targets (coverage: #12)
- understand × Claude Code: a Claude Code session can read Sampo's map in one Read call.
- understand × other agents: any agent with a file reader and a line cap gets the same map, with no Claude Code tool.

## Ideas (from the brainstorm, grounded)
fm mission, then fm ideas --rounds 4 --falsify --crossbreed --seen-latest 6 (research/brainstorm-20261104-002924: 399
distinct ideas; --deepen dropped by today's risk budget, recorded). Grounded:
- "Split MASTER.md into a generated index plus sections that Read accepts", with its twins ("Shard MASTER.md under a
  Read-safe ceiling", "Make MASTER.md a generated index plus per-verb shards each under 8k tokens"): new, and brief 1.
  The brainstorm reached it from five lenses.
- "Serve docs by verb: index card in the injection, `fm doc <verb>` for the rest" (cross-bred): partial. The index
  line and its link do this with no new verb. A verb is approach 4 and is not taken.
- "Collapse the double SessionStart injection to one copy": not confirmed on this machine (see Capability). It is
  carried as a lead with the burden numbers, not built blind.
- "Add `sampo prune --plan` for the 2.4 GB state, with apply going to a TTL trash": new. Held, because exam/ holds the
  held-out runs. Its kill test, a census first (`du` per folder), ran here: 2.9 of 3.2 GB is exam/.

## Approaches
1. Shards plus an index, one reader for the checks: File map and Operations bodies move to docs/map/ by subsection,
   each under 90,000 bytes, long bullets reflowed under 2,000 characters a line. MASTER.md keeps the other sections
   whole and one index line per entry. One helper feeds doctor, cli's file-map check and demo's fences the union.
   Likely outcome: the map in one Read, a module's full entry one link away. Fails if: a test reads a moved line
   directly; the gate and a word-multiset check catch it.
2. use what exists: `sampo outline` and ranged Reads. Fails if: Read's 2,000-character line cut still hides the long
   entries.
3. do less: wrap lines only. Fails if: the file stays around 115,000 tokens, and Read refuses it whole.
4. A `sampo doc SECTION` verb. Fails if: it adds a verb for what a link does (gen-0 §6).

Choice: 1 (70%).

## Exam (an outcome measure, with a live reading)
- Outcome measure: Read on MASTER.md in real sessions. From 7 failures and 1 success in the events window to none
  failing after the close, and the share of MASTER.md lookups done through Bash (83 of 91 today) falls. It is read on
  sessions after the merge, never on the task's own.
- Live reading at close: one Read of MASTER.md in the closing session succeeds whole. `wc -c` shows it at most
  90,000 bytes, and the word-multiset comparison shows no word lost.
- Lean row: always-on characters and hook p95 unchanged (no hook or injection changes). The sweep's lean row reads it.

## Long-horizon goal (end of run)
A fresh agent on any host orients from Sampo's map in two reads, and no session pays for a refused one.

## Risks
- Tests that read MASTER.md for a moved line: 14 files. The helper is the fix. A test that pins MASTER.md's own text
  is updated to read the union, never loosened.
- Merge churn: MASTER.md is the hub file every task edits (map.py:216). This lands as one change with nothing else in
  flight on MASTER.md, and later tasks add their line to the shard and their index line to MASTER.md.
- Drift between index and shard: a test checks that every index line's link resolves and every shard entry has its
  index line.

## Lean
Context: about 115,000 tokens of required reading becomes a 22,000-token map plus links. No verb, no hook.

## Tier share
Brief 1 is tier 3: the system map becomes usable by the sessions it is written for.

## Hands to the next generation
The burden lead (77 against 40 characters a turn) for a measured trim, and the exam/ census (2.9 GB) for a retention
rule that keeps every held-out run the end-of-run exam reads.

## Done when
T-2915's four criteria are green, the full gate passes, and CHANGELOG says it. MASTER.md itself says where its shards
are.
