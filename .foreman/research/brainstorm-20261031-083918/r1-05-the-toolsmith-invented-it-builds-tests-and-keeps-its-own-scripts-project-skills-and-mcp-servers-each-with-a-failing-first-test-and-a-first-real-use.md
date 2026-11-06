# Brainstorm — lens: the toolsmith (invented): it builds, tests and keeps its own scripts, project skills and MCP servers, each with a failing-first test and a first real use

- **Prove a built tool on a real miss before it counts** — FEATURE — value 5 — effort M — risk low — category: build-test-use
  Why: the request says "tests it, and uses it"; T-2278 scaffolds the tool and its failing-first test, but nothing shows a tool is retired from "new" until it has served the very miss that triggered it. Assumption: the miss record from T-2270 keeps the failing command.
  Done when: `fm new tool X` leaves a tool marked `unproven`, and it flips to `proven` only after `fm tool use X` reruns the original missed command and exits 0; `fm doctor` lists any unproven tool older than a day.

- **Search before build, and record why the find was rejected** — FEATURE — value 5 — effort M — risk low — category: find-or-build
  Why: the request orders find (`fm plugins find`, `fm lib search`) before build. Assumption: nothing enforces that order. A build task for a miss should carry the find's result (or "none") before `fm new tool` is allowed.
  Done when: `fm new tool X` refuses unless a find record for the same miss exists, and the record names each candidate and the reason it was rejected (fit, licence, maintenance, size).

- **Queue install grants as one reviewable card** — FEATURE — value 5 — effort M — risk med — category: grant queue
  Why: "install grants are queued for me, never self-granted". Several misses in one run could produce a pile of prompts. Assumption: the queue is per task today.
  Done when: `fm grants` lists pending installs with source, pinned version, hash, permissions the tool asks for, and the miss that wanted it; approving one spends a single-use grant, and an agent run of the approve verb is refused by the guard.

- **Pin and hash every adopted tool, and re-check on use** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Why: T-0791 (injection and supply-chain defenses) is still deferred, and this mission adds installs of third-party plugins and MCP servers. Assumption: no lockfile exists for tools.
  Done when: an installed or built tool has a lock entry (source, version, content hash); a changed hash blocks its use until the user re-approves; a test edits an installed file and sees the block.

- **Run built MCP servers and scripts in a sandbox with declared permissions** — SECURITY — value 4 — effort L — risk med — category: sandbox
  Why: a self-built tool runs code nobody reviewed line by line. Assumption: `fm mcp new` templates declare no permissions. A manifest listing network hosts, writable paths and env vars would be enforced at run time.
  Done when: a test tool that writes outside its declared path or opens an undeclared host fails with a named violation, and its manifest shows in the grant card.

- **Keep a tool shelf with usage and rot tracking** — FEATURE — value 4 — effort M — risk low — category: tool library
  Why: built tools sit in project skills and scripts, but nothing shows which ones were used again. Assumption: no use counts. Tools unused for 30 days are listed for retirement; tools whose test fails after a toolchain change are flagged.
  Done when: `fm tools` prints each tool with last use, use count, last test result; a stale or red one appears in `fm doctor`.

- **Promote a project tool to a shared one when a second repo misses the same thing** — FEATURE — value 3 — effort M — risk med — category: reuse
  Why: T-2270 counts a tool missing in 2+ sessions, but only within a project. Assumption: miss records are per project. A global miss index would offer an already-built tool from another repo, still behind the grant queue.
  Done when: a miss in repo B that matches a tool built in repo A names that tool and the copy command; copying runs its test in B first.

- **Check a built tool against the miss with a held-out case** — FEATURE — value 4 — effort M — risk low — category: test quality
  Why: the standing rule says to use signals Foreman didn't author, and a failing-first test written by the same model that wrote the tool can encode its own misreading. Assumption: the builder writes both.
  Done when: a second cold child, shown only the miss description, writes one extra case; the tool must pass it, and a tool that passes its own test but fails the extra case is reported as such.

- **Diagnose a miss as a missing tool, a missing permission, or a wrong invocation** — FIX — value 4 — effort S — risk low — category: miss triage
  Why: assumption: many "command not found" or permission-denied events are a PATH, a venv or a deny rule, and building a tool for them is waste. The trigger should classify before it proposes a build.
  Done when: a fixture miss caused by an unactivated venv gets the activation hint and no build task; a true absence gets the find-or-build note.

- **Wild: Let the toolsmith forge a tool from a recorded shell session** — FEATURE — value 3 — effort L — risk med — category: synthesis
  Why: wild. When the user or agent repeats the same 4-6 command sequence three times, Foreman offers to fold it into a script with arguments, writes the failing-first test from the recorded input and output, and shelves it.
  Done when: replaying a recorded fixture session yields a script whose test passes, and the original sequence is shown beside it for review.

- **Wild: Publish a tool's "birth certificate" with its first use** — FEATURE — value 3 — effort S — risk low — category: provenance
  Why: wild. Each built tool carries one page: the miss that caused it, the options weighed, the red-then-green test run, the first real use, and who granted it. It appears in the genesis site and the finish receipt.
  Done when: `fm tool show X` prints the certificate with all five parts, and a tool missing any part is labelled incomplete.

- **Wild: Hold a tool fire drill where a shelf tool is deliberately broken** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: wild. Once a week the toolsmith breaks a copy of one shelf tool (a renamed dependency, a changed API) and checks that the rot detector, the test and the repair path catch it and name the fix.
  Done when: the drill's broken copy fails the shelf check with a named cause, and a drill that goes unnoticed is filed as a FIX task.

- **Wild: Let a tool negotiate its own retirement** — CLEAN — value 2 — effort S — risk low — category: lifecycle
  Why: wild. When a find later turns up a maintained plugin that covers a built tool, Foreman proposes swapping, runs the old test against the new one, and files the diff, so the shelf shrinks rather than only grows.
  Done when: a fixture where a plugin passes a built tool's test produces a swap proposal; the swap needs user approval.

Next question: Which of the user's own recurring manual commands or scripts (shell history, Makefile targets) are tool candidates that no capability miss ever triggered?
Next question: When a built tool is wrong but its test passes, who or what finds out, and how long does it take?
