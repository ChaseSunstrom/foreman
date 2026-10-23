"""fm check office FILE (T-1406): a stdlib asserter for .xlsx and .docx deliverables, usable as a verify command.

xlsx: no error cells (#REF!, #DIV/0!, #N/A, …), `--sheets N`, `--cell 'Sheet1!B7=42'` (repeatable; a number compares
as a number). docx: no broken-field text ("Error! Reference source not found."), `--contains TEXT` (repeatable).
Exit 0 when every check holds, 1 when one fails, 2 when the file can't be read. zipfile and expat only; a member over
MEMBER_MAX unpacked is refused before it's parsed, and one declaring a DTD as the parse meets it.
ponytail: cached values only (a formula is never recalculated); .xls, .ods and .doc are refused.
"""
import os
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from xml.parsers import expat

MEMBER_MAX = 64 << 20
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WORD_ERRORS = ("Error! Reference source not found.", "Error! Bookmark not defined.", "Error! No text of specified style",
               "Error! Unknown switch argument.", "Error! Not a valid")
CELL = re.compile(r"^(?:'((?:[^']|'')+)'|([^!]+))!\$?([A-Za-z]{1,3})\$?(\d+)=(.*)$", re.S)


class OfficeError(Exception):
    pass


def _xml(z, name):
    """A member parsed, or None when absent; over MEMBER_MAX or with a DTD it's refused."""
    try:
        info = z.getinfo(name)
    except KeyError:
        return None
    if info.file_size > MEMBER_MAX:
        raise OfficeError(f"{name} unpacks to {info.file_size} bytes, over {MEMBER_MAX}")
    with z.open(info) as f:
        data = f.read(MEMBER_MAX + 1)
    if len(data) > MEMBER_MAX:
        raise OfficeError(f"{name} unpacks to over {MEMBER_MAX} bytes")
    return _parse(data, name)


def _parse(data, name):
    """expat into an ElementTree, refusing any DTD at its start in whatever encoding (Office never writes one, and
    external entities and entity expansion both need one), so no entity is ever declared or fetched."""
    tb, p = ET.TreeBuilder(), expat.ParserCreate(namespace_separator="}")
    qn = lambda n: "{" + n if "}" in n else n  # noqa: E731  expat's 'uri}local' as ElementTree's '{uri}local'

    def no_dtd(*_):
        raise OfficeError(f"{name} declares a DTD, which Office never writes: not read")
    p.StartDoctypeDeclHandler = p.EntityDeclHandler = no_dtd
    p.StartElementHandler = lambda tag, attrs: tb.start(qn(tag), {qn(k): v for k, v in attrs.items()})
    p.EndElementHandler = lambda tag: tb.end(qn(tag))
    p.CharacterDataHandler = tb.data
    try:
        p.Parse(data, True)
        return tb.close()
    except expat.ExpatError as e:
        raise OfficeError(f"{name} isn't well-formed XML: {e}") from None


def _value(c, shared):
    t, v = c.get("t"), c.find(M + "v")
    text = v.text if v is not None else None
    if t == "s":
        try:
            return shared[int(text)]
        except (TypeError, ValueError, IndexError):
            return ""
    if t == "inlineStr":
        return "".join(x.text or "" for x in c.iter(M + "t"))
    if t == "b":
        return text == "1"
    if t in ("e", "str"):
        return text or ""
    try:
        return float(text) if text is not None else None
    except ValueError:
        return text


