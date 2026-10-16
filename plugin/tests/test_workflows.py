"""T-0787: the workflows Foreman ships (plugin/workflows/*.js, run as /foreman:<name>) load: a pure-literal meta first,
its name the file's, every phase() title declared in meta.phases, valid ES module syntax, and nothing that breaks resume
(Date.now, Math.random, an argless new Date)."""
import glob
import os
import re
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FLOWS = sorted(glob.glob(os.path.join(HERE, "..", "workflows", "*.js")))


class Workflows(unittest.TestCase):
    def test_review_and_ideas_ship(self):
        self.assertEqual({os.path.basename(f) for f in FLOWS} >= {"review.js", "ideas.js"}, True, FLOWS)

    def test_each_loads(self):
        for path in FLOWS:
            with self.subTest(path=os.path.basename(path)), open(path, encoding="utf-8") as f:
                text = f.read()
                self.assertTrue(text.startswith("export const meta = {"), "meta must be the first statement")
                meta = text[:text.index("\n}\n") + 2]
                self.assertNotRegex(meta, r"\$\{|\.\.\.|\w\(", "meta is a pure literal: no interpolation, spreads or calls")
                name = re.search(r"\bname:\s*'([\w-]+)'", meta)
                self.assertEqual(name and name.group(1), os.path.basename(path)[:-3])
                self.assertRegex(meta, r"\bdescription:\s*'[^']+'")
                declared = set(re.findall(r"\{\s*title:\s*'([^']+)'", meta))
                used = set(re.findall(r"\bphase\(\s*'([^']+)'", text)) | set(re.findall(r"phase:\s*'([^']+)'", text))
                self.assertTrue(used, "phases are named")
                self.assertLessEqual(used, declared, "every phase used is declared in meta.phases")
                self.assertNotRegex(text, r"Date\.now|Math\.random|new Date\(\s*\)", "breaks resume")

    @unittest.skipUnless(shutil.which("node"), "node isn't installed")
    def test_each_parses(self):
        # the runner executes the body as an async function (top-level await and return), so check it that way
        for path in FLOWS:
            with self.subTest(path=os.path.basename(path)), tempfile.TemporaryDirectory() as d, \
                    open(path, encoding="utf-8") as f:
                body = f.read().replace("export const meta", "const meta", 1)
                wrapped = os.path.join(d, "flow.js")
                with open(wrapped, "w", encoding="utf-8") as out:
                    out.write("async function workflow(agent, parallel, pipeline, phase, log, args, budget) {\n"
                              + body + "\n}\n")
                r = subprocess.run(["node", "--check", wrapped], capture_output=True, text=True, timeout=60)
                self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
