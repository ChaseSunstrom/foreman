"""T-3222: sampo sandbox, the container tier. A job runs in its own user, mount, pid, ipc and uts namespaces through
bwrap: the system read-only, only its project and the folders it names writable, credential folders empty, secrets
gone from its environment, the network off unless asked. Each escape below must fail; ordinary work must not."""
import json
import os
import socket
import subprocess
import sys
import threading
import unittest
from unittest import mock

from helpers import ForemanTestCase

from sampo import sandbox as sb

OK, WHY = sb.available()


def server():
    """A TCP listener on this machine's loopback that answers 'hi' once per connection; (port, close)."""
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    s.listen(4)

    def serve():
        while True:
            try:
                c, _ = s.accept()
            except OSError:
                return
            c.sendall(b"hi")
            c.close()
    threading.Thread(target=serve, daemon=True).start()
    return s.getsockname()[1], s.close


@unittest.skipUnless(OK, f"no job sandbox here: {WHY}")
class JobTier(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.root = os.path.join(self.tmp, "proj")
        self.out = os.path.join(self.tmp, "outside")
        self.fake = os.path.join(self.tmp, "home")
        for d in (self.root, self.out, os.path.join(self.fake, ".ssh"), os.path.join(self.fake, ".config", "sampo")):
            os.makedirs(d)
        for rel, text in ((".ssh/id_rsa", "SECRET-KEY"), (".config/sampo/secrets.env", "LLM_API_KEY=sk-SECRET"),
                          (".git-credentials", "https://u:SECRET-TOKEN@github.com"),  # pragma: allowlist secret
                          ("notes.txt", "plain notes")):
            with open(os.path.join(self.fake, rel), "w") as f:
                f.write(text)

    def sh(self, script, **kw):
        kw.setdefault("home", self.fake)
        return sb.run(["sh", "-c", script], root=self.root, capture_output=True, text=True, timeout=60, **kw)

    def test_writes_land_only_in_the_project_and_named_folders(self):
        extra = os.path.join(self.tmp, "cache")
        os.makedirs(extra)
        r = self.sh(f"echo a > {self.root}/in.txt; echo b > {extra}/c.txt; echo c > {self.out}/out.txt; "
                    f"echo d > {self.fake}/notes.txt", writes=[extra])
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue(os.path.exists(os.path.join(self.root, "in.txt")))
        self.assertTrue(os.path.exists(os.path.join(extra, "c.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.out, "out.txt")))
        with open(os.path.join(self.fake, "notes.txt")) as f:
            self.assertEqual(f.read(), "plain notes")

    def test_credential_folders_and_files_read_empty_while_the_rest_of_home_reads(self):
        r = self.sh(f"cat {self.fake}/.ssh/id_rsa {self.fake}/.config/sampo/secrets.env {self.fake}/.git-credentials; "
                    f"cat {self.fake}/notes.txt")
        self.assertNotIn("SECRET", r.stdout + r.stderr)
        self.assertIn("plain notes", r.stdout)

    def test_the_network_is_off_unless_asked(self):
        port, close = server()
        self.addCleanup(close)
        probe = f"{sys.executable} -c \"import socket; print(socket.create_connection(('127.0.0.1', {port}), 3).recv(2))\""
        self.assertNotIn("hi", self.sh(probe).stdout)
        self.assertIn("hi", self.sh(probe, net="on").stdout, "the probe itself works")

    def test_processes_and_signals_stay_inside(self):
        outside = subprocess.Popen(["sleep", "60"])
        self.addCleanup(outside.wait)
        self.addCleanup(outside.kill)
        r = self.sh(f"kill -0 {outside.pid} && echo reached; cat /proc/1/comm")
        self.assertNotIn("reached", r.stdout)
        self.assertNotIn("systemd", r.stdout)
        self.assertIsNone(outside.poll())

    def test_secrets_leave_the_environment_and_sockets_to_the_host_are_gone(self):
        env = dict(os.environ, LLM_API_KEY="sk-SECRET", GITHUB_TOKEN="SECRET", MY_PASSWORD="SECRET",  # pragma: allowlist secret
                   KEEP_ME="yes")
        r = self.sh("env; ls /run/docker.sock /var/run/docker.sock /run/user 2>/dev/null | head -3", env=env)
        self.assertNotIn("SECRET", r.stdout)
        self.assertIn("KEEP_ME=yes", r.stdout)
        self.assertNotIn("docker.sock", r.stdout)

    def test_the_runtime_dir_exists_empty_and_private(self):
        r = self.sh('mkdir "$XDG_RUNTIME_DIR/fm-x" && ls -A "$XDG_RUNTIME_DIR" && stat -c %a "$XDG_RUNTIME_DIR"',
                    env=dict(os.environ, XDG_RUNTIME_DIR=f"/run/user/{os.getuid()}"))
        self.assertEqual(r.stdout.split(), ["fm-x", "700"], r.stderr)

    def test_ordinary_work_runs_unchanged(self):
        r = self.sh("git init -q . && git -c user.email=a@b -c user.name=a commit -q --allow-empty -m x && "
                    f"git log --oneline | wc -l && {sys.executable} -c 'print(6 * 7)' && echo tmp > $TMPDIR/t && cat $TMPDIR/t")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.split(), ["1", "42", "tmp"])

    def test_the_cli_runs_a_job_and_names_each_layer(self):
        p = self.fm("sandbox", "run", "--", "sh", "-c", f"echo x > {self.out}/cli.txt; echo ran", check=False)
        self.assertIn("ran", p.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.out, "cli.txt")))
        status = self.fm("sandbox", "status").stdout
        for layer in ("job", "session", "landlock"):
            self.assertIn(layer, status.lower())

    def test_the_cli_reads_options_typed_after_run(self):
        port, close = server()
        self.addCleanup(close)
        here = f"127.0.0.1:{port}"
        with open(os.path.join(self.root, "c.py"), "w") as f:
            f.write(CONNECT)
        ok = self.fm("sandbox", "run", "--net", "allow", "--allow", here, "--root", self.root, "--", sys.executable,
                     "c.py", here, cwd=self.root, check=False)
        self.assertIn("hi", ok.stdout)
        no = self.fm("sandbox", "run", "--net", "allow", "--root", self.root, "--", sys.executable, "c.py", here,
                     cwd=self.root, check=False)
        self.assertIn("403", no.stdout)
        self.assertIn(f"refused {here}", no.stderr)
        bad = self.fm("sandbox", "run", "--bogus", "--", "true", check=False)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("--bogus", bad.stderr)


CONNECT = """import os, socket, sys
from urllib.parse import urlsplit
u = urlsplit(os.environ["HTTPS_PROXY"])
s = socket.create_connection((u.hostname, u.port), 10)
s.sendall(f"CONNECT {sys.argv[1]} HTTP/1.1\\r\\nHost: {sys.argv[1]}\\r\\n\\r\\n".encode())
data = b""
while d := s.recv(4096):
    data += d
head, _, body = data.partition(b"\\r\\n\\r\\n")
print(head.decode(errors="replace").split("\\r\\n")[0], body.decode(errors="replace") or "-")
"""


@unittest.skipUnless(OK, f"no job sandbox here: {WHY}")
class AllowTier(ForemanTestCase):
    """Step 3: --net allow reaches only the allowlist, through a filtering proxy outside; link-local (cloud metadata)
    is refused even when listed, and a loopback or private address only when an entry names it with its port."""

    def setUp(self):
        super().setUp()
        self.root = os.path.join(self.tmp, "proj")
        os.makedirs(self.root)
        with open(os.path.join(self.root, "c.py"), "w") as f:
            f.write(CONNECT)
        self.port, close = server()
        self.addCleanup(close)

    def via(self, target, allow):
        return sb.run([sys.executable, "c.py", target], root=self.root, net="allow", allow=allow, capture_output=True,
                      text=True, timeout=60)

    def test_only_listed_hosts_get_through(self):
        here = f"127.0.0.1:{self.port}"
        self.assertEqual(self.via(here, [here]).stdout.split()[-1], "hi")
        self.assertEqual(self.via(f"localhost:{self.port}", [f"localhost:{self.port}"]).stdout.split()[-1], "hi")
        refused = self.via(here, ["example.com"])
        self.assertIn("403", refused.stdout)
        self.assertNotIn("hi", refused.stdout)
        self.assertIn(here, refused.stderr, "the denial is named")

    def test_loopback_needs_its_port_named_and_metadata_never_passes(self):
        self.assertIn("403", self.via(f"127.0.0.1:{self.port}", ["127.0.0.1"]).stdout)
        self.assertIn("403", self.via("169.254.169.254:80", ["169.254.169.254:80", "169.254.169.254"]).stdout)

    def test_a_direct_connection_around_the_proxy_fails(self):
        probe = (f"import socket\ntry:\n    socket.create_connection(('127.0.0.1', {self.port}), 3)\n    print('direct')\n"
                 "except OSError:\n    print('blocked')\n")
        r = sb.run([sys.executable, "-c", probe], root=self.root, net="allow", allow=[f"127.0.0.1:{self.port}"],
                   capture_output=True, text=True, timeout=60)
        self.assertEqual(r.stdout.strip(), "blocked")

    def test_non_global_addresses_need_their_port_named(self):
        cgnat = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("100.100.100.200", 443))]
        with mock.patch.object(sb.socket, "getaddrinfo", return_value=cgnat):
            self.assertFalse(sb.vet("meta.example", 443, ["*.example"])[0])
            self.assertTrue(sb.vet("meta.example", 443, ["meta.example:443"])[0])
        both = [(socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("::1", 80, 0, 0)),
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 80))]
        with mock.patch.object(sb.socket, "getaddrinfo", return_value=both):  # ::1 sits in ::/8, Python's "reserved"
            self.assertEqual(sb.vet("localhost", 80, ["localhost:80"]), (True, "", ["::1", "127.0.0.1"]))
            self.assertFalse(sb.vet("localhost", 80, ["localhost"])[0], "loopback still needs its port named")

    def test_a_malformed_request_gets_400_not_a_crash(self):
        bad = ("import os, socket\nfrom urllib.parse import urlsplit\nu = urlsplit(os.environ['HTTP_PROXY'])\n"
               "s = socket.create_connection((u.hostname, u.port), 10)\n"
               "s.sendall(b'GET http://github.com:99999/ HTTP/1.1\\r\\n\\r\\n')\nprint(s.recv(64).split(b'\\r\\n')[0].decode())\n")
        r = sb.run([sys.executable, "-c", bad], root=self.root, net="allow", allow=["github.com"],
                   capture_output=True, text=True, timeout=60)
        self.assertIn("400", r.stdout)
        self.assertNotIn("Traceback", r.stderr)

    def test_matching_rules(self):
        self.assertTrue(sb.allowed("pypi.org", 443, ["pypi.org"]))
        self.assertTrue(sb.allowed("files.pythonhosted.org", 443, ["*.pythonhosted.org"]))
        self.assertFalse(sb.allowed("evilpypi.org", 443, ["pypi.org"]))
        self.assertFalse(sb.allowed("pypi.org", 22, ["pypi.org:443"]))
        self.assertTrue(sb.allowed("github.com", 22, ["github.com"]), "a host with no port: any port")


