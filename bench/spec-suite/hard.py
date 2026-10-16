"""Spec suite, round 2 (T-1237): harder tasks, graded by the whole suite. Data only; make.py --suite hard builds it.

The repo is ledger, a small invoicing package whose modules share helpers (money, text). Four tasks change behaviour a
shared helper gives to one caller while a "Keep:" rule in the spec says another caller's must not change, so the
obvious edit to the helper breaks that caller's existing tests. Four have dense edge-case specs. A task's "files" map
each path to its whole new text (str) or to [(old, new)] edits on the parent's text, each old found exactly once.
Its "naive" entry is the plausible shortcut ("what"), as files on top of the parent, and the test module it must
fail ("fails"); make.py --check proves it does.
"""

VERIFY = "python3 -m unittest discover -s tests"

BASE_MESSAGE = r'''
ledger: a small stdlib-only invoicing package: money, text, invoices, export, customers, import, reports

Python 3.10+, standard library only. Each module is ledger/<name>.py with its unittest tests in
tests/test_<name>.py. Run every test with: python3 -m unittest discover -s tests
'''

BASE_FILES = {
    "README.md": r'''
# ledger

A small invoicing toolkit. Python 3.10+, standard library only.

- Each module is `ledger/<name>.py`; its tests are `tests/test_<name>.py` (unittest).
- Run every test from the repo root: `python3 -m unittest discover -s tests`
- Amounts of money are whole cents (int).
- Modules share helpers: `money` (amounts) and `text` (slugs, padding, wrapping) are used by `invoice`,
  `export`, `customers`, `importer` and `report`.
- The existing tests describe behaviour other code relies on. A change keeps them passing, and edits a test
  only where its task changes the behaviour that test checks.
''',
    ".gitignore": "__pycache__/\n",
    "ledger/__init__.py": r'''
"""ledger: a small stdlib-only invoicing toolkit."""
''',
    "ledger/money.py": r'''
"""Amounts of money, held as whole cents (int)."""
import re
from decimal import ROUND_HALF_UP, Decimal

_AMOUNT = re.compile(r"(-?)([0-9]+)(?:\.([0-9]{2}))?")


def parse_amount(text):
    """The cents in an exact amount: ASCII digits, an optional "-" before them and an optional "." and two digits
    after them. "12.34" is 1234, "-0.50" is -50, "7" is 700. Anything else raises ValueError."""
    m = _AMOUNT.fullmatch(text)
    if not m:
        raise ValueError(f"not an amount: {text!r}")
    sign, whole, frac = m.groups()
    cents = int(whole) * 100 + int(frac or 0)
    return -cents if sign else cents


def format_amount(cents):
    """The amount with two decimals and no separators: 1234 is "12.34", -5 is "-0.05", 0 is "0.00"."""
    sign = "-" if cents < 0 else ""
    whole, frac = divmod(abs(cents), 100)
    return f"{sign}{whole}.{frac:02d}"


def percent(cents, rate):
    """rate percent of cents (rate an int or a decimal string such as "7.5"), rounded to whole cents with halves
    away from zero: percent(250, 1) is 3, percent(-250, 1) is -3."""
    exact = Decimal(cents) * Decimal(rate) / 100
    return int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP))
''',
    "ledger/text.py": r'''
"""Text helpers shared by the other modules."""
import re
import unicodedata


def slugify(text):
    """Lowercase ASCII words joined by "-": accents dropped, each run of other characters one "-", none at the ends.
    "Smith & Sons" is "smith-sons"."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def pad(text, width, align="left"):
    """text padded with spaces to width, "left", "right" or "center" aligned; a longer text is returned whole."""
    if align == "left":
        return text.ljust(width)
    if align == "right":
        return text.rjust(width)
    if align == "center":
        return text.center(width)
    raise ValueError(f"align must be left, right or center, got {align!r}")


def wrap(text, width):
    """The words of text as lines of at most width characters; a longer word gets a line of its own."""
    if width < 1:
        raise ValueError(f"width must be at least 1, got {width}")
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}" if line else word
    if line:
        lines.append(line)
    return lines
''',
    "ledger/invoice.py": r'''
"""Invoices: lines, totals, a line typed as text, and a plain-text rendering."""
import dataclasses
import datetime
import re

from ledger import money, text


@dataclasses.dataclass
class Line:
    description: str
    quantity: int
    unit_price: int  # cents
    tax_rate: str = "0"  # percent: an int or a decimal string such as "7.5"
    discount: str = "0"  # percent taken off the line


@dataclasses.dataclass
class Invoice:
    number: str
    customer: str
    date: datetime.date
    lines: list = dataclasses.field(default_factory=list)
    notes: str = ""


def line_net(line):
    """quantity * unit_price less the discount, money.percent of it (halves rounded away from zero)."""
    gross = line.quantity * line.unit_price
    return gross - money.percent(gross, line.discount)


def line_tax(line):
    """The tax on the line's net amount: money.percent(line_net(line), line.tax_rate)."""
    return money.percent(line_net(line), line.tax_rate)


def totals(invoice):
    """(net, tax, total) of the invoice's lines, in cents."""
    net = sum(line_net(line) for line in invoice.lines)
    tax = sum(line_tax(line) for line in invoice.lines)
    return net, tax, net + tax


_TYPED = re.compile(r"([0-9]+) x (.+) @ (\S+)")


def parse_line(entry, tax_rate="0"):
    """A Line from text typed as "<quantity> x <description> @ <unit price>", such as "3 x Widget @ 2.50": the
    price is read by money.parse_amount, leading and trailing whitespace is ignored, anything else raises
    ValueError."""
    m = _TYPED.fullmatch(entry.strip())
    if not m:
        raise ValueError(f"not an invoice line: {entry!r}")
    quantity, description, price = m.groups()
    return Line(description, int(quantity), money.parse_amount(price), tax_rate)


def render(invoice):
    """The invoice as text, rows joined with "\n" and no newline at the end:
        "Invoice <number>", "Date: <YYYY-MM-DD>", "To: <customer>", ""
        one row per line: the description padded to 30, " ", the quantity right-aligned in 4, " x ", the unit
            price right-aligned in 10, " ", the line's net amount right-aligned in 12
        "", then "Net", "Tax" and "Total" rows: the label padded to 49, then the amount right-aligned in 12
        when notes has a non-whitespace character: "", "Notes:", then text.wrap(notes, 61)
    Amounts are written by money.format_amount; text.pad keeps a longer value whole."""
    rows = [f"Invoice {invoice.number}", f"Date: {invoice.date.isoformat()}", f"To: {invoice.customer}", ""]
    for line in invoice.lines:
        rows.append(f"{text.pad(line.description, 30)} {text.pad(str(line.quantity), 4, 'right')} x "
                    f"{text.pad(money.format_amount(line.unit_price), 10, 'right')} "
                    f"{text.pad(money.format_amount(line_net(line)), 12, 'right')}")
    rows.append("")
    for label, amount in zip(("Net", "Tax", "Total"), totals(invoice)):
        rows.append(text.pad(label, 49) + text.pad(money.format_amount(amount), 12, "right"))
    if invoice.notes.strip():
        rows += ["", "Notes:", *text.wrap(invoice.notes, 61)]
    return "\n".join(rows)
''',
    "ledger/export.py": r'''
"""Invoices to CSV for spreadsheets and accounting tools, and the export's file name."""
from ledger import invoice as inv, money, text

HEADER = "number,date,customer,net,tax,total"


def _field(value):
    """A CSV field: in double quotes, each " doubled, when it holds a comma, a double quote or a newline."""
    if any(ch in value for ch in ',"\n'):
        return '"' + value.replace('"', '""') + '"'
    return value


def to_csv(invoices):
    """HEADER, then one row per invoice (number, ISO date, customer, net, tax, total), each row ending in "\n";
    amounts are written by money.format_amount."""
    rows = [HEADER]
    for invoice in invoices:
        amounts = [money.format_amount(a) for a in inv.totals(invoice)]
        rows.append(",".join([_field(invoice.number), invoice.date.isoformat(), _field(invoice.customer), *amounts]))
    return "\n".join(rows) + "\n"


def filename(invoice):
    """"<customer part>-<number part>.csv", each part text.slugify of the customer and of the number:
    "Acme Corp." and "INV-0007" give "acme-corp-inv-0007.csv"."""
    return f"{text.slugify(invoice.customer)}-{text.slugify(invoice.number)}.csv"
''',
    "ledger/customers.py": r'''
"""Customers: names to stable keys, and a directory of them."""
from ledger import text


def key(name):
    """The customer's key, text.slugify(name): "Smith & Sons" is "smith-sons". Keys are stored in saved data, so a
    name's key never changes. A name without a letter or digit raises ValueError."""
    k = text.slugify(name)
    if not k:
        raise ValueError(f"a customer name needs a letter or a digit: {name!r}")
    return k


class Directory:
    """Customers by key: names that differ only in case, accents or punctuation are one customer."""

    def __init__(self):
        self._names = {}

    def add(self, name):
        """The customer's key; the first name added for a key is the one kept."""
        k = key(name)
        self._names.setdefault(k, name)
        return k

    def name(self, k):
        """The name kept for key k; KeyError when there is none."""
        return self._names[k]

    def __len__(self):
        return len(self._names)

    def __contains__(self, name):
        try:
            return key(name) in self._names
        except ValueError:
            return False
''',
    "ledger/importer.py": r'''
"""Bank statement import: lines of "date;description;amount"."""
import datetime

from ledger import money


def read_rows(data):
    """[(date, description, cents)] from lines "YYYY-MM-DD;description;amount"; blank lines are skipped. A bank
    file's amounts must be exact, so each is read by money.parse_amount. A bad line (not three fields, a bad date or
    amount) raises ValueError whose message starts with "line <n>: " (n counted from 1)."""
    rows = []
    for n, line in enumerate(data.splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split(";")
        if len(fields) != 3:
            raise ValueError(f"line {n}: expected date;description;amount, got {line!r}")
        day, description, amount = fields
        try:
            rows.append((datetime.date.fromisoformat(day), description, money.parse_amount(amount)))
        except ValueError as e:
            raise ValueError(f"line {n}: {e}") from None
    return rows
''',
    "ledger/report.py": r'''
"""Monthly summaries of invoices."""
from ledger import invoice as inv, money, text


def monthly_totals(invoices):
    """{"YYYY-MM": total in cents} of the invoices' totals (invoice.totals), months in ascending order."""
    months = {}
    for invoice in invoices:
        month = f"{invoice.date.year:04d}-{invoice.date.month:02d}"
        months[month] = months.get(month, 0) + inv.totals(invoice)[2]
    return dict(sorted(months.items()))


def render_summary(invoices):
    """One row per month, "YYYY-MM" padded to 10 and its total right-aligned in 14, then a "Total" row over all
    months laid out the same; rows joined with "\n". Amounts are written by money.format_amount."""
    months = monthly_totals(invoices)
    rows = [text.pad(m, 10) + text.pad(money.format_amount(c), 14, "right") for m, c in months.items()]
    rows.append(text.pad("Total", 10) + text.pad(money.format_amount(sum(months.values())), 14, "right"))
    return "\n".join(rows)
''',
    "tests/__init__.py": "",
    "tests/test_money.py": r'''
import unittest

from ledger.money import format_amount, parse_amount, percent


class ParseAmountTest(unittest.TestCase):
    def test_whole_amounts_and_two_decimals(self):
        self.assertEqual(parse_amount("12.34"), 1234)
        self.assertEqual(parse_amount("7"), 700)
        self.assertEqual(parse_amount("0.05"), 5)
        self.assertEqual(parse_amount("-0.50"), -50)

    def test_anything_else_raises_value_error(self):
        for text in ["", "12.5", "12.345", "1,234.50", " 12", "12 ", "+3", "€12", "12.", ".50", "1e3"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_amount(text)


class FormatAmountTest(unittest.TestCase):
    def test_two_decimals_and_no_separators(self):
        self.assertEqual(format_amount(1234), "12.34")
        self.assertEqual(format_amount(5), "0.05")
        self.assertEqual(format_amount(0), "0.00")
        self.assertEqual(format_amount(-5), "-0.05")
        self.assertEqual(format_amount(123456789), "1234567.89")


class PercentTest(unittest.TestCase):
    def test_rounds_to_whole_cents(self):
        self.assertEqual(percent(1000, 19), 190)
        self.assertEqual(percent(999, "7.5"), 75)

    def test_halves_round_away_from_zero(self):
        self.assertEqual(percent(250, 1), 3)
        self.assertEqual(percent(350, 1), 4)
        self.assertEqual(percent(-250, 1), -3)


if __name__ == "__main__":
    unittest.main()
''',
    "tests/test_text.py": r'''
import unittest

from ledger.text import pad, slugify, wrap


class SlugifyTest(unittest.TestCase):
    def test_lowercases_and_joins_words_with_dashes(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_drops_accents_and_outer_dashes(self):
        self.assertEqual(slugify("  Crème brûlée  "), "creme-brulee")

    def test_symbols_are_separators(self):
        self.assertEqual(slugify("Smith & Sons"), "smith-sons")
        self.assertEqual(slugify("A+B@C"), "a-b-c")


class PadTest(unittest.TestCase):
    def test_aligns(self):
        self.assertEqual(pad("ab", 5), "ab   ")
        self.assertEqual(pad("ab", 5, "right"), "   ab")
        self.assertEqual(pad("ab", 6, "center"), "  ab  ")

    def test_a_longer_text_is_kept_whole(self):
        self.assertEqual(pad("abcdef", 3, "right"), "abcdef")

    def test_an_unknown_alignment_raises_value_error(self):
        with self.assertRaises(ValueError):
            pad("ab", 5, "middle")


class WrapTest(unittest.TestCase):
    def test_breaks_between_words(self):
        self.assertEqual(wrap("the quick brown fox", 10), ["the quick", "brown fox"])

    def test_a_long_word_gets_its_own_line(self):
        self.assertEqual(wrap("a supercalifragilistic b", 5), ["a", "supercalifragilistic", "b"])

    def test_width_below_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            wrap("x", 0)


if __name__ == "__main__":
    unittest.main()
''',
    "tests/test_invoice.py": r'''
import datetime
import unittest

from ledger.invoice import Invoice, Line, line_net, line_tax, parse_line, render, totals


def sample():
    return Invoice("INV-0007", "Acme & Sons", datetime.date(2026, 1, 31), [
        Line("Widget", 3, 250, "19"),
        Line("Consulting, senior", 12, 150000, "19", "10"),
    ], notes="Payable within 30 days to account DE89370400440532013000. Thank you for your business!")


class LineTest(unittest.TestCase):
    def test_line_net_takes_the_discount_off(self):
        self.assertEqual(line_net(Line("Widget", 3, 250)), 750)
        self.assertEqual(line_net(Line("Pen", 1, 50, discount="5")), 47)

    def test_line_tax(self):
        self.assertEqual(line_tax(Line("Widget", 3, 250, "19")), 143)
        self.assertEqual(line_tax(Line("Lamp", 1, 999, "7.5")), 75)

    def test_totals(self):
        self.assertEqual(totals(sample()), (1620750, 307943, 1928693))
        self.assertEqual(totals(Invoice("INV-1", "A", datetime.date(2026, 1, 1))), (0, 0, 0))


class ParseLineTest(unittest.TestCase):
    def test_reads_quantity_description_and_price(self):
        self.assertEqual(parse_line("3 x Widget @ 2.50"), Line("Widget", 3, 250, "0"))
        self.assertEqual(parse_line(" 12 x Consulting, senior @ 1500.00 ", "19"),
                         Line("Consulting, senior", 12, 150000, "19"))

    def test_a_malformed_line_raises_value_error(self):
        for entry in ["x Widget @ 2.50", "3 Widget @ 2.50", "3 x Widget", "3 x  @ 2.50", "3 x Widget @ 2.5",
                      "3 x Widget @ 1,500.00"]:
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                parse_line(entry)


class RenderTest(unittest.TestCase):
    def test_lays_out_the_invoice(self):
        self.assertEqual(render(sample()), "\n".join([
            "Invoice INV-0007",
            "Date: 2026-01-31",
            "To: Acme & Sons",
            "",
            "Widget                            3 x       2.50         7.50",
            "Consulting, senior               12 x    1500.00     16200.00",
            "",
            "Net                                                  16207.50",
            "Tax                                                   3079.43",
            "Total                                                19286.93",
            "",
            "Notes:",
            "Payable within 30 days to account DE89370400440532013000.",
            "Thank you for your business!",
        ]))

    def test_no_notes_no_notes_section(self):
        invoice = Invoice("INV-2", "B", datetime.date(2026, 2, 1), [Line("Box", 1, 999)], notes="  ")
        self.assertEqual(render(invoice).splitlines()[-1], "Total" + " " * 52 + "9.99")


if __name__ == "__main__":
    unittest.main()
''',
    "tests/test_export.py": r'''
import datetime
import unittest

from ledger.export import filename, to_csv
from ledger.invoice import Invoice, Line


def invoices():
    return [
        Invoice("INV-0007", "Acme & Sons", datetime.date(2026, 1, 31), [Line("Consulting", 10, 150000, "19")]),
        Invoice("INV-0008", 'The "Best", Ltd', datetime.date(2026, 2, 1), [Line("Widget", 3, 250)]),
    ]


class ToCsvTest(unittest.TestCase):
    def test_one_row_per_invoice(self):
        self.assertEqual(to_csv(invoices()), (
            "number,date,customer,net,tax,total\n"
            "INV-0007,2026-01-31,Acme & Sons,15000.00,2850.00,17850.00\n"
            'INV-0008,2026-02-01,"The ""Best"", Ltd",7.50,0.00,7.50\n'))

    def test_no_invoices_just_the_header(self):
        self.assertEqual(to_csv([]), "number,date,customer,net,tax,total\n")


class FilenameTest(unittest.TestCase):
    def test_customer_and_number_slugs(self):
        self.assertEqual(filename(invoices()[0]), "acme-sons-inv-0007.csv")
        self.assertEqual(filename(Invoice("INV/2026 #7", "Crème Café", datetime.date(2026, 3, 1))),
                         "creme-cafe-inv-2026-7.csv")


if __name__ == "__main__":
    unittest.main()
''',
    "tests/test_customers.py": r'''
import unittest

from ledger.customers import Directory, key


class KeyTest(unittest.TestCase):
    def test_keys_are_slugs(self):
        self.assertEqual(key("Smith & Sons"), "smith-sons")
        self.assertEqual(key("Crème Brûlée Café"), "creme-brulee-cafe")
        self.assertEqual(key("A+B @ Home"), "a-b-home")

    def test_a_name_without_letters_or_digits_raises_value_error(self):
        with self.assertRaises(ValueError):
            key("!!!")


class DirectoryTest(unittest.TestCase):
    def test_names_that_differ_only_in_case_or_punctuation_are_one_customer(self):
        d = Directory()
        self.assertEqual(d.add("Acme Corp."), "acme-corp")
        self.assertEqual(d.add("ACME corp"), "acme-corp")
        self.assertEqual(len(d), 1)
        self.assertEqual(d.name("acme-corp"), "Acme Corp.")

    def test_membership(self):
        d = Directory()
        d.add("Smith & Sons")
        self.assertIn("smith  sons", d)
        self.assertNotIn("Smith and Sons", d)
        self.assertNotIn("&", d)


if __name__ == "__main__":
    unittest.main()
''',
    "tests/test_importer.py": r'''
import datetime
import unittest

from ledger.importer import read_rows


class ReadRowsTest(unittest.TestCase):
    def test_reads_rows_and_skips_blank_lines(self):
        self.assertEqual(read_rows("2026-01-05;Coffee;-3.50\n\n  \n2026-01-06;Refund, partial;12.00\n"), [
            (datetime.date(2026, 1, 5), "Coffee", -350),
            (datetime.date(2026, 1, 6), "Refund, partial", 1200),
        ])

    def test_an_inexact_amount_raises_value_error_naming_its_line(self):
        for amount in ["12.5", "1,234.50", "€12", "$3", " 12.00", "12.00 ", "12.345"]:
            with self.subTest(amount=amount), self.assertRaisesRegex(ValueError, "^line 2: "):
                read_rows("2026-01-05;ok;1.00\n2026-01-06;bad;" + amount)

    def test_a_line_without_three_fields_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "^line 1: "):
            read_rows("2026-01-05;Coffee")

    def test_a_bad_date_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "^line 1: "):
            read_rows("2026-13-01;Coffee;1.00")


if __name__ == "__main__":
    unittest.main()
''',
    "tests/test_report.py": r'''
import datetime
import unittest

from ledger.invoice import Invoice, Line
from ledger.report import monthly_totals, render_summary


def invoices():
    return [
        Invoice("INV-2", "B", datetime.date(2026, 2, 3), [Line("Box", 1, 10000)]),
        Invoice("INV-1", "A", datetime.date(2026, 1, 9), [Line("Consulting", 10, 150000, "19")]),
        Invoice("INV-3", "A", datetime.date(2026, 1, 20), [Line("Widget", 3, 250)]),
    ]


class ReportTest(unittest.TestCase):
    def test_monthly_totals_in_month_order(self):
        totals = monthly_totals(invoices())
        self.assertEqual(totals, {"2026-01": 1785750, "2026-02": 10000})
        self.assertEqual(list(totals), ["2026-01", "2026-02"])

    def test_render_summary(self):
        self.assertEqual(render_summary(invoices()), "\n".join([
            "2026-01         17857.50",
            "2026-02           100.00",
            "Total           17957.50",
        ]))

    def test_no_invoices(self):
        self.assertEqual(monthly_totals([]), {})
        self.assertEqual(render_summary([]), "Total               0.00")


if __name__ == "__main__":
    unittest.main()
''',
}

