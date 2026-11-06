# Brainstorm — lens: sci-fi: the 2030 harness that notices any capability it lacks, finds or builds the tool, proves it and uses it in the same task, worked back to what Python and Foreman can do today

Working backward from a 2030 harness that notices a missing capability, finds or builds the tool, proves it and uses it in the same task. Today's pieces: the capability-miss trigger (T-2270), `fm new tool` (T-2278), `fm plugins find`, `fm lib search`, and the install-grant queue. Nothing yet closes the loop between them.

- **Close the miss-to-use loop in one task** — FEATURE — value 5 — effort L — risk med — category: tools
  Why: the triggers and scaffolds exist separately (T-2270, T-2278). Nothing carries a miss through find, build, test and use inside the task that hit it. A miss currently ends as a note or a separate task.
  Done when: a scripted session that needs a missing CLI ends with the same task closed. Its evidence shows the miss, the tool chosen, the tool's test run and the call that used it.

- **Rank find-before-build with a written reason** — FEATURE — value 4 — effort M — risk low — category: tools
  Why: the request says "finds an existing plugin... or builds one", but no ordering is shown. Assumption: the search should come first, and builds cost more.
  Done when: for each miss, `fm tools why ID` lists the candidates from `fm plugins find` and `fm lib search`, with the pick and the reason. A build is allowed only when it records "no candidate fit: <why>".

- **Queue install grants as a single reviewable card** — FEATURE — value 4 — effort M — risk low — category: grants
  Why: "Install grants are queued for me, never self-granted." A queue of bare commands is hard to approve. Assumption: the user wants to see what each grant is for.
  Done when: each queue item shows the tool, its source, the permissions it asks for, the task that needs it and a diff of what would change. Approving it runs exactly that command and nothing else.

- **Prove a found tool before trusting it** — SECURITY — value 5 — effort M — risk med — category: supply chain
  Why: the standing intent covers injection and supply-chain defences (T-0791 is deferred). A plugin or MCP server found online is untrusted code that runs with the user's grants.
  Done when: before a found tool is queued, a sandboxed probe runs its own smoke test with no network and a throwaway home directory. The queue card shows pass or fail, and a failing tool can't be queued.

- **Test built tools on the miss that caused them** — FEATURE — value 4 — effort M — risk low — category: tests
  Why: `fm new tool` ships a failing-first test, but the test is generic. The real proof is that the tool solves the original miss.
  Done when: the scaffold's first test is seeded from the failing command and its error text, and it goes green only when that case passes.

- **Turn a repeated miss into a shared tool library entry** — FEATURE — value 3 — effort M — risk low — category: reuse
  Why: T-2270 turns a tool missing in 2+ sessions into one task. Assumption: a tool built once should be found by `fm lib search` next time, or the work is repeated.
  Done when: closing a build task adds the tool to the library with its test and the miss signature. A later session that hits that miss finds it in `fm lib search` and builds nothing.

- **Retire tools that go unused** — CLEAN — value 3 — effort S — risk low — category: footprint
  Why: the lean ratchet (Mission 8) warns when the always-on footprint grows. Built skills and tools add to it.
  Done when: `fm doctor` lists built tools with no call in 30 days, and a one-line command removes them and their descriptions.

- **Rehearse a capability gap on every generation** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the standing rule says every capability needs a session path, and exams use scenarios written by a tool-less child. Nothing checks #5 end to end.
  Done when: a child-authored scenario removes one tool from PATH, and the exam scores whether the foreman arm finds or builds a replacement while the plain arm stalls.

- **Wild: Let the harness ask the host what it has first** — FEATURE — value 3 — effort S — risk low — category: discovery
  Why: wild. Assumption: Claude Code and other hosts already expose built-in skills and MCP servers that the miss trigger doesn't check.
  Done when: the miss trigger lists host-provided tools before searching externally, and says "already available: X" when one fits.

- **Wild: Hold a nightly "what I couldn't do" digest** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: wild. The user's steers say to keep going without stopping, so misses should be batched for them to read, not interrupt them.
  Done when: one morning note lists every miss from the last day. Each entry is marked built, found, queued for a grant or still unsolved.

- **Wild: Let a tool grow its own successor** — FEATURE — value 3 — effort L — risk high — category: self-improvement
  Why: wild. The 2030 version notices when a built tool keeps failing in the same way and drafts an improved version.
  Done when: a tool with three recorded failures gets a v2 task. The new version must pass the old tests plus a test from each failure before it replaces v1.

- **Wild: Trade built tools between projects, reviewed by the user** — FEATURE — value 2 — effort L — risk high — category: sharing
  Why: wild. A tool built in one repo could help another, but sharing is an outward-facing action.
  Done when: `fm tools export NAME` writes a signed bundle with its tests and evidence. Importing it goes through the same grant queue as any found tool.

- **Show a miss's cost against the cost of building** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: assumption: the user steers on spend and wants the build-or-skip choice priced.
  Done when: each build task shows the tokens already burned on workarounds for that miss next to the estimated cost of building.

Next question: Which tools have the guard or the sandbox blocked from running even after the user granted them, and does the miss trigger tell those apart from tools that don't exist?
Next question: When a built tool passes its own test but a later session finds it wrong, what record links the tool, the miss and the task that trusted it?
