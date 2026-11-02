"""T-2560: the CI matrix keeps each job under its deadline: macOS (about 1.5x Ubuntu's time) runs the suite in thirds,
Ubuntu in halves, and the run line's shard count follows the job, so no shard of either is left out."""
import os
import re
import unittest

WORKFLOW = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                        ".github", "workflows", "test.yml")


class CiMatrix(unittest.TestCase):
    def test_macos_runs_thirds_and_ubuntu_halves(self):
        with open(WORKFLOW, encoding="utf-8") as f:
            text = f.read()
        macos = re.findall(r"- os: macos-latest.*?\n(?:\s+\w+: .*\n)*?\s+shard: (\d)", text)
        self.assertEqual(sorted(macos), ["1", "2", "3"], "every macOS third is a job")
        self.assertRegex(text, r"shard: \[1, 2\]", "Ubuntu runs both halves")
        self.assertIn("--shard ${{ matrix.shard }}/${{ matrix.experimental && 3 || 2 }}", text)


if __name__ == "__main__":
    unittest.main()