_OLD_WRAP = '''def wrap(text, width):
    """The words of text as lines of at most width characters; a longer word gets a line of its own."""
    if width < 1:
        raise ValueError(f"width must be at least 1, got {width}")
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}" if line else word
    if line:
        lines.append(line)
    return lines
'''

_NOTES_INDENT = [
    ('''        when notes has a non-whitespace character: "", "Notes:", then text.wrap(notes, 61)''',
     '''        when notes has a non-whitespace character: "", "Notes:", then text.wrap(notes, 61, indent="  ")'''),
    ('''*text.wrap(invoice.notes, 61)]''', '''*text.wrap(invoice.notes, 61, indent="  ")]'''),
]

_IMPORT_RE = ("import re\nimport unicodedata\n", "import re\nimport textwrap\nimport unicodedata\n")

TASKS = [
    {
        "name": "grouping",
        "message": r'''
Group thousands in invoice amounts: 1234567 cents shows as 12,345.67

ledger.invoice.render writes every amount it shows (unit prices, line amounts, and the Net, Tax and
Total figures) with a "," between each group of three digits of the whole part, counting from the
right. The decimals and a minus sign are written as before:

    1234567 cents  ->  12,345.67
     100000        ->   1,000.00
      99999        ->     999.99
    -123456        ->  -1,234.56
          5        ->       0.05

The layout is otherwise unchanged: each amount is still right-aligned in its column (10 characters
for the unit price, 12 for the line amount and for the Net, Tax and Total figures), and an amount
longer than its column is still written whole.

Keep: nothing else changes. money.format_amount, export.to_csv and report.render_summary give exactly
the same results as before, with no separators: spreadsheets and accounting tools read those.
''',
        "files": {
            "ledger/money.py": [
                ('''def format_amount(cents):
    """The amount with two decimals and no separators: 1234 is "12.34", -5 is "-0.05", 0 is "0.00"."""
    sign = "-" if cents < 0 else ""
    whole, frac = divmod(abs(cents), 100)
    return f"{sign}{whole}.{frac:02d}"''',
                 '''def format_amount(cents, grouping=False):
    """The amount with two decimals and no separators: 1234 is "12.34", -5 is "-0.05", 0 is "0.00". grouping puts
    a "," between each group of three digits of the whole part: 1234567 is "12,345.67"."""
    sign = "-" if cents < 0 else ""
    whole, frac = divmod(abs(cents), 100)
    return f"{sign}{whole:,}.{frac:02d}" if grouping else f"{sign}{whole}.{frac:02d}"'''),
            ],
            "ledger/invoice.py": [
                ("{text.pad(money.format_amount(line.unit_price), 10, 'right')}",
                 "{text.pad(money.format_amount(line.unit_price, grouping=True), 10, 'right')}"),
                ("{text.pad(money.format_amount(line_net(line)), 12, 'right')}",
                 "{text.pad(money.format_amount(line_net(line), grouping=True), 12, 'right')}"),
                ('text.pad(money.format_amount(amount), 12, "right")',
                 'text.pad(money.format_amount(amount, grouping=True), 12, "right")'),
                ("    Amounts are written by money.format_amount; text.pad keeps a longer value whole.",
                 "    Amounts are written by money.format_amount with grouping (12,345.67); text.pad keeps a longer value"
                 "\n    whole."),
            ],
            "tests/test_invoice.py": [
                ('''            "Consulting, senior               12 x    1500.00     16200.00",
            "",
            "Net                                                  16207.50",
            "Tax                                                   3079.43",
            "Total                                                19286.93",''',
                 '''            "Consulting, senior               12 x   1,500.00    16,200.00",
            "",
            "Net                                                 16,207.50",
            "Tax                                                  3,079.43",
            "Total                                               19,286.93",'''),
                ('''        self.assertEqual(render(invoice).splitlines()[-1], "Total" + " " * 52 + "9.99")
''',
                 '''        self.assertEqual(render(invoice).splitlines()[-1], "Total" + " " * 52 + "9.99")

    def test_amounts_group_thousands(self):
        invoice = Invoice("INV-0009", "Big Co", datetime.date(2026, 2, 1), [
            Line("Server", 2, 123456),
            Line("Refund", 1, -100000),
            Line("Tea", 1, 99999),
            Line("Pin", 1, 5),
            Line("Gold", 1, 123456789012),
        ])
        self.assertEqual(render(invoice).splitlines()[4:], [
            "Server                            2 x   1,234.56     2,469.12",
            "Refund                            1 x  -1,000.00    -1,000.00",
            "Tea                               1 x     999.99       999.99",
            "Pin                               1 x       0.05         0.05",
            "Gold                              1 x 1,234,567,890.12 1,234,567,890.12",
            "",
            "Net" + " " * 46 + "1,234,570,359.28",
            "Tax" + " " * 54 + "0.00",
            "Total" + " " * 44 + "1,234,570,359.28",
        ])
'''),
            ],
        },
        "naive": {
            "what": "format_amount itself groups thousands",
            "fails": "test_export",
            "files": {"ledger/money.py": [('return f"{sign}{whole}.{frac:02d}"', 'return f"{sign}{whole:,}.{frac:02d}"')]},
        },
    },
    {
        "name": "wrap",
        "message": r'''
Wrap text with indents, paragraphs and long words cut to fit; indent invoice notes

ledger.text.wrap takes two more optional arguments and follows exact rules:

    wrap(text: str, width: int, indent: str = "", first_indent: str | None = None) -> list[str]

It returns text's lines wrapped to width characters.

Paragraphs:
- text is split into lines at "\n". A line that is empty or holds only whitespace separates
  paragraphs; several such lines in a row count as one break, and such lines at the start or end of
  text are ignored.
- Each paragraph is wrapped on its own, and the result holds one empty string "" between the lines
  of two paragraphs. text with no paragraph (empty, or only whitespace) gives [].
- Within a paragraph a word is a run of non-whitespace characters (what str.split() returns): a
  single "\n", tabs and runs of spaces only separate words. Hyphens are ordinary characters, so a
  line breaks only between two words, or inside a word too long for a line (below).

Lines:
- The first line of each paragraph starts with first_indent (indent when first_indent is None);
  every other line starts with indent. A line is its indent followed by its words joined with single
  spaces, and is at most width characters long, indent included. A line's room is width minus the
  length of its indent.
- Words are placed in order:
  1. A word joins the current line if it fits there (after one space when the line already has a
     word).
  2. Otherwise, if the current line has a word, that line ends, and the word goes on a new line if it
     fits there.
  3. A word that doesn't fit even on an empty line is cut: its first characters fill that line's
     room, the line ends, and the rest of the word is placed by these same rules (it may need more
     cuts, and the next words may join its last piece).
- If width leaves no room on some line, that is width < len(indent) + 1 or
  width < len(first_indent) + 1, wrap raises ValueError, even for empty text.

Invoice notes: ledger.invoice.render now writes the lines after "Notes:" as
text.wrap(notes, 61, indent="  "), so each note line is indented by two spaces and an empty line
separates paragraphs. Nothing else in render changes.

Examples:
    wrap("the quick brown fox", 10) == ["the quick", "brown fox"]
    wrap("a supercalifragilistic b", 5) == ["a", "super", "calif", "ragil", "istic", "b"]
    wrap("one\n\n\ntwo", 10) == ["one", "", "two"]
    wrap("- item one two", 8, indent="  ", first_indent="") == ["- item", "  one", "  two"]
''',
        "files": {
            "ledger/text.py": [(_OLD_WRAP, '''def wrap(text, width, indent="", first_indent=None):
    """The lines of text wrapped to width characters, indent included. Lines that are empty or only whitespace
    separate paragraphs, and one "" separates the paragraphs' lines; the first line of each paragraph starts with
    first_indent (indent when None), the others with indent. Lines break between words (runs of non-whitespace);
    a word too long for an empty line is cut to fill it and goes on on the next."""
    first_indent = indent if first_indent is None else first_indent
    if width < len(indent) + 1 or width < len(first_indent) + 1:
        raise ValueError(f"width {width} leaves no room after the indent")
    paragraphs, words = [], []
    for line in text.split("\\n"):
        if line.strip():
            words += line.split()
        elif words:
            paragraphs.append(words)
            words = []
    if words:
        paragraphs.append(words)
    lines = []
    for words in paragraphs:
        if lines:
            lines.append("")
        lead, line = first_indent, ""
        for word in words:
            while True:
                room = width - len(lead)
                if len(line) + bool(line) + len(word) <= room:  # rule 1, or rule 2 on a fresh line
                    line = f"{line} {word}" if line else word
                    break
                if line:  # rule 2: end the line, try again on a new one
                    lines.append(lead + line)
                    lead, line = indent, ""
                    continue
                lines.append(lead + word[:room])  # rule 3: cut
                lead, word = indent, word[room:]
        lines.append(lead + line)
    return lines
''')],
            "ledger/invoice.py": _NOTES_INDENT,
            "tests/test_text.py": [('''class WrapTest(unittest.TestCase):
    def test_breaks_between_words(self):
        self.assertEqual(wrap("the quick brown fox", 10), ["the quick", "brown fox"])

    def test_a_long_word_gets_its_own_line(self):
        self.assertEqual(wrap("a supercalifragilistic b", 5), ["a", "supercalifragilistic", "b"])

    def test_width_below_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            wrap("x", 0)
''', '''class WrapTest(unittest.TestCase):
    def test_breaks_between_words(self):
        self.assertEqual(wrap("the quick brown fox", 10), ["the quick", "brown fox"])
        self.assertEqual(wrap("the quick brown fox", 9), ["the quick", "brown fox"])

    def test_a_word_too_long_for_a_line_is_cut(self):
        self.assertEqual(wrap("a supercalifragilistic b", 5), ["a", "super", "calif", "ragil", "istic", "b"])

    def test_the_next_words_may_join_the_last_piece_of_a_cut_word(self):
        self.assertEqual(wrap("abcdefgh ij", 6), ["abcdef", "gh ij"])

    def test_hyphens_are_ordinary_characters(self):
        self.assertEqual(wrap("a well-known fact", 8), ["a", "well-kno", "wn fact"])
        self.assertEqual(wrap("re-enter now", 5), ["re-en", "ter", "now"])

    def test_whitespace_runs_and_single_newlines_only_separate_words(self):
        self.assertEqual(wrap("one\\ttwo\\n three   four", 9), ["one two", "three", "four"])

    def test_paragraphs(self):
        self.assertEqual(wrap("one two\\n\\n \\n\\nthree", 20), ["one two", "", "three"])
        self.assertEqual(wrap("a\\n\\nb\\n\\t\\nc", 5), ["a", "", "b", "", "c"])
        self.assertEqual(wrap("\\n\\n  a\\n\\n", 5), ["a"])

    def test_no_paragraph_no_lines(self):
        self.assertEqual(wrap("", 5), [])
        self.assertEqual(wrap(" \\n\\t\\n", 5), [])

    def test_the_indent_counts_toward_the_width(self):
        self.assertEqual(wrap("one two three four", 9, indent="  "), ["  one two", "  three", "  four"])

    def test_first_indent(self):
        self.assertEqual(wrap("- item one two", 8, indent="  ", first_indent=""), ["- item", "  one", "  two"])
        self.assertEqual(wrap("aaa bbb ccc", 7, first_indent="    "), ["    aaa", "bbb ccc"])

    def test_each_paragraph_starts_with_first_indent(self):
        self.assertEqual(wrap("a b\\n\\nc d", 3, indent="  ", first_indent="* "), ["* a", "  b", "", "* c", "  d"])

    def test_a_cut_fills_the_room_of_its_own_line(self):
        self.assertEqual(wrap("abcdefghij", 7, indent=" ", first_indent="   "), ["   abcd", " efghij"])

    def test_no_room_raises_value_error(self):
        for args in [("x", 0), ("x", 2, "  "), ("x", 3, "", "   "), ("", 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                wrap(*args)
''')],
            "tests/test_invoice.py": [
                ('''            "Notes:",
            "Payable within 30 days to account DE89370400440532013000.",
            "Thank you for your business!",''',
                 '''            "Notes:",
            "  Payable within 30 days to account DE89370400440532013000.",
            "  Thank you for your business!",'''),
                ("    def test_amounts_group_thousands(self):\n", '''    def test_notes_are_wrapped_with_a_two_space_indent(self):
        invoice = Invoice("INV-3", "C", datetime.date(2026, 3, 1), notes="Thanks!\\n\\nBank: " + "x" * 70)
        self.assertEqual(render(invoice).splitlines()[-6:],
                         ["Notes:", "  Thanks!", "", "  Bank:", "  " + "x" * 59, "  " + "x" * 11])

    def test_amounts_group_thousands(self):
'''),
            ],
        },
        "naive": {
            "what": "wrap via textwrap.wrap",
            "fails": "test_text",
            "files": {
                "ledger/text.py": [_IMPORT_RE, (_OLD_WRAP, '''def wrap(text, width, indent="", first_indent=None):
    """The lines of text wrapped to width characters."""
    return textwrap.wrap(text, width, initial_indent=indent if first_indent is None else first_indent,
                         subsequent_indent=indent)
''')],
                "ledger/invoice.py": _NOTES_INDENT,
            },
        },
    },
    {
        "name": "filenames",
        "message": r'''
Export file names: spell out &, + and @, cap the customer part at 30 characters, never leave it empty

ledger.export.filename(invoice) still returns "<customer part>-<number part>.csv". The customer part
changes:

- Before slugifying, each "&" in the customer name becomes the word "and", each "+" the word "plus"
  and each "@" the word "at", each a word of its own: "Smith & Sons" and "Smith&Sons" both give
  "smith-and-sons", "A+B" gives "a-plus-b", "Ann @ Home" gives "ann-at-home".
- The result of text.slugify is then cut to its first 30 characters, and a "-" left at the end of
  the cut is dropped.
- If the customer part comes out empty (a name with no letter, digit, "&", "+" or "@"), it is
  "customer".

The number part is unchanged: text.slugify(invoice.number).

Keep: customers.key must give every name the same key as before, because keys are stored in saved
data ("Smith & Sons" keeps the key "smith-sons"). text.slugify and export.to_csv don't change.

Examples:
    filename(Invoice("INV-0008", "Smith & Sons", ...)) == "smith-and-sons-inv-0008.csv"
    filename(Invoice("INV-0009", "!!!", ...)) == "customer-inv-0009.csv"
''',
        "files": {
            "ledger/export.py": [('''def filename(invoice):
    """"<customer part>-<number part>.csv", each part text.slugify of the customer and of the number:
    "Acme Corp." and "INV-0007" give "acme-corp-inv-0007.csv"."""
    return f"{text.slugify(invoice.customer)}-{text.slugify(invoice.number)}.csv"
''', '''_SPELLED = {"&": " and ", "+": " plus ", "@": " at "}


def filename(invoice):
    """"<customer part>-<number part>.csv". The customer part is text.slugify of the customer with each "&", "+"
    and "@" spelled out as a word, cut to 30 characters with no "-" left at its end, or "customer" when that is
    empty; the number part is text.slugify(number). "Smith & Sons" and "INV-0008" give
    "smith-and-sons-inv-0008.csv"."""
    spelled = "".join(_SPELLED.get(ch, ch) for ch in invoice.customer)
    customer = text.slugify(spelled)[:30].rstrip("-") or "customer"
    return f"{customer}-{text.slugify(invoice.number)}.csv"
''')],
            "tests/test_export.py": [('''class FilenameTest(unittest.TestCase):
    def test_customer_and_number_slugs(self):
        self.assertEqual(filename(invoices()[0]), "acme-sons-inv-0007.csv")
        self.assertEqual(filename(Invoice("INV/2026 #7", "Crème Café", datetime.date(2026, 3, 1))),
                         "creme-cafe-inv-2026-7.csv")
''', '''def named(customer, number="INV-0008"):
    return Invoice(number, customer, datetime.date(2026, 2, 1))


class FilenameTest(unittest.TestCase):
    def test_customer_and_number_slugs(self):
        self.assertEqual(filename(named("Acme Corp.", "INV-0007")), "acme-corp-inv-0007.csv")
        self.assertEqual(filename(named("Crème Café", "INV/2026 #7")), "creme-cafe-inv-2026-7.csv")

    def test_symbols_are_spelled_out_as_words(self):
        self.assertEqual(filename(named("Smith & Sons")), "smith-and-sons-inv-0008.csv")
        self.assertEqual(filename(named("Smith&Sons")), "smith-and-sons-inv-0008.csv")
        self.assertEqual(filename(named("A+B")), "a-plus-b-inv-0008.csv")
        self.assertEqual(filename(named("Ann @ Home")), "ann-at-home-inv-0008.csv")
        self.assertEqual(filename(named("&")), "and-inv-0008.csv")

    def test_the_number_part_is_unchanged(self):
        self.assertEqual(filename(named("Acme", "A&B+1")), "acme-a-b-1.csv")

    def test_the_customer_part_is_cut_to_30_characters(self):
        self.assertEqual(filename(named("Northern Lights Photography & Video")),
                         "northern-lights-photography-an-inv-0008.csv")
        self.assertEqual(filename(named("Abcdefghijklmnopqrstuvwxyzabc Def")),
                         "abcdefghijklmnopqrstuvwxyzabc-inv-0008.csv")

    def test_an_empty_customer_part_is_customer(self):
        self.assertEqual(filename(named("!!!", "INV-0009")), "customer-inv-0009.csv")
        self.assertEqual(filename(named("")), "customer-inv-0008.csv")
''')],
        },
        "naive": {
            "what": "slugify itself spells out & + @",
            "fails": "test_customers",
            "files": {
                "ledger/text.py": [('''    ascii_text = unicodedata.normalize(''', '''    text = text.replace("&", " and ").replace("+", " plus ").replace("@", " at ")
    ascii_text = unicodedata.normalize(''')],
                "ledger/export.py": [('''    return f"{text.slugify(invoice.customer)}-{text.slugify(invoice.number)}.csv"''',
                                      '''    customer = text.slugify(invoice.customer)[:30].rstrip("-") or "customer"
    return f"{customer}-{text.slugify(invoice.number)}.csv"''')],
            },
        },
    },
    {
        "name": "ini",
        "message": r'''
Add ledger.ini.parse: read INI settings, with comments and continued values

Add the module ledger/ini.py with one function:

    parse(text: str) -> dict[str, dict[str, str]]

It returns {section name: {key: value}}, sections and keys in the order they first appear.

text is read line by line (str.splitlines()). Each line is the first of these that fits it:

1. Blank: empty or only whitespace. It ends the value being continued, if any (rule 3).
2. Comment: its first non-whitespace character is "#" or ";". It is skipped, and doesn't end the
   value being continued.
3. Continuation: it starts with a space or a tab while a value is being continued, that is, while
   the last line other than comments was a key line or a continuation. Its text, with any inline
   comment removed and then stripped, is added to the end of that value after one space (or becomes
   the value, if the value is empty).
4. Section header: once stripped, it starts with "[". With any inline comment removed and then
   stripped, it must be "[" name "]", where name holds no "[" or "]" and, stripped, isn't empty.
   The section's name is the stripped name; names are case-sensitive. A header for a section that
   has appeared before raises ValueError. A section with no keys is kept, as {}.
5. Key line: once stripped, it contains "=". The key is the text before the first "=", stripped and
   lowercased; an empty key raises ValueError. The value is the text after that "=", with any inline
   comment removed, then stripped; it may be empty. A key line before the first section header
   raises ValueError. A key that appears again in its section replaces the earlier value and keeps
   its first position.
6. Anything else raises ValueError.

So an indented line is a continuation only while a value is being continued; any other indented
line is read like an unindented one.

Inline comments: in a value, a continuation or a header, a "#" or ";" right after a space or a tab
starts a comment that runs to the end of the line. Anywhere else these characters are ordinary
text: "a=x#y" has the value "x#y", and "a = #y" has the value "".

Every ValueError's message contains "line N", N the number of the line at fault, counted from 1.

Example:
    parse("[main]\nName = Acme  ; the client\nnote = first\n  second\n\n[empty]\n")
        == {"main": {"name": "Acme", "note": "first second"}, "empty": {}}
''',
        "files": {
            "ledger/ini.py": r'''
"""INI settings: [section] headers and key = value lines, with comments and continued values."""
import re

_INLINE = re.compile(r"[ \t][#;]")
_HEADER = re.compile(r"\[([^\[\]]*)\]")


def _uncomment(s):
    """s without its inline comment: from a "#" or ";" right after a space or tab, to the end."""
    m = _INLINE.search(s)
    return s[:m.start()] if m else s


def parse(text):
    """{section: {key: value}} from INI text, sections and keys in the order they first appear. A line that is
    none of blank, comment, continuation, [section] or key = value raises ValueError naming it as "line <n>"."""
    sections, section, key, continuing = {}, None, None, False
    for n, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continuing = False
        elif stripped[0] in "#;":
            pass
        elif continuing and line[0] in " \t":
            more = _uncomment(line).strip()
            section[key] = f"{section[key]} {more}" if section[key] else more
        elif stripped.startswith("["):
            continuing = False
            m = _HEADER.fullmatch(_uncomment(stripped).strip())
            name = m.group(1).strip() if m else ""
            if not name:
                raise ValueError(f"line {n}: a section header must be [name]: {line!r}")
            if name in sections:
                raise ValueError(f"line {n}: the section {name!r} appears twice")
            section = sections[name] = {}
        elif "=" in stripped:
            raw_key, _, value = stripped.partition("=")
            key = raw_key.strip().lower()
            if not key:
                raise ValueError(f"line {n}: a key line needs a key before its '='")
            if section is None:
                raise ValueError(f"line {n}: a key line before any [section]")
            section[key] = _uncomment(value).strip()
            continuing = True
        else:
            raise ValueError(f"line {n}: not a [section], a key = value line or a comment: {line!r}")
    return sections
''',
            "tests/test_ini.py": r'''
import unittest

from ledger.ini import parse


class ParseTest(unittest.TestCase):
    def test_sections_and_keys_in_order(self):
        result = parse("[main]\nname = Acme\ncity=Berlin\n[billing]\nterms = 30 days\n")
        self.assertEqual(result, {"main": {"name": "Acme", "city": "Berlin"}, "billing": {"terms": "30 days"}})
        self.assertEqual(list(result), ["main", "billing"])
        self.assertEqual(list(result["main"]), ["name", "city"])

    def test_the_spec_example(self):
        self.assertEqual(parse("[main]\nName = Acme  ; the client\nnote = first\n  second\n\n[empty]\n"),
                         {"main": {"name": "Acme", "note": "first second"}, "empty": {}})

    def test_no_sections(self):
        self.assertEqual(parse(""), {})
        self.assertEqual(parse("\n  \n# only a comment\n"), {})

    def test_keys_are_stripped_and_lowercased_values_stripped(self):
        self.assertEqual(parse("[s]\n  Full Name  =  Ann Lee  \n"), {"s": {"full name": "Ann Lee"}})

    def test_a_value_runs_from_the_first_equals_sign(self):
        self.assertEqual(parse("[s]\nurl = a=b=c\n"), {"s": {"url": "a=b=c"}})

    def test_a_value_may_be_empty(self):
        self.assertEqual(parse("[s]\nk =\nj=  \n"), {"s": {"k": "", "j": ""}})

    def test_section_names_are_stripped_and_case_sensitive(self):
        self.assertEqual(parse("[ Main ]\na=1\n[main]\na=2\n"), {"Main": {"a": "1"}, "main": {"a": "2"}})

    def test_a_section_without_keys_is_kept(self):
        self.assertEqual(parse("[a]\n[b]\nx=1\n"), {"a": {}, "b": {"x": "1"}})

    def test_comment_lines(self):
        self.assertEqual(parse("# top\n[s]\n; note\n  # indented\nk = v\n"), {"s": {"k": "v"}})

    def test_inline_comments_need_a_space_or_tab_before_them(self):
        text = "[s] # the section\na = x # note\nb = y\t; note\nc = x#y;z\nd = #y\ne=#y\n"
        self.assertEqual(parse(text), {"s": {"a": "x", "b": "y", "c": "x#y;z", "d": "", "e": "#y"}})

    def test_continuation_lines_join_with_one_space(self):
        self.assertEqual(parse("[s]\nk = first\n  second\n\tthird ; note\n"), {"s": {"k": "first second third"}})

    def test_a_continuation_of_an_empty_value_becomes_the_value(self):
        self.assertEqual(parse("[s]\nk =\n   alone\n"), {"s": {"k": "alone"}})

    def test_comments_do_not_end_a_value_but_blank_lines_do(self):
        self.assertEqual(parse("[s]\nk = a\n# note\n  b\n\n  j = c\n"), {"s": {"k": "a b", "j": "c"}})

    def test_while_continuing_an_indented_key_line_is_a_continuation(self):
        self.assertEqual(parse("[s]\nk = a\n  j = b\n"), {"s": {"k": "a j = b"}})

    def test_an_indented_line_with_nothing_to_continue_is_read_as_usual(self):
        self.assertEqual(parse("  [s]\n  k = v\n\n  [t]\n"), {"s": {"k": "v"}, "t": {}})

    def test_a_repeated_key_replaces_the_value_and_keeps_its_place(self):
        result = parse("[s]\na = 1\nb = 2\nA = 3\n")
        self.assertEqual(result, {"s": {"a": "3", "b": "2"}})
        self.assertEqual(list(result["s"]), ["a", "b"])

    def test_windows_line_endings(self):
        self.assertEqual(parse("[s]\r\nk = v\r\n  w\r\n"), {"s": {"k": "v w"}})

    def test_errors_name_the_line(self):
        cases = [
            ("k = v\n", 1),  # a key line before any section
            ("[s]\na = 1\n[s]\n", 3),  # a section twice
            ("[s]\n= v\n", 2),  # an empty key
            ("[s]\njust words\n", 2),  # no "=", not a header or a comment
            ("\n[]\n", 2),  # an empty name
            ("[s]\n[ ]\n", 2),  # a name that is empty once stripped
            ("[s]\n[a]b\n", 2),  # text after the header
            ("[s]\n[a] b\n", 2),  # text after the header that isn't a comment
            ("[s]\n[a\n", 2),  # no closing bracket
            ("[s]\n[a]]\n", 2),  # a bracket in the name
        ]
        for text, line in cases:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, rf"line {line}\b"):
                parse(text)


if __name__ == "__main__":
    unittest.main()
''',
        },
        "naive": {
            "what": "configparser with inline comments",
            "fails": "test_ini",
            "files": {"ledger/ini.py": r'''
"""INI settings."""
import configparser


def parse(text):
    """{section: {key: value}} from INI text."""
    parser = configparser.ConfigParser(inline_comment_prefixes=("#", ";"), interpolation=None)
    parser.read_string(text)
    return {name: dict(parser[name]) for name in parser.sections()}
'''},
        },
    },
    {
        "name": "prices",
        "message": r'''
Typed invoice lines take prices the way people write them: 1,234.50, 12.5, €12

ledger.invoice.parse_line(entry, tax_rate="0") keeps its format, "<quantity> x <description> @ <price>",
and everything else about it; only the prices it accepts change. A price is now, in this order:

- optionally one currency sign, "€", "$" or "£", directly before the number;
- a whole part: either ASCII digits alone ("1234"), or 1 to 3 digits followed by one or more groups
  of a "," and exactly 3 digits ("1,234", "12,345,678");
- optionally a "." followed by one or two digits ("12.5" is 12.50, "12.05" is 12.05).

Nothing else is allowed: no sign, no space inside the price, no "." without a digit after it, no
other grouping ("12,34", "1,2345", ",123"), no more than two decimals, no second currency sign and
none after the number. Such a price raises ValueError, like any other malformed line.

Examples:
    parse_line("2 x Desk @ 1,234.50").unit_price == 123450
    parse_line("1 x Tea @ €3.5").unit_price == 350
    parse_line("1 x Pen @ $2").unit_price == 200

Keep: money.parse_amount is unchanged and stays exact ("12.5" and "1,234.50" still raise
ValueError), and so is importer.read_rows: a bank file's amounts must be exact, so it still rejects
every amount it rejects today.
''',
        "files": {
            "ledger/invoice.py": [(r'''_TYPED = re.compile(r"([0-9]+) x (.+) @ (\S+)")


def parse_line(entry, tax_rate="0"):
    """A Line from text typed as "<quantity> x <description> @ <unit price>", such as "3 x Widget @ 2.50": the
    price is read by money.parse_amount, leading and trailing whitespace is ignored, anything else raises
    ValueError."""
    m = _TYPED.fullmatch(entry.strip())
    if not m:
        raise ValueError(f"not an invoice line: {entry!r}")
    quantity, description, price = m.groups()
    return Line(description, int(quantity), money.parse_amount(price), tax_rate)''',
                                   r'''_TYPED = re.compile(r"([0-9]+) x (.+) @ (\S+)")
_PRICE = re.compile(r"[€$£]?([0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?:\.([0-9]{1,2}))?")


def _price(text):
    """The cents in a typed price: an optional €, $ or £, digits with optional "," thousands groups, and an
    optional "." with one or two digits ("€1,234.5" is 123450). Anything else raises ValueError."""
    m = _PRICE.fullmatch(text)
    if not m:
        raise ValueError(f"not a price: {text!r}")
    whole, frac = m.groups()
    return int(whole.replace(",", "")) * 100 + int((frac or "0").ljust(2, "0"))


def parse_line(entry, tax_rate="0"):
    """A Line from text typed as "<quantity> x <description> @ <unit price>", such as "3 x Widget @ 2.50": the
    price is read by _price ("1,234.50", "12.5", "€12"), leading and trailing whitespace is ignored, anything
    else raises ValueError."""
    m = _TYPED.fullmatch(entry.strip())
    if not m:
        raise ValueError(f"not an invoice line: {entry!r}")
    quantity, description, price = m.groups()
    return Line(description, int(quantity), _price(price), tax_rate)''')],
            "tests/test_invoice.py": [(r'''    def test_a_malformed_line_raises_value_error(self):
        for entry in ["x Widget @ 2.50", "3 Widget @ 2.50", "3 x Widget", "3 x  @ 2.50", "3 x Widget @ 2.5",
                      "3 x Widget @ 1,500.00"]:
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                parse_line(entry)
''', r'''    def test_a_malformed_line_raises_value_error(self):
        for entry in ["x Widget @ 2.50", "3 Widget @ 2.50", "3 x Widget", "3 x  @ 2.50", "3 x Widget @ 2.50 each"]:
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                parse_line(entry)

    def test_prices_as_people_type_them(self):
        cases = {"1,234.50": 123450, "12,345,678": 1234567800, "1234": 123400, "12.5": 1250, "12.05": 1205,
                 "0.5": 50, "€3.5": 350, "$2": 200, "£1,000": 100000, "€0": 0}
        for price, cents in cases.items():
            with self.subTest(price=price):
                self.assertEqual(parse_line(f"2 x Desk @ {price}").unit_price, cents)

    def test_the_rest_of_the_line_is_read_as_before(self):
        self.assertEqual(parse_line("  2 x Desk, oak @ €1,234.50 ", "19"), Line("Desk, oak", 2, 123450, "19"))

    def test_a_malformed_price_raises_value_error(self):
        for price in ["12,34", "1,2345", ",123", "1,234,", "1,,234", "12.", ".5", "12.345", "-5", "+5", "€€5",
                      "5€", "€-5", "1_000", "12a", "US$5", "1.234,50",
                      "\N{FULLWIDTH DIGIT ONE}\N{FULLWIDTH DIGIT TWO}"]:
            with self.subTest(price=price), self.assertRaises(ValueError):
                parse_line(f"2 x Desk @ {price}")
''')],
        },
        "naive": {
            "what": "money.parse_amount itself takes the new prices",
            "fails": "test_importer",
            "files": {"ledger/money.py": [
                (r'''_AMOUNT = re.compile(r"(-?)([0-9]+)(?:\.([0-9]{2}))?")''',
                 r'''_AMOUNT = re.compile(r"(-?)[€$£]?([0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?:\.([0-9]{1,2}))?")'''),
                ('''    cents = int(whole) * 100 + int(frac or 0)''',
                 '''    cents = int(whole.replace(",", "")) * 100 + int((frac or "0").ljust(2, "0"))'''),
            ]},
        },
    },
    {
        "name": "interval",
        "message": r'''
Add ledger.interval.Interval: exact interval arithmetic for estimates

Add the module ledger/interval.py with the class Interval: a closed range [lo, hi] of exact numbers,
whose arithmetic gives a range holding every result of the operation on members of its operands.

Construction:
- Interval(lo, hi=None): hi defaults to lo (a single point). Each bound must be an int or a
  fractions.Fraction; anything else (a float, a str, None, ...) raises TypeError. lo > hi raises
  ValueError.
- The attributes lo and hi hold the bounds as given, except that a Fraction whose denominator is 1
  is stored as an int: Interval(Fraction(4, 2)).lo is the int 2. This holds for every result below.

In every binary operation below, an int or a Fraction operand counts as the single point [x, x] and
may stand on either side (2 + i, i * Fraction(1, 2), 1 / i, 4 & i). An operand of any other type
raises TypeError.

Arithmetic, for intervals a and b:
- a + b is [a.lo + b.lo, a.hi + b.hi]; a - b is [a.lo - b.hi, a.hi - b.lo]; -a is [-a.hi, -a.lo].
- a * b is [the least, the greatest] of the four products a.lo*b.lo, a.lo*b.hi, a.hi*b.lo, a.hi*b.hi.
- a / b raises ZeroDivisionError when b holds 0 (b.lo <= 0 <= b.hi). Otherwise it is
  a * [1/b.hi, 1/b.lo], with the reciprocals as exact Fractions.
- a ** n, for an int n >= 0: [1, 1] when n is 0; [a.lo**n, a.hi**n] when n is odd. When n is even
  and positive: [a.lo**n, a.hi**n] if a.lo >= 0, [a.hi**n, a.lo**n] if a.hi <= 0, and
  [0, max(a.lo**n, a.hi**n)] if a.lo < 0 < a.hi. A negative int n raises ValueError; an n that
  isn't an int raises TypeError.

Sets and the rest:
- a & b is their intersection, an Interval, or None when they share no number. Intervals that touch
  share one: Interval(1, 2) & Interval(2, 3) == Interval(2).
- a | b is the smallest Interval holding both: Interval(1, 2) | Interval(5, 6) == Interval(1, 6).
- x in a: for an int or a Fraction x, a.lo <= x <= a.hi; for an Interval x, whether x lies entirely
  inside a. Any other x raises TypeError.
- a.width is a.hi - a.lo.
- a == b is True when b is an Interval with the same bounds: Interval(1, 2) == Interval(Fraction(2, 2), 2).
  An Interval never equals anything else (Interval(3) == 3 is False). Equal intervals have equal
  hashes.
- repr(a) is "Interval(<repr of lo>, <repr of hi>)": repr(Interval(Fraction(1, 2), 3)) is
  "Interval(Fraction(1, 2), 3)" and repr(Interval(5)) is "Interval(5, 5)".
''',
        "files": {
            "ledger/interval.py": r'''
"""Exact interval arithmetic: closed ranges [lo, hi] of ints and Fractions."""
from fractions import Fraction

_EXACT = (int, Fraction)


def _bound(x):
    if not isinstance(x, _EXACT):
        raise TypeError(f"an Interval bound must be an int or a Fraction, not {type(x).__name__}")
    return int(x) if isinstance(x, Fraction) and x.denominator == 1 else x


def _point(x):
    """x as an Interval (an int or a Fraction as a single point), or None for any other type."""
    if isinstance(x, Interval):
        return x
    return Interval(x) if isinstance(x, _EXACT) else None


class Interval:
    """[lo, hi]: every operation gives a range holding each result of it on members of its operands."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        lo = _bound(lo)
        hi = lo if hi is None else _bound(hi)
        if lo > hi:
            raise ValueError(f"lo {lo} is above hi {hi}")
        self.lo, self.hi = lo, hi

    def __repr__(self):
        return f"Interval({self.lo!r}, {self.hi!r})"

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return NotImplemented
        return (self.lo, self.hi) == (other.lo, other.hi)

    def __hash__(self):
        return hash((self.lo, self.hi))

    @property
    def width(self):
        return self.hi - self.lo

    def __add__(self, other):
        o = _point(other)
        return NotImplemented if o is None else Interval(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __sub__(self, other):
        o = _point(other)
        return NotImplemented if o is None else Interval(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, other):
        o = _point(other)
        return NotImplemented if o is None else o - self

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __mul__(self, other):
        o = _point(other)
        if o is None:
            return NotImplemented
        products = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = _point(other)
        if o is None:
            return NotImplemented
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError(f"division by {o!r}, which holds 0")
        return self * Interval(Fraction(1) / o.hi, Fraction(1) / o.lo)

    def __rtruediv__(self, other):
        o = _point(other)
        return NotImplemented if o is None else o / self

    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError(f"an Interval's power must be an int, not {type(n).__name__}")
        if n < 0:
            raise ValueError(f"an Interval's power must be at least 0, got {n}")
        if n == 0:
            return Interval(1)
        a, b = self.lo ** n, self.hi ** n
        if n % 2 or self.lo >= 0:
            return Interval(a, b)
        if self.hi <= 0:
            return Interval(b, a)
        return Interval(0, max(a, b))

    def __and__(self, other):
        o = _point(other)
        if o is None:
            return NotImplemented
        lo, hi = max(self.lo, o.lo), min(self.hi, o.hi)
        return Interval(lo, hi) if lo <= hi else None

    __rand__ = __and__

    def __or__(self, other):
        o = _point(other)
        return NotImplemented if o is None else Interval(min(self.lo, o.lo), max(self.hi, o.hi))

    __ror__ = __or__

    def __contains__(self, x):
        if isinstance(x, Interval):
            return self.lo <= x.lo and x.hi <= self.hi
        if isinstance(x, _EXACT):
            return self.lo <= x <= self.hi
        raise TypeError(f"an Interval holds ints, Fractions and Intervals, not {type(x).__name__}")
''',
            "tests/test_interval.py": r'''
import unittest
from fractions import Fraction

from ledger.interval import Interval


class ConstructionTest(unittest.TestCase):
    def test_bounds(self):
        self.assertEqual((Interval(1, 3).lo, Interval(1, 3).hi), (1, 3))
        self.assertEqual((Interval(5).lo, Interval(5).hi), (5, 5))
        self.assertEqual(Interval(Fraction(1, 2), 1).lo, Fraction(1, 2))

    def test_a_whole_fraction_is_stored_as_an_int(self):
        i = Interval(Fraction(4, 2), Fraction(9, 3))
        self.assertEqual((i.lo, i.hi), (2, 3))
        self.assertIs(type(i.lo), int)
        self.assertIs(type(i.hi), int)

    def test_lo_above_hi_raises_value_error(self):
        with self.assertRaises(ValueError):
            Interval(2, 1)

    def test_other_bound_types_raise_type_error(self):
        for args in [(1.5,), (1, 2.0), ("1", 2), (None,)]:
            with self.subTest(args=args), self.assertRaises(TypeError):
                Interval(*args)


class EqualityTest(unittest.TestCase):
    def test_equal_bounds_are_equal(self):
        self.assertEqual(Interval(1, 2), Interval(Fraction(2, 2), 2))
        self.assertNotEqual(Interval(1, 2), Interval(1, 3))
        self.assertEqual(hash(Interval(1, 2)), hash(Interval(Fraction(1), 2)))

    def test_never_equal_to_anything_else(self):
        self.assertFalse(Interval(3) == 3)
        self.assertNotEqual(Interval(1, 2), (1, 2))

    def test_repr(self):
        self.assertEqual(repr(Interval(1, 2)), "Interval(1, 2)")
        self.assertEqual(repr(Interval(Fraction(1, 2), 3)), "Interval(Fraction(1, 2), 3)")
        self.assertEqual(repr(Interval(-4)), "Interval(-4, -4)")


class ArithmeticTest(unittest.TestCase):
    def test_add_subtract_negate(self):
        self.assertEqual(Interval(1, 2) + Interval(10, 20), Interval(11, 22))
        self.assertEqual(Interval(1, 2) - Interval(10, 20), Interval(-19, -8))
        self.assertEqual(-Interval(1, 2), Interval(-2, -1))

    def test_numbers_are_single_points_on_either_side(self):
        self.assertEqual(Interval(1, 2) + 3, Interval(4, 5))
        self.assertEqual(3 + Interval(1, 2), Interval(4, 5))
        self.assertEqual(10 - Interval(1, 2), Interval(8, 9))
        self.assertEqual(Interval(1, 2) - Fraction(1, 2), Interval(Fraction(1, 2), Fraction(3, 2)))
        self.assertEqual(2 * Interval(-1, 3), Interval(-2, 6))
        self.assertEqual(Interval(-1, 3) * -2, Interval(-6, 2))

    def test_multiply_takes_the_least_and_greatest_of_the_four_products(self):
        self.assertEqual(Interval(2, 3) * Interval(4, 5), Interval(8, 15))
        self.assertEqual(Interval(-2, 3) * Interval(-1, 4), Interval(-8, 12))
        self.assertEqual(Interval(-3, -2) * Interval(1, 2), Interval(-6, -2))
        self.assertEqual(Interval(-3, -2) * Interval(-5, -4), Interval(8, 15))
        self.assertEqual(Interval(-1, 1) * Interval(-1, 1), Interval(-1, 1))

    def test_divide(self):
        self.assertEqual(Interval(1, 2) / Interval(4, 8), Interval(Fraction(1, 8), Fraction(1, 2)))
        self.assertEqual(Interval(-2, 4) / Interval(-2, -1), Interval(-4, 2))
        self.assertEqual(Interval(1, 3) / 2, Interval(Fraction(1, 2), Fraction(3, 2)))
        self.assertEqual(1 / Interval(2, 4), Interval(Fraction(1, 4), Fraction(1, 2)))
        self.assertIs(type((Interval(2, 4) / 2).lo), int)

    def test_dividing_by_an_interval_holding_zero_raises_zero_division_error(self):
        for divisor in [Interval(-1, 1), Interval(0, 2), Interval(-3, 0), 0]:
            with self.subTest(divisor=divisor), self.assertRaises(ZeroDivisionError):
                Interval(1, 2) / divisor
        with self.assertRaises(ZeroDivisionError):
            1 / Interval(-1, 1)

    def test_power(self):
        cases = [
            (Interval(-2, 3), 0, Interval(1)),
            (Interval(-2, 3), 1, Interval(-2, 3)),
            (Interval(-2, 3), 2, Interval(0, 9)),
            (Interval(-3, 2), 2, Interval(0, 9)),
            (Interval(-3, -2), 2, Interval(4, 9)),
            (Interval(2, 3), 2, Interval(4, 9)),
            (Interval(0, 2), 2, Interval(0, 4)),
            (Interval(-2, 3), 3, Interval(-8, 27)),
            (Interval(-3, -2), 3, Interval(-27, -8)),
            (Interval(Fraction(-1, 2), 1), 2, Interval(0, 1)),
        ]
        for base, n, result in cases:
            with self.subTest(base=base, n=n):
                self.assertEqual(base ** n, result)

    def test_a_negative_or_non_int_power_raises(self):
        with self.assertRaises(ValueError):
            Interval(1, 2) ** -1
        for n in [Fraction(1, 2), 2.0]:
            with self.subTest(n=n), self.assertRaises(TypeError):
                Interval(1, 2) ** n

    def test_other_operand_types_raise_type_error(self):
        operations = [lambda: Interval(1) + 1.5, lambda: 1.5 * Interval(1), lambda: Interval(1) - "1",
                      lambda: Interval(1) / 2.0, lambda: Interval(1) & 1.0, lambda: Interval(1) | None]
        for i, operation in enumerate(operations):
            with self.subTest(operation=i), self.assertRaises(TypeError):
                operation()


class SetTest(unittest.TestCase):
    def test_intersection(self):
        self.assertEqual(Interval(1, 5) & Interval(3, 8), Interval(3, 5))
        self.assertEqual(Interval(1, 2) & Interval(2, 3), Interval(2))
        self.assertIsNone(Interval(1, 2) & Interval(3, 4))
        self.assertEqual(Interval(1, 5) & 4, Interval(4))
        self.assertIsNone(4 & Interval(5, 6))

    def test_hull(self):
        self.assertEqual(Interval(1, 2) | Interval(5, 6), Interval(1, 6))
        self.assertEqual(Interval(1, 5) | Interval(2, 3), Interval(1, 5))
        self.assertEqual(0 | Interval(5, 6), Interval(0, 6))

    def test_contains(self):
        i = Interval(1, 3)
        for x in [1, 3, Fraction(5, 2), Interval(1, 2), Interval(3)]:
            with self.subTest(x=x):
                self.assertIn(x, i)
        for x in [0, Fraction(7, 2), Interval(2, 4)]:
            with self.subTest(x=x):
                self.assertNotIn(x, i)
        with self.assertRaises(TypeError):
            1.5 in i

    def test_width(self):
        self.assertEqual(Interval(1, 3).width, 2)
        self.assertEqual(Interval(Fraction(1, 2), 2).width, Fraction(3, 2))
        self.assertEqual(Interval(7).width, 0)


if __name__ == "__main__":
    unittest.main()
''',
        },
        "naive": {
            "what": "multiply bound by bound and raise each bound to n",
            "fails": "test_interval",
            "files": {"ledger/interval.py": [
                ('''        products = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Interval(min(products), max(products))''',
                 '''        return Interval(self.lo * o.lo, self.hi * o.hi)'''),
                ('''        a, b = self.lo ** n, self.hi ** n
        if n % 2 or self.lo >= 0:
            return Interval(a, b)
        if self.hi <= 0:
            return Interval(b, a)
        return Interval(0, max(a, b))''',
                 '''        return Interval(self.lo ** n, self.hi ** n)'''),
            ]},
        },
    },
    {
        "name": "taxround",
        "message": r'''
Round tax half to even, line by line, as the tax office requires

ledger.invoice.line_tax(line) still taxes the line's net amount, line_net(line), at line.tax_rate
percent, but now rounds the exact result to whole cents with halves going to the even cent
("banker's rounding"): 142.5 -> 142, 143.5 -> 144, 0.5 -> 0, 1.5 -> 2, -142.5 -> -142. A result
that isn't exactly half a cent rounds to the nearest cent as before (74.925 -> 75). invoice.totals
and invoice.render take the tax from line_tax, so their tax and total figures follow.

Keep: discounts still round halves away from zero, so line_net is unchanged (a 5% discount on 0.50
is 0.03, leaving 0.47), and money.percent keeps giving the same results: other code relies on its
rounding.
''',
        "files": {
            "ledger/money.py": [('''def percent(cents, rate):
    """rate percent of cents (rate an int or a decimal string such as "7.5"), rounded to whole cents with halves
    away from zero: percent(250, 1) is 3, percent(-250, 1) is -3."""
    exact = Decimal(cents) * Decimal(rate) / 100
    return int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP))''', '''def percent(cents, rate, rounding=ROUND_HALF_UP):
    """rate percent of cents (rate an int or a decimal string such as "7.5"), rounded to whole cents with halves
    away from zero: percent(250, 1) is 3, percent(-250, 1) is -3. rounding is another decimal rounding mode."""
    exact = Decimal(cents) * Decimal(rate) / 100
    return int(exact.quantize(Decimal(1), rounding=rounding))''')],
            "ledger/invoice.py": [
                ("import datetime\nimport re\n", "import datetime\nimport decimal\nimport re\n"),
                ('''def line_tax(line):
    """The tax on the line's net amount: money.percent(line_net(line), line.tax_rate)."""
    return money.percent(line_net(line), line.tax_rate)''', '''def line_tax(line):
    """The tax on the line's net amount, tax_rate percent of it, rounded to whole cents with halves to the even
    cent: 142.5 is 142, 143.5 is 144."""
    return money.percent(line_net(line), line.tax_rate, decimal.ROUND_HALF_EVEN)'''),
            ],
            "tests/test_invoice.py": [
                ('''    def test_line_tax(self):
        self.assertEqual(line_tax(Line("Widget", 3, 250, "19")), 143)
        self.assertEqual(line_tax(Line("Lamp", 1, 999, "7.5")), 75)
''', '''    def test_line_tax_rounds_halves_to_the_even_cent(self):
        cases = [(Line("Widget", 3, 250, "19"), 142), (Line("A", 1, 1850, "19"), 352), (Line("B", 1, 10, "5"), 0),
                 (Line("C", 1, 30, "5"), 2), (Line("Refund", 1, -750, "19"), -142), (Line("D", 1, -30, "5"), -2)]
        for line, tax in cases:
            with self.subTest(line=line):
                self.assertEqual(line_tax(line), tax)

    def test_line_tax_rounds_other_results_to_the_nearest_cent(self):
        self.assertEqual(line_tax(Line("Lamp", 1, 999, "7.5")), 75)
        self.assertEqual(line_tax(Line("Lamp", 1, 997, "7.5")), 75)
        self.assertEqual(line_tax(Line("Lamp", 1, 1001, "7.5")), 75)
        self.assertEqual(line_tax(Line("Lamp", 1, 1007, "7.5")), 76)

    def test_line_tax_is_on_the_net_after_the_discount(self):
        self.assertEqual(line_tax(Line("Pen", 10, 50, "19", "5")), 90)
        self.assertEqual(line_tax(Line("Pen", 1, 50, "10", "5")), 5)
'''),
                ("(1620750, 307943, 1928693)", "(1620750, 307942, 1928692)"),
                ('''            "Tax                                                  3,079.43",
            "Total                                               19,286.93",''',
                 '''            "Tax                                                  3,079.42",
            "Total                                               19,286.92",'''),
            ],
        },
        "naive": {
            "what": "money.percent rounds half to even",
            "fails": "test_money",
            "files": {"ledger/money.py": [
                ("from decimal import ROUND_HALF_UP, Decimal", "from decimal import ROUND_HALF_EVEN, Decimal"),
                ("rounding=ROUND_HALF_UP))", "rounding=ROUND_HALF_EVEN))"),
            ]},
        },
    },
    {
        "name": "lexer",
        "message": r'''
Add ledger.lexer.tokenize: split a formula into tokens

Add the module ledger/lexer.py with a named tuple and one function:

    Token = collections.namedtuple("Token", "kind value pos")
    tokenize(text: str) -> list[Token]

tokenize reads text from left to right and returns its tokens in order. pos is the 0-based index in
text of the token's first character. The kinds:

- "number": one or more ASCII digits, optionally followed by "." and one or more ASCII digits. value
  is the number's text as written ("007", "1.50"). A "-" before a number is an operator, not part of
  the number.
- "name": an ASCII letter or "_", followed by any number of ASCII letters, ASCII digits and "_".
  value is the name's text.
- "string": text between single quotes or between double quotes, ending at the next quote of the
  same kind that isn't escaped. A backslash starts an escape: \\ stands for a backslash, \' for a
  single quote, \" for a double quote, \n for a newline and \t for a tab. value is the text between
  the quotes with each escape replaced; the other kind of quote needs no escape ("it's" holds it's).
- "op": the longest of these that matches at the position:
      **  //  ==  !=  <=  >=  +  -  *  /  %  <  >  (  )  ,  =
  so "a**b" gives a, **, b and "<==" gives <=, =. value is the operator's text.

Between tokens, space, tab, "\n" and "\r" are skipped; empty or skip-only text gives [].

tokenize raises ValueError, its message containing "position N" with N the 0-based index where the
token that can't be read starts, for:
- a number directly followed by an ASCII letter, "_" or "." ("12abc", "1.2.3", "1.", "3_000"):
  N is the number's first digit;
- a string with no closing quote before a "\n" or the end of text ("\r" is ordinary text in a
  string), or with a backslash followed by anything but \ ' " n t (or by nothing): N is its opening
  quote;
- any other character where a token would start ("!" alone, "$", ".", "é", a non-breaking space):
  N is that character.

Example:
    tokenize("price * qty - 1.50") == [Token("name", "price", 0), Token("op", "*", 6),
        Token("name", "qty", 8), Token("op", "-", 12), Token("number", "1.50", 14)]
''',
        "files": {
            "ledger/lexer.py": r'''
"""Formula text to tokens: numbers, names, strings and operators."""
import collections
import string

Token = collections.namedtuple("Token", "kind value pos")

_OPS = sorted("** // == != <= >= + - * / % < > ( ) , =".split(), key=len, reverse=True)
_SKIP = " \t\n\r"
_DIGITS = string.digits
_START = string.ascii_letters + "_"
_ESCAPES = {"\\": "\\", "'": "'", '"': '"', "n": "\n", "t": "\t"}


def tokenize(text):
    """The tokens of text, left to right; ValueError naming the position of the first one that can't be read."""
    tokens, i, n = [], 0, len(text)
    while i < n:
        ch, start = text[i], i
        if ch in _SKIP:
            i += 1
        elif ch in _DIGITS:
            while i < n and text[i] in _DIGITS:
                i += 1
            if i + 1 < n and text[i] == "." and text[i + 1] in _DIGITS:
                i += 1
                while i < n and text[i] in _DIGITS:
                    i += 1
            if i < n and (text[i] in _START or text[i] == "."):
                raise ValueError(f"a malformed number at position {start}")
            tokens.append(Token("number", text[start:i], start))
        elif ch in _START:
            while i < n and (text[i] in _START or text[i] in _DIGITS):
                i += 1
            tokens.append(Token("name", text[start:i], start))
        elif ch in "'\"":
            chars, i = [], i + 1
            while True:
                if i >= n or text[i] == "\n":
                    raise ValueError(f"a string without its closing quote at position {start}")
                if text[i] == ch:
                    i += 1
                    break
                if text[i] == "\\":
                    if i + 1 >= n or text[i + 1] not in _ESCAPES:
                        raise ValueError(f"a string with a bad escape at position {start}")
                    chars.append(_ESCAPES[text[i + 1]])
                    i += 2
                else:
                    chars.append(text[i])
                    i += 1
            tokens.append(Token("string", "".join(chars), start))
        else:
            op = next((o for o in _OPS if text.startswith(o, i)), None)
            if op is None:
                raise ValueError(f"an unexpected character {ch!r} at position {i}")
            tokens.append(Token("op", op, i))
            i += len(op)
    return tokens
''',
            "tests/test_lexer.py": r'''
import unittest

from ledger.lexer import Token, tokenize


def kinds_values(text):
    return [(t.kind, t.value) for t in tokenize(text)]


class TokenTest(unittest.TestCase):
    def test_a_named_tuple(self):
        t = Token("name", "x", 0)
        self.assertEqual((t.kind, t.value, t.pos), ("name", "x", 0))
        self.assertEqual(t, ("name", "x", 0))


class TokenizeTest(unittest.TestCase):
    def test_a_formula(self):
        self.assertEqual(tokenize("price * qty - 1.50"), [
            Token("name", "price", 0), Token("op", "*", 6), Token("name", "qty", 8),
            Token("op", "-", 12), Token("number", "1.50", 14)])

    def test_nothing_to_read(self):
        self.assertEqual(tokenize(""), [])
        self.assertEqual(tokenize(" \t\r\n "), [])

    def test_numbers_keep_their_text(self):
        self.assertEqual(kinds_values("007 3.14 10"), [("number", "007"), ("number", "3.14"), ("number", "10")])

    def test_a_minus_sign_is_an_operator(self):
        self.assertEqual(kinds_values("-1"), [("op", "-"), ("number", "1")])

    def test_names(self):
        self.assertEqual(kinds_values("_a1 B_2 x"), [("name", "_a1"), ("name", "B_2"), ("name", "x")])
        self.assertEqual(kinds_values("2*x"), [("number", "2"), ("op", "*"), ("name", "x")])

    def test_operators_take_the_longest_match(self):
        self.assertEqual(kinds_values("a**b"), [("name", "a"), ("op", "**"), ("name", "b")])
        self.assertEqual([t.value for t in tokenize("<== ***//>=!=")], ["<=", "=", "**", "*", "//", ">=", "!="])
        self.assertEqual([t.value for t in tokenize("+-*/%<>(),=")], list("+-*/%<>(),="))
        self.assertEqual([t.value for t in tokenize("=>")], ["=", ">"])

    def test_positions(self):
        self.assertEqual([t.pos for t in tokenize("  ab\t<= 'x y'\n42")], [2, 5, 8, 14])

    def test_strings(self):
        self.assertEqual(kinds_values("'abc' \"d e\""), [("string", "abc"), ("string", "d e")])
        self.assertEqual(kinds_values("''"), [("string", "")])
        self.assertEqual(kinds_values("\"it's\" 'say \"hi\"'"), [("string", "it's"), ("string", 'say "hi"')])
        self.assertEqual(kinds_values("'a\rb'"), [("string", "a\rb")])

    def test_string_escapes(self):
        self.assertEqual(tokenize(r"'a\'b\\c\nd\te\"f'")[0].value, "a'b\\c\nd\te\"f")
        self.assertEqual(tokenize(r'"\""')[0].value, '"')


class ErrorTest(unittest.TestCase):
    def assertFailsAt(self, text, pos):
        with self.subTest(text=text), self.assertRaisesRegex(ValueError, rf"position {pos}\b"):
            tokenize(text)

    def test_unexpected_characters(self):
        for text, pos in [("a ! b", 2), ("$5", 0), ("x.y", 1), (".5", 0), ("café", 3), ("a1.5", 2),
                          ("a\N{NO-BREAK SPACE}b", 1), ("1 ; 2", 2), ("a & b", 2), ("\N{ARABIC-INDIC DIGIT ONE}", 0)]:
            self.assertFailsAt(text, pos)

    def test_a_number_run_into_a_letter_underscore_or_dot(self):
        for text, pos in [("12abc", 0), ("x + 1.2.3", 4), ("1.", 0), ("3_000", 0), ("7 1e3", 2), ("1.5x", 0)]:
            self.assertFailsAt(text, pos)

    def test_bad_strings(self):
        for text, pos in [("'abc", 0), ("x = \"abc", 4), ("'a\nb'", 0), (r"'a\qb'", 0), ("'abc\\", 0),
                          ("\"a'", 0)]:
            self.assertFailsAt(text, pos)


if __name__ == "__main__":
    unittest.main()
''',
        },
        "naive": {
            "what": "one regex alternation through re.finditer",
            "fails": "test_lexer",
            "files": {"ledger/lexer.py": r'''
"""Formula text to tokens."""
import collections
import re

Token = collections.namedtuple("Token", "kind value pos")

_TOKEN = re.compile(r"""(?P<number>\d+(?:\.\d+)?)|(?P<name>[A-Za-z_]\w*)|(?P<string>'[^']*'|"[^"]*")"""
                    r"|(?P<op>\*\*|//|==|!=|<=|>=|[-+*/%<>(),=])")


def tokenize(text):
    """The tokens of text."""
    tokens = []
    for m in _TOKEN.finditer(text):
        value = m.group()
        tokens.append(Token(m.lastgroup, value[1:-1] if m.lastgroup == "string" else value, m.start()))
    return tokens
'''},
        },
    },
]
