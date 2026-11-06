Verdict: changes needed (1 HIGH, 5 MEDIUM, 3 LOW); fixed or accepted with reason. Reviewer: one foreman:fm-reviewer, six lenses, read-only.

## lens: intent
- HIGH — exists had no defect and no duplicate check: an answer adding a copy of clamp while saying "clamp already exists" closed; "exist" also matched "does not exist"; the name had no word boundary. FIXED: `broken` when the answer's app defines more functions than the clean one (DEFS per language); readings `\bname\b` and `already|reuse`; the template gets an example the oracle says. Test: a copy plus the right words doesn't close; the words alone do.
- MEDIUM — parts measures several fixes in one request, not delegation or model choice. FIXED (said): PROXY puts on #9's row that it is a proxy and the long-horizon tier decides; the exam's session arm has no transcript of delegation to grade.
- MEDIUM — a trigger finding had to name nightly.yml and 'schedule'; any finding on exists was a false alarm. FIXED: a trigger finding may name any file (and cron/nightly/trigger/timer); exists counts no false alarms (nothing keyed).

## lens: adversary
- MEDIUM — TRIGGER ran over all files, so a README line or a comment met it. FIXED: only TRIGGER_FILES (CI workflows, timer/service units, crontabs) are read, and the check needs a schedule plus a test command. Test: a README schedule doesn't count.

## lens: edge
- MEDIUM — files 'any' read .venv/__pycache__, followed links (a FIFO could hang). FIXED: 'any' is gone (TRIGGER_FILES), links and non-regular files are skipped, .venv/venv/__pycache__ pruned.
- LOW — nothing checks a child exists request matches its function. Accepted (the example and readings tie the answer to the function).

## lens: operator
- LOW — default gen renders 18 kinds (+~20%). FIXED (said in the CHANGELOG).

## lens: maintainer
- MEDIUM — unanchored KIND_WORDS would map 'hybrid approach', DB triggers, Kubernetes orchestration; #13 matched 'approach'. FIXED: `\bexhaustive|use what exists`, `\bsubagents?\b`, `self-trigger|event triggers|\bwatchers?\b`; tested against gen-0's own lines and three user-style lines.
- LOW — duplicated ASKS + (...) and missing tests. Tests FIXED (copy, README trigger, real gen-0 text, proxy row); the tuple stays inline twice (two different sets: one with parts, one without).

Noticed: `_matches` couples basename and symbol (wildcard added for trigger only); `fm genesis spec` no longer gives #13 an exists row (anchored words).
