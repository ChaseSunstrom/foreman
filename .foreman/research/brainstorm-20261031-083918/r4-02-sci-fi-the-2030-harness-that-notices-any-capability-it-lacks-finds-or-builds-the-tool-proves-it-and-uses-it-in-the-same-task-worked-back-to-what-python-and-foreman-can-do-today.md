# Brainstorm — lens: sci-fi: the 2030 harness that notices any capability it lacks, finds or builds the tool, proves it and uses it in the same task, worked back to what Python and Foreman can do today

- **Match candidates by the miss's input/output example** — FEATURE — value 4 — effort M — risk low — category: search
  Why: `fm plugins find` and `fm lib search` match on text, but a capability miss usually comes with a concrete failing input. Assumption: a miss can carry one example pair.
  Done when: given a miss recorded with an example pair, `fm plugins find --example FILE` ranks a candidate whose `tools/list` schema accepts that input above a text-only match that doesn't, in a test with two fixture servers.

- **Scan found skills and plugins for injection before the grant card** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Why: a found SKILL.md becomes instructions the model follows. T-0791 (injection and supply-chain defenses) is deferred, and the grant card shows only the proof. Assumption: no pre-grant text scan exists.
  Done when: a fixture skill containing zero-width characters, a "ignore previous instructions" line and a hidden HTML comment is flagged on the grant card, and a clean skill is not.

- **Turn a "doc miss" into a version-pinned lib card from the installed package** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: "Getting the tools it lacks" covers commands and modules, but an `AttributeError` or unknown-API failure is the commonest miss that isn't a tool. `fm lib show NAME` cards exist, so a card generated from `pydoc`/`inspect` of the installed version can be local and offline.
  Done when: after an AttributeError on a fixture package, the capability-miss note names `fm lib card --from-installed PKG`, and the card it writes lists the real public signatures of the installed version.

- **Add `fm mcp check NAME`, a protocol conformance gate** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: `fm mcp new` scaffolds a server with `test_server.py`, but nothing checks a found or built server against the handshake itself. Assumption: the scaffold test doesn't cover malformed requests.
  Done when: `fm mcp check` fails a fixture server that returns a bad `initialize` result or non-JSON on stdout, and passes the scaffolded one.

- **Count an acquired tool's call latency on the lean ratchet** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: the ratchet tracks chars and hook p50, and `bench_hooks.py` exists. A built tool wired into a hook or the drive adds time the ratchet never sees.
  Done when: `fm doctor` warns when a hook-called shelf tool's p50 exceeds the recorded value by the ratchet's margin, tested with a deliberately slow fixture tool.

- **Rescan built tools for "build regret"** — FEATURE — value 3 — effort M — risk low — category: tool lifecycle
  Why: the loop prefers found over built, but a plugin published after the build is never noticed. Assumption: `fm plugins find` can be re-run from a stored miss description.
  Done when: a shelf tool built from a miss, plus a new fixture plugin covering the same miss, yields one "consider replacing" line naming both, and nothing is changed without the user.

- **Make the toolsmith lane return a bundle the orchestrator re-verifies** — FEATURE — value 5 — effort M — risk med — category: agents
  Why: standing rules say a model must not grade its own work. A builder that reports "tested" is a writer and judge in one, which answers the earlier question about verbs with a model on both sides.
  Done when: the orchestrator rejects a bundle whose recorded red-first run doesn't reproduce in a fresh worktree, in a test where the receipt was forged.

- **Classify "model too weak" as its own miss kind** — FIX — value 3 — effort S — risk low — category: diagnosis
  Why: with `fm code` on any model, a failure on a small model is often not a missing tool, and building one wastes the loop. The pack's diagnosis list is tool, permission or invocation.
  Done when: a miss that the same task passes on a stronger model in a replay is labelled `model` and routes to the model router, not `fm new tool`.

- **Detect token-heavy mechanical work and propose a script** — PERFORMANCE — value 3 — effort M — risk med — category: cost
  Why: assumption: transcripts show the model hand-computing counts, sorts and diffs in-context. Unlike "mine repeated manual sequences", this needs one occurrence, not a repeat, and the evidence is size.
  Done when: a fixture transcript with a 200-line hand-built table triggers one proposal naming a stdlib script and its token saving.

- **Expose find, build and prove as an MCP server for other hosts** — FEATURE — value 4 — effort M — risk med — category: surfaces
  Why: standing rule: Foreman isn't specific to Claude Code, yet the acquisition verbs are `fm` CLI calls. Codex, Gemini and opencode all speak MCP. Assumption: `fm` has no MCP server of its own.
  Done when: a stdio client lists `find`, `new_tool` and `prove` tools from `fm mcp serve`, and a call to `find` returns the same result as `fm plugins find`.

- **Bisect a failing shelf tool between its versions and the environment** — FIX — value 3 — effort M — risk low — category: reliability
  Why: re-testing on change says a tool broke, not why. Assumption: tool versions and environment fingerprints are both recorded.
  Done when: for a fixture tool broken by a changed dependency, the report names the first bad fingerprint, not just "failed".

- **Wild: Predict each candidate's fit, then score the prediction** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. Mission 8 already predicts and scores minutes and attempts. Reuse it so that before a trial the loop records "p(works) = 0.6" for each candidate and scores it afterwards, so search ranking learns from outcomes.
  Done when: `fm triggers` or the belt page shows a calibration line for find-vs-build predictions after 5 closed misses.

- **Wild: Package tools as cartridges, single-file .pyz with self-test** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: wild. A built tool as a zipapp carrying its test, manifest and hash runs on any host with Python and survives a copy to another repo. It is a natural unit for pinning and trading.
  Done when: `python3 -I tool.pyz --selftest` passes on a clean machine, and editing a byte makes the hash check fail.

- **Wild: Prebuild tools overnight in quarantine from the day's near-misses** — FEATURE — value 4 — effort L — risk med — category: initiative
  Why: wild. Existing ideas wait for a miss or digest it. Here an idle lane builds and proves the likeliest tools from today's workarounds on a quarantine branch. In the morning the user answers one word per card; unanswered ones are discarded.
  Done when: a seeded workaround produces a quarantined, red-first-proven tool and a one-line card, and nothing lands on the main branch without the user's grant.

Next question: Which acquired tools were never invoked after their grant, and what does that say about how well misses are described?
Next question: When a found tool and a built tool disagree on the same input, which does Foreman trust, and does the user ever see the disagreement?
