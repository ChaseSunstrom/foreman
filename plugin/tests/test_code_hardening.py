"""T-1432: fm code hardening. An inline --worker template that turns its CLI's approvals off is refused; more cloud metadata
endpoints (and names resolving to one) are refused; a server's odd usage counts don't crash a run; a lean claude planner
that loads more than the guard is stopped; a read from inside a worker never creates a project."""
import json
import os
import socket
import sys
import types
import unittest
from unittest import mock

from helpers import ForemanTestCase, git_repo
from test_code import CodeCase
import fmcode
import fmmodels


class InlineWorker(CodeCase):
    def test_an_inline_template_with_an_approval_off_flag_is_refused(self):
        for tpl in ("gemini --yolo {prompt}", "gemini -y -p {prompt}", "claude -p {prompt} --dangerously-skip-permissions"):
            with self.subTest(tpl=tpl):
                r = self.code("make calc.add add", "--worker", tpl, "--verify", "python3 test_calc.py", check=False)
                self.assertNotEqual(r.returncode, 0, r.stdout)
                self.assertIn("code.toml", r.stderr)
                self.assertIn("[ack]", r.stderr)
                self.assertIn("a - b", self.calc())
        self.assertEqual(fmcode.worker_argv("mycli -y {prompt}", "go", which=False), ["mycli", "-y", "go"])
        # T-1432 review: a shell wrapper's script is one word, so the flag inside it hid from the lint
        for tpl in ("sh -c 'gemini --yolo {prompt}'", "bash -lc \"claude -p {prompt} --dangerously-skip-permissions\"",
                    "env sh -c 'codex exec -a never {prompt}'"):
            with self.subTest(tpl=tpl):
                self.assertTrue(fmcode.dangerous_flags(tpl), tpl)
        self.assertEqual(fmcode.dangerous_flags("sh -c 'mycli -y {prompt}'"), [])


def model(url):
    return {"name": "x", "kind": "openai", "base_url": url, "model": "m"}


class MetadataEndpoints(unittest.TestCase):
    def addrs(self, *ips):
        return lambda host, *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443)) for ip in ips]

    def refused(self, url):
        with self.assertRaises(fmmodels.ModelError) as e:
            fmmodels.complete(model(url), [{"role": "user", "content": "hi"}], timeout=1)
        self.assertIn("metadata", str(e.exception))

    def test_alibaba_and_azure_metadata_addresses_are_refused(self):
        with mock.patch.object(socket, "getaddrinfo", side_effect=AssertionError("no lookup for an address")):
            for url in ("http://100.100.100.200/latest", "http://168.63.129.16/", "http://[::ffff:100.100.100.200]/"):
                with self.subTest(url=url):
                    self.refused(url)

    def test_a_hostname_resolving_to_a_metadata_address_is_refused(self):
        with mock.patch.object(socket, "getaddrinfo", self.addrs("10.0.0.5", "169.254.169.254")):
            self.refused("https://metadata.example.com/v1")
        with mock.patch.object(socket, "getaddrinfo", self.addrs("100.100.100.200")):
            self.refused("https://meta.example.com/v1")
        with mock.patch.object(socket, "getaddrinfo", self.addrs("10.0.0.5")):
            fmmodels._check_url({"name": "x"}, "https://models.example.com/v1", None)

    def test_a_lookup_that_fails_or_hangs_is_bounded_and_not_refused(self):
        with mock.patch.object(socket, "getaddrinfo", side_effect=socket.gaierror("no such name")):
            fmmodels._check_url({"name": "x"}, "https://nowhere.example.com/v1", None)
        import threading
        gate = threading.Event()
        with mock.patch.object(socket, "getaddrinfo", lambda *a, **k: gate.wait(30) and []), \
                mock.patch.object(fmmodels, "RESOLVE_TIMEOUT", 0.2):
            import time
            t0 = time.monotonic()
            fmmodels._check_url({"name": "x"}, "https://slow.example.com/v1", None)
            self.assertLess(time.monotonic() - t0, 5)
        gate.set()


class OddUsage(ForemanTestCase):
    def test_string_or_null_counts_count_as_zero(self):
        run = fmcode.Run(types.SimpleNamespace(), self.repo, self.tmp)
        for usage in ({"in": "12", "out": None}, {"in": None, "out": "lots"}, {"in": True, "out": [1]}, {}):
            run.usage({"usage": usage, "text": ""})
        run.usage({"usage": {"in": 3, "out": 4}, "text": ""})
        self.assertEqual(run.tokens, [3, 4])

    def test_a_cli_result_with_string_usage_reads(self):
        reply = os.path.join(self.tmp, "reply.json")
        with open(reply, "w") as f:
            json.dump({"type": "result", "result": "hi", "usage": {"input_tokens": "10", "cache_read_input_tokens": None,
                                                                   "output_tokens": "2"}}, f)
        got = fmmodels._cli({"name": "c", "kind": "cli", "argv": f"cat {reply}"}, [{"role": "user", "content": "x"}], 10)
        self.assertEqual(got["text"], "hi")
        self.assertEqual(got["usage"]["in"], 0)


class LeanPlanner(CodeCase):
    def test_a_lean_claude_planner_whose_init_lists_an_mcp_server_is_stopped(self):
        bin_ = os.path.join(self.tmp, "bin")
        os.makedirs(bin_)
        init = {"type": "system", "subtype": "init", "mcp_servers": [{"name": "evil", "status": "connected"}],
                "tools": ["Read"], "plugins": []}
        plan = {"type": "FIX", "tier": "S", "title": "t", "criteria": [{"text": "adds", "verify": "true"}], "steps": ["s"]}
        result = {"type": "result", "is_error": False, "result": json.dumps(plan), "usage": {}}
        with open(os.path.join(bin_, "claude"), "w") as f:
            f.write(f"#!/bin/sh\necho '{json.dumps(init)}'\nsleep 20\necho '{json.dumps(result)}'\n")
        os.chmod(os.path.join(bin_, "claude"), 0o755)
        import time
        t0 = time.monotonic()
        r = self.code("make calc.add add", "--worker", "claude", check=False,
                      env={"PATH": bin_ + os.pathsep + os.environ["PATH"]})
        self.assertLess(time.monotonic() - t0, 15, "stopped at its init line, not after the sleep")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("MCP server evil", r.stderr)
        self.assertIn("a - b", self.calc())


class WorkerReadCreatesNothing(ForemanTestCase):
    def test_fm_state_in_an_unregistered_folder_creates_no_project(self):
        import fmcore
        folder = git_repo(self.tmp, "other")  # a git repo fm never saw
        self.assertIsNone(fmcore.find_project(folder, create=False))
        self.fm("state", cwd=folder, check=False, env={"FOREMAN_WORKER_OF": "fm-code-T-0001"})
        self.assertIsNone(fmcore.find_project(folder, create=False))
        self.fm("state", cwd=folder, check=False)  # outside a worker, a read still sets the folder up as before
        self.assertIsNotNone(fmcore.find_project(folder, create=False))


if __name__ == "__main__":
    unittest.main()
