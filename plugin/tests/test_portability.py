"""T-1665: fm home export and import: a tarball of Foreman's state without secrets, checked on import into an empty home."""
import hashlib
import io
import json
import os
import tarfile

from helpers import ForemanTestCase

import fmcore as c

KEY = "sk-ant-" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6"  # pragma: allowlist secret


class Home(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Portable task", "--type", "FIX", "--tier", "S", "--ac", "works :: true")
        self.p = c.find_project(self.repo)
        os.makedirs(os.path.join(self.p.dir, "research"), exist_ok=True)
        with open(os.path.join(self.p.dir, "research", "note.md"), "w", encoding="utf-8") as f:
            f.write(f"the key was {KEY}\n")
        with open(os.path.join(self.p.dir, "api-token.json"), "w", encoding="utf-8") as f:
            f.write('{"value": "plain"}\n')  # credential-shaped by name: left out whatever it holds
        self.tar = os.path.join(self.tmp, "home.tar.gz")
        self.empty = os.path.join(self.tmp, "home2")

    def export(self):
        out = self.fm("home", "export", "--out", self.tar).stdout
        self.assertTrue(os.path.isfile(self.tar), out)
        return out

    def import_(self, path, check=True):
        return self.fm("home", "import", path, env={"FOREMAN_HOME": self.empty}, check=check)

    def members(self):
        with tarfile.open(self.tar) as t:
            return {m.name: t.extractfile(m).read() for m in t.getmembers() if m.isfile()}

    def test_round_trip_into_an_empty_home_keeps_tasks_and_drops_secrets(self):
        self.export()
        files = self.members()
        self.assertIn("MANIFEST.json", files)
        blob = b"".join(files.values())
        self.assertNotIn(KEY.encode(), blob, "a secret in a state file is redacted")
        self.assertFalse([n for n in files if "api-token" in n], "a credential-shaped file is left out")
        self.import_(self.tar)
        p = self.fm("task", "list", "--json", env={"FOREMAN_HOME": self.empty})
        self.assertIn("Portable task", p.stdout)

    def test_import_refuses_a_home_that_already_has_projects(self):
        self.export()
        self.import_(self.tar)
        r = self.import_(self.tar, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("empty", r.stdout + r.stderr)

    def rebuild(self, extra, manifest_too=True):
        """The export with one more member (name, TarInfo tweak), listed in the manifest so only the path check stops it."""
        files = self.members()
        man = json.loads(files.pop("MANIFEST.json"))
        name, data, kind = extra
        if manifest_too:
            man["files"][name] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
        bad = os.path.join(self.tmp, "bad.tar.gz")
        with tarfile.open(bad, "w:gz") as t:
            for n, d in [("MANIFEST.json", json.dumps(man).encode())] + sorted(files.items()) + [(name, data)]:
                info = tarfile.TarInfo(n)
                info.size = len(d)
                if n == name and kind == "symlink":
                    info.type, info.linkname, info.size, d = tarfile.SYMTYPE, "/etc/passwd", 0, b""
                t.addfile(info, io.BytesIO(d))
        return bad

    def assert_refused(self, bad, *outside):
        r = self.import_(bad, check=False)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.empty, "state", "projects")), "nothing imported")
        for path in outside:
            self.assertFalse(os.path.exists(path), path)
        return r

    def test_import_refuses_a_path_traversal_member(self):
        self.export()
        r = self.assert_refused(self.rebuild(("state/../../escaped.txt", b"x", "file")),
                                os.path.join(self.tmp, "escaped.txt"))
        self.assertIn("escaped.txt", r.stdout + r.stderr)

    def test_import_refuses_an_absolute_member_and_a_link(self):
        self.export()
        self.assert_refused(self.rebuild(("/" + os.path.join(self.tmp, "abs.txt").lstrip("/"), b"x", "file")),
                            os.path.join(self.tmp, "abs.txt"))
        self.assert_refused(self.rebuild(("state/link", b"", "symlink")))

    def test_import_refuses_a_file_the_manifest_doesnt_vouch_for(self):
        self.export()
        self.assert_refused(self.rebuild(("state/extra.md", b"x", "file"), manifest_too=False))
        files = self.members()
        name = next(n for n in files if n.endswith(".md"))
        bad = os.path.join(self.tmp, "tampered.tar.gz")
        with tarfile.open(bad, "w:gz") as t:
            for n, d in sorted(files.items()):
                info = tarfile.TarInfo(n)
                d = d[:-1] + (b"!" if d[-1:] != b"!" else b"?") if n == name else d  # same size: only the hash tells
                info.size = len(d)
                t.addfile(info, io.BytesIO(d))
        r = self.assert_refused(bad)
        self.assertIn(name, r.stdout + r.stderr)
        self.assertIn("hash", r.stdout + r.stderr)

    def test_a_sensitive_project_is_left_out(self):
        self.fm("sensitive", "on")
        out = self.export()
        self.assertFalse([n for n in self.members() if n.startswith(f"state/projects/{self.p.slug}/")])
        self.assertIn("sensitive", out)
