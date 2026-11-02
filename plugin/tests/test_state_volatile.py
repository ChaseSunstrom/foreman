"""T-2639: fm doctor's state-dir row warns when the state directory itself is on a volatile filesystem (tmpfs, ramfs),
wherever it is: the default, FOREMAN_STATE, or a fallback. A reboot would clear every brief and ledger."""
import os
import unittest
from unittest import mock

from helpers import ForemanTestCase  # noqa: F401  (puts plugin/lib on the path)

import fmdoctor as d


class StateVolatile(unittest.TestCase):
    def test_the_default_state_on_tmpfs_warns_naming_it(self):
        home = "/h/.claude/foreman"
        with mock.patch.object(d, "_fs_type", return_value="tmpfs"):
            r = d.check_state_dir(home, os.path.join(home, "state"))
        self.assertEqual(r.status, "WARN")
        self.assertIn("tmpfs", r.detail)
        self.assertIn("reboot", r.detail)

    def test_the_default_state_on_disk_passes(self):
        home = "/h/.claude/foreman"
        with mock.patch.object(d, "_fs_type", return_value="ext4"):
            self.assertEqual(d.check_state_dir(home, os.path.join(home, "state")).status, "PASS")

    def test_foreman_state_on_ramfs_says_so(self):
        with mock.patch.object(d, "_fs_type", return_value="ramfs"), \
                mock.patch.dict(os.environ, {"FOREMAN_STATE": "/r/state"}):
            r = d.check_state_dir("/h/.claude/foreman", "/r/state")
        self.assertEqual(r.status, "WARN")
        self.assertIn("ramfs", r.detail)
