# Brainstorm — lens: groundbreaking: 10x, not 10%

- **Route playbooks through a precomputed index, not a scan** — FEATURE — value 5 — effort M — risk med — category: playbook routing
  Why: The request asks for tens of thousands of playbooks, optimized and actually used. The pack already shows 1,229 skills in `plugin/skills/` and a "fm playbooks route stays fast and accurate at…" ask. Assumption: routing today scans the catalog per query.
  Done when: `fm playbooks route` over a 10,000-entry fixture returns in under 50 ms and puts the expected playbook in its top 3 for every query in a held-out set.

- **Enforce the context ceiling in the runtime, not by habit** — PERFORMANCE — value 5 — effort S — risk low — category: token budget
  Why: The user said "foreman should've figured it out itself" about usage burn. The pack has T-1796 (compact at 200k) and a target of under ~140k context per reply, but nothing enforces it.
  Done when: A session that crosses the ceiling compacts without a user command, and the `fm cost` bench reports under 140k context per reply on the standard run.

- **Keep a warm hook worker so each check skips process startup** — PERFORMANCE — value 4 — effort M — risk low — category: hook latency
  Why: `PreToolUse:Bash:script` p95 runs about 310 ms against a 300 ms budget. The pack says box and startup are the whole cost (124 s CPU for a full read).
  Done when: `bench_hooks.py --runs 20` at 0.6 load per core keeps `PreToolUse:Bash:script` p95 under 300 ms on three consecutive runs.

- **Release edit leases when the run ends, not on a timer** — FIX — value 4 — effort S — risk low — category: edit leases
  Why: A model run's edit leases outlive it, and the next run on the same code is refused for 20 minutes. `drop_session` only runs for worker runs.
  Done when: A test ends a model run and shows its leases released before the next run starts, and a killed run's leases are reaped within one sweep.

- **Let affected and evidence checks run beside the full gate** — FIX — value 4 — effort S — risk low — category: gate lock
  Why: `fm check --affected` and `--evidence` take the machine-wide gate lock, so every builder's affected run waits behind the others.
  Done when: Two concurrent `fm check --affected` runs in separate projects both start within 1 second.

- **Explain any stuck run in one command** — FEATURE — value 3 — effort M — risk low — category: run observability
  Why: T-1373 asks for `fm code why ID`, which explains a run from its journal (status, where it stopped, the stall's cause, the next command), plus the stalled card's w/k/m keys.
  Done when: `fm code why` on a fixture stalled run names the stall cause and prints one next command that resolves it.

- **Gate the rules file on its budget at write time** — CLEAN — value 3 — effort S — risk low — category: doctor budget
  Why: The rules file is 6,416 characters against the doctor's 6,400 budget, and it has been over since T-1520.
  Done when: `fm doctor` passes, and a test fails any commit that pushes the rules file over 6,400 characters.

- **Pick the ceremony profile per task kind from duel data** — FEATURE — value 4 — effort M — risk med — category: adaptive ceremony
  Why: T-1231 is the duel goal (more tasks passed, lower cost). T-1266 proposes choosing ceremony per task kind and model from duel data, and it is deferred.
  Done when: The duel bench shows adaptive profiles at lower cost than the fixed profile, with the same pass rate on the held-out tasks.

- **Retire unused skills from the default listing automatically** — FEATURE — value 4 — effort M — risk low — category: skill economy
  Why: The user wants skills "not all loaded, actually used," and the pack has a request for skills the model never loads itself to become user-only commands. Wild: the catalog learns which skills earn their listing slot.
  Done when: After 30 days with zero loads, a skill drops from the default listing and `fm <skill>` still runs it.

- **Serve a 10,000-playbook library from one local index file** — FEATURE — value 4 — effort L — risk low — category: playbook storage
  Why: The playbook library must scale, and the pack gives no sign it has to be loaded whole. Assumption. Wild: store the library as a local full-text index per domain and page in only the shard a query touches.
  Done when: `fm playbooks route` over 10,000 playbooks keeps resident memory under 5 MB and returns the expected shard for each query in a fixture set.

- **Score each brainstorm round against the last and keep only what beats it** — FEATURE — value 3 — effort M — risk med — category: recursive brainstorm
  Why: The request is a recursive brainstorm that builds on the finished product round after round. Wild: each round is a tournament, and the next slate only takes ideas that score above the previous round's top.
  Done when: A round-2 fixture slate contains only ideas scoring above the round-1 top score, and the scores are stored with the slate.

- **Schedule deferrals to the weekly reset in local time** — FIX — value 3 — effort S — risk low — category: scheduling
  Why: `fm task defer --until` takes a local time and "reset" (the weekly usage reset). Deferrals came back at midnight, two hours before the 02:00 reset (T-1802).
  Done when: A frozen-clock test defers a task with `--until reset` and it wakes at 02:00 local, not midnight.
