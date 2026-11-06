# Research: What does Python's tomllib module do and since which version?

Asked 2026-10-04 · 1 sub-question(s) · 8 claims: 7 quote found, 1 quote not found, 0 unchecked. ✓ means the quoted words are on the cited page, not that the claim is true.

## Already known (fm recall)
- research t0016-adversary: ":"standard","inference_geo":"not_available"},"input_transformations":[],"diagnostics":null,"context_management":null},"apiBlockIndex":0,"requestId":"req_011CfSLMkpyqvF2RGuJFhSPC","attributionAgent":"foreman:fm-reviewer","attributionPlugin":"foreman","type":"assistant","uuid":"f5898835-8d9e-4b1e-b91e-cc6a94676b15","timestamp":"2026-09-26T16:05:46.920Z","effort":"high","perTurnEffort":null,"userType":"external","entrypoint":"cli","cwd":"~/.claude/foreman","sessionId":"6901a8c8-aa34-4df7-8164-6500197eb1c7","version":"2.1.280","gitBranch":"foreman/build","slug":"starry-petting-quasar"}
- research t0023-grounding: Ledger events (this project, ~700 events): step_done 66, step_add 64, task_set 61, ac_check 58, audit 37, subagent 35,
- T-0170 [FIX M, done, 3 steps] Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them — lesson: Relax a guard by proving the safe case, not by listing the unsafe ones: an allowlist of imports plus a ban on exec-like calls is small enough to reason about; a blocklist of tricks never is.
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and the Python heredocs that only mention `import fmsecrets`/`import fmhooks` as text. The `.env` heredoc is only partly fixable, and the `state-direct` block can't be grounded from the code. The scope-reason refusal at `fmcli.py:240` gives no hint about ordering, and a one-line text change fixes that.

## What does Python's tomllib module do and since which Python version is it in the standard library?
- ✓ tomllib parses TOML 1.0.0 documents. — https://docs.python.org/3/library/tomllib.html "This module provides an interface for parsing TOML 1.0.0" (primary, unknown; quote found)
- ✓ tomllib has been in the standard library since Python 3.11. — https://docs.python.org/3/library/tomllib.html "Added in version 3.11." (primary, unknown; quote found)
- ✓ tomllib.load() reads a TOML file from a binary file object (opened "rb") and returns a dict. — https://docs.python.org/3/library/tomllib.html "The first argument should be a readable and binary file object." (primary, unknown; quote found)
- ✗ tomllib.loads() parses TOML from a str and returns a dict. — https://docs.python.org/3/library/tomllib.html "Load TOML from a str object. Return a dict." (primary, unknown; not found: the quoted words aren't on the page)
- ✓ tomllib is read-only and has no writing support. — https://docs.python.org/3/library/tomllib.html "This module does not support writing TOML." (primary, unknown; quote found)
- ✓ PEP 680 introduced tomllib for Python 3.11, motivated by packaging tools and config reading. — https://peps.python.org/pep-0680/ "core Python packaging tools, and projects that need to read TOML configuration files." (primary, unknown; quote found)
- ✓ The PEP left out writing because of design complexity and because no core developer would maintain it. — https://peps.python.org/pep-0680/ "there are too many degrees of freedom in how to design a write API." (primary, unknown; quote found)

Against:
- ✓ Writing TOML is not covered, and style-preserving edits need a third-party library. The PEP says edits to an existing file are better served by one, so tomllib alone is not enough for round-tripping. — https://peps.python.org/pep-0680/ "are better served by a style preserving library." (primary, unknown; quote found)

Open:
- Which TOML version later Python releases (3.12 to 3.14) support. I only fetched the docs page that says 1.0.0.
- The publication or update dates of the two pages. The fetched content didn't show them.
