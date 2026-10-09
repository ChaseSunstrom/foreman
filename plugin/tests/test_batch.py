"""fm batch (T-0257): related small requests worked as one host task — one plan, one gate run, one review, one commit —
each still closed honestly, done in the host."""
import json

from helpers import ForemanTestCase


class Batch(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.ids = [self.capture(f"FEATURE: small thing {i}\nDONE-WHEN: thing {i} works") for i in range(3)]

    def capture(self, block):
        out = self.fm("intake", block).stdout
        return next(w for w in out.split() if w.startswith("T-"))

    def state(self):
        return json.loads(self.fm("state", "--json").stdout)

    def test_a_batch_is_one_host_with_every_members_criteria(self):
        res = json.loads(self.fm("batch", *self.ids, "--json").stdout)
        host = res["id"]
        show = self.fm("task", "show", host).stdout
        for i, tid in enumerate(self.ids):
            self.assertIn(f"{tid}: thing {i} works", show)
            self.assertIn(f"{tid}: Small thing {i}", show.split("## Steps", 1)[1])
        inbox = [x["id"] for x in self.state()["inbox"]]
        self.assertFalse(set(self.ids) & set(inbox), "members leave the inbox while batched")
        self.assertIn(host, [x["id"] for x in self.state()["queue"]] + inbox)
        self.assertEqual(res["tier"], "M", "three small ones are one medium task")

    def test_the_host_closing_closes_its_members(self):
        host = json.loads(self.fm("batch", *self.ids, "--json").stdout)["id"]
        self.fm("task", "set", host, "--section", "Interpretation", "--text", "all three")
        self.fm("task", "set", host, "--section", "Approach (options → choice → why)", "--text", "together")
        self.fm("task", "set", host, "--section", "Acceptance criteria", "--text", "".join(
            f"- [ ] {tid}: thing {i} works — verify with `true`\n" for i, tid in enumerate(self.ids)))
        self.fm("focus", host)
        for n in range(1, 4):
            self.fm("task", "ac", host, "check", str(n), "--evidence", "true", "ok")
        for n in range(1, 4):
            self.fm("task", "step", host, "done", str(n), "--evidence", "true", "ok")
        for lens in ("self", "intent", "edge"):
            self.fm("task", "audit", host, lens, "x", "ok")
        self.fm("task", "set", host, "--section", "Docs impact", "--text", "none: test")
        self.fm("task", "set", host, "--section", "Regression test", "--text", "none: fixture")
        self.fm("task", "done", host, "--lesson", "batched")
        for tid in self.ids:
            show = json.loads(self.fm("task", "show", tid, "--json").stdout)
            self.assertEqual((show["meta"]["status"], show["meta"].get("done_in")), ("done", host))

    def test_started_or_single_items_are_refused(self):
        self.assertNotEqual(self.fm("batch", self.ids[0], check=False).returncode, 0, "one item isn't a batch")
        self.fm("task", "set", self.ids[0], "tier=S")
        self.fm("task", "set", self.ids[0], "--section", "Interpretation", "--text", "x")
        self.fm("task", "ac", self.ids[0], "add", "x :: true")
        self.fm("task", "step", self.ids[0], "add", "x")
        self.fm("focus", self.ids[0])
        out = self.fm("batch", *self.ids, check=False)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn(self.ids[0], out.stdout + out.stderr)

    def test_review_findings_hold(self):
        # T-0257 review: explore items need the user first; urgency carries; a host gone any way frees its members
        explore = self.capture("FEATURE?: maybe a thing")
        self.assertNotEqual(self.fm("batch", self.ids[0], explore, check=False).returncode, 0)
        urgent = self.capture("FEATURE!: urgent thing")
        self.fm("task", "step", self.ids[1], "add", "write it")
        self.fm("task", "step", self.ids[1], "add", "test it")
        host = json.loads(self.fm("batch", self.ids[1], urgent, "--json").stdout)["id"]
        show = json.loads(self.fm("task", "show", host, "--json").stdout)
        self.assertEqual(show["meta"]["priority"], "urgent")
        steps = self.fm("task", "show", host).stdout.split("## Steps", 1)[1]
        self.assertIn(f"{self.ids[1]}: write it", steps)
        self.assertIn(f"{self.ids[1]}: test it", steps)
        self.fm("task", "drop", host, "abandoned")  # a host that ends without closing them frees its members
        inbox = [x["id"] for x in self.state()["inbox"]]
        self.assertIn(self.ids[1], inbox)
        self.assertIn(urgent, inbox)

    def test_next_suggests_a_batch_of_small_ones(self):
        for tid in self.ids:
            self.fm("task", "set", tid, "tier=S")
        self.assertIn(f"fm batch {' '.join(self.ids)}", self.fm("next").stdout)


class Related(ForemanTestCase):
    """T-0670: related items of any size are offered as one batch; the brief says how to verify it cheaply."""
    def setUp(self):
        super().setUp()
        self.fm("init")
        cap = lambda block: next(w for w in self.fm("intake", block).stdout.split() if w.startswith("T-"))
        tail = "\nCONTEXT: from the frontier brainstorm, first version and value noted"
        self.guard = [cap(f"SECURITY: guard escape: a heredoc inside backticks hides rm {i}{tail}") for i in range(3)]
        self.other = cap(f"FEATURE: dark mode toggle for the settings page{tail}")
        for t in self.guard + [self.other]:
            self.fm("task", "set", t, "tier=M")

    def test_suggest_groups_related_items_only(self):
        out = self.fm("batch", "--suggest").stdout
        self.assertIn(f"fm batch {' '.join(self.guard)}", out)
        self.assertNotIn(self.other, out)

    def test_next_offers_the_related_group_for_any_tier(self):
        self.assertIn(f"fm batch {' '.join(self.guard)}", self.fm("next").stdout)

    def test_apply_creates_the_batches_and_their_brief_says_verify_once(self):
        res = self.fm("batch", "--suggest", "--apply").stdout
        host = next(w for w in res.split() if w.startswith("T-") and w not in self.guard + [self.other])
        show = self.fm("task", "show", host).stdout
        self.assertIn("full gates", show)
        self.assertIn("own new tests", show)
