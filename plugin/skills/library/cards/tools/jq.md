---
name: jq
title: jq
area: tools
tags: [jq, json, cli, filters, scripting, data]
detect: [file:*.jq]
related: [shell-scripting, sed-awk, ripgrep, github-cli]
---
jq: filter and reshape JSON on the command line, with correct quoting, null handling and exit codes.

## Verify
- `jq empty file.json`: the file is valid JSON (exit 0 when it parses).
- `jq -e '.ok == true' resp.json`: exit status reflects the result (non-zero for false or null).
- `jq -n --arg v "$X" '{value: $v}'`: strings are passed as variables, not spliced into the filter.
- `jq -S . a.json | diff - <(jq -S . b.json)`: key-order-independent comparison.

## Test first
Assert on a fixture. A filter that returns nothing or null should fail the script.
```sh
echo '{"items":[{"id":1,"tags":["a"]},{"id":2}]}' > /tmp/in.json
out=$(jq -r '[.items[] | select(.tags) | .id] | @csv' /tmp/in.json)
test "$out" = "1"
jq -e '.items | length == 2' /tmp/in.json
```

## Do
- Use `-r` for raw strings, `-c` for one-line output, `-e` for exit codes, `-n` with no input.
- Pass values with `--arg name value` (string), `--argjson name JSON`, `--slurpfile` or `--rawfile`.
- Use `.[]?` and `//` to default missing or null values: `.name // "none"`.
- Use `select`, `map`, `group_by`, `unique_by`, `to_entries` and `from_entries` for reshaping.
- Use `@csv`, `@tsv`, `@sh`, `@uri` and `@base64` for safe formatting.
- Use `-s` (slurp) to read many documents into one array; for big files use `--stream` or `limit`.
- Use `jq -r '.[] | [.a,.b] | @tsv'` for shell-friendly rows; iterate with `read` in a loop.
- Build JSON with jq, never with string concatenation.

## Avoid
- Interpolating shell variables into the filter (`jq ".x == \"$v\""`): injection and quoting bugs. Use `--arg`.
- Treating `-r` output as safe for shell: use `@sh` when feeding into `eval` or command words.
- Assuming a missing key errors: it yields `null`, which prints as "null". Use `-e` or `// empty` deliberately.
- Large integers (above 2^53) and precise decimals: jq numbers are IEEE doubles in many builds, so IDs can be rounded. Keep them as strings if the source quotes them.
- `jq . file > file`: truncates the input first. Write to a temp file and move it.
- `.[]` on an object or null without `?`: runtime error "Cannot iterate". Use `.[]?`.
- Parsing JSON with grep or sed.

## Review
- [ ] Inputs reach filters through `--arg`/`--argjson`.
- [ ] Missing keys and null are handled on purpose.
- [ ] Exit status is used (`-e`) where the script branches on a result.
- [ ] No in-place redirect onto the input.
