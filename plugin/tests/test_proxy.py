"""T-1064: under standard autonomy an ask the user answered the same way twice is answered from that precedent."""
from helpers import ForemanTestCase


class Proxy(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def ask(self, q):
        return self.fm_json("decide", "--ask", q, "--options", "yes", "no", "--default", "no")

    def user_says(self, q, ans):
        self.fm("decide", ans, "--answer", str(self.ask(q)["queued"]))

    def test_third_ask_is_proxied(self):
        self.user_says("Use tabs?", "yes")
        self.assertNotIn("proxy", self.ask("Use tabs?"))  # one precedent is not enough
        self.fm("decide", "yes", "--answer", "1")
        self.user_says("Use tabs?", "yes")
        r = self.ask("use  TABS??")
        self.assertTrue(r["proxy"])
        self.assertEqual(r["answer"], "yes")
        self.assertIn("Proxy answer (from 3 earlier answers)", self.fm("decide", "--ask", "Use tabs?", "--options", "yes", "no", "--default", "no").stdout)
        self.assertIn("Proxy answer", self.fm_json("decide", "--list")["rows"][-1]["why"])

    def test_disagreeing_precedents_no_proxy(self):
        self.user_says("Use spaces?", "yes")
        self.user_says("Use spaces?", "no")
        self.assertNotIn("proxy", self.ask("Use spaces?"))

    def test_overruled_proxies_stop(self):
        for q in ("Q one?", "Q two?"):
            self.user_says(q, "yes")
            self.user_says(q, "yes")
        proxied = [self.ask(q) for q in ("Q one?", "Q two?")]
        self.assertTrue(all(r.get("proxy") for r in proxied))
        for r in proxied:
            self.fm("decide", "no", "--answer", str(r["queued"]))
        self.user_says("Q three?", "yes")
        self.user_says("Q three?", "yes")
        self.assertNotIn("proxy", self.ask("Q three?"))

    def test_guard_named_never_proxies(self):
        for _ in range(2):
            self.fm("decide", "yes", "--answer", str(self.ask("Tabs again?")["queued"]))
        r = self.fm("decide", "--ask", "Force push now?", "--default", "no", check=False)
        self.assertEqual(r.returncode, 1)

    def test_options_are_part_of_the_ask(self):
        for _ in range(2):
            self.fm("decide", "yes", "--answer", str(self.ask("Same words?")["queued"]))
        r = self.fm_json("decide", "--ask", "Same words?", "--options", "maybe", "later", "--default", "later")
        self.assertNotIn("proxy", r)  # other options: another ask, and "yes" isn't one of them

    def test_empty_key_never_proxies(self):
        for _ in range(2):
            self.fm("decide", "yes", "--answer", str(self.ask("???")["queued"]))
        self.assertNotIn("proxy", self.ask("???"))
