<!-- Foreman's own playbook (written for Foreman, not ported). -->
# CLI errors and argument shape

Use when a command-line tool crashes with a traceback, rejects a natural argument shape, prints a wall of choices, acts on more than was named, or exits 0 on a failure.

1. **Reproduce with the exact argv**, from a shell, and note the exit code and both streams.
2. **Test through the entry point:** run the real binary in the test and assert the exit code, one line on stderr naming the problem and the fix, and no `Traceback`.
3. **Wrong input is a usage error, not a crash:** a missing file, a bad id, an unknown flag or verb exits with the tool's one usage code and one line. Catch at the boundary, not in every caller.
4. **Accept the shapes people type:** case, a short id (`t-5` for `T-0005`), an option before or after the positional, a range or list where many make sense. An unknown word gets a short "did you mean" from the closest names, never the full list.
5. **Act on exactly what was named:** a filter or an id narrows; output lists only what this call changed. Anything wider is a separate verb or flag.
6. **Many at once:** handle each item as if named alone, cap the count, say each failure by name, keep going, and exit non-zero when any failed.
7. **Keep `--json` in step:** the same fields as the text, errors included, and nothing else on stdout.

Mined from T-1225, T-1416, T-1877.
