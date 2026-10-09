"""fm instruments (T-0701): zero-token typed tools. Each answers a read, failure, log, data or trace question from a
small fixed fixture (real unittest, python and node runs; seeded logs and data) in a few capped lines that keep the
root cause, so the model reads that instead of the raw bytes."""
import argparse
import os
import re
import shutil
import sqlite3
import subprocess

from helpers import ForemanTestCase, read_text

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "instruments")
CAPS = {"sym": 40, "fail": 15, "logs": 40, "data": 40, "trace": 30}


class Case(ForemanTestCase):
    def with_repo(self):
        """The fixture project (shop, prices, a cart in JS) committed in the scratch repo under a task id."""
        shutil.copytree(os.path.join(FIX, "repo"), self.repo, dirs_exist_ok=True)
        for args in (["add", "-A"], ["commit", "-qm", "Shop, prices and cart (T-0042)"]):
            subprocess.run(["git", "-C", self.repo, *args], check=True, capture_output=True)

    def tool(self, name, *args, input=None):
        out = self.fm(name, *args, input=input).stdout
        self.assertLessEqual(len(out.splitlines()), CAPS[name], out)
        self.assertEqual(self.fm(name, *args, input=input).stdout, out, "stable output")
        return out


class Registry(Case):
    def test_lists_the_five_tools_with_schemas_and_caps(self):
        reg = self.fm_json("instruments")["instruments"]
        self.assertEqual([t["name"] for t in reg], list(CAPS))
        for t in reg:
            with self.subTest(tool=t["name"]):
                self.assertEqual(t["cap"], CAPS[t["name"]])
                self.assertTrue(t["summary"] and t["usage"].startswith(f"fm {t['name']}"))
                s = t["input_schema"]
                self.assertEqual((s["type"], s["additionalProperties"]), ("object", False))
                self.assertLessEqual(set(s["required"]), set(s["properties"]))
                for prop in s["properties"].values():
                    self.assertIn(prop["type"], ("string", "integer", "boolean"))
                    self.assertTrue(prop["description"])
        text = self.fm("instruments").stdout
        for name, cap in CAPS.items():
            self.assertRegex(text, rf"(?m)^  {name} .*≤{cap} lines")

    def test_each_schema_is_its_commands_arguments(self):
        import fmcli
        sub = next(a for a in fmcli.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
        for t in self.fm_json("instruments")["instruments"]:
            dests = {a.dest for a in sub.choices[t["name"]]._actions} - {"help", "json", "project"}
            self.assertEqual(dests, set(t["input_schema"]["properties"]), t["name"])


class Sym(Case):
    def setUp(self):
        super().setUp()
        self.with_repo()

    def test_a_method_and_its_one_hop_neighbourhood_never_the_whole_file(self):
        out = self.tool("sym", "shop.py:Cart.total")
        self.assertIn("shop.py:33-36", out)
        self.assertIn("return net + net * TAX_RATE * 100", out)  # the root cause: the rate is already a fraction
        for used in ("apply_discount", "shop.py:7", "TAX_RATE", "shop.py:4", "subtotal", "shop.py:30"):
            self.assertIn(used, out)
        self.assertRegex(out, r"checkout\.py:6 in checkout: .*cart\.total\(\)")  # its caller
        self.assertIn("callers (1):", out)  # not the mention in a string on checkout.py:13
        self.assertNotIn("report row", out)  # another function's body

    def test_other_languages_by_braces(self):
        out = self.tool("sym", "web/cart.js:cartTotal")
        self.assertIn("web/cart.js:9-12", out)
        self.assertIn("cart.tax.rate", out)
        self.assertIn("applyDiscount", out)
        self.assertIn("web/cart.js:1", out)
        self.assertRegex(out, r"web/cart\.js:17\b.*cartTotal\(")
        self.assertNotIn("require.main", out.split("callers")[0])  # the body ends at its closing brace

    def test_an_unknown_name_says_what_is_there(self):
        p = self.fm("sym", "shop.py:Cart.totl", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("Cart.total", p.stderr)


class Fail(Case):
    def setUp(self):
        super().setUp()
        self.with_repo()

    def test_a_real_unittest_failure_becomes_a_few_lines_with_the_right_source(self):
        out = self.tool("fail", input=read_text(os.path.join(FIX, "unittest_run.txt")))
        self.assertIn("tests.price_test.PriceTest.test_vat_on_standard", out.splitlines()[0])
        self.assertIn("KeyError: 'std'", out)
        self.assertRegex(out, r"(?m)^price\.py:6 in rate_for: return RATES\[kind\]")  # mapped from the CI path
        self.assertRegex(out, r"(?m)^price\.py:10 in with_vat")
        self.assertRegex(out, r"(?m)^  > +6 +return RATES\[kind\]")  # the deepest frame in the repo, in context
        self.assertIn("test_refund_of_a_refund", out)  # the other failure is named
        self.assertIn("FAILED (failures=1, errors=1)", out)
        self.assertNotIn("/home/runner", out)
        self.assertNotIn("catalogue item", out)

    def test_a_file_argument_reads_the_same(self):
        path = os.path.join(FIX, "unittest_run.txt")
        self.assertEqual(self.tool("fail", path), self.tool("fail", input=read_text(path)))


class Logs(Case):
    def test_a_log_becomes_templates_with_counts_errors_first(self):
        out = self.tool("logs", os.path.join(FIX, "bad.log"))
        self.assertRegex(out.splitlines()[0], r"240 lines → \d+ templates")
        self.assertLessEqual(len(out.splitlines()), 12)
        self.assertRegex(out, r"(?m)^ +3  ERROR db: connection refused to db-primary:5432 after <\*> retries")
        self.assertRegex(out, r"INFO http GET /api/items/<\*>")
        self.assertLess(out.index("connection refused"), out.index("INFO"))

    def test_whats_new_since_the_good_run(self):
        out = self.tool("logs", os.path.join(FIX, "bad.log"), "--since-good", os.path.join(FIX, "good.log"))
        rows = out.splitlines()[1:]
        new = [r for r in rows if r.startswith("new ")]
        self.assertTrue(new and "connection refused" in new[0], out)  # first seen of the new ones: the cause
        self.assertTrue(any("ERROR http POST /api/checkout" in r for r in new))
        self.assertFalse([r for r in rows if "GET" in r and r.startswith("new ")])
        self.assertEqual(rows[:len(new)], new, "new templates lead")


class Data(Case):
    def test_a_csv_as_schema_stats_and_samples(self):
        out = self.tool("data", os.path.join(FIX, "orders.csv"))
        self.assertIn("csv, 120 rows, 6 columns", out.splitlines()[0])
        col = {ln.split()[0]: ln for ln in out.splitlines() if ln.startswith("  ") and len(ln.split()) > 1}
        self.assertIn("number", col["amount"])
        self.assertIn("'N/A'×2", col["amount"])  # the root cause of a failing sum
        self.assertIn("3 empty", col["email"])
        self.assertIn("date", col["created"])
        self.assertIn("5 distinct", col["country"])
        self.assertIn("1,Customer 36,c1@example.com,183.69,SE,2026-09-15", out)
        self.assertNotIn("c6@example.com", out)  # 5 sample rows, not the file

    def test_jsonl_flattens_nested_keys_and_counts_missing_ones(self):
        out = self.tool("data", os.path.join(FIX, "events.jsonl"))
        self.assertIn("jsonl, 30 rows, 5 columns", out.splitlines()[0])
        col = {ln.split()[0]: ln for ln in out.splitlines() if ln.startswith("  ") and len(ln.split()) > 1}
        self.assertIn("1 empty", col["ms"])
        self.assertIn("bool", col["user.beta"])

    def test_sqlite_tables_with_their_columns(self):
        db = os.path.join(self.tmp, "shop.db")
        rows = [ln.split(",") for ln in read_text(os.path.join(FIX, "orders.csv")).splitlines()[1:]]
        with sqlite3.connect(db) as con:
            con.execute("CREATE TABLE orders (id INTEGER, customer TEXT, email TEXT, amount REAL, country TEXT, "
                        "created TEXT)")
            con.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", rows)
        con.close()
        out = self.tool("data", db)
        self.assertIn("sqlite, 1 table", out.splitlines()[0])
        self.assertIn("orders: 120 rows, 6 columns", out)
        self.assertIn("'N/A'×2", next(ln for ln in out.splitlines() if ln.split()[:1] == ["amount"]))


class Trace(Case):
    def setUp(self):
        super().setUp()
        self.with_repo()

    def frames(self, out):
        return [ln for ln in out.splitlines() if re.match(r"[\w./]+:\d+ ", ln)]

    def test_a_python_trace_mapped_to_repo_lines_age_and_task(self):
        out = self.tool("trace", input=read_text(os.path.join(FIX, "python_trace.txt")))
        self.assertEqual(out.splitlines()[0], "KeyError: 'std'")
        frames = self.frames(out)
        self.assertTrue(frames[0].startswith("price.py:6 in rate_for"), out)  # deepest first
        self.assertRegex(frames[0], r"\d{4}-\d\d-\d\d [0-9a-f]{7,} T-0042")
        self.assertIn("    return RATES[kind]", out)
        self.assertEqual([f.split()[0] for f in frames], ["price.py:6", "price.py:10", "app.py:7", "app.py:7",
                                                          "app.py:11"])
        self.assertIn("3 frames outside the repo", out)
        self.assertNotIn("/home/runner", out)

    def test_a_node_trace_and_uncommitted_lines(self):
        path = os.path.join(self.repo, "web", "cart.js")
        src = read_text(path).replace("console.log(cartTotal(", "console.info(cartTotal(")
        with open(path, "w") as f:
            f.write(src)
        out = self.tool("trace", os.path.join(FIX, "node_trace.txt"))
        self.assertEqual(out.splitlines()[0], "TypeError: Cannot read properties of undefined (reading 'rate')")
        frames = self.frames(out)
        self.assertTrue(frames[0].startswith("web/cart.js:11 in cartTotal"), out)
        self.assertIn("T-0042", frames[0])
        self.assertTrue(frames[1].startswith("web/cart.js:17 in Object.<anonymous>"), out)
        self.assertIn("uncommitted", frames[1])
        self.assertIn("    return net * (1 + cart.tax.rate);", out)
        self.assertIn("7 frames outside the repo", out)


if __name__ == "__main__":
    import unittest
    unittest.main()
