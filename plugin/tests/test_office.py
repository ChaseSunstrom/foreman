"""T-1406: fm check office, a stdlib asserter for xlsx and docx deliverables."""
import json
import os
import zipfile

from helpers import ForemanTestCase

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RELS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORD = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def xlsx(path, cells, sheets=("Sheet1",)):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("xl/workbook.xml", f'<workbook xmlns="{MAIN}" xmlns:r="{RELS}"><sheets>' + "".join(
            f'<sheet name="{n}" sheetId="{i}" r:id="rId{i}"/>' for i, n in enumerate(sheets, 1)) + "</sheets></workbook>")
        z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                   'relationships">' + "".join(f'<Relationship Id="rId{i}" Target="worksheets/sheet{i}.xml"/>'
                                               for i in range(1, len(sheets) + 1)) + "</Relationships>")
        z.writestr("xl/sharedStrings.xml", f'<sst xmlns="{MAIN}"><si><t>Total</t></si></sst>')
        for i in range(1, len(sheets) + 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", f'<worksheet xmlns="{MAIN}"><sheetData><row r="7">{cells}</row>'
                                                       "</sheetData></worksheet>")


def docx(path, text, member=None):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", member if member is not None else
                   f'<w:document xmlns:w="{WORD}"><w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>')


CLEAN = '<c r="A7" t="s"><v>0</v></c><c r="B7"><v>42</v></c><c r="D7" t="b"><v>1</v></c>'


class Office(ForemanTestCase):
    def office(self, *a):
        return self.fm("check", "office", *a, check=False)

    def test_a_workbook_with_an_error_cell_fails_and_a_clean_one_passes(self):
        good, bad = os.path.join(self.tmp, "good.xlsx"), os.path.join(self.tmp, "bad.xlsx")
        xlsx(good, CLEAN)
        xlsx(bad, CLEAN + '<c r="C7" t="e"><f>A1/0</f><v>#REF!</v></c>')
        p = self.office(good)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("✓", p.stdout)
        p = self.office(bad)
        self.assertEqual(p.returncode, 1)
        self.assertIn("Sheet1!C7 is #REF!", p.stdout)
        self.assertEqual(json.loads(self.office(bad, "--json").stdout)["failures"], ["Sheet1!C7 is #REF!"])

    def test_cells_and_the_sheet_count_are_checked(self):
        book = os.path.join(self.tmp, "b.xlsx")
        xlsx(book, CLEAN, sheets=("Sheet1", "My sheet"))
        for ok in ("Sheet1!B7=42", "Sheet1!b7=42.0", "Sheet1!A7=Total", "'My sheet'!$B$7=42", "Sheet1!D7=true",
                   "Sheet1!Z9="):
            self.assertEqual(self.office(book, "--cell", ok).returncode, 0, ok)
        p = self.office(book, "--cell", "Sheet1!B7=41", "--sheets", "3")
        self.assertEqual(p.returncode, 1)
        self.assertIn("Sheet1!B7 is 42.0, not '41'", p.stdout)
        self.assertIn("2 sheets, not 3", p.stdout)
        self.assertIn("no sheet 'Nope'", self.office(book, "--cell", "Nope!A1=1").stdout)
        self.assertEqual(self.office(book, "--cell", "B7=42").returncode, 2, "a cell needs its sheet")

    def test_a_document_with_a_broken_field_fails_and_contains_is_checked(self):
        doc = os.path.join(self.tmp, "d.docx")
        docx(doc, "See Error! Reference source not found. for totals")
        p = self.office(doc)
        self.assertEqual(p.returncode, 1)
        self.assertIn("broken field", p.stdout)
        docx(doc, "Quarterly totals")
        self.assertEqual(self.office(doc, "--contains", "totals").returncode, 0)
        self.assertIn("doesn't contain 'revenue'", self.office(doc, "--contains", "revenue").stdout)

    def test_a_dtd_in_any_encoding_and_files_it_cannot_read_are_refused(self):
        doc = os.path.join(self.tmp, "x.docx")
        bomb = ('<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE d [<!ENTITY a "aaaa">]><w:document xmlns:w="'
                + WORD + '"><w:body><w:p><w:r><w:t>&a;</w:t></w:r></w:p></w:body></w:document>').encode("utf-16")
        docx(doc, "", member=bomb)
        p = self.office(doc)
        self.assertEqual(p.returncode, 2)
        self.assertIn("declares a DTD", p.stderr)
        junk = os.path.join(self.tmp, "j.xlsx")
        with open(junk, "w") as f:
            f.write("not a zip")
        self.assertEqual(self.office(junk).returncode, 2)
        self.assertEqual(self.office(os.path.join(self.tmp, "old.xls")).returncode, 2)
        self.assertIn("--cell", self.office(doc, "--cell", "Sheet1!A1=1").stderr)
