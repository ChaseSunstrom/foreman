---
name: sandboxing
title: Sandboxing untrusted code
area: security
tags: [security, sandbox, containers, seccomp, isolation, untrusted-code]
detect: []
related: [kubernetes-security, llm-prompt-injection, ssrf, upload-security, command-injection]
---
Run untrusted code, files and tools in a disposable, unprivileged, resource-limited, network-restricted environment with no ambient credentials.

## Verify
- `docker run --rm --read-only --cap-drop=ALL --security-opt no-new-privileges --network none --pids-limit 64 --memory 256m IMAGE CMD`: the job runs with no capabilities, no network and bounded resources.
- `docker run --rm --network none IMAGE sh -c 'wget -T 2 -qO- http://example.com || echo blocked'`: egress is actually blocked.
- `docker run --rm --user 65534:65534 IMAGE id`: the process is not root.
- `pytest -q -k sandbox`: the escape-attempt tests below pass.

## Test first
Probe the boundary from inside the sandbox with harmless actions.
```python
def test_sandbox_blocks_network_fs_and_runaway(run_sandboxed):
    r = run_sandboxed("import socket; socket.create_connection(('1.1.1.1', 80), 2)")
    assert r.exit_code != 0
    r = run_sandboxed("open('/etc/shadow').read()")
    assert r.exit_code != 0
    r = run_sandboxed("open('/work/x', 'w')")        # root fs read-only
    assert r.exit_code != 0
    r = run_sandboxed("while True: pass", timeout=2)
    assert r.timed_out and r.killed
```

## Do
- Create a fresh sandbox per job and destroy it afterwards. Keep no shared state between tenants.
- Drop to a non-root numeric user, drop all capabilities, enable `no-new-privileges`, and keep the default seccomp profile (or tighten it).
- Make the root filesystem read-only and mount a small tmpfs or a single scratch directory for output.
- Disable the network, or allow only a named egress proxy with an allow-list. Block metadata endpoints.
- Set CPU, memory, process, file size and wall-clock limits, and kill on breach.
- Pass inputs as files or stdin, and pass no environment secrets, cloud credentials or host sockets.
- Use stronger isolation (gVisor, Firecracker or other microVMs) when the code is fully untrusted and multi-tenant, since containers share the host kernel.
- Validate and cap output size, and treat output as untrusted too.

## Avoid
- Mounting the Docker socket or the host root into the sandbox: that is host takeover. Mount only a scratch directory.
- `--privileged` or `--cap-add` to fix a permission error: identify the single need and handle it outside.
- Running as root "inside the container so it's fine": root plus a kernel bug is an escape. Use an unprivileged user.
- `eval`, `exec` or a language-level "safe" interpreter as a sandbox: these are not security boundaries. Use OS isolation.
- Reusing one long-lived container across users: state and files leak. Make one per job.
- Allowing metadata or internal network ranges: block them at the sandbox network.

## Review
- [ ] Non-root, no capabilities, no-new-privileges and read-only root are set.
- [ ] Network is off or allow-listed, with metadata blocked.
- [ ] CPU, memory, pids, size and time limits are enforced and tested.
- [ ] No secrets or host mounts enter the sandbox.
- [ ] Sandboxes are per job and destroyed after.
