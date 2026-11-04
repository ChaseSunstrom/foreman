"""T-2861: a branch that changes a string literal can split a producer from its consumer (T-2847: graph.py kept
writing 'Blast radius (fm graph blast)' while cli.py's check looked for the sampo form). lanes.twins names each
changed literal whose old text still lives elsewhere in plugin/, readers and module constants first, so the merge's
review sees the split."""
# map-links: plugin/lib/sampo/lanes.py
import os
import subprocess
import unittest

from helpers import ForemanTestCase

from sampo import lanes

G = ["git", "-c", "user.name=t", "-c", "user.email=t@localhost", "-c", "commit.gpgsign=false"]


class Twins(ForemanTestCase):
    def git(self, *a):
        return subprocess.run(G + list(a), cwd=self.root, capture_output=True, text=True, check=True).stdout.strip()

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def setUp(self):
        super().setUp()
        self.root = os.path.join(self.tmp, "r")
        os.makedirs(self.root)
        self.git("init", "-q")
        self.write("plugin/lib/graph.py", 'def line():\n    return "Blast radius (fm graph blast): " + "x"\n')
        self.write("plugin/lib/cli.py", 'def needs(s):\n    return "Blast radius (fm graph blast)" not in s\n'
                                        'HINT = "run fm check --affected first"\n')
        self.write("plugin/lib/other.py", 'SAY = "run fm check --affected first"\n')
        self.write("plugin/tests/test_x.py", 'X = "Blast radius (fm graph blast)"\n')
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD")

    def test_a_reader_respelled_alone_names_the_writer_that_kept_the_old_text(self):
        self.write("plugin/lib/cli.py", 'def needs(s):\n    return "Blast radius (sampo graph blast)" not in s\n'
                                        'HINT = "run sampo check --affected first"\n')
        self.git("commit", "-qam", "respell")
        got = lanes.twins(self.root, self.base, "HEAD")
        olds = [x["old"] for x in got]
        self.assertIn("Blast radius (fm graph blast)", olds)
        self.assertIn("run fm check --affected first", olds)
        blast = next(x for x in got if x["old"] == "Blast radius (fm graph blast)")
        self.assertEqual([w.split(":")[0] for w in blast["still"]], ["plugin/lib/graph.py"], "tests are not counted")
        self.assertEqual(olds[0], "Blast radius (fm graph blast)", "a reader's split comes first")
        lines = lanes.twins_lines(got)
        self.assertTrue(lines[0].startswith("- "), lines)
        self.assertIn("graph.py", "\n".join(lines))

    def test_a_literal_changed_everywhere_or_only_added_is_quiet(self):
        self.write("plugin/lib/graph.py", 'def line():\n    return "Blast radius (sampo graph blast): " + "x"\n')
        self.write("plugin/lib/cli.py", 'def needs(s):\n    return "Blast radius (sampo graph blast)" not in s\n'
                                        'HINT = "run fm check --affected first"\nNEW = "a brand new message here"\n')
        self.git("commit", "-qam", "respell both sides")
        self.assertEqual(lanes.twins(self.root, self.base, "HEAD"), [])


if __name__ == "__main__":
    unittest.main()
