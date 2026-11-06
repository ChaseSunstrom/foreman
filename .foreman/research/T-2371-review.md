T-2371 review (fm-reviewer, one pass): intent met; every criterion met (shelf tests, tool_search receipt, hook note, no-network test).
Fixed in f3116dd4: rows from a repo's own .mcp.json/tools labelled unreviewed (they were listed as configured); the hook note never names a repo tool; tests use a temp HOME, never the real one; config reads guarded; skipped shelves named in the output.
Left as noted: binaries searched only for one-word needs; project tools only under tools/; fmplugins._json has no FIFO/size guard (shared by other callers).
