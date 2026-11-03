"""T-2742 step 2 (SAMPO.md): `sampo` runs every verb, the renamed verbs (smith, rune, moons, louhi, underworld, ward)
reach the old ones, and `fm` with every old verb keeps working, saying once a day, to a person at a terminal, that
it is now `sampo`."""
import os
import pty
import subprocess
import sys

from helpers import FM, ForemanTestCase

SAMPO = os.path.join(os.path.dirname(FM), "sampo")


class RenameCli(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def env(self):
        e = dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_INHIBITED="1", FOREMAN_DOCTOR_BENCH="0")
        e.pop("CLAUDE_CODE_SESSION_ID", None)
        return e

    def sampo(self, *args, check=True):
        p = subprocess.run([sys.executable, SAMPO, *args], cwd=self.repo, env=self.env(), capture_output=True,
                           text=True, timeout=60)
        if check and p.returncode:
            raise AssertionError(f"sampo {' '.join(args)} exited {p.returncode}\n{p.stdout}\n{p.stderr}")
        return p

    def test_the_new_verbs_run_the_old_ones(self):
        for new, old in ((["rune", "status"], ["genesis", "status"]), (["ward", "try", "ls"], ["guard", "try", "ls"]),
                         (["louhi", "--help"], ["exam", "--help"]), (["smith", "--help"], ["code", "--help"])):
            with self.subTest(new=new):  # sampo against sampo: a usage line names what was typed
                self.assertEqual(self.sampo(*new).stdout, self.sampo(*old).stdout)
        self.assertEqual(self.sampo("rune", "status").stdout, self.fm("genesis", "status").stdout)

    def test_the_usage_names_what_was_typed(self):
        self.assertIn("usage: sampo exam", self.sampo("louhi", "--help").stdout)
        self.assertIn("usage: fm exam", self.fm("exam", "--help").stdout)
        self.assertIn("sampo help lists them", self.sampo("nosuchverb", check=False).stderr)

    def test_moons_and_underworld_open_their_tower_docs(self):
        self.assertEqual(self.sampo("moons").returncode, 0)
        out = self.sampo("underworld")
        self.assertIn("not-yet", out.stdout + out.stderr)

    def test_a_new_name_is_no_guess_to_report(self):
        self.assertNotIn("(ran `", self.sampo("rune", "status").stderr)

    def test_fm_and_the_old_verbs_still_work(self):
        self.fm("genesis", "status")
        self.fm("guard", "try", "ls")

    def tty_stderr(self, prog, *args):
        """What prog printed to stderr when stderr is a terminal, as for a person typing it."""
        master, slave = pty.openpty()
        subprocess.run([sys.executable, prog, *args], cwd=self.repo, env=self.env(), stdout=subprocess.DEVNULL,
                       stderr=slave, timeout=60)
        os.close(slave)
        out = b""
        try:
            while chunk := os.read(master, 4096):
                out += chunk
        except OSError:  # the terminal's other end closed: all read
            pass
        os.close(master)
        return out.decode(errors="replace")

    def test_fm_says_once_a_day_that_it_is_now_sampo(self):
        first = self.tty_stderr(FM, "state", "--line")
        self.assertIn("now sampo", first)
        self.assertEqual(first.strip().count("\n"), 0, "one line")
        self.assertNotIn("now sampo", self.tty_stderr(FM, "state", "--line"), "once a day")
        self.assertNotIn("now sampo", self.tty_stderr(SAMPO, "state", "--line"))

    def test_scripts_never_see_the_deprecation_line(self):
        self.assertNotIn("now sampo", self.fm("state", "--line").stderr)
