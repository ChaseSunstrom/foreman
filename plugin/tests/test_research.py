"""fm research ask (T-0206): recall first, parallel web researchers per sub-question, every quoted claim checked
against the page it cites, one note recorded."""
import json
import os

from helpers import ForemanTestCase, read_text

import fmresearch as r

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
stdin = sys.stdin.read()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "stdin": stdin}) + "\n")
if any("Split the question" in a for a in args):
    print("- How fast is A?\n- How fast is B?")
    sys.exit(0)
q = next(l for l in stdin.splitlines() if l.startswith("Sub-question: "))[14:]
print(f"Answer for {q}")
print(f'- CLAIM: {q} measured | SOURCE: https://example.com/{len(q)} | QUOTE: "it runs fast" | TIER: primary | DATE: 2026-01-02')
print('- AGAINST: a forum says otherwise | SOURCE: https://forum.example.org/t | QUOTE: "slow for me" | TIER: community | DATE: unknown')
print("- OPEN: nobody measured C")
'''


class Ask(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log}
        self.fm("init")

    def calls(self):
        return [json.loads(l) for l in read_text(self.log).splitlines()]

    def test_plans_fans_out_and_records_one_note(self):
        self.fm("research", "add", "speed-notes", input="# Parser speed\nThe json parser was benchmarked fast last year.\n")
        res = json.loads(self.fm("research", "ask", "How fast is the json parser?", "--no-verify", "--json",
                                 env=self.env).stdout)
        calls = self.calls()
        self.assertEqual(len(calls), 3, "one planner, then one researcher per sub-question")
        self.assertIn("--tools", calls[0]["args"])
        self.assertEqual(calls[0]["args"][calls[0]["args"].index("--tools") + 1], "", "the planner has no tools")
        for call in calls[1:]:
            self.assertEqual(call["args"][call["args"].index("--tools") + 1], "WebSearch,WebFetch")
            self.assertIn("--strict-mcp-config", call["args"])
        note = read_text(res["path"])
        self.assertIn("speed-notes", note, "what's already known comes first")
        self.assertIn("## How fast is A?", note)
        self.assertIn("## How fast is B?", note)
        self.assertIn("How fast is A? measured", note)
        self.assertIn("https://example.com/", note)
        self.assertIn("slow for me", note)
        self.assertIn("nobody measured C", note)
        self.assertEqual(res["claims"], 4)
        self.assertEqual(res["unchecked"], 4)

    def test_given_sub_questions_skip_the_planner(self):
        self.fm("research", "ask", "Q?", "--sub", "Only this?", "--no-verify", env=self.env)
        calls = self.calls()
        self.assertEqual(len(calls), 1)
        self.assertIn("Sub-question: Only this?", calls[0]["stdin"])

    def test_an_answer_without_claims_is_reported(self):
        stub = os.path.join(self.tmp, "bin", "claude")
        with open(stub, "w") as f:
            f.write("#!/bin/sh\ncat >/dev/null\necho 'I could not search.'\n")
        out = self.fm("research", "ask", "Q?", "--sub", "S?", "--no-verify", env=self.env, check=False)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("no claims", out.stdout + out.stderr)


class Verify(ForemanTestCase):
    def test_quotes_are_checked_against_the_fetched_page(self):
        pages = {"https://a.example/1": "<html><script>x</script><p>The engine &amp; it <b>runs  fast</b> on ARM.</p>",
                 "https://a.example/2": "<p>Nothing relevant here at all, sorry about that.</p>"}
        claims = [r.Claim("c1", "https://a.example/1", "the engine & it runs fast", "primary", "unknown"),
                  r.Claim("c2", "https://a.example/2", "it runs fast on ARM chips", "primary", "unknown"),
                  r.Claim("c3", "https://a.example/3", "anything", "primary", "unknown"),
                  r.Claim("c4", "", "no source", "secondary", "unknown")]

        def fetch(url):
            return (pages[url], None) if url in pages else (None, "HTTP 404")
        r.verify(claims, fetch=fetch)
        self.assertEqual([c.status for c in claims], ["verified", "not found", "unchecked", "unchecked"])
        self.assertIn("404", claims[2].why)

    def test_a_broken_page_or_short_quote_never_verifies_or_crashes(self):
        # T-0206 review: a hostile page (bogus charset, broken HTTP) must not lose the run; "the" isn't a quote
        claims = [r.Claim("c1", "https://a.example/1", "it runs fast", "primary", "unknown"),
                  r.Claim("c2", "https://a.example/2", "the", "primary", "unknown")]

        def fetch(url):
            if url.endswith("1"):
                raise __import__("http.client").client.IncompleteRead(b"")
            return "the page says the thing", None
        r.verify(claims, fetch=fetch)
        self.assertEqual([c.status for c in claims], ["unchecked", "unchecked"])
        self.assertIn("short", claims[1].why)
        self.assertEqual(r._decode(b"caf\xc3\xa9", "bogus-charset"), "café")

    def test_only_public_https_urls_are_fetched(self):
        for url in ("http://example.com/", "https://localhost/", "https://127.0.0.1/", "https://10.0.0.1/x",
                    "https://[::1]/", "file:///etc/passwd", "https://169.254.169.254/latest/meta-data", "ftp://x.org/"):
            with self.subTest(url=url):
                self.assertFalse(r.public_https(url))
                page, why = r.fetch(url)
                self.assertIsNone(page)
                self.assertTrue(why)

    def test_claim_lines_parse(self):
        got = r.parse_claims('- CLAIM: X is 3x faster | SOURCE: https://x.org/a | QUOTE: "three times" | TIER: primary'
                             ' | DATE: 2026-05-01\n- AGAINST: no | SOURCE: https://y.org | QUOTE: "nope" | TIER: community'
                             '\n- OPEN: what about Z?\nprose line\n')
        self.assertEqual([(c.kind, c.text, c.url, c.quote, c.tier) for c in got["claims"]],
                         [("claim", "X is 3x faster", "https://x.org/a", "three times", "primary"),
                          ("against", "no", "https://y.org", "nope", "community")])
        self.assertEqual(got["open"], ["what about Z?"])
