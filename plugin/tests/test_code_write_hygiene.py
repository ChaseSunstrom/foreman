"""T-1408: fm code's write and edit keep a file's line endings (LF text over a CRLF file stays CRLF), refuse a binary or
non-UTF-8 target instead of rewriting it, and refuse an option-shaped path ('-', '--x') cleanly."""
import os
import subprocess

from test_code import CodeCase, call, plan

SEED = {"crlf.txt": b"one\r\ntwo\r\n", "crlf_edit.txt": b"one\r\ntwo\r\nend\r\n", "lf.txt": b"one\ntwo\n",
        "blob.bin": b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR", "nul.txt": b"text\x00more\n", "latin.txt": b"caf\xe9\n"}


class WriteHygiene(CodeCase):
    def bytes_of(self, rel):
        with open(os.path.join(self.repo, rel), "rb") as f:
            return f.read()

    def test_endings_kept_binary_and_option_paths_refused(self):
        for rel, data in SEED.items():
            with open(os.path.join(self.repo, rel), "wb") as f:
                f.write(data)
        subprocess.run(["git", "-C", self.repo, "add", "."], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "seed"], check=True)
        actions = [call("write", file="crlf.txt", content="one\nTWO\nthree\n"),
                   call("edit", file="crlf_edit.txt", old="one\ntwo", new="one\nTWO\nmore"),
                   call("write", file="lf.txt", content="one\r\nTWO\r\n"),
                   call("write", file="new.txt", content="a\nb\n"),
                   call("write", file="blob.bin", content="x"),
                   call("edit", file="blob.bin", old="PNG", new="JPG"),
                   call("write", file="nul.txt", content="clean\n"),
                   call("edit", file="latin.txt", old="caf", new="cafe"),
                   call("write", file="--x", content="x"),
                   call("write", file="-", content="x"),
                   call("read", path="-"),
                   call("edit", file="calc.py", old="a - b", new="a + b")]
        f = self.serve("openai", plan(), *actions, call("done", summary="done"))
        r = self.code("fix add", "--model", "fake", "--no-commit", check=False)
        said = [f.seen[i + 2]["messages"][-1]["content"] for i in range(len(actions))]
        self.assertEqual(self.bytes_of("crlf.txt"), b"one\r\nTWO\r\nthree\r\n", said[0])
        self.assertEqual(self.bytes_of("crlf_edit.txt"), b"one\r\nTWO\r\nmore\r\nend\r\n", said[1])
        self.assertEqual(self.bytes_of("lf.txt"), b"one\nTWO\n", said[2])  # an LF file stays LF
        self.assertEqual(self.bytes_of("new.txt"), b"a\nb\n", said[3])  # a new file keeps LF
        for i, rel in ((4, "blob.bin"), (5, "blob.bin"), (6, "nul.txt"), (7, "latin.txt")):
            self.assertEqual(self.bytes_of(rel), SEED[rel], said[i])  # untouched
            self.assertIn("refused", said[i])
            self.assertIn("UTF-8", said[i])
        for i in (8, 9, 10):
            self.assertIn("looks like an option", said[i])
        self.assertFalse(os.path.exists(os.path.join(self.repo, "--x")))
        self.assertFalse(os.path.exists(os.path.join(self.repo, "-")))
        self.assertIn("return a + b", self.calc(), r.stdout + r.stderr)
