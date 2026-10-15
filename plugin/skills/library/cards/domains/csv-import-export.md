---
name: csv-import-export
title: CSV import and export
area: domains
tags: [csv, import, export, encoding, validation, injection]
detect: [dep:papaparse, dep:csv-parse]
related: [spreadsheets, file-uploads, unicode, cron-jobs]
---
CSV in and out: encoding and delimiter sniffing, row-level validation reports, streaming, idempotent imports, and formula-injection-safe export.

## Verify
- `pytest -q tests/test_csv.py`: parse, validate and export round-trip tests pass.
- `file -i sample.csv`: reports the charset of a customer file before you assume UTF-8.
- `head -c 3 sample.csv | xxd`: shows a UTF-8 BOM (`efbbbf`) if present.

## Test first
Export must neutralize cells that spreadsheets would execute.
```python
import csv, io
from app.csvio import export_rows

def test_export_escapes_formulas_and_roundtrips_quotes():
    rows = [{"name": '=HYPERLINK("http://x")', "note": 'say "hi",\nbye'}]
    text = export_rows(rows, ["name", "note"])
    back = list(csv.DictReader(io.StringIO(text, newline="")))
    assert back[0]["name"].startswith("'")           # neutralized
    assert back[0]["note"] == 'say "hi",\nbye'       # quoting survives
```

## Do
- Open files in binary or with `newline=""`; decode with `utf-8-sig` first, fall back to a declared or sniffed encoding, and report which.
- Use a real parser (Python `csv`, Papa Parse, csv-parse), never `split(",")`: quoted commas and newlines break it.
- Validate each row against a schema; collect errors with row number, column and message, and return a downloadable error file.
- Import in a transaction per batch, stream large files, and run in a background job with progress.
- Make imports idempotent with a natural key and upsert; offer a dry-run preview.
- Parse dates, numbers and booleans explicitly with a stated format and locale; reject ambiguous dates like 03/04/2026 unless the format is chosen.
- Export with a stable column order, ISO 8601 dates, UTF-8 with BOM only when Excel is the target, and a streamed response.
- Prefix cells beginning with `=`, `+`, `-`, `@`, tab or carriage return with `'` on export.

## Avoid
- Assuming comma and UTF-8: semicolon locales and Windows-1252 garble data. Sniff and let the user pick.
- Reading the whole file into memory: use streaming.
- Failing the entire import on row 40,000 with no detail: give a per-row report.
- Numbers stored as floats then exported (`1e+16`, lost leading zeros on ids/zips): keep identifiers as strings.
- Trusting exported user text: CSV injection. Escape on export.
- Header drift (renamed or reordered columns): map by header name and fail loudly on missing required ones.

## Review
- [ ] Encoding and delimiter handling are tested.
- [ ] Row errors are reported with line numbers.
- [ ] Import is idempotent and batched.
- [ ] Export neutralizes formulas.
- [ ] IDs and leading zeros survive a round trip.
