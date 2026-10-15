---
name: regex
title: Regular expressions
area: tools
tags: [regex, patterns, parsing, validation, redos, unicode]
detect: []
related: [ripgrep, sed-awk, shell-scripting, jq]
---
Regular expressions: precise, anchored, tested patterns that avoid catastrophic backtracking.

## Verify
- `rg -n -P 'PATTERN' path/`: the pattern matches exactly the intended lines in real files (`-P` for PCRE2 features).
- `printf '%s\n' input | grep -E '^PATTERN$'`: an anchored full-match check with ERE.
- `python -c "import re; print(re.fullmatch(r'PATTERN', 'text'))"`: a fullmatch result on a sample.
- Run the pattern against a long non-matching input and time it: it must return fast (ReDoS check).

## Test first
Table-driven cases: matching and non-matching samples, including edges.
```python
import re
P = re.compile(r"[A-Z]{2}\d{4}")
good = ["AB1234"]
bad = ["AB123", "ab1234", "AB12345", " AB1234", "AB1234\n"]
def test_pattern():
    assert all(P.fullmatch(s) for s in good)
    assert not any(P.fullmatch(s) for s in bad)
```

## Do
- Anchor: use fullmatch or `^...$`; in Python prefer `re.fullmatch`, in JS `^...$` with no `g` flag for tests.
- Use raw strings (`r"..."`, JS literals) so backslashes survive.
- Name captures: `(?P<year>\d{4})` in Python, `(?<year>\d{4})` in JS, PCRE and .NET.
- Make quantifiers lazy (`.*?`) or use negated classes (`[^"]*`) over `.*`.
- Escape user text with `re.escape` or a library function before embedding in a pattern.
- Use `(?x)` verbose mode for long patterns, and comment them.
- Compile once and reuse; keep a test table beside the pattern.
- Set a timeout or use a linear-time engine (RE2, Rust `regex`) for untrusted input.

## Avoid
- Nested quantifiers like `(a+)+` or `(.*)*` on untrusted input: exponential backtracking (ReDoS). Rewrite without ambiguity or use RE2.
- `$` that matches before a trailing newline (Python, Perl): `"AB1234\n"` passes. Use `\Z` or fullmatch.
- Parsing HTML, nested JSON or balanced parentheses with regex: use a real parser.
- Email or URL validation with a giant pattern: use a library, or just check for `@` and send a confirmation.
- `\d` and `\w` assuming ASCII: Unicode digits and letters match in many engines. Use `[0-9]` or an ASCII flag if required.
- Unescaped dots (`1.2` matches `1x2`): escape as `\.`.
- Forgetting flavor differences: lookbehind, possessive quantifiers and `\h` are not in every engine, and POSIX ERE has no `\d` or lazy quantifiers.

## Review
- [ ] Pattern is anchored or its partial-match intent is explicit.
- [ ] Tests include empty, near-miss, trailing newline and Unicode cases.
- [ ] No nested ambiguous quantifiers on untrusted input.
- [ ] Interpolated text is escaped.
