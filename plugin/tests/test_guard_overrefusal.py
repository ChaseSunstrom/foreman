"""T-2665: three over-refusals the friction pass found: git apply's read-only flags, a sys.path literal, a bare .ssh."""
from helpers import ForemanTestCase  # noqa: F401  (puts plugin/lib on the path)
from test_guard import GuardCase


class GitApply(GuardCase):
    def test_read_only_flags_allowed_plain_apply_blocked(self):
        for flag in ("--check", "--stat", "--numstat", "--summary", "--check --stat"):
            with self.subTest(flag=flag):
                self.assertIsNone(self.bash(f"git apply {flag} x.diff", cwd=self.fhome))
        for cmd in ("git apply x.diff", "git apply --stat --apply x.diff", "git apply --check --index x.diff",
                    "git apply x.diff --check --reverse"):
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(self.bash(cmd, cwd=self.fhome), cmd)


class SysPath(GuardCase):
    LIB = "{fhome}/plugin/lib"

    def test_sys_path_literal_is_not_a_write_target(self):
        for call in ("insert(0, '%s')", "append('%s')"):
            code = "import sys; sys.path." + (call % self.LIB) + "; print(1)"
            with self.subTest(call=call):
                self.assertIsNone(self.bash(f'python3 -c "{code}"', cwd=self.repo))

    def test_heredoc_that_writes_elsewhere_is_not_refused_for_its_sys_path(self):
        # the shape the guard ledger refused 7 times: a heredoc that puts plugin/lib on sys.path and writes a scratch file
        code = ("python3 - <<'EOF'\nimport sys\nsys.path.insert(0, '%s')\nopen('%s/out.txt', 'w').write('x')\nEOF"
                % (self.LIB, "{repo}"))
        self.assertIsNone(self.bash(code, cwd=self.repo))

    def test_same_literal_opened_for_write_still_blocks(self):
        code = "import sys; sys.path.insert(0, '%s'); open('%s/x.py', 'w').write('1')" % (self.LIB, self.LIB)
        self.assertIsNotNone(self.bash(f'python3 -c "{code}"', cwd=self.repo))
        code = "import sys; sys.path.insert(0, '%s'); open('%s', 'w').write('1')" % (self.LIB, self.LIB)
        self.assertIsNotNone(self.bash(f'python3 -c "{code}"', cwd=self.repo))


class BareCredName(GuardCase):
    """T-2665: kept fail-closed. Exempting code that calls no listed read API failed open (io.FileIO, linecache and
    fileinput read a file with none of them), so a credential name beside the home folder still blocks, text test or not."""

    def test_any_credential_name_beside_home_still_blocks(self):
        for cmd in ("python3 -c \"import os; print(open(os.path.join('{home}', '.ssh', 'id_rsa')).read())\"",
                    "python3 -c \"print(open('{home}/.ssh/id_rsa').read())\"",
                    "python3 -c \"import os; os.listdir('{home}'); print('.ssh')\"",
                    "python3 -c \"import io; print(io.FileIO('{home}' + '/.ssh/' + 'id_rsa').read())\"",
                    "python3 -c \"import linecache; print(linecache.getlines('{home}' + '/.ssh/' + 'id_rsa'))\"",
                    "python3 -c \"import sys; print('.ssh' in sys.argv[0], '{home}')\""):
            with self.subTest(cmd=cmd):
                self.assertBlocked(self.bash(cmd, cwd=self.repo), "credentials")
