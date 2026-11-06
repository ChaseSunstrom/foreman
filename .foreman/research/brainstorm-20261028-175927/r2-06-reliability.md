# Brainstorm — lens: reliability

- **Make every import and convert verb balance its books** — FEATURE — value 5 — effort M — risk low — category: correctness
  Why: round 5 review found "silent drops" and "hidden objects drawn" in the Figma/DTCG import and the xray/md outputs. Each was fixed individually, but the class is open.
  Done when: each verb that reads one format and writes another prints `N in, M out, K skipped (reasons)`, and a test fails if N ≠ M + K on any fixture.

- **Fuzz every file-reading verb with malformed content and treat a traceback as a failure** — FEATURE — value 5 — effort M — risk low — category: robustness
  Why: the review listed "TypeError tracebacks" in the new design and scene verbs. The existing fuzz idea covers option-shaped paths, not hostile file contents.
  Done when: a seeded corpus (truncated, wrong-type, deeply nested, huge-number JSON, plus a binary blob) runs through every verb that takes a file. Each case exits non-zero with one sentence and no `Traceback`.

- **Run every mutating verb twice and assert the second run is a no-op** — CLEAN — value 4 — effort M — risk low — category: idempotence
  Why: the review found that a Jira or Linear edit makes a second brief instead of updating the first, and `fm task new --from` had a re-plan bug. Repeat-run behaviour is a recurring defect.
  Done when: a fixture harness runs each verb in a registry twice, and fails if the second run changes any state file hash or output beyond a "nothing to do" line.

- **Give served pages a lifecycle: idle timeout, orphan reaping and a port-in-use fallback** — FIX — value 4 — effort S — risk low — category: served pages
  Why: `settings serve` and `swipe --serve` use a one-shot token and stop only on Ctrl-C. A killed terminal likely leaves a listener behind (assumption).
  Done when: `kill -9` on the parent leaves no listening port within 30 s, a busy default port picks another and prints it, and 10 minutes idle exits cleanly.

- **Check Host and Origin on every served-page request** — SECURITY — value 4 — effort S — risk low — category: served pages
  Why: the swipe page accepts POSTed verdicts that rewrite the backlog behind a bearer token on loopback. Without a Host check, DNS rebinding and cross-site POSTs are plausible (assumption).
  Done when: a request with `Host: evil.test` or a foreign `Origin` returns 403, and the same request with the right headers still works.

- **Give the swipe page a local outbox so a dead server never eats verdicts** — FEATURE — value 4 — effort M — risk low — category: served pages — wild
  Why: assumption: if the server dies or the token expires, a click fails silently and the user thinks the verdict was saved.
  Done when: killing the server mid-session turns the page into a visible "session ended" banner. Unsaved verdicts stay in localStorage and download as a file that `fm inbox swipe --import` replays.

- **Put registry entries in per-feature fragment files, merged at build** — CLEAN — value 4 — effort M — risk med — category: parallel lanes
  Why: three builder lanes ran at once (T-1830 to T-1832). The recent history includes a help-position collision (`fm dojo` at 306) and PLUGIN_ROUTES/APP_ONLY edits, all central tables every new verb touches.
  Done when: two lanes that each add a verb touch no common file, merge without conflict, and `test_help` and the parity test pass on the merged result.

- **Allocate task ids atomically under concurrent creation** — FIX — value 3 — effort S — risk low — category: concurrency
  Why: parallel lanes create tasks (T-1830 to T-1834 were launched together). The id counter's safety isn't shown in the pack (assumption).
  Done when: 20 parallel `fm task new` calls yield 20 distinct ids and no corrupt backlog line.

- **Test each learned known-fix against a negative corpus before it's saved** — FEATURE — value 4 — effort M — risk low — category: known fixes
  Why: T-1865 stopped a learned signature matching an unrelated failure, but only for the cases found by hand.
  Done when: saving a signature replays it over the last N distinct stored failures from other tasks, and refuses it if it matches any of them. The refusal names the colliding failure.

- **Replay each closing lane's diff in a clean checkout** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: the work runs in parallel lanes and worktrees. A change can pass only because of an untracked file or a leftover in the lane. Pillar 5 asks for real-path verification.
  Done when: close applies the committed diff to a fresh checkout and runs the task's verify command there. A test that only passes with an untracked file fails the close.

- **Check every co-released version string agrees in `fm release-check`** — CLEAN — value 3 — effort S — risk low — category: release
  Why: the review fix "foreman-design version follows foreman in fm release" shows the drift was real. Plugin manifests, foreman-design, the site and the changelog can still diverge.
  Done when: a release-check step reads every version field from one list and fails naming the first mismatch.

- **Stamp each verb and surface with the date it was last verified on its real path** — FEATURE — value 4 — effort M — risk low — category: verification — wild
  Why: pillar 5 wants verification on the real browser, device or car, but the pack gives no record of when each was last seen working. CI has browser tests off.
  Done when: `fm verified` lists each surface with a last-verified commit and date. Session start flags any surface whose code changed since its stamp, with the command that renews it.

- **Verify served pages in two tiers: a stdlib structural check always, a real browser nightly** — PERFORMANCE — value 4 — effort M — risk low — category: CI
  Why: CI turns browser tests off because the runner's chromium crashes under load, which leaves served pages (settings, swipe, app view) with thin coverage on every push.
  Done when: every push parses each served page, checks that its endpoints exist and its token flow works, and fails on a missing element id. A nightly serial job runs the real-browser flow and posts its result to the session-start line.

- **Add a nightly crasher farm that grows the fuzz corpus and minimises each crasher** — FEATURE — value 3 — effort L — risk med — category: robustness — wild
  Why: assumption: hand-written hostile inputs only find what someone thought of, and the importers have just grown several formats (Figma, DTCG, scenes).
  Done when: the nightly job mutates stored fixtures, shrinks any input that gives a traceback or a hang to a minimal case, and files it as a task with the exact repro command.

- **Record API payloads for ticket fetch and detect schema drift** — FEATURE — value 3 — effort M — risk low — category: integrations
  Why: T-1859 fetches Jira and Linear, and GitHub issues are a likely next source. Those APIs change shape, and offline or rate-limited failure paths aren't shown to be tested.
  Done when: recorded fixtures drive the tests with no network. A `--probe` run compares live field names to the fixtures and names any drift. A 429 or offline error exits with one sentence and leaves no half-written brief.
