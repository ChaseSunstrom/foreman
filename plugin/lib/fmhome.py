"""fm home export / import (T-1665): Foreman's state (tasks, decisions, research, settings) as one tarball without secrets,
checked on import into an empty home.

Export walks the state folder and tui.toml: every text file goes in with fmcore.redact applied; credential-shaped names,
binary files (they can't be redacted), sensitive projects, caches, live-process files and grants (trust.json) stay out,
each named in the output. MANIFEST.json lists each member's sha256 and size.

Import reads the headers first and refuses the whole file on any member that isn't a regular file, whose name is
absolute, has a `..` (or `.`, an empty part, a backslash) or lands outside state/ and tui.toml, that the manifest doesn't
list (or lists with another size), or a manifest entry with no member. Contents are then unpacked into a staging folder
and hashed; one mismatch removes the staging folder and refuses. Only then are the files moved in, and only into a home
without projects or a tui.toml. The manifest checks integrity, not origin: anyone can write a matching one."""
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import tarfile
import tempfile
import zlib

import fmcore as c
import fmcli

FORMAT = "foreman-home/1"
MANIFEST = "MANIFEST.json"
# an import's bounds per member, in all and in count (a gzip bomb stops here); export leaves out files over MAX_FILE
MAX_FILE, MAX_TOTAL, MAX_MEMBERS = 256 << 20, 4 << 30, 500_000
# top-level state folders that are caches, live processes or saved work trees, not state worth moving
_SKIP_DIRS = {"outputs", "snapshots", "lib-sources", "research-cache", "bus", "children", "agent-sessions"}
_SKIP_FILES = {"trust.json", "install-manifest.json", c._STATE_MARKER}  # grants and this machine's install stay here
_EPHEMERAL = re.compile(r"\.(?:lock|pid|sock|tmp)$")
_CRED = re.compile(r"(?i)(?:^|/)(?:\.env(?:\.[^/]*)?|[^/]*\.(?:pem|key|p12|pfx|jks|keystore)|id_(?:rsa|dsa|ecdsa|ed25519)"
                   r"[^/]*|\.netrc|\.npmrc|\.pypirc|\.git-credentials|[^/]*(?:credential|secret|token|passw)[^/]*)$")


def _sensitive(project_dir):
    try:
        with open(os.path.join(project_dir, "meta.json"), encoding="utf-8") as f:
            return bool(json.load(f).get("sensitive"))
    except (OSError, ValueError, AttributeError):
        return True  # unreadable meta: treat as sensitive, it stays out


def _candidates(state):
    """(member name, path) for each file worth exporting, and (name, why) for each one left out."""
    files, left = [], []
    for d, dirs, names in os.walk(state):
        rel = os.path.relpath(d, state)
        rel = "" if rel == "." else rel.replace(os.sep, "/") + "/"
        for sub in sorted(dirs):
            why = ("a cache or live-process folder" if not rel and sub in _SKIP_DIRS else
                   "a link" if os.path.islink(os.path.join(d, sub)) else
                   "a sensitive project (fm sensitive on)" if rel == "projects/" and _sensitive(os.path.join(d, sub))
                   else None)
            if why:
                dirs.remove(sub)
                left.append((f"state/{rel}{sub}/", why))
        for n in sorted(names):
            name, path = f"state/{rel}{n}", os.path.join(d, n)
            why = ("a link" if os.path.islink(path) or not os.path.isfile(path) else
                   "credential-shaped name" if _CRED.search(name) else
                   "grants or install record" if not rel and n in _SKIP_FILES else
                   "lock or temp file" if _EPHEMERAL.search(n) else None)
            (left.append((name, why)) if why else files.append((name, path)))
    return files, left