def workbook(path):
    """[(sheet name, {"B7": value}, [(ref, error code)])] in the workbook's order."""
    with zipfile.ZipFile(path) as z:
        wb = _xml(z, "xl/workbook.xml")
        if wb is None:
            raise OfficeError("no xl/workbook.xml: not an xlsx workbook")
        rels = _xml(z, "xl/_rels/workbook.xml.rels")
        targets = {r.get("Id"): r.get("Target") or "" for r in (rels if rels is not None else [])}
        sst = _xml(z, "xl/sharedStrings.xml")
        shared = ["".join(t.text or "" for t in si.iter(M + "t")) for si in (sst if sst is not None else [])]
        out = []
        for s in wb.iter(M + "sheet"):
            target = targets.get(s.get(R + "id"), "")
            member = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
            root = _xml(z, member)
            cells, errors = {}, []
            for c in (root.iter(M + "c") if root is not None else ()):
                ref = (c.get("r") or "").upper()
                cells[ref] = _value(c, shared)
                if c.get("t") == "e":
                    errors.append((ref, cells[ref]))
            out.append((s.get("name") or "", cells, errors))
        return out


def document(path):
    """A docx's paragraphs' text, one a line (body only)."""
    with zipfile.ZipFile(path) as z:
        root = _xml(z, "word/document.xml")
        if root is None:
            raise OfficeError("no word/document.xml: not a docx document")
        return "\n".join("".join(t.text or "" for t in p.iter(W + "t")) for p in root.iter(W + "p"))


def _same(got, want):
    if isinstance(got, bool):
        return want.strip().lower() == str(got).lower()
    if isinstance(got, float):
        try:
            return abs(got - float(want)) <= 1e-9 * max(1.0, abs(got))
        except ValueError:
            return False
    return ("" if got is None else str(got)) == want


def check(path, cells=(), sheets=None, contains=()):
    """(failures, summary): the failed checks as lines (empty when all hold) and one line on what was read."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        if contains:
            raise OfficeError("--contains is for docx; a workbook takes --cell")
        book, fails = workbook(path), []
        for name, _, errors in book:
            fails += [f"{name}!{ref} is {code}" for ref, code in errors[:20]]
        if sheets is not None and len(book) != sheets:
            fails.append(f"{len(book)} sheets, not {sheets}")
        byname = {name: values for name, values, _ in book}
        for spec in cells:
            m = CELL.match(spec)
            if not m:
                raise OfficeError(f"--cell {spec!r}: give Sheet!B7=value (quote a sheet name with spaces: 'My sheet'!B7=1)")
            name, ref, want = (m.group(1) or "").replace("''", "'") or m.group(2), (m.group(3) + m.group(4)).upper(), m.group(5)
            if name not in byname:
                fails.append(f"no sheet {name!r} (sheets: {', '.join(byname) or 'none'})")
            elif not _same(byname[name].get(ref), want):
                fails.append(f"{name}!{ref} is {byname[name].get(ref)!r}, not {want!r}")
        n = sum(len(v) for _, v, _ in book)
        return fails, f"{len(book)} sheet(s), {n} cells read"
    if ext == ".docx":
        if cells or sheets is not None:
            raise OfficeError("--cell and --sheets are for xlsx; a document takes --contains")
        text = document(path)
        fails = [f"broken field: {e!r}" for e in WORD_ERRORS if e in text]
        fails += [f"doesn't contain {want!r}" for want in contains if want not in text]
        return fails, f"{text.count(chr(10)) + 1 if text else 0} paragraph(s) read"
    raise OfficeError(f"{ext or 'no extension'}: fm check office reads .xlsx, .xlsm and .docx")


def cmd(args):
    import fmcli
    words = args.words or []
    if len(words) != 1:
        print("fm check office FILE [--cell 'Sheet1!B7=42' …] [--sheets N] [--contains TEXT …]", file=sys.stderr)
        return 2
    path = words[0]
    try:
        fails, summary = check(path, args.cell or (), args.sheets, args.contains or ())
    except (OSError, zipfile.BadZipFile, OfficeError) as e:
        print(f"fm check office: {path}: {e}", file=sys.stderr)
        return 2
    fmcli.out(args, {"file": path, "ok": not fails, "failures": fails, "read": summary},
              "\n".join([f"✗ {path}: {x}" for x in fails] or [f"✓ {path}: {summary}, every check holds"]))
    return 1 if fails else 0
