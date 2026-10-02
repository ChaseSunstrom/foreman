<!-- Foreman's own playbook (written for Foreman, not ported). -->
# API design

Use when adding or changing a public interface: a CLI, HTTP/RPC endpoint, library function, config format or file format.

1. **Start from the caller:** write the 3 most common calls as the user would type them before writing any code.
2. **Names and shapes:** one obvious way per task; consistent verbs/nouns with what exists; required inputs positional or explicit, options named; defaults safe.
3. **Errors are part of the API:** say what failed and what to do next; distinct exit codes or error types for distinct failures; never succeed silently on bad input.
4. **Machine-readable twin:** anything a human reads, a program can get as JSON (`--json`), with a stable, versioned shape and a test pinning it.
5. **Compatibility:** additive changes only, unless the user approved a break; deprecate with a warning and a migration note first.
6. **Document as you ship:** the help text, README and changelog change in the same task; one runnable example each.
