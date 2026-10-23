"""The guard evasion corpus holds (T-1263).

guard_evasions.jsonl and guard_gaps.jsonl are gen_evasions.py's output. These tests hold the current guard to every
label in the corpus, hold every listed gap to still being a gap, and fail if regenerating would change either file —
so a guard change (a fix or a regression) forces a reviewed regeneration, and a fixed gap has to move into the corpus.
Run: cd plugin/tests && python3 -m unittest test_guard_evasions"""
import os
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(os.path.dirname(HERE), "lib"), os.path.join(HERE, "fixtures")):
    if p not in sys.path:
        sys.path.insert(0, p)

import fmreplay  # noqa: E402
import gen_evasions  # noqa: E402

FIX = os.path.join(HERE, "fixtures")
CORPUS = os.path.join(FIX, "guard_evasions.jsonl")
GAPS = os.path.join(FIX, "guard_gaps.jsonl")


@unittest.skipIf(gen_evasions.home_in_a_repo(), "the home folder is inside a git tree: the guard judges it a project")
class GuardEvasions(unittest.TestCase):
    def _cases(self, path):
        cases, broken = fmreplay.load_cases(path)
        self.assertEqual(broken, 0, f"a line of {os.path.basename(path)} is not a case")
        return cases

    def test_the_committed_files_are_the_generators_current_output(self):
        # regenerating must not change the committed bytes: a guard change breaks this until someone regenerates
        corpus_text, gaps_text = gen_evasions.build()
        with open(CORPUS, encoding="utf-8") as f:
            self.assertEqual(f.read(), corpus_text, "guard_evasions.jsonl is stale: python3 fixtures/gen_evasions.py")
        with open(GAPS, encoding="utf-8") as f:
            self.assertEqual(f.read(), gaps_text, "guard_gaps.jsonl is stale: python3 fixtures/gen_evasions.py")

    def test_the_guard_holds_every_corpus_label(self):
        cases = self._cases(CORPUS)
        self.assertGreater(len(cases), 0, "no evasion corpus")
        # T-1291: pin the temp folder as the real corpus test does, so a different TMPDIR cannot make a case drift
        with mock.patch.object(tempfile, "tempdir", "/var/tmp"):
            self.assertEqual(fmreplay.drift(cases), [], "the guard disagrees with a labelled evasion")
            self.assertEqual(tempfile.tempdir, "/var/tmp", "verdicts must restore tempfile's folder")

    def test_every_listed_gap_is_still_a_gap(self):
        gaps = self._cases(GAPS)
        self.assertGreater(len(gaps), 0, "no gaps listed")
        with mock.patch.object(tempfile, "tempdir", "/var/tmp"):
            drifted = fmreplay.drift(gaps)
        # every gap must still be one the guard gets wrong; a fix drops it from drift -> this fails until it moves to
        # the corpus. The recorded `got` must be what the guard actually returns now.
        self.assertEqual(len(drifted), len(gaps), "a listed gap no longer drifts: regenerate and move it to the corpus")
        by_id = {g["id"]: g for g in gaps}
        for d in drifted:
            self.assertEqual(d["got"], by_id[d["id"]]["got"], f"stored got is stale for {d['cmd']!r}")
        # a gap is a dangerous command let through or, outside a project (the corpus runs from home), an everyday one
        # refused once obfuscated: the guard can't see which tree a hidden rm or git writes to, so it says no
        self.assertTrue(all(g["got"] != g["should"] for g in gaps))
        known = ("-rf build/", "checkout -b fix/login")
        self.assertEqual([g["cmd"] for g in gaps if g["should"] == "allow" and not any(k in g["cmd"] for k in known)],
                         [], "a new over-broad refusal")


