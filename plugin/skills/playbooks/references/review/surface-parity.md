<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Surface parity

Use when one product has several surfaces (CLI, plugin commands and skills, a web app, a pane, an API) and a feature, verb, setting or safety check must reach every one of them.

1. **List the surfaces and how each reaches the feature:** the command, route, menu entry or skill that calls it.
2. **One source of truth:** every surface calls the same function and reads the same data; none re-implements it.
3. **A parity test enumerates from the code:** walk the real verbs, routes or settings and fail on any one a surface can't reach, with an explicit, reasoned list of exceptions.
4. **A new feature lands on every surface in the same change**, or the exception list names why it doesn't.
5. **The same safety on each:** checks, confirmation and redaction run in the shared function, so a second surface can't skip them.
6. **The same words, exit codes and JSON keys** on each surface, so a user moving between them isn't surprised.

Mined from T-1520, T-1822, T-1856, T-0442.
