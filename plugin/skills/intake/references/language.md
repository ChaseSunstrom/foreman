# Intake language (reference)

```
FIX: login times out after 30s on slow networks
FEATURE: export report as CSV @src/reports
CLEAN: collapse the three date helpers into one
PERF: dashboard first paint takes 4s
SECURITY: review the upload endpoint
CONTEXT: Django app; don't touch migrations
DONE-WHEN: all tests pass and the CSV opens in Excel
```

| Tag (case-insensitive) | Aliases | Meaning |
|---|---|---|
| CLEAN | REFACTOR, TIDY | behavior-preserving improvement |
| PERFORMANCE | PERF | measurable speed/resource improvement |
| SECURITY | SEC | vulnerability, hardening, audit |
| FIX | BUG | incorrect behavior → correct behavior |
| FEATURE | FEAT, CAPABILITY, CAP, ADD | new behavior |
| RESEARCH | SPIKE, INVESTIGATE | findings and a recommendation, no product code |
| CONTEXT | NOTE | background for every item in the block |
| CONSTRAINT | MUST, NEVER | hard rules for the block |
| DONE-WHEN | ACCEPT | block-level acceptance criteria |
| SKIP | OUT | explicitly out of scope (becomes Non-goals) |

Modifiers: `TAG!:` urgent (priority urgent; preempts order and the current task) · `TAG?:` exploratory (`explore: true`: brief + options + recommendation; don't implement until confirmed) · `@path` scope hint · `#T-0012` relates to / depends on · indented lines continue the previous item · `NOW:` prefix = handle immediately.

Override words (whole message): `PAUSE`/`stop`/`hold on` (checkpoint, wait; drive pauses), `RESUME`, `STATUS`, "that's for the current task" (the previous message was a steer, not new work).

Untagged requests: classify them yourself and state it in one line ("Treating this as FEATURE, tier M.").

Canonical order: BASELINE → RESEARCH → CLEAN → PERFORMANCE → SECURITY → FIX → FEATURE → FINAL VERIFY → REFLECT.
- BASELINE (automatic): build and tests run, baseline metrics for PERF items, git state. A FIX that blocks the baseline is hoisted here.
- CLEAN first so later work lands in simpler code. Scope: code the listed items touch plus explicit CLEAN items; no drive-by rewrites. Tests pass before and after; add characterization tests first if coverage can't prove behavior is preserved.
- PERFORMANCE: measure before and after with the same method. No measurement, no claim.
- SECURITY: third, but critical findings (exposed secret, auth bypass, RCE, reachable injection) are hoisted immediately.
- FIX after structure settles; each fix gets a regression test that fails before and passes after.
- FEATURE last, on a clean, measured, secure, correct base.
- RESEARCH (Foreman): right after BASELINE, because findings shape the rest.
- Dependencies override order (topological sort; `fm queue` reports cycles and dangling deps). Re-plan between phases (`references/execute.md`).
