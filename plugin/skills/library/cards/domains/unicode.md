---
name: unicode
title: Unicode and Text Handling
area: domains
tags: [unicode, utf-8, normalization, encoding, grapheme, collation]
detect: []
related: [i18n, search, forms, file-uploads, web-scraping]
---
Text is bytes plus an encoding: decode at the boundary, normalize, count graphemes not code units, compare safely.

## Verify
- `python -c "import unicodedata as u; print(u.normalize('NFC','é')=='é')"`: NFC composes combining marks (prints True).
- `file -i data.txt`: reported charset of an input file (a hint, not proof).
- `iconv -f utf-8 -t utf-8 data.txt > /dev/null`: fails on invalid UTF-8 byte sequences.
- `node -e "console.log([...new Intl.Segmenter('en',{granularity:'grapheme'}).segment('👨‍👩‍👧')].length)"`: one grapheme where `.length` says 8.

## Test first
Put the awkward strings in a table test.
```python
import pytest
from app.text import slugify, truncate

CASES = ["café", "café", "İstanbul", "👨‍👩‍👧 family", "ﬁle", "Å", "العربية"]

@pytest.mark.parametrize("s", CASES)
def test_truncate_never_splits_a_character(s):
    out = truncate(s, 3)
    assert out.encode("utf-8").decode("utf-8") == out   # valid
    assert out in ("", s) or s.startswith(out.rstrip("…"))

def test_equivalent_forms_compare_equal():
    assert slugify("café") == slugify("café")
```

## Do
- Use UTF-8 everywhere: files, HTTP (`Content-Type: text/html; charset=utf-8`), DB (`utf8mb4` in MySQL), and `<meta charset="utf-8">`.
- Decode bytes to text once at input, work in text, encode once at output; open files with explicit `encoding="utf-8"`.
- Normalize to NFC before storing or comparing identifiers and search keys; use NFKC for loose matching (usernames, search).
- Count and slice by grapheme clusters for user-facing limits (`Intl.Segmenter`, Python `regex` `\X`, Rust `unicode-segmentation`).
- Case-insensitive compare with `casefold()` (Python) or locale-aware `Intl.Collator` with `sensitivity: 'base'`.
- Reject or strip control characters, bidi overrides (U+202E) and zero-width characters in names and URLs when they carry no meaning.
- Check homoglyph risk for identifiers and domains (Cyrillic "а" vs Latin "a").
- Treat database collation as part of the schema.

## Avoid
- `.length` or `len()` as a character count: UTF-16 units and code points differ from what users see. Segment graphemes.
- Truncating by bytes or slicing mid-sequence: produces mojibake or invalid UTF-8. Cut on grapheme boundaries.
- Latin-1 or Windows-1252 assumptions and silent `errors="ignore"`: lose data. Fail loudly or use `errors="replace"` knowingly.
- MySQL `utf8` (3-byte): drops emoji. Use `utf8mb4`.
- Comparing without normalization: visually identical strings differ, enabling duplicate accounts. Normalize first.
- `toLowerCase()` for case-insensitive keys: Turkish and German edge cases. Use casefold or collator.
- Regex `\w` and `[a-z]` assuming ASCII: reject valid names. Use Unicode properties (`\p{L}`).
- Sorting with codepoint order for users: wrong for most languages. Use collation.

## Review
- [ ] Encoding is explicit at every I/O and storage boundary.
- [ ] Stored identifiers are normalized; comparisons use the same form.
- [ ] Limits and truncation operate on graphemes.
- [ ] Emoji, combining marks, RTL and astral characters are in the tests.
- [ ] Database and connection use full UTF-8.
