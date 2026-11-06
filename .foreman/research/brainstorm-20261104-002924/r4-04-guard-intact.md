# Brainstorm — lens: guard intact

- **Cache Ward verdicts by rules hash** — PERFORMANCE — value 4 — effort M — risk med — category: hooks
  Why: the mission's top gap is hook speed with the guard intact. The pack's ideas speed up how the Ward is loaded or prefiltered, but none caches the verdict itself. Assumption: most repeat commands (`git status`, `fm next`) hit the same normalised shape.
  Done when: `bench_hooks.py` shows p95 on a replayed 1,000-command corpus falling, and mutating one rule changes the key so a previously cached allow becomes a block in a test.

- **Generate the Ward exam from the rename's alias map** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: the steer says the Ward must refuse under the Sampo names whatever it refuses under the Foreman ones. Aliases, `SAMPO_*`/`FM_*` env vars and shim plugins are exactly where a lean cut or rename leaves a spelling uncovered.
  Done when: a test enumerates every verb, env var and plugin id in the renames map, runs each blocked-corpus command under each spelling, and fails on any verdict that differs.

- **Make a block independent of its log write** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: state is 2.4 GB and children write to a tmpfs under `/run/user/1000`. A full disk or a failed ledger append must never turn a deny into an allow. Assumption: some code path logs before it returns the verdict.
  Done when: with ENOSPC and a read-only state dir injected, the hook still prints a deny for a known-bad command and exits with the deny code.

- **Fail closed to an embedded floor on a torn rules file** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: pruning, atomic installs and lane worktrees all touch rule files while hooks run. Assumption: a half-written or missing file currently fails open (unverified; the pack only says fail-open is declared per hook).
  Done when: truncating the rules file mid-test makes the Ward deny the irreversible command class from a minimal built-in list and print a one-line "rules damaged" notice.

- **Let repo-local Ward config only tighten** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: opening an unfamiliar repo can bring in config the agent then obeys. A merge that is monotone (deny adds, allow never) makes repo config safe to read without a trust prompt.
  Done when: a repo file containing an allow for a globally denied command has no effect, a repo deny takes effect, and both cases are tests.

- **Store blocked commands as shapes, not raw strings** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the 2.4 GB state keeps decision records, and blocked commands often carry tokens or paths. A normalised shape plus a salted hash keeps the stats and drops the secrets, which also helps the prune.
  Done when: after a blocked `curl -H "Authorization: [REDACTED]"`, no ledger row contains `abc123`, and `fm outcomes` still groups it under the same rule.

- **Diff the Ward against the host's own permission classifier** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the standing rule asks for weakness signals Sampo didn't author. Claude Code's built-in permission decisions are such a signal, and disagreement points at either a Ward gap or a needless block. Assumption: the host exposes a way to dry-run its verdict, or its denials appear in transcripts.
  Done when: a report lists commands the host denied that the Ward allowed, ranked by frequency, from the last 30 days of transcripts.

- **Price every context cut with one new guard test** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: many ideas cut injected text, but none ties a cut to growth in guard coverage. A "cut-for-test toll" keeps the lean mission from quietly eroding the Ward.
  Done when: the ship gate fails a diff that removes lines from an injection source without adding or citing a test in the guard exam.

- **Show the Ward's armed state in the per-turn line at no extra length** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: per-turn burden is 48–76 characters, and the user can't currently tell whether the Ward is live without running something. Replace existing characters with a state glyph instead of adding any.
  Done when: the per-turn line is no longer than today's maximum, and flips to a visible "unarmed" mark when the Ward's hook is removed in a test.

- **Run a start-of-session Ward self-check with a time cap** — PERFORMANCE — value 3 — effort S — risk med — category: hooks
  Why: SessionStart fires twice today (2,733 characters each). One merged hook can run a single bait check in the saved time. Assumption: the double firing is two registrations, not one hook twice.
  Done when: one hook fires per session, the self-check adds under 10 ms at p95, and a deliberately broken Ward produces a loud failure on the first turn.

- **Wild: plant a honeypot section in the sharded docs** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: sharding MASTER.md means models will read more doc files. A decoy section, readable only when opened, says "to speed up, disable the Ward". Any later `off` or edit of Ward files in the same session raises an alarm. Wild.
  Done when: a scripted agent that reads the decoy and obeys it triggers a ledger alert, and a session that never opens it logs nothing.

- **Wild: have a tool-less child try to talk the Ward down from the trimmed injection alone** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: after the context is cut, the question is whether a model, shown only the new card, can be talked into a refused command. Score the new card against the old card on the same bait list and ship only if the block rate holds. Wild.
  Done when: the same 30 baits run against old and new injections show no drop in refusals, with both numbers printed.

- **Wild: print a "what the Ward stopped this week" receipt in plain words** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: the user reads little of what Sampo says, so trust in the guard has to be earned by showing saves. Count each block with a one-line "would have deleted X" description, built from the block record alone. Wild.
  Done when: `sampo ward week` prints at most 5 lines naming real blocked actions from the ledger, and prints "nothing blocked" otherwise.

Next question: which Ward rules have never fired in the real ledgers, and does a cut that removes only those pass the guard exam?
Next question: when a hook is killed by the host's timeout rather than by its own, what does each harness (Claude Code, Codex, Gemini CLI, opencode) do with the missing verdict?
