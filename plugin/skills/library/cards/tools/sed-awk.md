---
name: sed-awk
title: sed and awk
area: tools
tags: [sed, awk, text, streams, shell, editing]
detect: [ext:.awk, ext:.sed]
related: [shell-scripting, regex, ripgrep, jq]
---
sed for line edits and awk for field-based filtering, with portable flags and safe in-place editing.

## Verify
- `sed -n 's/old/new/p' file`: preview exactly which lines change, without editing.
- `sed 's/old/new/' file | diff file -`: the full diff of the proposed edit.
- `awk -F, 'NR>1 {print $2}' file.csv`: field extraction behaves on a sample.
- `git diff --stat`: after an in-place edit, only the intended files changed.

## Test first
Practice check: run on a fixture and compare with the expected text.
```sh
printf 'a=1\nb=2\n' > /tmp/in
sed 's/^b=.*/b=9/' /tmp/in > /tmp/out
printf 'a=1\nb=9\n' | diff - /tmp/out
awk -F= '$1=="b"{print $2}' /tmp/in | grep -qx 2
```

## Do
- Preview before editing in place; use `sed -i.bak` where portable, then check and remove the backup.
- Use `-E` for extended regex in sed; use a different delimiter for paths: `s|/usr|/opt|g`.
- Use `-n` with `p` to print only matches; use address ranges `/start/,/end/`.
- In awk set the field separator with `-F` or `BEGIN{FS=","}`; use `-v name=value` to pass variables.
- Use awk for columns, sums and group-by (`{a[$1]+=$2} END{for(k in a) print k,a[k]}`).
- Use `NR==1`, `NF`, `$NF`, `OFS` and `printf` for formatted output.
- Use ripgrep to find the files first, then pass only those to sed.
- Quote the script in single quotes so the shell does not expand it.

## Avoid
- `sed -i` portability: GNU accepts `-i`, BSD/macOS requires `-i ''`. Use `-i.bak` which works on both, or write to a temp file and move it.
- Embedding shell variables in a sed script (`s/$x/y/`): metacharacters and delimiters break it or inject commands. Escape input first, or use awk `-v`.
- Regex with CSV containing quoted commas: awk `-F,` splits wrongly. Use a CSV tool or a real parser.
- GNU-only features (`\+`, `\b`, `-z`, `\n` in replacement) in portable scripts: BSD differs. Test or avoid.
- `sed ... file > file`: truncates the input before reading. Use a temp file.
- Greedy `.*` matching more than intended: use `[^,]*`.
- Editing JSON, YAML or HTML with sed: use jq, yq or a parser.

## Review
- [ ] The previewed diff matches intent before `-i` runs.
- [ ] Variables are passed with `-v` or escaped, not spliced.
- [ ] Flags work on the target platform (GNU versus BSD).
- [ ] Structured formats use proper tools.
