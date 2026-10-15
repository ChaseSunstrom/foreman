---
name: pdf-generation
title: PDF Generation
area: domains
tags: [pdf, rendering, html-to-pdf, reportlab, puppeteer, invoices]
detect: [dep:puppeteer, dep:playwright, dep:pdfkit, dep:pdf-lib, dep:@react-pdf/renderer, dep:reportlab, dep:weasyprint, dep:fpdf2, dep:pypdf, dep:wkhtmltopdf, dep:itext7]
related: [unicode, file-uploads, money, timezones]
---
Server-side PDFs from templates: deterministic output, embedded fonts, paged layout and text-based assertions.

## Verify
- `pdfinfo out.pdf`: page count, size, and that the file parses (poppler-utils).
- `pdftotext -layout out.pdf -`: extracted text contains the expected values in order.
- `pdffonts out.pdf`: all fonts show `emb yes`.
- `qpdf --check out.pdf`: structural validity.

## Test first
Generate, then assert on extracted text and page count rather than bytes.
```python
import subprocess
from app.invoices import render_invoice

def test_invoice_pdf(tmp_path):
    out = tmp_path / "inv.pdf"
    out.write_bytes(render_invoice({"number": "INV-7", "total_minor": 123450, "currency": "EUR",
                                     "lines": [{"desc": "Zażółć gęślą", "minor": 123450}]}))
    text = subprocess.run(["pdftotext", "-layout", str(out), "-"], capture_output=True, text=True).stdout
    assert "INV-7" in text and "1.234,50" in text and "Zażółć" in text
    info = subprocess.run(["pdfinfo", str(out)], capture_output=True, text=True).stdout
    assert "Pages:          1" in info
```

## Do
- Pick the tool by need: HTML to PDF (headless Chromium via Playwright or Puppeteer, WeasyPrint) for styled documents; ReportLab, pdfkit or fpdf2 for programmatic control; pypdf or pdf-lib to merge, split and fill.
- Style pages with CSS paged media: `@page { size: A4; margin: 20mm }`, `break-inside: avoid`, `break-before: page`, `thead { display: table-header-group }` for repeating table heads.
- Use `page.pdf({ printBackground: true, preferCSSPageSize: true })` in Playwright and Puppeteer, or backgrounds disappear.
- Embed fonts with full glyph coverage for the data's languages; test non-Latin and RTL text.
- Reuse one browser instance with a pool; render in a queue with a timeout, off the request path for big jobs.
- Wait for fonts and images to load (`document.fonts.ready`, `networkidle`) before printing.
- Pass data through the template engine with autoescaping; for archival use PDF/A where required.
- Set document title and language metadata; tag structure for accessibility when the audience needs it.
- Format dates, money and numbers with the document's locale and zone.

## Avoid
- Rendering user-controlled HTML or URLs in headless Chromium: SSRF and local file reads. Sanitize, block private IP ranges, disable JavaScript for untrusted input.
- wkhtmltopdf for new work: unmaintained, old WebKit. Use Chromium or WeasyPrint.
- Launching a new browser per request: seconds of latency and memory spikes. Pool and reuse contexts.
- Standard 14 PDF fonts with non-Latin text: missing glyphs or squares. Embed a Unicode font.
- Absolute-positioned layout that overflows into page breaks: clipped totals. Use flow layout with page-break rules.
- Byte-comparing PDFs in tests: timestamps and ids vary. Assert on text, page count and a rasterized diff.
- Storing generated PDFs publicly with guessable names: leaks invoices. Private storage with signed URLs.

## Review
- [ ] Output opens in two viewers; fonts embedded; text is extractable.
- [ ] Long content paginates correctly with repeated headers and no split rows.
- [ ] Untrusted input cannot reach the renderer as markup or URLs.
- [ ] Rendering has a timeout, pooling and error handling.
- [ ] Amounts and dates are formatted per the document locale.
