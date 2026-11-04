"""T-2866: a criterion's verify command may use Sampo's own verb names: core.unrunnable parses it the way the CLI does,
through cli._alias (sampo moons check was refused as 'unknown moons' though it runs)."""
# map-links: plugin/lib/sampo/core.py plugin/lib/sampo/cli.py
import unittest

from helpers import ForemanTestCase

from sampo import core as c


class VerifyAlias(ForemanTestCase):
    def test_a_sampo_alias_verb_is_a_runnable_verify_and_an_unknown_one_is_not(self):
        for cmd in ("sampo moons check", "sampo rune status", "fm louhi --help", "sampo genesis moonshot check"):
            self.assertIsNone(c.unrunnable(cmd, self.repo), cmd)
        self.assertIn("doesn't take", c.unrunnable("sampo moonz check", self.repo) or "")


if __name__ == "__main__":
    unittest.main()
