"""T-3279: sampo repro builds the generated files (the site from site/build.py, the README figures from
demo/readme_figures.py) twice from the working tree and once from a git worktree of REF, then names the files that
differ: nondeterministic (the two working-tree builds differ) and changed (the working tree's build differs from REF's).
Exit 1 only when a build is nondeterministic; a builder or a REF that can't build exits 2. Every build runs in a copy of
the tree, so the user's own files are never written; the REF worktree and the copies are removed after the run."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

from sampo import core as c

# (script, args...) run with a copy of the tree as cwd; "{out}" is a fresh folder outside the copy (the site's OUT)
BUILDERS = [["site/build.py", "{out}"], ["demo/readme_figures.py"]]
BUILD_TIMEOUT = 900  # seconds per builder
GIT_TIMEOUT = 120


class ReproError(Exception):
    """A build or a REF that can't be built: exit 2, which is not the nondeterminism exit 1."""


def _git(root, *args, check=True):
    try:
        p = subprocess.run(["git", "-C", root, *args], capture_output=True, timeout=GIT_TIMEOUT)
    except subprocess.TimeoutExpired:
        if check:  # a hung git is not "nondeterministic": exit 2, and the cleanup still runs
            raise ReproError(f"git {' '.join(args[:2])} timed out after {GIT_TIMEOUT} s")
        return subprocess.CompletedProcess(args, 1, b"", b"timed out")
    if check and p.returncode != 0:
        raise ReproError(f"git {' '.join(args[:2])} failed: {p.stderr.decode('utf-8', 'replace').strip()[-300:]}")
    return p


def _digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root):
    """{relative path: digest} of the files under root; a symlink is its target text and is never followed."""
    out = {}
    for dp, dns, fns in os.walk(root):
        for name in dns + fns:
            full = os.path.join(dp, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if os.path.islink(full):
                out[rel] = "link:" + os.readlink(full)
            elif os.path.isfile(full):
                out[rel] = _digest(full)
    return out


def diff_trees(a, b):
    """The relative paths only in b (added), only in a (removed) and in both with other contents (changed)."""
    sa, sb = snapshot(a), snapshot(b)
    return {"added": sorted(set(sb) - set(sa)), "removed": sorted(set(sa) - set(sb)),
            "changed": sorted(p for p in set(sa) & set(sb) if sa[p] != sb[p])}


def _names(d):
    return sorted(set(d["added"]) | set(d["removed"]) | set(d["changed"]))


def stage(src, dst):
    """Copy the tracked and the untracked, not ignored, files of src into dst; a symlink stays a symlink."""
    listed = _git(src, "ls-files", "-co", "--exclude-standard", "-z").stdout
    for rel in listed.decode("utf-8", "surrogateescape").split("\0"):
        p, q = os.path.join(src, rel), os.path.join(dst, rel)
        if not rel or not (os.path.isfile(p) or os.path.islink(p)):  # a deleted but still indexed file, a submodule
            continue
        os.makedirs(os.path.dirname(q), exist_ok=True)
        if os.path.islink(p):
            os.symlink(os.readlink(p), q)
        else:
            shutil.copyfile(p, q)


def _run_builder(argv, tree, site):
    cmd = [sys.executable, *(site if a == "{out}" else a for a in argv)]
    try:
        p = subprocess.run(cmd, cwd=tree, capture_output=True, timeout=BUILD_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise ReproError(f"{' '.join(argv)} ran past {BUILD_TIMEOUT} s")
    if p.returncode != 0:
        tail = p.stderr.decode("utf-8", "replace").strip()[-400:]
        raise ReproError(f"{' '.join(argv)} exited {p.returncode}: {tail}")


def _gone_diff(a, b):
    """The paths that one build removed and the other did not (a removal is a change too)."""
    return sorted(set(a) ^ set(b))


def build(src, out, builders):
    """Build src's generated files into the fresh folder out: a file a builder added or changed keeps its path, and the
    site's output goes under built-site/. Only those files are compared, not the sources that were already there.
    Returns the staged paths the builders removed (readme_figures deletes orphan SVGs)."""
    work = tempfile.mkdtemp()
    try:
        tree, site = os.path.join(work, "tree"), os.path.join(work, "site")
        os.mkdir(tree)
        stage(src, tree)
        before = snapshot(tree)
        for argv in builders:
            _run_builder(argv, tree, site)
        after = snapshot(tree)
        gone = sorted(p for p in before if p not in after)
        os.makedirs(out)
        for rel, digest in after.items():
            if before.get(rel) == digest:
                continue
            q = os.path.join(out, rel)
            os.makedirs(os.path.dirname(q), exist_ok=True)
            src_file = os.path.join(tree, rel)
            if os.path.islink(src_file):
                os.symlink(os.readlink(src_file), q)
            else:
                shutil.copyfile(src_file, q)
        if os.path.isdir(site):
            shutil.copytree(site, os.path.join(out, "built-site"), symlinks=True)
        return gone
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run(root, ref="HEAD", builders=None):
    """{"nondeterministic": [...], "changed": [...]} for the tree at root against REF."""
    builders = BUILDERS if builders is None else builders
    if ref.startswith("-"):
        raise ReproError(f"{ref!r} is not a commit")
    sha = _git(root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False).stdout.decode().strip()
    if not sha:
        raise ReproError(f"no commit {ref!r} in {root}")
    work = tempfile.mkdtemp()
    try:
        first, second, ref_out = (os.path.join(work, n) for n in ("first", "second", "ref"))
        gone1 = build(root, first, builders)
        gone2 = build(root, second, builders)
        nondet = set(_names(diff_trees(first, second))) | set(_gone_diff(gone1, gone2))
        ref_tree = os.path.join(work, "ref-tree")
        _git(root, "worktree", "add", "--detach", ref_tree, sha)
        try:
            gone_ref = build(ref_tree, ref_out, builders)
        finally:
            _git(root, "worktree", "remove", "--force", ref_tree, check=False)
            _git(root, "worktree", "prune", check=False)
        changed = set(_names(diff_trees(ref_out, first))) | set(_gone_diff(gone_ref, gone1))
        return {"nondeterministic": sorted(nondet), "changed": sorted(changed)}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def cmd(args):
    root = c.git_root(os.getcwd())
    ref = getattr(args, "ref", None) or "HEAD"
    try:
        if root is None:
            raise ReproError("not inside a git repository")
        got = run(root, ref)
    except ReproError as e:
        sys.stderr.write(f"sampo repro: {e}\n")
        return 2
    if getattr(args, "json", False):
        print(json.dumps({"ref": ref, **got}, indent=2))
    else:
        print(f"nondeterministic: {len(got['nondeterministic'])} file(s)")
        for p in got["nondeterministic"]:
            print(f"  {p}")
        print(f"changed vs {ref}: {len(got['changed'])} file(s)")
        for p in got["changed"]:
            print(f"  {p}")
    return 1 if got["nondeterministic"] else 0
