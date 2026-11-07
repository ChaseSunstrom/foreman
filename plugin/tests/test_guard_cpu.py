"""T-3592: sampo cpu cap sets a CPU quota on the session's systemd scope, the same change a typed
systemctl --user set-property makes, so it needs the same yes (category system); the meter and the goal don't."""
from test_guard import GuardCase


class CpuCap(GuardCase):
    def test_the_cap_needs_the_system_grant_and_the_meter_does_not(self):
        self.run_table([
            ("fm cpu cap 10", "system"),
            ("fm cpu cap off", "system"),
            ("fm --json cpu cap 25", "system"),
            ("fm -p app-1a2b3c cpu cap 25", "system"),
            ("python3 /x/plugin/bin/fm cpu cap 25", "system"),
            ("fm cpu -p x cap 10", "system"),  # options after the verb don't hide the action
            ("fm cpu --project x cap 10", "system"),
            ("fm cpu --project=x cap 10", "system"),
            ("fm cpu --win 5 cap 10", "system"),
            ("fm cpu --window 5 cap 10", "system"),
            ("fm cpu -- cap 10", "system"),
            ("X=cap; fm cpu $X 10", "system"),
            ('fm cpu "ca"p 10', "system"),
            ("fm cpu $ACTION 10", "system"),  # unknown at check time
            ("fm cpu $(echo cap) 10", "system"),
            ("fm cpu", None),
            ("fm cpu --window 3 --json", None),
            ("fm cpu goal 10", None),
            ("systemctl --user set-property --runtime kitty-1-0.scope CPUQuota=160%", "system"),  # unchanged
        ], self.bash)
        self.assertIsNone(self.bash("fm cpu cap 10", allow=["system"]))
