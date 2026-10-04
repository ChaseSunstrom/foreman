"""Research rigor (T-0277): pages cached per day and questions batched (T-0239); claims marked single source or
supported, contradictions across sub-questions flagged, and --quorum on a second model (T-0229)."""
import json
import os

from helpers import ForemanTestCase, read_text

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
stdin = sys.stdin.read()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "stdin": stdin}) + "\n")
model = args[args.index("--model") + 1]
if any("Split the question" in a for a in args):
    print("- Does the library stream?\n- What do users report?")
    sys.exit(0)
q = next(l for l in stdin.splitlines() if l.startswith("Sub-question: "))[14:]
if "stream" in q:
    print('- CLAIM: the library supports streaming responses | SOURCE: https://docs.alpha.dev/stream | QUOTE: "streaming is supported for all responses" | TIER: primary | DATE: 2026-01-02')
    print('- CLAIM: version 3 dropped the sync client entirely | SOURCE: https://docs.alpha.dev/v3 | QUOTE: "the sync client was removed in version 3" | TIER: primary | DATE: 2026-01-02')
else:
    print('- CLAIM: the library does not support streaming responses | SOURCE: https://forum.beta.org/t/1 | QUOTE: "no streaming at all here" | TIER: community | DATE: 2026-02-01')
    if model == "opus":
        print('- CLAIM: version 3 dropped the sync client | SOURCE: https://blog.gamma.io/v3 | QUOTE: "they removed the sync client" | TIER: secondary | DATE: 2026-01-05')
        print('- CLAIM: maintainers archived the repository in March | SOURCE: https://news.delta.net/a | QUOTE: "the project was archived in march" | TIER: secondary | DATE: 2026-03-02')
