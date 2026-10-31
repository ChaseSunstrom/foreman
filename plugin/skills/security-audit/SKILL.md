---
name: security-audit
description: Use whenever code takes user input, secrets, auth or an API route, or needs a security review: threat-check it.
---

# Foreman: security review

Security work is a SECURITY task: no brief yet → `/foreman:intake` first. Findings are proved before they are fixed, and a fix starts with a failing test that exploits the hole.

1. **Scan first.** `fm secrets` finds credentials in the tree and config (git history with `--history`); a hit is rotated by its owner, not just deleted. `fm deps` shows outdated or risky dependencies.
2. **Walk the checklist** in `../playbooks/references/security/security-review.md` for what the change touches: input validation, authentication and authorization, secrets, injection, output encoding, rate limits, error messages. Cloud or CI configuration → `../playbooks/references/security/cloud-infrastructure.md`.
3. **Trace each entry point:** `fm graph blast PATH` for what reaches the code, `fm sym PATH:NAME` for its callers. Mark which inputs an outsider controls.
4. **Hunting for holes** in a whole repo: `fm find --rank` lists leads, `fm prove` each one red before fixing it; `../playbooks/references/security/bounty-triage.md` (remotely reachable first). A guard or policy hook that blocks or allows wrongly → `../playbooks/references/security/command-guard.md`.
5. **Fix test-first.** The test sends the hostile input and fails; the fix turns it green: `fm task evidence ID --step N --run "<that test>"`.
6. **Report each finding** with severity, the path it takes, and what you proved. One you can't prove is a question, not a finding. Close with `fm audit prep ID` for one `foreman:fm-reviewer` pass.

Never put a real secret into a test, a log or a brief; use a synthetic value of the same shape. Proofs are local tests only: no live systems, no running untrusted code. Never loosen or edit the guard to make a check pass; a rule change goes through `fm ask ID core`.