class SessionTier(ForemanTestCase):
    """Step 4: sampo sandbox on --session turns on Claude Code's own sandbox for the user's sessions, and off puts the
    settings back as they were."""

    def setUp(self):
        super().setUp()
        self.cfg = os.path.join(self.tmp, "cc")
        os.makedirs(self.cfg)
        self.settings = os.path.join(self.cfg, "settings.json")
        self.before = '{\n  "theme": "dark",\n  "permissions": {"allow": ["Bash(ls)"]}\n}\n'
        with open(self.settings, "w") as f:
            f.write(self.before)
        self.env = {"CLAUDE_CONFIG_DIR": self.cfg}

    def read(self):
        with open(self.settings) as f:
            return f.read()

    def test_on_writes_claude_codes_sandbox_and_keeps_the_rest(self):
        self.fm("sandbox", "on", "--session", env=self.env)
        s = json.loads(self.read())
        self.assertEqual((s["theme"], s["permissions"]), ("dark", {"allow": ["Bash(ls)"]}))
        box = s["sandbox"]
        self.assertTrue(box["enabled"])
        self.assertIn("~/.ssh", box["filesystem"]["denyRead"])
        self.assertIn("~/.config/sampo", box["filesystem"]["denyRead"])
        self.assertIn("git push *", box["excludedCommands"])
        self.assertIn("sampo ship *", box["excludedCommands"])
        self.assertIn("github.com", box["network"]["allowedDomains"])
        self.assertIn("✓ session", self.fm("sandbox", "status", env=self.env).stdout)

    def test_off_puts_the_file_back_byte_for_byte(self):
        self.fm("sandbox", "on", "--session", env=self.env)
        self.fm("sandbox", "on", "--session", env=self.env)  # twice: the backup is still the first one
        self.fm("sandbox", "off", "--session", env=self.env)
        self.assertEqual(self.read(), self.before)
        self.assertIn("· session", self.fm("sandbox", "status", env=self.env).stdout)

    def test_off_keeps_what_the_user_changed_since(self):
        self.fm("sandbox", "on", "--session", env=self.env)
        s = json.loads(self.read())
        s["model"] = "opus"
        with open(self.settings, "w") as f:
            json.dump(s, f)
        self.fm("sandbox", "off", "--session", env=self.env)
        s = json.loads(self.read())
        self.assertEqual((s.get("model"), "sandbox" in s), ("opus", False))

    def test_an_edit_between_two_ons_survives_off(self):
        self.fm("sandbox", "on", "--session", env=self.env)
        s = json.loads(self.read())
        s["model"] = "opus"
        with open(self.settings, "w") as f:
            json.dump(s, f)
        self.fm("sandbox", "on", "--session", env=self.env)
        self.fm("sandbox", "off", "--session", env=self.env)
        s = json.loads(self.read())
        self.assertEqual((s.get("model"), s.get("theme"), "sandbox" in s), ("opus", "dark", False))

    def test_on_merges_into_the_users_own_sandbox_keys_and_off_restores_them(self):
        before = json.dumps({"theme": "dark", "sandbox": {"excludedCommands": ["docker *"],
                                                           "filesystem": {"allowWrite": ["~/.kube"]}}}, indent=2) + "\n"
        with open(self.settings, "w") as f:
            f.write(before)
        self.fm("sandbox", "on", "--session", env=self.env)
        box = json.loads(self.read())["sandbox"]
        self.assertIn("docker *", box["excludedCommands"])
        self.assertIn("git push *", box["excludedCommands"])
        self.assertEqual(box["filesystem"]["allowWrite"], ["~/.kube"])
        self.assertIn("~/.ssh", box["filesystem"]["denyRead"])
        self.fm("sandbox", "off", "--session", env=self.env)
        self.assertEqual(self.read(), before)

    def test_a_linked_settings_file_stays_a_link(self):
        real = os.path.join(self.tmp, "dotfiles", "settings.json")
        os.makedirs(os.path.dirname(real))
        os.replace(self.settings, real)
        os.symlink(real, self.settings)
        self.fm("sandbox", "on", "--session", env=self.env)
        self.assertTrue(os.path.islink(self.settings))
        self.assertIn('"sandbox"', self.read())
        self.fm("sandbox", "off", "--session", env=self.env)
        self.assertTrue(os.path.islink(self.settings))
        self.assertEqual(self.read(), self.before)

    def test_doctor_names_each_layer(self):
        from sampo import doctor
        r = doctor.check_sandbox()
        self.assertEqual(r.status, "PASS")
        for layer in ("job", "session", "landlock"):
            self.assertIn(layer, r.detail)