def export(out):
    state, tui = c.state_dir(), os.path.join(c.foreman_home(), "tui.toml")
    out = os.path.abspath(out)
    if os.path.realpath(out).startswith(os.path.realpath(state).rstrip("/") + "/"):
        raise fmcli.UsageError(f"--out {out} is inside the state folder it exports; write it elsewhere")
    if os.path.lexists(out):
        raise fmcli.UsageError(f"{out} exists; remove it or pick another --out")
    files, left = _candidates(state)
    if os.path.isfile(tui) and not os.path.islink(tui):
        files.append(("tui.toml", tui))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(out), prefix=".fm-home-", suffix=".tmp")  # 0600: it's personal data
    manifest = {"format": FORMAT, "exported": c.now(), "files": {}, "left_out": []}
    try:
        with os.fdopen(fd, "wb") as raw, tarfile.open(fileobj=raw, mode="w:gz") as t:
            for name, path in files:
                try:
                    if os.path.getsize(path) > MAX_FILE:
                        left.append((name, f"over {MAX_FILE >> 20} MB"))
                        continue
                    with open(path, "rb") as f:
                        text = f.read().decode("utf-8")
                except UnicodeDecodeError:
                    left.append((name, "binary (can't be redacted)"))
                    continue
                except OSError as e:
                    left.append((name, f"unreadable ({e.strerror})"))
                    continue
                data = c.redact(text).encode("utf-8")
                if len(data) > MAX_FILE:
                    left.append((name, f"over {MAX_FILE >> 20} MB"))
                    continue
                _add(t, name, data)
                manifest["files"][name] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
            manifest["left_out"] = [{"path": n, "why": w} for n, w in left]
            _add(t, MANIFEST, json.dumps(manifest, indent=1, sort_keys=True).encode("utf-8"))
        os.replace(tmp, out)
    except BaseException:
        os.unlink(tmp)
        raise
    return manifest


def _add(t, name, data):
    info = tarfile.TarInfo(name)
    info.size, info.mode, info.mtime = len(data), 0o600, int(datetime.datetime.now().timestamp())
    t.addfile(info, io.BytesIO(data))


class Refused(Exception):
    pass


def _check_name(m):
    n = m.name
    if not m.isfile():
        kind = "link" if m.issym() or m.islnk() else "folder" if m.isdir() else "special file"
        raise Refused(f"{n!r} is a {kind}; only regular files are imported")
    parts = n.split("/")
    if (n.startswith("/") or "\\" in n or "\0" in n or any(p in ("", ".", "..") for p in parts)
            or not (n in (MANIFEST, "tui.toml") or parts[0] == "state" and len(parts) > 1)):
        raise Refused(f"{n!r} would land outside the home's state/ and tui.toml (absolute, `..` or a stray name)")


def _verified(t):
    """The manifest and members, every header checked against it before any content is read."""
    members, seen = [], set()
    for m in t:  # one at a time, so a million-member archive stops at the cap, not after all of it is listed
        members.append(m)
        if len(members) > MAX_MEMBERS:
            raise Refused(f"over {MAX_MEMBERS} members")
        _check_name(m)
        if m.name in seen:
            raise Refused(f"{m.name!r} appears twice")
        seen.add(m.name)
    man_m = next((m for m in members if m.name == MANIFEST), None)
    if man_m is None or man_m.size > MAX_FILE:
        raise Refused(f"no {MANIFEST}: not an fm home export")
    try:
        manifest = json.loads(t.extractfile(man_m).read())
        files = manifest["files"]
        if manifest.get("format") != FORMAT or not isinstance(files, dict):
            raise ValueError(manifest.get("format"))
        sizes = {n: int(e["size"]) for n, e in files.items()}
        hashes = {n: str(e["sha256"]) for n, e in files.items()}
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        raise Refused(f"{MANIFEST} isn't an fm home manifest ({FORMAT}): {e}")
    body = [m for m in members if m.name != MANIFEST]
    for m in body:
        if m.name not in sizes:
            raise Refused(f"{m.name!r} isn't in the manifest")
        if m.size != sizes[m.name] or m.size > MAX_FILE:
            raise Refused(f"{m.name!r} is {m.size} bytes; the manifest says {sizes[m.name]} (cap {MAX_FILE >> 20} MB)")
    missing = sorted(set(sizes) - {m.name for m in body})
    if missing:
        raise Refused(f"the manifest lists {len(missing)} file(s) the archive lacks, e.g. {missing[0]!r}")
    if sum(m.size for m in body) > MAX_TOTAL:
        raise Refused(f"over {MAX_TOTAL >> 30} GB unpacked")
    return body, hashes


