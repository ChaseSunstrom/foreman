# Brainstorm — lens: reliability

- **Log every guard denial and its aftermath** — FIX — value 4 — effort S — risk low
  Why: the user never runs commands, so a false-positive PreToolUse deny stalls the loop with nobody to override it. The pack has a bypass corpus (misses) but nothing recording false positives. Mechanism: PostToolUse links each deny to the next tool call (retry, workaround, abandon); repeated workarounds become one yes/no "allow this pattern for this project".
  Done when: a scripted deny followed by a benign reworded retry produces a ledger row, and the third such row surfaces one approval prompt.

- **Record every skipped or fail-open gate and list them at done** — FEATURE — value 5 — effort M — risk low
  Why: hooks fail open and gates have timeouts, flaky reruns and cached passes, so "done" may rest on checks that never ran. Assumption: today that is only visible in a latency log. Mechanism: each skip appends `{gate, reason}` to the task log, and `fm task done` prints "unverified: …" and downgrades the verification grade.
  Done when: forcing a gate timeout in a test yields a weak grade and a listed skip.

- **Canary-check cached passes** — FIX — value 4 — effort S — risk low
  Why: cached pass on an identical tree is a correctness bet, and env fingerprints only cover known inputs. Mechanism: re-execute about 1 in 8 cached hits (and always before `done` on L tasks), and on a mismatch purge the cache and note which input was missing from the key.
  Done when: a test with a hidden env dependency (a file outside the key) is caught by the canary and the cache is invalidated.

- **Validate brainstorm child output and account for lens failures** — FIX — value 3 — effort S — risk low
  Why: `fm ideas` spawns tool-less `claude -p` children, and super mode multiplies calls. Assumption: malformed, truncated or refused output is currently parsed loosely. Mechanism: a strict format check, one repair-or-retry, and a "lens X failed: reason" line in the round summary, so a dry round isn't confused with a broken one.
  Done when: feeding a truncated child output gives a retry and a reported failure, never a silent "dry".

- **Retract lessons on contradiction** — FEATURE — value 4 — effort M — risk med
  Why: recall injects lessons at focus. Age decay handles staleness but not wrongness, and logged user corrections already exist. Mechanism: when a correction, a failed task or a tripwire override contradicts a lesson, mark it `disputed` (demoted, shown with a caveat), and `fm doctor` lists disputed lessons for a yes/no delete.
  Done when: a correction citing a lesson's file lowers its recall rank and shows the caveat text.

- **Replay old-version state fixtures through upgrades** — CLEAN — value 3 — effort M — risk low
  Why: schema stamps and fsck exist, but nothing proves that real prior-version state migrates. Mechanism: frozen state directories per released schema under tests/fixtures, run through migrate, then fsck, then a full hook cycle.
  Done when: CI fails if a schema change ships without a fixture and a passing migration.

- **Test against odd repo shapes** — FIX — value 3 — effort M — risk low
  Why: map, impact, affected-tests and tree hashes all assume a normal git repo. Assumption: shallow clones, detached HEAD, worktrees, submodules, no git, unicode or space paths and CRLF are untested. Mechanism: table-driven fixtures that build each shape and run focus, check and done on it.
  Done when: every shape either passes the loop or degrades with a stated note, never a traceback.