'''


class _Stubbed(ForemanTestCase):
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


class Cache(_Stubbed):
    def test_a_page_is_fetched_once_a_day(self):
        import fmresearch as r
        calls = []

        def net(url):
            calls.append(url)
            return "streaming is supported for all responses. " * 20, None
        page1 = r.cached_fetch("https://docs.alpha.dev/stream", fetch=net)
        page2 = r.cached_fetch("https://docs.alpha.dev/stream", fetch=net)
        self.assertEqual((page1, page2, calls), (page2, page1, ["https://docs.alpha.dev/stream"]))
        self.assertEqual(r.cached_fetch("https://docs.alpha.dev/missing", fetch=lambda u: (None, "HTTP 404")),
                         (None, "HTTP 404"))  # a failure isn't cached

    def test_earlier_days_are_pruned_when_a_page_is_written(self):
        import fmcore as c
        import fmresearch as r
        old = os.path.join(c.state_dir(), "research-cache", "2020-01-01")
        os.makedirs(old)
        r.cached_fetch("https://docs.alpha.dev/x", fetch=lambda u: ("a real page " * 60, None))
        self.assertFalse(os.path.exists(old))

    def test_a_failing_question_keeps_the_others_and_same_minute_names_differ(self):
        qs = os.path.join(self.tmp, "questions.txt")
        with open(qs, "w") as f:
            f.write("Does alpha stream?\nDoes alpha stream?\n")
        res = json.loads(self.fm("research", "ask", "--file", qs, "--no-verify", "--json", env=self.env).stdout)
        paths = [n["path"] for n in res["notes"]]
        self.assertEqual(len(set(paths)), 2)  # the repeat in the same minute didn't overwrite the first
        p = self.fm("research", "ask", "--file", qs, "--no-verify", "--json", env=dict(self.env, PATH="/nonexistent"),
                    check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(len(json.loads(p.stdout)["failed"]), 2)

    def test_a_file_of_questions_writes_a_note_each(self):
        qs = os.path.join(self.tmp, "questions.txt")
        with open(qs, "w") as f:
            f.write("Does alpha stream?\n\nIs alpha maintained?\n")
        res = json.loads(self.fm("research", "ask", "--file", qs, "--no-verify", "--json", env=self.env).stdout)
        self.assertEqual(len(res["notes"]), 2)
        for note in res["notes"]:
            self.assertTrue(os.path.exists(note["path"]))


class Cross(_Stubbed):
    def test_conflicts_and_single_sources_are_marked(self):
        res = json.loads(self.fm("research", "ask", "Does alpha stream?", "--no-verify", "--json", env=self.env).stdout)
        note = read_text(res["path"])
        self.assertIn("## Possible conflicts", note)
        self.assertIn("does not support streaming", note.split("## Possible conflicts", 1)[1])
        self.assertIn("single source", note)
        self.assertGreaterEqual(res["conflicts"], 1)
        view = json.loads(self.fm("ui", "--json").stdout)
        self.assertGreaterEqual(view["research"][0]["conflicts"], 1)  # the pane's research card reads these
        self.assertGreaterEqual(view["research"][0]["single"], 1)

    def test_two_models_disagreeing_on_one_sub_question_conflict_once(self):
        import fmresearch as r
        a = r.Claim("the library supports streaming responses", "https://docs.alpha.dev/s", "", "primary", "x")
        b = r.Claim("the library does not support streaming responses", "https://blog.alpha.dev/s", "", "primary", "x")
        a2 = r.Claim(a.text, a.url, "", "primary", "x")
        b2 = r.Claim(b.text, b.url, "", "primary", "x")
        a.model, b.model, a2.model, b2.model = "sonnet", "opus", "opus", "sonnet"
        conflicts = r.cross_check([a, b, a2, b2], ("sonnet", "opus"))
        self.assertEqual(len(conflicts), 1)  # one pair of statements, however many copies
        self.assertEqual(r._domain("https://blog.alpha.dev/x"), r._domain("https://docs.alpha.dev/y"))
        self.assertEqual(r._domain("https://news.bbc.co.uk/x"), "bbc.co.uk")

    def test_unverified_support_says_so_and_a_failed_second_model_is_named(self):
        import fmresearch as r
        x = r.Claim("version 3 dropped the sync client", "https://a.dev/1", "q", "primary", "x")
        y = r.Claim("version 3 dropped the sync client entirely", "https://b.dev/1", "q", "primary", "x")
        z = r.Claim("version 3 dropped the sync client too", "https://c.dev/1", "q", "primary", "x")
        x.status, y.status, z.status = "verified", "unchecked", "not found"
        x.model = y.model = z.model = "sonnet"
        r.cross_check([x, y, z], ("sonnet", "opus"))
        self.assertIn("b.dev (unchecked)", x.support)
        self.assertNotIn("c.dev", x.support)  # a quote not on its page supports nothing
        self.assertIn("opus gave no answer", x.support)

    def test_a_challenge_page_is_not_cached(self):
        import fmresearch as r
        calls = []
        r.cached_fetch("https://x.dev/p", fetch=lambda u: (calls.append(u), ("Just a moment..." + " " * 600, None))[1])
        r.cached_fetch("https://x.dev/p", fetch=lambda u: (calls.append(u), ("Just a moment..." + " " * 600, None))[1])
        self.assertEqual(len(calls), 2)

    def test_quorum_counts_twice_against_the_budget(self):
        self.fm("budget", "set", "--run", "1.0")  # one ask: a planner + 3 researchers ≈ $0.8; with a quorum ≈ $1.4
        self.fm("research", "ask", "Does alpha stream?", "--no-verify", env=self.env)
        p = self.fm("research", "ask", "Does alpha stream?", "--no-verify", "--quorum", "opus", env=self.env, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("--quorum", p.stderr)

    def test_quorum_marks_what_both_models_support(self):
        res = json.loads(self.fm("research", "ask", "Does alpha stream?", "--no-verify", "--quorum", "opus", "--json",
                                 env=self.env).stdout)
        models = [json.loads(x)["args"] for x in read_text(self.log).splitlines()]
        self.assertIn("opus", [a[a.index("--model") + 1] for a in models])
        note = read_text(res["path"])
        sync = [ln for ln in note.splitlines() if "sync client" in ln]
        self.assertTrue(any("both models" in ln for ln in sync), sync)
        self.assertTrue(any("only opus" in ln for ln in note.splitlines() if "news.delta.net" in ln))