class SnapshotForms(unittest.TestCase):
    """T-1482: the four bench SNAPSHOT commands are allowed in a project because the PreToolUse hook saves the work
    they discard first. The corpus leaves them out (their verdict hangs on the tree), so here each obfuscated form runs
    from a disposable git folder: the hook must save it, or the guard refuse it; one that does neither (\\git reset
    --hard read as no git command) throws the work away unsaved."""
    def setUp(self):
        import subprocess
        base = os.environ.get("XDG_RUNTIME_DIR") or os.path.expanduser("~/.cache")  # /tmp is scratch to the guard
        self._tmp = tempfile.TemporaryDirectory(dir=base if os.access(base, os.W_OK) else None)
        self.addCleanup(self._tmp.cleanup)
        self.t = os.path.realpath(self._tmp.name)
        self.home = os.path.join(self.t, "home")
        os.makedirs(os.path.join(self.home, ".claude", "foreman"))
        self.repo, self.other = os.path.join(self.t, "repo"), os.path.join(self.t, "other")
        for repo in (self.repo, self.other):
            os.makedirs(repo)
            git = lambda *a: subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@t",
                                             "-c", "commit.gpgSign=false", *a], check=True, capture_output=True)
            git("init", "-q")
            for i, step in enumerate(["0", "1", "2", "3", "4", "5", "6", "stashed", "dirty"]):
                with open(os.path.join(repo, "f.txt"), "w") as f:
                    f.write(step)
                if i < 7:  # HEAD~5 exists
                    git("add", "f.txt")
                    git("commit", "-qm", step)
                elif step == "stashed":  # a stash for stash clear to drop
                    git("stash", "push", "-q")
            # f.txt left "dirty": uncommitted work the commands would discard

    def judge(self, cmd, cwd):
        """(refusal or None, the hook's save note or None), in the hook's order: the guard, then the save."""
        import fmguard as g
        import fmhooks
        ctx = g.Ctx(cwd=cwd, project_root=g.project_root_for(cwd, self.home), home=self.home,
                    foreman_home=os.path.join(self.home, ".claude", "foreman"), scratch=["/tmp"], task_id="T-0001")
        refused = g.check("Bash", {"command": cmd}, ctx)
        note = fmhooks._snapshot_note({"tool_input": {"command": cmd}, "cwd": cwd}, g)
        self.assertTrue(note is None or note.startswith("Foreman saved"), note)  # "couldn't save" isn't a save
        return refused, note

    def test_every_obfuscated_snapshot_command_is_saved_or_refused(self):
        ran, unsaved = 0, []
        for cmd in sorted(gen_evasions.SNAPSHOT):
            variants = [(tr.__name__, tr(cmd)) for tr in gen_evasions.EVERY] + gen_evasions.stacked(cmd)
            for name, v in variants:
                if not v:
                    continue
                # in the folder, and from outside it after a cd (the save must land in the repo, not the hook's cwd)
                for full, cwd in ((v, self.repo), (f"cd {self.repo} && {v}", self.t)):
                    ran += 1
                    refused, saved = self.judge(full, cwd)
                    if refused is None and self.repo not in (saved or ""):
                        unsaved.append(f"{name}: {full!r} from {cwd}: {saved}")
        self.assertGreater(ran, len(gen_evasions.SNAPSHOT) * 10, "too few forms: the test would be vacuous")
        self.assertEqual(unsaved, [], "allowed with nothing saved first:\n" + "\n".join(unsaved))

    def test_each_folder_a_command_discards_in_is_saved(self):
        # review: a cd before eval, a second repo of the same kind, a -C through a variable
        for cmd, cwd, repos in [
            (f"cd {self.repo} && eval 'git clean -fdx'", self.t, [self.repo]),
            (f"cd {self.repo}; sh <<< 'git clean -fdx'", self.t, [self.repo]),
            ("git reset --hard; $'git' -C ../other clean -fdx", self.repo, [self.repo, self.other]),
            (f"R={self.repo}; $'git' -C $R clean -fdx", self.t, [self.repo]),
        ]:
            with self.subTest(cmd=cmd):
                _, saved = self.judge(cmd, cwd)
                for r in repos:
                    self.assertIn(f"git -C {r} ", saved or "")


if __name__ == "__main__":
    unittest.main()
