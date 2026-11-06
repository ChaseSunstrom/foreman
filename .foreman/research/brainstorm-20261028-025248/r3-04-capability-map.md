# Brainstorm — lens: capability map

- **Rebase a finished lane onto moved main and re-prove it** — FEATURE — value 4 — effort M — risk med — category: git flow
  Why: assumption: a lane proves its change against the base it started on, and nothing re-proves it when main moves underneath. The pack's proof-binding idea covers the diff, not the base.
  Done when: a lane whose base moved is rebased, `fm check` reruns on the new tree, and close refuses while the proof's tree hash differs from HEAD's.

- **Ship risky changes behind a flag and file the flag's removal as a task** — FEATURE — value 3 — effort M — risk low — category: release safety
  Why: assumption: flags get added and never removed. The pack's feature-expiry idea covers features, not flags.
  Done when: a task that adds a flag files a follow-up with a removal date, and `fm doctor` lists any flag past its date.

- **Emit a CycloneDX SBOM with every release** — SECURITY — value 3 — effort M — risk low — category: supply chain
  Why: the pack ships a provenance attestation for site deploys only. Assumption: plugin releases have no bill of materials.
  Done when: a release build writes an SBOM listing every bundled file hash and dependency, and it passes the CycloneDX schema check.

- **Gate container builds and fail on critical image CVEs** — SECURITY — value 2 — effort M — risk med — category: containers
  Why: assumption: a repo with a Dockerfile gets no build or scan step from Foreman.
  Done when: a Dockerfile change fails the gate if the image build fails or the scanner reports a critical CVE in the built image.

- **Open a task from a production alert, with a failing reproducer first** — FEATURE — value 4 — effort M — risk med — category: incidents
  Why: the pack turns pasted CI failures and GitHub issues into tasks, but no error-tracker alert can enter the queue.
  Done when: a stored alert payload becomes a task whose first step is a test that fails on the unfixed code and passes after the fix.

- **Ratchet test coverage on changed lines only** — FEATURE — value 3 — effort S — risk low — category: testing
  Why: the pack shows which changed lines a proof executes but does not fail a diff that adds uncovered lines.
  Done when: a diff adding untested lines fails the check, and the same diff with a covering test passes.

- **Give each web-facing lane a preview URL in its receipt** — FEATURE — value 3 — effort L — risk med — category: review
  Why: assumption: web lanes are reviewed from diffs and screenshots of the local build only. A live branch preview would let the user click through the change.
  Done when: a lane touching a web surface gets a preview URL in its receipt that serves that branch's build.

- **Review infrastructure plans before apply** — FEATURE — value 3 — effort M — risk high — category: infra
  Why: assumption: Terraform or Pulumi edits go through the gate with no plan review. A destroy can be missed in a diff.
  Done when: an infra diff prints add, change and destroy counts on the receipt, and apply refuses any destroy without an explicit flag.

- **Fix a known advisory on a locked dependency as its own lane** — SECURITY — value 4 — effort M — risk med — category: dependencies
  Why: the pack checks new dependencies for advisories at close. Assumption: an advisory on a dependency already in the lockfile has no path into the queue.
  Done when: an advisory files one lane whose first step is a test that reproduces the vulnerable call, and the lane closes only when that test fails before the bump and passes after.

- **Gate mobile screens on approved emulator screenshots** — FEATURE — value 2 — effort M — risk low — category: mobile
  Why: assumption: the pack's screenshot gate covers the web UI only, and no mobile project is covered.
  Done when: a change that alters a screen fails when the emulator capture differs from the approved image, and passes once the approval is recorded.

- **Run axe on every changed page before close** — FIX — value 3 — effort S — risk low — category: accessibility
  Why: the pack has keyboard and screen-reader ideas for the pane but no automated audit of the web UI's changed pages (assumption).
  Done when: a change to a page with an axe violation fails the check and names the rule and element.

- **Wild: a rival lane that pins the worst transitive version and checks whether the suite notices** — PERFORMANCE — value 3 — effort M — risk low — category: testing
  Why: (wild) the suite is trusted because it passes today. A lane that deliberately picks the oldest compatible transitive versions tests whether the suite would catch a bad upgrade.
  Done when: a seeded bad transitive version turns the gate red, and a clean one stays green.

- **Wild: a shadow release a stranger can try from a link and report back on** — FEATURE — value 2 — effort L — risk high — category: community
  Why: (wild) the pack's testing is all internal. A time-limited public build, with a feedback form that files tasks, would test the product on people who never saw its receipts.
  Done when: a link serves a build that expires, and a submitted report becomes a task with the build hash attached.

- **Wild: a dependency pet that files its own patch lane when its package goes unmaintained** — SECURITY — value 2 — effort S — risk low — category: dependencies
  Why: (wild) each locked dependency gets a visible status that worsens as its last release ages, and at a threshold it files a lane to evaluate a replacement.
  Done when: a dependency with no release in a set window shows the worse status on `fm status` and files one replacement-evaluation task.
