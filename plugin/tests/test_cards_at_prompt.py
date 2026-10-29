"""T-0977: a request that names a library or topic a stack card covers gets those cards named at prompt time (read
on demand), once per session per card, from a cached name index; doctor counts card use."""
import os

from test_hooks import HookCase

import fmcore as c
import fmdoctor as d
import fmlib


class CardsAtPrompt(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def ask(self, text, sid="s1"):
        return self.ctx_of(self.hook("UserPromptSubmit", {"prompt": text, "session_id": sid}))

    def test_named_libraries_get_their_cards_once_per_session(self):
        note = self.ask("fix the react hook that re-runs the postgres query on every render")
        self.assertIn("fm lib show", note)
        self.assertIn("react", note)
        self.assertIn("postgres", note)
        self.assertNotIn("stack cards", self.ask("the react page still re-renders").lower())  # once per session
        self.assertIn("react", self.ask("the react page still re-renders", sid="s2"))  # a new session hears it again

    def test_no_card_for_plain_words_common_words_or_notifications(self):
        for text in ("make it work again please", "go ahead", "fix the login timeout",
                     "<task-notification><result>react postgres</result></task-notification>"):
            self.assertNotIn("stack cards", self.ask(text).lower(), text)

    def test_matching_reads_a_cached_index(self):
        self.assertEqual(fmlib.cards_named("tune the kafka consumer and the redis cache"), ["kafka", "redis"])
        self.assertTrue(os.path.isfile(fmlib._names_path()))
        real = fmlib.cards
        fmlib.cards = lambda *a, **k: (_ for _ in ()).throw(AssertionError("parsed the cards again"))
        try:
            self.assertEqual(fmlib.cards_named("the redis cache"), ["redis"])
        finally:
            fmlib.cards = real
        self.assertEqual(fmlib.cards_named("set up react-hook-form validation"), ["react-hook-form"])  # longest first

    def test_doctor_counts_cards_read_and_named(self):
        self.ask("fix the react render loop")
        self.fm("lib", "show", "react", "--section", "avoid")
        detail = d.check_enforce(self.project()).detail
        self.assertIn("cards named 1", detail)
        self.assertIn("cards read 1", detail)

    def test_matching_compiles_only_the_names_the_request_contains(self):
        """T-2024: an alternation of every card name took ~9 ms to compile on each prompt; only names the text holds
        are compiled now, with the same answers (a name inside a longer word still isn't one)."""
        import re
        from unittest import mock
        real, seen = re.compile, []
        with mock.patch.object(fmlib.re, "compile", side_effect=lambda *a: seen.append(a[0]) or real(*a)):
            self.assertEqual(fmlib.cards_named("the redis cache"), ["redis"])
            self.assertEqual(fmlib.cards_named("predisposed to kafkaesque prose"), [])
        pats = [s for s in seen if "redis" in s]
        self.assertTrue(pats)
        self.assertFalse(any("postgres" in s for s in pats), pats)