def _empty(state, tui):
    projects = os.path.join(state, "projects")
    return not os.path.lexists(tui) and not (os.path.isdir(projects) and os.listdir(projects))


def import_(path):
    home, state = c.foreman_home(), c.state_dir()
    tui = os.path.join(home, "tui.toml")
    if not _empty(state, tui):
        raise Refused(f"{home} isn't empty (it has projects or a tui.toml); import goes into an empty home only")
    try:
        t = tarfile.open(path, "r:gz")
    except (OSError, tarfile.TarError) as e:
        raise Refused(f"{path} isn't a gzip tarball: {e}")
    os.makedirs(state, mode=0o700, exist_ok=True)
    stage = tempfile.mkdtemp(dir=state, prefix=".fm-home-import-")
    try:
        with t:
            try:
                body, hashes = _verified(t)
                for m in body:
                    data = t.extractfile(m).read(MAX_FILE + 1)
                    if hashlib.sha256(data).hexdigest() != hashes[m.name]:
                        raise Refused(f"{m.name!r}: its sha256 hash doesn't match the manifest (changed after export)")
                    dest = os.path.join(stage, *m.name.split("/"))
                    os.makedirs(os.path.dirname(dest), mode=0o700, exist_ok=True)
                    with open(dest, "xb") as f:
                        f.write(data)
            except (tarfile.TarError, EOFError, zlib.error) as e:
                raise Refused(f"{path} is truncated or corrupt: {e}")
        if not _empty(state, tui):  # another process filled it while this one checked
            raise Refused(f"{home} stopped being empty during the import")
        moved = 0
        for d, _, names in os.walk(stage):
            for n in names:
                src = os.path.join(d, n)
                rel = os.path.relpath(src, stage).split(os.sep)
                dest = tui if rel == ["tui.toml"] else os.path.join(state, *rel[1:])
                if os.path.lexists(dest) and rel[:2] != ["state", "projects"]:
                    continue  # a home-wide file fm wrote on its way in (events, ledger): the live one stays
                os.makedirs(os.path.dirname(dest), mode=0o700, exist_ok=True)
                os.replace(src, dest)
                moved += 1
        return moved, len(body)
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def cmd_home(args):
    if args.action == "export":
        out = args.out or args.file or f"foreman-home-{datetime.date.today().isoformat()}.tar.gz"
        m = export(out)
        print(f"Exported {len(m['files'])} file(s) to {os.path.abspath(out)} (secrets redacted; a hash per file in "
              f"{MANIFEST}).")
        if m["left_out"]:
            print(f"Left out {len(m['left_out'])}:")
            for e in m["left_out"][:40]:
                print(f"  {e['path']} — {e['why']}")
            if len(m["left_out"]) > 40:
                print(f"  … and {len(m['left_out']) - 40} more (listed in {MANIFEST})")
        return 0
    if not args.file:
        raise fmcli.UsageError("fm home import FILE: the tarball fm home export wrote")
    try:
        moved, total = import_(args.file)
    except Refused as e:
        print(f"fm home import: refused, nothing imported: {e}")
        return 1
    print(f"Imported {moved} of {total} file(s) into {c.foreman_home()} (every hash matched its manifest)."
          + (f" {total - moved} kept as this home already had them." if moved < total else ""))
    return 0
