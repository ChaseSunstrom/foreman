---
name: redos
title: Regex denial of service
area: security
tags: [security, regex, redos, dos, performance, validation]
detect: [dep:google-re2, dep:re2]
related: [input-validation, rate-limiting, owasp-top-10]
---
Avoid catastrophic backtracking: linear-time regex engines, bounded input length, and timing tests for every pattern on user input.

## Verify
- `git grep -nE "re\.(compile|match|search|fullmatch)|new RegExp|Pattern\.compile" -- ':!*test*'`: all patterns found, then check which see user input.
- `pytest -q -k redos`: the time-bound tests pass.
- `semgrep --config auto .`: flags known unsafe regex shapes where its rules cover them.

## Test first
Fail when a hostile string takes more than a small time budget.
```python
import re, time

def test_email_pattern_is_linear_on_hostile_input():
    s = "a" * 50_000 + "!"
    t = time.perf_counter()
    validate_email(s)
    assert time.perf_counter() - t < 0.2

def test_input_length_is_capped_before_matching():
    assert validate_email("a" * 10_000 + "@x.io") is False
```

## Do
- Cap input length before any regex runs (for example 254 for email, 2048 for URLs).
- Use a linear-time engine for untrusted input: RE2 bindings, Go `regexp`, Rust `regex`.
- In backtracking engines, avoid nested quantifiers `(a+)+`, overlapping alternations `(a|a)*` and `.*` followed by more `.*`.
- Anchor patterns and use possessive quantifiers or atomic groups where the engine supports them.
- Prefer a parser or stdlib validator (URL, email, IP, date) over a hand-written regex.
- Add a timeout where available (for .NET, a `matchTimeout`), and run heavy matching off the request thread.
- Test each user-facing pattern with long near-miss strings: a long run of the repeated class, then one mismatching character.

## Avoid
- Copy-pasted "perfect email" or URL regexes: they often backtrack. Use a validator library and a length cap.
- Running a regex on a whole request body to find a field: parse structure first, match the small field.
- Trusting that the input is short because the UI limits it: enforce at the server.
- Building patterns from user input with no escaping: use `re.escape` or run a literal search.
- Assuming JS `RegExp` has a timeout: it does not. Use RE2 bindings or a manual guard and size limit.
- Fixing by raising server timeouts: the CPU is still burned. Fix the pattern.

## Review
- [ ] Every regex on untrusted data has an input length cap.
- [ ] No nested quantifiers or overlapping alternation remains.
- [ ] A timing test with near-miss input exists per pattern.
- [ ] User-supplied patterns are escaped or run in a linear engine.
- [ ] Validators from libraries replace bespoke ones where possible.