@unittest.skipUnless(OK, f"no job sandbox here: {WHY}")
class SandboxedTests(ForemanTestCase):
    """Step 5: run.py --sandbox runs each test class in the job tier: the repo read-only, only the class's own temp
    folder writable, no network."""

    def test_a_class_runs_green_inside_and_cannot_touch_the_repo(self):
        import run
        here = os.path.dirname(os.path.abspath(run.__file__))
        tmp = os.path.join(self.tmp, "cls")
        os.makedirs(tmp)
        a, env = run.sandboxed([sys.executable, "-c", "open('../../probe.txt', 'w')"], tmp, dict(os.environ, TMPDIR=tmp))
        self.assertIn("--unshare-net", a)
        self.assertEqual(env["TMPDIR"], tmp)
        r = subprocess.run(a, cwd=here, env=env, capture_output=True, text=True, timeout=60)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(os.path.join(here, "..", "..", "probe.txt")))
        p = subprocess.run([sys.executable, "run.py", "--sandbox", "test_ci_annotations"], cwd=here,
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(p.returncode, 0, p.stderr[-800:])


@unittest.skipUnless(OK, f"no job sandbox here: {WHY}")
class Hardening(ForemanTestCase):
    """The T-3222 review's findings: each way a job could reach past its sandbox, closed."""

    def setUp(self):
        super().setUp()
        self.root = os.path.join(self.tmp, "proj")
        self.fake = os.path.join(self.tmp, "home")
        os.makedirs(os.path.join(self.fake, ".ssh"))
        with open(os.path.join(self.fake, ".ssh", "id_rsa"), "w") as f:
            f.write("SECRET-KEY")
        os.makedirs(self.root)
        subprocess.run(["git", "init", "-q", self.root], check=True)

    def sh(self, script, **kw):
        kw.setdefault("home", self.fake)
        return sb.run(["sh", "-c", script], root=self.root, capture_output=True, text=True, timeout=60, **kw)

    def test_a_job_cannot_plant_what_runs_outside_it_later(self):
        self.sh("echo evil > .git/hooks/pre-commit; git config core.fsmonitor evil; mkdir -p .claude; "
                "echo '{}' > .claude/settings.json; echo ok > work.txt")
        self.assertFalse(os.path.exists(os.path.join(self.root, ".git", "hooks", "pre-commit")))
        with open(os.path.join(self.root, ".git", "config")) as f:
            self.assertNotIn("fsmonitor", f.read())
        self.assertFalse(os.path.exists(os.path.join(self.root, ".claude", "settings.json")))
        self.assertTrue(os.path.exists(os.path.join(self.root, "work.txt")), "ordinary work still lands")
        r = self.sh("git -c user.email=a@b -c user.name=a commit -q --allow-empty -m x && git log --oneline | wc -l")
        self.assertEqual(r.stdout.strip(), "1", r.stderr)

    def test_what_the_project_lacks_cant_be_created_and_leaves_no_trace(self):
        import shutil
        shutil.rmtree(os.path.join(self.root, ".git", "hooks"))  # a clone made with an empty template has none
        self.sh("mkdir -p .git/hooks .vscode; echo evil > .git/hooks/pre-commit; echo '{}' > .vscode/tasks.json; "
                "echo 'export X=1' > .envrc; echo '{}' > .mcp.json; echo ok > work.txt")
        for rel in (".git/hooks", ".vscode", ".envrc", ".mcp.json", ".claude"):
            self.assertFalse(os.path.lexists(os.path.join(self.root, rel)), f"{rel} is gone after the job")
        self.assertTrue(os.path.exists(os.path.join(self.root, "work.txt")))

    def test_git_dirs_cant_be_swapped_and_submodules_and_nested_repos_are_guarded_too(self):
        mod = os.path.join(self.root, ".git", "modules", "sub")
        os.makedirs(os.path.join(mod, "hooks"))
        for f in ("config", "HEAD"):
            open(os.path.join(mod, f), "w").close()
        nested = os.path.join(self.root, "vendor", "lib")
        os.makedirs(nested)
        subprocess.run(["git", "init", "-q", nested], check=True)
        self.sh("mv .git .git-old; echo evil > .git/modules/sub/hooks/pre-commit; "
                "echo evil > vendor/lib/.git/hooks/pre-commit; git -C vendor/lib config core.fsmonitor evil; "
                "mv vendor/lib/.git vendor/lib/.git-old; echo ok > work.txt")
        self.assertFalse(os.path.exists(os.path.join(self.root, ".git-old")))
        self.assertTrue(os.path.isfile(os.path.join(self.root, ".git", "HEAD")), "the repo is still there")
        self.assertFalse(os.path.exists(os.path.join(mod, "hooks", "pre-commit")))
        self.assertFalse(os.path.exists(os.path.join(nested, ".git", "hooks", "pre-commit")))
        self.assertFalse(os.path.exists(os.path.join(nested, ".git-old")))
        with open(os.path.join(nested, ".git", "config")) as f:
            self.assertNotIn("fsmonitor", f.read())
        self.assertTrue(os.path.exists(os.path.join(self.root, "work.txt")))
        r = self.sh("git -c user.email=a@b -c user.name=a commit -q --allow-empty -m x && git log --oneline | wc -l")
        self.assertEqual(r.stdout.strip(), "1", r.stderr)

    def test_masks_follow_the_real_home_whatever_home_says(self):
        import types
        elsewhere = os.path.join(self.tmp, "elsewhere")
        os.makedirs(elsewhere)
        with mock.patch.object(sb.pwd, "getpwuid", return_value=types.SimpleNamespace(pw_dir=self.fake)), \
                mock.patch.dict(os.environ, {"HOME": elsewhere}):
            r = self.sh(f"cat {self.fake}/.ssh/id_rsa", home=None)
        self.assertNotIn("SECRET", r.stdout)

    def test_roots_that_would_open_the_home_or_the_system_are_refused(self):
        for root in ("/", self.fake, os.path.dirname(self.fake)):
            with self.subTest(root=root), self.assertRaises(ValueError):
                sb.argv(["true"], root, home=self.fake)

    def test_sampo_inside_a_job_keeps_its_state_read_only_instead_of_copying_it(self):
        env = sb.job_env({"PATH": "/usr/bin", "TMPDIR": "/x"}, self.root)
        self.assertEqual(env["FOREMAN_STATE_FALLBACK"], "0")
        self.assertIn("--disable-userns", sb.argv(["true"], self.root, home=self.fake))
        self.assertNotIn("--disable-userns", sb.argv(["true"], self.root, home=self.fake, nest=True))

    def test_run_together_secret_names_leave_too(self):
        for name in ("PGPASSWORD", "MYSQL_PWD", "NGROK_AUTHTOKEN", "DB_PASSPHRASE", "GITHUB_TOKEN", "LLM_API_KEY"):
            self.assertTrue(sb.secret(name), name)
        for name in ("PATH", "HOME", "PWD", "OLDPWD", "KEYBOARD_LAYOUT", "GIT_AUTHOR_NAME", "TERM"):
            self.assertFalse(sb.secret(name), name)


def _image():
    """A small image already on this machine (nothing is pulled), or None."""
    import shutil
    if not shutil.which("docker"):
        return None
    for name in ("alpine:latest", "busybox:latest"):
        try:
            if subprocess.run(["docker", "image", "inspect", name], capture_output=True, timeout=20).returncode == 0:
                return name
        except (OSError, subprocess.TimeoutExpired):
            return None
    return None


class Image(ForemanTestCase):
    """Criterion 3's other half: --image runs the job in docker instead, never by default."""

    def test_the_docker_argv_drops_everything_it_can(self):
        a = sb.docker_argv(["true"], self.tmp, "alpine:latest")
        for part in (["--network", "none"], ["--cap-drop", "ALL"], ["--security-opt", "no-new-privileges"],
                     ["--user", f"{os.getuid()}:{os.getgid()}"], ["--read-only"], ["--rm"]):
            with self.subTest(part=part):
                self.assertTrue(any(a[i:i + len(part)] == part for i in range(len(a))), a)
        self.assertFalse(any("docker.sock" in x for x in a))
        self.assertIn("bridge", sb.docker_argv(["true"], self.tmp, "alpine:latest", net="on"))
        with self.assertRaises(ValueError):
            sb.docker_argv(["true"], self.tmp, "alpine:latest", net="allow")

    @unittest.skipUnless(_image(), "no docker or no small image on this machine (nothing is pulled)")
    def test_an_image_job_writes_only_its_root_with_no_network(self):
        root = os.path.join(self.tmp, "proj")
        os.makedirs(root)
        r = sb.run(["sh", "-c", f"echo hi > {root}/x.txt; touch /etc/x 2>/dev/null || echo ro; "
                    "wget -q -T 3 -O- http://1.1.1.1 >/dev/null 2>&1 || echo offline"], root=root, image=_image(),
                   capture_output=True, text=True, timeout=120)
        self.assertEqual(r.stdout.split(), ["ro", "offline"], r.stderr)
        self.assertTrue(os.path.exists(os.path.join(root, "x.txt")))


class Fallback(ForemanTestCase):
    def test_without_a_sandbox_a_job_runs_plain_only_when_its_caller_says_so(self):
        target = os.path.join(self.tmp, "plain.txt")
        with mock.patch.object(sb, "available", return_value=(False, "no bwrap on PATH")):
            with self.assertRaises(sb.Unavailable) as e:
                sb.run(["sh", "-c", f"echo x > {target}"], root=self.tmp)
            self.assertIn("no bwrap", str(e.exception))
            self.assertFalse(os.path.exists(target))
            self.assertEqual(sb.run(["sh", "-c", f"echo x > {target}"], root=self.tmp, fallback=True).returncode, 0)
        self.assertTrue(os.path.exists(target))

    def test_available_says_why_when_bwrap_is_missing(self):
        with mock.patch.object(sb.shutil, "which", return_value=None):
            sb.available.cache_clear()
            self.addCleanup(sb.available.cache_clear)
            ok, why = sb.available()
        self.assertFalse(ok)
        self.assertIn("bwrap", why)


if __name__ == "__main__":
    unittest.main()
