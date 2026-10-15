---
name: spreadsheets
title: Spreadsheet files and grids
area: domains
tags: [xlsx, excel, spreadsheet, formulas, dates, streaming]
detect: [dep:exceljs, dep:openpyxl, dep:xlsx]
related: [csv-import-export, file-uploads, pdf-generation, timezones]
---
Reading and writing .xlsx: cached formula values, date serials, streaming for big sheets, typed cells, and distrust of uploaded workbooks.

## Verify
- `pytest -q tests/test_xlsx.py`: read, write and round-trip tests pass.
- `python -c "import openpyxl; wb=openpyxl.load_workbook('out.xlsx'); print(wb.sheetnames)"`: output opens and lists sheets (openpyxl).
- `unzip -l out.xlsx`: the file is a valid zip with `xl/worksheet` parts; check size for zip-bomb risk on uploads.

## Test first
Formulas have no cached value unless a spreadsheet app saved them; dates are serial numbers.
```python
import datetime as dt
from openpyxl import Workbook, load_workbook
from app.xlsx import read_sheet

def test_reads_values_not_formulas_and_real_dates(tmp_path):
    p = tmp_path / "a.xlsx"
    wb = Workbook(); ws = wb.active
    ws.append(["when", "n"]); ws.append([dt.date(2026, 3, 8), 5])
    ws["C2"] = "=B2*2"
    wb.save(p)
    rows = read_sheet(p)                       # must use data_only and flag missing cache
    assert rows[0]["when"] == dt.date(2026, 3, 8)
    assert rows[0]["n"] == 5
```

## Do
- Load with `data_only=True` (openpyxl) to get cached results; know that files written by code have no cached formula values until opened in Excel.
- Use streaming modes for large files: openpyxl `read_only=True` and `write_only=True`, ExcelJS streaming reader and writer.
- Write real types: dates as date objects with a number format, numbers as numbers, ids as text.
- Convert via the workbook's epoch (1900 or 1904 system); note the 1900 leap-year quirk.
- Set column widths, header style and freeze panes; keep one table per sheet with a header row.
- Cap upload size, sheet count, row and column counts; treat the file as untrusted and reject macros (`.xlsm`).
- Escape text that starts with `=`, `+`, `-` or `@` when it comes from users.
- Offer CSV when interchange is all that is needed.

## Avoid
- Reading formulas as values: you get strings like `=B2*2`. Use cached values or compute in code.
- Floats for money: store integer minor units or Decimal and format on write.
- Assuming the first sheet or header row: locate by name and validate headers.
- Merged cells in data sheets: they break parsing. Keep them for presentation sheets only.
- Reading a 200 MB workbook fully in memory: stream.
- Timezone-naive date-times silently shifted on import: state the timezone.

## Review
- [ ] Formula cache and date handling are tested.
- [ ] Large-file path streams.
- [ ] Upload limits and type checks exist.
- [ ] Types are real, not stringly typed.
- [ ] User text is escaped against formula injection.
