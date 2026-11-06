Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-early.diff. Verdict: approve with nits.
1. MEDIUM docs gate (fmcore docs_gap) only requires non-empty "Docs impact" text; "none: …" passes; nothing checks named docs were touched or drift-free. Fix: check named docs exist/changed/drift-free; report project drift at done.
2. LOW fm docs / doctor self-docs are detection-only; tidy reports drift as warn; nothing surfaces drift periodically. README "Docs stay current" overstates.
3. LOW "Next: …" injections are advisory; CHANGELOG "injected every turn" framing overstates enforcement. Enforced for real: no-task edit gate, focus plan gate, done blockers, autocompact override.
